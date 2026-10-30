"""Focused controller safety regressions; no App, supplier, model or UI."""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('continuation', Path(__file__).with_name('native_setup_continuation.py'))
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)


class Safety(unittest.TestCase):
    def test_slow_AX_stops_at_cleanup_deadline_before_original_child_escalation(self):
        with tempfile.TemporaryDirectory() as temp:
            run = controller.Supervisor(Path(temp), time.monotonic() - 1, time.monotonic() + 12.1)
            run.child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'],
                                         env={'PATH': '/usr/bin:/bin', 'CODEX_HOME': temp})
            class SlowAX:
                def quit_ui(self):
                    while True:
                        time.sleep(0.01)
                        run.alive()  # Each actual AX operation has this callback.
            run.ax = SlowAX()
            started = time.monotonic()
            try:
                run.settle()
                self.assertLess(time.monotonic() - started, 2)
                self.assertTrue(run.forced)
                self.assertIsNotNone(run.child.returncode)
                self.assertIn('native cleanup deadline', (Path(temp) / 'actions.jsonl').read_text())
            finally:
                if run.child.poll() is None:
                    run.child.kill()
                    run.child.wait()

    def test_logging_errors_cannot_bypass_native_failure_or_forced_settlement(self):
        for has_ax in (False, True):
            with self.subTest(has_ax=has_ax), tempfile.TemporaryDirectory() as temp:
                run = controller.Supervisor(Path(temp), time.monotonic() + 10)
                run.child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'],
                                             env={'PATH': '/usr/bin:/bin', 'CODEX_HOME': temp})
                class BrokenAX:
                    def quit_ui(self):
                        raise RuntimeError('native Quit failed')
                run.ax = BrokenAX() if has_ax else None
                try:
                    with patch.object(run, 'log', side_effect=OSError('log volume unavailable')):
                        run.settle()
                    self.assertTrue(run.forced)
                    self.assertIsNotNone(run.child.returncode)
                    self.assertGreaterEqual(len(run.log_errors), 3 if has_ax else 2)
                finally:
                    if run.child.poll() is None:
                        run.child.kill()
                        run.child.wait()

    def test_saved_request_rejects_rebound_sources_and_nonprivate_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            for name in ('account', 'shared', 'project', 'desktop-startup'):
                (root / name).mkdir(mode=0o700)
            (root / 'shared/config.toml').write_text('')
            (root / 'shared/AGENTS.md').write_text('')
            (root / 'shared/skills').mkdir()
            value = {'expected_app_data': str(root), 'native_input_paths': {
                'shared_config': str(root / 'shared/config.toml'), 'shared_agents': str(root / 'shared/AGENTS.md'),
                'shared_skills': str(root / 'shared/skills'), 'project': str(root / 'project')}}
            def ref(path):
                p = Path(path)
                s = p.stat()
                native = {'encoding': 'unix_bytes', 'bytes': list(os.fsencode(p))}
                return {'location': native, 'resolved': native, 'object': {'device': s.st_dev, 'inode': s.st_ino}}
            record = {'version': 1, 'supplier': 'bundled-owner-use-development', 'app_data': ref(root),
                      'account': ref(root / 'account'), 'shared': [ref(value['native_input_paths'][k]) for k in
                      ('shared_config', 'shared_agents', 'shared_skills')], 'project': ref(root / 'project')}
            request = root / 'desktop-startup/request.json'
            controller.write(request, record)
            request.chmod(0o600)
            controller.validate_request(request, root / 'account', value)
            for field, changed in [('version', 2), ('supplier', 'other'), ('project', ref(root / 'account')),
                                   ('shared', list(reversed(record['shared']))), ('account', ref(root / 'project'))]:
                with self.subTest(field=field):
                    controller.write(request, {**record, field: changed})
                    with self.assertRaises(RuntimeError):
                        controller.validate_request(request, root / 'account', value)
            controller.write(request, record)
            request.chmod(0o644)
            with self.assertRaisesRegex(RuntimeError, 'private owned regular file'):
                controller.validate_request(request, root / 'account', value)

    def test_expired_work_and_guard_failure_do_not_prevent_owned_child_cleanup(self):
        with tempfile.TemporaryDirectory() as temp:
            run = controller.Supervisor(Path(temp), time.monotonic() - 1)
            run.reason = 'original guard failure'
            run.child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'],
                                         env={'PATH': '/usr/bin:/bin', 'CODEX_HOME': temp}, start_new_session=True)
            try:
                code = run.settle()
                self.assertIsNotNone(code)
                self.assertTrue(run.forced)
                self.assertEqual(run.reason, 'original guard failure')
                self.assertTrue(run.stop.is_set())
            finally:
                if run.child.poll() is None:
                    run.child.kill()
                    run.child.wait()

    def test_monitor_exception_becomes_guard_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            run = controller.Supervisor(Path(temp), time.monotonic() + 10)
            with patch.object(run, 'sample', side_effect=subprocess.TimeoutExpired('ps', 2)):
                run.monitor()
            self.assertIn('timed out', run.reason)
            run.settle()
            self.assertTrue(run.stop.is_set())

    def test_setup_cannot_reuse_a_changed_historical_namespace_list(self):
        with patch.object(controller.json, 'loads', return_value={}):
            with self.assertRaisesRegex(RuntimeError, 'historical namespace list differs'):
                controller.namespaces()

    @unittest.skipUnless(sys.platform == 'darwin', 'macOS sandbox containment')
    def test_phase_A_policy_shape_denies_fork_and_unlisted_exec(self):
        # Same deny rules, allowing only this Python probe rather than the App.
        # Tests kernel enforcement; no supplier or inherited real home/credentials.
        with tempfile.TemporaryDirectory() as temp:
            policy = '(version 1)(allow default)(deny network*)(deny process-fork)(deny process-exec)'
            policy += '(allow process-exec (literal ' + controller.json.dumps(str(Path(sys.executable).resolve())) + '))'
            probe = '''import os,sys
try:
    pid=os.fork()
except PermissionError:
    pass
else:
    if pid==0: os._exit(2)
    os.waitpid(pid,0)
    sys.exit(3)
try:
    os.execv('/usr/bin/true',['true'])
except PermissionError:
    print('fork and unlisted exec denied')
else:
    sys.exit(4)
'''
            result = subprocess.run(['/usr/bin/sandbox-exec', '-p', policy, str(Path(sys.executable).resolve()), '-c', probe],
                                    env={'PATH': '/usr/bin:/bin', 'HOME': temp, 'CODEX_HOME': temp, 'TMPDIR': temp},
                                    capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), 'fork and unlisted exec denied')


if __name__ == '__main__':
    unittest.main()
