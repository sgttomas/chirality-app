"""B controller regressions: invented files/processes only; no App/supplier/UI."""
import copy
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

spec = importlib.util.spec_from_file_location('successor_B', Path(__file__).with_name('native_successor_relaunch.py'))
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
G = {'appSession': 'invented-session', 'home': 'invented-home', 'spawnCounter': 1}


def observation(bundle, state='ready'):
    supplier = bundle / 'Contents/Resources/codex/bin/codex'
    reply = {'userAgent': 'codex/0.160.0'}
    rows = [{'transitionId': 'LT-09', 'generation': G, 'toState': 'ready', 'supplierStanding': 'unverified-development',
             'versionIdentity': {'observedVersionLabel': 'codex-cli 0.160.0',
                'configurationIdentity': {'launcher': str(supplier)}, 'handshakeReportedIdentity': reply,
                'distributionContentIdentity': [{'path': 'bin/codex', 'identity': {'algorithm': 'sha-256', 'value': b.setup.digest(supplier)}}]}}]
    if state == 'stopped':
        rows.append({'transitionId': 'LT-23', 'generation': G, 'toState': 'stopped',
                     'exitFacts': {'exitCode': 0, 'signal': None, 'forcedAfterGrace': False},
                     'descendants': {'checked': True, 'surviving': 0, 'handling': b.LIMIT}})
    return {'rendered_state': state, 'generation': G, 'rendered_version': 'codex-cli 0.160.0', 'lifecycle': rows,
            'clientRequests': [{'method': 'initialize', 'generation': G, 'requestIdentity': 1,
                                'writeResult': 'written', 'outcome': 'response-observed-result', 'responseReceiptPosition': 1}],
            'envelopes': [{'generation': G, 'position': 1, 'class': 'response', 'frame': {'id': 1, 'result': reply}}]}


class BChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='successor-B-test-', dir=b.T3 / 'scratch')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.bundle = self.root / 'invented.app'
        binary = self.bundle / 'Contents/Resources/codex/bin/codex'
        binary.parent.mkdir(parents=True)
        binary.write_text('invented executable identity only; never execute')
        self.value = {'expected_generation_home': G['home'], 'candidate_key': 'invented-candidate', 'bundle': str(self.bundle), 'executable': str(self.bundle / 'Contents/MacOS/invented')}

    def test_actual_diagnostic_shape_is_parsed_without_synthetic_full_snapshot(self):
        observed = observation(self.bundle)
        parts = ['ready', 'earlier unrelated state', 'State:', 'ready', ' · generation ' + json.dumps(G) + ' · version ',
                 'codex-cli 0.160.0', ' · verification {}',
                 json.dumps({key: observed[key] for key in ('lifecycle', 'clientRequests')}), json.dumps(observed['envelopes'])]
        parsed = b.decode_diagnostics(parts)
        self.assertEqual(b.ready_gate(parsed, self.value), G)
        with self.assertRaisesRegex(RuntimeError, 'header unavailable'):
            b.decode_diagnostics([json.dumps({'state': 'ready', 'generation': G})])

    def test_same_generation_supplier_content_and_correlated_response_required(self):
        observed = observation(self.bundle)
        for mutate in [lambda v: v.update(generation={**G, 'home': 'wrong-account'}),
                       lambda v: v['lifecycle'][0]['versionIdentity']['configurationIdentity'].update(launcher='/wrong'),
                       lambda v: v['envelopes'][0].update(generation={**G, 'spawnCounter': 2}),
                       lambda v: v['clientRequests'][0].update(responseReceiptPosition=2),
                       lambda v: v.update(rendered_state='handshaking')]:
            changed = copy.deepcopy(observed)
            mutate(changed)
            with self.assertRaises(RuntimeError):
                b.ready_gate(changed, self.value)

    def test_prohibited_requests_and_unknown_or_foreign_settlement_refuse(self):
        observed = observation(self.bundle, 'stopped')
        self.assertEqual(b.settlement_gate(observed, G)['exitFacts']['exitCode'], 0)
        for mutate in [lambda v: v['clientRequests'][0].update(method='account/read'),
                       lambda v: v['clientRequests'][0].update(method='thread/start'),
                       lambda v: v['lifecycle'][-1]['exitFacts'].update(exitCode=None, signal=None),
                       lambda v: v['lifecycle'][-1]['exitFacts'].update(exitCode=None, signal=True),
                       lambda v: v['lifecycle'][-1]['descendants'].update(checked=False, surviving=None),
                       lambda v: v['lifecycle'][-1]['descendants'].update(surviving=1),
                       lambda v: v['lifecycle'][-1].update(generation={**G, 'spawnCounter': 2})]:
            changed = copy.deepcopy(observed)
            mutate(changed)
            with self.assertRaises(RuntimeError):
                b.settlement_gate(changed, G)

    @unittest.skipUnless(sys.platform == 'darwin' and hasattr(os, 'WNOWAIT'), 'macOS original-child observation')
    def test_early_exit_remains_unreaped_until_explicit_settlement_and_quit_gate(self):
        child = subprocess.Popen(['/usr/bin/true'], env={'PATH': '/usr/bin:/bin', 'CODEX_HOME': str(self.root)})
        reservation = b.AppReservation(child)
        try:
            deadline = time.monotonic() + 2
            while reservation.observe() is None and time.monotonic() < deadline:
                time.sleep(0.01)
            self.assertIsNotNone(reservation.observe())
            self.assertIsNone(child.returncode, 'WNOWAIT does not reap the original child')
            for settled, quit_requested in [(False, False), (True, False), (False, True)]:
                with self.assertRaisesRegex(RuntimeError, 'no settlement/quit permission'):
                    reservation.reap(settled, quit_requested)
            self.assertIsNone(child.returncode)
            self.assertEqual(reservation.reap(True, True), 0)
            with self.assertRaises(RuntimeError):
                reservation.observe()
        finally:
            # This is only an owned, immediately exiting invented test process.
            child.wait()

    def test_hold_records_unknown_without_reaping_or_stopping_guard(self):
        run = b.Run(self.root, self.value, time.monotonic() - 1)
        class Reservation:
            def observe(self):
                return {'code': os.CLD_EXITED, 'status': 0}
            def reap(self, *_):
                raise AssertionError('must not reap')
        run.reservation = Reservation()
        class EndTest(Exception):
            pass
        with patch.object(b.time, 'sleep', side_effect=EndTest), patch('builtins.print'):
            with self.assertRaises(EndTest):
                run.hold('generation observation lost')
        result = json.loads((self.root / 'held-result.json').read_text())
        self.assertEqual(result['state'], 'held-unknown')
        self.assertTrue(result['overrun'])
        self.assertFalse(result['original_app_reaped'])
        self.assertFalse(run.stop.is_set())
        self.assertTrue((self.root / 'held-heartbeat.jsonl').exists())

    def test_native_stop_settlement_precedes_quit_and_reap(self):
        run = b.Run(self.root, self.value, time.monotonic() + 60)
        actions = []
        state = {'stopped': False, 'quit': False}
        class AX:
            def find(self, role, title):
                return title
            def press(self, item):
                actions.append(item)
                if item == 'confirm-stop':
                    state['stopped'] = True
            def text(self, rows):
                return 'Home: account · App session invented-session · Codex process start 1 · state ready'
            def quit_ui(self):
                self_outer.assertTrue(run.supplier_settled)
                actions.append('quit')
                state['quit'] = True
        class Reservation:
            def observe(self):
                return {'code': os.CLD_EXITED, 'status': 0} if state['quit'] else None
            def reap(self, settled, requested):
                self_outer.assertTrue(settled and requested)
                actions.append('reap')
                return 0
        self_outer = self
        run.ax = AX()
        run.reservation = Reservation()
        run.alive = lambda: None
        run.open_disclosure = lambda *_args, **_kwargs: None
        run.dialog = lambda *_args: ([], 'confirm-stop')
        run.diagnostics = lambda: observation(self.bundle, 'stopped' if state['stopped'] else 'ready')
        self.assertEqual(run.stop_and_quit(G), 0)
        self.assertEqual(actions, ['Stop Codex…', 'confirm-stop', 'quit', 'reap'])

    def test_cleanup_liveness_preserves_reserved_deadline_despite_work_guard_failure(self):
        run = b.Run(self.root, self.value, time.monotonic() + 30)
        class Reservation:
            def observe(self):
                return None
        run.reservation = Reservation()
        run.work_end = time.monotonic() - 1
        run.reason = 'resource guard failed'
        run.note_log_error('disk unavailable')
        with self.assertRaises(RuntimeError):
            run.alive()
        run.cleanup = True
        run.alive()  # Actual reservation + cleanup deadline still enforced.
        run.cleanup_end = time.monotonic() - 1
        with self.assertRaisesRegex(RuntimeError, 'deadline'):
            run.alive()

    def test_explicit_held_cleanup_request_has_no_numeric_or_code_inputs(self):
        run = b.Run(self.root, self.value, time.monotonic() - 1)
        class Reservation:
            def observe(self):
                return None
        run.reservation = Reservation()
        actions = []
        run.cleanup_attempt = lambda: actions.append('source-revalidated-native-cleanup') or 0
        b.write_once(self.root / 'retry-native-cleanup.json', {'action': 'retry-native-cleanup', 'candidate': self.value['candidate_key']})
        with patch('builtins.print'):
            self.assertEqual(run.hold('original observation failure'), 1)
        self.assertEqual(actions, ['source-revalidated-native-cleanup'])
        result = json.loads((self.root / 'recovery-result.json').read_text())
        self.assertFalse(result['success'])
        self.assertEqual(result['original_error'], 'original observation failure')
        self.assertTrue(run.stop.is_set())

    def test_existing_exact_app_refuses_and_repeated_log_errors_remain_bounded(self):
        run = b.Run(self.root, self.value, time.monotonic() + 60)
        rows = '123 1 1024 ' + self.value['executable'] + '\n'
        with patch.object(b.subprocess, 'run'), patch.object(b.subprocess, 'check_output', return_value=rows):
            with self.assertRaisesRegex(RuntimeError, 'existing successor App/supplier'):
                run.sample(admission=True)
        for n in range(100):
            run.note_log_error(str(n) + 'x' * 2000)
        self.assertEqual(len(run.log_errors), 20)
        self.assertTrue(all(len(item) <= 512 for item in run.log_errors))

    def test_lost_stdout_does_not_end_the_held_observer(self):
        run = b.Run(self.root, self.value, time.monotonic() - 1)
        class Reservation:
            def observe(self):
                return None
        run.reservation = Reservation()
        class EndTest(Exception):
            pass
        with patch('builtins.print', side_effect=BrokenPipeError('consumer gone')), \
             patch.object(b.time, 'sleep', side_effect=EndTest):
            with self.assertRaises(EndTest):
                run.hold('AX unavailable')
        self.assertFalse(run.stop.is_set())
        self.assertEqual(run.log_errors, ['consumer gone'])
        self.assertTrue((self.root / 'held-heartbeat.jsonl').exists())

    def test_policy_admits_fork_but_only_exact_app_and_stock_executable(self):
        text = b.policy(self.value)
        self.assertIn('(allow process-fork)', text)
        self.assertNotIn('(deny process-fork)', text)
        self.assertIn('(deny network*)', text)
        self.assertIn('(deny process-exec)', text)
        self.assertIn(str(Path.home() / '.codex'), text)
        self.assertEqual(text.count('(literal '), 2)


if __name__ == '__main__':
    unittest.main()
