"""Tests for tools.source_audit.audit_images."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "audit_images.py"
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
            {
                "asset_id": "BookX_p0001_img01", "kind": "img", "page": 1,
                "caption": "Masthead", "png_path": "images/BookX_p0001_img01.png",
            },
            {
                "asset_id": "BookX_p0050_img01", "kind": "img", "page": 50,
                "caption": "Photo", "png_path": "images/BookX_p0050_img01.png",
            },
            # not an image
            {
                "asset_id": "BookX_p0001_fig01", "kind": "fig", "page": 1,
                "caption": "F", "png_path": "figures/BookX_p0001_fig01.png",
            },
        ],
    }
    manifest_path = source / "BookX_assets_manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return manifest_path, audit


class AuditImagesEndToEnd(unittest.TestCase):
    def test_renders_only_images(self):
        with tempfile.TemporaryDirectory() as tmp:
            mp, audit = _fixture(Path(tmp))
            out = audit / "images.html"
            proc = _run(mp, audit, out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            doc = out.read_text(encoding="utf-8")
            self.assertEqual(doc.count('class="chunk img"'), 2)
            self.assertNotIn('class="chunk fig"', doc)
            self.assertIn('data-key="image:BookX_p0001_img01"', doc)
            self.assertIn('id="p1"', doc)
            self.assertIn('id="p50"', doc)

    def test_loads_prior_images_flagged_sidecar(self):
        with tempfile.TemporaryDirectory() as tmp:
            mp, audit = _fixture(Path(tmp))
            (audit / "images_flagged.json").write_text(
                json.dumps({
                    "image:BookX_p0001_img01": {
                        "description": "page masthead, not content",
                        "flagged_at": "2026-01-01",
                    }
                }),
                encoding="utf-8",
            )
            out = audit / "images.html"
            _run(mp, audit, out)
            doc = out.read_text(encoding="utf-8")
            self.assertIn('data-key="image:BookX_p0001_img01" data-status="flagged"', doc)
            self.assertIn("page masthead, not content", doc)


if __name__ == "__main__":
    unittest.main()
