"""Lessons pipeline -- one sink (spec 02 section 2.8, SPEC-DELTA D15).

Replaces a hand-written lessons file where every lesson became permanent
injected prose. Capture is automatic (operator correction, gate fail,
eval fail, router owner-correction line, STARTUP-ALIVE / JOB-TRIAGE
incident); each captured lesson is routed to exactly ONE carrier, chosen
in the spec's preference order: executable check -> eval task -> module
line -> kernel line. A lesson counts as captured only when it has a
carrier AND an eval task that reproduces the incident (section 2.8.3);
`captured` below also requires that task to exist in the current suite.

CARRIERS is the assignment of record for the seven existing lessons:
ATOM-REGISTRY section 8 (D15: "Carriers for the seven existing lessons
are assigned in registry section 8"). Where the registry names both a
carrier and an eval task, the carrier is the sink and the task is the
reproduction. Known gaps, stated plainly:
- L-3 and L-4: the registry names a carrier but no eval task, so by
  section 2.8.3 they are routed but not yet captured.
- L-1, L-6, L-7: the registry names eval tasks K4, K5, K2/K3 that are
  not in the current eval suite (only K1 and K7 are), so those lessons
  are likewise not yet captured. The routing does not invent the tasks.
"""

# Registry section 8 verdicts, one primary carrier per lesson.
CARRIERS = {
    "L-1": {"kind": "kernel", "name": "kernel line (no filler / repeated status on calls)",
            "eval_tasks": ["K4"], "registry": "KERNEL line + eval K4"},
    "L-2": {"kind": "merge", "name": "A-016 (verification-core): green CI is not done",
            "eval_tasks": ["E2", "E4", "E7"], "registry": "MERGE (survivor: A-016); eval E-series"},
    "L-3": {"kind": "check", "name": "STARTUP-ALIVE (start the relay worker first)",
            "eval_tasks": [], "registry": "CHECK (STARTUP-ALIVE)"},
    "L-4": {"kind": "gate", "name": "DATA-NOT-ORDERS (ambient speech is not an order)",
            "eval_tasks": [], "registry": "MERGE (survivor: persona s9 line); DATA-NOT-ORDERS"},
    "L-5": {"kind": "gate", "name": "SOURCE-OR-SILENT, audited (read list items from the list)",
            "eval_tasks": ["K7"], "registry": "CHECK-audited (SOURCE-OR-SILENT); new eval task (D15: K7)"},
    "L-6": {"kind": "kernel", "name": "kernel line (stay silent while he narrates a screen)",
            "eval_tasks": ["K1", "K5"], "registry": "KERNEL line; eval K1, K5"},
    "L-7": {"kind": "kernel", "name": "kernel line (verdict before agreement)",
            "eval_tasks": ["K2", "K3"], "registry": "KERNEL line; eval K2, K3"},
}

PREFERENCE = ["check", "gate", "eval", "module", "merge", "kernel"]


def route(record, suite_ids):
    """Route one lesson record to its single assigned carrier.

    `record`: a lessons.jsonl line (spec 02 section 2.8 shape) whose `id`
    is one of the seven existing lessons, or a new incident carrying an
    explicit `lesson` field naming one. Returns the routing decision:
    exactly one carrier, its reproducing eval tasks, which of those tasks
    are missing from the suite, and whether the lesson is captured.
    """
    lid = record.get("lesson") or record.get("id")
    if lid not in CARRIERS:
        return {"lesson": lid, "carrier": None, "captured": False,
                "reason": "no carrier assigned; stays open (spec 02 s2.8.2)"}
    c = CARRIERS[lid]
    missing = [t for t in c["eval_tasks"] if t not in suite_ids]
    return {"lesson": lid,
            "carrier": {"kind": c["kind"], "name": c["name"]},
            "eval_tasks": list(c["eval_tasks"]),
            "missing_eval_tasks": missing,
            "captured": bool(c["eval_tasks"]) and not missing,
            "registry": c["registry"]}


def capture_report(records, suite_ids):
    """S10-shaped summary over a batch of lesson records: routed count,
    captured count, and the uncaptured ids with their blockers."""
    routed = [route(r, suite_ids) for r in records]
    return {"routed": len(routed),
            "captured": sum(1 for r in routed if r["captured"]),
            "uncaptured": [{"lesson": r["lesson"],
                            "missing_eval_tasks": r.get("missing_eval_tasks", []),
                            "reason": r.get("reason", "")}
                           for r in routed if not r["captured"]],
            "decisions": routed}
