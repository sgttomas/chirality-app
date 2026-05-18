"""Tests for tools.source_audit.chunk and tools.source_audit.page_strip."""
from __future__ import annotations

import unittest

from tools.source_audit import chunk, page_strip


class RenderChunkControls(unittest.TestCase):
    def test_includes_three_radios(self):
        out = chunk.render_chunk_controls("k1", "unreviewed", "")
        self.assertIn('value="unreviewed"', out)
        self.assertIn('value="verified"', out)
        self.assertIn('value="flagged"', out)

    def test_note_escaped(self):
        out = chunk.render_chunk_controls("k1", "flagged", "<script>x</script>")
        self.assertNotIn("<script>x", out)
        self.assertIn("&lt;script&gt;x", out)

    def test_radio_name_includes_key(self):
        out = chunk.render_chunk_controls("my-key", "unreviewed", "")
        self.assertIn('name="s_my-key"', out)


class InitialStatusForKey(unittest.TestCase):
    def test_verified_takes_precedence(self):
        s, n = chunk.initial_status_for_key("k", {"k": {}}, {"k": {"description": "x"}})
        self.assertEqual(s, "verified")
        self.assertEqual(n, "")

    def test_flagged_returns_description(self):
        s, n = chunk.initial_status_for_key("k", {}, {"k": {"description": "fix this"}})
        self.assertEqual(s, "flagged")
        self.assertEqual(n, "fix this")

    def test_flagged_falls_back_to_note(self):
        s, n = chunk.initial_status_for_key("k", {}, {"k": {"note": "legacy"}})
        self.assertEqual(s, "flagged")
        self.assertEqual(n, "legacy")

    def test_unknown_key_unreviewed(self):
        s, n = chunk.initial_status_for_key("k", {}, {})
        self.assertEqual(s, "unreviewed")
        self.assertEqual(n, "")


class RenderPageSection(unittest.TestCase):
    def test_anchor_and_count(self):
        out = page_strip.render_page_section(47, "pages/page_0047.png", "<div class='chunk'/>", 3)
        self.assertIn('id="p47"', out)
        self.assertIn("Page 47", out)
        self.assertIn("(3)", out)
        self.assertIn("pages/page_0047.png", out)

    def test_nav_links(self):
        out = page_strip.render_nav([1, 5, 12])
        self.assertIn('href="#p1"', out)
        self.assertIn('href="#p5"', out)
        self.assertIn('href="#p12"', out)


if __name__ == "__main__":
    unittest.main()
