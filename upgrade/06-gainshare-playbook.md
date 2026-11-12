# 6. Tokenomics Gainshare Playbook

An audit-and-optimize service for other teams' LLM and agent spend. We
are paid only from measured savings, with our compute covered first. The
measurement method is therefore the product.

Status of the claims here: the waste patterns and their order are
INFERENCE from the routing, caching, and context reasoning in sections 1
and 4, not results from a client engagement. No savings figure is
promised anywhere in this document. Percentages for share, tolerance
bands, and caps are contract blanks. Have the contract reviewed by a
lawyer before first use.

## 6.1 Data request — usage exports only

No code, no prompts, no completions.

| # | Item | Fields | Needed for |
|---|---|---|---|
| D1 | Per-request usage log, 8 weeks minimum | timestamp, request id, model, uncached input tokens, cache-read tokens, cache-write tokens, output tokens, reasoning tokens if billed separately, stop reason, status/error, latency, batch flag | everything |
| D2 | Segment tags per request | API key or project, route/feature name, prompt template id and version, session or task id, tool-call count | segmentation, loops |
| D3 | Invoices and price sheet | list prices, negotiated discounts, commitments | pricing |
| D4 | Volume driver per segment | one countable unit of work the client already tracks: tasks completed, tickets resolved, sessions | normalization |
| D5 | Quality metric per segment | one metric the client already tracks and trusts, with its history | the quality guard |
| D6 | Client change calendar | dates of their own prompt, model, or feature changes | attribution |

If D2 is missing, engagement step zero is adding a route tag and template
id to their request metadata. Without segments, nothing below is provable.
If D5 is missing for a segment, that segment is out of scope.

## 6.2 Waste patterns, in hunt order

Ordered by expected saving relative to effort and risk to quality.
Everything is detectable from D1–D2.

| # | Pattern | Signature in the export | Fix delivered |
|---|---|---|---|
| W1 | Stable prefix billed in full on every call | cache-read share near zero; input tokens per request have a high constant floor within a template | caching config: breakpoints, prefix ordering |
| W2 | Cache defeated by volatile content early in the prompt | cache writes ≥ cache reads; hit rate collapses at template version changes or on a clock | context rule: stable-first ordering; move timestamps and ids to the end |
| W3 | Top-tier model on low-difficulty routes | high volume, short low-variance outputs, on the most expensive model | routing config: tier per route |
| W4 | Context growth per turn | input tokens rise linearly with turn index within a session; late turns dominate session cost | context rules: compaction threshold, tool-output trimming, retrieval in place of standing text |
| W5 | Paying for failures | errors, timeouts, and `stop=length` followed by a re-request in the same session; duplicate request patterns | retry policy, max-tokens sizing, idempotency |
| W6 | Runaway agent sessions | tool-call and token distributions with a heavy tail; top 1% of sessions holding a large share of spend | per-task budget caps, loop detection |
| W7 | Synchronous work that tolerates delay | regular nightly or bulk bursts on standard endpoints | batch routing |
| W8 | Over-generation | outputs near max tokens; reasoning effort uniformly high; verbose formats on machine-read routes | output caps, effort per route, compact schemas |
| W9 | Repeated identical calls | same input-token count and template at high frequency (polling, re-asks) | memoization, dedupe window |
| W10 | Commercial terms | list price paid at committed-scale volume | advice only; excluded from gainshare unless agreed in writing |

Each finding is sized before any change: affected spend per month, a
conservative saving range, the quality risk, and the test that will prove it.

## 6.3 Measurement — built to be recomputed by the other side

### Definitions

- **Segment:** route × template family. The unit of all accounting.
- **Unit:** the D4 volume driver for that segment.
- **Token profile:** tokens per unit, by model and token type
  (uncached in, cache read, cache write, out).
- **Change ledger:** every change we deliver, with segment, mechanism,
  effective timestamp, and both parties' sign-off. A change not in the
  ledger earns nothing.

### Two methods; the stronger one wins wherever it is available

**Method H — live holdout (default).** For each changed segment, a random
5–10% of traffic stays on the pre-change configuration, assigned by a
hash of the session id. The holdout's cost per unit, in the same period,
is the counterfactual.

`savings_s = (holdout cost per unit − treated cost per unit) × treated units`

The holdout sees the same prices, the same workload drift, and the same
client changes as the treated traffic, so none of those need adjusting for.

**Method B — frozen baseline (fallback when a holdout is impossible).**
Baseline window: the 28–56 days before the first change, agreed and
frozen with a hash of the export. Baseline token profile per unit,
`T0_s`. In each period:

`counterfactual_s = T0_s × current prices × actual units_s`
`savings_s = counterfactual_s − actual cost_s`

Both sides of the subtraction use current prices, so a provider price cut
is not counted as our saving and a price rise is not counted against us.

### Attribution rules

1. Savings accrue per segment, from that segment's ledger effective date.
2. Segments we did not change are excluded, whether they got cheaper or
   more expensive.
3. Two changes in one segment are measured jointly; no splitting.
4. A saving in one segment that raises cost in another (a cheap first
   pass that causes more escalations downstream) is netted: linked
   segments are declared in the ledger and measured together.
5. If the client makes the same kind of change themselves in an untouched
   segment, that is theirs.
6. Cost of anything we add to their pipeline (verifier calls, classifier
   calls) is inside "actual cost" and reduces savings automatically.

### Quality guard

Each segment has its D5 metric and a tolerance band agreed before the
change. Under Method H the comparison is treated versus holdout in the
same period. If the metric falls outside the band, that segment earns
zero for the period and the change is rolled back or reworked. Savings
bought with quality are not savings.

### When the workload changes mid-period

| Event | Method H | Method B |
|---|---|---|
| Volume up or down | none needed; per-unit | none needed; per-unit |
| Mix shifts between segments | none needed; per-segment | none needed; per-segment |
| Provider price change | none needed | handled by current-price formula |
| New feature or segment | out of scope until it has a ledger entry and its own holdout | out of scope until 28 days of baseline exist |
| Client changes a prompt, model, or flow inside a changed segment | holdout absorbs it if the client's change applies to both arms; if it cannot, treat as below | **reset event:** savings for that segment stop at the event timestamp; resume after a new baseline, taken by running our change off on 10% of traffic for 14 days |
| Client reverts our change | savings stop at revert; nothing owed either way after | same |
| Units become unmeasurable (driver redefined) | segment paused until a new driver is agreed | same |
| Segment retired | final statement to retirement date | same |

A reset event can be declared by either side and must be evidenced from
the export: a template version change in D2, or the token profile of
untreated traffic moving by more than an agreed percentage.

### Payment waterfall

1. Sum segment savings for the period; negative segments count as
   negative (netting within the period).
2. Subtract our audit compute for the period, at cost, itemized, under a
   pre-agreed monthly cap.
3. If the result is positive, the share percentage applies to it. If zero
   or negative, no fee; the shortfall does not carry forward except
   unrecovered compute, up to the cap.
4. Each ledger change earns for a fixed term from its effective date,
   agreed up front.

### Dispute procedure

The monthly statement ships with: the export hash, the ledger, the
statement script and its version, and per-segment inputs. The client
recomputes with the same script on their own copy of the export. A
disagreement is by construction about an input (a unit count, a reset
date), never about the formula. Disputed segments are held out of that
month's payment; undisputed segments are paid.

## 6.4 Deliverables

| Deliverable | Form |
|---|---|
| Findings report | W1–W10 table with sized opportunities, risk, and proof test for each |
| Routing config | declarative table: route → model tier, escalation trigger, budget cap, effort and max-token settings |
| Caching changes | per template: cache breakpoint positions, required block order, TTL choice |
| Context rules | per route: compaction threshold, tool-output limits, what moves from standing text to retrieval |
| Holdout spec | assignment rule and percentage per segment |
| Change ledger | signed entries |
| Monthly statement | §6.3 outputs plus the script |

The client's engineers apply the changes; we never need code access.
Each change ships with its rollback.

## 6.5 Engagement sequence

| Week | Step |
|---|---|
| 0 | Data request; add segment tags if missing |
| 1 | Run the analyzer over D1–D2; findings report; agree units, quality metrics, bands |
| 2 | Freeze baseline; stand up holdouts; first changes are W1–W2 (no quality risk) |
| 3–4 | W3–W6 one segment at a time, each behind a holdout |
| 5+ | First statement; monthly loop begins |

## 6.6 Monthly re-optimization loop

1. Pull the new export; verify its hash chain against the previous month.
2. Re-run the W1–W10 detectors. New templates, new routes, and model
   releases surface as fresh W1/W3 findings.
3. Check every ledger change: holdout gap still present, quality in band,
   cache hit rate holding. A change whose gap has closed is flagged.
4. Re-fit routing per segment from the month's outcomes, at most one tier
   per segment per month, as in `04-router-policy.md` §4.6.
5. Propose new ledger entries; get sign-off.
6. Issue the statement.
7. Once a quarter, shrink holdouts on long-stable changes to the agreed
   minimum; never to zero while the change is still earning.

## 6.7 What we refuse to do

Count price cuts as savings; claim segments without a quality metric;
remove a holdout to raise the measured number; take prompts, completions,
or credentials. Each of these would make a statement disputable.

## 6.8 Cut from this section

Share percentages and term lengths (commercial decisions), a sample
contract, and the analyzer's code (step 14 in the build order).
