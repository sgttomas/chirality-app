#!/usr/bin/env python3
"""
Unit tests for migrate_csv_assets_to_archive.py.

Covers:
  - happy path: paired .csv + .xlsx → .csv moved to .archive/
  - idempotence: second run after first is a no-op
  - refusal: .csv without paired .xlsx → exit 3, no files moved
  - directory structure: .archive/ created beside the csvs
  - dry-run does not move anything

Run:
    python3 -m pytest tools/pdf2md/test_migrate_csv_assets_to_archive.py -v
"""

from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


_HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location(
    "migrate_csv_assets_to_archive", _HERE / "migrate_csv_assets_to_archive.py"
)
_MOD = importlib.util.module_from_spec(_SPEC)
sys.modules["migrate_csv_assets_to_archive"] = _MOD
_SPEC.loader.exec_module(_MOD)


def _seed(tmp: Path, *, csvs: list[str], xlsxs: list[str]) -> Path:
    tables = tmp / "tables"
    tables.mkdir()
    for name in csvs:
        (tables / name).write_text("a,b\n1,2\n", encoding="utf-8")
    for name in xlsxs:
        (tables / name).write_bytes(b"x")
    return tables


def _run(tables_dir: Path, *, dry_run: bool = False) -> int:
    argv = ["migrate_csv_assets_to_archive.py", "--tables-dir", str(tables_dir)]
    if dry_run:
        argv.append("--dry-run")
    sys.argv = argv
    return _MOD.main()


class HappyPath(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="migrate_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_paired_csv_xlsx_moved_to_archive(self):
        tables = _seed(self.tmp, csvs=["t1.csv"], xlsxs=["t1.xlsx"])
        rc = _run(tables)
        self.assertEqual(rc, 0)
        self.assertFalse((tables / "t1.csv").exists())
        self.assertTrue((tables / ".archive" / "t1.csv").is_file())
        self.assertTrue((tables / "t1.xlsx").is_file())

    def test_multiple_csvs_all_archived(self):
        tables = _seed(
            self.tmp,
            csvs=["a.csv", "b.csv", "c.csv"],
            xlsxs=["a.xlsx", "b.xlsx", "c.xlsx"],
        )
        rc = _run(tables)
        self.assertEqual(rc, 0)
        for name in ("a.csv", "b.csv", "c.csv"):
            self.assertTrue((tables / ".archive" / name).is_file())

    def test_second_run_is_no_op(self):
        tables = _seed(self.tmp, csvs=["t.csv"], xlsxs=["t.xlsx"])
        self.assertEqual(_run(tables), 0)
        self.assertEqual(_run(tables), 0)  # idempotent

    def test_no_csvs_returns_zero(self):
        tables = _seed(self.tmp, csvs=[], xlsxs=["t.xlsx"])
        self.assertEqual(_run(tables), 0)


class RefusalAndErrors(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="migrate_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_csv_without_xlsx_refused_exit_3(self):
        tables = _seed(self.tmp, csvs=["orphan.csv"], xlsxs=[])
        rc = _run(tables)
        self.assertEqual(rc, 3)
        # Nothing should have moved.
        self.assertTrue((tables / "orphan.csv").is_file())
        self.assertFalse((tables / ".archive").exists())

    def test_mixed_paired_and_orphan_refuses_all(self):
        """One missing-XLSX poisons the whole run — operator must resolve
        before any migration happens (forensic safety)."""
        tables = _seed(
            self.tmp,
            csvs=["paired.csv", "orphan.csv"],
            xlsxs=["paired.xlsx"],
        )
        rc = _run(tables)
        self.assertEqual(rc, 3)
        self.assertTrue((tables / "paired.csv").is_file())
        self.assertTrue((tables / "orphan.csv").is_file())

    def test_missing_dir_exit_2(self):
        sys.argv = ["migrate_csv_assets_to_archive.py", "--tables-dir", str(self.tmp / "nope")]
        self.assertEqual(_MOD.main(), 2)


class DryRun(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="migrate_"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_dry_run_does_not_move_anything(self):
        tables = _seed(self.tmp, csvs=["t.csv"], xlsxs=["t.xlsx"])
        rc = _run(tables, dry_run=True)
        self.assertEqual(rc, 0)
        self.assertTrue((tables / "t.csv").is_file())
        self.assertFalse((tables / ".archive").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
