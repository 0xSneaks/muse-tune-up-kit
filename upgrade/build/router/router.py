"""Step 12 router table (spec 04, SPEC-DELTA D14 and D25).

The table in S-082 (the model-routing skill) decides *which concrete
route* fills each task class.  This module makes those decisions
checkable rather than prose-only:

* every non-SOLE row has a ``second_route`` on a different platform
  and from a different maker (D14/D25);
* ``data_class`` limits eligible routes before a route is selected;
* wallet/security work excludes every model on the bench ban list and
  every route-specific ban, and a wallet verifier receives digests,
  never the payload itself (D14);
* asking for more budget than the owner approved returns
  ``SPEND-GATE-ASK``.  The router never silently selects the more
  expensive route (D14).

Bench-ban source: ``~/MEMORY.md`` line 92 ("Wallet/security ban
(2026-11-03 bench)"), which records Muse's bench-done report in
``~/ai-coms/handoffs/2026-11-03_0620_muse_model-bench-done.md``.
The underlying route-by-route results are in
``~/ai-coms/results/model-bench-2026-11-03/README.md`` ("BANNED from
wallet/security work" and "Route-specific bans").
"""
from dataclasses import dataclass


DATA_CLASSES = ("public", "personal", "private-code", "wallet")
PROTECTED_TASK_CLASSES = {"wallet-security-review", "security-review"}

# Names are normalized by _model_key(), so "iceman" also covers the
# bench's "iceman-contributor-free" route name.
WALLET_SECURITY_BANNED_MODELS = frozenset({
    "hy3",
    "qwen3.8-max",
    "kimi-k2.7-code",
    "gemini-4-argon",
    "qwen3.7-plus",
    "iceman",
    "grok-4.7",
    "longcat-2.0",
    "minimax-m3",
})

# Passed one bench leg and failed the other: banned only on the named
# platform/route.  Keys are (normalized model, platform).
WALLET_ROUTE_BANS = frozenset({
    ("step-5-preview", "opencode-go-api"),
    ("beam-free", "seeker-bridge"),
    ("deepseek-v4-pro", "seeker-bridge"),
    ("minimax-m3.1-flash", "seeker-bridge"),
})

# A wallet route is eligible only when that exact model/route was
# clean on the 2026-11-03 bench.  An untested route is not cleared.
WALLET_ROUTE_ALLOWLIST = frozenset({
    ("step-5-preview", "seeker-bridge"),
    ("kimi-k3", "opencode-go-api"),
    ("kimi-k3", "seeker-bridge"),
    ("claude-haiku-5-5", "opencode-go-api"),
    ("gpt-5.6-luna", "opencode-go-api"),
    ("gpt-6-luna", "opencode-go-api"),
    ("mimo-v2.6-pro", "opencode-go-api"),
    ("deepseek-v4-pro", "opencode-go-api"),
    ("deepseek-v4.1-flash", "opencode-go-api"),
})


@dataclass(frozen=True)
class Route:
    model: str
    maker: str
    platform: str
    channel: str = "direct-api"  # direct-api | bridge | free | contributor

    @property
    def key(self):
        return f"{self.model}@{self.platform}"

    @property
    def free_or_contributor(self):
        model = self.model.lower()
        return (self.channel in {"free", "contributor"} or ":free" in model
                or model.endswith("-free") or "contributor" in model)


@dataclass(frozen=True)
class TaskRow:
    task_class: str
    primary: Route
    second_route: Route | None
    data_class: str
    two_model_check: bool
    budget_cap: str
    sole_stop: str | None = None

    @property
    def sole(self):
        return self.second_route is None


def _r(model, maker, platform, channel="direct-api"):
    return Route(model, maker, platform, channel)


ROWS = (
    TaskRow(
        "classification-yes-no",
        _r("mimo-v2.6-flash", "Xiaomi", "opencode-go-api"),
        _r("deepseek-v4.1-flash", "DeepSeek", "deepseek-direct-api"),
        "public", False, "8k tokens / 0 tool calls"),
    TaskRow(
        "formatting-summary",
        _r("gpt-5.6-luna", "OpenAI", "opencode-go-api"),
        _r("claude-haiku-5-5", "Anthropic", "claude-cli-local"),
        "personal", False, "20k tokens / 2 tool calls"),
    TaskRow(
        "routine-code",
        _r("mimo-v2.6-pro", "Xiaomi", "opencode-go-api"),
        _r("kimi-k3", "Moonshot AI", "seeker-bridge", "bridge"),
        "private-code", False, "60k tokens / 8 tool calls"),
    TaskRow(
        "research-synthesis",
        _r("kimi-k3", "Moonshot AI", "opencode-go-api"),
        _r("claude-haiku-5-5", "Anthropic", "claude-cli-local"),
        "personal", True, "80k tokens / 5 tool calls"),
    TaskRow(
        "memory-adjudication",
        _r("deepseek-v4-pro", "DeepSeek", "deepseek-direct-api"),
        _r("claude-haiku-5-5", "Anthropic", "claude-cli-local"),
        "personal", False, "80k tokens / 30 tool calls"),
    TaskRow(
        "crew-subagent",
        _r("kimi-k3", "Moonshot AI", "opencode-go-api"),
        _r("mimo-v2.6-pro", "Xiaomi", "seeker-bridge", "bridge"),
        "private-code", True, "60k tokens / 10 tool calls"),
    TaskRow(
        "wallet-security-review",
        _r("step-5-preview", "StepFun", "seeker-bridge", "bridge"),
        _r("kimi-k3", "Moonshot AI", "opencode-go-api"),
        "wallet", True, "250k tokens / 40 tool calls"),
    TaskRow(
        "consequential-action",
        _r("deepseek-v4-pro", "DeepSeek", "deepseek-direct-api"),
        _r("kimi-k3", "Moonshot AI", "seeker-bridge", "bridge"),
        "personal", True, "250k tokens / 40 tool calls"),
    TaskRow(
        "frontier-design-review",
        _r("frontier-evaluator", "Anthropic", "claude-cli-local"),
        None,
        "personal", False, "owner-initiated session",
        sole_stop="STOP: report BLOCKED and wait for the owner to start a frontier session"),
)

TABLE = {row.task_class: row for row in ROWS}
ROUTES = {route.key: route for row in ROWS for route in
          (row.primary, row.second_route) if route is not None}


def _model_key(model):
    key = model.lower().replace("_", "-")
    for suffix in ("-contributor-free", "-contributor"):
        if key.endswith(suffix):
            key = key[:-len(suffix)]
    return key


def is_eligible(route, data_class, task_class=None):
    """Whether `route` may receive data of `data_class`.

    Free/contributor routes get public, throwaway work only.  Wallet
    data -- and wallet/security task classes, whatever data label a
    caller attached -- additionally require an exact bench-clean
    model+route and reject both the global and route-specific bans.
    """
    if data_class not in DATA_CLASSES:
        raise ValueError(f"unknown data_class: {data_class}")
    if route.free_or_contributor and data_class != "public":
        return False
    protected = (data_class == "wallet" or task_class in PROTECTED_TASK_CLASSES
                 or (task_class is not None
                     and ("wallet" in task_class or "security" in task_class)))
    if not protected:
        return True
    model = _model_key(route.model)
    if model in WALLET_SECURITY_BANNED_MODELS:
        return False
    if (model, route.platform) in WALLET_ROUTE_BANS:
        return False
    return (model, route.platform) in WALLET_ROUTE_ALLOWLIST


def two_model_check(task_class, verifier_route=None):
    """Prepare the D14 check for a task class.

    The verifier is the row's second route unless one is supplied.
    Same-maker verification is not a check at all: NOT_EXECUTED.
    For wallet work the verifier's payload mode is digest-only.
    """
    row = TABLE[task_class]
    if not row.two_model_check:
        return {"status": "NOT_REQUIRED", "task_class": task_class,
                "executor": row.primary.key, "verifier": None}
    verifier = verifier_route or row.second_route
    if verifier is None:
        return {"status": "NOT_EXECUTED", "task_class": task_class,
                "executor": row.primary.key, "verifier": None,
                "reason": "SOLE row has no second route"}
    if verifier.maker == row.primary.maker:
        return {"status": "NOT_EXECUTED", "task_class": task_class,
                "executor": row.primary.key, "verifier": verifier.key,
                "reason": "verifier is not from a different maker"}
    if not is_eligible(verifier, row.data_class, task_class):
        return {"status": "NOT_EXECUTED", "task_class": task_class,
                "executor": row.primary.key, "verifier": verifier.key,
                "reason": "verifier route is not eligible for this data class"}
    return {"status": "READY", "task_class": task_class,
            "executor": row.primary.key, "verifier": verifier.key,
            "payload_mode": "digest-only" if row.data_class == "wallet" else "output-and-acceptance-test"}


def request_escalation(task_class, requested_budget, approved_budget):
    """The budget half of D14: inside the approved budget the router
    may proceed; beyond it the only legal answer is SPEND-GATE-ASK."""
    if requested_budget <= approved_budget:
        return {"status": "WITHIN_APPROVED_BUDGET", "task_class": task_class,
                "requested_budget": requested_budget,
                "approved_budget": approved_budget, "route": TABLE[task_class].primary.key}
    return {"status": "SPEND-GATE-ASK", "task_class": task_class,
            "requested_budget": requested_budget,
            "approved_budget": approved_budget, "route": None}


def select_route(task_class, estimated_budget, approved_budget,
                 primary_available=True, second_available=True):
    """Select a route without ever hiding a failover or an overrun.

    A budget overrun is decided before availability: the answer is a
    spend-gate ask, not a silent route to the second (or a costlier)
    provider.  Routine work may fail over to the second route, but the
    result announces it; consequential and wallet/security work does
    not downgrade -- it reports BLOCKED (D25).
    """
    row = TABLE[task_class]
    if estimated_budget > approved_budget:
        return {"status": "SPEND-GATE-ASK", "task_class": task_class,
                "route": None, "estimated_budget": estimated_budget,
                "approved_budget": approved_budget}
    if not is_eligible(row.primary, row.data_class, task_class):
        return {"status": "BLOCKED", "task_class": task_class, "route": None,
                "reason": "primary route is not eligible for this data class"}
    if primary_available:
        return {"status": "ROUTED", "task_class": task_class,
                "route": row.primary.key, "data_class": row.data_class}
    if row.sole:
        return {"status": "BLOCKED", "task_class": task_class, "route": None,
                "reason": row.sole_stop}
    consequential = row.two_model_check or row.data_class == "wallet"
    if consequential:
        return {"status": "BLOCKED", "task_class": task_class, "route": None,
                "reason": "consequential work does not downgrade (D25)"}
    if second_available and is_eligible(row.second_route, row.data_class, task_class):
        return {"status": "FAILOVER_ANNOUNCED", "task_class": task_class,
                "route": row.second_route.key,
                "announcement": f"primary route {row.primary.key} unavailable; "
                                f"continuing on {row.second_route.key}"}
    return {"status": "BLOCKED", "task_class": task_class, "route": None,
            "reason": "no eligible second route available"}
