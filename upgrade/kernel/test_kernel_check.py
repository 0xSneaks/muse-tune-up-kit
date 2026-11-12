"""Tests for the step-8 kernel checker."""
import hashlib
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kernel_check

HERE = Path(__file__).resolve().parent
KERNEL = HERE / "KERNEL.md"
SOUL = Path.home() / "SOUL.md"


class RealPackage(unittest.TestCase):
    def test_real_kernel_passes_all_checks(self):
        errors, _ = kernel_check.check(KERNEL, SOUL)
        self.assertEqual(errors, [])

    def test_kernel_and_controlled_total_are_within_caps(self):
        _, metrics = kernel_check.check(KERNEL, SOUL)
        self.assertLessEqual(metrics["kernel_bytes"], kernel_check.KERNEL_HARD_CAP_BYTES)
        self.assertLessEqual(
            metrics["controlled_total_bytes"], kernel_check.CONTROLLED_CAP_BYTES
        )
        self.assertEqual(
            metrics["controlled_total_bytes"],
            metrics["kernel_bytes"]
            + kernel_check.LIVE_PROJECTION_BYTES
            + kernel_check.SKILLS_INDEX_BYTES,
        )

    def test_verbatim_blocks_hash_match_soul_sections(self):
        kernel_text = KERNEL.read_text(encoding="utf-8")
        soul_text = SOUL.read_text(encoding="utf-8")
        source = kernel_check.soul_sections(soul_text)
        blocks = kernel_check.kernel_verbatim_blocks(kernel_text)
        self.assertEqual(set(blocks), set(kernel_check.SOUL_SECTIONS))
        total = 0
        for number in kernel_check.SOUL_SECTIONS:
            total += len(source[number].encode("utf-8"))
            self.assertEqual(
                hashlib.sha256(blocks[number].encode("utf-8")).hexdigest(),
                hashlib.sha256(source[number].encode("utf-8")).hexdigest(),
            )
        self.assertEqual(total, 3519)

    def test_gate_index_names_all_skills_gate_types_and_x2_checks(self):
        gate_index = kernel_check._gate_index(KERNEL.read_text(encoding="utf-8"))
        self.assertTrue(gate_index)
        for name in (
            kernel_check.GATE_TYPES + kernel_check.RULE_SKILLS + kernel_check.X2_CHECKS
        ):
            self.assertIn(f"`{name}`", gate_index)


class Mutations(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.kernel = Path(self.tmp.name) / "KERNEL.md"
        shutil.copyfile(KERNEL, self.kernel)

    def tearDown(self):
        self.tmp.cleanup()

    def test_one_changed_word_in_a_verbatim_block_fails(self):
        text = self.kernel.read_text(encoding="utf-8")
        self.kernel.write_text(
            text.replace("Never lie to Sneaks", "Never mislead Sneaks", 1),
            encoding="utf-8",
        )
        errors, _ = kernel_check.check(self.kernel, SOUL)
        self.assertTrue(any("section 2 is not verbatim" in e for e in errors), errors)

    def test_removed_skill_from_gate_index_fails(self):
        text = self.kernel.read_text(encoding="utf-8")
        self.kernel.write_text(text.replace("`media-verify`", "`media-check`", 1), encoding="utf-8")
        errors, _ = kernel_check.check(self.kernel, SOUL)
        self.assertTrue(any("skill media-verify" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
