from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

from common import load_catalog  # noqa: E402
from check_boundary_owner_resolution import check_document  # noqa: E402
MIGRATION_AUTHORITY = "D-GOV-16@7584718aa32b112e415331736d1a8e68c12ac176"
ISSUED_ACCEPTED_BASIS = "execution/_Decomposition/SOFTWARE_DECOMP.md@abc123"
CONVERT = HERE / "convert_four_documents_to_scope_of_work.py"
VALIDATE = HERE / "validate_scope_of_work.py"
RENDER = HERE / "render_scope_of_work.py"
MAP = HERE / "map_scope_of_work_claims.py"
PARITY = HERE / "report_scope_of_work_parity.py"
CHECKLIST = HERE / "derive_review_checklist.py"
FINALIZE = HERE / "finalize_scope_of_work.py"


def run(tool: Path, *args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(tool), *(str(arg) for arg in args)], text=True, capture_output=True)


def fixture(tmp_path: Path, state: str = "IN_PROGRESS") -> Path:
    deliverable = tmp_path / "PKG-07" / "DEL-07-03_Test"
    deliverable.mkdir(parents=True)
    sources = {
        "Datasheet.md": "# Datasheet\n\n## Identification\n\nA bounded output.\n",
        "Specification.md": "# Specification\n\n## Requirements\n\nThe output shall be traceable.\n",
        "Procedure.md": "# Procedure\n\n## Verification\n\nRun the parity check.\n",
        "Guidance.md": "# Guidance\n\n## Principles\n\nPrefer source fidelity.\n",
    }
    for name, text in sources.items():
        (deliverable / name).write_text(text, encoding="utf-8")
    (deliverable / "_STATUS.md").write_text(f"# Status\n\n**Current State:** {state}\n\n## Remaining\n", encoding="utf-8")
    return deliverable


def convert(deliverable: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return run(
        CONVERT,
        "--deliverable", deliverable,
        "--deliverable-id", "DEL-07-03",
        "--package-id", "PKG-07",
        "--decomposition-basis", "execution/_Decomposition/SOFTWARE_DECOMP.md@abc123",
        "--project-scope-ref", "SOW-001",
        "--package-objective-ref", "OBJ-007",
        "--output-description", "A traceable deliverable contract.",
        "--acceptance-criterion", "The mapped source content is complete and internally resolvable.",
        "--verification-method", "Run the deterministic claim map and parity report.",
        *extra,
    )


def test_converter_requires_isolated_authority_and_preserves_lifecycle(tmp_path: Path) -> None:
    deliverable = fixture(tmp_path)
    status_before = hashlib.sha256((deliverable / "_STATUS.md").read_bytes()).hexdigest()
    denied = convert(deliverable)
    assert denied.returncode == 1
    assert "isolated-migration" in denied.stderr
    assert not (deliverable / "ScopeOfWork.md").exists()

    result = convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY)
    assert result.returncode == 0, result.stderr
    assert hashlib.sha256((deliverable / "_STATUS.md").read_bytes()).hexdigest() == status_before
    for name in ("Datasheet.md", "Specification.md", "Procedure.md", "Guidance.md"):
        assert (deliverable / name).is_file()


def issued_binding_args(deliverable: Path) -> list[str]:
    args = [
        "--issued-source-commit", "7654321",
        "--issued-status-sha256", hashlib.sha256((deliverable / "_STATUS.md").read_bytes()).hexdigest(),
    ]
    for name in ("Datasheet.md", "Specification.md", "Procedure.md", "Guidance.md"):
        digest = hashlib.sha256((deliverable / name).read_bytes()).hexdigest()
        args.extend(["--issued-source-sha256", f"{name}={digest}"])
    return args


def test_converter_rejects_unruled_migration_authorities(tmp_path: Path) -> None:
    for index, authority in enumerate(
        ("D-GOV-16@0123456", "D-GOV-16@" + "a" * 40, "D-GOV-16:malformed")
    ):
        deliverable = fixture(tmp_path / str(index))
        result = convert(deliverable, "--isolated-migration", "--migration-authority", authority)
        assert result.returncode == 1
        assert MIGRATION_AUTHORITY in result.stderr
        assert not (deliverable / "ScopeOfWork.md").exists()


def test_converter_and_resolver_reject_padded_ruled_authority(tmp_path: Path) -> None:
    for index, padded_authority in enumerate((f" {MIGRATION_AUTHORITY}", f"{MIGRATION_AUTHORITY}\t")):
        converter_deliverable = fixture(tmp_path / "converter" / str(index))
        denied = convert(
            converter_deliverable,
            "--isolated-migration",
            "--migration-authority",
            padded_authority,
        )
        assert denied.returncode == 1
        assert MIGRATION_AUTHORITY in denied.stderr
        assert not (converter_deliverable / "ScopeOfWork.md").exists()

        resolver_deliverable = fixture(tmp_path / "resolver" / str(index))
        authorized = convert(
            resolver_deliverable,
            "--isolated-migration",
            "--migration-authority",
            MIGRATION_AUTHORITY,
        )
        assert authorized.returncode == 0, authorized.stderr
        candidate = (resolver_deliverable / "ScopeOfWork.md").read_text(encoding="utf-8")
        assert f"<!-- migration-authority: {MIGRATION_AUTHORITY} -->" in candidate

        resolution = run(
            VALIDATE,
            resolver_deliverable,
            "--isolated-migration",
            "--migration-authority",
            padded_authority,
            "--json",
        )
        assert resolution.returncode == 1
        report = json.loads(resolution.stdout)
        assert report["format"] == "AMBIGUOUS"
        assert report["valid"] is False
        assert MIGRATION_AUTHORITY in " ".join(report["issues"])


def test_converter_requires_and_embeds_all_issued_bindings(tmp_path: Path) -> None:
    deliverable = fixture(tmp_path, "ISSUED")
    result = convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY)
    assert result.returncode == 1
    assert "issued-accepted-basis" in result.stderr

    missing_commit = convert(
        deliverable,
        "--isolated-migration",
        "--migration-authority", MIGRATION_AUTHORITY,
        "--issued-accepted-basis", ISSUED_ACCEPTED_BASIS,
    )
    assert missing_commit.returncode == 1
    assert "issued-source-commit" in missing_commit.stderr

    status_before = (deliverable / "_STATUS.md").read_bytes()
    binding_args = issued_binding_args(deliverable)
    missing_basis = convert(
        deliverable,
        "--isolated-migration",
        "--migration-authority", MIGRATION_AUTHORITY,
        *binding_args,
    )
    assert missing_basis.returncode == 1
    assert "issued-accepted-basis" in missing_basis.stderr

    authorized = convert(
        deliverable,
        "--isolated-migration",
        "--migration-authority",
        MIGRATION_AUTHORITY,
        "--issued-accepted-basis", ISSUED_ACCEPTED_BASIS,
        *binding_args,
    )
    assert authorized.returncode == 0, authorized.stderr
    output = (deliverable / "ScopeOfWork.md").read_text(encoding="utf-8")
    assert f"<!-- issued-preparation-accepted-basis: {ISSUED_ACCEPTED_BASIS} -->" in output
    assert "<!-- issued-preparation-source-commit: 7654321 -->" in output
    assert (deliverable / "_STATUS.md").read_bytes() == status_before
    for name in ("Datasheet.md", "Specification.md", "Procedure.md", "Guidance.md"):
        digest = hashlib.sha256((deliverable / name).read_bytes()).hexdigest()
        assert f"<!-- issued-preparation-source-sha256: {name}={digest} -->" in output
    status_digest = hashlib.sha256(status_before).hexdigest()
    assert f"<!-- issued-preparation-status-sha256: {status_digest} -->" in output

    clean = tmp_path / "issued-production" / "ScopeOfWork.md"
    report_path = tmp_path / "issued-finalization.json"
    finalized = run(
        FINALIZE,
        "--evidence-candidate", deliverable / "ScopeOfWork.md",
        "--output", clean,
        "--report", report_path,
    )
    assert finalized.returncode == 0, finalized.stderr
    assert "issued-preparation-" not in clean.read_text(encoding="utf-8")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["migration_control"]["issued-preparation-accepted-basis"] == ISSUED_ACCEPTED_BASIS
    assert report["migration_control"]["issued-preparation-source-commit"] == "7654321"
    assert len(report["migration_control"]["issued-preparation-source-sha256"]) == 4


def test_converter_rejects_unsafe_issued_accepted_basis(tmp_path: Path) -> None:
    for index, accepted_basis in enumerate((" leading", "two\nlines", "x" * 513, "basis --> escape")):
        deliverable = fixture(tmp_path / str(index), "ISSUED")
        result = convert(
            deliverable,
            "--isolated-migration",
            "--migration-authority", MIGRATION_AUTHORITY,
            "--issued-accepted-basis", accepted_basis,
            *issued_binding_args(deliverable),
        )
        assert result.returncode == 1
        assert "single-line value" in result.stderr
        assert not (deliverable / "ScopeOfWork.md").exists()


def test_format_resolution_fails_ambiguous_without_authority(tmp_path: Path) -> None:
    deliverable = fixture(tmp_path)
    assert convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY).returncode == 0
    ambiguous = run(VALIDATE, deliverable, "--json")
    assert ambiguous.returncode == 1
    assert json.loads(ambiguous.stdout)["format"] == "AMBIGUOUS"
    allowed = run(
        VALIDATE,
        deliverable,
        "--isolated-migration",
        "--migration-authority",
        MIGRATION_AUTHORITY,
        "--json",
    )
    assert allowed.returncode == 0, allowed.stdout
    assert json.loads(allowed.stdout)["format"] == "MIGRATION_DUAL"
    for wrong_authority in ("D-GOV-16@0123456", "D-GOV-16@" + "b" * 40, "D-GOV-16:wrong"):
        wrong_ref = run(
            VALIDATE,
            deliverable,
            "--isolated-migration",
            "--migration-authority",
            wrong_authority,
            "--json",
        )
        assert wrong_ref.returncode == 1
        assert MIGRATION_AUTHORITY in " ".join(json.loads(wrong_ref.stdout)["issues"])

    sow = deliverable / "ScopeOfWork.md"
    sow.write_text(sow.read_text(encoding="utf-8").replace(MIGRATION_AUTHORITY, "D-GOV-16@0123456"), encoding="utf-8")
    mismatched_marker = run(
        VALIDATE,
        deliverable,
        "--isolated-migration",
        "--migration-authority",
        MIGRATION_AUTHORITY,
        "--json",
    )
    assert mismatched_marker.returncode == 1
    assert "does not bind" in " ".join(json.loads(mismatched_marker.stdout)["issues"])


def test_legacy_and_sow_only_formats_are_valid_but_partial_legacy_is_not(tmp_path: Path) -> None:
    deliverable = fixture(tmp_path)
    legacy = run(VALIDATE, deliverable, "--json")
    assert legacy.returncode == 0
    assert json.loads(legacy.stdout)["format"] == "LEGACY_FOUR_DOC"

    assert convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY).returncode == 0
    for name in ("Datasheet.md", "Specification.md", "Procedure.md", "Guidance.md"):
        (deliverable / name).unlink()
    sow_only = run(VALIDATE, deliverable, "--json")
    assert sow_only.returncode == 0, sow_only.stdout
    assert json.loads(sow_only.stdout)["format"] == "SOW_V1"

    (deliverable / "Datasheet.md").write_text("# orphan\n", encoding="utf-8")
    partial = run(VALIDATE, deliverable, "--json")
    assert partial.returncode == 1
    assert json.loads(partial.stdout)["format"] == "INVALID"

    missing = tmp_path / "missing" / "DEL-07-04_Missing"
    missing.mkdir(parents=True)
    missing_result = run(VALIDATE, missing, "--json")
    assert missing_result.returncode == 1
    assert json.loads(missing_result.stdout)["issues"] == [
        "format state is INVALID",
        "missing production contract",
    ]


def test_invalid_scope_of_work_does_not_resolve_as_sow_v1(tmp_path: Path) -> None:
    deliverable = tmp_path / "DEL-07-05_Invalid"
    deliverable.mkdir()
    (deliverable / "ScopeOfWork.md").write_text("# not the schema\n", encoding="utf-8")
    result = run(VALIDATE, deliverable, "--json")
    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["format"] == "INVALID"
    assert any("frontmatter" in issue for issue in report["issues"])


def test_claim_map_and_parity_cover_every_source_line(tmp_path: Path) -> None:
    deliverable = fixture(tmp_path)
    assert convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY).returncode == 0
    mapping = tmp_path / "claim_map.csv"
    parity = tmp_path / "parity.json"
    map_result = run(MAP, "--scope-of-work", deliverable / "ScopeOfWork.md", "--source-dir", deliverable, "--output-csv", mapping)
    assert map_result.returncode == 0, map_result.stderr
    rows = list(csv.DictReader(mapping.open(encoding="utf-8")))
    assert rows and {row["SourceFile"] for row in rows} == {
        "Datasheet.md", "Specification.md", "Procedure.md", "Guidance.md"
    }
    parity_result = run(
        PARITY,
        "--scope-of-work",
        deliverable / "ScopeOfWork.md",
        "--source-dir",
        deliverable,
        "--output-json",
        parity,
        "--isolated-migration",
        "--migration-authority",
        MIGRATION_AUTHORITY,
    )
    assert parity_result.returncode == 0, parity_result.stderr
    assert json.loads(parity.read_text(encoding="utf-8"))["pass"] is True


def test_finalization_externalizes_metadata_and_binds_all_production_checks(tmp_path: Path) -> None:
    deliverable = fixture(tmp_path)
    (deliverable / "Specification.md").write_text(
        "# Specification\n\n## Requirements\n\nLegacy note AC-999 is quoted, not canonical.\n",
        encoding="utf-8",
    )
    assert convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY).returncode == 0
    evidence = deliverable / "ScopeOfWork.md"
    production_dir = tmp_path / "production"
    production = production_dir / "ScopeOfWork.md"
    finalization = tmp_path / "finalization.json"

    result = run(
        FINALIZE,
        "--evidence-candidate", evidence,
        "--output", production,
        "--report", finalization,
    )
    assert result.returncode == 0, result.stderr
    clean = production.read_text(encoding="utf-8")
    assert "This Scope of Work defines" in clean
    for token in ("migration candidate", "sow-source-", "migration-authority:", "issued-preparation-"):
        assert token not in clean
    assert "> Legacy note AC-999 is quoted, not canonical." in clean
    report = json.loads(finalization.read_text(encoding="utf-8"))
    production_sha = hashlib.sha256(production.read_bytes()).hexdigest()
    assert report["production_scope_of_work_sha256"] == production_sha
    assert report["migration_control"]["migration-authority"] == MIGRATION_AUTHORITY
    assert report["source_block_count"] > 0
    assert run(VALIDATE, production_dir).returncode == 0

    mapping = tmp_path / "clean-map.csv"
    mapped = run(
        MAP,
        "--scope-of-work", evidence,
        "--production-scope-of-work", production,
        "--source-dir", deliverable,
        "--output-csv", mapping,
    )
    assert mapped.returncode == 0, mapped.stderr
    assert {row["TargetSHA256"] for row in csv.DictReader(mapping.open(encoding="utf-8"))} == {production_sha}

    parity = tmp_path / "clean-parity.json"
    checked = run(
        PARITY,
        "--scope-of-work", evidence,
        "--production-scope-of-work", production,
        "--source-dir", deliverable,
        "--output-json", parity,
        "--isolated-migration",
        "--migration-authority", MIGRATION_AUTHORITY,
    )
    assert checked.returncode == 0, checked.stderr
    parity_report = json.loads(parity.read_text(encoding="utf-8"))
    assert parity_report["schema"] == "chirality-sow-parity/v2"
    assert parity_report["production_scope_of_work_sha256"] == production_sha
    assert run(CHECKLIST, production_dir, "--output", tmp_path / "clean-checklist.json").returncode == 0
    assert run(RENDER, production, "--output", tmp_path / "clean.html").returncode == 0

    production.write_text(clean.replace("This Scope of Work defines", "This altered Scope of Work defines"), encoding="utf-8")
    rejected = run(
        MAP,
        "--scope-of-work", evidence,
        "--production-scope-of-work", production,
        "--source-dir", deliverable,
        "--output-csv", tmp_path / "rejected.csv",
    )
    assert rejected.returncode == 1
    assert "deterministic finalization" in rejected.stderr


def test_renderer_is_deterministic_source_bound_and_script_free(tmp_path: Path) -> None:
    deliverable = fixture(tmp_path)
    assert convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY).returncode == 0
    first = tmp_path / "first.html"
    second = tmp_path / "second.html"
    for output in (first, second):
        result = run(
            RENDER,
            deliverable / "ScopeOfWork.md",
            "--output",
            output,
            "--isolated-migration",
            "--migration-authority",
            MIGRATION_AUTHORITY,
        )
        assert result.returncode == 0, result.stderr
    assert first.read_bytes() == second.read_bytes()
    rendered = first.read_text(encoding="utf-8")
    source_hash = hashlib.sha256((deliverable / "ScopeOfWork.md").read_bytes()).hexdigest()
    assert source_hash in rendered
    assert "<script" not in rendered.lower()
    assert "http://" not in rendered.lower() and "https://" not in rendered.lower()


def test_catalog_drives_unknown_reference_detection(tmp_path: Path) -> None:
    deliverable = fixture(tmp_path)
    assert convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY).returncode == 0
    sow = deliverable / "ScopeOfWork.md"
    sow.write_text(sow.read_text(encoding="utf-8") + "\nReference CLM-999.\n", encoding="utf-8")
    result = run(VALIDATE, deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY)
    assert result.returncode == 1
    assert "CLM-999" in result.stdout


def test_legacy_id_like_text_does_not_collide_with_candidate_catalog(tmp_path: Path) -> None:
    deliverable = fixture(tmp_path)
    specification = deliverable / "Specification.md"
    specification.write_text(
        specification.read_text(encoding="utf-8") + "\nLegacy review note AC-999 remains historical text.\n",
        encoding="utf-8",
    )
    result = convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY)
    assert result.returncode == 0, result.stderr
    validation = run(VALIDATE, deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY)
    assert validation.returncode == 0, validation.stdout


def test_orphan_output_acceptance_and_verification_definitions_fail(tmp_path: Path) -> None:
    for definition, expected in (
        ("- **OUT-999** — Orphan output.", "OUT-999"),
        ("- **AC-999** — Orphan acceptance criterion.", "AC-999"),
        ("- **VER-999** — Orphan verification method.", "VER-999"),
    ):
        deliverable = fixture(tmp_path / expected)
        assert convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY).returncode == 0
        sow = deliverable / "ScopeOfWork.md"
        sow.write_text(sow.read_text(encoding="utf-8") + f"\n{definition}\n", encoding="utf-8")
        result = run(VALIDATE, deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY)
        assert result.returncode == 1
        assert expected in result.stdout


def test_explicit_human_review_can_replace_verification_definition(tmp_path: Path) -> None:
    deliverable = fixture(tmp_path)
    assert convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY).returncode == 0
    sow = deliverable / "ScopeOfWork.md"
    text = sow.read_text(encoding="utf-8")
    text = text.replace("- **VER-001** — Run the deterministic claim map and parity report.\n", "")
    text = text.replace("| AC-001 | VER-001 |", "| AC-001 | HUMAN_REVIEW: owner inspection |")
    sow.write_text(text, encoding="utf-8")
    result = run(VALIDATE, deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY)
    assert result.returncode == 0, result.stdout


def test_review_checklist_is_exact_source_ordered_linked_and_deterministic(tmp_path: Path) -> None:
    deliverable = fixture(tmp_path)
    assert convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY).returncode == 0
    sow = deliverable / "ScopeOfWork.md"
    text = sow.read_text(encoding="utf-8")
    text = text.replace(
        "- **AC-001** — The mapped source content is complete and internally resolvable.\n",
        "- **AC-001** — The mapped source content is complete and internally resolvable.\n"
        "- **AC-002** — Human approval is recorded exactly.\n",
    )
    matrix_line = next(line for line in text.splitlines() if "| AC-001 | VER-001 |" in line)
    requirement_ref = matrix_line.split("|")[3].strip()
    text = text.replace(
        matrix_line,
        matrix_line + "\n"
        f"| OUT-001 | SOW-001 OBJ-007 | {requirement_ref} | AC-002 | "
        "HUMAN_REVIEW: owner inspects approval evidence | Human ruling |",
    )
    sow.write_text(text, encoding="utf-8")

    first = tmp_path / "checklist-1.json"
    second = tmp_path / "checklist-2.json"
    for output in (first, second):
        result = run(
            CHECKLIST,
            deliverable,
            "--isolated-migration",
            "--migration-authority",
            MIGRATION_AUTHORITY,
            "--output",
            output,
        )
        assert result.returncode == 0, result.stderr
    assert first.read_bytes() == second.read_bytes()
    report = json.loads(first.read_text(encoding="utf-8"))
    assert report["source"]["sha256"] == hashlib.sha256(sow.read_bytes()).hexdigest()
    assert [item["id"] for item in report["items"]] == ["AC-001", "AC-002"]
    assert report["items"][0]["text"] == "The mapped source content is complete and internally resolvable."
    assert report["items"][0]["verification"][0]["id"] == "VER-001"
    assert report["items"][1]["text"] == "Human approval is recorded exactly."
    assert report["items"][1]["verification"] == [
        {"kind": "HUMAN_REVIEW", "method": "owner inspects approval evidence"}
    ]

    for name in ("Datasheet.md", "Specification.md", "Procedure.md", "Guidance.md"):
        (deliverable / name).unlink()
    sow_only_first = tmp_path / "sow-only-checklist-1.json"
    sow_only_second = tmp_path / "sow-only-checklist-2.json"
    for output in (sow_only_first, sow_only_second):
        result = run(CHECKLIST, deliverable, "--output", output)
        assert result.returncode == 0, result.stderr
    assert sow_only_first.read_bytes() == sow_only_second.read_bytes()
    sow_only_report = json.loads(sow_only_first.read_text(encoding="utf-8"))
    assert sow_only_report["source"]["format"] == "SOW_V1"
    assert sow_only_report["items"] == report["items"]


def test_qualified_upstream_ids_are_not_harvested_as_local_references() -> None:
    local_re = load_catalog().local_re
    # Both qualified spellings in play upstream: slash-separated and
    # hyphen-separated. Neither is a local reference of THIS contract.
    assert local_re.findall("DEL-01-02/REQ-003") == []
    assert local_re.findall("DEL-01-02-REQ-004") == []
    # The B2 collision class: an upstream CLM-009 must not be read as the
    # authoring contract's own CLM-009.
    assert local_re.findall("DEL-01-01-CLM-009") == []
    assert local_re.findall("DEL-01-01/CLM-009") == []


def test_bare_local_ids_are_still_harvested() -> None:
    local_re = load_catalog().local_re
    assert local_re.findall("REQ-004") == ["REQ-004"]
    assert local_re.findall("bare CLM-009 here") == ["CLM-009"]
    # A qualified citation alongside a genuine local reference keeps the local
    # one and drops only the qualified tail.
    assert local_re.findall("See DEL-07-11/AC-004 and REQ-003") == ["REQ-003"]


def test_qualified_upstream_citation_does_not_break_a_valid_contract(tmp_path: Path) -> None:
    deliverable = fixture(tmp_path)
    assert convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY).returncode == 0
    sow = deliverable / "ScopeOfWork.md"
    baseline = run(VALIDATE, deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY)
    assert baseline.returncode == 0, baseline.stdout

    text = sow.read_text(encoding="utf-8")
    text = text.replace(
        "## Requirements\n",
        "## Requirements\n\nUpstream basis: DEL-01-02/REQ-003 and DEL-01-02-REQ-004.\n",
        1,
    )
    sow.write_text(text, encoding="utf-8")
    result = run(VALIDATE, deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY)
    assert result.returncode == 0, result.stdout


def test_blockquote_id_exemption_is_unchanged_by_the_left_context_guard(tmp_path: Path) -> None:
    deliverable = fixture(tmp_path)
    assert convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY).returncode == 0
    sow = deliverable / "ScopeOfWork.md"
    text = sow.read_text(encoding="utf-8")
    text = text.replace(
        "## Requirements\n",
        "## Requirements\n\n> Upstream quotation: REQ-777 and CLM-888 are source context.\n",
        1,
    )
    sow.write_text(text, encoding="utf-8")
    result = run(VALIDATE, deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY)
    assert result.returncode == 0, result.stdout


def test_review_checklist_warns_on_row_grouped_acceptance_without_changing_output(tmp_path: Path) -> None:
    deliverable = fixture(tmp_path)
    assert convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY).returncode == 0
    sow = deliverable / "ScopeOfWork.md"
    text = sow.read_text(encoding="utf-8")
    text = text.replace(
        "- **AC-001** — The mapped source content is complete and internally resolvable.\n",
        "- **AC-001** — The mapped source content is complete and internally resolvable.\n"
        "- **AC-002** — Human approval is recorded exactly.\n",
    )
    text = text.replace(
        "- **VER-001** — Run the deterministic claim map and parity report.\n",
        "- **VER-001** — Run the deterministic claim map and parity report.\n"
        "- **VER-002** — Inspect the recorded approval evidence.\n",
    )
    ungrouped = tmp_path / "checklist-ungrouped.json"
    result = run(
        CHECKLIST,
        deliverable,
        "--isolated-migration",
        "--migration-authority",
        MIGRATION_AUTHORITY,
        "--output",
        ungrouped,
    )
    assert result.returncode == 0, result.stderr
    assert "WARNING: matrix row" not in result.stderr

    matrix_line = next(line for line in text.splitlines() if "| AC-001 | VER-001 |" in line)
    grouped_line = matrix_line.replace("| AC-001 | VER-001 |", "| AC-001, AC-002 | VER-001, VER-002 |")
    sow.write_text(text.replace(matrix_line, grouped_line), encoding="utf-8")

    first = tmp_path / "checklist-grouped-1.json"
    second = tmp_path / "checklist-grouped-2.json"
    for output in (first, second):
        result = run(
            CHECKLIST,
            deliverable,
            "--isolated-migration",
            "--migration-authority",
            MIGRATION_AUTHORITY,
            "--output",
            output,
        )
        assert result.returncode == 0, result.stderr
        assert "WARNING: matrix row OUT-001 groups 2 acceptance criteria with 2 verification" in result.stderr

    # The warning is stderr-only: derivation stays deterministic and the JSON is
    # exactly the row-scoped superset it was before the warning existed.
    assert first.read_bytes() == second.read_bytes()
    report = json.loads(first.read_text(encoding="utf-8"))
    assert [item["id"] for item in report["items"]] == ["AC-001", "AC-002"]
    for item in report["items"]:
        assert [entry["id"] for entry in item["verification"]] == ["VER-001", "VER-002"]


def test_review_checklist_warns_when_a_matrix_row_carrying_acs_is_skipped(tmp_path: Path) -> None:
    deliverable = fixture(tmp_path)
    assert convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY).returncode == 0
    sow = deliverable / "ScopeOfWork.md"
    text = sow.read_text(encoding="utf-8")
    # Define AC-002 and link it in a well-formed row, so the malformed row added
    # below is the only thing that changes between the two derivations.
    text = text.replace(
        "- **AC-001** — The mapped source content is complete and internally resolvable.\n",
        "- **AC-001** — The mapped source content is complete and internally resolvable.\n"
        "- **AC-002** — Human approval is recorded exactly.\n",
    )
    matrix_line = next(line for line in text.splitlines() if "| AC-001 | VER-001 |" in line)
    requirement_ref = matrix_line.split("|")[3].strip()
    text = text.replace(
        matrix_line,
        matrix_line + "\n"
        f"| OUT-001 | SOW-001 OBJ-007 | {requirement_ref} | AC-002 | "
        "HUMAN_REVIEW: owner inspects approval evidence | Human ruling |",
    )
    sow.write_text(text, encoding="utf-8")

    clean = tmp_path / "checklist-clean.json"
    result = run(
        CHECKLIST, deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY,
        "--output", clean,
    )
    assert result.returncode == 0, result.stderr
    assert "matrix row skipped" not in result.stderr

    # A row whose cell 0 is not a bare OUT-NNN but which still carries AC
    # references. The deriver has always skipped these silently; the warning
    # names the real origin of the downstream "AC has no links entry" error.
    malformed = "| notes | continued from above | see AC-002 | AC-002 | VER-001 | ref |"
    sow.write_text(text.replace(matrix_line, matrix_line + "\n" + malformed), encoding="utf-8")
    after = tmp_path / "checklist-after.json"
    result = run(
        CHECKLIST, deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY,
        "--output", after,
    )
    assert result.returncode == 0, result.stderr
    assert "WARNING: matrix row skipped" in result.stderr
    assert "it contains AC references" in result.stderr
    # stderr-only: the skipped row contributes nothing to the derivation, so
    # every derived linkage is identical. Source hashes necessarily differ —
    # the contract file itself changed between the two runs — so compare the
    # substantive fields rather than raw bytes.
    def linkage(path: Path) -> list[dict[str, object]]:
        return [
            {
                "id": item["id"],
                "text": item["text"],
                "output_refs": item["output_refs"],
                "verification": item["verification"],
            }
            for item in json.loads(path.read_text(encoding="utf-8"))["items"]
        ]

    assert linkage(after) == linkage(clean)


def test_review_checklist_rejects_padded_ruled_authority_without_output(tmp_path: Path) -> None:
    deliverable = fixture(tmp_path)
    assert convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY).returncode == 0
    candidate = (deliverable / "ScopeOfWork.md").read_text(encoding="utf-8")
    assert f"<!-- migration-authority: {MIGRATION_AUTHORITY} -->" in candidate

    for index, padded_authority in enumerate((f" {MIGRATION_AUTHORITY}", f"{MIGRATION_AUTHORITY}\t")):
        output = tmp_path / f"padded-checklist-{index}.json"
        result = run(
            CHECKLIST,
            deliverable,
            "--isolated-migration",
            "--migration-authority",
            padded_authority,
            "--output",
            output,
        )
        assert result.returncode == 1
        assert MIGRATION_AUTHORITY in result.stderr
        assert not output.exists()


def test_review_checklist_fails_closed_for_ambiguous_invalid_and_wrong_authority(tmp_path: Path) -> None:
    deliverable = fixture(tmp_path)
    assert convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY).returncode == 0
    output = tmp_path / "must-not-exist.json"

    ambiguous = run(CHECKLIST, deliverable, "--output", output)
    assert ambiguous.returncode == 1
    assert "AMBIGUOUS" in ambiguous.stderr
    assert not output.exists()

    wrong_authority = run(
        CHECKLIST,
        deliverable,
        "--isolated-migration",
        "--migration-authority",
        "D-GOV-16@7654321",
        "--output",
        output,
    )
    assert wrong_authority.returncode == 1
    assert MIGRATION_AUTHORITY in wrong_authority.stderr
    assert not output.exists()

    sow = deliverable / "ScopeOfWork.md"
    sow.write_text(sow.read_text(encoding="utf-8").replace("- **AC-001**", "- **AC-999**"), encoding="utf-8")
    invalid = run(
        CHECKLIST,
        deliverable,
        "--isolated-migration",
        "--migration-authority",
        MIGRATION_AUTHORITY,
        "--output",
        output,
    )
    assert invalid.returncode == 1
    assert "format state is INVALID" in invalid.stderr
    assert not output.exists()


def test_review_checklist_ignores_id_shaped_definitions_inside_migrated_source(tmp_path: Path) -> None:
    deliverable = fixture(tmp_path)
    guidance = deliverable / "Guidance.md"
    guidance.write_text(
        guidance.read_text(encoding="utf-8") + "\n- **AC-001** — Historical source text, not a candidate definition.\n",
        encoding="utf-8",
    )
    assert convert(deliverable, "--isolated-migration", "--migration-authority", MIGRATION_AUTHORITY).returncode == 0
    result = run(
        CHECKLIST,
        deliverable,
        "--isolated-migration",
        "--migration-authority",
        MIGRATION_AUTHORITY,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["items"][0]["text"] == "The mapped source content is complete and internally resolvable."


# --- boundary-owner resolution (P7 §4, deterministic half) -------------------

BOUNDARY_SOW_TEMPLATE = """---
schema: chirality-deliverable-sow/v1
---

## Purpose and Objective Traceability

## Deliverable Definition — Ontology

- **CLM-012** — The acts that consume this model are owned by other
  deliverables and are cited here, never discharged: parsing the feeds is
  `DEL-02-01` through `DEL-02-07` (`SOW-011`); the rebuild is `DEL-03-01`.

## Completion and Reliance Basis — Epistemology

{requirements}

## Production and Verification Method — Praxeology

## Governing Values and Decisions — Axiology

## Output and Evaluation Matrix
"""


def boundary_doc(tmp_path: Path, requirements: str) -> tuple[Path, str]:
    path = tmp_path / "ScopeOfWork.md"
    raw = BOUNDARY_SOW_TEMPLATE.format(requirements=requirements)
    return path, raw


def test_boundary_owner_resolution_passes_when_owners_are_named_by_the_cited_claim(tmp_path: Path) -> None:
    path, raw = boundary_doc(
        tmp_path,
        "- **REQ-011** — This deliverable shall perform no act owned by another "
        "deliverable. In particular it shall run no rebuild (`DEL-03-01`); each "
        "is cited to its owner in CLM-012 and none is discharged here.\n",
    )
    report = check_document(path, raw)
    assert report.status == "OK"
    assert report.checked == 1
    assert [f for f in report.findings if f.category == "UNRESOLVED_OWNER"] == []


def test_boundary_owner_resolution_flags_an_owner_absent_from_the_cited_claim(tmp_path: Path) -> None:
    path, raw = boundary_doc(
        tmp_path,
        "- **REQ-011** — This deliverable shall perform no act owned by another "
        "deliverable. In particular it shall classify no drift (`DEL-03-03`); "
        "each is cited to its owner in CLM-012 and none is discharged here.\n",
    )
    report = check_document(path, raw)
    assert report.status == "FAIL"
    unresolved = [f for f in report.findings if f.category == "UNRESOLVED_OWNER"]
    assert len(unresolved) == 1
    assert unresolved[0].owners == ("DEL-03-03",)


def test_boundary_owner_resolution_expands_a_deliverable_range_in_the_claim(tmp_path: Path) -> None:
    # CLM-012 names `DEL-02-01` through `DEL-02-07`; DEL-02-04 is inside that
    # span but is not a literal token, so a naive membership test would fail it.
    path, raw = boundary_doc(
        tmp_path,
        "- **REQ-011** — This deliverable shall perform no act owned by another "
        "deliverable. In particular it shall parse no feed (`DEL-02-04`); each "
        "is cited to its owner in CLM-012 and none is discharged here.\n",
    )
    report = check_document(path, raw)
    assert report.status == "OK"


def test_boundary_owner_resolution_reports_per_act_clauses_as_not_checkable(tmp_path: Path) -> None:
    # A positive requirement carrying a per-act exclusion whose owner is not
    # syntactically bound to a claim. This is the skill's QA territory, and it
    # must not be reported as a contract failure.
    path, raw = boundary_doc(
        tmp_path,
        "- **REQ-003** — Every entity shall carry provenance. The act of "
        "attaching citations is `DEL-04-03`'s under `SOW-007`; this requirement "
        "obliges the model to hold what that act needs, and no more.\n",
    )
    report = check_document(path, raw)
    assert report.status == "OK"
    assert report.not_checkable == 1
    assert [f.category for f in report.findings] == ["NOT_CHECKABLE"]


def test_boundary_owner_resolution_reports_out_of_grammar_contracts(tmp_path: Path) -> None:
    # Legacy conversions define no REQ-NNN; they must be reported as
    # out-of-grammar rather than silently passing.
    path, raw = boundary_doc(tmp_path, "- **CLM-020** — A converted claim only.\n")
    report = check_document(path, raw)
    assert report.status == "NOT_APPLICABLE"
    assert report.checked == 0


def test_boundary_owner_resolution_ignores_ids_inside_blockquotes(tmp_path: Path) -> None:
    path, raw = boundary_doc(
        tmp_path,
        "- **REQ-011** — This deliverable shall perform no act owned by another "
        "deliverable; each is cited to its owner in CLM-012 and none is "
        "discharged here.\n"
        "\n"
        "> Legacy source quotation naming `DEL-09-09` as an owner.\n",
    )
    report = check_document(path, raw)
    # `DEL-09-09` lives only in a blockquote, so it is source context and is
    # never harvested as an excluded owner.
    assert report.status == "OK"


def test_boundary_owner_resolution_counts_an_uncited_exclusion_separately(tmp_path: Path) -> None:
    # A whole-requirement exclusion that cites no claim at all. Its owners
    # cannot be resolved against anything, so it is neither a pass nor a
    # per-act clause: it gets its own category and counter.
    path, raw = boundary_doc(
        tmp_path,
        "- **REQ-011** — This deliverable shall perform no act owned by another "
        "deliverable; the rebuild (`DEL-03-01`) is not discharged here.\n",
    )
    report = check_document(path, raw)
    assert report.no_cited_claim == 1
    assert report.not_checkable == 0
    assert report.checked == 0
    assert [f.category for f in report.findings] == ["NO_CITED_CLAIM"]
    # Unresolvable, but not a contract failure — it is reported, not gated.
    assert report.status == "OK"
    assert report.as_dict()["requirements_without_cited_claim"] == 1
