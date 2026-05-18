"""Tests for tools.source_audit.sidecar."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.source_audit import sidecar


class ContentHash(unittest.TestCase):
    def test_stable_and_12_chars(self):
        h = sidecar.content_hash("hello world")
        self.assertEqual(len(h), 12)
        self.assertEqual(h, sidecar.content_hash("hello world"))

    def test_strip_normalizes(self):
        self.assertEqual(
            sidecar.content_hash("hello"),
            sidecar.content_hash("  hello  "),
        )

    def test_content_change_changes_hash(self):
        self.assertNotEqual(
            sidecar.content_hash("a"),
            sidecar.content_hash("b"),
        )


class LoadSidecar(unittest.TestCase):
    def test_missing_returns_empty(self):
        self.assertEqual(sidecar.load_sidecar(Path("/nonexistent.json")), {})

    def test_invalid_json_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.json"
            p.write_text("not json", encoding="utf-8")
            self.assertEqual(sidecar.load_sidecar(p), {})

    def test_empty_dict_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "empty.json"
            p.write_text("{}", encoding="utf-8")
            self.assertEqual(sidecar.load_sidecar(p), {})

    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "x.json"
            payload = {"k": {"a": 1}}
            p.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(sidecar.load_sidecar(p), payload)


class LoadSidecarWithFallback(unittest.TestCase):
    def test_canonical_flat_preferred(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp)
            (audit / "figures_verified.json").write_text(
                json.dumps({"canonical": True}), encoding="utf-8"
            )
            (audit / "src_figures_verified_2025-01-01.json").write_text(
                json.dumps({"canonical": False}), encoding="utf-8"
            )
            data = sidecar.load_sidecar_with_fallback(audit, "figures_verified")
            self.assertTrue(data["canonical"])

    def test_exported_flat_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp)
            (audit / "src_figures_verified_2025-01-01.json").write_text(
                json.dumps({"v": 1}), encoding="utf-8"
            )
            (audit / "src_figures_verified_2025-02-01.json").write_text(
                json.dumps({"v": 2}), encoding="utf-8"
            )
            data = sidecar.load_sidecar_with_fallback(audit, "figures_verified")
            self.assertEqual(data["v"], 2)

    def test_nested_working_dir_searched(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp)
            nested = audit / "equations" / "working"
            nested.mkdir(parents=True)
            (nested / "verified.json").write_text(
                json.dumps({"from_nested": True}), encoding="utf-8"
            )
            data = sidecar.load_sidecar_with_fallback(audit, "verified")
            self.assertTrue(data["from_nested"])

    def test_returns_empty_when_no_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                sidecar.load_sidecar_with_fallback(Path(tmp), "nope"), {}
            )

    def test_canonical_flat_beats_nested(self):
        """Canonical flat layout takes precedence over nested when both exist."""
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp)
            (audit / "verified.json").write_text(
                json.dumps({"location": "flat"}), encoding="utf-8"
            )
            nested = audit / "equations" / "working"
            nested.mkdir(parents=True)
            (nested / "verified.json").write_text(
                json.dumps({"location": "nested"}), encoding="utf-8"
            )
            data = sidecar.load_sidecar_with_fallback(audit, "verified")
            self.assertEqual(data["location"], "flat")


if __name__ == "__main__":
    unittest.main()
