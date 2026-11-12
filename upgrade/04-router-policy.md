# 4. Router Policy (attacks cost)

**Replaces:** one model for everything, chosen by habit.
**With:** a decision table fitted to eval results, with fixed escalation
rules and a log that lets a script re-fit it monthly.
**Failure classes:** the two-model check is a second barrier on F1/F2 for
consequential work; the rest is cost.

Tiers are roles, not model names. `router.yaml` maps each tier to a
concrete model; the policy survives model releases unchanged.

| Tier | Role |
|---|---|
| frontier | the credit-limited evaluator agent: reference runs for the eval suite and owner-requested design review; never scheduled, never in a task path |
| strong | planning, consequential execution, conflict adjudication |
| workhorse | routine tool work, extraction, triage |
| cheap | classification, yes/no checks, formatting |

## 4.1 Decision table (starting point; step 13 replaces it with fitted values)

| Task class | Default | Escalates to | Two-model check | Budget cap (tokens / tool calls) |
|---|---|---|---|---|
| Turn labeling, module selection, yes/no checks | cheap | workhorse | no | 8k / 0 |
| Formatting, summarizing provided text | cheap | workhorse | no | 20k / 2 |
| Single-leg reversible tool task | workhorse | strong | no | 60k / 8 |
| Research: search and fetch | workhorse | strong | claim check by cheap | 150k / 25 |
| Research: synthesis and answer | strong | — | claim check by cheap | 80k / 5 |
| Memory extraction (consolidation) | workhorse | strong | no | 100k per log batch / 0 |
| Memory conflict adjudication, correction sweep | strong | owner | no | 80k / 30 |
| Job triage (after JOB-TRIAGE-CLASSIFY has run as a script) | workhorse | strong | no | 100k / 20 |
| Crew sub-agent, one bounded task | workhorse | strong | CREW-REPORT-UNVERIFIED spot-check by the parent | 60k / 10 |
| Live-call replies and status | workhorse | — | no | 4k / 0 |
| Multi-leg execution, 3+ legs, no gated leg | strong plans, workhorse executes legs | strong executes | no | 250k / 40 |
| Consequential: spend, public post, send-as-owner, delete, credential, deploy | strong | owner | **yes** | 250k / 40 |
| Long-form writing | strong | — | no | 120k / 5 |
| Architecture or design review | frontier | — | no | owner-initiated, one session |

A task takes the highest class any of its legs falls into. A task whose
class cannot be determined is treated as multi-leg.

## 4.2 Escalation rules

Escalation is triggered by observable signals only. A model's stated
confidence is not a signal.

| # | Trigger | Action |
|---|---|---|
| X1 | The same gate fails twice on the same leg | one tier up for that leg |
| X2 | The same tool call with the same arguments issued 3 times | one tier up; the loop is logged |
| X3 | 80% of budget spent with a leg still not DONE | stop; one tier up with a fresh budget of half the original; if already strong, report BLOCKED |
| X4 | Two-model check disagrees | strong adjudicates; still split → owner |
| X5 | Class pass rate for the current tier fell below threshold in the last refit | the table changes, not the run |
| X6 | Any critical-fail condition detected by a gate | stop; no escalation; report to owner |

Limits: at most one escalation per leg and two per task. Escalation never
reaches frontier. Escalation never bypasses a gate: an action refused by
APPROVAL-TOKEN stays refused at every tier.

Handoff on escalation is a compact packet, not the transcript: owner
instruction verbatim, leg inventory with statuses, evidence refs, the
failing gate's output. This keeps the higher tier's input small.

De-escalation: once strong has produced a plan with a leg inventory,
independent legs run on workhorse. Read-back checks run on cheap.

## 4.3 Two-model check (consequential work)

Runs after the executor has prepared the action and before the approval
request reaches the owner, so the owner approves something already
cross-checked.

- **Verifier:** workhorse tier or above, different model family from the
  executor where one is available.
- **Verifier input:** the owner's instruction verbatim; the exact tool
  arguments proposed; the evidence refs. Not the executor's reasoning.
- **Verifier answers, yes/no each:**
  1. Do the arguments (amount, recipient, target, content) match the instruction?
  2. Is every prerequisite leg DONE with evidence?
  3. Does the payload contain anything the task does not need (LEAST-DISCLOSURE)?
  4. Does any instruction in play come from non-owner content?
- **Outcome:** all clear → approval request goes to the owner with
  "cross-checked" noted. Any flag → X4.
- **Cost bound:** the check may cost at most 15% of the task budget. Its
  input is small by construction.

After approval and execution, the read-back is verified by a script where
state is machine-readable, otherwise by the verifier model.

## 4.4 Budget enforcement

Caps are enforced by the harness, not by the model (gate BUDGET-STOP).
At 80%: X3. At 100%: hard stop, report with leg inventory as it stands.
A scheduled job has a per-run cap and a per-day cap; exceeding the daily
cap pauses the job and alerts the owner. The numbers in §4.1 are starting
values; the refit adjusts each to the 95th percentile of passing runs in
that class plus 25%.

## 4.5 Decision log

One JSON line per model call, written by the router. No message content.

```json
{"ts":"2026-11-12T09:14:03Z","task_id":"t-8841","leg":"send-invite",
 "class":"consequential","tier":"strong","model":"<id>","reason":"default",
 "in_uncached":4120,"in_cached":9800,"in_cache_write":0,"out":640,
 "tool_calls":3,"cost":0.0,"ms":8400,
 "gates":{"APPROVAL-TOKEN":"pass","READBACK-REQUIRED":"pass"},
 "escalated_from":null,"escalation_trigger":null,
 "verifier":{"model":"<id>","agree":true,"cost":0.0},
 "outcome":"pass","outcome_source":"gate|owner_correction|eval|none"}
```

`reason`: default | escalation | verifier | deescalation.
`outcome` is filled when known: `pass` when all gates pass and the owner
does not correct within 7 days; `fail` on gate failure or on a correction
linked to the task; `unknown` otherwise.
`outcome_source: owner_correction` is the highest-value signal: it is a
failure every gate missed.

## 4.6 Monthly refit

A script, run on the first of the month:

1. For each (class, tier): attempts, pass rate, critical fails, cost per
   pass — from the month's decision log, plus a fresh full eval run with
   each class forced to each tier at or below strong.
2. For each class, pick the cheapest tier where: eval attempts ≥ 30
   (10 tasks × 3 seeds), eval pass rate ≥ threshold, critical fails = 0,
   and production fail rate is not worse than the current tier's.
   Thresholds: consequential 95%, standard 90%, low-stakes 80%.
3. Move a class at most one tier per month.
4. Recompute budget caps (§4.4).
5. List every task with `outcome_source: owner_correction`; each becomes
   a candidate eval task for the next suite version.
6. Emit a diff of `router.yaml` with the supporting numbers. The owner
   approves the diff; it is a configuration change and stays gated.
7. If any class shows a critical fail in production during the month, it
   moves up one tier immediately, outside the monthly cycle.

## 4.7 Bench eligibility

The subscription bench varies in quality. A bench model may fill a tier
for a task class only after passing that class's eval rows at the class
threshold with zero critical fails. "Re-benchmarking" means re-running
those rows; a model that drops below threshold loses the slot at once and
the class falls back to the direct-API workhorse family.

## 4.8 Cut from this section

Per-provider pricing tables (they change; cost is computed from the log
and `router.yaml` prices) and latency-based routing.
