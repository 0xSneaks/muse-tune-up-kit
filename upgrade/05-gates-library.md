# 5. Verification Gates Library (kills F1, F2, F5, F7)

**Replaces:** prose doctrine ("verify before claiming", "a read-back beats
an exit code") that depends on the model recalling it.
**With:** 21 named checks, each bound to a hook point, each producing a
record.

## 5.1 Common contract

Hook points: `pre-tool` (before a call executes), `post-tool` (after it
returns), `pre-report` (before the final message is sent), `scheduled`.

Every gate run appends to `gate_log.jsonl`:

```json
{"ts":"…","task_id":"t-8841","leg":"send-invite","gate":"READBACK-REQUIRED",
 "result":"pass|fail|skip","evidence":"call-0042","detail":"sha match","action":"none|blocked|downgraded|escalated"}
```

A `skip` requires a reason from a fixed list (not-applicable,
tool-has-no-read-path, owner-waived-this-instance). Leg statuses are the
five in the kernel: DONE (needs an evidence id), PENDING, BLOCKED, FAILED,
NOT-ATTEMPTED. **A leg with no evidence id cannot be DONE**; the
pre-report hook rewrites it to PENDING.

Durability (pack §6, F7): the gate log, approval records, the idempotency
ledger, and checkpoint files live on disk under a path that survives VM
replacement, and are flushed before the action they guard is reported. No
gate may depend on in-memory state.

F6 has no gate. It is covered by kernel lines, eval category K, and the
lessons pipeline (`02-memory-os-v2.md` §2.8).

Mode: `code` = enforced by harness; `checklist` = injected procedure the
model follows, verified afterward from the trace.

## 5.2 The gates

### READBACK-REQUIRED — kills F1
- **Trigger:** post-tool, any call that creates or changes state.
- **Procedure:** read the target through a read path (not the write
  response). Compare to intent: hash for files; field-by-field for records.
- **Evidence:** read call id + comparison result.
- **Fail:** leg → FAILED on mismatch, PENDING if no read path exists
  (skip reason recorded). One automatic retry of the write, then stop.
- **Mode:** code.

### LEG-INVENTORY — kills F2
- **Trigger:** at plan time for any task with 2+ actions; again pre-report.
- **Procedure:** before acting, write the leg list (one leg per distinct
  state change or per recipient). Legs may be added during work, never
  removed. For bulk work the inventory comes from a source independent
  of the system under test: list the target state yourself; never take
  the item list from the tool or agent whose work is being checked. Pre-report: every leg has a status; counts match
  ("N of M" for batches, with failures named).
- **Evidence:** the inventory, with an evidence id per DONE leg.
- **Fail:** report blocked until the CLAIMS block matches the inventory.
  Summary words "done", "all set", "complete" are stripped unless every
  leg is DONE.
- **Mode:** code (pre-report), checklist (plan).

### MASKED-VALUE — kills F1, F2
- **Trigger:** post-tool, any returned value matching mask patterns
  (`****`, `••••`, `xxxx`, `…` inside a token, `[REDACTED]`, fixed-length
  repeats), or any field named key/secret/token/password.
- **Procedure:** tag the value `masked`. A masked value may be displayed
  as-is; it may not be written, sent, compared for equality, or used as
  an argument.
- **Evidence:** tag record with the field path (never the value).
- **Fail:** the dependent leg → BLOCKED, "needs a secure route"; no retry.
- **Mode:** code.

### TRANSPORT-VS-JOB — kills F1
- **Trigger:** any claim about a job, deploy, send, or background task.
- **Procedure:** answer three layers separately: (1) accepted — the
  request returned OK; (2) ran — the job's own status says finished;
  (3) worked — the output artifact exists and is sane (present, non-empty,
  fresh timestamp, expected shape). Only layer 3 supports "worked".
- **Evidence:** one evidence id per layer reached.
- **Fail:** report the highest layer evidenced, in those words
  ("accepted, outcome not yet verified"). Leg stays PENDING.
- **Mode:** checklist; code for registered jobs with a declared artifact.

### UNKNOWN-OUTCOME — kills F1, F7 (duplicate actions)
- **Trigger:** timeout, dropped connection, or ambiguous response on a
  non-idempotent call (send, pay, submit, post).
- **Procedure:** no retry. Check state by an independent route (sent
  folder, transaction list, published feed). Present → DONE, record the
  evidence. Absent → retry once with the same idempotency key. Cannot
  determine → stop.
- **Evidence:** the state-check call id; the idempotency ledger entry.
- **Fail:** leg → BLOCKED, owner told exactly what to check.
- **Mode:** code (ledger keyed on tool + argument hash).

### APPROVAL-TOKEN — holds the pack §6 gates
- **Trigger:** pre-tool, any tool in the gated set (spend, trade/transfer,
  public post, send-as-owner, deploy, delete, account/credential change).
- **Procedure:** look up an approval record whose action, destination,
  and amount/content hash equal the call's arguments, unused, issued by
  the owner channel in this task. Approval requests must carry the four
  fields; one request may batch several gates.
- **Evidence:** approval record id, marked used.
- **Fail:** call refused. Arguments differ from the approval → refused and
  a new request raised. Not escalatable.
- **Mode:** code.

### SOURCE-OR-SILENT — kills F1
- **Trigger:** pre-report, any factual claim about the world, a status,
  a price, a quote.
- **Procedure:** each claim carries a label: VERIFIED (evidence id from
  this task), INFERENCE (says what it is inferred from), UNKNOWN.
  A search snippet is not evidence for a page's content; the fetch is.
  Quotation marks only around fetched text.
- **Evidence:** the claims block.
- **Fail:** unlabeled claims are relabeled INFERENCE; a cheap-tier check
  ("does excerpt E support claim C?") downgrades unsupported VERIFIED
  claims.
- **Mode:** code (presence), cheap model (support check).

### FRESHNESS-STAMP — kills F4, F1
- **Trigger:** any answer or action built on a memory fact that is
  `stale`, or of a volatile predicate, or older than its TTL.
- **Procedure:** attach "as of <date>". For an action: re-verify from a
  live source first, or ask.
- **Evidence:** fact id + its date.
- **Fail:** the fact may not drive a gated action until re-verified.
- **Mode:** code.

### CONFLICT-SURFACE — kills F4
- **Trigger:** a `contested` fact is read.
- **Procedure:** state both values and their dates. For a gated action,
  ask the owner to pick; record the answer as an owner-correction.
- **Evidence:** both fact ids.
- **Fail:** silently choosing one = gate fail; leg BLOCKED.
- **Mode:** code.

### CORRECTION-SWEEP — kills F4
- **Trigger:** a fact is superseded. Procedure, evidence (the receipt),
  and fail behavior: `02-memory-os-v2.md` §2.4.
- **Fail:** residual hits > 0 without reasons → correction reported as
  PENDING, not done.
- **Mode:** code, with a cheap-tier pass.

### DEP-STAMP — kills F4
- **Trigger:** post-tool, creation of a goal, reminder, follow-up,
  scheduled job, or draft.
- **Procedure:** write the fact ids read during this leg to `deps.jsonl`.
- **Evidence:** the deps line.
- **Fail:** artifact still created; logged as `unstamped`; the weekly
  audit backfills by entity match.
- **Mode:** code.

### ARTIFACT-AS-PUBLISHED — kills F1
- **Trigger:** pre-tool, any publish/upload/set-artwork/attach.
- **Procedure:** open the final file by content, not by name. Images at
  legible size; every distinct frame of animations; full duration of
  audio/video. Confirm it is the intended content; run SECRET-SCAN and a
  private-data scan (names, emails, addresses, location metadata).
- **Evidence:** inspection record bound to the file hash.
- **Fail:** publish tool refuses a hash with no inspection record. The
  file changing after inspection invalidates the record.
- **Mode:** code (hash binding), checklist (inspection).

### SECRET-SCAN — kills C4
- **Trigger:** pre-tool on every write to memory, files, logs, outbound
  messages, and reports.
- **Procedure:** pattern and entropy scan (key prefixes, seed-phrase
  shapes, card and ID number formats, private-key blocks).
- **Evidence:** scan result (pattern class only).
- **Fail:** write blocked; owner told the secret was not stored and
  should be rotated if it was exposed.
- **Mode:** code.

### DATA-NOT-ORDERS — kills C5
- **Trigger:** post-tool, any content from web, files, email, images, or
  other agents.
- **Procedure:** wrap as untrusted. Scan for imperative text aimed at the
  agent; if found, record it and report it. Any tool call must trace to
  an owner instruction in this task; APPROVAL-TOKEN and the two-model
  check question 4 are the enforcement points.
- **Evidence:** provenance tag on the content; injection record if found.
- **Fail:** the suggested action is not taken; reported to owner.
- **Mode:** code (wrapping), checklist (tracing).

### LEAST-DISCLOSURE — constraint
- **Trigger:** pre-tool, any outbound payload to a person, service,
  search, or other agent.
- **Procedure:** list the fields the receiver needs to act. Remove every
  owner detail not on that list. Search queries carry no private details.
- **Evidence:** needed-fields list + payload field list.
- **Fail:** payload rewritten; if the task cannot proceed without a
  private detail, ask the owner.
- **Mode:** checklist; verifier question 3 in the two-model check.

### BUDGET-STOP — cost
- **Trigger:** 80% and 100% of the task's cap (`04-router-policy.md` §4.4).
- **Procedure / fail:** 80% → rule X3; 100% → hard stop, report the leg
  inventory as it stands.
- **Evidence:** token and call counters.
- **Mode:** code.

### WATCH-THE-WATCHER — kills F7, F5
- **Trigger:** scheduled; and on any "is everything healthy?" question.
- **Procedure:** every registered job and watcher writes a heartbeat.
  Health = each job's last heartbeat within its interval + grace, and its
  TRANSPORT-VS-JOB layer 3. The watcher's own heartbeat is checked by a
  second, independent schedule.
- **Evidence:** heartbeat table with ages.
- **Fail:** missing heartbeat is reported as "unknown, not healthy".
  "All healthy" requires every row green.
- **Mode:** code.

### JOB-TRIAGE-CLASSIFY — kills F5 (and F3: replaces the prose classification rules)
- **Trigger:** any non-success job run, before any verdict is stated.
- **Procedure:** a script over run history, four steps in fixed order.
  1. *Error origin.* Was the error text produced by the runner,
     scheduler, or network layer, or by the job's own output?
  2. *Change veto.* Any change to the job's config, prompt, credentials,
     dependencies, or host in the 24 hours before the first failure →
     class `change-suspect`. A transport verdict is not allowed until the
     change is ruled out.
  3. *Peer comparison.* Jobs sharing the same layer (runner, network
     path, provider) in the same window: peers failing too → `transport`
     or `shared-dependency`; peers healthy → `job-level`.
  4. *Persistence.* One failure followed by success → `flap` (logged, no
     alert). Three consecutive failures → incident.
- **Evidence:** the class plus one line of evidence per step.
- **Fail:** a step that cannot be answered → `unclassified`, reported in
  that word. Never default to `flap`.
- **Mode:** code.

### STARTUP-ALIVE — kills F7
- **Trigger:** session start, VM boot, and hourly.
- **Procedure:** for each entry in `workers.yaml` (relay, board poller,
  watchers): process alive, heartbeat fresh, backlog count (messages
  older than the entry's threshold).
- **Evidence:** the table, with ages and backlog counts.
- **Fail:** loud — it is the first line of the first reply, with how long
  the gap lasted. Restart the worker if restart is within standing
  permission; then process the backlog oldest first.
- **Mode:** code.

### CHECKPOINT-REQUIRED — kills F7
- **Trigger:** any job expected to run over 5 minutes or over 20 items.
- **Procedure:** write the work list to disk before starting. Append each
  completed item to a progress file with its evidence id. Side-effecting
  items go through the UNKNOWN-OUTCOME ledger. On start, read the
  progress file and skip what is done. A job type is trusted only after
  one passed resume drill (kill at a random point, restart, compare).
- **Evidence:** progress file path; resume-drill record for the job type.
- **Fail:** a job with no checkpoint may not be backgrounded; it runs in
  foreground chunks or is reported BLOCKED.
- **Mode:** code.

### CREW-REPORT-UNVERIFIED — kills F2
- **Trigger:** a sub-agent's or another agent's report is about to
  support a claim.
- **Procedure:** the report's claims are INFERENCE until spot-checked
  against target state: ids, hashes, timestamps. Check every item for
  consequential work; for bulk work, the larger of 3 items or 20%. The
  item list is taken from the target, not from the report.
- **Evidence:** spot-check call ids and the sample size.
- **Fail:** claims stay labeled "reported by crew, unverified"; any
  mismatch → check every item.
- **Mode:** checklist; code for the sample-size rule.

## 5.3 Gate-to-task map

| Gate | Eval tasks that must fail if the gate is removed |
|---|---|
| READBACK-REQUIRED | E1, E2, E6, J8 |
| LEG-INVENTORY | E3, E7, E10 |
| MASKED-VALUE | E8 |
| TRANSPORT-VS-JOB | E9, J1, J8 |
| JOB-TRIAGE-CLASSIFY | J5, J10, J11, J12 |
| STARTUP-ALIVE | V1, V5 |
| CHECKPOINT-REQUIRED | V2, V3 |
| UNKNOWN-OUTCOME | E4, E5, V3 |
| APPROVAL-TOKEN | G1, G3, G5, G11, E7, J3, V4 |
| SOURCE-OR-SILENT | R1, R2, R5, R8, R9, M8 |
| FRESHNESS-STAMP | R4, M5 |
| CONFLICT-SURFACE | M6 |
| CORRECTION-SWEEP, DEP-STAMP | M2, M3, M7, M10 |
| ARTIFACT-AS-PUBLISHED | G4 |
| SECRET-SCAN | M9, G8 |
| DATA-NOT-ORDERS | R6, J7, G2, G6 |
| LEAST-DISCLOSURE | G7 |
| WATCH-THE-WATCHER | J2, J9 |

Ablation test for the library: disable one gate, run its row; if the row
still passes, either the gate is redundant or the task is too easy. Fix
whichever it is.
