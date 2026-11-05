"""Behavioral OS-effect doubles only; no App/native API, launch or UI action."""
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from j1_stage_a_phase import (Subject, Control, View, StageA, NativeAX, NativeSession,
                              NotReady, Refusal, phase_root, checked_locations, normal_terminate, run_prepared, checked_pending, private_journal,
                              checked_packet)

S = Subject('retained-source', '/invented/Test.app', 'dev.invented.test', '/invented/Test.app/Contents/MacOS/app',
            'a' * 64, '/invented/packet/session/project', '/invented/Library/Application Support/dev.invented.test')

LOCATIONS = {'Settings folder': S.app_data + '/settings/one',
             'Sign-in folder': S.app_data + '/account-homes/one',
             'Saved choices': S.app_data + '/desktop-startup/request.json'}

# Constructed golden question from eaf5d057 DesktopSetup::preview_statement;
# deliberately independent of the controller's expected-statement builder.
QUESTION = (
    'Desktop setup — next launch only\n'
    f"Create NEW App-owned settings folder: {LOCATIONS['Settings folder']}\n"
    'with an empty config.toml, an empty AGENTS.md and an empty skills folder.\n'
    f"Create NEW App-owned account directory: {LOCATIONS['Sign-in folder']}\n"
    'Link its config.toml, AGENTS.md and skills to those new settings.\n'
    'Read, import or change no other Codex settings, home or credential.\n'
    f'Project for next launch: {S.project}\n'
    f"Save a private pending request in {LOCATIONS['Saved choices']}.\n"
    'Codex: the copy included with this App (bundled-owner-use-development).\n'
    'The current workspace, homes, account/model choices, records and prepared messages stay unchanged. '
    'No automatic quit/restart/login/conversation.'
)


def c(label, role='AXButton', enabled=True, value=None, writable=False, ref=None):
    return Control(ref or label, role, label, enabled, value, writable)


class FakeIO:
    def __init__(self, now):
        self.now = now
        self.identity = None
        self.phase = 'main'
        self.events = []
        self.reads = 0
        self.selected = False
        self.expanded = False
        self.path = ''
        self.closed = False
        self.wrong = False
        self.failure = None
        self.calls = 0

    def admit(self, subject):
        self.events.append('admit-cleanup-prepared')

    def launch_once(self, subject):
        self.events.append('launch')
        self.identity = {'pid': 17, 'ppid': 1, 'uid': 501, 'ruid': 501, 'start_sec': 10,
                         'start_usec': 20, 'executable': S.executable}
        return self.identity

    def bind_cleanup(self, identity, subject):
        self.events.append('bind-original-cleanup')

    def check(self, identity):
        if self.wrong or identity != self.identity:
            raise Refusal('original identity differs')

    def supplier_started(self):
        return self.failure == 'supplier'

    def original_main(self, subject, deadline):
        self.events.append('original-main')
        return 'main-original'

    def same(self, a, b):
        return a == b

    def observe(self, main, phase, deadline):
        self.calls += 1
        if self.failure == 'cutoff' and phase == 'picker':
            self.now[0] = 110
        if self.failure == 'transient' and self.calls < 3:
            raise NotReady('transient value')
        if self.failure == 'missing-main':
            raise NotReady('no main')
        if phase == 'main':
            self.reads += 1
            web = self.reads >= 2 or self.selected
            controls = [c('Choose project folder…'), c('Start with new settings (recommended)', 'AXRadioButton', value=1),
                        c('Review setup', enabled=self.selected)] if web else []
            return View(main, main, controls, S.project if self.selected else 'Welcome', web)
        if phase == 'picker':
            if self.failure == 'ambiguous':
                raise Refusal('ambiguous related picker')
            controls = [c('Go to the folder:', 'AXTextField', value=self.path, writable=True), c('Go'), c('Open')]
            if self.failure == 'path-absent':
                controls = [c('Open'), c('Cancel')]
            return View(main, 'picker-related', controls, S.project if self.path else '')
        if phase == 'preview':
            paths = {'Settings folder': S.app_data + '/settings/one',
                     'Sign-in folder': S.app_data + '/account-homes/one',
                     'Saved choices': S.app_data + '/desktop-startup/request.json'} if self.expanded else {}
            return View(main, main, [c('Exact locations', 'AXDisclosureTriangle', value=self.expanded),
                                    c('Create settings and save for next launch…')], 'What setup will do', True, paths)
        if phase == 'confirmation':
            controls = [c('Leave setup unchanged'), c('Create settings and save for next launch'), c('Cancel')]
            if self.failure == 'question':
                controls[1] = c('Different action')
            return View(main, 'confirmation-related', controls, QUESTION)
        if phase == 'saved':
            return View(main, main, [], "You're set up", True)
        raise AssertionError(phase)

    def revalidate(self, view, control, deadline):
        if self.failure == 'stale':
            return replace(control, ref='replacement')
        if self.failure == 'wrong-identity':
            self.wrong = True
        return control

    def press(self, control, deadline):
        self.events.append('press:' + control.label)
        if self.failure == 'unknown-dispatch':
            raise OSError('dispatch returned no result')
        if control.label == 'Open':
            self.selected = True
        if control.label == 'Exact locations':
            self.expanded = True
        return 0

    def enter_path(self, control, path, deadline):
        assert path == S.project
        self.events.append('enter-exact-path')
        if self.failure == 'unknown-path':
            raise OSError('path dispatch outcome unknown')
        self.path = path
        return 0

    def read_value(self, control):
        return self.path

    def verify_saved(self, subject, locations):
        return {'standing': 'invented mocked saved result; not native execution'}

    def normal_terminate(self, identity, subject):
        self.events.append('terminate-original')
        if self.failure == 'terminate-unknown':
            raise OSError('normal request outcome unknown')
        if self.failure != 'terminate-false':
            self.closed = True
        return self.failure != 'terminate-false'

    def absent(self, identity):
        return self.closed

    def launch_unknown(self):
        return False


class ControllerTests(unittest.TestCase):
    def fixture(self, failure=None):
        now = [0.0]
        io = FakeIO(now)
        io.failure = failure
        records = []
        controller = StageA(S, io, clock=lambda: now[0], sleep=lambda n: now.__setitem__(0, now[0] + n),
                            record=lambda kind, value: records.append((kind, value)))
        return controller, io, now, records

    def test_complete_mocked_phase_flow_and_prebound_cleanup(self):
        runner, io, now, records = self.fixture()
        result = runner.run()
        self.assertTrue(result['setup_saved'])
        self.assertTrue(result['original_absent'])
        self.assertTrue(result['cleanup_within_reserved_interval'])
        self.assertFalse(result['J1_complete'])
        self.assertFalse(result['qualification'])
        self.assertEqual(io.events.count('launch'), 1)
        self.assertEqual(io.events.count('terminate-original'), 1)
        self.assertLess(io.events.index('bind-original-cleanup'), io.events.index('original-main'))
        self.assertEqual([x for x in io.events if x == 'enter-exact-path'], ['enter-exact-path'])
        with self.assertRaises(Refusal):
            runner.run()
        self.assertEqual(io.events.count('launch'), 1)

    def test_related_picker_phase_replaces_no_main_binding(self):
        runner, io, now, records = self.fixture()
        result = runner.run()
        phases = [v['phase'] for k, v in records if k == 'phase-observation']
        self.assertIn('picker', phases)
        self.assertIn('confirmation', phases)
        self.assertTrue(result['setup_saved'])
        self.assertEqual(runner.main, 'main-original')

    def test_wrong_identity_or_stale_target_sends_no_input(self):
        for failure in ('stale', 'wrong-identity', 'supplier'):
            with self.subTest(failure=failure):
                runner, io, now, records = self.fixture(failure)
                result = runner.run()
                self.assertFalse(any(x.startswith('press:') or x == 'enter-exact-path' for x in io.events))
                self.assertFalse(result['setup_saved'])
                if failure == 'wrong-identity':
                    self.assertNotIn('terminate-original', io.events)
                    self.assertTrue(result['slot_must_remain_held'])

    def test_ambiguous_picker_or_absent_path_capability_gets_no_picker_input(self):
        for failure in ('ambiguous', 'path-absent'):
            with self.subTest(failure=failure):
                runner, io, now, records = self.fixture(failure)
                result = runner.run()
                self.assertEqual([x for x in io.events if x.startswith('press:')], ['press:Choose project folder…'])
                self.assertNotIn('enter-exact-path', io.events)
                self.assertIn('terminate-original', io.events)
                self.assertFalse(result['setup_saved'])
                if failure == 'path-absent':
                    self.assertIn('NATIVE_PATH_ENTRY_UNAVAILABLE', result['setup_error'])

    def test_cutoff_begins_independent_cleanup_in_reserved_interval(self):
        runner, io, now, records = self.fixture('cutoff')
        result = runner.run()
        self.assertEqual(result['cleanup_started'], 110)
        self.assertTrue(result['cleanup_within_reserved_interval'])
        self.assertEqual(io.events.count('terminate-original'), 1)
        self.assertNotIn('enter-exact-path', io.events)
        self.assertLess(result['elapsed'], 180)

    def test_transient_values_have_bounded_readiness_and_no_focus_cycle(self):
        runner, io, now, records = self.fixture('transient')
        runner.run()
        self.assertLessEqual(now[0], 5)
        self.assertEqual(io.events.count('terminate-original'), 1)
        runner, io, now, records = self.fixture('missing-main')
        result = runner.run()
        self.assertEqual(io.calls, 3)
        self.assertLessEqual(result['cleanup_started'], 5)
        self.assertIn('terminate-original', io.events)

    def test_unknown_press_is_recorded_once_and_cleanup_does_not_need_parent(self):
        runner, io, now, records = self.fixture('unknown-dispatch')
        result = runner.run()
        self.assertEqual(len([x for x in io.events if x.startswith('press:')]), 1)
        dispatch = [v for k, v in records if k == 'press-result']
        self.assertIsNone(dispatch[0]['rc'])
        self.assertIn('OSError', dispatch[0]['error'])
        self.assertIn('terminate-original', io.events)
        self.assertTrue(result['original_absent'])

    def test_confirmation_changes_cannot_authorize_save(self):
        runner, io, now, records = self.fixture('question')
        result = runner.run()
        self.assertFalse(result['setup_saved'])
        self.assertNotIn('press:Create settings and save for next launch', io.events)
        self.assertTrue(result['original_absent'])

    def test_false_or_unknown_terminate_does_not_establish_absence_or_repeat(self):
        for failure in ('terminate-false', 'terminate-unknown'):
            with self.subTest(failure=failure):
                runner, io, now, records = self.fixture(failure)
                result = runner.run()
                self.assertEqual(io.events.count('terminate-original'), 1)
                self.assertFalse(result['original_absent'])
                self.assertTrue(result['slot_must_remain_held'])
                self.assertAlmostEqual(result['elapsed'], 180)


class FakeAX:
    def __init__(self):
        self.nodes = {
            'app': {'role': 'AXApplication', 'AXWindows': ['main'], 'owner': 17},
            'main': {'role': 'AXWindow', 'AXSheets': [], 'AXChildren': [], 'owner': 17},
        }
        self.reads = []

    def same(self, a, b):
        return a == b

    def role(self, ref):
        self.reads.append(('role', ref))
        if self.nodes[ref].get('owner') != 17:
            raise Refusal('wrong owner before content')
        return self.nodes[ref]['role']

    def refs(self, ref, name, optional=True):
        return self.nodes[ref].get(name, [])

    def ref(self, ref, name):
        return self.nodes[ref].get(name)

    def value(self, ref, name):
        return self.nodes[ref].get(name)

    def panel(self, ref='panel', parent='main', owner=17, role='AXSheet'):
        self.nodes[ref] = {'role': role, 'AXParent': parent, 'owner': owner, 'AXModal': True}
        self.nodes['app']['AXWindows'].append(ref)
        if parent == 'main':
            self.nodes['main']['AXSheets'].append(ref)


class WindowRelationshipTests(unittest.TestCase):
    def test_expected_distinct_picker_keeps_original_main(self):
        ax = FakeAX()
        ax.panel()
        self.assertEqual(phase_root(ax, 'app', 'main', 'picker'), 'panel')
        self.assertEqual(ax.nodes['app']['AXWindows'], ['main', 'panel'])
        with self.assertRaises(Refusal):
            phase_root(ax, 'app', 'main', 'main')

    def test_nested_path_sheet_requires_unique_relation(self):
        ax = FakeAX()
        ax.panel()
        ax.panel('path', parent='panel')
        self.assertEqual(phase_root(ax, 'app', 'main', 'picker'), 'path')
        with self.assertRaises(Refusal):
            phase_root(ax, 'app', 'main', 'confirmation')

    def test_wrong_owner_unrelated_window_and_ambiguous_sheet_refuse(self):
        for failure in ('owner', 'unrelated', 'ambiguous', 'missing-main'):
            with self.subTest(failure=failure):
                ax = FakeAX()
                if failure == 'owner':
                    ax.panel(owner=99)
                elif failure == 'unrelated':
                    ax.panel(parent='app')
                elif failure == 'ambiguous':
                    ax.panel(); ax.panel('other')
                else:
                    ax.nodes['main']['role'] = None
                with self.assertRaises(Refusal):
                    phase_root(ax, 'app', 'main', 'picker')

    def test_pending_picker_is_not_replaced_by_first_other_window(self):
        ax = FakeAX()
        with self.assertRaises(NotReady):
            phase_root(ax, 'app', 'main', 'picker')


class CleanupCorrespondenceTests(unittest.TestCase):
    def fixture(self):
        events = []
        identity = {'pid': 17, 'birth': 'original'}
        class Kit:
            @contextmanager
            def target(self, pid):
                events.append(('target', pid)); yield 'original'
            def describe(self, target):
                return {'pid': 17, 'bundle_identifier': S.identifier, 'executable': S.executable}
            def terminate(self, target):
                events.append('terminate'); return True
        return identity, Kit(), events

    def test_exact_original_correspondence_then_one_normal_request(self):
        identity, kit, events = self.fixture()
        result = normal_terminate(None, identity, S, lambda *a: events.append(a[0]), kit,
                                  lambda got: events.append('full-identity-check'))
        self.assertTrue(result)
        self.assertEqual(events.count('terminate'), 1)
        self.assertLess(events.index('normal-terminate-intent'), events.index('terminate'))
        self.assertEqual(events.count('full-identity-check'), 3)

    def test_wrong_bundle_executable_or_birth_sends_no_termination(self):
        for failure in ('bundle', 'executable', 'birth'):
            with self.subTest(failure=failure):
                identity, kit, events = self.fixture()
                original = kit.describe
                if failure != 'birth':
                    def wrong(target):
                        row = original(target)
                        row['bundle_identifier' if failure == 'bundle' else 'executable'] = 'wrong'
                        return row
                    kit.describe = wrong
                def check(got):
                    if failure == 'birth':
                        raise Refusal('birth changed')
                with self.assertRaises(Refusal):
                    normal_terminate(None, identity, S, lambda *a: None, kit, check)
                self.assertNotIn('terminate', events)

    def test_unknown_request_result_is_retained_without_false_effect(self):
        identity, kit, events = self.fixture(); records = []
        def unknown(target):
            events.append('terminate'); raise OSError('no BOOL returned')
        kit.terminate = unknown
        with self.assertRaises(OSError):
            normal_terminate(None, identity, S, lambda *a: records.append(a), kit, lambda got: None)
        self.assertEqual(events.count('terminate'), 1)
        self.assertIsNone(records[-1][1]['BOOL'])
        self.assertFalse(records[-1][1]['effect_proved'])


class NativeAccessTests(unittest.TestCase):
    def test_scalar_reference_is_not_confused_with_an_array(self):
        class Backend:
            def owner(self, ref): return 0, 17
            def attribute(self, ref, name):
                return {'return_code': 0, 'type': {'name': 'AXUIElement' if name == 'AXMenuBar' else 'CFArray'}, 'value': None}, ['reference']
        ax = NativeAX.__new__(NativeAX); ax.b = Backend(); ax.pid = 17; ax.check = lambda: None
        self.assertEqual(ax.value('app', 'AXMenuBar'), 'reference')
        self.assertEqual(ax.value('app', 'AXWindows'), ['reference'])

    def test_file_lists_recent_items_and_combo_history_are_not_traversed(self):
        nodes = {'panel': ('AXSheet', ['files', 'history-field', 'open']),
                 'files': ('AXOutline', ['private-file']),
                 'history-field': ('AXComboBox', ['recent-item']),
                 'open': ('AXButton', []), 'private-file': ('AXStaticText', []), 'recent-item': ('AXStaticText', [])}
        visited = []
        ax = NativeAX.__new__(NativeAX); ax.clock = lambda: 0; ax.project = S.project
        ax.same = lambda a, b: a == b
        ax.role = lambda ref: visited.append(ref) or nodes[ref][0]
        def value(ref, name):
            if ref in ('private-file', 'recent-item'):
                raise AssertionError('unrelated content enumerated')
            if name == 'AXChildren': return nodes[ref][1]
            if name == 'AXEnabled': return True
            if name == 'AXTitle': return 'Open' if ref == 'open' else 'Search'
            return None
        ax.value = value
        controls, text, web = ax._controls('panel', True, 1)
        self.assertNotIn('private-file', visited)
        self.assertNotIn('recent-item', visited)
        self.assertEqual(text, '')
        self.assertTrue(any(c.label == 'Open' for c in controls))

    def test_write_paths_require_all_three_exact_development_destinations(self):
        values = {'Settings folder': S.app_data + '/settings/new', 'Sign-in folder': S.app_data + '/account-homes/new',
                  'Saved choices': S.app_data + '/desktop-startup/request.json'}
        self.assertEqual(checked_locations(values, S), values)
        for field, path in [('Settings folder', '/owner/.codex'), ('Saved choices', S.app_data + '/wrong.json')]:
            changed = dict(values); changed[field] = path
            with self.assertRaises(Refusal): checked_locations(changed, S)
        with self.assertRaises(Refusal): checked_locations({'Settings folder': values['Settings folder']}, S)


class SlotFinalizerTests(unittest.TestCase):
    def test_selected_entry_observes_hold_before_return_and_releases_only_after_absence(self):
        import j1_stage_a_phase as module
        events = []
        class Session:
            def __init__(self, *args):
                self.identity = {'pid': 17}; self.backend = None
            def hold_until_absent(self, result):
                events.append('observe-held-original-until-absent')
                self.closed = True
            def absent(self, identity): return self.closed
        def result(*args):
            events.append('controller-ended-held')
            return {'slot_must_remain_held': True}
        with patch.object(module, 'NativeSession', Session), patch.object(module.StageA, 'run', result):
            got = run_prepared(S, {}, lambda *a: None)
        self.assertFalse(got['slot_must_remain_held'])
        self.assertTrue(got['original_absent'])
        self.assertIsNone(got['exit_status'])
        self.assertEqual(events, ['controller-ended-held', 'observe-held-original-until-absent'])

    def test_recording_failure_cannot_skip_hold_for_original_live_process(self):
        import j1_stage_a_phase as module
        events = []
        class Session:
            def __init__(self, *args):
                self.identity = {'pid': 17}; self.backend = None
            def absent(self, identity): return False
            def hold_until_absent(self, result):
                self.live = False; events.append(result['slot_must_remain_held'])
            def absent(self, identity): return not getattr(self, 'live', True)
        with patch.object(module, 'NativeSession', Session), patch.object(module.StageA, 'run', side_effect=OSError('record failed')):
            with self.assertRaises(OSError): run_prepared(S, {}, lambda *a: None)
        self.assertEqual(events, [True])


class ImmediateTargetTests(unittest.TestCase):
    def fixture(self):
        ax = NativeAX.__new__(NativeAX)
        ax.app, ax.main, ax.last_root, ax.last_phase = 'app', 'main', 'picker', 'picker'
        ax.check = lambda: None; ax.clock = lambda: 0; ax.same = lambda a, b: a == b
        parents = {'target': 'group', 'group': 'picker'}
        ax.role = lambda ref: 'AXButton'
        ax.value = lambda ref, name: True if name == 'AXEnabled' else 'Open'
        ax.ref = lambda ref, name: parents.get(ref)
        return ax, parents

    def test_native_target_requires_phase_parent_chain_before_input(self):
        ax, parents = self.fixture(); target = c('Open', ref='target')
        with patch('j1_stage_a_phase.phase_root', return_value='picker'):
            ax._bound_target(target, 1)
            parents['group'] = 'unrelated'
            with self.assertRaises(Refusal): ax._bound_target(target, 1)
            parents['target'] = 'target'
            with self.assertRaises(Refusal): ax._bound_target(target, 1)
        with patch('j1_stage_a_phase.phase_root', return_value='replacement'):
            with self.assertRaises(Refusal): ax._bound_target(target, 1)


class BindingAndEarlyFailureTests(unittest.TestCase):
    def test_launch_receipt_failure_after_identity_still_terminates_original_once(self):
        now = [0.0]; io = FakeIO(now); launch = io.launch_once
        def failed_receipt(subject):
            launch(subject)
            raise OSError('launch receipt failed after identity retained')
        io.launch_once = failed_receipt
        runner = StageA(S, io, clock=lambda: now[0], sleep=lambda n: now.__setitem__(0, now[0] + n))
        result = runner.run()
        self.assertEqual(result['launches'], 1)
        self.assertTrue(result['original_absent'])
        self.assertEqual(io.events.count('terminate-original'), 1)
        self.assertFalse(result['flow_complete'])

    def test_native_session_consumes_even_an_unknown_termination_result(self):
        io = NativeSession(S, {}, lambda *a: None)
        io.check = lambda identity: None
        io.backend = object(); io.appkit = object()
        with patch('j1_stage_a_phase.normal_terminate', side_effect=OSError('unknown')) as dispatch:
            with self.assertRaises(OSError): io.normal_terminate({'pid': 17}, S)
            with self.assertRaises(Refusal): io.normal_terminate({'pid': 17}, S)
        self.assertEqual(dispatch.call_count, 1)


class PendingRequestTests(unittest.TestCase):
    def fixture(self):
        locations = {'Settings folder': S.app_data + '/shared-settings/new',
                     'Sign-in folder': S.app_data + '/account-homes/new',
                     'Saved choices': S.app_data + '/desktop-startup/request.json'}
        def reference(path):
            native = {'encoding': 'unix_bytes', 'bytes': list(path.encode())}
            return {'location': native, 'resolved': native, 'object': {'device': 1, 'inode': 2}}
        value = {'version': 1, 'supplier': 'bundled-owner-use-development',
                 'app_data': reference(S.app_data), 'account': reference(locations['Sign-in folder']),
                 'project': reference(S.project),
                 'shared': [reference(locations['Settings folder'] + '/' + name) for name in ('config.toml', 'AGENTS.md', 'skills')]}
        return value, locations

    def test_real_requested_input_shape_uses_lossless_native_paths(self):
        value, locations = self.fixture()
        self.assertTrue(checked_pending(value, S, locations)['pending_only'])

    def test_wrong_project_source_or_encoding_is_refused(self):
        import copy
        for change in ('project', 'supplier', 'encoding', 'identity'):
            value, locations = self.fixture()
            if change == 'project': value['project']['location']['bytes'] = list(b'/different')
            if change == 'supplier': value['supplier'] = 'different'
            if change == 'encoding': value['shared'][0]['location']['encoding'] = 'display'
            if change == 'identity': value['account']['object'] = None
            with self.subTest(change=change), self.assertRaises(Refusal): checked_pending(value, S, locations)


class EvidenceWriterTests(unittest.TestCase):
    def test_concrete_journal_preserves_repeated_facts_and_refuses_overwrite(self):
        import json
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve(); root.chmod(0o700)
            record = private_journal(root)
            record('phase', {'actual': 1}); record('phase', {'actual': 2})
            files = sorted(root.iterdir())
            self.assertEqual([json.loads(p.read_text())['actual'] for p in files], [1, 2])
            self.assertTrue(all(p.stat().st_mode & 0o777 == 0o600 for p in files))
            with self.assertRaises(FileExistsError): private_journal(root)('phase', {'actual': 3})


class TransitionAndLateClosureTests(unittest.TestCase):
    def test_transient_picker_value_is_reobserved_without_repeating_picker_press(self):
        now = [0.0]; io = FakeIO(now); original = io.observe; pending = [0]
        def observe(main, phase, deadline):
            if phase == 'picker' and pending[0] < 2:
                pending[0] += 1
                raise NotReady('picker relation still transitioning')
            return original(main, phase, deadline)
        io.observe = observe
        result = StageA(S, io, clock=lambda: now[0], sleep=lambda n: now.__setitem__(0, now[0] + n)).run()
        self.assertTrue(result['setup_saved'])
        self.assertEqual(io.events.count('press:Choose project folder…'), 1)
        self.assertEqual(io.events.count('terminate-original'), 1)

    def test_late_absence_is_recorded_separately_without_relabelling_initial_held_result(self):
        import j1_stage_a_phase as module
        now = [0.0]; records = []
        class Session(FakeIO):
            def __init__(self, *args):
                super().__init__(now); self.failure = 'terminate-false'; self.backend = None
            def hold_until_absent(self, result):
                self.assert_held = result['slot_must_remain_held']
                now[0] = 190; self.closed = True
        with patch.object(module, 'NativeSession', Session):
            result = run_prepared(S, {}, lambda k, v: records.append((k, dict(v))),
                                  clock=lambda: now[0], sleep=lambda n: now.__setitem__(0, now[0] + n))
        initial = [v for k, v in records if k == 'result'][0]
        self.assertTrue(initial['slot_must_remain_held']); self.assertFalse(initial['flow_complete'])
        self.assertTrue(result['original_absent']); self.assertFalse(result['slot_must_remain_held'])
        self.assertEqual(result['final_overrun'], 10); self.assertFalse(result['flow_complete'])


class FinalPreparationRegressionTests(unittest.TestCase):
    def test_unknown_path_write_is_retained_and_not_repeated(self):
        now = [0.0]; io = FakeIO(now); io.failure = 'unknown-path'; records = []
        runner = StageA(S, io, clock=lambda: now[0], sleep=lambda n: now.__setitem__(0, now[0] + n),
                        record=lambda k, v: records.append((k, v)))
        result = runner.run()
        self.assertEqual(io.events.count('enter-exact-path'), 1)
        self.assertIn('native exact-project path entry', result['actions'])
        returned = [v for k, v in records if k == 'path-entry-result'][0]
        self.assertIsNone(returned['rc']); self.assertIn('unknown', returned['error'])
        self.assertEqual(io.events.count('terminate-original'), 1)
        self.assertTrue(result['original_absent']); self.assertFalse(result['setup_saved'])

    def test_full_identity_checks_bracket_phase_not_each_property(self):
        ax = NativeAX.__new__(NativeAX); checks = []
        ax.check = lambda: checks.append('full-original-check')
        ax.main = 'main'; ax.app = 'app'; ax.same = lambda a, b: a == b; ax.clock = lambda: 0
        ax._controls = lambda *a: ([], 'Welcome', True)
        with patch('j1_stage_a_phase.phase_root', return_value='main'):
            ax.observe('main', 'main', 1)
        self.assertEqual(len(checks), 2)
        class Backend:
            def owner(self, ref): return 0, 17
            def attribute(self, ref, key):
                return {'return_code': 0, 'type': {'name': 'CFString'}, 'value': 'owned text'}, []
        ax.b = Backend(); ax.pid = 17
        for _ in range(5): self.assertEqual(ax.value('owned', 'AXTitle'), 'owned text')
        self.assertEqual(len(checks), 2)


class ReviewRepairTests(unittest.TestCase):
    def test_cleanup_intent_receipt_failure_still_dispatches_and_reports_evidence_gap(self):
        now = [0.0]; io = FakeIO(now)
        def record(kind, value):
            if kind == 'cleanup-intent': raise OSError('invented ENOSPC')
        result = StageA(S, io, clock=lambda: now[0],
                        sleep=lambda n: now.__setitem__(0, now[0] + n), record=record).run()
        self.assertEqual(io.events.count('terminate-original'), 1)
        self.assertTrue(result['original_absent'])
        self.assertFalse(result['flow_complete'])
        self.assertEqual(result['evidence_errors'][0]['record'], 'cleanup-intent')

    def test_native_cleanup_receipt_errors_cannot_suppress_or_repeat_request(self):
        for failed in ('normal-terminate-intent', 'normal-terminate-result'):
            with self.subTest(failed=failed):
                identity, kit, events = CleanupCorrespondenceTests().fixture()
                def record(kind, value):
                    if kind == failed: raise OSError('invented receipt failure')
                session = NativeSession(S, {}, record)
                session.backend = object(); session.appkit = kit; session.check = lambda got: None
                self.assertTrue(session.normal_terminate(identity, S))
                self.assertEqual(events.count('terminate'), 1)
                self.assertEqual(session.evidence_errors[0]['record'], failed)
                with self.assertRaises(Refusal): session.normal_terminate(identity, S)
                self.assertEqual(events.count('terminate'), 1)

    def test_failed_launch_intent_is_known_undispatched_but_dispatch_timeout_is_unknown(self):
        import subprocess
        def failed(*args): raise OSError('invented launch-intent write failure')
        session = NativeSession(S, {}, failed)
        with patch('subprocess.run') as dispatch:
            with self.assertRaises(OSError): session.launch_once(S)
        dispatch.assert_not_called()
        self.assertFalse(session.launch_unknown())
        session = NativeSession(S, {}, lambda *a: None)
        with patch('subprocess.run', side_effect=subprocess.TimeoutExpired('open', 5)) as dispatch:
            with self.assertRaises(subprocess.TimeoutExpired): session.launch_once(S)
            with self.assertRaises(Refusal): session.launch_once(S)
        self.assertEqual(dispatch.call_count, 1)
        self.assertTrue(session.launch_unknown())

    def test_changed_confirmation_destinations_or_abbreviation_never_receive_affirmative(self):
        for change in ('settings', 'account', 'abbreviated'):
            with self.subTest(change=change):
                now = [0.0]; io = FakeIO(now); observe = io.observe
                def altered(main, phase, deadline):
                    view = observe(main, phase, deadline)
                    if phase == 'confirmation':
                        if change == 'abbreviated': view.text = 'Desktop setup\n' + S.project + '\n' + S.app_data
                        else:
                            key = 'Settings folder' if change == 'settings' else 'Sign-in folder'
                            view.text = view.text.replace(LOCATIONS[key], LOCATIONS[key] + '-different')
                    return view
                io.observe = altered
                result = StageA(S, io, clock=lambda: now[0], sleep=lambda n: now.__setitem__(0, now[0] + n)).run()
                self.assertFalse(result['setup_saved'])
                self.assertNotIn('press:Create settings and save for next launch', io.events)
                self.assertEqual(io.events.count('terminate-original'), 1)

    def test_same_button_cannot_revalidate_a_changed_native_statement(self):
        ax = NativeAX.__new__(NativeAX)
        ax.last_phase = 'confirmation'; ax.same = lambda a, b: a == b
        button = c('Create settings and save for next launch')
        previous = View('main', 'question', [button], 'reviewed full statement')
        ax.observe = lambda *args: View('main', 'question', [button], 'changed full statement')
        with self.assertRaisesRegex(Refusal, 'content changed'):
            ax.revalidate(previous, button, 10)

    def test_statement_is_checked_again_at_actual_press_boundary(self):
        from types import SimpleNamespace
        from unittest.mock import Mock
        ax = NativeAX.__new__(NativeAX)
        button = c('Create settings and save for next launch')
        ax.last_phase = 'confirmation'; ax.main = 'main'; ax.same = lambda a, b: a == b
        ax.last_view = View('main', 'question', [button], 'reviewed full statement')
        ax.observe = lambda *args: View('main', 'question', [button], 'changed just before dispatch')
        ax.clock = lambda: 0; ax.check = lambda: None; ax._bound_target = lambda *a: None
        def actions(ref, out): out._obj.value = 1; return 0
        dispatch = Mock(return_value=0)
        ax.b = SimpleNamespace(a=SimpleNamespace(AXUIElementCopyActionNames=actions,
                                                AXUIElementPerformAction=dispatch), held=[],
                               scalar=lambda x: 'AXPress', array=lambda *a: [1], string=lambda x: x)
        with self.assertRaisesRegex(Refusal, 'statement changed'):
            ax.press(button, 10)
        dispatch.assert_not_called()

    def test_project_prefix_does_not_authorize_review(self):
        now = [0.0]; io = FakeIO(now); observe = io.observe
        def altered(main, phase, deadline):
            view = observe(main, phase, deadline)
            if phase == 'main' and io.selected: view.text = S.project + '-different'
            return view
        io.observe = altered
        result = StageA(S, io, clock=lambda: now[0], sleep=lambda n: now.__setitem__(0, now[0] + n)).run()
        self.assertFalse(result['setup_saved'])
        self.assertNotIn('press:Review setup', io.events)

    def test_unknown_picker_container_refuses_before_any_content_read(self):
        for role in ('AXGroup', 'AXScrollArea'):
            with self.subTest(role=role):
                ax = NativeAX.__new__(NativeAX); ax.clock = lambda: 0; ax.same = lambda a, b: a == b
                ax.role = lambda ref: {'panel': 'AXSheet', 'unknown': role, 'open': 'AXButton'}[ref]
                reads = []
                def value(ref, name):
                    reads.append((ref, name))
                    if ref == 'panel' and name == 'AXChildren': return ['open', 'unknown']
                    raise AssertionError('unclassified content must not be read')
                ax.value = value
                with self.assertRaisesRegex(Refusal, 'unclassified picker structure'):
                    ax._controls('panel', True, 10)
                self.assertEqual(reads, [('panel', 'AXChildren')])

    def test_flat_picker_reads_no_static_text_or_path_history(self):
        ax = NativeAX.__new__(NativeAX); ax.clock = lambda: 0; ax.same = lambda a, b: a == b
        ax.project = S.project; ax.path_entry_verified = True
        roles = {'panel': 'AXSheet', 'open': 'AXButton', 'private': 'AXStaticText', 'directory': 'AXPathControl'}
        ax.role = lambda ref: roles[ref]
        def value(ref, name):
            if ref == 'panel' and name == 'AXChildren': return ['private', 'directory', 'open']
            if ref == 'directory' and name == 'AXValue': return S.project
            if ref == 'open' and name == 'AXTitle': return 'Open'
            if ref == 'open' and name == 'AXEnabled': return True
            raise AssertionError('private content or control descendants read')
        ax.value = value
        controls, text, _ = ax._controls('panel', True, 10)
        self.assertEqual(text, S.project)
        self.assertEqual([x.label for x in controls], ['Open'])

    def test_pid_reuse_proves_original_absent_without_targeting_replacement(self):
        from types import SimpleNamespace
        identity = {'pid': 17, 'start_sec': 10, 'start_usec': 20}
        session = NativeSession(S, {}, lambda *a: None)
        occupied = SimpleNamespace(returncode=0, stdout='17 /invented/replacement\n')
        with patch('subprocess.run', return_value=occupied):
            session.process_birth = lambda pid: (10, 20)
            self.assertFalse(session.absent(identity))
            session.process_birth = lambda pid: (11, 20)
            self.assertTrue(session.absent(identity))
            session.process_birth = lambda pid: (_ for _ in ()).throw(OSError('unknown'))
            self.assertFalse(session.absent(identity))
        with patch('subprocess.run', return_value=SimpleNamespace(returncode=1, stdout='')):
            self.assertTrue(session.absent(identity))
        with patch('subprocess.run', return_value=SimpleNamespace(returncode=1, stdout='', stderr='observation denied')):
            self.assertFalse(session.absent(identity))
        self.assertFalse(session.termination_used)

    def test_slow_operation_records_failed_overrun_not_a_hard_deadline_pass(self):
        now = [0.0]; io = FakeIO(now); observe = io.observe
        def delayed(main, phase, deadline):
            view = observe(main, phase, deadline)
            if phase == 'picker': now[0] = 185
            return view
        io.observe = delayed
        result = StageA(S, io, clock=lambda: now[0], sleep=lambda n: now.__setitem__(0, now[0] + n)).run()
        self.assertEqual(result['cleanup_started'], 185)
        self.assertEqual(result['overrun'], 5)
        self.assertFalse(result['flow_complete'])


class ReviewedPacketAdmissionTests(unittest.TestCase):
    def test_changed_case_with_regenerated_manifests_fails_before_native_preparation(self):
        import hashlib
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); packet = root / 'packet'; project = packet / 'session/project'
            project.mkdir(parents=True)
            (project / 'BRIEF.md').write_text('reviewed invented task')
            (packet / 'README.md').write_text('invented packet')
            def manifest(name, members):
                rows = []
                for member in members:
                    digest = hashlib.sha256((packet / member).read_bytes()).hexdigest()
                    rows.append({'manifest': name, 'path': member, 'sha256': digest})
                (packet / name).write_text(''.join(row['sha256'] + '  ' + row['path'] + '\n' for row in rows))
                return rows
            def regenerate():
                case = manifest('case-manifest.sha256', ['session/project/BRIEF.md'])
                return manifest('PACKET.sha256', ['README.md', 'case-manifest.sha256']) + case
            reviewed = regenerate()
            checked_packet(packet, reviewed)
            exe = root / 'Test.app/Contents/MacOS/app'; exe.parent.mkdir(parents=True); exe.write_bytes(b'invented executable')
            subject = replace(S, bundle=str(root / 'Test.app'), executable=str(exe),
                              executable_sha256=hashlib.sha256(exe.read_bytes()).hexdigest(),
                              project=str(project), app_data=str(root / 'home/Library/Application Support' / S.identifier))
            preflight = {'source': subject.source, 'bundle': subject.bundle, 'identifier': subject.identifier,
                         'executable': subject.executable, 'executable_sha256': subject.executable_sha256,
                         'packet': str(packet), 'development_state': [], 'manifest_checks': reviewed}
            with patch.object(Path, 'home', return_value=root / 'home'), \
                 patch('subprocess.check_output', side_effect=RuntimeError('mock parent checkpoint')) as parent:
                with self.assertRaisesRegex(RuntimeError, 'parent checkpoint'):
                    NativeSession(subject, preflight, lambda *a: None).admit(subject)
                parent.assert_called_once()
            (project / 'BRIEF.md').write_text('changed case')
            regenerate()
            with patch.object(Path, 'home', return_value=root / 'home'), patch('subprocess.check_output') as parent:
                with self.assertRaisesRegex(Refusal, 'manifest differs'):
                    NativeSession(subject, preflight, lambda *a: None).admit(subject)
                parent.assert_not_called()
            for rows in (reviewed[:-1], reviewed + [dict(reviewed[0])]):
                with self.assertRaises(Refusal): checked_packet(packet, rows)
