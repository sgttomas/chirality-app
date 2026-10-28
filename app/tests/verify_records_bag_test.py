"""Bounded byte-verifier races; invented local packages, no native acts."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parent.parent / "tools/verify_records_bag.py"
spec = importlib.util.spec_from_file_location("verify_records_bag", SOURCE)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class VerifyBagTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve() / "bag"
        (self.root / "data").mkdir(parents=True)
        (self.root / "data/evidence.bin").write_bytes(b"invented unchanged bytes")
        for tag in verifier.TAGS:
            (self.root / tag).write_bytes(b"invented tag bytes")
        (self.root / "bagit.txt").write_bytes(b"BagIt-Version: 1.0\nTag-File-Character-Encoding: UTF-8\n")
        (self.root / "verify.py").write_bytes(SOURCE.read_bytes())
        self.write_manifest("manifest-sha256.txt", {"data/evidence.bin"})
        self.write_manifest("tagmanifest-sha256.txt", verifier.TAGS)

    def write_manifest(self, name, paths):
        lines = [hashlib.sha256((self.root / path).read_bytes()).hexdigest() + "  " + path + "\n" for path in sorted(paths)]
        (self.root / name).write_text("".join(lines), encoding="utf-8")

    def test_valid_package_and_legacy_history_limit(self):
        self.assertEqual(verifier.verify(self.root), (1, False))

    def test_both_head_profiles_keep_full_byte_verification_without_chain_semantics(self):
        role = self.root / "data/role-supply/observations.jsonl"
        role.parent.mkdir()
        role.write_bytes(b"retained source bytes; schema deliberately unexamined\n")
        for version in ("0.1", "0.2"):
            with self.subTest(profile=version):
                # This portable tool checks all package bytes, including this
                # tag. App Rust verification separately interprets its profile
                # and schema/chain semantics; no adoption/authority follows.
                heads = {"format": "chirality.records-export-chain-heads",
                         "formatVersion": version, "logs": []}
                (self.root / "records-chain-heads.json").write_text(json.dumps(heads), encoding="utf-8")
                self.write_manifest("manifest-sha256.txt", {"data/evidence.bin", "data/role-supply/observations.jsonl"})
                self.write_manifest("tagmanifest-sha256.txt", verifier.TAGS)
                self.assertEqual(verifier.verify(self.root), (2, False))

    def test_leaf_replacement_between_metadata_and_open_refuses_symlink_or_fifo(self):
        for relative in ("data/evidence.bin", "bagit.txt", "manifest-sha256.txt", "tagmanifest-sha256.txt"):
            path = self.root / relative
            original = path.read_bytes()
            for kind in ("symlink", "fifo"):
                with self.subTest(member=relative, replacement=kind):
                    outside = self.root.parent / "outside"
                    outside.write_bytes(original)
                    actual_open = os.open
                    changed = False
                    def replace_before_open(candidate, flags, *args, **kwargs):
                        nonlocal changed
                        if Path(candidate) == path and not changed:
                            # Fail before entering a FIFO if safe-open flags ever
                            # regress, so this negative test cannot hang CI.
                            self.assertEqual(flags & (os.O_NOFOLLOW | os.O_NONBLOCK), os.O_NOFOLLOW | os.O_NONBLOCK)
                            changed = True
                            path.unlink()
                            if kind == "symlink":
                                path.symlink_to(outside)
                            else:
                                os.mkfifo(path, 0o600)
                        return actual_open(candidate, flags, *args, **kwargs)
                    started = time.monotonic()
                    with patch.object(verifier.os, "open", side_effect=replace_before_open):
                        with self.assertRaises((OSError, ValueError)):
                            verifier.verify(self.root)
                    self.assertTrue(changed)
                    self.assertLess(time.monotonic() - started, 2)
                    path.unlink()
                    path.write_bytes(original)

    def test_final_census_refuses_new_member_after_initial_inventory(self):
        original_digest = verifier.digest
        changed = False
        def late_member(path):
            nonlocal changed
            result = original_digest(path)
            if path == self.root / "data/evidence.bin" and not changed:
                changed = True
                (self.root / "late-evidence.bin").write_bytes(b"not in the checked inventory")
            return result
        with patch.object(verifier, "digest", side_effect=late_member):
            with self.assertRaisesRegex(ValueError, "package changed"):
                verifier.verify(self.root)


if __name__ == "__main__":
    unittest.main()
