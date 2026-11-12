#!/usr/bin/env python3
"""Checks of the version-advance inventory, difference and evidence check, and of its committed result.

No supplier or model is executed. Run from `app/`: python3 supplier_checks/test_version_advance.py
"""
import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import version_advance as VA

HERE = Path(__file__).resolve().parent
COMMITTED = HERE / "version_advance" / "0.160.0-to-0.167.0.json"
RESOURCES = HERE.parent / "src-tauri" / "resources" / "supplier"
RECORDINGS = HERE / "recordings" / "0.167.0"
NEXT = "0.167.9"  # an invented pin whose inputs the tests derive from 0.167.0's


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def dispose(path, identifiers):
    write(path, [{"finding": identifier, "decided_by": "invented decider", "decision": "invented decision",
                  "where_recorded": "invented record"} for identifier in identifiers])


class CommittedResult(unittest.TestCase):
    def test_regenerating_the_committed_result_gives_the_same_bytes(self):
        self.assertEqual(VA.render(VA.compare("0.160.0", "0.167.0")), COMMITTED.read_text(encoding="utf-8"))


class IdentityAndDifference(unittest.TestCase):
    def test_identity_is_exact_content_equality(self):
        self.assertEqual(VA.diff_paths({"a": 1, "b": [1, 2]}, {"b": [1, 2], "a": 1}), [])
        self.assertEqual(VA.diff_paths({"a": 1}, {"a": 1.0}), [{"path": "/a", "before": 1, "after": 1.0}])
        self.assertEqual(VA.diff_paths({"title": "x", "description": "y"}, {"title": "x", "description": "z"}),
                         [{"path": "/description", "before": "y", "after": "z"}])

    def test_differences_are_listed_by_path_with_long_values_by_digest(self):
        long_text = "x" * (VA.LONG + 10)
        self.assertEqual(VA.diff_paths({"p": {"q": [1, 2]}, "gone": 1}, {"p": {"q": [1, 3]}, "new": long_text}), [
            {"path": "/gone", "before": 1, "after": "<absent>"},
            {"path": "/new", "before": "<absent>", "after": {"sha256": VA.content_sha(long_text),
                                                               "length": len(long_text) + 2}},
            {"path": "/p/q/1", "before": 2, "after": 3}])
        self.assertEqual(VA.diff_paths({"e": ["a"]}, {"e": ["a", "b"]}),
                         [{"path": "/e/1", "before": "<absent>", "after": "b"}])


def request(method, params):
    return {"properties": {"id": {"type": "integer"}, "method": {"enum": [method], "type": "string"},
                           "params": {"$ref": "#/definitions/v2/%sParams" % params}},
            "required": ["id", "method", "params"], "type": "object"}


def notification(method):
    return {"properties": {"method": {"enum": [method], "type": "string"}}, "required": ["method"],
            "type": "object"}


def bundle(inner):
    """A tiny invented protocol: invented/read returns InventedReadResponse, which reaches Inner."""
    return {"definitions": {
        "ClientRequest": {"oneOf": [request("invented/read", "InventedRead")]},
        "ClientNotification": {"oneOf": [notification("invented/initialized")]},
        "ServerNotification": {"oneOf": [notification("invented/changed")]},
        "ServerRequest": {"oneOf": [request("invented/ask", "InventedAsk")]},
        "v2": {"InventedReadParams": {"type": "object"}, "InventedAskParams": {"type": "object"},
               "InventedReadResponse": {"type": "object", "properties": {"inner": {"$ref": "#/definitions/v2/Inner"}}},
               "Inner": inner}}}


def flat(value):
    copy = dict(value["definitions"]["v2"], **{k: v for k, v in value["definitions"].items() if k != "v2"})
    return json.loads(json.dumps({"definitions": copy}).replace("#/definitions/v2/", "#/definitions/"))


class Findings(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.resources = self.root / "resources"
        self.write_pin("1.0.0", {"type": "object", "properties": {"flag": {"type": "boolean"}}})
        self.write_pin("1.1.0", {"type": "object", "properties": {}})
        self.source = self.root / "src"
        (self.source).mkdir()
        (self.source / "host.rs").write_text('fn read() { call("invented/read"); }\n')
        self.dispositions = self.root / "dispositions.json"
        write(self.dispositions, [])

    def tearDown(self):
        shutil.rmtree(self.root)

    def write_pin(self, pin, inner):
        value = bundle(inner)
        write(self.resources / pin / VA.BUNDLE, value)
        write(self.resources / pin / VA.V2_BUNDLE, flat(value))
        (self.resources / pin / VA.MANIFEST).write_text("aa  json-schema/stable/v2/Inner.json\n"
                                                        "aa  json-schema/experimental/v2/Inner.json\n")

    def run_compare(self, **overrides):
        arguments = dict(resources=self.resources, source=self.source, dispositions=self.dispositions,
                         scenarios=())
        arguments.update(overrides)
        return VA.compare("1.0.0", "1.1.0", **arguments)

    def test_a_definition_reached_only_by_reference_is_compared_and_its_change_is_a_finding(self):
        result = self.run_compare()
        self.assertEqual(result["relied_on"]["roots"], ["v2/InventedReadParams", "v2/InventedReadResponse"])
        self.assertEqual(result["schema"]["relied_on_and_reached"]["unchanged"],
                         ["v2/InventedReadParams", "v2/InventedReadResponse"])
        changed = result["schema"]["relied_on_and_reached"]["changed"]["v2/Inner"]
        self.assertEqual((changed["state"], changed["role"]), ("changed", "reached by reference"))
        self.assertEqual(changed["difference"], [{"path": "/properties/flag", "before": {"type": "boolean"},
                                                  "after": "<absent>"}])
        [found] = result["findings"]
        self.assertEqual((found["kind"], found["subject"]), ("definition changed", "v2/Inner"))
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")

    def test_a_matching_disposition_passes_and_one_for_a_different_change_does_not(self):
        identifier = self.run_compare()["findings"][0]["id"]
        dispose(self.dispositions, [identifier])
        self.assertEqual(self.run_compare()["verdict"]["verdict"], "passed")
        # The same definition changed differently: the decided identifier no longer applies.
        self.write_pin("1.1.0", {"type": "object", "properties": {"flag": {"type": "string"}}})
        result = self.run_compare()
        self.assertNotEqual(result["findings"][0]["id"], identifier)
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")
        self.assertEqual(result["verdict"]["dispositions_naming_no_finding"], [identifier])

    def test_any_change_to_a_relied_on_definition_is_a_finding_whatever_it_contains(self):
        """Round 2 probe B in its new meaning: a new optional property whose schema is false or holds pattern."""
        for addition in (False, {"type": "string", "pattern": "^x"}, {"description": "words only"}):
            with self.subTest(addition=addition):
                self.write_pin("1.1.0", {"type": "object", "properties": {"flag": {"type": "boolean"},
                                                                          "invented": addition}})
                result = self.run_compare()
                self.assertEqual([f["subject"] for f in result["findings"]], ["v2/Inner"])
                self.assertEqual(result["verdict"]["verdict"], "returned for decision")

    def test_a_disposition_naming_no_finding_prevents_passing(self):
        identifier = self.run_compare()["findings"][0]["id"]
        dispose(self.dispositions, [identifier, "VA-does-not-exist"])
        verdict = self.run_compare()["verdict"]
        self.assertEqual((verdict["verdict"], verdict["dispositions_naming_no_finding"]),
                         ("returned for decision", ["VA-does-not-exist"]))

    def test_missing_and_empty_inputs_never_pass(self):
        dispose(self.dispositions, [self.run_compare()["findings"][0]["id"]])
        (self.resources / "1.1.0" / VA.MANIFEST).unlink()
        result = self.run_compare()
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")
        self.assertEqual(len(result["inadmissible"]["missing_inputs"]), 1)
        for pin in ("1.0.0", "1.1.0"):
            for name in (VA.BUNDLE, VA.V2_BUNDLE):
                write(self.resources / pin / name, {"definitions": {}})
            (self.resources / pin / VA.MANIFEST).write_text("")
            (self.resources / pin / VA.SUPPLEMENT).mkdir()
        (self.source / "host.rs").write_text("fn main() {}\n")
        problems = {(p["role"], p["problem"]) for p in self.run_compare()["inadmissible"]["missing_structure"]}
        for expected in [("generated schema bundle", "no v2 definitions"),
                         ("generated schema bundle", "no usable ClientRequest union (members naming their method)"),
                         ("generator output manifest", "lists no json-schema file in variant(s) experimental, stable"),
                         ("supplement at 1.0.0", "present but not readable as a file (IsADirectoryError)"),
                         ("host source", "no protocol method of either pin appears in it as a string literal")]:
            self.assertIn(expected, problems)

    def test_the_v2_bundle_is_compared_in_both_directions(self):
        main = json.loads((RESOURCES / "0.167.0" / VA.BUNDLE).read_text())
        v2 = json.loads((RESOURCES / "0.167.0" / VA.V2_BUNDLE).read_text())
        self.assertEqual(VA.v2_bundle_differences(VA.definitions(main), v2), [])
        del v2["definitions"]["ThreadItem"]
        self.assertEqual(VA.v2_bundle_differences(VA.definitions(main), v2), ["ThreadItem (absent from the v2 bundle)"])

    def test_an_unknown_pin_is_refused_with_a_clear_message(self):
        with self.assertRaisesRegex(VA.Refused, "unknown pin 9.9.9"):
            VA.compare("1.0.0", "9.9.9", resources=self.resources)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = VA.main(["compare", "--from", "0.160.0", "--to", "9.9.9", "--out", str(self.root / "out.json")])
        self.assertEqual(code, 2)
        self.assertIn("unknown pin 9.9.9", stderr.getvalue())


class Evidence(unittest.TestCase):
    """0.167.0 against an invented next pin with byte-identical schemas and 0.167.0's recordings: it passes on
    evidence alone, and each defect of the evidence prevents passing whatever is disposed."""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.resources = self.root / "resources"
        (self.resources / NEXT).mkdir(parents=True)
        for name in (VA.BUNDLE, VA.V2_BUNDLE, VA.MANIFEST):
            shutil.copyfile(RESOURCES / "0.167.0" / name, self.resources / NEXT / name)
        self.recordings = self.root / "recordings"
        self.records = {}
        for scenario in VA.SCENARIOS:
            record = json.loads((RECORDINGS / (scenario + ".recording.json")).read_text())
            self.records[scenario] = dict(record, pin=NEXT)
        self.dispositions = self.root / "dispositions.json"
        write(self.dispositions, [])

    def tearDown(self):
        shutil.rmtree(self.root)

    def run_compare(self, dispose_all=True):
        for scenario, record in self.records.items():
            write(self.recordings / (scenario + ".recording.json"), record)
        arguments = dict(to_resources=self.resources, to_recordings=self.recordings, dispositions=self.dispositions)
        result = VA.compare("0.167.0", NEXT, **arguments)
        if dispose_all and result["findings"]:
            dispose(self.dispositions, [f["id"] for f in result["findings"]])
            result = VA.compare("0.167.0", NEXT, **arguments)
        return result

    def frames(self, scenario, keep):
        self.records[scenario]["frames"] = [row for row in self.records[scenario]["frames"] if keep(row)]

    def assert_inadmissible(self, section, fragment):
        result = self.run_compare()
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")
        self.assertEqual(result["verdict"]["undisposed_findings"], [])
        self.assertTrue(any(fragment in json.dumps(item) for item in result["inadmissible"][section]),
                        result["inadmissible"][section])

    def test_identical_schemas_and_healthy_recordings_pass_with_nothing_to_dispose(self):
        result = self.run_compare(dispose_all=False)
        self.assertEqual((result["verdict"]["verdict"], result["findings"], result["verdict"]["reasons"]),
                         ("passed", [], []))
        self.assertEqual(result["schema"]["relied_on_and_reached"]["changed"], {})

    def test_an_unhealthy_socket_watch_never_passes(self):
        cases = {
            "failed_samples present and zero": lambda w: w.update(failed_samples=1),
            "samples an integer greater than zero": lambda w: w.update(samples=0),
            "samples_by_generation of at least one": lambda w: w["samples_by_generation"].pop("2"),
            "non_loopback_peers present and empty": lambda w: w.update(non_loopback_peers=["192.0.2.1"]),
            "loopback_peers only 127.0.0.1 or ::1": lambda w: w.update(loopback_peers=["10.0.0.1"]),
        }
        for fragment, change in cases.items():
            with self.subTest(fragment):
                self.setUp()
                change(self.records["st5"]["socket_watch"])
                self.assert_inadmissible("recording_admission", fragment)
        with self.subTest("no report"):
            self.setUp()
            del self.records["nv04"]["socket_watch"]
            self.assert_inadmissible("recording_admission", "a socket_watch report")

    def test_a_missing_script_step_in_any_generation_never_passes(self):
        """Round 2 probe C: generation 2's nv04 thread/items/list request and reply removed."""
        removed = [row["frame"]["id"] for row in self.records["nv04"]["frames"] if row["generation"] == 2
                   and row["frame"].get("method") == "thread/items/list"]
        self.frames("nv04", lambda row: not (row["generation"] == 2 and row["frame"].get("id") in removed))
        self.assert_inadmissible("recording_admission", "generation 2: App request thread/items/list with its result")

    def test_a_new_pin_recording_of_the_older_format_never_passes(self):
        self.records["st5"]["format"] = VA.OLDER
        self.records["st5"].pop("pin")
        self.records["st5"]["events"] = [{"event": "begin", "pin": NEXT}] + self.records["st5"]["events"]
        self.assert_inadmissible("recording_admission", "the current recording format")

    def test_a_validation_failure_at_the_new_pin_never_passes(self):
        for row in self.records["st5"]["frames"]:
            if row["frame"].get("method") == "turn/started":
                row["frame"]["params"] = {"invented": True}
        self.assert_inadmissible("validation_failures", "turn/started")

    def test_an_expected_mechanism_not_observed_never_passes(self):
        frames = self.records["st5"]["frames"]
        answer = next(i for i, row in enumerate(frames) if row["direction"] == "app->codex"
                      and "method" not in row["frame"] and row["generation"] == 1)
        frames.insert(answer + 1, dict(frames[answer], direction="codex->app", position=999, frame={
            "method": "serverRequest/resolved", "params": {"threadId": "t", "requestId": 0}}))
        self.assert_inadmissible("mechanisms_not_observed", "acknowledged")

    def test_a_relied_on_group_that_disappears_is_a_finding(self):
        self.frames("st5", lambda row: row["frame"].get("method") != "turn/started")
        result = self.run_compare(dispose_all=False)
        self.assertIn(("recorded group absent at the new pin", "st5 notification turn/started"),
                      [(f["kind"], f["subject"]) for f in result["findings"]])


class Shape(unittest.TestCase):
    def rows(self, *frames):
        return [{"generation": 1, "direction": "codex->app", "position": n + 1, "t_ms": 0, "redacted": False,
                 "frame": frame} for n, frame in enumerate(frames)]

    def test_identifiers_and_times_are_ignored_and_a_missing_key_is_caught(self):
        first = {"method": "turn/started", "params": {"threadId": "019a-one", "startedAtMs": 1000,
                                                      "byThread": {"0f8fad5b-d9cb-469f-a165-70867728950e": 1}}}
        second = {"method": "turn/started", "params": {"threadId": "019a-two", "startedAtMs": 2999,
                                                       "byThread": {"7c9e6679-7425-40de-944b-e07fc1f90ae7": 5}}}
        before, after = VA.shapes(self.rows(first)), VA.shapes(self.rows(second))
        self.assertEqual(VA.shape_differences(before, after), {})
        missing = {"method": "turn/started", "params": {"threadId": "019a-three",
                                                        "byThread": {"7c9e6679-7425-40de-944b-e07fc1f90ae7": 5}}}
        differences = VA.shape_differences(before, VA.shapes(self.rows(missing)))
        self.assertEqual(differences["notification turn/started"]["paths_only_before"], ["$.params.startedAtMs"])


if __name__ == "__main__":
    unittest.main()
