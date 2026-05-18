#!/usr/bin/env python3
"""
Unit tests for rewrite_inline_asset_refs.py.

Run:
    python3 tools/pdf2md/test_rewrite_inline_asset_refs.py
Exit 0 = all assertions passed; non-zero = at least one failure.
"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


_HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location(
    "rewrite_inline_asset_refs",
    _HERE / "rewrite_inline_asset_refs.py",
)
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules["rewrite_inline_asset_refs"] = _MOD
_SPEC.loader.exec_module(_MOD)


def _materialized_page(page: int, assets: list[dict]) -> dict:
    return {"page": page, "assets": assets, "schema_version": "pdf2md-assets-materialized/v1"}


class InlineRewriteTests(unittest.TestCase):
    def test_page3_citation_survives_inside_label(self):
        """Page 3 carries the canonical bracketed-citation pattern. The rewriter
        must produce a Markdown image whose alt-text contains the escaped \\[1\\]
        and whose link target ends cleanly with ".png)".
        """
        page_md = (
            "2    DESIGN OF PIPING SYSTEMS\n\n"
            "[FIGURE: Fig. 1.1 Yield stress-strain curve of copper in compression. "
            "After Cook and Larke [1].]\n\n"
            "plastic failure without instability.\n"
        )
        materialized = _materialized_page(
            3,
            [
                {
                    "asset_id": "MWK_1956_p0003_fig01",
                    "kind": "fig",
                    "ordinal": 1,
                    "caption": "Yield stress-strain curve of copper in compression",
                    "png_path": "figures/MWK_1956_p0003_fig01_yield-stress-strain-curve.png",
                    "status": "materialized",
                },
            ],
        )

        text = _MOD.strip_existing_asset_block(page_md)
        matches = _MOD.find_inline_matches(text)
        self.assertEqual(len(matches), 1, f"expected exactly one inline match; got {matches}")
        start, end, kind, body = matches[0]
        self.assertEqual(kind, "fig")
        self.assertIn("[1]", body, "body must include the nested citation [1]")
        self.assertTrue(body.rstrip().endswith("[1]."), f"body should end with the full marker including '[1].'; got {body!r}")

        # Synthesize the rewritten output the way main() does it.
        page_obj = materialized["assets"][0]
        replacement = _MOD.build_inline_replacement(page_obj, body)
        rewritten = text[:start] + replacement + text[end:]

        # Validate the resulting Markdown image has properly nested escaping.
        self.assertIn(
            "![Fig. 1.1 Yield stress-strain curve of copper in compression. After Cook and Larke \\[1\\].](figures/MWK_1956_p0003_fig01_yield-stress-strain-curve.png)",
            rewritten,
            f"expected escaped citation inside alt-text and clean link target; got:\n{rewritten}",
        )
        # Specifically: the link target must end with ".png)" not ".png).]" — i.e. no
        # trailing literal "].]" carryover from the regex stopping at the citation.
        self.assertNotIn(".png).]", rewritten, "trailing '].]' is the bug from the citation-aware match")
        self.assertNotIn(".png).", rewritten, "trailing '].' is the bug from the citation-aware match")

    def test_simple_figure_without_citation(self):
        page_md = "[FIGURE: Fig. 1.2 Stress-strain curve of the ideally plastic material.]\n"
        materialized = _materialized_page(
            3,
            [
                {
                    "kind": "fig",
                    "ordinal": 1,
                    "caption": "Stress-strain curve",
                    "png_path": "figures/x.png",
                    "status": "materialized",
                },
            ],
        )
        text = _MOD.strip_existing_asset_block(page_md)
        matches = _MOD.find_inline_matches(text)
        self.assertEqual(len(matches), 1)
        body = matches[0][3]
        replacement = _MOD.build_inline_replacement(materialized["assets"][0], body)
        rewritten = text[: matches[0][0]] + replacement + text[matches[0][1]:]
        self.assertIn("![Fig. 1.2 Stress-strain curve of the ideally plastic material.](figures/x.png)", rewritten)

    def test_non_canonical_markdown_image_form_is_drift_not_match(self):
        """The non-canonical `![Fig. ...]` markdown-image form is forbidden by
        skills/pdf2md-page/SKILL.md RULE 8. The tightened rewriter MUST NOT
        match it (matching would silently rewrite a skill-contract violation
        and let drift accumulate). Instead it is surfaced via detect_drift()
        as a warning the orchestrator and human reviewers can see."""
        page_md = "![Fig. 1.9 Types of creep curves [Andrade 1914] for various materials.]\n"
        text = _MOD.strip_existing_asset_block(page_md)

        # Canonical pattern matcher should find ZERO matches for this drift.
        matches = _MOD.find_inline_matches(text)
        self.assertEqual(len(matches), 0,
                         f"non-canonical ![Fig. ...] form must not be rewritten; got {matches}")

        # Drift detector should surface the drift.
        drift = _MOD.detect_drift(text)
        self.assertTrue(len(drift) >= 1,
                        f"non-canonical ![Fig. ...] form must be flagged as drift; got {drift}")
        labels = [label for label, _ in drift]
        self.assertTrue(
            any("markdown-image" in label for label in labels),
            f"drift label should call out markdown-image syntax; got labels {labels}",
        )

    def test_canonical_figure_with_complex_caption(self):
        """The canonical `[FIGURE: ...]` form with embedded citations still
        matches under tightening — case-sensitive uppercase FIGURE: required."""
        page_md = "[FIGURE: Fig. 1.9 Types of creep curves [Andrade 1914] for various materials.]\n"
        materialized = _materialized_page(
            10,
            [
                {
                    "kind": "fig",
                    "ordinal": 1,
                    "caption": "Types of creep curves",
                    "png_path": "figures/y.png",
                    "status": "materialized",
                },
            ],
        )
        text = _MOD.strip_existing_asset_block(page_md)
        matches = _MOD.find_inline_matches(text)
        self.assertEqual(len(matches), 1, f"canonical form should match; got {matches}")
        body = matches[0][3]
        self.assertIn("[Andrade 1914]", body)
        replacement = _MOD.build_inline_replacement(materialized["assets"][0], body)
        rewritten = text[: matches[0][0]] + replacement + text[matches[0][1]:]
        self.assertIn(
            "![Fig. 1.9 Types of creep curves \\[Andrade 1914\\] for various materials.](figures/y.png)",
            rewritten,
        )

    def test_table_with_citation_in_caption(self):
        page_md = "[TABLE: Table 4.2 Comparison of stress values [ASME 1955].]\n"
        materialized = _materialized_page(
            100,
            [
                {
                    "kind": "tbl",
                    "ordinal": 1,
                    "caption": "Comparison of stress values",
                    "xlsx_path": "tables/z.xlsx",
                    "png_path": "tables/z.png",
                    "status": "materialized",
                },
            ],
        )
        text = _MOD.strip_existing_asset_block(page_md)
        matches = _MOD.find_inline_matches(text)
        self.assertEqual(len(matches), 1)
        body = matches[0][3]
        self.assertIn("[ASME 1955]", body)
        replacement = _MOD.build_inline_replacement(materialized["assets"][0], body)
        rewritten = text[: matches[0][0]] + replacement + text[matches[0][1]:]
        self.assertIn("[XLSX](tables/z.xlsx)", rewritten)
        self.assertIn("[source crop](tables/z.png)", rewritten)
        # Bold span retains escaped nested brackets.
        self.assertIn("\\[ASME 1955\\]", rewritten)


if __name__ == "__main__":
    unittest.main(verbosity=2)
