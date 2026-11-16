"""Read the retained 0.169.0 captures; no supplier, provider or model execution."""
import hashlib
import json
from pathlib import Path
import unittest

from jsonschema import Draft7Validator

import test_recordings as historical

HERE = Path(__file__).resolve().parent
RESOURCES = HERE.parent / "src-tauri/resources/supplier/0.169.0"
RECORDINGS = HERE / "recordings/0.169.0"
DIGESTS = {"st5": "7bde5cf31b57a15262c0d0b9d0c4eca39640897a4ce8f0ab59babb6ef4af00a0",
           "nv04": "6fe2739de177a559314db2d9dfcafd35234f56456d0045c50f4abd2c03d2c1a8"}
RESPONSES = {"initialize": "InitializeResponse", "thread/start": "v2/ThreadStartResponse",
             "turn/start": "v2/TurnStartResponse", "thread/read": "v2/ThreadReadResponse",
             "thread/turns/list": "v2/ThreadTurnsListResponse", "thread/items/list": "v2/ThreadItemsListResponse",
             "thread/loaded/list": "v2/ThreadLoadedListResponse", "thread/resume": "v2/ThreadResumeResponse",
             "item/commandExecution/requestApproval": "CommandExecutionRequestApprovalResponse"}


def record(case):
    return json.loads((RECORDINGS / (case + ".recording.json")).read_bytes())


def validate_frames(capture, resources=RESOURCES):
    schema = json.loads((resources / "codex_app_server_protocol.schemas.json").read_bytes())
    def validate(name, value):
        try:
            Draft7Validator({"$ref": "#/definitions/" + name, "definitions": schema["definitions"]}).validate(value)
        except Exception as error:
            # A missing schema reference otherwise prints the entire supplier bundle.
            raise AssertionError("recorded value failed " + name + ": " + type(error).__name__) from None
    pending, answered, positions = {}, set(), {}
    for row in capture["frames"]:
        generation, direction, frame = row["generation"], row["direction"], row["frame"]
        assert generation in (1, 2) and direction in ("app->codex", "codex->app")
        position_key = generation, direction
        positions[position_key] = positions.get(position_key, 0) + 1
        assert row["position"] == positions[position_key]
        if "method" in frame:
            kind = ("Client" if direction == "app->codex" else "Server") + ("Request" if "id" in frame else "Notification")
            validate(kind, frame)
            if "id" in frame:
                key = generation, direction, json.dumps(frame["id"])
                assert key not in pending, "request identity repeated within its generation and direction"
                pending[key] = frame["method"]
        else:
            assert "id" in frame and "result" in frame and "error" not in frame
            opposite = "codex->app" if direction == "app->codex" else "app->codex"
            key = generation, opposite, json.dumps(frame["id"])
            assert key in pending and key not in answered, "unmatched or repeated reply"
            validate(RESPONSES[pending[key]], frame["result"])
            answered.add(key)
    return [pending[key] for key in pending.keys() - answered]


class Recordings0169(unittest.TestCase):
    def test_recorded_identity_and_all_frames_against_the_actual_pin_schema(self):
        generation = json.loads((RESOURCES / "GENERATION.json").read_bytes())
        for case, digest in DIGESTS.items():
            with self.subTest(case=case):
                raw = (RECORDINGS / (case + ".recording.json")).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), digest)
                capture = record(case)
                self.assertEqual(capture["pin"], "0.169.0")
                self.assertEqual(capture["version_identity"]["binary_sha256"], generation["supplier"]["main_sha256"])
                self.assertEqual(capture["version_identity"]["distribution"]["archive_sha256"], generation["supplier"]["archive_sha256"])
                self.assertEqual(validate_frames(capture), ["thread/turns/list"] if case == "st5" else [])
                self.assertFalse(capture["socket_watch"]["observed"])
                self.assertFalse(capture["settings_supplied"]["allow_login_shell"])
                self.assertFalse(capture["settings_supplied"]["features.shell_snapshot"])
                self.assertFalse(any(path in raw.decode() for path in ("/Users/", "/private/", "/var/folders/")))

    def test_st5_request_and_interrupted_history_are_observations_not_a_successful_command(self):
        capture = record("st5")
        frames = capture["frames"]
        approval = [row["frame"] for row in frames if row["frame"].get("method") == "item/commandExecution/requestApproval"]
        self.assertEqual(len(approval), 1)
        self.assertFalse(any(row["frame"].get("method") in ("serverRequest/resolved", "turn/completed") for row in frames if row["generation"] == 1))
        self.assertFalse(any("id" in row["frame"] and "method" in row["frame"] for row in frames
                             if row["generation"] == 2 and row["direction"] == "codex->app"))
        histories = [(request["method"], reply["result"]) for generation, request, reply in historical.replies(capture)
                     if generation == 2 and request["method"] in ("thread/read", "thread/resume")]
        self.assertEqual({method for method, _result in histories}, {"thread/read", "thread/resume"})
        for _method, result in histories:
            self.assertEqual(result["thread"]["turns"][0]["status"], "interrupted")

    def test_nv04_parent_and_child_have_separate_completion_and_history(self):
        capture = record("nv04")
        frames = [row["frame"] for row in capture["frames"] if row["generation"] == 1]
        spawn = next(f["params"]["item"] for f in frames if f.get("method") == "item/completed"
                     and f["params"]["item"]["type"] == "collabAgentToolCall")
        parent, child = spawn["senderThreadId"], spawn["receiverThreadIds"][0]
        self.assertNotEqual(parent, child)
        completions = [f["params"]["threadId"] for f in frames if f.get("method") == "turn/completed"]
        self.assertLess(completions.index(parent), completions.index(child))
        reads = historical.replies(capture)
        for generation in (1, 2):
            parent_methods = {request["method"] for gen, request, reply in reads if gen == generation
                              and request["params"].get("threadId") == parent and historical.spawn_items(reply)}
            self.assertTrue({"thread/read", "thread/turns/list", "thread/items/list"} <= parent_methods)
            self.assertTrue(any(gen == generation and request["method"] == "thread/read"
                                and request["params"].get("threadId") == child for gen, request, _reply in reads))


if __name__ == "__main__":
    unittest.main()
