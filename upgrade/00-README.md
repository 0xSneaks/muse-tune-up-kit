# Muse Architecture Upgrade — design assets

Six specs a mid-tier builder agent can implement and operate. Nothing here
needs a frontier model at runtime.

| # | File | Attacks |
|---|---|---|
| 1 | `01-context-diet.md` | F3 |
| 2 | `02-memory-os-v2.md` | F4 |
| 3 | `03-eval-harness.md` | F1, F2 (contract for the whole upgrade) |
| 4 | `04-router-policy.md` | cost |
| 5 | `05-gates-library.md` | F1, F2, F5 |
| 6 | `06-gainshare-playbook.md` | revenue seed |

## READ FIRST — what these designs were built on

**The context pack was not in the session.** The brief said "below is a
sanitized context pack"; nothing followed, and this repo holds only the
generic tune-up kit. So:

- VERIFIED (from the brief itself): rules file is 144 KB; memory tree is 134
  files with dated logs, person/group files and one live layer; F3 is the
  class the context diet attacks, F4 memory, F1/F2 the eval harness, F1/F2/F5
  the gates; gate names READBACK-REQUIRED, LEG-INVENTORY, MASKED-VALUE,
  TRANSPORT-VS-JOB; one operator; approval gates stay; no secrets anywhere.
- ASSUMPTION (inferred from those hints, not read from the pack):

| Class | Assumed meaning |
|---|---|
| F1 | Claim without proof: "done / sent / fixed / the price is X" with no evidence behind it |
| F2 | Multi-leg work reported as done when a leg failed, was skipped, or was never verified |
| F3 | Standing-context bloat: 144 KB injected every turn; rules diluted, contradicted, or ignored |
| F4 | Memory conflict and stale facts; a correction fixed in one place and wrong in five others |
| F5 | Wrong-layer evidence: transport success read as job success, masked value read as real value |
| F6 | **Unknown.** Treated as approval-gate / injection discipline (eval category G) |
| F7 | **Unknown.** Not designed against |

- NOT AVAILABLE: the measured baselines. No number in these files is a
  measurement of Muse. Every threshold is a design target, marked as such,
  to be replaced by the first baseline run (`03-eval-harness.md` §5).

If F5–F7 mean something else, the fix is local: retag the eval tasks
(`guards` column) and the gates (`kills` line). The structures do not change.

## (a) Implementation order — mid-tier builder agent, ~39 working days

Order is forced by one rule: **measure before you move anything.**

| Step | Work | Days | Depends on |
|---|---|---|---|
| 1 | Gate log + report claims block; gates READBACK-REQUIRED, LEG-INVENTORY, UNKNOWN-OUTCOME, APPROVAL-TOKEN, SECRET-SCAN as hooks | 4 | — |
| 2 | Eval fixtures (mock tools, frozen web corpus, memory fixture), runner, 12-task smoke set | 4 | 1 |
| 3 | **Baseline run** of smoke set on the current 144 KB system; freeze results | 1 | 2 |
| 4 | Remaining 38 tasks; judge mutation test | 4 | 2 |
| 5 | Rules manifest (chunk + classify the 144 KB file) | 2 | 3 |
| 6 | Remaining executable checks and gates | 3 | 1, 5 |
| 7 | Module extraction, one module per commit, eval between each | 4 | 4, 6 |
| 8 | Kernel cut; legacy file demoted to logged fallback | 1 | 7 |
| 9 | Memory: fact ledger, backfill of 134 files, generated views | 4 | 4 |
| 10 | Memory: DEP-STAMP, CORRECTION-SWEEP, resurrection guard | 3 | 9 |
| 11 | Memory: nightly consolidation + weekly staleness audit jobs | 2 | 10 |
| 12 | Router: decision log, static table, escalation, two-model check | 3 | 4 |
| 13 | Full suite + head-to-head vs frontier reference; first router fit | 2 | 8, 11, 12 |
| 14 | Gainshare export analyzer (waste-pattern detectors + statement script) | 2 | 12 |

Steps 9–11 can run in parallel with 5–8 if two builders exist. The legacy
rules file is deleted only after 30 days with zero fallback loads.

## (b) Top 3 risks in these designs

1. **Designed blind to the pack.** The F-class mapping is inferred. If real
   incidents do not map to a gate and an eval task, the suite will score well
   while the live failure continues. Mitigation is Pass B item 1.
2. **Retrieval miss replaces bloat with absence.** A rule that was diluted
   at 144 KB at least existed in context; a module that fails to load does
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

1. **Incident coverage.** Take every real F1–F7 incident in the pack. Each
   must map to at least one gate and one eval task that would have caught
   it. Any unmapped incident is a gap in the contract; fix before building.
2. **Retrieval-miss rate in shadow mode.** Run the trigger map against a
   week of real turns while the 144 KB file is still loaded. Count turns
   where a rule was needed and its module would not have loaded.
3. **M2 + M3 on a copy of the real memory tree.** Correct one real fact,
   run the sweep, then re-run consolidation over the old logs. Residual
   hits or a resurrected value means Memory OS v2 does not yet kill F4.
4. **Judge mutation test.** Inject known violations into passing
   transcripts; a judge that misses more than 1 in 20 cannot score the suite.
5. **Kernel under load.** Run category G with the kernel alone, no modules.
   It must still produce zero critical fails; the kernel is the last line.
