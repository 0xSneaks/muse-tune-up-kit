"""Harness self-test: every scorer must pass the careful reference and fail the naive one.
If a task passes the naive agent, the task cannot detect its failure class."""
import os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from evalrig import agents, tasks
from evalrig.runner import run_one


class Harness(unittest.TestCase):
    def test_careful_passes_and_naive_fails_every_task_and_seed(self):
        with tempfile.TemporaryDirectory() as d:
            for tid in tasks.SMOKE:
                for seed in (1, 2, 3, 4, 5):
                    good = run_one(agents.CAREFUL, tid, seed, True, os.path.join(d, "g"))
                    bad = run_one(agents.NAIVE, tid, seed, False, os.path.join(d, "n"))
                    self.assertTrue(good["pass"], (tid, seed, [c for c in good["criteria"] if not c["pass"]], good["error"]))
                    self.assertFalse(bad["pass"], (tid, seed))
                    self.assertEqual(good["critical_fails"], [])

    def test_fixtures_vary_by_seed(self):
        from evalrig.fixtures import World
        ctxs = {str(tasks.T["M2"].setup(World(s))) for s in range(1, 9)}
        self.assertGreater(len(ctxs), 3)

    def test_command_agent_protocol(self):
        echo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "adapters", "example_agent.py")
        with tempfile.TemporaryDirectory() as d:
            r = run_one(agents.CommandAgent(f"{sys.executable} {echo}"), "G9", 1, True, d)
        self.assertIsNone(r["error"])
        self.assertTrue(r["pass"], r["criteria"])
        self.assertEqual(r["usage"][0]["cost"], 0.0)


if __name__ == "__main__":
    unittest.main()
