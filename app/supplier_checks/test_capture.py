#!/usr/bin/env python3
"""Checks of the capture tool's refusals and of the recordings committed at the declared pin.

No supplier is executed. Run from `app/`: python3 supplier_checks/test_capture.py
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import types
import urllib.request
import unittest
from pathlib import Path

import capture
import stub_provider

HERE = Path(__file__).resolve().parent
PIN = "0.167.0"
RECORDINGS = HERE / "recordings" / PIN
CHILD_PROMPT = capture.CHILD_MARKER + ": count the invented files."


def recording(scenario):
    return json.loads((RECORDINGS / (scenario + ".recording.json")).read_bytes())


def spawn_items(value):
    found = []
    if isinstance(value, dict):
        if value.get("type") == "collabAgentToolCall":
            found.append(value)
        for inner in value.values():
            found += spawn_items(inner)
    elif isinstance(value, list):
        for inner in value:
            found += spawn_items(inner)
    return found


def replies(record):
    """[(generation, request frame, reply frame)] for every answered App-side request."""
    requests, out = {}, []
    for row in record["frames"]:
        frame = row["frame"]
        if row["direction"] == "app->codex" and "method" in frame and "id" in frame:
            requests[row["generation"], frame["id"]] = frame
        elif row["direction"] == "codex->app" and "id" in frame and "method" not in frame:
            out.append((row["generation"], requests[row["generation"], frame["id"]], frame))
    return out


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
        return capture.vendor_differences(str(self.vendor), self.inventory)

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
                with self.assertRaisesRegex(capture.Refused, "not a pin of the table"):
                    capture.expected_distribution(pin)
        self.assertEqual(capture.expected_distribution(PIN)["pin"], PIN)
        # Every pin the repository keeps a distribution record for is in the table and is admitted.
        kept = sorted(path.parent.name for path in capture.RESOURCES.glob("*/CANONICAL_DISTRIBUTION.json"))
        self.assertIn(PIN, kept)
        for pin in kept:
            self.assertEqual(capture.expected_distribution(pin)["archive"]["sha256"], capture.PINS[pin]["sha256"])

    def test_a_record_that_is_absent_or_names_another_archive_refuses(self):
        committed = capture.expected_distribution(PIN)
        original, capture.RESOURCES = capture.RESOURCES, Path(self.root.name) / "records"
        try:
            with self.assertRaisesRegex(capture.Refused, "no expected distribution"):
                capture.expected_distribution(PIN)
            (capture.RESOURCES / PIN).mkdir(parents=True)
            for field, value in (("pin", "0.167.2"), ("source_commit", "0" * 40), ("archive", None),
                                 ("archive", dict(committed["archive"], sha256="0" * 64)),
                                 ("archive", dict(committed["archive"], size=1)),
                                 ("package_metadata", {"version": "0.167.2"})):
                with self.subTest(field=field, value=value):
                    (capture.RESOURCES / PIN / "CANONICAL_DISTRIBUTION.json").write_text(
                        json.dumps(dict(committed, **{field: value})))
                    with self.assertRaisesRegex(capture.Refused, "does not name the table's pin and archive"):
                        capture.expected_distribution(PIN)
            (capture.RESOURCES / PIN / "CANONICAL_DISTRIBUTION.json").write_text("[]")
            with self.assertRaisesRegex(capture.Refused, "does not name the table's pin and archive"):
                capture.expected_distribution(PIN)
        finally:
            capture.RESOURCES = original

    def test_a_differing_tree_refuses_without_executing_and_writes_nothing(self):
        with self.assertRaisesRegex(capture.Refused, "differs from the expected 0.167.0 inventory"):
            capture.verified_vendor(str(self.vendor), capture.expected_distribution(PIN))
        out = Path(self.root.name) / "out"
        self.assertEqual(capture.main(["--vendor", str(self.vendor), "--pin", PIN, "--out", str(out), "nv04"]), 2)
        self.assertFalse(out.exists())
        with self.assertRaises(SystemExit), open(os.devnull, "w") as quiet:
            stderr, sys.stderr = sys.stderr, quiet
            try:
                capture.main(["--vendor", str(self.vendor), "--pin", "../../escaped", "--out", str(out), "nv04"])
            finally:
                sys.stderr = stderr
        self.assertFalse(out.exists())


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
        self.assertEqual(capture.metadata_members(self.record), {"entrypoint": "bin/codex", "pathDir": "codex-path"})
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
                with self.assertRaisesRegex(capture.Refused, "of the verified inventory"):
                    capture.metadata_members(record)
                with self.assertRaises(capture.Refused):
                    capture.admitted_path(str(self.vendor), record, "entrypoint")

    def test_an_entrypoint_that_is_not_executable_in_the_inventory_refuses(self):
        self.record["inventory"]["entries"][1]["mode"] = 0o644
        with self.assertRaisesRegex(capture.Refused, "not executable"):
            capture.metadata_members(self.record)

    def test_the_path_is_admitted_again_at_the_moment_of_use(self):
        binary = capture.admitted_path(str(self.vendor), self.record, "entrypoint")
        self.assertEqual(binary, str(self.vendor / "bin/codex"))
        (self.vendor / "bin/codex").write_bytes(b"other")
        with self.assertRaisesRegex(capture.Refused, "no longer equals"):
            capture.admitted_path(str(self.vendor), self.record, "entrypoint")

    def test_a_link_in_place_of_the_entrypoint_or_of_its_directory_refuses(self):
        (self.vendor / "bin/codex").unlink()
        os.symlink(self.vendor.parent / "not-in-inventory", self.vendor / "bin/codex")
        with self.assertRaisesRegex(capture.Refused, "passes through a link"):
            capture.admitted_path(str(self.vendor), self.record, "entrypoint")
        (self.vendor / "bin/codex").unlink()
        (self.vendor / "bin").rmdir()
        os.symlink(self.vendor.parent, self.vendor / "bin")
        with self.assertRaisesRegex(capture.Refused, "passes through a link"):
            capture.admitted_path(str(self.vendor), self.record, "entrypoint")

    def test_the_supplier_environment_is_six_variables_and_its_path_names_only_the_admitted_directory(self):
        homes = []
        for name in ("user-home", "home", "tmp"):
            (self.vendor.parent / name).mkdir()
            homes.append(str(self.vendor.parent / name))
        admitted = capture.admitted_path(str(self.vendor), self.record, "pathDir")
        environment = capture.supplier_environment(admitted, str(self.vendor), *homes)
        self.assertEqual(sorted(environment), ["CODEX_HOME", "HOME", "LANG", "PATH", "TMPDIR", "TZ"])
        self.assertEqual(environment["TZ"], "UTC")
        self.assertEqual(environment["PATH"].split(os.pathsep), [admitted, "/usr/bin", "/bin", "/usr/sbin", "/sbin"])
        outside = str(self.vendor.parent / "not-in-inventory")
        for path_directory in (admitted + os.pathsep + outside, outside, str(self.vendor), "codex-path", ""):
            with self.subTest(path_directory=path_directory):
                with self.assertRaises((capture.Refused, ValueError)):
                    capture.supplier_environment(path_directory, str(self.vendor), *homes)
        with self.assertRaisesRegex(capture.Refused, "HOME"):
            capture.supplier_environment(admitted, str(self.vendor), homes[0] + os.pathsep + outside, *homes[1:])

    def test_the_harness_refuses_metadata_that_escapes_before_anything_can_run(self):
        self.record["package_metadata"]["entrypoint"] = "../not-in-inventory"
        with self.assertRaises(capture.Refused):
            capture.Harness(str(self.vendor), self.record, str(self.vendor.parent / "out"), 1.0)
        self.assertFalse((self.vendor.parent / "out").exists())


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
        return capture.outside_configuration(str(self.work), preference, system or self.absent)

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
                        with self.assertRaisesRegex(capture.Refused, "holds a %s entry" % re.escape(name)):
                            self.check()
                    finally:
                        marker.rmdir()
        (self.base / "project/.git").write_text("gitdir: elsewhere\n")  # a worktree's file counts as well
        with self.assertRaisesRegex(capture.Refused, "holds a .git entry"):
            self.check()

    def test_system_configuration_or_a_managed_preference_refuses(self):
        (self.base / "system").mkdir()
        with self.assertRaisesRegex(capture.Refused, "system configuration"):
            self.check(system=str(self.base / "system"))
        with self.assertRaisesRegex(capture.Refused, "managed preference"):
            self.check(preference=lambda: True)

    def test_a_check_that_cannot_be_made_refuses(self):
        def failing():
            raise OSError("invented")
        with self.assertRaisesRegex(capture.Refused, "could not be checked"):
            self.check(preference=failing)
        with self.assertRaisesRegex(capture.Refused, "managed preference"):
            self.check(preference=lambda: None)  # an answer that is not a plain no
        if os.geteuid() != 0:
            os.chmod(self.base / "project", 0o000)
            with self.assertRaisesRegex(capture.Refused, "could not be checked"):
                self.check()

    @unittest.skipUnless(sys.platform == "darwin", "the supplier reads managed preferences on macOS only")
    def test_the_managed_preference_reading_answers_yes_or_no(self):
        self.assertIn(capture.managed_preference_present(), (True, False))


class ObservationSettles(unittest.TestCase):
    """Nothing observes after the health decision."""

    def test_a_reader_still_running_refuses(self):
        harness = capture.Harness.__new__(capture.Harness)
        release = threading.Event()
        thread = threading.Thread(target=release.wait, daemon=True)
        thread.start()
        harness.gens, harness.SETTLE_SECONDS = [types.SimpleNamespace(number=1, threads=[thread])], 0.05
        try:
            with self.assertRaisesRegex(capture.Refused, "still being read"):
                harness.settle()
        finally:
            release.set()
        thread.join()
        harness.settle()

    def test_the_stub_provider_reports_an_answer_still_in_progress_when_closed(self):
        log = []
        provider = stub_provider.Provider(lambda index, body: ([stub_provider.message("x", "m")], 1.5, "held"), log)
        request = urllib.request.Request("http://127.0.0.1:%d/v1/responses" % provider.port, data=b"{}", method="POST")
        reader = threading.Thread(target=lambda: urllib.request.urlopen(request, timeout=10).read(), daemon=True)
        reader.start()
        for _ in range(100):
            if log:
                break
            time.sleep(0.02)
        self.assertFalse(provider.close(timeout=0.1))
        reader.join(10)
        self.assertTrue(provider.close(timeout=5))

    def test_a_rollout_name_in_another_zone_than_utc_is_named(self):
        epoch = '"createdAt": 1794475811, "updatedAtMs": 1794475811123'
        self.assertEqual(capture.clock_disclosures(epoch + ' "path": "s/rollout-2026-11-12T03-30-11-0193.jsonl"'),
                         ["2026-11-12T03-30-11"])
        self.assertEqual(capture.clock_disclosures(epoch + ' "path": "s/rollout-2026-11-12T09-30-12-0193.jsonl"'), [])
        self.assertEqual(capture.clock_disclosures('"path": "s/rollout-2026-11-12T09-30-12-0193.jsonl"'),
                         ["2026-11-12T09-30-12"])  # no epoch to compare with is not a pass
        self.assertEqual(capture.clock_disclosures(epoch), [])


class SocketWatch(unittest.TestCase):
    @staticmethod
    def lsof(returncode, stdout="", stderr=""):
        return lambda *args, **kwargs: types.SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)

    def test_a_sample_is_taken_only_when_lsof_reports_cleanly(self):
        header = "COMMAND PID PGID USER FD TYPE DEVICE SIZE/OFF NODE NAME\n"
        row = "codex 1 1 u 9u IPv4 0x0 0t0 TCP 127.0.0.1:50000->%s:443 (ESTABLISHED)\n"
        self.assertEqual(capture.socket_peers(1, self.lsof(1)), [])
        self.assertEqual(capture.socket_peers(1, self.lsof(0, header)), [])
        self.assertEqual(capture.socket_peers(1, self.lsof(0, header + row % "127.0.0.1")), ["127.0.0.1"])
        self.assertEqual(capture.socket_peers(1, self.lsof(0, header + row % "203.0.113.7")), ["203.0.113.7"])
        self.assertIsNone(capture.socket_peers(1, self.lsof(2)))
        self.assertIsNone(capture.socket_peers(1, self.lsof(1, stderr="lsof: no pwd entry")))
        self.assertIsNone(capture.socket_peers(1, self.lsof(1, header + row % "127.0.0.1")))

    def test_an_unreadable_process_list_is_not_an_empty_group(self):
        listing = lambda code, out="", err="": (lambda *a, **k: types.SimpleNamespace(returncode=code, stdout=out, stderr=err))
        self.assertEqual(capture.group_members(7, listing(0, "  1\n  7\n  7\n")), 2)
        self.assertEqual(capture.group_members(7, listing(0, "  1\n  3\n")), 0)
        self.assertIsNone(capture.group_members(7, listing(2)))
        self.assertIsNone(capture.group_members(7, listing(0, "")))
        self.assertIsNone(capture.group_members(7, listing(0, "  7\n", "ps: warning")))

    def test_a_sample_that_fails_as_the_process_exits_still_counts_as_failed(self):
        harness = capture.Harness.__new__(capture.Harness)
        harness.gens, harness.events, harness.started = [], [], 0.0
        harness.stop_reason, harness.socket_samples, harness.failed_samples = None, 0, 0
        harness.loopback_peers, harness.samples_by_generation, harness.sample_lock = set(), {}, threading.Lock()
        process = subprocess.Popen(["/bin/sleep", "30"], start_new_session=True)
        done = threading.Event()

        def failing_as_it_exits(group):
            process.kill()
            process.wait()
            done.set()
            return None
        harness.gens.append(types.SimpleNamespace(proc=process, pgid=os.getpgid(process.pid), number=1))
        original, capture.socket_peers = capture.socket_peers, failing_as_it_exits
        try:
            harness.watch_sockets(done)
        finally:
            capture.socket_peers = original
        self.assertEqual((harness.socket_samples, harness.failed_samples), (0, 1))
        self.assertIn("could not take a sample", harness.stop_reason)

    def test_a_failed_sample_or_a_foreign_peer_stops_the_run(self):
        for peers, expected in ((None, "could not take a sample"), (["203.0.113.7"], "non-loopback socket")):
            with self.subTest(peers=peers), tempfile.TemporaryDirectory() as root:
                harness = capture.Harness.__new__(capture.Harness)
                harness.gens, harness.events, harness.started = [], [], 0.0
                harness.stop_reason, harness.socket_samples, harness.failed_samples = None, 0, 0
                harness.loopback_peers, harness.samples_by_generation, harness.sample_lock = set(), {}, threading.Lock()
                process = subprocess.Popen(["/bin/sleep", "30"], start_new_session=True)
                try:
                    harness.gens.append(types.SimpleNamespace(proc=process, pgid=os.getpgid(process.pid), number=1))
                    done = threading.Event()
                    original, capture.socket_peers = capture.socket_peers, lambda group: peers
                    try:
                        watcher = threading.Thread(target=harness.watch_sockets, args=(done,))
                        watcher.start()
                        process.wait(timeout=10)
                    finally:
                        done.set()
                        watcher.join()
                        capture.socket_peers = original
                finally:
                    if process.poll() is None:
                        process.kill()
                self.assertIn(expected, harness.stop_reason)
                self.assertEqual(harness.failed_samples, 1 if peers is None else 0)


STAND_IN = r'''#!%(python)s
"""An invented stand-in for the supplier, for the capture harness's own tests. Not Codex."""
import json, os, sys
MODE = %(mode)r
if sys.argv[1:] == ["--version"]:
    print("codex-cli 9.9.9")
    sys.exit(7 if MODE == "version-exit-7" else 0)
P, C, X, T = "parent-thread-0001", "child-thread-0002", "other-thread-0003", "turn-0001"
ITEM = {"type": "collabAgentToolCall", "id": "call_spawn_1", "tool": "spawnAgent", "senderThreadId": P,
        "prompt": "st5-child-brief-marker: count the invented files."}
def send(message):
    sys.stdout.write(json.dumps(message) + "\n")
    sys.stdout.flush()
def note(method, params):
    send({"jsonrpc": "2.0", "method": method, "params": params})
for line in sys.stdin:
    message = json.loads(line)
    if "id" not in message or "method" not in message:
        continue
    reply = lambda result: send({"jsonrpc": "2.0", "id": message["id"], "result": result})
    method = message["method"]
    if method == "initialize":
        identity = {"opaque": "invented-private-installation"} if MODE == "identity-object" else "invented-id"
        reply({"codexHome": os.environ["CODEX_HOME"], "userAgent": "stand-in/1", "installationId": identity,
               "platformFamily": "unix", "platformOs": "macos", "environment": sorted(os.environ)})
    elif method == "thread/start":
        reply({"thread": {"id": P}})
    elif method == "turn/start":
        reply({"turn": {"id": T}})
        note("item/started", {"threadId": P, "item": dict(ITEM, status="inProgress", receiverThreadIds=[])})
        receivers = [] if MODE == "no-receiver" else [C]
        note("item/completed", {"threadId": P, "item": dict(ITEM, status="completed", receiverThreadIds=receivers)})
        if MODE == "child-first":
            note("turn/completed", {"threadId": C, "turn": {"id": "turn-c"}})
        if MODE != "no-parent-completion":
            note("turn/completed", {"threadId": P, "turn": {"id": T}})
        if MODE == "unrelated-completion":
            note("turn/completed", {"threadId": X, "turn": {"id": "turn-x"}})
        elif MODE not in ("no-child-completion", "child-first"):
            note("turn/completed", {"threadId": C, "turn": {"id": "turn-c"}})
    elif method == "thread/items/list" and MODE == "no-reply":
        pass
    elif method == "thread/turns/list" and MODE == "error-reply":
        send({"jsonrpc": "2.0", "id": message["id"], "error": {"code": -32000, "message": "invented"}})
    else:
        reply({"data": [], "thread": {"id": message.get("params", {}).get("threadId")}})
'''


class HarnessAgainstAStandInSupplier(unittest.TestCase):
    """The whole nv04 path against an invented peer: what the harness refuses to record."""

    def setUp(self):
        self.root = tempfile.TemporaryDirectory()
        self.base = Path(os.path.realpath(self.root.name))
        self.originals = (capture.socket_peers, capture.group_members, capture.scenario_nv04, tempfile.tempdir)
        capture.socket_peers = lambda group: []  # the stand-in opens no socket; lsof is not what is tested here

    def tearDown(self):
        capture.socket_peers, capture.group_members, capture.scenario_nv04, tempfile.tempdir = self.originals
        self.root.cleanup()

    def run_nv04(self, mode):
        vendor = self.base / "vendor"
        (vendor / "bin").mkdir(parents=True)
        (vendor / "codex-path").mkdir()
        (vendor / "bin/codex").write_text(STAND_IN % {"python": sys.executable, "mode": mode})
        os.chmod(vendor / "bin/codex", 0o755)
        (vendor / "codex-package.json").write_text(json.dumps(
            {"version": "9.9.9", "entrypoint": "bin/codex", "pathDir": "codex-path"}))
        import intake
        record = intake.distribution_record(str(vendor), "9.9.9", {
            "url": "https://example.invalid/a", "size": 1, "sha256": "0" * 64, "source_commit": "0" * 40})
        try:
            capture.record_scenario(str(vendor), record, str(self.base / "out"), "nv04", child_hold=0, step_timeout=2)
            code = 0
        except capture.Refused:
            code = 2
        self.assertEqual(sorted(path.name for path in (self.base / "out").glob("*")),
                         ["nv04.recording.json"] if code == 0 else [])
        return code, self.base / "out/nv04.recording.json"

    def test_a_complete_run_is_recorded_with_identities_withheld_and_a_six_variable_environment(self):
        for mode in ("complete", "identity-object"):
            with self.subTest(mode=mode):
                self.tearDown()
                self.setUp()
                code, path = self.run_nv04(mode)
                self.assertEqual(code, 0)
                text = path.read_text()
                self.assertNotIn("invented-private-installation", text)
                self.assertNotIn("invented-id", text)
                self.assertNotIn("stand-in/1", text)
                record = json.loads(text)
                initialize = next(row["frame"]["result"] for row in record["frames"]
                                  if row["direction"] == "codex->app" and "result" in row["frame"])
                self.assertEqual(initialize["installationId"], "<REDACTED-INSTALLATION-ID>")
                # macOS adds __CF_USER_TEXT_ENCODING inside a process itself; nothing else may appear.
                self.assertEqual(sorted(set(initialize["environment"]) - {"__CF_USER_TEXT_ENCODING"}),
                                 ["CODEX_HOME", "HOME", "LANG", "PATH", "TMPDIR", "TZ"])
                self.assertEqual(record["settings_in_effect"]["outside_configuration"]["system_configuration_folder"],
                                 "absent")
                self.assertEqual((record["socket_watch"]["failed_samples"], record["pin"]), (0, "9.9.9"))
                self.assertGreater(record["socket_watch"]["samples"], 0)

    def test_an_observation_that_was_not_made_writes_no_recording(self):
        for mode in ("no-reply", "error-reply", "no-parent-completion", "no-child-completion",
                     "unrelated-completion", "child-first", "no-receiver", "version-exit-7"):
            with self.subTest(mode=mode):
                self.tearDown()
                self.setUp()
                code, path = self.run_nv04(mode)
                self.assertEqual(code, 2)
                self.assertFalse(path.exists())

    def test_a_failed_socket_sample_or_an_unreadable_process_list_writes_no_recording(self):
        for failing in ("socket_peers", "group_members"):
            with self.subTest(failing=failing):
                self.tearDown()
                self.setUp()
                setattr(capture, failing, lambda group: None)
                code, path = self.run_nv04("complete")
                self.assertEqual(code, 2)
                self.assertFalse(path.exists())


    def test_a_sample_in_flight_that_fails_after_the_script_ends_writes_no_recording(self):
        # The watcher's sample of a live generation is held until after the script has ended, then
        # fails. The decision must wait for it: no recording, however the timing falls.
        release, entered, script = threading.Event(), threading.Event(), capture.scenario_nv04

        def held(group):
            if threading.current_thread() is threading.main_thread():
                entered.wait(10)  # the script goes on only once the watcher's sample is in flight
                return []
            entered.set()
            release.wait(10)
            return None

        def then_release(harness):
            try:
                return script(harness)
            finally:
                threading.Timer(0.3, release.set).start()
        capture.socket_peers, capture.scenario_nv04 = held, then_release
        code, path = self.run_nv04("complete")
        self.assertTrue(entered.is_set() and release.is_set())
        self.assertEqual(code, 2)
        self.assertFalse(path.exists())

    def test_scratch_beneath_a_project_refuses_before_the_supplier_runs(self):
        for name in (".git", ".codex"):
            with self.subTest(name=name):
                self.tearDown()
                self.setUp()
                (self.base / "project" / name).mkdir(parents=True)
                (self.base / "project/tmp").mkdir()
                tempfile.tempdir = str(self.base / "project/tmp")
                code, path = self.run_nv04("complete")
                self.assertEqual(code, 2)
                self.assertFalse(path.exists())
                self.assertEqual(list((self.base / "project/tmp").iterdir()), [])


class Redaction(unittest.TestCase):
    def redactor(self, user="example", host="machine.local"):
        return capture.redactor(
            [("/Users/example/x/home", "<HOME>"), ("/Users/example/x", "<SCRATCH>"), ("/Users/example", "<USER-HOME>")],
            user, host)

    def test_paths_host_user_and_identity_values_are_replaced_wherever_they_occur(self):
        redact, leaks, counts = self.redactor()
        frame = {"codexHome": "/Users/example/x/home", "cwd": "/Users/example/x/workspace",
                 "other": "/Users/example/Documents", "owner": "example", "userAgent": "client/1 (machine)",
                 "nested": [{"serverName": "machine.local", "installationId": "invented-private-installation"}],
                 "/Users/example/as-a-key": 1, "text": "on machine, by example; examples stay"}
        redacted = redact(frame)
        self.assertEqual(redacted, {
            "codexHome": "<HOME>", "cwd": "<SCRATCH>/workspace", "other": "<USER-HOME>/Documents",
            "owner": "<USER>", "userAgent": "<REDACTED-USER-AGENT>",
            "nested": [{"serverName": "<REDACTED-HOST>", "installationId": "<REDACTED-INSTALLATION-ID>"}],
            "<USER-HOME>/as-a-key": 1, "text": "on <HOST>, by <USER>; examples stay"})
        self.assertEqual(leaks(json.dumps(redacted)), [])
        self.assertEqual(counts["installation identifier"], 1)

    def test_identity_values_are_replaced_whatever_their_spacing_type_or_nesting(self):
        redact, leaks, _ = self.redactor()
        spaced = json.loads('{"installationId": "invented-private-installation", "serverName" : "host"}')
        self.assertEqual(redact(spaced), {"installationId": "<REDACTED-INSTALLATION-ID>", "serverName": "<REDACTED-HOST>"})
        for value in ({"opaque": "invented-private-installation"}, ["invented-private-installation"], None, 7):
            with self.subTest(value=value):
                redacted = redact({"outer": [{"installationId": value}]})
                self.assertEqual(redacted, {"outer": [{"installationId": "<REDACTED-INSTALLATION-ID>"}]})
                self.assertEqual(leaks(json.dumps(redacted)), [])
        held = redact({"arguments": json.dumps({"userAgent": "client/1", "keep": 1})})
        self.assertEqual(json.loads(held["arguments"]), {"userAgent": "<REDACTED-USER-AGENT>", "keep": 1})
        unchanged = json.dumps({"keep": 1}, indent=2)
        self.assertEqual(redact({"arguments": unchanged}), {"arguments": unchanged})

    def test_text_that_is_not_json_and_names_an_identity_key_is_withheld_whole(self):
        redact, leaks, _ = self.redactor()
        for text in ('log {"installationId" :  "invented-private-installation"} tail',
                     'escaped {\\"userAgent\\":\\"client\\\\\\"x suffix-secret\\"} end'):
            with self.subTest(text=text):
                self.assertEqual(redact({"note": text}), {"note": capture.TEXT_MARKER})
        self.assertEqual(redact("the userAgent is a word here"), "the userAgent is a word here")

    def test_the_final_check_names_a_remembered_identity_value_or_an_unreplaced_identity_key(self):
        redact, leaks, _ = self.redactor()
        redact({"installationId": {"opaque": "invented-private-installation"}})
        self.assertEqual(leaks('{"elsewhere": "invented-private-installation"}'), ["invented-private-installation"])
        self.assertEqual(leaks('{"installationId": {"opaque": "x"}}'), ["installationId not replaced by its marker"])
        self.assertEqual(leaks('{"installationId": "<REDACTED-INSTALLATION-ID>", "userAgent client identity": 2}'), [])

    def test_short_names_are_replaced_and_anything_left_is_reported(self):
        redact, leaks, _ = self.redactor(user="al", host="mb")
        self.assertEqual(redact({"who": "al", "where": "mb", "word": "also male, amber"}),
                         {"who": "<USER>", "where": "<HOST>", "word": "also male, amber"})
        self.assertEqual(leaks("written by al on mb under /Users/example"), ["/Users/example", "mb", "al"])
        self.assertEqual(leaks("also male, amber"), [])


class RecordingsAtThePin(unittest.TestCase):
    def test_each_recording_names_the_pin_and_the_verified_distribution(self):
        expected = capture.expected_distribution(PIN)
        main = next(e for e in expected["inventory"]["entries"] if e["path"] == "bin/codex")
        self.assertEqual(sorted(p.name for p in RECORDINGS.iterdir()),
                         sorted(s + ".recording.json" for s in capture.SCENARIOS))
        for scenario in capture.SCENARIOS:
            with self.subTest(scenario):
                record = recording(scenario)
                self.assertEqual((record["format"], record["scenario"], record["pin"]),
                                 (capture.FORMAT, scenario, PIN))
                identity = record["version_identity"]
                self.assertEqual(identity["version_output"], "codex-cli " + PIN)
                self.assertEqual(identity["binary_sha256"], main["sha256"])
                self.assertEqual(identity["distribution"]["archive_sha256"], expected["archive"]["sha256"])
                self.assertEqual(identity["distribution"]["inventory_manifest_sha256"],
                                 expected["inventory"]["manifest_sha256"])
                self.assertEqual(record["events"][0]["pin"], PIN)
                self.assertIsNone(record["app_candidate"])
                self.assertGreater(record["socket_watch"]["samples"], 0)
                self.assertEqual(record["socket_watch"]["failed_samples"], 0)
                self.assertEqual(sorted(record["socket_watch"]["samples_by_generation"]), ["1", "2"])
                self.assertTrue(all(record["socket_watch"]["samples_by_generation"].values()))
                self.assertEqual(record["socket_watch"]["non_loopback_peers"], [])
                settings = record["settings_in_effect"]
                self.assertEqual(settings["environment"], ["CODEX_HOME", "HOME", "LANG", "PATH", "TMPDIR", "TZ"])
                self.assertEqual((settings["outside_configuration"]["system_configuration_folder"],
                                  settings["outside_configuration"]["managed_preferences"]), ("absent", "absent"))
                self.assertLessEqual(set(record["socket_watch"]["loopback_peers"]), {"127.0.0.1", "::1"})

    def test_frames_are_ordered_and_every_reply_answers_a_recorded_request(self):
        for scenario in capture.SCENARIOS:
            with self.subTest(scenario):
                record = recording(scenario)
                positions, last = {}, -1
                for row in record["frames"]:
                    self.assertEqual(set(row), {"generation", "direction", "position", "t_ms", "redacted", "frame"})
                    key = row["generation"], row["direction"]
                    self.assertEqual(row["position"], positions.get(key, 0) + 1)
                    positions[key] = row["position"]
                    self.assertGreaterEqual(row["t_ms"], last)
                    last = row["t_ms"]
                    self.assertIsInstance(row["frame"], dict)
                self.assertEqual({key[0] for key in positions}, {1, 2})
                replies(record)  # raises KeyError on a reply without its request

    def test_no_local_path_or_address_remains(self):
        pattern = re.compile(r"/Users/|/private/|/var/folders|/home/|[A-Za-z0-9._-]+@[A-Za-z0-9-]+\.[a-z]{2,}")
        for scenario in capture.SCENARIOS:
            with self.subTest(scenario):
                text = (RECORDINGS / (scenario + ".recording.json")).read_text()
                self.assertIsNone(pattern.search(text))
                # A rollout file name in another zone than UTC would state the host's offset.
                self.assertIn("rollout-", text)
                self.assertEqual(capture.clock_disclosures(text), [])

    def test_st5_answer_was_written_and_never_acknowledged_and_nothing_was_re_raised(self):
        for scenario in ("st5", "st5-race"):
            with self.subTest(scenario):
                events = {event["event"]: event for event in recording(scenario)["events"]}
                self.assertEqual(events["answer-written"]["decision"], "accept")
                if scenario == "st5":
                    # Frozen before the write: no acknowledgment can exist. The race is an observation.
                    self.assertFalse(events["acknowledgment-reading"]["serverRequest_resolved_observed"])
                self.assertEqual(events["re-raised-request-reading"]["server_requests_after_resume"], 0)
                self.assertFalse(events["workspace-reading-end"]["marker_folder_exists"])

    def test_nv04_spawn_item_carries_its_prompt_live_and_on_every_history_read_of_the_parent(self):
        record = recording("nv04")
        live = {row["frame"]["method"]: row["frame"]["params"]["item"] for row in record["frames"]
                if row["frame"].get("method") in ("item/started", "item/completed")
                and row["frame"]["params"]["item"].get("type") == "collabAgentToolCall"}
        self.assertEqual(sorted(live), ["item/completed", "item/started"])
        started, completed = live["item/started"], live["item/completed"]
        self.assertEqual((started["prompt"], completed["prompt"]), (CHILD_PROMPT, CHILD_PROMPT))
        self.assertEqual(started["receiverThreadIds"], [])
        self.assertEqual(len(completed["receiverThreadIds"]), 1)
        parent, child = completed["senderThreadId"], completed["receiverThreadIds"][0]
        self.assertEqual(started["senderThreadId"], parent)
        seen = {}
        for generation, request, reply in replies(record):
            thread = request.get("params", {}).get("threadId")
            if request["method"] not in ("thread/read", "thread/turns/list", "thread/items/list"):
                continue
            self.assertIn("result", reply, (generation, request["method"]))
            if thread == parent:
                items = spawn_items(reply["result"])
                self.assertEqual([(i["prompt"], i["senderThreadId"], i["receiverThreadIds"]) for i in items],
                                 [(CHILD_PROMPT, parent, [child])], (generation, request["method"]))
                seen[generation, request["method"]] = True
            else:
                self.assertEqual(thread, child)
                described = reply["result"]["thread"]
                self.assertEqual(described["parentThreadId"], parent)
                self.assertTrue(described["agentNickname"])
                # The scripted spawn call names no role, so none is reported.
                self.assertIsNone(described["agentRole"])
                seen[generation, "child"] = True
        self.assertEqual(sorted(seen), sorted(
            (generation, name) for generation in (1, 2)
            for name in ("thread/read", "thread/turns/list", "thread/items/list", "child")))


if __name__ == "__main__":
    unittest.main()
