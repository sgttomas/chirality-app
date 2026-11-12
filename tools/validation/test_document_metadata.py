"""Typed maintained App surfaces; frozen inputs keep their original bytes.

Run with ``python -m pytest -q tools/validation/test_document_metadata.py``.
The released schema is retained locally; no sibling checkout or network is read.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
RECEIVING = ROOT / "reference/library-v3.4.0"
MANIFEST = json.loads((RECEIVING / "MANIFEST.json").read_text())
SCHEMA = json.loads((RECEIVING / "document-metadata.schema.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA)


def documents():
    paths = {
        ROOT / "AGENTS.md", ROOT / "init-prompt.md",
        *(ROOT / "docs").rglob("*.md"),
        *(ROOT / "tools").rglob("README.md"),
        *(ROOT / "workflows").glob("*/WORKFLOW.md"),
    }
    for home in (".agents/skills", ".claude/skills", "skills", "workflows", "tools"):
        paths.update((ROOT / home).rglob("SKILL.md"))
    return sorted(paths)


def header(path):
    lines = path.read_text().splitlines()
    assert lines and lines[0] == "---", f"{path}: missing leading YAML header"
    assert "---" in lines[1:], f"{path}: missing closing YAML delimiter"
    end = lines.index("---", 1)
    return yaml.safe_load("\n".join(lines[1:end]))


@pytest.mark.parametrize("path", documents(), ids=lambda p: p.relative_to(ROOT).as_posix())
def test_maintained_document_header(path):
    VALIDATOR.validate(header(path))


def test_schema_source_identity_and_contract():
    assert MANIFEST["commit"] == "1bba3d170e7a25bc2a04e0a4dfe77b624ea440ca"
    binding = MANIFEST["documentMetadataSchema"]
    raw = (RECEIVING / binding["path"]).read_bytes()
    assert binding["sourcePath"] == "docs/document-metadata.schema.json"
    assert len(raw) == binding["bytes"]
    assert hashlib.sha256(raw).hexdigest() == binding["sha256"]
    assert hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest() == binding["gitBlob"]
    assert binding["gitMode"] == "100644"
    Draft202012Validator.check_schema(SCHEMA)


def test_frozen_and_product_inputs_are_not_retyped():
    selected = {p.relative_to(ROOT).as_posix() for p in documents()}
    assert {"AGENTS.md", "init-prompt.md"} <= selected
    assert not any(p.startswith(("execution/", "reference/", "app/")) for p in selected)


@pytest.mark.parametrize("field", ("status", "date", "revision"))
@pytest.mark.parametrize("nested", (False, True))
def test_revision_and_status_fields_are_rejected(field, nested):
    data = header(ROOT / "AGENTS.md")
    (data["metadata"] if nested else data)[field] = "current"
    with pytest.raises(ValidationError):
        VALIDATOR.validate(data)


@pytest.mark.parametrize("change", (
    {"name": "HELP_HUMAN"}, {"name": "a" * 65}, {"description": ""},
    {"description": "two\nlines"}, {"description": "trailing\n"},
    {"metadata": {"kind": "accepted", "surface": "role"}},
    {"metadata": {"kind": "instruction", "surface": "session"}},
    {"metadata": {"surface": "standing"}},
))
def test_invalid_metadata_is_rejected(change):
    data = header(ROOT / "AGENTS.md")
    data.update(change)
    with pytest.raises(ValidationError):
        VALIDATOR.validate(data)


def test_package_extensions_remain_valid():
    data = copy.deepcopy(header(ROOT / "AGENTS.md"))
    data["metadata"]["applicability"] = "Authorized project maintenance"
    data["allowed-tools"] = "Read"
    VALIDATOR.validate(data)


def test_bootstrap_wrapper_and_claude_pointer():
    text = (ROOT / "init-prompt.md").read_text()
    assert text.index("\n---\n") < text.index("<init-prompt>")
    assert text.count("<init-prompt>") == text.count("</init-prompt>") == 1
    block = text.split("<init-prompt>", 1)[1].split("</init-prompt>", 1)[0]
    assert "{REPO_ROOT}/AGENTS.md" in block and "AGENT_HELP_HUMAN.md" in block
    assert "name:" not in block
    assert (ROOT / "CLAUDE.md").read_bytes() == b"@AGENTS.md\n"


@pytest.mark.parametrize("upstream", (
    {}, {"source": "workflows/project-setup/resources/project-entry.md"},
    {"source": "", "edition": "library-v3.3.0"},
    {"source": "source.md", "edition": "main"},
    {"source": "source.md", "edition": "library-v3.3.0", "extra": True},
))
def test_incomplete_or_unsupported_derivation_metadata_is_rejected(upstream):
    data = copy.deepcopy(header(ROOT / "AGENTS.md"))
    data["metadata"]["upstream"] = upstream
    with pytest.raises(ValidationError):
        VALIDATOR.validate(data)


@pytest.mark.parametrize("name", ("AGENTS.md", "init-prompt.md"))
def test_reconciled_entry_documents_name_the_canonical_released_template(name):
    data = header(ROOT / name)
    VALIDATOR.validate(data)
    assert data["metadata"]["upstream"] == {
        "source": "workflows/project-setup/resources/project-entry.md",
        "edition": "library-v3.4.0",
    }
