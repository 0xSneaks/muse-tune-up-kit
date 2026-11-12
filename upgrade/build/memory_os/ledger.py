"""Fact ledger schema (spec 02 section 2.1) plus the D17 extension.

SPEC-DELTA D17: standing orders leave LIVE. A new ledger predicate class,
`standing-order`, is rendered into the rules layer -- the kernel when the
order binds a gate, otherwise the matching skill -- each rendered line
carrying the owner's quote and the date as provenance (PAIR-MAP P-C5,
registry M-3/M-4). A standing order never renders into LIVE; LIVE is
generated from facts and current state only (spec 02 section 2.2).

Production records must carry a real owner quote and date. Fixture
records built from the muse-side counts pack (MUSE-SIDE-REPORT section D:
counts and structure only, no content) carry them as None and render with
an explicit PENDING marker; `validate_fact(..., production=True)` rejects
them. The values arrive at backfill time (spec 02 section 2.6 step 3),
from the live file, on Muse's machine -- never by copying live content
into this repo.
"""
import re

# Spec 02 section 2.1: a closed vocabulary of about 40 predicates, each
# declared single-valued or multi-valued; only single-valued predicates
# can conflict. `standing-order` is the D17 addition: it is not a fact
# about the world but a rule the owner stated, and it is multi-valued
# (the owner holds many standing orders; they never conflict by value).
PREDICATE_CLASSES = {
    "birthday": "single",
    "location": "single",
    "employer": "single",
    "role": "single",
    "relationship": "multi",
    "contact-pref": "single",
    "member-of": "multi",
    "project-status": "single",
    "deadline": "single",
    "price": "single",
    "preference": "multi",
    "standing-rule": "single",
    "standing-order": "multi",
}

STATUSES = {"active", "contested", "stale", "superseded", "retracted"}
CONFIDENCE = {"owner-correction", "owner-stated", "tool-observed", "inferred"}

_BASE_FIELDS = {"id", "subject", "predicate", "value", "status",
                "confidence", "source", "learned_at"}
_ORDER_FIELDS = {"binds_gate", "skill", "owner_quote", "owner_date"}
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def is_standing_order(rec):
    return rec.get("predicate") == "standing-order"


def validate_fact(rec, production=False):
    """Return a list of schema errors (empty = valid)."""
    errs = []
    missing = _BASE_FIELDS - set(rec)
    if missing:
        errs.append(f"missing fields: {sorted(missing)}")
    pred = rec.get("predicate")
    if pred is not None and pred not in PREDICATE_CLASSES \
            and not str(pred).startswith("other:"):
        errs.append(f"predicate not in vocabulary: {pred}")
    if rec.get("status") not in STATUSES:
        errs.append(f"bad status: {rec.get('status')}")
    if rec.get("confidence") not in CONFIDENCE:
        errs.append(f"bad confidence: {rec.get('confidence')}")
    if is_standing_order(rec):
        extra_missing = _ORDER_FIELDS - set(rec)
        if extra_missing:
            errs.append(f"standing-order missing fields: {sorted(extra_missing)}")
        if rec.get("binds_gate") is True and rec.get("skill") is not None:
            errs.append("gate-binding order renders to the kernel, not a skill")
        if rec.get("binds_gate") is False and not rec.get("skill"):
            errs.append("non-gate order must name its destination skill")
        if production:
            if rec.get("binds_gate") is None:
                errs.append("production: binds_gate unresolved")
            if not rec.get("owner_quote"):
                errs.append("production: owner_quote required (D17 provenance)")
            if not (rec.get("owner_date") and _DATE.match(rec["owner_date"])):
                errs.append("production: owner_date must be YYYY-MM-DD")
    return errs


def _render_line(rec):
    quote = rec.get("owner_quote")
    date = rec.get("owner_date")
    prov = (f'owner: "{quote}" ({date})' if quote and date
            else "owner: PENDING (quote + date arrive at backfill, spec 02 s2.6)")
    return f"- [{rec['id']}] {rec['value']} -- {prov} [source: {rec['source']}]"


def render_rules_layer(records):
    """Render standing-order records into the rules layer (D17).

    Returns {"kernel": [...], "skills": {skill: [...]}, "unresolved": [...]}.
    Gate-binding orders go to the kernel, the rest to their named skill.
    Orders whose content is not yet in the pack (binds_gate is None) land
    in `unresolved` -- visible, never silently dropped, never in LIVE.
    Non-standing-order records are ignored.
    """
    out = {"kernel": [], "skills": {}, "unresolved": []}
    for rec in records:
        if not is_standing_order(rec) or rec.get("status") != "active":
            continue
        line = _render_line(rec)
        if rec.get("binds_gate") is True:
            out["kernel"].append(line)
        elif rec.get("binds_gate") is False:
            out["skills"].setdefault(rec["skill"], []).append(line)
        else:
            out["unresolved"].append(line)
    return out


def live_lines_for(records):
    """LIVE lines contributed by these records. Standing orders: none, ever
    (D17). Ordinary facts contribute a line only via LIVE generation from
    the ledger, which lives in the consolidation job, not here."""
    return [r for r in records if not is_standing_order(r)]
