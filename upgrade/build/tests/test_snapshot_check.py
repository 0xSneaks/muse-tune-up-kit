"""Tests for the step-6 snapshot checker against the real D1-D5 fixtures
in upgrade/diatomic/muse-side/, plus synthetic drift/parse-error cases."""
import io, os, shutil, sys, tempfile, unittest
from contextlib import redirect_stderr, redirect_stdout
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from wrappers import snapshot_check

SIDE = snapshot_check.DEFAULT_SIDE


def run(side):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = snapshot_check.main(["--side-dir", side])
    return code, out.getvalue(), err.getvalue()


class RealFixtures(unittest.TestCase):
    def test_pairs_against_committed_fixtures(self):
        pairs = dict()
        for name, ok, _ in snapshot_check.check_pairs(SIDE):
            pairs[name] = ok
        self.assertEqual(pairs, {"goals": True, "jobs": True, "health-schedule": True,
                                 "skills": True, "memory-counts": True,
                                 "manifest": False,      # known: scopes 131/134 vs recount 135
                                 "cross-file": True})

    def test_exit_code_is_1_while_manifest_drifts(self):
        code, out, _ = run(SIDE)
        self.assertEqual(code, 1)
        self.assertIn("PAIR manifest: DRIFT", out)
        self.assertIn("PAIR goals: MATCH", out)


class Synthetic(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.side = os.path.join(self.tmp.name, "side")
        shutil.copytree(SIDE, self.side)

    def tearDown(self):
        self.tmp.cleanup()

    def _edit(self, name, old, new):
        p = os.path.join(self.side, name)
        with open(p) as f:
            text = f.read()
        with open(p, "w") as f:
            f.write(text.replace(old, new, 1))

    def test_mutated_goal_count_reports_drift(self):
        self._edit("D2-goals.md", "Count: 132", "Count: 131")
        pairs = {n: ok for n, ok, _ in snapshot_check.check_pairs(self.side)}
        self.assertFalse(pairs["goals"])

    def test_missing_fixture_dir_is_checker_error_exit_2(self):
        code, _, err = run(os.path.join(self.tmp.name, "nope"))
        self.assertEqual(code, 2)
        self.assertIn("checker error", err)


if __name__ == "__main__":
    unittest.main()
