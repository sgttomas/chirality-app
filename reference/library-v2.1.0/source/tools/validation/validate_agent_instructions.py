#!/usr/bin/env python3
"""Validate the mechanically observable AGENT_*.md instruction contract.

Usage:
    python3 tools/validation/validate_agent_instructions.py
    python3 tools/validation/validate_agent_instructions.py agents/AGENT_TASK.md
    python3 tools/validation/validate_agent_instructions.py --json

Checks the canonical role registry (agents/registry.json): HELP_HUMAN,
HELPS_HUMANS, WORKING_ITEMS, TASK and the opt-in INTERLOCUTOR. It checks direct
entry and delegation eligibility, role capability configuration, and the four
ordered prose sections. A repository without the registry is an input failure; read
historical snapshots at their recorded revision with the validator of that
revision. Semantic role quality remains a judgment review.

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


# Canonical roles and their agent types. INTERLOCUTOR is the opt-in Type 2
# advisor to Agent 0; it is delegated, never entered directly.
CANONICAL_ROLES = (
    ('HELP_HUMAN', 0),
    ('HELPS_HUMANS', 1),
    ('WORKING_ITEMS', 1),
    ('TASK', 2),
    ('INTERLOCUTOR', 2),
)
# Required child eligibility by parent type. Agent 0 responsibilities can be
# held through any direct-entry role, so each may delegate INTERLOCUTOR.
CHILDREN = {
    0: ('HELPS_HUMANS', 'WORKING_ITEMS', 'TASK', 'INTERLOCUTOR'),
    1: ('TASK', 'INTERLOCUTOR'),
    2: (),
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


def add(findings: list[Finding], severity: str, code: str, path: Path, message: str) -> None:
    findings.append(Finding(severity, code, path.as_posix(), message))


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


def validate_registry(repo_root: Path) -> list[Finding]:
    findings = []
    path = repo_root / 'agents/registry.json'
    registry = json.loads(path.read_text())
    if not isinstance(registry, dict) or not isinstance(registry.get('roles'), dict):
        raise ValueError('registry and roles must be mappings')
    roles = registry['roles']
    expected = dict(CANONICAL_ROLES)
    def error(code, message):
        add(findings, 'ERROR', code, path.relative_to(repo_root), message)
    if registry.get('schema_version') != 1 or set(roles) != set(expected):
        error('ROLE_REGISTRY', f'schema_version 1 and exactly the canonical roles required: {", ".join(expected)}')
    catalog = registry.get('workflow_catalog')
    if not isinstance(catalog, dict) or set(catalog) != {'schema','catalog','index'}:
        error('WORKFLOW_CATALOG_REF', 'workflow_catalog must contain stable schema, catalog, and index references')
    elif catalog.get('schema') != 'chirality-method-index/v1' or catalog.get('catalog') != 'workflows/catalog.yaml' or catalog.get('index') != 'workflows/index.json':
        error('WORKFLOW_CATALOG_REF', 'workflow_catalog references do not match the Root catalog contract')
    for name, config in roles.items():
        if not isinstance(config, dict):
            error('ROLE_SHAPE', f'{name}: role configuration must be a mapping')
            continue
        typ = expected.get(name)
        if type(config.get('type')) is not int or config.get('type') != typ or config.get('direct_entry') is not (typ in (0, 1)):
            error('ROLE_ENTRY', f'{name}: invalid type or direct entry')
        if not isinstance(config.get('description'), str) or not config['description'].strip():
            error('ROLE_DESCRIPTOR', f'{name}: non-empty description required')
        if config.get('default_for_new_chat') is not (name == 'HELP_HUMAN'):
            error('ROLE_DESCRIPTOR', f'{name}: invalid default_for_new_chat')
        child_list = config.get('delegates_to', [])
        if not isinstance(child_list, list) or any(not isinstance(x, str) for x in child_list):
            error('ROLE_SHAPE', f'{name}: delegates_to must be a string list')
            child_list = []
        children = set(child_list)
        required = set(CHILDREN.get(typ, ()))
        if children != required or config.get('allow_generalist_agent2') is not (typ in (0, 1)):
            error('ROLE_DELEGATION', f'{name}: invalid child eligibility')
        if not isinstance(config.get('tools'), list) or any(not isinstance(x,str) for x in config.get('tools', [])) or not isinstance(config.get('write_scope'), str):
            error('ROLE_POLICY', f'{name}: tools and write_scope required')
            continue
        if typ == 2 and ('delegate_agent' in (config.get('tools') or []) or config.get('allow_generalist_agent2')):
            error('TYPE2_DELEGATION', f'{name}: Type 2 roles cannot delegate')
        instruction = repo_root / str(config.get('instruction', ''))
        if not instruction.resolve().is_relative_to((repo_root/'agents').resolve()) or not instruction.is_file():
            error('ROLE_INSTRUCTION', f'{name}: missing or escaping instruction path')
            continue
        if instruction.name != f'AGENT_{name}.md':
            error('ROLE_INSTRUCTION', f'{name}: instruction name mismatch')
        text = instruction.read_text()
        headings = re.findall(r'^## (.+)$', text, re.MULTILINE)
        if headings != ['PROTOCOL', 'SPEC', 'STRUCTURE', 'RATIONALE']:
            error('ROLE_SECTIONS', f'{name}: requires exactly four ordered sections')
        if text.startswith('---') or 'AGENT_TYPE' in text or '[[BEGIN:' in text:
            error('ROLE_PROSE_METADATA', f'{name}: obsolete instruction envelope')
    actual = {p.name for p in (repo_root/'agents').glob('AGENT_*.md')}
    if actual != {f'AGENT_{name}.md' for name in expected}:
        error('ROLE_ROSTER', 'live instruction files differ from registry')
    return findings


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[2]
    try:
        paths = resolve_paths(args, repo_root)
        if not (repo_root / 'agents/registry.json').is_file():
            raise FileNotFoundError(f"agent registry not found: {repo_root / 'agents/registry.json'}")
        findings = validate_registry(repo_root)
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
