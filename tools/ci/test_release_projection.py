"""Regression checks for the exported library and release-repository boundary."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

import pytest

from validate_release_projection import PRIVATE_PATHS, REQUIRED_FILES, ROOT, validate_projection
from build_workflow_index import validate_and_build


def test_automatic_ci_inputs_exist_in_the_release_repository():
    workflow = (ROOT / ".github/workflows/governance-harness.yml").read_text()
    inputs = set(re.findall(r"(tools/[A-Za-z0-9_./-]+\.(?:py|txt))", workflow))
    assert inputs
    for relative in inputs:
        assert (ROOT / relative).is_file(), relative


@pytest.fixture
def projection(tmp_path):
    for name in ("agents", "workflows", ".agents", "tools"):
        shutil.copytree(ROOT / name, tmp_path / name, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    for relative in REQUIRED_FILES:
        source = ROOT / relative
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    return tmp_path


def test_current_release_projection_is_reproducible():
    report = validate_projection(ROOT)
    assert report["status"] == "PASS"
    assert report["sourceVersions"]["desktop"] == json.loads((ROOT / "desktop/package.json").read_text())["version"]


def test_public_mode_preserves_index_and_legacy_project_identity(projection):
    index = validate_and_build(projection, public_export=True)
    assert index == json.loads((projection / "workflows/index.json").read_text())
    assert index["legacy"]["retiredRoles"]["CHANGE"]["canonical_successor"] == {
        "kind": "skill", "name": "chirality-change", "scope": "project",
    }
    assert not any(method["name"] == "chirality-change" for method in index["methods"])
    with pytest.raises(ValueError, match="unknown skill successor: CHANGE"):
        validate_and_build(projection)


def test_exclusion_does_not_hide_other_missing_packages(projection):
    shutil.rmtree(projection / ".agents/skills/researcher")
    with pytest.raises(ValueError, match="unknown skill successor"):
        validate_and_build(projection, public_export=True)


def test_exclusion_does_not_whitelist_a_retired_role(projection):
    path = projection / "workflows/legacy-agents.json"
    retired = json.loads(path.read_text())
    retired["aliases"]["CHANGE"]["canonical_successor"]["name"] = "unpublished-skill"
    path.write_text(json.dumps(retired))
    with pytest.raises(ValueError, match="unknown skill successor: CHANGE"):
        validate_and_build(projection, public_export=True)


def test_omitted_successor_must_retain_project_scope(projection):
    path = projection / "workflows/legacy-agents.json"
    retired = json.loads(path.read_text())
    retired["aliases"]["CHANGE"]["canonical_successor"]["scope"] = "bundled"
    path.write_text(json.dumps(retired))
    with pytest.raises(ValueError, match="unknown skill successor: CHANGE"):
        validate_and_build(projection, public_export=True)


def test_unknown_converted_method_still_fails(projection):
    path = projection / "workflows/legacy-methods.json"
    methods = json.loads(path.read_text())
    methods["convertedWorkflowAliases"]["unpublished-alias"] = {"kind": "skill", "name": "unpublished-skill"}
    path.write_text(json.dumps(methods))
    with pytest.raises(ValueError, match="mapping targets unknown"):
        validate_and_build(projection, public_export=True)


def test_public_mode_still_validates_an_existing_excluded_package(projection):
    package = projection / ".agents/skills/chirality-change"
    package.mkdir()
    (package / "SKILL.md").write_text("---\nname: chirality-change\ndescription: Project change\n---\n")
    outside = projection.parent / "private.txt"
    outside.write_text("private fixture")
    (package / "escape.txt").symlink_to(outside)
    with pytest.raises(ValueError, match="escaping resource"):
        validate_and_build(projection, public_export=True)


@pytest.mark.parametrize("relative", PRIVATE_PATHS)
def test_private_monorepo_state_is_rejected(projection, relative):
    (projection / relative).mkdir(parents=True)
    with pytest.raises(ValueError, match="private monorepo path"):
        validate_projection(projection)


def test_missing_and_escaping_source_fail(projection):
    source = projection / "desktop/electron/main.ts"
    source.unlink()
    with pytest.raises(ValueError, match="missing or escaping"):
        validate_projection(projection)
    outside = projection.parent / "main.ts"
    outside.write_text("external fixture")
    source.symlink_to(outside)
    with pytest.raises(ValueError, match="missing or escaping"):
        validate_projection(projection)


def test_stale_index_fails(projection):
    path = projection / "workflows/index.json"
    index = json.loads(path.read_text())
    index["methods"][0]["description"] = "unpublished description"
    path.write_text(json.dumps(index, indent=2) + "\n")
    with pytest.raises(ValueError, match="index is stale"):
        validate_projection(projection)


@pytest.mark.parametrize("workspace", ["desktop", "runtime"])
@pytest.mark.parametrize("field", ["version", "root-version", "dependencies", "workspaces"])
def test_manifest_lock_drift_fails(projection, workspace, field):
    path = projection / workspace / "package-lock.json"
    lock = json.loads(path.read_text())
    if field == "version":
        lock[field] = "unpublished"
    elif field == "root-version":
        lock["packages"][""]["version"] = "unpublished"
    elif field == "dependencies":
        lock["packages"][""][field] = {"unexpected": "1.0.0"}
    else:
        lock["packages"][""][field] = ["unpublished/*"]
    path.write_text(json.dumps(lock))
    with pytest.raises(ValueError, match="package/lock .* mismatch"):
        validate_projection(projection)


def test_validator_cli_checks_public_mode(projection):
    result = subprocess.run([
        sys.executable, str(ROOT / "tools/validation/validate_workflow_metadata.py"),
        str(projection / "workflows"), "--public-export", "--json",
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["invalid_workflow_count"] == 0
