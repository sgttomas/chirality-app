"""Invented trace/admission boundary units only. Never native P-03 evidence."""
from contextlib import redirect_stderr
import importlib.util
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V, R = load('verify_p03'), load('run_hosted_p03')
NONCE = 'a' * 32


class TraceBoundaries(unittest.TestCase):
    def rows(self, scenario='positive'):
        g = f'appSession={NONCE};home=fixture-home;spawnCounter=1'
        details = [
            ('IDENTITY', 'processMachine=0;nativeMachine=34404;pointerBytes=8;frequency=1000;experimentEnd=12000;cleanupEnd=18000'),
            ('BOUND', g),
            ('DESCENDANT', 'originalLeaderHandle=true;originalJobMember=true;live=true'),
            *[('REFUSED', s) for s in ('second-bind', 'numeric-pid', 'serialized-pid',
                                      'stale-session', 'stale-home', 'stale-counter')],
            ('STOP_CAUSE', 'cause=explicit-fixture-stop;' + g), ('STDIN_CLOSED', g),
            ('GRACE', 'testMilliseconds=150;leaderSignaled=true;descendantLive=true;originalActive=1'),
            ('PENDING_CAPTURE', g), ('SLOT_REPLACED', g.replace('Counter=1', 'Counter=2')),
            ('REFUSED', 'stale-generation-start'),
            ('PRE_TERMINATE', 'originalDescendantLive=True;successorLive=True'),
            ('TERMINATE_ATTEMPT', 'target=current-slot-negative' if scenario == 'wrong-slot' else 'target=captured-original'),
            ('TERMINATE_RESULT', 'ok=True;error=0;confirmed=false'),
            ('REFUSED', 'success-alone;leader-only;zero-only'),
        ]
        if scenario == 'missing-observation':
            details += [('OBSERVATION_UNKNOWN', 'injected-authoritative-job-query-unavailable;custody-retained=true')]
        else:
            observation = ('originalLeaderSignaled=True;originalDescendantSignaled=True;originalActive=0;successorSignaled=False;successorActive=1') if scenario == 'positive' else (
                'originalLeaderSignaled=True;originalDescendantSignaled=False;originalActive=1;successorSignaled=True;successorActive=0')
            details += [('OBSERVATION', observation)]
        details += [
            ('RETIREMENT', 'CONFIRMED' if scenario == 'positive' else 'UNKNOWN'),
            ('CASE_DONE', scenario + ';elapsedTicks=100'),
            ('CONTROLLER_CLEANUP', 'allRetainedActorsSignaled=true;allOriginalJobsActive=0;caseCompleted=True'),
            ('SAFETY_TERMINATE', 'fixture-cleanup-only'),
            ('SAFETY_CLEANUP', 'retainedControllerSignaled=true;active=0'),
        ]
        return [[str(i * 200 + 1), NONCE, kind, detail] for i, (kind, detail) in enumerate(details)]

    def raw(self, rows):
        return ('\n'.join('\t'.join(r) for r in rows) + '\n').encode('ascii')

    def test_three_distinct_outcomes(self):
        for scenario in ('positive', 'wrong-slot', 'missing-observation'):
            result = V.verify(self.raw(self.rows(scenario)), NONCE, scenario)
            self.assertEqual(result['mechanism_pass'], scenario == 'positive')

    def test_each_event_required_exactly_once(self):
        for index in range(len(self.rows())):
            for duplicate in (False, True):
                rows = self.rows()
                if duplicate:
                    rows.insert(index, rows[index])
                else:
                    del rows[index]
                with self.subTest(index=index, duplicate=duplicate), self.assertRaises(ValueError):
                    V.verify(self.raw(rows), NONCE, 'positive')

    def test_identity_generation_observations_and_cleanup_fail_closed(self):
        mutations = [
            ('IDENTITY', 'nativeMachine=34404', 'nativeMachine=43620'),
            ('BOUND', 'fixture-home', 'other-home'),
            ('PENDING_CAPTURE', 'spawnCounter=1', 'spawnCounter=2'),
            ('PENDING_CAPTURE', NONCE, 'b' * 32),
            ('SLOT_REPLACED', 'spawnCounter=2', 'spawnCounter=1'),
            ('TERMINATE_ATTEMPT', 'captured-original', 'current-slot-negative'),
            ('TERMINATE_RESULT', 'confirmed=false', 'confirmed=true'),
            ('OBSERVATION', 'originalLeaderSignaled=True', 'originalLeaderSignaled=False'),
            ('OBSERVATION', 'originalActive=0', 'originalActive=1'),
            ('OBSERVATION', 'successorSignaled=False', 'successorSignaled=True'),
            ('OBSERVATION', 'successorActive=1', 'successorActive=0'),
            ('CONTROLLER_CLEANUP', 'allOriginalJobsActive=0', 'allOriginalJobsActive=1'),
            ('SAFETY_CLEANUP', 'active=0', 'active=UNKNOWN'),
        ]
        for kind, old, new in mutations:
            rows = self.rows()
            next(r for r in rows if r[2] == kind)[3] = next(r[3] for r in rows if r[2] == kind).replace(old, new)
            with self.subTest(kind=kind, new=new), self.assertRaises(ValueError):
                V.verify(self.raw(rows), NONCE, 'positive')

    def test_negative_controls_cannot_be_promoted(self):
        for scenario in ('wrong-slot', 'missing-observation'):
            with self.assertRaises(ValueError):
                V.verify(self.raw(self.rows(scenario)), NONCE, 'positive')
            rows = self.rows(scenario)
            next(r for r in rows if r[2] == 'RETIREMENT')[3] = 'CONFIRMED'
            with self.assertRaises(ValueError):
                V.verify(self.raw(rows), NONCE, scenario)

    def test_deadlines_and_grace(self):
        rows = self.rows()
        grace = next(i for i, r in enumerate(rows) if r[2] == 'GRACE')
        rows[grace][0] = str(int(rows[grace - 1][0]) + 149)
        with self.assertRaises(ValueError):
            V.verify(self.raw(rows), NONCE, 'positive')
        for kind in ('RETIREMENT', 'SAFETY_CLEANUP'):
            rows = self.rows()
            next(r for r in rows if r[2] == kind)[0] = '18001'
            with self.assertRaises(ValueError):
                V.verify(self.raw(rows), NONCE, 'positive')

    def test_raw_bounds_format_and_nonce(self):
        for raw in (b'', b'x' * (128 * 1024 + 1), b'bad\ttrace\n', self.raw(self.rows()).replace(b'a' * 32, b'b' * 32)):
            with self.assertRaises(ValueError):
                V.verify(raw, NONCE, 'positive')


class Admission(unittest.TestCase):
    def test_non_host_refuses_before_git_scratch_or_execution(self):
        with patch.dict('os.environ', {}, clear=True), patch.object(sys, 'argv', ['probe', '--source-commit', '0' * 40]), \
                patch.object(R.HOST, 'capture') as capture, patch.object(R.HOST, 'bind_sources') as bind, \
                patch.object(Path, 'mkdir') as mkdir, redirect_stderr(io.StringIO()):
            self.assertEqual(R.main(), 1)
            capture.assert_not_called()
            bind.assert_not_called()
            mkdir.assert_not_called()

    def test_bound_verifier_bytes_are_used(self):
        raw = TraceBoundaries().raw(TraceBoundaries().rows())
        result = R.check_trace(raw, (HERE / 'verify_p03.py').read_bytes(), NONCE, 'positive')
        self.assertTrue(result['mechanism_pass'])
        with self.assertRaises(ValueError):
            R.check_trace(raw, b'def verify(*args): raise ValueError("bound bytes")', NONCE, 'positive')


if __name__ == '__main__':
    unittest.main()
