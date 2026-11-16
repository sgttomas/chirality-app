"""Invented values only: these tests never execute the supplier."""
import copy
import json
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch

import delegation_probe as probe


class ProbeTests(unittest.TestCase):
    def reads(self, version=None):
        return {"config/read": {"layers": [], "config": {}},
                "configRequirements/read": {"requirements": None},
                "model/list": {"data": [{"model": probe.MODEL, "multiAgentVersion": version}], "nextCursor": None}}

    def test_provider_answers_text_only_and_refuses_a_second_request(self):
        declarations = []
        plan = probe.response_plan(declarations)
        body = {"tools": [{"type": "function", "name": "spawn_agent"}], "input": "not retained"}
        items, delay, label = plan(1, body)
        self.assertEqual([item["type"] for item in items], ["message"])
        self.assertEqual(delay, 0)
        self.assertNotIn("input", str(declarations))
        body["tools"].clear()
        self.assertEqual(declarations[0][0]["name"], "spawn_agent")
        with self.assertRaises(probe.capture.Refused):
            plan(2, body)

    def test_no_configured_delegation_except_named_disabled_case(self):
        for case in probe.CASES:
            config = tomllib.loads(probe.configuration(Path("/invented"), case, 1234))
            self.assertNotIn("multi_agent", config["features"])
            self.assertNotIn("multi_agent_v2", config["features"])
            self.assertEqual(config.get("agents"), {"enabled": False} if case == "agents-disabled" else None)
            self.assertEqual(probe.catalog(case)["models"][0].get("multi_agent_version"),
                             "disabled" if case == "catalog-disabled" else None)

    def test_missing_or_contrary_observation_refuses(self):
        tools = [[{"type": "namespace", "name": "agents", "tools": [{"name": "spawn_agent"}]}]]
        self.assertEqual(probe.check_observation("baseline", self.reads(), tools), ["spawn_agent"])
        for case, version in [("agents-disabled", None), ("catalog-disabled", "disabled")]:
            reads = self.reads(version)
            if case == "agents-disabled":
                reads["config/read"]["config"]["agents"] = {"enabled": False}
            self.assertEqual(probe.check_observation(case, reads, [[]]), [])
            with self.assertRaises(probe.capture.Refused):
                probe.check_observation(case, reads, tools)
        with self.assertRaises(probe.capture.Refused):
            probe.check_observation("baseline", self.reads(), [[]])
        for key, value in [("model/list", {"data": [], "nextCursor": "more"}),
                           ("config/read", {"config": {}}), ("configRequirements/read", {})]:
            reads = copy.deepcopy(self.reads())
            reads[key] = value
            with self.assertRaises(probe.capture.Refused):
                probe.check_observation("baseline", reads, tools)
        for altered in [{"config": {"features": {"multi_agent": False}}},
                        {"config": {"agents": {"enabled": True}}}, {"config": None}]:
            reads = self.reads()
            reads["config/read"]["layers"] = [altered]
            with self.assertRaises(probe.capture.Refused):
                probe.check_observation("baseline", reads, tools)
        reads = self.reads()
        reads["configRequirements/read"]["requirements"] = {"featureRequirements": {"multi_agent": True}}
        with self.assertRaises(probe.capture.Refused):
            probe.check_observation("baseline", reads, tools)

    def test_supplier_start_failure_still_closes_owned_run(self):
        closed = []
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "home").mkdir()
            class Run:
                def __init__(self, *args):
                    self.root = root
                    self.provider = type("Provider", (), {})()
                    self.frames = []
                def close(self):
                    closed.append(True)
            with patch.object(probe.capture, "Run", Run), patch.object(probe.capture, "Pipe", side_effect=OSError("invented failure")):
                with self.assertRaises(OSError):
                    probe.observe("unused", {}, root, "baseline", 1234)
            self.assertEqual(closed, [True])
            self.assertFalse((root / "observation.json").exists())
            self.assertEqual(json.loads((root / "refusal.json").read_text())["refusal"], "invented failure")

    def test_already_received_error_is_kept_on_refusal(self):
        with tempfile.TemporaryDirectory() as folder:
            run = type("Run", (), {})()
            run.root = Path(folder)
            run.frames = [{"direction": "codex->app", "generation": 1, "frame": {
                "id": 2, "error": {"code": -32600, "message": "invented invalid catalogue",
                                      "data": {"userId": "invented-identity"}}}}]
            before = copy.deepcopy(run.frames)
            probe.retain_refusal(run, "baseline", probe.capture.Refused("config/read did not return a result"))
            record = json.loads((run.root / "refusal.json").read_text())
            error = record["frames"][0]["frame"]["error"]
            self.assertEqual(error["message"], "invented invalid catalogue")
            self.assertEqual(error["code"], -32600)
            self.assertEqual(error["data"]["userId"], "<WITHHELD>")
            self.assertEqual(run.frames, before)
            with self.assertRaises(FileExistsError):
                probe.retain_refusal(run, "baseline", Exception("second"))


if __name__ == "__main__":
    unittest.main()
