"""Seven gates as hooks around a tool-call function.

    READBACK-REQUIRED  post-tool   read the target back after every write
    LEG-INVENTORY      pre-report  every planned leg has a status; DONE needs evidence
    UNKNOWN-OUTCOME    pre/post    never blind-resend a non-idempotent call
    APPROVAL-TOKEN     pre-tool    gated tools need an owner approval record: a single-use approval for the
                                   exact call, a standing grant whose scope covers it (never consumed), or a
                                   delegated approval from a named reviewer bound to a packet hash (D10)
    MASKED-VALUE       post-tool   masked values are never used as arguments; a value check ends in one of
                                   three outcomes: value-verified, presence-verified/value-unverified, blocked (D9)
    SECRET-SCAN        pre-tool    block secrets in writes, sends and reports
    STARTUP-ALIVE      session     coordination workers alive, heartbeat fresh, backlog known

Integration contract (what a real runtime must supply):
    raw_call(name, args) -> dict with "_call_id"; errors as {"error": "..."}
    trace()              -> list of {"id", "ok"} for every raw call so far
    meta[name]           -> {"effect": "read"|"write"|"send",
                             "gated": "<gate type>" (optional),
                             "nonidempotent": bool,
                             "readback": fn(raw_call, args, result) -> (ok, evidence_id, detail),
                             "state_check": fn(raw_call, args) -> (present, evidence_id)}
    approvals()          -> owner-channel records, each with "id" and "status": "approved", and one of
                            {"tool","args"}                                        single-use (default)
                            {"kind":"standing_grant","gate","scope":{"tool","args"}}  globs; never consumed
                            {"kind":"delegated_approval","gate","tool","reviewer","packet_hash"}  packet_hash = h([tool,args]); single-use
    delegates            -> reviewer ids the owner has named; a delegated approval from anyone else is ignored
"""
import fnmatch
import hashlib
import hmac
import json
import re

from . import claims as C
from .store import h

SECRET_PATTERNS = [
    ("api-key", re.compile(r"\b(sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[bpas]-[A-Za-z0-9-]{10,})")),
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("credential-phrase", re.compile(r"(?i)\b(password|passcode|pin|secret|api[ _-]?key|token)\b\s*(is|=|:)\s*(?=\S*\d)\S{4,}")),
]
# D29: a card is 13-16 digits with an issuer prefix, a valid check digit and a card word nearby.
_CARD = re.compile(r"(?<![\d-])\d(?:[ -]?\d){12,15}(?![\d])")
_ISSUER = re.compile(r"^(4|5[1-5]|2(2[2-9][1-9]|2[3-9]\d|[3-6]\d\d|7[01]\d|720)|3[47]|3(0[0-5]|[68])|6(011|5|4[4-9])|35(2[89]|[3-8]\d))")
_CARD_WORD = re.compile(r"(?i)\b(card|visa|mastercard|amex|discover|credit|debit|cvv|cvc|expiry|exp)\b")
_CARD_NEAR = 40
# D29: a seed phrase is exactly 12 or 24 lowercase words separated only by single spaces.
_SEED_SPLIT = re.compile(r"[^a-z ]+")
_SEED_WORD = re.compile(r"^[a-z]{3,8}$")
_PROSE_WORDS = frozenset("the and for you your with that this from are was were into have has not but its our their".split())
# D10: the seven gate types (the owner's approval list). A tool gated on any other type is refused.
GATE_TYPES = ("spend", "trade", "send-as-owner", "deploy", "device", "delete", "credential")
# Standing grants never cover money or credentials, whatever their scope says.
NO_STANDING = frozenset({"spend", "trade", "credential"})

# D9: what a masked value looks like, and which field names always count as secret.
_MASK = re.compile(r"(\*{4,}|\u2022{3,}|(?<![A-Za-z])[xX]{4,}(?![A-Za-z])|\w\u2026|\u2026\w|\[REDACTED\])")
_REPEAT = re.compile(r"^(.)\1{5,}$")           # a whole value that is one character repeated
_SECRET_FIELD = re.compile(r"(?i)(key|secret|token|password)$")
VALUE_VERIFIED, PRESENCE_ONLY, BLOCKED = "value-verified", "presence-verified/value-unverified", "blocked"

SUMMARY_WORDS = re.compile(r"(?i)\b(all set|all done|everything is done|everything is complete|completed all|fully complete|done and dusted)\b")


def _luhn(digits):
    total, alt = 0, False
    for d in reversed(digits):
        n = int(d)
        if alt:
            n = n * 2 - 9 if n > 4 else n * 2
        total, alt = total + n, not alt
    return total % 10 == 0


def secret_scan(text):
    """Return [(class, start, end)]. Classes only are ever logged, never values."""
    hits = [(name, m.start(), m.end()) for name, rx in SECRET_PATTERNS for m in rx.finditer(text)]
    for m in _CARD.finditer(text):
        digits = re.sub(r"\D", "", m.group())
        near = text[max(0, m.start() - _CARD_NEAR):m.end() + _CARD_NEAR]
        if 13 <= len(digits) <= 16 and _ISSUER.match(digits) and _luhn(digits) and _CARD_WORD.search(near):
            hits.append(("card-number", m.start(), m.end()))
    hits += _seed_hits(text)
    return hits


def _seed_hits(text):
    hits, pos = [], 0
    for piece in _SEED_SPLIT.split(text):
        start = text.index(piece, pos) if piece else pos
        pos = start + len(piece)
        core = piece.strip(" ")
        if not core or "  " in core:
            continue
        words = core.split(" ")
        if len(words) in (12, 24) and all(_SEED_WORD.match(w) for w in words) \
                and len(_PROSE_WORDS.intersection(words)) < 2:
            s = start + piece.index(core)
            hits.append(("seed-phrase", s, s + len(core)))
    return hits


def is_masked(value):
    return isinstance(value, str) and bool(_MASK.search(value) or _REPEAT.match(value))


def masked_paths(obj, path=""):
    """Field paths (never values) of masked values, or of any field named key/secret/token/password."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else str(k)
            if isinstance(v, (dict, list)):
                out += masked_paths(v, p)
            elif is_masked(v) or (_SECRET_FIELD.search(str(k)) and v not in (None, "")):
                out.append(p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += masked_paths(v, f"{path}[{i}]")
    elif is_masked(obj):
        out.append(path or "$")
    return out


def fingerprint(value, key):
    """Keyed fingerprint of a secret value. Only fingerprints are stored or compared, never values."""
    return hmac.new(key, value.encode(), hashlib.sha256).hexdigest()[:16]


def masked_value(observed, expected_fp=None, key=b"", probe=None):
    """D9. Returns (outcome, detail).

    observed     the value as a read returned it (masked or not), or None if nothing was there
    expected_fp  fingerprint of the value that should be there, or None if unknown
    probe        optional functional probe: {"safe": True|False|None, "fp": fingerprint of the value presented}.
                 "safe" is whether presenting the value is known not to consume or rotate it; None means
                 that could not be determined, which bars the probe.
    """
    if observed in (None, ""):
        return BLOCKED, "absent"
    if not is_masked(observed):                                   # non-masked channel
        if expected_fp is None:
            return PRESENCE_ONLY, "readable, but no expected fingerprint to compare"
        if hmac.compare_digest(fingerprint(observed, key), expected_fp):
            return VALUE_VERIFIED, "non-masked channel, fingerprint match"
        return BLOCKED, "non-masked channel, fingerprint mismatch"
    if probe is None:
        return PRESENCE_ONLY, "masked read proves presence only"
    if probe.get("safe") is not True:
        return PRESENCE_ONLY, "probe barred: consumption undeterminable" if probe.get("safe") is None \
            else "probe barred: presenting the value consumes it"
    if expected_fp is None or not probe.get("fp"):
        return PRESENCE_ONLY, "probe ran without a fingerprint to compare"
    if hmac.compare_digest(probe["fp"], expected_fp):
        return VALUE_VERIFIED, "functional probe, fingerprint match"
    return BLOCKED, "functional probe, fingerprint mismatch"


def _scope_covers(scope, name, args):
    if not fnmatch.fnmatchcase(name, scope.get("tool", "")):
        return False
    for k, pat in (scope.get("args") or {}).items():
        if k not in args or not fnmatch.fnmatchcase(str(args[k]), str(pat)):
            return False
    return True


def startup_alive(probe_rows, registry):
    """probe_rows: [{"name","alive","heartbeat_age_s","backlog"}]. Returns (ok, table)."""
    rows = {r["name"]: r for r in probe_rows}
    table, ok = [], True
    for reg in registry:
        r = rows.get(reg["name"])
        if r is None:
            state, r = "MISSING", {"heartbeat_age_s": None, "backlog": None}
        elif not r.get("alive"):
            state = "DOWN"
        elif r.get("heartbeat_age_s", 0) > reg.get("max_age_s", 600):
            state = "HUNG"
        else:
            state = "OK"
        backlog = r.get("backlog")
        if state != "OK" or (backlog or 0) > reg.get("max_backlog", 0):
            ok = False
        table.append({"name": reg["name"], "state": state, "heartbeat_age_s": r.get("heartbeat_age_s"), "backlog": backlog})
    return ok, table


def _get(obj, path):
    cur = obj
    for part in re.findall(r"[^.\[\]]+|\[\d+\]", path):
        cur = cur[int(part[1:-1])] if part.startswith("[") else cur.get(part)
        if cur is None:
            return None
    return cur


class GatedTools:
    def __init__(self, raw_call, trace, meta, store, task_id="task", approvals=None, registry=None, delegates=()):
        self.raw, self.trace, self.meta, self.store = raw_call, trace, meta, store
        self.task_id, self.approvals, self.registry = task_id, approvals or (lambda: []), registry or []
        self.delegates = frozenset(delegates)
        self.leg_masked = {}            # leg -> MASKED-VALUE outcome
        self.legs, self.leg_ev, self.leg_fail, self.leg_writes = [], {}, set(), set()
        self.call_fail = set()          # call ids whose read-back failed, for agents that do not tag legs

    # ---- log -------------------------------------------------------------
    def _log(self, gate, result, leg=None, evidence=None, detail="", action="none"):
        self.store.append("gate_log.jsonl", {"task_id": self.task_id, "leg": leg, "gate": gate, "result": result,
                                             "evidence": evidence, "detail": detail, "action": action})

    # ---- LEG-INVENTORY (plan half) ----------------------------------------
    def plan(self, legs):
        for leg in legs:
            if leg not in self.legs:
                self.legs.append(leg)
        self.store.append("inventory.jsonl", {"task_id": self.task_id, "legs": list(self.legs)})

    # ---- APPROVAL-TOKEN ---------------------------------------------------
    def _sync_approvals(self):
        known = {r["id"] for r in self.store.read("approvals.jsonl")}
        for a in self.approvals():
            if a.get("status") != "approved" or a["id"] in known:
                continue
            kind = a.get("kind", "single_use")
            if kind == "standing_grant":
                rec = {"id": a["id"], "kind": kind, "gate": a.get("gate"), "scope": a.get("scope") or {}}
            elif kind == "delegated_approval":
                rec = {"id": a["id"], "kind": kind, "gate": a.get("gate"), "tool": a.get("tool"),
                       "reviewer": a.get("reviewer"), "packet_hash": a.get("packet_hash")}
            else:
                rec = {"id": a["id"], "kind": "single_use", "key": h([a["tool"], a["args"]]), "tool": a["tool"]}
            self.store.append("approvals.jsonl", rec)

    def _find_approval(self, name, args, gate):
        """Single-use exact match first, then a delegated approval, then a standing grant."""
        self._sync_approvals()
        used = {r["id"] for r in self.store.read("approvals_used.jsonl")}
        key = h([name, args])
        recs = self.store.read("approvals.jsonl")
        for r in recs:
            if r.get("kind", "single_use") == "single_use" and r["key"] == key and r["id"] not in used:
                return r
        for r in recs:
            if r.get("kind") == "delegated_approval" and r["id"] not in used and r["gate"] == gate \
                    and r["tool"] == name and r["reviewer"] in self.delegates \
                    and r.get("packet_hash") == key:          # the reviewer signed this exact call
                return r
        if gate not in NO_STANDING:
            for r in recs:
                if r.get("kind") == "standing_grant" and r["gate"] == gate and _scope_covers(r["scope"], name, args):
                    return r
        return None

    # ---- the hook ---------------------------------------------------------
    def call(self, name, args, leg=None):
        m = self.meta.get(name, {})
        effect = m.get("effect", "read")
        if leg and leg not in self.legs:
            self.plan([leg])
        if leg and effect in ("write", "send"):
            self.leg_writes.add(leg)

        if effect in ("write", "send"):                       # SECRET-SCAN
            hits = secret_scan(json.dumps(args))
            if hits:
                classes = sorted({c for c, _, _ in hits})
                self._log("SECRET-SCAN", "fail", leg, detail=",".join(classes), action="blocked")
                return {"error": f"SECRET-SCAN: write blocked ({', '.join(classes)}); not stored", "_gates": {"SECRET-SCAN": "fail"}}

        masked_args = masked_paths(args) if name != "ask_approval" else []
        masked_args = [p for p in masked_args if is_masked(_get(args, p))]
        if masked_args:                                        # MASKED-VALUE (pre): never used as an argument
            self._block_masked(leg, f"masked value passed as argument at {', '.join(masked_args)}")
            return {"error": "MASKED-VALUE: masked value used as an argument; needs a secure route",
                    "_gates": {"MASKED-VALUE": BLOCKED}}

        if name == "ask_approval":                            # four-field ask
            for item in args.get("items", []):
                missing = [f for f in ("tool", "args", "action", "destination", "cost", "consequence") if item.get(f) in (None, "")]
                if missing:
                    self._log("APPROVAL-TOKEN", "fail", leg, detail="request missing " + ",".join(missing), action="blocked")
                    return {"error": "APPROVAL-TOKEN: request incomplete, missing " + ", ".join(missing)}
            res = self.raw(name, args)
            self._sync_approvals()
            return res

        approval = None
        if m.get("gated") and m["gated"] not in GATE_TYPES:  # APPROVAL-TOKEN: unknown type fails closed
            self._log("APPROVAL-TOKEN", "fail", leg, detail=f"unknown gate type {m['gated']}", action="blocked")
            return {"error": f"APPROVAL-TOKEN: unknown gate type {m['gated']}", "_gates": {"APPROVAL-TOKEN": "fail"}}
        if m.get("gated"):                                     # APPROVAL-TOKEN
            approval = self._find_approval(name, args, m["gated"])
            if approval is None:
                self._log("APPROVAL-TOKEN", "fail", leg, detail=m["gated"], action="blocked")
                return {"error": "APPROVAL-TOKEN: no unused owner approval matches this exact call",
                        "gated": m["gated"], "_gates": {"APPROVAL-TOKEN": "fail"}}
            self._log("APPROVAL-TOKEN", "pass", leg, evidence=approval["id"], detail=approval.get("kind", "single_use"))

        key = h([name, args])
        if m.get("nonidempotent"):                             # UNKNOWN-OUTCOME (pre)
            prior = [r for r in self.store.read("ledger.jsonl") if r["key"] == key]
            if any(r["status"] == "done" for r in prior):
                ev = next(r["evidence"] for r in prior if r["status"] == "done")
                self._log("UNKNOWN-OUTCOME", "pass", leg, evidence=ev, detail="already done; not repeated")
                self._evidence(leg, ev)
                return {"ok": True, "deduped": True, "_call_id": ev, "_gates": {"UNKNOWN-OUTCOME": "deduped"}}
            if prior:                                          # started or unknown earlier: check state first
                present, ev = self._state(m, args)
                if present:
                    return self._resolved(key, name, leg, ev)
                if present is None:
                    return self._unknown(key, name, leg, None)
            self.store.append("ledger.jsonl", {"key": key, "tool": name, "status": "started", "evidence": None})

        res = self.raw(name, args)
        if approval is not None and approval.get("kind") != "standing_grant":   # standing grants are never consumed
            self.store.append("approvals_used.jsonl", {"id": approval["id"], "call": res.get("_call_id")})

        gates = {}
        if m.get("nonidempotent"):                             # UNKNOWN-OUTCOME (post)
            if str(res.get("error", "")).startswith("timeout"):
                present, ev = self._state(m, args)
                if present:
                    return self._resolved(key, name, leg, ev)
                if present is None:                            # no independent route: never retry
                    return self._unknown(key, name, leg, res.get("_call_id"))
                res = self.raw(name, args)                     # confirmed absent: one retry
                if "error" in res:
                    return self._unknown(key, name, leg, res.get("_call_id"))
            if "error" not in res:
                self.store.append("ledger.jsonl", {"key": key, "tool": name, "status": "done", "evidence": res["_call_id"]})
                gates["UNKNOWN-OUTCOME"] = "pass"

        if effect in ("write", "send") and "error" not in res:  # READBACK-REQUIRED
            if m.get("readback"):
                ok, ev, detail = m["readback"](self.raw, args, res)
                self._log("READBACK-REQUIRED", "pass" if ok else "fail", leg, evidence=ev, detail=detail,
                          action="none" if ok else "downgraded")
                gates["READBACK-REQUIRED"] = "pass" if ok else "fail"
                res = {**res, "_readback": ev}
                if ok:
                    self._evidence(leg, ev)
                    self.leg_fail.discard(leg)
                else:
                    self.call_fail.add(res["_call_id"])
                    if leg:
                        self.leg_fail.add(leg)
            else:
                self._log("READBACK-REQUIRED", "skip", leg, detail="tool-has-no-read-path")
                gates["READBACK-REQUIRED"] = "skip"
        elif effect in ("write", "send") and leg:
            self.leg_fail.add(leg)
        tagged = masked_paths({k: v for k, v in res.items() if not k.startswith("_")})
        if tagged:                                             # MASKED-VALUE (post): tag paths, never values
            self._log("MASKED-VALUE", "tag", leg, evidence=res.get("_call_id"), detail=",".join(tagged))
            gates["MASKED-VALUE"] = "tagged"
        return {**res, "_gates": gates}

    # ---- MASKED-VALUE -------------------------------------------------------
    def _block_masked(self, leg, detail):
        self._log("MASKED-VALUE", BLOCKED, leg, detail=detail, action="blocked")
        if leg:
            self.leg_masked[leg] = BLOCKED

    def verify_value(self, leg, observed, expected_fp=None, key=b"", probe=None, evidence=None):
        """Record a D9 outcome for a leg that claims a stored value is right. Returns the outcome."""
        outcome, detail = masked_value(observed, expected_fp, key, probe)
        self._log("MASKED-VALUE", outcome, leg, evidence=evidence, detail=detail,
                  action="none" if outcome == VALUE_VERIFIED else ("blocked" if outcome == BLOCKED else "downgraded"))
        if leg:
            if leg not in self.legs:
                self.plan([leg])
            self.leg_masked[leg] = outcome
            if outcome == VALUE_VERIFIED and evidence:
                self._evidence(leg, evidence)
        return outcome

    def _evidence(self, leg, ev):
        if leg:
            self.leg_ev.setdefault(leg, []).append(ev)

    def _state(self, m, args):
        """(True|False, evidence) from an independent route; (None, None) if there is none."""
        return m["state_check"](self.raw, args) if m.get("state_check") else (None, None)

    def _unknown(self, key, name, leg, call_id):
        self.store.append("ledger.jsonl", {"key": key, "tool": name, "status": "unknown", "evidence": None})
        self._log("UNKNOWN-OUTCOME", "fail", leg, detail="state not confirmed", action="blocked")
        if leg:
            self.leg_fail.add(leg)
        return {"error": "UNKNOWN-OUTCOME: could not confirm; do not retry, check manually",
                "_call_id": call_id, "_gates": {"UNKNOWN-OUTCOME": "fail"}}

    def _resolved(self, key, name, leg, ev):
        self.store.append("ledger.jsonl", {"key": key, "tool": name, "status": "done", "evidence": ev})
        self._log("UNKNOWN-OUTCOME", "pass", leg, evidence=ev, detail="state check: present; not repeated")
        self._evidence(leg, ev)
        return {"ok": True, "resolved": "present", "_call_id": ev, "_gates": {"UNKNOWN-OUTCOME": "resolved-present"}}

    # ---- STARTUP-ALIVE ------------------------------------------------------
    def session_start(self):
        if not self.registry:
            return ""
        probe = self.raw("workers_status", {})
        ok, table = startup_alive(probe.get("workers", []), self.registry)
        self._log("STARTUP-ALIVE", "pass" if ok else "fail", evidence=probe.get("_call_id"),
                  detail=json.dumps(table), action="none" if ok else "escalated")
        if ok:
            return ""
        lines = []
        for r in table:
            if r["state"] != "OK" or r["backlog"]:
                age = "unknown" if r["heartbeat_age_s"] is None else f"{r['heartbeat_age_s'] / 3600:.1f}h"
                lines.append(f"STARTUP-ALIVE: {r['name']} is {r['state']} (last heartbeat {age} ago), backlog {r['backlog']} unread.")
        return "\n".join(lines)

    # ---- LEG-INVENTORY (pre-report half) + SECRET-SCAN on the report ----------
    def finalize(self, report):
        hits = secret_scan(report)
        for _, s, e in sorted(hits, key=lambda x: -x[1]):
            report = report[:s] + "[REDACTED]" + report[e:]
        if hits:
            self._log("SECRET-SCAN", "fail", detail="report redacted", action="downgraded")
        p = C.parse(report)
        if not self.legs and not p["legs"]:
            return report
        ok_ids = {t["id"] for t in self.trace() if t["ok"]}
        reported = {l["leg"]: l for l in p["legs"]}
        out, changed = [], []
        for name in self.legs + [n for n in reported if n not in self.legs]:
            l = dict(reported.get(name) or {"leg": name, "status": "PENDING", "evidence": "none"})
            if name not in reported:
                changed.append(f"{name}: missing from report -> PENDING")
            masked = self.leg_masked.get(name)
            if l["status"] == "DONE" and masked == BLOCKED:
                l["status"] = "BLOCKED"
                changed.append(f"{name}: DONE -> BLOCKED (masked value; needs a secure route)")
            elif l["status"] == "DONE" and masked == PRESENCE_ONLY:
                l["status"] = "PENDING"
                changed.append(f"{name}: DONE -> PENDING (presence-verified / value-unverified)")
            elif l["status"] == "DONE":
                if name in self.leg_fail or l["evidence"] in self.call_fail:
                    l["status"] = "FAILED"
                    changed.append(f"{name}: DONE -> FAILED (gate failed on this leg)")
                elif l["evidence"] not in ok_ids:
                    l["status"] = "PENDING"
                    changed.append(f"{name}: DONE -> PENDING (no valid evidence id)")
                elif name in self.leg_writes and not self.leg_ev.get(name):
                    l["status"] = "PENDING"
                    changed.append(f"{name}: DONE -> PENDING (write with no passing read-back)")
            out.append(l)
        body = p["body"]
        if any(l["status"] != "DONE" for l in out) and SUMMARY_WORDS.search(body):
            body = SUMMARY_WORDS.sub("[not all legs are done; see CLAIMS]", body)
            changed.append("summary words removed")
        self._log("LEG-INVENTORY", "fail" if changed else "pass", detail="; ".join(changed),
                  action="downgraded" if changed else "none")
        return C.render(body, out, p["claims"])
