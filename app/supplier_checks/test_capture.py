#!/usr/bin/env python3
"""Checks of the capture tool's refusals and of the recordings committed at the declared pin.

No supplier is executed. Run from `app/`: python3 supplier_checks/test_capture.py
"""
import hashlib
import json
import os
import re
import tempfile
import unittest
from pathlib import Path

import capture

HERE = Path(__file__).resolve().parent
# The pin the host declares (src-tauri/src/hosting.rs DECLARED_PIN).
PIN = re.search(r'^pub const DECLARED_PIN: &str = "([0-9.]+)";$',
                (HERE.parent / "src-tauri" / "src" / "hosting.rs").read_text(encoding="utf-8"), re.M).group(1)
RECORDINGS = HERE / "recordings" / PIN
CHILD_PROMPT = capture.CHILD_MARKER + ": count the invented files."


def recording(scenario):
    return json.loads((RECORDINGS / (scenario + ".recording.json")).read_bytes())


def spawn_items(value):
    found = []
    if isinstance(value, dict):
        if value.get("type") == "collabAgentToolCall":
            found.append(value)
        for inner in value.values():
            found += spawn_items(inner)
    elif isinstance(value, list):
        for inner in value:
            found += spawn_items(inner)
    return found


def replies(record):
    """[(generation, request frame, reply frame)] for every answered App-side request."""
    requests, out = {}, []
    for row in record["frames"]:
        frame = row["frame"]
        if row["direction"] == "app->codex" and "method" in frame and "id" in frame:
            requests[row["generation"], frame["id"]] = frame
        elif row["direction"] == "codex->app" and "id" in frame and "method" not in frame:
            out.append((row["generation"], requests[row["generation"], frame["id"]], frame))
    return out


class VendorVerification(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.TemporaryDirectory()
        self.vendor = Path(self.root.name) / "vendor"
        (self.vendor / "bin").mkdir(parents=True)
        (self.vendor / "bin/codex").write_bytes(b"entry")
        os.chmod(self.vendor / "bin/codex", 0o755)
        os.chmod(self.vendor / "bin", 0o755)
        (self.vendor / "codex-package.json").write_bytes(b"{}")
        os.chmod(self.vendor / "codex-package.json", 0o644)
        self.inventory = {"entries": [
            {"path": "bin", "kind": "dir", "mode": 0o755},
            {"path": "bin/codex", "kind": "file", "mode": 0o755, "size": 5,
             "sha256": hashlib.sha256(b"entry").hexdigest()},
            {"path": "codex-package.json", "kind": "file", "mode": 0o644, "size": 2,
             "sha256": hashlib.sha256(b"{}").hexdigest()}]}

    def tearDown(self):
        self.root.cleanup()

    def differences(self):
        return capture.vendor_differences(str(self.vendor), self.inventory)

    def test_equal_tree_has_no_difference(self):
        self.assertEqual(self.differences(), [])

    def test_each_kind_of_difference_is_named(self):
        cases = {
            "content: bin/codex": lambda: (self.vendor / "bin/codex").write_bytes(b"entrY"),
            "mode: bin/codex": lambda: os.chmod(self.vendor / "bin/codex", 0o700),
            "mode: bin": lambda: os.chmod(self.vendor / "bin", 0o700),
            "extra: bin/added": lambda: (self.vendor / "bin/added").write_bytes(b""),
            "missing: codex-package.json": lambda: (self.vendor / "codex-package.json").unlink(),
        }
        for expected, change in cases.items():
            with self.subTest(expected):
                self.tearDown()
                self.setUp()
                change()
                self.assertEqual(self.differences(), [expected])

    def test_a_link_in_place_of_a_member_is_a_type_difference(self):
        (self.vendor / "codex-package.json").unlink()
        os.symlink(self.vendor / "bin/codex", self.vendor / "codex-package.json")
        self.assertEqual(self.differences(), ["type: codex-package.json"])

    def test_refuses_without_executing_when_the_pin_has_no_record_or_the_tree_differs(self):
        with self.assertRaisesRegex(capture.Refused, "no expected distribution"):
            capture.verified_vendor(str(self.vendor), "0.0.1")
        with self.assertRaisesRegex(capture.Refused, "differs from the expected " + re.escape(PIN) + " inventory"):
            capture.verified_vendor(str(self.vendor), PIN)
        resources = Path(self.root.name) / "records"
        (resources / "9.9.9").mkdir(parents=True)
        (resources / "9.9.9/CANONICAL_DISTRIBUTION.json").write_text(json.dumps(
            {"pin": "9.9.8", "package_metadata": {"version": "9.9.9"}, "inventory": self.inventory}))
        with self.assertRaisesRegex(capture.Refused, "does not name pin"):
            capture.verified_vendor(str(self.vendor), "9.9.9", resources)

    def test_main_refuses_a_differing_tree_with_exit_two_and_writes_nothing(self):
        out = Path(self.root.name) / "out"
        self.assertEqual(capture.main(["--vendor", str(self.vendor), "--pin", PIN, "--out", str(out), "nv04"]), 2)
        self.assertFalse(out.exists())


class Redaction(unittest.TestCase):
    def test_paths_host_user_and_identity_fields_are_replaced(self):
        redact, counts = capture.redactor(
            [("/Users/example/x/home", "<HOME>"), ("/Users/example/x", "<SCRATCH>"), ("/Users/example", "<USER-HOME>")],
            "example", "machine.local")
        text = redact(json.dumps({"codexHome": "/Users/example/x/home", "cwd": "/Users/example/x/workspace",
                                  "other": "/Users/example/Documents", "owner": "example",
                                  "userAgent": "client/1 (machine)", "serverName": "machine.local",
                                  "installationId": "abc"}, separators=(",", ":")))
        self.assertEqual(json.loads(text), {
            "codexHome": "<HOME>", "cwd": "<SCRATCH>/workspace", "other": "<USER-HOME>/Documents",
            "owner": "<USER>", "userAgent": "<REDACTED-USER-AGENT>", "serverName": "<REDACTED-HOST>",
            "installationId": "<REDACTED-INSTALLATION-ID>"})
        self.assertEqual(counts["personal path"], 3)
        self.assertEqual(counts["user name"], 1)


class RecordingsAtThePin(unittest.TestCase):
    def test_each_recording_names_the_pin_and_the_verified_distribution(self):
        expected = capture.expected_distribution(PIN)
        main = next(e for e in expected["inventory"]["entries"] if e["path"] == "bin/codex")
        self.assertEqual(sorted(p.name for p in RECORDINGS.iterdir()),
                         sorted(s + ".recording.json" for s in capture.SCENARIOS))
        for scenario in capture.SCENARIOS:
            with self.subTest(scenario):
                record = recording(scenario)
                self.assertEqual((record["format"], record["scenario"], record["pin"]),
                                 (capture.FORMAT, scenario, PIN))
                identity = record["version_identity"]
                self.assertEqual(identity["version_output"], "codex-cli " + PIN)
                self.assertEqual(identity["binary_sha256"], main["sha256"])
                self.assertEqual(identity["distribution"]["archive_sha256"], expected["archive"]["sha256"])
                self.assertEqual(identity["distribution"]["inventory_manifest_sha256"],
                                 expected["inventory"]["manifest_sha256"])
                self.assertEqual(record["events"][0]["pin"], PIN)
                self.assertIsNone(record["app_candidate"])
                self.assertGreater(record["socket_watch"]["samples"], 0)
                self.assertEqual(record["socket_watch"]["non_loopback_peers"], [])
                self.assertLessEqual(set(record["socket_watch"]["loopback_peers"]), {"127.0.0.1", "::1"})

    def test_frames_are_ordered_and_every_reply_answers_a_recorded_request(self):
        for scenario in capture.SCENARIOS:
            with self.subTest(scenario):
                record = recording(scenario)
                positions, last = {}, -1
                for row in record["frames"]:
                    self.assertEqual(set(row), {"generation", "direction", "position", "t_ms", "redacted", "frame"})
                    key = row["generation"], row["direction"]
                    self.assertEqual(row["position"], positions.get(key, 0) + 1)
                    positions[key] = row["position"]
                    self.assertGreaterEqual(row["t_ms"], last)
                    last = row["t_ms"]
                    self.assertIsInstance(row["frame"], dict)
                self.assertEqual({key[0] for key in positions}, {1, 2})
                replies(record)  # raises KeyError on a reply without its request

    def test_no_local_path_or_address_remains(self):
        pattern = re.compile(r"/Users/|/private/|/var/folders|/home/|[A-Za-z0-9._-]+@[A-Za-z0-9-]+\.[a-z]{2,}")
        for scenario in capture.SCENARIOS:
            with self.subTest(scenario):
                text = (RECORDINGS / (scenario + ".recording.json")).read_text()
                self.assertIsNone(pattern.search(text))

    def test_st5_answer_was_written_and_never_acknowledged_and_nothing_was_re_raised(self):
        for scenario in ("st5", "st5-race"):
            with self.subTest(scenario):
                events = {event["event"]: event for event in recording(scenario)["events"]}
                self.assertEqual(events["answer-written"]["decision"], "accept")
                if scenario == "st5":
                    # Frozen before the write: no acknowledgment can exist. The race is an observation.
                    self.assertFalse(events["acknowledgment-reading"]["serverRequest_resolved_observed"])
                self.assertEqual(events["re-raised-request-reading"]["server_requests_after_resume"], 0)
                self.assertFalse(events["workspace-reading-end"]["marker_folder_exists"])

    def test_nv04_spawn_item_carries_its_prompt_live_and_on_every_history_read_of_the_parent(self):
        record = recording("nv04")
        live = {row["frame"]["method"]: row["frame"]["params"]["item"] for row in record["frames"]
                if row["frame"].get("method") in ("item/started", "item/completed")
                and row["frame"]["params"]["item"].get("type") == "collabAgentToolCall"}
        self.assertEqual(sorted(live), ["item/completed", "item/started"])
        started, completed = live["item/started"], live["item/completed"]
        self.assertEqual((started["prompt"], completed["prompt"]), (CHILD_PROMPT, CHILD_PROMPT))
        self.assertEqual(started["receiverThreadIds"], [])
        self.assertEqual(len(completed["receiverThreadIds"]), 1)
        parent, child = completed["senderThreadId"], completed["receiverThreadIds"][0]
        self.assertEqual(started["senderThreadId"], parent)
        seen = {}
        for generation, request, reply in replies(record):
            thread = request.get("params", {}).get("threadId")
            if request["method"] not in ("thread/read", "thread/turns/list", "thread/items/list"):
                continue
            self.assertIn("result", reply, (generation, request["method"]))
            if thread == parent:
                items = spawn_items(reply["result"])
                self.assertEqual([(i["prompt"], i["senderThreadId"], i["receiverThreadIds"]) for i in items],
                                 [(CHILD_PROMPT, parent, [child])], (generation, request["method"]))
                seen[generation, request["method"]] = True
            else:
                self.assertEqual(thread, child)
                described = reply["result"]["thread"]
                self.assertEqual(described["parentThreadId"], parent)
                self.assertTrue(described["agentNickname"])
                # The scripted spawn call names no role, so none is reported.
                self.assertIsNone(described["agentRole"])
                seen[generation, "child"] = True
        self.assertEqual(sorted(seen), sorted(
            (generation, name) for generation in (1, 2)
            for name in ("thread/read", "thread/turns/list", "thread/items/list", "child")))


if __name__ == "__main__":
    unittest.main()
