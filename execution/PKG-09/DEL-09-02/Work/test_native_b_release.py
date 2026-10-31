"""Mocked administrative-release checks; no App, process, signal or UI action."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from types import SimpleNamespace
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('admin_release', Path(__file__).with_name('native_b_release.py'))
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class Reservation:
    def __init__(self):
        self.exit = {'code': os.CLD_EXITED, 'status': 0}
        self.reaped = False
        self.waits = []

    def observe(self):
        if self.reaped:
            raise RuntimeError('original reservation already released')
        return copy.deepcopy(self.exit)

    def administrative_reap(self, expected):
        if self.observe() != expected:
            raise RuntimeError('actual original exit differs')
        self.waits.append(expected)
        self.reaped = True
        return 0


class AdministrativeRelease(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='native-B-admin-test-',
            dir='/Users/ryan/dev/chirality-t3/scratch')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.reported, self.joined = [], []
        self.run = SimpleNamespace(root=self.root, value={'candidate_key': 'invented-candidate'},
            admission_sha='a' * 64, reservation=Reservation(), cleanup=False,
            stop=threading.Event(), supplier_settled=False, generation=None,
            thread=SimpleNamespace(join=lambda timeout: self.joined.append(timeout)))
        self.run.record = lambda name, value: (self.root / name).write_text(json.dumps(value))
        self.run.report = self.reported.append

    def write_control(self, value=None):
        value = release.request_for(self.run) if value is None else value
        path = self.root / release.CONTROL
        path.write_text(json.dumps(value))
        path.chmod(0o600)
        return path

    def assert_not_reaped(self):
        self.assertFalse(self.run.reservation.reaped)
        self.assertEqual(self.run.reservation.waits, [])
        self.assertFalse(self.run.stop.is_set())

    def test_absent_request_is_no_action(self):
        self.assertIsNone(release.release_if_requested(self.run, 'original failure'))
        self.assert_not_reaped()

    def test_actual_normal_exit_then_explicit_release_remains_failed(self):
        request = release.request_for(self.run)
        self.assertEqual(set(request), {'action', 'candidate', 'admission_sha256', 'expected_app_exit'})
        path = self.write_control(request)
        self.assertEqual(release.release_if_requested(self.run, 'main window unavailable'), 1)
        self.assertEqual(self.run.reservation.waits, [{'code': os.CLD_EXITED, 'status': 0}])
        self.assertTrue(self.run.stop.is_set())
        self.assertEqual(self.joined, [8])
        self.assertEqual((self.root / 'administrative-release-request.json').read_bytes(), path.read_bytes())
        result = json.loads((self.root / 'administrative-release-result.json').read_text())
        self.assertFalse(result['success'])
        self.assertTrue(result['administrative_app_reap'])
        self.assertFalse(result['supplier_settled_observed'])
        self.assertIsNone(result['generation'])
        self.assertEqual(result['actual_app_wait_code'], 0)
        self.assertEqual(result['original_error'], 'main window unavailable')

    def test_live_abnormal_or_lost_app_never_offers_or_performs_release(self):
        request = release.request_for(self.run)
        self.write_control(request)
        for observed in (None, {'code': os.CLD_EXITED, 'status': 1},
                         {'code': os.CLD_KILLED, 'status': 9}, {'code': True, 'status': 0}):
            self.run.reservation.exit = observed
            with self.subTest(observed=observed):
                self.assertIsNone(release.request_for(self.run))
                with self.assertRaisesRegex(RuntimeError, 'normal exit'):
                    release.release_if_requested(self.run, 'failed')
                self.assert_not_reaped()
        with patch.object(self.run.reservation, 'observe', side_effect=RuntimeError('lost')):
            self.assertIsNone(release.request_for(self.run))
            with self.assertRaises(RuntimeError):
                release.release_if_requested(self.run, 'failed')
        self.assert_not_reaped()

    def test_wrong_binding_extra_fields_and_boolean_exit_refuse(self):
        original = release.request_for(self.run)
        changes = [dict(original, candidate='foreign'), dict(original, admission_sha256='b' * 64),
                   dict(original, pid=123), dict(original, command='quit'),
                   dict(original, expected_app_exit={'code': os.CLD_EXITED, 'status': False})]
        for request in changes:
            self.write_control(request)
            with self.subTest(request=request), self.assertRaises(RuntimeError):
                release.release_if_requested(self.run, 'failed')
            self.assert_not_reaped()
        self.run.admission_sha = None
        self.assertIsNone(release.request_for(self.run))

    def test_mode_symlink_hardlink_and_foreign_owner_refuse(self):
        path = self.write_control()
        path.chmod(0o644)
        with self.assertRaises(RuntimeError):
            release.release_if_requested(self.run, 'failed')
        path.chmod(0o600)
        twin = self.root / 'invented-hardlink'
        os.link(path, twin)
        with self.assertRaises(RuntimeError):
            release.release_if_requested(self.run, 'failed')
        twin.unlink()
        source = self.root / 'invented-request'
        path.rename(source)
        path.symlink_to(source)
        with self.assertRaises((OSError, RuntimeError)):
            release.release_if_requested(self.run, 'failed')
        path.unlink()
        source.rename(path)
        with patch.object(release.os, 'getuid', return_value=os.getuid() + 1):
            with self.assertRaises(RuntimeError):
                release.release_if_requested(self.run, 'failed')
        self.assert_not_reaped()

    def test_oversize_and_duplicate_json_refuse(self):
        path = self.write_control()
        path.write_text(' ' * 4097)
        with self.assertRaises(RuntimeError):
            release.release_if_requested(self.run, 'failed')
        path.write_text('{"action":"first","action":"second"}')
        with self.assertRaisesRegex(RuntimeError, 'duplicate'):
            release.release_if_requested(self.run, 'failed')
        self.assert_not_reaped()

    def test_intent_failure_precedes_any_reap_and_existing_intent_is_preserved(self):
        self.write_control()
        original_write = release._write_once
        def fail_intent(directory, name, raw):
            if name == 'administrative-release-intent.json':
                raise OSError('invented intent write failure')
            original_write(directory, name, raw)
        with patch.object(release, '_write_once', side_effect=fail_intent):
            with self.assertRaises(OSError):
                release.release_if_requested(self.run, 'failed')
        self.assert_not_reaped()
        first = (self.root / 'administrative-release-request.json').read_bytes()
        with self.assertRaises(FileExistsError):
            release.release_if_requested(self.run, 'failed')
        self.assertEqual((self.root / 'administrative-release-request.json').read_bytes(), first)
        self.assert_not_reaped()

    def test_reporting_or_join_failure_after_reap_never_returns_to_hold(self):
        self.write_control()
        def broken(*_args, **_kwargs):
            raise OSError('invented post-reap failure')
        self.run.thread.join = broken
        self.run.record = broken
        self.run.report = broken
        self.assertEqual(release.release_if_requested(self.run, 'original failure'), 1)
        self.assertTrue(self.run.reservation.reaped)
        self.assertTrue(self.run.stop.is_set())
        self.assertTrue((self.root / 'administrative-release-intent.json').exists())


if __name__ == '__main__':
    unittest.main()
