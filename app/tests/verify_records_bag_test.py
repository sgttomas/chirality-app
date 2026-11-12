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

    def run_verifier(self):
        """Runs the package's own carried copy, as a person without the App would."""
        return subprocess.run([sys.executable, str(self.root / "verify.py"), str(self.root)], capture_output=True, text=True)

    LABELS = ("Manifests and inventory:", "Exported log bytes:", "Chains:", "Limits:", "  FOUND by this verifier:",
              "  STATED by the package, not checked here:", "  NOT CHECKED:", "Note. FOUND by this verifier:",
              "Note. STATED by the package, not checked here:", "Not checked by this verifier:", "Result:",
              "Administration snapshot:", "Unsigned:")

    def output(self, status):
        """Runs the carried verifier, expects `status`, and requires every line it
        prints to begin with the name of a check or a label: nothing else is said."""
        ran = self.run_verifier()
        self.assertEqual(ran.returncode, status, ran.stdout + ran.stderr)
        for line in ran.stdout.splitlines():
            self.assertTrue(line.startswith(self.LABELS), line)
        self.assertEqual(ran.stdout == "", status == 1)
        if status == 1:
            first, second = ran.stderr.splitlines()
            self.assertTrue(first.startswith("Result: a check failed (exit status 1). "), ran.stderr)
            self.assertEqual(second, "Not checked by this verifier: anything after the check that failed.")
        return ran.stdout.splitlines() if status != 1 else ran.stderr

    def test_valid_package_with_no_chained_log(self):
        self.assertEqual(verifier.verify(self.root), (1, False, {"profile": "0.3", "logs": 0, "pinned": 0, "recomputed": 0,
                                                                 "found": [], "stated": [], "notChecked": [], "notes": []}))
        lines = self.output(0)
        self.assertEqual(lines[:3], ["Manifests and inventory: agree. 1 payload files and the export tags.",
                                     "Chains: the package holds no chained log.", "Limits: none."])
        self.assertIn("Result: every check this verifier makes passed; no limit listed (exit status 0).", lines)
        self.assertIn("Administration snapshot: none in the package.", lines)

    def test_each_check_is_named_with_its_result_and_exit_status_0_says_what_was_not_checked(self):
        data = linked([entry(1, "first"), entry(2, "second"), entry(3, "third")])
        self.write_log(LOG, data)
        self.write_heads(**{LOG: head(data)})
        self.assertEqual(verifier.verify(self.root)[2], {"profile": "0.3", "logs": 1, "pinned": 1, "recomputed": 1,
                                                         "found": [], "stated": [], "notChecked": [], "notes": []})
        self.assertEqual(self.output(0)[:6], [
            "Manifests and inventory: agree. 2 payload files and the export tags.",
            "Exported log bytes: 1 of 1 chained log equal the length and SHA-256 the chain-head tag records.",
            "Chains: 1 of 1 recomputed from the lines; each recomputed head equals the recorded one.",
            "Limits: none.",
            "Not checked by this verifier: whether each line is a record or an observation the App accepts (this verifier does not hold those "
            "formats); the package's account of which lines the App set aside or closed as torn. To have them checked, verify the package through the App.",
            "Result: every check this verifier makes passed; no limit listed (exit status 0)."])

    def test_a_changed_log_with_the_tag_unchanged_fails_on_its_bytes(self):
        # The second check is an equality on each chained log's exact bytes.
        # Every change below is sealed with regenerated manifests, as someone
        # altering the package would, and the tag is left byte for byte.
        nothing = {"method": verifier.METHOD, "value": "0" * 64}
        records = linked([entry(1, "first"), entry(2, "second")])
        aside = json.dumps(dict(entry(9, "deeper"), body={"label": 7}, prevLine=nothing)).encode() + b"\n"
        role = linked([{"seq": 1, "observationId": "obs:one"}, {"seq": 2, "observationId": "obs:two"}])
        refused = {"state": "unreadable or invalid role supply chain", "error": "invented", "line": 1, "kind": "unreadable line"}
        cases = {
            "a line before a line set aside": (LOG, records + aside, dict(head(records + aside), setAside=[3]), lambda d: d.replace(b'"second"', b'"SECOND"')),
            "the first line": (LOG, records, head(records), lambda d: d.replace(b'"first"', b'"FIRST"')),
            "the last line": ("acts/person.jsonl", records, head(records, "person.jsonl"), lambda d: d.replace(b'"second"', b'"SECOND"')),
            "bytes appended": (LOG, records, head(records), lambda d: d + b" "),
            "an unclosed part added": (LOG, records, head(records), lambda d: d + b'{"unfinished'),
            "the last line removed": (LOG, records, head(records), lambda d: d[:d.rindex(b"\n", 0, -1) + 1]),
            "a blank line added": (LOG, records, head(records), lambda d: d + b"\n"),
            "the registered legacy copy": ("legacy/coordination.rs.jsonl", records, head(records, "coordination.rs.jsonl"), lambda d: d.replace(b'"first"', b'"FIRST"')),
            "a role log the App read": (ROLE, role, head(role, "role supply observations"), lambda d: d.replace(b"obs:two", b"obs:TWO")),
            "a role log the App refused, replaced by one refused the same way": (ROLE, b"not json\n", refused, lambda d: b"{\n"),
        }
        for case, (log, data, recorded, change) in cases.items():
            with self.subTest(case=case):
                self.write_log(log, data)
                self.write_heads(**{log: recorded})
                self.assertIn(self.run_verifier().returncode, (0, 2))
                tag = (self.root / "records-chain-heads.json").read_bytes()
                self.write_log(log, change(data))
                self.seal()
                self.assertEqual((self.root / "records-chain-heads.json").read_bytes(), tag)
                with self.assertRaisesRegex(verifier.ChainDisagreement, "its bytes .* are not the ones the package's chain-head tag records"):
                    verifier.verify(self.root)
                self.assertIn(f"{log}: its bytes", self.output(1))
                (self.root / "data" / log).unlink()
        # A head that does not pin its log, or pins it in another form, fails too.
        self.write_log(LOG, records)
        for member, value in (("bytes", None), ("bytes", float(len(records))), ("bytes", str(len(records))), ("bytes", True),
                              ("sha256", None), ("sha256", sha(records).upper()), ("sha256", 7)):
            with self.subTest(member=member, value=value):
                self.write_heads(**{LOG: dict(head(records), **{member: value})})
                with self.assertRaises(verifier.ChainDisagreement):
                    verifier.verify(self.root)
        self.write_heads()
        with self.assertRaisesRegex(ValueError, "payload log has no recorded chain head"):
            verifier.verify(self.root)

    def test_the_chain_is_recomputed_and_compared_with_every_recorded_fact(self):
        # The third check, with the bytes pinned as they stand: what the tag
        # records for the chain must be what the lines give.
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
                with self.assertRaisesRegex(verifier.ChainDisagreement, f"chain broken at line {line}: {why}.*the package records no break there"):
                    verifier.verify(self.root)
        self.write_log(LOG, lines)
        for fact, value in (("linked", False), ("unchained", 3), ("unchainedLimit", "app-writer.jsonl: unchained (legacy): no line carries a chain link (3 lines)"),
                            ("lines", 4), ("lines", 3.0), ("head", None), ("head", sha(parts[1])), ("method", "another method"), ("linked", 1)):
            with self.subTest(fact=fact, value=value):
                self.write_heads(**{LOG: dict(head(lines), **{fact: value})})
                with self.assertRaises(verifier.ChainDisagreement):
                    verifier.verify(self.root)
        for missing in ("unchained", "broken", "head"):
            self.write_heads(**{LOG: {k: v for k, v in head(lines).items() if k != missing}})
            with self.assertRaises(verifier.ChainDisagreement):
                verifier.verify(self.root)
        # A line that is not a JSON object cannot be followed unless the account sets it aside.
        junk = lines + b"not json at all\n"
        self.write_log(LOG, junk)
        self.write_heads(**{LOG: dict(head(junk), lines=4)})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "line 4 is not a JSON object, and the package's account does not list it as set aside"):
            verifier.verify(self.root)

    def test_a_chain_broken_at_export_is_found_and_listed_only_with_exactly_the_recorded_breaks(self):
        whole = linked([entry(1, "first"), entry(2, "second"), entry(3, "third")])
        first = whole.split(b"\n")[0]
        lines = whole.replace(b'"first"', b'"FIRST"')
        self.write_log(LOG, lines)
        # As the App records it (record_lines.rs, Chain::step): the faithful
        # package of a store whose log was already broken.
        recorded = [f"app-writer.jsonl: chain broken at line 2: it links to \"{sha(first)}\", but the preceding line's identity is {sha(lines.split(b'\n')[0])}; never repaired"]
        self.write_heads(**{LOG: head(lines, broken=recorded)})
        report = verifier.verify(self.root)[2]
        self.assertEqual((report["recomputed"], len(report["found"]), report["stated"], report["notChecked"]), (1, 1, [], []))
        out = self.output(2)
        self.assertEqual(out[2:4], ["Chains: 1 of 1 recomputed from the lines; each recomputed head equals the recorded one.", "Limits: 1."])
        self.assertTrue(out[4].startswith(f"  FOUND by this verifier: {LOG}: chain broken at line 2: it links to"), out[4])
        self.assertTrue(out[4].endswith("never repaired (the package records the same break)"), out[4])
        self.assertIn("Result: every check this verifier makes passed; 1 limit listed (exit status 2).", out)
        # A recorded break the lines do not have, another break at that line, one that cannot be placed, and one recorded twice.
        self.write_log(LOG, whole)
        self.write_heads(**{LOG: head(whole, broken=recorded)})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "records a chain broken at line 2, but the recomputed chain is not broken there"):
            verifier.verify(self.root)
        self.write_log(LOG, lines)
        self.write_heads(**{LOG: head(lines, broken=[recorded[0].replace(sha(first), "0" * 64)])})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "the break the package records at line 2 is not the break its lines give"):
            verifier.verify(self.root)
        for listed in (["broken somewhere"], recorded * 2, [7]):
            self.write_heads(**{LOG: head(lines, broken=listed)})
            with self.assertRaisesRegex(verifier.ChainDisagreement, "cannot compare"):
                verifier.verify(self.root)

    def test_the_account_is_followed_and_what_it_states_is_listed_as_stated_and_not_checked(self):
        nothing = {"method": verifier.METHOD, "value": "0" * 64}
        legacy = json.dumps(entry(1, "legacy")).encode()
        first = json.dumps(dict(entry(2, "first"), prevLine={"method": verifier.METHOD, "value": sha(legacy)})).encode()
        torn = b'{"torn'
        # Line 4 is invalid in its body and carries a link that names nothing:
        # the App counts it and does not examine its link, and says so.
        aside = json.dumps(dict(entry(9, "deeper"), body={"label": 7}, prevLine=nothing)).encode()
        last = json.dumps(dict(entry(3, "last"), prevLine={"method": verifier.METHOD, "value": sha(aside)})).encode()
        data = b"\n".join([legacy, first, torn, aside, b" \t\r", last]) + b"\n" + b'{"unfinished'
        self.write_log(LOG, data)
        recorded = {"method": verifier.METHOD, "head": sha(last), "lines": 4, "linked": True, "unchained": 1, "broken": [],
                    "unchainedLimit": "app-writer.jsonl: unchained (legacy): lines before the first linked line (1) carry no chain link; the chain starts after them",
                    "setAside": [4], "torn": [3]}
        self.write_heads(**{LOG: recorded})
        report = verifier.verify(self.root)[2]
        self.assertEqual(report["found"], [f"{LOG}: partial entry at end (not read): 12 bytes after the last complete line"])
        self.assertEqual(report["stated"], [f"{LOG}: line 4 was set aside by the App as invalid: it is not read as a record, and its own link is not examined"])
        self.assertEqual((report["notChecked"], report["recomputed"]), ([], 1))
        out = self.output(2)
        self.assertIn("Limits: 2.", out)
        self.assertIn(f"  STATED by the package, not checked here: {LOG}: line 4 was set aside by the App as invalid: it is not read as a record, and its own link is not examined", out)
        self.assertIn(f"  FOUND by this verifier: {LOG}: partial entry at end (not read): 12 bytes after the last complete line", out)
        # Not limits, and labelled for what they are.
        self.assertIn(f"Note. STATED by the package, not checked here: {LOG}: line 3 is a torn line the App closed after an interrupted write; it is not counted in the chain", out)
        self.assertIn(f"Note. FOUND by this verifier: {LOG}: 1 lines before the chain starts carry no link", out)
        # A line the account leaves out is examined: here its link names nothing, so the chain is broken there and nothing records it.
        self.write_heads(**{LOG: dict(recorded, setAside=[])})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "chain broken at line 4: .*the package records no break there"):
            verifier.verify(self.root)
        # The account states the unclosed part; one that states none, or another length, disagrees.
        for stated in (None, 3, 12.0):
            self.write_heads(**{LOG: dict(recorded, unclosedEnd=stated)})
            with self.assertRaisesRegex(verifier.ChainDisagreement, "unclosedEnd: the log has"):
                verifier.verify(self.root)
        # A malformed account, or one naming a line the log does not have, fails.
        for account in ({"setAside": None}, {"setAside": "4"}, {"setAside": [4, 4]}, {"setAside": [0]}, {"setAside": [True]},
                        {"setAside": [3]}, {"setAside": [4, 9]}, {"torn": None}, {"torn": [3.0]}):
            with self.subTest(account=account):
                self.write_heads(**{LOG: dict(recorded, **account)})
                with self.assertRaises(verifier.ChainDisagreement):
                    verifier.verify(self.root)
        for missing in ("setAside", "torn"):
            self.write_heads(**{LOG: {k: v for k, v in recorded.items() if k != missing}})
            with self.assertRaisesRegex(verifier.ChainDisagreement, "is missing or malformed"):
                verifier.verify(self.root)

    def test_an_account_that_omits_a_line_is_not_asserted_to_be_complete(self):
        # A line the App sets aside (invalid in its body) that is correctly
        # linked. With its entry removed from the account and the tag manifest
        # regenerated, the App's own verification refuses the account. This
        # verifier cannot: every check it makes passes, and it says the account
        # is not checked. It never says that no line was set aside.
        first = json.dumps(dict(entry(1, "first"), prevLine={"method": verifier.METHOD, "value": None})).encode()
        aside = json.dumps(dict(entry(9, "deeper"), body={"label": 7}, prevLine={"method": verifier.METHOD, "value": sha(first)})).encode()
        last = json.dumps(dict(entry(2, "last"), prevLine={"method": verifier.METHOD, "value": sha(aside)})).encode()
        data = first + b"\n" + aside + b"\n" + last + b"\n"
        self.write_log(LOG, data)
        self.write_heads(**{LOG: dict(head(data), setAside=[2])})
        self.output(2)
        self.write_heads(**{LOG: head(data)})
        out = "\n".join(self.output(0))
        self.assertIn("\nLimits: none.\n", out)
        self.assertIn("the package's account of which lines the App set aside or closed as torn. To have them checked, verify the package through the App.", out)
        for phrase in ("set aside as", "no line was", "intact", "no chain is broken", "agree with", "consistent"):
            self.assertNotIn(phrase, out)

    def test_a_role_log_is_followed_whole_and_one_the_app_refused_is_stated_and_its_chain_not_checked(self):
        lines = linked([{"seq": 1, "observationId": "obs:one"}, {"seq": 2, "observationId": "obs:two"}])
        whole = head(lines, "role supply observations")
        self.write_log(ROLE, lines)
        self.write_heads(**{ROLE: whole})
        report = verifier.verify(self.root)[2]
        self.assertEqual((report["recomputed"], report["found"], report["stated"], report["notChecked"], report["notes"]), (1, [], [], [], []))
        self.output(0)
        # The App takes this log whole or not at all: an account cannot set its lines aside.
        self.write_heads(**{ROLE: dict(whole, setAside=[2])})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "takes this log whole or not at all"):
            verifier.verify(self.root)
        # A log the App could not take at export: its bytes are compared, what
        # the package says of it is listed as stated, and its chain as not checked.
        self.write_log(ROLE, lines + b"not json\n")
        self.write_heads(**{ROLE: {"state": "unreadable or invalid role supply chain", "error": "invented", "line": 3, "kind": "unreadable line"}})
        report = verifier.verify(self.root)[2]
        self.assertEqual((report["pinned"], report["recomputed"], report["found"]), (1, 0, []))
        self.assertEqual(report["stated"], [f"{ROLE}: the App could not read this log's chain at line 3 (unreadable line) (unreadable or invalid role supply chain: invented)"])
        self.assertEqual(report["notChecked"], [f"{ROLE}: its chain"])
        out = self.output(2)
        # Nothing is said of agreement where no head was compared.
        self.assertEqual(out[1:4], ["Exported log bytes: 1 of 1 chained log equal the length and SHA-256 the chain-head tag records.",
                                    "Chains: 0 of 1 recomputed from the lines.", "Limits: 2."])
        self.assertIn("; the chain of 1 log. To have them checked, verify the package through the App.", "\n".join(out))
        # A refusal that records no line is relayed without one.
        self.write_heads(**{ROLE: {"state": "unreadable or invalid role supply chain", "error": "invented"}})
        self.assertEqual(verifier.verify(self.root)[2]["stated"], [f"{ROLE}: the App could not read this log's chain (unreadable or invalid role supply chain: invented)"])
        # A record log recorded as unreadable disagrees: its copy is readable here.
        self.write_log(LOG, linked([entry(1, "only")]))
        self.write_heads(**{LOG: {"state": "unreadable", "error": "invented"}, ROLE: {"state": "unreadable or invalid role supply chain", "error": "invented"}})
        with self.assertRaisesRegex(verifier.ChainDisagreement, "recorded at export as unreadable"):
            verifier.verify(self.root)

    def test_for_an_earlier_profile_only_the_manifests_are_checked_and_every_chain_is_listed_as_not_checked(self):
        records = linked([entry(1, "first"), entry(2, "second")])
        role = linked([{"seq": 1, "observationId": "obs:one"}])
        self.write_log(LOG, records)
        self.write_log(ROLE, role)
        earlier = {k: v for k, v in head(records).items() if k not in ("setAside", "torn")}
        for version, heads in (("0.2", {LOG: earlier, ROLE: {k: v for k, v in head(role, "role supply observations").items() if k not in ("setAside", "torn")}}),
                               ("0.1", {LOG: earlier})):
            with self.subTest(version=version):
                self.write_heads(version=version, **heads)
                report = verifier.verify(self.root)[2]
                self.assertEqual((report["pinned"], report["recomputed"], report["found"], report["stated"]), (0, 0, [], []))
                self.assertEqual(report["notChecked"], [f"{ROLE}: its chain", f"{LOG}: its chain"])
                out = self.output(2)
                self.assertEqual(out[:3], ["Manifests and inventory: agree. 3 payload files and the export tags.",
                                           f"Chains: not checked by this verifier for a package of profile {version}; verify through the App.", "Limits: 2."])
                self.assertIn(f"Not checked by this verifier: the chain of 2 chained logs (the tag's profile, {version}, records neither a log's bytes "
                              "nor an account of its lines), and whether each line is a record the App accepts. To have them checked, verify the package through the App.", out)
                # So for such a package a changed line with regenerated manifests
                # is not shown here: the result is the same, and it says why.
                self.write_log(LOG, records.replace(b'"first"', b'"FIRST"'))
                self.seal()
                self.assertEqual(self.output(2), out)
                self.write_log(LOG, records)
                # The tag must still cover exactly the payload's chained logs.
                self.write_heads(version=version)
                with self.assertRaisesRegex(ValueError, "payload log has no recorded chain head"):
                    verifier.verify(self.root)
        self.write_heads(version="0.4", **{LOG: earlier})
        with self.assertRaisesRegex(ValueError, "unsupported chain-head tag profile"):
            verifier.verify(self.root)

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
