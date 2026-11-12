# PAIR-MAP — where the atoms duplicate, contradict, depend, or leave gaps

Ids are from `ATOM-REGISTRY.md`: A = rules file, P = persona section,
M = live memory section, Y = synthesis section, L = lesson, S = skill,
F/G = manifest atoms. Six atoms below are not in the manifest; they are
existing tools in the private repo and are given X ids:

| Id | Existing asset (private repo, outside `corpus/`) | State per its own document |
|---|---|---|
| X-1 | checkpointed job runner | built, unit-tested |
| X-2 | health checker and its schedule | checker built; schedule marked "spec only, not installed" |
| X-3 | golden eval set v0, 25 tasks | spec only; samples live outside the repo |
| X-4 | cheap-model routing bench | PARK |
| X-5 | context-compression bench | TEST |
| X-6 | approval-prompt inventory | compiled 2026-10-19 |

Evidence labels: READ = both atoms read in full; OPENING = at least one
side read only at its opening; TITLE = inferred from titles; STRUCTURE =
headings and sizes of a personal file.

## 1. DUPLICATION — the same job done more than once

| Id | Atoms | Same job | Should die | Survivor | Evidence |
|---|---|---|---|---|---|
| P-U1 | P-07, P-16, S-082, spec 04, X-4 | model routing, two-model check, escalation | routing lines in P-07 and P-16; spec 04's separate table | S-082 plus a `router.yaml` it points to | READ (persona), DESCRIPTION-LINE (skill) |
| P-U2 | A-016, P-04, P-17, L-2 | "a first readout is not done" | A-016 prose, L-2 | one kernel line + READBACK-REQUIRED | READ |
| P-U3 | A-027, P-07, spec CHECKPOINT-REQUIRED, X-1 | long jobs checkpoint and resume | the three prose copies | X-1; the gate becomes "background work goes through X-1" | READ |
| P-U4 | 42 on-chain atoms (30,622 B) plus the cross-domain ones, S-083, two market skills with local-state notes | how to send on-chain safely | the copy in the rules file | one skill `onchain-send` | TITLE |
| P-U5 | A-045, A-068, A-086, S-058; and A-050, A-075, A-078 | bind verification to bytes not paths; path-only bar | A-045/A-068 carry the same title in two sections; A-050 and A-078 restate A-075 | one `verification-core` rule (see P-D2) | TITLE (rules), DESCRIPTION-LINE (skill) |
| P-U6 | chain C-PUB-WAIVER (9 atoms, 7,575 B), A-081, A-089, A-093, A-101, S-059, P-14 line 4, L-4 | whose word counts as the owner's | scattered copies | S-059 as the single home | TITLE |
| P-U7 | A-017, S-061, S-086, spec LEG-INVENTORY | split work into legs, verify each | — | A-017's rule as the core; the two skills cite it | READ (A-017), DESCRIPTION-LINE (skills) |
| P-U8 | S-063 … S-079 | CORRECTED after measurement: the 17 market-data playbooks share a recurring phrase but only one identical paragraph; removable duplicate text is 16,283 B of 649,562 B (2.5%) | nothing | no merge; they stay on-demand as they are | MEASURED by script; CONFIRMED by the full read (second run) |
| P-U9 | A-031, P-12 last paragraph, X-6 §4 | batch all approvals before the flow | A-031 | P-12 | READ |
| P-U10 | A-036, P-17 item 4, S-086 | docs or ground truth before claiming a mechanic | A-036 | S-086, one kernel line | READ |
| P-U11 | P-10, L-1, L-4, L-6 | call discipline | the lessons, once carried | three kernel lines + skill `comms-live` | READ |
| P-U12 | X-2, spec STARTUP-ALIVE, spec WATCH-THE-WATCHER | is everything alive | the spec's separate gates | X-2 extended with a worker registry | READ (X-2 opening) |
| P-U13 | X-3, spec 03 | eval suite | neither | one suite: 64 mock tasks + 25 real-workflow tasks; 7 overlap | READ |
| P-U14 | Y-2 … Y-4, F-4, M-2, M-3 | who the owner is, boundaries | depends on P-G1 | — | STRUCTURE |

Bytes at stake in the rules file from P-U4, P-U5, P-U6 alone: about 45 KB.

## 2. CONTRADICTION — atoms that cannot both be obeyed

| Id | Atoms | The conflict | Resolution | Evidence |
|---|---|---|---|---|
| P-C1 | A-006, A-022 vs F-1, F-5 | The rules file opens with "It starts empty and is meant to grow slowly… a short, accurate file beats a long, stale one" and holds "Standing context is a per-turn tax". The file is 144,702 B; live memory is 22,247 B | Prose cannot hold this line. Byte caps enforced by a script | READ |
| P-C2 | P-08, A-034, A-036, spec claims block | Four label sets: "VERIFIED, INFERENCE, ASSUMPTION, NOT_EXECUTED" (P-08); "VERIFIED / INFERENCE / UNCONFIRMED" (A-034); "UNVERIFIED" (A-036, A-017); VERIFIED / INFERENCE / UNKNOWN (spec) | One set, Muse's own: claims VERIFIED / INFERENCE / ASSUMPTION / UNVERIFIED; legs DONE / PENDING / BLOCKED / FAILED / NOT_EXECUTED; inventories carry an UNVERIFIED flag | READ |
| P-C3 | A-030, P-15 vs A-017, spec CREW-REPORT-UNVERIFIED | "Spot-check one; don't re-fetch the rest" and "deep-check one item" against "account for every leg in that inventory"; the spec says 3 items or 20% | Proof presence is checked for every item by script (cheap); content is deep-checked on one item for routine work and on every item for gated work | READ |
| P-C4 | spec 04 rules X1–X3 vs P-16 | Spec escalates a tier automatically; P-16: "Escalation that costs money passes the spending gate first". Spec: verifier from a different family "where one is available"; P-07: "from a different maker" | Escalation inside a pre-approved task budget is automatic; beyond it, it is a spend-gate ask. Two-model check requires a different maker or is reported as not done | READ |
| P-C5 | M-3, M-4 vs M-1, spec 02 LIVE budget | The live memory header calls itself a live layer, yet 11,420 B of its 22,247 B sit under "standing orders" and "money, wallets, trading". Spec 02 gives LIVE 6 KB including standing rules | Standing orders are rules. They move to the rules layer with the owner's quote and date as provenance; LIVE keeps facts and state | STRUCTURE |
| P-C6 | P-09 vs F-8 vs the amendment zone | P-09: "one dated line" per miss, read every session. The lessons file has 7 multi-sentence entries in about 5 weeks. The rules file meanwhile took 16 amendment versions (129 atoms, 82,208 B) | There are two lesson sinks and the mandated one is the unused one. One pipeline (spec 02 §2.8), one sink | READ |
| P-C7 | A-160 vs A-149; A-124 vs A-115; A-154 vs A-143; 13 more | 16 atoms state that they replace earlier wording. The replaced wording is still in the file. A-143 is replaced "in full" by A-154 and is still injected. A-160: "expiry of the validity window is NOT a mandatory conjunct", against the earlier bullet it names | Collapse each chain to its current state; archive history. See D4 | OPENING |
| P-C8 | A-089 vs its section | An on-chain rule (its own tag says so) is filed under the pre-publish section | Refile by tag, not by position, before any split into skills | OPENING |
| P-C9 | F-1 headings vs content vs pack | The last heading names two versions; the section holds 14 (v3.5.8 – v3.5.21, 115 atoms). The pack says v3.5.19 | Headers are generated from content, never typed | READ |
| P-C10 | spec MASKED-VALUE vs A-017 | Spec: a masked value "may not be … compared for equality, or used". A-017 permits value verification through a non-masked channel or a functional probe that fingerprints the value actually presented, and defines "presence-verified / value-unverified" | Spec is wrong. Adopt A-017's three outcomes | READ |
| P-C11 | spec JOB-TRIAGE-CLASSIFY vs A-035 | Spec: change window 24 h; three consecutive failures is an incident. A-035: change window runs from the last qualifying success to the first failure; "No success-ratio threshold applies"; adds a stuck-run precondition, a veto rebuttal, a qualifying-success definition and family escalation | Spec is a lossy copy. Implement A-035 as written | READ |
| P-C12 | spec APPROVAL-TOKEN and the built gate vs P-12 | Spec and code: every gated call needs a single-use approval matching exact arguments. P-12 grants a standing permission for routine git work ("Never re-confirm this grant") and a delegated approval for submissions | Add two record types: standing grant (scope pattern, not consumed) and delegated approval (named reviewer, bound to a packet hash) | READ |
| P-C13 | P-12 vs pack §6 vs spec 01 kernel | P-12 lists seven gate types, including installs or changes on the owner's devices, and messages sent "as him or as me". The pack and the spec say six | Seven. The persona file is the source | READ |

## 3. DEPENDENCY — A silently assumes B

| Id | A assumes B | What breaks when B moves | Evidence |
|---|---|---|---|
| P-D1 | A-035 clause 2 assumes A-007: "A known job-side cause documented in" the rules file vetoes a transport verdict | Moving platform quirks into a skill empties the veto. The classifier needs its own known-causes table, with A-007 as its first row | READ |
| P-D2 | 14 atoms (9,408 B) are tagged to two or three domains: A-109, A-119, A-144, A-148, A-177, A-182, A-189, A-193, A-197, A-202, A-204, A-205, A-206, A-213. A-019 leans on "the same default the [on-chain] re-check rule applies" | Four separate skills would each miss shared rules. A fifth unit, `verification-core`, must hold inventory independence, audience vantage, digests, deviation bounds, and be loaded by all four | TITLE, READ (A-019) |
| P-D3 | 89 of 129 amendment atoms carry a relation verb (58 "qualifies", 15 "replaces", 15 "extends"); 28 point at another atom by version or bullet position | Any reorder, merge or deletion breaks the pointers. Resolve every pointer into plain text before consolidating | READ (script count) |
| P-D4 | L-3 (start the relay first) assumes P-09 ("read it at the start of every session"). The lessons file is not among the injected files in the manifest | The only carrier of the one F7 incident on record is a voluntary read | READ |
| P-D5 | Any kernel rewrite assumes Muse can edit the persona file. P-09: sections 2, 11, 12, 13 are never self-edited and "no change goes live without" the owner | 3,519 B must enter the kernel verbatim, and the kernel cut is an owner-approved change, not a builder task | READ |
| P-D6 | P-19 is a hand-kept index of skills | Three of the names it lists match none of the 37 custom skills in the manifest | READ |
| P-D7 | Spec BUDGET-STOP and router caps assume the harness can count tokens and stop a run. X-5 states the runtime has "no hooks, no control of its model's base URL" | No interception point exists. The existing carrier is S-085 (prose) | READ (X-5 line), needs Muse to confirm |
| P-D8 | Every spec gate described as a pre-tool or post-tool hook assumes a hook surface. X-5 says there is none; X-2 says scripts cannot call the scheduler tools ("those are Muse tools, not shell commands") | Gates can be enforced only where the action runs through a script Muse executes. Everything else can only be audited after the fact. See D1 | READ (X-5, X-2), needs Muse to confirm |
| P-D9 | Spec 01 context profiles assume crew and cron context can differ from main-chat context | Unknown whether the platform allows it. If not, every cron keeps paying the full standing load | BLOCKED: platform behavior, not in corpus |
| P-D10 | Spec two-model check sends "the exact tool arguments" to a second maker. P-14: other models get least context, and wallet data never goes to free routes | For wallet or signing work the verifier must be an allowed provider and must see digests, not raw arguments | READ |
| P-D11 | X-2 skips its own job and relies on a second schedule to watch it | STARTUP-ALIVE must not be a third watcher; it is X-2 run at session start | READ (X-2 opening) |

## 4. GAP — a failure-class surface no pair covers

| Id | Gap | Why it matters | Evidence |
|---|---|---|---|
| P-G1 | Nothing in the corpus says who generates and injects the alignment synthesis (F-7: 34,150 B, 15% of standing bytes, one 26,880 B section on a single line, under a path named "derived") | If the platform writes and injects it nightly, Muse cannot trim it and the 16 KB target has a 34 KB floor | STRUCTURE |
| P-G2 | No atom, anywhere, names an enforcement point. All 220 rules are prose addressed to the model | This is why the file grew: the only available fix for a miss was more prose. Without an enforcement or audit point the diet regrows | READ |
| P-G3 | Effort is concentrated away from four of the seven classes. Of 220 rule atoms, 190 (93.5% of atom bytes) cover publish, send, media and deploy. F4 has none (the word "correction" appears once, "reminder" never). F5 has one. F6 has two one-liners (A-024, A-034). F7 has two atoms (A-008, A-027) | The self-audit program red-teamed the same four domains through 16 versions while the classes that produced the recorded lessons got almost nothing | READ (script count) |
| P-G4 | The inventory fails its own rule. A-017: an inventory drawn from the system under test is UNVERIFIED. The manifest was generated by Muse about Muse. It says 135 memory files where the pack says 134 and the corpus holds 131; 25 MB where the corpus holds 12.5 MB; and it omits X-1 … X-6 | This registry inherits that. Coverage is 100% of the manifest, not 100% of the system | READ |
| P-G5 | Jobs (31), goal workspaces (131) and handoffs (730) appear only as counts | Job-to-job duplication, jobs whose purpose ended, and job-to-goal links cannot be assessed. P-18 ("scheduled tasks only when he asks") cannot be checked against G-4 | BLOCKED-ON-CORPUS |
| P-G6 | No test covers the 16 replacements in P-C7 | Consolidating adversarially evolved rules with a mid-tier model can silently drop a protection. Each replacement is a ready-made regression case | OPENING |
| P-G7 | No atom covers memory writes: what may be stored, where, with what provenance | F4 has no carrier at all before spec 02 is built | READ (script count) |

## 5. Platform atoms and F8 (addendum questions 1 and 2)

Capabilities that run through a platform Muse rents or that meters it.
Names are generic; evidence ids point at where the dependence is stated.

| Id | Platform atom | Meter or limit | Precedent on record | Second route designed? | Evidence |
|---|---|---|---|---|---|
| PL-1 | multi-model API subscription (the bench; carries the main workhorse route) | fixed term with an end date; provider rate limits | none on record; the term has a stated end date and renewal is off | named in a recommended stack, not shown as configured | M-5, M-9, S-082 |
| PL-2 | phone bridge tunnel (phone-hosted models, device control) | none; availability | repeated tunnel outages; a recovery skill exists because of them | partial: bench API for models, browser sign-in for access | A-035, S-091, M-3 |
| PL-3 | the host agent platform (VM, egress proxy, scheduler, approval cards, context injection) | not in corpus | per-session credentials go stale in long-lived workers; an approval card timed out and killed a watcher run | none possible: it is the runtime | A-008, X-6 |
| PL-4 | frontier reviewer agent on a consumer subscription | 5-hour and weekly meters | weekly meter at 91% on 2026-11-12; **one read lane of this analysis stopped on the 5-hour limit** | none | P-12, P-15, coordination usage file |
| PL-5 | other chat-agent subscriptions used as lanes | per-plan usage | one at 40% on its reset day, 2026-11-10 | stated behavior is "blocked → stop and tell the owner" | M-3, addendum |
| PL-6 | code-hosting platform as the coordination bus | API limits; an approval card per connector call | 16 of 20 approval cards in one day were for this connector | stored-token path, tested once | X-6 |
| PL-7 | market-data API behind a CLI | tiered leaky bucket (three tiers; a full wallet run weighs more than the middle tier); a 429 starts a ban that repeated calls extend to about 5 min; finest candle resolution and some calls are paid-tier. 15 of 17 state a limit rule (stop on 429, retry once at most, pacing, or never loop); 2 state none (S-063, S-067) | none on record | per skill, no shared one: 10 of 17 state a data fallback (cannot-assess, partial report, on-chain-only card); none falls back to another provider, and web lookup is forbidden in S-069. The two money skills never auto-resubmit | S-063 … S-079 |
| PL-8 | chain data / RPC API behind a key | provider limits | none on record | none stated in the execution skill | S-083, A-057 |
| PL-9 | hosted browser and logged-in web sessions | session lifetime | — | yes: the timed-session skill sizes work to the session | S-094, S-060 |
| PL-10 | messenger mini-app host, web hosting, social networks | plan and platform rules | — | partial or none | S-062, S-092 |

Of the 20 custom skills read in full, 12 depend on a rented or metered
platform and 3 state a complete fallback (skills lane, `PAIR-MAP-RULES.md`).

| Id | Platform × other atom | Finding | Type |
|---|---|---|---|
| P-F1 | PL-1, PL-4, PL-5 × S-082 §6, P-16 | The router's only limit rule is "A provider fails → say so, name the next option. No silent failover." That covers a failure that is noticed. Nothing reads a meter before the limit, and no table names the next option per job | GAP |
| P-F2 | PL-4 × P-12, P-15 | Two things hang on one metered agent: the delegated approval for submissions and "a different agent accepts my work". When its meter runs out, submissions and acceptance both stop, with no stated substitute | DEPENDENCY |
| P-F3 | PL-4 × spec 03, spec 04 | The head-to-head reference and the frontier tier use the same metered agent. Spec 03 already limits it to one run per suite version; nothing checks the meter before that run starts | DEPENDENCY |
| P-F4 | PL-1 × S-082 §2 | Every row of the routing table resolves to the bench. A term end removes all rows at once | DEPENDENCY |
| P-F5 | PL-2 × A-035 | Bridge outages are already a named transport family in the triage rule, so an outage is classified. That part of F8 is F5 and is covered | DUPLICATION with F5 |
| P-F6 | PL-3 × A-008 × spec STARTUP-ALIVE | Liveness that tests reachability passes while credentials are stale. One-machine-per-lane isolation helps here: a lane on its own machine has its own credentials and its death does not take the orchestrator with it | DEPENDENCY |
| P-F7 | coordination usage file × all other agents | A working meter reader exists for one agent (thresholds: session 80%, weekly 70%). Ten roster agents have none | GAP |
| P-F8 | rule clause "sign off when near your usage limit" × no meter | The coordination rule already requires the F8 behavior; without a meter it cannot be obeyed | CONTRADICTION |

**Verdict on F8: it stands as its own class, narrowed.** It is not F7.
F7 is internal state lost (a worker not started, a job killed). F8 is
external capacity running out or a sole route disappearing: a different
cause, read from a different place (a meter or a term date, in advance),
with a different fix (a second route or a planned stop). The outage half
of the proposed F8 is already F5 (P-F5) and stays there.

F8, as adopted: **a meter, term or sole route that could have been read in
advance is not read, and the work stops or degrades without a plan.**
Carriers: dependency card per platform; a meter snapshot in the existing
health checker; a second-route column in the router; sign-off before the
limit. Deltas D24–D27.

## 6. The three methods (addendum question 3), judged on corpus evidence

| Method | Evidence in the corpus | Verdict |
|---|---|---|
| (a) Map a tool before depending on it | Seven platform quirks were each learned by failure (A-007 … A-013). The no-hook surface was found by reading an integration surface, and it invalidates part of spec 05 (P-D8). Existing bench documents already open with a "this fails if…" table. A skill for ground-truth capability checks exists (S-086) | ADOPT, as an extension of S-086: a dependency card (meter, limits, auth lifetime, hook surface, failure modes, exit route) before a tool enters a build lane. D24 |
| (b) Design before code, as a UI gate | The persona already requires real references and a concrete target for visual work, and a quality-bars skill exists. The upgrade has one visual deliverable: the gainshare statement | ADOPT narrowly: a mock of the statement is approved before step 14 is coded. No new atom |
| (c) One orchestrator over several machines | The VM has 2 CPUs and 7.7 GB and cannot host parallel builders. Credentials are per session (A-008). The routing skill already defines lanes with one owner and separate files. Builder agents on their own machines do not inherit the 222 KB standing context and are not bound by the no-hook limit | ADOPT for the build, as directed. The phone is not a build lane: it is reached through the tunnel with the outage record. D28 |

## 7. Coordination-layer pairs

| Id | Atoms | Finding | Type |
|---|---|---|---|
| P-B1 | coordination rule "read the board" × board size | The board file is 183,293 B; its requests section alone is 116,888 B. A check-in that reads it costs about 46k tokens; Muse's timer does this six times a day | F3 at the coordination layer |
| P-B2 | rule "keep last 10 handoffs" × requests and claims | Handoff lines are capped by the checker; requests (273 lines, 85 DONE still present) and claims are not | GAP |
| P-B3 | checker warning at 24 h × board state | 13 of 21 claims are older than 7 days; 40 open requests are older than 14 days. A warning nobody must clear is not a carrier | GAP |
| P-B4 | board labels × Muse labels | VERIFIED / INTENT / INFERENCE / UNKNOWN is a fifth vocabulary (see P-C2) | CONTRADICTION |
| P-B5 | relay worker × its own README × L-3 | The README still marks the Muse link "not verified"; the lesson says the worker was never started. The worker is in no registry | DEPENDENCY |
| P-B6 | state file "read this first" × its content | It describes a gate dated six days before the read | CONTRADICTION |

Model and conformance table: `../MUSE-MODEL.md` §3.
