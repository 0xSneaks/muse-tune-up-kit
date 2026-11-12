# SPEC-DELTA — corrections to specs 01–06 forced by the atoms and pairs

Every delta cites registry or pair-map ids. Nothing here is applied to
specs 01–06 yet; this file is the change list for Muse to accept or
reject. Two deltas (D1, D16) rest on a question only Muse can answer and
are marked.

## Deltas that change the architecture

### D1 — Gates cannot be hooks. Split every check into ENFORCED or AUDITED
**Forced by:** P-D8, P-D7, P-G2. **Needs Muse to confirm** that the runtime
has no pre-tool or pre-reply hook.
**Changes:** spec 05 §5.1 (hook points), spec 01 §1.4 (T1 trigger), spec 04
§4.4, and how the step-1 code is used.

| Enforcement class | Where it works | Gates |
|---|---|---|
| ENFORCED-WRAPPER | actions Muse performs by running a script: on-chain sends, git and publish CLIs, file writes through a helper | APPROVAL-TOKEN, UNKNOWN-OUTCOME, READBACK-REQUIRED, SECRET-SCAN, ARTIFACT-AS-PUBLISHED. The built `GatedTools` is this wrapper |
| ENFORCED-SNAPSHOT | Muse gathers state with native tools, writes a JSON snapshot, a script judges and exits 0/1/2 (the pattern X-2 already uses) | STARTUP-ALIVE, WATCH-THE-WATCHER, JOB-TRIAGE-CLASSIFY, staleness audit, byte caps |
| AUDITED | everything that happens inside a reply or a native tool call | LEG-INVENTORY, SOURCE-OR-SILENT, DATA-NOT-ORDERS, LEAST-DISCLOSURE, FRESHNESS-STAMP, communication rules |

AUDITED means a scheduled auditor reads the day's transcripts and gate
logs, scores them with the eval harness's own scorers, and writes each
violation to the lessons pipeline. It does not prevent; it guarantees
detection within a day. **New component: the auditor job** (workhorse
tier, nightly). Spec 05 must state the class next to every gate; a gate
with no class is prose.

### D2 — Modules are skills. Do not build a second retrieval mechanism
**Forced by:** P-19 ("I load only the skill a task needs"), S-rows, P-U4,
P-U5, P-U6. **Changes:** spec 01 §1.1, §1.4.
The platform already loads skills on demand; 94 exist. L1 modules become
skills with the platform's own file layout: a core file and reference
files. Because loading is by description match, not by tool hook (D1),
each kernel gate-index line names its skill explicitly: "before any
on-chain send, load `onchain-send`". The trigger table in §1.4 becomes
that kernel index.

### D3 — Module size budget was wrong by a factor of eight
**Forced by:** §2 domain totals; chains in registry.
Spec 01 allowed 6 KB per module, 12 KB per turn. The pre-publish domain alone is 48,648 B. New contract: core skill file ≤ 8 KB (the current-state
rule for every chain), reference files per chain loaded only when that
chain is in play. Five units:

| Skill | Source atoms | Raw bytes | Chains |
|---|---|---|---|
| `verification-core` | A-016 … A-019, the 14 cross-domain atoms (9,408 B), digest and vantage chains | ~17 KB | C-DEP-INVENTORY, C-DEP-VANTAGE, C-DEP-DIGEST, C-PATH-ONLY |
| `pre-publish` | 68 atoms | 48,648 | waiver, envelope, assembly, closure, personalised, live |
| `onchain-send` | 42 atoms + S-083 | 30,622 + 6,580 | claim, release, class, bounds |
| `media-verify` | 42 atoms | 26,705 | AV, transform, container |
| `deploy-verify` | the rest of the 24 deploy atoms (17,623 B) | ~10 KB | probe, continuing |

Consolidated size after D4 is an ASSUMPTION until done: 40–60% of raw.

### D4 — Collapse amendment chains before moving anything
**Forced by:** P-C7, P-D3, P-G6, P-C8, P-C9.
New build step, ahead of module extraction:
1. Resolve all 28 positional pointers into plain text (P-D3).
2. Refile atoms by tag, not position (A-089, P-C8).
3. Delete A-143 (replaced in full).
4. For each of the 20 chains, write one current-state rule; move the
   version history to archive.
5. **Chain regression set:** one test per replacement in P-C7 (16), each
   asserting the newer rule's outcome on a case where old and new differ.
   A consolidated chain ships only when its tests pass.
Steps 1–3 are mechanical. Step 4 is the one place a mid-tier model can
lose a protection; step 5 is its guard. Step 4 needs the 184 atoms read in
full, which this session did not do.

### D5 — JOB-TRIAGE-CLASSIFY implements A-035 exactly
**Forced by:** P-C11, P-D1. **Changes:** spec 05 gate, spec 03 tasks.
Replace the four-step procedure with A-035's: classification window
(24 h or 20 runs, whichever is shorter); stuck-run precondition
(STUCK/UNVERIFIED); clause 1 error origin from a runner-generated field;
clause 2 veto (known job-side cause, change between last qualifying
success and first failure, input correlation, failing alone) with its
peer-overlap rebuttal; clause 3 qualifying success (post-change, artifact
attributable to that run, no-op runs never qualify); family escalation at
three in 24 h without summing across families. No success-ratio
threshold. Ship a `known_causes.json` seeded from A-007.
New eval tasks: J13 stuck in-flight run; J14 veto rebutted by overlapping
peer failures; J15 no-op "success" does not qualify; J16 family
escalation. J10's fixture needs a runner-origin field, which the built
fixture already has.

### D6 — The kernel carries 3.5 KB verbatim and is an owner change
**Forced by:** P-D5, P-C13, registry §3.
Persona §2, §11, §12, §13 (3,519 B) enter the kernel unedited. With the
trimmed persona lines (~2.6 KB), speed mode (~0.7 KB), identity and owner
cards (~0.6 KB) and the gate index (~1.5 KB), the kernel is about 9 KB,
not 8. New budget: target 9 KB, hard cap 10 KB. The gate list is seven
types. The kernel cut is proposed to the owner as one diff; Muse does not
apply it alone.

## Deltas that correct a gate, task or rule

| Id | Change | Forced by |
|---|---|---|
| D7 | One label set everywhere: claims VERIFIED / INFERENCE / ASSUMPTION / UNVERIFIED; legs DONE / PENDING / BLOCKED / FAILED / NOT_EXECUTED. `claims.py` accepts UNKNOWN and NOT-ATTEMPTED as aliases for one release, then drops them | P-C2 |
| D8 | LEG-INVENTORY gains an inventory-level flag UNVERIFIED (sole-source, self-authored or common-mode inventories), and UNVERIFIED blocks dependent execution (A-097) | A-017, A-018, A-019, A-097 |
| D9 | MASKED-VALUE: three outcomes — value-verified (non-masked channel, or functional probe with matching fingerprint), presence-verified / value-unverified, blocked | P-C10 |
| D10 | APPROVAL-TOKEN: add `standing_grant` (scope pattern, never consumed, never re-asked) and `delegated_approval` (reviewer id + packet hash); seven gate types; approvals are requested before the flow on planned arguments, and a mid-flow change beyond the approved deviation bound re-asks | P-C12, P-C13, P-U9 |
| D11 | CREW-REPORT-UNVERIFIED: proof presence checked on every item by script; content deep-check on one item (routine) or all (gated) | P-C3 |
| D12 | CHECKPOINT-REQUIRED is "use X-1". Remove the design; keep the resume drill (V2, V3) | P-U3 |
| D13 | STARTUP-ALIVE and WATCH-THE-WATCHER are X-2 plus a worker registry, run at session start as well as on schedule. Liveness must test the worker's credentials, not only reachability (A-008) | P-U12, P-D11, A-008 |
| D14 | Router: escalation beyond the task's approved budget is a spend-gate ask; two-model check needs a different maker or is reported NOT_EXECUTED; add a data-class column (wallet, private code, personal, public) that limits eligible providers; verifier sees digests for wallet work. The router table lives in S-082 | P-C4, P-D10, P-U1 |
| D15 | Lessons pipeline: one sink. Carriers for the seven existing lessons are assigned in registry §8. New eval task K7 (L-5): on a call, a question about a numbered item in a document already sent is answered from the document or not at all | P-C6, P-D4, L-5 |
| D16 | **Needs Muse to answer P-G1.** If the synthesis is platform-injected, the acceptance line becomes "Muse-controlled standing bytes ≤ 16 KB", reported next to the platform's bytes | P-G1 |
| D17 | Memory: standing orders leave LIVE. New ledger predicate class `standing-order` is rendered into the rules layer (kernel if it binds a gate, otherwise the matching skill), each with owner quote and date. LIVE budget stays 6 KB | P-C5 |
| D18 | Eval suite absorbs X-3: add category W (25 real-workflow tasks, samples on Muse's machine). Seven overlap existing tasks and are merged. Cost comes from the tracing tool X-3's document already tested | P-U13 |
| D19 | Coverage rebalance: of the next lessons and eval tasks written, none go to publish, send, media or deploy until F4, F6 and F7 each have an ENFORCED or AUDITED carrier | P-G3, P-G7 |
| D20 | Spec 01 §1.6 step M0 is done at domain level by this registry. Remaining: full read of 184 atoms for the CHECK split | registry §2 |
| D21 | The 17 market-data skills share one preamble: move it to one reference file. Three skills over 35 KB (S-058, S-061, S-085) get the same chain-collapse treatment as D4 | P-U8, S-rows |
| D22 | Generated headers and indexes: the rules-file version line, the persona skills index, and the manifest itself are produced by a script from content | P-C9, P-D6, P-G4 |

## What does not change

Spec 02's ledger, sweep and resurrection guard; spec 03's rig and scoring;
spec 06. The step 1–2 code is still correct for the ENFORCED-WRAPPER
class; D7–D11 are small edits to it.

## Day estimates revised

| Step | Was | Now | Why |
|---|---|---|---|
| 0 (new) Confirm P-D8, P-D9, P-G1 with Muse | — | 0.5 | three answers decide D1 and D16 |
| 1 Gates as hooks | 5 (done as a library) | +2 | D7–D11 edits; wrapper CLIs for the exec-reachable actions |
| 4 Remaining tasks | 5 | 6 | J13–J16, K7, category W |
| 5 Rules manifest | 2 | 1 | domain level done here; full read remains |
| 5b (new) Chain collapse + regression set | — | 6 | D4 |
| 6 Remaining gates | 3 | 3 | checkpoint and health already exist (−2); auditor job (+2) |
| 7 Module extraction | 4 | 3 | five skills, after 5b |
| 8 Kernel cut | 2 | 1 + owner review | D6 |
| 11 Memory jobs | 3 | 4 | D17 |
| Others | unchanged | | |
| **Total** | **43** | **about 52** | |
