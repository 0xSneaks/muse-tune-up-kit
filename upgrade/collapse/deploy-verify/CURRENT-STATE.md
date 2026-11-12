# deploy-verify — current state (DRAFT, step 5b, deploy chains)

The deploy-specific rules: what must be checked before and after a
deploy, when a completion claim becomes final, when a stored
credential may be probed, and how personalised-send snapshots are
recorded and destroyed. Collapsed from atoms A-014, A-129, A-138,
A-142, A-153, A-162, A-169, A-178, A-212, A-220 of the rules file
(A-152 is subsumed into §3, not carried as an atom). The shared
verification rules this skill depends on — read-back, leg-by-leg
reporting, inventories, continuing legs, verified-live, vantages,
digests — are NOT restated here; they live in verification-core and
are cross-referenced in §5. Every positional pointer in the source
atoms is resolved into plain text below. This file is a draft in the
upgrade clone only; the live rules file is unchanged.

## 1. Before and after a deploy

Before any deploy, check whether the platform can override the
requested target — for example, a platform may promote the first
deployment of a new project to production even when the target is
omitted, despite its schema saying an omitted target means preview.
State that risk explicitly in the approval request, before the flow
starts. After deploying, report actual vs. expected (target, URL,
protection) verified from the platform's API response, never from
schema documentation alone (verification-core §1).

## 2. Completion: re-draw the inventory; provisional until the async re-check

The leg inventory is re-enumerated AT COMPLETION, including the legs
the operation itself created (auto-created previews, buckets,
deployments, DNS records, webhooks). Pre-execution completeness does
not cover execution-created legs: an operation is never reported
verified while any self-created leg is unaccounted or unverified.

The inventory is re-drawn at completion from the operation's plan or
spec cross-checked against an independent source (verification-core
§3). A self-created leg provisioned after the inventory was drawn —
including an immutable one — is an unaccounted leg from the moment
it exists: the operation is not fully verified, and no leg depending
on it is verified, until that leg is added to the inventory and
itself verified. Immutability does not exempt a late leg from the
inventory; it only changes how the leg is verified once inventoried.

Completion stays PROVISIONAL until a delayed re-check at a stated
window covers the asynchronously-provisioned self-created legs.
Until that re-check passes, the operation is reported PROVISIONAL,
never verified. The window is stated in the leg record before the
provisional claim is made, and is at most 24 hours (the bundle's own
outer bound for asynchronous re-checks). If no window was stated,
the claim never becomes final. A leg that comes into existence
after the window has closed opens a new leg — an incident if it
carries un-gated content — and does not reopen the final claim; a
leg that existed during the window but was missed is a closure
failure, and the final claim is corrected, not merely supplemented.
Self-created legs that are mutable destinations are continuing legs
(verification-core §5); the re-check moves them only to
verified-at-that-moment.

## 3. Probing a stored credential

The probe itself — presenting the exact stored value with caches,
keychains, environment fallbacks and client-side substitution
disabled, and matching a fingerprint of what was presented — is
verification-core §2. The fingerprint is recorded in the keyed form
verification-core §8 requires for low-entropy values, never as a
plain digest. This section governs whether a probe may run at all.

Before probing a stored credential, determine whether presenting it
consumes, rotates, or invalidates it (rotating refresh tokens,
one-time codes, and similar consumables), AND the rotation's
side-effect scope — which sibling sessions or tokens it revokes and
any scope or expiry changes. Both determinations come from the
provider's documentation or observed properties, and count only if
they apply to THIS stored credential's account — its tier or plan,
auth configuration, and API version — with the source, version, and
date recorded in the leg. Documentation for a different tier, plan,
or configuration, stale documentation, or properties observed on a
different account or test tenant determine nothing for this account.
Conflicting documentation, or documentation whose applicability
cannot be established, is undeterminable.

If EITHER determination cannot be made, the probe is barred: no
functional probe is run against the stored value, and the leg is
reported presence-verified / value-unverified with the undetermined
element named. Inventorying side-effects only during or after a
probe does not satisfy this duty; an irreversible revocation that
has already fired is an incident, not an inventory.

If presenting the value consumes or rotates it, probe ONLY through
a non-consuming validation route where one exists. Otherwise either
capture-and-restore under the confirmed-store protocol, or do not
probe and report the leg presence-verified / value-unverified with
the destructive-probe risk named. Capture-and-restore verifies only
when the successor value the probe issues is stored AND the store
is read back confirmed, all inside the same leg, before the leg is
reported; the verified value is then the successor, and the report
says so. A failure between rotation and confirmed store is an
incident: the leg is value-unverified and escalates immediately,
because the stored value may be dead. A probe that destroys or
rotates the value it presents, without the successor captured under
this protocol, does NOT verify the stored value going forward,
however exactly its fingerprint matched at presentation. The known
side-effects of a rotation that does proceed are inventoried as
legs of the same operation.

## 4. Merge-value snapshots: record digests, destroy the working copy

The send-time gate runs on a snapshot of the actual merge values
(pre-publish; the gate reads the ephemeral working copy, not the
durable record). The durable leg record holds, per recipient, only
a keyed digest or a present/absent marker of the merge values —
never the plaintext values. A durable plaintext aggregate of
recipients' personal fields fails the leg. The keyed digest uses a
purpose-separated key whose key-id names the purpose domain,
distinct from any credential-fingerprint key (digest mechanics:
verification-core §8).

Any working plaintext snapshot needed to execute the send lives
only in the approved secret store or an ephemeral execution store,
access-limited to the executing session. It is deleted within 30
days — the deadline runs from the send for sent snapshots and from
staging for never-sent ones — and deletion is verified by an
independent read-back: a second session's store listing showing the
snapshot's absence, not the deleter's report alone. The deletion is
recorded.

## 5. Carried by verification-core (cross-reference, not restated)

| Topic | Atoms | Lives in |
|---|---|---|
| Read-back before "done"; batch/write reporting; deploy actual-vs-expected | A-016, A-015 | verification-core §1 |
| Leg-by-leg reporting; masked read-back; functional-probe standard | A-017 | verification-core §2 |
| Leg inventory from an independent source; independence as distinct infrastructure; distinctness established out-of-band; the corroborator's own upstream | A-017, A-018, A-019, A-102 | verification-core §3 |
| The UNVERIFIED inventory flag and its execution block (D8) | A-097 | verification-core §4 |
| Continuing legs: mutable self-created destinations; the at-most-24-hour re-observation interval; per-leg reporting; dependency established by enumeration through every hop, including non-link reachability; unknown means dependent | A-145, A-156, A-164, A-171 | verification-core §5 — with one contested sentence: §5 as drafted also closes a continuing leg when "the operation itself ends". The pair map (R-050) resolves the other way: operation end alone HANDS THE LEG OVER, it does not close it. Deploy-verify follows R-050 — a handover is reported as a handover — until verification-core is corrected. See PROOF FLAG-1. |
| Verified-live: audience-identical fetch; cache-busted proves origin only; coverage across the audience's segments | A-184, A-191 | verification-core §6 |
| Vantage inventory and fallback for continuing legs; deferral capped at 3 cycles or 7 days; authorisation only through the owner's own channel | A-213, A-219 | verification-core §7 |
| Digest standard: full strong digest for artifacts; keyed digest or presence-only for low-entropy secrets | A-193, A-202, A-205 | verification-core §8 |
| Total effect on the user, one sentence | A-177 | verification-core §2 |

One named exception to verification-core §3 exists, and §3 as
drafted does not mention it: for parser-set listing only, a
platform's self-report is admissible as input and corroboration is
the parsings actually served (A-144, homed in media-verify). The
exception is scoped to that one leg; every other inventory keeps
the full out-of-band bar (R-052).

## 6. Carried by other domain skills (cross-reference)

| Topic | Atoms | Home |
|---|---|---|
| Waivers: grant and provenance; binds to the bytes as shipped; the shipped variant set; derivation verified by reproduction; interaction-variant legs close post-publish | A-070, A-146, A-185, A-196, A-210, A-215, A-218 | pre-publish |
| The send-time merge-value snapshot gate itself | A-087 | pre-publish (§4 above carries only the record/retention half, A-212 + A-220) |
| Verified-live as filed in the publish gate; audience-identical link checks; the anonymous first-visit vantage | A-083, A-130, A-139 | pre-publish (substance also in verification-core §6) |
| Publication-history inventories | A-109, A-119 | pre-publish, on verification-core §3 |
| Live-gate variants for live or unbounded artifacts | A-148, A-159 | pre-publish |
| Deviation and materiality bounds: total effect, single numeraire, price integrity, send-time value | A-177, A-182, A-189, A-197, A-206 | onchain-send — the deploy tag on these atoms is dropped (R-079): no deploy rule defines a deviation or materiality bound, and every operative clause in the chain is about sends |
