#!/usr/bin/env python3
"""Validate a DomainEngineProfile YAML against the canonical contract.

Purpose:
  Deterministically validate a DomainEngineProfile YAML for required fields,
  enum membership, path-taxonomy shape, deterministic tool declarations,
  operation proposal contract shape, and professional-boundary structure.

Usage:
  python3 tools/validation/validate_domain_engine_profile.py \
    _DomainEngines/profiles/open_pipe_stress.yaml \
    --output-report _DomainEngines/profiles/_validation/open_pipe_stress.validation.json

Inputs:
  profile_yaml:
    YAML file whose canonical root key is domain_profile.
  --output-report:
    JSON report path. The resolved path must be under <repo-root>/_DomainEngines/.
  --repo-root:
    Repository root used to resolve relative input/output paths. Defaults to cwd.

Outputs:
  Writes a machine-readable JSON report to --output-report. The report contains
  one finding object per invalid field. The tool never mutates the input profile.

Exit codes:
  0 = profile is schema-valid
  1 = profile is schema-invalid and report was written
  2 = CLI, filesystem, YAML parse, or report-write failure

Idempotence:
  Given the same profile and output path, the report is overwritten with the same
  deterministic content. No timestamps or hidden state are written.

Scope boundary:
  The only write is --output-report, and it must resolve under _DomainEngines/.
  This tool never marks a profile VALIDATED or ADOPTED.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - exercised only in missing dependency environments.
    yaml = None  # type: ignore[assignment]


CONTRACT_SOURCE = "agents/AGENT_DOMAIN_ENGINE.md@77a327727"
REPORT_SCHEMA = "domain-engine-profile-validation/v1"
TOOL_NAME = "validate_domain_engine_profile"

ASCII_TOKEN_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")

REQUIRED_STRING_FIELDS = (
    "schema_version",
    "id",
    "name",
    "engine_type",
    "profile_version",
)

REQUIRED_LIST_FIELDS = (
    "domain_root_patterns",
    "authoritative_artifacts",
    "chirality_readable_artifacts",
    "protected_write_paths",
    "agent_writable_paths",
)

REQUIRED_DETERMINISTIC_TOOL_FIELDS = (
    "id",
    "mode",
    "requires_human_confirmation",
    "validate_result_schema",
    "apply_result_schema",
)

REQUIRED_OPERATION_CONTRACT_FIELDS = (
    "lifecycle",
    "risk_classes",
    "deterministic_check_result_schema",
    "accepted_or_applied_requires",
)

PROFILE_STATUS_VALUES = {
    "NONE",
    "DRAFT",
    "VALIDATED",
    "ADOPTED",
    "STALE",
    "INVALID",
    "UNKNOWN",
}

INTEGRATION_LEVEL_VALUES = {
    "MANUAL_BRIDGE",
    "READ_ONLY",
    "DOMAIN_CONTROLLED_WRITE",
    "OPERATION_PROPOSAL",
    "EXTERNAL_RESULT_STATE",
}

TOOL_MODE_VALUES = {
    "read_only",
    "summary_write",
    "domain_controlled_write",
    "proposal_validate",
    "proposal_apply",
}

OPERATION_RISK_CLASS_VALUES = {
    "engine_checkable",
    "engine_silent",
}

OPERATION_LIFECYCLE_VALUES = (
    "draft",
    "ready_for_review",
    "accepted",
    "rejected",
    "applied",
)


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    field: str
    message: str
    expected: Any | None = None
    actual: Any | None = None


def add_finding(
    findings: list[Finding],
    code: str,
    field: str,
    message: str,
    *,
    expected: Any | None = None,
    actual: Any | None = None,
) -> None:
    findings.append(
        Finding(
            severity="error",
            code=code,
            field=field,
            message=message,
            expected=expected,
            actual=actual,
        )
    )


def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def display_value(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return "<mapping>"
    return f"<{type(value).__name__}>"


def require_mapping(data: dict[str, Any], key: str, path: str, findings: list[Finding]) -> dict[str, Any] | None:
    field = f"{path}.{key}"
    if key not in data:
        add_finding(findings, "REQUIRED_FIELD_MISSING", field, f"Required field missing: {field}")
        return None
    value = data[key]
    if not isinstance(value, dict):
        add_finding(
            findings,
            "TYPE_ERROR",
            field,
            f"{field} must be a mapping",
            expected="mapping",
            actual=display_value(value),
        )
        return None
    return value


def require_nonempty_string(data: dict[str, Any], key: str, path: str, findings: list[Finding]) -> str | None:
    field = f"{path}.{key}"
    if key not in data:
        add_finding(findings, "REQUIRED_FIELD_MISSING", field, f"Required field missing: {field}")
        return None
    value = data[key]
    if not isinstance(value, str):
        add_finding(
            findings,
            "TYPE_ERROR",
            field,
            f"{field} must be a non-empty string",
            expected="non-empty string",
            actual=display_value(value),
        )
        return None
    if not value.strip():
        add_finding(findings, "EMPTY_VALUE", field, f"{field} must not be empty")
        return None
    return value


def require_bool(data: dict[str, Any], key: str, path: str, findings: list[Finding]) -> bool | None:
    field = f"{path}.{key}"
    if key not in data:
        add_finding(findings, "REQUIRED_FIELD_MISSING", field, f"Required field missing: {field}")
        return None
    value = data[key]
    if not isinstance(value, bool):
        add_finding(
            findings,
            "TYPE_ERROR",
            field,
            f"{field} must be a boolean",
            expected="boolean",
            actual=display_value(value),
        )
        return None
    return value


def require_nonempty_string_list(
    data: dict[str, Any],
    key: str,
    path: str,
    findings: list[Finding],
) -> list[str] | None:
    field = f"{path}.{key}"
    if key not in data:
        add_finding(findings, "REQUIRED_FIELD_MISSING", field, f"Required field missing: {field}")
        return None
    value = data[key]
    if not isinstance(value, list):
        add_finding(
            findings,
            "TYPE_ERROR",
            field,
            f"{field} must be a non-empty list of strings",
            expected="non-empty list[string]",
            actual=display_value(value),
        )
        return None
    if not value:
        add_finding(findings, "EMPTY_VALUE", field, f"{field} must contain at least one entry")
        return None
    for index, item in enumerate(value):
        item_field = f"{field}[{index}]"
        if not isinstance(item, str):
            add_finding(
                findings,
                "TYPE_ERROR",
                item_field,
                f"{item_field} must be a string",
                expected="string",
                actual=display_value(item),
            )
        elif not item.strip():
            add_finding(findings, "EMPTY_VALUE", item_field, f"{item_field} must not be empty")
    return value if all(isinstance(item, str) for item in value) else None


def validate_ascii_token(value: str | None, field: str, findings: list[Finding]) -> None:
    if value is None:
        return
    if not ASCII_TOKEN_RE.fullmatch(value):
        add_finding(
            findings,
            "INVALID_ID",
            field,
            f"{field} must be a stable ASCII token",
            expected=ASCII_TOKEN_RE.pattern,
            actual=value,
        )


def validate_enum(
    data: dict[str, Any],
    key: str,
    path: str,
    allowed: set[str],
    findings: list[Finding],
    *,
    required: bool,
) -> None:
    field = f"{path}.{key}"
    if key not in data:
        if required:
            add_finding(findings, "REQUIRED_FIELD_MISSING", field, f"Required field missing: {field}")
        return
    value = data[key]
    if not isinstance(value, str):
        add_finding(
            findings,
            "TYPE_ERROR",
            field,
            f"{field} must be a string enum",
            expected=sorted(allowed),
            actual=display_value(value),
        )
        return
    if value not in allowed:
        add_finding(
            findings,
            "INVALID_ENUM",
            field,
            f"{field} has invalid enum value {value!r}",
            expected=sorted(allowed),
            actual=value,
        )


def validate_schema_ref(data: dict[str, Any], key: str, path: str, findings: list[Finding]) -> None:
    value = require_nonempty_string(data, key, path, findings)
    if value is None:
        return
    if value != "TBD" and not value.strip():
        add_finding(
            findings,
            "INVALID_SCHEMA_REF",
            f"{path}.{key}",
            f"{path}.{key} must be a schema reference or TBD",
            expected="schema reference string or TBD",
            actual=value,
        )


def validate_exact_enum_list(
    data: dict[str, Any],
    key: str,
    path: str,
    expected_values: tuple[str, ...],
    findings: list[Finding],
) -> None:
    values = require_nonempty_string_list(data, key, path, findings)
    if values is None:
        return

    expected_set = set(expected_values)
    field = f"{path}.{key}"
    for index, value in enumerate(values):
        item_field = f"{field}[{index}]"
        if isinstance(value, str) and value not in expected_set:
            add_finding(
                findings,
                "INVALID_ENUM",
                item_field,
                f"{item_field} has invalid enum value {value!r}",
                expected=list(expected_values),
                actual=value,
            )

    if tuple(values) != expected_values:
        add_finding(
            findings,
            "CONTRACT_MISMATCH",
            field,
            f"{field} must match the canonical contract values in order",
            expected=list(expected_values),
            actual=values,
        )


def validate_risk_class_list(
    data: dict[str, Any],
    key: str,
    path: str,
    findings: list[Finding],
    *,
    exact_contract: bool,
) -> None:
    values = require_nonempty_string_list(data, key, path, findings)
    if values is None:
        return

    field = f"{path}.{key}"
    for index, value in enumerate(values):
        item_field = f"{field}[{index}]"
        if value not in OPERATION_RISK_CLASS_VALUES:
            add_finding(
                findings,
                "INVALID_ENUM",
                item_field,
                f"{item_field} has invalid enum value {value!r}",
                expected=sorted(OPERATION_RISK_CLASS_VALUES),
                actual=value,
            )

    if exact_contract and tuple(values) != tuple(sorted(OPERATION_RISK_CLASS_VALUES)):
        add_finding(
            findings,
            "CONTRACT_MISMATCH",
            field,
            f"{field} must match the canonical risk-class contract values",
            expected=sorted(OPERATION_RISK_CLASS_VALUES),
            actual=values,
        )


def validate_deterministic_tools(profile: dict[str, Any], path: str, findings: list[Finding]) -> None:
    field = f"{path}.deterministic_tools"
    if "deterministic_tools" not in profile:
        add_finding(findings, "REQUIRED_FIELD_MISSING", field, f"Required field missing: {field}")
        return

    tools = profile["deterministic_tools"]
    if not isinstance(tools, list):
        add_finding(
            findings,
            "TYPE_ERROR",
            field,
            f"{field} must be a non-empty list of mappings",
            expected="non-empty list[mapping]",
            actual=display_value(tools),
        )
        return
    if not tools:
        add_finding(findings, "EMPTY_VALUE", field, f"{field} must contain at least one tool declaration")
        return

    for index, tool in enumerate(tools):
        tool_path = f"{field}[{index}]"
        if not isinstance(tool, dict):
            add_finding(
                findings,
                "TYPE_ERROR",
                tool_path,
                f"{tool_path} must be a mapping",
                expected="mapping",
                actual=display_value(tool),
            )
            continue

        tool_id = require_nonempty_string(tool, "id", tool_path, findings)
        validate_ascii_token(tool_id, f"{tool_path}.id", findings)
        validate_enum(tool, "mode", tool_path, TOOL_MODE_VALUES, findings, required=True)
        require_bool(tool, "requires_human_confirmation", tool_path, findings)
        validate_schema_ref(tool, "validate_result_schema", tool_path, findings)
        validate_schema_ref(tool, "apply_result_schema", tool_path, findings)


def validate_operation_contract(profile: dict[str, Any], path: str, findings: list[Finding]) -> None:
    contract = require_mapping(profile, "operation_proposal_contract", path, findings)
    if contract is None:
        return

    contract_path = f"{path}.operation_proposal_contract"
    validate_exact_enum_list(contract, "lifecycle", contract_path, OPERATION_LIFECYCLE_VALUES, findings)
    validate_risk_class_list(contract, "risk_classes", contract_path, findings, exact_contract=True)
    validate_schema_ref(contract, "deterministic_check_result_schema", contract_path, findings)
    require_nonempty_string_list(contract, "accepted_or_applied_requires", contract_path, findings)


def validate_professional_boundary(profile: dict[str, Any], path: str, findings: list[Finding]) -> None:
    boundary = require_mapping(profile, "professional_boundary", path, findings)
    if boundary is None:
        return
    require_nonempty_string_list(boundary, "agent_must_not_claim", f"{path}.professional_boundary", findings)


def extract_profile(document: Any) -> tuple[dict[str, Any], list[Finding]]:
    findings: list[Finding] = []
    if not isinstance(document, dict):
        add_finding(
            findings,
            "TYPE_ERROR",
            "domain_profile",
            "YAML root must be a mapping containing domain_profile",
            expected="mapping with domain_profile",
            actual=display_value(document),
        )
        return {}, findings

    if "domain_profile" not in document:
        add_finding(
            findings,
            "REQUIRED_FIELD_MISSING",
            "domain_profile",
            "Required root field missing: domain_profile",
        )
        return document, findings

    profile = document["domain_profile"]
    if not isinstance(profile, dict):
        add_finding(
            findings,
            "TYPE_ERROR",
            "domain_profile",
            "domain_profile must be a mapping",
            expected="mapping",
            actual=display_value(profile),
        )
        return {}, findings

    return profile, findings


def validate_profile_document(document: Any) -> tuple[bool, list[Finding], dict[str, Any]]:
    profile, findings = extract_profile(document)
    path = "domain_profile"

    for field in REQUIRED_STRING_FIELDS:
        value = require_nonempty_string(profile, field, path, findings)
        if field == "id":
            validate_ascii_token(value, f"{path}.{field}", findings)

    for field in REQUIRED_LIST_FIELDS:
        require_nonempty_string_list(profile, field, path, findings)

    validate_enum(profile, "profile_status", path, PROFILE_STATUS_VALUES, findings, required=False)
    validate_enum(profile, "integration_level", path, INTEGRATION_LEVEL_VALUES, findings, required=False)
    validate_enum(profile, "operation_risk_class", path, OPERATION_RISK_CLASS_VALUES, findings, required=False)

    if "operation_risk_class_axis" in profile:
        validate_risk_class_list(profile, "operation_risk_class_axis", path, findings, exact_contract=False)

    validate_deterministic_tools(profile, path, findings)
    validate_operation_contract(profile, path, findings)
    validate_professional_boundary(profile, path, findings)

    valid = not findings
    return valid, findings, profile


def load_yaml(path: Path) -> Any:
    if yaml is None:
        raise RuntimeError("PyYAML is required to parse profile YAML")
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:  # type: ignore[union-attr]
        raise ValueError(f"YAML parse error in {path}: {exc}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"Unable to decode {path} as UTF-8: {exc}") from exc


def make_report(profile_path: Path, valid: bool, findings: list[Finding], profile: dict[str, Any]) -> dict[str, Any]:
    finding_dicts = [asdict(finding) for finding in findings]
    return {
        "schema": REPORT_SCHEMA,
        "tool": TOOL_NAME,
        "contract_source": CONTRACT_SOURCE,
        "profile_path": profile_path.as_posix(),
        "profile_id": profile.get("id") if isinstance(profile, dict) else None,
        "profile_status": profile.get("profile_status") if isinstance(profile, dict) else None,
        "result": "VALID" if valid else "INVALID",
        "valid": valid,
        "summary": {
            "error_count": len(findings),
            "warning_count": 0,
        },
        "findings": finding_dicts,
    }


def resolve_repo_path(path_text: str, repo_root: Path) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def ensure_report_scope(report_path: Path, repo_root: Path) -> None:
    domain_root = (repo_root / "_DomainEngines").resolve()
    try:
        report_path.relative_to(domain_root)
    except ValueError as exc:
        raise ValueError(f"--output-report must resolve under {domain_root}: {report_path}") from exc


def write_report(report_path: Path, report: dict[str, Any]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a DomainEngineProfile YAML.")
    parser.add_argument("profile_yaml", help="DomainEngineProfile YAML path")
    parser.add_argument(
        "--output-report",
        required=True,
        help="JSON report path; must resolve under <repo-root>/_DomainEngines/",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root used to resolve relative paths (default: cwd)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    repo_root = Path(args.repo_root).resolve()
    profile_path = resolve_repo_path(args.profile_yaml, repo_root)
    report_path = resolve_repo_path(args.output_report, repo_root)

    if not repo_root.is_dir():
        print(f"ERROR: repo root is not a directory: {repo_root}", file=sys.stderr)
        return 2
    if not profile_path.is_file():
        print(f"ERROR: profile YAML not found: {profile_path}", file=sys.stderr)
        return 2
    try:
        ensure_report_scope(report_path, repo_root)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    try:
        document = load_yaml(profile_path)
        valid, findings, profile = validate_profile_document(document)
        report = make_report(profile_path, valid, findings, profile)
        write_report(report_path, report)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if valid:
        print(f"VALID: {profile_path}")
        print(f"Report: {report_path}")
        return 0

    print(f"INVALID: {profile_path} ({len(findings)} error(s))", file=sys.stderr)
    print(f"Report: {report_path}", file=sys.stderr)
    for finding in findings:
        print(f"  {finding.field}: {finding.message}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
