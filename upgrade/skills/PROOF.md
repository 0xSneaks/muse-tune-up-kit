# Step 7 PROOF — the five rule skills

Lane B8 (Blue-8 via Muse). Sources: the five reconciled collapse
drafts (`../collapse/<name>/CURRENT-STATE.md`), SPEC-DELTA D2/D3
skill shape (platform layout, core SKILL.md ≤ 8 KB, reference files
carry the long form). The C2 media ruling was NOT applied anywhere.

## Method — gate ownership

No canonical gate→skill table exists in the sources (spec 05
§5.2/§5.3 and spec 01 §1.4 predate the five-skill split). Ownership
was therefore derived per skill: a gate row exists where the
skill's CURRENT-STATE carries a check-bearing section, named by the
spec-05 gate name where one applies, otherwise by the section's own
check name. Every gate row in every SKILL.md cites its source
section(s); the tables below are extracted from the files as
written, not reconstructed.

## Per-skill results

### verification-core — 6,311 B (band 4,000–8,000 ✓)
- Sections covered: §1–§8 of 8 — all.
- Gates listed: 8. Gates in source: 8. **MATCH.**
  READBACK-REQUIRED (§1) · LEG-INVENTORY (§3, §4) · MASKED-VALUE
  (§2) · TOTAL-EFFECT (§2) · CONTINUING-LEG (§5) · VERIFIED-LIVE
  (§6) · VANTAGE-AUTHORISATION (§7) · DIGEST-STANDARD (§8).
- A-091 lives here — see below.

### media-verify — 8,000 B (band ✓, at ceiling)
- Sections covered: §1–§12 of 12 — all, one gate per section.
- Gates listed: 12. Gates in source: 12. **MATCH.**
  OPEN-AND-LOOK (§1) · MEDIA-INJECTION-GUARD (§2) ·
  EVERY-REPRESENTATION (§3) · THUMBNAIL-POSTER (§4) · AUDIO-LEG
  (§5) · BYTE-LEG (§6) · FRAME-COVERAGE (§7) · TIMING-DECODE (§8) ·
  TRANSFORM-SET (§9) · PARSER-DIFFERENTIAL (§10) ·
  PLAIN-MEANING-ASSEMBLY (§11) · BYTES-NOT-PATHS (§12).
- Both UNSATISFIABLE-AS-WRITTEN pairs are carried in the skill
  exactly as written in the source, markers intact (2 markers,
  at FRAME-COVERAGE §7 and TRANSFORM-SET §9), with the proposed
  rulings quoted but NOT applied.

### deploy-verify — 5,894 B (band ✓)
- Sections covered: §1–§4 of 4 check-bearing sections. §5 and §6
  of the source are cross-reference sections (carried elsewhere),
  pointed to, not gated.
- Gates listed: 4. Gates in source: 4. **MATCH.**
  DEPLOY-TARGET (§1) · COMPLETION-REDRAW (§2) · CREDENTIAL-PROBE
  (§3) · SNAPSHOT-RETENTION (§4).

### onchain-send — 7,900 B (band ✓)
- Sections covered: §1–§9 of 9. §1 (the working route, no exempt
  stack) is carried as the skill's standing operative rule, not a
  gate row — it states a route, not a check.
- Gates listed: 8. Gates in source: 8. **MATCH.**
  UNKNOWN-OUTCOME (§2) · SAFE-TO-RESEND (§3) · STATED-BOUND (§4) ·
  PRICE-INTEGRITY (§5) · CLASS-CLAIM (§6) · CLAIM-RELEASE (§7) ·
  CLAIM-RECORD-INTEGRITY (§8) · PARKED-FUNDS (§9).

### pre-publish — 7,988 B (band ✓)
- Sections covered: §1–§13 of 13 check-bearing sections. §14 of
  the source is cross-reference only (carried elsewhere), pointed
  to, not gated.
- Gates listed: 11. Gates in source: 11. **MATCH.**
  FINISHED-ARTIFACT-SCAN (§1, §2 — the §2 owner-exemption clause is
  stated inside this row) · CONSTITUENT-SET (§3) ·
  LINK-DESTINATIONS (§4) · LINK-CLOSURE (§5, §6) ·
  CROSS-ARTIFACT-ASSEMBLY (§7) · HISTORY-INVENTORY (§8) ·
  GENERATED-VARIANTS (§9) · WAIVER (§10) · PERSONALISED-SNAPSHOT
  (§11) · LIVE-GATE-VARIANT (§12) · SCHEDULED-SNAPSHOT (§13).

## Dangling-pointer check — PASS, zero dangling

Method: every § reference in each SKILL.md was extracted and
checked against the section inventory of the CURRENT-STATE it
points at (own-skill references against its own file; cross-skill
references against the named skill's file).

- Own-skill references: verification-core §1–§8 (source has §1–§8)
  · media-verify §1–§12 (source §1–§12) · deploy-verify §1–§6
  (source §1–§6) · onchain-send §1–§9 (source §1–§9) · pre-publish
  §1–§14 (source §1–§14). All resolve.
- Cross-skill references, each verified against the target file:
  deploy-verify → verification-core §8, pre-publish §10, §11,
  media-verify §10 · media-verify → verification-core §8 ·
  onchain-send → verification-core §3–§4 · pre-publish →
  verification-core §1–§8 and §3–§4, media-verify §2, §4, §11, §12,
  deploy-verify §2, §4. All resolve.
- Every relative path pointer (`../../collapse/<name>/…`) names a
  file that exists in the tree.

## A-091 — closed

Atom A-091 (AGENTS.md v3.5.5 cross-check competence bullet; registry
row `| A-091 | 35290d4b | 553 | PUBLISH |`) had no collapsed home
(pre-publish PROOF FLAG-2). It is now homed in
`../collapse/verification-core/CURRENT-STATE.md` §3 (leg-inventory
territory, its parent gate): a paragraph stating competence is per
leg type, that a blind source's agreement is vacuous, and that legs
with only a blind cross-check stay UNVERIFIED. The §3 header atom
list is annotated, a one-line addendum was added to
`../collapse/verification-core/PROOF.md`, and the clause is
reflected in the verification-core skill under gate LEG-INVENTORY.
