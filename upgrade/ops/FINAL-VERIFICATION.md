# FINAL VERIFICATION — Muse OS upgrade, step 13 + step-14 prep (lane B13)

Run fresh on 2026-11-12 (07:12 UTC) in the local clone
`~/workspace/fable-brainstorm/session-clone`. Every number below comes
from a command run in this session or a file measured in this session.
Nothing live was touched; nothing here is committed or pushed (the
orchestrator publishes).

## 1. Suite results — exact counts

| Suite | Command | Result | Expected | Verdict |
|---|---|---|---|---|
| Build suite | `python3 -m unittest discover -s tests` in `upgrade/build` | **Ran 53 tests — OK** (0 failures, 0 errors) | 53 | MATCH |
| Kernel suite | `python3 -m unittest test_kernel_check` in `upgrade/kernel` | **Ran 6 tests — OK** | 6 | MATCH |
| Kernel check (direct) | `python3 kernel/kernel_check.py` | `kernel_bytes=9464`, `verbatim_bytes=3519`, `controlled_total_bytes=16381 (kernel 9464 + LIVE 6144 + skills index 773)`, `KERNEL CHECK: PASS` | PASS | MATCH |
| Statement-analyzer mock (step-14 prep, separate) | `python3 -m unittest statement_analyzer.test_analyzer` in `upgrade/build` | **Ran 6 tests — OK** | n/a (new) | PASS, not counted in the build suite (see §4) |

### Snapshot checker against the D1–D5 fixtures

`python3 upgrade/build/wrappers/snapshot_check.py --side-dir upgrade/diatomic/muse-side`
— exit code **1**, verbatim output:

```
PAIR goals: MATCH — D2 claims 132, enumerates 132 workspaces
PAIR jobs: MATCH — D1 claims 31, enumerates 31 jobs (24 enabled)
PAIR health-schedule: MATCH — muse-health-watch installed and enabled in D1; SCHEDULE.md's 'not installed' text is stale (E3)
PAIR skills: MATCH — D3 parts 57 + 37 = 94 vs stated total 94
PAIR memory-counts: MATCH — both sections sum
PAIR manifest: DRIFT — script recount 135 vs manifest scope counts [131, 134] — scopes differ and the manifest never stated its scope (UNVERIFIED, D8)
PAIR cross-file: MATCH — D5 restates goals=132, skills=94 against D2/D3
```

6 MATCH / 1 DRIFT. The manifest DRIFT is the known, documented one
(the manifest never stated its counting scope; three scopes counted
131/134/135) and exit 1 is the asserted-correct behaviour — the build
suite's `test_exit_code_is_1_while_manifest_drifts` encodes exactly
this. It is reported here, not smoothed: the pair stays DRIFT until
the manifest gains its scope line (kernel-cut territory, step 8).

## 2. Head-to-head (step 13, offline part) — before / after

"Before" = the recorded CURRENT live measurements. "After" = measured
artifacts of the upgrade package, this session. The eval-rig rows use
the rig's **scripted** careful/naive reference agents (the rig's own
self-test mode) — they prove the rig discriminates; they are **not**
model runs.

| Measure | Before (live, recorded) | After (measured artifacts) | Source of "after" |
|---|---|---|---|
| Standing controlled bytes | 188,428 B | **16,381 B** (kernel 9,464 + LIVE 6,144 + skills index 773) | `kernel_check.py` on the actual files |
| On-demand rule skills | — (rules inline in standing files) | 5 skills, **36,093 B** total (deploy 5,894 · media 8,000 · onchain 7,900 · pre-publish 7,988 · verification-core 6,311), loaded per task, not standing | `wc -c upgrade/skills/*/SKILL.md` |
| Eval smoke tasks | 24 | 24 (same rig set) | `evalrig.tasks.T` |
| Scripted careful agent, gates ON | — | **24/24 tasks passed, 0 critical-fail runs** (72 runs) | fresh rig run, this session |
| Scripted naive agent, gates OFF | — | **0/24 tasks passed, 63 critical-fail runs** | fresh rig run, this session |
| Scripted naive agent, gates ON | — | **3/24 tasks passed, 45 critical-fail runs** | fresh rig run, this session |
| Step-4 tasks J13–J16 + K7 | did not exist | careful/gates-on **5/5**; naive/gates-off **0/5, 15 critical-fail runs** | fresh rig run, this session |
| Lessons captured (of 7) | **2/7** (pre-B11) | **7/7** — router output: routed 7, captured 7, uncaptured none | `memory_os.lessons.capture_report` run this session |
| Build unit suite | 15 tests at program start | **53 tests, OK** | §1 |
| Kernel unit suite | did not exist | **6 tests, OK** | §1 |

Caveat on the byte row: 16,381 B is the upgrade package's controlled
total as checked against its caps — the kernel has **not** been cut
over live (step 8 is the owner's single reviewed diff). The comparison
is package-vs-live, stated as such.

Note on stored rig results: `upgrade/build/results/selftest-*.json`
from earlier lanes cover only 15 of the 24 smoke tasks (a stale subset
of the current rig). The fresh runs above supersede them; the stored
files were not edited.

### Live-agent head-to-head — PENDING-BASELINE

The real comparison (a live model agent on the recorded baseline
tasks, gates off vs the upgraded package, gates on) is **not** run
here and is **not** faked. It waits for the step-3 baseline run, which
is sequenced after the Claude weekly reset (Sat Nov 14, 14:00 ET) or
the owner's "run it now". Status: **PENDING-BASELINE**.

## 3. Regression sweep (collapse cases + skills pointers)

Scripted, not eyeballed (chain-aware section resolver: a `§N` ref
resolves against the chain named on its line, else the file's own
chain CURRENT-STATE; ranges expanded).

- **Regression cases:** 88 total across the five chains
  (deploy-verify 19 · media-verify 28 · onchain-send 16 ·
  pre-publish 21 · verification-core 4). The cases are prose cases in
  `upgrade/collapse/*/REGRESSION.md`; their expected outcomes are
  encoded as gate-level unit tests in the build suite (gates,
  wrappers, memory_os, snapshot check), which passes 53/53 (§1).
  Section citations inside the cases: 165 refs checked.
- **Skills pointers:** 240 section refs checked across the five
  `upgrade/skills/*/SKILL.md` files.
- **Flags:** the script flagged 5 refs (2 in skills, 3 in regression
  files). Each was adjudicated against its full context; all 5 are
  multi-target lines the line-based resolver cannot split, and each
  resolves:
  - `skills/pre-publish/SKILL.md` "Carried elsewhere" list: `§12, §4,
    §11, §2` belong to `media-verify` (named at the end of the
    preceding line); media-verify CURRENT-STATE has §§1–12 — all four
    exist.
  - `collapse/media-verify/REGRESSION.md` RC-13: bare `§12` is
    media-verify's own §12 (the manifest duty); the same sentence's
    `verification-core §8` also exists.
  - `collapse/pre-publish/REGRESSION.md` rows R-080 / R-084+R-091:
    "§11 above" / "§14 above" refer to pre-publish's own CURRENT-STATE
    §§11/14 — both exist.
- **Genuinely dangling pointers: 0.**

## 4. Step-14 prep — statement analyzer (MOCK ONLY)

`upgrade/build/statement_analyzer/` — `analyzer.py` + `__init__.py` +
`fixtures/synthetic_statement.csv` + `test_analyzer.py` (6 tests, OK,
§1). The module header states, and the code enforces:

- It processes **NO real statements**: input whose first line lacks
  the `SYNTHETIC FIXTURE` marker is refused (tested), and a fixture
  whose running balances do not reconcile is refused (tested).
- It activates only on **owner approval of the mock** (step 14's
  gate). Nothing live imports it; its tests live inside the package,
  deliberately outside `build/tests`, so the shipped suite count (53)
  is untouched.
- Output is the ledger's claim format: one
  `other:statement-transaction` record per fixture row plus one
  `other:statement-balance` record, every record passing
  `memory_os.ledger.validate_fact` (tested); ids are deterministic
  digests (tested); fixture totals reconcile 100,000 + Σamounts =
  332,592 cents (tested). All fixture names/amounts are fictional
  ("First Example Bank", "EXAMPLE CUSTOMER").

## 5. Failures and mismatches — complete list

1. Snapshot pair `manifest`: **DRIFT** (expected/documented; §1).
2. Stored rig result files cover 15/24 tasks — stale subsets,
   superseded by this session's fresh runs (§2). Files left as-is.
3. Nothing else failed. Build 53 = expected 53; kernel 6 = expected 6;
   no test in any suite failed or errored.
