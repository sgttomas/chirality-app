"""Tests for tools.source_audit.audit_tables."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "audit_tables.py"
ROOT = Path(__file__).resolve().parents[2]


def _run(manifest: Path, audit_dir: Path, out_html: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT),
         "--asset-manifest", str(manifest),
         "--audit-dir", str(audit_dir),
         "--output-html", str(out_html)],
        capture_output=True, text=True, cwd=str(ROOT),
    )


def _fixture(tmp: Path) -> tuple[Path, Path]:
    source = tmp / "BookX"
    audit = source / "audit"
    audit.mkdir(parents=True)
    manifest = {
        "schema_version": "pdf2md-assets-document/v2",
        "doc_stem": "BookX",
        "assets": [
            # Normal table — both XLSX and JSON present
            {
                "asset_id": "BookX_p0007_tbl01", "kind": "tbl", "page": 7,
                "caption": "Properties of pipe", "png_path": "tables/BookX_p0007_tbl01.png",
                "xlsx_path": "tables/BookX_p0007_tbl01.xlsx",
                "table_data_json_path": "tables/BookX_p0007_tbl01.json",
            },
            # needs_extraction — no XLSX/JSON links, shows chip
            {
                "asset_id": "BookX_p0007_tbl02", "kind": "tbl", "page": 7,
                "caption": "Complex form", "png_path": "tables/BookX_p0007_tbl02.png",
                "needs_extraction": True,
            },
            # not a table — should not appear
            {
                "asset_id": "BookX_p0007_fig01", "kind": "fig", "page": 7,
                "caption": "F", "png_path": "figures/BookX_p0007_fig01.png",
            },
        ],
    }
    manifest_path = source / "BookX_assets_manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return manifest_path, audit


class AuditTablesEndToEnd(unittest.TestCase):
    def test_renders_xlsx_and_json_links_for_normal(self):
        with tempfile.TemporaryDirectory() as tmp:
            mp, audit = _fixture(Path(tmp))
            out = audit / "tables.html"
            proc = _run(mp, audit, out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            doc = out.read_text(encoding="utf-8")
            self.assertEqual(doc.count('class="chunk tbl"'), 2)
            self.assertNotIn('class="chunk fig"', doc)
            self.assertIn('class="xlsxlink"', doc)
            self.assertIn('class="jsonlink"', doc)
            self.assertIn('BookX_p0007_tbl01.xlsx', doc)
            self.assertIn('BookX_p0007_tbl01.json', doc)

    def test_needs_extraction_shows_chip_no_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            mp, audit = _fixture(Path(tmp))
            out = audit / "tables.html"
            _run(mp, audit, out)
            doc = out.read_text(encoding="utf-8")
            # The needs_extraction chunk has the chip
            self.assertIn(
                'data-asset-id="BookX_p0007_tbl02" data-page="7" data-needs-extraction="true"',
                doc,
            )
            self.assertIn('needs_extraction', doc)
            # ...and its block does NOT carry an xlsx link
            # (find the tbl02 block bounds and assert no xlsxlink within)
            start = doc.index('id="asset-BookX_p0007_tbl02"')
            end = doc.index('</div>', start)
            block = doc[start:end]
            self.assertNotIn('xlsxlink', block)
            self.assertNotIn('jsonlink', block)

    def test_loads_prior_tables_verified_sidecar(self):
        with tempfile.TemporaryDirectory() as tmp:
            mp, audit = _fixture(Path(tmp))
            (audit / "tables_verified.json").write_text(
                json.dumps({"table:BookX_p0007_tbl01": {"verified_at": "2026-01-01"}}),
                encoding="utf-8",
            )
            out = audit / "tables.html"
            _run(mp, audit, out)
            doc = out.read_text(encoding="utf-8")
            self.assertIn('data-key="table:BookX_p0007_tbl01" data-status="verified"', doc)


if __name__ == "__main__":
    unittest.main()
