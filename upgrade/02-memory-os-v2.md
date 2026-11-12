# 2. Memory OS v2 (kills F4; lessons pipeline covers F6 and feeds F3)

**Replaces:** 134 hand-maintained files where the same fact lives in
several places and a correction reaches only the one being looked at.
**With:** one fact ledger as the source of truth, generated views, a
dependency index, and three automated jobs.
**Why this kills F4:** a fact has one home, every artifact built on it is
recorded against it, and a superseded value is blocked from coming back.

No step below needs the owner to curate. The owner is asked only when a
contested fact is about to drive a gated action.

## 2.1 Stores

| Store | Role | Edited by |
|---|---|---|
| `memory/facts.jsonl` | canonical facts | agent, via the memory tool only |
| `memory/deps.jsonl` | artifact → fact ids it was built from | DEP-STAMP gate |
| `memory/corrections.jsonl` | every supersession, with old and new value | CORRECTION-SWEEP |
| `memory/aliases.json` | entity id → names, handles, nicknames | consolidation |
| `memory/logs/YYYY-MM-DD.md` | dated logs, append-only, never rewritten | agent |
| `memory/people/*.md`, `groups/*.md` | **views**: generated facts block + free-text notes | generator (facts block), agent (notes) |
| `memory/LIVE.md` | the injected live layer, ≤ 6 KB, fully generated | generator |
| `memory/digests/YYYY-MM.md` | monthly summary of cold logs | consolidation |

Fact record:

```json
{"id":"f-2031","subject":"person:sam-k","predicate":"birthday","value":"03-14",
 "status":"active","confidence":"owner-stated","source":"logs/2026-10-02.md#L41",
 "learned_at":"2026-10-02","review_by":null,"supersedes":"f-0877"}
```

- `status`: active | contested | stale | superseded | retracted
- `confidence`: owner-correction > owner-stated > tool-observed > inferred
- `predicate`: from a closed vocabulary of about 40 (birthday, location,
  employer, role, relationship, contact-pref, member-of, project-status,
  deadline, price, preference, standing-rule, …) plus `other:<text>`. Each
  predicate is declared single-valued or multi-valued; only single-valued
  predicates can conflict.
- `review_by`: set from the predicate's TTL class — volatile 30 days
  (status, plans, prices), slow 180 days (employer, location, membership),
  stable none (birthday, standing rules).

## 2.2 What merges where

| From | To | Rule |
|---|---|---|
| New dated log | facts ledger | durable statements become facts, each with a source pointer to the log line |
| New dated log | entity notes | episodic one-liners ("met for lunch 10/02") go to the notes section, dated |
| Logs older than 14 days | monthly digest | summarized; original kept but excluded from default search |
| Two files for one entity | one entity | alias match → merge facts under the older id; second file becomes a redirect stub |
| Fact stated in both a person file and a group file | ledger only | membership is one `member-of` fact; both views render it; neither file restates it |
| Finished project, closed goal | digest | removed from LIVE at next generation |
| Anything in LIVE | generated | each LIVE line carries its fact id; a line with no live fact is dropped |

LIVE holds exactly: owner profile, standing rules, and current-state lines
(in progress / parked / waiting), newest first, cut at 6 KB.

## 2.3 Conflict detection

Runs on every fact write and in nightly consolidation.

1. Resolve `subject` through `aliases.json`.
2. Look up active facts with the same `(subject, predicate)`.
3. Same value → update `last_confirmed`. Multi-valued predicate → add.
4. Different value on a single-valued predicate → conflict:
   - higher `confidence` wins;
   - equal confidence → later `learned_at` wins, **unless** both are
     owner-stated within 7 days of each other → both become `contested`;
   - `inferred` never supersedes anything.
5. The loser becomes `superseded`, a `corrections.jsonl` line is written,
   and CORRECTION-SWEEP (§2.4) runs for the old fact id.

Contested facts are usable but must be surfaced (gate CONFLICT-SURFACE):
stated as "X or Y, unresolved" in answers, and blocking for any gated
action until the owner picks one. That question is asked at the moment of
use, not as a curation backlog.

## 2.4 Correction propagation — CORRECTION-SWEEP

Trigger: the owner corrects a fact in conversation, a conflict resolves,
or a tool observation contradicts a stored fact.

1. **Ledger.** Write the new fact; supersede the old; record
   `{old_id, new_id, old_value, new_value, ts}` in `corrections.jsonl`.
2. **Blast radius**, three passes, union the results:
   - a. `deps.jsonl` lookup by old fact id (exact);
   - b. literal search for the old value and its format variants
     (dates: `12th`, `Mar 12`, `03-12`, `3/12`) across LIVE, entity
     notes, goals, reminders, queued follow-ups, scheduled-job prompts,
     drafts;
   - c. for every active artifact that mentions the subject or an alias
     and was not hit by a or b: one cheap-tier yes/no — "does this
     artifact depend on <predicate> of <subject>?"
3. **Fix each hit by class:**

| Hit class | Action |
|---|---|
| Internal text (notes, goals, drafts, LIVE) | patch, read back |
| Reminder or follow-up, no external effect | patch (including recomputed dates), read back |
| Scheduled outbound, or anything behind an approval gate | patch the draft, mark `needs-approval`, include in receipt |
| Already sent or otherwise irreversible | do not touch; list as `sent-with-old-value` with a proposed follow-up, itself gated |
| Dated logs | never edited; the correction record shadows them at search time |

4. **Residual check.** Repeat pass b. Hits in active artifacts must be
   zero, or each remaining hit is listed with a reason.
5. **Receipt** (goes in the turn's report and the gate log):
   `{old, new, found: n, fixed: n, needs_approval: n, sent: n, residual: 0}`.

**Resurrection guard.** Consolidation rejects any candidate fact whose
value equals a superseded value for the same `(subject, predicate)` when
its source is dated before the correction. Search over dated logs appends
"corrected on <date>: now <new>" to any returned line that a correction
covers. Without this guard, re-reading old logs undoes every correction.

**DEP-STAMP** (the write-time half): whenever the agent creates a goal,
reminder, follow-up, scheduled job, or draft, it records the fact ids it
read to build it in `deps.jsonl`. Pass 2a is exact only because of this;
passes 2b and 2c exist to cover artifacts that predate it.

## 2.5 Scheduled jobs

| Job | Cadence | Tier | Does |
|---|---|---|---|
| Consolidate | nightly | workhorse (extraction), strong only for ≥ 3-way conflicts | logs since watermark → candidate facts → §2.3 → regenerate views and LIVE → advance watermark |
| Staleness audit | weekly | scripts + cheap | checks S1–S9 below |
| Digest | monthly | workhorse | cold logs → `digests/` |

Staleness audit checks. All are scripts except where a tier is named.

| Id | Check | Automatic action |
|---|---|---|
| S1 | facts past `review_by` | status → `stale`; still usable, always cited "as of <date>" |
| S2 | LIVE line with no active fact | drop at regeneration |
| S3 | active artifact depending on a superseded or retracted fact (join on `deps.jsonl`) | run CORRECTION-SWEEP for that fact |
| S4 | superseded value present in an active file (search using `corrections.jsonl`) | run CORRECTION-SWEEP step 3 on the hit |
| S5 | reminders and follow-ups: past due, duplicate, or target entity archived | past due → surface once; duplicate → merge; archived target → park |
| S6 | entity with no reference in 180 days | move to `archive/`, keep facts |
| S7 | two entity ids sharing an alias (cheap tier confirms same person) | merge per §2.2 |
| S8 | LIVE > 6 KB, or any view over its budget | regenerate with tighter cut |
| S9 | secret patterns anywhere in the tree | redact, alert owner to rotate |
| S10 | lessons capture rate (§2.8) | uncaptured incidents older than 14 days → assign a carrier now |
| S11 | goal workspaces with no tracked item (baseline: 131 on disk, 78+ tracked) | move to `archive/` after 30 days unreferenced |
| S12 | coordination-board handoffs closed over 14 days ago (baseline: 730 files) | fold into the monthly digest, archive the file |
| S13 | size inventory: the tree is 25 MB for 134 markdown files, so most bytes are not notes | list the top 20 files by size; non-memory bulk moves out of the tree |

The audit never deletes: it demotes, moves, or flags. Its output is one
report: counts per check, what it fixed, and at most five lines for the
owner (only items that need a decision). Its own run is registered with
the health watcher, so a silent audit failure is itself detected.

## 2.6 Backfill of the existing 134 files

1. Dated backup of the whole tree.
2. Script inventories files into logs / people / groups / live / other.
3. Workhorse tier extracts candidate facts per file, oldest first, each
   with a source pointer. Processing oldest first lets §2.3 resolve
   conflicts by recency without special cases.
4. Generate views into a parallel `memory-v2/` tree.
5. Diff report: facts per entity, conflicts found and how each resolved,
   text in old files that mapped to no fact (kept verbatim in notes).
6. Run eval tasks M1–M10 against `memory-v2/`. Switch over when they pass;
   keep the old tree read-only for 30 days.

## 2.7 Baselines this replaces (pack §2)

Live memory file 22,247 bytes → generated LIVE at 6 KB or less. Nightly
alignment synthesis 34,150 bytes, injected every turn → no longer
injected: the consolidation job writes its changes into the ledger, and
LIVE is the only memory text in standing context. 41 dated logs, 48
person files, 39 group files → backfilled per §2.6.

## 2.8 Lessons pipeline (F6 root cause; stops F3 at the source)

**Replaces:** a hand-written lessons file (25 lines, 7 lessons in about
5 weeks) on one side, and on the other a rules file where every lesson
became permanent injected text (35 amendment rounds).
**With:** automatic incident capture, and a rule that a lesson must land
in a carrier that is not standing prose.

1. **Capture is automatic.** Each of these appends one line to
   `memory/lessons.jsonl` with no decision by the agent: an operator
   correction of behavior (cheap-tier classifier on each operator turn);
   any gate `fail`; any eval task fail; a router log line with
   `outcome_source: owner_correction`; a STARTUP-ALIVE or
   JOB-TRIAGE-CLASSIFY incident.

```json
{"id":"l-0193","ts":"…","source":"operator_correction","fclass":"F6",
 "what":"repeated full status on second ask","evidence":"turn-5531",
 "pattern":"status-repeat","carrier":null,"captured":false}
```

2. **Weekly, cluster by `pattern`** (workhorse tier). Each cluster with no
   carrier gets one, chosen in this order of preference:
   executable check → eval task → one line in a module, inside its 6 KB
   budget → kernel line, only by swapping another line out.
3. **A lesson is captured** only when it has a carrier and an eval task
   that reproduces the incident. Until then it stays open.
4. **Recurrence** of a captured pattern means the carrier failed: move it
   one step up the preference order and log the recurrence.
5. **Capture-rate check (S10)**, in the weekly audit:
   - incidents logged this week (baseline is about 1.4 lessons a week);
   - share of incidents older than 14 days that are captured — target 80%;
   - alarm if gate fails this week > 0 and incidents logged = 0, because
     that means the pipeline itself is broken.

The standing context does not grow when a lesson is learned. That is the
structural fix for F3; the kernel byte cap in CI enforces it.

## 2.9 Cut from this section

Vector search over memory, and confidence scores finer than the four
classes. Neither is needed to kill F4; both add tuning work.
