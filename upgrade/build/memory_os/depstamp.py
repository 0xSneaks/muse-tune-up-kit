"""DEP-STAMP and CORRECTION-SWEEP (spec 02 section 2.4).

DEP-STAMP is the write-time half: whenever the agent creates a goal,
reminder, follow-up, scheduled job, or draft, it records the fact ids it
read to build it in `deps.jsonl`. That is what makes sweep pass (a) exact.

CORRECTION-SWEEP runs when a fact is superseded. Blast radius, three
passes, unioned:
  a. deps.jsonl lookup by old fact id (exact);
  b. literal search for the old value and its format variants across
     active artifacts (dated logs are never searched for editing and
     never edited -- the correction record shadows them at search time);
  c. a cheap-tier yes/no per remaining subject-mentioning artifact. This
     needs a model tier, so it is an injected callable (`ask`); with no
     callable the pass is reported as not run, never silently skipped.

Fix by hit class (spec table): internal text and reminders are patched;
scheduled outbound / approval-gated drafts are patched and marked
needs-approval; already-sent artifacts are listed as sent-with-old-value
and never touched. Then a residual check repeats pass (b): remaining
hits must be zero or each carries its class reason.
"""
import re

ARTIFACT_KINDS = {"goal", "reminder", "follow_up", "scheduled_job", "draft"}
# Artifact classes for sweep hits, per the spec 02 section 2.4 table.
HIT_CLASSES = {"internal", "reminder", "scheduled_outbound", "sent", "log"}

_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def date_variants(value):
    """Format variants of a date value, per spec 02 section 2.4 pass (b):
    `2027-03-12` -> also `03-12`, `3/12`, `Mar 12`, `12th`. A bare MM-DD
    value gets the same treatment. Non-dates yield just the value."""
    out = {value}
    m = re.match(r"^(\d{4}-)?(\d{2})-(\d{2})$", value or "")
    if m:
        mon, day = int(m.group(2)), int(m.group(3))
        out.add(f"{mon:02d}-{day:02d}")
        out.add(f"{mon}/{day}")
        out.add(f"{_MONTHS[mon - 1]} {day}")
        out.add(f"{day}th" if day not in (1, 21, 31) else f"{day}st")
    return sorted(out)


def stamp(store, artifact_id, kind, fact_ids, ts):
    """Record the fact ids an artifact was built from (DEP-STAMP)."""
    if kind not in ARTIFACT_KINDS:
        raise ValueError(f"unstampable artifact kind: {kind}")
    rec = {"artifact": artifact_id, "kind": kind,
           "facts": list(fact_ids), "ts": ts}
    store.append("deps.jsonl", rec)
    return rec


def _find(text, needles):
    return [n for n in needles if n and n in text]


def sweep(store, old_fact, new_fact, artifacts, ask=None, ts=""):
    """Run CORRECTION-SWEEP for old_fact -> new_fact.

    `artifacts`: {artifact_id: {"text": str, "class": one of HIT_CLASSES}}.
    Writes the correction record and the deps for the sweep itself.
    Returns (receipt, patched_texts) where receipt is the spec shape
    {old, new, found, fixed, needs_approval, sent, residual} plus a
    `detail` list carrying each hit's class action and reason.
    """
    store.append("corrections.jsonl",
                 {"old_id": old_fact["id"], "new_id": new_fact["id"],
                  "old_value": old_fact["value"], "new_value": new_fact["value"],
                  "ts": ts})
    needles = date_variants(old_fact["value"])
    dep_hits = {r["artifact"] for r in store.read("deps.jsonl")
                if old_fact["id"] in r.get("facts", [])}
    hits = {}  # artifact_id -> set of passes that hit it
    for aid in dep_hits:
        if aid in artifacts and artifacts[aid]["class"] != "log":
            hits.setdefault(aid, set()).add("a")
    for aid, art in artifacts.items():
        if art["class"] == "log":
            continue  # dated logs are never edited; corrections shadow them
        if _find(art["text"], needles):
            hits.setdefault(aid, set()).add("b")
    pass_c = "not-run"
    if ask is not None:
        pass_c = "ran"
        for aid, art in artifacts.items():
            if aid in hits or art["class"] == "log":
                continue
            if old_fact["subject"] in art["text"] or old_fact["subject"].split(":")[-1] in art["text"]:
                if ask(aid, art["text"], old_fact):
                    hits.setdefault(aid, set()).add("c")

    # Pass-(a) hits are fixed at the dependency record itself: re-point
    # the artifact at the new fact id, whatever its text says.
    for r in store.read("deps.jsonl"):
        if old_fact["id"] in r.get("facts", []):
            store.append("deps.jsonl",
                         {"artifact": r["artifact"], "kind": r["kind"],
                          "facts": [new_fact["id"] if f == old_fact["id"] else f
                                    for f in r["facts"]],
                          "ts": ts, "repointed_from": old_fact["id"]})

    patched, detail = {}, []
    fixed = needs_approval = sent = 0
    for aid in sorted(hits):
        art = artifacts[aid]
        cls = art["class"]
        new_text = art["text"]
        for n in needles:
            new_text = new_text.replace(n, new_fact["value"] if n == old_fact["value"]
                                        else _remap(n, old_fact["value"], new_fact["value"]))
        if cls in ("internal", "reminder"):
            action, reason = "patched", ""
            patched[aid] = new_text
            fixed += 1
        elif cls == "scheduled_outbound":
            action, reason = "patched-needs-approval", "behind an approval gate"
            patched[aid] = new_text
            needs_approval += 1
        elif cls == "sent":
            action, reason = "sent-with-old-value", "already sent, irreversible"
            sent += 1
        else:
            action, reason = "skipped", f"class {cls}"
        detail.append({"artifact": aid, "passes": sorted(hits[aid]),
                       "class": cls, "action": action, "reason": reason})

    # Residual check: repeat pass (b) over the post-fix state. A remaining
    # hit is explained iff its class action already accounts for it
    # (needs-approval draft carries the new value; sent keeps the old one
    # and is listed). Anything else is an unexplained residual.
    residual = []
    for aid, art in artifacts.items():
        if art["class"] == "log":
            continue
        after = patched.get(aid, art["text"])
        if _find(after, needles) and not (
                aid in patched and after == art["text"]):
            entry = next((d for d in detail if d["artifact"] == aid), None)
            if not (entry and entry["action"] == "sent-with-old-value"):
                residual.append(aid)
    receipt = {"old": old_fact["id"], "new": new_fact["id"],
               "found": len(hits), "fixed": fixed,
               "needs_approval": needs_approval, "sent": sent,
               "residual": len(residual), "pass_c": pass_c,
               "detail": detail, "residual_ids": residual}
    return receipt, patched


def _remap(variant, old_value, new_value):
    """Map a format variant of the old value to the same format of the new
    value (Mar 12 -> Mar 15 when 2027-03-12 -> 2027-03-15)."""
    old_variants = date_variants(old_value)
    new_variants = date_variants(new_value)
    if variant in old_variants and len(old_variants) == len(new_variants):
        return new_variants[old_variants.index(variant)]
    return new_value


def resurrection_guard(candidate, facts, corrections):
    """Spec 02 section 2.4: consolidation rejects a candidate fact whose
    value equals a superseded value for the same (subject, predicate)
    when its source predates the correction. Returns True = reject."""
    for corr in corrections:
        old = next((f for f in facts if f["id"] == corr["old_id"]), None)
        if old is None:
            continue
        if (candidate.get("subject") == old["subject"]
                and candidate.get("predicate") == old["predicate"]
                and candidate.get("value") == corr["old_value"]
                and candidate.get("learned_at", "") < corr.get("ts", "")):
            return True
    return False
