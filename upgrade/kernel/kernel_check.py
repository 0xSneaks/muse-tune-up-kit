#!/usr/bin/env python3
"""Checks for the step-8 kernel proposal package.

The checker is intentionally narrow and deterministic:

* KERNEL.md must be no larger than the D6 hard cap (10,240 B).
* The proposed Muse-controlled standing total must be no larger than
  16,384 B: KERNEL.md + the D17 generated-LIVE projection (6,144 B) +
  the generated persona skills index (773 B, ATOM-REGISTRY P-19).
* Each owner-locked SOUL section (2, 11, 12, 13) must appear exactly
  once between its VERBATIM markers and hash-match the corresponding
  section of ~/SOUL.md.  A section is normalised by stripping trailing
  whitespace only; that is the convention under which the four sections
  total 3,519 B in SPEC-DELTA D6.
* The gate index must name the seven approval gate types from SOUL
  section 11, all five rule skills, and the two X-2 snapshot checks
  (STARTUP-ALIVE and WATCH-THE-WATCHER).

Run from anywhere:
    python3 upgrade/kernel/kernel_check.py [--kernel PATH] [--soul PATH]
Exit code 0 means every check passed; 1 means at least one failed.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

KERNEL_HARD_CAP_BYTES = 10_240
CONTROLLED_CAP_BYTES = 16_384
LIVE_PROJECTION_BYTES = 6_144
SKILLS_INDEX_BYTES = 773  # SOUL section 18 / ATOM-REGISTRY P-19.

SOUL_SECTIONS = ("2", "11", "12", "13")
GATE_TYPES = (
    "SPEND",
    "TRADE-OR-TRANSFER",
    "PUBLIC-SEND-OR-POST",
    "DEPLOY-OR-RELEASE",
    "DEVICE-CHANGE",
    "DELETE-OR-IRREVERSIBLE",
    "ACCOUNT-OR-CREDENTIAL",
)
RULE_SKILLS = (
    "verification-core",
    "media-verify",
    "deploy-verify",
    "onchain-send",
    "pre-publish",
)
X2_CHECKS = ("STARTUP-ALIVE", "WATCH-THE-WATCHER")

_SECTION_RE = re.compile(r"(?m)^(## .*)$")


def soul_sections(text: str) -> dict[str, str]:
    """Return SOUL sections keyed by number, trailing whitespace stripped."""
    parts = _SECTION_RE.split(text)
    sections: dict[str, str] = {}
    for i in range(1, len(parts), 2):
        heading = parts[i]
        match = re.match(r"## (\d+)\.", heading)
        if not match:
            continue
        sections[match.group(1)] = (heading + "\n" + parts[i + 1]).rstrip()
    return sections


def kernel_verbatim_blocks(text: str) -> dict[str, str]:
    """Return the marked verbatim blocks keyed by SOUL section number."""
    blocks: dict[str, str] = {}
    for number in SOUL_SECTIONS:
        pattern = re.compile(
            rf"<!-- VERBATIM:SOUL-{number}:BEGIN -->\n(.*?)\n<!-- VERBATIM:SOUL-{number}:END -->",
            re.DOTALL,
        )
        matches = pattern.findall(text)
        if len(matches) == 1:
            blocks[number] = matches[0].rstrip()
        elif len(matches) > 1:
            blocks[number] = "\n".join(matches)  # check() reports the duplicate.
    return blocks


def _gate_index(text: str) -> str:
    match = re.search(
        r"(?ms)^## Gate index\b(.*?)(?=^## |\Z)", text
    )
    return match.group(1) if match else ""


def check(kernel_path: Path, soul_path: Path) -> tuple[list[str], dict[str, int]]:
    """Return (errors, metrics).  An empty error list means PASS."""
    errors: list[str] = []
    kernel_bytes = kernel_path.read_bytes()
    kernel_text = kernel_bytes.decode("utf-8")
    soul_text = soul_path.read_text(encoding="utf-8")

    kernel_size = len(kernel_bytes)
    controlled_total = kernel_size + LIVE_PROJECTION_BYTES + SKILLS_INDEX_BYTES
    metrics = {
        "kernel_bytes": kernel_size,
        "live_projection_bytes": LIVE_PROJECTION_BYTES,
        "skills_index_bytes": SKILLS_INDEX_BYTES,
        "controlled_total_bytes": controlled_total,
    }
    if kernel_size > KERNEL_HARD_CAP_BYTES:
        errors.append(
            f"KERNEL.md is {kernel_size} B, above the {KERNEL_HARD_CAP_BYTES} B hard cap"
        )
    if controlled_total > CONTROLLED_CAP_BYTES:
        errors.append(
            "Muse-controlled total is "
            f"{controlled_total} B, above the {CONTROLLED_CAP_BYTES} B cap "
            f"(kernel {kernel_size} + LIVE {LIVE_PROJECTION_BYTES} + "
            f"skills index {SKILLS_INDEX_BYTES})"
        )

    source_sections = soul_sections(soul_text)
    blocks = kernel_verbatim_blocks(kernel_text)
    verbatim_total = 0
    for number in SOUL_SECTIONS:
        source = source_sections.get(number)
        if source is None:
            errors.append(f"SOUL.md section {number} not found")
            continue
        verbatim_total += len(source.encode("utf-8"))
        block = blocks.get(number)
        if block is None:
            errors.append(f"KERNEL.md has no single verbatim block for SOUL section {number}")
            continue
        source_hash = hashlib.sha256(source.encode("utf-8")).hexdigest()
        block_hash = hashlib.sha256(block.encode("utf-8")).hexdigest()
        if block_hash != source_hash:
            errors.append(
                f"SOUL section {number} is not verbatim: "
                f"kernel sha256 {block_hash} != SOUL sha256 {source_hash}"
            )
    metrics["verbatim_bytes"] = verbatim_total

    gate_index = _gate_index(kernel_text)
    if not gate_index:
        errors.append("KERNEL.md gate index section not found")
    else:
        for gate_type in GATE_TYPES:
            if f"`{gate_type}`" not in gate_index:
                errors.append(f"gate index does not name gate type {gate_type}")
        for skill in RULE_SKILLS:
            if f"`{skill}`" not in gate_index:
                errors.append(f"gate index does not name skill {skill}")
        for check_name in X2_CHECKS:
            if f"`{check_name}`" not in gate_index:
                errors.append(f"gate index does not name X-2 check {check_name}")
    return errors, metrics


def main(argv: list[str] | None = None) -> int:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kernel", type=Path, default=here / "KERNEL.md")
    parser.add_argument("--soul", type=Path, default=Path.home() / "SOUL.md")
    args = parser.parse_args(argv)

    try:
        errors, metrics = check(args.kernel, args.soul)
    except (OSError, UnicodeDecodeError) as exc:
        print(f"KERNEL CHECK: ERROR — {exc}")
        return 1

    print(f"kernel_bytes={metrics['kernel_bytes']}")
    print(f"verbatim_bytes={metrics['verbatim_bytes']}")
    print(
        "controlled_total_bytes="
        f"{metrics['controlled_total_bytes']} "
        f"(kernel {metrics['kernel_bytes']} + LIVE {metrics['live_projection_bytes']} "
        f"+ skills index {metrics['skills_index_bytes']})"
    )
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print("KERNEL CHECK: FAIL")
        return 1
    print("KERNEL CHECK: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
