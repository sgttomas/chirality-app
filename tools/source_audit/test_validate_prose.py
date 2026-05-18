"""Tests for tools.source_audit.validate_prose CLI."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "validate_prose.py"
ROOT = Path(__file__).resolve().parents[2]


class ValidateProseCLI(unittest.TestCase):
    def test_clean_pair_emits_zero_finding_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_p = Path(tmp)
            work = tmp_p / "work"
            reext = tmp_p / "reext"
            audit = tmp_p / "audit"
            for d in (work, reext, audit):
                d.mkdir()
            (work / "page_0001.md").write_text("Hello world.", encoding="utf-8")
            (reext / "page_0001.reextract.md").write_text("Hello world.", encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPT),
                 "--work-dir", str(work),
                 "--reextract-dir", str(reext),
                 "--audit-dir", str(audit)],
                capture_output=True, text=True, cwd=str(ROOT),
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads((audit / "prose_validation.json").read_text())
            self.assertEqual(data["schema_version"], "pdf2md-prose-validate/v1")
            self.assertEqual(data["counts"]["pages_compared"], 1)
            self.assertEqual(data["counts"]["prose_hunks"], 0)

    def test_divergent_pair_reports_findings(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_p = Path(tmp)
            work = tmp_p / "work"; reext = tmp_p / "reext"; audit = tmp_p / "audit"
            for d in (work, reext, audit):
                d.mkdir()
            (work / "page_0001.md").write_text(
                "The cat sat.\n\n$$a + b$$", encoding="utf-8")
            (reext / "page_0001.reextract.md").write_text(
                "The dog sat.\n\n$$a - b$$", encoding="utf-8")
            subprocess.run(
                [sys.executable, str(SCRIPT),
                 "--work-dir", str(work),
                 "--reextract-dir", str(reext),
                 "--audit-dir", str(audit)],
                capture_output=True, text=True, cwd=str(ROOT),
            )
            data = json.loads((audit / "prose_validation.json").read_text())
            self.assertEqual(data["counts"]["prose_hunks"], 1)
            self.assertEqual(data["counts"]["equation_content_proposals"], 1)

    def test_missing_reextract_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_p = Path(tmp)
            work = tmp_p / "work"; reext = tmp_p / "reext"; audit = tmp_p / "audit"
            for d in (work, reext, audit):
                d.mkdir()
            (work / "page_0001.md").write_text("hi", encoding="utf-8")
            (work / "page_0002.md").write_text("hi2", encoding="utf-8")
            (reext / "page_0001.reextract.md").write_text("hi", encoding="utf-8")
            subprocess.run(
                [sys.executable, str(SCRIPT),
                 "--work-dir", str(work),
                 "--reextract-dir", str(reext),
                 "--audit-dir", str(audit)],
                capture_output=True, text=True, cwd=str(ROOT),
            )
            data = json.loads((audit / "prose_validation.json").read_text())
            self.assertEqual(data["missing_reextract"], [2])


if __name__ == "__main__":
    unittest.main()
