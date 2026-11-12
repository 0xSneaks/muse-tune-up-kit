"""Run tasks x seeds against an agent, with gates on or off, and write a results file.

    python3 -m evalrig.runner --agent careful --gates on  --out results/x.json
    python3 -m evalrig.runner --agent "cmd:python3 my_muse_adapter.py" --gates off --freeze --out results/baseline.json
"""
import argparse
import datetime
import hashlib
import json
import os
import tempfile

from muse_gates import GatedTools, Store
from . import agents, tasks
from .fixtures import META, REGISTRY, TOOLS, World


class RawTools:
    """Gates off: the agent talks to the world directly. Same interface as GatedTools."""
    names = TOOLS

    def __init__(self, world):
        self.w = world

    def call(self, name, args, leg=None):
        return self.w.call(name, args)

    def plan(self, legs):
        pass

    def session_start(self):
        return ""

    def finalize(self, report):
        return report


def run_one(agent, tid, seed, gates, state_root):
    task, w = tasks.T[tid], World(seed)
    ctx = task.setup(w)
    if gates:
        store = Store(os.path.join(state_root, f"{tid}-{seed}"))
        tools = GatedTools(w.call, lambda: w.trace, META, store, task_id=f"{tid}-{seed}", approvals=lambda: w.approvals, registry=REGISTRY)
        tools.names = TOOLS
    else:
        tools = RawTools(w)
    agent.start(tid, ctx if agent.scripted else None, tools, gates)
    replies, error = [], None
    try:
        for i, msg in enumerate(task.turns(ctx)):
            w.turn = -1                      # harness-initiated calls are not the agent's
            banner = tools.session_start() if i == 0 else ""
            w.turn = i
            reply = tools.finalize(agent.turn(i, msg, tools) or "")
            replies.append((banner + "\n" + reply).strip() if banner else reply)
    except Exception as e:  # an agent crash is a failed run, not a harness crash
        error = f"{type(e).__name__}: {e}"
        replies += [""] * (len(task.turns(ctx)) - len(replies))
    finally:
        agent.stop()
    crit = [{"criterion": n, "pass": bool(ok), "critical": code} for n, ok, code in task.score(w, ctx, replies)]
    return {"task": tid, "seed": seed, "pass": error is None and all(c["pass"] for c in crit),
            "critical_fails": sorted({c["critical"] for c in crit if c["critical"] and not c["pass"]}),
            "criteria": crit, "tool_calls": len(w.trace), "error": error, "usage": getattr(agent, "usage", [])}


def summarize(runs, task_ids, seeds):
    per_task, cost, have_cost = {}, 0.0, False
    for tid in task_ids:
        rs = [r for r in runs if r["task"] == tid]
        n = sum(r["pass"] for r in rs)
        per_task[tid] = {"guards": tasks.T[tid].guards, "seeds_passed": n, "pass": n * 2 > len(seeds),
                         "flaky": 0 < n < len(seeds), "critical_fails": sorted({c for r in rs for c in r["critical_fails"]})}
    for r in runs:
        for u in r["usage"]:
            if u.get("cost") is not None:
                cost, have_cost = cost + u["cost"], True
    passed = sum(t["pass"] for t in per_task.values())
    return {"tasks": len(task_ids), "passed": passed, "pass_rate": round(passed / len(task_ids), 3),
            "critical_fail_runs": sum(bool(r["critical_fails"]) for r in runs),
            "critical_by_code": {c: sum(c in r["critical_fails"] for r in runs) for c in ("C1", "C2", "C3", "C4", "C5")},
            "total_cost": round(cost, 4) if have_cost else None,
            "cost_per_pass": round(cost / passed, 4) if have_cost and passed else None,
            "tool_calls_median": sorted(r["tool_calls"] for r in runs)[len(runs) // 2], "per_task": per_task}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", required=True, help="careful | naive | cmd:<shell command speaking the JSONL protocol>")
    ap.add_argument("--gates", choices=["on", "off"], required=True)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--tasks", default="smoke", help="smoke or comma-separated task ids")
    ap.add_argument("--label", default="")
    ap.add_argument("--out", required=True)
    ap.add_argument("--freeze", action="store_true", help="write <out>.sha256 and refuse to overwrite an existing frozen file")
    a = ap.parse_args(argv)
    if a.freeze and os.path.exists(a.out + ".sha256"):
        raise SystemExit(f"{a.out} is frozen; choose a new --out")
    agent = {"careful": agents.CAREFUL, "naive": agents.NAIVE}.get(a.agent) or agents.CommandAgent(a.agent[4:])
    ids = tasks.SMOKE if a.tasks == "smoke" else a.tasks.split(",")
    seeds = list(range(1, a.seeds + 1))
    with tempfile.TemporaryDirectory() as state:
        runs = [run_one(agent, t, s, a.gates == "on", state) for t in ids for s in seeds]
    out = {"label": a.label, "agent": a.agent, "scripted_reference": agent.scripted, "gates": a.gates, "seeds": seeds,
           "date": datetime.date.today().isoformat(), "summary": summarize(runs, ids, seeds), "runs": runs}
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    body = json.dumps(out, indent=1, sort_keys=True)
    with open(a.out, "w") as f:
        f.write(body + "\n")
    if a.freeze:
        with open(a.out + ".sha256", "w") as f:
            f.write(hashlib.sha256((body + "\n").encode()).hexdigest() + "  " + os.path.basename(a.out) + "\n")
    s = out["summary"]
    print(f"{a.agent} gates={a.gates}: {s['passed']}/{s['tasks']} tasks passed, critical-fail runs {s['critical_fail_runs']}, cost/pass {s['cost_per_pass']}")
    for tid, t in s["per_task"].items():
        print(f"  {tid:4} {'PASS' if t['pass'] else 'FAIL'} seeds {t['seeds_passed']}/{len(seeds)} {'FLAKY ' if t['flaky'] else ''}{' '.join(t['critical_fails'])}")
    return out


if __name__ == "__main__":
    main()
