"""Checks of the bundled Library workflows that need no Library release.

The committed tree is checked against its own manifest and against the
project's record of the selected edition; the generator's rules are exercised
on an invented archive. That the tree equals the selected release is
established with the release archive: `python3 -m tools.library_workflows
compare --archive <release .tar>`.
"""

from __future__ import annotations

import io
import json
import re
import tarfile
from pathlib import Path

import pytest

from tools.library_workflows import bundle

ROOT = bundle.ROOT
OUTPUT = ROOT / bundle.OUTPUT


def manifest() -> dict:
    return json.loads((OUTPUT / bundle.MANIFEST_NAME).read_text(encoding="utf-8"))


def test_committed_tree_is_what_its_manifest_records():
    assert bundle.verify_tree(OUTPUT) == []


def test_manifest_names_the_selected_edition_and_the_compiled_pin():
    selection = bundle.read_selection()
    recorded = manifest()
    source = recorded["source"]
    assert {key: source[key] for key in ("repository", "tag", "commit", "archive")} == selection
    assert recorded["release_subject"] == f"chirality-library:{selection['tag']}"
    # The edition the repository instructions select is the one bundled.
    instructions = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert f"tag `{selection['tag']}`, commit `{selection['commit']}`" in instructions
    # The host admits only the manifest whose digest it was compiled with.
    catalog = (ROOT / "app/src-tauri/src/workflow_catalog.rs").read_text(encoding="utf-8")
    pin = re.search(r'SELECTED_BUNDLED_MANIFEST_SHA256: &str =\s*"([0-9a-f]{64})"', catalog).group(1)
    assert pin == bundle.sha256((OUTPUT / bundle.MANIFEST_NAME).read_bytes())
    assert f'RELEASE_SUBJECT: &str = "{recorded["release_subject"]}"' in catalog


def test_every_index_entry_is_accounted_for():
    recorded = manifest()
    names = [row["name"] for row in recorded["packages"]]
    assert names == sorted(set(names), key=lambda n: n.encode())
    assert all(entry["kind"] != "workflow" for entry in recorded["index_entries_not_bundled"])
    folders = sorted(path.name for path in OUTPUT.iterdir() if path.is_dir())
    assert folders == sorted(names)


# An invented release: two workflows, one skill, and the Library files around them.
FILES = {
    "LICENSE.md": b"invented licence\n",
    "README.md": b"# invented library\n",
    "agents/AGENT_TASK.md": b"role\n",
    "docs/guide.md": b"guide\n",
    "docs/PRD.md": b"the library's own PRD\n",
    "tools/check/run.py": b"print('x')\n",
    "tools/REGISTRY.md": b"registry\n",
    ".agents/skills/researcher/SKILL.md": b"skill\n",
    "workflows/README.md": b"inventory\n",
    "workflows/alpha/WORKFLOW.md": (
        b"---\nname: alpha\n---\n"
        b"Run `python3 tools/check/run.py:*` or \"$INSTRUCTION_ROOT/tools/check/run.py\".\n"
        b"Load `agents/AGENT_TASK.md`. See [the guide](../../docs/guide.md#part) and\n"
        b"[its README](../../README.md). Use the `researcher` skill and tools/absent.py.\n"
        b"Read `resources/note.md`, [beta](../beta/WORKFLOW.md) and tools/local.py.\n"
        b"See https://example.invalid/blob/abc/docs/PRD.md and tools/check/.\n"
    ),
    "workflows/alpha/resources/note.md": b"See `.agents/skills/researcher/SKILL.md`.\n",
    "workflows/alpha/tools/local.py": b"pass\n",
    "workflows/beta/WORKFLOW.md": b"---\nname: beta\n---\nMethod text only.\n",
}


def method(name: str, resources: list[str], **more) -> dict:
    return {
        "kind": "workflow", "name": name, "source": "bundled", "sourceRootId": "invented-root",
        "description": f"Use {name}.", "central": False, "compatibility": "canonical",
        "executionRoleIds": ["TASK"], "resources": resources,
        "navigation": {"category": "specialist", "tier": "primary", "order": 1}, **more,
    }


def index(methods: list[dict]) -> bytes:
    return json.dumps({"schema": bundle.INDEX_SCHEMA, "methods": methods}).encode()


METHODS = [
    method("alpha", ["WORKFLOW.md", "resources/note.md", "tools/local.py"],
           execution={"schemaVersion": 1, "compatibleRoles": ["TASK"], "tools": {"commands": ["python3 tools/check/run.py:*"]}}),
    method("beta", ["WORKFLOW.md"]),
    {"kind": "skill", "name": "researcher"},
]


def release(files: dict[str, bytes], links: dict[str, str] | None = None) -> bytes:
    data = io.BytesIO()
    with tarfile.open(fileobj=data, mode="w") as tar:
        for path, content in files.items():
            member = tarfile.TarInfo(path)
            member.size = len(content)
            tar.addfile(member, io.BytesIO(content))
        for path, target in (links or {}).items():
            member = tarfile.TarInfo(path)
            member.type = tarfile.SYMTYPE
            member.linkname = target
            tar.addfile(member)
    return data.getvalue()


def selection_for(archive: bytes) -> dict:
    return {
        "repository": "https://example.invalid/library", "tag": "library-v0.0.0", "commit": "0" * 40,
        "archive": {"name": "invented.tar", "bytes": len(archive), "sha256": bundle.sha256(archive)},
    }


def built(tmp_path: Path, files: dict[str, bytes], methods=METHODS, links=None) -> dict[str, bytes]:
    archive = release({**files, bundle.INDEX_PATH: index(methods)}, links)
    path = tmp_path / "invented.tar"
    path.write_bytes(archive)
    selection = selection_for(archive)
    return bundle.build(bundle.read_release(path, selection), selection)


def test_generated_tree_is_the_release_packages_byte_for_byte(tmp_path):
    tree = built(tmp_path, FILES)
    recorded = json.loads(tree.pop(bundle.MANIFEST_NAME))
    assert tree == {
        path.removeprefix("workflows/"): data
        for path, data in FILES.items()
        if path.startswith(("workflows/alpha/", "workflows/beta/"))
    }
    assert [row["name"] for row in recorded["packages"]] == ["alpha", "beta"]
    assert recorded["index_entries_not_bundled"] == [{"kind": "skill", "name": "researcher"}]
    alpha, beta = recorded["packages"]
    package = {path.removeprefix("alpha/"): data for path, data in tree.items() if path.startswith("alpha/")}
    assert alpha["revision"] == bundle.revision(package)
    assert [row["path"] for row in alpha["files"]] == ["WORKFLOW.md", "resources/note.md", "tools/local.py"]
    # What the Library's index states is carried in its words, absent as null.
    assert alpha["library_execution"] == METHODS[0]["execution"]
    assert beta["library_execution"] is None
    # Writing and verifying round-trip, and a changed byte is found.
    output = tmp_path / "out"
    bundle.write_tree({**tree, bundle.MANIFEST_NAME: json.dumps(recorded).encode()}, output)
    assert bundle.verify_tree(output) == []
    (output / "alpha/resources/note.md").write_bytes(b"edited\n")
    (output / "gamma").mkdir()
    (output / "gamma/WORKFLOW.md").write_bytes(b"extra\n")
    assert bundle.verify_tree(output) == ["alpha: files differ from the manifest", "not in the manifest: gamma/WORKFLOW.md"]


def test_named_paths_are_library_tool_skill_and_role_paths_and_nothing_else(tmp_path):
    recorded = json.loads(built(tmp_path, FILES)[bundle.MANIFEST_NAME])
    alpha, beta = recorded["packages"]
    assert alpha["library_paths_named"] == [
        # The path a package file gives, not the skill's bare name in prose.
        ".agents/skills/researcher/SKILL.md",
        "agents/AGENT_TASK.md",
        # A folder of the release, and a file under a prefix or before `:*`.
        "tools/check",
        "tools/check/run.py",
    ]
    # Not counted: a document, by link or by path (docs/guide.md, README.md,
    # docs/PRD.md); a path absent from the release (tools/absent.py); a path
    # of this package (resources/note.md, tools/local.py); another bundled
    # workflow (../beta/WORKFLOW.md); and the rest of a URL.
    assert beta["library_paths_named"] == []
    # A relative link is resolved from the file that names it.
    linked = {**FILES, "workflows/beta/WORKFLOW.md": b"---\nname: beta\n---\n[run](../../tools/check/run.py) [doc](../../docs/PRD.md) docs/PRD.md\n"}
    beta = json.loads(built(tmp_path, linked)[bundle.MANIFEST_NAME])["packages"][1]
    assert beta["library_paths_named"] == ["tools/check/run.py"]


def test_a_release_the_app_would_not_admit_is_refused(tmp_path):
    def refused(files, methods=METHODS, links=None) -> str:
        with pytest.raises(bundle.BundleError) as error:
            built(tmp_path, files, methods, links)
        return str(error.value)

    assert "disagree" in refused({**FILES, "workflows/gamma/WORKFLOW.md": b"unlisted\n"})
    assert "disagree" in refused(FILES, [*METHODS, method("gamma", ["WORKFLOW.md"])])
    assert "resources" in refused({**FILES, "workflows/beta/extra.md": b"unlisted file\n"})
    assert "link" in refused(FILES, links={"workflows/beta/linked.md": "WORKFLOW.md"})
    assert "operating-system" in refused(
        {**FILES, "workflows/beta/.DS_Store": b""}, [METHODS[0], method("beta", ["WORKFLOW.md", ".DS_Store"]), METHODS[2]]
    )
    assert "kinds" in refused(FILES, [*METHODS, {"kind": "plugin", "name": "x"}])
    renamed = {path.replace("workflows/beta/", "workflows/Beta_1/"): data for path, data in FILES.items()}
    assert "not a workflow name" in refused(renamed, [METHODS[0], method("Beta_1", ["WORKFLOW.md"]), METHODS[2]])


def test_an_archive_that_is_not_the_selected_one_is_refused(tmp_path):
    archive = release({**FILES, bundle.INDEX_PATH: index(METHODS)})
    path = tmp_path / "invented.tar"
    path.write_bytes(archive + b"\0" * 512)
    with pytest.raises(bundle.BundleError, match="not the selected release archive"):
        bundle.read_release(path, selection_for(archive))
