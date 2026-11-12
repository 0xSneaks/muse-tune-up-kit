# Kernel cut — owner-review package (step 8)

**Status: PROPOSAL ONLY.** Nothing in this folder is live, applied,
installed, or a substitute for the owner's review. The lane that built
it made no commit and no push.

## Contents

| File | What it is |
|---|---|
| `KERNEL.md` | The proposed kernel: SOUL §§2/11/12/13 verbatim, trimmed persona lines, speed mode, identity/owner cards, the seven-type gate index, the manifest scope line, and the D17 standing-order rendering rule. |
| `KERNEL-DIFF.md` | The owner's review document: current vs proposed bytes, section by section, plus the three carried decisions with the exact text that would change. |
| `kernel_check.py` | Deterministic checker (stdlib only). |
| `test_kernel_check.py` | The checker's tests, including mutation tests. |

## Measured acceptance

- `KERNEL.md`: **9,464 B** — under the D6 hard cap of 10,240 B; 464 B
  over the nominal 9,000 B target.
- Muse-controlled standing total: **16,381 B** = kernel 9,464 +
  generated LIVE projection 6,144 + generated persona skills index
  773 — under the D16 cap of 16,384 B **by 3 bytes**. Any addition to
  the kernel, LIVE, or the index must be offset before this package
  can be applied.
- Owner-locked verbatim content: **3,519 B**, hash-matched section by
  section against `~/SOUL.md` by the checker.

Run:

```
python3 upgrade/kernel/kernel_check.py
python3 -W error -m unittest discover -s upgrade/kernel -p 'test_*.py'
```

## OPEN ITEM FOR THE OWNER — verbatim persona text in a public repo

This clone is the **public** kit repository, and D6 requires the kernel
to carry SOUL §§2, 11, 12, and 13 **verbatim**. `KERNEL.md` therefore
contains those owner-locked sections exactly as written. The lane did
not silently redact them (that would break D6 and the hash check) and
does not decide their publication home. Before this package is
published or applied, the owner chooses one:

1. keep the verbatim kernel in the public kit;
2. move `KERNEL.md` to the private corpus and keep only the design and
   numbers in the public kit; or
3. another owner-specified home for the verbatim kernel.

Until that choice is made, treat this folder as an unpublished review
package, not as approved public content.
