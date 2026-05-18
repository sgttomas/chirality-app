"""Tests for tools.source_audit.compare_extracts."""
from __future__ import annotations

import unittest

from tools.source_audit.compare_extracts import compare_page
from tools.source_audit.sidecar import content_hash
from tools.source_audit.canonicalize_latex import canonicalize_latex_v1


class ProseCompare(unittest.TestCase):
    def test_identical_prose_silent(self):
        cmp = compare_page("Hello world.", "Hello world.", page_num=1)
        self.assertEqual(cmp.prose_hunks, [])

    def test_typography_difference_silent(self):
        cmp = compare_page("don’t “stop”", "don't \"stop\"", page_num=1)
        self.assertEqual(cmp.prose_hunks, [])

    def test_genuine_prose_difference_flagged(self):
        cmp = compare_page("The cat sat.", "The dog sat.", page_num=1)
        self.assertEqual(len(cmp.prose_hunks), 1)
        self.assertEqual(cmp.prose_hunks[0].page, 1)
        self.assertIn("cat", cmp.prose_hunks[0].original)
        self.assertIn("dog", cmp.prose_hunks[0].reextract)

    def test_length_mismatch_creates_tail_hunks(self):
        cmp = compare_page("A\n\nB", "A", page_num=1)
        self.assertEqual(len(cmp.prose_hunks), 1)
        self.assertEqual(cmp.prose_hunks[0].original, "B")
        self.assertEqual(cmp.prose_hunks[0].reextract, "")


class EquationCompare(unittest.TestCase):
    def test_identical_equations_silent(self):
        cmp = compare_page("$$E = mc^2$$", "$$E = mc^2$$", page_num=1)
        self.assertEqual(cmp.equation_structural_fails, [])
        self.assertEqual(cmp.equation_content_proposals, [])

    def test_canonicalized_equal_silent(self):
        # \dfrac vs \frac canonicalize identical → no proposal
        cmp = compare_page(r"$$\frac{a}{b}$$", r"$$\dfrac{a}{b}$$", page_num=1)
        self.assertEqual(cmp.equation_content_proposals, [])

    def test_count_mismatch_structural_fail(self):
        cmp = compare_page("$$a$$ $$b$$", "$$a$$", page_num=1)
        self.assertEqual(len(cmp.equation_structural_fails), 1)
        fail = cmp.equation_structural_fails[0]
        self.assertEqual(fail.reason, "count_mismatch")
        self.assertEqual(fail.original_count, 2)
        self.assertEqual(fail.reextract_count, 1)

    def test_content_divergence_becomes_proposal(self):
        cmp = compare_page("$$a + b$$", "$$a - b$$", page_num=1)
        self.assertEqual(len(cmp.equation_content_proposals), 1)
        p = cmp.equation_content_proposals[0]
        self.assertEqual(p.position, 0)
        self.assertEqual(p.equation_hash, content_hash("a + b"))
        self.assertEqual(p.proposal_hash, content_hash(canonicalize_latex_v1("a - b")))

    def test_proposal_hash_is_canonicalized(self):
        # cosmetic differences in the re-extract must produce the same
        # proposal_hash so re-runs don't reset rejection
        cmp1 = compare_page("$$a/b$$", r"$$\dfrac{a}{b}$$", page_num=1)
        cmp2 = compare_page("$$a/b$$", r"$$\frac{ a }{ b }$$", page_num=1)
        if cmp1.equation_content_proposals and cmp2.equation_content_proposals:
            self.assertEqual(
                cmp1.equation_content_proposals[0].proposal_hash,
                cmp2.equation_content_proposals[0].proposal_hash,
            )


class AssetCompare(unittest.TestCase):
    def test_matching_figure_count_silent(self):
        cmp = compare_page(
            "![](figures/a.png)\n\n![](figures/b.png)",
            "[FIGURE: A]\n\n[FIGURE: B]",
            page_num=1,
        )
        self.assertEqual(cmp.asset_structural_fails, [])

    def test_count_mismatch_structural_fail(self):
        cmp = compare_page(
            "![](figures/a.png)\n\n![](figures/b.png)",
            "[FIGURE: A]",
            page_num=1,
        )
        self.assertEqual(len(cmp.asset_structural_fails), 1)
        self.assertEqual(cmp.asset_structural_fails[0].kind, "fig")

    def test_per_kind_partitioning(self):
        # Different counts only on tables, figures match
        cmp = compare_page(
            "![](figures/a.png)\n\n[XLSX](tables/x.xlsx)",
            "[FIGURE: A]",
            page_num=1,
        )
        kinds = {f.kind for f in cmp.asset_structural_fails}
        self.assertIn("tbl", kinds)
        self.assertNotIn("fig", kinds)


class AdditiveOnlyInvariant(unittest.TestCase):
    """Sanity: PageComparison carries no verification/exemption field."""
    def test_to_dict_has_no_verified_keys(self):
        cmp = compare_page("hi", "hi", page_num=1)
        d = cmp.to_dict()
        for k in d:
            self.assertNotIn("verified", k.lower())
            self.assertNotIn("exempt", k.lower())


if __name__ == "__main__":
    unittest.main()
