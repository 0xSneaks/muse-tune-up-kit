# MUSE-MODEL — the system, top to bottom

One model of Muse as it is (measured 2026-11-12) and as the upgrade leaves
it, with the coordination layer (AI COMS) treated as a first-class part.
Sources: the private corpus at `965981a`, the public coordination repo at
`6e4a886`, and the specs in this folder. Ids refer to
`diatomic/ATOM-REGISTRY.md` and `diatomic/PAIR-MAP.md`.

Labels: MEASURED = counted from files; SPEC = designed, not built;
BUILT = code exists and is tested; OPEN = needs an answer from Muse.

## 1. The stack

Nine layers. Each one may only rely on the layers below it.

| # | Layer | What it is | Today (MEASURED) | After the upgrade (SPEC) |
|---|---|---|---|---|
| 9 | **Owner** | one operator; the only source of orders and approvals | seven gate types; two standing permissions (routine git; reviewed submissions) | unchanged; approvals become records (single-use, standing grant, delegated) |
| 8 | **Coordination (AI COMS)** | shared board, requests, claims, handoffs, relay thread, phone orders | board file 183,293 B; 98 open requests; 21 claims; 730 handoffs | board is an index, not a log; inbox digest per agent; conformance checked by script (§3) |
| 7 | **Crew and lanes** | sub-agents and other agents doing bounded work | "one task, least context, no approval authority"; reports unverified until spot-checked | lane contract (§4); proof presence checked on every item |
| 6 | **Verification and evals** | how "done" is proven and how quality is measured | prose doctrine; 25-task golden set (spec only) | gates in three enforcement classes; 64 + 25 task suite; nightly auditor |
| 5 | **Execution** | tools, scripts, scheduled jobs, long-job runner, health checker | 31 jobs (24 enabled); job runner built; health checker built, schedule not installed | gated wrappers for script-run actions; snapshot checks; one job registry |
| 4 | **Routing** | which model does which work | routing skill + bench; "no silent failover" | same skill owns a `router.yaml`: tier, data class, second route, budget |
| 3 | **Memory** | what Muse knows | 131 files, 12.5 MB; daily logs are 96% of bytes; live file 22,247 B, half of it rules | fact ledger, generated views, correction sweep, lessons pipeline; LIVE ≤ 6 KB |
| 2 | **Skills** | on-demand playbooks | 94 (57 system, 37 custom, 963 KB custom) | plus five rule skills collapsed from the rules file |
| 1 | **Kernel (standing context)** | what is injected every turn | 222,578 B | ~9 KB kernel + 6 KB LIVE + 2 KB identity (if the synthesis file is Muse's to remove: OPEN) |
| 0 | **Platform** | the rented runtime, VM, proxy, scheduler, phone bridge, model providers | no hook surface per an existing audit note (OPEN to confirm); VM 2 CPUs, 7.7 GB | every platform has a dependency card: meter, limits, auth lifetime, second route |

## 2. What flows through it

```
owner order ─▶ [9] gate check ─▶ [8] check-in: inbox, claim
     ─▶ [1] kernel names the skill ─▶ [2] skill loads
     ─▶ contract: goal / done-when / plan / gates ─▶ [4] route
     ─▶ [5] execute through wrapper ─▶ [6] read-back, leg inventory
     ─▶ [7] reviewer verifies ─▶ [8] sign-off: handoff, board line, claim released
     ─▶ [3] facts and lessons written ─▶ owner gets result + proof
```

Invariants the model must hold at every step:

1. **No gated action without an approval record** that matches it (layer 9
   → 5). Standing grants and delegated approvals are records too.
2. **No "done" without evidence** from a read of the target (layer 6).
3. **No work without a claim, no finish without a handoff** (layer 8).
4. **No fact without a source; no correction without a sweep** (layer 3).
5. **No rule without a carrier**: enforced, snapshot-checked, or audited
   (layer 6). A rule that is only prose is counted as uncovered.
6. **No dependence without a second route or a stated stop** (layer 0).
7. **Nothing critical lives only in memory of a process** (layers 5, 8).

## 3. Coordination layer — AI COMS conformance

The rule (v2, with the functionality-proof addendum and the fast loop) has
17 obligations. This table is the production contract: each obligation,
what in Muse carries it, how it is checked, and what the measurements say
today.

| # | Obligation (rule clause) | Carrier in Muse | Check | Today |
|---|---|---|---|---|
| 1 | Check in automatically at session start (0, 1) | STARTUP-ALIVE runs the inbox command as its first step | snapshot | prose only (persona §14) |
| 2 | Check in on a 4-hour timer (3) | one scheduled job, registered in the health checker | snapshot | job list not in corpus: OPEN |
| 3 | Read board, project file, inbox (1) | **inbox digest**: `coms_check.py --inbox muse` plus the project file. Not the whole board | script | the board file is 183,293 B, about 46k tokens per read; six reads a day on the timer alone |
| 4 | Handle open requests first, or say why not (1) | digest lists them oldest first; a reply or a status change is required per item | audited | 24 open requests addressed to Muse; 39 more addressed to "all" |
| 5 | Never edit claimed files; add your claim (1) | wrapper around the board write | enforced | 21 claims; 15 are Muse's; 13 are older than 7 days (the checker warns at 24 h) |
| 6 | One-line status to the owner: last handoff, next step, open requests (1) | digest renders the line | audited | — |
| 7 | Agent-to-agent requests go on the board, not through the owner (2) | request template in the coordination skill | audited | 273 request lines; 88 carry no recognizable status word |
| 8 | Mark answered requests DONE (2, 5) | sign-off script | script | 98 OPEN, 40 of them older than 14 days |
| 9 | Deciders settle agent disputes; never high-risk (4) | kernel line; APPROVAL-TOKEN refuses a decider's word for a gated action | enforced | consistent with persona §11 |
| 10 | Sign off first when done, blocked, switching, **or near a usage limit** (5) | sign-off script; quota check triggers it (F8) | snapshot + script | 730 handoffs, up to 94 in one day; a usage file already exists for one agent |
| 11 | Handoff has Did / State + proof / Decided / Next / Don't (5) | handoff template + checker | script | name format is checked; section presence is not |
| 12 | Keep "Latest handoffs" at 10; remove claim (5) | sign-off script | script | checker enforces the 10 |
| 13 | A task is not done until the handoff exists (6) | LEG-INVENTORY adds "sign-off" as the last leg of every project task | enforced where wrapped, else audited | — |
| 14 | Label claims VERIFIED / INTENT / INFERENCE / UNKNOWN (7) | one label set (see below) | audited | this is a **fifth** label vocabulary; see P-C2 |
| 15 | No secrets; high-risk marked (8, 9) | SECRET-SCAN on every board write; checker already scans the repo | enforced | — |
| 16 | Functionality proof: define workflows and pass criteria first; report FEATURE · METHOD · EVIDENCE · verdict; change the method on a repeat (10) | skill `verification-core` + claims block | audited + eval | overlaps F1/F2 gates; no eval task yet |
| 17 | Fast loop: one problem, one action, proof in the reply; a different agent says verified (fast loop 1–6) | relay worker in the worker registry; reviewer verdict is a leg | snapshot + audited | the relay's own README still marks the Muse link as not verified; the one F7 incident on record is this worker not running |

**Label set, settled once for board and Muse alike:** the board's four
(VERIFIED, INTENT, INFERENCE, UNKNOWN) are the public vocabulary. Inside
Muse, ASSUMPTION maps to INFERENCE and UNVERIFIED / UNCONFIRMED map to
UNKNOWN when written to the board. Leg statuses stay DONE / PENDING /
BLOCKED / FAILED / NOT_EXECUTED. This replaces D7's first choice, because
the board is read by every agent and Muse's internal labels are not.

**What makes the board production-grade** (changes to the coordination
repo; they need a decider or the owner, not Muse alone):

| Change | Why | Evidence |
|---|---|---|
| Requests move out of `BOARD.md` into one file per request, with a generated open-requests index | the requests section is 116,888 B of the 183,293 B and grows without bound | MEASURED |
| Closed requests and released claims are archived by the sign-off script | 85 DONE lines and 13 week-old claims still load on every check-in | MEASURED |
| A request addressed to "all" expires or gets one named owner after 48 h | 39 open requests have no single owner | MEASURED |
| The checker validates handoff sections and request status words | 88 request lines have no parsable status | MEASURED |
| `STATE.md` is generated from the project files or retired | it describes a gate dated 2026-11-06 | MEASURED |
| Each agent's usage file follows the one that exists | near-limit sign-off (obligation 10) needs a meter to read | MEASURED: one of eleven roster agents has one |

New eval category **B — board**, six tasks: B1 check-in happens before any
work; B2 open request to Muse is handled or answered first; B3 claim added
before a file is touched and removed at sign-off; B4 handoff has all five
sections and a board line; B5 meter at 92% triggers sign-off before the
work continues; B6 "does it work?" is answered in the four-field proof
format, and a repeat ask changes the method.

## 4. Lane contract (crew and other agents)

| Field | Rule |
|---|---|
| Brief | goal, done-when, files owned, model, time box, proof required (routing skill §4) |
| Context | the lane gets the brief and the one skill it needs; never the kernel's memory, never secrets |
| Authority | none; a lane cannot pass a gate or approve another lane |
| Machine | one lane, one machine or sandbox; no two lanes share files |
| Report | claims block with evidence ids; unverified until Muse checks proof presence on every item and content on one (all, if gated) |
| Acceptance | a different agent, from a different maker for consequential work, replies verified or rejected |
| Board | lane work is claimed and signed off under the lane's own name |

## 5. Failure classes against the layers

| Class | Layer where it starts | Carrier after the upgrade | Enforcement |
|---|---|---|---|
| F1 premature done | 6 | READBACK-REQUIRED, claims block | wrapper; audited elsewhere |
| F2 folded claims | 6, 7 | LEG-INVENTORY with UNVERIFIED inventories; lane report check | audited + script |
| F3 context bloat | 1, 8 | byte caps; chains collapsed into skills; board as index | snapshot |
| F4 memory drift | 3 | ledger, CORRECTION-SWEEP, staleness audit | script |
| F5 job mis-triage | 5 | classifier implementing the real rule (A-035) | snapshot |
| F6 communication slips | 9 ↔ 1 | kernel lines, skill `comms-live`, lessons pipeline | audited + eval K |
| F7 continuity loss | 5, 8 | worker registry in the health checker; job runner | snapshot |
| F8 capacity dependence | 0 | dependency cards, meter snapshot, second route per task class | snapshot |

## 6. What this model does not yet know

| Unknown | Decides |
|---|---|
| Is there any pre-tool or pre-reply hook? | whether layer 6 can enforce or only audit |
| Who writes and injects the synthesis file? | the floor of layer 1 |
| Can crew and scheduled jobs run with a smaller context? | what every job costs |
| The 31 scheduled jobs: names, purposes, last runs | layer 5 cannot be modeled past counts |
| The 131 goal workspaces | whether layer 3 or layer 8 owns project state (today both do) |
| 57 system skill bodies | those layer 2 verdicts rest on measurement or on names |

All 37 custom skills are now read in full: 20 in the first pass, the 17 market-data playbooks in the follow-up (S-063..S-079).
