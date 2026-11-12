#!/usr/bin/env python3
"""Checks of the capture tool's refusals and of the recordings committed at the declared pin.

No supplier is executed. Run from `app/`: python3 supplier_checks/test_capture.py
"""
import hashlib
import json
import os
import re
import subprocess
import tempfile
import threading
import types
import unittest
from pathlib import Path

import capture

HERE = Path(__file__).resolve().parent
PIN = "0.167.0"
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
        with self.assertRaisesRegex(capture.Refused, "differs from the expected 0.167.0 inventory"):
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


class MetadataPaths(unittest.TestCase):
    """Nothing the package metadata says may name a path outside the verified tree."""

    def setUp(self):
        self.root = tempfile.TemporaryDirectory()
        self.vendor = Path(os.path.realpath(self.root.name)) / "vendor"
        (self.vendor / "bin").mkdir(parents=True)
        (self.vendor / "codex-path").mkdir()
        (self.vendor / "bin/codex").write_bytes(b"entry")
        os.chmod(self.vendor / "bin/codex", 0o755)
        (self.vendor.parent / "not-in-inventory").write_bytes(b"outside")
        os.chmod(self.vendor.parent / "not-in-inventory", 0o755)
        self.record = {"package_metadata": {"entrypoint": "bin/codex", "pathDir": "codex-path"}, "inventory": {
            "entries": [{"path": "bin", "kind": "dir", "mode": 0o755},
                        {"path": "bin/codex", "kind": "file", "mode": 0o755, "size": 5,
                         "sha256": hashlib.sha256(b"entry").hexdigest()},
                        {"path": "codex-path", "kind": "dir", "mode": 0o755}]}}

    def tearDown(self):
        self.root.cleanup()

    def test_only_inventory_members_of_the_right_kind_are_admitted(self):
        self.assertEqual(capture.metadata_members(self.record), {"entrypoint": "bin/codex", "pathDir": "codex-path"})
        for field, value in (("entrypoint", "../not-in-inventory"), ("entrypoint", "/bin/sh"), ("entrypoint", "bin"),
                             ("entrypoint", "bin/absent"), ("entrypoint", "bin/../bin/codex"), ("entrypoint", ""),
                             ("entrypoint", None), ("entrypoint", 7), ("pathDir", "bin/codex"), ("pathDir", "."),
                             ("pathDir", ".."), ("execServer", "../not-in-inventory"), ("resourcesDir", "bin/codex")):
            with self.subTest(field=field, value=value):
                record = json.loads(json.dumps(self.record))
                record["package_metadata"][field] = value
                with self.assertRaisesRegex(capture.Refused, "of the verified inventory"):
                    capture.metadata_members(record)
                with self.assertRaises(capture.Refused):
                    capture.admitted_path(str(self.vendor), record, "entrypoint")

    def test_an_entrypoint_that_is_not_executable_in_the_inventory_refuses(self):
        self.record["inventory"]["entries"][1]["mode"] = 0o644
        with self.assertRaisesRegex(capture.Refused, "not executable"):
            capture.metadata_members(self.record)

    def test_the_path_is_admitted_again_at_the_moment_of_use(self):
        binary = capture.admitted_path(str(self.vendor), self.record, "entrypoint")
        self.assertEqual(binary, str(self.vendor / "bin/codex"))
        (self.vendor / "bin/codex").write_bytes(b"other")
        with self.assertRaisesRegex(capture.Refused, "no longer equals"):
            capture.admitted_path(str(self.vendor), self.record, "entrypoint")

    def test_a_link_in_place_of_the_entrypoint_or_of_its_directory_refuses(self):
        (self.vendor / "bin/codex").unlink()
        os.symlink(self.vendor.parent / "not-in-inventory", self.vendor / "bin/codex")
        with self.assertRaisesRegex(capture.Refused, "passes through a link"):
            capture.admitted_path(str(self.vendor), self.record, "entrypoint")
        (self.vendor / "bin/codex").unlink()
        (self.vendor / "bin").rmdir()
        os.symlink(self.vendor.parent, self.vendor / "bin")
        with self.assertRaisesRegex(capture.Refused, "passes through a link"):
            capture.admitted_path(str(self.vendor), self.record, "entrypoint")

    def test_the_harness_refuses_metadata_that_escapes_before_anything_can_run(self):
        self.record["package_metadata"]["entrypoint"] = "../not-in-inventory"
        with self.assertRaises(capture.Refused):
            capture.Harness(str(self.vendor), self.record, str(self.vendor.parent / "out"), 1.0)
        self.assertFalse((self.vendor.parent / "out").exists())


class SocketWatch(unittest.TestCase):
    @staticmethod
    def lsof(returncode, stdout="", stderr=""):
        return lambda *args, **kwargs: types.SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)

    def test_a_sample_is_taken_only_when_lsof_reports_cleanly(self):
        header = "COMMAND PID PGID USER FD TYPE DEVICE SIZE/OFF NODE NAME\n"
        row = "codex 1 1 u 9u IPv4 0x0 0t0 TCP 127.0.0.1:50000->%s:443 (ESTABLISHED)\n"
        self.assertEqual(capture.socket_peers(1, self.lsof(1)), [])
        self.assertEqual(capture.socket_peers(1, self.lsof(0, header)), [])
        self.assertEqual(capture.socket_peers(1, self.lsof(0, header + row % "127.0.0.1")), ["127.0.0.1"])
        self.assertEqual(capture.socket_peers(1, self.lsof(0, header + row % "203.0.113.7")), ["203.0.113.7"])
        self.assertIsNone(capture.socket_peers(1, self.lsof(2)))
        self.assertIsNone(capture.socket_peers(1, self.lsof(1, stderr="lsof: no pwd entry")))
        self.assertIsNone(capture.socket_peers(1, self.lsof(1, header + row % "127.0.0.1")))

    def test_a_failed_sample_or_a_foreign_peer_stops_the_run(self):
        for peers, expected in ((None, "could not take a sample"), (["203.0.113.7"], "non-loopback socket")):
            with self.subTest(peers=peers), tempfile.TemporaryDirectory() as root:
                harness = capture.Harness.__new__(capture.Harness)
                harness.gens, harness.events, harness.started = [], [], 0.0
                harness.stop_reason, harness.socket_samples, harness.failed_samples = None, 0, 0
                harness.loopback_peers = set()
                process = subprocess.Popen(["/bin/sleep", "30"], start_new_session=True)
                try:
                    harness.gens.append(types.SimpleNamespace(proc=process, pgid=os.getpgid(process.pid)))
                    done = threading.Event()
                    original, capture.socket_peers = capture.socket_peers, lambda group: peers
                    try:
                        watcher = threading.Thread(target=harness.watch_sockets, args=(done,))
                        watcher.start()
                        process.wait(timeout=10)
                    finally:
                        done.set()
                        watcher.join()
                        capture.socket_peers = original
                finally:
                    if process.poll() is None:
                        process.kill()
                self.assertIn(expected, harness.stop_reason)
                self.assertEqual(harness.failed_samples, 1 if peers is None else 0)


class Redaction(unittest.TestCase):
    def redactor(self, user="example", host="machine.local"):
        return capture.redactor(
            [("/Users/example/x/home", "<HOME>"), ("/Users/example/x", "<SCRATCH>"), ("/Users/example", "<USER-HOME>")],
            user, host)

    def test_paths_host_user_and_identity_values_are_replaced_wherever_they_occur(self):
        redact, leaks, counts = self.redactor()
        frame = {"codexHome": "/Users/example/x/home", "cwd": "/Users/example/x/workspace",
                 "other": "/Users/example/Documents", "owner": "example", "userAgent": "client/1 (machine)",
                 "nested": [{"serverName": "machine.local", "installationId": "invented-private-installation"}],
                 "/Users/example/as-a-key": 1, "text": "on machine, by example; examples stay"}
        redacted = redact(frame)
        self.assertEqual(redacted, {
            "codexHome": "<HOME>", "cwd": "<SCRATCH>/workspace", "other": "<USER-HOME>/Documents",
            "owner": "<USER>", "userAgent": "<REDACTED-USER-AGENT>",
            "nested": [{"serverName": "<REDACTED-HOST>", "installationId": "<REDACTED-INSTALLATION-ID>"}],
            "<USER-HOME>/as-a-key": 1, "text": "on <HOST>, by <USER>; examples stay"})
        self.assertEqual(leaks(json.dumps(redacted)), [])
        self.assertEqual(counts["installation identifier"], 1)

    def test_identity_values_are_replaced_whatever_the_spacing_and_in_text_that_is_not_json(self):
        redact, _, _ = self.redactor()
        spaced = json.loads('{"installationId": "invented-private-installation", "serverName" : "host"}')
        self.assertEqual(redact(spaced), {"installationId": "<REDACTED-INSTALLATION-ID>", "serverName": "<REDACTED-HOST>"})
        self.assertEqual(redact('not json {"installationId" :  "invented-private-installation"}'),
                         'not json {"installationId" :  "<REDACTED-INSTALLATION-ID>"}')
        self.assertEqual(redact('escaped {\\"userAgent\\":\\"client\\"}'),
                         'escaped {\\"userAgent\\":\\"<REDACTED-USER-AGENT>\\"}')

    def test_short_names_are_replaced_and_anything_left_is_reported(self):
        redact, leaks, _ = self.redactor(user="al", host="mb")
        self.assertEqual(redact({"who": "al", "where": "mb", "word": "also male, amber"}),
                         {"who": "<USER>", "where": "<HOST>", "word": "also male, amber"})
        self.assertEqual(leaks("written by al on mb under /Users/example"), ["/Users/example", "mb", "al"])
        self.assertEqual(leaks("also male, amber"), [])


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
                self.assertEqual(record["socket_watch"]["failed_samples"], 0)
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
