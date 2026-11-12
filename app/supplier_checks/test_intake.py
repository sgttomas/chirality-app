#!/usr/bin/env python3
"""Checks of archive intake and of the generator run, on invented archives and an invented generator.

No supplier is executed and nothing is fetched.

Run from `app/`: python3 supplier_checks/test_intake.py
"""
import hashlib
import io
import json
import os
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

import capture
import intake

PIN = "9.9.9"
URL = "https://example.invalid/package.tar.gz"
COMMIT = "0" * 40


def member(name, data=b"", mode=0o644, kind=tarfile.REGTYPE, link=""):
    info = tarfile.TarInfo(name)
    info.type, info.mode, info.size, info.linkname = kind, mode, len(data), link
    return info, data


def plain_members():
    return [member("bin", mode=0o755, kind=tarfile.DIRTYPE), member("bin/codex", b"\xcf\xfa\xed\xfe main", 0o755),
            member("codex-path", mode=0o755, kind=tarfile.DIRTYPE),
            member("codex-package.json", json.dumps({"version": PIN, "entrypoint": "bin/codex",
                                                     "pathDir": "codex-path"}).encode())]


class ArchiveIntake(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.TemporaryDirectory()
        self.base = Path(os.path.realpath(self.root.name))

    def tearDown(self):
        self.root.cleanup()

    def archive(self, members):
        path = self.base / "package.tar.gz"
        with tarfile.open(path, "w:gz") as tar:
            for info, data in members:
                tar.addfile(info, io.BytesIO(data))
        return path, path.stat().st_size, hashlib.sha256(path.read_bytes()).hexdigest()

    def take(self, members, size=None, digest=None, pin=PIN):
        path, actual_size, actual_digest = self.archive(members)
        facts = {"url": URL, "size": actual_size if size is None else size, "sha256": digest or actual_digest,
                 "source_commit": COMMIT}
        return intake.take_archive(str(path), facts, pin, str(self.base / "out"))

    def test_record_inventories_every_member_and_the_tree_then_verifies_against_it(self):
        record = self.take(plain_members())
        self.assertEqual((record["pin"], record["files"], record["macho_files"]), (PIN, 2, 1))
        self.assertEqual([(e["path"], e["kind"], e["mode"]) for e in record["inventory"]["entries"]],
                         [("bin", "dir", 0o755), ("bin/codex", "file", 0o755), ("codex-package.json", "file", 0o644),
                          ("codex-path", "dir", 0o755)])
        self.assertEqual((record["source_commit"], record["archive"]["url"]), (COMMIT, URL))
        written = json.loads((self.base / "out/CANONICAL_DISTRIBUTION.json").read_bytes())
        self.assertEqual(written, record)
        self.assertEqual(sorted(path.name for path in (self.base / "out").iterdir()),
                         ["CANONICAL_DISTRIBUTION.json", "vendor"])
        vendor = self.base / "out/vendor"
        binary, _ = capture.verified_vendor(str(vendor), record)
        self.assertEqual(binary, str(vendor / "bin/codex"))
        (vendor / "bin/codex").write_bytes(b"changed")
        with self.assertRaisesRegex(capture.Refused, "content: bin/codex"):
            capture.verified_vendor(str(vendor), record)

    def test_size_or_digest_other_than_published_refuses_before_extraction(self):
        with self.assertRaisesRegex(intake.Refused, "bytes, not the published"):
            self.take(plain_members(), size=1)
        with self.assertRaisesRegex(intake.Refused, "not the published one"):
            self.take(plain_members(), digest="0" * 64)
        self.assertFalse((self.base / "out").exists())

    def test_links_special_members_escaping_paths_and_repeats_refuse(self):
        cases = {
            "symbolic link": member("bin/link", kind=tarfile.SYMTYPE, link="codex"),
            "hard link": member("bin/hard", kind=tarfile.LNKTYPE, link="bin/codex"),
            "device": member("bin/device", kind=tarfile.CHRTYPE),
            "parent path": member("../outside", b"x"),
            "absolute path": member("/outside", b"x"),
            "repeated member": member("./bin/codex", b"again", 0o755),
        }
        for name, extra in cases.items():
            with self.subTest(name):
                self.tearDown()
                self.setUp()
                with self.assertRaises(intake.Refused):
                    self.take(plain_members() + [extra])
                self.assertFalse((self.base / "outside").exists())
                self.assertFalse((self.base / "out").exists())

    def test_no_path_is_built_from_the_pin(self):
        # A pin is compared with the metadata and recorded; whatever it says, every file lands in `out`.
        pin = "../../escaped"
        members = plain_members()[:3] + [member("codex-package.json", json.dumps(
            {"version": pin, "entrypoint": "bin/codex", "pathDir": "codex-path"}).encode())]
        self.assertEqual(self.take(members, pin=pin)["pin"], pin)
        self.assertEqual(sorted(path.name for path in self.base.iterdir()), ["out", "package.tar.gz"])
        self.assertEqual(sorted(path.name for path in (self.base / "out").iterdir()),
                         ["CANONICAL_DISTRIBUTION.json", "vendor"])

    def test_the_command_takes_only_a_pin_of_the_table_and_that_pins_archive(self):
        path, _, _ = self.archive(plain_members())
        with self.assertRaisesRegex(intake.Refused, "not a pin of the table"):
            intake.take_in(str(path), "../../escaped", str(self.base / "out"))
        with self.assertRaisesRegex(intake.Refused, "not a pin of the table"):
            intake.take_in(str(path), PIN, str(self.base / "out"))
        pin = sorted(capture.PINS)[0]
        self.assertEqual(intake.main(["--archive", str(path), "--pin", pin, "--out", str(self.base / "out")]), 2)
        self.assertFalse((self.base / "out").exists())

    def test_metadata_may_name_only_members_of_the_inventory(self):
        for field, value in (("entrypoint", "../not-in-inventory"), ("entrypoint", "/bin/sh"),
                             ("entrypoint", "bin/absent"), ("entrypoint", "bin"), ("entrypoint", "bin/./codex"),
                             ("pathDir", "bin/codex"), ("pathDir", ".."), ("execServer", "../outside"),
                             ("resourcesDir", "codex-package.json")):
            with self.subTest(field=field, value=value):
                self.tearDown()
                self.setUp()
                members = plain_members()[:2] + [member("codex-path", mode=0o755, kind=tarfile.DIRTYPE)]
                metadata = {"version": PIN, "entrypoint": "bin/codex", "pathDir": "codex-path"}
                metadata[field] = value
                with self.assertRaisesRegex(intake.Refused, "not a (file|dir) of the verified inventory"):
                    self.take(members + [member("codex-package.json", json.dumps(metadata).encode())])
                self.assertFalse((self.base / "out").exists())

    def test_a_refused_intake_removes_unwritable_extracted_directories(self):
        members = [member("bin", mode=0o555, kind=tarfile.DIRTYPE), member("bin/codex", b"main", 0o755),
                   member("codex-package.json", json.dumps({"version": "0.0.1"}).encode())]
        with self.assertRaises(intake.Refused):
            self.take(members)
        self.assertFalse((self.base / "out").exists())

    def test_metadata_naming_another_version_refuses(self):
        with self.assertRaisesRegex(intake.Refused, "not 9.9.8"):
            self.take(plain_members(), pin="9.9.8")
        self.assertFalse((self.base / "out").exists())

    def test_an_existing_output_directory_is_never_reused(self):
        (self.base / "out").mkdir()
        path, size, digest = self.archive(plain_members())
        with self.assertRaises(FileExistsError):
            intake.take_archive(str(path), {"url": URL, "size": size, "sha256": digest, "source_commit": COMMIT},
                                PIN, str(self.base / "out"))
        self.assertEqual(list((self.base / "out").iterdir()), [])


GENERATOR = r'''#!%(python)s
"""An invented stand-in for the supplier's schema generator, for intake's own tests. Not Codex."""
import os, sys, time
MODE = %(mode)r
time.sleep(0.4)
if MODE == "fails":
    sys.exit(3)
out = sys.argv[sys.argv.index("--out") + 1]
os.makedirs(out)
if MODE != "writes-nothing":
    for name in ("codex_app_server_protocol.schemas.json", "codex_app_server_protocol.v2.schemas.json"):
        with open(os.path.join(out, name), "w") as handle:
            handle.write("{}")
'''


class GeneratorRun(unittest.TestCase):
    """What a generation refuses to record, against an invented generator."""

    def setUp(self):
        self.root = tempfile.TemporaryDirectory()
        self.base = Path(os.path.realpath(self.root.name))
        self.originals = (capture.socket_rows, tempfile.tempdir)
        capture.socket_rows = lambda group: []  # the stand-in opens no socket; lsof is tested in test_capture

    def tearDown(self):
        capture.socket_rows, tempfile.tempdir = self.originals
        self.root.cleanup()

    def generate(self, mode):
        vendor = self.base / "vendor"
        (vendor / "bin").mkdir(parents=True)
        (vendor / "codex-path").mkdir()
        (vendor / "bin/codex").write_text(GENERATOR % {"python": sys.executable, "mode": mode})
        os.chmod(vendor / "bin/codex", 0o755)
        (vendor / "codex-package.json").write_text(json.dumps(
            {"version": PIN, "entrypoint": "bin/codex", "pathDir": "codex-path"}))
        record = intake.distribution_record(str(vendor), PIN, {"url": URL, "size": 1, "sha256": "0" * 64,
                                                               "source_commit": COMMIT})
        (self.base / "out").mkdir()
        return intake.generate(str(vendor), record, str(self.base / "out"))

    def test_a_complete_generation_records_its_samples_environment_and_the_checks_made(self):
        generation = self.generate("complete")
        self.assertEqual(generation["environment"]["allowlist"], ["CODEX_HOME", "HOME", "LANG", "PATH", "TMPDIR", "TZ"])
        self.assertEqual(generation["environment"]["outside_configuration"]["system_configuration_folder"], "absent")
        for variant in generation["variants"].values():
            self.assertGreater(variant["socket_samples"], 0)
        self.assertEqual(sorted(path.name for path in (self.base / "out").iterdir()),
                         ["GENERATION.json", "MANIFEST.sha256"] + sorted(intake.BUNDLES))

    def test_a_failed_sample_a_socket_a_failing_generator_or_no_output_writes_no_generation(self):
        row = "codex 1 1 u 9u IPv4 0x0 0t0 TCP 127.0.0.1:50000 (LISTEN)"
        for mode, rows, expected in (("complete", None, "could not take a sample"),
                                     ("complete", [row], "opened a socket"),
                                     ("fails", [], "exited with 3"),
                                     ("writes-nothing", [], "wrote 0 files")):
            with self.subTest(mode=mode, rows=rows):
                self.tearDown()
                self.setUp()
                capture.socket_rows = lambda group: rows
                with self.assertRaisesRegex(intake.Refused, expected):
                    self.generate(mode)
                self.assertEqual(list((self.base / "out").iterdir()), [])

    def test_scratch_beneath_a_project_refuses_before_the_generator_runs(self):
        (self.base / "project/.codex").mkdir(parents=True)
        (self.base / "project/tmp").mkdir()
        tempfile.tempdir = str(self.base / "project/tmp")
        with self.assertRaisesRegex(intake.Refused, "holds a .codex entry"):
            self.generate("complete")
        self.assertEqual(list((self.base / "out").iterdir()), [])
        self.assertEqual(list((self.base / "project/tmp").iterdir()), [])


if __name__ == "__main__":
    unittest.main()
