"""Step 11b: lessons pipeline -- one sink, exactly one carrier per
lesson (spec 02 section 2.8, SPEC-DELTA D15, ATOM-REGISTRY section 8)."""
import os, re, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory_os import lessons

BUILD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def suite_ids():
    with open(os.path.join(BUILD, "evalrig", "tasks.py")) as f:
        src = f.read()
    return set(re.findall(r'@task\("([A-Z0-9]+)"', src))


def record(lid):
    return {"id": lid.replace("L", "l-"), "lesson": lid, "ts": "2026-11-12",
            "source": "operator_correction", "fclass": "F6",
            "what": "fixture", "evidence": "test", "pattern": "fixture",
            "carrier": None, "captured": False}


class LessonsPipeline(unittest.TestCase):
    def setUp(self):
        self.suite = suite_ids()
        self.assertIn("K7", self.suite)  # sanity: the suite really loaded

    def test_seven_lessons_each_route_to_exactly_one_carrier(self):
        self.assertEqual(len(lessons.CARRIERS), 7)
        for lid in lessons.CARRIERS:
            d = lessons.route(record(lid), self.suite)
            self.assertIsNotNone(d["carrier"], lid)
            self.assertIn(d["carrier"]["kind"],
                          ("check", "gate", "eval", "module", "merge", "kernel"))
            # One sink: the decision carries a single carrier object,
            # never a list of destinations.
            self.assertIsInstance(d["carrier"], dict)

    def test_captured_only_when_reproducing_task_exists(self):
        # L-5: carrier SOURCE-OR-SILENT + K7, and K7 is in the suite.
        d = lessons.route(record("L-5"), self.suite)
        self.assertEqual(d["eval_tasks"], ["K7"])
        self.assertTrue(d["captured"])
        # L-2: carrier A-016 merge + the E-series, all present.
        d = lessons.route(record("L-2"), self.suite)
        self.assertEqual(d["missing_eval_tasks"], [])
        self.assertTrue(d["captured"])

    def test_uncaptured_lessons_name_their_blocker(self):
        # L-3, L-4: registry names a carrier but no eval task (s2.8.3).
        for lid in ("L-3", "L-4"):
            d = lessons.route(record(lid), self.suite)
            self.assertFalse(d["captured"], lid)
            self.assertEqual(d["eval_tasks"], [], lid)
        # L-1, L-6, L-7: registry names K4 / K5 / K2+K3, none in suite.
        expected_missing = {"L-1": ["K4"], "L-6": ["K5"], "L-7": ["K2", "K3"]}
        for lid, missing in expected_missing.items():
            d = lessons.route(record(lid), self.suite)
            self.assertFalse(d["captured"], lid)
            self.assertEqual(d["missing_eval_tasks"], missing, lid)

    def test_unassigned_lesson_stays_open(self):
        d = lessons.route(record("L-99"), self.suite)
        self.assertIsNone(d["carrier"])
        self.assertFalse(d["captured"])

    def test_capture_report_counts(self):
        rep = lessons.capture_report([record(l) for l in lessons.CARRIERS],
                                     self.suite)
        self.assertEqual(rep["routed"], 7)
        self.assertEqual(rep["captured"], 2)  # L-2 and L-5 only
        self.assertEqual(len(rep["uncaptured"]), 5)


if __name__ == "__main__":
    unittest.main()
