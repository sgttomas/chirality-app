from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

import validate_domain_engine_profile as validator


def valid_profile() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "id": "open_pipe_stress",
        "name": "OpenPipeStress Piping-Stress Engine",
        "engine_type": "structural/piping-stress-analysis",
        "profile_version": "0.1",
        "profile_status": "DRAFT",
        "integration_level": "MANUAL_BRIDGE",
        "domain_root_patterns": ["projects/chirality-piping/**"],
        "authoritative_artifacts": ["projects/chirality-piping/core/**"],
        "chirality_readable_artifacts": ["<analysis_run record per schema>"],
        "protected_write_paths": ["projects/chirality-piping/core/**"],
        "agent_writable_paths": ["_DomainEngines/proposals/open_pipe_stress/**"],
        "deterministic_tools": [
            {
                "id": "operation_applier.validate",
                "mode": "proposal_validate",
                "requires_human_confirmation": False,
                "validate_result_schema": "TBD",
                "apply_result_schema": "TBD",
            }
        ],
        "operation_risk_class_axis": ["engine_checkable", "engine_silent"],
        "operation_proposal_contract": {
            "lifecycle": ["draft", "ready_for_review", "accepted", "rejected", "applied"],
            "risk_classes": ["engine_checkable", "engine_silent"],
            "deterministic_check_result_schema": "TBD",
            "accepted_or_applied_requires": [
                "human approval bound to git SHA per K-AUTH-2",
                "domain-engine-controlled apply or external terminal acceptance record",
            ],
        },
        "professional_boundary": {
            "agent_must_not_claim": [
                "code compliant for reliance",
                "professionally approved",
                "certified",
                "sealed",
            ]
        },
    }


def document(profile: dict[str, Any]) -> dict[str, Any]:
    return {"domain_profile": profile}


def delete_path(data: dict[str, Any], path: tuple[Any, ...]) -> None:
    current: Any = data
    for part in path[:-1]:
        current = current[part]
    del current[path[-1]]


def set_path(data: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    current: Any = data
    for part in path[:-1]:
        current = current[part]
    current[path[-1]] = value


def finding_fields(findings: list[validator.Finding]) -> set[str]:
    return {finding.field for finding in findings}


def test_valid_domain_engine_profile_passes() -> None:
    is_valid, findings, profile = validator.validate_profile_document(document(valid_profile()))

    assert is_valid is True
    assert findings == []
    assert profile["id"] == "open_pipe_stress"


REQUIRED_FIELD_CASES = [
    (("schema_version",), "domain_profile.schema_version"),
    (("id",), "domain_profile.id"),
    (("name",), "domain_profile.name"),
    (("engine_type",), "domain_profile.engine_type"),
    (("profile_version",), "domain_profile.profile_version"),
    (("domain_root_patterns",), "domain_profile.domain_root_patterns"),
    (("authoritative_artifacts",), "domain_profile.authoritative_artifacts"),
    (("chirality_readable_artifacts",), "domain_profile.chirality_readable_artifacts"),
    (("protected_write_paths",), "domain_profile.protected_write_paths"),
    (("agent_writable_paths",), "domain_profile.agent_writable_paths"),
    (("deterministic_tools",), "domain_profile.deterministic_tools"),
    (("deterministic_tools", 0, "id"), "domain_profile.deterministic_tools[0].id"),
    (("deterministic_tools", 0, "mode"), "domain_profile.deterministic_tools[0].mode"),
    (
        ("deterministic_tools", 0, "requires_human_confirmation"),
        "domain_profile.deterministic_tools[0].requires_human_confirmation",
    ),
    (
        ("deterministic_tools", 0, "validate_result_schema"),
        "domain_profile.deterministic_tools[0].validate_result_schema",
    ),
    (
        ("deterministic_tools", 0, "apply_result_schema"),
        "domain_profile.deterministic_tools[0].apply_result_schema",
    ),
    (("operation_proposal_contract",), "domain_profile.operation_proposal_contract"),
    (
        ("operation_proposal_contract", "lifecycle"),
        "domain_profile.operation_proposal_contract.lifecycle",
    ),
    (
        ("operation_proposal_contract", "risk_classes"),
        "domain_profile.operation_proposal_contract.risk_classes",
    ),
    (
        ("operation_proposal_contract", "deterministic_check_result_schema"),
        "domain_profile.operation_proposal_contract.deterministic_check_result_schema",
    ),
    (
        ("operation_proposal_contract", "accepted_or_applied_requires"),
        "domain_profile.operation_proposal_contract.accepted_or_applied_requires",
    ),
    (("professional_boundary",), "domain_profile.professional_boundary"),
    (
        ("professional_boundary", "agent_must_not_claim"),
        "domain_profile.professional_boundary.agent_must_not_claim",
    ),
]


def test_missing_domain_profile_root_is_invalid() -> None:
    is_valid, findings, _profile = validator.validate_profile_document(valid_profile())

    assert is_valid is False
    assert "domain_profile" in finding_fields(findings)


def test_each_required_field_missing_case_is_invalid() -> None:
    for field_path, expected_field in REQUIRED_FIELD_CASES:
        profile = valid_profile()
        delete_path(profile, field_path)

        is_valid, findings, _profile = validator.validate_profile_document(document(profile))

        assert is_valid is False, field_path
        assert expected_field in finding_fields(findings), field_path


ENUM_VIOLATION_CASES = [
    (("profile_status",), "READY", "domain_profile.profile_status"),
    (("integration_level",), "LIVE_WRITE", "domain_profile.integration_level"),
    (("deterministic_tools", 0, "mode"), "write_direct", "domain_profile.deterministic_tools[0].mode"),
    (("operation_risk_class_axis", 0), "human_judgment", "domain_profile.operation_risk_class_axis[0]"),
    (
        ("operation_proposal_contract", "risk_classes", 0),
        "human_judgment",
        "domain_profile.operation_proposal_contract.risk_classes[0]",
    ),
    (
        ("operation_proposal_contract", "lifecycle", 0),
        "done",
        "domain_profile.operation_proposal_contract.lifecycle[0]",
    ),
]


def test_each_enum_violation_case_is_invalid() -> None:
    for field_path, bad_value, expected_field in ENUM_VIOLATION_CASES:
        profile = valid_profile()
        set_path(profile, field_path, bad_value)

        is_valid, findings, _profile = validator.validate_profile_document(document(profile))

        assert is_valid is False, field_path
        assert expected_field in finding_fields(findings), field_path
        assert any(finding.code == "INVALID_ENUM" for finding in findings), field_path


def test_operation_risk_class_optional_enum_is_checked_when_present() -> None:
    profile = valid_profile()
    profile["operation_risk_class"] = "human_judgment"

    is_valid, findings, _profile = validator.validate_profile_document(document(profile))

    assert is_valid is False
    assert "domain_profile.operation_risk_class" in finding_fields(findings)


def test_cli_writes_report_under_domain_engines(tmp_path: Path) -> None:
    repo_root = tmp_path
    profile_path = repo_root / "_DomainEngines/profiles/test_profile.yaml"
    report_path = repo_root / "_DomainEngines/profiles/_validation/test_profile.validation.json"
    profile_path.parent.mkdir(parents=True)
    profile_path.write_text(yaml.safe_dump(document(valid_profile()), sort_keys=False), encoding="utf-8")

    exit_code = validator.main(
        [
            str(profile_path),
            "--repo-root",
            str(repo_root),
            "--output-report",
            str(report_path),
        ]
    )

    assert exit_code == 0
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["valid"] is True
    assert report["result"] == "VALID"
    assert report["findings"] == []


def test_cli_rejects_report_outside_domain_engines(tmp_path: Path) -> None:
    repo_root = tmp_path
    profile_path = repo_root / "_DomainEngines/profiles/test_profile.yaml"
    report_path = repo_root / "reports/test_profile.validation.json"
    profile_path.parent.mkdir(parents=True)
    profile_path.write_text(yaml.safe_dump(document(valid_profile()), sort_keys=False), encoding="utf-8")

    exit_code = validator.main(
        [
            str(profile_path),
            "--repo-root",
            str(repo_root),
            "--output-report",
            str(report_path),
        ]
    )

    assert exit_code == 2
    assert not report_path.exists()


def test_report_for_invalid_profile_contains_per_field_findings() -> None:
    profile = deepcopy(valid_profile())
    delete_path(profile, ("operation_proposal_contract",))
    is_valid, findings, returned_profile = validator.validate_profile_document(document(profile))

    report = validator.make_report(Path("_DomainEngines/profiles/test.yaml"), is_valid, findings, returned_profile)

    assert report["valid"] is False
    assert report["summary"]["error_count"] == 1
    assert report["findings"][0]["field"] == "domain_profile.operation_proposal_contract"
