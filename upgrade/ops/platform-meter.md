# PLATFORM-METER — weekly report spec (step 6, SPEC-DELTA D26 + D16)

**Status: SPEC ONLY.** Not installed, no checker is patched. D26 puts
PLATFORM-METER inside the existing health checker as a separate row;
wiring it there is a live change and waits for the owner's word. This
spec defines what the report contains so the wiring is mechanical.

## Cadence

Weekly, aligned to the health watch's existing schedule family (the
report is a section the weekly health run emits, not a new job).
State: `platform-meter-state.json` beside the report — last run's
numbers, so every figure below ships with its delta.

## Section 1 — standing-context bytes

Byte counts of the nine standing files, exactly as injected at session
construction (MUSE-SIDE-REPORT §A2 measured all nine at 222,578 B):

| File | Owner of the bytes |
|---|---|
| AGENTS.md | Muse |
| SOUL.md | owner (Muse edits only as directed) |
| TOOLS.md | Muse |
| IDENTITY.md | Muse |
| USER.md | Muse |
| MEMORY.md | Muse |
| memory/people/INDEX.md | platform-rendered from Muse's memory |
| memory/groups/INDEX.md | platform-rendered from Muse's memory |
| dreams/alignment/derived/ALIGNMENT_SYNTHESIS.md | **platform** |

Reporting rule (D16, resolved by §A3): the acceptance line is
**Muse-controlled standing bytes ≤ 16 KB** (target after the kernel
cut; 20 KB hard cap). The platform's bytes — ALIGNMENT_SYNTHESIS at
34,150 B at last measurement, plus the two rendered indexes — are
reported alongside, never folded into the budget and never blamed on
it. Every file row shows bytes now, bytes at last report, and the
delta; a file that appears or disappears from the injection is a
finding, not a silent row change.

## Section 2 — scheduled jobs

Job count from the same snapshot the health watch already captures:
total user jobs, enabled, disabled (last snapshot: 31 total, 24
enabled — D1). Deltas vs last report. A job count change with no
matching owner instruction in the week's record is a finding.

## Section 3 — platform meters and term dates (D26)

For each platform with a readable meter or a term date (source: the
ai-coms `usage/` files — claude.md, deepseek.md, muse-crew.md — plus
connector status): current usage %, reset/term date, days to term.

- **≥ 70%** of a period meter: warn row in the report.
- **≥ 90%**: plan row — the report names the work that must move,
  shrink or wait (the router's decision log is the input; where no
  meter is readable, D26's fallback applies: estimate from that log).
- **Term ending within 14 days**: plan row naming the renewal decision
  and its owner. Nothing renews itself; the meter never spends.

## Output

One report file per week (`platform-meter-YYYY-MM-DD.md` beside this
spec's runtime home), sections in the order above, every number with
its delta, findings as explicit rows. Delivery follows the health
watch's existing rules — the report existing is not a chat message;
only warn/plan rows ride the health watch's normal alert path.

## What this is not

Not STARTUP-ALIVE (D26: a separate row, not an extension of it), not a
spend action, not an auto-renewal, and not a context editor: shrinking
a standing file is the kernel cut (step 8, owner-reviewed diff), never
something this meter does.
