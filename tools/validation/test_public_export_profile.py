from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
EXPORTER = REPO_ROOT / "exports" / "chirality-app" / "export_public.py"


def load_exporter():
    if not EXPORTER.exists():
        pytest.skip("public export intentionally excludes the private export profile")
    spec = importlib.util.spec_from_file_location("chirality_public_export", EXPORTER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_public_export_excludes_private_runtime_surfaces(tmp_path: Path) -> None:
    exporter = load_exporter()
    stage = tmp_path / "stage"
    exporter.build_stage(stage)

    assert (stage / 'agents/registry.json').is_file()
    assert len(list((stage / 'agents').glob('AGENT_*.md'))) == 4
    source_index = json.loads((REPO_ROOT / 'workflows/index.json').read_text(encoding='utf-8'))
    expected_workflows = {
        item['name'] for item in source_index['methods']
        if item['kind'] == 'workflow' and item['source'] == 'bundled'
    }
    assert {path.parent.name for path in (stage / 'workflows').glob('*/WORKFLOW.md')} == expected_workflows
    assert not (stage / 'ADOPTION_HOLD.json').exists()
    assert not (stage / 'skills').exists()
    bundled_skills = sorted(path.parent.name for path in (stage / '.agents/skills').glob('*/SKILL.md'))
    assert bundled_skills == sorted(exporter.BUNDLED_SKILL_NAMES)
    assert 'chirality-change' not in bundled_skills
    assert not (stage / "execution").exists()
    index = __import__('json').loads((stage / 'workflows/index.json').read_text(encoding='utf-8'))
    assert index['schema'] == 'chirality-method-index/v1'
    assert not any(item.get('kind') == 'skill' and item.get('name') == 'chirality-change' for item in index['methods'])
    assert not (stage / ".github/workflows/harness-premerge.yml").exists()
    assert not any((stage / "docs/governance_harness/briefs").glob("*"))
    assert not (stage / "tools/practitioner_harness/BACKLOG.md").exists()

    prompt = (stage / "init/init-prompt.md").read_text(encoding="utf-8")
    assert "does not include project loop entrypoints" in prompt
    assert "projects/chirality-app-dev" not in prompt
    assert "projects/chirality-piping" not in prompt

    public_readme = (stage / "README.md").read_text(encoding="utf-8")
    dedicated_readme = (exporter.PROFILE_DIR / "PUBLIC_README.md").read_text(encoding="utf-8")
    canonical_readme = (exporter.REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert public_readme == dedicated_readme
    assert public_readme != canonical_readme
    for marker in exporter.PUBLIC_README_REQUIRED_MARKERS:
        assert marker in public_readme
    for marker in exporter.PUBLIC_README_FORBIDDEN_MARKERS:
        assert marker.casefold() not in public_readme.casefold()

    # The private project's governance scaffold must not enter the public
    # runtime workspace, and an ignored old runtime/ cannot mask an empty export.
    assert (stage / "runtime/package.json").read_bytes() == (
        REPO_ROOT / "projects/chirality-runtime/package.json"
    ).read_bytes()
    assert (stage / "runtime/packages/core/src/runtime-service.ts").is_file()
    assert not (stage / "runtime/chirality.project.json").exists()
    assert not (stage / "runtime/AGENTS.md").exists()
    assert not (stage / "runtime/execution").exists()
    assert not (stage / "runtime/loop").exists()
    assert not (stage / "runtime/docs").exists()

    # The public desktop source is projected without its private project
    # custody, dependency directories, or generated build output.
    assert (stage / "desktop/package.json").read_bytes() == (
        REPO_ROOT / "projects/chirality-app-dev/frontend/package.json"
    ).read_bytes()
    assert (stage / "desktop/src").is_dir()
    assert (stage / "desktop/electron").is_dir()
    assert (stage / "desktop/build/icon.icns").is_file()
    assert not (stage / "desktop/node_modules").exists()
    assert not (stage / "desktop/dist").exists()
    assert not (stage / "desktop/.next").exists()
    assert not (stage / "desktop/.chirality").exists()

    assert exporter.boundary_findings(stage) == []


def test_public_export_rejects_private_canonical_readme_framing(tmp_path: Path) -> None:
    exporter = load_exporter()
    stage = tmp_path / "stage"
    stage.mkdir()
    (stage / "README.md").write_text(
        "\n".join(exporter.PUBLIC_README_REQUIRED_MARKERS)
        + "\n## Private Canonical Repository\n",
        encoding="utf-8",
    )

    assert (
        "private canonical README marker in public README: ## Private Canonical Repository"
        in exporter.boundary_findings(stage)
    )


def test_copy_tree_rejects_symlinked_source_directories_and_files(tmp_path, monkeypatch):
    exporter = load_exporter()
    repo = tmp_path / 'repo'
    source = repo / '.agents/skills/example'
    source.mkdir(parents=True)
    outside = tmp_path / 'outside'
    outside.mkdir()
    (outside / 'secret.md').write_text('private\n', encoding='utf-8')
    monkeypatch.setattr(exporter, 'REPO_ROOT', repo)

    directory_link = repo / '.agents/skills/directory-link'
    directory_link.symlink_to(outside, target_is_directory=True)
    with pytest.raises(SystemExit, match='symlinked path component'):
        exporter.copy_tree(directory_link, tmp_path / 'directory-stage', '.agents/skills/example')

    real_parent = repo / 'real-parent'
    (real_parent / 'nested-skill').mkdir(parents=True)
    (real_parent / 'nested-skill/SKILL.md').write_text('safe fixture\n', encoding='utf-8')
    linked_parent = repo / 'linked-parent'
    linked_parent.symlink_to(real_parent, target_is_directory=True)
    with pytest.raises(SystemExit, match='symlinked path component'):
        exporter.copy_tree(
            linked_parent / 'nested-skill',
            tmp_path / 'intermediate-stage',
            '.agents/skills/example',
        )

    (source / 'SKILL.md').symlink_to(outside / 'secret.md')
    with pytest.raises(SystemExit, match='symlinked export source entry'):
        exporter.copy_tree(source, tmp_path / 'file-stage', '.agents/skills/example')
    assert not (tmp_path / 'file-stage/SKILL.md').exists()
    (source / 'SKILL.md').unlink()
    os.mkfifo(source / 'unsupported-entry')
    with pytest.raises(SystemExit, match='unsupported export source entry'):
        exporter.copy_tree(source, tmp_path / 'fifo-tree-stage', '.agents/skills/example')


def test_direct_file_copy_and_metadata_outputs_reject_symlink_sources(tmp_path, monkeypatch):
    exporter = load_exporter()
    repo = tmp_path / 'repo'
    repo.mkdir()
    outside = tmp_path / 'outside.txt'
    outside.write_text('private\n', encoding='utf-8')
    monkeypatch.setattr(exporter, 'REPO_ROOT', repo)

    for relative in [
        'AGENTS.md',
        'exports/chirality-app/PUBLIC_README.md',
        'projects/chirality-runtime/package.json',
    ]:
        source = repo / relative
        source.parent.mkdir(parents=True, exist_ok=True)
        source.symlink_to(outside)
        with pytest.raises(SystemExit, match='symlinked path component'):
            exporter.copy_source_file(source, tmp_path / 'stage' / source.name)

    profile = tmp_path / 'profile'
    profile.mkdir()
    manifest = profile / 'export-manifest.csv'
    manifest.symlink_to(outside)
    monkeypatch.setattr(exporter, 'PROFILE_DIR', profile)
    monkeypatch.setattr(exporter, 'MANIFEST_PATH', manifest)
    with pytest.raises(SystemExit, match='symlinked path component'):
        exporter.admit_fixed_profile_output(manifest, manifest)

    fifo_source = repo / 'FIFO.md'
    os.mkfifo(fifo_source)
    with pytest.raises(SystemExit, match='not a regular file'):
        exporter.copy_source_file(fifo_source, tmp_path / 'fifo-stage/FIFO.md')

    manifest.unlink()
    os.mkfifo(manifest)
    with pytest.raises(SystemExit, match='not a regular file'):
        exporter.admit_fixed_profile_output(manifest, manifest)


def test_stage_admission_rejects_source_overlap_before_deletion(tmp_path, monkeypatch):
    exporter = load_exporter()
    repo = tmp_path / 'repo'
    protected = repo / 'agents'
    protected.mkdir(parents=True)
    sentinel = protected / 'preserve.md'
    sentinel.write_text('preserve\n', encoding='utf-8')
    default_stage = repo / 'exports/chirality-app/staging'
    monkeypatch.setattr(exporter, 'REPO_ROOT', repo)
    monkeypatch.setattr(exporter, 'DEFAULT_STAGE', default_stage)

    with pytest.raises(SystemExit, match='overlaps the canonical repository'):
        exporter.admit_stage_path(protected)
    assert sentinel.read_text(encoding='utf-8') == 'preserve\n'

    stage_alias = tmp_path / 'stage-alias'
    stage_alias.symlink_to(protected, target_is_directory=True)
    with pytest.raises(SystemExit, match='symlinked export stage'):
        exporter.admit_stage_path(stage_alias)
    assert sentinel.read_text(encoding='utf-8') == 'preserve\n'

    fifo_stage = tmp_path / 'fifo-stage'
    os.mkfifo(fifo_stage)
    with pytest.raises(SystemExit, match='not a directory'):
        exporter.admit_stage_path(fifo_stage)
