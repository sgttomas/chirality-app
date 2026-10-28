"""The opt-in supplier check must stop its own pipe-holding descendants."""
import importlib.util
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import threading
import time
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch


@unittest.skipUnless(os.name == "posix", "owned process-group cleanup is Unix-only")
class ChildCarrierCleanup(unittest.TestCase):
    def test_exited_leader_with_owned_descendant_holding_stdout(self):
        path = Path(__file__).resolve().parents[1] / "supplier_checks/child_roles.py"
        spec = importlib.util.spec_from_file_location("child_roles", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as root:
            descendant = "import time; time.sleep(60)"
            leader = ("import subprocess,sys; subprocess.Popen([sys.executable,'-c',"
                      + repr(descendant) + "]); print('ready',flush=True)")
            stderr = (Path(root) / "stderr").open("w")
            process = subprocess.Popen([sys.executable, "-c", leader], stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=stderr, text=True,
                                       start_new_session=True)
            reader = threading.Thread(target=process.stdout.read, daemon=True)
            native = module.Native.__new__(module.Native)
            # Retain the OS leader's allocated PID through this regression's
            # watchdog cleanup. Native's wait call is tested separately below;
            # this case tests real same-group pipe-holder termination.
            native.process = SimpleNamespace(pid=process.pid, stdin=process.stdin,
                                             stdout=process.stdout, wait=lambda timeout: None)
            native.reader, native.stderr = reader, stderr
            errors = []

            def close():
                try:
                    native.close()
                except Exception as error:
                    errors.append(error)

            closer = threading.Thread(target=close, daemon=True)
            try:
                self.assertEqual(process.stdout.readline().strip(), "ready")
                # Let the leader exit, keeping it unreaped so its PID/PGID
                # remains allocated until Native has sent all group signals.
                time.sleep(.05)
                reader.start()
                closer.start()
                closer.join(timeout=3)
                self.assertFalse(closer.is_alive(), "checker cleanup blocked on an owned descendant")
                self.assertFalse(reader.is_alive())
                self.assertEqual(errors, [])
            finally:
                if reader.is_alive() or closer.ident is None:
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                process.wait(timeout=5)
                if reader.ident is not None:
                    reader.join(timeout=1)
                if closer.ident is not None:
                    closer.join(timeout=1)
                process.stdin.close()
                process.stdout.close()
                stderr.close()

    def test_failed_reader_cleanup_sends_no_group_signal_after_reap(self):
        path = Path(__file__).resolve().parents[1] / "supplier_checks/child_roles.py"
        spec = importlib.util.spec_from_file_location("child_roles_detached", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        events = []
        native = module.Native.__new__(module.Native)
        native.process = SimpleNamespace(pid=1234, stdin=Mock(), stdout=Mock(),
                                         wait=lambda timeout: events.append("reaped"))
        native.reader = Mock()
        native.reader.is_alive.return_value = True  # A detached holder escaped the owned group.
        native.stderr = Mock()
        with patch.object(module.os, "killpg", side_effect=lambda pid, sig: events.append(sig)):
            with self.assertRaisesRegex(RuntimeError, "cleanup limit"):
                native.close()
        self.assertEqual(events, [signal.SIGTERM, signal.SIGKILL, "reaped"])
        native.process.stdout.close.assert_not_called()  # Closing a locked buffer could block.


class ChildCarrierCollision(unittest.TestCase):
    def setUp(self):
        path = Path(__file__).resolve().parents[1] / "supplier_checks/child_roles.py"
        spec = importlib.util.spec_from_file_location("child_roles_collision", path)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def test_known_standalone_fixture_collision_with_null_agents_withholds_all_app_keys(self):
        # Known synthetic case construction is the reason for withholding.
        # A null agents value by itself proves no generic name availability.
        self.assertEqual(self.module.fixture_role_overrides(
            "standalone-collision", None, Path("unused-app-task.toml")), {})

    def test_known_origin_controls_withhold_all_app_keys_even_when_table_key_is_only_alias(self):
        alias = {"ALIAS": {"description": "Person fixture", "config_file": "person-role.toml"}}
        for case in self.module.ORIGIN_CASES:
            for effective in (None, alias):
                self.assertEqual(self.module.fixture_role_overrides(case, effective, Path("app-task.toml")), {})

    def test_complete_config_currency_oracle_ignores_only_object_key_order(self):
        before = {"origins": {"first": 1, "second": 2}, "config": {"agents": None}}
        reordered = {"config": {"agents": None}, "origins": {"second": 2, "first": 1}}
        self.assertEqual(self.module.unchanged_config_reading(before, reordered),
                         self.module.unchanged_config_reading(before, before))
        for changed in ({"origins": {"first": 1, "second": 3}, "config": {"agents": None}},
                        {"origins": {"first": 1.0, "second": 2}, "config": {"agents": None}},
                        {"origins": {"first": 1, "second": 2}, "config": {"agents": {}}}):
            with self.assertRaisesRegex(AssertionError, "reports standalone-file currency"):
                self.module.unchanged_config_reading(before, changed)

    def test_origin_catalog_requires_actual_role_name_not_only_same_description(self):
        description = "CONTROLLED_DESCRIPTION"
        self.module.assert_origin_catalog("Available roles:\nTASK: {\nCONTROLLED_DESCRIPTION\n}",
                                          [("TASK", description)], [])
        for wrong_name in ("ALIAS", "NOTTASK"):
            with self.assertRaisesRegex(AssertionError, "name/description association missing"):
                self.module.assert_origin_catalog(f"Available roles:\n{wrong_name}: {{\n{description}\n}}",
                                                  [("TASK", description)], [])

    def test_table_collision_and_unknown_native_shape_never_override(self):
        roles = {"TASK": {"description": "Person's definition", "config_file": "person.toml"}}
        self.assertEqual(self.module.fixture_role_overrides("collision", roles, Path("app.toml")), {})
        self.assertEqual(roles["TASK"]["config_file"], "person.toml")
        for unknown in ([], "not a role map", 0):
            with self.assertRaisesRegex(RuntimeError, "unknown; no role override"):
                self.module.fixture_role_overrides("none", unknown, Path("app.toml"))
        supplied = self.module.fixture_role_overrides("none", None, Path("app.toml"))
        self.assertEqual(set(supplied), {"agents.TASK.description", "agents.TASK.config_file"})
        self.assertEqual(supplied["agents.TASK.config_file"], "app.toml")

    def test_selected_executable_allowance_is_exact_and_escaped_without_tree_access(self):
        binary = Path('/Users/synthetic/acquired "café"/codex')
        profile = self.module.fixture_sandbox(binary)
        self.assertIn('(deny file-read* (subpath "/Users"))\n', profile)
        self.assertIn('(allow file-read* (literal "/Users/synthetic/acquired \\"café\\"/codex"))\n', profile)
        self.assertEqual(profile.count('(allow file-read*'), 1)
        self.assertNotIn('(allow file-read* (subpath', profile)
        self.assertIn('(deny network*)', profile)

    def test_native_fixture_home_auth_and_local_oss_survive_cold_reopen_without_parent_env_change(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            (root / "home").mkdir()
            (root / "work").mkdir()
            parent_home = "/synthetic/person/home"
            with patch.dict(self.module.os.environ, {"HOME": parent_home,
                    "CODEX_HOME": "/synthetic/person/codex", "PATH": "/synthetic/path",
                    "OPENAI_API_KEY": "CREDENTIAL-ENV-CANARY",
                    "CODEX_OSS_BASE_URL": "http://nonloopback.invalid"}, clear=True):
                for _ in range(2):  # records_delivery reopens this same home.
                    process = SimpleNamespace(stdout=iter(()))
                    with patch.object(self.module.subprocess, "Popen", return_value=process) as opened:
                        native = self.module.Native(Path("/never-executed/codex"), root, local_oss_port=4321)
                    native.reader.join(timeout=1)
                    native.stderr.close()
                    self.assertFalse(native.reader.is_alive())
                    argv = opened.call_args.args[0]
                    env = opened.call_args.kwargs["env"]
                    self.assertEqual(env["HOME"], str(root / "os-home"))
                    self.assertTrue((root / "os-home").is_dir())
                    self.assertEqual(env["CODEX_HOME"], str(root / "home"))
                    self.assertEqual(env["CODEX_OSS_BASE_URL"], "http://127.0.0.1:4321/v1")
                    self.assertNotIn("OPENAI_API_KEY", env)
                    self.assertEqual(argv[-3:], ["-c", 'cli_auth_credentials_store="file"', "app-server"])
                    self.assertEqual(self.module.os.environ["HOME"], parent_home)
