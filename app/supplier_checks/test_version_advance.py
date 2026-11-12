#!/usr/bin/env python3
"""Checks of the version-advance comparison and of its committed result.

No supplier or model is executed. Run from `app/`: python3 supplier_checks/test_version_advance.py
"""
import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft7Validator

import version_advance as VA

HERE = Path(__file__).resolve().parent
COMMITTED = HERE / "version_advance" / "0.160.0-to-0.167.0.json"
RESOURCES = HERE.parent / "src-tauri" / "resources" / "supplier"


def classes(before, after):
    return sorted({change["class"] for change in VA.diff_schema(before, after, "X")})


class CommittedResult(unittest.TestCase):
    def test_regenerating_the_committed_result_gives_the_same_bytes(self):
        result = VA.compare("0.160.0", "0.167.0")
        self.assertEqual(VA.render(result), COMMITTED.read_text(encoding="utf-8"))


class Classification(unittest.TestCase):
    OBJECT = {"type": "object", "properties": {"a": {"type": "string"}}, "required": ["a"]}

    def with_(self, **changes):
        node = json.loads(json.dumps(self.OBJECT))
        node.update(changes)
        return node

    def test_documentation_only(self):
        self.assertEqual(classes(self.OBJECT, self.with_(description="new words")), ["documentation only"])

    def test_each_additive_kind(self):
        cases = {
            "optional property": (self.OBJECT, self.with_(
                properties={"a": {"type": "string"}, "b": {"type": "integer"}})),
            "widened type": (self.OBJECT, self.with_(properties={"a": {"type": ["string", "null"]}})),
            "enum value": ({"enum": ["x"], "type": "string"}, {"enum": ["x", "y"], "type": "string"}),
            "anyOf member": ({"anyOf": [{"$ref": "#/definitions/A"}]},
                             {"anyOf": [{"$ref": "#/definitions/A"}, {"$ref": "#/definitions/B"}]}),
            "previous form kept as an alternative": ({"type": "string"},
                                                     {"anyOf": [{"type": "string"}, {"type": "null"}]}),
        }
        for name, (before, after) in cases.items():
            with self.subTest(name):
                self.assertEqual(classes(before, after), ["additive"])

    def test_a_distinctly_tagged_oneOf_member_is_additive(self):
        def member(tag):
            return {"type": "object", "properties": {"type": {"enum": [tag], "type": "string"}}, "required": ["type"]}
        self.assertEqual(classes({"oneOf": [member("a")]}, {"oneOf": [member("a"), member("b")]}), ["additive"])
        self.assertEqual(classes({"oneOf": [{"enum": ["a"]}]}, {"oneOf": [{"enum": ["a"]}, {"enum": ["b"]}]}),
                         ["additive"])

    def test_each_breaking_kind(self):
        cases = {
            "removed property": (self.OBJECT, self.with_(properties={}, required=[])),
            "removed enum value": ({"enum": ["x", "y"], "type": "string"}, {"enum": ["x"], "type": "string"}),
            "removed alternative": ({"anyOf": [{"$ref": "#/definitions/A"}, {"$ref": "#/definitions/B"}]},
                                    {"anyOf": [{"$ref": "#/definitions/A"}]}),
            "narrowed type": ({"type": ["string", "null"]}, {"type": "string"}),
            "changed type": ({"type": "string"}, {"type": "integer"}),
            "changed reference": ({"$ref": "#/definitions/A"}, {"$ref": "#/definitions/B"}),
            "newly required": (self.with_(required=[]), self.OBJECT),
            "newly required although never named": (self.OBJECT, self.with_(required=["a", "z"])),
            "required property added": (self.OBJECT, self.with_(
                properties={"a": {"type": "string"}, "b": {"type": "string"}}, required=["a", "b"])),
        }
        for name, (before, after) in cases.items():
            with self.subTest(name):
                self.assertEqual(classes(before, after), ["breaking"])

    def test_what_cannot_be_classified_is_never_additive(self):
        self.assertEqual(classes(self.OBJECT, self.with_(required=[])), ["unclassified"])
        self.assertEqual(classes({"type": "string", "default": "a"}, {"type": "string", "default": "b"}),
                         ["unclassified"])
        self.assertEqual(classes({"type": "integer", "format": "int32"}, {"type": "integer", "format": "int64"}),
                         ["unclassified"])

    def test_a_keyword_the_classifier_does_not_support_is_reported_unsupported(self):
        self.assertEqual(classes({"type": "string"}, {"type": "string", "pattern": "^a"}), ["unsupported"])
        self.assertEqual(classes({"type": "array", "items": [{"type": "string"}]},
                                 {"type": "array", "items": [{"type": "integer"}]}), ["unsupported"])

    def test_reviewer_probes_that_break_an_existing_sender_are_never_additive(self):
        probes = [
            ("oneOf overlap", {"oneOf": [{"type": "integer"}]},
             {"oneOf": [{"type": "integer"}, {"type": "number"}]}, 1),
            ("alternative hides sibling constraint", {"type": "string"},
             {"anyOf": [{"type": "string"}, {"type": "null"}], "maxLength": 1}, "xx"),
            ("documentation-named property hidden", {"type": "object", "properties": {"title": {"type": "string"}}},
             {"anyOf": [{"type": "object", "properties": {"title": {"type": "integer"}}}, {"type": "null"}]},
             {"title": "x"}),
            ("draft change", {"$schema": "http://json-schema.org/draft-07/schema#", "type": "array",
                              "items": [{"type": "string"}]},
             {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "array",
              "items": [{"type": "string"}]}, []),
        ]
        for name, before, after, instance in probes:
            with self.subTest(name):
                found = set(classes(before, after))
                self.assertTrue(found & {"breaking", "unclassified", "unsupported"}, found)
                if name != "draft change":  # a dialect change is not judged by Draft 7
                    self.assertTrue(Draft7Validator(before).is_valid(instance))
                    self.assertFalse(Draft7Validator(after).is_valid(instance))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def request(method, params):
    return {"properties": {"id": {"type": "integer"}, "method": {"enum": [method], "type": "string"},
                           "params": {"$ref": "#/definitions/v2/%sParams" % params}},
            "required": ["id", "method", "params"], "type": "object"}


def notification(method):
    return {"properties": {"method": {"enum": [method], "type": "string"}}, "required": ["method"],
            "type": "object"}


def bundle(capability_properties):
    """A tiny invented protocol: client requests invented/read, whose response carries
    `capability_properties`, and invented/list, which does not change."""
    unions = {"ClientRequest": {"oneOf": [request("invented/read", "InventedRead"),
                                          request("invented/list", "InventedList")]},
              "ClientNotification": {"oneOf": [notification("invented/initialized")]},
              "ServerNotification": {"oneOf": [notification("invented/changed")]},
              "ServerRequest": {"oneOf": [request("invented/ask", "InventedAsk")]}}
    return {"definitions": dict(unions, v2={
        "InventedReadParams": {"type": "object"}, "InventedListParams": {"type": "object"},
        "InventedAskParams": {"type": "object"}, "InventedListResponse": {"type": "object"},
        "InventedReadResponse": {"type": "object", "properties": capability_properties}})}


def flat(value):
    """The v2 bundle of an invented main bundle: its v2 definitions and unions, references flattened."""
    copy = dict(value["definitions"]["v2"], **{k: v for k, v in value["definitions"].items() if k != "v2"})
    return json.loads(json.dumps({"definitions": copy}).replace("#/definitions/v2/", "#/definitions/"))


class Verdict(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.resources = self.root / "resources"
        before = bundle({"flag": {"type": "boolean"}, "kept": {"type": "string"}})
        after = bundle({"kept": {"type": "string"}})
        for pin, value in (("1.0.0", before), ("1.1.0", after)):
            write(self.resources / pin / VA.BUNDLE, value)
            write(self.resources / pin / VA.V2_BUNDLE, flat(value))
            (self.resources / pin / VA.MANIFEST).write_text(
                "aa  json-schema/stable/v2/InventedReadResponse.json\n"
                "aa  json-schema/experimental/v2/InventedReadResponse.json\n")
        self.source = self.root / "src"
        self.source.mkdir()
        (self.source / "host.rs").write_text('fn read() { call("invented/read"); call("invented/list"); }\n')
        self.dispositions = self.root / "dispositions.json"
        write(self.dispositions, [])

    def tearDown(self):
        shutil.rmtree(self.root)

    def run_compare(self, **overrides):
        arguments = dict(resources=self.resources, source=self.source, dispositions=self.dispositions,
                         scenarios=())
        arguments.update(overrides)
        return VA.compare("1.0.0", "1.1.0", **arguments)

    def dispose(self, *identifiers):
        write(self.dispositions, [{"finding": identifier, "decided_by": "invented decider",
                                   "decision": "invented decision", "where_recorded": "invented record"}
                                  for identifier in identifiers])

    def test_breaking_change_to_a_relied_on_element_needs_a_disposition(self):
        result = self.run_compare()
        self.assertEqual(result["relied_on"]["methods"], {"invented/list": ["host.rs"], "invented/read": ["host.rs"]})
        self.assertIn("v2/InventedReadResponse", result["relied_on"]["definitions"])
        [found] = result["findings"]
        self.assertEqual((found["subject"], found["detail"]),
                         ("v2/InventedReadResponse/properties/flag", "property removed"))
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")
        self.assertEqual(result["verdict"]["undisposed_findings"], [found["id"]])
        self.dispose(found["id"])
        result = self.run_compare()
        self.assertEqual(result["verdict"]["verdict"], "passed")
        self.assertEqual(result["verdict"]["reasons"], [])
        self.assertEqual(result["verdict"]["disposed_findings"], [found["id"]])

    def test_the_same_change_to_an_element_not_relied_on_is_no_finding(self):
        (self.source / "host.rs").write_text(
            'fn list() { call("invented/list"); }\n#[cfg(test)]\nmod tests { const M: &str = "invented/read"; }\n')
        (self.source / "host_tests.rs").write_text('const M: &str = "invented/read";\n')
        result = self.run_compare()
        self.assertEqual(result["relied_on"]["methods"], {"invented/list": ["host.rs"]})
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["verdict"]["verdict"], "passed")

    def test_a_disposition_naming_no_finding_prevents_passing(self):
        found = self.run_compare()["findings"][0]["id"]
        self.dispose(found, "VA-does-not-exist")
        verdict = self.run_compare()["verdict"]
        self.assertEqual(verdict["verdict"], "returned for decision")
        self.assertEqual(verdict["dispositions_naming_no_finding"], ["VA-does-not-exist"])

    def test_a_missing_input_never_passes(self):
        (self.resources / "1.1.0" / VA.MANIFEST).unlink()
        result = self.run_compare()
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")
        self.assertEqual([entry["state"] for entry in result["unusable"]["missing_inputs"]], ["missing"])
        result = self.run_compare(scenarios=("st5",), from_recordings=self.root / "none",
                                  to_recordings=self.root / "none")
        self.assertEqual(len(result["unusable"]["missing_inputs"]), 3)

    def test_empty_and_unusable_inputs_never_pass(self):
        """The reviewer's fixture: valid JSON everywhere, no protocol, no manifest lines, no frames."""
        recordings = self.root / "recordings"
        for pin in ("1.0.0", "1.1.0"):
            for name in (VA.BUNDLE, VA.V2_BUNDLE):
                write(self.resources / pin / name, {"definitions": {}})
            (self.resources / pin / VA.MANIFEST).write_text("")
            for scenario in VA.SCENARIOS:
                write(recordings / pin / (scenario + ".recording.json"), {
                    "format": "chirality.app-v4.supplier-capture.v2", "scenario": scenario, "pin": pin, "frames": []})
        (self.source / "host.rs").write_text("fn main() {}\n")
        result = self.run_compare(scenarios=VA.SCENARIOS, from_recordings=recordings / "1.0.0",
                                  to_recordings=recordings / "1.1.0")
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")
        problems = {(item["role"], item["problem"]) for item in result["unusable"]["missing_structure"]}
        for expected in [("generated schema bundle", "no usable ClientRequest union (members naming their method)"),
                         ("generated schema bundle", "no v2 definitions"),
                         ("generator output manifest", "lists no json-schema file in variant(s) experimental, stable"),
                         ("recording nv04", "no frames"),
                         ("host source", "no protocol method of either pin appears in it as a string literal")]:
            self.assertIn(expected, problems)

    def test_a_supplement_path_that_is_not_a_file_is_an_input_problem(self):
        for pin in ("1.0.0", "1.1.0"):
            (self.resources / pin / VA.SUPPLEMENT).mkdir()
        self.dispose(self.run_compare()["findings"][0]["id"])
        result = self.run_compare()
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")
        self.assertEqual(sorted(item["role"] for item in result["unusable"]["missing_structure"]),
                         ["supplement at 1.0.0", "supplement at 1.1.0"])

    def test_an_unsupported_construct_prevents_passing(self):
        value = bundle({"kept": {"type": "string"}})
        value["definitions"]["v2"]["InventedListResponse"]["pattern"] = "^a"
        write(self.resources / "1.1.0" / VA.BUNDLE, value)
        write(self.resources / "1.1.0" / VA.V2_BUNDLE, flat(value))
        self.dispose(self.run_compare()["findings"][0]["id"])
        result = self.run_compare()
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")
        self.assertEqual(result["unusable"]["unsupported_constructs"],
                         [{"path": "v2/InventedListResponse/pattern", "construct": "keyword pattern is not supported"}])

    def test_the_v2_bundle_is_compared_in_both_directions(self):
        main = json.loads((RESOURCES / "0.167.0" / VA.BUNDLE).read_text())
        v2 = json.loads((RESOURCES / "0.167.0" / VA.V2_BUNDLE).read_text())
        self.assertEqual(VA.v2_bundle_differences(VA.definitions(main), v2), [])
        del v2["definitions"]["ThreadItem"]
        self.assertEqual(VA.v2_bundle_differences(VA.definitions(main), v2),
                         ["ThreadItem (absent from the v2 bundle)"])

    def test_an_unknown_pin_is_refused_with_a_clear_message(self):
        with self.assertRaisesRegex(VA.Refused, "unknown pin 9.9.9"):
            VA.compare("1.0.0", "9.9.9", resources=self.resources)
        with self.assertRaisesRegex(VA.Refused, "not a pin"):
            VA.compare("1.0.0", "latest", resources=self.resources)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = VA.main(["compare", "--from", "0.160.0", "--to", "9.9.9", "--out", str(self.root / "out.json")])
        self.assertEqual(code, 2)
        self.assertIn("unknown pin 9.9.9", stderr.getvalue())
        self.assertFalse((self.root / "out.json").exists())


class Recordings(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.root)

    def changed_recordings(self, change):
        folder = self.root / "to"
        folder.mkdir()
        for path in (HERE / "recordings" / "0.167.0").glob("*.recording.json"):
            record = json.loads(path.read_text())
            change(record)
            (folder / path.name).write_text(json.dumps(record))
        return folder

    def test_a_relied_on_group_that_disappears_although_driven_is_a_finding(self):
        """The reviewer's probe: every supplier turn/started frame removed from the new recordings."""
        baseline = json.loads(COMMITTED.read_text())
        folder = self.changed_recordings(lambda record: record.update(frames=[
            row for row in record["frames"] if row["frame"].get("method") != "turn/started"]))
        result = VA.compare("0.160.0", "0.167.0", to_recordings=folder)
        new = [f for f in result["findings"] if f["id"] not in {g["id"] for g in baseline["findings"]}]
        self.assertEqual(sorted((f["kind"], f["subject"]) for f in new), [
            ("recorded group absent although driven", "%s notification turn/started" % scenario)
            for scenario in ("nv04", "st5", "st5-race")])
        dispositions = self.root / "dispositions.json"
        write(dispositions, [{"finding": f["id"], "decided_by": "invented", "decision": "invented",
                              "where_recorded": "invented"} for f in baseline["findings"]])
        self.assertEqual(VA.compare("0.160.0", "0.167.0", to_recordings=folder, dispositions=dispositions)[
            "verdict"]["verdict"], "returned for decision")

    def test_a_group_whose_eliciting_step_is_gone_is_listed_as_not_driven(self):
        before = [{"generation": 1, "direction": d, "position": n, "frame": f} for n, (d, f) in enumerate([
            ("app->codex", {"id": 1, "method": "turn/start"}), ("codex->app", {"method": "turn/started"})])]
        absent = VA.absent_groups(before, before[:0], VA.shapes(before), {})
        self.assertEqual(absent["notification turn/started"]["driven"], False)

    def test_a_recording_that_lacks_required_coverage_never_passes(self):
        folder = self.changed_recordings(lambda record: record.update(frames=[
            row for row in record["frames"]
            if row["frame"].get("method") != "item/commandExecution/requestApproval"]))
        result = VA.compare("0.160.0", "0.167.0", to_recordings=folder)
        lacks = {(item["scenario"], item["lacks"]) for item in result["unusable"]["insufficient_coverage"]}
        self.assertIn(("st5", VA.COVERAGE["st5"][0]), lacks)
        self.assertIn(("st5-race", VA.COVERAGE["st5-race"][0]), lacks)
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")


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
