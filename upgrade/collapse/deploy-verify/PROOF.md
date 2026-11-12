# deploy-verify — collapse proof (DRAFT)

Atom-by-atom coverage for the deploy domain: where each deploy
atom's operative content lives after this collapse. Source byte
sizes are the ATOM-REGISTRY figures. Nothing in the live file was
edited; this folder is a draft in the upgrade clone only. Atoms
lane B2 already collapsed into verification-core are cross-
referenced, never duplicated, per the lane brief.

## Collapsed here (CURRENT-STATE.md)

| Atom | Size (B) | Lands in | Notes |
|---|---|---|---|
| A-014 | 286 | §1 | Platform-override check before any deploy; risk stated in the approval request. Kept whole. Not in verification-core (its §1 carries read-back, not the pre-deploy override duty). |
| A-129 | 390 | §2 | Completion re-enumeration including self-created legs. Merged with A-178 into one completion rule per R-098. |
| A-138 | 341 | §2 | Completion provisional until the delayed async re-check. The "stated window" gains a maximum — see FLAG-4. |
| A-142 | 873 | §3 | Non-destructive probe duty: determine consume/rotate behaviour first; non-consuming route preferred; do-not-probe reporting. Its "capture-and-restore atomically" wording is NOT carried — replaced by A-153's protocol per R-045 (FLAG-3). |
| A-153 | 691 | §3 | Capture-and-restore as confirmed-store protocol; failure between rotation and confirmed store is an incident; successor is the verified value. Its "unknown side-effects are an open leg" treatment is superseded by A-162 for the unknown case per R-044 (FLAG-3); known side-effects remain inventoried legs. |
| A-162 | 835 | §3 | Two-part pre-probe determination: (a) consume/rotate/invalidate, (b) side-effect scope; either undeterminable bars the probe. Survivor of the probe chain; absorbs A-152. |
| A-169 | 713 | §3 | Determination counts only from sources matching this account's tier/plan, auth configuration and API version, recorded with source, version and date; conflicts are undeterminable. Kept whole. |
| A-178 | 668 | §2 | Late-provisioned self-created legs are unaccounted from the moment they exist, immutable ones included. Merged with A-129 per R-098; finality behaviour per R-078. |
| A-212 | 572 | §4 | Durable snapshot record: keyed digest or presence marker per recipient, never plaintext; working plaintext restricted to approved/ephemeral store. Merged with A-220 per R-054. Homing tension: FLAG-5. |
| A-220 | 445 | §4 | 30-day deletion deadline runs from staging for never-sent snapshots; deletion verified by independent read-back; purpose-separated digest key. Registry homes this atom in pre-publish; collapsed here because its entire content amends A-212's rule — FLAG-5. |

## Dropped as an atom (content preserved)

| Atom | Size (B) | Where its content lives | Reason |
|---|---|---|---|
| A-152 | 553 | §3, as clause (a)'s consequence inside the A-162 determination | Registry verdict DELETE (survivor A-162); R-099 confirms it is clause (a) of the later two-part rule with the same reported status. Nothing A-152 forbade is permitted by §3. FLAG-2. |

## Cross-referenced to verification-core (collapsed by lane B2 — not duplicated here)

| Atom | Size (B) | verification-core |
|---|---|---|
| A-015 | 140 | §1 (folded in by B2 with the base Deployments text) |
| A-016 | 542 | §1 |
| A-017 | 3,866 | §2, §3 |
| A-018 | 694 | §3 |
| A-019 | 725 | §3 |
| A-097 | 404 | §4 (the UNVERIFIED flag; D8's execution block) |
| A-102 | 347 | §3 |
| A-145 | 818 | §5 — see FLAG-1 (RESOLVED-BY-OWNER, 2026-11-12) |
| A-156 | 681 | §5, §7 |
| A-164 | 1,053 | §5 (carried as the dependency definition qualifying A-156; B2 gives it no PROOF row of its own — coverage exists, attribution is thin) |
| A-171 | 762 | §5 (the every-hop resolution inside the same paragraph; likewise no PROOF row of its own) |
| A-184 | 496 | §6 |
| A-191 | 680 | §6 |
| A-193 | 546 | §8 |
| A-202 | 544 | §8 |
| A-205 | 744 | §8 |
| A-213 | 612 | §7 |
| A-219 | 493 | §7 |

## Cross-referenced to other domain skills (not deploy-verify's to collapse)

| Atom | Size (B) | Home |
|---|---|---|
| A-070, A-146, A-185, A-196, A-210, A-215, A-218 | 1,889 / 785 / 557 / 793 / 710 / 610 / 435 | pre-publish — the waiver and interaction-variant chain. The lane brief's topic list names "waiver/variant rules"; the registry homes every one of these atoms in pre-publish and the pair map files the waiver chain in the publish lane, so they are cross-referenced here (§6), not collapsed. FLAG-5. |
| A-087 | 672 | pre-publish — the send-time snapshot gate; §4 carries only A-212/A-220's record-and-retention half |
| A-083, A-130, A-139 | 597 / 409 / 319 | pre-publish (substance also in verification-core §6) |
| A-109, A-119 | 647 / 465 | pre-publish, on verification-core §3 |
| A-144 | 980 | media-verify — the parser-set exception; pointer carried in §5 per R-052 |
| A-148, A-159 | 867 / 406 | pre-publish — live-gate variants |
| A-177, A-182, A-189, A-197, A-206 | 679 / 521 / 1,014 / 647 / 601 | onchain-send — total-effect-bounds chain; deploy tag dropped per R-079. A-177's one total-effect sentence for leg reports is already in verification-core §2 (B2). No content dropped; the chain was never deploy law. |

## Contradiction resolutions applied

19 regression cases (REGRESSION.md RC-1…RC-19) for rows R-041,
R-042, R-043, R-044, R-045, R-046, R-050, R-052, R-053, R-054,
R-062, R-063, R-078, R-079, R-080, R-096, R-098, R-099, R-100.
B2 already covered R-047, R-051, R-076, R-077; R-004 duplicates
R-041's pair and is not recounted. Summary of protections: every
resolution keeps both sides' protections except the three items
named in FLAG-3, which are tightenings (a weaker wording or
sequencing replaced by its own later, stricter amendment), and
FLAG-1, a divergence from verification-core §5 that the owner
resolved in §5's favour on 2026-11-12 (RESOLVED-BY-OWNER, below).

## Flags (named, never silent)

- **FLAG-1 — RESOLVED-BY-OWNER (2026-11-12).** Owner ruling on
  R-050: "When it's done it's done." Operation end CLOSES a
  continuing leg. Verification-core §5 stands exactly as drafted
  (no correction needed), regression RC-7's expected outcome is
  flipped to closure-at-end, and CURRENT-STATE §5 now follows
  verification-core with no divergence. The divergence this flag
  recorded is closed by the owner's word, not by either lane.
  History, as originally flagged: **DROP-PROTECTION RISK, in
  verification-core §5 (lane B2's draft), not in this folder.**
  R-050's resolution: a continuing leg closes only on
  immutability, privacy or destruction; operation end alone hands
  it over. Verification-core §5 as drafted still lists "or the
  operation itself ends" as a closure condition, so §5 does not
  pass regression RC-7. This draft follows R-050 and records the
  divergence in CURRENT-STATE §5. The orchestrator/B2 must correct
  §5 or explicitly overrule R-050; until then the two drafts
  disagree on a closure condition for public mutable
  destinations.
- **FLAG-2 — DROPPED ATOM, content preserved.** A-152 is deleted
  as a standalone atom (registry-directed, survivor A-162). Its
  full operative content — undeterminable consume behaviour means
  treat as consumable, no probe, presence-verified /
  value-unverified — is clause (a)'s consequence in §3.
- **FLAG-3 — SUPERSEDED WORDING/TREATMENT, both tightenings.**
  (a) A-142's "capture-and-restore atomically" is dropped in
  favour of A-153's stored-AND-read-back-confirmed protocol
  (R-045). (b) A-153's "unknown side-effects are an open leg" is
  dropped in favour of A-162's "unknown side-effects bar the
  probe" (R-044); known side-effects remain inventoried legs. In
  both cases the dropped text is the earlier, weaker half of the
  atom's own amendment chain — no protection the later text carries
  is lost.
- **FLAG-4 — DECISION introduced by this collapse.** R-078
  requires a stated maximum for the async re-check window but
  names no number. §2 sets the maximum at 24 hours, anchored to
  the bundle's own outer bound for post-publication re-checks. It
  only tightens (an unstated or longer window now fails the
  claim), but the number is this lane's choice and wants the
  reviewer lane's confirmation.
- **FLAG-5 — HOMING tensions for the orchestrator.** (a) A-212 +
  A-220 are collapsed here per the lane brief's topic list
  (snapshot rules), while the registry homes A-220 in pre-publish
  and R-054/R-080 file the merged snapshot rule beside the
  personalised-send procedure. If the pre-publish lane takes the
  merged rule, §4 becomes a cross-reference; the content must exist
  exactly once. (b) The waiver/variant atoms are likewise named in
  the brief's topics but registry-homed in pre-publish; they are
  cross-referenced (§6), not collapsed, to avoid a second copy.
- **FLAG-6 — GAP in verification-core §3.** R-052's resolution
  requires the core to mention that the parser-set exception
  exists; §3 as drafted does not. CURRENT-STATE §5 carries the
  pointer for deploy readers; the fix itself belongs in B2's
  folder.

**DROP-PROTECTION flags in this folder's own resolutions: none
silent, and none net.** FLAG-1 was a protection B2's draft
appeared to drop; the owner ruled for B2's text on 2026-11-12, so
that closure reading is now owner-decided and recorded, not a
silent drop by either lane; FLAG-3's two items replace
weaker text with the stricter later amendment; FLAG-2 deletes an
atom whose content survives entire.

## Size accounting

- Source atoms collapsed here (registry sizes, 11 atoms including
  the subsumed A-152): 6,367 B.
- CURRENT-STATE.md as drafted: 10,352 B against 6,367 B of source
  atoms collapsed here — larger, not smaller, and the reason is
  stated plainly: most of §1–§4's source text was already
  current-state prose, while §5 and §6 (the cross-reference tables
  that keep this skill from dangling, per R-062) are new bytes
  with no source-atom counterpart. The sections that collapse
  actual amendment chains (§2: three atoms into one rule; §3: five
  atoms into one rule) do shrink their sources; the file as a
  whole does not, because it also carries the domain's map to
  verification-core. No operative clause was cut to hit a size
  target.
- Cross-referenced atoms total 28,750 B of registry size
  (18 verification-core, 16 other-skill, 5 onchain-send) — listed
  here so the deploy domain's full coverage can be audited from
  this one file.
