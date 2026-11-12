"""Step 12: router table -- one test per SPEC-DELTA D14 rule, plus
the D25 second-route / SOLE / failover rules the same delta set adds."""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from router import router
from router.router import Route


class RouterD14(unittest.TestCase):
    def test_second_route_is_a_different_maker_and_platform(self):
        for row in router.ROWS:
            if row.sole:
                self.assertTrue(row.sole_stop, row.task_class)
                continue
            self.assertNotEqual(row.primary.maker, row.second_route.maker,
                                row.task_class)
            self.assertNotEqual(row.primary.platform, row.second_route.platform,
                                row.task_class)

    def test_two_model_check_requires_a_different_maker(self):
        ready = router.two_model_check("consequential-action")
        self.assertEqual(ready["status"], "READY")
        same_maker = Route("deepseek-v4.1-flash", "DeepSeek",
                           "deepseek-direct-api")
        skipped = router.two_model_check("consequential-action", same_maker)
        self.assertEqual(skipped["status"], "NOT_EXECUTED")
        self.assertIn("different maker", skipped["reason"])

    def test_data_class_limits_eligible_providers(self):
        free = Route("beam-free", "community contributor route",
                     "opencode-go-api", "free")
        self.assertTrue(router.is_eligible(free, "public"))
        for data_class in ("personal", "private-code", "wallet"):
            self.assertFalse(router.is_eligible(free, data_class), data_class)
        # Every route the shipped table actually selects is eligible
        # for its own row's data class.
        for row in router.ROWS:
            self.assertTrue(router.is_eligible(row.primary, row.data_class,
                                               row.task_class), row.task_class)
            if row.second_route:
                self.assertTrue(router.is_eligible(row.second_route,
                                                   row.data_class,
                                                   row.task_class), row.task_class)

    def test_wallet_and_security_work_excludes_the_bench_ban_list(self):
        # The list of record is ~/MEMORY.md line 92 (2026-11-03 bench);
        # route names are normalized, so suffixed contributor names
        # are caught too.
        for model in router.WALLET_SECURITY_BANNED_MODELS:
            route = Route(model, "any maker", "opencode-go-api")
            self.assertFalse(router.is_eligible(route, "wallet"), model)
            self.assertFalse(router.is_eligible(route, "personal",
                                                "wallet-security-review"), model)
        contributor = Route("iceman-contributor-free", "community",
                            "opencode-go-api", "contributor")
        self.assertFalse(router.is_eligible(contributor, "wallet"))
        # Route-specific ban: DeepSeek V4 Pro is cleared for wallet
        # work on the direct API leg, banned on the bridge leg.
        direct = Route("deepseek-v4-pro", "DeepSeek", "opencode-go-api")
        bridge = Route("deepseek-v4-pro", "DeepSeek", "seeker-bridge", "bridge")
        self.assertTrue(router.is_eligible(direct, "wallet"))
        self.assertFalse(router.is_eligible(bridge, "wallet"))

    def test_wallet_verifier_sees_digests_only(self):
        check = router.two_model_check("wallet-security-review")
        self.assertEqual(check["status"], "READY")
        self.assertEqual(check["payload_mode"], "digest-only")

    def test_budget_escalation_beyond_approval_is_a_spend_gate_ask(self):
        inside = router.request_escalation("routine-code", 40, 50)
        self.assertEqual(inside["status"], "WITHIN_APPROVED_BUDGET")
        beyond = router.request_escalation("routine-code", 51, 50)
        self.assertEqual(beyond["status"], "SPEND-GATE-ASK")
        self.assertIsNone(beyond["route"])
        selected = router.select_route("routine-code", 51, 50)
        self.assertEqual(selected["status"], "SPEND-GATE-ASK")
        self.assertIsNone(selected["route"])

    def test_failover_is_announced_and_consequential_work_blocks(self):
        routine = router.select_route("routine-code", 10, 50,
                                      primary_available=False)
        self.assertEqual(routine["status"], "FAILOVER_ANNOUNCED")
        self.assertIn("unavailable", routine["announcement"])
        consequential = router.select_route("consequential-action", 10, 50,
                                            primary_available=False)
        self.assertEqual(consequential["status"], "BLOCKED")
        self.assertIsNone(consequential["route"])
        sole = router.select_route("frontier-design-review", 10, 50,
                                   primary_available=False)
        self.assertEqual(sole["status"], "BLOCKED")
        self.assertIn("frontier session", sole["reason"])


if __name__ == "__main__":
    unittest.main()
