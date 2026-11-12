#!/usr/bin/env python3
"""Checks of the same-basis check on invented pins. No supplier is executed and nothing is fetched.

The new pin's records are made here by intake.py itself, run against an invented generator, so
that what the check admits is what intake.py writes. Run from `app/`:
python3 supplier_checks/test_same_basis.py
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import intake
import same_basis

OLD, NEW = "9.9.8", "9.9.9"
GENERATOR = r'''#!%(python)s
"""An invented stand-in for the supplier's schema generator, for the same-basis tests. Not Codex."""
import os, sys, time
time.sleep(0.3)
out = sys.argv[sys.argv.index("--out") + 1]
os.makedirs(out)
for name in ("codex_app_server_protocol.schemas.json", "codex_app_server_protocol.v2.schemas.json", "Other.json"):
    with open(os.path.join(out, name), "w") as handle:
        handle.write('{"invented": "%%s"}' %% name)
'''


def facts(pin):
    return {"url": "https://example.invalid/%s.tar.gz" % pin, "size": 1, "sha256": hashlib.sha256(pin.encode()).hexdigest(),
            "source_commit": "0" * 40}


class SameBasis(unittest.TestCase):
    made = None

    @classmethod
    def setUpClass(cls):
        """Make the new pin's folder once, with intake.py, and keep it to copy from."""
        cls.kept = Path(os.path.realpath(tempfile.mkdtemp()))
        cls.pins, intake.PINS = intake.PINS, {OLD: facts(OLD), NEW: facts(NEW)}
        cls.rows, intake.socket_rows = intake.socket_rows, lambda group: []  # the stand-in opens no socket
        vendor, out = cls.kept / "vendor", cls.kept / NEW
        (vendor / "bin").mkdir(parents=True)
        (vendor / "codex-path").mkdir()
        (vendor / "bin/codex").write_text(GENERATOR % {"python": sys.executable})
        os.chmod(vendor / "bin/codex", 0o755)
        (vendor / "codex-package.json").write_text(json.dumps(
            {"version": NEW, "entrypoint": "bin/codex", "pathDir": "codex-path"}))
        record = intake.distribution_record(str(vendor), NEW, intake.PINS[NEW])
        out.mkdir()
        intake.write_json(str(out / "CANONICAL_DISTRIBUTION.json"), record)
        intake.generate(str(vendor), record, str(out))

    @classmethod
    def tearDownClass(cls):
        intake.PINS, intake.socket_rows = cls.pins, cls.rows
        shutil.rmtree(cls.kept)

    def setUp(self):
        self.root = Path(os.path.realpath(tempfile.mkdtemp()))
        self.originals = (intake.RESOURCES, same_basis.RESULTS, same_basis.ANALYSIS)
        self.resources, self.results = self.root / "resources", self.root / "results"
        shutil.copytree(self.kept / NEW, self.resources / NEW)
        (self.resources / OLD).mkdir()
        for name in same_basis.GENERATED:
            shutil.copyfile(self.kept / NEW / name, self.resources / OLD / name)
        self.results.mkdir()
        for name in ("analysis.json", "analysis.dispositions.json"):
            (self.results / name).write_text("invented " + name)
        intake.RESOURCES, same_basis.RESULTS = self.resources, self.results
        same_basis.ANALYSIS = {OLD: ("analysis.json", "analysis.dispositions.json")}

    def tearDown(self):
        intake.RESOURCES, same_basis.RESULTS, same_basis.ANALYSIS = self.originals
        shutil.rmtree(self.root)

    def record(self, name):
        """The good record, as intake.py wrote it; each case changes a fresh copy."""
        return json.loads((self.kept / NEW / name).read_text())

    def write(self, name, value):
        (self.resources / NEW / name).write_text(json.dumps(value))

    def refused(self, message):
        return self.assertRaisesRegex(same_basis.Refused, message)

    def test_what_intake_writes_for_an_identical_basis_is_admitted_and_the_result_says_what_it_is(self):
        result = same_basis.compare(OLD, NEW)
        self.assertEqual(result["result"], "admitted on the same generated basis")
        self.assertEqual(sorted(result["generated_files_equal_byte_for_byte"]), sorted(same_basis.GENERATED))
        self.assertEqual(sorted(result["admitted_whole"]), ["CANONICAL_DISTRIBUTION.json", "GENERATION.json"])
        self.assertTrue(any("behaves the same" in limit for limit in result["does_not_establish"]))
        self.assertEqual(result["consumer_analysis_that_carries_over"]["analysis.json"],
                         hashlib.sha256(b"invented analysis.json").hexdigest())

    def test_a_generated_file_that_differs_or_cannot_be_read_refuses(self):
        for name in same_basis.GENERATED:
            with self.subTest(name=name):
                self.tearDown()
                self.setUp()
                path = self.resources / OLD / name
                path.write_bytes(path.read_bytes() + b"\n")
                with self.refused("a changed schema needs a full comparison"):
                    same_basis.compare(OLD, NEW)
                path.unlink()
                with self.refused("could not be read"):
                    same_basis.compare(OLD, NEW)
                os.symlink(self.resources / NEW / name, path)
                with self.refused("not a regular file"):
                    same_basis.compare(OLD, NEW)

    def test_pins_outside_the_table_without_inputs_or_without_an_analysis_refuse(self):
        for pins, message in ((("9.9.7", NEW), "not a pin of the table"), ((OLD, "../" + NEW), "not a pin of the table"),
                              ((OLD, OLD), "the same"), ((NEW, OLD), "no consumer analysis is kept")):
            with self.subTest(pins=pins):
                with self.refused(message):
                    same_basis.compare(*pins)
        (self.results / "analysis.json").unlink()
        with self.refused("could not be read"):
            same_basis.compare(OLD, NEW)
        shutil.rmtree(self.resources / OLD)
        with self.refused("holds no generated schema for " + OLD):
            same_basis.compare(OLD, NEW)

    def test_a_supplement_at_either_pin_refuses(self):
        for pin in (OLD, NEW):
            for content in ("[]", "null"):
                with self.subTest(pin=pin, content=content):
                    self.tearDown()
                    self.setUp()
                    (self.resources / pin / same_basis.SUPPLEMENT).write_text(content)
                    with self.refused("supplements are not handled"):
                        same_basis.compare(OLD, NEW)

    def test_a_distribution_record_with_one_wrong_value_refuses(self):
        def entry(record, path):
            return next(e for e in record["inventory"]["entries"] if e["path"] == path)
        changes = {
            "another pin": lambda r: r.update(pin=OLD),
            "another format": lambda r: r.update(format="bad"),
            "another source commit": lambda r: r.update(source_commit="1" * 40),
            "another archive digest": lambda r: r["archive"].update(sha256="0" * 64),
            "an extra key": lambda r: r.update(generator_join="invented"),
            "a missing key": lambda r: r.pop("limits"),
            "file count zero": lambda r: r.update(files=0),
            "macho count above the files": lambda r: r.update(macho_files=99),
            "entrypoint of kind dir": lambda r: entry(r, "bin/codex").update(kind="dir"),
            "an entry's digest zeroed": lambda r: entry(r, "codex-package.json").update(sha256="0" * 64),
            "an entry's digest missing": lambda r: entry(r, "codex-package.json").pop("sha256"),
            "inventory digest null": lambda r: r["inventory"].update(manifest_sha256=None),
            "inventory digest missing": lambda r: r["inventory"].pop("manifest_sha256"),
            "no entries": lambda r: r["inventory"].update(entries=[]),
            "entries null": lambda r: r["inventory"].update(entries=None),
            "inventory an empty object": lambda r: r.update(inventory={}),
            "an entry repeated": lambda r: r["inventory"]["entries"].append(dict(r["inventory"]["entries"][-1])),
            "an entry out of order": lambda r: r["inventory"]["entries"].reverse(),
            "an entry outside a listed directory": lambda r: r["inventory"]["entries"].pop(0),
            "a path that climbs": lambda r: entry(r, "codex-path").update(path="../codex-path"),
            "a mode that is not a mode": lambda r: entry(r, "bin").update(mode=True),
            "metadata of another pin": lambda r: r["package_metadata"].update(version=OLD),
            "metadata entrypoint outside the inventory": lambda r: r["package_metadata"].update(entrypoint="../x"),
            "limits empty": lambda r: r.update(limits=[]),
        }
        for name, change in changes.items():
            with self.subTest(name):
                record = self.record("CANONICAL_DISTRIBUTION.json")
                change(record)
                self.write("CANONICAL_DISTRIBUTION.json", record)
                with self.assertRaises(same_basis.Refused, msg=name):
                    same_basis.compare(OLD, NEW)
        good = (self.kept / NEW / "CANONICAL_DISTRIBUTION.json").read_text()
        repeated = good.replace('"pin": "%s"' % NEW, '"pin": "0.0.0",\n "pin": "%s"' % NEW, 1)
        self.assertNotEqual(repeated, good)
        (self.resources / NEW / "CANONICAL_DISTRIBUTION.json").write_text(repeated)
        with self.refused("repeated key"):
            same_basis.compare(OLD, NEW)
        (self.resources / NEW / "CANONICAL_DISTRIBUTION.json").write_text(good)
        same_basis.compare(OLD, NEW)

    def test_a_generation_record_with_one_wrong_value_refuses(self):
        changes = {
            "another pin": lambda g: g.update(pin=OLD),
            "another format": lambda g: g.update(format="bad"),
            "an extra key": lambda g: g.update(official_release={}),
            "exit code 7": lambda g: g["variants"]["experimental"].update(exit_code=7),
            "exit code false": lambda g: g["variants"]["stable"].update(exit_code=False),
            "no socket samples": lambda g: g["variants"]["experimental"].update(socket_samples=0),
            "a failed sample": lambda g: g["variants"]["stable"].update(failed_samples=1),
            "a socket seen": lambda g: g["variants"]["experimental"].update(sockets_seen=1),
            "variants empty": lambda g: g.update(variants={}),
            "variants null": lambda g: g.update(variants=None),
            "a variant's file count wrong": lambda g: g["variants"]["stable"].update(files=1),
            "a variant's manifest digest wrong": lambda g: g["variants"]["experimental"].update(manifest_sha256="0" * 64),
            "a variant run with another command": lambda g: g["variants"]["stable"]["argv"].append("--experimental"),
            "another archive": lambda g: g["supplier"].update(archive_sha256="0" * 64),
            "archive digest missing": lambda g: g["supplier"].pop("archive_sha256"),
            "another entrypoint": lambda g: g["supplier"].update(main_sha256="0" * 64),
            "tree digest null": lambda g: g["supplier"].update(tree_manifest_sha256=None),
            "another source": lambda g: g["supplier"].update(source="retained installed npm package"),
            "another manifest": lambda g: g.update(manifest_sha256="0" * 64),
            "another bundle digest": lambda g: g["compiled_experimental_bundles"].update(
                {intake.BUNDLES[0]: "0" * 64}),
            "a third bundle": lambda g: g["compiled_experimental_bundles"].update({"Other.json": "0" * 64}),
            "environment inherited": lambda g: g["environment"].update(inherit_environment=True),
            "five variables": lambda g: g["environment"]["allowlist"].remove("TZ"),
            "system configuration present": lambda g: g["environment"]["outside_configuration"].update(
                system_configuration_folder="present"),
            "managed preferences not checked": lambda g: g["environment"]["outside_configuration"].update(
                managed_preferences="not checked: the supplier reads managed preferences on macOS only"),
            "no outside-configuration checks": lambda g: g["environment"].pop("outside_configuration"),
        }
        for name, change in changes.items():
            with self.subTest(name):
                generation = self.record("GENERATION.json")
                change(generation)
                self.write("GENERATION.json", generation)
                with self.assertRaises(same_basis.Refused, msg=name):
                    same_basis.compare(OLD, NEW)

    def test_a_manifest_not_read_whole_or_naming_a_file_twice_refuses(self):
        """The manifest must be equal at both pins, so each change is made to both and to the record's digest."""
        good = (self.kept / NEW / same_basis.MANIFEST).read_text()
        first = good.split("\n")[0]
        cases = {
            "names a file twice": first.replace(first[:64], "0" * 64) + "\n" + good,
            "not a digest and a json-schema path": "not a row\n" + good,
            "not a digest and a json-schema path ": good.replace(first[:64], "ZZ" + first[2:64], 1),
            "does not end with a line end": good.rstrip("\n"),
            "experimental rows followed by the stable rows": "".join(reversed(good.splitlines(keepends=True))),
            "does not name the digest of the compiled bundle": "\n".join(
                line for line in good.split("\n") if intake.BUNDLES[0] not in line or "/stable/" in line),
        }
        for message, text in cases.items():
            with self.subTest(message):
                for pin in (OLD, NEW):
                    (self.resources / pin / same_basis.MANIFEST).write_text(text)
                generation = json.loads((self.kept / NEW / "GENERATION.json").read_text())
                generation["manifest_sha256"] = hashlib.sha256(text.encode()).hexdigest()
                self.write("GENERATION.json", generation)
                with self.refused(message.strip()):
                    same_basis.compare(OLD, NEW)

    def test_the_command_writes_the_result_only_when_admitted(self):
        self.assertEqual(same_basis.main(["--from", OLD, "--to", NEW]), 0)
        written = self.results / ("%s-to-%s.json" % (OLD, NEW))
        self.assertEqual(written.read_text(), same_basis.render(same_basis.compare(OLD, NEW)))
        written.unlink()
        generation = self.record("GENERATION.json")
        generation["variants"]["stable"]["exit_code"] = 7
        self.write("GENERATION.json", generation)
        self.assertEqual(same_basis.main(["--from", OLD, "--to", NEW]), 2)
        self.assertFalse(written.exists())


if __name__ == "__main__":
    unittest.main()
