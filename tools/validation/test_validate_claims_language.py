from pathlib import Path
import sys


VALIDATION_DIR = Path(__file__).resolve().parent
if str(VALIDATION_DIR) not in sys.path:
    sys.path.insert(0, str(VALIDATION_DIR))

import validate_claims_language as validator


PROJECT = validator.PROJECT_RELPATH
PRD_FRAGMENT = (
    "does not certify, seal, approve, authenticate, or determine code "
    "compliance for professional reliance"
)
MATURITY = "Technical preview — not a released product."
RENDERER_FRAGMENT = "decision-support software"
LITANY_LINE = (
    "No certification, no sealing, no approval, and no endorsement is made.\n"
)
BS_ACCEPT = (
    "Results are engineering decision-support information. Acceptance, "
    "professional judgment, and any certification, sealing, or "
    "code-compliance determination remain with the responsible engineer "
    "and project authority.\n"
)


def _write(repo: Path, rel: str, text: str) -> Path:
    path = repo / PROJECT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    _write(repo, "docs/PRD.md", f"# PRD\n\nThe generated report {PRD_FRAGMENT}.\n")
    _write(repo, "apps/desktop/src/App.tsx", f"export const banner = \"{MATURITY}\";\n")
    _write(
        repo,
        "core/reporting/report_renderer/src/lib.rs",
        f"// Emits the {RENDERER_FRAGMENT} notice.\n",
    )
    return repo


def _codes(repo: Path) -> list[str]:
    return [f.code for f in validator.validate_claims_language(repo)]


def test_clean_tree_passes(tmp_path, capsys):
    repo = _repo(tmp_path)
    _write(repo, "docs/user_guide/index.md", "# Guide\n\nOrdinary prose.\n")
    assert _codes(repo) == []
    assert validator.main(["--repo-root", str(repo)]) == 0
    assert capsys.readouterr().out.startswith("VALID ")


def test_litany_line_in_scope_of_work_is_flagged(tmp_path):
    repo = _repo(tmp_path)
    _write(
        repo,
        "execution/PKG-01/1_Working/DEL-01-01/ScopeOfWork.md",
        f"# SOW\n\n{LITANY_LINE}",
    )
    findings = validator.validate_claims_language(repo)
    assert [f.code for f in findings] == ["AD_HOC_CLAIMS_LITANY"]
    assert findings[0].line == 3
    assert findings[0].path.endswith("DEL-01-01/ScopeOfWork.md")


def test_registered_canonical_text_is_not_flagged(tmp_path):
    repo = _repo(tmp_path)
    _write(repo, "docs/user_guide/results.md", f"# Results\n\n{BS_ACCEPT}")
    assert _codes(repo) == []


def test_wrapped_registered_text_line_is_not_flagged(tmp_path):
    # A wrapped fragment of BS-ACCEPT carries >= 15 consecutive registered
    # characters, so the suppression window applies even though the litany
    # threshold is met on the line.
    repo = _repo(tmp_path)
    _write(
        repo,
        "docs/user_guide/results.md",
        "professional judgment, and any certification, sealing, or\n",
    )
    assert _codes(repo) == []


def test_not_authoritative_is_flagged(tmp_path):
    repo = _repo(tmp_path)
    _write(repo, "docs/user_guide/index.md", "Output is Not Authoritative.\n")
    assert _codes(repo) == ["AD_HOC_CLAIMS_LITANY"]


def test_two_terms_are_not_a_litany(tmp_path):
    repo = _repo(tmp_path)
    _write(
        repo,
        "docs/user_guide/index.md",
        "Certification and sealing decisions happen elsewhere.\n",
    )
    assert _codes(repo) == []


def test_excluded_paths_are_not_scanned(tmp_path):
    repo = _repo(tmp_path)
    for rel in (
        "execution/PKG-01/1_Working/DEL-01-01/_run_records/RUN.md",
        "execution/_Reconciliation/notes.md",
        "docs/_history/2026-01-01_old.md",
        "docs/security/threat_model.md",
        "docs/PROFESSIONAL_BOUNDARY.md",
        "apps/desktop/src/App.test.tsx",
    ):
        _write(repo, rel, LITANY_LINE + "Also not authoritative.\n")
    assert _codes(repo) == []


def test_desktop_source_litany_is_flagged(tmp_path):
    repo = _repo(tmp_path)
    _write(
        repo,
        "apps/desktop/src/features/Panel.tsx",
        "const note = \"Not a certification, sealing, approval, or "
        "code-compliance result.\";\n",
    )
    assert _codes(repo) == ["AD_HOC_CLAIMS_LITANY"]


def test_missing_prd_notice_fires(tmp_path):
    repo = _repo(tmp_path)
    _write(repo, "docs/PRD.md", "# PRD without the notice\n")
    assert _codes(repo) == ["MISSING_PRD_NOTICE"]


def test_missing_maturity_banner_fires(tmp_path):
    repo = _repo(tmp_path)
    _write(repo, "apps/desktop/src/App.tsx", "export const App = null;\n")
    assert _codes(repo) == ["MISSING_MATURITY_BANNER"]


def test_missing_renderer_notice_fires_when_file_absent(tmp_path):
    repo = _repo(tmp_path)
    (repo / PROJECT / "core/reporting/report_renderer/src/lib.rs").unlink()
    assert _codes(repo) == ["MISSING_RENDERER_NOTICE"]


def test_findings_exit_one_with_invalid_lines(tmp_path, capsys):
    repo = _repo(tmp_path)
    _write(repo, "docs/user_guide/index.md", LITANY_LINE)
    assert validator.main(["--repo-root", str(repo)]) == 1
    out = capsys.readouterr().out
    assert out.startswith("INVALID AD_HOC_CLAIMS_LITANY ")
    assert "docs/user_guide/index.md:1:" in out


def test_missing_project_root_is_operational(tmp_path, capsys):
    assert validator.main(["--repo-root", str(tmp_path)]) == 2
    assert "OPERATIONAL_ERROR" in capsys.readouterr().err


def test_authority_citation_line_is_not_flagged(tmp_path):
    repo = _repo(tmp_path)
    _write(
        repo,
        "docs/RELEASE_NOTES_TEMPLATE.md",
        "Waivers must not authorize professional approval claims, "
        "certification, sealing, or code-compliance claims (PRD §21.2).\n",
    )
    assert _codes(repo) == []


def test_enforcement_vocab_line_is_not_flagged(tmp_path):
    repo = _repo(tmp_path)
    _write(
        repo,
        "apps/desktop/src/features/x/Panel.tsx",
        'const prohibited = ["software certifies", "software seals", '
        '"software approves", "code compliant for reliance"];\n',
    )
    assert _codes(repo) == []


def test_scope_of_work_not_scanned_when_wave2_gate_off(tmp_path, monkeypatch):
    monkeypatch.setattr(validator, "WAVE2_SURFACES_ACTIVE", False)
    repo = _repo(tmp_path)
    _write(
        repo,
        "execution/PKG-01/1_Working/DEL-01-01/ScopeOfWork.md",
        "No certification, sealing, approval, or code-compliance claim.\n",
    )
    assert _codes(repo) == []
