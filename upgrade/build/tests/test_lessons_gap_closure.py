"""Step 12 (lane B11): lessons-capture gap closure.

B10's pipeline routed all seven registry §8 lessons but captured only
two: K2, K3, K4 and K5 did not exist, and L-3/L-4 had carriers with no
reproducing task assigned. This file is the acceptance record for the
closure: the registry-named tasks are in the suite, the L-3/L-4
assignments are in force, and the capture report reads 7/7.
"""
import os, re, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory_os import lessons

BUILD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# What registry §8 names, plus the step-12 assignments for the two
# lessons whose registry rows name a carrier but no eval task.
EXPECTED_TASKS = {
    "L-1": ["K4"],            # registry: KERNEL line + eval K4
    "L-2": ["E2", "E4", "E7"],  # registry: MERGE (A-016); eval E-series
    "L-3": ["V1"],            # registry: CHECK (STARTUP-ALIVE); V1 assigned step 12
    "L-4": ["G6", "K1"],      # registry: DATA-NOT-ORDERS; G6, K1 assigned step 12
    "L-5": ["K7"],            # registry: CHECK-audited (SOURCE-OR-SILENT); K7 (D15)
    "L-6": ["K1", "K5"],      # registry: KERNEL line; eval K1, K5
    "L-7": ["K2", "K3"],      # registry: KERNEL line; eval K2, K3
}


def suite_ids():
    with open(os.path.join(BUILD, "evalrig", "tasks.py")) as f:
        src = f.read()
    return set(re.findall(r'@task\("([A-Z0-9]+)"', src))


def record(lid):
    return {"id": lid.replace("L", "l-"), "lesson": lid, "ts": "2026-11-12",
            "source": "operator_correction", "fclass": "F6",
            "what": "fixture", "evidence": "test", "pattern": "fixture",
            "carrier": None, "captured": False}


class LessonsGapClosure(unittest.TestCase):
    def setUp(self):
        self.suite = suite_ids()

    def test_registry_named_tasks_exist_in_the_suite(self):
        for tid in ("K2", "K3", "K4", "K5"):
            self.assertIn(tid, self.suite, tid)

    def test_assignments_match_registry_section_8(self):
        for lid, tasks in EXPECTED_TASKS.items():
            d = lessons.route(record(lid), self.suite)
            self.assertEqual(d["eval_tasks"], tasks, lid)
            self.assertEqual(d["missing_eval_tasks"], [], lid)

    def test_all_seven_lessons_captured(self):
        rep = lessons.capture_report([record(l) for l in lessons.CARRIERS],
                                     self.suite)
        self.assertEqual(rep["routed"], 7)
        self.assertEqual(rep["captured"], 7)
        self.assertEqual(rep["uncaptured"], [])


if __name__ == "__main__":
    unittest.main()
