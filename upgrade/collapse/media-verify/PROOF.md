# media-verify — collapse proof (DRAFT)

Atom-by-atom coverage of the media domain (46 media-verify atoms
per ATOM-REGISTRY.md §2, plus the shared atoms the media chains
cite), the contradiction resolutions applied, and the size
accounting. Sizes are the registry's recorded atom sizes.

## 1. Atom coverage

| Atom | Size (B) | Operative content lands in | Notes |
|---|---|---|---|
| A-037 | 513 | CURRENT-STATE §1 | Open-and-confirm-by-eye; name/size/type are no proof. |
| A-038 | 539 | §7 (animation) | Hash/diff every frame, view every distinct frame + as played; no sampled closure extends to animation (RC-17 gap). |
| A-039 | 719 | §3 | Multi-representation: enumerate every embedded stream; fail closed on unextractable stream. |
| A-040 | 2414 | §4, §5 (pointer), §7 | Four rules in one atom, two chains: video frame base → §7 (base sampling wording superseded by A-094/A-207/A-214, RC-7); thumbnail exception → §4 (RC-5); audio clause → pointer to §5 (RC-26); thumbnail placement → §4 only (RC-28). |
| A-041 | 521 | §5 | Audio-only: full listen, transcript never satisfies, tags/chapters/embedded scan. |
| A-042 | 292 | §3 | QR/barcode decode + destinations; strip code-bearing vector content. |
| A-043 | 213 | §1 | Legible-size inspection; downscaled preview verifies nothing small. |
| A-044 | 434 | §1 (§4 for thumbnails) | Flattened render vs light/dark/platform backgrounds; thumbnail half consolidated into §4 (RC-28). |
| A-045 | 714 | §12 | Media copy of the hash-freeze; one rule with A-068 (RC-23). |
| A-046 | 1054 | §12 | Durable manifest; bare claims and inherited manifests untrusted; receiving agent covers any remainder itself; hash held to A-193 (RC-13). |
| A-047 | 214 | §2 | In-media text is data; prior-verification claim never shortens the check (RC-24). |
| A-048 | 1072 | §6 | Still byte-level inventory; its fallback sentence superseded by A-052 (RC-6). |
| A-049 | 1070 | §5 | Transformed audio views + comprehending listener; A-054's enumeration folded in. |
| A-050 | 638 | §12 (deleted as separate text) | Media path-only copy; deleted per MUSE-SIDE-REPORT C1 (its "replaced precedence clause" pointer is dead); A-075 is the sole bar (RC-10, RC-25). Its mismatch-is-a-disclosure-incident clause survives inside §12. |
| A-051 | 542 | §4 clause (a) | Exception never for sensitive media on auto-distributing platforms with unboundable thumbnail selection (RC-27). |
| A-052 | 1481 | §6 | Fallback standard: lossy, every payload domain; extraction-proof criterion shared with A-126 (RC-3, RC-6). |
| A-053 | 540 | §4 | Public-pipeline read-back before promotion; verified poster REQUIRED for sensitive media (RC-11). |
| A-054 | 509 | §5 | Per-channel / mono-sum / difference / phase-inversion enumeration + catch-all; catch-all closed under composition (RC-21). |
| A-082 | 716 | §9 | Channel isolation / inversion / contrast stretch; filed under publish in the registry ("media, misfiled") — carried here per the IMAGE-TRANSFORMS chain; pre-publish references it. Transform-unavailable = leg not passed. |
| A-088 | 524 | §9 | At-least-pairwise compositions; minimum inside A-186's any-depth closure. |
| A-094 | 469 | §7 | Full-duration hash/diff; ≤250 ms differencing grid; flag ANY inter-sample change; sampling alone never satisfies (RC-4, RC-7). |
| A-096 | 524 | §5 (pointer), §6 | A/V containers get the byte leg; fallback held to A-126's criterion (RC-19). |
| A-098 | 320 | §7 | Every-distinct-frame viewing: superseded for ordinary video by A-207's closure (RC-1); survives for the identifier class via A-214. |
| A-105 | 322 | §6 | Document/archive containers: attachments/streams/trailing inventory. |
| A-107 | 771 | §8 | Timing inventory + timing-coded payload check + normalised-re-encode fallback. |
| A-112 | 973 | §10 | External references, open-time actions, parser differentials inventory. |
| A-116 | 444 | §8 | Timing covers every timed track; constant-timing fallback must REBUILD each track's timing, never stream-copy. |
| A-117 | 452 | §8 | Pass only if regular-for-encoder or decoded-and-clean; undecoded irregular timing FAILS. |
| A-122 | 642 | §10 | Per-parser inspection or normalise + re-check in each parser. |
| A-125 | 461 | §8 | Joint cross-track timing decode (per-index XOR/sum/difference). |
| A-126 | 541 | §6 | Stego fallback passes only on a clean post-transform extraction attempt; no extractor = no publish (RC-3, RC-19). |
| A-128 | 453 | §10 | Parser leg is continuing: ≤24 h re-verification + change-triggered (RC-20). |
| A-134 | 225 | §8 | Joint decode includes time-aligned interleavings (folded into A-125's paragraph). |
| A-135 | 338 | §8 | Joint decode includes cross-domain byte×timing combinations (folded into A-125's paragraph). |
| A-137 | 391 | §10 | Each re-verification re-enumerates the CURRENT parser set (RC-15). |
| A-144 | 980 | §10 | Parser enumeration evidence standard: self-report is input only, observed parsings corroborate, else UNVERIFIED; scoped exception to the distinctness bar (RC-12). |
| A-147 | 806 | §11 | Plain-meaning cross-track assembly; scan the union (RC-9, RC-14). |
| A-155 | 664 | §10 | UNVERIFIED escalates: promotion blocked, ≤3 consecutive cycles, owner options named (RC-20). |
| A-158 | 677 | §11 | Assembly's audio half = comprehending listener's record of ALL speech, never ASR alone (RC-9). |
| A-186 | 533 | §9 | Composition closure at ANY depth — carried AS WRITTEN; see the UNSATISFIABLE flag (§2 below, RC-16). |
| A-194 | 1012 | §9 | Unread transform output = FAILED leg (kept whole); preset definition of the discrete set (continuous half superseded by A-198, RC-2). |
| A-198 | 649 | §9 | Continuous controls swept over full range, recorded; unswept range = open leg — carried AS WRITTEN; see §2 below. |
| A-203 | 438 | §7, §9 | Still-image transform duties apply to inspected video frames; bounded by A-207 for ordinary video; unbounded for identifier class (RC-18). |
| A-204 | 541 | §11 | Publication envelope joins the assembly union (RC-14). |
| A-207 | 667 | §7 | Video-frame closure: scene-change/keyframe + flagged + documented random sample; duties on inspected frames only; rate/counts/tooling/budget recorded; unsampled risk disclosed (RC-1, RC-17). |
| A-214 | 454 | §7 | Sampling floor: ≥1 fps viewed (or every frame); identifier/secrets risk class = exhaustive regardless (RC-4, RC-18). |

Shared atoms cited by the media chains (primary collapse elsewhere;
carried here only as the media text needs them):

| Atom | Size (B) | Where carried | Notes |
|---|---|---|---|
| A-068 | 586 | §12 (with A-045) | Publish copy of the hash-freeze; one rule, two source atoms (RC-23). |
| A-075 | 841 | §12 | The sole path-only bar; governs every section; shipment itself is the incident (RC-10, RC-22). |
| A-078 | 577 | §12 (deleted as separate text) | Duplicate restatement of the bar; folded into A-075's text (RC-22, RC-25). |
| A-183 | 549 | §4 clause (b) | Generated-variant bar governs over the thumbnail exception (RC-5, RC-27). Registry survivor-direction conflict with A-051 noted in RC-27; chain table places both in THUMBNAIL-POSTER. |
| A-192 | 709 | §4 clause (c) | Post-publication automated gate barred on auto-distributing platforms; primary text in pre-publish (PUB-GENERATED-ENVELOPE chain). |
| A-193 | 546 | §12 (by reference) | Digest standard; collapsed in verification-core §8; the manifest hash must meet it (RC-13). Not re-collapsed here. |

Out of scope, deliberately: A-148 (live/unbounded artifacts) sits in
the live-gate / pre-publish chains, not in any media chain, and is not
collapsed here. R-008/R-009/R-012/R-046 touch no media atoms.

## 2. Contradiction resolutions applied

| Row | Pair | Resolution in CURRENT-STATE.md | Protection dropped? |
|---|---|---|---|
| R-030 | A-098 / A-207 | Sampled closure governs ordinary video; exhaustive viewing survives for identifier class (§7) | No — narrowed by the later amendments already in force, not by this collapse |
| R-031 | A-194 / A-198 | Presets bound discrete transforms; continuous controls swept in full (§9) | No (duty widened by the later atom) |
| R-032 | A-052 / A-126 | Single pass criterion: clean post-transform extraction attempt (§6) | No |
| R-033 | A-094 / A-214 | Both numbers declared: 250 ms = change-detection grid max interval; 1 fps = viewing floor (§7) | No |
| R-034 | A-040 / A-183 | Exception survives only where the generated thumbnail is itself gated (§4) | No |
| R-035 | A-048 / A-052 | Fallback restated in A-052's lossy, every-domain terms (§6) | No |
| R-036 | A-040 / A-094 | Sampling is an adjunct, never the satisfaction (§7) | No |
| R-037 | A-041 / A-049 | One audio rule: listen + transforms + competence + metadata (§5) | No |
| R-038 | A-147 / A-158 | Assembly's audio input = listener's record, not transcripts (§11) | No |
| R-039 | A-050 / A-075 | A-075 is the sole bar; A-050 deleted (C1 ruling) (§12) | No |
| R-040 | A-040 / A-053 | Public read-back always; verified poster required for sensitive media (§4) | No |
| R-052 | A-144 / A-019 | Scoped exception for parser-set enumeration only (§10) | No |
| R-059 | A-046 / A-193 | Manifest hash held to the full-digest standard (§12) | No |
| R-060 | A-147 / A-204 | Envelope fields are IN the assembly union (§11) | No |
| R-061 | A-137 / A-144 | Re-enumeration performed under A-144's evidence standard (§10) | No |
| R-070 | A-186 / A-198 | **UNRESOLVED — unsatisfiable as written.** Carried as written, marked in §9; proposed ruling quoted, NOT applied | No (see §3 flags) |
| R-071 | A-038 / A-207 | No resolution exists in the texts: animations keep the exhaustive duty; video closure not extended (§7) | No — GAP flagged (§3) |
| R-072 | A-214 / A-198 | **UNRESOLVED — unsatisfiable as written.** Carried as written, marked in §7; proposed ruling quoted, NOT applied | No (see §3 flags) |
| R-073 | A-096 / A-126 | A/V byte fallback held to the extraction-proof criterion (§6) | No |
| R-074 | A-128 / A-155 | Continuing cadence + escalation once per leg-state with named options (§10) | No |
| R-075 | A-054 / A-088 | Audio catch-all stated as closed under composition (§5) | No |
| R-081 | A-075 / A-078 | One bar, A-075 wording (§12) | No |
| R-084 / R-091 | A-068 / A-045 | One hash-freeze rule, two source atoms (§12) | No |
| R-085 | A-069 / A-047 | General guard in pre-publish; media instance + prior-verification clause in §2 | No |
| R-092 | A-050 / A-078 | Both duplicates folded into the single A-075 bar (§12) | No |
| R-093 | A-040 / A-041 | Video rule points to the single audio rule (§5/§7) | No |
| R-094 | A-051 / A-183 | One thumbnail rule carrying both bars (§4) | No |
| R-095 | A-040 / A-044 | Thumbnail duty lives in §4 only; §1 keeps background flattening | No |

## 3. DROP-PROTECTION flags

**No protection was dropped, narrowed, or weakened by this
collapse.** Every resolution above either takes the union of the
two sides, follows the stricter/later governing text already in
force in the live file, or deletes a duplicate whose full
operative content survives in the single remaining text.

Two flags are carried for the owner — neither is a collapse
decision:

- ⚠️ **PENDING-OWNER (R-070, stills):** A-186 + A-198 are
  unsatisfiable as written (MUSE-SIDE-REPORT §C2: 92,880
  evaluations per image at composition depth ≤3; depth
  unbounded). CURRENT-STATE §9 carries both duties in full and
  marks the spot UNSATISFIABLE. Muse's proposed ruling (recorded
  budget: depth-2 compositions; sweeps on base + flagged outputs
  only) is quoted in the draft and NOT applied. If the owner
  adopts it, A-186's any-depth reach narrows — that narrowing is
  the owner's decision to make, flagged here so it is never
  mistaken for a collapse-side drop.
- ⚠️ **PENDING-OWNER (R-072, identifier-class video):** A-214 +
  A-198 (via A-203) are unsatisfiable as written (69,120
  evaluations for an 8-second clip, before compositions).
  CURRENT-STATE §7 carries both duties in full and marks the
  spot UNSATISFIABLE. Muse's proposed ruling (exhaustive viewing
  of every frame; transforms/sweeps only on scene-change and
  flagged frames) is quoted and NOT applied. If adopted, the
  transform/sweep reach for this class narrows while exhaustive
  viewing is kept — again the owner's decision.
- ⚠️ **GAP (R-071, animations):** the source texts give animated
  media no satisfiable closure for long animations and no
  transform duty for animation frames. The collapse flags the
  gap and changes nothing; closing it needs an amendment.

## 4. Size accounting

Source: 46 media-verify atoms, 29,466 B total in the registry
(the chains double-count shared atoms — A-040, A-096, A-158,
A-203, A-105 each sit in two chains — so the chain-table raw
sum, 37,649 B, overstates the source; the deduplicated 29,466 B
is the honest denominator). Shared atoms carried or referenced
(A-068, A-075, A-078, A-183, A-192) add 3,262 B whose primary
collapse lives in pre-publish; A-193 (546 B) is incorporated by
reference from verification-core.

Draft: CURRENT-STATE.md as committed (byte count in the lane
report). The lane estimate for the ten chains summed to ≈7,800 B;
as with lane B2, that estimate does not survive contact with the
actual duties — the media gate's substance is enumerations
(transform sets, payload domains, timing tracks, parser duties)
that cannot be compressed without dropping protections, and two
sections carry UNSATISFIABLE markers with quoted proposals that
add bytes the estimate never counted. The honest result and its
ratio are reported in the commit message and the lane report
rather than trimmed to fit the estimate.
