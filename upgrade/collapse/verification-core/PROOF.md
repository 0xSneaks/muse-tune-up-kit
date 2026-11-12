# verification-core — collapse proof (DRAFT)

Atom-by-atom coverage: where each source atom's operative content
lives in CURRENT-STATE.md. Source byte sizes are the ATOM-REGISTRY
figures for the live rules-file atoms. Nothing in the live file was
edited; this folder is a draft in the upgrade clone only.

| Atom | Size (B) | Operative content lands in | Notes |
|---|---|---|---|
| A-016 | 542 | §1 | Read-back before "done"; deploy actual-vs-expected folded in from the same Deployments base text. Kept whole. |
| A-017 | 3,866 | §2, §3, §4 (flag) | The big atom, split as the registry directs: leg-by-leg reporting + masked read-back + functional-probe standard → §2; total-effect sentence → §2 (see A-177 note); leg-inventory-first from an independent source → §3; the UNVERIFIED flag that D8 adds → §3/§4. Kept whole. |
| A-018 | 694 | §3 | Distinct infrastructure, not provenance; common-mode sources count as one; completeness probed per source. Kept whole. |
| A-019 | 725 | §3 | Out-of-band establishment of distinctness; system-under-test answers to completeness probes are self-reports. Kept whole (merged with A-018 per registry MERGE direction, survivor wording consolidated in §3). |
| A-097 | 404 | §4 | UNVERIFIED inventory blocks irreversible / multi-target execution, except legs that establish the inventory. Kept whole. |
| A-102 | 347 | §3 | Receiving system corroborates only if its own data upstream is shown distinct; same-upstream wallet/explorer = same source. Kept whole (registry MERGE survivor was A-019's clause set; §3 carries it inside the inventory rule). |
| A-145 | 818 | §5 | Mutable self-created destination is a continuing leg; one clean re-check never closes it; closes on immutable / made private or destroyed / operation ends. Closure wording fixed per R-077 (source text read "de-privatised/destroyed", meaning made public — the opposite of the intended event; see REGRESSION RC-4). |
| A-156 | 681 | §5 | Interval + per-leg reporting + never-verified status. C1 rulings applied: reads "interval of at most 24 hours" (the source's "sibling-clause floor" wording dropped — it called a maximum a floor); the deferral cap sits in §7 in the same rule as the deferral it caps (R-051). Its non-blocking clause is restated as applying only after dependency enumeration (R-047); the dependency definition itself is the A-164 qualification of this atom, carried in §5 and attributed there. |
| A-184 | 496 | §6 | Audience-identical fetch (ordinary profile, warm cache, no cache-buster); cache-busted proves origin only. Kept whole. |
| A-191 | 680 | §6 | Coverage across viewer classes / geographies / session states; one vantage = scoped claim only. The per-segment accounting step (covered / owner-scoped-out / unverified) is added per R-076 — additive, no content removed. |
| A-193 | 546 | §8 | Load-bearing hash = full strong digest (SHA-256 full hex or stronger) over exact bytes; truncated/weak = no hash. Kept whole. |
| A-202 | 544 | §8 | Low-entropy values: keyed digest with key stored elsewhere, or present/absent only. Kept whole, under the A-205 precedence ruling. |
| A-205 | 744 | §8 | Keyed-digest precedence over the plain-digest rule for low-entropy values; record algorithm + key id + custody; no key available = presence-only, never a plain-digest fallback. Kept whole. Purpose-separated keys (§8 last sentence) come from the v3.5.21 qualification of this clause set. |
| A-213 | 612 | §7 | Authorised-vantage inventory per continuing leg; owner's device/session only on explicit authorisation; else UNVERIFIED + defer. C1 ruling applied: the atom's pointer to a "v3.5.19 vantage bullet" is a dead label — retargeted to the v3.5.20 audience-vantage bullet (§7's own text) as qualified by v3.5.21 (§7 cap + provenance, via A-219). |
| A-219 | 493 | §7 | Deferral capped at 3 cycles / 7 days, then escalate + block dependents; authorisation counts only via the owner's own channel. Kept whole. |
| A-177 (not a chain atom) | 679 | §2, one sentence | Included only as instructed: Muse's C1 ruling says A-177 is self-contained and its sentence IS the principle — deviation/materiality bounds are judged on the total effect on the user in one numeraire, not field-by-field. It sits in §2 because a leg report's "verified" status is where the total-effect test bites. A-177's send-side clauses (bound-field breach blocks a send, numeraire mechanics) are NOT in this chain and are not duplicated here; they belong to onchain-send. |

## Contradiction resolutions applied

| Row | Atoms | Resolution in CURRENT-STATE | Protection dropped? |
|---|---|---|---|
| R-047 | A-156, A-164 | Default-dependent until enumeration completes; A-156's non-blocking clause applies only after enumeration (§5) | No — both sides kept (see REGRESSION RC-1) |
| R-051 | A-156, A-213 | 3-cycle / 7-day deferral cap stated in the same rule as the deferral (§5 + §7) | No (RC-2) |
| R-076 | A-191, A-213 | Per-segment list: covered / owner-scoped-out (named, not verified) / unverified (§6) | No (RC-3) |
| R-077 | A-145, A-156 | "made private or destroyed"; "interval of at most 24 hours" (§5) | No — wording fix (RC-4) |

**DROP-PROTECTION flags: none.** No resolution in this chain drops a
protection; the four contradictions were an ambiguity (R-047), a
missing cap (R-051), a missing procedure step (R-076) and inverted
wording (R-077), and each resolution is additive or clarifying.

## Addendum (step 7, lane B8)

A-091 (553 B) — the cross-check observable-types clause — had no
collapsed home (pre-publish PROOF FLAG-2); it is now homed in §3
(competence per leg type; a blind source's agreement is vacuous),
closing that gap. Reflected in skill `verification-core` under
LEG-INVENTORY.

## Size accounting

- Source atoms (registry sizes, 15 atoms): 12,192 B.
- CURRENT-STATE.md as drafted: 10,277 B — only ~16% smaller.
- The pair-map lane estimate for this chain was ~5,200 B after
  collapse. That estimate does not survive contact with the atoms:
  unlike the amendment-heavy chains, these 15 atoms are mostly base
  current-state prose already (A-017 alone is 3,866 B of operative
  text with almost no version history in it). Compressing to 5,200 B
  would require cutting operative clauses — i.e. dropping protections
  — so the draft keeps the content and reports the miss instead.
  Where the bytes went: §3 (inventory independence) and §2 (probe
  standard) are the two sections that cannot shrink without losing
  the distinctions the red-team runs added them for.
