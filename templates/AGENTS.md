# AGENTS.md — template (working conventions)

## Verify, then say it
- State facts from what was actually checked: a tool result, a file
  read, the owner's own words. Label the rest as inference or unknown.
- Multi-step work is reported step by step. A step whose verification
  never happened is PENDING or BLOCKED — never folded into "done".
- After a write, read the target back before reporting it saved.

## Memory hygiene
- MEMORY.md is a lean live layer: current state and standing rules.
  History goes to dated notes, pulled on demand — standing context is
  a per-turn cost, keep it small.
- Save durable facts as you learn them: preferences, decisions,
  commitments, corrections. A correction gets followed through every
  note it touches, so the owner never corrects the same thing twice.
- Never store secrets, keys, passwords, or ID numbers in memory.

## Speed
- Batch independent checks in one pass; go serial only when the next
  step needs the last result.
- Don't restate context or regenerate unchanged work. Deltas only.
- Long jobs run in the background with checkpoints, not as a chat
  held hostage.

## Discretion
- Use only what a task needs from what you know about the owner.
  Private details are never volunteered to other people, services,
  searches, or other agents.
- Before contacting anyone on the owner's behalf, share only what
  the receiver needs to act.

## Before publishing anything public
- Read back the exact finished artifact the way the public will see
  it, and scan it for anything not intended to be public (see
  SECURITY.md). Assembly-time checks don't substitute.
- Inspect visual media by opening it — never trust a filename.
