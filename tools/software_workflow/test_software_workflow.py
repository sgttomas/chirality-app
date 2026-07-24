import json
import socket
import subprocess
import sys
from pathlib import Path

from common import contained_path, matches
from compare_structured import flatten
from validate_change_scope import contained


def test_containment_and_globs(tmp_path: Path) -> None:
    assert contained_path(tmp_path, "src/a.ts") == tmp_path / "src/a.ts"
    assert matches("src/a.ts", ["src/**/*.ts", "src/*.ts"])
    assert contained("src/a.ts", "src")
    assert not contained("scripts/a.ts", "src")


def test_flatten_structured_values() -> None:
    assert flatten({"a": [1, {"b": 2}]}) == {"$.a[0]": 1, "$.a[1].b": 2}


def test_change_scope_includes_untracked_files(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "allowed").mkdir()
    (tmp_path / "allowed" / "tracked.txt").write_text("tracked\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "allowed/tracked.txt"], check=True)
    subprocess.run(
        [
            "git", "-C", str(tmp_path), "-c", "user.name=Test", "-c",
            "user.email=test@example.com", "commit", "-qm", "base"
        ],
        check=True,
    )
    (tmp_path / "outside.txt").write_text("untracked\n", encoding="utf-8")
    script = Path(__file__).with_name("validate_change_scope.py")
    completed = subprocess.run(
        [sys.executable, str(script), str(tmp_path), "--allowed", "allowed"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 1
    report = json.loads(completed.stdout)
    assert "outside.txt" in report["paths"]
    assert report["violations"] == ["outside.txt"]


def test_registered_checks_timeout_and_contain_output(tmp_path: Path) -> None:
    profile = tmp_path / "software-workflow.json"
    profile.write_text(
        json.dumps({
            "schema": "chirality-software-workflow/v1",
            "project_root": ".",
            "workspace_root": ".",
            "checks": {
                "slow": {
                    "cwd": ".",
                    "command": [sys.executable, "-c", "import time; time.sleep(1)"],
                    "timeout_seconds": 0.01,
                }
            },
        }),
        encoding="utf-8",
    )
    script = Path(__file__).with_name("run_registered_checks.py")
    result = subprocess.run(
        [sys.executable, str(script), str(profile), "--check", "slow", "--output", "evidence.json"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1
    report = json.loads((tmp_path / "evidence.json").read_text(encoding="utf-8"))
    assert report["results"][0]["exit_code"] == 124

    outside_path = tmp_path.parent / f"{tmp_path.name}-outside.json"
    outside = subprocess.run(
        [sys.executable, str(script), str(profile), "--check", "slow", "--output", str(outside_path)],
        text=True,
        capture_output=True,
        check=False,
    )
    assert outside.returncode != 0
    assert not outside_path.exists()


def test_registered_check_owns_service_lifecycle(tmp_path: Path) -> None:
    profile = tmp_path / "software-workflow.json"
    profile.write_text(
        json.dumps({
            "schema": "chirality-software-workflow/v1",
            "project_root": ".",
            "workspace_root": ".",
            "checks": {
                "self-contained": {
                    "cwd": ".",
                    "command": [
                        sys.executable,
                        "-c",
                        "import os, urllib.request; urllib.request.urlopen(os.environ['TEST_URL'])",
                    ],
                    "service": {
                        "command": [sys.executable, "-m", "http.server", "{port}", "--bind", "127.0.0.1"],
                        "ready_url": "http://127.0.0.1:{port}",
                        "check_env": {"TEST_URL": "http://127.0.0.1:{port}"},
                        "startup_timeout_seconds": 5,
                    },
                }
            },
        }),
        encoding="utf-8",
    )
    script = Path(__file__).with_name("run_registered_checks.py")
    completed = subprocess.run(
        [sys.executable, str(script), str(profile), "--check", "self-contained", "--output", "evidence.json"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    report = json.loads((tmp_path / "evidence.json").read_text(encoding="utf-8"))
    result = report["results"][0]
    assert result["status"] == "PASS"
    assert result["service"]["status"] == "READY"
    assert result["service"]["stopped_after_run"] is True
    assert str(tmp_path) not in json.dumps(report)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.settimeout(0.5)
        assert probe.connect_ex(("127.0.0.1", result["service"]["port"])) != 0


def test_registered_check_stops_service_after_check_failure(tmp_path: Path) -> None:
    profile = tmp_path / "software-workflow.json"
    profile.write_text(
        json.dumps({
            "schema": "chirality-software-workflow/v1",
            "project_root": ".",
            "workspace_root": ".",
            "checks": {
                "failing": {
                    "cwd": ".",
                    "command": [sys.executable, "-c", "raise SystemExit(7)"],
                    "service": {
                        "command": [sys.executable, "-m", "http.server", "{port}", "--bind", "127.0.0.1"],
                        "ready_url": "http://127.0.0.1:{port}",
                        "startup_timeout_seconds": 5,
                    },
                }
            },
        }),
        encoding="utf-8",
    )
    script = Path(__file__).with_name("run_registered_checks.py")
    completed = subprocess.run(
        [sys.executable, str(script), str(profile), "--check", "failing", "--output", "evidence.json"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 1
    report = json.loads((tmp_path / "evidence.json").read_text(encoding="utf-8"))
    result = report["results"][0]
    assert result["exit_code"] == 7
    assert result["service"]["stopped_after_run"] is True
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.settimeout(0.5)
        assert probe.connect_ex(("127.0.0.1", result["service"]["port"])) != 0
