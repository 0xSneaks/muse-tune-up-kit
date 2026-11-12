# REVIEW-PASS — second check of the lane verdicts

The 184 rule-atom verdicts (A-037 … A-220) and the rows in `PAIR-MAP-RULES.md`
came from one read each. This pass re-read a sample against the rules file.
Each atom was matched by the sha column: the first 8 hex of the SHA-256 of the
line, with no trailing newline. All 50 rows matched a line.

## Sample

| Set | How chosen | Rows |
|---|---|---|
| Every DELETE | all of them | 4 (A-050, A-101, A-143, A-152) |
| CONTRADICTION rows whose resolution drops, scopes or weakens a protection | read all 65 resolutions, kept those that delete, scope, merge away or add an option on a gate | 26 (24 rules-file rows, 2 skills-lane rows that cite a rule atom or a gate) |
| MERGE verdicts | `random.sample` with seed 1024 over the 65 lane MERGE rows | 20 |
| **Total** | | **50** |

## Tally

| Result | DELETE | CONTRADICTION | MERGE | Total |
|---|---|---|---|---|
| CONFIRMED | 4 | 18 | 19 | **41** |
| WRONG (corrected in place) | 0 | 4 | 0 | **4** |
| UNCLEAR (owner decision) | 0 | 4 | 1 | **5** |

Wrong in the sample: 4 of 50 (8%), all in the resolution column, all where a
resolution offered a looser option than the source text. None of the four
DELETE or 20 MERGE verdicts was wrong.

## Rows

| Row | Result | Note |
|---|---|---|
| A-050 | CONFIRMED | Survivor A-075 replaces it explicitly and is stricter |
| A-101 | CONFIRMED | Survivor A-089 supersedes it in full and adds the value-and-unit match |
| A-143 | CONFIRMED | A-154 replaces it in full. The replacement drops the absolute bar on unbounded ranges in favour of construction-level enumeration. That is the owner's later text, so it is recorded here, not reversed |
| A-152 | CONFIRMED | A-162 qualifies it and keeps the same fail-closed outcome for an undeterminable probe |
| R-006 | CONFIRMED | Scoping matches both atoms |
| R-007 | **WRONG** | The resolution offered an owner-acceptance bypass of the auto-distribution bar, which the source does not grant. Corrected |
| R-009 | CONFIRMED | Matches the later bar |
| R-012 | CONFIRMED | Keeps the stricter latest wording and the transitive tracing |
| R-016 | **WRONG** | The "base permission stands" option would undo the later lock. Corrected |
| R-017 | **WRONG** | Deleting the absolute sentence would drop it for broadcast, unknown-outcome and non-durable claims. Corrected to scope it instead |
| R-018 | CONFIRMED | Stricter |
| R-019 | UNCLEAR | Money: fail-closed versus exact-key locking under an unverified price. The later atom qualifies but does not replace. Owner decides; fail-closed holds until then |
| R-020 | UNCLEAR | Same decision as R-019 |
| R-022 | CONFIRMED | The later atom makes the search part of the atomic claim |
| R-023 | CONFIRMED | Keeps fail-closed and the ban on invented references |
| R-025 | CONFIRMED | Removes a looser provenance path |
| R-027 | CONFIRMED | The later atom replaces it explicitly |
| R-029 | CONFIRMED | Matches the later qualifier |
| R-030 | CONFIRMED | Matches the later two atoms, including the exhaustive class |
| R-031 | CONFIRMED | Stricter |
| R-033 | **WRONG** | "Or pick one number" would drop a duty; the two numbers measure different things. Corrected |
| R-036 | CONFIRMED | Points to the stricter rule |
| R-045 | CONFIRMED | Stricter |
| R-046 | CONFIRMED | Stricter |
| R-047 | CONFIRMED | Stricter |
| R-049 | CONFIRMED | The later atom scopes the test itself |
| R-050 | UNCLEAR | The resolution adds wording the source does not have ("hands over"). Whether operation end may close a public mutable leg is the owner's call |
| R-052 | CONFIRMED | The later atom names the scope itself |
| K-09 | CONFIRMED | Keeps the stricter re-send criterion |
| K-11 | UNCLEAR | The persona-file grant covers merges and the playbook bars them. Owner decides. The second-reviewer rule for wallet, signing and auth code stays either way |
| A-051 | CONFIRMED | |
| A-078 | CONFIRMED | |
| A-113 | CONFIRMED | Merged text must carry route independence and the unknown-beneficiary fail-closed (see R-021) |
| A-119 | CONFIRMED | |
| A-122 | CONFIRMED | |
| A-127 | CONFIRMED | |
| A-135 | CONFIRMED | |
| A-136 | CONFIRMED | |
| A-174 | CONFIRMED | |
| A-178 | CONFIRMED | |
| A-186 | CONFIRMED | Merged text must carry composition to any depth |
| A-188 | CONFIRMED | |
| A-190 | CONFIRMED | The qualifier governs the merged text (R-029) |
| A-192 | CONFIRMED | The bar governs the merged text |
| A-194 | CONFIRMED | |
| A-195 | CONFIRMED | |
| A-196 | CONFIRMED | |
| A-199 | CONFIRMED | |
| A-214 | CONFIRMED | Merged text must carry the 1 fps floor and the exhaustive class |
| A-216 | UNCLEAR | The merge is right, but the merged text waits on R-019 |

## Not reviewed

- 45 of the 65 lane MERGE rows.
- 39 CONTRADICTION rows whose resolution keeps the stricter text.
- All 48 CHECK (script), 26 CHECK (checklist) and 41 MODULE verdicts.
- The DUPLICATION, GAP and DEPENDENCY rows in `PAIR-MAP-RULES.md`.

At an 8% resolution error rate in the sample, expect a few more loose
resolutions among the unreviewed rows. Re-read any resolution that adds an
"or" option on a gate before it is applied.
