"""Step 6 — the four ENFORCED-WRAPPER gates (SPEC-DELTA D1, MUSE-SIDE-REPORT §A1).

D1 split every check into ENFORCED-WRAPPER, ENFORCED-SNAPSHOT or AUDITED,
because the runtime has no pre-tool hook (§A1: VERIFIED). A wrapper gate is
the enforceable kind: it sits in front of a script-mediated action (a
function call in the harness, a CLI in production) and the action cannot
happen except through it. These four wrap the harness's scripted tools the
same way `muse_gates.GatedTools` wraps its raw tool function:

    LEDGER-APPEND-ONLY       a ledger/log file may only grow by append
    INVENTORY-DISTINCTNESS   (builder half) a declared inventory's sources
                             must be mechanically distinct before use
    SECRET-SCAN (send-side)  no secret leaves in an outbound payload
    MANIFEST-COMPLETE        (builder half) a manifest must cover exactly
                             the files its builder enumerated

Each wrapper logs to the same gate_log.jsonl, in the same record shape as
GatedTools._log, and a blocked call returns the same error shape
({"error": ..., "_gates": {GATE: "fail"}}) without invoking the wrapped
function. "Builder half" means the wrapper judges what the builder
*declared* (the inventory list, the file listing) at call time; whether the
declaration matches reality is the snapshot/auditor half's job, not this
one's.

API assumptions (local tree): `muse_gates.Store` (append/read) and
`muse_gates.secret_scan` (returns [(class, start, end)], classes only).
The local secret_scan predates the D29 tightening that exists on the
branch (ab4831e); this wrapper imports whatever muse_gates provides and
inherits its patterns unchanged.
"""
import json

from muse_gates import secret_scan


class _Wrapper:
    GATE = "?"

    def __init__(self, store, task_id="task"):
        self.store, self.task_id = store, task_id

    def _log(self, result, detail="", action="none"):
        self.store.append("gate_log.jsonl", {"task_id": self.task_id, "leg": None, "gate": self.GATE,
                                             "result": result, "evidence": None, "detail": detail,
                                             "action": action})

    def _blocked(self, detail):
        self._log("fail", detail=detail, action="blocked")
        return {"error": f"{self.GATE}: call blocked ({detail})", "_gates": {self.GATE: "fail"}}

    def _passed(self, detail=""):
        self._log("pass", detail=detail)


class LedgerAppendOnly(_Wrapper):
    """Wrap a file-write tool so a ledger can only ever grow by append.

    check(old, new) passes iff `new` has `old` as a prefix: appending is
    the only legal edit. Rewriting a line, truncating, or reordering all
    destroy history and are blocked. Writing a not-yet-existing file
    (old == "") always passes.
    """
    GATE = "LEDGER-APPEND-ONLY"

    def check(self, old, new):
        if new.startswith(old):
            return True, f"append of {len(new) - len(old)} chars"
        return False, "new content does not extend the existing ledger (rewrite/truncate)"

    def wrap(self, raw_write):
        """raw_write(path, text) -> result dict; the wrapped tool reads the
        current file itself, so a caller cannot pre-truncate it."""
        import os

        def wrapped(path, text):
            old = ""
            if os.path.exists(path):
                with open(path) as f:
                    old = f.read()
            ok, detail = self.check(old, text)
            if not ok:
                return self._blocked(detail)
            res = raw_write(path, text)
            if "error" not in res:
                self._passed(detail)
            return res

        return wrapped


class InventoryDistinctness(_Wrapper):
    """Builder half of INVENTORY-DISTINCTNESS.

    An inventory corroborates only if its sources are independent, and
    independence means distinct infrastructure, not just distinct names:
    two sources sharing a backend OR a counting/pagination mechanism are
    one source (common-mode failure). The declared sources collapse into
    equivalence classes under that sharing relation; the gate passes iff
    the number of classes meets `required`.
    """
    GATE = "INVENTORY-DISTINCTNESS"

    @staticmethod
    def distinct_count(sources):
        parent = list(range(len(sources)))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for i, a in enumerate(sources):
            for j, b in enumerate(sources):
                if i < j and (a.get("backend") == b.get("backend")
                              or a.get("mechanism") == b.get("mechanism")):
                    parent[find(i)] = find(j)
        return len({find(i) for i in range(len(sources))})

    def check(self, sources, required=2):
        if not sources:
            return False, "empty inventory declares no sources"
        n = self.distinct_count(sources)
        if n >= required:
            return True, f"{n} distinct source(s) from {len(sources)} declared"
        return False, (f"only {n} distinct source(s) from {len(sources)} declared "
                       f"(shared backend/mechanism collapses the rest); {required} required")

    def wrap(self, raw_call, sources_of, required=2):
        """sources_of(args) extracts the declared inventory from the call."""
        def wrapped(args):
            ok, detail = self.check(sources_of(args), required)
            if not ok:
                return self._blocked(detail)
            res = raw_call(args)
            if "error" not in res:
                self._passed(detail)
            return res

        return wrapped


class SecretScanSend(_Wrapper):
    """SECRET-SCAN, send-side: wrap an outbound send tool.

    The payload is scanned as serialized (the whole args dict, so a secret
    in any field counts). On a hit the send never happens and only the
    pattern classes are logged — never the value (same rule as
    GatedTools). Clean payloads pass through byte-identical.
    """
    GATE = "SECRET-SCAN"

    def check(self, args):
        hits = secret_scan(json.dumps(args, default=str))
        classes = sorted({c for c, _, _ in hits})
        if classes:
            return False, ",".join(classes)
        return True, "clean"

    def wrap(self, raw_send):
        def wrapped(args):
            ok, detail = self.check(args)
            if not ok:
                return self._blocked(detail)
            res = raw_send(args)
            if "error" not in res:
                self._passed()
            return res

        return wrapped


class ManifestComplete(_Wrapper):
    """Builder half of MANIFEST-COMPLETE.

    A manifest ships only if it accounts for exactly the files the builder
    enumerated: a stated scope line, every listed file present in the
    listing, and every listed-out file either in the manifest or in its
    declared `excluded` set. An inventory with an unstated scope is
    UNVERIFIED (D8) and blocks here.
    """
    GATE = "MANIFEST-COMPLETE"

    def check(self, manifest, listing):
        scope = (manifest.get("scope") or "").strip()
        if not scope:
            return False, "manifest states no scope line (inventory UNVERIFIED, D8)"
        listed = set(manifest.get("files") or [])
        excluded = set(manifest.get("excluded") or [])
        present = set(listing)
        missing = sorted(listed - present)
        if missing:
            return False, "listed but absent: " + ", ".join(missing[:5])
        unaccounted = sorted(present - listed - excluded)
        if unaccounted:
            return False, "present but unaccounted: " + ", ".join(unaccounted[:5])
        return True, f"{len(listed)} files, scope stated, listing fully accounted"

    def wrap(self, raw_call, manifest_of, listing_of):
        def wrapped(args):
            ok, detail = self.check(manifest_of(args), listing_of(args))
            if not ok:
                return self._blocked(detail)
            res = raw_call(args)
            if "error" not in res:
                self._passed(detail)
            return res

        return wrapped
