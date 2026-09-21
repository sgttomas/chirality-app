"""Regression fixtures for exact CSV facts and explicit current-state/format checks."""
import csv
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from audit_common import schema, sow
from audit_dependencies import audit as dependencies
from audit_structure import audit as structure, current_state, CONTRACT


def row(**updates):
    result = {name: "" for name in schema.REQUIRED_COLUMNS}
    result.update(RegisterSchemaVersion="v3.1", DependencyID="DEP-001", FromPackageID="PKG-01", FromDeliverableID="DEL-01-01",
        DependencyClass="ANCHOR", AnchorType="IMPLEMENTS_NODE", Direction="UPSTREAM", DependencyType="OTHER", TargetType="WBS_NODE",
        Explicitness="EXPLICIT", SatisfactionStatus="TBD", Confidence="HIGH", Origin="DECLARED", Status="ACTIVE", EvidenceFile="source.md")
    result.update(updates)
    return result


def register(root, number, rows, header=None):
    path = root / f"PKG-01_A/1_Working/DEL-01-{number:02d}_Item/Dependencies.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=header or schema.REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    return path


def test_all_files_exact_anchor_multiline_and_final_enum(tmp_path):
    register(tmp_path, 1, [row(AnchorType="", Statement="IMPLEMENTS_NODE,\nquoted prose", EvidenceFile="proof, one.md")])
    register(tmp_path, 2, [row()])
    register(tmp_path, 3, [row(Direction="sideways")])
    result = dependencies(tmp_path)
    assert result["run_status"] == "COMPLETE"
    assert result["subject_status"] == "FAIL"
    assert result["summary"]["files"] == 3
    assert result["summary"]["rows"] == 3
    assert result["summary"]["evidence_populated"] == 3
    assert result["files"][0]["implements_node_rows"] == 0
    assert result["files"][2]["row_findings"]


def test_malformed_and_empty_denominators(tmp_path):
    path = register(tmp_path, 1, [row()])
    with path.open("a") as stream:
        stream.write("too,few\n")
    register(tmp_path, 2, []).write_text("")
    result = dependencies(tmp_path)
    assert result["summary"]["rows"] == 2
    assert result["summary"]["readable_rows"] == 1
    assert result["summary"]["malformed_rows"] == 1
    assert result["summary"]["evidence_coverage_percent"] == 50
    path.write_text(','.join(schema.REQUIRED_COLUMNS) + '\n"unterminated')
    result = dependencies(tmp_path)
    assert not result["summary"]["denominator_complete"]
    assert result["summary"]["evidence_coverage_percent"] is None


def test_exact_and_duplicate_header(tmp_path):
    path = register(tmp_path, 1, [row()])
    path.write_text(path.read_text().replace("AnchorType", "AnchorTypeExtra"))
    result = dependencies(tmp_path)
    assert "AnchorType" in result["files"][0]["issues"][0]
    path.write_text(','.join(schema.REQUIRED_COLUMNS + ["Status"]) + '\n')
    assert not dependencies(tmp_path)["files"][0]["schema_valid"]


def make_workspace(root, state="RETIRED"):
    unit = register(root, 1, []).parent
    for name in ("_CONTEXT.md", "_DEPENDENCIES.md", "_REFERENCES.md"):
        (unit / name).touch()
    (unit / "_STATUS.md").write_text(f"# History\nOPEN happened before.\n\n**Current State:** `{state}`\n")
    for name in CONTRACT["partition_directories"]:
        (unit.parent.parent / name).mkdir(exist_ok=True)
    for name in CONTRACT["tool_roots"]:
        (root / name).mkdir(exist_ok=True)
    return unit


def test_retired_state_not_history_and_initialized_missing(tmp_path):
    unit = make_workspace(tmp_path)
    result = structure(tmp_path, "SOFTWARE")
    assert result["subject_status"] == "PASS"
    assert result["units"][0]["current_state"] == "RETIRED"
    (unit / "_STATUS.md").write_text("Current State: INITIALIZED\nHistory OPEN\n")
    result = structure(tmp_path, "SOFTWARE")
    assert result["run_status"] == "COMPLETE" and result["subject_status"] == "FAIL"
    assert result["summary"]["production_formats"] == {"INVALID": 1}


def test_legacy_and_dual_formats(tmp_path):
    unit = make_workspace(tmp_path, "INITIALIZED")
    for name in sow.LEGACY_FILES:
        (unit / name).touch()
    assert structure(tmp_path, "PROJECT")["units"][0]["production_format"]["state"] == "LEGACY_FOUR_DOC"
    # Use the actual canonical SOW schema, including matrix and authority marker.
    text = "---\nschema: chirality-deliverable-sow/v1\ndeliverable_id: DEL-01-01\npackage_id: PKG-01\ndecomposition_basis: source@abc\nproject_scope_refs: [S-1]\npackage_objective_refs: [O-1]\n---\n"
    for heading in sow.REQUIRED_HEADINGS:
        text += f"## {heading}\n"
        if heading == "Deliverable Definition — Ontology":
            text += "### OUT-001 — Output\n"
        if heading == "Completion and Reliance Basis — Epistemology":
            text += "### AC-001 — Acceptance\n"
        if heading == "Output and Evaluation Matrix":
            text += "| " + " | ".join(sow.MATRIX_COLUMNS) + " |\n| OUT-001 | S-1 | | AC-001 | HUMAN_REVIEW: owner | proof |\n"
    text += sow.migration_marker(sow.MIGRATION_AUTHORITY) + "\n"
    (unit / "ScopeOfWork.md").write_text(text)
    assert structure(tmp_path, "PROJECT")["units"][0]["production_format"]["state"] == "AMBIGUOUS"
    result = structure(tmp_path, "PROJECT", isolated_migration=True, migration_authority=sow.MIGRATION_AUTHORITY)
    assert result["units"][0]["production_format"]["state"] == "MIGRATION_DUAL"
    assert not result["units"][0]["production_format"]["accepted_baseline"]
    for name in sow.LEGACY_FILES:
        (unit / name).unlink()
    assert structure(tmp_path, "PROJECT")["units"][0]["production_format"]["state"] == "SOW_V1"


def test_explicit_inventory_includes_missing_and_domain(tmp_path):
    manifest = tmp_path / "inventory.json"
    manifest.write_text(json.dumps({"schema_version": 1, "units": [{"path": "CAT-01_A/1_Working/KTY-01-01_B", "required_files": ["Reference.md"]}]}))
    report = structure(tmp_path, "DOMAIN", manifest)
    assert report["summary"]["units"] == 1
    assert report["units"][0]["production_format"]["state"] == "NOT_APPLICABLE"
    assert "missing required file: Reference.md" in report["units"][0]["issues"]


def test_cli_arbitrary_cwd_and_source_protection(tmp_path):
    root = tmp_path / "workspace"
    root.mkdir()
    source = register(root, 1, [row(Direction="INVALID")])
    before = source.read_bytes()
    script = Path(__file__).with_name("audit_dependencies.py")
    output = tmp_path / "report.json"
    run = subprocess.run([sys.executable, str(script), "--root", str(root), "--output", str(output)], cwd="/", capture_output=True)
    assert run.returncode == 0
    assert json.loads(output.read_text())["subject_status"] == "FAIL"
    blocked = subprocess.run([sys.executable, str(script), "--root", str(root), "--output", str(source)], capture_output=True)
    assert blocked.returncode == 2 and source.read_bytes() == before
