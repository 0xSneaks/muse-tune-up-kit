# onchain-send — collapse proof (DRAFT)

Atom-by-atom coverage: where each source atom's operative content
lives in CURRENT-STATE.md. Source byte sizes are the ATOM-REGISTRY
figures for the live rules-file atoms. Nothing in the live file was
edited; this folder is a draft in the upgrade clone only.

Scope: the 42 atoms the registry tags SEND (30,622 B), the 5 atoms
tagged SEND+DEPLOY (3,462 B), and 3 send atoms the registry tags
PUBLISH but the pair-map lane notes home in this module (2,663 B) —
50 atoms, 36,747 B. Each is collapsed exactly once, here.

| Atom | Size (B) | Operative content lands in | Notes |
|---|---|---|---|
| A-055 | 554 | §1 | Silently-dropping transport named, working curl route given, unknown-outcome rule stated for every send stack per transaction. Kept whole. |
| A-056 | 324 | §2 | Re-check balances + signature status via an independent route before any re-send. Kept whole. |
| A-057 | 2,442 | §2 | The independent re-check defined: two distinct-infrastructure providers, currency corroborated not self-reported, account-state findings corroborated across both, resellers count as one, distinctness established out-of-band. Kept whole. The general inventory-distinctness rules live in verification-core §3; this section states the send-specific form the atom carries, not a copy of the core text. |
| A-058 | 168 | §2 | "Balances" = source + destination for the asset moved + any separate fee payer. Kept whole. |
| A-059 | 1,086 | §2 | Lost signature: fingerprint a landing from history fields; fallback fingerprint (deltas, nonce/memo, route, tolerance); unresolvable collision = unresolved, no re-send. Kept whole. |
| A-060 | 1,443 | §3 | Safe-to-resend (blockhash): expiry AND attribution of every delta; aggregate per-asset sums; no de-minimis; fragmented landing is a landing. Kept whole. |
| A-061 | 1,039 | §3 | Durable-nonce criterion: nonce-state test replaces expiry; advanced-by-identified-other branch kept whole. The not-advanced branch's exit is governed by A-181/A-190 (registry override): same-nonce re-send no longer self-authorises on a clean re-check — §3 states the lock and points to §7. See RC-1. |
| A-062 | 859 | §3 | Bundle re-sent only whole, rebuilt fresh. Its pricing clause is the general bound rule, stated once in §4 per R-087; §3 keeps atomicity + rebuild and points there. |
| A-063 | 478 | §4 | The deviation bound applies to every re-send; beyond-bound or unstated bound escalates for re-approval. Kept whole (survivor of the R-087 duplication). |
| A-064 | 814 | §3 | Opaque/multi-step sends: freeze, reconcile per leg, never restart; escalate after a stated wait + second reconciliation. Kept whole. |
| A-085 | 884 | §6 | Sole re-sender status established via the shared claim record before any re-send; unestablishable = no re-send. Registry-tagged PUBLISH (misfiled send rule); collapsed here per pair-map lane notes — see FLAG-4. |
| A-089 | 1,082 | §4 | Stated bound = owner confirmed the field through an owner channel AND the encoded field matches in value and units. Kept whole; it is the survivor A-093 and A-101 merge into. Registry-tagged PUBLISH (misfiled); see FLAG-4. |
| A-090 | 697 | §6 | The sole-sender claim must be an atomic create-or-fail before acting; no such mechanism = no re-send. Kept whole. Registry-tagged PUBLISH (misfiled); see FLAG-4. |
| A-092 | 614 | §6 | Every send, original or re-send, first claims atomically in the shared cross-session record. Its exact field-hash key is superseded by the semantic class key (A-131 line); the claim duty and atomicity are kept whole. One claim sentence shared with A-106 per R-088. |
| A-093 | 538 | §4 | Plan/spec is a bound source only if it traces to the owner. The "or is the signed transaction's own record" alternative is REMOVED per R-025 (see FLAG-3 note in resolutions table); the unverified-authorship-is-data idea survives in §4 per R-056. |
| A-100 | 499 | §6 | Canonical fields from the staged record; near-equal/split amounts are the same intent — kept inside the atomic claim. Its "before claiming, search" sentence is dropped per R-022 (RC-7). |
| A-101 | 370 | §4 | Third-party builder tolerance the owner never confirmed is not a stated bound. Registry verdict DELETE (survivor A-089): content preserved entire inside §4's stated-bound rule. |
| A-106 | 1,010 | §6 | Same-intent test inside one atomic test-and-set on the class key; an open class claim blocks all sends in the class. Its class-key definition is replaced by A-113/A-131's semantic key (registry override); mechanism kept whole. |
| A-113 | 801 | §6 | Class = economic intent traced through any route/intermediary/wrapping; a different route is the same class. Its literal key wording (original source, net asset delivered) is superseded by A-123/A-131 per R-021 (RC-6); route-independence kept whole. |
| A-114 | 727 | §6 (allowance half), §7 (lifecycle half) | Two rules in one atom (pair-map lane note: split before merging). Allowance provenance → §6 (provenanced allowance or the same-source/purpose default). Lifecycle → §7 state table: resolves only on landing or the full safe-to-resend test, plus the never-sent and abandonment exits the later atoms add; "null status, timeout, or passage of time never resolves" kept verbatim for every state (R-089: stated once, in §7). |
| A-115 | 563 | §4 | Conversion only at the reference recorded at original send time. Its "rounds toward the smaller bound" is replaced by polarity rounding (A-124/A-133) per R-024 (RC-9). |
| A-123 | 789 | §6 | Class identity = beneficiary, purpose, staged value; sender-equivalent sources and value-equivalent assets are the same class. Its fail-closed clause for unestablishable equivalence is overridden for the unverified-price case by A-211/A-216 per R-019/R-020 — see FLAG-1 (RC-4, RC-5); it governs in full wherever equivalence is establishable. |
| A-124 | 424 | §4 | Polarity rounding: ceilings down, floors up; a loosened bound is not confirmed. Kept whole (merged into §4 with A-115/A-133). |
| A-131 | 423 | §6 | The atomic claim keys on beneficiary, purpose, staged value across assets; split parts summing to the value are one intent. Kept whole; the obligation distinguisher (A-151) and unverified-price keying (A-216) qualify it in the same section. |
| A-132 | 363 | §6 | All destinations controlled by the same beneficiary are equivalent; unknown control = same class. Kept whole, with A-216's exact-key exception for unverified prices stated in the same paragraph block. |
| A-133 | 475 | §4 | Polarity/rounding set by the effective bound after re-expression in the delivered asset. Kept whole (merged with A-115/A-124). |
| A-140 | 1,068 | §7 | First statement of the never-sent release (clean dual re-check + owner release or pre-stated time limit). Its definition of never-sent by an empty signature field is deleted per R-027 (RC-12); its release shape survives, re-conjuncted by A-149/A-160/A-166/A-167/A-173/A-180 into §7's conjunct list. |
| A-141 | 950 | §6 | Owner-staged per-intent reference distinguishes otherwise identical intents. Its "distinct references are distinct classes" is superseded by A-151's obligation rule per R-023 (RC-8); kept whole from it: serialisation where the chain cannot carry the reference, and the ban on agent-invented references splitting a class. |
| A-149 | 784 | §7 | Never-sent needs positive evidence the broadcast step did not run; unknown broadcast state = broadcast. Its staged/process-record parenthetical is replaced by the independent-source definition per R-028 (RC-13), and its absolute no-release-before-expiry sentence is deleted per R-017 (RC-2). |
| A-150 | 483 | §7 | TTL counts only with owner provenance and never shortens the expiry wait; release time is the later of the two. Scoped per R-068: the TTL path exists only for expiring sends; A-160's path requires owner release with no TTL alternative (stated in §7). |
| A-151 | 810 | §6 | The class distinguisher is the underlying obligation instance; references are evidence only; unknown identity = same class. Kept whole; under an unverified price the staged record id joins the key (A-216). |
| A-160 | 1,155 | §7 | Proven never-sent claim releases without expiry: independent evidence, clean re-check, unused nonce, owner release. Its "unused nonce proves it cannot land" reasoning is removed per R-018 (RC-3); the conjunct list is kept and completed by A-166/A-173. Its owner-release pointer ("the waiver-provenance bullet below") is resolved to the owner-channel provenance rule named in §7 conjunct 5 per R-057 — that definition is A-161, a publish-lane atom referenced here by name, not re-collapsed (see FLAG-5). |
| A-166 | 737 | §7 | Signed-copy accounting: same-nonce replacement, proven destruction, or nonce burned by a known transaction. Kept whole as conjunct 4; its conjuncts are defined once and referenced by the abandonment paragraph (R-090). |
| A-167 | 810 | §7 | Non-broadcast evidence must come from a system independent of the sender; unverifiable hand-off = treated as broadcast. Kept whole (survivor for A-173's merge). |
| A-173 | 1,073 | §7 | Every never-sent conjunct needs sender-independent evidence; unproven destruction bars a different-nonce send. Kept whole (merged into §7's conjuncts + the paragraph after them). |
| A-174 | 744 | §7 | Expiry never releases a never-expiring or unknown-outcome claim; expiry path is for proven never-sent expiring sends only. Kept whole (merged into §7's expiry paragraph). |
| A-177 | 679 | §5 (send-side); one sentence in verification-core §2 | The total-effect principle. Its leg-report sentence ("a report's verified status is judged on the total effect…") is already collapsed in verification-core §2 and is NOT duplicated here. Its send-side clauses — a total beyond the bound blocks the send; a field-by-field pass with a drifting total is a failed check — live in §5. Deploy tag dropped per R-079 (deploy-verify PROOF concurs: the chain was never deploy law). |
| A-180 | 611 | §7 | The broadcaster/worker set is an inventory needing independent records; an unverified set bars release. Kept whole as part of conjunct 1; the inventory rules it invokes are verification-core §3–§4, cross-referenced per R-058 (see FLAG-5). |
| A-181 | 659 | §7 | Unknown-outcome claim on an unused nonce: reported PENDING, escalated; only owner risk acceptance abandons the class; the claim is never reclassified never-sent and a later landing is an incident against the acceptance. Kept whole (survivor for A-190/A-199); its booking language is narrowed by A-190 per R-029 (RC-14). |
| A-182 | 521 | §5 | Total bound tested in one owner-named numeraire, conversion source + time recorded; unpriced movements block. Kept whole; A-189's integrity standard and A-206's send-time rule qualify it in the same section. Cross-referenced (not collapsed) in deploy-verify, per its PROOF. |
| A-189 | 1,014 | §5 | Conversion-price integrity: independent of the operation, manipulation-resistant, time fixed in advance; else unpriced. Kept whole; A-206 scopes its test (send-time value governs) and A-197 adds the minimum parameters, both in §5. Cross-referenced in deploy-verify. |
| A-190 | 765 | §7 | Abandonment unlocks only a same-nonce replacement; a different-nonce send still needs full signed-copy accounting. Kept whole (merged into §7's abandonment paragraph). |
| A-197 | 647 | §5 | Time-weighted price counts only if its window spans staging-to-send and market depth exceeds what the operation could move. Kept whole (merged into §5 with A-189); A-206 scopes the depth conjunct to where price is the consideration (RC-16). Cross-referenced in deploy-verify. |
| A-199 | 523 | §7 | Same-nonce replacement must keep beneficiary, amount within allowance, and purpose; any change is a new intent. Kept whole (merged into §7's abandonment paragraph). |
| A-201 | 541 | §8 | Claim record is authenticated and append-only; deletion/restore locks every affected class until re-established. Kept whole. |
| A-206 | 601 | §5 | Send-time actual value governs a bound; averages are evidence only; depth tests only where price is the consideration. Kept whole. Cross-referenced in deploy-verify. |
| A-209 | 724 | §8 | Tamper-locked class released only by an authenticated superseding entry citing independent evidence and a stated reason. Kept whole; A-217's tightening is in the same section. |
| A-211 | 507 | §6 | Price for value-equivalence must be independent, deep enough, time-fixed; else value is UNVERIFIED and class is judged on asset, beneficiary, purpose. Kept whole (survivor for A-216's merge). |
| A-216 | 408 | §6 | An unverified price never merges distinct obligations; only an exact duplicate obligation key locks; send-time value else integrity-passing staging price. Kept whole (merged into §6 with A-211). See FLAG-1. |
| A-217 | 467 | §8 | Releasing session must post-date the restore and use the approved credential channel; each supersession reason needs its own independent check. Kept whole (merged into §8 with A-209). |

Not collapsed here, by design:

| Item | Why |
|---|---|
| A-009 (QUIRK, 348 B) | Registry verdict assigns it to this skill's REFERENCE file, not the rule text: it records that public test-network RPC endpoints are unreachable from this VM while a keyed devnet endpoint answers reads. Platform fact, not a send rule; no other lane should collapse it either. |
| A-161 (PUBLISH, 944 B) | The owner-channel provenance definition that §7 conjunct 5 and §4's provenance rule reference BY NAME (R-057). It is a publish-lane atom; this folder references it and does not re-collapse it. The pre-publish lane collapses it; verification-core is its long-term home (three domains use it). |
| Parked-funds guard (§9) | NOT a rules-file atom. Sourced from live-memory standing state (the parked-funds / $99-guard entry; the registry's M-4 row splits money state to the ledger). Included because the brief requires the interaction; flagged so no lane hunts for an A-number that does not exist. See FLAG-6. |

## Contradiction resolutions applied

| Row | Atoms | Resolution in CURRENT-STATE | Protection dropped? |
|---|---|---|---|
| R-016 | A-061, A-181 | Not-advanced-nonce branch: clean re-check no longer self-authorises; claim stays locked, owner acceptance unlocks at most a same-nonce replacement (§3, §7) | No — later atoms govern the exit; A-061's mutual-exclusivity protection kept (RC-1) |
| R-017 | A-149, A-160 | Absolute no-release sentence deleted; proven never-sent releases without expiry on the full conjunct set (§7) | No (RC-2) |
| R-018 | A-160, A-166 | "Cannot land" reasoning removed; signed-copy accounting folded into the conjunct list (§7) | No (RC-3) |
| R-019 | A-123, A-216 | Unverified price never merges distinct obligations; exact-duplicate key only (§6) | **YES — amendment-carried; see FLAG-1** (RC-4) |
| R-020 | A-123, A-211 | Failed price → class judged on asset/beneficiary/purpose/obligation; cross-asset merge only at a verified price (§6) | **YES — amendment-carried; see FLAG-1** (RC-5) |
| R-021 | A-113, A-123 | One key definition (beneficiary, purpose, value, obligation); only route-independence kept from the older wording (§6) | No (RC-6) |
| R-022 | A-100, A-106 | Search sentence dropped; same-intent tests inside the atomic claim (§6) | No (RC-7) |
| R-023 | A-141, A-151 | Obligation rule governs; serialisation + no-invented-references kept from the older atom (§6) | No (RC-8) |
| R-024 | A-115, A-124 | Rounding never widens the effective tolerance after canonicalisation (§4) | No (RC-9) |
| R-025 | A-093, A-101 | Own-record provenance alternative removed; one provenance rule in §4 | No — the removed alternative was the hole (RC-10) |
| R-026 | A-114, A-140 | One state table with an exit per state; null/timeout/time sentence kept for all states (§7) | No (RC-11) |
| R-027 | A-140, A-149 | Empty-field definition of never-sent deleted; positive proof required (§7) | No (RC-12) |
| R-028 | A-149, A-167 | Staged-record example replaced by the independent-source definition (§7) | No (RC-13) |
| R-029 | A-181, A-190 | Acceptance unlocks only a same-nonce, same-intent replacement (§7) | No (RC-14) |
| R-048 | A-189, A-206 | Send-time actual value is the test; fixed-time/average prices are supporting evidence (§5) | No (RC-15) |
| R-049 | A-197, A-206 | Depth test scoped to trades and cross-unit bounds in the surviving text (§5) | No (RC-16) |

Dependency, gap, and duplication rows touching these atoms,
resolved structurally (no separate regression case, per the brief):

- R-056 (A-093, A-089): the surviving idea of the overwritten
  listing — a plan of unverified authorship is data — is folded
  into §4's provenance rule.
- R-057 (A-160, A-161): the positional "bullet below" pointer is
  resolved to the owner-channel provenance rule, named in §7
  conjunct 5. FLAG-5.
- R-058 (A-180, A-097): the worker-set bar invokes the shared
  inventory rules; §7 conjunct 1 cross-references verification-core
  §3–§4, where those rules are collapsed. FLAG-5.
- R-067 (A-115, A-206): gap closed by an explicit line in §4 —
  conversion of the bound at the original reference; breach tested
  at the re-send's actual expected value; both must pass.
- R-068 (A-150, A-160): gap closed in §7 — time-limit release
  exists only for expiring sends; never-expiring claims need owner
  release.
- R-069 (A-092, A-114): gap closed by an explicit line in §7 — a
  re-send that passes the safe-to-resend test closes the original
  claim; the re-send takes a fresh claim.
- R-086 (A-101, A-089): builder-tolerance rule stated once, in §4
  (A-089's text); A-101 deleted as its restatement.
- R-087 (A-062, A-063): the general deviation rule stated once, in
  §4 (A-063); §3's bundle rule keeps only atomicity and rebuild.
- R-088 (A-092, A-106): the atomic-claim-before-any-send sentence
  stated once, in §6.
- R-089 (A-114, A-140): the claim-resolution rule stated once, as
  §7's state table.
- R-090 (A-166, A-190): signed-copy conjuncts defined once (§7
  conjunct 4) and referenced by name in the abandonment paragraph.

## Flags

- **FLAG-1 — protection change carried by the latest amendment
  (R-019, R-020; §6).** A-123's clause "where source control or
  value-equivalence cannot be established, treat as same class" is
  a fail-closed protection: under doubt, block. A-216 (the newest
  amendment, v3.5.21) overrides it for the unverified-price case:
  an unverified price never merges distinct obligations and only an
  exact duplicate key locks. The collapse follows the later
  amendment and the registry's override chain, so the fail-closed
  default no longer applies where the ONLY failure is an
  integrity-failing price and the obligations are distinct. The
  protection survives everywhere else: exact duplicates lock under
  any price state; unestablishable source/beneficiary control still
  fails closed; cross-asset merges still apply at a verified price.
  The diatomic review pass separately flagged this pair for owner
  confirmation — if the owner instead picks A-123's default, §6's
  final paragraph flips back to fail-closed and RC-4/RC-5's expected
  results invert. Named here, never silently resolved.
- **FLAG-2 — A-177 lives in two places, once each.** Its
  leg-report sentence is collapsed in verification-core §2 (its
  home for reporting); its send-side clauses are collapsed in §5
  here, and deploy-verify cross-references the whole
  total-effect-bounds chain (A-177, A-182, A-189, A-197, A-206) to
  this folder. No sentence is collapsed twice; the deploy tag is
  dropped per R-079.
- **FLAG-3 — two source sentences removed as holes, not merged.**
  A-093's "or is the signed transaction's own record" provenance
  alternative (R-025) and A-160's "cannot land" reasoning (R-018)
  were deleted rather than carried: each was the exploitable half
  of its contradiction. Both deletions are named in the resolutions
  table and regression cases; the protections on the other side of
  each pair are kept in full.
- **FLAG-4 — three atoms collapsed here are registry-tagged
  PUBLISH (A-085, A-089, A-090).** They are send rules (sole
  re-sender claim; deviation-bound provenance) misfiled in the
  publish section; the pair-map files them in send chains
  (RESEND-CLAIM-AND-BOUND, INTENT-CLASS-CLAIM, DEVIATION-BOUND) and
  its lane notes assign them to this module. The pre-publish lane
  must cross-reference them, not re-collapse them.
- **FLAG-5 — two pointers resolved by name, not by importing the
  target atom.** §7 conjunct 5 depends on the owner-channel
  definition (A-161, publish lane) and §7 conjunct 1 on the shared
  inventory rules (verification-core §3–§4). Both are referenced by
  name so the target atoms are still collapsed exactly once, in
  their own folders; if verification-core's text changes, §7's
  cross-references must be re-checked.
- **FLAG-6 — §9 is standing state, not an atom.** The parked-funds
  guard comes from live memory (parked ledger, never traded, $99
  conversion watcher, send-back on the owner's word). Its
  interaction clauses are the brief's requirement, written against
  §§2–§6; they create no new send permission — a guard conversion
  and a send-back obey every rule in this file.

## Size accounting

- Source atoms in scope (registry sizes, 50 atoms): 36,747 B.
- CURRENT-STATE.md as drafted: ~25,700 B — about 70% of source.
- The pair-map lane estimate for the six send chains was ~13,000 B
  after collapse. As with verification-core, the estimate does not
  survive contact: these atoms are amendment-dense, and most of
  their bytes are conjuncts added by red-team runs (the §2 re-check
  definition, the §7 release conjuncts, the §5 integrity standard),
  not version history that can be stripped. Compressing to the
  estimate would require cutting conjuncts — i.e. dropping
  protections — so the draft keeps the content and reports the miss
  instead. Where the bytes went: §7 (lifecycle: state table + five
  release conjuncts + abandonment) and §2 (the re-check definition)
  are the sections that cannot shrink without losing distinctions
  the red-team runs added them for.
