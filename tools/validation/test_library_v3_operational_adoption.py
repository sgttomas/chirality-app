"""Released v3 contributor-source compatibility; never a live product role supply.

All Library execution uses the small retained fixture. No sibling checkout,
network, Library Git object or native App is required by these checks.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
RECEIVING = ROOT / "reference/library-v3.0.0"
SOURCE = RECEIVING / "source"
MANIFEST = json.loads((RECEIVING / "MANIFEST.json").read_text())
REVISION = "5170575f3f4c1fc51386fa5cd38c7ef9ac048b20"
CURRENT = ROOT / "reference/library-v3.1.0"
CURRENT_MANIFEST = json.loads((CURRENT / "MANIFEST.json").read_text())
CURRENT_REVISION = "88ab3f4f5f8ec7f7e030279164dbd1a4aa38b514"
ROLES = ("HELP_HUMAN", "HELPS_HUMANS", "WORKING_ITEMS", "TASK", "INTERLOCUTOR")


def _load_resolver():
    spec = importlib.util.spec_from_file_location(
        "app_library_v3_resolver", SOURCE / "tools/workflow_runtime/resolve_workflow.py"
    )
    module = importlib.util.module_from_spec(spec)
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


def test_fixture_is_exact_and_closed():
    assert MANIFEST["commit"] == REVISION
    assert MANIFEST["tag"] == "library-v3.0.0"
    assert MANIFEST["kind"] == "partial-test-source-fixture"
    assert {p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob("*") if p.is_file()} == {
        row["path"] for row in MANIFEST["files"]
    }
    for row in MANIFEST["files"]:
        p = SOURCE / row["path"]
        raw = p.read_bytes()
        assert not p.is_symlink()
        assert len(raw) == row["bytes"]
        assert hashlib.sha256(raw).hexdigest() == row["sha256"]
        assert hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest() == row["gitBlob"]
        assert bool(p.stat().st_mode & stat.S_IXUSR) == (row["gitMode"] == "100755")


def test_released_validator_accepts_yaml_roles_in_isolated_export(tmp_path):
    relocated = tmp_path / "export"
    shutil.copytree(SOURCE, relocated)
    result = subprocess.run(
        # Preserve the released CLI's adjacent-module import while ignoring
        # Python environment overrides and user-site packages.
        [sys.executable, "-E", "-s", "-B", str(relocated / "tools/validation/validate_agent_instructions.py"), "--json"],
        cwd=tmp_path, capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    assert json.loads(result.stdout) == {
        "files_checked": 5, "errors": 0, "warnings": 0, "findings": []
    }


def test_historical_v2_validator_refuses_v3_yaml_without_rewriting_history(tmp_path):
    # Actual compatibility break: the old reader rejects the new header. Keep
    # each historical consumer paired with its own edition rather than patch it.
    old = ROOT / "reference/library-v2.1.0/source/tools/validation/validate_agent_instructions.py"
    result = subprocess.run(
        [sys.executable, "-I", "-B", str(old), "--repo-root", str(SOURCE), "--json"],
        cwd=tmp_path, capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 1, result.stderr + result.stdout
    report = json.loads(result.stdout)
    assert report["errors"] == 5
    assert {f["code"] for f in report["findings"]} == {"ROLE_PROSE_METADATA"}


@pytest.mark.parametrize("role", ROLES)
def test_resolver_carries_complete_yaml_source_and_fingerprint(role):
    result = _load_resolver().resolve(SOURCE, role)
    instruction = result["context"][0]
    raw = (SOURCE / f"agents/AGENT_{role}.md").read_bytes()
    assert raw.startswith(b"---\n")
    assert instruction["content"].encode() == raw
    assert instruction["sha256"] == hashlib.sha256(raw).hexdigest()
    assert re.findall(r"^## (.+)$", raw.decode(), re.MULTILINE) == [
        "PROTOCOL", "SPEC", "STRUCTURE", "RATIONALE"
    ]


def test_interlocutor_retains_no_delegation_or_unassigned_write_authority():
    resolver = _load_resolver()
    result = resolver.resolve(SOURCE, "INTERLOCUTOR")
    resolver.bind_write_authority(result, None)
    assert result["methods"] == []
    assert result["role_configuration"]["delegates_to"] == []
    assert result["allowed_write_targets"] == []
    assert "write" not in result["effective_tools"]["capabilities"]
    assert "delegate_agent" not in result["effective_tools"]["capabilities"]


def test_v3_method_selection_still_requires_explicit_interlocutor_eligibility(tmp_path):
    root = tmp_path / "constructed-root"
    shutil.copytree(SOURCE, root)
    folder = root / "workflows/ordinary"
    folder.mkdir(parents=True)
    (root / "workflows/catalog.yaml").write_text(json.dumps({
        "schema": "chirality-workflow-catalog/v1",
        "library": {"source": "bundled", "sourceRootId": "app-v3-constructed"},
    }))
    (folder / "WORKFLOW.md").write_text(
        "---\nname: ordinary\ndescription: Constructed compatibility input.\n"
        "metadata:\n  kind: instruction\n  surface: workflow\n---\n# Ordinary\n"
    )
    resolver = _load_resolver()
    resolver.resolve(root, "TASK", workflow="ordinary")
    with pytest.raises(ValueError, match="method incompatible with role"):
        resolver.resolve(root, "INTERLOCUTOR", workflow="ordinary")


def test_active_selection_and_entry_do_not_depend_on_packaged_instructions():
    agents = (ROOT / "AGENTS.md").read_text()
    assert CURRENT_REVISION in agents and "library-v3.1.0" in agents
    assert (ROOT / "CLAUDE.md").read_bytes() == b"@AGENTS.md\n"
    prompt = (ROOT / "init/init-prompt.md").read_text()
    assert prompt.count("<init-prompt>") == prompt.count("</init-prompt>") == 1
    assert "loop/LOOP_INIT.md" in prompt and "AGENT_HELP_HUMAN.md" in prompt
    binding = json.loads((ROOT / "app/src-tauri/resources/instructions/ROLE_SET_SOURCE_BINDING.json").read_text())
    assert binding["basisCommit"] == "89acac6a3983c605820496d0d121c73bb2297706"


def test_current_edition_delta_is_exact_and_readers_are_unchanged():
    assert CURRENT_MANIFEST["commit"] == CURRENT_REVISION
    assert CURRENT_MANIFEST["tag"] == "library-v3.1.0"
    assert CURRENT_MANIFEST["baseCommit"] == REVISION
    overrides = {"agents/AGENT_HELP_HUMAN.md", "agents/AGENT_INTERLOCUTOR.md"}
    assert {p.relative_to(CURRENT / "source").as_posix()
            for p in (CURRENT / "source").rglob("*") if p.is_file()} == overrides
    base_rows = {row["path"]: row for row in MANIFEST["files"]}
    assert {row["path"] for row in CURRENT_MANIFEST["files"]} == set(base_rows)
    for row in CURRENT_MANIFEST["files"]:
        expected_home = CURRENT if row["path"] in overrides else RECEIVING
        path = ROOT / row["retainedPath"]
        assert path == expected_home / "source" / row["path"]
        raw = path.read_bytes()
        assert not path.is_symlink()
        assert len(raw) == row["bytes"]
        assert hashlib.sha256(raw).hexdigest() == row["sha256"]
        assert hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest() == row["gitBlob"]
        assert bool(path.stat().st_mode & stat.S_IXUSR) == (row["gitMode"] == "100755")
        if row["path"] not in overrides:
            assert {k: row[k] for k in base_rows[row["path"]]} == base_rows[row["path"]]
    schema = CURRENT_MANIFEST["documentMetadataSchema"]
    assert schema["sha256"] == MANIFEST["documentMetadataSchema"]["sha256"]
    assert schema["gitBlob"] == MANIFEST["documentMetadataSchema"]["gitBlob"]


def test_current_roles_use_released_validator_and_complete_source(tmp_path):
    exported = tmp_path / "current-export"
    for row in CURRENT_MANIFEST["files"]:
        destination = exported / row["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / row["retainedPath"], destination)
    result = subprocess.run(
        [sys.executable, "-E", "-s", "-B", str(exported / "tools/validation/validate_agent_instructions.py"), "--json"],
        cwd=tmp_path, capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    assert json.loads(result.stdout) == {
        "files_checked": 5, "errors": 0, "warnings": 0, "findings": []
    }
    resolver = _load_resolver()
    for role in ("HELP_HUMAN", "INTERLOCUTOR"):
        resolved = resolver.resolve(exported, role)
        instruction = resolved["context"][0]
        raw = (exported / f"agents/AGENT_{role}.md").read_bytes()
        assert instruction["content"].encode() == raw
        assert instruction["sha256"] == hashlib.sha256(raw).hexdigest()
    resolver.bind_write_authority(resolved, None)
    assert resolved["role_configuration"]["delegates_to"] == []
    assert resolved["allowed_write_targets"] == []
