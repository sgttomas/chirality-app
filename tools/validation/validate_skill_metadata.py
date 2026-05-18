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
  7. metadata.chirality-skill-version is present
  8. metadata.chirality-task-profile is present and valid
  9. allowed-tools, when present, follows the canonical TASK-consumed format
 10. allowed-tools tool paths resolve to existing files under tools/
 11. BRIEF_SCHEMA.md is present in the skill folder
 12. TOOL_POLICY.md is present in the skill folder
 13. QA_CHECKS.md is present in the skill folder

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
PROFILE_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")
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


def strip_matching_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_allowed_tools(raw_value: str, repo_root: Path) -> list[str]:
    issues: list[str] = []

    if not raw_value:
        return ["allowed-tools must be omitted or a non-empty scalar"]

    if "," in raw_value and ", " not in raw_value:
        return ["allowed-tools must use comma-space delimiters between command specs"]

    specs = raw_value.split(", ")
    for spec in specs:
        if not spec:
            issues.append("allowed-tools contains an empty command spec")
            continue

        if spec.count(":") < 1:
            issues.append(f"allowed-tools spec is missing :<scope_glob>: {spec}")
            continue

        command_prefix, scope_glob = spec.rsplit(":", 1)
        if not scope_glob:
            issues.append(f"allowed-tools spec is missing scope_glob after final colon: {spec}")
            continue

        parts = command_prefix.split(" ")
        if len(parts) != 2:
            issues.append(
                "allowed-tools spec must be exactly '<interpreter> <repo-relative-tool-path>:<scope_glob>'"
            )
            continue

        interpreter, tool_path = parts
        if not interpreter or not tool_path:
            issues.append(f"allowed-tools spec has empty interpreter or tool path: {spec}")
            continue

        if not tool_path.startswith("tools/"):
            issues.append(f"allowed-tools tool path must start with tools/: {tool_path}")
            continue

        resolved_path = (repo_root / tool_path).resolve()
        try:
            resolved_path.relative_to((repo_root / "tools").resolve())
        except ValueError:
            issues.append(f"allowed-tools tool path must resolve under tools/: {tool_path}")
            continue

        if not resolved_path.is_file():
            issues.append(f"allowed-tools tool path does not exist: {tool_path}")

    return issues


def extract_frontmatter(skill_md: Path) -> tuple[dict[str, object], list[str]]:
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
    data: dict[str, object] = {}
    current_key: str | None = None

    for raw_line in frontmatter_lines:
        if not raw_line.strip():
            continue

        if raw_line.startswith((" ", "\t")):
            if current_key == "description":
                issues.append("description must be a single-line scalar, not a block or nested value")

            if current_key is None:
                issues.append(f"unexpected indented line in frontmatter: {raw_line.rstrip()}")
                continue

            match = TOP_LEVEL_KEY_RE.match(raw_line.strip())
            if not match:
                issues.append(f"could not parse nested frontmatter line: {raw_line.rstrip()}")
                continue

            nested_key = match.group(1)
            nested_value = strip_matching_quotes(match.group(2) if match.group(2) is not None else "")
            existing = data.get(current_key)
            if not isinstance(existing, dict):
                existing = {}
                data[current_key] = existing
            existing[nested_key] = nested_value
            continue

        match = TOP_LEVEL_KEY_RE.match(raw_line)
        if not match:
            current_key = None
            continue

        key = match.group(1)
        value = strip_matching_quotes(match.group(2) if match.group(2) is not None else "")
        data[key] = value
        current_key = key

        if key == "description" and value.strip() in {"", "|", ">"}:
            issues.append("description must be present as a single-line scalar")

    return data, issues


def validate_skill_dir(skill_dir: Path, repo_root: Path) -> dict:
    issues: list[str] = []
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.is_file():
        return {
            "skill_dir": skill_dir.name,
            "valid": False,
            "issues": ["SKILL.md is missing"],
        }

    brief_schema_md = skill_dir / "BRIEF_SCHEMA.md"
    if not brief_schema_md.is_file():
        issues.append(
            "BRIEF_SCHEMA.md is missing "
            "(required by AGENT_HELPS_HUMANS Design Outcomes for Skill Contracts)"
        )

    tool_policy_md = skill_dir / "TOOL_POLICY.md"
    if not tool_policy_md.is_file():
        issues.append("TOOL_POLICY.md is missing (required by AGENT_HELPS_HUMANS Design Outcomes for Skill Contracts)")

    qa_checks_md = skill_dir / "QA_CHECKS.md"
    if not qa_checks_md.is_file():
        issues.append(
            "QA_CHECKS.md is missing "
            "(required by AGENT_HELPS_HUMANS Design Outcomes for Skill Contracts)"
        )

    data, fm_issues = extract_frontmatter(skill_md)
    issues.extend(fm_issues)

    name = data.get("name")
    description = data.get("description")
    allowed_tools = data.get("allowed-tools")
    metadata = data.get("metadata")

    if not isinstance(name, str) or name == "":
        issues.append("frontmatter must include non-empty name")
    else:
        if not NAME_RE.fullmatch(name):
            issues.append("name must use lowercase letters, digits, and hyphens only, max 64 chars")
        if name != skill_dir.name:
            issues.append(f"name must match folder name ({skill_dir.name})")

    if not isinstance(description, str) or description == "":
        issues.append("frontmatter must include non-empty description")
    else:
        if "\n" in description:
            issues.append("description must be single-line")

    if allowed_tools is not None:
        if not isinstance(allowed_tools, str):
            issues.append("allowed-tools must be a single-line scalar when present")
        else:
            issues.extend(parse_allowed_tools(allowed_tools, repo_root))

    if not isinstance(metadata, dict):
        issues.append("frontmatter must include metadata mapping")
        metadata = {}

    skill_version = metadata.get("chirality-skill-version")
    if not isinstance(skill_version, str) or skill_version == "":
        issues.append("metadata.chirality-skill-version must be present as a non-empty scalar")

    task_profile = metadata.get("chirality-task-profile")
    if not isinstance(task_profile, str) or task_profile == "":
        issues.append("metadata.chirality-task-profile must be present as a non-empty scalar")
    else:
        if task_profile != "NONE" and not PROFILE_RE.fullmatch(task_profile):
            issues.append("metadata.chirality-task-profile must be NONE or an uppercase token")
        if task_profile != "NONE":
            expected_profile_file = repo_root / "agents" / f"AGENT_{task_profile}.md"
            if not expected_profile_file.is_file():
                issues.append(
                    f"metadata.chirality-task-profile must resolve to an agent instruction file ({expected_profile_file.name})"
                )

    return {
        "skill_dir": skill_dir.name,
        "valid": not issues,
        "issues": issues,
    }


def main() -> int:
    args = parse_args()
    skills_root = Path(args.skills_root).expanduser().resolve()
    repo_root = skills_root.parent

    if not skills_root.exists():
        print(f"ERROR: skills root does not exist: {skills_root}", file=sys.stderr)
        return 1
    if not skills_root.is_dir():
        print(f"ERROR: skills root is not a directory: {skills_root}", file=sys.stderr)
        return 1

    skill_dirs = sorted([path for path in skills_root.iterdir() if path.is_dir()])
    results = [validate_skill_dir(skill_dir, repo_root) for skill_dir in skill_dirs]

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
