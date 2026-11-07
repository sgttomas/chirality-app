"""Injected fake OS/session/time/stream adapters only.

No native framework loading, capture, input, App launch or process/resource
probe. The exact reviewed core and owned-window reader are loaded through the
tool's hash-checked loaders; both are inert on import.
"""
from datetime import datetime, timedelta, timezone
import contextlib
import importlib.util
import io as stdio
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock

import native_visual_session as nvs

WORK = Path(__file__).resolve().parent
core = nvs.load_core(WORK)
reader = nvs.load_reader(WORK)
BASE = datetime(2026, 11, 7, 12, 0, 0, tzinfo=timezone.utc)
PID = 4242
MAIN = {'number': 7.0, 'layer': 0.0, 'bounds': {'X': 100.0, 'Y': 100.0, 'Width': 800.0, 'Height': 600.0},
        'on_screen': True, 'title_key_present': True, 'title': 'Chirality'}
RETINA = {'display': 1, 'bounds': [0.0, 0.0, 1512.0, 982.0], 'mode_points': [1512, 982], 'mode_pixels': [3024, 1964]}


def subject(app_data='/invented/Library/Application Support/dev.invented.test'):
    return core.Subject('eaf-source', '/invented/Test.app', 'dev.invented.test',
                        '/invented/Test.app/Contents/MacOS/app', 'a' * 64, nvs.EXACT_PROJECT, app_data)


IDENTITY = {'pid': PID, 'ppid': 1, 'uid': 501, 'ruid': 501, 'start_sec': 10, 'start_usec': 20,
            'executable': '/invented/Test.app/Contents/MacOS/app'}


class Time:
    def __init__(self):
        self.t = 1000.0

    def clock(self):
        return self.t

    def utc(self):
        return BASE + timedelta(seconds=self.t - 1000.0)

    def sleep(self, seconds):
        assert seconds >= 0
        self.t += seconds


class Commands:
    """Lines, callables, 'EOF'; an exhausted queue idles until the offered timeout."""
    def __init__(self, time, items):
        self.time, self.items, self.reads = time, list(items), 0

    def read(self, timeout):
        self.reads += 1
        if not self.items:
            self.time.t += timeout
            return nvs.LineReader.TIMEOUT
        item = self.items.pop(0)
        if callable(item):
            item = item()
        if item == 'EOF':
            return nvs.LineReader.EOF
        return item if isinstance(item, bytes) else json.dumps(item).encode()


class Output:
    def __init__(self, fail=False):
        self.lines, self.fail = [], fail

    def write(self, value):
        if self.fail:
            raise nvs.SessionStop('operator output unavailable')
        self.lines.append(json.loads(json.dumps(value)))

    def events(self):
        return [line.get('event') or line.get('op') or ('refused' if line.get('ok') is False else None)
                for line in self.lines]


class Backend:
    """Window/identity backend for the reused reader; foreign rows decode -> failure."""
    def __init__(self):
        self.rows = [{'owner': 999, 'decoded': None}, {'owner': PID, 'decoded': json.loads(json.dumps(MAIN))}]
        self.birth = dict(IDENTITY)
        self.closed = 0

    def screen_access(self):
        return True

    def window_rows(self):
        return list(self.rows)

    def owner_pid(self, row):
        return row['owner']

    def decode_owned_window(self, row, access):
        assert row['owner'] == PID, 'foreign row decoded'
        return json.loads(json.dumps(row['decoded']))

    def identity(self, pid):
        assert pid == PID
        return dict(self.birth)

    def close(self):
        self.closed += 1


class IO:
    def __init__(self, time, subject_):
        self.time, self.subject = time, subject_
        self.events, self.identity, self.pending_launch = [], None, False
        self.backend, self.appkit = Backend(), None
        self.evidence_errors = []
        self.terminations, self.absent_after_terminate, self.absent_never = 0, True, False
        self.terminate_error, self.admit_seconds, self.wrong = None, 0, False
        self.holds = []

    def admit(self, subject_):
        self.events.append('admit')
        self.time.t += self.admit_seconds

    def launch_once(self, subject_):
        self.events.append('launch')
        self.identity = dict(IDENTITY)
        return dict(IDENTITY)

    def bind_cleanup(self, identity, subject_):
        self.events.append('bind-cleanup')

    def check(self, identity):
        if self.wrong or identity != self.identity:
            raise core.Refusal('original birth/UID/path/PGID changed')

    def supplier_started(self):
        return False

    def normal_terminate(self, identity, subject_):
        self.terminations += 1
        self.events.append('terminate')
        if self.terminate_error:
            raise self.terminate_error
        return True

    def absent(self, identity):
        if self.absent_never:
            return False
        return bool(self.terminations and self.absent_after_terminate) or self.wrong

    def launch_unknown(self):
        return self.pending_launch or self.identity is not None

    def hold_until_absent(self, result):
        self.holds.append(dict(result))
        self.absent_never = False
        self.absent_after_terminate = True
        self.terminations = max(self.terminations, 1)  # late actual absence in this fake

    def verify_saved(self, subject_, locations):
        return core.NativeSession(subject_, {}, lambda *a: None).verify_saved(subject_, locations)


class Adapter:
    def __init__(self):
        self.pre = {'screen_capture': True, 'post_event': True, 'ax_trusted': True}
        self.front = {'correspondence': None, 'active': True, 'frontmost_pid': PID}
        self.geo = json.loads(json.dumps(RETINA))
        self.pixels = (3024, 1964)
        self.posts, self.released, self.activations, self.allocated = [], [], 0, 0
        self.post_error_on, self.fail_event_at, self.release_error = None, None, False
        self.closed = 0

    def preflight(self):
        return dict(self.pre)

    def foreground(self, identity):
        value = dict(self.front)
        if value['correspondence'] is None:
            value['correspondence'] = {'pid': identity['pid'], 'bundle_identifier': 'dev.invented.test',
                                       'executable': '/invented/Test.app/Contents/MacOS/app'}
        return value

    def geometry(self):
        return json.loads(json.dumps(self.geo))

    def capture(self, number, timeout):
        assert 0 < timeout <= nvs.CAPTURE_TIMEOUT
        return {'path': f'/private/frames/frame-{number:03d}.png', 'sha256': f'{number:064x}', 'pixels': self.pixels}

    def activate(self, identity, expected, before_dispatch=lambda: None):
        before_dispatch()
        self.activations += 1
        assert expected['pid'] == identity['pid'] == PID
        return True

    def source(self):
        self.allocated += 1
        return 'source'

    def event(self, source, spec, down):
        self.allocated += 1
        if self.fail_event_at == self.allocated:
            return None
        return (spec, down, self.allocated)

    def post(self, pid, event):
        self.posts.append((pid, event[0], event[1]))
        if self.post_error_on is not None and len(self.posts) == self.post_error_on:
            raise OSError('post failed')

    def release(self, value):
        self.released.append(value)
        if self.release_error:
            raise OSError('release failed')

    def close(self):
        self.closed += 1


class Journal:
    def __init__(self, fail=()):
        self.rows, self.fail = [], set(fail)

    def __call__(self, kind, value):
        if kind in self.fail:
            raise OSError('journal unavailable: ' + kind)
        self.rows.append((kind, json.loads(json.dumps(value, default=str))))

    def kinds(self):
        return [k for k, _ in self.rows]


def make(items=(), owner_seconds=3600, subject_=None, journal=None, output=None):
    time = Time()
    subj = subject_ or subject()
    io, adapter = IO(time, subj), Adapter()
    journal = journal or Journal()
    output = output or Output()
    factory_calls = []

    def factory():
        factory_calls.append(1)
        return adapter
    commands = Commands(time, items)
    session = nvs.VisualSession(core, subj, io, factory, reader, journal, BASE + timedelta(seconds=owner_seconds),
                                commands, output, time.clock, time.utc, time.sleep)
    return session, io, adapter, journal, output, commands, factory_calls, time


CAP = {'op': 'capture'}


class InertAndSourceBinding(unittest.TestCase):
    def test_import_and_help_perform_no_os_work(self):
        spec = importlib.util.spec_from_file_location('nvs_inert_copy', WORK / 'native_visual_session.py')
        module = importlib.util.module_from_spec(spec)
        self.addCleanup(sys.modules.pop, 'nvs_inert_copy', None)
        sys.modules['nvs_inert_copy'] = module
        with mock.patch('ctypes.CDLL', side_effect=AssertionError('native load on import')), \
                mock.patch('subprocess.run', side_effect=AssertionError('process on import')):
            spec.loader.exec_module(module)
            with mock.patch.object(module, 'load_core', side_effect=AssertionError('help loaded core')), \
                    contextlib.redirect_stdout(stdio.StringIO()) as out, self.assertRaises(SystemExit) as exit_:
                module.main(['--help'])
        self.assertEqual(exit_.exception.code, 0)
        self.assertIn('--owner-window-end', out.getvalue())

    def test_exact_source_hashes_and_tamper_refusal(self):
        self.assertEqual(nvs.sha256((WORK / 'j1_stage_a_phase.py').read_bytes()), nvs.CORE_SHA)
        self.assertEqual(Path(core.__file__).resolve(), (WORK / 'j1_stage_a_phase.py').resolve())
        with tempfile.TemporaryDirectory() as tmp:
            for name in ('j1_stage_a_phase.py', 'native_b_diagnostic.py'):
                shutil.copy(WORK / name, Path(tmp) / name)
            with open(Path(tmp) / 'j1_stage_a_phase.py', 'a') as f:
                f.write('\n# changed\n')
            with self.assertRaises(nvs.SessionStop):
                nvs.load_core(tmp)
            with open(Path(tmp) / 'native_b_diagnostic.py', 'a') as f:
                f.write('\n# changed\n')
            with self.assertRaises(nvs.SessionStop):
                nvs.load_reader(tmp)

    def test_reviewed_subject_is_exact(self):
        preflight = dict(nvs.REVIEWED_SUBJECT, ready=True, refusals=[])
        built = nvs.reviewed_subject(core, preflight, home='/invented-home')
        self.assertEqual(built.project, nvs.EXACT_PROJECT)
        self.assertEqual(built.app_data, '/invented-home/Library/Application Support/' + preflight['identifier'])
        for key in ('executable_sha256', 'identifier', 'packet'):
            with self.assertRaises(nvs.SessionStop):
                nvs.reviewed_subject(core, dict(preflight, **{key: 'other'}), home='/h')


class DeadlinesAndCleanup(unittest.TestCase):
    def test_owner_end_format(self):
        self.assertEqual(nvs.parse_owner_end('2026-11-07T12:10:00Z'), BASE + timedelta(minutes=10))
        for bad in ('2026-11-07T12:10:00', '2026-11-07T12:10:00+00:00', '2026-11-07 12:10:00Z', '2026-13-07T12:10:00Z'):
            with self.assertRaises(nvs.SessionStop):
                nvs.parse_owner_end(bad)

    def test_stale_or_insufficient_window_never_launches(self):
        for seconds in (-5, 0, 299):
            session, io, adapter, journal, _, _, factory, _ = make(owner_seconds=seconds)
            result = session.run()
            self.assertEqual(io.events, [])
            self.assertEqual(factory, [])
            self.assertIn('window-refusal', journal.kinds())
            self.assertTrue(result['original_absent'])
            self.assertEqual(result['launches'], 0)

    def test_admission_time_counts_before_launch(self):
        session, io, *_ = make(owner_seconds=301)
        io.admit_seconds = 5
        result = session.run()
        self.assertEqual(io.events, ['admit'])
        self.assertIn('insufficient UI time', result['session_error'])

    def test_preflight_false_no_admission(self):
        session, io, adapter, journal, *_ = make()
        adapter.pre['post_event'] = False
        session.run()
        self.assertEqual(io.events, [])
        self.assertIn('visual-preflight', journal.kinds())

    def test_idle_ui_cutoff_cleans_up_without_parent_roundtrip(self):
        session, io, adapter, journal, output, commands, _, time = make()
        result = session.run()
        self.assertEqual(result['stop_reason'], 'ui-cutoff')
        self.assertEqual(io.events, ['admit', 'launch', 'bind-cleanup', 'terminate'])
        self.assertTrue(result['closed_normally'])
        self.assertLessEqual(result['cleanup_started'], nvs.UI_CAP + 1e-9)
        self.assertEqual(output.events()[-2:], ['closing', 'closed'])
        self.assertEqual(adapter.closed, 1)
        self.assertEqual(io.backend.closed, 1)

    def test_owner_end_clips_caps(self):
        session, io, _, _, _, _, _, time = make(owner_seconds=400)
        result = session.run()
        self.assertAlmostEqual(result['cleanup_started'], 400 - nvs.CLEANUP_RESERVE)
        self.assertEqual(result['owner_end_overrun'], 0)

    def test_eof_and_signal_trigger_cleanup(self):
        session, io, *_ = make(['EOF'])
        self.assertEqual(session.run()['stop_reason'], 'eof')
        self.assertEqual(io.terminations, 1)

        def interrupt():
            raise nvs.SessionSignal(15)
        session, io, *_ = make([interrupt])
        result = session.run()
        self.assertIn('SessionSignal', result['session_error'])
        self.assertEqual(io.terminations, 1)
        with self.assertRaises(nvs.SessionStop):
            session.run()  # one session only, no rearm

    def test_unknown_absence_is_held_and_quit_not_repeated(self):
        session, io, adapter, journal, output, commands, _, time = make([{'op': 'quit'}])
        io.absent_never = True
        result = session.run()
        self.assertEqual(io.terminations, 1)
        self.assertEqual(len(io.holds), 1)
        self.assertTrue(io.holds[0]['slot_must_remain_held'])
        self.assertFalse(result['closed_normally'])
        self.assertTrue(result['late_absence'] and result['initial_held'])
        self.assertIn('held', output.events())
        self.assertEqual(commands.reads, 1)  # no more input after closing
        self.assertIn('final-closure', journal.kinds())

    def test_terminate_error_is_not_retried(self):
        session, io, *_ = make([{'op': 'quit'}])
        io.terminate_error, io.absent_never = OSError('selector failed'), True
        result = session.run()
        self.assertEqual(io.terminations, 1)
        self.assertIn('selector failed', result['cleanup_error'])
        self.assertEqual(len(io.holds), 1)

    def test_launch_outcome_unknown_without_identity_is_held(self):
        session, io, *_ = make()

        def lost_launch(subject_):
            io.pending_launch = True
            raise OSError('open outcome unknown')
        io.launch_once = lost_launch
        io.hold_until_absent = lambda result: io.holds.append(result) or (_ for _ in ()).throw(
            nvs.SessionStop('fake hold never releases'))
        with self.assertRaises(nvs.SessionStop):
            session.run()
        self.assertEqual(io.terminations, 0)
        self.assertTrue(io.holds[0]['slot_must_remain_held'])
        self.assertEqual(io.backend.closed, 1)

    def test_recording_failures(self):
        session, io, adapter, journal, *_ = make([CAP, {'op': 'click', 'frame': 1, 'x': 400, 'y': 400}],
                                                 journal=Journal({'input-intent'}))
        result = session.run()
        self.assertEqual(adapter.posts, [])
        self.assertEqual(io.terminations, 1)
        self.assertIn('input-intent', result['session_error'])

        session, io, adapter, journal, *_ = make([CAP, {'op': 'click', 'frame': 1, 'x': 400, 'y': 400}],
                                                 journal=Journal({'input-result'}))
        result = session.run()
        self.assertEqual(len(adapter.posts), 2)
        self.assertIn('input result evidence failed', result['session_error'])
        self.assertEqual(io.terminations, 1)

        session, io, adapter, journal, *_ = make(journal=Journal({'cleanup-intent', 'result'}))
        result = session.run()
        self.assertEqual(io.terminations, 1)
        self.assertEqual([e['record'] for e in result['evidence_errors']], ['cleanup-intent', 'result'])
        self.assertFalse(result['closed_normally'])

    def test_output_loss_stops_and_cleans_up(self):
        session, io, *_ = make([CAP], output=Output(fail=True))
        result = session.run()
        self.assertIn('operator output unavailable', result['session_error'])
        self.assertEqual(io.terminations, 1)

    def test_wait_is_bounded_and_clipped(self):
        session, io, adapter, journal, output, commands, _, time = make([{'op': 'wait', 'seconds': 11}])
        session.run()
        self.assertIn('wait seconds', output.lines[1]['refused'])
        session, io, adapter, journal, output, commands, _, time = make(
            [lambda: (setattr(time, 't', time.t + nvs.UI_CAP - 3), json.dumps({'op': 'wait', 'seconds': 10}).encode())[1]])
        result = session.run()
        self.assertAlmostEqual(output.lines[1]['waited'], 3)
        self.assertEqual(result['stop_reason'], 'ui-cutoff')


class FramesAndInput(unittest.TestCase):
    def test_dispatch_cutoff_after_preparation(self):
        click = {'op': 'click', 'frame': 1, 'x': 400, 'y': 400}
        for phase, expiry in [('intent', 'ui'), ('allocation', 'ui'), ('check', 'ui'), ('intent', 'owner')]:
            with self.subTest(phase=phase, expiry=expiry):
                session, io, adapter, journal, output, commands, _, time = make(owner_seconds=600)
                def late_capture():
                    time.sleep(session.ui_left() - 2)
                    return json.dumps(CAP).encode()
                commands.items = [late_capture, click]
                expired = [False]
                def expire():
                    if not expired[0]:
                        expired[0] = True
                        time.sleep(3 if expiry == 'ui' else session.owner_left() + 1)
                if phase == 'intent':
                    def record(kind, value):
                        journal(kind, value)
                        if kind == 'input-intent':
                            expire()
                    session.record = record
                elif phase == 'allocation':
                    original_event = adapter.event
                    def event(source, spec, down):
                        result = original_event(source, spec, down)
                        expire()
                        return result
                    adapter.event = event
                else:
                    original_check = io.check
                    def check(identity):
                        original_check(identity)
                        if adapter.allocated:
                            expire()
                    io.check = check
                result = session.run()
                self.assertTrue(expired[0])
                self.assertEqual(adapter.posts, [], 'preparation expiry must prevent a new down')
                self.assertIn('cutoff', result['session_error'])
                self.assertEqual(io.terminations, 1)

    def test_context_drift_during_preparation_prevents_dispatch(self):
        click = {'op': 'click', 'frame': 1, 'x': 400, 'y': 400}
        for phase in ('intent', 'allocation'):
            for change in ('foreground', 'window', 'frame_age'):
                with self.subTest(phase=phase, change=change):
                    session, io, adapter, journal, output, commands, _, time = make([CAP, click])
                    changed = [False]
                    def drift():
                        if changed[0]:
                            return
                        changed[0] = True
                        if change == 'foreground':
                            adapter.front['active'] = False
                        elif change == 'window':
                            io.backend.rows[1]['decoded']['bounds']['X'] = 101.0
                        else:
                            time.sleep(nvs.FRAME_MAX_AGE + 1)
                    if phase == 'intent':
                        def record(kind, value):
                            journal(kind, value)
                            if kind == 'input-intent':
                                drift()
                        session.record = record
                    else:
                        original_event = adapter.event
                        def event(source, spec, down):
                            result = original_event(source, spec, down)
                            drift()
                            return result
                        adapter.event = event
                    session.run()
                    self.assertTrue(changed[0])
                    self.assertEqual(adapter.posts, [], 'final visual safeguards must see preparation drift')
                    self.assertEqual(io.terminations, 1)

    def test_activation_cutoff_and_text_chunk_release(self):
        for phase in ('intent', 'adapter'):
            with self.subTest(activation_preparation=phase):
                session, io, adapter, journal, output, commands, _, time = make(owner_seconds=600)
                adapter.front['active'], adapter.front['frontmost_pid'] = False, 999
                def late_capture():
                    time.sleep(session.ui_left() - 2)
                    return json.dumps(CAP).encode()
                commands.items = [late_capture, {'op': 'activate', 'frame': 1}]
                if phase == 'intent':
                    def record(kind, value):
                        journal(kind, value)
                        if kind == 'activation-intent':
                            time.sleep(3)
                    session.record = record
                else:
                    original_activate = adapter.activate
                    def activate(identity, expected, before_dispatch=lambda: None):
                        time.sleep(3)
                        return original_activate(identity, expected, before_dispatch)
                    adapter.activate = activate
                result = session.run()
                self.assertEqual(adapter.activations, 0)
                self.assertIn('cutoff', result['session_error'])
                self.assertEqual(io.terminations, 1)

        session, io, adapter, journal, output, commands, _, time = make([
            CAP, {'op': 'click', 'frame': 1, 'x': 400, 'y': 400}, CAP,
            {'op': 'confirm_first_effect', 'frame': 2}, {'op': 'type_project', 'frame': 2}])
        original_post = adapter.post
        def post(pid, event):
            original_post(pid, event)
            if event[0][0] == 'text' and event[1] is True:
                time.sleep(nvs.UI_CAP + 1)
        adapter.post = post
        result = session.run()
        text = [p for p in adapter.posts if p[1][0] == 'text']
        self.assertEqual([p[2] for p in text], [True, False], 'release the attempted down, then stop new chunks')
        self.assertIn('cutoff', result['session_error'])
        self.assertEqual(len(adapter.released), adapter.allocated)
        self.assertEqual(io.terminations, 1)

    def test_retina_capture_and_click_mapping(self):
        session, io, adapter, journal, output, *_ = make([CAP, {'op': 'click', 'frame': 1, 'x': 400, 'y': 400}])
        session.run()
        frame = output.lines[1]
        self.assertTrue(frame['actionable'])
        self.assertEqual(frame['scale'], 2.0)
        self.assertEqual(frame['windows_pixels'][0]['bounds'], [200.0, 200.0, 1600.0, 1200.0])
        self.assertEqual(adapter.posts, [(PID, ('click', 200.0, 200.0, 7), True), (PID, ('click', 200.0, 200.0, 7), False)])
        self.assertEqual(len(adapter.released), 3)
        click = output.lines[2]
        self.assertEqual((click['dispatch'], click['handling'], click['up_attempted']), ('attempted', 'unknown', 1))
        intent = dict(journal.rows)['input-intent']
        self.assertEqual(intent['global_point'], [200.0, 200.0])

    def test_geometry_rules(self):
        self.assertEqual(nvs.frame_geometry(RETINA, (3024, 1964))['scale'], 2.0)
        one = {'bounds': [0, 0, 1920, 1080], 'mode_points': [1920, 1080], 'mode_pixels': [1920, 1080]}
        self.assertEqual(nvs.frame_geometry(one, (1920, 1080))['scale'], 1.0)
        bad = [(dict(RETINA, bounds=[10, 0, 1512, 982]), (3024, 1964)),
               (dict(RETINA, mode_pixels=[3000, 1964]), (3000, 1964)),
               (RETINA, (3000, 1964)),
               (dict(RETINA, mode_points=[1500, 982]), (3024, 1964)),
               ({'bounds': [0, 0, 1000, 1000], 'mode_points': [1000, 1000], 'mode_pixels': [1500, 1500]}, (1500, 1500)),
               (dict(RETINA, bounds=[0, 0, float('nan'), 982]), (3024, 1964))]
        for geometry, pixels in bad:
            with self.assertRaises(nvs.ActionRefused):
                nvs.frame_geometry(geometry, pixels)

    def test_off_main_or_invalid_geometry_frame_not_actionable(self):
        session, io, adapter, journal, output, *_ = make([CAP, {'op': 'click', 'frame': 1, 'x': 400, 'y': 400}])
        adapter.pixels = (3000, 1964)
        session.run()
        self.assertFalse(output.lines[1]['actionable'])
        self.assertIn('refused', output.lines[2])
        self.assertEqual(adapter.posts, [])

    def test_target_outside_original_window_refused(self):
        clicks = [(150, 150), (1900, 1500), (3024, 10), (0, 0)]
        for x, y in clicks:
            session, io, adapter, journal, output, *_ = make([CAP, {'op': 'click', 'frame': 1, 'x': x, 'y': y}])
            session.run()
            self.assertIn('refused', output.lines[2], (x, y))
            self.assertEqual(adapter.posts, [])
        session, io, adapter, journal, output, *_ = make([CAP, {'op': 'click', 'frame': 1, 'x': 400, 'y': 400}])
        io.backend.rows[1]['decoded']['on_screen'] = None
        session.run()
        self.assertFalse(output.lines[1]['actionable'])
        self.assertEqual(adapter.posts, [])

    def test_stale_replayed_old_and_changed_frames(self):
        click = {'op': 'click', 'frame': 1, 'x': 400, 'y': 400}
        session, io, adapter, journal, output, commands, _, time = make([CAP, click, click, dict(click, frame=2)])
        session.run()
        self.assertEqual(len(adapter.posts), 2)
        self.assertIn('consumed', output.lines[3]['refused'])
        self.assertIn('stale', output.lines[4]['refused'])

        session, io, adapter, journal, output, commands, _, time = make(
            [CAP, lambda: (setattr(time, 't', time.t + nvs.FRAME_MAX_AGE + 1), json.dumps(click).encode())[1]])
        session.run()
        self.assertIn('too old', output.lines[2]['refused'])
        self.assertEqual(adapter.posts, [])

        def move():
            io.backend.rows[1]['decoded']['bounds']['X'] = 101.0
            return json.dumps(click).encode()
        session, io, adapter, journal, output, *_ = make([CAP, move])
        session.run()
        self.assertIn('geometry changed', output.lines[2]['refused'])
        self.assertEqual(adapter.posts, [])

    def test_foreground_and_identity_refusals(self):
        click = {'op': 'click', 'frame': 1, 'x': 400, 'y': 400}
        session, io, adapter, journal, output, *_ = make([CAP, click])
        adapter.front['frontmost_pid'] = 999
        session.run()
        self.assertFalse(output.lines[1]['actionable'])
        self.assertEqual(adapter.posts, [])

        def lose_foreground():
            adapter.front['active'] = False
            return json.dumps(click).encode()
        session, io, adapter, journal, output, *_ = make([CAP, lose_foreground])
        session.run()
        self.assertIn('not foreground', output.lines[2]['refused'])
        self.assertEqual(adapter.posts, [])

        session, io, adapter, journal, output, *_ = make([CAP])
        adapter.front['correspondence'] = {'pid': PID, 'bundle_identifier': 'other.app', 'executable': '/other'}
        result = session.run()
        self.assertIn('correspondence', result['session_error'])
        self.assertEqual(io.terminations, 1)

        def reused_pid():
            io.wrong = True
            return json.dumps(click).encode()
        session, io, adapter, journal, output, *_ = make([CAP, reused_pid])
        result = session.run()
        self.assertEqual(adapter.posts, [])
        self.assertIn('changed', result['session_error'])
        self.assertEqual(io.terminations, 0)  # never terminate a possibly foreign PID
        self.assertIn('changed', result['cleanup_error'])

    def test_first_input_gate_and_confirmation(self):
        session, io, adapter, journal, output, *_ = make([
            CAP, {'op': 'key', 'frame': 1, 'key': 'return'},
            CAP, {'op': 'click', 'frame': 2, 'x': 400, 'y': 400},
            {'op': 'confirm_first_effect', 'frame': 2},
            CAP, {'op': 'key', 'frame': 3, 'key': 'select_all'},
            {'op': 'confirm_first_effect', 'frame': 3},
            {'op': 'key', 'frame': 3, 'key': 'select_all'},
            CAP, {'op': 'key', 'frame': 4, 'key': 'go_to_folder'}])
        session.run()
        lines = output.lines[1:]
        self.assertIn('first input must be one benign visible click', lines[1]['refused'])
        self.assertEqual(lines[1]['op'], 'key')
        self.assertTrue(lines[3]['ok'])
        self.assertIn('post-click', lines[4]['refused'])
        self.assertIn('not confirmed', lines[6]['refused'])
        self.assertFalse(lines[7]['tool_proof'])
        self.assertIn('consumed', lines[8]['refused'])
        self.assertTrue(lines[10]['ok'])
        self.assertEqual([p[1] for p in adapter.posts[2:]], [('key', 0x05, 0x120000)] * 2)
        self.assertIn('operator-first-effect', journal.kinds())

    def test_type_project_is_literal_utf16(self):
        chunks = nvs.utf16_chunks(nvs.EXACT_PROJECT)
        self.assertTrue(all(len(c) <= nvs.UTF16_CHUNK for c in chunks))
        decoded = ''.join(bytes(b for u in c for b in u.to_bytes(2, 'little')).decode('utf-16-le') for c in chunks)
        self.assertEqual(decoded, nvs.EXACT_PROJECT)
        emoji = 'a' * 19 + '\U0001F600' + 'b'
        split = nvs.utf16_chunks(emoji)
        self.assertEqual([len(c) for c in split], [19, 3])
        self.assertTrue(0xD800 <= split[1][0] <= 0xDBFF)

        session, io, adapter, journal, output, *_ = make([
            CAP, {'op': 'click', 'frame': 1, 'x': 400, 'y': 400}, CAP, {'op': 'confirm_first_effect', 'frame': 2},
            {'op': 'type_project', 'frame': 2}])
        session.run()
        text = [p for p in adapter.posts if p[1][0] == 'text']
        self.assertEqual(len(text), 2 * len(chunks))
        self.assertEqual([p[2] for p in text], [True, False] * len(chunks))
        downs = [p[1][1] for p in text if p[2]]
        self.assertEqual(''.join(bytes(b for u in c for b in u.to_bytes(2, 'little')).decode('utf-16-le')
                                 for c in downs), nvs.EXACT_PROJECT)
        self.assertEqual(dict(journal.rows)['input-intent']['text'], nvs.EXACT_PROJECT)

        session, *_ = make(subject_=core.Subject('s', '/b', 'i', '/e', 'a' * 64, '/other/project', '/d'))
        session.identity, session.frames = dict(IDENTITY), []
        with self.assertRaises(nvs.SessionStop):
            session.op_type_project({'op': 'type_project', 'frame': 1})

    def test_gesture_pairs_and_releases_on_failures(self):
        ok_check = lambda: None
        spec = [('key', 0x24, 0)]
        adapter = Adapter()
        adapter.post_error_on = 1
        gesture = nvs.Gesture(adapter)
        with self.assertRaises(OSError):
            gesture.run(PID, spec, ok_check, ok_check)
        self.assertEqual([p[2] for p in adapter.posts], [True, False])  # up still posted
        self.assertEqual(len(adapter.released), 3)

        adapter, calls = Adapter(), []

        def birth():
            calls.append(1)
            raise nvs.SessionStop('birth changed')
        gesture = nvs.Gesture(adapter)
        with self.assertRaises(nvs.SessionStop):
            gesture.run(PID, spec, ok_check, birth)
        self.assertEqual([p[2] for p in adapter.posts], [True])  # no up to a possibly reused PID
        self.assertEqual((gesture.state['down_attempted'], gesture.state['up_attempted']), (1, 0))
        self.assertEqual(len(adapter.released), 3)

        adapter = Adapter()
        adapter.fail_event_at = 3
        with self.assertRaises(nvs.SessionStop):
            nvs.Gesture(adapter).run(PID, spec, ok_check, ok_check)
        self.assertEqual(adapter.posts, [])
        self.assertEqual(len(adapter.released), 2)

        adapter = Adapter()
        with self.assertRaises(core.Refusal):
            nvs.Gesture(adapter).run(PID, spec, lambda: (_ for _ in ()).throw(core.Refusal('foreign')), ok_check)
        self.assertEqual(adapter.posts, [])
        self.assertEqual(len(adapter.released), 3)

        adapter = Adapter()
        adapter.release_error = True
        gesture = nvs.Gesture(adapter)
        with self.assertRaises(nvs.SessionStop):
            gesture.run(PID, spec, ok_check, ok_check)
        self.assertEqual(len(adapter.posts), 2)
        self.assertEqual(gesture.state['release_errors'], ['OSError'] * 3)

    def test_post_failure_in_session_is_unknown_and_stops(self):
        session, io, adapter, journal, output, *_ = make([CAP, {'op': 'click', 'frame': 1, 'x': 400, 'y': 400}])
        adapter.post_error_on = 1
        result = session.run()
        self.assertEqual(result['actions'][0]['dispatch'], 'attempted')
        self.assertEqual(result['actions'][0]['up_attempted'], 1)
        self.assertEqual(result['handling'], 'unknown')
        self.assertEqual(io.terminations, 1)

    def test_one_activation_only(self):
        session, io, adapter, journal, output, *_ = make([
            CAP, {'op': 'activate', 'frame': 1}, CAP, {'op': 'activate', 'frame': 2}])
        adapter.front['frontmost_pid'] = 999
        session.run()
        self.assertEqual(adapter.activations, 1)
        self.assertEqual(output.lines[2]['effect'], 'unknown until a fresh capture')
        self.assertIn('one activation', output.lines[4]['refused'])
        session, io, adapter, journal, output, *_ = make([CAP, {'op': 'activate', 'frame': 1}])
        session.run()
        self.assertIn('already foreground', output.lines[2]['refused'])
        self.assertEqual(adapter.activations, 0)


class CommandsAndSave(unittest.TestCase):
    def test_command_schema_bounds(self):
        bad = [b'not json', b'[]', b'{"op":"eval","code":"1"}', b'{"op":"capture","x":1}',
               b'{"op":"click","frame":1,"x":true,"y":2}', b'{"op":"click","frame":1,"x":-1,"y":2}',
               b'{"op":"key","frame":1,"key":"cmd_q"}', b'{"op":"type_project","frame":1,"text":"/etc"}',
               b'{"op":"wait","seconds":0}', b'{"op":"wait","seconds":1e999}', b'{"op":"capture","op":"quit"}',
               b'{"op":"click","frame":1.0,"x":1,"y":2}', b'{"op":"expected_effects","settings_folder":"rel",'
               b'"sign_in_folder":"/a"}', b'{"op":"activate","frame":1,"pid":99}', b'\xff\xfe']
        for line in bad:
            with self.assertRaises(nvs.ActionRefused, msg=line):
                nvs.parse_command(line)
        self.assertEqual(nvs.parse_command(b'{"op":"key","frame":3,"key":"return"}'),
                         {'op': 'key', 'frame': 3, 'key': 'return'})
        session, io, adapter, journal, output, *_ = make([b'{"op":"eval"}', {'op': 'status'}])
        session.run()
        self.assertFalse(output.lines[1]['ok'])
        self.assertTrue(output.lines[2]['ok'])

    def test_line_reader_bounds_and_eof(self):
        r, w = os.pipe()
        try:
            os.write(w, b'{"op":"status"}\npartial')
            os.close(w)
            w = None
            lines = nvs.LineReader(r)
            self.assertEqual(lines.read(0), b'{"op":"status"}')
            self.assertEqual(lines.read(0), nvs.LineReader.EOF)
        finally:
            os.close(r)
            if w is not None:
                os.close(w)
        r, w = os.pipe()
        try:
            self.assertEqual(nvs.LineReader(r).read(0), nvs.LineReader.TIMEOUT)
            os.write(w, b'x' * (nvs.MAX_LINE + 1))
            with self.assertRaises(nvs.SessionStop):
                nvs.LineReader(r).read(0)
        finally:
            os.close(r)
            os.close(w)

    def test_expected_effects_and_pending_save_use_existing_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            app_data = str(Path(tmp).resolve() / 'dev.invented.test')
            subj = subject(app_data)
            settings, account = app_data + '/settings/one', app_data + '/account-homes/one'

            def native(path):
                return {'encoding': 'unix_bytes', 'bytes': list(os.fsencode(path))}

            def ref(path):
                return {'location': native(path), 'resolved': native(path), 'object': {'device': 1, 'inode': 2}}
            pending = {'version': 1, 'supplier': 'bundled-owner-use-development', 'app_data': ref(app_data),
                       'account': ref(account), 'project': ref(nvs.EXACT_PROJECT),
                       'shared': [ref(settings + '/' + n) for n in ('config.toml', 'AGENTS.md', 'skills')]}
            request = Path(app_data) / 'desktop-startup/request.json'
            request.parent.mkdir(parents=True)
            request.write_text(json.dumps(pending))
            effects = {'op': 'expected_effects', 'settings_folder': settings, 'sign_in_folder': account}
            session, io, adapter, journal, output, *_ = make([
                {'op': 'verify_saved'},
                dict(effects, settings_folder='/elsewhere/settings'), effects,
                {'op': 'verify_saved'}, {'op': 'verify_saved'}], subject_=subj)
            session.run()
            lines = output.lines[1:]
            self.assertIn('expected_effects', lines[0]['refused'])
            self.assertIn('outside exact development ID', lines[1]['refused'])
            locations = {'Settings folder': settings, 'Sign-in folder': account, 'Saved choices': str(request)}
            self.assertEqual(lines[2]['text'], core.setup_effects(subj, locations))
            self.assertEqual(lines[3]['checked'], {'project': nvs.EXACT_PROJECT, 'locations': locations,
                                                   'pending_only': True})
            self.assertIn('already used', lines[4]['refused'])
            self.assertIn('saved-state', journal.kinds())

            pending['project'] = ref('/invented/other')
            request.write_text(json.dumps(pending))
            session, io, adapter, journal, output, *_ = make([effects, {'op': 'verify_saved'}], subject_=subj)
            session.run()
            self.assertIn('saved reference differs', output.lines[2]['refused'])
            self.assertIn('saved-state-refusal', journal.kinds())


if __name__ == '__main__':
    unittest.main()
