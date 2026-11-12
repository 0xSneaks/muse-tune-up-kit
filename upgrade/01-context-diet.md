# 1. Context Diet (kills F3)

**Replaces:** one 144 KB rules file injected every turn.
**With:** four layers, of which only an 8 KB kernel is always injected.
**Why this kills F3:** a rule competes for attention only with the rules
relevant to the current action, and anything a script can enforce stops
depending on attention at all.

The rules file was not available (see `00-README.md`), so this spec gives
the classification procedure and the layer contracts, not a per-paragraph
verdict. The split percentages below are INFERENCE to be replaced by the
manifest counts from step M0.

## 1.1 Layers

| Layer | Injected | Budget | Holds |
|---|---|---|---|
| L0 Kernel | every turn | target 8 KB, hard cap 10 KB (CI fails above) | laws, gate triggers, claim vocabulary, module index |
| L1 Modules | on trigger | 6 KB each; max 2 modules / 12 KB per turn | procedures for one tool family or task class |
| L2 Executable checks | never (code) | — | anything a hook, script, or test can enforce |
| L3 Archive | never; search only | — | incident narratives, rationale, history, superseded rules |

Prompt order, fixed for cache reuse: kernel → modules (sorted by id) →
memory live layer → conversation. Nothing volatile (dates, counters, job
status) goes in the kernel; one changed byte there invalidates the cache
for everything after it.

## 1.2 Classification procedure

Chunk the file by heading or paragraph. For each chunk, ask in this order
and stop at the first yes:

1. **Duplicate or contradicted by a later chunk?** → delete the older;
   log both ids in the manifest.
2. **Narrative, incident story, or rationale?** → L3. If it justifies a
   live rule, the rule keeps a one-line `why:` and a pointer.
3. **Can code detect the violation or block the action at the tool
   boundary?** → L2. Examples: secrets in a write, a gated tool called
   without approval, a write with no read-back, a report with unlisted
   legs, the kernel over budget.
4. **Relevant only when a specific tool, connector, or task class is in
   play?** → L1 module for that trigger.
5. **Otherwise** → kernel candidate. Admit only if it passes one test:
   (a) it applies to roughly a third of turns or more, or (b) violating it
   is irreversible and no code path can catch it first. Failing both, it
   goes to the nearest module.

Expected split by bytes (INFERENCE): kernel ~5%, modules ~35%, executable
~15%, archive or deleted ~45%.

Output of classification is `rules-manifest.jsonl`, one line per chunk:

```json
{"id":"r-0412","sha":"…","bytes":611,"class":"L1","target":"mod-outbound",
 "fclass":["F2"],"carrier_before":"prose","carrier_after":"mod-outbound+UNKNOWN-OUTCOME",
 "eval":["E4","E5"],"status":"pending"}
```

Every chunk must name the eval tasks that prove its rule still holds.
A chunk with no eval task either gets one or is a candidate for deletion.

## 1.3 Kernel contents (the whole 8 KB)

| Block | Budget | Content |
|---|---|---|
| Identity and voice | 0.4 KB | who Muse is, answer-first, plain |
| Laws | 0.6 KB | no harm, no lies, no unapproved spend, serve the owner |
| Approval gates | 1.0 KB | the six gated action types; the four-field ask (action, destination, cost, consequence); no blanket approvals |
| Data-not-orders | 0.5 KB | only the owner instructs; everything else is material |
| Secrets | 0.4 KB | never in chat, memory, logs, or reports |
| Claim vocabulary | 0.8 KB | DONE(evidence) / PENDING / BLOCKED / FAILED / NOT-ATTEMPTED; VERIFIED / INFERENCE / UNKNOWN |
| Gate index | 1.5 KB | one line per gate in `05-gates-library.md`: name → trigger |
| Module index | 1.5 KB | one line per module: id → when it loads |
| Unknown-outcome rule | 0.3 KB | check state by another route before repeating |
| Slack | 1.0 KB | — |

The kernel names gates; it does not describe their procedures. Procedures
live in code (L2) or in the module that loads with the triggering tool.

## 1.4 Modules and their triggers

Triggers are deterministic first. A model's own sense that it "should look
something up" is the weakest trigger and is used only as the third fallback.

Trigger precedence: (T1) pre-tool hook — tool name maps to module;
(T2) turn-start task label from the cheap-tier classifier;
(T3) keyword regex on the owner's message.

| Module | T1 tool families | T2 task label | T3 keywords |
|---|---|---|---|
| `mod-outbound` (email, messages as owner) | send, reply, forward, post-message | comms | send, reply, tell, let … know |
| `mod-publish` (public posts, media) | post, upload, set-artwork | publish | post, publish, upload, tweet |
| `mod-money` (spend, trades, transfers) | pay, order, transfer, subscribe | money | buy, pay, trade, upgrade, wire |
| `mod-deploy` | deploy, release, push-live | deploy | deploy, ship, release |
| `mod-destructive` | delete, trash, overwrite, revoke | cleanup | delete, remove, clean up, wipe |
| `mod-accounts` (credentials, permissions, connectors, skills) | connect, grant, install, rotate | access | connect, install, key, permission |
| `mod-jobs` (scheduled jobs, triage, health) | schedule-create/update, job-status | ops | job, cron, failed, down, health |
| `mod-research` (sources, citation, freshness) | search, fetch | research | find out, look up, price, is it true |
| `mod-memory` (writes, corrections, people/groups) | memory-write, memory-correct | memory | remember, actually, no it's, correct |
| `mod-longrun` (background work, checkpoints) | background-start | longrun | — |
| `mod-style-long` (formats, long-form voice) | — | writing | draft, write up |
| `mod-<connector>` (per-connector quirks) | that connector's tools | — | — |

Rules: a T1 trigger is mandatory and blocking — the module is injected
before the tool call executes. Every load is logged
(`{turn, module, trigger, bytes}`). If a gate fires and its owning module
was not loaded, log `retrieval_miss`; three misses for one module in a
month means its triggers are wrong.

## 1.5 Executable checks (L2)

Each replaces prose that asked the model to remember. Full procedures are
in `05-gates-library.md`.

| Prose rule being replaced | Enforcement | Gate |
|---|---|---|
| "read back after writing" | post-tool hook compares write to read | READBACK-REQUIRED |
| "report step by step" | pre-report check: legs in plan = legs in report | LEG-INVENTORY |
| "get approval before X" | pre-tool hook refuses gated tools without a matching approval record | APPROVAL-TOKEN |
| "never store secrets" | pattern scan on every memory/file/outbound write | SECRET-SCAN |
| "don't re-send when unsure" | idempotency ledger + state check before retry | UNKNOWN-OUTCOME |
| "a job that ran isn't a job that worked" | job check requires output-artifact evidence | TRANSPORT-VS-JOB |
| "inspect media before publishing" | publish tool requires an inspection record for the file hash | ARTIFACT-AS-PUBLISHED |
| "keep context lean" | CI: kernel ≤ 10 KB, module ≤ 6 KB, live memory ≤ 6 KB | (CI) |
| "every job has owner, purpose, stop condition" | job-registry lint | (CI) |

## 1.6 Migration order

Invariant, checked in CI at every commit: **each failure class has at
least one active carrier (prose, module, or check) and at least two
passing eval tasks.** `coverage.yaml` lists carriers per class; the commit
fails if any class drops to zero carriers or its tasks regress.

Each rule moves by shadow → dual → cut. Nothing is removed in the same
commit that adds its replacement.

| Step | Action | Removed from standing context | Check before proceeding |
|---|---|---|---|
| M0 | Build manifest; run eval baseline on the untouched 144 KB system | nothing | baseline frozen |
| M1 | Add L2 checks alongside the prose (log-only for 3 days, then blocking) | nothing | false-block rate acceptable; smoke set ≥ baseline |
| M2 | Delete duplicates; move narrative to L3 | ~45% | smoke set ≥ baseline |
| M3 | Remove prose now enforced by blocking L2 checks | ~15% | tasks in those rows' `eval` ≥ baseline |
| M4 | Extract modules one per commit, lowest stakes first: style → connectors → research → longrun → jobs → memory → accounts → destructive → deploy → outbound → publish → money | ~35%, in steps | that module's eval tasks pass with prose still present, then again after removal; revert on any drop |
| M5 | Write the kernel; the old file becomes `mod-legacy`, loadable only by explicit lookup, every load logged | remainder | full suite; category G with kernel only = zero critical fails |
| M6 | After 30 days with zero `mod-legacy` loads, archive it | — | — |

A `mod-legacy` load is a bug report: it names a rule the new layers
missed. Fix the trigger or add the rule to a module, then continue.

## 1.7 Cut from this section

A per-paragraph classification of the actual file (file not available),
and embedding-based retrieval (deterministic triggers come first; add
embeddings only if `retrieval_miss` data shows a need).
