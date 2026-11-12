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
        self.logs = {}
        self.write_heads()

    def write_manifest(self, name, paths):
        lines = [hashlib.sha256((self.root / path).read_bytes()).hexdigest() + "  " + path + "\n" for path in sorted(paths)]
        (self.root / name).write_text("".join(lines), encoding="utf-8")

    def write_log(self, relative, data):
        path = self.root / "data" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def seal(self):
        """Recomputes both manifests over the package as it now stands, as
        someone altering it would; the chain-head tag is left as it is."""
        payload = {p.relative_to(self.root).as_posix() for p in (self.root / "data").rglob("*") if p.is_file()}
        self.write_manifest("manifest-sha256.txt", payload)
        self.write_manifest("tagmanifest-sha256.txt", verifier.TAGS)

    def write_heads(self, version="0.2", **chains):
        """Records `chains` (log: chain) as the export would, then seals."""
        heads = {"format": "chirality.records-export-chain-heads", "formatVersion": version,
                 "method": verifier.METHOD, "logs": [{"log": log, "chain": chain} for log, chain in sorted(chains.items())]}
        (self.root / "records-chain-heads.json").write_text(json.dumps(heads, indent=2), encoding="utf-8")
        self.seal()

    def test_valid_package_and_legacy_history_limit(self):
        self.assertEqual(verifier.verify(self.root), (1, False, {"profile": "0.2", "logs": 0, "notes": []}))

    def test_role_log_chain_is_recomputed_in_profile_0_2_and_left_as_a_limit_in_0_1(self):
        lines = linked([{"seq": 1, "observationId": "obs:one"}, {"seq": 2, "observationId": "obs:two"}])
        self.write_log("role-supply/observations.jsonl", lines)
        self.write_heads(**{"role-supply/observations.jsonl": head(lines)})
        self.assertEqual(verifier.verify(self.root)[2]["logs"], 1)
        self.write_heads()
        with self.assertRaisesRegex(ValueError, "observations.jsonl: payload log has no recorded chain head"):
            verifier.verify(self.root)
        # The legacy profile recorded RS heads only and never this log's.
        self.write_log("role-supply/observations.jsonl", b"retained source bytes; schema deliberately unexamined\n")
        self.write_heads(version="0.1")
        notes = verifier.verify(self.root)[2]["notes"]
        self.assertEqual(len(notes), 1)
        self.assertIn("legacy chain-head profile 0.1", notes[0])
        self.write_heads()
        with self.assertRaises(ValueError):
            verifier.verify(self.root)

    def test_unaltered_chained_log_verifies_and_a_changed_line_with_rehashed_manifests_fails_at_the_next_line(self):
        log = "runs/run-one/app-writer.jsonl"
        lines = linked([{"seq": 1, "body": "first"}, {"seq": 2, "body": "second"}, {"seq": 3, "body": "third"}])
        self.write_log(log, lines)
        self.write_heads(**{log: head(lines)})
        self.assertEqual(verifier.verify(self.root)[2], {"profile": "0.2", "logs": 1, "notes": []})
        # Same length, still JSON, every checksum recomputed; the chain is not.
        self.write_log(log, lines.replace(b'"first"', b'"FIRST"'))
        self.seal()
        with self.assertRaisesRegex(ValueError, r"runs/run-one/app-writer.jsonl: chain broken at line 2: it links to"):
            verifier.verify(self.root)

    def test_changed_last_line_fails_on_the_recorded_head(self):
        log = "acts/person.jsonl"
        lines = linked([{"seq": 1, "body": "first"}, {"seq": 2, "body": "last"}])
        self.write_log(log, lines)
        self.write_heads(**{log: head(lines)})
        self.write_log(log, lines.replace(b'"last"', b'"LAST"'))
        self.seal()
        with self.assertRaisesRegex(ValueError, r"acts/person.jsonl: recomputed chain head .* differs from the recorded head"):
            verifier.verify(self.root)

    def test_removed_reordered_unlinked_and_restarted_lines_break_the_chain(self):
        log = "runs/run-one/app-writer.jsonl"
        rows = [{"seq": n, "body": f"line {n}"} for n in (1, 2, 3)]
        lines = linked(rows)
        parts = lines.split(b"\n")[:-1]
        cases = {
            "removed": (b"\n".join([parts[0], parts[2]]) + b"\n", 2),
            "reordered": (b"\n".join([parts[1], parts[0], parts[2]]) + b"\n", 1),
            "unlinked": (lines + json.dumps({"seq": 4}).encode() + b"\n", 4),
            "restarted": (lines + linked([{"seq": 4}]), 4),
        }
        for case, (data, line) in cases.items():
            with self.subTest(case=case):
                self.write_log(log, data)
                self.write_heads(**{log: head(data)})
                with self.assertRaisesRegex(ValueError, f"chain broken at line {line}:"):
                    verifier.verify(self.root)

    def test_a_chain_the_store_already_recorded_broken_is_not_verified_whole(self):
        log = "runs/run-one/app-writer.jsonl"
        lines = linked([{"seq": 1}, {"seq": 2}]).replace(b'"seq": 1', b'"seq": 9')
        self.write_log(log, lines)
        chain = head(lines)
        chain["broken"] = ["app-writer.jsonl: chain broken at line 2: recorded by the App"]
        self.write_heads(**{log: chain})
        with self.assertRaisesRegex(ValueError, r"chain broken at line 2: .*also records it broken at export"):
            verifier.verify(self.root)

    def test_legacy_unchained_lines_torn_lines_blank_lines_and_partial_tail_follow_the_app(self):
        log = "legacy/coordination.rs.jsonl"
        legacy = b'{"seq": 1, "legacy": true}\n'
        torn = b'{"seq": 2, "torn'
        limit = {"kind": "evidence_limit", "seq": 2, "body": {"label": verifier.PARTIAL,
                 "subjectRef": f"line 2; {len(torn)} bytes; sha256 {hashlib.sha256(torn).hexdigest()}"}}
        first = json.dumps(dict(limit, prevLine={"method": verifier.METHOD, "value": hashlib.sha256(legacy[:-1]).hexdigest()})).encode()
        after = json.dumps({"seq": 3, "prevLine": {"method": verifier.METHOD, "value": hashlib.sha256(first).hexdigest()}}).encode()
        data = legacy + torn + b"\n" + first + b"\n \t\r\n" + after + b"\n" + b'{"seq": 4, "unclosed'
        self.write_log(log, data)
        chain = {"method": verifier.METHOD, "head": hashlib.sha256(after).hexdigest(), "lines": 3, "broken": []}
        self.write_heads(**{log: chain})
        notes = verifier.verify(self.root)[2]["notes"]
        self.assertEqual(len(notes), 2)
        self.assertIn("line 2 is a torn line W-0 terminated", notes[0])
        self.assertIn("unchained (legacy): 1 lines", notes[1])

    def test_recorded_heads_must_cover_exactly_the_payload_logs(self):
        log = "runs/run-one/app-writer.jsonl"
        lines = linked([{"seq": 1}])
        self.write_log(log, lines)
        self.write_heads(**{log: head(lines), "runs/absent.jsonl": head(lines)})
        with self.assertRaisesRegex(ValueError, "runs/absent.jsonl: recorded chain head names no payload log"):
            verifier.verify(self.root)
        self.write_heads(**{log: head(lines), "evidence.bin": head(lines)})
        with self.assertRaisesRegex(ValueError, "not a chained log"):
            verifier.verify(self.root)
        self.write_heads(**{log: {"state": "unreadable", "error": "invented"}})
        with self.assertRaisesRegex(ValueError, "recorded at export as unreadable"):
            verifier.verify(self.root)

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


def linked(rows):
    """Invented lines, each linked to the one before as the App writes them; the
    first line of the rows given starts a chain."""
    out, previous = b"", None
    for row in rows:
        raw = json.dumps(dict(row, prevLine={"method": verifier.METHOD, "value": previous})).encode()
        previous = hashlib.sha256(raw).hexdigest()
        out += raw + b"\n"
    return out


def head(data):
    """The head the export records for a whole chain of complete lines."""
    lines = data.split(b"\n")[:-1]
    return {"method": verifier.METHOD, "head": hashlib.sha256(lines[-1]).hexdigest(), "lines": len(lines),
            "linked": True, "unchained": 0, "unchainedLimit": None, "broken": []}


if __name__ == "__main__":
    unittest.main()
