#!/usr/bin/env python3
"""Checks of archive intake and of the generator run, on invented archives and an invented generator.

No supplier is executed and nothing is fetched.

Run from `app/`: python3 supplier_checks/test_intake.py
"""
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import types
import unittest
from pathlib import Path

import intake

PIN = "9.9.9"
COMMITTED = "0.167.0"  # the pin whose distribution record the repository keeps
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
        binary, _ = intake.verified_vendor(str(vendor), record)
        self.assertEqual(binary, str(vendor / "bin/codex"))
        (vendor / "bin/codex").write_bytes(b"changed")
        with self.assertRaisesRegex(intake.Refused, "content: bin/codex"):
            intake.verified_vendor(str(vendor), record)

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
        pin = sorted(intake.PINS)[0]
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
        return intake.vendor_differences(str(self.vendor), self.inventory)

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

    def test_a_pin_is_admitted_only_as_a_key_of_the_table(self):
        for pin in ("../../escaped", "0.167.0/..", "/0.167.0", "0.167", "", "0.167.0\n", "9.9.9", None, 7):
            with self.subTest(pin=pin):
                with self.assertRaisesRegex(intake.Refused, "not a pin of the table"):
                    intake.expected_distribution(pin)
        self.assertEqual(intake.expected_distribution(COMMITTED)["pin"], COMMITTED)
        # Every pin the repository keeps a distribution record for is in the table and is admitted.
        kept = sorted(path.parent.name for path in intake.RESOURCES.glob("*/CANONICAL_DISTRIBUTION.json"))
        self.assertIn(COMMITTED, kept)
        for pin in kept:
            self.assertEqual(intake.expected_distribution(pin)["archive"]["sha256"], intake.PINS[pin]["sha256"])

    def test_a_record_that_is_absent_or_names_another_archive_refuses(self):
        committed = intake.expected_distribution(COMMITTED)
        original, intake.RESOURCES = intake.RESOURCES, Path(self.root.name) / "records"
        try:
            with self.assertRaisesRegex(intake.Refused, "no expected distribution"):
                intake.expected_distribution(COMMITTED)
            (intake.RESOURCES / COMMITTED).mkdir(parents=True)
            for field, value in (("pin", "0.167.2"), ("source_commit", "0" * 40), ("archive", None),
                                 ("archive", dict(committed["archive"], sha256="0" * 64)),
                                 ("archive", dict(committed["archive"], size=1)),
                                 ("package_metadata", {"version": "0.167.2"})):
                with self.subTest(field=field, value=value):
                    (intake.RESOURCES / COMMITTED / "CANONICAL_DISTRIBUTION.json").write_text(
                        json.dumps(dict(committed, **{field: value})))
                    with self.assertRaisesRegex(intake.Refused, "does not name the table's pin and archive"):
                        intake.expected_distribution(COMMITTED)
            (intake.RESOURCES / COMMITTED / "CANONICAL_DISTRIBUTION.json").write_text("[]")
            with self.assertRaisesRegex(intake.Refused, "does not name the table's pin and archive"):
                intake.expected_distribution(COMMITTED)
        finally:
            intake.RESOURCES = original

    def test_a_differing_tree_refuses_without_executing(self):
        with self.assertRaisesRegex(intake.Refused, "differs from the expected 0.167.0 inventory"):
            intake.verified_vendor(str(self.vendor), intake.expected_distribution(COMMITTED))


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
        self.assertEqual(intake.metadata_members(self.record), {"entrypoint": "bin/codex", "pathDir": "codex-path"})
        for field, value in (("entrypoint", "../not-in-inventory"), ("entrypoint", "/bin/sh"), ("entrypoint", "bin"),
                             ("entrypoint", "bin/absent"), ("entrypoint", "bin/../bin/codex"), ("entrypoint", ""),
                             ("entrypoint", None), ("entrypoint", 7), ("pathDir", "bin/codex"), ("pathDir", "."),
                             ("pathDir", ".."), ("execServer", "../not-in-inventory"), ("resourcesDir", "bin/codex"),
                             ("pathDir", "search:/outside"), ("entrypoint", "bin/co:dex")):
            with self.subTest(field=field, value=value):
                record = json.loads(json.dumps(self.record))
                record["package_metadata"][field] = value
                # Even as a genuine inventory member, a name holding the path separator is refused.
                record["inventory"]["entries"].append(
                    {"path": value, "kind": "dir" if field == "pathDir" else "file", "mode": 0o755,
                     "size": 0, "sha256": hashlib.sha256(b"").hexdigest()} if isinstance(value, str) and ":" in value
                    else {"path": "unused", "kind": "dir", "mode": 0o755})
                with self.assertRaisesRegex(intake.Refused, "of the verified inventory"):
                    intake.metadata_members(record)
                with self.assertRaises(intake.Refused):
                    intake.admitted_path(str(self.vendor), record, "entrypoint")

    def test_an_entrypoint_that_is_not_executable_in_the_inventory_refuses(self):
        self.record["inventory"]["entries"][1]["mode"] = 0o644
        with self.assertRaisesRegex(intake.Refused, "not executable"):
            intake.metadata_members(self.record)

    def test_the_path_is_admitted_again_at_the_moment_of_use(self):
        binary = intake.admitted_path(str(self.vendor), self.record, "entrypoint")
        self.assertEqual(binary, str(self.vendor / "bin/codex"))
        (self.vendor / "bin/codex").write_bytes(b"other")
        with self.assertRaisesRegex(intake.Refused, "no longer equals"):
            intake.admitted_path(str(self.vendor), self.record, "entrypoint")

    def test_a_link_in_place_of_the_entrypoint_or_of_its_directory_refuses(self):
        (self.vendor / "bin/codex").unlink()
        os.symlink(self.vendor.parent / "not-in-inventory", self.vendor / "bin/codex")
        with self.assertRaisesRegex(intake.Refused, "passes through a link"):
            intake.admitted_path(str(self.vendor), self.record, "entrypoint")
        (self.vendor / "bin/codex").unlink()
        (self.vendor / "bin").rmdir()
        os.symlink(self.vendor.parent, self.vendor / "bin")
        with self.assertRaisesRegex(intake.Refused, "passes through a link"):
            intake.admitted_path(str(self.vendor), self.record, "entrypoint")

    def test_the_supplier_environment_is_six_variables_and_its_path_names_only_the_admitted_directory(self):
        homes = []
        for name in ("user-home", "home", "tmp"):
            (self.vendor.parent / name).mkdir()
            homes.append(str(self.vendor.parent / name))
        admitted = intake.admitted_path(str(self.vendor), self.record, "pathDir")
        environment = intake.supplier_environment(admitted, str(self.vendor), *homes)
        self.assertEqual(sorted(environment), ["CODEX_HOME", "HOME", "LANG", "PATH", "TMPDIR", "TZ"])
        self.assertEqual(environment["TZ"], "UTC")
        self.assertEqual(environment["PATH"].split(os.pathsep), [admitted, "/usr/bin", "/bin", "/usr/sbin", "/sbin"])
        outside = str(self.vendor.parent / "not-in-inventory")
        for path_directory in (admitted + os.pathsep + outside, outside, str(self.vendor), "codex-path", ""):
            with self.subTest(path_directory=path_directory):
                with self.assertRaises((intake.Refused, ValueError)):
                    intake.supplier_environment(path_directory, str(self.vendor), *homes)
        with self.assertRaisesRegex(intake.Refused, "HOME"):
            intake.supplier_environment(admitted, str(self.vendor), homes[0] + os.pathsep + outside, *homes[1:])


class OutsideConfiguration(unittest.TestCase):
    """No configuration from outside the fresh homes may reach the supplier; a check not made refuses."""

    def setUp(self):
        self.root = tempfile.TemporaryDirectory()
        self.base = Path(os.path.realpath(self.root.name))
        self.work = self.base / "project/deeper/scratch/workspace"
        self.work.mkdir(parents=True)
        self.absent = str(self.base / "no-system-folder")

    def tearDown(self):
        os.chmod(self.base / "project", 0o700)
        self.root.cleanup()

    def check(self, preference=lambda: False, system=None):
        return intake.outside_configuration(str(self.work), preference, system or self.absent)

    def test_a_clean_place_names_every_check_made(self):
        checks = self.check()
        self.assertEqual((checks["system_configuration_folder"], checks["managed_preferences"]), ("absent", "absent"))
        self.assertRegex(checks["working_directory_ancestors"], r"^\d+ checked, none holds")

    def test_a_project_or_codex_folder_in_any_ancestor_refuses(self):
        for holder in ("project", "project/deeper", "project/deeper/scratch", "project/deeper/scratch/workspace"):
            for name in (".git", ".codex"):
                with self.subTest(holder=holder, name=name):
                    marker = self.base / holder / name
                    marker.mkdir()
                    try:
                        with self.assertRaisesRegex(intake.Refused, "holds a %s entry" % re.escape(name)):
                            self.check()
                    finally:
                        marker.rmdir()
        (self.base / "project/.git").write_text("gitdir: elsewhere\n")  # a worktree's file counts as well
        with self.assertRaisesRegex(intake.Refused, "holds a .git entry"):
            self.check()

    def test_system_configuration_or_a_managed_preference_refuses(self):
        (self.base / "system").mkdir()
        with self.assertRaisesRegex(intake.Refused, "system configuration"):
            self.check(system=str(self.base / "system"))
        with self.assertRaisesRegex(intake.Refused, "managed preference"):
            self.check(preference=lambda: True)

    def test_a_check_that_cannot_be_made_refuses(self):
        def failing():
            raise OSError("invented")
        with self.assertRaisesRegex(intake.Refused, "could not be checked"):
            self.check(preference=failing)
        with self.assertRaisesRegex(intake.Refused, "managed preference"):
            self.check(preference=lambda: None)  # an answer that is not a plain no
        if os.geteuid() != 0:
            os.chmod(self.base / "project", 0o000)
            with self.assertRaisesRegex(intake.Refused, "could not be checked"):
                self.check()

    @unittest.skipUnless(sys.platform == "darwin", "the supplier reads managed preferences on macOS only")
    def test_the_managed_preference_reading_answers_yes_or_no(self):
        self.assertIn(intake.managed_preference_present(), (True, False))


class SocketRows(unittest.TestCase):
    @staticmethod
    def lsof(returncode, stdout="", stderr=""):
        return lambda *args, **kwargs: types.SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)

    def test_a_sample_is_taken_only_when_lsof_reports_cleanly(self):
        header = "COMMAND PID PGID USER FD TYPE DEVICE SIZE/OFF NODE NAME\n"
        row = "codex 1 1 u 9u IPv4 0x0 0t0 TCP 127.0.0.1:50000->127.0.0.1:443 (ESTABLISHED)\n"
        self.assertEqual(intake.socket_rows(1, self.lsof(1)), [])
        self.assertEqual(intake.socket_rows(1, self.lsof(0, header)), [])
        self.assertEqual(intake.socket_rows(1, self.lsof(0, header + row)), [row.rstrip("\n")])
        self.assertIsNone(intake.socket_rows(1, self.lsof(2)))
        self.assertIsNone(intake.socket_rows(1, self.lsof(1, stderr="lsof: no pwd entry")))
        self.assertIsNone(intake.socket_rows(1, self.lsof(1, header + row)))

        def unanswered(*args, **kwargs):
            raise subprocess.TimeoutExpired("lsof", 1)
        self.assertIsNone(intake.socket_rows(1, unanswered))


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
        self.originals = (intake.socket_rows, tempfile.tempdir)
        intake.socket_rows = lambda group: []  # the stand-in opens no socket; SocketRows tests the reading

    def tearDown(self):
        intake.socket_rows, tempfile.tempdir = self.originals
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
                intake.socket_rows = lambda group: rows
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
