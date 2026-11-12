# Standing-orders extraction — DRY RUN (step 11c)

SPEC-DELTA D17: standing orders leave LIVE. Each becomes a ledger record
with the new `standing-order` predicate class (`build/memory_os/ledger.py`)
and renders into the rules layer — kernel if it binds a gate, else the
matching skill — with the owner's quote and date as provenance (PAIR-MAP
P-C5). **Nothing was extracted. This is the plan and the arithmetic.**

## Source and its limits

The muse-side pack carries counts and structure only, never content
(MUSE-SIDE-REPORT §D). D4-memory-counts.md counts the live MEMORY.md
bullets; ATOM-REGISTRY §4 gives section byte sizes. So this dry run can
enumerate the orders as ids with source pointers, and project bytes, but
cannot name per-order destinations: whether an order binds a gate is a
property of its text, which is not in the pack. Per-order destination
resolution happens at backfill (spec 02 §2.6 step 3), on Muse's machine,
from the live file. The fixture in `build/memory_os/fixtures.py` is
generated from the D4 counts and unit-tested against them
(`tests/test_memory_os.py`): every fixture order renders exactly once,
and LIVE keeps none of them.

Destinations by section, per the registry §4 verdicts:

- **M-3 "Standing orders"** → rules layer: kernel (gate-binding) or the
  matching skill (MODULE/KERNEL verdict).
- **M-4 "Money, wallets, trading"** → split: rules to skill
  `onchain-send` and persona §12; state to the ledger.

## The orders (28 rule-like; ids are fixture ids, text stays in the live file)

M-3, 19 bullets at ~289 B each — 16 rule-like → standing orders
`so-001`…`so-016`; 3 fact-like → ledger facts `so-fact-1`…`so-fact-3`
(they are not rules and do not render to the rules layer).

M-4, 16 bullets at ~371 B each — 12 rule-like → standing orders
`mw-001`…`mw-012`, destination skill `onchain-send` / persona §12 once
content is read; 4 fact-like → ledger facts `mw-fact-1`…`mw-fact-4`.

Every one of the 28 records is currently `binds_gate: null`,
`owner_quote: null`, `owner_date: null`: schema-valid as a fixture,
rejected by `validate_fact(production=True)`. That is deliberate — the
renderer prints a PENDING provenance marker rather than an invented
quote, and no order is silently assigned to kernel or skill.

## Projected LIVE bytes

Itemized base: registry §4 section sizes sum to **21,895 B** (the stated
LIVE total is 22,247 B; 352 B is unitemized — see gaps). Byte shares
within a section are pro-rata by bullet count (D4 heuristic shares, not
measured per-bullet sizes).

| Step | Bytes |
|---|---|
| LIVE today (itemized) | 21,895 |
| M-3 rule-like share leaves (16/19 × 5,489) | −4,622 |
| M-4 rule-like share leaves (12/16 × 5,931) | −4,448 |
| **After extraction only** | **12,825** |
| M-1 header deleted (generated, D22) | −251 |
| M-7 launch doctrine → rules layer (186) | −186 |
| M-9 setup → module skill (1,404) | −1,404 |
| M-5 accounts → ledger facts, rendered on demand (1,982) | −1,982 |
| **LIVE-eligible content under full §2.2 generation** | **9,002** |
| Generated LIVE, newest first, **cut at 6 KB** (§2.2) | **6,144** |

Two honest readings:

1. **Extraction alone does not meet the budget.** 12,825 B > 6 KB. D17
   was never the whole fix; the ≤6 KB figure is a property of the full
   §2.2 generation (LIVE holds exactly: owner profile 2,481 + current
   state 3,586 + fact lines ~2,935 from M-3/M-4/M-6), not of the move.
2. **The budget holds by construction, not by content fitting.**
   Eligible content is 9,002 B; the generator cuts at 6,144 B, newest
   first. The overflow is not deleted — it stays in the ledger and the
   monthly digest, retrievable on demand. The unit test asserts the
   projected generated LIVE ≤ 6,144 B and that zero standing orders
   render into it.

## Gaps

- **Per-order destination unresolved** until backfill reads the text
  (above). The kernel-vs-skill split of the 28 orders is the one number
  this dry run cannot produce from the pack.
- **352 B unitemized**: registry §4 section sizes sum to 21,895 B
  against a stated 22,247 B LIVE total. Immaterial to the budget (both
  projections clear it the same way), but the manifest/scope discipline
  (D8) says an inventory that doesn't foot is UNVERIFIED until it does.
- **Brief vs pack filename**: the lane brief named a "D3 file of live
  MEMORY.md lines"; in the pack, D3 is skills and the memory counts are
  D4, counts only — there is no file of MEMORY.md lines. The fixture was
  built from D4.
