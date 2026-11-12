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

import version_advance as VA

HERE = Path(__file__).resolve().parent
# Each committed comparison result: (prior pin, pin it advanced to).
COMMITTED = (("0.160.0", "0.167.0"), ("0.167.0", "0.167.2"))


def classes(before, after):
    return sorted({change["class"] for change in VA.diff_schema(before, after, "X")})


class CommittedResult(unittest.TestCase):
    def test_regenerating_each_committed_result_gives_the_same_bytes(self):
        for from_pin, to_pin in COMMITTED:
            with self.subTest(from_pin=from_pin, to_pin=to_pin):
                committed = HERE / "version_advance" / ("%s-to-%s.json" % (from_pin, to_pin))
                result = VA.compare(from_pin, to_pin)
                self.assertEqual(VA.render(result), committed.read_text(encoding="utf-8"))

    def test_the_advance_to_the_declared_pin_passed_with_no_findings(self):
        result = json.loads((HERE / "version_advance" / "0.167.0-to-0.167.2.json").read_text(encoding="utf-8"))
        self.assertEqual(result["verdict"]["verdict"], "passed")
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["inputs"]["missing"], [])


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
            "optional property": self.with_(properties={"a": {"type": "string"}, "b": {"type": "integer"}}),
            "widened type": self.with_(properties={"a": {"type": ["string", "null"]}}),
        }
        for name, after in cases.items():
            with self.subTest(name):
                self.assertEqual(classes(self.OBJECT, after), ["additive"])
        with self.subTest("enum value"):
            self.assertEqual(classes({"enum": ["x"], "type": "string"}, {"enum": ["x", "y"], "type": "string"}),
                             ["additive"])
        with self.subTest("alternative"):
            self.assertEqual(classes({"oneOf": [{"$ref": "#/definitions/A"}]},
                                     {"oneOf": [{"$ref": "#/definitions/A"}, {"$ref": "#/definitions/B"}]}),
                             ["additive"])
        with self.subTest("previous form kept as an alternative"):
            self.assertEqual(classes({"type": "string"}, {"anyOf": [{"type": "string"}, {"type": "null"}]}),
                             ["additive"])

    def test_each_breaking_kind(self):
        cases = {
            "removed property": (self.OBJECT, self.with_(properties={}, required=[])),
            "removed enum value": ({"enum": ["x", "y"], "type": "string"}, {"enum": ["x"], "type": "string"}),
            "removed alternative": ({"oneOf": [{"$ref": "#/definitions/A"}, {"$ref": "#/definitions/B"}]},
                                    {"oneOf": [{"$ref": "#/definitions/A"}]}),
            "narrowed type": ({"type": ["string", "null"]}, {"type": "string"}),
            "changed type": ({"type": "string"}, {"type": "integer"}),
            "changed reference": ({"$ref": "#/definitions/A"}, {"$ref": "#/definitions/B"}),
            "newly required": (self.with_(required=[]), self.OBJECT),
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


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def bundle(capability_properties):
    """A tiny invented protocol: one client request whose response carries `capability_properties`."""
    request = {"properties": {"id": {"type": "integer"}, "method": {"enum": ["invented/read"], "type": "string"},
                              "params": {"$ref": "#/definitions/v2/InventedReadParams"}},
               "required": ["id", "method", "params"], "type": "object"}
    unions = {name: {"oneOf": []} for name in ("ClientNotification", "ServerNotification", "ServerRequest")}
    return {"definitions": dict(unions, ClientRequest={"oneOf": [request]}, v2={
        "InventedReadParams": {"type": "object"},
        "InventedReadResponse": {"type": "object", "properties": capability_properties}})}


class Verdict(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.resources = self.root / "resources"
        before = bundle({"flag": {"type": "boolean"}, "kept": {"type": "string"}})
        after = bundle({"kept": {"type": "string"}})
        for pin, value in (("1.0.0", before), ("1.1.0", after)):
            write(self.resources / pin / VA.BUNDLE, value)
            v2 = dict(value["definitions"]["v2"], ClientRequest=json.loads(json.dumps(
                value["definitions"]["ClientRequest"]).replace("#/definitions/v2/", "#/definitions/")))
            v2.update({k: value["definitions"][k] for k in ("ServerNotification",)})
            write(self.resources / pin / VA.V2_BUNDLE, {"definitions": v2})
            (self.resources / pin / VA.MANIFEST).write_text(
                "aa  json-schema/stable/v2/InventedReadResponse.json\n"
                "aa  json-schema/experimental/v2/InventedReadResponse.json\n")
        self.source = self.root / "src"
        self.source.mkdir()
        (self.source / "host.rs").write_text('fn read() { call("invented/read"); }\n')
        self.dispositions = self.root / "dispositions.json"

    def tearDown(self):
        shutil.rmtree(self.root)

    def run_compare(self, **overrides):
        arguments = dict(resources=self.resources, source=self.source, dispositions=self.dispositions,
                         scenarios=())
        arguments.update(overrides)
        return VA.compare("1.0.0", "1.1.0", **arguments)

    def test_breaking_change_to_a_relied_on_element_needs_a_disposition(self):
        write(self.dispositions, [])
        result = self.run_compare()
        self.assertEqual(result["relied_on"]["methods"], {"invented/read": ["host.rs"]})
        self.assertIn("v2/InventedReadResponse", result["relied_on"]["definitions"])
        [found] = result["findings"]
        self.assertEqual((found["subject"], found["detail"]),
                         ("v2/InventedReadResponse/properties/flag", "property removed"))
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")
        self.assertEqual(result["verdict"]["undisposed_findings"], [found["id"]])
        write(self.dispositions, [{"finding": found["id"], "decided_by": "invented decider",
                                   "decision": "invented decision", "where_recorded": "invented record"}])
        result = self.run_compare()
        self.assertEqual(result["verdict"]["verdict"], "passed")
        self.assertEqual(result["verdict"]["disposed_findings"], [found["id"]])

    def test_the_same_change_to_an_element_not_relied_on_is_no_finding(self):
        (self.source / "host.rs").write_text('fn read() {}\n#[cfg(test)]\nmod tests { const M: &str = "invented/read"; }\n')
        (self.source / "host_tests.rs").write_text('const M: &str = "invented/read";\n')
        write(self.dispositions, [])
        result = self.run_compare()
        self.assertEqual(result["relied_on"]["methods"], {})
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["verdict"]["verdict"], "passed")

    def test_a_missing_input_never_passes(self):
        write(self.dispositions, [])
        (self.resources / "1.1.0" / VA.MANIFEST).unlink()
        result = self.run_compare(scenarios=())
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")
        self.assertEqual([entry["state"] for entry in result["inputs"]["missing"]], ["missing"])
        result = self.run_compare(scenarios=("st5",), from_recordings=self.root / "none",
                                  to_recordings=self.root / "none")
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")
        self.assertEqual(len(result["inputs"]["missing"]), 3)

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
