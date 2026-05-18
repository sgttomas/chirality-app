#!/usr/bin/env python3
"""
Unit tests for prune_old_snapshots.py.

The tool prunes accumulated audit artifacts (snapshot directories,
timestamped export JSONs, .bak archives) while never touching the live
canonical state or anything inside an immutable snapshot. Tests build
isolated tmpdir fixtures and verify the keep-N behaviour, idempotence,
the dry-run safety net, the --snapshots-only / --exports-only modes,
and that protected files are NEVER deleted.

Run:
    python3 -m pytest tools/equation_audit/test_prune_old_snapshots.py -v
"""

from __future__ import annotations

import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


_HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location(
    "prune_old_snapshots", _HERE / "prune_old_snapshots.py"
)
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules["prune_old_snapshots"] = _MOD
_SPEC.loader.exec_module(_MOD)


def _make_audit_root(tmp: Path, *,
                     snapshots: int = 0,
                     verified_exports: int = 0,
                     flagged_exports: int = 0,
                     backcheck_exports: int = 0,
                     baks: int = 0) -> Path:
    """Build a synthetic `audit/equations/` layout with N artifacts.

    Names embed a numerical timestamp so lexicographic sort matches
    chronological sort (which mirrors the real-world filenames).
    """
    root = tmp / "equations"
    working = root / "working"
    snaps = root / "snapshots"
    working.mkdir(parents=True)
    snaps.mkdir(parents=True)

    # Always create the canonical-live-state files; tests assert these survive.
    (root / "_LATEST.md").write_text("pointer\n")
    (working / "equations.html").write_text("<html/>")
    (working / "equations.jsonl").write_text("{}\n")
    (working / "verified.json").write_text("{}")
    (working / "flagged.json").write_text("{}")
    (working / "backcheck.json").write_text("{}")

    for i in range(snapshots):
        # ISO-like timestamps: 2026-05-{01..N}_HHMM
        name = f"EQ_BOOK_2026-05-{(i+1):02d}_1200"
        (snaps / name).mkdir()
        (snaps / name / "RUN_SUMMARY.md").write_text("ok")

    def _stamp(kind: str, n: int) -> None:
        for i in range(n):
            ts = f"2026-05-{(i+1):02d}-12-00-00"
            (working / f"BOOK_{kind}_{ts}.json").write_text("{}")

    _stamp("verified", verified_exports)
    _stamp("flagged", flagged_exports)
    _stamp("backcheck", backcheck_exports)

    for i in range(baks):
        ts = f"20260501T1200{i:02d}"
        (working / f"flagged.json.{ts}.bak").write_text("{}")

    return root


def _run_main(audit_root: Path, *extra) -> tuple[int, dict]:
    sys.argv = ["prune_old_snapshots.py", "--audit-root", str(audit_root), *extra]
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = _MOD.main()
    output = buf.getvalue().strip()
    parsed = json.loads(output) if output else {}
    return rc, parsed


class KeepBehaviour(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_prune_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_keep_default_20_when_fewer_present_is_noop(self):
        root = _make_audit_root(self.tmp, snapshots=5, verified_exports=5,
                                flagged_exports=5, backcheck_exports=5, baks=5)
        rc, plan = _run_main(root)
        self.assertEqual(rc, 0)
        self.assertEqual(plan["removed_count"], 0)
        # All five snapshots still on disk
        self.assertEqual(len(list((root / "snapshots").iterdir())), 5)

    def test_keep_20_with_25_snapshots_prunes_5_oldest(self):
        root = _make_audit_root(self.tmp, snapshots=25)
        rc, plan = _run_main(root)
        self.assertEqual(rc, 0)
        self.assertEqual(plan["removed_count"], 5)
        remaining = sorted(p.name for p in (root / "snapshots").iterdir())
        self.assertEqual(len(remaining), 20)
        # The five oldest (May 1..5) are gone
        for i in range(1, 6):
            self.assertNotIn(f"EQ_BOOK_2026-05-{i:02d}_1200", remaining)
        # The newest (May 25) is kept
        self.assertIn("EQ_BOOK_2026-05-25_1200", remaining)

    def test_keep_custom_value_3(self):
        root = _make_audit_root(self.tmp, snapshots=10)
        rc, plan = _run_main(root, "--keep", "3")
        self.assertEqual(rc, 0)
        self.assertEqual(plan["removed_count"], 7)
        self.assertEqual(len(list((root / "snapshots").iterdir())), 3)

    def test_per_kind_keep_window(self):
        """Each export kind (verified/flagged/backcheck) gets its own keep window —
        we don't pool them into a single global window."""
        root = _make_audit_root(self.tmp, verified_exports=25, flagged_exports=5,
                                backcheck_exports=25, baks=25)
        rc, plan = _run_main(root)
        self.assertEqual(rc, 0)
        # Pruned: 5 verified + 5 backcheck + 5 baks = 15. Flagged untouched (only 5).
        self.assertEqual(plan["removed_count"], 15)
        working = root / "working"
        self.assertEqual(len(list(working.glob("BOOK_verified_*.json"))), 20)
        self.assertEqual(len(list(working.glob("BOOK_flagged_*.json"))), 5)
        self.assertEqual(len(list(working.glob("BOOK_backcheck_*.json"))), 20)
        self.assertEqual(len(list(working.glob("*.bak"))), 20)


class DryRun(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_prune_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_dry_run_reports_plan_without_deleting(self):
        root = _make_audit_root(self.tmp, snapshots=25)
        snapshots_before = sorted(p.name for p in (root / "snapshots").iterdir())
        rc, plan = _run_main(root, "--dry-run")
        self.assertEqual(rc, 0)
        self.assertEqual(plan["status"], "dry_run")
        self.assertEqual(plan["would_remove_count"], 5)
        self.assertNotIn("removed", plan)  # only `would_remove` in dry-run
        snapshots_after = sorted(p.name for p in (root / "snapshots").iterdir())
        self.assertEqual(snapshots_before, snapshots_after)


class Idempotence(unittest.TestCase):
    def test_second_run_is_noop(self):
        tmp = Path(tempfile.mkdtemp(prefix="test_prune_"))
        try:
            root = _make_audit_root(tmp, snapshots=25, baks=25)
            rc, plan1 = _run_main(root)
            self.assertEqual(rc, 0)
            self.assertGreater(plan1["removed_count"], 0)
            rc2, plan2 = _run_main(root)
            self.assertEqual(rc2, 0)
            self.assertEqual(plan2["removed_count"], 0)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class ScopeFlags(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_prune_"))
        self.root = _make_audit_root(self.tmp, snapshots=25, verified_exports=25,
                                     flagged_exports=25, backcheck_exports=25,
                                     baks=25)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_snapshots_only_leaves_exports_intact(self):
        rc, plan = _run_main(self.root, "--snapshots-only")
        self.assertEqual(rc, 0)
        # 5 snapshots pruned; exports / baks untouched (25 of each remain)
        self.assertEqual(plan["removed_count"], 5)
        working = self.root / "working"
        self.assertEqual(len(list(working.glob("BOOK_verified_*.json"))), 25)
        self.assertEqual(len(list(working.glob("BOOK_flagged_*.json"))), 25)
        self.assertEqual(len(list(working.glob("BOOK_backcheck_*.json"))), 25)
        self.assertEqual(len(list(working.glob("*.bak"))), 25)
        self.assertEqual(len(list((self.root / "snapshots").iterdir())), 20)

    def test_exports_only_leaves_snapshots_intact(self):
        rc, plan = _run_main(self.root, "--exports-only")
        self.assertEqual(rc, 0)
        # 5*4 = 20 export+bak files pruned; snapshots untouched
        self.assertEqual(plan["removed_count"], 20)
        self.assertEqual(len(list((self.root / "snapshots").iterdir())), 25)

    def test_mutually_exclusive(self):
        sys.argv = [
            "prune_old_snapshots.py",
            "--audit-root", str(self.root),
            "--snapshots-only", "--exports-only",
        ]
        # argparse exits 2 for mutually-exclusive violation
        with self.assertRaises(SystemExit) as ctx:
            _MOD.main()
        self.assertEqual(ctx.exception.code, 2)


class ProtectedFiles(unittest.TestCase):
    """Live canonical state and snapshot contents must NEVER be touched."""

    def test_canonical_state_files_survive(self):
        tmp = Path(tempfile.mkdtemp(prefix="test_prune_"))
        try:
            root = _make_audit_root(tmp, snapshots=25, verified_exports=25, baks=25)
            _run_main(root)
            # All canonical files still present
            self.assertTrue((root / "_LATEST.md").is_file())
            for name in ("equations.html", "equations.jsonl",
                         "verified.json", "flagged.json", "backcheck.json"):
                self.assertTrue((root / "working" / name).is_file(), f"missing: {name}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_snapshot_internal_files_not_touched(self):
        """Even when a snapshot dir is kept, we never reach into it."""
        tmp = Path(tempfile.mkdtemp(prefix="test_prune_"))
        try:
            root = _make_audit_root(tmp, snapshots=25)
            kept_dir = root / "snapshots" / "EQ_BOOK_2026-05-25_1200"
            self.assertTrue((kept_dir / "RUN_SUMMARY.md").is_file())
            _run_main(root)
            self.assertTrue((kept_dir / "RUN_SUMMARY.md").is_file())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_unrelated_top_level_directory_preserved(self):
        """proposals/, .archive/, pages symlink — none of these are pruning targets."""
        tmp = Path(tempfile.mkdtemp(prefix="test_prune_"))
        try:
            root = _make_audit_root(tmp, snapshots=25)
            # Drop a sibling directory that resembles legacy / unrelated state
            sibling = root / "proposals"
            sibling.mkdir()
            (sibling / "p1.json").write_text("{}")
            _run_main(root)
            self.assertTrue(sibling.is_dir())
            self.assertTrue((sibling / "p1.json").is_file())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class FailureModes(unittest.TestCase):
    def test_missing_audit_root_exits_2(self):
        sys.argv = ["prune_old_snapshots.py", "--audit-root", "/tmp/nonexistent_qqz"]
        self.assertEqual(_MOD.main(), 2)

    def test_keep_zero_rejected(self):
        tmp = Path(tempfile.mkdtemp(prefix="test_prune_"))
        try:
            root = _make_audit_root(tmp)
            sys.argv = ["prune_old_snapshots.py", "--audit-root", str(root),
                        "--keep", "0"]
            self.assertEqual(_MOD.main(), 2)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_missing_working_and_snapshots_subdirs_is_noop(self):
        """If the audit root has no working/ or snapshots/, nothing to do."""
        tmp = Path(tempfile.mkdtemp(prefix="test_prune_"))
        try:
            root = tmp / "equations"
            root.mkdir()
            rc, plan = _run_main(root)
            self.assertEqual(rc, 0)
            self.assertEqual(plan["removed_count"], 0)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
