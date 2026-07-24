#!/usr/bin/env python3
"""Validate the mechanically observable AGENT_*.md instruction contract.

Usage:
    python3 tools/validation/validate_agent_instructions.py
    python3 tools/validation/validate_agent_instructions.py agents/AGENT_TASK.md
    python3 tools/validation/validate_agent_instructions.py --json

Checks structural fields and section presence, type/class compatibility,
R-identifier references, exact AGENT_*.md references, and D-GOV-11 dedicated
Agent 2 requalification posture. Semantic agent qualification remains a rubric audit.

Exit codes:
    0 = no ERROR findings (WARN findings may remain)
    1 = one or more ERROR findings
    2 = operational/input failure
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


REQUIRED_MARKERS = (
    "[[DOC:AGENT_INSTRUCTIONS]]",
    "[[BEGIN:PROTOCOL]]",
    "[[END:PROTOCOL]]",
    "[[BEGIN:SPEC]]",
    "[[END:SPEC]]",
    "[[BEGIN:STRUCTURE]]",
    "[[END:STRUCTURE]]",
    "[[BEGIN:RATIONALE]]",
    "[[END:RATIONALE]]",
)
REQUIRED_FIELDS = (
    "AGENT_TYPE",
    "AGENT_CLASS",
    "INTERACTION_SURFACE",
    "WRITE_SCOPE",
    "BLOCKING",
    "PRIMARY_OUTPUTS",
)
WRITE_SCOPE_PREFIXES = (
    "repo-wide",
    "project-level",
    "package-level",
    "deliverable-local",
    "tool-root-only",
    "workspace-scaffold-only",
    "repo-metadata-only",
    "bounded-task-brief",
    "none",
)

REQUIRED_DELEGATION_EDGES = {
    "PROJECT_SETUP": {"PREPARATION", "DOMAIN_HYPERGRAPH", "AGGREGATION", "TASK"},
    "RESEARCH": {"RESEARCHER"},
    "EVALUATION": {
        "TASK",
        "AUDIT_DEP_CLOSURE",
        "AUDIT_AGENTS",
        "AUDIT_DECOMP",
        "AUDIT_GOVERNANCE",
        "AUDIT_EPISTEMIC",
        "AUDIT_HYPERGRAPH_CLOSURE",
        "AUDIT_SCOPE_CLOSURE",
        "EVALUATION_REPORT",
        "EVALUATION_STRUCTURE_AUDIT",
        "EVALUATION_DEPENDENCY_AUDIT",
    },
}


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Agent files; defaults to agents/AGENT_*.md")
    parser.add_argument("--repo-root", default=None, help="Repository root; auto-detected by script location")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    return parser.parse_args()


def table_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    pattern = re.compile(r"^\|\s*\*\*([A-Z_]+)\*\*\s*\|\s*(.*?)\s*\|\s*$", re.MULTILINE)
    for match in pattern.finditer(text):
        fields.setdefault(match.group(1), match.group(2).strip())
    return fields


def canonical_r_ids(standard_path: Path) -> set[str]:
    if not standard_path.is_file():
        raise FileNotFoundError(f"missing workflow-component standard: {standard_path}")
    return set(re.findall(r"^\|\s*(R\d+)\s*\|", standard_path.read_text(encoding="utf-8"), re.MULTILINE))


def add(findings: list[Finding], severity: str, code: str, path: Path, message: str) -> None:
    findings.append(Finding(severity, code, path.as_posix(), message))


def validate_file(path: Path, repo_root: Path, valid_r_ids: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    text = path.read_text(encoding="utf-8")
    rel = path.resolve().relative_to(repo_root.resolve())

    if not text.startswith("---\n"):
        add(findings, "ERROR", "FRONTMATTER_MISSING", rel, "file must begin with YAML frontmatter")
    else:
        closing = text.find("\n---\n", 4)
        if closing < 0:
            add(findings, "ERROR", "FRONTMATTER_UNCLOSED", rel, "YAML frontmatter has no closing delimiter")
        elif not re.search(r"^description:\s*.+$", text[4:closing], re.MULTILINE):
            add(findings, "ERROR", "DESCRIPTION_MISSING", rel, "frontmatter requires description")

    heading_match = re.search(r"^# AGENT INSTRUCTIONS — ([A-Z0-9_]+) \(.+\)$", text, re.MULTILINE)
    if not heading_match:
        add(findings, "ERROR", "HEADING_INVALID", rel, "canonical agent heading is missing or malformed")
        role = path.stem.removeprefix("AGENT_")
    else:
        role = heading_match.group(1)
        expected = path.stem.removeprefix("AGENT_")
        if role != expected:
            add(findings, "ERROR", "ROLE_FILENAME_MISMATCH", rel, f"heading role {role} does not match filename role {expected}")

    for marker in REQUIRED_MARKERS:
        if marker not in text:
            add(findings, "ERROR", "MARKER_MISSING", rel, f"missing required marker {marker}")

    body_type_match = re.search(r"^AGENT_TYPE:\s*([012])\s*$", text, re.MULTILINE)
    if not body_type_match:
        add(findings, "ERROR", "BODY_TYPE_MISSING", rel, "body AGENT_TYPE: 0|1|2 is missing")
        body_type = None
    else:
        body_type = body_type_match.group(1)

    fields = table_fields(text)
    for field in REQUIRED_FIELDS:
        if field not in fields:
            add(findings, "ERROR", "TYPE_FIELD_MISSING", rel, f"Agent Type table missing {field}")

    table_type_match = re.match(r"TYPE\s+([012])\b", fields.get("AGENT_TYPE", ""))
    table_type = table_type_match.group(1) if table_type_match else None
    if body_type and table_type != body_type:
        add(findings, "ERROR", "TYPE_MISMATCH", rel, "body and table AGENT_TYPE values differ")

    agent_class = fields.get("AGENT_CLASS", "").split()[0].strip("*()")
    blocking = fields.get("BLOCKING", "").lower()
    if body_type == "1" and agent_class != "PERSONA":
        add(findings, "ERROR", "TYPE1_CLASS", rel, "Type 1 agents must declare PERSONA")
    if body_type == "2":
        if agent_class != "TASK":
            add(findings, "ERROR", "TYPE2_CLASS", rel, "Type 2 agents must declare TASK")
        if not blocking.startswith("never"):
            add(findings, "ERROR", "TYPE2_BLOCKING", rel, "Type 2 agents must be non-blocking")
        if role != "TASK":
            approval_match = re.search(
                r"^dedicated_agent2_approval:\s*(D-GOV-\d+)\s*$",
                frontmatter_block(text),
                re.MULTILINE,
            )
            if not approval_match:
                add(findings, "WARN", "TYPE2_REQUALIFICATION_REQUIRED", rel, "D-GOV-11 requires evidence and human approval for each dedicated Agent 2 package")
            else:
                approval_ref = approval_match.group(1)
                decision_matches = sorted(
                    (repo_root / "docs" / "governance_harness" / "_DECISIONS").glob(
                        f"{approval_ref}_*.md"
                    )
                )
                if len(decision_matches) != 1:
                    add(findings, "ERROR", "TYPE2_APPROVAL_UNRESOLVED", rel, f"{approval_ref} must resolve to exactly one decision record")
                else:
                    decision_text = decision_matches[0].read_text(encoding="utf-8")
                    if not re.search(r"^Status:\s+RULED\s*$", decision_text, re.MULTILINE):
                        add(findings, "ERROR", "TYPE2_APPROVAL_NOT_RULED", rel, f"{approval_ref} is not RULED")
                    if not re.search(rf"^\|\s*{re.escape(role)}\s*\|", decision_text, re.MULTILINE):
                        add(findings, "ERROR", "TYPE2_APPROVAL_ROLE_MISSING", rel, f"{approval_ref} does not approve role {role}")

    write_scope = fields.get("WRITE_SCOPE", "")
    if write_scope and not write_scope.startswith(WRITE_SCOPE_PREFIXES):
        add(findings, "ERROR", "WRITE_SCOPE_INVALID", rel, f"unrecognized write-scope prefix: {write_scope}")
    if role.startswith("AUDIT_") and "_Evaluation/" not in write_scope:
        add(
            findings,
            "ERROR",
            "AUDIT_OUTPUT_ROOT_INVALID",
            rel,
            "current generic audit specialists must write under _Evaluation/; _Reconciliation/ audit paths are historical only",
        )

    for ref in sorted(set(re.findall(r"\b(AGENT_[A-Z0-9_]+\.md)\b", text))):
        if not (repo_root / "agents" / ref).is_file():
            add(findings, "WARN", "AGENT_REFERENCE_UNRESOLVED", rel, f"referenced live agent file does not exist: {ref}")

    # R0 is a local research-grade token. Every positive R identifier is
    # otherwise checked against the loaded workflow-standard catalog.
    for rid in sorted(set(re.findall(r"\bR\d+\b", text)) - {"R0"}):
        if rid not in valid_r_ids:
            add(findings, "WARN", "R_ID_UNKNOWN", rel, f"requirement identifier is not defined by the standard: {rid}")

    return findings


def frontmatter_block(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    closing = text.find("\n---\n", 4)
    return "" if closing < 0 else text[4:closing]


def frontmatter_list(text: str, key: str) -> list[str]:
    match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", frontmatter_block(text), re.MULTILINE)
    if not match or not match.group(1).strip():
        return []
    value = match.group(1).strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [item.strip().strip("'\"") for item in value.split(",") if item.strip()]


def validate_hierarchy(paths: list[Path], repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    records: dict[str, tuple[Path, str, str, dict[str, str]]] = {}
    for path in paths:
        text = path.read_text(encoding="utf-8")
        type_match = re.search(r"^AGENT_TYPE:\s*([012])\s*$", text, re.MULTILINE)
        if not type_match:
            continue
        records[path.stem.removeprefix("AGENT_")] = (
            path,
            text,
            type_match.group(1),
            table_fields(text),
        )

    type_zero = sorted(role for role, (_, _, agent_type, _) in records.items() if agent_type == "0")
    suite_path = Path("agents")
    if type_zero != ["HELP_HUMAN"]:
        add(
            findings,
            "ERROR",
            "AGENT0_ROSTER_INVALID",
            suite_path,
            f"exactly HELP_HUMAN must be Agent 0; found {', '.join(type_zero) or 'none'}",
        )

    for role, (path, text, agent_type, fields) in records.items():
        rel = path.resolve().relative_to(repo_root.resolve())
        subagents = frontmatter_list(text, "subagents")
        if agent_type == "2" and subagents:
            add(findings, "ERROR", "TYPE2_DELEGATION_DECLARED", rel, "Agent 2 may not declare subagents")
        for child in subagents:
            child_record = records.get(child)
            if not child_record:
                add(findings, "ERROR", "SUBAGENT_ROLE_UNRESOLVED", rel, f"subagent role does not exist: {child}")
                continue
            child_type = child_record[2]
            if agent_type == "0" and child_type != "1":
                add(findings, "ERROR", "AGENT0_CHILD_TYPE", rel, f"Agent 0 child {child} must be Agent 1")
            if agent_type == "1" and child_type != "2":
                add(findings, "ERROR", "AGENT1_CHILD_TYPE", rel, f"Agent 1 child {child} must be Agent 2")
        allows_generalist = re.search(
            r"^allow_generalist_agent2:\s*true\s*$",
            frontmatter_block(text),
            re.MULTILINE,
        )
        if allows_generalist and agent_type != "1":
            add(findings, "ERROR", "GENERALIST_PARENT_TYPE", rel, "only Agent 1 may allow ephemeral generalist Agent 2 children")
        interaction = fields.get("INTERACTION_SURFACE", "").lower()
        if agent_type == "1" and not (interaction.startswith("chat") or interaction.startswith("both")):
            add(findings, "ERROR", "AGENT1_DIRECT_ENTRY", rel, "Agent 1 must support direct human invocation")
        if agent_type == "2" and (interaction.startswith("chat") or interaction.startswith("both")):
            add(findings, "ERROR", "TYPE2_DIRECT_ENTRY", rel, "Agent 2 may not be a direct-chat persona")

    for parent, required_children in REQUIRED_DELEGATION_EDGES.items():
        parent_record = records.get(parent)
        if not parent_record:
            continue
        parent_path, parent_text, _, _ = parent_record
        declared = set(frontmatter_list(parent_text, "subagents"))
        for child in sorted(required_children - declared):
            rel = parent_path.resolve().relative_to(repo_root.resolve())
            add(
                findings,
                "ERROR",
                "REQUIRED_DELEGATION_EDGE_MISSING",
                rel,
                f"canonical dispatch relationship {parent} -> {child} is not declared in subagents",
            )

    return findings


def resolve_paths(args: argparse.Namespace, repo_root: Path) -> list[Path]:
    if args.paths:
        paths = [(repo_root / item).resolve() if not Path(item).is_absolute() else Path(item).resolve() for item in args.paths]
    else:
        paths = sorted((repo_root / "agents").glob("AGENT_*.md"))
    for path in paths:
        try:
            path.relative_to(repo_root.resolve())
        except ValueError as exc:
            raise ValueError(f"path outside repository: {path}") from exc
        if not path.is_file():
            raise FileNotFoundError(f"agent file not found: {path}")
    return paths


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[2]
    try:
        valid_r_ids = canonical_r_ids(repo_root / "docs" / "WORKFLOW_COMPONENT_STANDARD.md")
        paths = resolve_paths(args, repo_root)
        findings = [finding for path in paths for finding in validate_file(path, repo_root, valid_r_ids)]
        roster_paths = sorted((repo_root / "agents").glob("AGENT_*.md"))
        findings.extend(validate_hierarchy(roster_paths, repo_root))
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    error_count = sum(item.severity == "ERROR" for item in findings)
    warn_count = sum(item.severity == "WARN" for item in findings)
    if args.json:
        print(json.dumps({"files_checked": len(paths), "errors": error_count, "warnings": warn_count, "findings": [asdict(item) for item in findings]}, indent=2))
    else:
        for item in findings:
            print(f"{item.severity:<5} {item.code:<34} {item.path}: {item.message}")
        print(f"\nSummary: {len(paths)} files, {error_count} errors, {warn_count} warnings")
    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
