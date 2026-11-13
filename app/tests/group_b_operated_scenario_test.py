#!/usr/bin/env python3
"""The operated scenario's walk and checks, replayed on recorded views (DEL-09-02 examination tooling).

Nothing here starts an application or touches a screen: walk.mjs is given a stand-in for the supplier's window
service. The wrong-state files show the unchanged walk and checks rejecting states that are known to be wrong.
"""
import contextlib
import errno
import importlib.util
import io
import json
import os
import plistlib
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

APP = Path(__file__).resolve().parents[1]
OPERATED = APP / 'examination/standalone/operated'
WALK = OPERATED / 'walk.mjs'
REPLAY = OPERATED / 'replay.mjs'
SCENARIO = OPERATED / 'first-use-setup.scenario.json'
FIXTURES = APP / 'tests/group_b_operated_fixtures/first-use-setup'
VIEWS = FIXTURES / 'views.json'
NODE = shutil.which('node')
OUTCOMES = {'SETUP CHOICES REVIEWED', 'REFUSAL: REVIEW SETUP UNAVAILABLE BEFORE ANY CHOICE',
            'REFUSAL: REVIEW SETUP UNAVAILABLE WITH EXISTING SETTINGS AND NOTHING CHOSEN',
            'STARTING STATE: SETUP REQUIRED, APP DATA UNDER THE THROWAWAY HOME'}
HARNESS = '''
import { readFileSync } from 'node:fs';
const walk = await import(process.argv[1]);
const scenario = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const recorded = JSON.parse(readFileSync(process.argv[3], 'utf8'));
let texts = recorded.views.map(view => view.text);
const touched = [];
let next = 0, asked = 0, preface = null;  // the two views before any click come from the first recorded view
const nextView = () => (asked++ < 2 ? (preface ?? [texts[0], texts[0]])[asked - 1] : texts[next++]);
const service = new Proxy({}, { get(_, name) {
  if (name === 'then') return undefined;
  touched.push(String(name));
  if (name === 'get_app_state') return async () => ({ app: viewOf.app, text: nextView() });
  if (name === 'click') return async () => {};
  throw new Error('a method the walk must never use: ' + String(name));
} });
const viewOf = { app: recorded.bundle };
const watched = (change = {}) => () => ({ pid: process.pid, running: true, at_ms: Date.now(), children: [],
  executable: recorded.bundle + '/Contents/MacOS/chirality-app-v4', ...change });
const base = { sky: service, scenario, app: recorded.app, home: recorded.home, bundle: recorded.bundle, pid: process.pid,
  readWatch: watched(), sleep: async () => {} };
const out = await (async () => { CASE })();
console.log(JSON.stringify({ out, touched }));
'''


def setUpModule():
    if NODE is None:
        if os.environ.get('CI'):
            raise RuntimeError('node is required for the operated scenario tests in CI')
        raise unittest.SkipTest('node is not installed')


def replay(*paths):
    done = subprocess.run([NODE, str(REPLAY), *map(str, paths)], capture_output=True, text=True)
    return done.returncode, (json.loads(done.stdout) if done.stdout.strip() else None), done.stderr


def harness(case):
    done = subprocess.run([NODE, '--input-type=module', '-e', HARNESS.replace('CASE', case), WALK.as_uri(), str(SCENARIO),
                           str(VIEWS)], capture_output=True, text=True)
    if done.returncode != 0:
        raise AssertionError(done.stderr)
    return json.loads(done.stdout)


class Replay(unittest.TestCase):
    def test_the_recorded_views_show_the_outcome_and_both_refusals(self):
        code, report, said = replay(SCENARIO, VIEWS)
        self.assertEqual((code, report['verdict'], report['stopped']), (0, 'pass', None), said)
        self.assertEqual(report['outcomes'], {name: 'shown' for name in OUTCOMES})
        self.assertEqual([step['id'] for step in report['steps']], [f'S{n}' for n in range(1, 9)])
        self.assertTrue(all(step['checks'] and all(check['pass'] for check in step['checks']) for step in report['steps']))
        self.assertEqual([call['call'] for call in report['calls']],
                         ['get_app_state'] * 3 + ['click', 'get_app_state'] * 7)  # two whole views first, then the walk
        self.assertEqual([view['whole'] for view in report['whole_views_before_any_click']], [True, True])
        self.assertEqual({call['app'] for call in report['calls']}, {'dev.chirality.app-v4.candidate.invented'})

    def test_each_known_wrong_state_is_rejected_at_its_step_and_only_there(self):
        wrong = sorted(FIXTURES.glob('wrong.*.json'))
        self.assertEqual(len(wrong), 6)
        for path in wrong:
            with self.subTest(path.name):
                expected = json.loads(path.read_text())
                code, report, said = replay(SCENARIO, VIEWS, path)
                if 'stops' in expected:  # a control that is not the one named: nothing is clicked, and nothing is concluded
                    self.assertEqual((code, report['verdict']), (2, expected['verdict']), said)
                    self.assertIn(f"stopped at {expected['stops']}: the control to click was found 0 times", report['stopped'])
                    self.assertEqual(report['outcomes']['REFUSAL: REVIEW SETUP UNAVAILABLE WITH EXISTING SETTINGS AND NOTHING CHOSEN'],
                                     'not shown')
                    self.assertEqual(len([call for call in report['calls'] if call['call'] == 'click']), 5)
                    continue
                self.assertEqual((code, report['verdict']), (1, 'fail'), said)
                failed = {step['id']: [check['expectation'] for check in step['checks'] if not check['pass']]
                          for step in report['steps'] if any(not check['pass'] for check in step['checks'])}
                self.assertEqual(failed, {step: [expectation] for step, expectation in expected['fails'].items()})
                self.assertEqual({name for name, state in report['outcomes'].items() if state != 'shown'},
                                 {expected['outcome_not_shown']})
                self.assertIn('found:', said)

    def test_the_whole_result_arrives_through_a_pipe(self):
        done = subprocess.run([NODE, str(REPLAY), str(SCENARIO), str(VIEWS)], capture_output=True, text=True)
        self.assertGreater(len(done.stdout), 65536)  # longer than a pipe holds at once
        self.assertEqual(json.loads(done.stdout)['verdict'], 'pass')

    def test_a_wrong_state_file_that_does_not_match_the_views_is_an_error_not_a_pass(self):
        bad = FIXTURES.parent / 'does-not-apply.json'
        bad.write_text(json.dumps({'replace': [{'view': 0, 'from': 'button Not On The Page', 'to': 'x'}]}))
        self.addCleanup(bad.unlink)
        code, report, said = replay(SCENARIO, VIEWS, bad)
        self.assertEqual((code, report), (2, None), said)


class TheWalkItself(unittest.TestCase):
    def test_it_uses_a_view_and_a_click_and_no_other_method_of_the_service(self):
        result = harness('return (await walk.run(base)).verdict;')
        self.assertEqual(result['out'], 'pass')
        self.assertEqual(set(result['touched']), {'get_app_state', 'click'})

    def test_it_refuses_before_any_call_unless_a_running_development_build_is_named_by_its_identifier(self):
        cases = {'a name, not an identifier': "{ ...base, app: 'Chirality App v4 (development invented)' }",
                 'the release identifier': "{ ...base, app: 'com.chirality.app' }",
                 'another application': "{ ...base, app: 'com.apple.finder' }",
                 'no identifier': '{ ...base, app: undefined }',
                 'a watch file that says the process has gone': '{ ...base, readWatch: watched({ running: false }) }',
                 'a watch file last written a minute ago': '{ ...base, readWatch: watched({ at_ms: Date.now() - 60000 }) }',
                 'a watch file last written four seconds ago': '{ ...base, readWatch: watched({ at_ms: Date.now() - 4000 }) }',
                 'a watched executable outside the bundle': "{ ...base, readWatch: watched({ executable: '/invented/elsewhere/Contents/MacOS/chirality-app-v4' }) }",
                 'a watched executable not known': '{ ...base, readWatch: watched({ executable: null }) }',
                 'no bundle': '{ ...base, bundle: undefined }',
                 'a bundle that is not an .app folder': "{ ...base, bundle: '/invented/candidate' }",
                 'a scenario with no steps': '{ ...base, scenario: { ...scenario, steps: [] } }',
                 'a step with nothing expected': '{ ...base, scenario: { ...scenario, steps: scenario.steps.map((s, i) => i === 6 ? { ...s, expect: [] } : s) } }',
                 'an outcome naming no such step': "{ ...base, scenario: { ...scenario, outcomes: { X: ['S99'] } } }",
                 'a watch file for another process': '{ ...base, readWatch: watched({ pid: 1 }) }',
                 'a watch file that cannot be read': '{ ...base, readWatch: () => null }',
                 'no watch file': '{ ...base, readWatch: undefined }',
                 'no process number': '{ ...base, pid: undefined }',
                 'a home that is not absolute': "{ ...base, home: 'relative/home' }"}
        for name, options in cases.items():
            with self.subTest(name):
                result = harness(f'const r = await walk.run({options}); return [r.verdict, r.stopped, r.calls.length, r.steps.length];')
                verdict, stopped, calls, steps = result['out']
                self.assertEqual((verdict, calls, steps, result['touched']), ('inconclusive', 0, 0, []))
                self.assertTrue(stopped.startswith(('refused before any call: ', 'stopped before any call: ')), stopped)

    def test_it_stops_without_a_further_call_when_a_view_holds_something_that_is_not_the_page(self):
        window = '0 standard window Chirality, Secondary Actions: Raise'
        inside = {'a sheet': '\\t900 sheet Confirm', 'a dialog': '\\t900 dialog', 'an alert': '\\t900 alert Allow?',
                  'a kind of thing nobody listed': '\\t900 popover Something new'}
        for name, line in inside.items():
            with self.subTest(name):
                result = harness(f"texts[2] = texts[2].replace('{window}', '{window}\\n{line}'); const r = await walk.run(base); "
                                 'return [r.verdict, r.stopped, r.calls.length];')
                verdict, stopped, calls = result['out']
                self.assertEqual((verdict, calls), ('inconclusive', 7), stopped)  # five views, two clicks, then nothing
                self.assertIn('stopped at S3: the window holds something that is not the page', stopped)
                self.assertIn('no agent answers a prompt or a dialog', stopped)
        beside = {'a second window': '900 standard window Confirm', 'a system dialog beside it': '900 system dialog Allow?',
                  'something unnamed beside it': '900 group'}
        for name, line in beside.items():
            with self.subTest(name):
                result = harness(f"texts[2] = texts[2] + '\\n{line}'; const r = await walk.run(base); "
                                 'return [r.verdict, r.stopped, r.calls.length];')
                verdict, stopped, calls = result['out']
                self.assertEqual((verdict, calls), ('inconclusive', 7), stopped)
                self.assertIn('the view holds something beside the window "Chirality"', stopped)
        for name, change in (('a window whose title only begins the same way', "'standard window Chirality Setup, Secondary Actions: Raise'"),
                             ('no window', "'group'")):
            with self.subTest(name):
                result = harness(f"texts[0] = texts[0].replace('standard window Chirality, Secondary Actions: Raise', {change}); "
                                 'const r = await walk.run(base); return [r.verdict, r.stopped, r.calls.length];')
                self.assertEqual((result['out'][0], result['out'][2]), ('inconclusive', 1), result['out'][1])

    def test_page_words_about_a_dialog_do_not_stop_it(self):
        text = json.loads(VIEWS.read_text())['views'][3]['text']
        self.assertNotIn('dialog', ' '.join(line.strip().split(' ')[1] for line in text.split('\n')[1:] if line.strip()))
        result = harness("texts[3] = texts[3] + '\\n\\t\\t\\t\\t\\t\\t\\t999 text The App asks you to confirm in its own dialog.'; "
                         'return (await walk.run(base)).verdict;')
        self.assertEqual(result['out'], 'pass')

    def test_it_stops_when_the_view_is_of_another_window_or_the_build_ends(self):
        result = harness("texts[1] = texts[1].replace('standard window Chirality', 'standard window Something Else'); "
                         'const r = await walk.run(base); return [r.verdict, r.stopped, r.calls.length];')
        self.assertEqual(result['out'][0], 'inconclusive')
        self.assertIn('beside the window "Chirality"', result['out'][1])
        self.assertEqual(result['out'][2], 5)
        result = harness('let readings = 0; const r = await walk.run({ ...base, readWatch: () => watched({ running: ++readings < 4 })() }); '
                         'return [r.verdict, r.stopped];')
        self.assertEqual(result['out'][0], 'inconclusive')
        self.assertIn('no longer shows the build running', result['out'][1])
        result = harness("viewOf.app = '/invented/another/Other.app'; const r = await walk.run(base); "
                         'return [r.verdict, r.stopped, r.calls.length];')
        self.assertEqual((result['out'][0], result['out'][2]), ('inconclusive', 1))
        self.assertIn('the view does not say it is of the bundle', result['out'][1])
        result = harness('viewOf.app = undefined; const r = await walk.run(base); return [r.verdict, r.stopped, r.calls.length];')
        self.assertEqual((result['out'][0], result['out'][2]), ('inconclusive', 1))  # a view that names no application is not taken as ours

    def test_an_expected_text_or_location_name_present_twice_is_not_what_was_expected(self):
        # A second copy is put inside the page, before the window's close button, so that only the count is wrong.
        cases = (('a text', 2, '\\t\\t\\t901 text Ready to review. Nothing is created or saved until you confirm.', 'S3'),
                 ('a location name', 4, '\\t\\t\\t901 text Saved choices\\n\\t\\t\\t902 text /invented/elsewhere', 'S5'),
                 ('the start of a text', 1, '\\t\\t\\t901 text Launch: setup-required. And again.', 'S2'))
        for name, view, lines, step in cases:
            with self.subTest(name):
                result = harness(f"texts[{view}] = texts[{view}].replace('\\n\\t41 close button', '\\n{lines}\\n\\t41 close button'); "
                                 'const r = await walk.run(base); '
                                 'return [r.verdict, r.steps.filter(s => s.checks.some(c => !c.pass)).map(s => s.id), '
                                 'r.steps.flatMap(s => s.checks.filter(c => !c.pass).map(c => String(c.found)))];')
                verdict, failed, found = result['out']
                self.assertEqual((verdict, failed), ('fail', [step]), found)
                self.assertTrue(any('2 times' in text for text in found), found)

    def test_no_view_is_made_once_the_watch_stops_showing_the_build_running(self):
        # The build goes during the wait after the fourth step's click: the view that would follow is not made.
        result = harness('''let gone = false; const r = await walk.run({ ...base, readWatch: () => watched({ running: !gone })(),
            sleep: async () => { gone = true; } });
          return [r.verdict, r.stopped, r.calls.map(c => c.call).join(' ')];''')
        verdict, stopped, calls = result['out']
        self.assertEqual(verdict, 'inconclusive')
        self.assertIn('stopped at S4, before its view: the watch file no longer shows the build running', stopped)
        self.assertTrue(calls.endswith('click'), calls)  # the click had been made; no view after it
        self.assertEqual(calls.count('get_app_state'), 5)
        # The build goes during the last view: the walk does not pass.
        result = harness('''let views = 0; const service2 = { get_app_state: async () => { views += 1; return { app: viewOf.app, text: nextView() }; }, click: async () => {} };
          const r = await walk.run({ ...base, sky: service2, readWatch: () => watched({ running: views < 10 })() });
          return [r.verdict, r.stopped, r.steps.at(-1).child_processes];''')
        verdict, stopped, children = result['out']
        self.assertEqual(verdict, 'inconclusive')
        self.assertIn('stopped after S8', stopped)
        self.assertEqual(children, 'see why the walk stopped')

    def test_a_control_is_the_one_whose_words_are_exactly_the_scenarios(self):
        for words in ('Use my existing Codex settingsBackup', 'Use my existing Codex settings and delete my sign-in\u2026'):
            with self.subTest(words):
                result = harness("texts = texts.map(t => t.replace(/(radio button Value: [01], )Use my existing Codex settings [^\\n]*/, '$1" + words + "')); "
                                 'const r = await walk.run(base); return [r.verdict, r.stopped, r.calls.filter(c => c.call === "click").length];')
                verdict, stopped, clicks = result['out']
                self.assertNotEqual(verdict, 'pass')
                self.assertEqual(clicks, 5, stopped)  # the five clicks before it; the differently named control is not clicked
                self.assertIn('S7', stopped)

    def test_a_view_rebuilt_from_differences_supports_neither_a_pass_nor_a_failure(self):
        difference = ('The following is a diff from the previous accessibility tree for Window: "Chirality"\\n'
                      'The focused UI element is 2 HTML content')
        # At a step: the walk stops there. No call follows, the step has no credited check, and nothing after is reached.
        result = harness(f"texts[1] = '{difference}'; const r = await walk.run(base); "
                         'return [r.verdict, r.stopped, r.calls.map(c => c.call).join(" "), r.steps.map(s => [s.id, s.checks.length]), '
                         'r.outcomes, typeof r.steps.at(-1).rebuilt_for_reading, r.steps.at(-1).returned.slice(0, 30)];')
        verdict, stopped, calls, steps, outcomes, rebuilt, returned = result['out']
        self.assertEqual(verdict, 'inconclusive', stopped)
        self.assertIn('stopped at S2: the view came back as differences', stopped)
        self.assertEqual(calls, 'get_app_state get_app_state get_app_state click get_app_state')  # and none after it
        self.assertEqual(steps[-1], ['S2', 0])
        self.assertEqual(outcomes['STARTING STATE: SETUP REQUIRED, APP DATA UNDER THE THROWAWAY HOME'], 'not shown')
        self.assertEqual({state for name, state in outcomes.items() if 'STARTING STATE' not in name and 'BEFORE ANY CHOICE' not in name},
                         {'not reached'})
        self.assertEqual((rebuilt, returned), ('string', 'The following is a diff from t'))  # kept, for reading
        # Before any click: the second of the two views comes back as differences. Nothing is clicked.
        for name, which, made in (('the second', f"[texts[0], '{difference}']", 2), ('the first', f"['{difference}', texts[0]]", 1)):
            with self.subTest(name):
                result = harness(f'preface = {which}; const r = await walk.run(base); '
                                 'return [r.verdict, r.stopped, r.calls.map(c => c.call).join(" "), r.steps.length];')
                verdict, stopped, calls, steps = result['out']
                self.assertEqual((verdict, calls, steps), ('inconclusive', ' '.join(['get_app_state'] * made), 0), stopped)
                self.assertIn(f'stopped at {name} view before any click: the view came back as differences', stopped)

    def test_a_child_process_of_the_app_stops_the_walk_and_fails_it_at_whichever_reading_shows_it(self):
        child = "[{ pid: 4242, command: '/invented/codex' }]"
        # Shown once, at the reading after the fourth step's click and wait, and gone by the next reading: no view follows.
        result = harness(f'''let waited = false, shown = false;
          const r = await walk.run({{ ...base, sleep: async () => {{ waited = true; }},
            readWatch: () => watched({{ children: waited && !shown ? (shown = true, {child}) : [] }})() }});
          return [r.verdict, r.stopped, r.calls.map(c => c.call).join(' ')];''')
        verdict, stopped, calls = result['out']
        self.assertEqual(verdict, 'fail', stopped)
        self.assertIn('stopped at S4, before its view: the App has a child process (1), and this scenario starts none', stopped)
        self.assertTrue(calls.endswith('click'), calls)
        self.assertEqual(calls.count('get_app_state'), 5)
        # Shown at every reading from the start: nothing is called at all.
        result = harness(f'return await walk.run({{ ...base, readWatch: watched({{ children: {child} }}) }});')
        self.assertEqual((result['out']['verdict'], result['out']['calls']), ('fail', []), result['out']['stopped'])
        self.assertIn('stopped before any call', result['out']['stopped'])
        # Shown at the reading after the first view before any click: the second is not made.
        result = harness(f'''let readings = 0;
          const r = await walk.run({{ ...base, readWatch: () => watched({{ children: ++readings === 3 ? {child} : [] }})() }});
          return [r.verdict, r.stopped, r.calls.length];''')
        self.assertEqual(result['out'][0::2], ['fail', 1], result['out'][1])
        self.assertIn('after the first view before any click', result['out'][1])
        result = harness(f'scenario.starts_no_process = false; return (await walk.run({{ ...base, readWatch: watched({{ children: {child} }}) }})).verdict;')
        self.assertEqual(result['out'], 'pass')  # a scenario that may start a process is not stopped by one

    def test_a_watch_file_without_its_list_of_children_is_not_taken_as_running(self):
        result = harness('return await walk.run({ ...base, readWatch: watched({ children: undefined }) });')
        self.assertEqual((result['out']['verdict'], result['out']['calls']), ('inconclusive', []))

    def test_it_never_clicks_a_control_whose_words_end_with_an_ellipsis_or_one_it_cannot_find_exactly_once(self):
        result = harness("scenario.steps[4] = { id: 'S5', act: 'click', control: { kind: 'button', label: 'Create settings and save for next launch\\u2026' }, expect: [{ text: 'x' }] }; "
                         'const r = await walk.run(base); return [r.verdict, r.stopped, r.calls.filter(c => c.call === "click").length];')
        self.assertEqual(result['out'][0], 'inconclusive')
        self.assertIn('never clicked', result['out'][1])
        self.assertEqual(result['out'][2], 3)  # the three clicks before it, and not this one
        result = harness("scenario.steps[1].control.label = 'Not On The Page'; const r = await walk.run(base); "
                         'return [r.verdict, r.stopped, r.calls.length];')
        self.assertEqual((result['out'][0], result['out'][2]), ('inconclusive', 3))
        self.assertIn('found 0 times', result['out'][1])

    def test_an_unavailable_control_is_not_clicked_and_that_is_a_failure(self):
        result = harness("scenario.steps.splice(1, 2); scenario.outcomes = {}; const r = await walk.run(base); "  # S4 straight after S1: Review setup is unavailable
                         'return [r.verdict, r.stopped, r.calls.filter(c => c.call === "click").length];')
        self.assertEqual((result['out'][0], result['out'][2]), ('fail', 0))
        self.assertIn('unavailable', result['out'][1])

    def test_a_view_returned_as_differences_is_applied_to_the_view_before_it(self):
        result = harness('''
          const before = walk.parseView('Window: "Chirality"\\n0 standard window Chirality\\n\\t1 button (disabled) Review setup\\n\\t2 summary Details, Value: off\\n\\t\\t3 text Details\\n\\t4 close button');
          const after = walk.applyDifference(before, 'The following is a diff from the previous accessibility tree for Window: "Chirality"\\nRemoved element IDs: 2-3\\n~\\t1 button Review setup\\n+\\t5 container (expanded)\\n+\\t\\t6 summary Details, Value: on\\nThe focused UI element is 6');
          const same = walk.applyDifference(after, 'There has been no change in the accessibility tree for Window: "Chirality".');
          return [after.map(e => e.index + ':' + e.depth + ':' + e.content), same.length];''')
        self.assertEqual(result['out'], [['0:0:standard window Chirality', '1:1:button Review setup', '5:1:container (expanded)',
                                          '6:2:summary Details, Value: on', '4:1:close button'], 5])


class TheWatchFile(unittest.TestCase):
    def test_it_says_running_with_the_children_and_then_that_the_process_has_gone(self):
        folder = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, folder, True)
        parent = subprocess.Popen(['/bin/sh', '-c', 'sleep 30 & wait'])
        self.addCleanup(lambda: (parent.poll() is None and parent.kill(), parent.wait()))
        watch = subprocess.Popen([sys.executable, '-B', str(OPERATED / 'watch.py'), str(parent.pid), str(folder / 'watch.json')])
        self.addCleanup(lambda: (watch.poll() is None and watch.kill(), watch.wait()))
        deadline = time.monotonic() + 10
        seen = None
        while time.monotonic() < deadline:
            if (folder / 'watch.json').exists():
                seen = json.loads((folder / 'watch.json').read_text())
                if seen['children']:
                    break
            time.sleep(0.1)
        self.assertEqual((seen['pid'], seen['running']), (parent.pid, True))
        self.assertTrue(abs(seen['at_ms'] - time.time() * 1000) < 5000)
        self.assertEqual([child['command'].rsplit('/', 1)[-1] for child in seen['children']], ['sleep'])
        subprocess.run(['/bin/kill', str(seen['children'][0]['pid'])])
        parent.wait(timeout=10)
        self.assertEqual(watch.wait(timeout=10), 0)
        last = json.loads((folder / 'watch.json').read_text())
        self.assertEqual((last['running'], last['children'], last['executable']), (False, [], None))
        self.assertEqual(os.listdir(folder), ['watch.json'])

    def test_a_process_that_has_exited_or_another_program_at_the_number_is_not_running(self):
        spec = importlib.util.spec_from_file_location('watch_under_test', OPERATED / 'watch.py')
        watch = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(watch)
        app = '/invented/bundle.app/Contents/MacOS/chirality-app-v4'
        live = watch.state(41, None, [(41, 7, 'S', app), (42, 41, 'S', '/invented/codex'), (43, 1, 'S', '/invented/other')])
        self.assertEqual((live['running'], live['executable'], live['children']),
                         (True, app, [{'pid': 42, 'command': '/invented/codex'}]))
        for name, rows in (('exited and not collected', [(41, 7, 'Z', '<defunct>')]),
                           ('exited, its child still listed', [(41, 7, 'Z+', '<defunct>'), (42, 41, 'S', '/invented/codex')]),
                           ('another program at the number', [(41, 7, 'S', '/invented/something-else')]),
                           ('not in the listing', [(40, 7, 'S', app)])):
            with self.subTest(name):
                seen = watch.state(41, app, rows)
                self.assertEqual((seen['running'], seen['executable'], seen['children']), (False, None, []))

    def test_it_refuses_anything_but_one_process_number_and_a_file(self):
        for arguments in ([], ['12'], ['abc', 'file'], ['1', 'file'], ['12', 'file', 'more']):
            with self.subTest(arguments=arguments):
                done = subprocess.run([sys.executable, '-B', str(OPERATED / 'watch.py'), *arguments], capture_output=True, text=True)
                self.assertEqual(done.returncode, 2)


class Detached(unittest.TestCase):
    def test_the_command_runs_in_a_session_of_its_own_with_its_output_in_the_folder(self):
        folder = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, folder, True)
        done = subprocess.run([sys.executable, '-B', str(OPERATED / 'detached.py'), str(folder), 'stand-in', '--',
                               '/bin/sh', '-c', 'echo to-out; echo to-err >&2; sleep 30'], capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        started = json.loads(done.stdout)
        self.addCleanup(lambda: subprocess.run(['/bin/kill', str(started['pid'])], capture_output=True))
        self.assertEqual(os.getsid(started['pid']), started['pid'])  # the leader of a new session
        self.assertNotEqual(os.getsid(started['pid']), os.getsid(0))
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline and not Path(started['err']).read_text():
            time.sleep(0.05)
        self.assertEqual((Path(started['out']).read_text(), Path(started['err']).read_text()), ('to-out\n', 'to-err\n'))
        self.assertEqual(sorted(os.listdir(folder)), ['stand-in.err', 'stand-in.out', 'stand-in.started.json'])
        os.kill(started['pid'], 0)  # still running after the starter returned
        written = json.loads((folder / 'stand-in.started.json').read_text())
        self.assertEqual(written, started)
        self.assertEqual(written['command'], ['/bin/sh', '-c', 'echo to-out; echo to-err >&2; sleep 30'])

    def test_no_shell_reads_the_command_and_nothing_else_is_started(self):
        folder = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, folder, True)
        marker = folder / 'made-by-a-shell'
        done = subprocess.run([sys.executable, '-B', str(OPERATED / 'detached.py'), str(folder), 'plain', '--',
                               '/bin/echo', f'$(touch {marker})', ';', 'touch', str(marker), '*'], capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline and not (folder / 'plain.out').read_text():
            time.sleep(0.05)
        self.assertEqual((folder / 'plain.out').read_text(), f'$(touch {marker}) ; touch {marker} *\n')  # printed, not run
        self.assertFalse(marker.exists())

    def test_it_refuses_a_missing_folder_existing_output_and_a_malformed_call(self):
        folder = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, folder, True)
        (folder / 'taken.out').write_text('earlier')
        tool = [sys.executable, '-B', str(OPERATED / 'detached.py')]
        for name, arguments in (('no folder', [str(folder / 'absent'), 'x', '--', '/usr/bin/true']),
                                ('output exists', [str(folder), 'taken', '--', '/usr/bin/true']),
                                ('no separator', [str(folder), 'x', '/usr/bin/true']),
                                ('a path as the name', [str(folder), '../x', '--', '/usr/bin/true']),
                                ('no command', [str(folder), 'x', '--']),
                                ('a command that does not exist', [str(folder), 'y', '--', '/invented/no-such-program'])):
            with self.subTest(name):
                self.assertEqual(subprocess.run(tool + arguments, capture_output=True, text=True).returncode, 2)
        self.assertEqual((folder / 'taken.out').read_text(), 'earlier')
        self.assertFalse((folder / 'taken.started.json').exists())
        self.assertEqual(json.loads((folder / 'y.started.json').read_text())['not_started'], 'FileNotFoundError')


class TheReceipt(unittest.TestCase):
    def test_a_started_file_that_cannot_be_written_whole_ends_the_command_and_claims_no_more(self):
        spec = importlib.util.spec_from_file_location('detached_under_test', OPERATED / 'detached.py')
        detached = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(detached)
        real_write = os.write
        for name, fault in (('the write fails', OSError(errno.ENOSPC, 'invented')), ('nothing is written', 0)):
            with self.subTest(name):
                folder = Path(tempfile.mkdtemp())
                self.addCleanup(shutil.rmtree, folder, True)

                def write(handle, data):
                    if b'"started_at"' in bytes(data):
                        if isinstance(fault, OSError):
                            raise fault
                        return fault
                    return real_write(handle, data)
                said = io.StringIO()
                with mock.patch.object(detached.os, 'write', write), contextlib.redirect_stderr(said), contextlib.redirect_stdout(io.StringIO()):
                    code = detached.main(['detached.py', str(folder), 'stand-in', '--', '/bin/sleep', '60'])
                report = json.loads(said.getvalue())
                self.assertEqual((code, report['command_gone']), (3, True), report)
                self.assertNotIn('ended', report)  # it does not say that everything was ended
                self.assertIn('stray search', report['next'])
                self.assertIn('could not be written whole', report['error'])
                with self.assertRaises(ProcessLookupError):  # the command it started is gone
                    os.kill(report['pid'], 0)
                written = (folder / 'stand-in.started.json').read_text()
                self.assertEqual(written, '')  # and no partial record is left to be taken for a whole one


class StrayStart(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('stray_under_test', OPERATED / 'stray.py')
        self.stray = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.stray)
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.bundle = self.tmp / 'candidate' / 'Invented Build (development).app'
        for path in ('Contents/MacOS/chirality-app-v4', 'Contents/Resources/codex/bin/codex'):
            (self.bundle / path).parent.mkdir(parents=True, exist_ok=True)
            (self.bundle / path).write_text('invented')
        with open(self.bundle / 'Contents' / 'Info.plist', 'wb') as stream:
            plistlib.dump({'CFBundleExecutable': 'chirality-app-v4'}, stream)
        (self.tmp / 'elsewhere').mkdir()
        (self.tmp / 'elsewhere' / 'chirality-app-v4').write_text('invented')

    def test_a_process_running_the_bundles_executable_is_found_however_its_path_is_spelled(self):
        bundle = str(self.bundle)
        (self.tmp / 'alias').symlink_to(self.bundle.parent)
        executable = bundle + '/Contents/MacOS/chirality-app-v4'
        when = 'Thu Nov 12 22:07:34 2026'
        paths = {501: executable,                                                        # started by the system
                 503: bundle + '/Contents/Resources/codex/bin/codex',                    # another file of the bundle: not its executable
                 504: str(self.tmp / 'alias' / self.bundle.name / 'Contents/MacOS/chirality-app-v4'),  # through a link
                 505: str(self.tmp / 'elsewhere' / 'chirality-app-v4'),                  # the same name, another file
                 506: None,                                                              # gone since the listing
                 507: str(self.tmp / 'removed-since'),                                   # removed between the two questions
                 509: self.stray.NO_PATH}                                                # the system gives no path: removed
        case_ignored = os.path.exists(executable.upper()) and os.path.samefile(executable, executable.upper())
        if case_ignored:
            paths[508] = executable.upper()                                              # another letter case
        lines = [f'  {pid}     1 {when}' for pid in paths] + ['not a process line']
        found, no_path = self.stray.processes(executable, lines, path_of=paths.get)
        self.assertEqual(no_path, [507, 509])
        expected = [501, 504] + ([508] if case_ignored else [])
        self.assertEqual([entry['pid'] for entry in found], expected)
        self.assertEqual((found[0]['parent'], found[0]['started'], found[0]['executable']), (1, when, executable))
        # The executable named through the link finds the same processes.
        again, _ = self.stray.processes(paths[504], lines, path_of=paths.get)
        self.assertEqual([entry['pid'] for entry in again], expected)

    def test_its_exit_status_says_whether_it_looked_and_what_it_found(self):
        argv = ['stray.py', str(self.bundle)]
        executable = str(self.bundle / 'Contents/MacOS/chirality-app-v4')
        with mock.patch.object(self.stray, 'on_macos', return_value=True), mock.patch.object(self.stray, 'listing', return_value=[]), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.stray.main(argv), 0)
        out = io.StringIO()
        with mock.patch.object(self.stray, 'on_macos', return_value=True), contextlib.redirect_stdout(out), \
                mock.patch.object(self.stray, 'listing', return_value=['  601     1 Thu Nov 12 22:07:34 2026']), \
                mock.patch.object(self.stray, 'executable_of', return_value=executable):
            self.assertEqual(self.stray.main(argv), 1)
        self.assertEqual([p['pid'] for p in json.loads(out.getvalue())['remaining_candidate_processes']], [601])
        with mock.patch.object(self.stray, 'on_macos', return_value=True), contextlib.redirect_stderr(io.StringIO()), \
                mock.patch.object(self.stray, 'listing', return_value=['  602     1 Thu Nov 12 22:07:34 2026']), \
                mock.patch.object(self.stray, 'executable_of', side_effect=OSError(13, 'invented')):
            self.assertEqual(self.stray.main(argv), 2)  # a process that could not be asked is not "found none"
        with contextlib.redirect_stderr(io.StringIO()), mock.patch.object(self.stray, 'on_macos', return_value=True):
            self.assertEqual(self.stray.main(['stray.py', str(self.tmp / 'no-such.app')]), 2)  # no bundle to look for
        said = io.StringIO()
        with contextlib.redirect_stderr(said), mock.patch.object(self.stray, 'on_macos', return_value=False), \
                mock.patch.object(self.stray, 'listing', side_effect=AssertionError('looked although not on macOS')):
            self.assertEqual(self.stray.main(argv), 2)  # elsewhere it looks for nothing and says so
        self.assertIn('macOS only; nothing was looked for', said.getvalue())
        tool = [sys.executable, '-B', str(OPERATED / 'stray.py')]
        for arguments in ([], ['relative.app'], ['/invented/folder'], ['/invented/x.app', 'more']):
            with self.subTest(arguments=arguments):
                self.assertEqual(subprocess.run(tool + arguments, capture_output=True, text=True).returncode, 2)


class SessionEnvironment(unittest.TestCase):
    """session_env.py: whether a start by the launch service would be given any of the App's configuration variables."""
    def setUp(self):
        spec = importlib.util.spec_from_file_location('session_env_under_test', OPERATED / 'session_env.py')
        self.env = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.env)
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def domain(self, *entries):
        return 'gui/501 = {\n\ttype = gui\n\tenvironment = {\n' + ''.join(f'\t\t{e}\n' for e in entries) + '\t}\n\tservices = {\n\t}\n}\n'

    def bundle(self, plist):
        bundle = self.tmp / 'Invented.app'
        (bundle / 'Contents').mkdir(parents=True, exist_ok=True)
        with open(bundle / 'Contents' / 'Info.plist', 'wb') as stream:
            plistlib.dump(plist, stream)
        return str(bundle)

    def test_it_asks_for_exactly_the_variables_by_which_the_app_takes_its_configuration_from_the_environment(self):
        source = (APP / 'src-tauri/src/lib.rs').read_text()
        keys = source[source.index('fn explicit_environment_launch'):]
        keys = keys[keys.index('const KEYS'):keys.index('];')]
        self.assertEqual(set(self.env.NAMES), set(re.findall(r'"(CHIRALITY_[A-Z0-9_]+)"', keys)))
        self.assertEqual(len(self.env.NAMES), 10)

    def test_a_variable_present_and_empty_is_present_and_refuses(self):
        names, reason = self.env.session_names(self.domain('SSH_AUTH_SOCK => /invented', 'CHIRALITY_WORKSPACE => '))
        self.assertEqual((names, reason), ({'SSH_AUTH_SOCK', 'CHIRALITY_WORKSPACE'}, None))
        result = self.env.states(names, None, set(), None)
        self.assertEqual(result['CHIRALITY_WORKSPACE'], 'present')
        self.assertEqual({v for k, v in result.items() if k != 'CHIRALITY_WORKSPACE'}, {'absent'})
        self.assertEqual(self.env.status(result), 1)

    def test_none_present_is_absent_for_all_and_no_value_is_kept(self):
        names, _ = self.env.session_names(self.domain('SSH_AUTH_SOCK => /invented/secret-value'))
        result = self.env.states(names, None, set(), None)
        self.assertEqual((set(result.values()), self.env.status(result)), ({'absent'}, 0))
        self.assertNotIn('secret-value', json.dumps(result))

    def test_the_bundles_own_environment_counts(self):
        result = self.env.states(set(), None, self.env.bundle_names(self.bundle({'LSEnvironment': {'CHIRALITY_CODEX_HOME': ''}})), None)
        self.assertEqual((result['CHIRALITY_CODEX_HOME'], self.env.status(result)), ('present', 1))

    def test_what_cannot_be_read_is_could_not_be_established_never_absent(self):
        for name, text in (('no environment block', 'gui/501 = {\n\ttype = gui\n}\n'),
                           ('two blocks', self.domain('A => 1') + self.domain('B => 2')),
                           ('a line it cannot read', self.domain('SSH_AUTH_SOCK => /x', 'something else')),
                           ('a block that does not end', 'gui/501 = {\n\tenvironment = {\n\t\tA => 1\n')):
            with self.subTest(name):
                names, reason = self.env.session_names(text)
                self.assertIsNone(names)
                result = self.env.states(names, reason, set(), None)
                self.assertTrue(all(v.startswith('could not be established: ') for v in result.values()), result)
                self.assertEqual(self.env.status(result), 2)
        # One present is said as present even when the rest could not be established.
        self.assertEqual(self.env.status(self.env.states({'CHIRALITY_WORKSPACE'}, None, None, 'unreadable')), 1)

    def test_elsewhere_than_macos_it_establishes_nothing_and_says_so(self):
        out = io.StringIO()
        with mock.patch.object(self.env, 'on_macos', return_value=False), contextlib.redirect_stdout(out), \
                mock.patch.object(self.env.subprocess, 'run', side_effect=AssertionError('asked although not on macOS')):
            self.assertEqual(self.env.main(['session_env.py', self.bundle({})]), 2)
        self.assertEqual(set(json.loads(out.getvalue()).values()), {'could not be established: this is asked on macOS only'})


class TheScenarioFile(unittest.TestCase):
    def setUp(self):
        self.scenario = json.loads(SCENARIO.read_text())

    def test_every_outcome_names_steps_that_exist_and_have_expectations(self):
        steps = {step['id']: step for step in self.scenario['steps']}
        self.assertEqual(set(self.scenario['outcomes']), OUTCOMES)
        for name, ids in self.scenario['outcomes'].items():
            for step in ids:
                self.assertTrue(steps[step]['expect'], (name, step))

    def test_no_step_types_chooses_a_file_or_clicks_a_confirming_control(self):
        for step in self.scenario['steps']:
            self.assertIn(step['act'], ('view', 'click'))
            if step['act'] == 'click':
                label = step['control']['label']
                self.assertFalse(label.endswith(('…', '...')), label)
                self.assertNotIn(label, self.scenario['never_clicked'])
                self.assertIn(step['control']['kind'], ('button', 'summary', 'radio'))

    def test_the_recorded_views_name_no_account_and_no_real_build(self):
        text = VIEWS.read_text()
        self.assertNotIn('/Users/', text)
        self.assertEqual(json.loads(text)['app'], 'dev.chirality.app-v4.candidate.invented')


if __name__ == '__main__':
    unittest.main()
