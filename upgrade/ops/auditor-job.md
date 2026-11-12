# Auditor job — spec (step 6, SPEC-DELTA D1 AUDITED class)

**Status: SPEC ONLY.** Not installed. Installing it is a live-cron change
and needs the owner's word like any other scheduled job. This spec is the
artifact step 6 owes; nothing here runs yet.

## Why it exists

D1 (confirmed by MUSE-SIDE-REPORT §A1): the runtime has no pre-tool or
pre-reply hook, so gates split into ENFORCED-WRAPPER, ENFORCED-SNAPSHOT
and AUDITED. AUDITED gates cannot prevent anything — they guarantee
*detection*. The auditor is the detection half: it re-reads the day's
gate logs and flags what the wrappers let through or never saw.

## Schedule and tier

- **Every 15 minutes**, shadow mode (see Limits). Workhorse tier — the
  job is log arithmetic, no judgment model required; ambiguous entries
  are flagged, not resolved.
- Runtime budget: one pass over the state directory's JSONL files;
  incremental by byte offset recorded in its own state file, so a pass
  never re-reads history it already reconciled.

## Inputs (read-only)

From the gates state directory (the `muse_gates` store root):

- `gate_log.jsonl` — every gate verdict the wrappers and GatedTools wrote
- `approvals.jsonl` / `approvals_used.jsonl` — owner approvals and their
  consumption
- `ledger.jsonl` — non-idempotent call outcomes (UNKNOWN-OUTCOME)
- `inventory.jsonl` — declared leg inventories

## Reconciliation rules

One finding per unreconciled entry. An entry is unreconciled when:

1. **Spend** — an APPROVAL-TOKEN `pass` whose approval id never appears
   in `approvals_used.jsonl`, or a gated spend-class call in the gate
   log with no APPROVAL-TOKEN row at all in the same task.
2. **Merge** — a merge-class call recorded as executed with no approval
   row and no standing-grant scope match noted in its gate-log detail
   (standing grants are D10 records; a merge under one must name it).
3. **Credential** — any SECRET-SCAN `pass` on a credential-class tool, or
   a credential action (key create/rotate/revoke) with no gate row:
   credential actions must never be silent.
4. **Public send** — a send-effect call whose destination is public
   (per the tool metadata the runtime supplies) with no SECRET-SCAN row
   in the same task, or a SECRET-SCAN `fail` (blocked) that is followed
   in the same task by a successful send of the same payload hash —
   that pair means something routed around the wrapper, and it is the
   highest-severity finding this job can write.

Entries the wrappers blocked (`action: "blocked"`) are reconciled by
construction and never findings. Findings carry the gate-log record's
own fields (task, gate, timestamps, evidence ids) — never secret values;
the gate log stores pattern classes only, and the auditor adds nothing
more sensitive than what it read.

## Output

- Appends findings to `auditor_findings.jsonl` in the same state
  directory (append-only; LEDGER-APPEND-ONLY applies to the auditor's
  own writes when it is wired through the wrapper).
- A daily rollup line in the same file at 00:05 ET: counts by class,
  oldest unreconciled age. No prose report, no chat message.

## Limits (shadow mode — the point of the spec)

- **Writes findings only.** It never edits the gate log, never marks an
  entry reconciled, never retries or reverses an action.
- **Pages nobody.** No chat delivery, no notification, no escalation
  channel. A human (or the orchestrator, in session) reads the findings
  file; promotion out of shadow mode — paging, blocking, a health-check
  row — is a separate owner decision, not part of this spec.
- **Installs nothing.** It does not register itself, patch the health
  checker (which has no worker registry — MUSE-SIDE-REPORT E3), or
  touch any other job.
- Exit codes: 0 = pass complete (findings or none), 1 = pass complete
  with findings written, 2 = the auditor itself failed (missing/corrupt
  input); a 2 is recorded in its own state file, not delivered.
