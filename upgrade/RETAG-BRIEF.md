# RETAG BRIEF — the real F-classes and baselines (from Muse, 2026-11-12)

The context pack is now in this folder as `CONTEXT-PACK.md`. The specs in this
folder were designed without it. This brief is the delta: what the pack
actually says, where the inferred meanings in `00-README.md` were wrong or
incomplete, and what to retag. Structures do not change; tags and two
coverage gaps do.

## Real failure classes (pack §4) vs. the inferred table in 00-README

| Class | Real meaning | Inferred meaning | Verdict |
|---|---|---|---|
| F1 | Premature "done": completion claimed from a first readout / HTTP 200 / local edit, no read-back of target state | Claim without proof | MATCH |
| F2 | Folded claims: multi-leg work reported as one claim; the unverified leg hides inside the verified ones; inventories drawn from the system under test treated as complete | Multi-leg work reported as done when a leg failed/skipped/unverified | MATCH |
| F3 | Standing-context bloat: every lesson becomes permanent injected text; 144 KB rules file taxes every turn | Standing-context bloat | MATCH |
| F4 | Memory drift: stale facts in the live layer conflicting with newer decisions; corrections not propagated to dependent artifacts | Memory conflict and stale facts | MATCH |
| F5 | **Job-failure mis-triage**: cron failure clusters misread as transport flaps (or vice versa); the classification rules themselves are a large chunk of the bloat | Wrong-layer evidence (transport success read as job success; masked value read as real value) | PARTIAL — the real F5 is specifically about *scheduled-job failure classification* (transport-layer failure vs. the job's own logic/inputs/permissions). The masked-value pattern belongs to F1/F2's evidence rules, keep it there. Retag F5 tasks/gates to job-triage: runner-generated error origin vs. job-output text, peer-job comparison on the same layer, change-correlation veto |
| F6 | **Communication slips**: answering fragments while the operator is mid-task or narrating a screen; filler/repeated status on live calls; reflexive agreement with the operator's ideas instead of an independent verdict first. Root cause is also structural: the lessons pipeline under-captures (7 lessons in ~5 weeks), so these recur | Treated as approval-gate / injection discipline | WRONG — gate/injection discipline is already covered by the constraints and F1/F2 gates; it is not F6. F6 needs its own coverage: eval tasks for fragment-discipline (do not answer incomplete input), verdict-first evaluation, and call pacing; and a lessons-capture mechanism in Memory OS v2 (an incident-to-lesson pipeline with a capture-rate check), because F6 recurs precisely when lessons are not captured |
| F7 | **Continuity loss**: a worker/relay process not started silently eats messages for hours (one real incident: 6.5 hours of unread messages); long jobs interrupted by VM replacement need checkpointed, resumable recovery; no in-memory-only critical state | Not designed against | GAP — needs design: (a) a startup/heartbeat gate — session-start check that coordination workers are alive, with a loud failure if not; (b) a checkpoint rule for any job over ~5 minutes (incremental output on disk, resume-after-replacement verified, not assumed); (c) eval tasks: worker-down detection time, and recovery-after-kill drills. Candidates: add to 05-gates-library (STARTUP-ALIVE, CHECKPOINT-REQUIRED) and to 01/02 as operating rules |

## Real baselines (pack §2 — replace design targets with these as the "before" numbers)

- Standing context injected per turn: **188,428 bytes total** — rules file 144,702 B /
  279 lines; persona 14,507 B; live memory 22,247 B; identity+user+tools ~7,000 B;
  plus a nightly alignment synthesis of 34,150 B also injected.
- Memory tree: **25 MB, 134 files** — 41 dated logs, 48 person files, 39 group files.
- Lessons file: **25 lines, 7 lessons in ~5 weeks** (the F6 capture-rate baseline).
- Skills: **94** (57 system, 37 custom).
- Goal workspaces: **131** on disk; 78+ tracked items.
- Coordination board: **730 handoff files**.
- Scheduled jobs: **31 user jobs, 24 enabled** (snapshot 2026-11-12T05:00Z);
  3 jobs had a non-success most-recent run at snapshot.
- Rules file amendment history: **35 rounds (v3.5.19)** — the bloat is accumulated
  verification legislation, which is why the diet must convert prose to executable
  checks rather than delete protections.

## Still missing (unchanged by this brief)

- §1 per-paragraph classification of the 144 KB file still cannot be done from
  the pack — the pack contains measurements and structure, not the file's text.
  The classification procedure in `01-context-diet.md` stands as the method;
  the manifest step (build order step 5) is where per-paragraph verdicts happen,
  on the machine that holds the file.

## Retag checklist

1. `00-README.md`: replace the ASSUMPTION table with the real classes above;
   mark F1–F4 MATCH, F5 CORRECTED, F6 REPLACED, F7 ADDED.
2. `03-eval-harness.md`: retag `guards` for F5 tasks to job-triage; add F6 tasks
   (fragment discipline, verdict-first, call pacing) and F7 tasks (worker-down
   detection, recovery drill). Keep the 50-task structure; additions extend it.
3. `05-gates-library.md`: retag `kills` lines for F5; add STARTUP-ALIVE and
   CHECKPOINT-REQUIRED gates for F7; confirm no gate claims F6 falsely — F6 is
   covered by eval tasks + the lessons pipeline, not by a gate.
4. `02-memory-os-v2.md`: add the incident-to-lesson capture pipeline (F6 root
   cause) with a capture-rate check in the weekly staleness audit.
5. Replace "design target" thresholds that the baselines above now supersede;
   keep the rest as targets for the baseline run (build order step 3).
