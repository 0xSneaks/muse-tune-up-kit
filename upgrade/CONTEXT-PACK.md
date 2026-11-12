# PASS A CONTEXT PACK — for Fable 5.2 (sanitized)
Prepared by Muse, 2026-11-12. Contains system architecture and measured baselines ONLY.
No personal data, no credentials, no keys, no wallet data, no private content of any memory file.

## 1. What Muse is
A personal agent running 24/7 on its own Linux VM for one operator. It has: a persistent
filesystem, long-term memory files, a task/goal tracking system, scheduled jobs (crons),
a browser, sub-agents it spawns for bounded tasks ("crew"), and a message board it uses to
coordinate with other AI agents (an evaluator, a repo-builder, a planner, etc.).
Its work pattern: contract (goal / done-when / plan / gates) -> execute -> prove by read-back.
Approval gates exist for: spending, trades, public posts, deploys, deletions, credential
changes. A standing permission covers routine git work.

## 2. Measured inventory (taken 2026-11-12, this machine)
- Standing context injected into EVERY conversation turn:
  - Operating rules file (AGENTS.md): 144,702 bytes / 279 lines  <-- dominant cost
  - Persona file (SOUL.md): 14,507 bytes / 141 lines
  - Live memory file (MEMORY.md): 22,247 bytes / 93 lines
  - Identity + user + tools files: ~7,000 bytes combined
  - TOTAL standing files: 188,428 bytes (~47k tokens estimated) before any user message
  - Plus a nightly alignment synthesis: 34,150 bytes, also injected
- Long-term memory tree: 25 MB, 134 markdown files
  - 41 dated daily logs, 48 person files, 39 group files, indexes for both
  - A lessons file: only 25 lines / 7 lessons captured across ~5 weeks of operation
- Skills (playbooks): 94 total — 57 system, 37 custom-learned
- Goals/projects: 131 goal workspaces on disk; 78+ tracked items in the goal system
- Agent coordination board: 730 handoff files accumulated
- Scheduled jobs: 31 user jobs, 24 enabled (snapshot 2026-11-12T05:00Z);
  at snapshot, 3 jobs had a non-success most-recent run
- Self-audit program: the operating rules file has been through 35 amendment rounds
  (v3.5.19) — almost all of its 144 KB is accumulated verification legislation

## 3. How work actually flows
- Main chat = direction/decisions. One side chat per project = execution.
- Background systems maintain memory, goals, and proactive briefings between sessions.
- Sub-agents ("crew") get one bounded task each, least context needed, no approval authority;
  their reports are treated as unverified until Muse spot-checks proof (IDs, hashes, timings).
- Models available for routing: a subscription API bench of many models (quality varies,
  re-benchmarked periodically), a direct-API workhorse model family, frontier models via
  a separate evaluator agent who is CREDIT-LIMITED and deliberately used sparingly.
- Verification doctrine (hard-won): never report a write as done from the first readout;
  read back target state; report multi-leg operations leg by leg; a masked read-back
  verifies presence, never value.

## 4. Baseline failure classes (the patterns that keep recurring)
F1. Premature "done" — claiming completion from a first readout / HTTP 200 / local edit
    without a read-back of the target state. Paid for repeatedly (batch writes reported
    done that had not landed).
F2. Folded claims — multi-leg operations reported as one claim; the unverified leg hides
    inside the verified ones. Inventories drawn from the system under test itself
    (self-report) treated as complete.
F3. Standing-context bloat — every lesson learned becomes permanent injected text; the
    rules file grew to 144 KB, taxing every turn, every sub-agent, every cron.
F4. Memory drift — stale facts in the live memory layer conflicting with newer decisions;
    corrections not always propagated to goals/reminders/queued work.
F5. Job-failure mis-triage — cron failure clusters misread as transport flaps (or vice
    versa); classification rules exist but are themselves a large chunk of the bloat.
F6. Communication slips — answering fragments while the operator is mid-task; filler on
    live calls; reflexive agreement with the operator's ideas instead of an independent
    verdict first. (7 lessons in 5 weeks = the lessons pipeline under-captures.)
F7. Continuity loss — a worker/relay not started silently eats messages for hours;
    long jobs interrupted by VM replacement need checkpointed recovery.

## 5. What "upgraded" must measurably mean (acceptance frame)
Against a frontier evaluator agent as the reference, on a suite of REAL operator tasks:
- Quality gap closed by >= 50% after Pass B, at a fraction of the frontier cost
- Standing-context bytes per turn cut materially WITHOUT losing failure-class coverage
  (F1-F7 must each still be prevented by something — a gate, a check, or a test)
- Every design output must be implementable and runnable by mid-tier models, not by Fable
- No design may weaken the approval gates or the read-back verification doctrine

## 6. Hard constraints for any design Fable proposes
- Approval gates are fixed: spend / trade / public post / deploy / deletion / credential
  changes always require the operator's explicit OK for that specific action.
- Secrets never appear in files, logs, prompts, or memory. Designs must preserve this.
- The operator is one person; any design requiring a team to operate it is a failed design.
- Everything must survive VM replacement: state on disk, jobs recoverable, no in-memory-only
  critical state.
