#!/usr/bin/env python3
"""
validate_skill_metadata.py
Validate repo-native skill folders under skills/.

Checks:
  1. Each skill folder contains SKILL.md
  2. SKILL.md begins with YAML frontmatter delimited by ---
  3. Frontmatter includes name and description
  4. name matches the skill folder name
  5. name uses lowercase letters, digits, and hyphens only, max 64 chars
  6. description is a single-line scalar

Usage:
    python3 validate_skill_metadata.py
    python3 validate_skill_metadata.py skills
    python3 validate_skill_metadata.py skills --json

Outputs:
    Human-readable PASS/FAIL summary to stdout by default.
    JSON report with --json.

Exit codes:
    0 = all checked skills valid
    1 = one or more skills invalid, or input error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
TOP_LEVEL_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate skill metadata and frontmatter.")
    parser.add_argument(
        "skills_root",
        nargs="?",
        default="skills",
        help="Path to the skills root directory (default: skills)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of human-readable text",
    )
    return parser.parse_args()


def extract_frontmatter(skill_md: Path) -> tuple[dict[str, str | None], list[str]]:
    issues: list[str] = []
    text = skill_md.read_text(encoding="utf-8", errors="replace")

    if not text.startswith("---\n"):
        return {}, ["SKILL.md must begin with YAML frontmatter delimited by ---"]

    lines = text.splitlines()
    end_index = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_index = idx
            break

    if end_index is None:
        return {}, ["SKILL.md frontmatter is missing a closing --- delimiter"]

    frontmatter_lines = lines[1:end_index]
    data: dict[str, str | None] = {}
    current_key: str | None = None

    for raw_line in frontmatter_lines:
        if not raw_line.strip():
            continue

        if raw_line.startswith((" ", "\t")):
            if current_key == "description":
                issues.append("description must be a single-line scalar, not a block or nested value")
            continue

        match = TOP_LEVEL_KEY_RE.match(raw_line)
        if not match:
            current_key = None
            continue

        key = match.group(1)
        value = match.group(2) if match.group(2) is not None else ""
        data[key] = value
        current_key = key

        if key == "description" and value.strip() in {"", "|", ">"}:
            issues.append("description must be present as a single-line scalar")

    return data, issues


def validate_skill_dir(skill_dir: Path) -> dict:
    issues: list[str] = []
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.is_file():
        return {
            "skill_dir": skill_dir.name,
            "valid": False,
            "issues": ["SKILL.md is missing"],
        }

    data, fm_issues = extract_frontmatter(skill_md)
    issues.extend(fm_issues)

    name = data.get("name")
    description = data.get("description")

    if name is None or name == "":
        issues.append("frontmatter must include non-empty name")
    else:
        if not NAME_RE.fullmatch(name):
            issues.append("name must use lowercase letters, digits, and hyphens only, max 64 chars")
        if name != skill_dir.name:
            issues.append(f"name must match folder name ({skill_dir.name})")

    if description is None or description == "":
        issues.append("frontmatter must include non-empty description")
    else:
        if "\n" in description:
            issues.append("description must be single-line")

    return {
        "skill_dir": skill_dir.name,
        "valid": not issues,
        "issues": issues,
    }


def main() -> int:
    args = parse_args()
    skills_root = Path(args.skills_root).expanduser().resolve()

    if not skills_root.exists():
        print(f"ERROR: skills root does not exist: {skills_root}", file=sys.stderr)
        return 1
    if not skills_root.is_dir():
        print(f"ERROR: skills root is not a directory: {skills_root}", file=sys.stderr)
        return 1

    skill_dirs = sorted([path for path in skills_root.iterdir() if path.is_dir()])
    results = [validate_skill_dir(skill_dir) for skill_dir in skill_dirs]

    valid_count = sum(1 for item in results if item["valid"])
    invalid_count = len(results) - valid_count

    report = {
        "skills_root": str(skills_root),
        "checked_skill_count": len(results),
        "valid_skill_count": valid_count,
        "invalid_skill_count": invalid_count,
        "results": results,
    }

    if args.json:
        sys.stdout.write(json.dumps(report, indent=2, sort_keys=True) + "\n")
    else:
        for item in results:
            if item["valid"]:
                print(f"PASS  {item['skill_dir']}")
            else:
                print(f"FAIL  {item['skill_dir']}")
                for issue in item["issues"]:
                    print(f"  - {issue}")
        print(
            f"\nSummary: {valid_count} valid, {invalid_count} invalid, {len(results)} checked"
        )

    return 0 if invalid_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
