#!/usr/bin/env python3
"""Checks of the version-advance inventory, difference and evidence check, and of its committed result.

No supplier or model is executed. The tool reads every input from its place in the repository;
these tests point those places at invented trees. Run from `app/`:
python3 supplier_checks/test_version_advance.py
"""
import contextlib
import hashlib
import io
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

import intake
import version_advance as VA

HERE = Path(__file__).resolve().parent
COMMITTED = HERE / "version_advance" / "0.160.0-to-0.167.0.json"
RESOURCES = HERE.parent / "src-tauri" / "resources" / "supplier"
RECORDINGS = HERE / "recordings" / "0.167.0"
OLD, PIN, NEXT = "0.160.0", "0.167.0", "0.167.2"  # pins of the table; the trees under them are invented


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


class InventedTree(unittest.TestCase):
    """Points every place the tool reads at a temporary tree, and puts them back."""

    def setUp(self):
        self.root = Path(os.path.realpath(tempfile.mkdtemp()))
        self.originals = (intake.RESOURCES, VA.RECORDINGS, VA.SOURCE, VA.RESULTS)
        self.resources, self.recordings = self.root / "resources", self.root / "recordings"
        self.source, self.results = self.root / "src", self.root / "results"
        for folder in (self.resources, self.recordings, self.source, self.results):
            folder.mkdir()
        intake.RESOURCES, VA.RECORDINGS, VA.SOURCE, VA.RESULTS = (
            self.resources, self.recordings, self.source, self.results)
        self.pins = (OLD, PIN)

    def tearDown(self):
        intake.RESOURCES, VA.RECORDINGS, VA.SOURCE, VA.RESULTS = self.originals
        for folder, _, _ in os.walk(self.root):
            os.chmod(folder, 0o700)
        shutil.rmtree(self.root)

    def dispositions(self):
        return self.results / ("%s-to-%s.dispositions.json" % self.pins)

    def dispose(self, identifiers):
        write(self.dispositions(), [{"finding": identifier, "decided_by": "invented decider",
                                     "decision": "invented decision", "where_recorded": "invented record"}
                                    for identifier in identifiers])

    def distribution(self, pin):
        """The committed 0.167.0 record, renamed to the table's facts for `pin`."""
        record = json.loads((RESOURCES / PIN / "CANONICAL_DISTRIBUTION.json").read_bytes())
        facts = intake.PINS[pin]
        record.update(pin=pin, source_commit=facts["source_commit"],
                      archive={key: facts[key] for key in ("url", "size", "sha256")},
                      package_metadata=dict(record["package_metadata"], version=pin))
        return record

    def bind(self, pin, archive=True):
        """Write the distribution and generation records that bind the folder's bundles and manifest."""
        folder = self.resources / pin
        record = self.distribution(pin)
        write(folder / "CANONICAL_DISTRIBUTION.json", record)
        entry = next(e for e in record["inventory"]["entries"] if e["path"] == "bin/codex")
        supplier = {"main_sha256": entry["sha256"]}
        if archive:
            supplier.update(tree_manifest_sha256=record["inventory"]["manifest_sha256"],
                            archive_sha256=record["archive"]["sha256"])
        write(folder / VA.GENERATION, {
            "pin": pin, "supplier": supplier, "manifest_sha256": sha((folder / VA.MANIFEST).read_bytes()),
            "compiled_experimental_bundles": {name: sha((folder / name).read_bytes())
                                              for name in (VA.BUNDLE, VA.V2_BUNDLE)}})

    def verdict(self, **arguments):
        return VA.compare(*self.pins, **arguments)["verdict"]["verdict"]


class CommittedResult(unittest.TestCase):
    def test_regenerating_the_committed_result_gives_the_same_bytes(self):
        self.assertEqual(VA.render(VA.compare(OLD, PIN)), COMMITTED.read_text(encoding="utf-8"))

    def test_the_committed_result_passed_with_each_finding_disposed_once_and_its_limits_named(self):
        result = json.loads(COMMITTED.read_text(encoding="utf-8"))
        self.assertEqual((result["verdict"]["verdict"], result["verdict"]["reasons"]), ("passed", []))
        self.assertEqual(sorted(e["finding"] for e in result["verdict"]["dispositions"]),
                         sorted(f["id"] for f in result["findings"]))
        states = {(row["pin"], row["binding"]): row["state"] for row in result["identity"]["bindings"]}
        self.assertEqual(sorted(key for key, state in states.items() if state != "bound"), sorted(VA.EXCEPTIONS))
        self.assertTrue(all(state == "bound" or state.startswith("not checked: ") for state in states.values()))


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

    def test_a_reordering_inside_a_longer_list_is_reported(self):
        """Round 3 finding 12: [a, b] to [b, a, c] is more than the addition of c."""
        differences = VA.diff_paths(["a", "b"], ["b", "a", "c"])
        self.assertIn({"path": "/2", "before": "<absent>", "after": "c"}, differences)
        self.assertGreater(len(differences), 1)
        rebuilt = ["a", "b"]
        for difference in sorted((d for d in differences if d["after"] == "<absent>"),
                                 key=lambda d: d["path"], reverse=True):
            del rebuilt[int(difference["path"][1:])]
        for difference in sorted((d for d in differences if d["before"] == "<absent>"), key=lambda d: d["path"]):
            rebuilt.insert(int(difference["path"][1:]), difference["after"])
        self.assertEqual(rebuilt, ["b", "a", "c"])

    def test_json_with_a_repeated_key_is_not_read(self):
        with self.assertRaises(ValueError):
            json.loads('{"a": 1, "a": 2}', object_pairs_hook=VA.no_repeated_key)


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


FLAG = {"type": "object", "properties": {"flag": {"type": "boolean"}}}


class Findings(InventedTree):
    """0.160.0 to 0.167.0 over a tiny invented protocol, with no recordings."""

    def setUp(self):
        super().setUp()
        self.write_pin(OLD, FLAG)
        self.write_pin(PIN, {"type": "object", "properties": {}})
        (self.source / "host.rs").write_text('fn read() { call("invented/read"); }\n')
        write(self.dispositions(), [])

    def write_pin(self, pin, inner):
        value, folder = bundle(inner), self.resources / pin
        write(folder / VA.BUNDLE, value)
        write(folder / VA.V2_BUNDLE, flat(value))
        (folder / VA.MANIFEST).write_text(
            "aa  json-schema/stable/v2/Inner.json\naa  json-schema/experimental/v2/Inner.json\n" + "".join(
                "%s  json-schema/experimental/%s\n" % (sha((folder / name).read_bytes()), name)
                for name in (VA.BUNDLE, VA.V2_BUNDLE)))
        if pin != OLD:
            self.bind(pin, archive=False)  # 0.167.0's generation record does not name the archive's tree

    def run_compare(self):
        return VA.compare(OLD, PIN, scenarios=())

    def pass_then(self):
        """Dispose the one finding so that the comparison passes; return a function that reruns it."""
        self.dispose([f["id"] for f in self.run_compare()["findings"]])
        self.assertEqual(self.run_compare()["verdict"]["verdict"], "passed")
        return self.run_compare

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
        self.pass_then()
        # The same definition changed differently: the decided identifier no longer applies.
        self.write_pin(PIN, {"type": "object", "properties": {"flag": {"type": "string"}}})
        result = self.run_compare()
        self.assertNotEqual(result["findings"][0]["id"], identifier)
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")
        self.assertEqual(result["verdict"]["dispositions_naming_no_finding"], [identifier])

    def test_any_change_to_a_relied_on_definition_is_a_finding_whatever_it_contains(self):
        for addition in (False, {"type": "string", "pattern": "^x"}, {"description": "words only"}):
            with self.subTest(addition=addition):
                self.write_pin(PIN, dict(FLAG, properties=dict(FLAG["properties"], invented=addition)))
                result = self.run_compare()
                self.assertEqual([f["subject"] for f in result["findings"]], ["v2/Inner"])
                self.assertEqual(result["verdict"]["verdict"], "returned for decision")

    def test_a_disposition_naming_no_finding_or_naming_one_twice_prevents_passing(self):
        identifier = self.run_compare()["findings"][0]["id"]
        self.dispose([identifier, "VA-does-not-exist"])
        verdict = self.run_compare()["verdict"]
        self.assertEqual((verdict["verdict"], verdict["dispositions_naming_no_finding"]),
                         ("returned for decision", ["VA-does-not-exist"]))
        # Round 3 finding 10: a second entry for one finding, here with a contrary decision.
        self.dispose([identifier, identifier])
        entries = json.loads(self.dispositions().read_text())
        entries[1]["decision"] = "Do not accept this change"
        write(self.dispositions(), entries)
        result = self.run_compare()
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")
        self.assertIn("two dispositions name the finding " + identifier,
                      [p["problem"] for p in result["inadmissible"]["missing_structure"]])

    def test_missing_and_empty_inputs_never_pass(self):
        rerun = self.pass_then()
        (self.resources / PIN / VA.MANIFEST).unlink()
        result = rerun()
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")
        self.assertEqual(len(result["inadmissible"]["missing_inputs"]), 1)
        for pin in (OLD, PIN):
            for name in (VA.BUNDLE, VA.V2_BUNDLE):
                write(self.resources / pin / name, {"definitions": {}})
            (self.resources / pin / VA.MANIFEST).write_text("")
            (self.resources / pin / VA.SUPPLEMENT).mkdir()
        (self.source / "host.rs").write_text("fn main() {}\n")
        problems = {(p["role"], p["problem"]) for p in self.run_compare()["inadmissible"]["missing_structure"]}
        for expected in [("generated schema bundle", "no v2 definitions"),
                         ("generated schema bundle", "no usable ClientRequest union (members naming their method)"),
                         ("generator output manifest", "lists no json-schema file in variant(s) experimental, stable"),
                         ("supplement at " + OLD, "present but not readable as a file (IsADirectoryError)"),
                         ("host source", "no protocol method of either pin appears in it as a string literal")]:
            self.assertIn(expected, problems)

    def test_host_source_that_is_not_read_in_full_never_passes(self):
        """Round 3 finding 5: an unreadable subtree made the relied-on set smaller, silently."""
        (self.source / "hidden").mkdir()
        (self.source / "hidden/more.rs").write_text('fn ask() { call("invented/ask"); }\n')
        self.assertEqual(sorted(self.run_compare()["relied_on"]["methods"]), ["invented/ask", "invented/read"])
        rerun = self.pass_then()
        if os.geteuid() != 0:
            os.chmod(self.source / "hidden", 0o000)
            result = rerun()
            os.chmod(self.source / "hidden", 0o700)
            self.assertEqual(result["verdict"]["verdict"], "returned for decision")
            self.assertIn(("host source", "a folder could not be listed (PermissionError)"),
                          {(p["role"], p["problem"]) for p in result["inadmissible"]["missing_structure"]})
        (self.source / "hidden/more.rs").write_bytes(b'fn ask() { call("invented/ask"); } // \xff\n')
        result = rerun()
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")
        self.assertIn("hidden/more.rs could not be read as UTF-8 text (UnicodeDecodeError)",
                      [p["problem"] for p in result["inadmissible"]["missing_structure"]])

    def test_a_reached_definition_that_refers_to_nothing_or_is_not_a_schema_cannot_be_disposed(self):
        """Round 3 finding 7: the same unusable definition at both pins, its change disposed."""
        for unusable, fragment in (({"$ref": "#/definitions/v2/MissingDefinition"}, "refers to"),
                                   ({"type": "not-a-type"}, "is not a valid schema")):
            with self.subTest(unusable=unusable):
                self.write_pin(OLD, dict(FLAG, properties={"invented": unusable}))
                self.write_pin(PIN, dict(FLAG, properties={"invented": unusable, "more": {"type": "string"}}))
                result = self.run_compare()
                self.dispose([f["id"] for f in result["findings"]])
                result = self.run_compare()
                self.assertEqual((result["verdict"]["verdict"], result["verdict"]["undisposed_findings"]),
                                 ("returned for decision", []))
                problems = [p["problem"] for p in result["inadmissible"]["missing_structure"]]
                self.assertTrue(any(fragment in problem for problem in problems), problems)

    def test_a_supplement_entry_must_name_its_own_pin_and_its_evidence(self):
        """Round 3 finding 11."""
        rerun = self.pass_then()
        good = [{"element": "invented/supplement", "pin": None, "evidence": "invented evidence"}]
        for pin in (OLD, PIN):
            write(self.resources / pin / VA.SUPPLEMENT, [dict(good[0], pin=pin)])
        self.assertEqual(rerun()["verdict"]["verdict"], "passed")
        for change in ({"pin": 7}, {"pin": OLD}, {"evidence": None}, {"evidence": " "}, {"element": ""}):
            with self.subTest(change=change):
                write(self.resources / PIN / VA.SUPPLEMENT, [dict(dict(good[0], pin=PIN), **change)])
                self.assertEqual(rerun()["verdict"]["verdict"], "returned for decision")

    def test_a_generated_basis_not_bound_to_its_pin_never_passes(self):
        """Round 3 finding 4, for the generated schema."""
        rerun, folder = self.pass_then(), self.resources / PIN
        generation = json.loads((folder / VA.GENERATION).read_text())
        manifest = (folder / VA.MANIFEST).read_text()
        cases = {
            "generation record names another pin": lambda: write(folder / VA.GENERATION, dict(generation, pin=NEXT)),
            "generation record names another manifest": lambda: write(
                folder / VA.GENERATION, dict(generation, manifest_sha256="0" * 64)),
            "generation record names another entrypoint": lambda: write(
                folder / VA.GENERATION, dict(generation, supplier={"main_sha256": "0" * 64})),
            "no generation record": lambda: (folder / VA.GENERATION).unlink(),
            "no distribution record": lambda: (folder / "CANONICAL_DISTRIBUTION.json").unlink(),
            "distribution record of another archive": lambda: write(
                folder / "CANONICAL_DISTRIBUTION.json", dict(self.distribution(PIN), source_commit="0" * 40)),
            "the prior pin's manifest": lambda: shutil.copyfile(self.resources / OLD / VA.MANIFEST,
                                                                folder / VA.MANIFEST),
            "manifest naming another bundle digest": lambda: (folder / VA.MANIFEST).write_text(
                manifest.replace(sha((folder / VA.BUNDLE).read_bytes()), "0" * 64)),
        }
        for name, change in cases.items():
            with self.subTest(name):
                self.write_pin(PIN, {"type": "object", "properties": {}})
                change()
                result = rerun()
                self.assertEqual((result["verdict"]["verdict"], result["verdict"]["undisposed_findings"]),
                                 ("returned for decision", []), name)
                self.assertTrue(result["inadmissible"]["identity"] or result["inadmissible"]["missing_inputs"], name)

    def test_only_the_bindings_the_table_excepts_are_listed_as_not_checked(self):
        rows = self.pass_then()()["identity"]["bindings"]
        self.assertEqual(sorted((row["pin"], row["binding"]) for row in rows if row["state"] != "bound"),
                         sorted(key for key in VA.EXCEPTIONS if key[1] != "recording to the distribution record"))
        # The same gap at a pin the table does not except for it is inadmissible, not a note.
        original = dict(VA.EXCEPTIONS)
        try:
            del VA.EXCEPTIONS[(PIN, "generation record to the distribution record's tree and archive")]
            result = self.run_compare()
        finally:
            VA.EXCEPTIONS.clear()
            VA.EXCEPTIONS.update(original)
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")
        self.assertEqual([p["state"] for p in result["inadmissible"]["identity"]], ["not bound"])

    def test_the_v2_bundle_is_compared_in_both_directions(self):
        main = json.loads((RESOURCES / PIN / VA.BUNDLE).read_text())
        v2 = json.loads((RESOURCES / PIN / VA.V2_BUNDLE).read_text())
        self.assertEqual(VA.v2_bundle_differences(VA.definitions(main), v2), [])
        del v2["definitions"]["ThreadItem"]
        self.assertEqual(VA.v2_bundle_differences(VA.definitions(main), v2), ["ThreadItem (absent from the v2 bundle)"])

    def test_a_pin_outside_the_table_or_without_inputs_is_refused_and_nothing_is_written(self):
        for pins, message in ((("9.9.9", PIN), "not a pin of the table"), ((OLD, "../0.167.0"), "not a pin of the table"),
                              ((PIN, OLD), "only as the pin advanced from"), ((PIN, PIN), "the same"),
                              ((PIN, NEXT), "unknown pin " + NEXT)):
            with self.subTest(pins=pins):
                with self.assertRaisesRegex(VA.Refused, message):
                    VA.compare(*pins)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            self.assertEqual(VA.main(["--from", PIN, "--to", NEXT]), 2)
            with self.assertRaises(SystemExit):
                VA.main(["--from", OLD, "--to", "9.9.9"])
        self.assertIn("unknown pin " + NEXT, stderr.getvalue())
        self.assertEqual([path.name for path in self.results.iterdir()], [self.dispositions().name])


class Evidence(InventedTree):
    """0.167.0 against 0.167.2, the second built here from 0.167.0's committed schemas and recordings under
    0.167.2's identity: it passes on evidence alone, and each defect of the evidence or of its binding
    prevents passing whatever is disposed."""

    def setUp(self):
        super().setUp()
        self.pins = (PIN, NEXT)
        shutil.copytree(RESOURCES / PIN, self.resources / PIN)
        shutil.copytree(RECORDINGS, self.recordings / PIN)
        (self.resources / NEXT).mkdir()
        for name in (VA.BUNDLE, VA.V2_BUNDLE, VA.MANIFEST):
            shutil.copyfile(RESOURCES / PIN / name, self.resources / NEXT / name)
        self.bind(NEXT)
        shutil.copytree(self.originals[2], self.source, dirs_exist_ok=True)
        self.records = {}
        for scenario in VA.SCENARIOS:
            record = json.loads((RECORDINGS / (scenario + ".recording.json")).read_text())
            record["pin"] = NEXT
            record["events"] = [dict(event, pin=NEXT) if event.get("event") == "begin" else event
                                for event in record["events"]]
            identity = record["version_identity"]
            identity["version_output"] = "codex-cli " + NEXT
            identity["distribution"]["archive_sha256"] = intake.PINS[NEXT]["sha256"]
            self.records[scenario] = record
        write(self.dispositions(), [])

    def run_compare(self, dispose_all=True):
        for scenario, record in self.records.items():
            write(self.recordings / NEXT / (scenario + ".recording.json"), record)
        result = VA.compare(PIN, NEXT)
        if dispose_all and result["findings"]:
            self.dispose([f["id"] for f in result["findings"]])
            result = VA.compare(PIN, NEXT)
        return result

    def frames(self, scenario, keep):
        """Keep some frames and count positions again, as a recording without them would."""
        kept, counted = [], {}
        for row in self.records[scenario]["frames"]:
            if keep(row):
                key = (row["generation"], row["direction"])
                counted[key] = counted.get(key, 0) + 1
                kept.append(dict(row, position=counted[key]))
        self.records[scenario]["frames"] = kept

    def assert_inadmissible(self, section, fragment):
        result = self.run_compare()
        self.assertEqual(result["verdict"]["verdict"], "returned for decision")
        self.assertEqual(result["verdict"]["undisposed_findings"], [])
        self.assertTrue(any(fragment in json.dumps(item) for item in result["inadmissible"][section]),
                        result["inadmissible"][section])

    def test_identical_schemas_and_healthy_bound_recordings_pass_with_nothing_to_dispose(self):
        result = self.run_compare(dispose_all=False)
        self.assertEqual((result["verdict"]["verdict"], result["findings"], result["verdict"]["reasons"]),
                         ("passed", [], []))
        self.assertEqual(result["schema"]["relied_on_and_reached"]["changed"], {})
        self.assertEqual({row["state"] for row in result["identity"]["bindings"] if row["pin"] == NEXT}, {"bound"})

    def test_a_recording_not_bound_to_the_pins_supplier_never_passes(self):
        """Round 3 finding 4: each of these passed with no finding and no reason."""
        cases = {
            "binary digest zeroed": lambda r: r["version_identity"].update(binary_sha256="0" * 64),
            "another version label": lambda r: r["version_identity"].update(version_output="codex-cli 0.160.0"),
            "no version identity": lambda r: r.pop("version_identity"),
            "another archive": lambda r: r["version_identity"]["distribution"].update(archive_sha256="0" * 64),
            "another tree": lambda r: r["version_identity"]["distribution"].update(inventory_manifest_sha256="0" * 64),
        }
        for name, change in cases.items():
            with self.subTest(name):
                self.tearDown()
                self.setUp()
                change(self.records["st5"])
                self.assert_inadmissible("identity", "st5")
        self.tearDown()
        self.setUp()
        self.records["nv04"]["events"][0]["pin"] = "0.160.0"
        self.assert_inadmissible("missing_structure", "the begin event names another pin")

    def test_frames_out_of_order_or_with_a_gap_never_pass(self):
        """Round 3 finding 6: generation 2 before generation 1, a deleted frame, positions of -1."""
        def reordered(frames):
            return [row for row in frames if row["generation"] == 2] + [row for row in frames if row["generation"] == 1]

        def gap(frames):
            first = next(i for i, row in enumerate(frames) if row["direction"] == "codex->app"
                         and "id" not in row["frame"])
            return frames[:first] + frames[first + 1:]
        cases = [("come after frames of generation", reordered), ("do not count from 1 without a gap", gap),
                 ("do not count from 1 without a gap", lambda frames: [dict(row, position=-1) for row in frames]),
                 ("not a counting number", lambda frames: [dict(row, position=True) for row in frames]),
                 ("not a counting number", lambda frames: [dict(row, generation="1") for row in frames])]
        for fragment, change in cases:
            with self.subTest(fragment):
                self.tearDown()
                self.setUp()
                self.records["nv04"]["frames"] = change(self.records["nv04"]["frames"])
                self.assert_inadmissible("missing_structure", fragment)

    def test_history_reads_that_carry_nothing_never_pass(self):
        """Round 3 finding 6: every nv04 history result replaced by an empty object, its findings disposed."""
        asked = {(row["generation"], row["frame"]["id"]) for row in self.records["nv04"]["frames"]
                 if row["direction"] == "app->codex"
                 and row["frame"].get("method") in ("thread/read", "thread/turns/list", "thread/items/list")}
        for row in self.records["nv04"]["frames"]:
            if row["direction"] == "codex->app" and "method" not in row["frame"] \
                    and (row["generation"], row["frame"].get("id")) in asked:
                row["frame"]["result"] = {}
        self.assert_inadmissible("mechanisms_not_observed", "every_history_read_carries_the_spawn_item")

    def test_an_unhealthy_socket_watch_never_passes(self):
        cases = {
            "failed_samples present and zero": lambda w: w.update(failed_samples=1),
            "samples an integer greater than zero": lambda w: w.update(samples=0),
            "samples_by_generation of at least one": lambda w: w["samples_by_generation"].pop("2"),
            "summing to samples": lambda w: w.update(samples=1),
            "naming exactly generation(s)": lambda w: w["samples_by_generation"].update({"3": 1}),
            "non_loopback_peers present and empty": lambda w: w.update(non_loopback_peers=["192.0.2.1"]),
            "loopback_peers only 127.0.0.1 or ::1": lambda w: w.update(loopback_peers=["10.0.0.1"]),
        }
        for fragment, change in cases.items():
            with self.subTest(fragment):
                self.tearDown()
                self.setUp()
                change(self.records["st5"]["socket_watch"])
                self.assert_inadmissible("recording_admission", fragment)
        with self.subTest("no report"):
            self.tearDown()
            self.setUp()
            del self.records["nv04"]["socket_watch"]
            self.assert_inadmissible("recording_admission", "a socket_watch report")

    def test_a_missing_script_step_in_any_generation_never_passes(self):
        removed = [row["frame"]["id"] for row in self.records["nv04"]["frames"] if row["generation"] == 2
                   and row["frame"].get("method") == "thread/items/list"]
        self.frames("nv04", lambda row: not (row["generation"] == 2 and row["frame"].get("id") in removed))
        self.assert_inadmissible("recording_admission", "generation 2: App request thread/items/list with its result")

    def test_a_new_pin_recording_of_the_older_format_never_passes(self):
        self.records["st5"]["format"] = VA.OLDER
        self.records["st5"].pop("pin")
        self.assert_inadmissible("recording_admission", "the current recording format")

    def test_a_validation_failure_at_the_new_pin_never_passes(self):
        for row in self.records["st5"]["frames"]:
            if row["frame"].get("method") == "turn/started":
                row["frame"]["params"] = {"invented": True}
        self.assert_inadmissible("validation_failures", "turn/started")

    def test_an_expected_mechanism_not_observed_never_passes(self):
        # st5 freezes the supplier before the answer is written, so an acknowledgment after it is not expected.
        frames = self.records["st5"]["frames"]
        answer = next(i for i, row in enumerate(frames) if row["direction"] == "app->codex"
                      and "method" not in row["frame"] and row["generation"] == 1)
        frames.insert(answer + 1, dict(frames[answer], direction="codex->app", frame={
            "method": "serverRequest/resolved", "params": {"threadId": "t", "requestId": 0}}))
        self.frames("st5", lambda row: True)
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
