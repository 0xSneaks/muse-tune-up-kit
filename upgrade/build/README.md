# Build — steps 1–3 of the upgrade order

Python 3, standard library only. No network, no accounts, no secrets.

| Step | Status | Where |
|---|---|---|
| 1. Gate log, claims block, seven gates | BUILT and tested as a library. **Not wired into Muse's live runtime** (no access from the build machine) | `muse_gates/` |
| 2. Fixtures, runner, smoke set | BUILT and tested | `evalrig/`, `adapters/` |
| 3. Baseline run, frozen | **BLOCKED here.** Must run on Muse's machine; procedure below | — |

## Run it

```
cd upgrade/build
python3 -W error -m unittest discover -s tests      # 35 tests
python3 -m evalrig.runner --agent careful --gates on  --out /tmp/x.json
python3 -m evalrig.runner --agent naive   --gates off --out /tmp/y.json
```

## Step 1 — `muse_gates/`

| File | Holds |
|---|---|
| `store.py` | append-only JSONL on disk, fsynced on every write |
| `claims.py` | the CLAIMS block: parse and render |
| `gates.py` | `GatedTools` (the hook), `secret_scan`, `startup_alive` |

`GatedTools.call(name, args, leg)` is the pre-tool and post-tool hook;
`finalize(report)` is the pre-report hook; `session_start()` is the
STARTUP-ALIVE hook. State files, all under one directory that must be on
persistent disk: `gate_log.jsonl`, `inventory.jsonl`, `approvals.jsonl`,
`approvals_used.jsonl`, `ledger.jsonl`.

To wire it into a real runtime, supply the five things listed in the
docstring at the top of `gates.py`: a raw tool-call function, a trace, a
per-tool metadata table (effect, gate type, read-back function,
state-check function), the owner's approval records, and a worker
registry. `evalrig/fixtures.py` `META` is a worked example for 11 tools.

Behaviors worth knowing before wiring:
- Gated tools carry one of seven gate types: spend, trade, send-as-owner,
  deploy, device, delete, credential. Any other type is refused (D10).
- Three approval kinds (D10). Single-use: one exact call, used once.
  Standing grant: a tool/argument glob scope for one gate type, never
  consumed, and never honoured for spend, trade or credential (a choice made
  here for Muse to accept or reject). Delegated approval: from a reviewer
  the owner lists in `delegates`, bound to the hash of the exact call, used
  once.
- MASKED-VALUE (D9). A masked value is never passed as an argument.
  `verify_value` ends in value-verified (fingerprint match on a readable
  value, or on a functional probe known not to consume the value),
  presence-verified/value-unverified (a masked read, or a probe barred
  because consumption cannot be ruled out), or blocked (absent or
  mismatch). A presence-only leg cannot be DONE; a blocked one becomes
  BLOCKED. Only field paths and keyed fingerprints are logged.
- Claim labels are VERIFIED / INTENT / INFERENCE / UNKNOWN; ASSUMPTION is
  read as INFERENCE, UNVERIFIED and UNCONFIRMED as UNKNOWN (D7).
- A card number needs an issuer prefix, a valid Luhn check and a card word
  nearby; a seed phrase is exactly 12 or 24 short words that do not read as
  prose. Long numeric ids and sentences about seed phrases pass (D29).
- A non-idempotent tool with no state-check route is never retried.
- A DONE leg is rewritten to FAILED if its evidence call failed read-back,
  and to PENDING if the evidence id is not a successful call in the trace.
- Secret values are never written to the gate log, only the pattern class.

## Step 2 — `evalrig/`

- `fixtures.py` — mock world, 28 tools, fault injection
  (silent no-op write, timeout-after-delivery), seeded variation.
- `tasks.py` — the 20 smoke tasks with script scorers:
  R2 R5 E2 E4 E7 M2 M3 J1 J3 G1 G6 G9 J11 J13 J14 J15 J16 K1 K7 V1.
  (J13–J16 and K7 were added in step 4 per SPEC-DELTA D5/D15.) No judge
  model is needed for any of them.
- `runner.py` — tasks × seeds, gates on or off, results JSON, `--freeze`.
- `agents.py` — `CommandAgent` (JSON-lines protocol for any real agent)
  and two scripted reference agents.
- `adapters/muse_agent.py` — Muse itself, via the local Claude CLI
  (step 3 below; written, mock-tested only — never run against the live
  model without the owner's route authorization).
- `adapters/example_agent.py` — the protocol in 40 lines; copy it to wrap
  a model.

Deviations from the spec, stated plainly:
- **15 tasks, not 12.** The retag added J11, K1, V1 to the smoke set
  (`03-eval-harness.md` §3.2); the 12 originally named are all included.
- **M3** is specced as "run consolidation over the old logs". No
  consolidation job exists before step 11, so M3 is realized as a second
  operator turn asking the agent to consolidate and then answer. It runs
  against any agent.
- **K1** delivers the two message parts as two turns; there is no
  wall-clock delay.
- **Token and cost figures** come only from what the agent adapter
  reports in `usage`. With no usage reported, cost per pass is `null`.
- **Process kill-and-restart fault** (needed for V2–V4, not in the smoke
  set) is not built yet. The ledger's restart survival is unit-tested.

## Self-test results (`results/selftest-*.json`)

These are **scripted reference agents, not models, and not the
baseline.** They prove one thing: every scorer can produce both a pass
and a fail. 3 seeds each.

| Config | Tasks passed | Runs with a critical fail (of 45) |
|---|---|---|
| careful script, gates on | 15 / 15 | 0 |
| naive script, gates off | 0 / 15 | 36 (C1 12, C2 21, C3 3) |
| naive script, gates on | 3 / 15 (E2, E4, G6) | 18 (all C2) |

The third row shows what the six gates alone change for an agent that
ignores them: every unapproved action (C1) and duplicate send (C3) is
blocked, and false "done" claims on failed writes are rewritten. Invented
facts and wrong verdicts (C2) are untouched — those belong to gates built
in step 6 (SOURCE-OR-SILENT, TRANSPORT-VS-JOB, JOB-TRIAGE-CLASSIFY).

## Step 3 — the baseline, on Muse's machine

What blocks it here: the baseline is a measurement of Muse's current
system — its 222,578 bytes of standing context and its model. Neither
exists on the build machine, and the standing files must not leave
Muse's machine.

Procedure:

1. Copy `adapters/example_agent.py` to `adapters/muse_agent.py`. Replace
   its body with a loop that sends each `turn` message to Muse's normal
   model with Muse's **unmodified** standing context, exposes the tool
   names from the `session` message, forwards each tool call as a
   `tool_call` line, and returns the final text as `reply` with `usage`.
   Add one instruction to the context for the run: end every reply with
   the CLAIMS block (format in `muse_gates/claims.py`).
2. Run, gates off:
   ```
   python3 -m evalrig.runner --agent "cmd:python3 adapters/muse_agent.py" \
     --gates off --seeds 3 --label "baseline v3.5.19, 222578 B standing" \
     --freeze --out results/baseline-2026-11.json
   ```
3. Commit `results/baseline-2026-11.json` and its `.sha256`. `--freeze`
   refuses to overwrite a frozen file.
4. Optional second run with `--gates on` and the same adapter: the
   difference is the measured effect of step 1 on the real system.

The adapter contains no secrets if the model credential stays in Muse's
environment; do not commit a key.
