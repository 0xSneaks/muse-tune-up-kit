"""Six gates as hooks around a tool-call function.

    READBACK-REQUIRED  post-tool   read the target back after every write
    LEG-INVENTORY      pre-report  every planned leg has a status; DONE needs evidence
    UNKNOWN-OUTCOME    pre/post    never blind-resend a non-idempotent call
    APPROVAL-TOKEN     pre-tool    gated tools need a matching, unused owner approval
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
    approvals()          -> owner-channel records [{"id","tool","args","status"}]
"""
import json
import re

from . import claims as C
from .store import h

SECRET_PATTERNS = [
    ("api-key", re.compile(r"\b(sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[bpas]-[A-Za-z0-9-]{10,})")),
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("credential-phrase", re.compile(r"(?i)\b(password|passcode|pin|secret|api[ _-]?key|token)\b\s*(is|=|:)\s*(?=\S*\d)\S{4,}")),
    ("seed-phrase", re.compile(r"(?i)(seed phrase|mnemonic|recovery phrase)\W+(\b[a-z]{3,8}\b\W+){11,}")),
]
_CARD = re.compile(r"\b(?:\d[ -]?){13,19}\b")
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
        if 13 <= len(digits) <= 19 and _luhn(digits):
            hits.append(("card-number", m.start(), m.end()))
    return hits


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


class GatedTools:
    def __init__(self, raw_call, trace, meta, store, task_id="task", approvals=None, registry=None):
        self.raw, self.trace, self.meta, self.store = raw_call, trace, meta, store
        self.task_id, self.approvals, self.registry = task_id, approvals or (lambda: []), registry or []
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
            if a.get("status") == "approved" and a["id"] not in known:
                self.store.append("approvals.jsonl", {"id": a["id"], "key": h([a["tool"], a["args"]]), "tool": a["tool"]})

    def _find_approval(self, name, args):
        self._sync_approvals()
        used = {r["id"] for r in self.store.read("approvals_used.jsonl")}
        key = h([name, args])
        for r in self.store.read("approvals.jsonl"):
            if r["key"] == key and r["id"] not in used:
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
        if m.get("gated"):                                     # APPROVAL-TOKEN
            approval = self._find_approval(name, args)
            if approval is None:
                self._log("APPROVAL-TOKEN", "fail", leg, detail=m["gated"], action="blocked")
                return {"error": "APPROVAL-TOKEN: no unused owner approval matches this exact call",
                        "gated": m["gated"], "_gates": {"APPROVAL-TOKEN": "fail"}}
            self._log("APPROVAL-TOKEN", "pass", leg, evidence=approval["id"])

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
        if approval is not None:
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
        return {**res, "_gates": gates}

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
            if l["status"] == "DONE":
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
