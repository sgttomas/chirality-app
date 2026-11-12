#!/usr/bin/env python3
"""Checks of archive intake on invented archives. No supplier is executed and nothing is fetched.

Run from `app/`: python3 supplier_checks/test_intake.py
"""
import hashlib
import io
import json
import os
import tarfile
import tempfile
import unittest
from pathlib import Path

import capture
import intake

PIN = "9.9.9"
URL = "https://example.invalid/package.tar.gz"


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
        return intake.take_archive(str(path), URL, actual_size if size is None else size,
                                   digest or actual_digest, pin, str(self.base / "out"))

    def test_record_inventories_every_member_and_the_tree_then_verifies_against_it(self):
        record = self.take(plain_members())
        self.assertEqual((record["pin"], record["files"], record["macho_files"]), (PIN, 2, 1))
        self.assertEqual([(e["path"], e["kind"], e["mode"]) for e in record["inventory"]["entries"]],
                         [("bin", "dir", 0o755), ("bin/codex", "file", 0o755), ("codex-package.json", "file", 0o644),
                          ("codex-path", "dir", 0o755)])
        written = json.loads((self.base / "out/supplier" / PIN / "CANONICAL_DISTRIBUTION.json").read_bytes())
        self.assertEqual(written, record)
        vendor = self.base / "out/vendor"
        _, binary, _ = capture.verified_vendor(str(vendor), PIN, self.base / "out/supplier")
        self.assertEqual(binary, str(vendor / "bin/codex"))
        (vendor / "bin/codex").write_bytes(b"changed")
        with self.assertRaisesRegex(capture.Refused, "content: bin/codex"):
            capture.verified_vendor(str(vendor), PIN, self.base / "out/supplier")

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
        self.assertEqual(intake.main(["archive", "--archive", str(path), "--url", URL, "--size", str(size),
                                      "--sha256", digest, "--pin", PIN, "--out", str(self.base / "out")]), 2)
        self.assertEqual(list((self.base / "out").iterdir()), [])


if __name__ == "__main__":
    unittest.main()
