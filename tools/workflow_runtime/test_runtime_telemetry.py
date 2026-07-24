import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).with_name("runtime_telemetry.py")


def record(run_root: Path, event_id: str, event_type: str, outcome: str, timestamp: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "record",
            "--run-root",
            str(run_root),
            "--event-id",
            event_id,
            "--run-id",
            "RUN-1",
            "--instance-id",
            "WORKING-PKG01",
            "--session-id",
            "AUTHOR-PKG01",
            "--role",
            "TASK",
            "--package-id",
            "PKG-01",
            "--event-type",
            event_type,
            "--outcome",
            outcome,
            "--timestamp",
            timestamp,
        ],
        text=True,
        capture_output=True,
        check=False,
    )


def test_record_summarize_and_duplicate_rejection(tmp_path: Path) -> None:
    assert record(tmp_path, "E-001", "START", "STARTED", "2026-07-13T00:00:00Z").returncode == 0
    remediation = record(tmp_path, "E-002", "REMEDIATION", "INFO", "2026-07-13T00:01:00Z")
    assert remediation.returncode == 0
    assert record(tmp_path, "E-003", "FINISH", "PASS", "2026-07-13T00:02:00Z").returncode == 0
    duplicate = record(tmp_path, "E-003", "FINISH", "PASS", "2026-07-13T00:03:00Z")
    assert duplicate.returncode == 2
    assert len((tmp_path / "RUNTIME_EVENTS.jsonl").read_text(encoding="utf-8").splitlines()) == 3

    summary = subprocess.run(
        [sys.executable, str(SCRIPT), "summarize", "--run-root", str(tmp_path)],
        text=True,
        capture_output=True,
        check=False,
    )
    assert summary.returncode == 0, summary.stderr
    report = json.loads((tmp_path / "RUNTIME_SUMMARY.json").read_text(encoding="utf-8"))
    assert report["status"] == "PASS"
    assert report["events"] == 3
    assert report["session_results"][0]["duration_seconds"] == 120.0
    assert report["session_results"][0]["remediations"] == 1
    assert report["context_telemetry"]["starts_without_context_occupancy"] == 1


def test_output_must_remain_inside_run_root(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "record",
            "--run-root",
            str(tmp_path),
            "--output",
            "../outside.jsonl",
            "--event-id",
            "E-001",
            "--run-id",
            "RUN-1",
            "--instance-id",
            "I-1",
            "--session-id",
            "S-1",
            "--role",
            "TASK",
            "--event-type",
            "START",
            "--outcome",
            "STARTED",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 2
    assert not (tmp_path.parent / "outside.jsonl").exists()
