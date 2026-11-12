# MUSE-SIDE REPORT — Muse's half of the upgrade (2026-11-12, ~01:20 ET)

Read-back first, with two corrections to the tasking block:
- **Registry: 379 rows VERIFIED** by the registry's own accounting (108 manifest atoms + 271 sub-atoms; per-section counts match the section headings: 220 rule atoms, 19 persona, 94 skills, rest sections).
- **Tests: 15 passing, not 16.** `python3 -W error -m unittest discover -s tests` → "Ran 15 tests, OK" (12 in test_gates.py + 3 in test_harness.py). The build README itself says 15. The block's "16" is wrong by one.
- Branch pulled to `8ac7e91`. Everything below is committed locally; nothing pushed (push rule unchanged).

## A. Three answers (step 0) — all tested, none recalled

**A1. Intercept a tool call / a reply: NO — VERIFIED.**
Test: enumerated my full tool surface and the hooks registry (empty). Hooks on this platform are poll-and-wake automations only (a script polls a condition, wakes an agent) — there is no pre-tool or pre-reply event type to register. The only interception that exists is the platform's own approval-card system on flagged actions, which I neither control nor install. Conclusion: D1's premise is correct — gates are ENFORCED-WRAPPER (script-mediated actions), ENFORCED-SNAPSHOT, or AUDITED. Nothing else is available.

**A2. Crew / scheduled jobs with less standing context: NO — VERIFIED.**
Test: spawned a probe lane with a measurement brief. It received all 9 standing files (AGENTS, SOUL, TOOLS, IDENTITY, USER, MEMORY, both indexes, ALIGNMENT_SYNTHESIS — the same ~222,578 B) plus a compaction summary and forked transcript. Not the brief alone, not less. Scheduled-job workers show the same injection (tonight's cron handoffs carried the same standing files). No reduced-context mode exists that I can select. The 2 KB crew kernel in spec 01 is not buildable from my side today.

**A3. The 34 KB synthesis file: the PLATFORM writes and injects it; I cannot remove it — VERIFIED.**
Evidence: it lives in the runtime-managed `~/dreams/alignment/derived/` beside platform state files; mtime 2026-11-11 19:33 ET (nightly cadence, no session of mine ran it); none of my 31 user jobs produces it (full job list enumerated for D1); the A2 probe lane received it too, i.e. it is injected at session construction. No tool or setting available to me removes or shrinks it. **D16 therefore resolves:** the acceptance line is "Muse-controlled standing bytes ≤ 16 KB", with the platform's 34,150 B reported alongside, outside the budget.

## B. The baseline (step 3): BLOCKED — one decision is Sneaks's

The rig works on this machine (scripted reference agents run; careful + gates-on passes, re-run tonight). The adapter cannot be built as specced:
1. There is **no callable endpoint for my own model** on this machine. I am a platform session, not an API; no key or route for Muse's model exists in my environment or connectors.
2. The only local model CLI is Claude Code (`claude`), which is a **different agent** with its own context — not "Muse's normal model with Muse's unmodified standing context" — and it runs on Sneaks's Claude meter: **weekly at 91%** (claude-eyes, 2026-11-12 00:44 ET). 45 runs × ~222 KB of standing context would burn a large share of what is left before Saturday's reset, and Claude is benched by Sneaks's standing order except when he orders it in per-task.
No adapter file was written — a shell that cannot call the model would be theatre.
**What Sneaks must do (one line):** authorize a capped Claude-CLI baseline by name (e.g. "baseline, 1 seed, gates off") or leave step 3 parked until a platform route to my own model exists. The gates-on second run is not started; it depends on the first.

## C. Rulings

**C1. The four pointers:**
- A-050 → "run-17 v3.5 precedence clause": **DEAD as a pointer.** No such labeled clause remains in the file. Its operative content (later, more specific wording supersedes earlier general wording on inventories) survives inside the v3.5.17+ bullets themselves. Collapse treats A-075 as the sole bar (matches R-039/R-092).
- A-177 → "aggregate-deviation principle": **DEAD as a pointer; A-177 is self-contained.** No atom carries that name (nearest is A-063, a different rule). A-177's own sentence — bounds apply to the total effect on the user — IS the principle. Collapse keeps the sentence, drops the reference.
- A-156 → "sibling-clause floor": **MEANT something; wording fix.** It pointed at the sibling continuing-leg clause's 24 h re-observation interval, mislabeled a "floor" (R-077). On collapse it reads "interval of at most 24 h", with the v3.5.21 deferral cap (3 cycles / 7 days) carried into the same sentence (R-051).
- A-213 → "v3.5.19 vantage bullet": **DEAD as labeled — off-by-one version.** No vantage bullet exists under v3.5.19. The target is the v3.5.20 audience-vantage bullet (the A-191/A-195 family), as qualified by v3.5.21. Retarget on collapse.

**C2. The two combinations — CONFIRMED unsatisfiable on real files; ruling proposed, NOT applied (it drops a protection, so it is Sneaks's):**
- A-186 + A-198 (stills), on `table-kit.png` (real, 244,467 B): A-198 sweeps alone = 360 evaluations per image (72 rotation steps × 5 level settings, one control pair). Compositions of any depth over a 6-transform set: depth ≤ 3 alone = 258 sequences × 360 = **92,880 evaluations per image**, and depth is unbounded as written — the leg cannot terminate, by construction.
- A-214 + A-198 (identifier-class video), on a real avatar clip (8.0 s, 24 fps, 192 frames, ffprobe): exhaustive frames × full sweeps = 192 × 360 = **69,120 evaluations for 8 seconds**, before any compositions.
- **Proposed ruling:** stills get the closure video already has — a recorded budget: compositions to depth 2 over the named transform set, continuous sweeps on the base image and flagged outputs only. Identifier-class video: exhaustive *viewing* of every frame; transforms and sweeps only on scene-change and flagged frames. This narrows two protections → **Sneaks decides; nothing is applied.**

**C3. SPEC-DELTA D1–D32 (+D22a): ACCEPT all, with three notes.**
D1 ACCEPT (proven by A1). D2 ACCEPT. D3 ACCEPT as revised by the full-read run (37 chains, ~48,400 B after collapse). D4 ACCEPT (regression case per R-row, not 16). D5 ACCEPT. D6 ACCEPT — the kernel diff is an owner change and comes to Sneaks as one diff; nothing applied by me. D7 ACCEPT as revised (the board's label set wins on the board). D8–D15 ACCEPT. D16 ACCEPT as resolved by A3 (see above). D17–D20 ACCEPT. D21 ACCEPT its withdrawal (the session's own correction). D22, D22a ACCEPT. D23 ACCEPT. D24 ACCEPT. D25 ACCEPT. D26 ACCEPT. D27 ACCEPT. D28 ACCEPT (already the owner's directive; addendum applied in this run's method). D29 ACCEPT — tighten SECRET-SCAN before it guards any memory write. D30 ACCEPT. D31 ACCEPT. D32 ACCEPT — filed as E4 below.
No REJECTs: every delta I could test from this machine checked out; the rest are forced by pair evidence I spot-verified (R-039, R-051, R-070, R-072, R-077).

## D. What only this machine has — sanitized, counts and structure only
Files in `upgrade/diatomic/muse-side/` (committed locally with this report):
- **D1 jobs:** 31 user jobs, 24 enabled — name, enabled, interval, last run, last status per job (`D1-jobs.md`, from cron.list + the health snapshot).
- **D2 goals:** 132 goal workspace dirs with last-touched dates (`D2-goals.md`). The analysis said 131 — the script counts 132 today; one more than the pack-era count, scope/recency, not a lost workspace.
- **D3 skills:** 57 system skills are **platform-owned — VERIFIED** (write test on a system SKILL.md: not writable; `/opt/muse/skills` is read-only and replaced on deployment). 37 custom skills are mine/Sneaks's to edit. Total 94 — this unblocks the 57 BLOCKED-ON-CORPUS rows: their verdict is platform-owned, KEEP-AS-IS, not Muse's to change.
- **D4 memory counts (counts only):** MEMORY.md "Standing orders" = 19 bullets: 16 rule-like, 3 fact-like. "Money, wallets, trading" = 16 bullets: 12 rule-like, 4 fact-like. (Heuristic: imperative/prohibition markers. Method stated; no content reproduced.)
- **D5 manifest diff:** script recount = **135** .md files in the memory tree (full recursive, including runtime-managed bank/index). 131 and 134 were narrower authored-tree scopes at earlier dates. Diff is a scope definition, not missing files — but the manifest never stated its scope, so its inventory stands UNVERIFIED under D8 until the scope line is added (`D5-manifest-diff.md`).

## E. AI COMS
- **E1 check-in cost — MEASURED:** full BOARD.md read = 183,293 B (~46k tokens). `python3 tools/coms_check.py --inbox muse` output = 38,587 B (~9.6k tokens) — **~79% smaller per check-in**, and it is what I now use. (Counting note: coms_check reports 62 OPEN requests to muse incl. "all"; MUSE-MODEL's 24 + 39 split counts differently — requests vs lines.)
- **E2 claims/requests: PARTIAL — not bulk-cleared, deliberately.** Tonight's triage: 15 Muse claims on the board (18 lines incl. duplicates), 7 marked DONE; 62 OPEN requests to muse/all, none newly actionable (all gated, predecessor-gated, or parked — verified again at 00:59 ET). Bulk-editing a 183 KB board to "clear" claims tied to live projects (e.g. the cherry-holdem claim, whose portal leg is still open) would be the F1/F2 failure in a new costume. Ruling: DONE claims release at each project's sign-off; live claims stay with a status line. **Blocker for a full clear: a per-claim pass with each claim's project state in hand — one work session, not a sweep.**
- **E3 relay + checker schedule: schedule VERIFIED installed; relay NOT added — scope.** `muse-health-watch` runs every 15 min on my cron list and ran all night (the repo's SCHEDULE.md still says "spec only, not installed" — that text is stale). But `health_check.py` has **no worker registry**: its checks are three hardcoded functions (maestro, bridge, crons). Adding a relay check is a code change in step-6 territory (wrappers/snapshot checks), outside the steps 1–3 authorization. Not built; named here as the blocker.
- **E4 decider request — DONE, VERIFIED.** One request to the deciders covering all six MUSE-MODEL §3 changes, filed on BOARD.md (Requests, line 431) — ai-coms commit `ae69d88`, pushed via the API wrapper: **PUSH COMPLETE**, remote main updated to `ae69d88` on top of `6e4a886`. I did not apply any of the six changes myself.
- **E5 usage files — DONE, same commit.** `usage/deepseek.md` (routes, states, where each meter lives) and `usage/muse-crew.md` (no external meter; lanes cost the same standing context as main — A2's measurement) added beside `usage/claude.md`, pushed in `ae69d88`.

## Scoreboard
VERIFIED: read-back (379 rows; 15 tests), A1, A2, A3, C1 (4 rulings), C2 (both confirmed), C3 (D1–D32 ruled), D1–D5, E1, E4, E5.
BLOCKED: B (baseline) — needs Sneaks's one-line route authorization. E2 (full clear) — needs a per-claim pass. E3 (relay check) — outside steps 1–3 scope.
Not started, per the order: module extraction, kernel cut.
