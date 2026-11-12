"""ENFORCED-SNAPSHOT checker for the step-6 snapshot set (SPEC-DELTA D1).

Pairs each named snapshot location (the D1–D5 files Muse gathered in
upgrade/diatomic/muse-side/) with its check and prints one line per pair:

    PAIR <name>: MATCH — <detail>
    PAIR <name>: DRIFT — <detail>

Pairs:
    goals            D2's claimed count vs the rows D2 actually enumerates
    jobs             D1's claimed total vs the rows D1 actually enumerates
    health-schedule  the health job (muse-health-watch) is installed and
                     enabled in D1 — the repo SCHEDULE.md text that calls
                     it "not installed" is the stale side (MUSE-SIDE-REPORT E3)
    skills           D3's parts (system + custom) vs D3's stated total
    memory-counts    D4's per-section rule-like + fact-like vs bullets
    manifest         D5's script recount vs the manifest's own scope counts;
                     a scope that was never stated makes this DRIFT by
                     design (the inventory stands UNVERIFIED, D8)
    cross-file       D5's restated goal/skill totals vs D2's and D3's own

Exit codes follow the snapshot pattern: 0 = every pair MATCH, 1 = at
least one DRIFT, 2 = a fixture is missing or unparseable (checker error).

Run:  python3 -m wrappers.snapshot_check [--side-dir PATH]
      python3 wrappers/snapshot_check.py [--side-dir PATH]
Default --side-dir is upgrade/diatomic/muse-side, resolved from this file.
"""
import argparse
import os
import re
import sys

DEFAULT_SIDE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "..", "diatomic", "muse-side")


def _read(side, name):
    with open(os.path.join(side, name)) as f:
        return f.read()


def _table_rows(text, first_col_header):
    """Data rows of the markdown table whose header starts with first_col_header."""
    rows, in_table = [], False
    for line in text.splitlines():
        if line.startswith("|") and first_col_header in line:
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                break
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(set(c) <= {"-", " ", ":"} for c in cells):  # separator row
                continue
            rows.append(cells)
    return rows


def check_pairs(side):
    """Return [(name, ok, detail)] or raise ValueError on a parse failure."""
    pairs = []

    d2 = _read(side, "D2-goals.md")
    m = re.search(r"Count: (\d+)", d2)
    if not m:
        raise ValueError("D2: no 'Count:' line")
    claimed, rows = int(m.group(1)), _table_rows(d2, "Workspace")
    pairs.append(("goals", claimed == len(rows),
                  f"D2 claims {claimed}, enumerates {len(rows)} workspaces"))

    d1 = _read(side, "D1-jobs.md")
    m = re.search(r"user jobs listed: (\d+)", d1)
    if not m:
        raise ValueError("D1: no 'user jobs listed:' line")
    claimed = int(m.group(1))
    rows = _table_rows(d1, "Job")
    enabled = sum(1 for r in rows if len(r) > 1 and r[1] == "True")
    pairs.append(("jobs", claimed == len(rows),
                  f"D1 claims {claimed}, enumerates {len(rows)} jobs ({enabled} enabled)"))
    health = [r for r in rows if r and r[0] == "muse-health-watch"]
    ok = bool(health) and health[0][1] == "True"
    pairs.append(("health-schedule", ok,
                  "muse-health-watch installed and enabled in D1; "
                  "SCHEDULE.md's 'not installed' text is stale (E3)" if ok
                  else "muse-health-watch missing or disabled in D1"))

    d3 = _read(side, "D3-skills.md")
    ms = re.search(r"System skills[^:]*: (\d+)", d3)
    mc = re.search(r"Custom skills[^:]*: (\d+)", d3)
    mt = re.search(r"Total: (\d+)", d3)
    if not (ms and mc and mt):
        raise ValueError("D3: system/custom/total line missing")
    parts, total = int(ms.group(1)) + int(mc.group(1)), int(mt.group(1))
    pairs.append(("skills", parts == total,
                  f"D3 parts {ms.group(1)} + {mc.group(1)} = {parts} vs stated total {total}"))

    d4 = _read(side, "D4-memory-counts.md")
    secs = re.findall(r"bullets=(\d+), rule-like=(\d+), fact-like=(\d+)", d4)
    if len(secs) < 2:
        raise ValueError("D4: expected two section count lines")
    bad = [f"bullets={b} vs {r}+{f}" for b, r, f in secs if int(r) + int(f) != int(b)]
    pairs.append(("memory-counts", not bad,
                  "both sections sum" if not bad else "mismatch: " + "; ".join(bad)))

    d5 = _read(side, "D5-manifest-diff.md")
    m = re.search(r"Script count, memory tree: \*\*(\d+)", d5)
    if not m:
        raise ValueError("D5: no script-count line")
    recount = int(m.group(1))
    # D5's bullets restate each historical count; the bullet equal to the
    # recount is the recount itself, not a manifest scope.
    scopes = [int(x) for x in re.findall(r"^- \*\*(\d+)\*\* =", d5, re.M)
              if int(x) != recount]
    ok = bool(scopes) and all(s == recount for s in scopes)
    pairs.append(("manifest", ok,
                  f"script recount {recount} vs manifest scope counts {scopes or 'none stated'}"
                  + ("" if ok else " — scopes differ and the manifest never stated its scope (UNVERIFIED, D8)")))

    mg = re.search(r"Goal workspace dirs: \*\*(\d+)\*\*", d5)
    mk = re.search(r"skills: \*\*(\d+)\*\*", d5)
    if not (mg and mk):
        raise ValueError("D5: restated goal/skill totals missing")
    ok = int(mg.group(1)) == claimed_goals(d2) and int(mk.group(1)) == total
    pairs.append(("cross-file", ok,
                  f"D5 restates goals={mg.group(1)}, skills={mk.group(1)} against D2/D3"))
    return pairs


def claimed_goals(d2_text):
    return int(re.search(r"Count: (\d+)", d2_text).group(1))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Step-6 snapshot checker (D1-D5 pairs).")
    ap.add_argument("--side-dir", default=DEFAULT_SIDE)
    a = ap.parse_args(argv)
    try:
        pairs = check_pairs(os.path.normpath(a.side_dir))
    except (OSError, ValueError) as e:
        print(f"snapshot_check: checker error: {e}", file=sys.stderr)
        return 2
    drift = 0
    for name, ok, detail in pairs:
        print(f"PAIR {name}: {'MATCH' if ok else 'DRIFT'} — {detail}")
        drift += 0 if ok else 1
    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(main())
