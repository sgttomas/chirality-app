"""Offline regression tests for the synthetic redacted-recording supplier peer."""
import copy
from contextlib import redirect_stderr
import hashlib
import io
import json
import os
from pathlib import Path
import select
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

import recorded_replay as peer

HERE = Path(__file__).resolve().parent
RECORDINGS = HERE.parents[1] / "execution/PKG-01/DEL-01-01/Design/prototype/st5/recordings"


def capture(scenario="st5"):
    path = RECORDINGS / (scenario + ".recording.json")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return path, digest, peer.load_recording(path, digest)


def inputs(recording, generation, profile="strict", remap=False):
    frames = []
    for row in recording["frames"]:
        if row["generation"] != generation or row["direction"] != "app->codex":
            continue
        frame = copy.deepcopy(row["frame"])
        if "method" in frame and "id" in frame and remap:
            # Simultaneously prove string "1" and integer 1 are distinct IDs.
            frame["id"] = {1: "1", 2: 1, 3: "actual-turn", 4: 104, 5: 105}[frame["id"]]
        if profile != "strict" and frame.get("method") == "initialize":
            frame["params"] = {"clientInfo": peer.APP_CLIENT,
                               "capabilities": {**peer.CAPABILITIES, "explicitGatewayOauth": True}}
        if profile == "app" and frame.get("method") == "thread/start":
            frame["params"] = {"cwd": "<WORKSPACE>", "model": "st5-stub-model", "modelProvider": "st5_stub"}
        if profile == "app" and frame.get("method") == "turn/start":
            frame["params"]["input"][0]["text_elements"] = []
        if profile == "app-recovery" and frame.get("method") == "thread/read":
            frame["params"]["includeTurns"] = False
        if profile == "app-recovery" and frame.get("method") == "thread/turns/list":
            frame["params"].update(itemsView="summary", sortDirection="desc")
        frames.append(frame)
        if profile == "app-recovery" and frame.get("method") == "thread/turns/list":
            break
    return frames


class ScriptedInput:
    def __init__(self, frames):
        self.frames = iter(frames)

    def read(self):
        return next(self.frames, None)


def run_memory(recording, generation=1, profile="strict", supplied=None, **kwargs):
    audit, output = io.StringIO(), io.StringIO()
    replay = peer.Replay(recording, generation, profile, peer.Audit(audit), **kwargs)
    replay.run(ScriptedInput(inputs(recording, generation, profile) if supplied is None else supplied), output)
    return [json.loads(line) for line in output.getvalue().splitlines()], [
        json.loads(line) for line in audit.getvalue().splitlines()]


class RecordingValidation(unittest.TestCase):
    def test_all_real_recordings_bind_and_progress_through_each_generation(self):
        for scenario in ("st5", "st5-race", "nv04"):
            _, _, recording = capture(scenario)
            for generation in sorted({row["generation"] for row in recording["frames"]}):
                with self.subTest(scenario=scenario, generation=generation):
                    output, audit = run_memory(recording, generation)
                    self.assertEqual(output, [row["frame"] for row in recording["frames"]
                                              if row["generation"] == generation and row["direction"] == "codex->app"])
                    self.assertEqual(audit[-1]["event"], "finish")
                    self.assertEqual(audit[-1]["remaining_frame_indices"], [])
                    self.assertIn("synthetic", audit[0]["synthetic_standing"])

    def test_hash_and_malformed_json_are_refused(self):
        path, digest, _ = capture()
        with self.assertRaisesRegex(peer.ReplayError, "sha256-mismatch"):
            peer.load_recording(path, "0" * 64)
        for invalid in ("bad", "0" * 63):
            with self.assertRaisesRegex(peer.ReplayError, "invalid-sha256"):
                peer.load_recording(path, invalid)
        for data in (b'{"format":1,"format":2}', b'{"bad":NaN}', b'{', b'\xff'):
            with tempfile.TemporaryDirectory() as root:
                target = Path(root) / "recording.json"
                target.write_bytes(data)
                with self.assertRaises(peer.ReplayError):
                    peer.load_recording(target, hashlib.sha256(data).hexdigest())
        self.assertEqual(peer.load_recording(path, digest.upper())["scenario"], "st5")

    def test_structural_metadata_order_and_correlation_corruptions_are_refused(self):
        _, _, recording = capture()
        mutations = [
            lambda d: d.update(format="unknown"),
            lambda d: d.update(scenario="other"),
            lambda d: d.update(fixture_standing="scripted"),
            lambda d: d["version_identity"].update(version_output="codex-cli 9.9.9"),
            lambda d: d["version_identity"].update(binary_sha256="0" * 64),
            lambda d: d["events"][0].update(pin="9.9.9"),
            lambda d: d["frames"][0].update(generation=True),
            lambda d: d["frames"][0].update(direction="supplier->host"),
            lambda d: d["frames"][0].update(position=2),
            lambda d: d["frames"][0].update(redacted=1),
            lambda d: d["frames"][1].update(t_ms=-1),
            lambda d: d["frames"][1].update(t_ms=10**1000),
            lambda d: d["frames"][0]["frame"].update(id=True),
            lambda d: d["frames"][0]["frame"].update(jsonrpc="1.0"),
            lambda d: d["frames"][1]["frame"].update(id="1"),
            lambda d: d["frames"][4]["frame"].update(id=1),
            lambda d: d["frames"][17]["frame"].update(id=99),
            lambda d: d["frames"][0]["frame"].update(result={}),
            lambda d: d["frames"].pop(),
            lambda d: d["frames"].__delitem__(18),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(corruption=index):
                altered = copy.deepcopy(recording)
                mutate(altered)
                with self.assertRaises(peer.ReplayError):
                    peer.validate_recording(altered)

    def test_typed_recording_and_actual_ids_preserve_correlation(self):
        _, _, recording = capture()
        supplied = inputs(recording, 1, remap=True)
        output, audit = run_memory(recording, supplied=supplied)
        self.assertEqual([frame["id"] for frame in output if "id" in frame and "method" not in frame],
                         ["1", 1, "actual-turn"])
        self.assertEqual(next(frame["id"] for frame in output if frame.get("method") ==
                              "item/commandExecution/requestApproval"), 0)
        rows = [row for row in audit if row.get("actual_rpc_id") == "1"]
        self.assertTrue(rows)
        self.assertTrue(all(row["actual_rpc_id_type"] == "str" for row in rows))
        # Captured IDs also distinguish string and integer in the same generation.
        recording["frames"][4]["frame"]["id"] = "1"
        recording["frames"][5]["frame"]["id"] = "1"
        peer.validate_recording(recording)
        output, _ = run_memory(recording)
        self.assertEqual(output[0]["id"], 1)
        self.assertEqual(output[2]["id"], "1")

    def test_negative_method_params_decision_ids_and_premature_eof(self):
        _, _, recording = capture()
        changes = [
            (0, lambda f: f["params"]["capabilities"].update(experimentalApi=1)),
            (0, lambda f: f["params"]["clientInfo"].update(name="unknown")),
            (0, lambda f: f.update(jsonrpc="1.0")),
            (2, lambda f: f.update(method="thread/resume")),
            (2, lambda f: f["params"].update(cwd="/unknown/private/value")),
            (2, lambda f: f["params"].update(extra=True)),
            (2, lambda f: f.update(id=1)),
            (2, lambda f: f.update(id=None)),
            (4, lambda f: f["result"].update(decision="cancel")),
            (4, lambda f: f.update(id="0")),
            (4, lambda f: f.update(id=12345)),
            (4, lambda f: f.update(error={"code": -1, "message": "unknown"})),
        ]
        for case, (index, mutate) in enumerate(changes):
            with self.subTest(case=case):
                supplied = inputs(recording, 1)
                mutate(supplied[index])
                with self.assertRaises(peer.ReplayError):
                    run_memory(recording, supplied=supplied)
        with self.assertRaisesRegex(peer.ReplayError, "premature-input-eof"):
            run_memory(recording, supplied=inputs(recording, 1)[:-1])

    def test_optional_valid_envelope_only_and_no_answer_acknowledgment(self):
        _, _, recording = capture()
        supplied = inputs(recording, 1)
        for frame in supplied:
            frame.pop("jsonrpc", None)
        output, audit = run_memory(recording, supplied=supplied)
        self.assertFalse(any(frame.get("method") == "serverRequest/resolved" for frame in output))
        self.assertFalse(any(frame.get("method") == "turn/completed" for frame in output))
        self.assertEqual(audit[-1]["outcome"], "captured-unanswered-request-eof")
        self.assertEqual(audit[-1]["acknowledgment"], "not-inferred-from-answer-write")


class AppProfiles(unittest.TestCase):
    def test_adaptation_rejects_missing_reply_without_stop_iteration(self):
        _, _, recording = capture()
        replay = peer.Replay(recording, 1, "app", peer.Audit(io.StringIO()))
        expected = copy.deepcopy(recording["frames"][4]["frame"])
        expected["id"] = "no-captured-reply"
        with self.assertRaisesRegex(peer.ReplayError, "invalid-captured-thread-start-reply"):
            replay.adapted_params(expected, {})

    def test_exact_initialize_adaptation_is_allowed_and_audited_in_strict(self):
        _, _, recording = capture()
        supplied = inputs(recording, 1)
        supplied[0] = inputs(recording, 1, "app")[0]
        _, audit = run_memory(recording, supplied=supplied)
        row = next(row for row in audit if row.get("frame_index") == 0)
        self.assertEqual(len(row["adaptations"]), 2)
        for change in (lambda p: p["capabilities"].update(requestAttestation=True),
                       lambda p: p["capabilities"].update(explicitGatewayOauth=False),
                       lambda p: p["capabilities"].update(extra=True),
                       lambda p: p["clientInfo"].update(version="anything-else")):
            altered = copy.deepcopy(supplied)
            change(altered[0]["params"])
            with self.assertRaises(peer.ReplayError):
                run_memory(recording, supplied=altered)

    def test_app_profile_binds_exact_model_policy_omission_and_text_shape(self):
        for scenario in ("st5", "nv04", "st5-race"):
            _, _, recording = capture(scenario)
            output, audit = run_memory(recording, profile="app")
            self.assertEqual(output, [row["frame"] for row in recording["frames"]
                                      if row["generation"] == 1 and row["direction"] == "codex->app"])
            adaptations = [change for row in audit for change in row.get("adaptations", [])]
            self.assertIn("thread/start:add-exact-captured-model-and-modelProvider", adaptations)
            self.assertIn("turn/start.input[0].text_elements:add-empty-array", adaptations)
        for index, key, value in ((2, "model", "different"), (2, "modelProvider", "different"),
                                  (2, "approvalPolicy", "on-request"), (2, "cwd", "/changed")):
            supplied = inputs(recording, 1, "app")
            supplied[index]["params"][key] = value
            with self.assertRaises(peer.ReplayError):
                run_memory(recording, profile="app", supplied=supplied)
        supplied = inputs(recording, 1, "app")
        supplied[3]["params"]["input"][0]["text_elements"] = [{"unexpected": True}]
        with self.assertRaises(peer.ReplayError):
            run_memory(recording, profile="app", supplied=supplied)
        with self.assertRaises(peer.ReplayError):
            run_memory(recording, profile="strict", supplied=inputs(recording, 1, "app"))

    def test_recovery_changes_only_queries_and_ends_before_loaded_list_resume(self):
        _, _, recording = capture()
        output, audit = run_memory(recording, 2, "app-recovery", inputs(recording, 2, "app-recovery", remap=True))
        expected = [copy.deepcopy(row["frame"]) for row in recording["frames"][19:28]
                    if row["direction"] == "codex->app"]
        for frame in expected:
            if "id" in frame:
                frame["id"] = {1: "1", 2: 1, 3: "actual-turn"}[frame["id"]]
        self.assertEqual(output, expected)
        self.assertEqual(audit[-1]["outside_segment_frame_indices"], list(range(28, 35)))
        self.assertEqual(audit[-1]["consumed_frame_indices"], list(range(19, 28)))
        self.assertTrue(any("thread/read.includeTurns:true-to-false" in row.get("adaptations", []) for row in audit))
        supplied = inputs(recording, 2, "app-recovery")
        with self.assertRaises(peer.ReplayError):
            run_memory(recording, 2, "strict", supplied)
        for index, key, value in ((2, "includeTurns", True), (2, "threadId", "other"),
                                  (3, "itemsView", "full"), (3, "sortDirection", "asc"), (3, "extra", 1)):
            altered = copy.deepcopy(supplied)
            altered[index]["params"][key] = value
            with self.assertRaises(peer.ReplayError):
                run_memory(recording, 2, "app-recovery", altered)
        with self.assertRaisesRegex(peer.ReplayError, "extra-input"):
            run_memory(recording, 2, "app-recovery", supplied + inputs(recording, 2)[4:5])
        for scenario, generation, profile in (("st5", 1, "app-recovery"), ("st5-race", 2, "app-recovery"),
                                              ("nv04", 1, "app-recovery"), ("st5", 2, "app")):
            with self.assertRaises(peer.ReplayError):
                run_memory(capture(scenario)[2], generation, profile)


class SubprocessReplay(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.TemporaryDirectory()
        self.addCleanup(self.root.cleanup)
        self.audit = Path(self.root.name) / "audit.jsonl"

    def start(self, scenario="st5", generation=1, extra=()):
        path, digest, recording = capture(scenario)
        command = [sys.executable, str(HERE / "recorded_replay.py"), "--recording", str(path),
                   "--sha256", digest, "--generation", str(generation), "--audit", str(self.audit), *extra]
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.addCleanup(self.cleanup_process, process)
        return process, peer.JsonLineInput(process.stdout, timeout=2), recording

    @staticmethod
    def cleanup_process(process):
        if process.poll() is None:
            process.kill()
        process.wait(timeout=3)
        for stream in (process.stdin, process.stdout, process.stderr):
            if stream and not stream.closed:
                stream.close()

    @staticmethod
    def send(process, frame):
        process.stdin.write(json.dumps(frame).encode() + b"\n")
        process.stdin.flush()

    def invoke(self, path, digest, audit, profile="app", generation=1, supplied=(), extra=()):
        return subprocess.run([sys.executable, str(HERE / "recorded_replay.py"),
                               "--recording", str(path), "--sha256", digest,
                               "--generation", str(generation), "--audit", str(audit),
                               "--profile", profile, *extra],
                              input=b"".join(json.dumps(frame).encode() + b"\n" for frame in supplied),
                              capture_output=True, timeout=2)

    def test_malformed_adaptation_metadata_has_fixed_error_and_terminal_audit(self):
        _, _, original = capture()
        cases = [
            (1, "app", lambda d: d["frames"][5]["frame"].update(result=None)),
            (1, "app", lambda d: d["frames"][5]["frame"].update(result=[])),
            (1, "app", lambda d: d["frames"][5]["frame"].update(result="private-malformed-result")),
            (1, "app", lambda d: d["frames"][5]["frame"]["result"].pop("model")),
            (1, "app", lambda d: d["frames"][5]["frame"]["result"].update(modelProvider=None)),
            (1, "app", lambda d: d["frames"][4]["frame"].pop("params")),
            (1, "app", lambda d: d["frames"][4]["frame"]["params"].pop("cwd")),
            (1, "app", lambda d: d["frames"][4]["frame"]["params"].update(cwd=[])),
            (1, "app", lambda d: d["frames"][7]["frame"].pop("params")),
            (1, "app", lambda d: d["frames"][7]["frame"]["params"].update(input=[None])),
            (1, "app", lambda d: d["frames"][7]["frame"]["params"].update(input=[[]])),
            (1, "app", lambda d: d["frames"][7]["frame"]["params"].update(input=["private-malformed-input"])),
            (1, "app", lambda d: d["frames"][7]["frame"]["params"]["input"][0].pop("text")),
            (1, "app", lambda d: d["frames"][7]["frame"]["params"]["input"][0].update(text=[])),
            (2, "app-recovery", lambda d: d["frames"][23]["frame"].pop("params")),
            (2, "app-recovery", lambda d: d["frames"][23]["frame"]["params"].pop("threadId")),
            (2, "app-recovery", lambda d: d["frames"][26]["frame"].pop("params")),
            (2, "app-recovery", lambda d: d["frames"][26]["frame"]["params"].update(itemsView=None)),
        ]
        for index, (generation, profile, mutate) in enumerate(cases):
            with self.subTest(case=index):
                altered = copy.deepcopy(original)
                mutate(altered)
                path = Path(self.root.name) / f"malformed-{index}.json"
                data = json.dumps(altered).encode()
                path.write_bytes(data)
                audit = Path(self.root.name) / f"malformed-audit-{index}.jsonl"
                result = self.invoke(path, hashlib.sha256(data).hexdigest(), audit, profile,
                                     generation, inputs(original, generation, profile))
                self.assertEqual(result.returncode, 2, result.stderr.decode())
                self.assertNotIn(b"Traceback", result.stderr)
                self.assertNotIn(str(HERE).encode(), result.stderr)
                self.assertNotIn(b"private-malformed", result.stderr + audit.read_bytes())
                rows = [json.loads(line) for line in audit.read_text().splitlines()]
                self.assertEqual(rows[-1]["event"], "exit")
                self.assertEqual(rows[-1]["outcome"], "error")
                self.assertTrue(rows[-1]["code"].startswith(("invalid-captured-", "missing-captured-", "unsupported-captured-")))
                self.assertEqual(rows[-2]["event"], "error")
                self.assertEqual(result.stderr, ("recorded-replay: " + rows[-1]["code"] + "\n").encode())
                for line in result.stdout.splitlines():
                    peer.frame_kind(json.loads(line))
                self.assertFalse(any(row["event"] == "finish" for row in rows))
                self.assertEqual(path.read_bytes(), data)

    def test_short_recording_refuses_pause_index_with_terminal_audit(self):
        _, _, recording = capture("nv04")
        recording["frames"] = recording["frames"][:10] + recording["frames"][-2:]
        positions = {}
        for row in recording["frames"]:
            positions[row["direction"]] = positions.get(row["direction"], 0) + 1
            row["position"] = positions[row["direction"]]
        peer.validate_recording(recording)
        path = Path(self.root.name) / "short-recording.json"
        data = json.dumps(recording).encode()
        path.write_bytes(data)
        result = self.invoke(path, hashlib.sha256(data).hexdigest(), self.audit,
                             extra=("--pause-after-frame", "28", "--release", str(Path(self.root.name) / "release")))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stderr, b"recorded-replay: unsupported-pause-frame\n")
        self.assertEqual(result.stdout, b"")
        self.assertEqual(json.loads(self.audit.read_text().splitlines()[-1]),
                         {"event": "exit", "outcome": "error", "code": "unsupported-pause-frame"})
        self.assertEqual(path.read_bytes(), data)

    def test_existing_audit_destinations_and_source_aliases_preserve_all_bytes(self):
        original_path, digest, recording = capture()
        original = original_path.read_bytes()
        for kind in ("same-path", "symlink", "dangling-symlink", "hardlink", "existing-output"):
            with self.subTest(kind=kind):
                root = Path(self.root.name) / kind
                root.mkdir()
                path, audit = root / "recording.json", root / "audit.jsonl"
                path.write_bytes(original)
                if kind == "same-path":
                    audit = path
                elif kind == "symlink":
                    audit.symlink_to(path)
                elif kind == "dangling-symlink":
                    audit.symlink_to(root / "must-not-be-created")
                elif kind == "hardlink":
                    os.link(path, audit)
                else:
                    audit.write_bytes(b"existing-audit-must-stay-unchanged\n")
                audit_before = audit.read_bytes() if audit.exists() else None
                result = self.invoke(path, digest, audit, supplied=inputs(recording, 1, "app"))
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, b"")
                self.assertEqual(path.read_bytes(), original)
                if audit_before is not None:
                    self.assertEqual(audit.read_bytes(), audit_before)
                else:
                    self.assertTrue(audit.is_symlink())
                    self.assertFalse(audit.exists())
                self.assertEqual(result.stderr, b"recorded-replay: audit-destination-exists\n")

    def test_audit_link_created_immediately_before_open_cannot_clobber_source(self):
        original_path, digest, _ = capture()
        original = original_path.read_bytes()
        path = Path(self.root.name) / "recording.json"
        path.write_bytes(original)
        open_original = Path.open

        def racing_open(target, mode="r", *args, **kwargs):
            if target == self.audit and mode in ("w", "x"):
                os.link(path, self.audit)
            return open_original(target, mode, *args, **kwargs)

        errors = io.StringIO()
        with patch.object(Path, "open", racing_open), redirect_stderr(errors):
            code = peer.main(["--recording", str(path), "--sha256", digest,
                              "--generation", "1", "--audit", str(self.audit)])
        self.assertEqual(code, 2)
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(self.audit.read_bytes(), original)
        self.assertEqual(errors.getvalue(), "recorded-replay: audit-destination-exists\n")

    def test_st5_waits_for_unanswered_request_before_eof_without_ack(self):
        process, reader, recording = self.start(extra=("--", "-c", "fixture=inert", "app-server"))
        output = []
        for row in recording["frames"][:18]:
            if row["direction"] == "app->codex":
                self.send(process, row["frame"])
            else:
                output.append(reader.read())
        self.assertIsNone(process.poll())
        self.assertEqual(reader.buffer, b"")
        self.assertFalse(select.select([process.stdout], [], [], .05)[0])
        self.send(process, recording["frames"][18]["frame"])
        self.assertIsNone(reader.read())
        self.assertEqual(process.wait(timeout=2), 0)
        self.assertFalse(any(frame.get("method") == "serverRequest/resolved" for frame in output))
        self.assertFalse(any(frame.get("method") == "turn/completed" for frame in output))
        self.assertEqual(json.loads(self.audit.read_text().splitlines()[-1])["outcome"], "success")

    def test_nv04_last_reply_remains_observable_before_process_eof(self):
        process, reader, recording = self.start("nv04")
        for row in recording["frames"]:
            if row["direction"] == "app->codex":
                self.send(process, row["frame"])
            else:
                self.assertEqual(reader.read(), row["frame"])
        self.assertIsNone(process.poll())
        self.assertFalse(select.select([process.stdout], [], [], .05)[0])
        process.stdin.close()
        self.assertIsNone(reader.read())
        self.assertEqual(process.wait(timeout=2), 0)

    def test_nv04_pause_gate_preserves_interleaving_and_order(self):
        release = Path(self.root.name) / "release"
        process, reader, recording = self.start("nv04", extra=("--pause-after-frame", "28", "--release", str(release)))
        for row in recording["frames"][:29]:
            if row["direction"] == "app->codex":
                self.send(process, row["frame"])
            else:
                self.assertEqual(reader.read(), row["frame"])
        deadline = time.monotonic() + 2
        while '"event": "paused"' not in self.audit.read_text() and time.monotonic() < deadline:
            time.sleep(.01)
        self.assertIn('"event": "paused"', self.audit.read_text())
        self.assertEqual(reader.buffer, b"")
        self.assertFalse(select.select([process.stdout], [], [], .05)[0])
        release.touch()
        for row in recording["frames"][29:]:
            if row["direction"] == "app->codex":
                self.send(process, row["frame"])
            else:
                self.assertEqual(reader.read(), row["frame"])
        process.stdin.close()
        self.assertIsNone(reader.read())
        self.assertEqual(process.wait(timeout=2), 0)
        self.assertIn('"event": "released"', self.audit.read_text())

    def test_clean_nonzero_error_and_audit_never_echo_unknown_payload(self):
        process, reader, _ = self.start()
        unknown = "PRIVATE_CANARY_NEVER_ECHO_7b459"
        self.send(process, {"method": unknown, "id": "private-id", "params": {"secret": unknown}})
        process.stdin.close()
        self.assertIsNone(reader.read())
        self.assertEqual(process.wait(timeout=2), 2)
        stderr = process.stderr.read().decode()
        self.assertNotIn(unknown, stderr + self.audit.read_text())
        self.assertNotIn("private-id", stderr + self.audit.read_text())
        self.assertNotIn("Traceback", stderr)
        self.assertIn("mismatch", stderr)
        self.assertIn('"remaining_frame_indices"', self.audit.read_text())

    def test_bounded_partial_line_and_extra_input_refusal(self):
        read_fd, write_fd = os.pipe()
        with os.fdopen(read_fd, "rb") as stream:
            try:
                os.write(write_fd, b'{"method":')
                with self.assertRaisesRegex(peer.ReplayError, "input-timeout"):
                    peer.JsonLineInput(stream, timeout=.02).read()
            finally:
                os.close(write_fd)
        process, reader, recording = self.start("nv04")
        for frame in inputs(recording, 1) + [{"method": "unexpected", "params": {}}]:
            self.send(process, frame)
        process.stdin.close()
        while reader.read() is not None:
            pass
        self.assertEqual(process.wait(timeout=2), 2)
        self.assertIn("extra-input-after-segment", process.stderr.read().decode())

    def test_gate_bounds_version_and_hash_errors(self):
        _, _, recording = capture()
        for generation, pause, release in ((1, 28, "missing"), (1, None, "missing"), (1, 28, None)):
            with self.assertRaises(peer.ReplayError):
                run_memory(recording, generation, pause_after_frame=pause, release=release)
        _, _, nv04 = capture("nv04")
        existing = Path(self.root.name) / "existing"
        existing.touch()
        with self.assertRaisesRegex(peer.ReplayError, "already-exists"):
            run_memory(nv04, pause_after_frame=28, release=existing)
        # Unit-level shortened deadline proves the same fixed-timeout gate failure.
        audit = io.StringIO()
        replay = peer.Replay(nv04, 1, "strict", peer.Audit(audit), pause_after_frame=28,
                             release=Path(self.root.name) / "absent")
        old_timeout = peer.INPUT_TIMEOUT
        try:
            peer.INPUT_TIMEOUT = .02
            with self.assertRaisesRegex(peer.ReplayError, "release-marker-timeout"):
                replay.run(ScriptedInput(inputs(nv04, 1)), io.StringIO())
        finally:
            peer.INPUT_TIMEOUT = old_timeout
        self.assertIn('"event": "error"', audit.getvalue())
        result = subprocess.run([sys.executable, str(HERE / "recorded_replay.py"), "--version"],
                                capture_output=True, timeout=2)
        self.assertEqual((result.returncode, result.stdout, result.stderr), (0, b"codex-cli 0.160.0\n", b""))
        path, _, _ = capture()
        result = subprocess.run([sys.executable, str(HERE / "recorded_replay.py"), "--recording", str(path),
                                 "--sha256", "0" * 64, "--generation", "1", "--audit", str(self.audit)],
                                capture_output=True, timeout=2)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, b"")
        self.assertNotIn(b"Traceback", result.stderr)
        self.assertIn("recording-sha256-mismatch", self.audit.read_text())


if __name__ == "__main__":
    unittest.main()
