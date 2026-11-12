# DIATOMIC ANALYSIS — full OS audit + upgrade (tasking for the architect session, from Muse, 2026-11-12)

## What "diatomic" means here — two passes over the same system

1. **ATOMS.** Every smallest indivisible component of Muse's OS, one at a time:
   each standing-file section, each rule, each skill, each scheduled job, each memory
   mechanism, each gate, each routing decision. Nothing is too small to be an atom,
   and no atom gets skipped because it looks fine.
2. **PAIRS.** Every interaction between two atoms: where they duplicate each other,
   contradict each other, depend on each other, cover the same failure class twice,
   or leave a gap neither covers. A system fails at its bonds more often than at
   its atoms — the pair pass is the point of this analysis.

The existing `upgrade/` specs (00–06, retagged at ffc9a52) are the design layer.
This analysis is the **audit layer underneath them**: it tests the real system
atom by atom against those specs, and corrects the specs where the atoms disagree.

## Inputs

IN THIS REPO (read first): `upgrade/CONTEXT-PACK.md` (measured baselines),
`upgrade/RETAG-BRIEF.md` (real F1–F7), `upgrade/00-README.md` through
`06-gainshare-playbook.md`, and `upgrade/CORPUS-MANIFEST.md` (every atom's
identity: name, size, hash — the inventory this analysis must account for, in full).

NOT IN THIS REPO: the *contents* of the standing files, memory files, and skill
bodies. They live on Muse's machine and include personal data; they are supplied
only through a private channel the operator chooses. Any verdict that needs a
file's text and doesn't have it is marked **BLOCKED-ON-CORPUS** with the exact
file and section named — never inferred, never smoothed over. (This is how the
first draft went blind. Do not repeat it.)

## Deliverables (commit to `upgrade/diatomic/`)

1. **ATOM-REGISTRY.md** — every atom from the manifest, one row each: id, type
   (rule / file-section / skill / job / mechanism / gate), size, what it does in
   one line, which failure class (F1–F7) it serves, and its verdict:
   KERNEL / MODULE / CHECK (make it executable) / MERGE (name the survivor) /
   DELETE (name what makes it safe to delete) / KEEP-AS-IS.
   The registry must account for 100% of the manifest. An atom with no row is a
   failed analysis, by the LEG-INVENTORY gate's own standard.
2. **PAIR-MAP.md** — every material pair interaction, grouped: DUPLICATION
   (same job done twice — name the one that should die), CONTRADICTION (atoms
   that cannot both be obeyed — quote the conflict, propose the resolution),
   DEPENDENCY (atom A silently assumes atom B — what breaks when B moves),
   GAP (a failure-class surface no pair covers). Each entry names both atoms
   by registry id.
3. **SPEC-DELTA.md** — corrections to specs 01–06 that the atom/pair evidence
   forces: sections to change, gates/tasks to add or kill, build-order steps
   re-sequenced, day estimates revised. Every delta cites the registry or
   pair-map ids that force it. No delta without evidence.
4. **UPGRADE-VERDICT.md** — the closers, as before: (a) the revised build order
   with the analysis folded in; (b) the top 3 risks the PAIR pass found (bond
   risks, not atom risks); (c) what Pass B tests first, given the pair map.

## Discipline

- Default effort. No fast mode. No sub-agent swarm. This is depth, not breadth
  theatre: one careful pass beats a thousand shallow ones.
- Evidence discipline from the pack applies to you: a claim about an atom you
  could not read is an ASSUMPTION and is labelled as one; a verdict on a file
  you could not read is BLOCKED-ON-CORPUS. Your own earlier F-inferences —
  three right, one partial, one wrong, one missing — are the calibration for
  how much your guesses are worth here.
- The acceptance frame is unchanged: quality gap to the frontier reference
  closed by half per category, standing context ≤16 KB typical, nothing at
  runtime may require a frontier model.
- Public repo rules stand: designs, numbers, and hashes only. Never request,
  quote, or reconstruct personal content from the corpus. If the private
  corpus reaches you, its personal contents are still never committed here.

## Order of work

1. Registry skeleton from the manifest (100% coverage, verdicts pending).
2. Pair pass over the subsystems the pack describes (memory, routing, gates,
   jobs, crew, context layers) — most pair findings are reachable from the
   pack + specs alone.
3. Atom verdicts for everything the pack describes in enough detail; the rest
   go BLOCKED-ON-CORPUS in one consolidated list, so the operator sees exactly
   what the private corpus would unlock.
4. Spec delta + verdict closers.

Report per deliverable: commit hash, file list, atom coverage count
(rows ÷ manifest atoms), and the BLOCKED-ON-CORPUS count. To Sneaks AND to Muse.
Nothing is "done" until Muse verifies the read-back.

## Addendum in force (2026-11-12)

`upgrade/ADDENDUM-OWNED-ORCHESTRATION.md` — owned orchestration / platform-limit independence. Its four questions are part of the pair pass, and proposed class F8 is judged there (stands alone, or folds into F7 with the merged carrier named). No build-order change: steps 1–3 remain the only authorized build steps.
