# UPGRADE-VERDICT — closers from the diatomic analysis

Sources: private corpus at `965981a`; public coordination repo at
`6e4a886`. Second edition, after the full-read run.

## Counts

| Item | Count |
|---|---|
| Registry rows ÷ atoms | 379 ÷ 379 = 100% (108 manifest atoms, 271 sub-atoms) |
| Rule atoms read in full | 220 of 220 |
| Custom skills read in full | 20 of 37; the other 17 measured by script |
| BLOCKED-ON-CORPUS | 59 (57 system skill bodies, the scheduled-job list, the goal workspaces) |
| Pair findings, system level (`PAIR-MAP.md`) | 59: 14 duplication, 13 contradiction, 11 dependency, 7 gap, 8 platform, 6 coordination |
| Pair findings inside the rules file and skills (`PAIR-MAP-RULES.md`) | 125: 65 contradiction, 27 duplication, 21 gap, 12 dependency. Each lane reported its 25 strongest, so this is a cap, not a census |
| Amendment chains | 37; 126,753 B raw, about 48,400 B after collapse (lane estimates) |
| Spec deltas | 33 (D1–D32 and D22a), one withdrawn |

## The verdict in six lines

1. The rules file is four tool-specific procedures (93.5% of rule bytes),
   not a general rulebook. It does not need to load on an ordinary turn.
2. Those procedures contradict themselves. The full read found 53
   contradictions inside the rules file: amendments that override text
   still present, rules filed under the wrong section, and at least two
   combinations that cannot be satisfied as written.
3. The same growth pattern is inside three large skills (about 85%
   amendment text), so moving rules into skills without collapsing them
   only moves the problem.
4. Muse already owns the loading mechanism (skills), a job runner, a
   health checker, an eval set and one working usage meter. The first
   specs re-designed four of those.
5. The runtime reportedly has no hook. Checks must be wrappers around
   scripts, snapshot checks, or after-the-fact audits.
6. F8 stands as its own class, narrowed to capacity that could have been
   read in advance. It hit this analysis: one read lane stopped on a
   usage limit with no second route.

## (a) Build order, in lanes and machines

Method, per the owner's directive: Muse is the single orchestrator;
builders run in parallel lanes on separate machines; a tool gets a
dependency card before a lane depends on it; visual work gets a mock
first; direct routes are preferred to metered wrappers. No new paid
account is assumed. **Only steps 1–3 are authorized to build.** The rest
is the plan.

Machines on hand, as far as the corpus shows:

| Machine | Use | Limits |
|---|---|---|
| VM | orchestrator; anything that touches live Muse state or personal data | 2 CPUs, 7.7 GB; per-session credentials; no parallel builders |
| Cloud coding sandboxes (the kind earlier tune-up runs and this session used) | stateless builder lanes on code with no personal data | no access to Muse's live state; the agents that drive them are metered |
| Phone | model route and test device only | reached through the tunnel with the outage record; **not a build lane** |

Lanes:

| Lane | Runs on | Driven by | Owns |
|---|---|---|---|
| O orchestrator | VM | Muse | board, integration, baseline, anything personal, the kernel diff |
| B1 builder | cloud sandbox | main coding agent | gates, wrappers, eval rig, auditor |
| B2 builder | cloud sandbox | second coding agent, different maker | router, analyzer, chain-collapse drafts |
| R reviewer | chat | a different maker from the lane under review | verified / rejected on each lane's proof |
| F frontier | metered | evaluator agent | reference run and one chain attack; scheduled against its meter |

| Step | Work | Lane | Days | State |
|---|---|---|---|---|
| 0 | Dependency cards for the runtime: hook surface, context per crew and job, who injects the synthesis file, each machine's auth lifetime | O | 0.5 | open |
| 1 | Gates library | B1 | done | `d3c7684`; follow-ups D8–D11, D29: 2 days |
| 2 | Eval rig, 15 smoke tasks | B1 | done | `d3c7684` |
| 3 | Baseline on the live system, frozen | O | 1 | blocked on Muse's machine |
| 4 | Remaining tasks: J13–J16, K7, categories W, Q, B; judge mutation test | B1 | 7 | plan |
| 5 | Rulings on 4 unresolved pointers and 2 unsatisfiable combinations | O + owner where a protection changes | 0.5 | plan |
| 5b | Chain collapse: 37 chains, drafts by B2, each attacked by R against its regression cases (one per contradiction row) | B2 → R | 7 | plan |
| 6 | Wrappers and snapshot checks; auditor job; triage classifier from A-035; PLATFORM-METER | B1 | 4 | plan |
| 7 | Five rule skills from the collapsed chains, one per commit | B2 → O | 3 | plan |
| 8 | Kernel diff: 3.5 KB verbatim plus trimmed lines | O → owner | 1 + review | owner-gated |
| 9 | Ledger; backfill from person and group files | O | 3 | plan |
| 10 | DEP-STAMP, CORRECTION-SWEEP, resurrection guard | B1 → O | 3 | plan |
| 11 | Consolidation, staleness audit, lessons pipeline, standing orders out of LIVE | O | 4 | plan |
| 12 | Router table in the routing skill: second route, data class, spend-gated escalation | B2 | 3 | plan |
| 13 | Full suite; head-to-head | O + F | 2 | plan |
| 14 | Statement mock approved, then the export analyzer | B2 | 2 | plan |
| C | Coordination repo changes, as one request to the deciders | deciders | 2 | plan |

About 54 working days of lane time; with B1 and B2 in parallel, roughly
30 calendar days after step 3. Lanes B1 and B2 never touch the same
files: B1 owns `upgrade/build/`, B2 owns the skills and the router.

## (b) Top 3 risks the pair pass found — bond risks

1. **Collapsing rules that fight each other.** 53 contradictions, a
   set of atoms under the wrong heading, 4 pointers that lead nowhere, 19 chains
   marked "collapse with care". Each chain's table row names the
   protection a careless merge would drop. A collapse that resolves a
   contradiction the wrong way weakens the verification doctrine while
   looking like a clean-up. The guard is step 5b's rule: no chain ships
   without a regression case per contradiction and a reviewer from a
   different maker.
2. **Rules whose carrier is a hook that does not exist.** A rule removed
   from standing context and "replaced by a gate" is replaced by nothing
   if the gate cannot attach. Of the 74 atoms the lanes marked as
   checkable, each must be assigned wrapper, snapshot or audit before its
   prose leaves. The same bond exists in the coordination layer: warnings
   that nobody must clear (P-B3).
3. **Everything that matters hangs on a few metered routes.** The main
   model route, the reviewer who accepts work, the delegated approval for
   submissions, and the head-to-head reference each have one route and no
   meter check. A limit on any one stops a class of work, and the
   coordination rule's own remedy (sign off before the limit) cannot be
   obeyed without a meter.

Carried from the first edition and still true: the 16 KB target depends
on who owns the 34 KB synthesis file and on four owner-locked persona
sections.

## (c) What Pass B tests first

1. **The hook question**, on Muse's machine: try to intercept one native
   tool call and one reply.
2. **One chain end to end**: the claim-release chain in the on-chain
   domain. Collapse it, run its regression cases, and let the frontier
   evaluator attack the result against the original atoms.
3. **The two unsatisfiable combinations** the media lane found (A-186
   with A-198; A-214 with A-198): confirm on a real file that no
   procedure satisfies both, then rule.
4. **The triage rule as code** over 30 days of real job history.
5. **A meter drill**: start a long job with a meter above its warning
   threshold and confirm the sign-off-first behavior (Q1, B5).
6. **Check-in cost**: time and tokens for one check-in reading the whole
   board against one using the inbox command.
7. **Rebuild the manifest by script** and diff it against the one Muse
   wrote (131 / 134 / 135 files).

## (d) Still blocked, and still unread

| What | Count | Unlocks with |
|---|---|---|
| System skill bodies | 57 | their text, or confirmation they are platform-owned |
| Scheduled-job list | 31 jobs | name, schedule, purpose, last status per job |
| Goal workspaces | 131 | a list with last-touched dates |
| Market-data skill bodies (not read; measured) | 17 | re-running one read lane once the usage limit resets |
| Personal files and the memory tree (structure only, by design) | 5 files + 129 files | stays on Muse's machine; spec 02's backfill does the per-file work |

## Calibration

First edition, before the full read: I classified 184 rule atoms from
their titles. The full read kept the domain split but changed the
picture inside it: 4 dead atoms instead of 1, 53 contradictions instead
of 16 known replacements, and a collapse estimate of 38% where I had
guessed 40–60%. One of my own first-edition findings was wrong (the
shared preamble in the market-data skills: 2.5%, not a merge candidate).
The step-1 code I built has a real defect found by running it on the
memory tree (D29). Treat the lane outputs the same way: they are one
read each, unreviewed by a second model, because the usage limit that
stopped one lane also left no room for a review pass.
