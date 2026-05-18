"""Tests for tools.source_audit.audit_folios."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "audit_folios.py"
ROOT = Path(__file__).resolve().parents[2]


def _run(page_folios: Path, audit_dir: Path, out_html: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT),
         "--page-folios-json", str(page_folios),
         "--audit-dir", str(audit_dir),
         "--output-html", str(out_html)],
        capture_output=True, text=True, cwd=str(ROOT),
    )


def _fixture(tmp: Path) -> tuple[Path, Path]:
    source = tmp / "BookX"
    work = source / "BookX_pdf2md_work"
    audit = source / "audit"
    audit.mkdir(parents=True)
    work.mkdir(parents=True)
    page_folios = {
        "1": {
            "schema_version": "pdf2md-folio-extract/v1",
            "run_status": "SUCCESS",
            "page": 1,
            "page_label": "i",
            "page_label_source": "vlm",
            "location": "bottom-center",
            "confidence": "high",
            "rationale": "Roman numeral i centered in footer.",
        },
        "2": {
            "schema_version": "pdf2md-folio-extract/v1",
            "run_status": "SUCCESS",
            "page": 2,
            "page_label": None,
            "page_label_source": "vlm",
            "location": None,
            "confidence": "high",
            "rationale": "Blank verso, no printed folio.",
        },
        "5": {
            "schema_version": "pdf2md-folio-extract/v1",
            "run_status": "FAILED",
            "page": 5,
            "page_label": None,
            "page_label_source": None,
            "location": None,
            "confidence": None,
            "rationale": "VLM call timed out.",
        },
    }
    pf_path = work / "page_folios.json"
    pf_path.write_text(json.dumps(page_folios), encoding="utf-8")
    return pf_path, audit


class AuditFoliosEndToEnd(unittest.TestCase):
    def test_renders_one_chunk_per_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            pf, audit = _fixture(Path(tmp))
            out = audit / "folios.html"
            proc = _run(pf, audit, out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            doc = out.read_text(encoding="utf-8")
            # one chunk per record
            self.assertEqual(doc.count('class="chunk folio"'), 3)
            # data-keys are stable
            self.assertIn('data-key="folio:p1"', doc)
            self.assertIn('data-key="folio:p2"', doc)
            self.assertIn('data-key="folio:p5"', doc)
            # anchor ids
            self.assertIn('id="p1"', doc)
            self.assertIn('id="p5"', doc)
            # null page_label renders as "(no folio)"
            self.assertIn("(no folio)", doc)
            # failed extractor surfaced
            self.assertIn("extractor FAILED", doc)
            # 3-state only: no backcheck chip in toolbar
            self.assertNotIn('id="stat-backcheck"', doc)

    def test_loads_prior_folios_flagged_sidecar(self):
        with tempfile.TemporaryDirectory() as tmp:
            pf, audit = _fixture(Path(tmp))
            (audit / "folios_flagged.json").write_text(
                json.dumps({
                    "folio:p1": {
                        "description": "correct: ii (not i)",
                        "flagged_at": "2026-01-01",
                    }
                }),
                encoding="utf-8",
            )
            out = audit / "folios.html"
            _run(pf, audit, out)
            doc = out.read_text(encoding="utf-8")
            self.assertIn('data-key="folio:p1"', doc)
            self.assertIn('data-status="flagged"', doc)
            self.assertIn("correct: ii (not i)", doc)


if __name__ == "__main__":
    unittest.main()
