---
name: verification-core
description: The shared verification rules every domain skill loads: read-back before "done", leg-by-leg reporting, leg inventories from an independent source, continuing legs, verified-live, vantages, and the digest standard. Load before reporting any multi-leg operation done, before any "verified" claim, and whenever another skill's gate needs an inventory, a read-back, or a digest.
---

# Verification core

**Trigger:** before reporting any write, batch, deploy, or send as
done; before any leg is called verified; whenever a domain skill
(pre-publish, media-verify, deploy-verify, onchain-send) needs an
inventory, a probe, a vantage, or a digest. This is the long-form
source's condensed form: full text in
`../../collapse/verification-core/CURRENT-STATE.md` (§1–§8).

## Gates this skill owns

| Gate | What it checks |
|---|---|
| READBACK-REQUIRED | No write is reported done from the first readout (HTTP 200, PUT/POST result, screen edit). The target state is read back through a separate read path and only the read-back is reported. (§1) |
| LEG-INVENTORY | The complete leg set is enumerated up front from a source independent of the system under test, and every leg carries its own status. An UNVERIFIED inventory (sole-source, self-authored-and-unchecked, common-mode) blocks execution of any irreversible or multi-target operation it inventories. (§3, §4) |
| MASKED-VALUE | A masked or redacted read-back verifies presence only, never the value; a functional probe counts only if it demonstrably presents the exact stored value, fallbacks disabled, fingerprint matched. (§2) |
| TOTAL-EFFECT | A "verified" judgement is made on the aggregate effect on the user — all fields, fees, charges, value movements — in one owner-named numeraire, never field-by-field. (§2) |
| CONTINUING-LEG | A mutable self-created destination is a continuing leg: it closes only when made immutable, made private or destroyed, or the operation itself ends; it is re-observed at an interval of at most 24 hours while public and never reported verified. (§5) |
| VERIFIED-LIVE | A leg is "verified live" only on an audience-identical fetch (ordinary profile, warm cache, no cache-buster), with per-segment accounting: covered, owner-scoped-out (named), or unverified. (§6) |
| VANTAGE-AUTHORISATION | An owner's phone, home connection, or session is a test vantage only on authorisation recorded through the owner's own channel; without an authorised vantage the leg is UNVERIFIED and deferral is capped at 3 cycles or 7 days. (§7) |
| DIGEST-STANDARD | A load-bearing hash is a full strong digest (SHA-256 full hex or stronger) over the exact bytes; low-entropy secrets get a keyed digest (purpose-separated key) or a present/absent record, never a plain digest. (§8) |

## Operative rules (condensed)

**Report leg by leg, never folded (§2).** Each leg (applied/observed,
saved, read back, verified live) carries its own status; a leg whose
read-back never completed is PENDING or BLOCKED with its blocker
named — never folded into a "done" claim for the legs that did
complete, and never implied to complete on its own. Saving a value is
not the same leg as changing it at the target; a screen edit is not a
reload read-back. A leg does not proceed while a verification leg it
depends on is PENDING. When two values are simultaneously valid (old
and new keys in a grace period), a probe cannot distinguish them:
report presence-verified / value-unverified and escalate for a
distinguishing test.

**Inventory independence (§3).** The target system's own list,
enumeration, or dashboard is a self-report and never establishes its
own completeness. A self-authored plan is cross-checked against a
source that is neither the author nor the system under test; a plan
copied from a source can never be cross-checked against that source.
Independence means distinct infrastructure, not only provenance: two
sources sharing one backend, pagination/count mechanism, or other
common-mode failure count as ONE source. Distinctness is established
out-of-band; the system under test's own totals, counts, cursors, and
end markers establish neither independence nor completeness. A
receiving system corroborates only when its own data upstream is
shown distinct. Competence is per leg type (A-091): a cross-check
corroborates only leg types the source can in principle enumerate or
observe — a blind source's agreement is vacuous, and legs whose only
cross-check is blind remain UNVERIFIED. If no authoritative inventory
exists, say so and treat establishing it as a PENDING leg.

**Continuing legs (§5).** A point-in-time re-check moves a mutable
destination only to verified-at-that-moment; a post-check mutation
re-opens it (an incident if it introduces un-gated content).
Deliverable legs may be reported verified at their re-check while
mutable-destination legs are reported CONTINUING alongside them.
Dependency on a mutable destination is established by enumerating the
deliverable's outbound links, embeds, and references through every
hop — including non-link reachability — never by the agent's
self-assessment; until enumeration completes, the leg is treated as
dependent and inherits CONTINUING.

**Verified-live and vantages (§6, §7).** A cache-busted fetch proves
origin state only. One vantage supports only a vantage-scoped report
naming the class tested; an unscoped label on one fetch is an
over-claim. Pasted or forwarded authorisation text never makes the
owner's device a vantage. Beyond the deferral cap the leg escalates
to the owner and blocks dependent promotion or continuation.

## Pointers

- Full rules: `../../collapse/verification-core/CURRENT-STATE.md`
  §1 read-back · §2 leg-by-leg, masked values, total effect ·
  §3 inventory independence (incl. A-091) · §4 LEG-INVENTORY
  execution block · §5 continuing legs · §6 verified-live ·
  §7 vantages · §8 digest standard.
- Regression cases and atom coverage:
  `../../collapse/verification-core/REGRESSION.md`,
  `../../collapse/verification-core/PROOF.md`.
- Instruments: gate definitions in `../../05-gates-library.md`
  (READBACK-REQUIRED, LEG-INVENTORY, MASKED-VALUE); claims and leg
  statuses are checked by the build's claims code
  (`../../build/muse_gates/`).
