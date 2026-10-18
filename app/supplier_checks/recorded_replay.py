#!/usr/bin/env python3
"""Synthetic, offline development peer for the redacted ST5/NV04 captures.

This is not Codex and does not qualify a supplier or App candidate. It executes
no recorded commands and opens no network, model or account connection. Caller
SHA-256 binds the exact recording file; replay preserves supplier JSON values
except correlated client-reply IDs. Audit JSONL is scratch evidence, not an EXP
or qualification record. Capture timestamps are metadata, never replay delays.

Use --recording PATH --sha256 HEX --generation N --audit PATH, optionally
--profile strict|app|app-recovery. Host CLI arguments may follow -- and remain
inert. --version reports the required synthetic development label. The optional
NV04 --pause-after-frame 28 --release PATH gate lets a test inspect the real
consumer between parent completion and the following child frames.
The audit destination must be fresh: exclusive creation refuses existing files,
symlinks and hardlinks without overwriting their bytes.
"""
import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import select
import stat
import sys
import time

FORMAT = "chirality.app-v4.hosting-capture.st5.v1"
VERSION = "codex-cli 0.160.0"
BINARY_SHA256 = "112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b"
SYNTHETIC_STANDING = "synthetic-offline-recorded-peer; not supplier/App qualification"
INPUT_TIMEOUT = 10.0
MAX_LINE_BYTES = 1024 * 1024
APP_CLIENT = {"name": "chirality-app-v4", "title": "Chirality App v4 (walking skeleton)",
              "version": "0.0.0-skeleton"}
PROTOTYPE_CLIENT = {"name": "chirality-st5-harness", "title": "Chirality ST-5 capture harness",
                    "version": "0.0.0-st5"}
CAPABILITIES = {"experimentalApi": True, "requestAttestation": False}


class ReplayError(Exception):
    """Only fixed, non-payload-bearing codes cross the CLI/audit boundary."""


def require(condition, code):
    if not condition:
        raise ReplayError(code)


def exact(left, right):
    # Python equality otherwise treats True as 1, and 1 as 1.0.
    return json.dumps(left, sort_keys=True, ensure_ascii=False, allow_nan=False) == json.dumps(
        right, sort_keys=True, ensure_ascii=False, allow_nan=False)


def unique_object(pairs):
    value = {}
    for key, item in pairs:
        require(key not in value, "duplicate-json-key")
        value[key] = item
    return value


def require_unicode_scalar_text(value):
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        raise ReplayError("invalid-json-unicode") from None


def decode(data):
    def reject_constant(unused):
        raise ReplayError("nonfinite-json")

    def finite_float(token):
        number = float(token)
        require(math.isfinite(number), "nonfinite-json")
        return number

    try:
        value = json.loads(data, object_pairs_hook=unique_object,
                           parse_constant=reject_constant, parse_float=finite_float)
        # Escaped lone UTF-16 surrogates are accepted by Python's JSON parser,
        # but cannot be written as UTF-8 protocol/audit data. Check keys too.
        pending = [value]
        while pending:
            item = pending.pop()
            if isinstance(item, str):
                require_unicode_scalar_text(item)
            elif isinstance(item, dict):
                pending.extend(item.keys())
                pending.extend(item.values())
            elif isinstance(item, list):
                pending.extend(item)
        return value
    except (ValueError, UnicodeError, RecursionError):
        raise ReplayError("invalid-json") from None


def rpc_id(value):
    require(type(value) in (int, str), "invalid-rpc-id")
    if isinstance(value, str):
        require_unicode_scalar_text(value)
    return type(value).__name__, value


def frame_kind(frame):
    require(isinstance(frame, dict), "invalid-frame-object")
    require("jsonrpc" not in frame or frame["jsonrpc"] == "2.0", "invalid-jsonrpc-envelope")
    if "id" in frame:
        rpc_id(frame["id"])
    if "method" in frame:
        require(isinstance(frame["method"], str) and bool(frame["method"]), "invalid-method")
        require("result" not in frame and "error" not in frame, "ambiguous-frame")
        require("params" not in frame or isinstance(frame["params"], dict), "invalid-params-shape")
        return "request" if "id" in frame else "notification"
    require("id" in frame and ("result" in frame) != ("error" in frame), "invalid-reply")
    require(set(frame) <= {"id", "result", "error", "jsonrpc"}, "invalid-reply-fields")
    if "error" in frame:
        error = frame["error"]
        require(isinstance(error, dict) and type(error.get("code")) is int
                and isinstance(error.get("message"), str), "invalid-error-shape")
    return "reply"


def without_envelope(frame):
    return {key: value for key, value in frame.items() if key != "jsonrpc"}


def validate_recording(value):
    require(isinstance(value, dict) and value.get("format") == FORMAT, "unsupported-format")
    scenario = value.get("scenario")
    require(scenario in ("st5", "st5-race", "nv04"), "unsupported-scenario")
    standing = "recorded" if scenario == "nv04" else "recorded-truncated"
    require(value.get("fixture_standing") == standing, "unsupported-recorded-standing")
    require(isinstance(value.get("standing_note"), str) and bool(value["standing_note"]), "missing-standing-note")
    identity = value.get("version_identity")
    require(isinstance(identity, dict) and identity.get("version_output") == VERSION
            and identity.get("binary_sha256") == BINARY_SHA256, "unsupported-supplier-pin")
    require(value.get("app_candidate") is None and value.get("app_side") ==
            "st5_harness.py (prototype observation harness)", "unsupported-capture-origin")
    require(exact(value.get("declared_capabilities"), CAPABILITIES), "unsupported-capture-capabilities")
    events = value.get("events")
    require(isinstance(events, list) and events and isinstance(events[0], dict)
            and events[0].get("event") == "begin" and events[0].get("scenario") == scenario
            and events[0].get("pin") == "0.160.0", "invalid-scenario-pin-event")
    frames = value.get("frames")
    require(isinstance(frames, list) and bool(frames), "missing-frames")
    generations, positions, pending, seen = {}, {}, {}, {}
    last_generation, last_time = 1, -1
    for index, row in enumerate(frames):
        require(isinstance(row, dict) and set(row) ==
                {"generation", "direction", "position", "t_ms", "redacted", "frame"}, "invalid-frame-record")
        generation, direction = row["generation"], row["direction"]
        require(type(generation) is int and generation in (last_generation, last_generation + 1), "invalid-generation-order")
        require(direction in ("app->codex", "codex->app"), "invalid-direction")
        require(type(row["position"]) is int and row["position"] == positions.get((generation, direction), 0) + 1,
                "invalid-frame-position")
        positions[generation, direction] = row["position"]
        stamp = row["t_ms"]
        require(type(stamp) in (int, float) and 0 <= stamp <= 2**53 and stamp >= last_time, "invalid-frame-time")
        require(type(row["redacted"]) is bool, "invalid-redaction-marker")
        last_generation, last_time = generation, stamp
        generations.setdefault(generation, []).append(index)
        frame = row["frame"]
        kind = frame_kind(frame)
        if kind == "request":
            key = generation, direction, rpc_id(frame["id"])
            require(key not in seen, "duplicate-recorded-request-id")
            seen[key] = True
            pending[key] = frame
        elif kind == "reply":
            opposite = "codex->app" if direction == "app->codex" else "app->codex"
            key = generation, opposite, rpc_id(frame["id"])
            require(key in pending, "uncorrelated-recorded-reply")
            del pending[key]
    expected_generations = {1} if scenario == "nv04" else {1, 2}
    require(set(generations) == expected_generations, "unsupported-generations")
    for generation, indices in generations.items():
        first = frames[indices[0]]
        require(first["direction"] == "app->codex" and first["frame"].get("method") == "initialize"
                and frame_kind(first["frame"]) == "request", "missing-generation-initialize")
        require(exact(first["frame"].get("params"), {"clientInfo": PROTOTYPE_CLIENT,
                "capabilities": CAPABILITIES}), "unsupported-recorded-initialize")
        require(len(indices) > 3 and frames[indices[3]]["direction"] == "app->codex"
                and exact(without_envelope(frames[indices[3]]["frame"]), {"method": "initialized"}),
                "missing-recorded-initialized")
        last = frames[indices[-1]]
        if scenario != "nv04" and generation == 1:
            require(last["direction"] == "app->codex" and last["frame"].get("method") == "thread/turns/list"
                    and frame_kind(last["frame"]) == "request", "missing-captured-unanswered-request")
            expected_pending = {(1, "app->codex", rpc_id(last["frame"]["id"]))}
            require({key for key in pending if key[0] == generation} == expected_pending, "invalid-capture-pending-requests")
        else:
            require(not any(key[0] == generation for key in pending), "truncated-recorded-correlation")
            if scenario == "nv04":
                require(frame_kind(last["frame"]) == "reply" and len(indices) > 1
                        and frames[indices[-2]]["frame"].get("method") == "thread/loaded/list",
                        "truncated-nv04-ending")
            else:
                require(last["direction"] == "codex->app" and
                        last["frame"].get("method") == "thread/goal/cleared", "truncated-st5-ending")
    return value


def load_recording(path, expected_sha256):
    require(isinstance(expected_sha256, str) and re.fullmatch(r"[0-9a-fA-F]{64}", expected_sha256), "invalid-sha256")
    try:
        data = Path(path).read_bytes()
    except OSError:
        raise ReplayError("recording-read-failed") from None
    digest = hashlib.sha256(data).hexdigest()
    require(digest == expected_sha256.lower(), "recording-sha256-mismatch")
    return validate_recording(decode(data))


class Audit:
    def __init__(self, stream):
        self.stream = stream

    def emit(self, event, **fields):
        self.stream.write(json.dumps({"event": event, **fields}, ensure_ascii=False, allow_nan=False) + "\n")
        self.stream.flush()


class JsonLineInput:
    """Read a complete bounded line by deadline, including partial-line stalls."""
    def __init__(self, stream, timeout=INPUT_TIMEOUT):
        self.fd, self.buffer, self.timeout = stream.fileno(), b"", timeout

    def read(self):
        deadline = time.monotonic() + self.timeout
        while b"\n" not in self.buffer:
            remaining = deadline - time.monotonic()
            require(remaining > 0 and bool(select.select([self.fd], [], [], remaining)[0]), "input-timeout")
            chunk = os.read(self.fd, 65536)
            if not chunk:
                require(not self.buffer, "unterminated-input-frame")
                return None
            self.buffer += chunk
            require(len(self.buffer.split(b"\n", 1)[0]) <= MAX_LINE_BYTES, "input-frame-too-large")
        line, self.buffer = self.buffer.split(b"\n", 1)
        frame = decode(line)
        frame_kind(frame)
        return frame


class Replay:
    def __init__(self, recording, generation, profile, audit, *, sha256=None,
                 pause_after_frame=None, release=None):
        self.recording, self.generation, self.profile, self.audit = recording, generation, profile, audit
        require(type(generation) is int and any(row["generation"] == generation for row in recording["frames"]),
                "unsupported-selected-generation")
        require(profile in ("strict", "app", "app-recovery"), "unsupported-profile")
        require(profile != "app" or generation == 1, "unsupported-app-profile")
        require(profile != "app-recovery" or (recording["scenario"] == "st5" and generation == 2),
                "unsupported-recovery-profile")
        require((pause_after_frame is None) == (release is None), "incomplete-pause-gate")
        if pause_after_frame is not None:
            require(type(pause_after_frame) is int and pause_after_frame == 28 and
                    recording["scenario"] == "nv04" and generation == 1, "unsupported-pause-gate")
            require(len(recording["frames"]) > 28 and recording["frames"][28]["direction"] == "codex->app" and
                    recording["frames"][28]["frame"].get("method") == "turn/completed",
                    "unsupported-pause-frame")
            require(not Path(release).exists(), "release-marker-already-exists")
        self.pause_after_frame, self.release = pause_after_frame, release
        self.indices = [i for i, row in enumerate(recording["frames"]) if row["generation"] == generation]
        self.outside_segment = []
        if profile == "app-recovery":
            end = next((offset + 1 for offset, index in enumerate(self.indices)
                        if offset and recording["frames"][self.indices[offset - 1]]["frame"].get("method") == "thread/turns/list"
                        and frame_kind(recording["frames"][index]["frame"]) == "reply"), None)
            require(end is not None, "missing-recovery-segment")
            self.indices, self.outside_segment = self.indices[:end], self.indices[end:]
        self.consumed, self.current_index = [], None
        self.id_map, self.actual_ids, self.pending_server = {}, set(), set()
        self.audit.emit("binding", sha256=sha256, scenario=recording["scenario"], generation=generation,
                        profile=profile, recorded_standing=recording["fixture_standing"],
                        synthetic_standing=SYNTHETIC_STANDING, selected_frame_indices=self.indices,
                        outside_segment_frame_indices=self.outside_segment,
                        other_generation_frame_indices=[i for i, row in enumerate(recording["frames"])
                                                        if row["generation"] != generation])

    def adapted_params(self, expected, actual):
        """Return only declared, exact App alternatives; never wildcard fields."""
        require(isinstance(expected, dict), "invalid-captured-adaptation-request")
        changes = []
        method, params = expected.get("method"), expected.get("params")
        if method == "initialize":
            require(exact(params, {"clientInfo": PROTOTYPE_CLIENT, "capabilities": CAPABILITIES}),
                    "unsupported-captured-initialize")
            adapted = {"clientInfo": APP_CLIENT, "capabilities": {**CAPABILITIES, "explicitGatewayOauth": True}}
            if exact(actual, adapted):
                return adapted, ["initialize.clientInfo:prototype-to-current-App", "initialize.capabilities.explicitGatewayOauth:add-true"]
        if self.profile == "app" and method == "thread/start":
            policy = "never" if self.recording["scenario"] == "nv04" else "on-request"
            require(exact(params, {"cwd": "<WORKSPACE>", "approvalPolicy": policy, "sandbox": "read-only"}),
                    "invalid-captured-thread-start-params")
            require("id" in expected, "invalid-captured-thread-start-request")
            recorded_id = rpc_id(expected["id"])
            reply = next((row["frame"] for row in self.recording["frames"]
                          if row["generation"] == self.generation and row["direction"] == "codex->app"
                          and frame_kind(row["frame"]) == "reply" and rpc_id(row["frame"]["id"]) == recorded_id), None)
            require(isinstance(reply, dict) and isinstance(reply.get("result"), dict),
                    "invalid-captured-thread-start-reply")
            result = reply["result"]
            adapted = {"cwd": params["cwd"], "model": result.get("model"), "modelProvider": result.get("modelProvider")}
            require(isinstance(adapted["model"], str) and bool(adapted["model"])
                    and isinstance(adapted["modelProvider"], str) and bool(adapted["modelProvider"]),
                    "missing-captured-model-selection")
            return adapted, ["thread/start:omit-captured-approvalPolicy-and-sandbox", "thread/start:add-exact-captured-model-and-modelProvider"]
        if self.profile == "app" and method == "turn/start":
            require(isinstance(params, dict) and set(params) == {"threadId", "input"}
                    and isinstance(params["threadId"], str) and bool(params["threadId"]),
                    "invalid-captured-turn-start-params")
            elements = params["input"]
            require(isinstance(elements, list) and len(elements) == 1 and isinstance(elements[0], dict)
                    and set(elements[0]) == {"type", "text"} and elements[0]["type"] == "text"
                    and isinstance(elements[0]["text"], str) and bool(elements[0]["text"]),
                    "unsupported-captured-text-input")
            adapted = copy.deepcopy(params)
            adapted["input"][0]["text_elements"] = []
            return adapted, ["turn/start.input[0].text_elements:add-empty-array"]
        if self.profile == "app-recovery" and method == "thread/read":
            require(isinstance(params, dict) and set(params) == {"threadId", "includeTurns"}
                    and isinstance(params["threadId"], str) and bool(params["threadId"])
                    and params["includeTurns"] is True, "invalid-captured-thread-read-params")
            return {**params, "includeTurns": False}, ["thread/read.includeTurns:true-to-false"]
        if self.profile == "app-recovery" and method == "thread/turns/list":
            require(isinstance(params, dict) and set(params) == {"threadId", "itemsView"}
                    and isinstance(params["threadId"], str) and bool(params["threadId"])
                    and params["itemsView"] == "full", "invalid-captured-turns-list-params")
            return {**params, "itemsView": "summary", "sortDirection": "desc"}, [
                "thread/turns/list.itemsView:full-to-summary", "thread/turns/list.sortDirection:add-desc"]
        return params, changes

    def accept(self, expected, actual):
        require(actual is not None, "premature-input-eof")
        kind = frame_kind(actual)
        require(kind == frame_kind(expected), "input-kind-mismatch")
        actual_body, expected_body = without_envelope(actual), without_envelope(expected)
        changes, correlation = [], {}
        if kind == "request":
            recorded_id, actual_id = rpc_id(expected["id"]), rpc_id(actual["id"])
            require(recorded_id not in self.id_map and actual_id not in self.actual_ids, "duplicate-actual-request-id")
            expected_body["id"] = actual["id"]
            params, changes = self.adapted_params(expected, actual.get("params"))
            if "params" in expected_body:
                expected_body["params"] = params
            require(exact(expected_body, actual_body), "request-method-or-params-mismatch")
            self.id_map[recorded_id] = actual["id"]
            self.actual_ids.add(actual_id)
            correlation = {"recorded_rpc_id": expected["id"], "actual_rpc_id": actual["id"],
                           "recorded_rpc_id_type": recorded_id[0], "actual_rpc_id_type": actual_id[0]}
        else:
            if kind == "reply":
                require(rpc_id(actual["id"]) in self.pending_server, "unsolicited-or-wrong-server-reply-id")
            require(exact(expected_body, actual_body), "reply-or-notification-payload-mismatch")
            if kind == "reply":
                self.pending_server.remove(rpc_id(actual["id"]))
                correlation = {"recorded_rpc_id": expected["id"], "actual_rpc_id": actual["id"],
                               "recorded_rpc_id_type": rpc_id(expected["id"])[0],
                               "actual_rpc_id_type": rpc_id(actual["id"])[0]}
        return {"adaptations": changes, **correlation}

    def pause(self):
        self.audit.emit("paused", frame_index=self.current_index, reason="nv04-parent-completed-consumer-inspection")
        deadline = time.monotonic() + INPUT_TIMEOUT
        while time.monotonic() < deadline:
            try:
                mode = Path(self.release).stat().st_mode
                require(stat.S_ISREG(mode), "invalid-release-marker")
                self.audit.emit("released", frame_index=self.current_index)
                return
            except FileNotFoundError:
                time.sleep(.01)
        raise ReplayError("release-marker-timeout")

    def remaining(self):
        return [index for index in self.indices if index not in self.consumed]

    def run(self, reader, writer):
        try:
            for index in self.indices:
                self.current_index = index
                row, info = self.recording["frames"][index], {}
                frame = row["frame"]
                if row["direction"] == "app->codex":
                    info = self.accept(frame, reader.read())
                else:
                    outgoing = copy.deepcopy(frame)
                    kind = frame_kind(frame)
                    if kind == "reply":
                        key = rpc_id(frame["id"])
                        require(key in self.id_map, "missing-actual-client-correlation")
                        outgoing["id"] = self.id_map[key]
                        info = {"recorded_rpc_id": frame["id"], "actual_rpc_id": outgoing["id"],
                                "recorded_rpc_id_type": key[0], "actual_rpc_id_type": rpc_id(outgoing["id"])[0]}
                    elif kind == "request":
                        self.pending_server.add(rpc_id(frame["id"]))
                    writer.write(json.dumps(outgoing, ensure_ascii=False, allow_nan=False) + "\n")
                    writer.flush()
                self.consumed.append(index)
                self.audit.emit("frame", frame_index=index, direction=row["direction"], kind=frame_kind(frame), **info)
                if index == self.pause_after_frame:
                    self.pause()
            captured_eof = self.recording["scenario"] != "nv04" and self.generation == 1
            if not captured_eof:
                self.audit.emit("awaiting-input-eof", remaining_frame_indices=[],
                                outside_segment_frame_indices=self.outside_segment)
                require(reader.read() is None, "extra-input-after-segment")
            self.audit.emit("finish", outcome="captured-unanswered-request-eof" if captured_eof else "input-eof-after-segment",
                            consumed_frame_indices=self.consumed, remaining_frame_indices=[],
                            outside_segment_frame_indices=self.outside_segment,
                            acknowledgment="not-inferred-from-answer-write")
        except (ReplayError, OSError, ValueError, RecursionError) as error:
            code = str(error) if isinstance(error, ReplayError) else "peer-io-or-value-error"
            self.audit.emit("error", code=code, frame_index=self.current_index,
                            consumed_frame_indices=self.consumed, remaining_frame_indices=self.remaining(),
                            outside_segment_frame_indices=self.outside_segment)
            if isinstance(error, ReplayError):
                raise
            raise ReplayError(code) from None


class SafeParser(argparse.ArgumentParser):
    def error(self, unused):
        raise ReplayError("invalid-cli-arguments")


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    split = args.index("--") if "--" in args else len(args)
    options, host_args = args[:split], args[split + 1:]
    if "--version" in options or "--version" in host_args:
        print(VERSION)
        return 0
    audit = None
    try:
        parser = SafeParser(description=__doc__)
        parser.add_argument("--recording", required=True, type=Path)
        parser.add_argument("--sha256", required=True)
        parser.add_argument("--generation", required=True, type=int)
        parser.add_argument("--audit", required=True, type=Path)
        parser.add_argument("--profile", choices=("strict", "app", "app-recovery"), default="strict")
        parser.add_argument("--pause-after-frame", type=int)
        parser.add_argument("--release", type=Path)
        config = parser.parse_args(options)
        require(not host_args or "app-server" in host_args, "unsupported-host-cli-mode")
        try:
            # O_CREAT|O_EXCL is checked atomically by open: an alias created
            # concurrently cannot turn this operation into a truncating write.
            stream = config.audit.open("x", encoding="utf-8")
        except FileExistsError:
            raise ReplayError("audit-destination-exists") from None
        with stream:
            audit = Audit(stream)
            audit.emit("start", synthetic_standing=SYNTHETIC_STANDING)
            replay = None
            try:
                recording = load_recording(config.recording, config.sha256)
                replay = Replay(recording, config.generation, config.profile, audit, sha256=config.sha256.lower(),
                                pause_after_frame=config.pause_after_frame, release=config.release)
                replay.run(JsonLineInput(sys.stdin.buffer), sys.stdout)
            except (ReplayError, OSError, ValueError, RecursionError) as error:
                code = str(error) if isinstance(error, ReplayError) else "peer-io-or-value-error"
                # Replay.run records its own remaining indices. Construction,
                # loading and input setup can also fail before run is entered.
                if replay is None or not isinstance(error, ReplayError):
                    audit.emit("error", code=code,
                               frame_index=replay.current_index if replay is not None else None,
                               consumed_frame_indices=replay.consumed if replay is not None else [],
                               remaining_frame_indices=replay.remaining() if replay is not None else None,
                               outside_segment_frame_indices=replay.outside_segment if replay is not None else [])
                audit.emit("exit", outcome="error", code=code)
                if isinstance(error, ReplayError):
                    raise
                raise ReplayError(code) from None
            audit.emit("exit", outcome="success")
        return 0
    except ReplayError as error:
        print("recorded-replay: " + str(error), file=sys.stderr)
    except (OSError, ValueError, RecursionError):
        # Paths, protocol payloads and OS exception text can contain private input.
        print("recorded-replay: peer-io-or-value-error", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
