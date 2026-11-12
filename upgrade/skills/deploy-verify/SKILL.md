---
name: deploy-verify
description: Deploy-specific verification: platform-override checks before a deploy, actual-vs-expected after it, the completion inventory re-draw with its provisional window, when a stored credential may be probed, and how personalised-send snapshots are recorded and destroyed. Load before any deploy, release, or push-live, and before probing a stored credential or staging a personalised send. Loads with verification-core.
---

# Deploy verify

**Trigger:** before any deploy, release, merge-to-live, or site
update; at the completion of any multi-leg operation that created
resources; before functionally probing a stored credential; when a
personalised send's snapshot is staged, sent, or destroyed. Full
text: `../../collapse/deploy-verify/CURRENT-STATE.md` (§1–§6).
The shared rules (read-back, inventories, continuing legs,
verified-live, vantages, digests) live in `verification-core` and
are cross-referenced there, never restated.

## Gates this skill owns

| Gate | What it checks |
|---|---|
| DEPLOY-TARGET | Before the deploy: whether the platform can override the requested target (e.g. promoting a first deployment to production despite the schema), stated in the approval request. After: actual vs. expected (target, URL, protection) verified from the platform's API response, never from schema docs. (§1) |
| COMPLETION-REDRAW | At completion the leg inventory is re-enumerated, including legs the operation itself created. Completion stays PROVISIONAL until a delayed re-check inside a stated window of at most 24 hours covers the asynchronously-provisioned legs; no stated window, no final claim. (§2) |
| CREDENTIAL-PROBE | A stored credential may be probed only after two determinations for THIS account (tier, plan, auth config, API version): whether presenting it consumes/rotates/invalidates it, and the rotation's side-effect scope. Either undeterminable → no probe; the leg is presence-verified / value-unverified. (§3) |
| SNAPSHOT-RETENTION | A personalised send's durable record holds only a keyed digest or present/absent marker per recipient — never plaintext. Working plaintext lives only in the approved secret store or an ephemeral execution store and is deleted within 30 days of send (or of staging, if never sent), deletion verified by an independent read-back. (§4) |

## Operative rules (condensed)

**Completion (§2).** Pre-execution completeness does not cover
execution-created legs (auto-created previews, buckets, deployments,
DNS records, webhooks): an operation is never reported verified
while any self-created leg is unaccounted or unverified, and
immutability does not exempt a late leg from the inventory. The
re-drawn inventory is the plan cross-checked against an independent
source (verification-core §3). Until the async re-check passes, the
operation is reported PROVISIONAL, never verified. A leg appearing
after the window closed opens a new leg — an incident if it carries
un-gated content — and does not reopen the final claim; a leg that
existed during the window but was missed is a closure failure and
the final claim is corrected, not merely supplemented. Mutable
self-created legs are continuing legs (verification-core §5).

**Probing (§3).** The probe standard itself — exact stored value,
fallbacks disabled, fingerprint matched — is verification-core §2;
the fingerprint is recorded keyed (verification-core §8), never as a
plain digest. Documentation for a different tier, plan, or
configuration, stale documentation, or properties observed on a
different account determine nothing for this account; conflicting or
inapplicable documentation is undeterminable, and inventorying
side-effects only during or after a probe does not satisfy the duty.
If presenting the value consumes or rotates it, probe only through
a non-consuming validation route where one exists; otherwise
capture-and-restore under the confirmed-store protocol (successor
stored AND store read back confirmed, inside the same leg — the
verified value is then the successor, and the report says so) or do
not probe. A failure between rotation and confirmed store is an
incident: the leg is value-unverified and escalates immediately. A
probe that destroys or rotates the value without the successor
captured does not verify the stored value going forward, however
exactly its fingerprint matched. The known side-effects of a
rotation that proceeds are inventoried as legs of the same
operation.

**Snapshots (§4).** The send-time gate runs on the snapshot of
actual merge values (pre-publish §11; the gate reads the ephemeral
working copy, not the durable record). A durable plaintext aggregate
of recipients' personal fields fails the leg. The keyed digest uses
a purpose-separated key whose key-id names the purpose domain,
distinct from any credential-fingerprint key. The 30-day deletion
deadline runs from staging for never-sent snapshots as well as from
send; deletion is verified by a second session's store listing
showing absence, not the deleter's report alone, and is recorded.

## Pointers

- Full rules: `../../collapse/deploy-verify/CURRENT-STATE.md`
  §1 deploy target · §2 completion and provisional closure ·
  §3 credential probe · §4 snapshot record and retention ·
  §5 carried by verification-core (incl. the R-050 owner ruling:
  a continuing leg closes when the operation itself ends) ·
  §6 carried by other skills.
- Regression cases and atom coverage:
  `../../collapse/deploy-verify/REGRESSION.md`,
  `../../collapse/deploy-verify/PROOF.md`.
- Relied on, not restated: `verification-core` §1–§8 (in
  particular §2 probe standard, §3 inventory, §5 continuing legs,
  §8 digest standard); `pre-publish` §10 (waivers), §11
  (personalised snapshot gate); `media-verify` §10 (the one named
  exception to verification-core §3: parser-set enumeration).
