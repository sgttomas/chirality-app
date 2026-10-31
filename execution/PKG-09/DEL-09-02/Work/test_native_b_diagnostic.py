"""Pure mocked diagnostics; no native APIs, App, supplier or permission probes."""
import copy
import hashlib
import importlib.util
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('B_diagnostic', Path(__file__).with_name('native_b_diagnostic.py'))
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)


class Reservation:
    reaped = False
    def __init__(self):
        self.child = SimpleNamespace(pid=123)
        self.exit = None
    def observe(self):
        return self.exit


class Backend:
    def __init__(self, identity):
        self.identities = [identity]
        self.closed = False
        self.access = False
        self.decoded = []
        self.roles = []
        self.foreign_references = False
        self.references = ['app', 'window', 'window']
        self.error = 0
    def identity(self, pid):
        return self.identities.pop(0) if len(self.identities) > 1 else self.identities[0]
    def close(self): self.closed = True
    def screen_access(self): return self.access
    def window_rows(self): return ['foreign-sensitive', 'own']
    def owner_pid(self, row): return 123 if row == 'own' else 456
    def decode_owned_window(self, row, access):
        if row != 'own': raise AssertionError('foreign metadata must never be decoded')
        self.decoded.append(row)
        return {'number': 7, 'layer': 0, 'bounds': {'X': 0, 'Y': 0, 'Width': 10, 'Height': 10},
                'on_screen': False, 'title_key_present': False, 'title': None}
    def app(self, pid): return 'app'
    def element_type(self, element): return {'id': 9, 'name': 'AXUIElement'}
    def owner(self, element):
        return (0, 456) if self.foreign_references and element != 'app' else (0, 123)
    def equal(self, left, right): return left == right
    def attribute(self, element, name):
        if name == 'AXRole':
            self.roles.append(element)
            return {'return_code': 0, 'type': {'id': 7, 'name': 'CFString'},
                    'value': 'AXApplication' if element == 'app' else 'AXWindow'}, []
        return {'return_code': self.error, 'type': {'id': 3, 'name': 'CFArray'}, 'value': None}, ([] if self.error else list(self.references))


class DiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='native-diagnostic-test-', dir='/Users/ryan/dev/chirality-t3/scratch')
        self.addCleanup(self.temp.cleanup)
        self.executable = Path(self.temp.name) / 'not-executed'
        self.executable.write_bytes(b'invented bytes, never executed')
        self.run = SimpleNamespace(reservation=Reservation(), value={
            'executable': str(self.executable), 'executable_sha256': hashlib.sha256(self.executable.read_bytes()).hexdigest(),
            'candidate_key': 'invented'})
        self.identity = {'pid': 123, 'ppid': os.getpid(), 'uid': os.getuid(), 'ruid': os.getuid(),
                         'start_sec': 10, 'start_usec': 3, 'executable': str(self.executable)}
        self.backend = Backend(self.identity)
    def capture(self): return d.capture(self.run, lambda: self.backend)

    def test_filters_foreign_windows_before_any_metadata_and_preserves_absent_title(self):
        observed = self.capture()
        self.assertEqual(self.backend.decoded, ['own'])
        self.assertNotIn('foreign-sensitive', str(observed))
        self.assertFalse(observed['window_server']['screen_capture_preflight_access'])
        self.assertFalse(observed['window_server']['rows'][0]['title_key_present'])
        self.assertIsNone(observed['window_server']['rows'][0]['title'])
        self.assertTrue(self.backend.closed)

    def test_self_reference_and_duplicate_are_bounded_not_recursed(self):
        observed = self.capture()['accessibility']['attributes']
        self.assertEqual(len(observed), 4)
        for row in observed:
            self.assertTrue(row['references'][0]['application_self_reference'])
            self.assertTrue(row['references'][2]['duplicate_reference'])
        self.assertEqual(self.backend.roles.count('window'), 4)

    def test_raw_error_and_type_are_retained_without_inventing_missing_window(self):
        self.backend.error = -25212
        observed = self.capture()['accessibility']['attributes']
        self.assertEqual([row['return_code'] for row in observed], [-25212] * 4)
        self.assertEqual(observed[0]['type'], {'id': 3, 'name': 'CFArray'})
        self.assertEqual(observed[0]['references'], [])

    def test_changed_birth_between_windowserver_and_ax_refuses(self):
        changed = dict(self.identity, start_usec=4)
        self.backend.identities = [self.identity, changed]
        with self.assertRaisesRegex(RuntimeError, 'changed across WindowServer'):
            self.capture()
        self.assertEqual(self.backend.roles, [])
        self.assertTrue(self.backend.closed)

    def test_changed_path_parent_uid_or_hash_refuses_before_window_inventory(self):
        for key, value in [('executable', '/other'), ('ppid', 99), ('uid', os.getuid() + 1), ('ruid', os.getuid() + 1)]:
            with self.subTest(key=key):
                self.backend = Backend(dict(self.identity, **{key: value}))
                with self.assertRaises(RuntimeError): self.capture()
                self.assertEqual(self.backend.decoded, [])
        self.backend = Backend(self.identity)
        self.run.value['executable_sha256'] = '0' * 64
        with self.assertRaisesRegex(RuntimeError, 'content differs'): self.capture()
        self.assertEqual(self.backend.decoded, [])

    def test_exited_child_refuses_without_pid_fallback(self):
        self.run.reservation.exit = {'code': 1, 'status': 0}
        with self.assertRaisesRegex(RuntimeError, 'exited during diagnostic'): self.capture()
        self.assertEqual(self.backend.decoded, [])
        self.assertFalse(self.backend.closed, 'factory is not invoked for an exited child')

    def test_foreign_ax_reference_refuses_before_role_read(self):
        self.backend.foreign_references = True
        observed = self.capture()
        self.assertIn('ownership unavailable or foreign', observed['accessibility']['error'])
        self.assertEqual(len(observed['window_server']['rows']), 1)
        self.assertNotIn('window', self.backend.roles)

    def test_reference_and_owned_window_limits(self):
        self.backend.references = ['window'] * (d.MAX_AX_REFERENCES + 1)
        observed = self.capture()
        self.assertIn('references exceed bound', observed['accessibility']['error'])
        self.assertEqual(len(observed['window_server']['rows']), 1)
        self.backend = Backend(self.identity)
        self.backend.window_rows = lambda: ['own'] * (d.MAX_OWN_WINDOWS + 1)
        with self.assertRaisesRegex(RuntimeError, 'rows exceed bound'): self.capture()
        self.assertEqual(len(self.backend.decoded), d.MAX_OWN_WINDOWS)

    def test_changed_identity_after_ax_refuses(self):
        self.backend.identities = [self.identity, self.identity, dict(self.identity, start_sec=11)]
        with self.assertRaisesRegex(RuntimeError, 'changed across AX'): self.capture()
        self.assertTrue(self.backend.closed)

    def test_deadline_and_total_window_bound_refuse_without_decoding(self):
        with patch.object(d.time, 'monotonic', side_effect=[0, 9]):
            with self.assertRaisesRegex(RuntimeError, 'deadline'): self.capture()
        self.assertEqual(self.backend.decoded, [])
        self.backend = Backend(self.identity)
        self.backend.window_rows = lambda: ['foreign-sensitive'] * (d.MAX_WINDOWS + 1)
        with self.assertRaisesRegex(RuntimeError, 'list exceeds bound'): self.capture()
        self.assertEqual(self.backend.decoded, [])

    def test_no_native_factory_when_reservation_missing_or_stop_reason(self):
        from unittest.mock import Mock
        factory=Mock(side_effect=AssertionError('must not load native frameworks'))
        self.run.reservation=None
        with self.assertRaises(RuntimeError):d.capture(self.run,factory)
        factory.assert_not_called()
        self.run.reservation=Reservation();self.run.reason='exclusive pending'
        with self.assertRaisesRegex(RuntimeError,'skipped'):d.capture(self.run,factory)
        factory.assert_not_called()

    def test_timeout_is_set_on_each_child_before_remote_reads(self):
        events=[]
        backend=d.NativeBackend.__new__(d.NativeBackend)
        backend.kind=lambda value: {'name':'AXUIElement','id':9}
        backend.string=lambda value: value
        backend.a=SimpleNamespace(
            AXUIElementSetMessagingTimeout=lambda element,seconds: events.append(('timeout',element,seconds)) or 0,
            AXUIElementGetPid=lambda element,out: events.append(('owner',element)) or -25202,
            AXUIElementCopyAttributeValue=lambda element,name,out: events.append(('attribute',element,name)) or -25212)
        backend.owner(123);backend.attribute(123,'AXRole')
        self.assertEqual(events,[('timeout',123,0.5),('owner',123),('timeout',123,0.5),('attribute',123,'AXRole')])

    def test_precreated_application_and_single_attribute_use_real_inventory_path(self):
        self.backend.app=lambda pid: (_ for _ in ()).throw(AssertionError('must reuse supplied reference'))
        result=d.ax_inventory(self.backend,123,application='app',attributes=('AXWindows',))
        self.assertEqual(len(result['attributes']),1)
        self.assertEqual(result['attributes'][0]['attribute'],'AXWindows')
        self.assertTrue(result['attributes'][0]['references'][0]['application_self_reference'])
        with self.assertRaisesRegex(RuntimeError,'subset'):
            d.ax_inventory(self.backend,123,application='app',attributes=('foreign-attribute',))


if __name__ == '__main__':
    unittest.main()
