"""ROLE prototype receipts stay outside Work; explicit fixtures remain writable."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "app/contract_inputs/PKG-02/DEL-02-04/Work"
EXAMPLES = (
    "role-supply-record.valid.example.json", "role-supply-record.invalid.examples.json",
    "role-limit-account.valid.example.json", "role-limit-account.invalid.examples.json",
)


def snapshot(work):
    return {p.relative_to(work).as_posix(): p.read_bytes() for p in work.rglob("*") if p.is_file()}


@pytest.fixture
def case(tmp_path):
    work = tmp_path / "Work"
    shutil.copytree(WORK, work, ignore=shutil.ignore_patterns("__pycache__"))
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    return work, scratch


def run(case, *args):
    work, scratch = case
    env = {**os.environ, "TMPDIR": str(scratch), "CODEX_HOME": str(scratch / "codex-home")}
    env.pop("PYTHONDONTWRITEBYTECODE", None)
    return subprocess.run([sys.executable, str(work / "prototype/run_cases.py"), *args],
                          env=env, capture_output=True, text=True)


@pytest.mark.parametrize("options", [(), ("--record",), ("--record-output",)])
def test_default_and_receipt_modes_preserve_work(case, options):
    work, scratch = case
    before = snapshot(work)
    args = [*options, str(scratch / "explicit.txt")] if options == ("--record-output",) else options
    result = run(case, *args)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "fail=0" in result.stdout
    assert snapshot(work) == before
    receipts = list(scratch.rglob("*.txt"))
    assert len(receipts) == bool(options)
    if options:
        assert "TOTAL pass=" in receipts[0].read_text()
        assert f"Receipt: {receipts[0]}" in result.stdout


def test_explicit_fixture_output_still_regenerates_all_four_examples(case):
    work, _ = case
    for name in EXAMPLES:
        (work / name).write_text("fixture to regenerate\n")
    before = snapshot(work)
    result = run(case, "--write-examples", "--record")
    assert result.returncode == 0, result.stdout + result.stderr
    after = snapshot(work)
    assert {p for p in before if before[p] != after[p]} == set(EXAMPLES)
    assert all(isinstance(json.loads((work / name).read_text()), (dict, list)) for name in EXAMPLES)
    assert "fail=0" in result.stdout


@pytest.mark.parametrize("kind", ["work", "symlink", "existing"])
def test_receipt_cannot_write_work_or_overwrite_evidence(case, kind):
    work, scratch = case
    if kind == "work":
        output = work / "prototype/results/new.txt"
    elif kind == "symlink":
        alias = scratch / "alias"
        alias.symlink_to(work, target_is_directory=True)
        output = alias / "new.txt"
    else:
        output = scratch / "retained.txt"
        output.write_text("retained evidence\n")
    before = snapshot(work)
    result = run(case, "--record-output", str(output))
    assert result.returncode == 2
    assert snapshot(work) == before
    if kind == "existing":
        assert output.read_text() == "retained evidence\n"
