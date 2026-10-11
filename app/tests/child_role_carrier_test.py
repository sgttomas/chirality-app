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
