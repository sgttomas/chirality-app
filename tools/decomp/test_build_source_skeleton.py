#!/usr/bin/env python3
"""Tests for DOMAIN_DECOMP source skeleton dispatch planning."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


TOOL = Path(__file__).resolve().parent / "build_source_skeleton.py"


def run_skeleton(tmp_path: Path, source_text: str, *extra_args: str) -> tuple[dict, dict]:
    md = tmp_path / "source.md"
    manifest = tmp_path / "source_assets_manifest.json"
    skeleton = tmp_path / "source_skeleton.json"
    dispatch = tmp_path / "source_dispatch_plan.json"
    md.write_text(source_text, encoding="utf-8")
    manifest.write_text(
        json.dumps({"doc_stem": "SRC-TEST", "assets": [], "pages": []}) + "\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--md",
            str(md),
            "--asset-manifest",
            str(manifest),
            "--output-skeleton",
            str(skeleton),
            "--output-dispatch-plan",
            str(dispatch),
            "--source-prefix",
            "TST",
            *extra_args,
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return (
        json.loads(skeleton.read_text(encoding="utf-8")),
        json.loads(dispatch.read_text(encoding="utf-8")),
    )


def test_in_scope_override_makes_standalone_glossary_dispatchable(tmp_path: Path) -> None:
    skeleton, dispatch = run_skeleton(
        tmp_path,
        "# Glossary\n\n| Term | Definition |\n|---|---|\n| Gate | Human approval point. |\n",
        "--in-scope-overrides",
        '["SEC-TST-0001"]',
    )

    section = skeleton["sections"][0]
    assert section["title"] == "Glossary"
    assert section["is_back_matter"] is False
    assert section["in_scope_default"] is True
    assert dispatch["unit_count"] == 1
    assert dispatch["units"][0]["target_section_ids"] == ["SEC-TST-0001"]


def test_late_glossary_stays_out_without_override(tmp_path: Path) -> None:
    skeleton, dispatch = run_skeleton(
        tmp_path,
        "# Chapter 1\n\nSubstantive source content.\n\n# Glossary\n\nTerm list.\n",
    )

    glossary = skeleton["sections"][1]
    assert glossary["title"] == "Glossary"
    assert glossary["is_back_matter"] is True
    assert glossary["in_scope_default"] is False
    assert dispatch["unit_count"] == 1
    assert "SEC-TST-0002" not in dispatch["units"][0]["target_section_ids"]
