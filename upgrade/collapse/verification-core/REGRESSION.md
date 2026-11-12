# verification-core — regression cases (DRAFT)

One case per contradiction row in PAIR-MAP-RULES.md touching this
chain's atoms. Each case is built so the old (pre-collapse) reading
and the collapsed rule give different outcomes; the collapsed rule
must produce the expected result. No case below drops a protection:
where the two sides carried different protections, the resolution
keeps both, and the case names them.

## RC-1 — R-047 (A-156 vs A-164): dependency is enumerated, not self-assessed

- Setup: an operation creates a public preview page (mutable,
  CONTINUING) and ships a deliverable page. The reporting agent
  believes the deliverable does not depend on the preview and, under
  the A-156 sentence "never silently blocks legs that do not depend
  on it", reports the deliverable VERIFIED without enumerating its
  links. The deliverable in fact embeds the preview through a
  link-shortener hop.
- Old-rule outcome: ambiguous and exploitable — A-156's non-blocking
  clause reads as permission to proceed on the agent's own view of
  dependency; A-164 (later) says self-assessment is not evidence and
  unknown means dependent. The two atoms give opposite answers to the
  same report.
- New-rule outcome (CURRENT-STATE §5): dependency is established only
  by enumerating outbound links/embeds/references, resolved through
  every hop; until that enumeration completes the leg is treated as
  dependent, so the deliverable inherits CONTINUING and may not be
  reported VERIFIED. After enumeration, a genuinely non-dependent leg
  proceeds unblocked.
- Expected result: report = deliverable CONTINUING (not VERIFIED)
  before enumeration; the shortener-hop embed is found by the
  enumeration, so it stays CONTINUING after enumeration too.
- Protections: A-156 side — honest per-leg progress, a continuing leg
  does not silently hold unrelated deliverable legs hostage (kept:
  non-blocking applies after enumeration). A-164 side — no
  self-serving dependency claims (kept: self-assessment is not
  evidence; unknown = dependent). Neither dropped.

## RC-2 — R-051 (A-156 vs A-213): capped deferral, in the same sentence

- Setup: a continuing leg's destination is public, so the
  at-most-24-hour re-observation interval applies — but no authorised
  audience-identical vantage exists (the only candidate is the
  owner's phone, never authorised for this leg).
- Old-rule outcome: deadlock with no exit — A-156 demands
  re-observation at most every 24 h; A-213's deferral has no limit
  stated in the atom, so the leg can sit "deferred" forever while
  formally breaching the interval duty every day.
- New-rule outcome (CURRENT-STATE §5 + §7): the leg is reported
  UNVERIFIED with the blocker named and re-observation is deferred;
  deferral is capped at 3 re-observation cycles or 7 days, whichever
  first; beyond the cap the leg escalates to the owner and blocks
  promotion/continuation that depends on it. The owner's phone is
  never used without authorisation recorded through the owner's own
  channel.
- Expected result: days 1–7: UNVERIFIED-deferred, blocker named. Day
  8 (or after cycle 3): escalated to the owner; dependent promotion
  blocked. No silent use of the owner's device at any point.
- Protections: A-156 side — the interval duty keeps pressure on a
  public mutable destination (kept as the cap's clock). A-213 side —
  never fabricate a vantage, never silently use the owner's identity,
  IP or session (kept in full). A-219 side — deferral cannot become a
  permanent pass (kept: the cap). None dropped.

## RC-3 — R-076 (A-191 vs A-213): per-segment accounting for verified-live

- Setup: a leg's audience spans anonymous and logged-in viewers in
  two geographies. Authorised audience-identical vantages exist for
  anonymous US viewers only; no authorised vantage exists for the
  logged-in segment.
- Old-rule outcome: A-191 requires coverage of every segment the
  audience spans and leaves the leg unverified for untested segments;
  A-213 forbids using unauthorised vantages but no rule says how to
  handle the untestable segment — the reporter must either over-claim,
  silently drop the segment from the report, or stall.
- New-rule outcome (CURRENT-STATE §6): the report lists every required
  segment with a status — anonymous US: covered (vantage-scoped
  "verified live for anonymous US viewers"); logged-in: unverified
  (or scoped out by the owner, and then named as scoped-out in the
  report, never omitted and never reported as verified).
- Expected result: no unscoped "verified live" claim; the unverified
  segment is visible in the report by name.
- Protections: A-191 side — no over-claiming across the audience's
  actual spread (kept: unscoped label on one fetch is an over-claim).
  A-213 side — only authorised vantages are ever used (kept).
  Guard against a new hole: owner scoping-out narrows the CLAIM, it
  does not pass the leg; a segment omitted from the list entirely
  fails this case. None dropped.

## RC-4 — R-077 (A-145 vs A-156): closure wording means what it says

- Setup: a mutable self-created destination (a public preview bucket)
  is taken down by making it private. A reader applying A-145's
  closure clause literally — "de-privatised/destroyed" — reads the
  closure condition as the destination being made PUBLIC, the exact
  opposite of the intended event; the same chain calls the 24-hour
  maximum interval a "floor", inviting a reading of "at least every
  24 h" as a minimum-frequency guarantee rather than a maximum gap.
- Old-rule outcome: closure can be claimed on the wrong event (or
  denied on the right one), and the interval can be read as
  satisfied by re-observing less often than the cap intends.
- New-rule outcome (CURRENT-STATE §5): the leg "closes only when the
  destination is made immutable, made private or destroyed, or the
  operation itself ends", and is re-observed "at an interval of at
  most 24 hours while the destination is public".
- Expected result: making the bucket private closes the leg;
  making it public (or leaving it public) never does; a 30-hour gap
  between re-observations breaches the rule.
- Protections: wording-only fix (per Muse's C1 ruling on A-156).
  No protection dropped; the fix removes an inversion that could
  have passed an open leg as closed.
