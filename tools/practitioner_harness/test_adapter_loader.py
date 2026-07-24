#!/usr/bin/env python3
"""Adapter-manifest loader tests (operational-error posture, exit 2)."""

from __future__ import annotations

from pathlib import Path

import pytest

import adapter_loader
import harness
from harness_common import HarnessOperationalError
from test_self_check_fixtures import ADAPTER_YAML, build_mini_repo


def _project(tmp_path: Path, manifest_text: str) -> Path:
    root = tmp_path / "proj"
    (root / "_harness").mkdir(parents=True, exist_ok=True)
    (root / "_harness" / "adapter.yaml").write_text(manifest_text, encoding="utf-8")
    return root


def test_valid_manifest_loads(tmp_path):
    root = _project(tmp_path, ADAPTER_YAML.format(
        project="fixture", baseline_mismatch=3, baseline_files=7,
        requires_sha="true", sha_field="Checking Approval SHA"))
    m = adapter_loader.load_adapter(root)
    assert m.project == "fixture"
    assert m.schema == adapter_loader.ADAPTER_SCHEMA
    assert m.drift_baseline_mismatch == 3
    assert m.drift_baseline_files == 7
    assert m.states[0] == "OPEN" and m.states[-1] == "ISSUED"
    assert m.guard_requires_approval_sha is True
    assert m.guard_approval_sha_field == "Checking Approval SHA"
    assert m.exclude_globs == [".archive/**", "node_modules/**"]


def test_missing_required_key_is_operational_error(tmp_path):
    text = ADAPTER_YAML.format(
        project="fixture", baseline_mismatch=0, baseline_files=0,
        requires_sha="false", sha_field="")
    text = text.replace('status_glob: "execution/PKG-*/1_Working/*/_STATUS.md"\n', "")
    root = _project(tmp_path, text)
    with pytest.raises(HarnessOperationalError) as exc:
        adapter_loader.load_adapter(root)
    assert "status_glob" in str(exc.value)


def test_unknown_schema_is_operational_error(tmp_path):
    text = ADAPTER_YAML.format(
        project="fixture", baseline_mismatch=0, baseline_files=0,
        requires_sha="false", sha_field="")
    text = text.replace("practitioner-harness-adapter/v1", "mystery-adapter/v9")
    root = _project(tmp_path, text)
    with pytest.raises(HarnessOperationalError) as exc:
        adapter_loader.load_adapter(root)
    assert "unknown schema" in str(exc.value)


def test_manifest_absent_is_operational_error(tmp_path):
    root = tmp_path / "empty"
    root.mkdir()
    with pytest.raises(HarnessOperationalError):
        adapter_loader.load_adapter(root)


def test_unparseable_manifest_is_operational_error(tmp_path):
    root = _project(tmp_path, "schema: [unclosed\n  broken: {{{{\n")
    with pytest.raises(HarnessOperationalError):
        adapter_loader.load_adapter(root)


def test_pyyaml_absent_is_operational_error(tmp_path, monkeypatch):
    root = _project(tmp_path, ADAPTER_YAML.format(
        project="fixture", baseline_mismatch=0, baseline_files=0,
        requires_sha="false", sha_field=""))
    monkeypatch.setattr(adapter_loader, "yaml", None)
    with pytest.raises(HarnessOperationalError) as exc:
        adapter_loader.load_adapter(root)
    assert "PyYAML" in str(exc.value)


def test_cli_exit_2_on_broken_manifest(tmp_path, capsys):
    repo = build_mini_repo(tmp_path)
    manifest = repo / "projects" / "chirality-piping" / "_harness" / "adapter.yaml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            "practitioner-harness-adapter/v1", "mystery/v9"),
        encoding="utf-8")
    rc = harness.main(["--repo-root", str(repo), "drift", "--project", "piping"])
    assert rc == 2
    assert "ERROR" in capsys.readouterr().err
