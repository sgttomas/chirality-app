"""Bounded byte-verifier races; invented local packages, no native acts."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
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

    def write_heads(self, version="0.3", **chains):
        """Records `chains` (log: chain) as the export would, then seals. A
        profile 0.3 head also pins the log's exact bytes, taken here from the
        log as it stands unless the test states them itself."""
        if version == "0.3":
            chains = {log: dict(chain) for log, chain in chains.items()}
            for log, chain in chains.items():
                if not (self.root / "data" / log).is_file():
                    continue
                data = (self.root / "data" / log).read_bytes()
                chain.setdefault("bytes", len(data))
                chain.setdefault("sha256", hashlib.sha256(data).hexdigest())
                if "state" not in chain:
                    chain.setdefault("unclosedEnd", verifier.unclosed_end(data))
        heads = {"format": "chirality.records-export-chain-heads", "formatVersion": version,
                 "method": verifier.METHOD, "logs": [{"log": log, "chain": chain} for log, chain in sorted(chains.items())]}
        (self.root / "records-chain-heads.json").write_text(json.dumps(heads, indent=2), encoding="utf-8")
        self.seal()

    def earlier_profile(self):
        """Rewrites the tag as a build of profile 0.2 recorded it, with no
        account and no pin on a log's bytes, then seals: what is left to show
        a change is the chain."""
        heads = json.loads((self.root / "records-chain-heads.json").read_text(encoding="utf-8"))
        heads["formatVersion"] = "0.2"
        for item in heads["logs"]:
            for name in ("bytes", "sha256", "setAside", "torn", "unclosedEnd", "line", "kind"):
                item["chain"].pop(name, None)
        (self.root / "records-chain-heads.json").write_text(json.dumps(heads, indent=2), encoding="utf-8")
        self.seal()

    def run_verifier(self):
        """Runs the package's own carried copy, as a person without the App would."""
        return subprocess.run([sys.executable, str(self.root / "verify.py"), str(self.root)], capture_output=True, text=True)

    def test_valid_package_and_legacy_history_limit(self):
        self.assertEqual(verifier.verify(self.root), (1, False, {"profile": "0.3", "logs": 0, "recomputed": 0, "limited": [], "limitedLogs": 0, "notCompared": [], "notes": []}))
        whole = self.run_verifier()
        self.assertEqual(whole.returncode, 0, whole.stderr)
        self.assertTrue(whole.stdout.startswith("Package bytes: consistent."), whole.stdout)
        # A package with no chained log says nothing was there to check; it
        # does not report unbroken chains it never examined.
        self.assertIn("\nLog integrity: nothing to check. This package carries no chained log.", whole.stdout)
        self.assertIn("\nResult: every check this verifier makes passed: package bytes consistent; no chained log in the package (exit status 0).", whole.stdout)
        self.assertNotIn("no chain is broken", whole.stdout)
        self.assertNotIn("LIMITED", whole.stdout)
        self.assertIn("A package whose records, manifests and chain heads were replaced together still verifies.", whole.stdout)

    def test_the_top_level_of_the_record_format_carried_here_is_the_schemas(self):
        # The verifier carries no schema; what it does carry must equal it.
        schema = json.loads((SOURCE.parent.parent / "src-tauri/schemas/RS_RECORD.schema.json").read_text(encoding="utf-8"))["$defs"]
        entry, group, link = schema["entry"], schema["groupLine"], schema["chainLink"]
        # The whole structure the verifier mirrors, so that no change at the
        # top level of the format can pass here unnoticed.
        self.assertEqual(set(entry), {"type", "required", "additionalProperties", "properties", "anyOf", "oneOf"})
        self.assertEqual(entry["type"], "object")
        for name in ("recordId", "corrects"):
            self.assertEqual(entry["properties"][name], {"$ref": "#/$defs/recordId"})
        self.assertEqual(entry["properties"]["runId"], {"$ref": "#/$defs/runId"})
        self.assertEqual(entry["properties"]["prevLine"], {"$ref": "#/$defs/chainLink"})
        # Below the top level the format is a body by kind, which is not carried here.
        for choice in entry["oneOf"]:
            self.assertEqual(set(choice), {"properties"})
            self.assertEqual(set(choice["properties"]), {"kind", "body"})
            self.assertIn(choice["properties"]["kind"]["const"], verifier.KINDS)
        self.assertEqual({choice["properties"]["kind"]["const"] for choice in entry["oneOf"]}, set(verifier.KINDS))
        self.assertEqual(set(group), {"description", "type", "required", "additionalProperties", "properties"})
        self.assertEqual(group["type"], "object")
        self.assertEqual(group["properties"]["prevLine"], {"$ref": "#/$defs/chainLink"})
        self.assertEqual(list(verifier.ENTRY_REQUIRED), entry["required"])
        self.assertEqual(verifier.ENTRY_MEMBERS, set(entry["properties"]))
        self.assertIs(entry["additionalProperties"], False)
        self.assertEqual(entry["properties"]["format"], {"const": verifier.ENTRY_FORMAT})
        self.assertEqual(entry["properties"]["formatVersion"], {"type": "string", "pattern": "^[0-9]+\\.[0-9]+$"})
        self.assertEqual(verifier.KINDS, set(entry["properties"]["kind"]["enum"]))
        self.assertEqual(entry["properties"]["recorder"], {"type": "object", "required": ["role", "identity"], "additionalProperties": False,
                         "properties": {"role": {"enum": sorted(verifier.RECORDER_ROLES, key=entry["properties"]["recorder"]["properties"]["role"]["enum"].index)},
                                        "identity": {"type": "string", "minLength": 1}}})
        self.assertEqual(entry["properties"]["context"], {"type": "object", "required": ["surface"], "additionalProperties": False,
                         "properties": {"surface": {"enum": ["App", "host"]}, "hostIdentity": {"type": "string"}}})
        self.assertEqual(verifier.SURFACES, {"App", "host"})
        self.assertEqual(entry["properties"]["seq"], {"type": "integer", "minimum": 1})
        self.assertEqual(entry["properties"]["writtenAt"], {"type": "string", "minLength": 1})
        self.assertEqual(entry["properties"]["observedAt"], {"type": "string"})
        self.assertEqual(entry["properties"]["correctionReason"], {"type": "string", "minLength": 1})
        self.assertEqual(entry["properties"]["body"], {"type": "object"})
        self.assertEqual(entry["anyOf"], [{"not": {"required": ["corrects"]}}, {"required": ["corrects", "correctionReason"]}])
        self.assertEqual(schema["recordId"], {"type": "string", "pattern": "^" + verifier.RECORD_ID.pattern[:-2] + "$"})
        self.assertEqual(schema["runId"], {"type": "string", "pattern": "^" + verifier.RUN_ID.pattern[:-2] + "$"})
        self.assertEqual({k: v for k, v in link.items() if k != "description"}, {"type": "object", "required": ["method", "value"], "additionalProperties": False,
                         "properties": {"method": {"const": verifier.METHOD}, "value": {"oneOf": [{"type": "string", "pattern": "^" + verifier.HEX64.pattern[:-2] + "$"}, {"type": "null"}]}}})
        self.assertEqual(list(verifier.GROUP_REQUIRED), group["required"])
        self.assertEqual(verifier.GROUP_MEMBERS, set(group["properties"]))
        self.assertIs(group["additionalProperties"], False)
        self.assertEqual(group["properties"]["format"], {"const": verifier.GROUP_FORMAT})
        self.assertEqual(group["properties"]["formatVersion"], {"const": "0.1"})
        self.assertEqual(group["properties"]["groupId"], {"type": "string", "pattern": "^grp:"})
        self.assertEqual(group["properties"]["entries"], {"type": "array", "minItems": 2, "items": {"allOf": [{"$ref": "#/$defs/entry"}, {"not": {"required": ["prevLine"]}}]}})

    def test_role_log_chain_is_compared_and_a_log_the_app_refused_is_never_taken_on_trust(self):
        lines = linked([{"seq": 1, "observationId": "obs:one"}, {"seq": 2, "observationId": "obs:two"}])
        whole = head(lines, "role supply observations")
        self.write_log(ROLE, lines)
        self.write_heads(**{ROLE: whole})
        report = verifier.verify(self.root)[2]
        self.assertEqual((report["recomputed"], report["limited"], report["notCompared"]), (1, [], []))
        # What this verifier does not check of a role log is said, not left out.
        self.assertIn("does not check that each observation is one the App accepts", report["notes"][0])
        # A changed role log with the tag unchanged fails on the bytes the tag pins.
        self.write_log(ROLE, linked([{"seq": 1, "observationId": "obs:one"}, {"seq": 2, "observationId": "obs:TWO"}]))
        self.seal()
        with self.assertRaisesRegex(verifier.ChainDisagreement, "its bytes .* are not the ones the package's chain-head tag records"):
            verifier.verify(self.root)
        # The chain is still recomputed: a head recorded for other lines
        # disagrees, and a line that is not JSON cannot be a link.
        self.write_heads(**{ROLE: whole})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "recomputed chain head .* differs from the recorded head"):
            verifier.verify(self.root)
        self.write_log(ROLE, lines + b"not json\n")
        self.write_heads(**{ROLE: whole})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "line 3 is not a readable record"):
            verifier.verify(self.root)
        # The App takes this log whole or not at all: an account cannot set its lines aside.
        self.write_log(ROLE, lines)
        self.write_heads(**{ROLE: dict(whole, setAside=[2])})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "takes this log whole or not at all"):
            verifier.verify(self.root)
        self.write_heads()
        with self.assertRaisesRegex(ValueError, "observations.jsonl: payload log has no recorded chain head"):
            verifier.verify(self.root)

        # A log the App could not take at export. The tag pins its bytes and
        # states where and why the App stopped; this verifier compares the
        # bytes and relays the statement, and infers nothing from the lines.
        def refused(line, kind):
            return {"state": "unreadable or invalid role supply chain", "error": "invented", "line": line, "kind": kind}
        self.write_log(ROLE, lines + b"not json\n")
        self.write_heads(**{ROLE: refused(3, "unreadable line")})
        report = verifier.verify(self.root)[2]
        self.assertEqual((len(report["limited"]), report["limitedLogs"], report["recomputed"], report["notCompared"]), (1, 1, 0, []))
        self.assertIn("the package states that the App could not read this log's chain when it was exported at line 3 (unreadable line)", report["limited"][0])
        self.assertIn("its bytes are the ones the tag records, and no chain head is established for it", report["limited"][0])
        same = self.run_verifier()
        self.assertEqual(same.returncode, 2, same.stderr)
        # No head compared is never "each agrees".
        self.assertIn("\nRecorded chain heads: 0 of 1 compared with the lines. No head is established for the others, which are named under log integrity.\n", same.stdout)
        self.assertNotIn("each agrees", same.stdout)
        self.assertNotIn("each of those agrees", same.stdout)
        self.assertIn("\nLog integrity: LIMITED. 1 limit in 1 log.", same.stdout)
        # The refused log replaced by another the App would refuse at the same
        # line for the same kind of fault: not the bytes the tag records.
        self.write_log(ROLE, lines + b"{\n")
        self.seal()
        with self.assertRaisesRegex(verifier.ChainDisagreement, "its bytes .* are not the ones the package's chain-head tag records"):
            verifier.verify(self.root)
        # A refused log whose tag does not pin it fails too.
        self.write_heads(**{ROLE: dict(refused(3, "unreadable line"), sha256="0" * 64)})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "its bytes .* are not the ones the package's chain-head tag records"):
            verifier.verify(self.root)
        # An earlier profile records a refusal with no pin on the log's bytes:
        # said as not compared, never as agreement.
        self.write_heads(version="0.2", **{ROLE: {"state": "unreadable or invalid role supply chain", "error": "invented"}})
        report = verifier.verify(self.root)[2]
        self.assertEqual(report["notCompared"], [ROLE])
        self.assertIn("this profile does not pin the log's bytes in its tag, so this verifier cannot establish that this log is the one the package describes", report["limited"][0])
        unsure = self.run_verifier()
        self.assertEqual(unsure.returncode, 2, unsure.stderr)
        self.assertIn(f"NOT COMPARED: {ROLE}. This verifier cannot establish that such a log is the one the package describes; the App can.", unsure.stdout)
        self.assertIn("\nResult: package bytes consistent; log integrity limited; 1 recorded head not compared (exit status 2).", unsure.stdout)
        self.assertIn("\nNot checked: this verifier does not hold the record format, and this package's chain-head profile (0.1 or 0.2)", unsure.stdout)
        # The legacy profile recorded RS heads only and never this log's.
        self.write_log(ROLE, b"retained source bytes; schema deliberately unexamined\n")
        self.write_heads(version="0.1")
        report = verifier.verify(self.root)[2]
        # Not checked is not clean: an integrity limit and its own exit
        # status, never part of "no chain is broken".
        self.assertEqual((report["notes"], len(report["limited"]), report["notCompared"]), ([], 1, [ROLE]))
        self.assertIn("legacy chain-head profile (0.1) records no head for this log, so its chain was not checked", report["limited"][0])
        unchecked = self.run_verifier()
        self.assertEqual(unchecked.returncode, 2, unchecked.stderr)
        self.assertNotIn("no chain is broken", unchecked.stdout)
        self.write_heads()
        with self.assertRaises(ValueError):
            verifier.verify(self.root)

    def test_unaltered_chained_log_verifies_and_a_changed_line_with_rehashed_manifests_fails_at_the_next_line(self):
        lines = linked([entry(1, "first"), entry(2, "second"), entry(3, "third")])
        self.write_log(LOG, lines)
        self.write_heads(**{LOG: head(lines)})
        self.assertEqual(verifier.verify(self.root)[2], {"profile": "0.3", "logs": 1, "recomputed": 1, "limited": [], "limitedLogs": 0, "notCompared": [], "notes": []})
        clean = self.run_verifier()
        self.assertEqual(clean.returncode, 0, clean.stderr)
        self.assertEqual(clean.stdout.split("\n")[1], "Exported logs: each of the 1 chained log is byte for byte the log the chain-head tag records. "
                         "This says it is the log that was exported; it does not say its records are intact.")
        self.assertIn("\nLog integrity: no chain is broken, and the package's account lists no line as set aside. Every link this verifier examined names the line before it.\n", clean.stdout)
        # Exit status 0 is "every check this verifier makes passed", and every such run says what was not checked.
        self.assertIn("\nResult: every check this verifier makes passed: package bytes consistent; no chain is broken (exit status 0).", clean.stdout)
        self.assertIn("\nNot checked: this verifier does not hold the record format.", clean.stdout)
        self.assertIn("Only the App's own verification establishes that every line was read as a record.", clean.stdout)
        # Same length, still a record, every checksum recomputed; the tag is
        # not, and it pins the log's bytes.
        self.write_log(LOG, lines.replace(b'"first"', b'"FIRST"'))
        self.seal()
        with self.assertRaisesRegex(verifier.ChainDisagreement, "its bytes .* are not the ones the package's chain-head tag records"):
            verifier.verify(self.root)
        # A package of the earlier profile has no such pin; there the chain shows it.
        self.earlier_profile()
        with self.assertRaisesRegex(verifier.ChainDisagreement, r"runs/run-one/app-writer.jsonl: chain broken at line 2: it links to"):
            verifier.verify(self.root)

    def test_changed_last_line_fails_on_the_recorded_head(self):
        log = "acts/person.jsonl"
        lines = linked([entry(1, "first"), entry(2, "last")])
        self.write_log(log, lines)
        self.write_heads(**{log: head(lines, "person.jsonl")})
        self.write_log(log, lines.replace(b'"last"', b'"LAST"'))
        self.seal()
        with self.assertRaisesRegex(verifier.ChainDisagreement, "its bytes .* are not the ones the package's chain-head tag records"):
            verifier.verify(self.root)
        self.earlier_profile()
        with self.assertRaisesRegex(verifier.ChainDisagreement, r"acts/person.jsonl: recomputed chain head .* differs from the recorded head"):
            verifier.verify(self.root)

    def test_removed_reordered_unlinked_and_restarted_lines_break_the_chain(self):
        lines = linked([entry(n, f"line {n}") for n in (1, 2, 3)])
        parts = lines.split(b"\n")[:-1]
        cases = {
            "removed": (b"\n".join([parts[0], parts[2]]) + b"\n", 2, "it links to"),
            "reordered": (b"\n".join([parts[1], parts[0], parts[2]]) + b"\n", 1, "it links to .*, but it is the first line of its log"),
            "unlinked": (lines + json.dumps(entry(4, "unlinked")).encode() + b"\n", 4, "no chain link after linked lines"),
            "restarted": (lines + linked([entry(4, "restarted")]), 4, "it starts a new chain after earlier lines"),
        }
        for case, (data, line, why) in cases.items():
            with self.subTest(case=case):
                self.write_log(LOG, data)
                self.write_heads(**{LOG: head(data)})
                with self.assertRaisesRegex(verifier.ChainDisagreement, f"chain broken at line {line}: {why}"):
                    verifier.verify(self.root)

    def test_a_chain_broken_in_the_store_at_export_verifies_only_with_exactly_the_recorded_breaks(self):
        whole = linked([entry(1, "first"), entry(2, "second"), entry(3, "third")])
        first = whole.split(b"\n")[0]
        lines = whole.replace(b'"first"', b'"FIRST"')
        self.write_log(LOG, lines)
        # As the App records it (record_lines.rs, Chain::step): the faithful
        # package of a store whose log was already broken.
        def recorded(now):
            return [f"app-writer.jsonl: chain broken at line 2: it links to \"{sha(first)}\", but the preceding line's identity is {sha(now.split(b'\n')[0])}; never repaired"]
        self.write_heads(**{LOG: head(lines, broken=recorded(lines))})
        report = verifier.verify(self.root)[2]
        self.assertEqual((report["logs"], len(report["limited"]), report["limitedLogs"], report["notes"]), (1, 1, 1, []))
        self.assertRegex(report["limited"][0], r"app-writer.jsonl: chain broken at line 2: it links to .* records it broken there when exported")
        # Two statements, never one pass: the bytes are consistent, and this
        # log's integrity is limited at this line. Its own exit status.
        limited = self.run_verifier()
        self.assertEqual(limited.returncode, 2, limited.stderr)
        one, pinned, two = limited.stdout.split("\n")[:3]
        self.assertTrue(one.startswith("Package bytes: consistent."), limited.stdout)
        self.assertTrue(pinned.startswith("Exported logs: each of the 1 chained log is byte for byte the log the chain-head tag records."), limited.stdout)
        self.assertEqual(two, "Recorded chain heads: 1 of 1 compared with the lines, and each agrees.")
        self.assertTrue(limited.stdout.split("\n")[3].startswith("Log integrity: LIMITED. 1 limit in 1 log."), limited.stdout)
        self.assertIn("\n  Integrity limit: runs/run-one/app-writer.jsonl: chain broken at line 2:", limited.stdout)
        self.assertIn("\nResult: package bytes consistent; log integrity limited (exit status 2).", limited.stdout)
        for phrase in ("no chain is broken", "lists no line as set aside", "names the line before it", "Result: verified", "exit status 0", "every check"):
            self.assertNotIn(phrase, limited.stdout)
        # The line before the recorded break changed again after export: the
        # break is at the same line, and it is no longer the break recorded.
        again = whole.replace(b'"first"', b'"OTHER"')
        self.write_log(LOG, again)
        self.seal()
        with self.assertRaisesRegex(verifier.ChainDisagreement, "its bytes .* are not the ones the package's chain-head tag records"):
            verifier.verify(self.root)
        failed = self.run_verifier()
        self.assertEqual((failed.returncode, failed.stdout), (1, ""))
        self.assertTrue(failed.stderr.startswith("Result: failed (exit status 1). Verification failed: runs/run-one/app-writer.jsonl: its bytes"), failed.stderr)
        # A package whose tag pins its bytes leaves nothing this verifier cannot tell.
        self.assertNotIn("cannot tell", failed.stderr)
        self.earlier_profile()
        with self.assertRaisesRegex(verifier.ChainDisagreement, "the break the package records at line 2 is not the break its lines give"):
            verifier.verify(self.root)
        # A further line changed after export is a break the package does not record.
        self.write_log(LOG, lines.replace(b'"second"', b'"SECOND"'))
        self.seal()
        with self.assertRaisesRegex(verifier.ChainDisagreement, r"chain broken at line 3: .*the package records no break there"):
            verifier.verify(self.root)
        failed = self.run_verifier()
        self.assertEqual((failed.returncode, failed.stdout), (1, ""))
        self.assertTrue(failed.stderr.startswith("Result: failed (exit status 1). Verification failed: runs/run-one/app-writer.jsonl: chain broken at line 3:"), failed.stderr)
        # A recorded break the lines do not have, one the verifier cannot place, and none stated.
        self.write_log(LOG, whole)
        self.write_heads(**{LOG: head(whole, broken=recorded(lines))})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "records a chain broken at line 2, but the recomputed chain is not broken there"):
            verifier.verify(self.root)
        self.write_heads(**{LOG: head(whole, broken=["broken somewhere"])})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "cannot compare"):
            verifier.verify(self.root)
        self.write_heads(**{LOG: {k: v for k, v in head(whole).items() if k != "broken"}})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "does not say whether the chain was broken at export"):
            verifier.verify(self.root)

    def test_every_recorded_fact_of_a_head_is_compared_with_the_lines(self):
        lines = linked([entry(1, "first"), entry(2, "second")])
        self.write_log(LOG, lines)
        for fact, value in (("linked", False), ("unchained", 3), ("unchainedLimit", "app-writer.jsonl: unchained (legacy): no line carries a chain link (2 lines)"),
                            ("lines", 3), ("lines", 2.0), ("head", None), ("method", "another method"), ("linked", 1)):
            with self.subTest(fact=fact, value=value):
                self.write_heads(**{LOG: dict(head(lines), **{fact: value})})
                with self.assertRaises(verifier.ChainDisagreement):
                    verifier.verify(self.root)
        self.write_heads(**{LOG: {k: v for k, v in head(lines).items() if k != "unchained"}})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "records unchained as null"):
            verifier.verify(self.root)

    def test_legacy_unchained_lines_torn_lines_blank_lines_and_partial_tail_follow_the_app(self):
        log = "legacy/coordination.rs.jsonl"
        legacy = json.dumps(entry(1, "legacy")).encode() + b"\n"
        torn = b'{"seq": 2, "torn'
        limit = entry(2, f"line 2; {len(torn)} bytes; sha256 {sha(torn)}", label=verifier.PARTIAL)
        first = json.dumps(dict(limit, prevLine={"method": verifier.METHOD, "value": sha(legacy[:-1])})).encode()
        after = json.dumps(dict(entry(3, "after"), prevLine={"method": verifier.METHOD, "value": sha(first)})).encode()
        data = legacy + torn + b"\n" + first + b"\n \t\r\n" + after + b"\n" + b'{"seq": 4, "unclosed'
        self.write_log(log, data)
        chain = {"method": verifier.METHOD, "head": sha(after), "lines": 3, "linked": True, "unchained": 1, "broken": [],
                 "unchainedLimit": "coordination.rs.jsonl: unchained (legacy): lines before the first linked line (1) carry no chain link; the chain starts after them"}
        # With the account (profile 0.3) the torn line is listed and relayed
        # as the package's statement; without it (0.2) this verifier works it
        # out as the App's reader does. Both ways it is a note that says why it
        # is not a limit. The unclosed final part is a limit in every profile.
        unclosed = f"{log}: partial entry at end (not read): {len(b'{\"seq\": 4, \"unclosed')} bytes after the last complete line"
        for version, account, said in (("0.3", {"setAside": [], "torn": [2]}, "the package's account lists line 2 as a torn line the App closed and set aside after an interrupted write. It is not a limit: "),
                                       ("0.2", {}, "line 2 is a torn line the App closed and set aside after an interrupted write. It is not a limit: "
                                                   "the line after it names its exact length and SHA-256 and is itself in the chain")):
            self.write_heads(version=version, **{log: dict(chain, **account)})
            report = verifier.verify(self.root)[2]
            self.assertEqual((report["limited"], report["limitedLogs"], len(report["notes"])), ([unclosed], 1, 2), version)
            self.assertIn(said, report["notes"][0])
            self.assertEqual(self.run_verifier().returncode, 2)
        # The account states the unclosed part; one that states none, or another length, disagrees.
        for stated in (None, 3):
            self.write_heads(**{log: dict(chain, setAside=[], torn=[2], unclosedEnd=stated)})
            with self.assertRaisesRegex(verifier.ChainDisagreement, "states an unclosed final part"):
                verifier.verify(self.root)
        # An account that lists the wrong line as torn leaves the torn bytes to be read as a line.
        self.write_heads(**{log: dict(chain, setAside=[], torn=[1])})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "line 2 is not a readable record"):
            verifier.verify(self.root)
        # The same log ending in a complete line: no limit, and the notes.
        data = legacy + torn + b"\n" + first + b"\n \t\r\n" + after + b"\n"
        self.write_log(log, data)
        self.write_heads(**{log: dict(chain, setAside=[], torn=[2])})
        notes = verifier.verify(self.root)[2]["notes"]
        self.assertEqual(len(notes), 2)
        self.assertIn("unchained (legacy): 1 lines", notes[1])
        # Lines with no link are said to be outside what the result covers.
        legacy_run = self.run_verifier()
        self.assertEqual(legacy_run.returncode, 0, legacy_run.stderr)
        self.assertIn("Every link this verifier examined names the line before it. 2 notes below name what that does not cover.", legacy_run.stdout)
        self.assertIn("\nResult: every check this verifier makes passed: package bytes consistent; no chain is broken; see the notes (exit status 0).", legacy_run.stdout)
        # A limit that names the line before it with other bytes sets nothing
        # aside: the torn line is then a counted line, and the head differs.
        wrong = json.dumps(dict(entry(2, f"line 2; {len(torn)} bytes; sha256 {sha(b'other')}", label=verifier.PARTIAL),
                                prevLine={"method": verifier.METHOD, "value": sha(legacy[:-1])})).encode()
        self.write_log(log, legacy + torn + b"\n" + wrong + b"\n")
        self.write_heads(version="0.2", **{log: dict(chain, head=sha(wrong), lines=2)})
        with self.assertRaises(verifier.ChainDisagreement):
            verifier.verify(self.root)

    def test_the_account_of_set_aside_lines_is_followed_and_can_only_add_stated_limits(self):
        # Profile 0.3. The App counted line 2 without reading it as a record
        # and says so; the verifier follows that and reports it as a limit.
        nothing = {"method": verifier.METHOD, "value": "0" * 64}
        first = json.dumps(dict(entry(1, "first"), prevLine={"method": verifier.METHOD, "value": None})).encode()
        # Whole at its top level, invalid deeper, with a link that names
        # nothing: the case no schema-less reader can judge. The account settles it.
        aside = json.dumps(dict(entry(9, "deeper"), body={"unknown": "member"}, prevLine=nothing)).encode()
        last = json.dumps(dict(entry(2, "last"), prevLine={"method": verifier.METHOD, "value": sha(aside)})).encode()
        data = first + b"\n" + aside + b"\n" + last + b"\n"
        self.write_log(LOG, data)
        recorded = {"method": verifier.METHOD, "head": sha(last), "lines": 3, "linked": True, "unchained": 0, "unchainedLimit": None, "broken": []}
        self.write_heads(**{LOG: dict(recorded, setAside=[2], torn=[])})
        report = verifier.verify(self.root)[2]
        self.assertEqual(report["limited"], [f"{LOG}: line 2 was set aside by the App as invalid: it is not read as a record, and its own link is not examined"])
        self.assertEqual((report["limitedLogs"], report["recomputed"], report["notes"]), (1, 1, []))
        # A set-aside line never reads as a clean pass: its own status and statement.
        ran = self.run_verifier()
        self.assertEqual(ran.returncode, 2, ran.stderr)
        self.assertIn("\nLog integrity: LIMITED. 1 limit in 1 log.", ran.stdout)
        self.assertIn("\n  Integrity limit: runs/run-one/app-writer.jsonl: line 2 was set aside by the App as invalid", ran.stdout)
        for phrase in ("no chain is broken", "lists no line as set aside", "exit status 0", "every check"):
            self.assertNotIn(phrase, ran.stdout)
        # Which lines were set aside is the package's statement, and is marked as that.
        self.assertIn("\n  Which lines the App set aside is the package's own account of what the App's reader did; this verifier relays that account and does not check it.", ran.stdout)
        # The line before a set-aside line is not tied to the head by the chain
        # (the App does not examine a set-aside line's link). The tag's pin on
        # the log's bytes is what shows a change to it, tag unchanged.
        self.write_log(LOG, data.replace(b'"first"', b'"FIRST"'))
        self.seal()
        with self.assertRaisesRegex(verifier.ChainDisagreement, "its bytes .* are not the ones the package's chain-head tag records"):
            verifier.verify(self.root)
        self.assertEqual(self.run_verifier().returncode, 1)
        self.write_log(LOG, data)
        # An account that leaves the line out: this verifier cannot know the
        # App set it aside (its link here names nothing, so it fails; had its
        # link been right it would pass). So a clean result never asserts that
        # no line was set aside, only that the account lists none.
        # The account cannot remove a failure. A line it does not list must
        # link, or its break must be the one recorded:
        self.write_heads(**{LOG: dict(recorded, setAside=[], torn=[])})
        with self.assertRaisesRegex(verifier.ChainDisagreement, r"chain broken at line 2: .*the package records no break there"):
            verifier.verify(self.root)
        # and must be readable:
        junk = first + b"\nnot json at all\n"
        self.write_log(LOG, junk)
        self.write_heads(**{LOG: dict(recorded, head=sha(b"not json at all"), lines=2, setAside=[], torn=[])})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "line 2 is not a readable record, and the package's account does not list it as set aside"):
            verifier.verify(self.root)
        self.write_heads(**{LOG: dict(recorded, head=sha(b"not json at all"), lines=2, setAside=[2], torn=[])})
        self.assertEqual(len(verifier.verify(self.root)[2]["limited"]), 1)
        # Listing a line does not hide its bytes: the tag pins them.
        self.write_log(LOG, first + b"\nnot json at ALL\n")
        self.seal()
        with self.assertRaisesRegex(verifier.ChainDisagreement, "its bytes .* are not the ones the package's chain-head tag records"):
            verifier.verify(self.root)
        # A failure on a package with an account carries no "cannot tell" sentence.
        failed = self.run_verifier()
        self.assertEqual(failed.returncode, 1)
        self.assertNotIn("cannot tell", failed.stderr)
        # A torn line whose naming line the App itself set aside: the App's
        # reader takes the naming from that line whatever it makes of it, so
        # the account lists both and the verifier follows it.
        torn = b'{"torn'
        naming = json.dumps({"kind": "evidence_limit", "unknownMember": True,
                             "body": {"label": verifier.PARTIAL, "subjectRef": f"line 2; {len(torn)} bytes; sha256 {sha(torn)}"}}).encode()
        after = json.dumps(dict(entry(2, "after"), prevLine={"method": verifier.METHOD, "value": sha(naming)})).encode()
        self.write_log(LOG, first + b"\n" + torn + b"\n" + naming + b"\n" + after + b"\n")
        self.write_heads(**{LOG: dict(recorded, head=sha(after), lines=3, setAside=[3], torn=[2])})
        report = verifier.verify(self.root)[2]
        self.assertEqual(report["limited"], [f"{LOG}: line 3 was set aside by the App as invalid: it is not read as a record, and its own link is not examined"])
        self.assertEqual(len(report["notes"]), 1)
        self.assertIn("lists line 2 as a torn line the App closed and set aside", report["notes"][0])
        # A malformed account, or one naming a line the log does not have, fails.
        self.write_log(LOG, data)
        for account in ({"setAside": [2]}, {"setAside": "2", "torn": []}, {"setAside": [2, 2], "torn": []}, {"setAside": [0], "torn": []},
                        {"setAside": [2], "torn": [2]}, {"setAside": [2, 9], "torn": []}, {"setAside": [True], "torn": []},
                        {"setAside": [2], "torn": [], "bytes": len(data) + 0.0}, {"setAside": [2], "torn": [], "bytes": None},
                        {"setAside": [2], "torn": [], "sha256": None}, {"setAside": [2], "torn": [], "sha256": sha(data).upper()}):
            with self.subTest(account=account):
                self.write_heads(**{LOG: dict(recorded, **account)})
                with self.assertRaises(verifier.ChainDisagreement):
                    verifier.verify(self.root)

    def test_a_clean_result_states_only_what_was_checked(self):
        # A line the App sets aside (invalid in its body) that is correctly
        # linked. Faithfully the account lists it. With the entry removed and
        # the tag manifest regenerated, payload untouched, the App's own
        # verification refuses the account; this verifier cannot, and says so:
        # it never asserts that no line was set aside.
        first = json.dumps(dict(entry(1, "first"), prevLine={"method": verifier.METHOD, "value": None})).encode()
        aside = json.dumps(dict(entry(9, "deeper"), body={"label": 7}, prevLine={"method": verifier.METHOD, "value": sha(first)})).encode()
        last = json.dumps(dict(entry(2, "last"), prevLine={"method": verifier.METHOD, "value": sha(aside)})).encode()
        data = first + b"\n" + aside + b"\n" + last + b"\n"
        self.write_log(LOG, data)
        self.write_heads(**{LOG: dict(head(data), setAside=[2])})
        self.assertEqual(self.run_verifier().returncode, 2)
        self.write_heads(**{LOG: head(data)})
        ran = self.run_verifier()
        self.assertEqual(ran.returncode, 0, ran.stderr)
        self.assertNotIn("no line was set aside", ran.stdout)
        self.assertIn("\nLog integrity: no chain is broken, and the package's account lists no line as set aside.", ran.stdout)
        self.assertIn("\nResult: every check this verifier makes passed:", ran.stdout)
        self.assertIn("\nNot checked: this verifier does not hold the record format. It compared each log's bytes with the length and SHA-256 "
                      "the chain-head tag records, recomputed each chain from the lines, and relays the package's own account of the lines "
                      "the App set aside. Only the App's own verification establishes that every line was read as a record.\n", ran.stdout)
        # The same sentence stands on a limited run, and its earlier-profile
        # form on a package without the pin and the account.
        self.write_heads(**{LOG: dict(head(data), setAside=[2])})
        self.assertIn("\nNot checked: this verifier does not hold the record format.", self.run_verifier().stdout)
        self.earlier_profile()
        earlier = self.run_verifier()
        self.assertIn("so this verifier can report no limit where the App reports one, and a change to a line before a line the App set aside "
                      "is not shown by an unchanged tag.", earlier.stdout)
        self.assertNotIn("Exported logs:", earlier.stdout)

    def test_without_an_account_lines_the_app_sets_aside_are_counted_and_their_links_not_examined(self):
        # Each of these the App's reader refuses (record_lines.rs decode_line,
        # serde_json) and counts without examining a link; a faithful package
        # of a store that holds them must not fail here. Every one carries a
        # link that names nothing, which only a line that is read would break on.
        nothing = {"method": verifier.METHOD, "value": "0" * 64}
        # The record, its body and "detail" are three levels; 125 more make 128,
        # one past what the App's JSON reader takes (127).
        deep = "[" * 125 + "]" * 125
        refused = [
            b"{}",
            b"not json at all",
            json.dumps(dict(entry(9, "no kind"), prevLine=nothing, kind="not a kind")).encode(),
            json.dumps({k: v for k, v in dict(entry(9, "no body"), prevLine=nothing).items() if k != "body"}).encode(),
            json.dumps(dict(entry(9, "extra member"), prevLine=nothing, extra=True)).encode(),
            json.dumps(dict(entry(9, "bad link"), prevLine={"method": verifier.METHOD, "value": "short"})).encode(),
            json.dumps(dict(entry(9, "number"), prevLine=nothing)).encode().replace(b'"seq": 9', b'"seq": 1e400'),
            json.dumps(dict(entry(9, "surrogate"), prevLine=nothing)).encode().replace(b'"surrogate"', b'"\\ud800"'),
            # A repeated key whose first value holds the lone surrogate: the
            # App's reader refuses it before the last value would replace it.
            b'{"writtenAt":"\\ud800",' + json.dumps(dict(entry(9, "repeated key"), prevLine=nothing)).encode()[1:],
            json.dumps(dict(entry(9, "deep"), prevLine=nothing)).encode().replace(b'"deep"}', b'"deep", "detail": {"a": ' + deep.encode() + b'}}'),
            json.dumps({"format": verifier.GROUP_FORMAT, "formatVersion": "0.1", "groupId": "grp:invented", "prevLine": nothing,
                        "entries": [entry(5, "group a"), entry(7, "group b")]}).encode(),
            json.dumps({"format": verifier.GROUP_FORMAT, "formatVersion": "0.1", "groupId": "grp:invented", "prevLine": nothing,
                        "entries": [dict(entry(5, "group a"), recordId="rec:same"), dict(entry(6, "group b"), recordId="rec:same")]}).encode(),
        ]
        data, previous = b"", None
        rows = [json.dumps(dict(entry(1, "first"), prevLine={"method": verifier.METHOD, "value": None})).encode()] + refused
        for raw in rows:
            data, previous = data + raw + b"\n", sha(raw)
        last = json.dumps(dict(entry(2, "last"), prevLine={"method": verifier.METHOD, "value": previous})).encode()
        data += last + b"\n"
        self.write_log(LOG, data)
        self.write_heads(version="0.2", **{LOG: {"method": verifier.METHOD, "head": sha(last), "lines": len(rows) + 1, "linked": True, "unchained": 0, "unchainedLimit": None, "broken": []}})
        report = verifier.verify(self.root)[2]
        self.assertEqual(report["limited"], [f"{LOG}: line {no} was set aside by the App as invalid: it is not read as a record, and its own link is not examined"
                                             for no in range(2, len(refused) + 2)])
        self.assertEqual((report["notes"], report["limitedLogs"]), ([], 1))
        # One level fewer is JSON the App reads, so that line's link is examined.
        within = json.dumps(dict(entry(9, "deep"), prevLine=nothing)).encode().replace(b'"deep"}', b'"deep", "detail": {"a": ' + b"[" * 124 + b"]" * 124 + b'}}')
        self.write_log(LOG, rows[0] + b"\n" + within + b"\n")
        self.write_heads(version="0.2", **{LOG: {"method": verifier.METHOD, "head": sha(within), "lines": 2, "linked": True, "unchained": 0, "unchainedLimit": None, "broken": []}})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "chain broken at line 2: it links to"):
            verifier.verify(self.root)
        # A whole, well-formed group is read: its link is examined.
        group = json.dumps({"format": verifier.GROUP_FORMAT, "formatVersion": "0.1", "groupId": "grp:invented", "prevLine": nothing,
                            "entries": [entry(5, "group a"), entry(6, "group b")]}).encode()
        self.write_log(LOG, rows[0] + b"\n" + group + b"\n")
        self.write_heads(version="0.2", **{LOG: {"method": verifier.METHOD, "head": sha(group), "lines": 2, "linked": True, "unchained": 0, "unchainedLimit": None, "broken": []}})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "chain broken at line 2: it links to"):
            verifier.verify(self.root)
        # A torn line the next line names is set aside even when it is JSON,
        # unless it is a whole record (which is read as written).
        named = b"{}"
        limit = json.dumps(dict(entry(2, f"line 2; {len(named)} bytes; sha256 {sha(named)}", label=verifier.PARTIAL),
                                prevLine={"method": verifier.METHOD, "value": sha(rows[0])})).encode()
        self.write_log(LOG, rows[0] + b"\n" + named + b"\n" + limit + b"\n")
        self.write_heads(version="0.2", **{LOG: {"method": verifier.METHOD, "head": sha(limit), "lines": 2, "linked": True, "unchained": 0, "unchainedLimit": None, "broken": []}})
        self.assertIn("line 2 is a torn line the App closed and set aside", verifier.verify(self.root)[2]["notes"][0])

    def test_a_record_invalid_deeper_than_its_top_level_is_the_stated_case_this_verifier_cannot_tell(self):
        # Every top-level member present, and a body the record schema refuses
        # for its kind: the App sets the line aside and examines no link; this
        # verifier, which carries no schema, examines it. The stated limit.
        deeper = json.dumps(dict(entry(2, "deeper"), body={"unknown": "member"}, prevLine={"method": verifier.METHOD, "value": "0" * 64})).encode()
        first = linked([entry(1, "first")])
        self.write_log(LOG, first + deeper + b"\n")
        # The head the App records for it: counted, no break.
        self.write_heads(version="0.2", **{LOG: {"method": verifier.METHOD, "head": sha(deeper), "lines": 2, "linked": True, "unchained": 0, "unchainedLimit": None, "broken": []}})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "chain broken at line 2"):
            verifier.verify(self.root)
        failed = self.run_verifier()
        self.assertEqual(failed.returncode, 1)
        self.assertIn("\nThis package is of a chain-head profile that carries no account of its lines (0.1 or 0.2). "
                      "This verifier reads each record only as far as the top level of the record format.", failed.stderr)
        self.assertIn("this package may be a faithful export: this verifier cannot tell that from an altered line, and the App can.", failed.stderr)
        # A failure that is not about a chain carries no such sentence.
        (self.root / "data/evidence.bin").write_bytes(b"changed")
        other = self.run_verifier()
        self.assertEqual(other.returncode, 1)
        self.assertNotIn("cannot tell", other.stderr)

    def test_recorded_heads_must_cover_exactly_the_payload_logs(self):
        lines = linked([entry(1, "only")])
        self.write_log(LOG, lines)
        self.write_heads(**{LOG: head(lines), "runs/absent.jsonl": head(lines)})
        with self.assertRaisesRegex(ValueError, "runs/absent.jsonl: recorded chain head names no payload log"):
            verifier.verify(self.root)
        self.write_heads(**{LOG: head(lines), "evidence.bin": head(lines)})
        with self.assertRaisesRegex(ValueError, "not a chained log"):
            verifier.verify(self.root)
        self.write_heads(**{LOG: {"state": "unreadable", "error": "invented"}})
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


LOG = "runs/run-one/app-writer.jsonl"
ROLE = "role-supply/observations.jsonl"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def entry(seq, subject, label="unresolvable reference"):
    """An invented record with the top level the record format requires."""
    return {"format": "chirality.rs.record", "formatVersion": "0.1", "recordId": f"rec:invented-{seq}-{abs(hash(subject)) % 10 ** 6}",
            "kind": "evidence_limit", "recorder": {"role": "App writer", "identity": "app-writer:invented"},
            "context": {"surface": "App"}, "seq": seq, "writtenAt": "2026-01-01T00:00:00Z",
            "body": {"label": label, "subjectRef": subject}}


def linked(rows):
    """Invented lines, each linked to the one before as the App writes them; the
    first line of the rows given starts a chain."""
    out, previous = b"", None
    for row in rows:
        raw = json.dumps(dict(row, prevLine={"method": verifier.METHOD, "value": previous})).encode()
        previous = sha(raw)
        out += raw + b"\n"
    return out


def head(data, name="app-writer.jsonl", broken=()):
    """The head the export records for a chain of complete, linked lines
    (record_lines.rs, chain_head)."""
    lines = data.split(b"\n")[:-1]
    return {"method": verifier.METHOD, "head": sha(lines[-1]), "lines": len(lines),
            "linked": True, "unchained": 0, "unchainedLimit": None, "broken": list(broken), "setAside": [], "torn": []}


if __name__ == "__main__":
    unittest.main()
