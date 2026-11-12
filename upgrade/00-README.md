# Muse Architecture Upgrade — design assets

Six specs a mid-tier builder agent can implement and operate. Nothing here
needs a frontier model at runtime.

| # | File | Attacks |
|---|---|---|
| 1 | `01-context-diet.md` | F3 (and carries F5, F6, F7 rules out of prose) |
| 2 | `02-memory-os-v2.md` | F4; lessons pipeline for F6 |
| 3 | `03-eval-harness.md` | F1–F7 (contract for the whole upgrade) |
| 4 | `04-router-policy.md` | cost |
| 5 | `05-gates-library.md` | F1, F2, F5, F7 |
| 6 | `06-gainshare-playbook.md` | revenue seed |

Inputs: `CONTEXT-PACK.md` (architecture and measured baselines) and
`RETAG-BRIEF.md` (the delta against the first draft). The specs were first
written without the pack and have since been retagged to it.

## Failure classes (pack §4) and what carries each

| Class | Meaning | Status vs first draft | Carriers |
|---|---|---|---|
| F1 | Premature "done" from a first readout, HTTP 200, or local edit | MATCH | READBACK-REQUIRED, TRANSPORT-VS-JOB, SOURCE-OR-SILENT, UNKNOWN-OUTCOME; tasks R, E |
| F2 | Folded claims; self-reported inventories treated as complete | MATCH, extended | LEG-INVENTORY (independent inventory), CREW-REPORT-UNVERIFIED, MASKED-VALUE; tasks E |
| F3 | Standing-context bloat; every lesson becomes permanent text | MATCH, rescoped to all 222,578 standing bytes | context diet, CI byte caps, lessons pipeline |
| F4 | Memory drift; corrections not propagated | MATCH | fact ledger, CORRECTION-SWEEP, DEP-STAMP, staleness audit; tasks M |
| F5 | Job-failure mis-triage: transport flap vs job-level failure | CORRECTED | JOB-TRIAGE-CLASSIFY; tasks J5, J10–J12 |
| F6 | Communication slips; lessons under-captured | REPLACED | kernel lines, `mod-comms-live`, lessons pipeline with capture-rate check; tasks K. No gate, by design |
| F7 | Continuity loss: silent dead worker, unresumable long jobs | ADDED | STARTUP-ALIVE, CHECKPOINT-REQUIRED, WATCH-THE-WATCHER, on-disk gate state; tasks V |

Approval gates, secrets, and injection discipline are pack §6 constraints,
not a numbered class. Eval category G and the gates APPROVAL-TOKEN,
SECRET-SCAN, DATA-NOT-ORDERS, and LEAST-DISCLOSURE hold them.

## What is measured and what is still a target

- MEASURED (pack §2): 222,578 bytes of standing context per turn; 134
  memory files in 25 MB; 7 lessons in about 5 weeks; 31 jobs, 24 enabled,
  3 with a failed last run; 730 handoff files; 131 goal workspaces.
- TARGET, not measured: every pass rate, the 20 KB context cap, cost per
  pass, capture rate. The pack has no pass-rate or cost baseline; build
  step 3 produces them.
- NOT DONE: per-paragraph classification of the rules file. The pack has
  its size, not its text. Build step 5 does this on the machine that
  holds the file.

## (a) Implementation order — mid-tier builder agent, ~43 working days

Order is forced by one rule: **measure before you move anything.**

| Step | Work | Days | Depends on |
|---|---|---|---|
| 1 | Gate log and report claims block, all state on disk; gates READBACK-REQUIRED, LEG-INVENTORY, UNKNOWN-OUTCOME, APPROVAL-TOKEN, SECRET-SCAN, STARTUP-ALIVE as hooks | 5 | — |
| 2 | Eval fixtures (mock tools, frozen web corpus, memory fixture, kill-and-restart), runner, 15-task smoke set | 4 | 1 |
| 3 | **Baseline run** of the smoke set on the current 222 KB system; freeze results | 1 | 2 |
| 4 | Remaining 49 tasks; judge mutation test | 5 | 2 |
| 5 | Rules manifest (chunk and classify the 144 KB file) | 2 | 3 |
| 6 | Remaining gates, including JOB-TRIAGE-CLASSIFY, CHECKPOINT-REQUIRED, CREW-REPORT-UNVERIFIED | 3 | 1, 5 |
| 7 | Module extraction, one module per commit, eval between each | 4 | 4, 6 |
| 8 | Kernel cut; context profiles for crew and crons; persona and nightly synthesis out of standing context; legacy file demoted to logged fallback | 2 | 7 |
| 9 | Memory: fact ledger, backfill of 134 files, generated views | 4 | 4 |
| 10 | Memory: DEP-STAMP, CORRECTION-SWEEP, resurrection guard | 3 | 9 |
| 11 | Memory: nightly consolidation, weekly staleness audit, lessons pipeline | 3 | 10 |
| 12 | Router: decision log, static table, escalation, two-model check, bench eligibility | 3 | 4 |
| 13 | Full suite and head-to-head against the evaluator agent (one reference run, results stored); first router fit | 2 | 8, 11, 12 |
| 14 | Gainshare export analyzer (waste-pattern detectors and statement script) | 2 | 12 |

Steps 9–11 can run in parallel with 5–8 if two builders exist. The legacy
rules file is deleted only after 30 days with zero fallback loads.
STARTUP-ALIVE is in step 1 because the one F7 incident on record cost
6.5 hours of unread messages and the check is a day of work.

## (b) Top 3 risks in these designs

1. **The rules file's text is still unseen.** The class mapping is now
   from the pack, but the classification split and the module list are
   inferred from a size and a description. If the manifest (step 5) shows
   a large body of rules that fits no module here, the module list
   changes. The procedure and the coverage invariant do not.
2. **Retrieval miss replaces bloat with absence.** A rule that was diluted
   at 222 KB at least existed in context; a module that fails to load does
   not. Mitigations: triggers keyed on tool names, not on model judgment;
   irreversible actions enforced by executable gates that do not depend on
   retrieval; logged legacy fallback for 30 days.
3. **The fact ledger makes wrong facts authoritative.** A mid-tier extractor
   will mis-key some facts, and a canonical store repeats its errors with
   confidence. The closed predicate vocabulary also drops nuance.
   Mitigations: every fact carries a source pointer and a confidence class;
   inferred facts never win a conflict; entity files keep a free-text notes
   section; backfill ships with a diff report, originals kept.

Runner-up: the eval suite's mock tools behave more cleanly than real ones,
so pass rates overstate live reliability. The monthly router refit uses
production outcomes for that reason, not suite results alone.

## (c) What to test first in a Pass B review

1. **Incident coverage.** Take every real F1–F7 incident in the operating
   history (the pack names classes, not incidents). Each
   must map to at least one gate and one eval task that would have caught
   it. Any unmapped incident is a gap in the contract; fix before building.
2. **Retrieval-miss rate in shadow mode.** Run the trigger map against a
   week of real turns while the full standing context is still loaded. Count turns
   where a rule was needed and its module would not have loaded.
3. **M2 + M3 on a copy of the real memory tree.** Correct one real fact,
   run the sweep, then re-run consolidation over the old logs. Residual
   hits or a resurrected value means Memory OS v2 does not yet kill F4.
4. **Judge mutation test.** Inject known violations into passing
   transcripts; a judge that misses more than 1 in 20 cannot score the suite.
5. **Kill drills.** V2 and V3 on a real long job: kill mid-run, restart,
   confirm nothing is redone and nothing is sent twice.
6. **Kernel under load.** Run category G with the kernel alone, no modules.
   It must still produce zero critical fails; the kernel is the last line.
