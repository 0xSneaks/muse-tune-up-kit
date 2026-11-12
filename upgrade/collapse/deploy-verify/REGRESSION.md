# deploy-verify — regression cases (DRAFT)

One case per contradiction row in PAIR-MAP-RULES.md touching the
deploy atoms, excluding the four verification-core already covers
(R-047, R-051, R-076, R-077). Each case is built so the old
(pre-collapse) reading and the collapsed rule give different
outcomes; the collapsed rule must produce the expected result. Rows
whose operative fix lives in verification-core are marked with
their core section; the case still belongs to this set because a
deploy atom is one side of the contradiction. R-004 (publish lane)
is the same A-083/A-184 pair as RC-1 and is not counted twice.

## RC-1 — R-041 (A-083 vs A-184): cache-busted is origin-verified, never verified-live

- Setup: a deploy is verified by fetching the page with a unique
  query string to bypass the CDN. The fetch shows the new content.
- Old-rule outcome: A-083 accepts a cache-busted read-back as live
  verification, so the leg is reported verified live — while the
  audience's warm cache still serves the old page.
- New-rule outcome (verification-core §6): a cache-busted fetch
  proves origin state only and supports at most a
  presence/origin-verified report; verified-live needs at least one
  ordinary-viewer fetch, warm cache, no cache-buster.
- Expected result: leg = origin-verified, not verified live, until
  an audience-identical fetch shows the new state.
- Protections: A-184 side — the audience's actual experience is the
  claim (kept). The cache-busted fetch is not banned; it is demoted
  to the claim it can actually support. None dropped.

## RC-2 — R-042 (A-193 vs A-202): plain digest for artifacts, keyed for secrets

- Setup: a leg record fingerprints a stored API key with a full
  SHA-256, citing the rule that every load-bearing hash is a full
  strong digest.
- Old-rule outcome: A-193's plain reading orders exactly that;
  A-202 says recording a plain digest of a low-entropy secret fails
  the leg — the two atoms give opposite verdicts on the same record.
- New-rule outcome (verification-core §8): plain full digest for
  artifacts; for low-entropy secrets, a keyed digest whose key is
  never recorded alongside it, or present/absent only.
- Expected result: the SHA-256-of-key record FAILS the leg; a keyed
  digest with algorithm, key id and custody recorded passes.
- Protections: A-193 side — no truncated or weak digest ever counts
  (kept). A-202 side — the record itself must not become a
  brute-force oracle (kept). Neither dropped; A-205 supplies the
  precedence (RC-12's digest half).

## RC-3 — R-043 (A-017 vs A-202): the probe fingerprint is a keyed fingerprint

- Setup: a functional probe (CURRENT-STATE §3 permits it) presents a
  stored credential; the agent records "a fingerprint (e.g. a hash)"
  of the presented value, following A-017's base wording literally.
- Old-rule outcome: the base text reads as an order to record a
  plain hash of a credential — itself a disclosure under A-202.
- New-rule outcome (CURRENT-STATE §3, first paragraph;
  verification-core §2 + §8): the fingerprint is recorded in keyed
  form; the match against the stored value's fingerprint is a match
  of keyed digests.
- Expected result: a leg record containing a plain hash of a
  presented credential fails review even if the probe itself passed.
- Protections: A-017 side — the probe must demonstrably present the
  exact stored value, fingerprint matched (kept). A-202 side — no
  plain digest of a secret in any record (kept). None dropped.

## RC-4 — R-044 (A-153 vs A-162): unknown side-effects bar the probe; they do not open a leg

- Setup: a probe is permitted on consume/rotate behaviour, but what
  the rotation revokes (sibling sessions? scope changes?) cannot be
  determined beforehand.
- Old-rule outcome: A-153's wording lets the probe proceed and
  treats unknown side-effects as "an open leg, never assumed none"
  — the revocation fires during the probe and is inventoried after
  the fact.
- New-rule outcome (CURRENT-STATE §3): side-effect scope is
  determination (b) of the pre-probe duty; if it cannot be
  determined, the probe is barred and the leg is reported
  presence-verified / value-unverified with the undetermined
  element named. Known side-effects of a rotation that does proceed
  are still inventoried as legs of the operation.
- Expected result: no probe runs; the report names side-effect
  scope as the undetermined element.
- Protections: A-162 side — no irreversible revocation is
  discovered by causing it (kept; this is the stricter side and it
  wins). A-153 side — side-effects are never silently ignored
  (kept, moved before the probe and retained for known effects).
  The dropped element is only A-153's weaker sequencing for the
  unknown case. See PROOF FLAG-3.

## RC-5 — R-045 (A-142 vs A-153): "atomically" is gone; confirmed store or it did not verify

- Setup: probing rotates a refresh token. The agent stores the
  successor in the vault and reports the leg verified on the store
  call's success response, without reading the store back.
- Old-rule outcome: A-142's "capture-and-restore atomically (any
  successor value the probe issues is stored in the same leg)"
  reads as satisfied by the store attempt.
- New-rule outcome (CURRENT-STATE §3): capture-and-restore verifies
  only when the successor is stored AND the store is read back
  confirmed, inside the same leg, before the leg is reported — and
  the verified value is the successor, reported as such. A failure
  between rotation and confirmed store is an incident.
- Expected result: the report is rejected; leg = value-unverified,
  escalated, until the store read-back confirms the successor.
- Protections: A-153 side — a rotation whose successor was never
  confirmed stored leaves a dead stored value, the worst outcome in
  this chain (kept). A-142 side — capture-and-restore remains an
  allowed route when no non-consuming route exists (kept). The
  dropped word "atomically" carried no protection; it carried an
  ambiguity. See PROOF FLAG-3.

## RC-6 — R-046 (A-164 vs A-171): closure runs through intermediaries the operation did not create

- Setup: a deliverable page reaches a mutable preview through a
  third-party link shortener the operation did not create. The
  agent's dependency enumeration stops at the shortener because
  A-164's parenthetical limits closure to "anything it links to
  that the operation also created".
- Old-rule outcome: the deliverable is reported independent of the
  continuing leg; A-171 (later) requires resolution through every
  intermediary "whether or not the operation created them".
- New-rule outcome (verification-core §5): outbound references are
  resolved through every intermediate hop to final destinations,
  whoever created the hop; the deliverable inherits CONTINUING.
- Expected result: deliverable = CONTINUING until the preview leg
  closes or the reference is removed.
- Protections: A-171 side — dependency cannot be laundered through
  a third-party hop (kept). A-164 side — dependency is still proven
  by enumeration, not assumed (kept). None dropped.

## RC-7 — R-050 (A-145 vs A-145): operation end closes a continuing leg (owner ruling, 2026-11-12)

- Setup: a public preview bucket created by an operation is still
  public and mutable when the operation ends (the deliverable
  shipped, the team moved on). The final report marks the bucket's
  leg CLOSED, citing the atom's "or the operation itself ends".
- Old-rule outcome: the same atom also says the leg stays open "for
  as long as it is public" — both readings are in force, and the
  closure reading wins by being the last one the reporter reaches.
- Pre-ruling draft outcome (pair-map resolution; this case as
  originally written): closure requires the destination to be made
  immutable, made private or destroyed. Operation end alone hands
  the leg over: the report names the handover (who or what now
  owns re-observation), and the leg remains CONTINUING. Expected
  result was: report = leg CONTINUING, handed over — never CLOSED
  while the bucket is public and mutable — and verification-core
  §5, which carries the closure reading, was flagged as NOT
  passing this case (PROOF FLAG-1).
- Owner ruling (2026-11-12): "When it's done it's done." Operation
  end CLOSES the leg. The pair-map hand-over resolution is
  overruled; verification-core §5 as drafted by lane B2 (closure on
  immutability, privacy, destruction, or operation end) stands
  unchanged and now passes this case.
- Expected result: report = leg CLOSED at operation end, even
  while the bucket remains public and mutable. The re-observation
  duty ends with the operation; a destination that must stay
  watched beyond the operation has to be carried into a new
  operation, or closed by immutability, privacy or destruction
  before this one ends.
- Protections: the at-most-24-hour re-observation duty and the
  per-leg CONTINUING reporting govern for the whole life of the
  operation (kept). The risk the hand-over resolution guarded
  against — a public mutable destination outliving its watcher —
  is, by the owner's ruling, accepted at operation end rather than
  carried as a perpetual duty; that acceptance is recorded here,
  not silently absorbed. See PROOF FLAG-1 (RESOLVED-BY-OWNER).

## RC-8 — R-052 (A-144 vs A-019): one named, scoped exception to the self-report bar

- Setup: a parser-set re-verification. The platform's own dashboard
  lists the current parsers; the agent also fetches the parsings
  actually served by the live previewers.
- Old-rule outcome: A-019's general rule says a system's own
  answers never establish corroboration; A-144's exception admits
  observed served parsings as corroboration for this leg only. A
  reader of the general rule alone rejects the corroboration; a
  reader of the exception alone might extend it to other
  inventories.
- New-rule outcome (CURRENT-STATE §5, exception note; exception
  itself homed in media-verify): self-report is input, never
  corroboration; corroboration is observed behaviour — the parsings
  actually served, fetched audience-identically. The exception is
  scoped to parser-set listing; every other inventory keeps the
  full bar. Where only self-report exists, the parser inventory is
  UNVERIFIED and the leg stays open.
- Expected result: the re-verification discharges on the observed
  parsings; a second inventory in the same operation (say, the
  artifact's publication history) may NOT borrow the exception.
- Protections: A-019 side — no general weakening of the
  distinctness bar (kept; the exception is named and fenced).
  A-144 side — a leg that can only be evidenced by observed
  behaviour is not left impossible (kept). None dropped. Noted gap:
  R-052 also requires verification-core §3 itself to mention the
  exception; §3 as drafted does not. See PROOF FLAG-6.

## RC-9 — R-053 (A-017 vs A-097): an UNVERIFIED inventory is an execution block, not a reporting style

- Setup: a multi-target operation's leg inventory can only be
  drawn from the target system's own dashboard. The agent writes
  an honest report: inventory UNVERIFIED, establishing it treated
  as a PENDING leg — and proceeds with the irreversible send
  anyway, citing A-017's base sentence.
- Old-rule outcome: the base text treats a missing inventory as a
  reporting matter; A-097 makes it an execution block. Both remain
  in the file, so the weaker reading is loadable alone.
- New-rule outcome (verification-core §3 + §4): the inventory
  carries the UNVERIFIED flag, and the flag BLOCKS execution of any
  irreversible or multi-target operation it inventories — except
  the legs needed to establish the inventory itself. Honest
  reporting never substitutes for the gate.
- Expected result: the send does not proceed; the report shows the
  block and the inventory-establishing legs as the only work done.
- Protections: A-097 side — the gate (kept, and folded into the
  same rule as the inventory duty so it cannot be loaded without
  it). A-017 side — the PENDING-leg honesty duty for the inventory
  itself (kept). None dropped.

## RC-10 — R-054 (A-212 vs A-220): the deletion clock runs from staging too

- Setup: a personalised send is staged with a working plaintext
  snapshot, then abandoned before sending. Thirty-five days later
  the snapshot is still in the execution store; the agent cites
  A-212's "deleted within 30 days after the send" — there was no
  send, so on that reading no deadline ever started.
- Old-rule outcome: A-212 alone leaves never-sent snapshots
  immortal; A-220 (filed in another domain) starts the clock at
  staging, but an agent loading only the deploy atom never sees it.
- New-rule outcome (CURRENT-STATE §4): the 30-day deadline runs
  from staging for never-sent snapshots and from the send for sent
  ones; deletion is verified by an independent read-back.
- Expected result: the day-35 snapshot is a failed leg; deletion
  plus a second session's store listing showing absence closes it.
- Protections: A-220 side — staged personal data has the same
  lifetime cap as sent (kept). A-212 side — the durable record
  never holds plaintext (kept). None dropped.

## RC-11 — R-062 (A-109 vs A-017): pointers to "the inventory rules" resolve to verification-core

- Setup: three different domain rules — a publication-history
  listing, a parser-set enumeration, a broadcaster/worker set —
  each declare themselves "a leg inventory under the Deployments
  inventory rules" and load no deploy text.
- Old-rule outcome: if the inventory, distinctness and gate rules
  live inside a deploy-verify skill that a publish or send task
  never loads, every one of those pointers dangles and each domain
  improvises its own bar.
- New-rule outcome (CURRENT-STATE §5): the inventory rules,
  distinctness standard and the UNVERIFIED execution gate live in
  verification-core, which every domain skill loads; the pointers
  resolve to core §3 and §4.
- Expected result: all three inventories are judged by the same
  bar; a sole platform listing is UNVERIFIED and blocks in each
  domain, not just in deploy.
- Protections: one bar, everywhere (kept). No domain loses its own
  additional conditions — A-109's blocking effect, for instance,
  rides on the core flag. None dropped.

## RC-12 — R-063 (A-212 vs A-205): snapshot digests use the purpose-separated keyed rule

- Setup: the merge-value snapshot record is written with plain
  SHA-256 digests per recipient, on the argument that §4 says
  "keyed digest" but the digest standard lives in another section
  of the file that this task did not load.
- Old-rule outcome: A-212 depends on "the keyed-digest bullet"
  (A-205, filed under deploy but amendable from three domains);
  without it in scope, a plain digest looks compliant — and is
  brute-forceable from the log for low-entropy merge values.
- New-rule outcome (CURRENT-STATE §4 + verification-core §8): the
  record uses a keyed digest under a purpose-separated key whose
  key-id names the purpose domain, distinct from any
  credential-fingerprint key; if the key is unavailable the record
  is presence-only, never a plain-digest fallback.
- Expected result: plain-digest snapshot records fail the leg even
  though every recipient is listed.
- Protections: A-205 side — keyed precedence and no plain fallback
  (kept). A-212 side — per-recipient accountability in the durable
  record (kept). None dropped.

## RC-13 — R-078 (A-138 vs A-178): the async window has a maximum; later legs are new legs

- Setup: an operation is reported complete. Its provisional
  re-check window was stated as "eventually". Eight days later an
  asynchronously-provisioned webhook from the operation appears;
  the agent re-opens the closed completion claim to account for it.
- Old-rule outcome: A-138 states a window with no maximum, so
  "eventually" satisfies it and the claim was never really final;
  A-178 says the late leg is unaccounted "from the moment it
  exists", which reads as retroactively falsifying the claim. No
  rule says when finality arrives.
- New-rule outcome (CURRENT-STATE §2): the window is stated in the
  leg record before the provisional claim and is at most 24 hours.
  A leg existing during the window but missed is a closure
  failure — the claim is corrected. A leg coming into existence
  after the window closes opens a NEW leg (an incident if it
  carries un-gated content); it does not reopen the final claim.
- Expected result: "eventually" is rejected at claim time; the
  day-8 webhook is opened as a new leg/incident; the final claim
  stands, with the new leg reported alongside it.
- Protections: A-178 side — late legs are never silently absorbed
  (kept; within the window they block and falsify). A-138 side —
  completion can actually become final, so reports mean something
  (kept, by giving the window a maximum). The 24-hour maximum is a
  parameter this collapse introduces, anchored to the bundle's own
  async re-check bound; it tightens, it does not drop. See PROOF FLAG-4.

## RC-14 — R-079 (A-177 vs A-182): no deploy-side bound exists; the chain is homed in onchain-send

- Setup: a deploy report is challenged: "the total effect drifted
  beyond its bound." The reporter searches the deploy rules for
  the deviation bound that was supposedly breached.
- Old-rule outcome: A-177/A-182 carry a DEPLOY tag, so the chain
  appears to be deploy law — but no deploy atom defines a
  deviation or materiality bound, a numeraire for deploys, or a
  blocking consequence; every operative clause is about sends.
- New-rule outcome (CURRENT-STATE §6): the total-effect-bounds
  chain (A-177, A-182, A-189, A-197, A-206) is homed in
  onchain-send and the deploy tag is dropped. Deploy-verify
  carries only the one total-effect sentence that verification-
  core §2 states for leg reports generally.
- Expected result: no deploy rule purports to define a send bound;
  a bound challenge on a send is judged in onchain-send, and a
  deploy report's "verified" status is judged on its legs.
- Protections: none dropped — this is a homing correction. The
  risk it removes is a phantom deploy bound being cited as
  satisfied (or breached) when no such test exists.

## RC-15 — R-080 (A-212 vs A-087): the gate reads the ephemeral copy; the record holds digests

- Setup: to satisfy "snapshot the actual merge values", an agent
  writes the plaintext merge values into the durable leg record —
  the only copy of the snapshot it keeps.
- Old-rule outcome: A-087 (in the publish gate) orders a snapshot
  of actual values; A-212 (under deploy) fails any durable record
  holding plaintext. Loaded separately, each atom makes the other
  look violated.
- New-rule outcome (CURRENT-STATE §4): two copies, two rules — the
  gate runs on the ephemeral working snapshot in the approved or
  ephemeral store; the durable record holds only keyed digests or
  presence markers. The retention half of the merged rule lives in
  §4; the send-time gate itself is pre-publish's A-087.
- Expected result: a durable record containing plaintext merge
  values fails the leg even if the send gated correctly.
- Protections: A-087 side — the gate sees real values, not digests
  of them (kept). A-212 side — no durable plaintext aggregate of
  recipients' personal fields (kept). None dropped. Homing note in PROOF FLAG-5.

## RC-16 — R-096 (A-102 vs A-019): the corroborator's own upstream is part of the same rule

- Setup: an inventory drawn from a platform's API is
  "corroborated" by the platform's official explorer, presented as
  the receiving system's actual state.
- Old-rule outcome: A-102 and A-019 state the same requirement in
  two places (the corroborator counts only if shown not to share
  the system under test's backend/upstream); a collapse that keeps
  only one wording risks losing the wallet/explorer same-upstream
  example that makes the rule bite.
- New-rule outcome (verification-core §3): one clause — a
  receiving system's state corroborates only when its own data
  upstream is shown distinct; a wallet, explorer or dashboard fed
  by the same upstream is the same source; unestablishable
  upstream distinctness means UNVERIFIED.
- Expected result: the explorer corroboration is rejected; the
  inventory is UNVERIFIED until an out-of-band source appears.
- Protections: both atoms' content survives in the single clause,
  example included. None dropped — this row was a duplication,
  and the merge is the resolution B2 already applied in §3.

## RC-17 — R-098 (A-129 vs A-178): one completion rule — re-draw, include late legs, stay provisional

- Setup: at completion, an agent re-enumerates the inventory from
  the original plan (A-129) but omits a DNS record the operation
  created mid-flight, arguing A-178 is a different domain's
  amendment that its checklist did not load.
- Old-rule outcome: the two atoms state the same completion duty
  in two places with different emphases; a partial load satisfies
  one and silently misses the other.
- New-rule outcome (CURRENT-STATE §2): one rule — the inventory is
  re-drawn at completion, self-created and late-provisioned legs
  are included and accounted for, and the claim is provisional
  until the async re-check (RC-13).
- Expected result: the completion report is rejected until the DNS
  leg is inventoried and verified or carried as unaccounted (which
  blocks the verified claim).
- Protections: A-129 side — completion is a fresh enumeration, not
  a rubber stamp of the plan (kept). A-178 side — immutability
  does not exempt a late leg (kept). None dropped.

## RC-18 — R-099 (A-152 vs A-162): the fail-closed atom is deleted because the two-part rule subsumes it

- Setup: a reviewer diffs the collapsed §3 against the atom list
  and finds A-152 missing as a standalone rule: "if consume
  behaviour cannot be determined, treat as consumable, do not
  probe."
- Old-rule outcome: A-152 is clause (a) of A-162's two-part
  determination, stated earlier and separately, with the same
  reported status. Keeping both invites a future edit to one that
  silently diverges from the other.
- New-rule outcome (CURRENT-STATE §3): one determination duty —
  (a) consume/rotate/invalidate AND (b) side-effect scope; if
  EITHER cannot be determined, the probe is barred and the leg is
  presence-verified / value-unverified with the undetermined
  element named. A-152's content is clause (a)'s consequence,
  stated verbatim in the consolidated text.
- Expected result: an undeterminable consume behaviour bars the
  probe under §3 exactly as A-152 required; nothing that A-152
  forbade is permitted.
- Protections: none dropped — DROPPED-ATOM, content preserved.
  This is the one atom deletion in this chain, and it follows the
  registry's own verdict (DELETE, survivor A-162). See PROOF
  FLAG-2.

## RC-19 — R-100 (A-145 vs A-073): "continuing leg" is defined once, in core

- Setup: a mutable link inside a published artifact and a mutable
  preview bucket from a deploy are both re-checked clean once. The
  publish-side rule (A-073) calls the clean re-check "monitoring
  evidence, not closure" under one closure list; the deploy-side
  atom (A-145) defines its own, different closure list.
- Old-rule outcome: two definitions of the same status with
  different closure conditions — a leg can be closed under one
  domain's list while open under the other's.
- New-rule outcome (verification-core §5): "continuing leg" is
  defined once, in core; each domain adds only its own closure
  conditions on top. A clean point-in-time re-check never
  permanently verifies a mutable leg in either domain.
- Expected result: both legs report CONTINUING after the single
  clean re-check; neither report claims closure from it.
- Protections: A-145 side — the deploy closure conditions (subject
  to RC-7's correction) (kept). A-073 side — publish's closure
  conditions and the monitoring-evidence wording (kept, in
  pre-publish on top of the core definition). None dropped.
