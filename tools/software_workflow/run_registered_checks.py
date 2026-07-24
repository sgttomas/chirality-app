#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import signal
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from common import load_profile


def as_text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value


def interpolate(value: str, port: int) -> str:
    return value.replace("{port}", str(port))


def allocate_loopback_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as handle:
        handle.bind(("127.0.0.1", 0))
        return int(handle.getsockname()[1])


def string_map(value: Any, label: str, port: int) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict) or not all(
        isinstance(key, str) and isinstance(item, str) for key, item in value.items()
    ):
        raise ValueError(f"{label} must be an object of string values")
    return {key: interpolate(item, port) for key, item in value.items()}


def command_array(value: Any, label: str, port: int | None = None) -> list[str]:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{label} must be a non-empty string array")
    return [interpolate(item, port) for item in value] if port is not None else list(value)


def normalize_evidence_text(value: str, workspace_root: Path) -> str:
    replacements = {
        str(workspace_root): "{WORKSPACE_ROOT}",
        tempfile.gettempdir(): "{TMPDIR}",
    }
    normalized = value
    for literal, replacement in sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True):
        normalized = normalized.replace(literal, replacement)
    return normalized


def read_log_tail(handle: Any, limit: int = 16_000) -> str:
    handle.flush()
    handle.seek(0, os.SEEK_END)
    size = handle.tell()
    handle.seek(max(0, size - limit))
    return handle.read()


def wait_for_service(process: subprocess.Popen[str], ready_url: str, timeout_seconds: float) -> float:
    started = time.monotonic()
    deadline = started + timeout_seconds
    last_error = "service did not answer"
    while time.monotonic() < deadline:
        exit_code = process.poll()
        if exit_code is not None:
            raise RuntimeError(f"service exited before readiness with code {exit_code}")
        try:
            with urllib.request.urlopen(ready_url, timeout=1.0) as response:
                if 200 <= response.status < 500:
                    return round(time.monotonic() - started, 3)
                last_error = f"readiness returned HTTP {response.status}"
        except urllib.error.HTTPError as error:
            if 200 <= error.code < 500:
                return round(time.monotonic() - started, 3)
            last_error = f"readiness returned HTTP {error.code}"
        except (OSError, urllib.error.URLError) as error:
            last_error = str(error)
        time.sleep(0.1)
    raise TimeoutError(f"service readiness timed out after {timeout_seconds} seconds: {last_error}")


def stop_service(process: subprocess.Popen[str], timeout_seconds: float) -> tuple[bool, int | None]:
    if process.poll() is None:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait(timeout=timeout_seconds)
    return process.poll() is not None, process.returncode


def run_check(
    *,
    check_id: str,
    spec: dict[str, Any],
    command: list[str],
    cwd: Path,
    project_root: Path,
    workspace_root: Path,
    default_timeout_seconds: float,
) -> dict[str, Any]:
    started = time.monotonic()
    timeout_seconds = spec.get("timeout_seconds", default_timeout_seconds)
    if not isinstance(timeout_seconds, (int, float)) or timeout_seconds <= 0:
        raise ValueError(f"check {check_id} timeout_seconds must be positive")

    service_spec = spec.get("service")
    process: subprocess.Popen[str] | None = None
    service_stdout = None
    service_stderr = None
    service_record: dict[str, Any] | None = None
    check_env = os.environ.copy()
    exit_code = 125
    stdout = ""
    stderr = ""

    try:
        if service_spec is not None:
            if not isinstance(service_spec, dict):
                raise ValueError(f"check {check_id} service must be an object")
            port_value = service_spec.get("port", "auto")
            if port_value == "auto":
                port = allocate_loopback_port()
            elif isinstance(port_value, int) and 1 <= port_value <= 65535:
                port = port_value
            else:
                raise ValueError(f"check {check_id} service port must be 'auto' or 1..65535")

            service_command = command_array(
                service_spec.get("command"), f"check {check_id} service command", port
            )
            service_cwd = (project_root / service_spec.get("cwd", spec.get("cwd", "."))).resolve()
            service_cwd.relative_to(workspace_root)
            if not service_cwd.is_dir():
                raise ValueError(f"check {check_id} service cwd does not exist: {service_cwd}")
            ready_url_value = service_spec.get("ready_url")
            if not isinstance(ready_url_value, str) or not ready_url_value:
                raise ValueError(f"check {check_id} service ready_url must be a non-empty string")
            ready_url = interpolate(ready_url_value, port)
            startup_timeout = service_spec.get("startup_timeout_seconds", 60.0)
            shutdown_timeout = service_spec.get("shutdown_timeout_seconds", 10.0)
            if not isinstance(startup_timeout, (int, float)) or startup_timeout <= 0:
                raise ValueError(f"check {check_id} service startup_timeout_seconds must be positive")
            if not isinstance(shutdown_timeout, (int, float)) or shutdown_timeout <= 0:
                raise ValueError(f"check {check_id} service shutdown_timeout_seconds must be positive")

            service_env = os.environ.copy()
            service_env.update(string_map(service_spec.get("env"), f"check {check_id} service env", port))
            check_env.update(
                string_map(service_spec.get("check_env"), f"check {check_id} service check_env", port)
            )
            service_stdout = tempfile.TemporaryFile(mode="w+t", encoding="utf-8")
            service_stderr = tempfile.TemporaryFile(mode="w+t", encoding="utf-8")
            process = subprocess.Popen(
                service_command,
                cwd=service_cwd,
                env=service_env,
                text=True,
                stdin=subprocess.DEVNULL,
                stdout=service_stdout,
                stderr=service_stderr,
                shell=False,
                start_new_session=True,
            )
            service_record = {
                "command": service_command,
                "cwd": service_cwd.relative_to(workspace_root).as_posix() or ".",
                "port": port,
                "ready_url": ready_url,
                "startup_timeout_seconds": startup_timeout,
                "shutdown_timeout_seconds": shutdown_timeout,
                "status": "STARTING",
                "stopped_after_run": False,
            }
            service_record["startup_duration_seconds"] = wait_for_service(
                process, ready_url, float(startup_timeout)
            )
            service_record["status"] = "READY"

        try:
            completed = subprocess.run(
                command,
                cwd=cwd,
                env=check_env,
                text=True,
                capture_output=True,
                shell=False,
                timeout=float(timeout_seconds),
            )
            exit_code = completed.returncode
            stdout = completed.stdout
            stderr = completed.stderr
        except subprocess.TimeoutExpired as error:
            exit_code = 124
            stdout = as_text(error.stdout)
            stderr = as_text(error.stderr) + f"\ncheck timed out after {timeout_seconds} seconds"
    except (OSError, RuntimeError, TimeoutError, ValueError) as error:
        exit_code = 125
        stderr = f"service setup failed: {error}"
        if service_record is not None:
            service_record["status"] = "FAIL"
    finally:
        if process is not None and service_record is not None:
            stopped, service_exit = stop_service(process, float(service_record["shutdown_timeout_seconds"]))
            service_record["stopped_after_run"] = stopped
            service_record["exit_code"] = service_exit
            if service_stdout is not None:
                service_record["stdout_tail"] = normalize_evidence_text(
                    read_log_tail(service_stdout), workspace_root
                )
                service_stdout.close()
            if service_stderr is not None:
                service_record["stderr_tail"] = normalize_evidence_text(
                    read_log_tail(service_stderr), workspace_root
                )
                service_stderr.close()

    result = {
        "id": check_id,
        "command": command,
        "cwd": cwd.relative_to(workspace_root).as_posix() or ".",
        "exit_code": exit_code,
        "timeout_seconds": timeout_seconds,
        "duration_seconds": round(time.monotonic() - started, 3),
        "stdout": normalize_evidence_text(stdout, workspace_root),
        "stderr": normalize_evidence_text(stderr, workspace_root),
        "status": "PASS" if exit_code == 0 else "FAIL",
    }
    if service_record is not None:
        result["service"] = service_record
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run allowlisted software checks without a shell.")
    parser.add_argument("profile")
    parser.add_argument("--check", action="append", default=[])
    parser.add_argument("--output", required=True)
    parser.add_argument("--timeout-seconds", type=float, default=600.0)
    args = parser.parse_args()
    profile_path = Path(args.profile).resolve()
    project_root, profile = load_profile(profile_path)
    workspace_root = (profile_path.parent / profile.get("workspace_root", profile.get("project_root", "."))).resolve()
    project_root.relative_to(workspace_root)
    checks = profile.get("checks", {})
    selected = args.check or list(checks)
    unknown = sorted(set(selected) - set(checks))
    if unknown:
        parser.error(f"unknown check(s): {', '.join(unknown)}")
    results = []
    for check_id in selected:
        spec = checks[check_id]
        command = command_array(spec.get("command"), f"check {check_id} command")
        cwd = (project_root / spec.get("cwd", ".")).resolve()
        cwd.relative_to(workspace_root)
        if not cwd.is_dir():
            raise ValueError(f"check {check_id} cwd does not exist: {cwd}")
        results.append(run_check(
            check_id=check_id,
            spec=spec,
            command=command,
            cwd=cwd,
            project_root=project_root,
            workspace_root=workspace_root,
            default_timeout_seconds=args.timeout_seconds,
        ))
    report = {
        "schema": "chirality-software-check-evidence/v1",
        "profile": Path(args.profile).resolve().relative_to(workspace_root).as_posix(),
        "project_root": project_root.relative_to(workspace_root).as_posix() or ".",
        "workspace_root": ".",
        "status": "PASS" if all(item["exit_code"] == 0 for item in results) else "FAIL",
        "results": results,
    }
    output = Path(args.output)
    if not output.is_absolute():
        output = (workspace_root / output).resolve()
    else:
        output = output.resolve()
    output.relative_to(workspace_root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "output": str(output), "checks": selected}))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
