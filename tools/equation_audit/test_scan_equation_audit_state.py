#!/usr/bin/env python3
"""
Unit tests for scan_equation_audit_state.py.

Covers the state counter the EQUATION_AUDIT persona consults at Gate 0
(resume state) and Gate 6 (close eligibility): overlap detection (entries
in 2+ sidecars), orphan-key warnings (sidecar references to equations no
longer present in equations.jsonl), per-page breakdown, and sidecar
fallback (canonical else latest export).

Run:
    python3 -m pytest tools/equation_audit/test_scan_equation_audit_state.py -v
"""

from __future__ import annotations

import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


_HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location(
    "scan_equation_audit_state", _HERE / "scan_equation_audit_state.py"
)
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules["scan_equation_audit_state"] = _MOD
_SPEC.loader.exec_module(_MOD)


def _run_scan(audit_root: Path) -> dict:
    """Invoke main() and return the parsed JSON output."""
    sys.argv = ["scan_equation_audit_state.py", "--audit-root", str(audit_root)]
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = _MOD.main()
    if rc != 0:
        raise RuntimeError(f"main() exited {rc}: {buf.getvalue()}")
    return json.loads(buf.getvalue())


def _make_audit(audit_root: Path, equations: list[dict],
                verified: dict | None = None,
                flagged: dict | None = None,
                backcheck: dict | None = None):
    """Build a minimal audit/equations/working/ fixture."""
    audit_root.mkdir(parents=True, exist_ok=True)
    with (audit_root / "equations.jsonl").open("w") as f:
        for e in equations:
            f.write(json.dumps(e) + "\n")
    if verified is not None:
        (audit_root / "verified.json").write_text(json.dumps(verified))
    if flagged is not None:
        (audit_root / "flagged.json").write_text(json.dumps(flagged))
    if backcheck is not None:
        (audit_root / "backcheck.json").write_text(json.dumps(backcheck))


class BasicCounts(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_scan_"))
        self.root = self.tmp / "working"
        equations = [
            {"page": 1, "hash": "aaaaaaaaaaaa"},
            {"page": 1, "hash": "bbbbbbbbbbbb"},
            {"page": 2, "hash": "cccccccccccc"},
            {"page": 2, "hash": "dddddddddddd"},
            {"page": 3, "hash": "eeeeeeeeeeee"},
        ]
        _make_audit(
            self.root, equations,
            verified={"1:aaaaaaaaaaaa": {"page": 1, "hash": "aaaaaaaaaaaa"}},
            flagged={"2:cccccccccccc": {"page": 2, "hash": "cccccccccccc"}},
            backcheck={},
        )

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_counts(self):
        d = _run_scan(self.root)
        self.assertEqual(d["total"], 5)
        self.assertEqual(d["verified"], 1)
        self.assertEqual(d["flagged"], 1)
        self.assertEqual(d["backcheck"], 0)
        self.assertEqual(d["unreviewed"], 3)
        self.assertEqual(d["overlaps"], 0)

    def test_per_page_breakdown(self):
        d = _run_scan(self.root)
        self.assertEqual(d["per_page"]["1"]["total"], 2)
        self.assertEqual(d["per_page"]["1"]["verified"], 1)
        self.assertEqual(d["per_page"]["1"]["unreviewed"], 1)
        self.assertEqual(d["per_page"]["2"]["flagged"], 1)
        self.assertEqual(d["per_page"]["2"]["unreviewed"], 1)
        self.assertEqual(d["per_page"]["3"]["total"], 1)
        self.assertEqual(d["per_page"]["3"]["unreviewed"], 1)


class OverlapDetection(unittest.TestCase):
    def test_equation_in_both_verified_and_flagged_counts_as_overlap(self):
        tmp = Path(tempfile.mkdtemp(prefix="test_scan_"))
        try:
            root = tmp / "working"
            _make_audit(
                root,
                equations=[{"page": 1, "hash": "aaaaaaaaaaaa"}],
                verified={"1:aaaaaaaaaaaa": {"page": 1, "hash": "aaaaaaaaaaaa"}},
                flagged={"1:aaaaaaaaaaaa": {"page": 1, "hash": "aaaaaaaaaaaa"}},
            )
            d = _run_scan(root)
            self.assertEqual(d["overlaps"], 1)
            # Both v and f are counted (set-based), but overlap field flags the anomaly
            self.assertEqual(d["verified"], 1)
            self.assertEqual(d["flagged"], 1)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class OrphanWarnings(unittest.TestCase):
    def test_sidecar_entries_for_missing_equations_become_warnings(self):
        tmp = Path(tempfile.mkdtemp(prefix="test_scan_"))
        try:
            root = tmp / "working"
            _make_audit(
                root,
                equations=[{"page": 1, "hash": "aaaaaaaaaaaa"}],
                verified={
                    "1:aaaaaaaaaaaa": {"page": 1, "hash": "aaaaaaaaaaaa"},
                    # Orphan: hash not in equations.jsonl
                    "9:ffffffffffff": {"page": 9, "hash": "ffffffffffff"},
                },
                flagged={
                    # Two orphans in flagged
                    "8:eeeeeeeeeeee": {"page": 8, "hash": "eeeeeeeeeeee"},
                    "7:dddddddddddd": {"page": 7, "hash": "dddddddddddd"},
                },
            )
            d = _run_scan(root)
            # Orphans excluded from active counts
            self.assertEqual(d["verified"], 1)  # only the matching one
            self.assertEqual(d["flagged"], 0)
            # Warnings present
            self.assertEqual(len(d["warnings"]), 2)  # one for verified, one for flagged
            self.assertTrue(any("verified" in w and "1 sidecar" in w for w in d["warnings"]))
            self.assertTrue(any("flagged" in w and "2 sidecar" in w for w in d["warnings"]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class SidecarFallback(unittest.TestCase):
    def test_uses_timestamped_export_when_canonical_empty(self):
        tmp = Path(tempfile.mkdtemp(prefix="test_scan_"))
        try:
            root = tmp / "working"
            _make_audit(
                root,
                equations=[{"page": 1, "hash": "aaaaaaaaaaaa"}],
                verified={},  # canonical empty
            )
            # Add a timestamped export with real state
            (root / "MWK_verified_2026-05-13-15-01-33.json").write_text(
                json.dumps({"1:aaaaaaaaaaaa": {"page": 1, "hash": "aaaaaaaaaaaa"}})
            )
            d = _run_scan(root)
            self.assertEqual(d["verified"], 1)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_uses_latest_when_multiple_exports(self):
        tmp = Path(tempfile.mkdtemp(prefix="test_scan_"))
        try:
            root = tmp / "working"
            _make_audit(
                root,
                equations=[
                    {"page": 1, "hash": "aaaaaaaaaaaa"},
                    {"page": 2, "hash": "bbbbbbbbbbbb"},
                ],
            )
            # Older export with 1 entry
            (root / "MWK_verified_2026-05-12-04-15-33.json").write_text(
                json.dumps({"1:aaaaaaaaaaaa": {"page": 1, "hash": "aaaaaaaaaaaa"}})
            )
            # Newer export with 2 entries
            (root / "MWK_verified_2026-05-13-15-01-33.json").write_text(
                json.dumps({
                    "1:aaaaaaaaaaaa": {"page": 1, "hash": "aaaaaaaaaaaa"},
                    "2:bbbbbbbbbbbb": {"page": 2, "hash": "bbbbbbbbbbbb"},
                })
            )
            d = _run_scan(root)
            self.assertEqual(d["verified"], 2)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class FailureModes(unittest.TestCase):
    def test_missing_audit_root_exits_2(self):
        sys.argv = ["scan_equation_audit_state.py", "--audit-root", "/tmp/nonexistent_qq"]
        self.assertEqual(_MOD.main(), 2)

    def test_missing_equations_jsonl_exits_3(self):
        tmp = Path(tempfile.mkdtemp(prefix="test_scan_"))
        try:
            (tmp / "verified.json").write_text("{}")
            sys.argv = ["scan_equation_audit_state.py", "--audit-root", str(tmp)]
            self.assertEqual(_MOD.main(), 3)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
