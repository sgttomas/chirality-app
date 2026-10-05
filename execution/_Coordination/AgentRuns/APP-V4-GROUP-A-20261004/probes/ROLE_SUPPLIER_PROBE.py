#!/usr/bin/env python3
"""Parent-run, capture-only stock Codex ROLE witness. Authoring never executes it."""
from __future__ import annotations
import argparse
import hashlib
import http.server
import json
import os
from pathlib import Path
import queue
import secrets
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time

METHOD = "chirality.app.exact-bytes.sha256/v1"
BINARY_SHA256 = "112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b"
COMMON_SHA256 = "d9233f5af0393e045f0d50fe14b60ede6ec3558da625c1a0deec84fae07afc27"
ROLE_SHA256 = "11e619e41acad799b90552dda19a3d49c4d3921bcebbce7317254a58d03e04be"
COMPOSED_SHA256 = "ad560fe79f9552fef1042dd613a0274ca87babd7165bc1ecd0a278a3ada98343"
MODEL = "gpt-6.1-sol"
EFFORT = "medium"
PROVIDER = "role_capture"
PROMPT = "Reply with one short greeting. Use no tools."


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def identity(data: bytes) -> dict:
    return {"method": METHOD, "value": digest(data), "bytes": len(data)}


def file_identity(path: Path) -> dict:
    h = hashlib.sha256()
    count = 0
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
            count += len(chunk)
    return {"method": METHOD, "value": h.hexdigest(), "bytes": count}


def mktemp_directory(template: Path | None = None) -> Path:
    """Parent execution uses actual mktemp -d, not an inferred equivalent."""
    command = ["/usr/bin/mktemp", "-d"]
    if template is None:
        command += ["-t", "chirality-role-capture"]
    else:
        command.append(str(template))
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, timeout=5)
    directory = Path(result.stdout.strip()).resolve(strict=True)
    expected_parent = template.parent.resolve() if template is not None else Path(tempfile.gettempdir()).resolve()
    if not directory.is_dir() or directory.parent != expected_parent:
        raise RuntimeError("mktemp result escaped its owned parent")
    os.chmod(directory, 0o700)
    return directory


def exact_composition(resources: Path) -> tuple[str, dict]:
    """Independent, pinned output oracle for production Composition::new.
    Source files and complete output must match the reviewed exact hashes.
    This does not claim to invoke the Rust producer or test App store seeding.
    """
    common = (resources / "AGENTS.md").read_bytes()
    role = (resources / "agents/AGENT_HELP_HUMAN.md").read_bytes()
    if digest(common) != COMMON_SHA256 or digest(role) != ROLE_SHA256:
        raise ValueError("reviewed guidance source changed; do not silently rebind")
    separator = b"\n\n# Active role: HELP_HUMAN\n\n"
    composed = common + separator + role
    if len(composed) != 4856 or digest(composed) != COMPOSED_SHA256:
        raise ValueError("composition differs from independently checked production output")
    return composed.decode("utf-8"), {
        "compositionFormat": "chirality.role.compose/0.2",
        "composed": identity(composed), "baseInstructions": "not-set",
        "parts": [
            {"kind": "product-guidance", "path": "AGENTS.md", "offset": 0,
             "length": len(common), "content": identity(common)},
            {"kind": "role-guidance", "role": "HELP_HUMAN",
             "path": "agents/AGENT_HELP_HUMAN.md", "offset": len(common) + len(separator),
             "length": len(role), "content": identity(role)},
        ],
    }


def text_segments(payload: dict) -> list[dict]:
    """Keep actual provider roles/positions; do not export complete text."""
    segments = []
    if isinstance(payload.get("instructions"), str):
        segments.append({"position": "instructions", "role": "system-base", "text": payload["instructions"]})
    for field in ("input", "messages"):
        rows = payload.get(field)
        if not isinstance(rows, list):
            continue
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                continue
            role = row.get("role", "unknown")
            content = row.get("content")
            if isinstance(content, str):
                segments.append({"position": f"{field}/{index}/content", "role": role, "text": content})
            elif isinstance(content, list):
                for part, value in enumerate(content):
                    if isinstance(value, dict) and isinstance(value.get("text"), str):
                        segments.append({"position": f"{field}/{index}/content/{part}/text", "role": role, "text": value["text"]})
    return segments


class CaptureHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_POST(self):
        # No forwarding/model prediction. No authentication headers are read or stored.
        length = int(self.headers.get("Content-Length", "0"))
        if not 0 < length <= 8 * 1024 * 1024:
            self.send_error(413)
            return
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw)
            if not isinstance(payload, dict):
                raise ValueError("provider payload is not an object")
            path = self.server.raw_dir / f"payload-{secrets.token_hex(8)}.json"
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(descriptor, "wb") as output:
                output.write(raw)
            self.server.captures.put((payload, identity(raw), path.name, self.path))
        except (ValueError, OSError) as exc:
            self.server.captures.put((None, str(exc), None, self.path))
        body = b'{"error":{"message":"deliberate capture-only refusal; no model executed","type":"capture_only","code":"capture_only"}}'
        self.send_response(400)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class NativeResponseError(RuntimeError):
    """A correlated supplier error, distinct from unexpected server requests."""


class NativeRpc:
    def __init__(self, binary: Path, home: Path, workspace: Path, scratch: Path, timeout: float,
                 *, _popen=None, _thread=None, _open_stderr=None, _chmod=None,
                 _cleanup_killpg=None, _cleanup_sleep=None, _cleanup_clock=None):
        self.timeout = timeout
        self.serial = 0
        self.frames = queue.Queue()
        self.process = None
        self.reader = None
        self.reader_started = False
        self.stderr = None
        self.stderr_path = scratch / "native-stderr.raw.txt"
        env = {name: os.environ[name] for name in ("PATH", "HOME", "TMPDIR", "LANG", "LC_ALL") if name in os.environ}
        env.update(CODEX_HOME=str(home), CODEX_INTERNAL_APP_SERVER_REMOTE_CONTROL_DISABLED="1")
        try:
            self.stderr = (_open_stderr or (lambda path: path.open("wb")))(self.stderr_path)
            (_chmod or os.chmod)(self.stderr_path, 0o600)
            self.process = (_popen or subprocess.Popen)([str(binary), "app-server"], cwd=workspace, env=env,
                                              stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.stderr,
                                              start_new_session=True)
            # Cleanup ownership exists before reader construction/start can fail.
            self.reader = (_thread or threading.Thread)(target=self._read, daemon=True)
            self.reader.start()
            self.reader_started = True
        except BaseException as failure:
            if self.process is not None:
                try:
                    self.close(_killpg=_cleanup_killpg or os.killpg,
                               _sleep=_cleanup_sleep or time.sleep,
                               _clock=_cleanup_clock or time.monotonic)
                except BaseException as cleanup_failure:
                    failure.add_note("startup cleanup not established: " + type(cleanup_failure).__name__)
            elif self.stderr is not None:
                self.stderr.close()
            raise

    def _read(self):
        for raw in self.process.stdout:
            try:
                frame = json.loads(raw)
                self.frames.put(frame)
            except ValueError:
                self.frames.put({"probe_error": "native stdout was not JSON"})
        self.frames.put({"probe_error": "native stdout closed"})

    def send(self, frame: dict):
        self.process.stdin.write(json.dumps(frame, ensure_ascii=False).encode() + b"\n")
        self.process.stdin.flush()

    def request(self, method: str, params: dict) -> dict:
        self.serial += 1
        request_id = self.serial
        self.send({"id": request_id, "method": method, "params": params})
        deadline = time.monotonic() + self.timeout
        while time.monotonic() < deadline:
            try:
                frame = self.frames.get(timeout=max(0.01, deadline - time.monotonic()))
            except queue.Empty:
                raise TimeoutError(f"native {method} response timeout")
            if "probe_error" in frame:
                raise RuntimeError(frame["probe_error"])
            if "method" in frame and "id" in frame:
                # Capture fixture has no act/auth/tool facility. Answer every
                # unexpected supplier request with an explicit error, then stop.
                self.send({"id": frame["id"], "error": {"code": -32601, "message": "unsupported by read-only capture probe"}})
                raise RuntimeError(f"unexpected native server request: {frame['method']}")
            if frame.get("id") == request_id and "method" not in frame:
                if "error" in frame:
                    raise NativeResponseError(f"native {method} returned an error")
                return frame["result"]
        raise TimeoutError(f"native {method} response timeout")

    def close(self, *, _killpg=os.killpg, _sleep=time.sleep, _clock=time.monotonic):
        # start_new_session=True pins this PGID to the launch PID. A leader's
        # successful exit never establishes that its descendants have ended.
        group = self.process.pid
        def exists():
            try:
                _killpg(group, 0)
                return True
            except ProcessLookupError:
                return False
        def send(sig):
            try:
                _killpg(group, sig)
            except ProcessLookupError:
                pass  # Raced with group termination; verify absence below.
        def wait_absent(seconds):
            deadline = _clock() + seconds
            while exists() and _clock() < deadline:
                _sleep(0.05)
            return not exists()
        try:
            if self.process.stdin:
                try:
                    self.process.stdin.close()
                except BrokenPipeError:
                    pass
            if self.process.poll() is None:
                try:
                    self.process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    pass  # Leader may still run; the group controls follow.
            if exists():
                send(signal.SIGTERM)
                if not wait_absent(3):
                    send(signal.SIGKILL)
                    if not wait_absent(3):
                        raise RuntimeError("native process-group end not established after bounded cleanup")
            # Reap the owned leader separately; absence of PGID is the tree oracle.
            self.process.wait(timeout=1)
            return {"leader_reaped": True, "process_group_end": "observed-absent"}
        finally:
            if self.reader is not None and (getattr(self, "reader_started", False)
                    or getattr(self.reader, "ident", None) is not None):
                self.reader.join(timeout=1)
            if self.stderr is not None:
                self.stderr.close()


def capture_case(rpc: NativeRpc, server, workspace: Path, composition: str | None,
                 label: str, timeout: float) -> tuple[dict, dict]:
    if not server.captures.empty():
        raise RuntimeError("unassigned provider request before case start")
    params = {"cwd": str(workspace), "model": MODEL, "modelProvider": PROVIDER}
    if composition is not None:
        params["developerInstructions"] = composition
    assert "baseInstructions" not in params and "config" not in params
    start = rpc.request("thread/start", params)
    thread_id = start["thread"]["id"]
    turn = rpc.request("turn/start", {"threadId": thread_id, "effort": EFFORT, "input": [{"type": "text", "text": PROMPT, "text_elements": []}]})
    try:
        payload, payload_identity, raw_file, path = server.captures.get(timeout=timeout)
    except queue.Empty:
        raise TimeoutError(f"{label}: provider request not observed")
    if payload is None:
        raise RuntimeError(f"{label}: malformed provider capture: {payload_identity}")
    report = {
        "case": label, "native_thread": thread_id,
        "native_turn": turn.get("turn", {}).get("id"), "native_start_succeeded": True,
        "requested_model": MODEL, "requested_effort": EFFORT,
        "native_reported_model": start.get("model"), "native_reported_provider": start.get("modelProvider"),
        "native_reported_effort": start.get("reasoningEffort", "not-reported"),
        "provider_payload_model": payload.get("model", "not-reported"),
        "provider_payload_reasoning": payload.get("reasoning", "not-reported"),
        "native_instruction_sources": start.get("instructionSources", "not-reported"),
        "base_override_sent": False, "config_or_policy_override_sent": False,
        "developer_instructions_sent": identity(composition.encode()) if composition is not None else None,
        "raw_payload": {"scratch_file": raw_file, "content": payload_identity},
        "provider_endpoint_path": path.split("?", 1)[0],
        "payload_top_level_keys": sorted(payload.keys()),
        "model_prediction": "none: endpoint deliberately returns HTTP400",
    }
    # The first provider capture is enough for carriage; stop this failed turn
    # explicitly before pairing so a retry cannot be attributed to another case.
    try:
        rpc.request("turn/interrupt", {"threadId": thread_id, "turnId": report["native_turn"]})
        report["interrupt_reply"] = "observed"
    except NativeResponseError:
        report["interrupt_reply"] = "error (turn may already have failed)"
    return payload, report


def comparisons(baseline: dict, active: dict, composition: str, global_marker: str, project_marker: str) -> dict:
    base = text_segments(baseline)
    role = text_segments(active)
    base_native = [x["text"].encode() for x in base if x["role"] in ("system", "system-base")]
    role_native = [x["text"].encode() for x in role if x["role"] in ("system", "system-base")]
    base_observed = any(len(text) > 0 for text in base_native) and any(len(text) > 0 for text in role_native)
    preserved = base_observed and base_native == role_native
    developer = [x for x in role if x["role"] == "developer"]
    carriage = any(composition.encode() in x["text"].encode() for x in developer)
    joined_base = "\n".join(x["text"] for x in base)
    joined_active = "\n".join(x["text"] for x in role)
    markers = {
        "native_global": {"marker": global_marker, "baseline_seen": global_marker in joined_base, "active_seen": global_marker in joined_active},
        "native_project": {"marker": project_marker, "baseline_seen": project_marker in joined_base, "active_seen": project_marker in joined_active},
    }
    return {
        "exact_composition_in_developer_segment": carriage,
        "composition_absent_from_baseline": composition not in joined_base,
        "native_base_observable": base_observed,
        "native_base_byte_equal_to_baseline": preserved if base_observed else "unknown",
        "native_base_segment_identities": [identity(x) for x in base_native],
        "markers": markers,
        "developer_segment_structure": [{"position": x["position"], "bytes": len(x["text"].encode()), "content": identity(x["text"].encode())} for x in developer],
        "passed": carriage and composition not in joined_base and preserved and all(m["baseline_seen"] and m["active_seen"] for m in markers.values()),
    }


def self_check() -> int:
    """Pure oracles/fake process cleanup only; no native, provider or OS signals."""
    base = {"instructions": "", "input": [{"role": "user", "content": "global project"}]}
    active = {"instructions": "", "input": [{"role": "user", "content": "global project"},
              {"role": "developer", "content": "exact composition"}]}
    verdict = comparisons(base, active, "exact composition", "global", "project")
    assert verdict["native_base_observable"] is False
    assert verdict["native_base_byte_equal_to_baseline"] == "unknown"
    assert verdict["passed"] is False
    empty_system_base = {"input": [{"role": "system", "content": ""}, {"role": "user", "content": "global project"}]}
    empty_system_active = {"input": [{"role": "system", "content": ""}, {"role": "user", "content": "global project"}, {"role": "developer", "content": "exact composition"}]}
    system_verdict = comparisons(empty_system_base, empty_system_active, "exact composition", "global", "project")
    assert not system_verdict["native_base_observable"] and not system_verdict["passed"]
    assert system_verdict["native_base_byte_equal_to_baseline"] == "unknown"
    # Preserve complete authoritative byte comparison, including empty segments
    # and CRLF/whitespace. Presence checks must not normalize comparison content.
    base["instructions"] = active["instructions"] = "native base\r\n"
    assert comparisons(base, active, "exact composition", "global", "project")["passed"]
    active["instructions"] = "native base\n"
    assert not comparisons(base, active, "exact composition", "global", "project")["passed"]
    class Handle:
        def close(self): pass
    class Reader:
        def join(self, timeout): pass
    class Process:
        pid = 424242
        stdin = Handle()
        def __init__(self, already_exited): self.exited = already_exited
        def poll(self): return 0 if self.exited else None
        def wait(self, timeout): self.exited = True; return 0
    for already_exited in (True, False):
        for resists_term in (False, True):
            fake = NativeRpc.__new__(NativeRpc)
            fake.process = Process(already_exited)
            fake.reader = Reader()
            fake.stderr = Handle()
            state = {"alive": True, "clock": 0.0, "signals": []}
            def killpg(pgid, sig):
                assert pgid == 424242
                if not state["alive"]: raise ProcessLookupError()
                if sig:
                    state["signals"].append(sig)
                    if sig == signal.SIGKILL or not resists_term: state["alive"] = False
            def sleep(seconds): state["clock"] += seconds
            fake.close(_killpg=killpg, _sleep=sleep, _clock=lambda: state["clock"])
            assert not state["alive"]
            assert state["signals"] == ([signal.SIGTERM, signal.SIGKILL] if resists_term else [signal.SIGTERM])
    # A group that remains observable after SIGKILL is unknown/failure, never
    # reported ended from its leader status. All functions here are injected fakes.
    fake = NativeRpc.__new__(NativeRpc)
    fake.process = Process(True)
    fake.reader = Reader()
    fake.stderr = Handle()
    state = {"clock": 0.0, "signals": []}
    def stubborn_group(pgid, sig):
        assert pgid == 424242
        if sig: state["signals"].append(sig)
    def advance(seconds): state["clock"] += seconds
    try:
        fake.close(_killpg=stubborn_group, _sleep=advance, _clock=lambda: state["clock"])
        raise AssertionError("observable remaining group was incorrectly accepted")
    except RuntimeError as exc:
        assert "end not established" in str(exc)
    assert state["signals"] == [signal.SIGTERM, signal.SIGKILL]
    # Constructor fakes explicitly inject every cleanup primitive. No default-
    # bound real killpg can be reached, even if the fake reader startup fails.
    class TrackedHandle:
        def __init__(self): self.closed = False
        def close(self): self.closed = True
    class FailedReader:
        ident = None
        def start(self): raise RuntimeError("injected reader startup failure")
        def join(self, timeout): raise AssertionError("unstarted reader must not be joined")
    for failure_point in ("popen", "reader-construction", "reader-start"):
        stderr = TrackedHandle()
        process = Process(True)
        process.stdin = TrackedHandle()
        state = {"alive": True, "signals": [], "clock": 0.0, "reaped": False}
        def reap(timeout): state["reaped"] = True; return 0
        process.wait = reap
        def popen(*args, **kwargs):
            if failure_point == "popen": raise OSError("injected spawn failure")
            return process
        def thread(**kwargs):
            if failure_point == "reader-construction": raise RuntimeError("injected reader construction failure")
            return FailedReader()
        def cleanup_signal(pgid, sig):
            assert pgid == 424242
            if not state["alive"]: raise ProcessLookupError()
            if sig: state["signals"].append(sig); state["alive"] = False
        try:
            NativeRpc(Path("/invented/codex"), Path("/invented/home"), Path("/invented/work"),
                      Path("/invented/scratch"), 1, _popen=popen, _thread=thread,
                      _open_stderr=lambda path: stderr, _chmod=lambda *args: None,
                      _cleanup_killpg=cleanup_signal, _cleanup_sleep=lambda _: None,
                      _cleanup_clock=lambda: state["clock"])
            raise AssertionError("injected constructor failure did not propagate")
        except (OSError, RuntimeError):
            pass
        assert stderr.closed
        if failure_point == "popen":
            assert not state["signals"] and not state["reaped"]
        else:
            assert state["signals"] == [signal.SIGTERM]
            assert not state["alive"] and state["reaped"] and process.stdin.closed
    assert MODEL == "gpt-6.1-sol" and EFFORT == "medium"
    print("PASS empty-base unknown/fail; exact CRLF byte comparison; five fake leader/descendant cleanup cases; three guarded constructor failures; model/effort constants. No native/provider/mktemp/OS signal executed.")
    return 0


def main() -> int:
    if sys.argv[1:] == ["--self-check"]:
        return self_check()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", type=Path, required=True, help="approved stock0.160.0 executable")
    parser.add_argument("--report", type=Path, required=True, help="durable structural JSON; contains no complete request prompts/auth headers")
    parser.add_argument("--keep-scratch", action="store_true", help="retain mode0700 raw scratch for parent inspection")
    parser.add_argument("--timeout", type=float, default=20)
    args = parser.parse_args()
    if not 1 <= args.timeout <= 60:
        parser.error("timeout must be between1 and60 seconds")
    binary = args.codex.resolve(strict=True)
    binary_identity = file_identity(binary)
    if binary_identity["value"] != BINARY_SHA256:
        raise ValueError("binary identity differs from approved0.160.0 development hash")
    working_root = next(p for p in Path(__file__).resolve().parents if p.name == "chirality-app-v4")
    resources = working_root / "app/src-tauri/resources/instructions"
    composed, source_account = exact_composition(resources)
    scratch = mktemp_directory()
    os.chmod(scratch, 0o700)
    report = {"format": "chirality.role.capture-witness/0.1", "supplier_pin": "0.160.0",
              "supplier_standing": "unverified-development", "binary": binary_identity,
              "source": source_account, "adoption": "unknown", "cases": [], "passed": False,
              "evidence_limits": ["Independent exact production-output oracle, not Rust Host invocation or connected App witness",
                                  "HTTP400 capture-only endpoint performs no prediction and no provider/model adoption is inferred",
                                  "Primary HELP_HUMAN only; other roles/no-role/lifetime/resume/fork/child carrier/availability remain separate",
                                  "Instruction source path reports are distinct from observed marker content",
                                  "Development binary hash is not distribution/supplier qualification"]}
    server = None
    rpc = None
    try:
        home = mktemp_directory(scratch / "codex-home.XXXXXXXX")
        workspace = scratch / "workspace"
        raw = scratch / "raw-provider-payloads"
        for directory in (workspace, raw):
            directory.mkdir(mode=0o700)
        global_marker = "ROLE_NATIVE_GLOBAL_" + secrets.token_hex(8)
        project_marker = "ROLE_NATIVE_PROJECT_" + secrets.token_hex(8)
        (home / "AGENTS.md").write_text(f"Synthetic native-global discovery marker: {global_marker}.\n")
        (workspace / "AGENTS.md").write_text(f"Synthetic native-project discovery marker: {project_marker}.\n")
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), CaptureHandler)
        server.daemon_threads = True
        server.captures = queue.Queue()
        server.raw_dir = raw
        threading.Thread(target=server.serve_forever, daemon=True).start()
        port = server.server_address[1]
        config = f'''model_provider = "{PROVIDER}"
model = "{MODEL}"
model_reasoning_effort = "{EFFORT}"
[model_providers.{PROVIDER}]
name = "ROLE capture-only loopback"
base_url = "http://127.0.0.1:{port}/v1"
wire_api = "responses"
requires_openai_auth = false
supports_websockets = false
[features]
plugins = false
[analytics]
enabled = false
'''
        (home / "config.toml").write_text(config)
        report["selected_model"] = MODEL
        report["selected_effort"] = EFFORT
        report["scratch_creation"] = "actual /usr/bin/mktemp -d for owned root and CODEX_HOME"
        report["scratch_sources"] = {"config": identity(config.encode()),
                                     "native_global": identity((home / "AGENTS.md").read_bytes()),
                                     "native_project": identity((workspace / "AGENTS.md").read_bytes())}
        rpc = NativeRpc(binary, home, workspace, scratch, args.timeout)
        rpc.request("initialize", {"clientInfo": {"name": "chirality-role-capture-probe", "version": "0.1"},
                                   "capabilities": {"experimentalApi": True}})
        rpc.send({"method": "initialized"})
        baseline, base_report = capture_case(rpc, server, workspace, None, "no-App-guidance baseline", args.timeout)
        report["cases"].append(base_report)
        active, active_report = capture_case(rpc, server, workspace, composed, "common + HELP_HUMAN", args.timeout)
        report["cases"].append(active_report)
        report["comparison"] = comparisons(baseline, active, composed, global_marker, project_marker)
        report["source_files_unchanged"] = (
            identity((home / "config.toml").read_bytes()) == report["scratch_sources"]["config"]
            and identity((home / "AGENTS.md").read_bytes()) == report["scratch_sources"]["native_global"]
            and identity((workspace / "AGENTS.md").read_bytes()) == report["scratch_sources"]["native_project"])
        report["passed"] = report["comparison"]["passed"] and report["source_files_unchanged"]
    except Exception as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        if rpc is not None:
            try:
                report["native_cleanup"] = rpc.close()
            except Exception as exc:
                report["cleanup_error"] = type(exc).__name__
                report["native_cleanup"] = {"process_group_end": "unknown"}
                report["passed"] = False
        if server is not None:
            server.shutdown()
            server.server_close()
        report["raw_scratch_retained"] = args.keep_scratch
        if args.keep_scratch:
            report["raw_scratch"] = str(scratch)
        else:
            shutil.rmtree(scratch)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
        print(json.dumps({"report": str(args.report), "passed": report["passed"],
                          "adoption": "unknown", "raw_scratch_retained": args.keep_scratch}))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
