# onchain-send — regression cases (DRAFT)

One case per contradiction row in PAIR-MAP-RULES.md touching this
domain's atoms: the fourteen send-lane rows R-016…R-029 and the two
deploy_cross rows whose atoms are homed here, R-048 and R-049. Each
case is built so the old (pre-collapse) reading and the collapsed
rule give different outcomes; the collapsed rule must produce the
expected result. Where a resolution follows the later amendment over
an earlier text, the case says so and names what each side carried.

## RC-1 — R-016 (A-061 vs A-181/A-190): an unadvanced nonce locks until the owner accepts

- Setup: a durable-nonce send's outcome is unknown. The independent
  re-check is clean (no landing) and the nonce account has NOT
  advanced.
- Old-rule outcome: A-061's not-advanced branch reads as
  self-authorising — clean re-check, nonce unadvanced, so the
  re-send signed against the same nonce proceeds. A-181 says the
  same claim stays locked and pending absent owner acceptance. The
  two atoms give opposite answers to the same re-send.
- New-rule outcome (CURRENT-STATE §3 + §7): the claim stays LOCKED,
  is reported PENDING with the lock named, and is escalated. Only an
  owner risk acceptance unlocks anything, and what it unlocks is at
  most a same-nonce replacement preserving the staged intent. (The
  advanced branch is untouched: advancement by a positively
  identified non-original transaction still proves the original can
  never land, and a fresh transaction against the current nonce
  proceeds.)
- Expected result: no re-send without owner acceptance; with
  acceptance, a same-nonce replacement only.
- Protections: A-061 side — original and re-send mutually exclusive
  on one nonce, never two independently valid transactions (kept:
  the unlocked replacement is same-nonce only, and substituting a
  recent-blockhash transaction in that branch stays forbidden).
  A-181 side — an unadvanced nonce at check time proves nothing
  about a detached signed copy (kept: lock + escalation). Neither
  dropped; the later atoms govern the branch's exit condition.

## RC-2 — R-017 (A-149 vs A-160): a proven never-sent claim releases without expiry

- Setup: a durable-nonce staged send is positively proven never
  broadcast (independent evidence, §7 conjuncts all hold). A
  durable-nonce transaction has no validity window, so no expiry
  can ever be shown.
- Old-rule outcome: A-149's absolute sentence — "a clean re-check
  before the would-be transaction's expiry window has passed never
  releases any claim" — combined with its expiry conjunct makes the
  claim unreleasable forever, even though nothing was ever sent.
- New-rule outcome (CURRENT-STATE §7): expiry is NOT a mandatory
  conjunct for a proven never-sent claim; the claim releases on the
  §7 conjunct set (independent non-broadcast evidence, no signature
  ever recorded, clean dual re-check with nonce non-advanced,
  signed-copy accounting, owner release). The absolute sentence is
  deleted; the two release paths stand side by side in the state
  table.
- Expected result: release with all conjuncts proven; no release on
  any subset.
- Protections: A-149 side — unknown broadcast state never benefits
  from the never-sent path (kept: positive proof of non-broadcast is
  conjunct 1; unknown = broadcast). A-160 side — a provably
  never-sent claim does not lock its class forever (kept). Neither
  dropped.

## RC-3 — R-018 (A-160 vs A-166/A-173): an unused nonce proves "not yet", not "cannot"

- Setup: a never-sent claim's nonce is unadvanced, but one signed
  copy of the staged transaction sits in a relayer queue outside the
  signer's view; its destruction or custody cannot be independently
  evidenced.
- Old-rule outcome: A-160's reasoning — the unused nonce "proves the
  staged transaction has not landed and cannot land without
  consuming that nonce" — reads as proof the copy is harmless:
  release, then a different-nonce send proceeds while the queued
  copy can still land later. Double payment.
- New-rule outcome (CURRENT-STATE §7 conjuncts 3–4): a non-advanced
  nonce proves only that the staged transaction has not landed yet,
  never that it cannot land later. Signed-copy accounting is a
  release conjunct, and the destruction/custody showing needs
  sender-independent evidence; unproven, it bars any different-nonce
  send. Release for a different-nonce send is available only via
  same-nonce consumption or the nonce being advanced/burned by a
  known transaction that is not the staged payment.
- Expected result: class stays locked for a different-nonce send;
  the same-nonce path remains available.
- Protections: A-160 side — proven never-sent claims have a real
  exit (kept, via the same-nonce route). A-166/A-173 side — no live
  signed blob is left able to land after the class unlocks (kept).
  The 'cannot land' reasoning sentence is removed; no operative
  protection dropped.

## RC-4 — R-019 (A-123 vs A-216): an unverified price never merges distinct obligations

- Setup: a claim is open for obligation X to a beneficiary. A second
  send to the same beneficiary for the same purpose but a DISTINCT
  obligation is proposed; the only value-equivalence evidence rests
  on a reference price from a thin pool that fails the §5 integrity
  standard.
- Old-rule outcome: A-123's fail-closed clause — "where source
  control or value-equivalence cannot be established, treat as same
  class" — merges the distinct obligation into the open claim and
  blocks the send: a manipulable price has effectively decided
  class identity.
- New-rule outcome (CURRENT-STATE §6, last paragraph): value is
  marked UNVERIFIED; an unverified price never merges distinct
  obligations. Classes are keyed by obligation identity (beneficiary
  + purpose + staged record id) in addition to asset; only an exact
  duplicate key locks. The second send is not blocked by the first
  claim (it still takes its own claim and passes every other rule).
- Expected result: distinct obligation proceeds under its own claim;
  an exact duplicate of obligation X still locks.
- Protections: A-123 side — fail-closed duplicate protection (KEPT
  for every case where equivalence is establishable, for
  source/beneficiary control, and for exact duplicates under any
  price state). A-216 side — class identity cannot be moved by a
  price that fails the integrity standard (kept). FLAGGED: this is
  the one place the collapse follows the later amendment over an
  earlier fail-closed default; see PROOF FLAG-1.

## RC-5 — R-020 (A-123 vs A-211): a different asset with an unverified value does not merge

- Setup: a claim is open paying a beneficiary a staged value in
  asset A. A second send pays the same beneficiary the "same value"
  in asset B, for a distinct obligation; the A→B price fails the
  integrity standard.
- Old-rule outcome: A-123 — "an open class claim blocks a duplicate
  from any sender-controlled source and in any value-equivalent
  asset" — treats the B payment as the same class and blocks it,
  even though the equivalence it relies on is exactly what cannot
  be established.
- New-rule outcome (CURRENT-STATE §6): with the price unverified,
  class identity is judged on asset, beneficiary, purpose, and
  obligation (A-211's fallback, as completed by A-216); a
  different-asset, distinct-obligation payment is not merged into
  the open claim. With a verified price, A-123's cross-asset rule
  applies in full and the same payment WOULD be the same class.
- Expected result: blocked as a duplicate only when value-equivalence
  is established at an integrity-passing price; otherwise judged on
  its own key.
- Protections: A-123 side — cross-asset duplicates cannot slip the
  lock (kept wherever equivalence is provable). A-211 side — an
  unprovable equivalence asserts nothing in either direction
  (kept). Same flag as RC-4 (PROOF FLAG-1).

## RC-6 — R-021 (A-113 vs A-123/A-131): one key definition; route is not identity

- Setup: an intent is re-sent through a different pool, via an
  intermediary account, delivering the wrapped form of the same
  asset to the same ultimate beneficiary.
- Old-rule outcome: A-113's key names "the original source, the
  ULTIMATE beneficiary, and the net asset ultimately delivered"
  read literally — a changed route/source and a wrapped delivered
  asset read as a different class, so the open claim does not block
  the re-send.
- New-rule outcome (CURRENT-STATE §6): the key is beneficiary,
  purpose, staged value, obligation. Sources and delivered assets
  enter only as equivalence classes (sender-controlled sources are
  equivalent; wrapped = native); route, pool, intermediary, and
  wrapping are traced through and are not identity. Only
  route-independence is kept from the older definition's wording.
- Expected result: the re-send is the same class and is blocked by
  the open claim.
- Protections: A-113 side — no escaping a claim by re-routing
  (kept, strengthened). A-123/A-131 side — one canonical key, so
  the atomic claim tests one thing (kept). None dropped.

## RC-7 — R-022 (A-100 vs A-106): the same-intent test lives inside the atomic claim

- Setup: two sessions send the same intent concurrently. Both search
  the open-claim record, both see no claim, both write a claim, both
  send. Duplicate payment.
- Old-rule outcome: A-100 orders exactly that sequence — "before
  claiming, a sender searches open claims" — and A-106 forbids it
  ("never a search-then-claim sequence"). Followed literally, the
  earlier atom manufactures the race the later one exists to
  prevent.
- New-rule outcome (CURRENT-STATE §6): the search sentence is
  dropped. Canonicalisation and the same-intent tests (fee/rounding
  allowance, split parts summing to the staged value) are evaluated
  inside one atomic test-and-set on the class key; the second
  session's claim fails atomically and it does not send.
- Expected result: exactly one send; the losing session re-checks
  the existing claim's outcome.
- Protections: A-100 side — canonical fields and the split/allowance
  same-intent tests (kept, inside the claim). A-106 side — atomicity
  (kept). None dropped.

## RC-8 — R-023 (A-141 vs A-151): the obligation distinguishes, references are evidence

- Setup: (i) one obligation is invoiced twice under two different
  references (a re-issued bill); a claim is open under the first
  reference. (ii) A vendor reuses one reference across distinct
  monthly obligations; a claim is open for last month's instance.
- Old-rule outcome: A-141 — "DISTINCT owner-staged references are
  DISTINCT classes" — lets (i) pay the same obligation twice, and
  merges (ii)'s distinct instances into one class, blocking a
  legitimate new payment.
- New-rule outcome (CURRENT-STATE §6): the distinguisher is the
  underlying obligation instance recorded in the staged record;
  references are only evidence of it. (i) Same obligation, two
  references = same class: blocked. (ii) One reference, two
  instances = distinct classes: the new instance proceeds under its
  own claim. Kept from the older atom: where the chain cannot carry
  the reference, distinct-reference intents are serialised rather
  than conflated, and an agent-invented reference never splits a
  class.
- Expected result: (i) blocked as a duplicate; (ii) not merged.
- Protections: A-141 side — genuinely distinct staged intents are
  not conflated (kept via obligation identity + serialisation).
  A-151 side — labels cannot create or dissolve obligations (kept).
  None dropped.

## RC-9 — R-024 (A-115 vs A-124/A-133): rounding never widens the effective tolerance

- Setup: a re-send's bound is a minimum-output floor stated in a
  relative form; converting it to an absolute amount at the original
  reference produces a fraction that must be rounded.
- Old-rule outcome: A-115 — conversion "rounds toward the STRICTER
  (smaller) bound" — rounds the floor DOWN, widening what the bound
  permits, and the loosened bound is then treated as owner-confirmed.
- New-rule outcome (CURRENT-STATE §4): polarity is taken from the
  effective bound after the quotation is canonicalised into the
  asset actually delivered; ceilings round down, floors round up;
  rounding must never widen the effective tolerance in either
  orientation, and a conversion whose rounding would widen it is
  unstated — escalate.
- Expected result: the floor rounds up; if no rounding keeps the
  tolerance intact, the bound is unstated and the re-send escalates
  instead of sending.
- Protections: A-115 side — conversion only at the original staged
  reference, never at quote/landing prices (kept). A-124/A-133
  side — a converted bound is never looser than the owner confirmed
  (kept). None dropped.

## RC-10 — R-025 (A-093 vs A-101/A-089): the transaction's own record is not provenance

- Setup: a signed transaction carries a slippage field embedded by
  a third-party builder; the owner never saw it. A re-send's pricing
  deviates beyond that field.
- Old-rule outcome: A-093's alternative — a plan/spec counts as
  provenance if it "is the signed transaction's own record" — makes
  the builder's field a stated bound, so the deviation test runs
  against a bound the owner never set.
- New-rule outcome (CURRENT-STATE §4): the own-record alternative is
  removed. One provenance rule: a bound is stated only when the
  owner saw and set or confirmed the field through an owner channel
  AND the encoded field matches it in value and units. The builder
  field is unstated; the position is "no bound was stated" and the
  re-send escalates for re-approval. A-093's surviving idea — a
  plan of unverified authorship is data — is folded into the same
  rule.
- Expected result: escalation before re-send; no deviation test is
  run against the builder's number.
- Protections: A-093 side — owner-traced plans still inform what
  bound was intended (kept as context, not as a stated bound).
  A-101/A-089 side — only owner-confirmed fields bind (kept). None
  dropped; the removed alternative was the hole.

## RC-11 — R-026 (A-114 vs A-140 and successors): one state table, an exit per state

- Setup: a claim exists for a send that, it turns out, was never
  broadcast — no signature, and non-broadcast is provable.
- Old-rule outcome: A-114's lifecycle sentence — a claim "resolves
  ONLY by landing or the full safe-to-resend test", and "a null
  status, a timeout, or the mere passage of time never resolves a
  claim" — leaves no exit at all for a claim with no transaction:
  the class locks forever, or an operator is tempted to let time or
  a null status quietly resolve it.
- New-rule outcome (CURRENT-STATE §7): one state table — BROADCAST,
  UNKNOWN-OUTCOME, NEVER-SENT, TAMPER-LOCKED — each with its exits.
  The never-sent claim exits by RELEASE on its conjuncts; the
  null/timeout/time sentence survives verbatim as a rule for every
  state.
- Expected result: the claim is routed to the NEVER-SENT branch and
  held until its conjuncts are proven; it is never resolved by time
  or silence.
- Protections: A-114 side — no resolution by null status, timeout,
  or passage of time (kept for all states). A-140 side — a claim
  with no transaction has a defined, evidence-gated exit (kept).
  None dropped.

## RC-12 — R-027 (A-140 vs A-149): an empty signature field is not evidence

- Setup: a send crashed mid-flow. The claim record contains NO
  signature. Whether the broadcast step ran is unknown — a detached
  worker may have fired it.
- Old-rule outcome: A-140 defines NEVER-SENT by the record's shape
  ("the claim record contains NO signature, because the send
  crashed…"), so this claim enters the release path on the strength
  of an empty field — while the transaction may in fact be live.
- New-rule outcome (CURRENT-STATE §7): the older definition is
  deleted. Never-sent requires positive evidence the broadcast step
  never executed; a crash with unknown broadcast state is an
  UNKNOWN-OUTCOME claim, treated as broadcast until proven
  otherwise.
- Expected result: no release; the claim follows the broadcast
  exits (landing, or the §3 criterion).
- Protections: A-140 side — claims with no transaction have a
  release path (kept, re-gated on proof). A-149 side — an empty
  field never masquerades as evidence (kept). None dropped.

## RC-13 — R-028 (A-149 vs A-167/A-173/A-180): the sender's own record is a self-report

- Setup: the only evidence offered for non-broadcast is the sending
  system's own staged/process record, which shows the send stopped
  before broadcast.
- Old-rule outcome: A-149's parenthetical illustrates positive
  evidence by exactly that record — "the staged/process record
  shows the send stopped before broadcast" — so the release
  conjunct is satisfied by the system whose failure is in question.
- New-rule outcome (CURRENT-STATE §7 conjunct 1): the parenthetical
  is replaced by the independent-source definition. Positive
  evidence comes from a source independent of the sending process —
  relayer/queue/worker infrastructure records, or instrumentation
  of the broadcast step across every session/worker that could have
  performed it — and the worker set is itself an inventory that must
  be independently established; release is barred while it is
  UNVERIFIED.
- Expected result: never-sent not established on the self-report;
  the claim is treated as broadcast.
- Protections: A-149 side — never-sent still requires positive
  evidence, not absence of evidence (kept). A-167 side — no
  self-certification of the load-bearing fact (kept). None dropped.

## RC-14 — R-029 (A-181 vs A-190/A-199): abandonment unlocks a same-nonce replacement, nothing else

- Setup: the owner has recorded a risk acceptance abandoning an
  intent class whose staged durable-nonce transaction may still be
  live. A replacement is proposed on a DIFFERENT nonce, with any
  later double-land to be "booked as an incident charged against
  that acceptance".
- Old-rule outcome: A-181's booking language implies the class is
  free once the acceptance exists — the different-nonce send
  proceeds and the possible double payment is paperwork.
- New-rule outcome (CURRENT-STATE §7, abandonment): acceptance
  unlocks at most a replacement that consumes the SAME nonce and
  preserves the staged intent (same beneficiary, amount within the
  allowance, purpose — A-199); any change makes it a new intent
  needing fresh approval and full signed-copy accounting. A
  different-nonce send additionally requires the conjunct-4
  accounting in full; the acceptance does not make it compliant.
- Expected result: the different-nonce replacement is blocked; a
  same-nonce, same-intent replacement may proceed.
- Protections: A-181 side — the owner can consciously accept a
  named risk and unstick a class (kept, narrowed to the
  mutually-exclusive route). A-190 side — an acceptance never waives
  an irreversibility invariant on money movement (kept). None
  dropped.

## RC-15 — R-048 (A-189 vs A-206): the send-time actual value governs the bound

- Setup: a bound's conversion was fixed in advance at a time whose
  price passes, and a window average also passes — but the actual
  deliverable value at send time breaches the bound.
- Old-rule outcome: A-189's test — conversion "at a time fixed in
  advance", or a window average — passes the send on the fixed-time
  or averaged figure while the real value moved against the owner.
- New-rule outcome (CURRENT-STATE §5): the send-time actual
  deliverable value governs a bound; a time-weighted or fixed-time
  conversion is evidence for that value, never an override of it.
  If the send-time value breaches, the send fails the bound
  regardless of any average. A-189's integrity standard (independent
  source, manipulation-resistant, time fixed in the staged record)
  survives as the standard the evidence must meet.
- Expected result: send blocked/escalated on the actual value.
- Protections: A-189 side — no favourable-timestamp picking; prices
  must be independent and manipulation-resistant (kept). A-206
  side — the number tested is the number the owner actually gets
  (kept). None dropped.

## RC-16 — R-049 (A-197 vs A-206): the depth test is scoped to where price is the consideration

- Setup: a plain transfer of a fixed amount of an asset, with its
  bound stated in that asset's own units ("send exactly N of X").
  Asset X trades in a thin pool.
- Old-rule outcome: A-197 — a short-window average over a thin pool
  is manipulable, so the asset is UNPRICED — blocks a transfer whose
  bound never depended on any price at all.
- New-rule outcome (CURRENT-STATE §5, last paragraph): the
  depth/time-weighting conjuncts apply only where price is the
  consideration for the bound — a trade, or a bound stated in
  another numeraire. A plain non-trade transfer bounded in its own
  units is not UNPRICED for lack of depth, and proceeds under its
  own-unit bound (every other rule — claim, re-check, total effect
  in its own asset — still applies).
- Expected result: the transfer is not blocked by the depth test;
  the same asset used in a cross-unit bound still fails UNPRICED on
  the thin pool.
- Protections: A-197 side — a thin pool can never set a price the
  owner is bound by (kept, scoped to where a price is used).
  A-206 side — a unit-exact obligation is not hostage to market
  depth it never referenced (kept). None dropped.
