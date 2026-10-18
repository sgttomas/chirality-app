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
        if profile in ("app-recovery", "app-continue") and frame.get("method") == "thread/read":
            frame["params"]["includeTurns"] = False
        if profile in ("app-recovery", "app-continue") and frame.get("method") == "thread/turns/list":
            frame["params"].update(itemsView="summary", sortDirection="desc")
        if profile == "app-continue" and frame.get("method") == "thread/resume":
            frames.append({"jsonrpc": "2.0", "id": "constructed-catalog", "method": "thread/list",
                           "params": {"sortDirection": "desc"}})
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
    def test_decode_refuses_overflow_and_unpaired_surrogates_without_changing_valid_values(self):
        for data, code in ((b'{"value":1e999}', "nonfinite-json"),
                           (b'{"value":-1e999}', "nonfinite-json"),
                           (b'{"value":"\\ud800"}', "invalid-json-unicode"),
                           (b'{"\\udc00":0}', "invalid-json-unicode")):
            with self.subTest(data=data):
                with self.assertRaisesRegex(peer.ReplayError, code):
                    peer.decode(data)
        valid = b'{"float":1.5,"integer":1,"text":"\\ud83d\\ude00","nested":[null,true]}'
        self.assertEqual(peer.decode(valid), json.loads(valid))
        self.assertIs(type(peer.decode(valid)["float"]), float)
        with self.assertRaisesRegex(peer.ReplayError, "invalid-json-unicode"):
            peer.rpc_id("\ud800")

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

    def start(self, scenario="st5", generation=1, extra=(), env=None):
        path, digest, recording = capture(scenario)
        command = [sys.executable, str(HERE / "recorded_replay.py"), "--recording", str(path),
                   "--sha256", digest, "--generation", str(generation), "--audit", str(self.audit), *extra]
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
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

    def test_continue_keeps_full_tape_and_separately_labels_exact_constructed_catalog(self):
        path, digest, recording = capture()
        supplied = inputs(recording, 2, "app-continue", remap=True)
        catalog = next(frame for frame in supplied if frame.get("method") == "thread/list")
        # This equals a recorded source ID, but not an actual request ID.
        # Its separate correlation must not steal recorded resume ID 5.
        catalog["id"] = 5
        result = self.invoke(path, digest, self.audit, "app-continue", 2, supplied)
        self.assertEqual((result.returncode, result.stderr), (0, b""))
        output = [json.loads(line) for line in result.stdout.splitlines()]
        expected, mapped_ids = [], {1: "1", 2: 1, 3: "actual-turn", 4: 104, 5: 105}
        for index in range(19, 35):
            row = recording["frames"][index]
            if row["direction"] == "codex->app":
                frame = copy.deepcopy(row["frame"])
                if "id" in frame and "method" not in frame:
                    frame["id"] = mapped_ids[frame["id"]]
                expected.append(frame)
            if index == 29:
                expected.append({"id": 5, "result": {"data": [copy.deepcopy(recording["frames"][25]["frame"]["result"]["thread"])],
                                                       "nextCursor": None}})
        self.assertEqual(output, expected)
        self.assertEqual(output[5]["result"], {"data": [], "nextCursor": None})
        self.assertEqual(output[6]["result"]["data"][0], recording["frames"][25]["frame"]["result"]["thread"])
        rows = [json.loads(line) for line in self.audit.read_text().splitlines()]
        binding = next(row for row in rows if row["event"] == "binding")
        self.assertEqual(binding["selected_frame_indices"], list(range(19, 35)))
        self.assertEqual(binding["outside_segment_frame_indices"], [])
        constructed = [row for row in rows if row["event"] == "constructed-frame"]
        self.assertEqual([row["direction"] for row in constructed], ["app->codex", "codex->app"])
        for row in constructed:
            self.assertNotIn("frame_index", row)
            self.assertNotIn("recorded_rpc_id", row)
            self.assertEqual(row["source_frame_index"], 25)
            self.assertEqual(row["recipe"], "thread-list-envelope-from-thread-read")
            self.assertEqual(row["actual_rpc_id"], 5)
            self.assertEqual(row["actual_rpc_id_type"], "int")
            self.assertIn("envelope/membership not captured", row["constructed_standing"])
        self.assertEqual([row["frame_index"] for row in rows if row["event"] == "frame"], list(range(19, 35)))
        finish = next(row for row in rows if row["event"] == "finish")
        self.assertEqual(finish["consumed_frame_indices"], list(range(19, 35)))
        self.assertEqual(finish["remaining_frame_indices"], [])
        self.assertEqual(finish["outside_segment_frame_indices"], [])

    def test_continue_catalog_and_resume_refuse_missing_wrong_duplicate_or_reused_inputs(self):
        path, digest, recording = capture()
        original = inputs(recording, 2, "app-continue")
        cases = [
            ("missing", lambda frames: frames.__delitem__(slice(5, None))),
            ("resume-before-catalog", lambda frames: frames.pop(5)),
            ("wrong-method", lambda frames: frames[5].update(method="thread/loaded/list")),
            ("wrong-params", lambda frames: frames[5]["params"].update(sortDirection="asc")),
            ("missing-params", lambda frames: frames[5].pop("params")),
            ("extra-params", lambda frames: frames[5]["params"].update(cursor="PRIVATE_CATALOG_CANARY")),
            ("reused-id", lambda frames: frames[5].update(id=1)),
            ("invalid-id", lambda frames: frames[5].update(id=None)),
            ("notification", lambda frames: frames[5].pop("id")),
            ("duplicate-catalog", lambda frames: frames.insert(6, {**copy.deepcopy(frames[5]), "id": "second-catalog"})),
            ("resume-reuses-catalog-id", lambda frames: frames[6].update(id=frames[5]["id"])),
            ("wrong-resume-thread", lambda frames: frames[6]["params"].update(threadId="PRIVATE_CATALOG_CANARY")),
            ("extra-resume-param", lambda frames: frames[6]["params"].update(excludeTurns=True)),
        ]
        for name, mutate in cases:
            with self.subTest(case=name):
                supplied = copy.deepcopy(original)
                mutate(supplied)
                audit = Path(self.root.name) / (name + ".jsonl")
                result = self.invoke(path, digest, audit, "app-continue", 2, supplied)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn(b"Traceback", result.stderr)
                self.assertNotIn(b"PRIVATE_CATALOG_CANARY", result.stderr + audit.read_bytes())
                rows = [json.loads(line) for line in audit.read_text().splitlines()]
                self.assertEqual(rows[-2]["event"], "error")
                self.assertEqual(rows[-2]["frame_index"], 30)
                self.assertEqual(rows[-2]["consumed_frame_indices"], list(range(19, 30)))
                self.assertEqual(rows[-2]["remaining_frame_indices"], list(range(30, 35)))
                self.assertEqual(rows[-1]["outcome"], "error")
                self.assertFalse(any(row.get("frame_index") == 30 and row["event"] == "frame" for row in rows))
                self.assertFalse(any(row["event"] == "finish" for row in rows))

    def test_continue_profile_and_pause_gate_refuse_unsupported_or_existing_inputs(self):
        for index, (scenario, generation) in enumerate((("st5", 1), ("st5-race", 2), ("nv04", 1))):
            with self.subTest(scenario=scenario, generation=generation):
                path, digest, _ = capture(scenario)
                audit = Path(self.root.name) / f"unsupported-{index}.jsonl"
                result = self.invoke(path, digest, audit, "app-continue", generation)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, b"")
                self.assertEqual(result.stderr, b"recorded-replay: unsupported-continue-profile\n")
        path, digest, _ = capture()
        release = Path(self.root.name) / "existing-release"
        release.touch()
        cases = [
            (("--pause-after-frame", "32", "--release", str(release)), "release-marker-already-exists"),
            (("--pause-after-frame", "28", "--release", str(release)), "unsupported-pause-gate"),
            (("--pause-after-frame", "32"), "incomplete-pause-gate"),
            (("--release", str(release)), "incomplete-pause-gate"),
        ]
        for index, (extra, code) in enumerate(cases):
            with self.subTest(gate=index):
                audit = Path(self.root.name) / f"gate-{index}.jsonl"
                result = self.invoke(path, digest, audit, "app-continue", 2, extra=extra)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, b"")
                self.assertEqual(result.stderr, ("recorded-replay: " + code + "\n").encode())
                self.assertEqual(json.loads(audit.read_text().splitlines()[-1])["outcome"], "error")

    def test_continue_refuses_malformed_source_or_pause_metadata_with_terminal_audit(self):
        _, _, original = capture()
        cases = [
            lambda d: d["frames"][25]["frame"].update(result=None),
            lambda d: d["frames"][25]["frame"]["result"].pop("thread"),
            lambda d: d["frames"][25]["frame"]["result"].update(thread=[]),
            lambda d: d["frames"][25]["frame"]["result"]["thread"].pop("id"),
            lambda d: d["frames"][25]["frame"]["result"]["thread"].update(id=None),
            lambda d: d["frames"][29]["frame"].update(result=None),
            lambda d: d["frames"][30]["frame"]["params"].update(threadId="other-thread"),
            lambda d: d["frames"][32]["frame"].update(method="warning"),
            lambda d: d["frames"][32]["frame"]["params"].update(status=None),
        ]
        for index, mutate in enumerate(cases):
            with self.subTest(case=index):
                recording = copy.deepcopy(original)
                mutate(recording)
                data = json.dumps(recording).encode()
                path = Path(self.root.name) / f"continue-malformed-{index}.json"
                path.write_bytes(data)
                audit = Path(self.root.name) / f"continue-malformed-{index}.jsonl"
                result = self.invoke(path, hashlib.sha256(data).hexdigest(), audit, "app-continue", 2,
                                     extra=("--pause-after-frame", "32", "--release", str(Path(self.root.name) / "release")))
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, b"")
                self.assertNotIn(b"Traceback", result.stderr)
                rows = [json.loads(line) for line in audit.read_text().splitlines()]
                self.assertEqual(rows[-1]["outcome"], "error")
                self.assertIn(rows[-1]["code"], ("invalid-captured-catalog-source", "unsupported-continue-tape", "unsupported-pause-frame"))
                self.assertEqual(path.read_bytes(), data)

    def test_constructed_catalog_closed_stdout_retains_clean_failure_and_recorded_indices(self):
        env = {key: value for key, value in os.environ.items() if key != "PYTHONUNBUFFERED"}
        process, reader, recording = self.start(generation=2, extra=("--profile", "app-continue"), env=env)
        supplied = iter(inputs(recording, 2, "app-continue"))
        for index in range(19, 30):
            row = recording["frames"][index]
            if row["direction"] == "app->codex":
                self.send(process, next(supplied))
            else:
                self.assertEqual(reader.read(), row["frame"])
        self.assertEqual(reader.buffer, b"")
        process.stdout.close()
        self.send(process, next(supplied))
        process.stdin.close()
        self.assertEqual(process.wait(timeout=2), 2)
        self.assertEqual(process.stderr.read(), b"recorded-replay: peer-io-or-value-error\n")
        rows = [json.loads(line) for line in self.audit.read_text().splitlines()]
        self.assertEqual([row["direction"] for row in rows if row["event"] == "constructed-frame"], ["app->codex"])
        self.assertEqual(rows[-2]["frame_index"], 30)
        self.assertEqual(rows[-2]["consumed_frame_indices"], list(range(19, 30)))
        self.assertEqual(rows[-2]["remaining_frame_indices"], list(range(30, 35)))
        self.assertEqual(rows[-1]["outcome"], "error")

    def test_continue_pause_holds_idle_before_unchanged_resume_reply(self):
        release = Path(self.root.name) / "continue-release"
        process, reader, recording = self.start(generation=2, extra=("--profile", "app-continue", "--pause-after-frame", "32", "--release", str(release)))
        supplied = iter(inputs(recording, 2, "app-continue"))
        for index in range(19, 33):
            row = recording["frames"][index]
            if index == 30:
                catalog = next(supplied)
                self.send(process, catalog)
                self.assertEqual(reader.read(), {"id": catalog["id"], "result": {
                    "data": [recording["frames"][25]["frame"]["result"]["thread"]], "nextCursor": None}})
            if row["direction"] == "app->codex":
                self.send(process, next(supplied))
            else:
                self.assertEqual(reader.read(), row["frame"])
        deadline = time.monotonic() + 2
        while '"event": "paused"' not in self.audit.read_text() and time.monotonic() < deadline:
            time.sleep(.01)
        rows = [json.loads(line) for line in self.audit.read_text().splitlines()]
        paused = next(row for row in rows if row["event"] == "paused")
        self.assertEqual(paused["frame_index"], 32)
        self.assertEqual(paused["reason"], "st5-continue-idle-before-resume-reply")
        self.assertEqual(reader.buffer, b"")
        self.assertFalse(select.select([process.stdout], [], [], .05)[0])
        self.assertIsNone(process.poll())
        release.touch()
        self.assertEqual(reader.read(), recording["frames"][33]["frame"])
        self.assertEqual(reader.read(), recording["frames"][34]["frame"])
        self.assertIsNone(process.poll())
        process.stdin.close()
        self.assertIsNone(reader.read())
        self.assertEqual(process.wait(timeout=2), 0)

    def test_continue_pause_timeout_leaves_resume_reply_unconsumed(self):
        release = Path(self.root.name) / "absent-release"
        process, reader, recording = self.start(generation=2, extra=("--profile", "app-continue", "--pause-after-frame", "32", "--release", str(release)))
        for frame in inputs(recording, 2, "app-continue"):
            self.send(process, frame)
        process.stdin.close()
        # Nine frames reach the consumer: eight original supplier frames
        # through idle plus the separately constructed catalog result.
        for unused in range(9):
            self.assertIsInstance(reader.read(), dict)
        self.assertEqual(process.wait(timeout=12), 2)
        self.assertEqual(process.stderr.read(), b"recorded-replay: release-marker-timeout\n")
        self.assertIsNone(reader.read())
        rows = [json.loads(line) for line in self.audit.read_text().splitlines()]
        self.assertEqual(rows[-2]["event"], "error")
        self.assertEqual(rows[-2]["frame_index"], 32)
        self.assertEqual(rows[-2]["consumed_frame_indices"], list(range(19, 33)))
        self.assertEqual(rows[-2]["remaining_frame_indices"], [33, 34])
        self.assertEqual(rows[-1]["outcome"], "error")

    def test_malformed_actual_numbers_unicode_and_rpc_ids_have_complete_failure_audits(self):
        path, digest, recording = capture()
        first = json.dumps(inputs(recording, 1)[0]).encode()
        cases = [
            (first.replace(b'"experimentalApi": true', b'"experimentalApi": 1e999'), "nonfinite-json"),
            (first.replace(b'"experimentalApi": true', b'"experimentalApi": -1e999'), "nonfinite-json"),
            (first.replace(b'"id": 1', b'"id": "\\ud800"'), "invalid-json-unicode"),
            (first.replace(b'"id": 1', b'"id": "\\udfff"'), "invalid-json-unicode"),
            (first.replace(b'"clientInfo": {', b'"clientInfo": {"\\ud800": "private-canary",'), "invalid-json-unicode"),
        ]
        for index, (supplied, code) in enumerate(cases):
            with self.subTest(case=index):
                audit = Path(self.root.name) / f"actual-malformed-{index}.jsonl"
                result = subprocess.run([sys.executable, str(HERE / "recorded_replay.py"),
                                         "--recording", str(path), "--sha256", digest,
                                         "--generation", "1", "--audit", str(audit)],
                                        input=supplied + b"\n", capture_output=True, timeout=2)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, b"")
                self.assertEqual(result.stderr, ("recorded-replay: " + code + "\n").encode())
                rows = [json.loads(line) for line in audit.read_text().splitlines()]
                self.assertEqual(rows[-2]["event"], "error")
                self.assertEqual(rows[-2]["frame_index"], 0)
                self.assertEqual(rows[-2]["consumed_frame_indices"], [])
                self.assertEqual(rows[-2]["remaining_frame_indices"], list(range(19)))
                self.assertEqual(rows[-1], {"event": "exit", "outcome": "error", "code": code})
                self.assertNotIn("private-canary", audit.read_text())

    def test_sha_bound_malformed_values_are_refused_without_changing_source(self):
        _, _, recording = capture()
        original = json.dumps(recording).encode()
        for index, (replacement, code) in enumerate(((b'1e999', "nonfinite-json"),
                                                     (b'"\\ud800"', "invalid-json-unicode"))):
            with self.subTest(case=index):
                data = original.replace(b'"userAgent": "<REDACTED-USER-AGENT>"', b'"userAgent": ' + replacement)
                self.assertNotEqual(data, original)
                path = Path(self.root.name) / f"malformed-value-{index}.json"
                path.write_bytes(data)
                audit = Path(self.root.name) / f"malformed-value-{index}.jsonl"
                result = self.invoke(path, hashlib.sha256(data).hexdigest(), audit,
                                     supplied=inputs(recording, 1, "app"))
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, b"")
                self.assertEqual(result.stderr, ("recorded-replay: " + code + "\n").encode())
                rows = [json.loads(line) for line in audit.read_text().splitlines()]
                self.assertEqual(rows[-1], {"event": "exit", "outcome": "error", "code": code})
                self.assertEqual(path.read_bytes(), data)

    def test_valid_unicode_rpc_id_is_preserved_in_protocol_and_audit(self):
        path, digest, recording = capture()
        supplied = inputs(recording, 1)
        actual_id = json.loads('"caller-\\ud83d\\ude00-\\ud800\\udc00"')
        supplied[0]["id"] = actual_id
        result = self.invoke(path, digest, self.audit, profile="strict", supplied=supplied)
        self.assertEqual((result.returncode, result.stderr), (0, b""))
        output = [json.loads(line) for line in result.stdout.splitlines()]
        expected = [copy.deepcopy(row["frame"]) for row in recording["frames"]
                    if row["generation"] == 1 and row["direction"] == "codex->app"]
        expected[0]["id"] = actual_id
        self.assertEqual(output, expected)
        rows = [json.loads(line) for line in self.audit.read_text().splitlines()]
        self.assertTrue(any(row.get("actual_rpc_id") == actual_id for row in rows))
        self.assertEqual(rows[-1], {"event": "exit", "outcome": "success"})

    def test_recoverable_reader_failures_are_audited_before_closing_the_stream(self):
        path, digest, _ = capture()
        failures = [ValueError("private-reader-canary"), OSError("private-reader-canary"),
                    RecursionError("private-reader-canary"),
                    UnicodeEncodeError("utf-8", "\ud800", 0, 1, "private-reader-canary")]
        for index, error in enumerate(failures):
            with self.subTest(case=index):
                audit = Path(self.root.name) / f"reader-failure-{index}.jsonl"
                errors = io.StringIO()
                with patch.object(peer.JsonLineInput, "read", side_effect=error), redirect_stderr(errors):
                    code = peer.main(["--recording", str(path), "--sha256", digest,
                                      "--generation", "1", "--audit", str(audit)])
                self.assertEqual(code, 2)
                self.assertEqual(errors.getvalue(), "recorded-replay: peer-io-or-value-error\n")
                rows = [json.loads(line) for line in audit.read_text().splitlines()]
                self.assertEqual(rows[-2]["event"], "error")
                self.assertEqual(rows[-2]["frame_index"], 0)
                self.assertEqual(rows[-2]["remaining_frame_indices"], list(range(19)))
                self.assertEqual(rows[-1], {"event": "exit", "outcome": "error", "code": "peer-io-or-value-error"})
                self.assertNotIn("private-reader-canary", audit.read_text())

    def test_output_and_input_setup_errors_keep_terminal_failure_audits(self):
        path, digest, recording = capture()
        for stage in ("output", "input-setup"):
            with self.subTest(stage=stage):
                audit = Path(self.root.name) / f"{stage}-failure.jsonl"
                errors = io.StringIO()
                if stage == "output":
                    failure = UnicodeEncodeError("utf-8", "\ud800", 0, 1, "private-output-canary")
                    failing_writer = io.StringIO()
                    patcher = patch.object(failing_writer, "write", side_effect=failure)
                    input_patch = patch.object(peer.JsonLineInput, "read", return_value=inputs(recording, 1)[0])
                else:
                    failing_writer = io.StringIO()
                    patcher = patch.object(peer.JsonLineInput, "__init__", side_effect=ValueError("private-setup-canary"))
                    input_patch = patch.object(peer.JsonLineInput, "read")
                with patcher, input_patch, patch.object(sys, "stdout", failing_writer), redirect_stderr(errors):
                    code = peer.main(["--recording", str(path), "--sha256", digest,
                                      "--generation", "1", "--audit", str(audit)])
                self.assertEqual(code, 2)
                self.assertEqual(errors.getvalue(), "recorded-replay: peer-io-or-value-error\n")
                rows = [json.loads(line) for line in audit.read_text().splitlines()]
                self.assertEqual(rows[-2]["event"], "error")
                self.assertEqual(rows[-2]["consumed_frame_indices"], [0] if stage == "output" else [])
                self.assertEqual(rows[-2]["remaining_frame_indices"], list(range(1 if stage == "output" else 0, 19)))
                self.assertEqual(rows[-1], {"event": "exit", "outcome": "error", "code": "peer-io-or-value-error"})
                self.assertNotIn("private-output-canary", audit.read_text())
                self.assertNotIn("private-setup-canary", audit.read_text())

    def test_closed_stdout_pipe_exits_cleanly_with_complete_failure_audit(self):
        # Keep ordinary buffered stdout: its shutdown flush is part of this
        # regression, so an inherited unbuffered-mode setting must not mask it.
        env = {key: value for key, value in os.environ.items() if key != "PYTHONUNBUFFERED"}
        process, _, recording = self.start(env=env)
        process.stdout.close()
        self.send(process, inputs(recording, 1)[0])
        process.stdin.close()
        status = process.wait(timeout=2)
        errors = process.stderr.read()
        self.assertEqual(status, 2, errors.decode())
        self.assertEqual(errors, b"recorded-replay: peer-io-or-value-error\n")
        rows = [json.loads(line) for line in self.audit.read_text().splitlines()]
        self.assertEqual(rows[-2]["event"], "error")
        self.assertEqual(rows[-2]["frame_index"], 1)
        self.assertEqual(rows[-2]["consumed_frame_indices"], [0])
        self.assertEqual(rows[-2]["remaining_frame_indices"], list(range(1, 19)))
        self.assertEqual(rows[-1], {"event": "exit", "outcome": "error", "code": "peer-io-or-value-error"})
        self.assertFalse(any(row["event"] == "finish" for row in rows))

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
