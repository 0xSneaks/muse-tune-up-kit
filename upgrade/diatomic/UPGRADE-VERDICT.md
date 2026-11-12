# UPGRADE-VERDICT — closers from the diatomic analysis

Corpus read at private commit `965981a`. Counts: 379 registry rows over
379 atoms (100% of the manifest and its sub-atoms); 63 rows
BLOCKED-ON-CORPUS; 45 pair findings (14 duplication, 13 contradiction, 11 dependency, 7 gap).

## The verdict in five lines

1. The rules file is not a general rulebook. 93.5% of its rule bytes are four
   tool-specific procedures (pre-publish, on-chain send, media, deploy).
   Almost none of it needs to be in context on an ordinary turn.
2. Those procedures are amendment chains: 129 amendment atoms across 16
   versions, 16 of which replace wording that is still in the file.
3. The system already owns the mechanism the diet needs (skills) and two
   of the tools the specs designed from scratch (job runner, health
   checker). The specs duplicated them.
4. The runtime reportedly has no hooks. Gates designed as hooks must be
   re-cut as wrappers, snapshot checks, or after-the-fact audits.
5. The self-audit effort went where the incidents were dramatic, not
   where they recur: F4, F6 and F7 have almost no carriers.

## (a) Revised build order

| Step | Work | Days | Status |
|---|---|---|---|
| 0 | Muse answers three questions: is there any pre-tool or pre-reply hook (P-D8); can crew and cron context differ from main chat (P-D9); who generates and injects the synthesis file (P-G1) | 0.5 | open |
| 1 | Gates library | done | built, `d3c7684`. Follow-up edits D7–D11 and wrapper CLIs: 2 days |
| 2 | Eval rig + 15 smoke tasks | done | built, `d3c7684` |
| 3 | Baseline run on Muse's machine, frozen | 1 | blocked on Muse |
| 4 | Remaining tasks incl. J13–J16, K7, category W; judge mutation test | 6 | |
| 5 | Full read of 184 rule atoms and 37 skill bodies; final CHECK split | 1 | |
| 5b | Chain collapse: resolve pointers, refile, one current-state rule per chain, 16-case regression set | 6 | new |
| 6 | Remaining gates as wrappers or snapshot checks; the nightly auditor job; JOB-TRIAGE-CLASSIFY from A-035 | 3 | |
| 7 | Five skills from the collapsed chains, one per commit, eval between each | 3 | |
| 8 | Kernel diff proposed to the owner (3.5 KB verbatim + trimmed lines) | 1 + review | owner-gated |
| 9 | Fact ledger, backfill, generated views | 4 | |
| 10 | DEP-STAMP, CORRECTION-SWEEP, resurrection guard | 3 | |
| 11 | Consolidation, staleness audit, lessons pipeline (one sink), standing orders out of LIVE | 4 | |
| 12 | Router folded into the existing routing skill; data-class column; spend-gated escalation | 3 | |
| 13 | Full suite, head-to-head, first router fit | 2 | |
| 14 | Gainshare export analyzer | 2 | |

About 52 working days in total, up from 43. The increase is step 5b.
Order rule added: step 5b before step 7, and steps 9–11 before any new
rule is written for publish, send, media or deploy (D19).

## (b) Top 3 risks the pair pass found — bond risks

1. **Splitting bonded rules (P-D2, P-D3, P-C7).** The four domains are
   not separable as filed: 14 atoms span domains, 28 point at other atoms
   by position, and 16 override text that is still present. Moving them
   into skills before the chains are collapsed produces skills that
   contradict themselves or miss a shared rule. This is the most likely
   way the upgrade weakens the verification doctrine, which the
   acceptance frame forbids.
2. **Checks bonded to a hook that is not there (P-D8, P-D7, P-G2).** The
   specs converted prose to "executable checks" on the assumption of an
   interception point. If none exists, a rule removed from standing
   context and "replaced by a gate" is replaced by nothing. Every rule
   must be shown to have an ENFORCED or AUDITED carrier before its prose
   leaves the standing files.
3. **A diet bonded to files Muse may not control or edit (P-G1, P-D5,
   P-D9).** 34 KB of synthesis may be platform-written; 3.5 KB of persona
   is owner-locked; crew and cron context may not be separable. If all
   three go the wrong way, the reachable floor is near 50 KB of standing
   context, not 16.

## (c) What Pass B tests first, given the pair map

1. **The hook question, empirically.** On Muse's machine, try to
   intercept one native tool call and one reply. The answer picks between
   the spec-05 design and D1.
2. **One chain end to end.** Collapse C-SEND-RELEASE (12 atoms, 8,881 B,
   three replacements) to a current-state rule, write its three
   regression cases, and have the frontier evaluator attack the collapsed
   rule against the original 12. If it holds, D4 is viable for the other
   19 chains.
3. **A-035 as code.** Implement the classifier from the atom and run it
   over the last 30 days of real job history. Disagreements with Muse's
   own past classifications are either bugs or evidence the prose was not
   being followed.
4. **Standing orders audit.** Classify each line of M-3 and M-4 as rule
   or fact (on Muse's machine; personal content). That sets the real LIVE
   size.
5. **Inventory independence.** Rebuild the manifest from the filesystem
   by script and diff it against the one Muse wrote (P-G4): 131 / 134 /
   135 files and the missing X assets.

## (d) What the private corpus unlocked, and what is still blocked

Unlocked (was blind before): the domain split, the chain structure, the
label conflict, the locked persona sections, the real triage rule, the
existing tools, and every READ row in the pair map.

BLOCKED-ON-CORPUS (63 rows), consolidated:

| What | Rows | What would unlock it |
|---|---|---|
| System skill bodies | 57 (S-001 … S-057) | their text, or confirmation they are platform-owned and not editable |
| Scheduled job list | 1 (G-4; 31 jobs) | name, schedule, purpose, last status per job |
| Goal workspaces | 1 (G-5; 131) | list with last-touched dates |
| Coordination handoffs | 1 (G-6; 730) | list with open/closed state |
| Memory tree, per file | 3 (G-1, G-2, G-3; 129 files) | present in the corpus but deliberately not opened: personal content, and per-file verdicts are spec 02's backfill job on Muse's machine |

NOT-READ-IN-FULL — a limit of this session, not of the corpus:

| What | Count | Consequence |
|---|---|---|
| Rule atoms A-037 … A-220 | 184 | domain and chain verdicts stand; the 102 CHECK-candidate flags are a keyword heuristic |
| Custom skill bodies | 37 | verdicts rest on the first line of each |
| Live memory, synthesis, user, identity, tools content | 5 files | headings and sizes only, by design |

## Calibration

The first-draft specs guessed at a system they had not seen. Scored
against the corpus: the kernel-and-modules shape, the ledger, and the
eval rig hold; the module budget was wrong by 8×; two gates contradicted
the real rules (P-C10, P-C11); one contradicted the persona (P-C12); and
three components were re-designs of things that exist. Treat the
TITLE-level verdicts in the registry with the same suspicion until
step 5 is done.
