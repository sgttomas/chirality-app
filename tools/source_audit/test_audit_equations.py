"""Tests for tools.source_audit.equations + the audit_equations CLI wrapper."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.source_audit import chunk as sa_chunk
from tools.source_audit import equations


SCRIPT = Path(__file__).resolve().parents[2] / "tools" / "equation_audit" / "audit_equations.py"
ROOT = Path(__file__).resolve().parents[2]


def _write_pages(work: Path, pages: dict[int, str]) -> None:
    for pg, body in pages.items():
        (work / f"page_{pg:04d}.md").write_text(body, encoding="utf-8")


def _run_cli(work: Path, out_html: Path, out_jsonl: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable, str(SCRIPT),
            "--work-dir", str(work),
            "--out-html", str(out_html),
            "--out-jsonl", str(out_jsonl),
            "--title", "Test Equation Audit",
        ],
        capture_output=True, text=True, cwd=str(ROOT),
    )


class ScanPages(unittest.TestCase):
    def test_extracts_display_equations_in_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            _write_pages(work, {
                1: "text before $$a = b$$ more $$c = d$$",
                2: "no equations here",
                3: "$$E = mc^2$$",
            })
            recs = equations.scan_pages(work)
            self.assertEqual(len(recs), 3)
            self.assertEqual(recs[0]["page"], 1)
            self.assertEqual(recs[0]["index"], 1)
            self.assertEqual(recs[0]["latex"], "a = b")
            self.assertEqual(recs[1]["index"], 2)
            self.assertEqual(recs[2]["page"], 3)
            self.assertEqual(recs[2]["latex"], "E = mc^2")
            self.assertTrue(all(r["key"] == f"{r['page']}:{r['hash']}" for r in recs))


class FourStateStatusResolution(unittest.TestCase):
    def test_verified_beats_flagged_beats_backcheck(self):
        s, n = sa_chunk.initial_status_for_key(
            "k", {"k": {}}, {"k": {"description": "x"}}, backcheck={"k": {}}
        )
        self.assertEqual(s, "verified")
        s, n = sa_chunk.initial_status_for_key(
            "k", {}, {"k": {"description": "x"}}, backcheck={"k": {}}
        )
        self.assertEqual(s, "flagged")
        self.assertEqual(n, "x")
        s, n = sa_chunk.initial_status_for_key("k", {}, {}, backcheck={"k": {}})
        self.assertEqual(s, "backcheck")
        s, n = sa_chunk.initial_status_for_key("k", {}, {}, backcheck={})
        self.assertEqual(s, "unreviewed")

    def test_three_state_call_still_works(self):
        # callers that don't pass backcheck must continue to function
        s, n = sa_chunk.initial_status_for_key("k", {"k": {}}, {})
        self.assertEqual(s, "verified")


class AuditEquationsEndToEnd(unittest.TestCase):
    def _fixture(self, tmp: Path) -> tuple[Path, Path, Path, Path]:
        work = tmp / "work"
        work.mkdir()
        audit = tmp / "audit"
        audit.mkdir()
        _write_pages(work, {
            1: "$$a = b$$ and $$c = d$$",
            5: "$$E = mc^2$$",
        })
        out_html = audit / "equations.html"
        out_jsonl = audit / "equations.jsonl"
        return work, audit, out_html, out_jsonl

    def test_renders_chunks_with_chunk_eq_class(self):
        with tempfile.TemporaryDirectory() as tmp:
            work, audit, out_html, out_jsonl = self._fixture(Path(tmp))
            proc = _run_cli(work, out_html, out_jsonl)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            doc = out_html.read_text(encoding="utf-8")
            # DOM class must be `chunk eq` so the shared JS .chunk selector matches
            # AND equation-specific CSS via .chunk.eq applies.
            self.assertEqual(doc.count('class="chunk eq"'), 3)
            self.assertIn('data-kind="equation"', doc)
            self.assertIn('id="p1"', doc)
            self.assertIn('id="p5"', doc)

    def test_katex_includes_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            work, audit, out_html, out_jsonl = self._fixture(Path(tmp))
            _run_cli(work, out_html, out_jsonl)
            doc = out_html.read_text(encoding="utf-8")
            self.assertIn("katex.min.css", doc)
            self.assertIn("auto-render.min.js", doc)
            self.assertIn("renderMathInElement", doc)

    def test_only_backcheck_filter_chip_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            work, audit, out_html, out_jsonl = self._fixture(Path(tmp))
            _run_cli(work, out_html, out_jsonl)
            doc = out_html.read_text(encoding="utf-8")
            self.assertIn('id="only-backcheck"', doc)
            self.assertIn('id="stat-backcheck"', doc)
            self.assertIn("body.only-backcheck", doc)

    def test_export_filenames_use_equations_kind(self):
        with tempfile.TemporaryDirectory() as tmp:
            work, audit, out_html, out_jsonl = self._fixture(Path(tmp))
            _run_cli(work, out_html, out_jsonl)
            doc = out_html.read_text(encoding="utf-8")
            self.assertIn("equations_verified.json + equations_flagged.json", doc)
            self.assertIn('const KIND = "equations"', doc)

    def test_jsonl_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            work, audit, out_html, out_jsonl = self._fixture(Path(tmp))
            _run_cli(work, out_html, out_jsonl)
            lines = out_jsonl.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 3)
            rec0 = json.loads(lines[0])
            self.assertEqual(rec0["page"], 1)
            self.assertEqual(rec0["index"], 1)
            self.assertEqual(rec0["latex"], "a = b")
            self.assertNotIn("key", rec0)

    def test_loads_canonical_kind_prefixed_sidecars(self):
        with tempfile.TemporaryDirectory() as tmp:
            work, audit, out_html, out_jsonl = self._fixture(Path(tmp))
            # determine the hash for "a = b" and seed a verified entry
            recs = equations.scan_pages(work)
            v_key = recs[0]["key"]  # 1:<hash(a = b)>
            f_key = recs[1]["key"]  # 1:<hash(c = d)>
            bc_key = recs[2]["key"]  # 5:<hash(E = mc^2)>

            (audit / "equations_verified.json").write_text(
                json.dumps({v_key: {"verified_at": "2026-05-17"}}),
                encoding="utf-8",
            )
            (audit / "equations_flagged.json").write_text(
                json.dumps({f_key: {"description": "fix the numerator"}}),
                encoding="utf-8",
            )
            (audit / "equations_backcheck.json").write_text(
                json.dumps({bc_key: {"description": "applied fix", "prev_latex": "E=mc"}}),
                encoding="utf-8",
            )

            _run_cli(work, out_html, out_jsonl)
            doc = out_html.read_text(encoding="utf-8")
            self.assertIn(f'data-key="{v_key}" data-page="1" data-hash="{recs[0]["hash"]}" data-status="verified"', doc)
            self.assertIn(f'data-status="flagged"', doc)
            self.assertIn("fix the numerator", doc)
            self.assertIn(f'data-status="backcheck"', doc)
            self.assertIn("Fix applied — please backcheck", doc)
            self.assertIn("E=mc", doc)

    def test_loads_legacy_bare_sidecars(self):
        """Sources not yet migrated to kind-prefixed names still load."""
        with tempfile.TemporaryDirectory() as tmp:
            work, audit, out_html, out_jsonl = self._fixture(Path(tmp))
            recs = equations.scan_pages(work)
            v_key = recs[0]["key"]
            (audit / "verified.json").write_text(
                json.dumps({v_key: {"verified_at": "2026-05-17"}}),
                encoding="utf-8",
            )
            _run_cli(work, out_html, out_jsonl)
            doc = out_html.read_text(encoding="utf-8")
            self.assertIn(f'data-key="{v_key}" data-page="1" data-hash="{recs[0]["hash"]}" data-status="verified"', doc)


class GatePOneFiveIntegration(unittest.TestCase):
    """1.5-P UI extensions: source badges + Reject + equations_rejected suppression."""
    def _fixture(self, tmp: Path):
        work = tmp / "work"; work.mkdir()
        audit = tmp / "audit"; audit.mkdir()
        # one equation per page so we can target keys deterministically
        (work / "page_0001.md").write_text("$$a + b$$", encoding="utf-8")
        out_html = audit / "equations.html"
        out_jsonl = audit / "equations.jsonl"
        return work, audit, out_html, out_jsonl

    def test_one_five_p_machine_badge_and_reject_button(self):
        with tempfile.TemporaryDirectory() as tmp:
            work, audit, out_html, out_jsonl = self._fixture(Path(tmp))
            recs = equations.scan_pages(work)
            key = recs[0]["key"]
            eq_hash = recs[0]["hash"]
            (audit / "equations_backcheck.json").write_text(
                json.dumps({
                    key: {
                        "page": 1, "hash": eq_hash,
                        "source": "1.5-P-machine",
                        "proposal_hash": "deadbeefcafe",
                        "description": "1.5-P proposal: \\frac{a}{b}",
                        "prev_latex": "a + b",
                    }
                }),
                encoding="utf-8",
            )
            _run_cli(work, out_html, out_jsonl)
            doc = out_html.read_text(encoding="utf-8")
            self.assertIn("bcsource-prefilter", doc)
            self.assertIn("1.5-P-machine", doc)
            self.assertIn("Reject proposal", doc)
            self.assertIn('data-proposalhash="deadbeefcafe"', doc)
            self.assertIn('data-eqhash="' + eq_hash + '"', doc)

    def test_phase3_source_badge_no_reject_button(self):
        with tempfile.TemporaryDirectory() as tmp:
            work, audit, out_html, out_jsonl = self._fixture(Path(tmp))
            recs = equations.scan_pages(work)
            key = recs[0]["key"]
            eq_hash = recs[0]["hash"]
            (audit / "equations_backcheck.json").write_text(
                json.dumps({
                    key: {
                        "page": 1, "hash": eq_hash,
                        "source": "EQUATION_AUDIT-phase3",
                        "description": "applied fix",
                    }
                }),
                encoding="utf-8",
            )
            _run_cli(work, out_html, out_jsonl)
            doc = out_html.read_text(encoding="utf-8")
            self.assertIn("bcsource-phase3", doc)
            self.assertIn("EQUATION_AUDIT-phase3", doc)
            self.assertNotIn("Reject proposal", doc)

    def test_rejected_proposal_suppressed_at_render(self):
        with tempfile.TemporaryDirectory() as tmp:
            work, audit, out_html, out_jsonl = self._fixture(Path(tmp))
            recs = equations.scan_pages(work)
            key = recs[0]["key"]
            eq_hash = recs[0]["hash"]
            prop_hash = "deadbeefcafe"
            (audit / "equations_backcheck.json").write_text(
                json.dumps({
                    key: {
                        "page": 1, "hash": eq_hash,
                        "source": "1.5-P-machine",
                        "proposal_hash": prop_hash,
                        "description": "proposal text",
                    }
                }),
                encoding="utf-8",
            )
            (audit / "equations_rejected.json").write_text(
                json.dumps({
                    f"{eq_hash}:{prop_hash}": {
                        "equation_hash": eq_hash,
                        "proposal_hash": prop_hash,
                        "rejected_at": "2026-05-17",
                    }
                }),
                encoding="utf-8",
            )
            _run_cli(work, out_html, out_jsonl)
            doc = out_html.read_text(encoding="utf-8")
            # Chunk renders as unreviewed (not backcheck), no bcnote block
            self.assertIn(f'data-key="{key}" data-page="1" data-hash="{eq_hash}" data-status="unreviewed"', doc)
            self.assertNotIn("Fix applied — please backcheck", doc)


class FiguresStillThreeStateOnly(unittest.TestCase):
    """Regression: figures.html must not gain a backcheck filter chip."""
    def test_figures_html_has_no_backcheck_widgets(self):
        # The figures test fixture creates a manifest and renders; check the
        # rendered output for absence of backcheck.
        from tools.source_audit import audit_figures  # noqa: F401
        figures_script = Path(__file__).resolve().parent / "audit_figures.py"
        with tempfile.TemporaryDirectory() as tmp:
            tmp_p = Path(tmp)
            source = tmp_p / "BookY"
            audit = source / "audit"
            audit.mkdir(parents=True)
            manifest = {
                "schema_version": "pdf2md-assets-document/v2",
                "doc_stem": "BookY",
                "assets": [
                    {"asset_id": "BookY_p0001_fig01", "kind": "fig", "page": 1,
                     "caption": "C", "png_path": "figures/BookY_p0001_fig01.png"},
                ],
            }
            mp = source / "BookY_assets_manifest.json"
            mp.write_text(json.dumps(manifest), encoding="utf-8")
            out = audit / "figures.html"
            subprocess.run(
                [sys.executable, str(figures_script),
                 "--asset-manifest", str(mp),
                 "--audit-dir", str(audit),
                 "--output-html", str(out)],
                capture_output=True, text=True, cwd=str(ROOT),
            )
            doc = out.read_text(encoding="utf-8")
            self.assertNotIn('id="only-backcheck"', doc)
            self.assertNotIn('id="stat-backcheck"', doc)
            self.assertNotIn("katex.min.css", doc)


if __name__ == "__main__":
    unittest.main()
