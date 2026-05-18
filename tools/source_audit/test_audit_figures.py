"""Tests for tools.source_audit.audit_figures."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "audit_figures.py"
ROOT = Path(__file__).resolve().parents[2]


def _run(manifest: Path, audit_dir: Path, out_html: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable, str(SCRIPT),
            "--asset-manifest", str(manifest),
            "--audit-dir", str(audit_dir),
            "--output-html", str(out_html),
        ],
        capture_output=True, text=True, cwd=str(ROOT),
    )


def _fixture(tmp: Path) -> tuple[Path, Path, Path]:
    """Create source/, source/audit/, and a minimal asset manifest with two
    figures on page 5 and one on page 12."""
    source = tmp / "BookX"
    audit = source / "audit"
    audit.mkdir(parents=True)
    (source / "figures").mkdir()
    # PNG files don't need to be real — the HTML lazy-loads via src=
    manifest = {
        "schema_version": "pdf2md-assets-document/v2",
        "doc_stem": "BookX",
        "assets": [
            {
                "asset_id": "BookX_p0005_fig01", "kind": "fig", "page": 5,
                "caption": "Fig 1 caption", "png_path": "figures/BookX_p0005_fig01_x.png",
            },
            {
                "asset_id": "BookX_p0005_fig02", "kind": "fig", "page": 5,
                "caption": "Fig 2 <script>", "png_path": "figures/BookX_p0005_fig02_y.png",
            },
            {
                "asset_id": "BookX_p0012_fig01", "kind": "fig", "page": 12,
                "caption": "Fig 3", "png_path": "figures/BookX_p0012_fig01_z.png",
            },
            # one table — should not appear in figures.html
            {
                "asset_id": "BookX_p0005_tbl01", "kind": "tbl", "page": 5,
                "caption": "T", "png_path": "tables/BookX_p0005_tbl01_t.png",
            },
        ],
    }
    manifest_path = source / "BookX_assets_manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return manifest_path, audit, source


class AuditFiguresEndToEnd(unittest.TestCase):
    def test_renders_only_figures_grouped_by_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            mp, audit, _ = _fixture(Path(tmp))
            out = audit / "figures.html"
            proc = _run(mp, audit, out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            doc = out.read_text(encoding="utf-8")
            # three figures
            self.assertEqual(doc.count('class="chunk fig"'), 3)
            # no table chunks
            self.assertNotIn('class="chunk tbl"', doc)
            # page anchors
            self.assertIn('id="p5"', doc)
            self.assertIn('id="p12"', doc)
            # page heading counts
            self.assertIn('Page 5 <span class="count">(2)</span>', doc)
            self.assertIn('Page 12 <span class="count">(1)</span>', doc)
            # anchor key
            self.assertIn('data-key="figure:BookX_p0005_fig01"', doc)
            # caption escaped (the <script> tag in caption must not appear literally)
            self.assertNotIn("<script>x</script>", doc)
            self.assertIn("Fig 2 &lt;script&gt;", doc)

    def test_loads_prior_verified_sidecar(self):
        with tempfile.TemporaryDirectory() as tmp:
            mp, audit, _ = _fixture(Path(tmp))
            (audit / "figures_verified.json").write_text(
                json.dumps({"figure:BookX_p0005_fig01": {"verified_at": "2026-01-01"}}),
                encoding="utf-8",
            )
            out = audit / "figures.html"
            proc = _run(mp, audit, out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            doc = out.read_text(encoding="utf-8")
            # the verified chunk renders with data-status="verified"
            self.assertIn('data-key="figure:BookX_p0005_fig01" data-status="verified"', doc)
            # stat counter shows 1 verified
            self.assertIn('id="stat-verified">1<', doc)

    def test_export_filenames_in_js(self):
        with tempfile.TemporaryDirectory() as tmp:
            mp, audit, _ = _fixture(Path(tmp))
            out = audit / "figures.html"
            _run(mp, audit, out)
            doc = out.read_text(encoding="utf-8")
            self.assertIn('const KIND = "figures"', doc)
            self.assertIn("${KIND}_verified_${ts}", doc)
            self.assertIn("${KIND}_flagged_${ts}", doc)


if __name__ == "__main__":
    unittest.main()
