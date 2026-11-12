"""Fixtures for steps 9-11, built from the muse-side counts pack only.

The pack is counts and structure, never content (MUSE-SIDE-REPORT
section D). So the standing-order fixture is faithful to the counts in
D4-memory-counts.md -- 19 bullets in "Standing orders" (16 rule-like, 3
fact-like) and 16 in "Money, wallets, trading" (12 rule-like, 4
fact-like) -- and each record's `value` is a source pointer into the
live file, not invented rule text. Owner quote/date and gate-binding
arrive at backfill (spec 02 section 2.6) on Muse's machine.
"""
import os
import re

D4_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "..", "diatomic", "muse-side",
                       "D4-memory-counts.md")

SECTIONS = [("Standing orders", "M-3", "so"),
            ("Money, wallets, trading", "M-4", "mw")]


def d4_counts(path=D4_PATH):
    """{(section): (bullets, rule_like, fact_like)} parsed from D4."""
    with open(path) as f:
        text = f.read()
    out = {}
    for line in text.splitlines():
        m = re.match(r"(.+?): bullets=(\d+), rule-like=(\d+), fact-like=(\d+)", line)
        if m:
            out[m.group(1)] = tuple(int(m.group(i)) for i in (2, 3, 4))
    return out


def standing_order_fixture():
    """Ledger records for every bullet D4 counts: rule-like bullets as
    `standing-order` records (destination unresolved until backfill),
    fact-like bullets as ordinary fact records (they stay ledger facts,
    never rules-layer lines)."""
    counts = d4_counts()
    records = []
    for name, mid, prefix in SECTIONS:
        key = next(k for k in counts if k.startswith(name))
        _, rule_like, fact_like = counts[key]
        for i in range(1, rule_like + 1):
            records.append({
                "id": f"{prefix}-{i:03d}", "subject": "owner",
                "predicate": "standing-order",
                "value": (f"<rule text not in pack> live MEMORY.md section "
                          f"'{name}' bullet {i} ({mid})"),
                "status": "active", "confidence": "owner-stated",
                "source": f"diatomic/muse-side/D4-memory-counts.md ({mid} bullet {i})",
                "learned_at": "2026-11-12",
                "binds_gate": None, "skill": None,
                "owner_quote": None, "owner_date": None})
        for i in range(1, fact_like + 1):
            records.append({
                "id": f"{prefix}-fact-{i}", "subject": "owner",
                "predicate": "preference",
                "value": (f"<fact not in pack> live MEMORY.md section "
                          f"'{name}' fact-like bullet {i} ({mid})"),
                "status": "active", "confidence": "owner-stated",
                "source": f"diatomic/muse-side/D4-memory-counts.md ({mid} fact {i})",
                "learned_at": "2026-11-12"})
    return records
