from __future__ import annotations

import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
EXPORTER = REPO_ROOT / "exports" / "chirality-app" / "export_public.py"


def load_exporter():
    spec = importlib.util.spec_from_file_location("chirality_public_export", EXPORTER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_public_export_excludes_private_runtime_surfaces(tmp_path: Path) -> None:
    exporter = load_exporter()
    stage = tmp_path / "stage"
    exporter.build_stage(stage)

    assert not (stage / ".github/workflows/harness-premerge.yml").exists()
    assert not any((stage / "docs/governance_harness/briefs").glob("*"))
    assert not (stage / "tools/practitioner_harness/BACKLOG.md").exists()

    prompt = (stage / "init/init-prompt.md").read_text(encoding="utf-8")
    assert "private project loop entrypoints" in prompt
    assert "projects/chirality-app-dev" not in prompt
    assert "projects/chirality-piping" not in prompt
    assert exporter.boundary_findings(stage) == []
