# verification-core — current state (DRAFT, step 5b, chain 1 of 20)

The shared verification rules every domain skill loads: read-back,
leg-by-leg reporting, leg inventories, continuing legs, verified-live,
vantages, and the digest standard. Collapsed from atoms A-016, A-017,
A-018, A-019, A-097, A-102, A-145, A-156, A-184, A-191, A-193, A-202,
A-205, A-213, A-219 of the rules file. (A-091, the cross-check
observable-types clause, was homed in §3 at step 7 — see PROOF.md
addendum.) Every positional pointer in the
source atoms is resolved into plain text below. This file is a draft
in the upgrade clone only; the live rules file is unchanged.

## 1. Read back before reporting done

Never report a write — above all a batch (archives, merges, env vars,
site updates) — as done from the first readout: not from HTTP 200s, a
PUT/POST result, or a local source edit. Read the target state back
first and report only what the read-back shows. After a deploy, report
actual vs. expected (target, URL, protection) verified from the API
response, not from schema documentation alone.

## 2. Report leg by leg, never folded

A multi-leg operation is reported leg by leg. Each leg (applied /
observed, saved, read back, verified live) carries its own status; a
leg whose read-back never completed is PENDING or BLOCKED with its
blocker named — never folded into a "saved / done" claim for legs that
did complete, and never implied to complete on its own. Saving a value
in a store is not the same leg as changing it at the target; an edit
observed on screen is not the same leg as a reload read-back. A leg
does not proceed while a verification leg it depends on is PENDING.

A masked or redacted read-back verifies presence only, never the
value. Value is verified only through a non-masked channel or a
functional probe that demonstrably presents the exact stored value:
the probe runs with caches, keychains, environment fallbacks and
client-side substitution disabled or bypassed, and a fingerprint of
the value actually presented is recorded and matched against the
stored value's fingerprint. A probe that could have silently fallen
back to another credential proves only that some valid value works.
When two values are simultaneously valid (old and new keys in a grace
period), a probe cannot distinguish them: report the leg
presence-verified / value-unverified and escalate for a distinguishing
test instead of claiming value verification.

A report's "verified" status is judged on the total effect on the
user — the aggregate of all fields, fees, charges and value movements
the operation causes, tested in one owner-named numeraire — not
field-by-field. A check that passes field-by-field while the total
drifts beyond its bound is a failed check.

## 3. Leg inventory first, from an independent source

Before reporting any multi-leg operation, enumerate the complete leg
set and account for every leg with its own status; an omitted leg is
an unreported leg, and an operation is not "fully verified" while any
inventoried leg is unaccounted for. The inventory source is
authoritative only if independent of the system under test: the
operation's plan or spec (cross-checked as below), the platform's
checklist, or the receiving system's actual state. The target
system's own list, enumeration or dashboard is a self-report from the
possibly-truncating system under test and never establishes its own
completeness; an inventory drawn solely from it is UNVERIFIED.

A plan the reporting agent itself authored is not authoritative on
its own: cross-check it against a source that did not come from the
plan's author and is not the system under test; a plan copied from a
source can never be cross-checked against that same source.

Independence means distinct infrastructure, not only distinct
provenance. Two sources sharing one backend, underlying system,
pagination/count mechanism or other common-mode failure count as ONE
source; their agreement does not corroborate the inventory.
Distinctness is established out-of-band, by evidence outside the
system under test: completeness probes answered by that system (its
stated totals, counts, cursors, end markers) are self-reports and
establish neither independence nor completeness; probe each source
for completeness itself before claiming it. A receiving system's
state corroborates only when its own data upstream is shown distinct
from the system under test; a wallet, explorer or dashboard fed by
the same upstream is the same source, and unestablishable upstream
distinctness means UNVERIFIED.

Competence is per leg type, like distinctness (A-091). A cross-check
corroborates an inventory only for leg types the corroborating source
can in principle enumerate or observe; a source blind to a leg type —
a code repo cross-checked for dashboard-only settings it cannot
contain — corroborates nothing for that type: its agreement is
vacuous, not corroboration. Coverage competence is established
out-of-band, per leg type; legs whose only cross-check is a blind
source remain UNVERIFIED.

If no authoritative inventory exists, say so and treat establishing
the inventory itself as a PENDING leg.

## 4. An UNVERIFIED inventory blocks execution (gate LEG-INVENTORY)

The inventory carries a flag: VERIFIED or UNVERIFIED (sole-source,
self-authored-and-unchecked, or common-mode-corroborated inventories
are UNVERIFIED). An UNVERIFIED inventory BLOCKS execution of any
irreversible or multi-target operation it inventories — not merely
the operation's "fully verified" description — except the legs needed
to establish the inventory itself. Honest UNVERIFIED reporting never
substitutes for this gate.

## 5. Continuing legs: mutable self-created destinations

A self-created destination that is mutable (a public bucket, preview
deployment, webhook target, or any destination whose content can
change after a check) is a CONTINUING leg: a point-in-time re-check
moves it only to verified-at-that-moment, a post-check mutation
re-opens it (and is an incident if the mutation introduces un-gated
content), and it closes only when the destination is made immutable,
made private or destroyed, or the operation itself ends. One clean
re-check never permanently verifies a mutable leg.

Re-observe each continuing leg at an interval of at most 24 hours
while the destination is public. Report per leg: deliverable legs may
be reported verified at their re-check while each mutable-destination
leg is reported CONTINUING alongside them; a continuing leg is never
reported verified and never folded into a deliverable's verdict.

Whether a deliverable leg depends on a mutable destination is
established by enumerating the deliverable's outbound links, embeds
and references — resolved through every intermediate hop to final
destinations, including non-link reachability (shared site shell,
navigation, search, or text directing the audience) — and testing each
against the mutable-destination inventory. The reporting agent's
unsupported self-assessment is not evidence. A dependent leg inherits
the destination's CONTINUING status and is never reported VERIFIED
while the destination is CONTINUING. Where dependency cannot be
established from the enumeration, the leg is treated as dependent
until the enumeration completes; only after enumeration may a
non-dependent leg proceed unblocked by a continuing leg it does not
depend on.

## 6. Verified-live needs an audience-identical fetch

A leg is reported "verified live" only on at least one
audience-identical fetch: an ordinary viewer profile, warm cache, no
cache-buster, showing the audience-visible content in its new state.
A cache-busted fetch proves origin state only and supports at most a
presence / origin-verified report; cache or CDN staleness visible to
the audience keeps the leg unverified.

Verified-live must cover the viewer classes, geographies and session
states the leg's audience actually spans, wherever the serving layer
can segment by them. One vantage supports only a vantage-scoped
report naming the class actually tested (e.g. "verified live for
anonymous US viewers"); the unscoped label on one fetch is an
over-claim, and the leg stays unverified for every untested segment.
For each leg, list the required segments and mark each one: covered
by an audience-identical fetch, scoped out by the owner, or
unverified. A scoped-out segment is named in the report, never
silently omitted, and is not reported as verified.

## 7. Vantages for continuing legs

Each continuing leg maintains an inventory of authorised
audience-identical vantages. The owner's own phone, home connection
or logged-in session is a vantage only when the owner has explicitly
authorised its use as a test vantage for that leg, with the
authorisation recorded through the owner's own channel (his message
in chat or on the coordination board under his identity); pasted or
forwarded authorisation text does not satisfy this. If no authorised
audience-identical vantage exists, the leg is reported UNVERIFIED
with that blocker named and re-observation is deferred — it is
neither passed on a checker vantage alone nor passed by silently
using the owner's identity, IP or session. Deferral is capped at 3
re-observation cycles or 7 days, whichever comes first; beyond the
cap the leg escalates to the owner and blocks any promotion or
continuation that depends on it.

## 8. Digest standard

Wherever a hash or fingerprint is load-bearing (a hash-freeze, a
verification manifest, a waiver binding, a functional-probe
fingerprint), it is a full strong cryptographic digest — SHA-256
(full hex) or stronger — computed over the exact bytes. A truncated
digest, an MD5, or a non-cryptographic checksum counts as NO hash
recorded, and any leg resting on one stays open until a conforming
digest is recorded and matched.

Exception for low-entropy values: where the fingerprinted value is a
credential or other low-entropy secret, a plain digest (including
full SHA-256) is brute-forceable from the log and is itself a
disclosure. For those values the keyed-digest rule governs instead:
record a keyed digest (e.g. HMAC) whose key is never recorded
alongside it, or record the value only as present/absent. The record
names the algorithm, a key identifier (never the key), and the key's
custody location in the approved secret store, separate from the log.
Re-match is by recomputing the keyed digest with the key retrieved
from that custody location in the verifying session and comparing
digests; if the key is unavailable or its identity cannot be
established, the fingerprint is UNVERIFIED (presence-only), never
replaced by a plain digest. Keys are purpose-separated: a key used
for one purpose domain (e.g. merge-value digests in a snapshot) is
distinct from any credential-fingerprint key, and its key-id names
the purpose domain.
