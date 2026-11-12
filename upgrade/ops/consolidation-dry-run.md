# Consolidation pass — SPEC + DRY RUN (step 11a)

The consolidation job (spec 02 §2.5: nightly, workhorse tier for
extraction, strong only for ≥3-way conflicts) turns dated logs into
ledger facts, regenerates the entity views and LIVE, and advances a
watermark. **This document is the pass spec plus a dry run over the
counts in the pack. Nothing was merged, moved, or regenerated.**

## The pass, per spec 02 §2.2 / §2.5

1. Read dated logs since the watermark. Durable statements → candidate
   facts, each with a source pointer to the log line (§2.6 step 3 runs
   the same extraction oldest-first at backfill). Episodic one-liners →
   the entity's notes section, dated.
2. Every candidate runs the resurrection guard
   (`build/memory_os/depstamp.py`): a value equal to a superseded value
   for the same (subject, predicate), sourced before the correction, is
   rejected — re-reading old logs must not undo corrections.
3. Candidates run conflict detection (§2.3): alias resolution, then
   confidence order (owner-correction > owner-stated > tool-observed >
   inferred; inferred never supersedes). A supersession writes a
   `corrections.jsonl` line and triggers CORRECTION-SWEEP (§2.4,
   implemented + tested in `build/memory_os/depstamp.py`).
4. Logs older than 14 days → monthly digest; originals kept, excluded
   from default search.
5. Two files for one entity → one entity: alias match merges facts under
   the older id; the second file becomes a redirect stub.
6. A fact stated in both a person file and a group file lives in the
   ledger only (one `member-of` fact); both views render it, neither
   restates it.
7. Finished projects and closed goals leave LIVE at next generation.
8. Regenerate views and LIVE: every LIVE line carries its fact id; a
   line with no live fact is dropped (§2.5 S2). LIVE budget 6 KB
   (see `standing-orders-dry-run.md` for the byte projection).
9. Advance the watermark. Register the run with the health watcher so a
   silent consolidation failure is itself detected (§2.5).

What the weekly staleness audit (S1–S13) does with the results — demote,
move, flag, never delete — is spec 02 §2.5 and unchanged by this lane.

## Dry run: which live stores WOULD merge

Counts only — from the pack (MUSE-SIDE-REPORT §D, ATOM-REGISTRY §§4/8,
spec 02 §2.7 baselines). No live content was copied into this repo.

| Store | Count (source) | Would become |
|---|---|---|
| Dated logs | 41 files (§2.7 baseline) | candidate facts → ledger; episodic lines → entity notes; >14 days → monthly digest |
| Person files | 48 (§2.7) | generated views: facts block from ledger + free-text notes |
| Group files | 39 (§2.7) | same; membership restated nowhere — one `member-of` fact each |
| Live memory file | 22,247 B, 9 sections (registry §4) | generated LIVE ≤ 6 KB; standing orders out first (D17 dry run) |
| Standing orders in LIVE | 35 bullets total across M-3/M-4; 28 rule-like, 7 fact-like (D4) | 28 `standing-order` ledger records → rules layer; 7 stay ledger facts |
| Lessons file | 7 lessons, 2,946 B (registry §8) | one sink: each lesson routed to exactly one carrier (`build/memory_os/lessons.py`); the file stops being a carrier |
| Goal workspaces | 132 dirs (D2) vs 78+ tracked (§2.5 S11 baseline) | S11: untracked workspaces move to `archive/` after 30 days unreferenced — flagged, not moved, by this dry run |
| Alignment synthesis | 34,150 B injected nightly (§2.7) | no longer injected: consolidation writes its changes into the ledger; LIVE is the only memory text in standing context |

Lessons routing outcome (D15; registry §8 is the assignment of record,
implemented in `build/memory_os/lessons.py`, tested per lesson):

| Lesson | Carrier (the one sink) | Reproducing eval | Captured? |
|---|---|---|---|
| L-1 | kernel line | K4 | no — K4 not in suite |
| L-2 | merge into A-016 | E-series (E2/E4/E7 present) | yes |
| L-3 | check STARTUP-ALIVE | none assigned | no — no eval task (§2.8.3) |
| L-4 | gate DATA-NOT-ORDERS | none assigned | no — no eval task (§2.8.3) |
| L-5 | gate SOURCE-OR-SILENT (audited) | K7 (present) | yes |
| L-6 | kernel line | K1 (present), K5 | no — K5 not in suite |
| L-7 | kernel line | K2, K3 | no — neither in suite |

2 of 7 captured. The other five are routed — each has exactly one
carrier — but §2.8.3 withholds "captured" until a reproducing eval task
exists. Writing K2–K5 and tasks for L-3/L-4 is eval-harness work
(step 4 territory), not consolidation work; it is named here as the
blocker, not done here.
