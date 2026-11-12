"""The CLAIMS block: the machine-readable tail every final report must carry.

CLAIMS:
- leg: <name> | status: DONE|PENDING|BLOCKED|FAILED|NOT-ATTEMPTED | evidence: <call id or none>
- claim: <text> | label: VERIFIED|INTENT|INFERENCE|UNKNOWN | evidence: <call id or none>

D7 (revised): the public label set is VERIFIED / INTENT / INFERENCE / UNKNOWN.
Older labels are accepted on input and mapped: ASSUMPTION -> INFERENCE,
UNVERIFIED and UNCONFIRMED -> UNKNOWN. Any other label is dropped, never guessed.
"""
import re

STATUSES = ("DONE", "PENDING", "BLOCKED", "FAILED", "NOT-ATTEMPTED")
LABELS = ("VERIFIED", "INTENT", "INFERENCE", "UNKNOWN")
LABEL_ALIASES = {"ASSUMPTION": "INFERENCE", "UNVERIFIED": "UNKNOWN", "UNCONFIRMED": "UNKNOWN"}
_LEG = re.compile(r"^- leg:\s*(.+?)\s*\|\s*status:\s*([A-Z-]+)\s*\|\s*evidence:\s*(.+?)\s*$")
_CLAIM = re.compile(r"^- claim:\s*(.+?)\s*\|\s*label:\s*([A-Z]+)\s*\|\s*evidence:\s*(.+?)\s*$")


def parse(report):
    body, _, tail = (report or "").partition("CLAIMS:")
    legs, claims = [], []
    for line in tail.splitlines():
        m = _LEG.match(line.strip())
        if m and m.group(2) in STATUSES:
            legs.append({"leg": m.group(1), "status": m.group(2), "evidence": m.group(3)})
            continue
        m = _CLAIM.match(line.strip())
        label = m and normalize_label(m.group(2))
        if label:
            claims.append({"claim": m.group(1), "label": label, "evidence": m.group(3)})
    return {"body": body.rstrip(), "legs": legs, "claims": claims, "has_block": "CLAIMS:" in (report or "")}


def normalize_label(label):
    """Public label for an input label, or None if it is not one we accept."""
    label = (label or "").upper()
    return label if label in LABELS else LABEL_ALIASES.get(label)


def render(body, legs=(), claims=()):
    out = [body.rstrip(), "", "CLAIMS:"]
    out += [f"- leg: {l['leg']} | status: {l['status']} | evidence: {l['evidence']}" for l in legs]
    out += [f"- claim: {c['claim']} | label: {normalize_label(c['label']) or c['label']} | evidence: {c['evidence']}" for c in claims]
    return "\n".join(out)
