#!/usr/bin/env python3
"""
Unit tests for migrate_audit_layout.py.

The migration is destructive (moves files; not idempotent without the
explicit check) so the tests build isolated tmpdir layouts and verify:
  - fresh migration produces the canonical structure
  - re-run after migration is a no-op (`already_migrated`)
  - name collisions between top-level and target are refused (exit 3)
  - `pages` symlink and unrelated subdirs are NEVER touched
  - dry-run mode does not modify the filesystem

Run:
    python3 -m pytest tools/equation_audit/test_migrate_audit_layout.py -v
"""

from __future__ import annotations

import importlib.util
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


_HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location(
    "migrate_audit_layout", _HERE / "migrate_audit_layout.py"
)
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules["migrate_audit_layout"] = _MOD
_SPEC.loader.exec_module(_MOD)


def _make_legacy(audit: Path, with_archive: bool = False,
                 with_pages: bool = True, with_proposals: bool = False) -> None:
    """Build a legacy flat audit/ layout for testing."""
    audit.mkdir(parents=True, exist_ok=True)
    (audit / "equations.html").write_text("<html></html>")
    (audit / "equations.jsonl").write_text('{"page": 1, "hash": "abc"}\n')
    (audit / "verified.json").write_text("{}")
    (audit / "flagged.json").write_text("{}")
    (audit / "backcheck.json").write_text("{}")
    (audit / "MWK_1956_verified_2026-05-12-04-15-33.json").write_text('{"k": "v"}')
    (audit / "MWK_1956_flagged_2026-05-12-04-15-33.json").write_text('{"k": "v"}')
    (audit / "flagged.json.20260511T220605.bak").write_text('{"bak": true}')
    if with_archive:
        archive = audit / ".archive"
        archive.mkdir()
        (archive / "old.json").write_text("{}")
    if with_pages:
        target = audit.parent / "page_work"
        target.mkdir(exist_ok=True)
        (audit / "pages").symlink_to(target)
    if with_proposals:
        prop = audit / "proposals"
        prop.mkdir()
        (prop / "p1.json").write_text("{}")


class FreshMigration(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_migrate_"))
        self.audit = self.tmp / "audit"
        _make_legacy(self.audit, with_archive=True, with_pages=True, with_proposals=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_fresh_migration_creates_canonical_layout(self):
        sys.argv = ["migrate_audit_layout.py", "--source-audit-dir", str(self.audit)]
        rc = _MOD.main()
        self.assertEqual(rc, 0)
        # Canonical layout
        self.assertTrue((self.audit / "equations" / "working").is_dir())
        self.assertTrue((self.audit / "equations" / "snapshots").is_dir())
        self.assertTrue((self.audit / "equations" / "_LATEST.md").is_file())
        # State files moved into working/
        for name in ["equations.html", "equations.jsonl", "verified.json",
                     "flagged.json", "backcheck.json",
                     "MWK_1956_verified_2026-05-12-04-15-33.json",
                     "MWK_1956_flagged_2026-05-12-04-15-33.json",
                     "flagged.json.20260511T220605.bak"]:
            self.assertTrue((self.audit / "equations" / "working" / name).exists(),
                           f"missing: {name}")
        # .archive moved into working/
        self.assertTrue((self.audit / "equations" / "working" / ".archive").is_dir())
        self.assertTrue((self.audit / "equations" / "working" / ".archive" / "old.json").exists())

    def test_pages_symlink_preserved(self):
        sys.argv = ["migrate_audit_layout.py", "--source-audit-dir", str(self.audit)]
        _MOD.main()
        # symlink should still be at top level, NOT moved into working/
        self.assertTrue((self.audit / "pages").is_symlink())
        self.assertFalse((self.audit / "equations" / "working" / "pages").exists())

    def test_proposals_dir_preserved(self):
        sys.argv = ["migrate_audit_layout.py", "--source-audit-dir", str(self.audit)]
        _MOD.main()
        # proposals/ is unrelated; should remain at top level
        self.assertTrue((self.audit / "proposals").is_dir())
        self.assertTrue((self.audit / "proposals" / "p1.json").exists())
        self.assertFalse((self.audit / "equations" / "working" / "proposals").exists())

    def test_latest_stub_pointer_created(self):
        sys.argv = ["migrate_audit_layout.py", "--source-audit-dir", str(self.audit)]
        _MOD.main()
        latest = (self.audit / "equations" / "_LATEST.md").read_text()
        self.assertIn("no snapshot yet", latest)


class Idempotence(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_migrate_"))
        self.audit = self.tmp / "audit"
        _make_legacy(self.audit, with_archive=True)
        sys.argv = ["migrate_audit_layout.py", "--source-audit-dir", str(self.audit)]
        _MOD.main()  # initial migration

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_rerun_after_migration_returns_already_migrated(self):
        plan = _MOD.survey(self.audit)
        self.assertTrue(plan.is_noop)
        # Run main again — should exit 0 (no error) with already_migrated status
        sys.argv = ["migrate_audit_layout.py", "--source-audit-dir", str(self.audit)]
        rc = _MOD.main()
        self.assertEqual(rc, 0)


class CollisionRefusal(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test_migrate_"))
        self.audit = self.tmp / "audit"
        _make_legacy(self.audit, with_archive=False)
        sys.argv = ["migrate_audit_layout.py", "--source-audit-dir", str(self.audit)]
        _MOD.main()  # initial migration
        # Re-introduce a top-level file with same name as one inside working/
        (self.audit / "verified.json").write_text('{"collision": true}')

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_collision_refused_with_exit_3(self):
        sys.argv = ["migrate_audit_layout.py", "--source-audit-dir", str(self.audit)]
        rc = _MOD.main()
        self.assertEqual(rc, 3)
        # The top-level file remains untouched (not silently merged or overwritten)
        self.assertTrue((self.audit / "verified.json").exists())


class NoLegacyState(unittest.TestCase):
    def test_no_legacy_files_returns_no_legacy_state(self):
        tmp = Path(tempfile.mkdtemp(prefix="test_migrate_"))
        try:
            audit = tmp / "audit"
            audit.mkdir(parents=True)
            # Only a `pages` symlink — no equation state at all
            target = audit.parent / "page_work"
            target.mkdir()
            (audit / "pages").symlink_to(target)
            sys.argv = ["migrate_audit_layout.py", "--source-audit-dir", str(audit)]
            rc = _MOD.main()
            self.assertEqual(rc, 0)
            # No equations/ directory should have been created when there's nothing to migrate
            self.assertFalse((audit / "equations").exists())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class DryRun(unittest.TestCase):
    def test_dry_run_does_not_touch_filesystem(self):
        tmp = Path(tempfile.mkdtemp(prefix="test_migrate_"))
        try:
            audit = tmp / "audit"
            _make_legacy(audit, with_archive=True)
            files_before = sorted(os.listdir(audit))
            sys.argv = ["migrate_audit_layout.py", "--source-audit-dir", str(audit),
                        "--dry-run"]
            rc = _MOD.main()
            self.assertEqual(rc, 0)
            files_after = sorted(os.listdir(audit))
            self.assertEqual(files_before, files_after,
                             "dry-run must not modify the filesystem")
            self.assertFalse((audit / "equations").exists())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
