#!/usr/bin/env python3
"""Checks of the recordings committed at the declared pin: what the files themselves establish.

The recordings are evidence, made once by a harness that is not maintained (see the note beside
them). Nothing is executed here. Run from `app/`: python3 supplier_checks/test_recordings.py
"""
import calendar
import json
import re
import time
import unittest
from pathlib import Path

import intake

HERE = Path(__file__).resolve().parent
PIN = "0.167.0"
RECORDINGS = HERE / "recordings" / PIN
FORMAT = "chirality.app-v4.supplier-capture.v2"
SCENARIOS = ("st5", "nv04")
CHILD_PROMPT = "st5-child-brief-marker: count the invented files."


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


def clock_disclosures(text):
    """Rollout file names whose time, read as UTC, has no epoch in the text within two minutes of it.

    The supplier names a rollout file by the local clock. Beside the UTC epochs a recording also
    carries, a name written in another zone would state the host's offset from UTC.
    """
    epochs = [int(digits[:10]) for digits in re.findall(r"(?<![0-9.])[0-9]{10}(?:[0-9]{3})?(?![0-9.])", text)]
    names = sorted(set(re.findall(r"rollout-([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}-[0-9]{2}-[0-9]{2})", text)))
    return [name for name in names
            if not any(abs(calendar.timegm(time.strptime(name, "%Y-%m-%dT%H-%M-%S")) - epoch) < 120
                       for epoch in epochs)]


class RecordingsAtThePin(unittest.TestCase):
    def test_each_recording_names_the_pin_and_the_verified_distribution(self):
        expected = intake.expected_distribution(PIN)
        main = next(e for e in expected["inventory"]["entries"] if e["path"] == "bin/codex")
        self.assertEqual(sorted(p.name for p in RECORDINGS.iterdir()),
                         sorted([s + ".recording.json" for s in SCENARIOS] + ["README.md"]))
        for scenario in SCENARIOS:
            with self.subTest(scenario):
                record = recording(scenario)
                self.assertEqual((record["format"], record["scenario"], record["pin"]),
                                 (FORMAT, scenario, PIN))
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
                self.assertEqual(sorted(record["socket_watch"]["samples_by_generation"]), ["1", "2"])
                self.assertTrue(all(record["socket_watch"]["samples_by_generation"].values()))
                self.assertEqual(record["socket_watch"]["non_loopback_peers"], [])
                settings = record["settings_in_effect"]
                self.assertEqual(settings["environment"], ["CODEX_HOME", "HOME", "LANG", "PATH", "TMPDIR", "TZ"])
                self.assertEqual((settings["outside_configuration"]["system_configuration_folder"],
                                  settings["outside_configuration"]["managed_preferences"]), ("absent", "absent"))
                self.assertLessEqual(set(record["socket_watch"]["loopback_peers"]), {"127.0.0.1", "::1"})

    def test_frames_are_ordered_and_every_reply_answers_a_recorded_request(self):
        for scenario in SCENARIOS:
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

    def test_every_required_request_of_each_script_has_its_result(self):
        # What the files establish: each script's requests up to its last required reply were
        # answered with a result. Nothing here speaks of what the supplier sent after that reply.
        required = {
            "st5": {1: ["initialize", "thread/start", "turn/start"],
                    2: ["initialize", "thread/loaded/list", "thread/read", "thread/resume", "thread/turns/list"]},
            "nv04": {1: ["initialize", "thread/items/list", "thread/loaded/list", "thread/read", "thread/read",
                         "thread/start", "thread/turns/list", "turn/start"],
                     2: ["initialize", "thread/items/list", "thread/read", "thread/read", "thread/turns/list"]}}
        for scenario in SCENARIOS:
            answered = {1: [], 2: []}
            for generation, request, reply in replies(recording(scenario)):
                if "result" in reply:
                    answered[generation].append(request["method"])
            with self.subTest(scenario):
                self.assertEqual({g: sorted(methods) for g, methods in answered.items()}, required[scenario])

    def test_no_local_path_or_address_remains(self):
        pattern = re.compile(r"/Users/|/private/|/var/folders|/home/|[A-Za-z0-9._-]+@[A-Za-z0-9-]+\.[a-z]{2,}")
        for scenario in SCENARIOS:
            with self.subTest(scenario):
                text = (RECORDINGS / (scenario + ".recording.json")).read_text()
                self.assertIsNone(pattern.search(text))
                # A rollout file name in another zone than UTC would state the host's offset.
                self.assertIn("rollout-", text)
                self.assertEqual(clock_disclosures(text), [])

    def test_st5_answer_was_written_while_frozen_and_never_acknowledged_and_nothing_was_re_raised(self):
        events = {event["event"]: event for event in recording("st5")["events"]}
        names = [event["event"] for event in recording("st5")["events"]]
        self.assertEqual(events["answer-written"]["decision"], "accept")
        # Frozen before the answer was written: no acknowledgment can exist.
        self.assertLess(names.index("process-group-frozen"), names.index("answer-written"))
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


class ClockCheck(unittest.TestCase):
    def test_a_rollout_name_in_another_zone_than_utc_is_named(self):
        epoch = '"createdAt": 1794475811, "updatedAtMs": 1794475811123'
        self.assertEqual(clock_disclosures(epoch + ' "path": "s/rollout-2026-11-12T03-30-11-0193.jsonl"'),
                         ["2026-11-12T03-30-11"])
        self.assertEqual(clock_disclosures(epoch + ' "path": "s/rollout-2026-11-12T09-30-12-0193.jsonl"'), [])
        self.assertEqual(clock_disclosures('"path": "s/rollout-2026-11-12T09-30-12-0193.jsonl"'),
                         ["2026-11-12T09-30-12"])  # no epoch to compare with is not a pass


if __name__ == "__main__":
    unittest.main()
