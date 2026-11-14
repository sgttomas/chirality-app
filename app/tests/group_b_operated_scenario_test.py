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
from types import SimpleNamespace
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
const walkModule = await import(process.argv[1]);
// A scenario that names no listed states (the first-use scenario, kept for the hosted driver) is given, for these
// tests of the walk's mechanics, the views it is fed as its states, read when the walk starts.
const listAll = () => {
  if (scenario.states) return;
  scenario.states = {};
  scenario.steps.forEach((step, n) => {
    if (['type', 'click', 'confirm_sheet'].includes(step.act)) {
      step.from_state = 'V' + (n - 1);
      scenario.states[step.from_state] = String(texts[Math.max(n - 1, 0)] ?? '').split('\\n');
    }
  });
};
const walk = { ...walkModule, run: options => { listAll(); return walkModule.run(options); } };
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
    def views_file(self, views=None):
        folder = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, folder, True)
        path = folder / 'views.json'
        path.write_text(json.dumps(views or setup_views()))
        return path

    def test_the_setup_scenario_replays_against_its_own_listed_states(self):
        code, report, said = replay(SETUP, self.views_file())
        self.assertEqual((code, report['verdict'], report['stopped']), (0, 'pass', None), said)
        self.assertEqual([step['id'] for step in report['steps']], ['S1', 'S2', 'S3', 'S4', 'S5'])
        self.assertEqual([call['call'] for call in report['calls'] if call['call'] != 'get_app_state'],
                         ['set_value', 'click', 'click', 'click', 'click'])
        self.assertEqual({call['app'] for call in report['calls']}, {'dev.chirality.app-v4.candidate.invented'})

    def test_a_scenario_that_acts_and_names_no_listed_state_is_refused_before_any_call(self):
        code, report, said = replay(SCENARIO, VIEWS)  # the first-use scenario, kept for the hosted driver
        self.assertEqual((code, report['verdict'], report['calls']), (2, 'inconclusive', []), said)
        self.assertIn('names no listed state it acts from; the walk acts only in a listed state', report['stopped'])

    def test_the_whole_result_arrives_through_a_pipe(self):
        views = setup_views()
        # The page after the press, which nothing acts from, given a long text so the result outgrows a pipe.
        views['views'][5]['text'] = views['views'][5]['text'].replace(f'\t\t\t\t6 text Project: {PROJECT}',
                                                                      f'\t\t\t\t6 text Project: {PROJECT}\n\t\t\t\t7 text ' + 'invented words ' * 5000)
        done = subprocess.run([NODE, str(REPLAY), str(SETUP), str(self.views_file(views))], capture_output=True, text=True)
        self.assertGreater(len(done.stdout), 65536)  # longer than a pipe holds at once
        self.assertEqual(json.loads(done.stdout)['verdict'], 'pass')

    def test_a_wrong_state_file_that_does_not_match_the_views_is_an_error_not_a_pass(self):
        bad = FIXTURES.parent / 'does-not-apply.json'
        bad.write_text(json.dumps({'replace': [{'view': 0, 'from': 'button Not On The Page', 'to': 'x'}]}))
        self.addCleanup(bad.unlink)
        code, report, said = replay(SETUP, self.views_file(), bad)
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
        self.assertTrue(children.startswith('not known'), children)

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
        self.assertIn('stopped at S2: the view came back as differences although the whole window was asked for;', stopped)
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
                asked = ('it was the first view of this build in the walk, asked with the application alone' if name == 'the first'
                         else 'the whole window was asked for')
                self.assertIn(f'although {asked};', stopped)  # what was asked, said truly for each view

    def test_the_first_view_asks_with_the_application_alone_and_every_later_view_for_the_whole_window(self):
        result = harness('''const asked = [];
          const service2 = { get_app_state: async options => { asked.push(options); return { app: viewOf.app, text: nextView() }; },
                             click: async () => {} };
          const r = await walk.run({ ...base, sky: service2 });
          return [r.verdict, asked, r.calls.filter(c => c.call === 'get_app_state').map(c => c.disableDiff ?? null)];''')
        verdict, asked, recorded = result['out']
        self.assertEqual(verdict, 'pass')
        app = 'dev.chirality.app-v4.candidate.invented'
        self.assertEqual(asked[0], {'app': app})  # no disableDiff key at all
        self.assertEqual(asked[1:], [{'app': app, 'disableDiff': True}] * (len(asked) - 1))
        self.assertEqual(len(asked), 10)
        self.assertEqual(recorded, [None] + [True] * 9)  # the result says how each view was asked for

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
        result = harness(f'scenario.starts_no_process = false; const r = await walk.run({{ ...base, readWatch: watched({{ children: {child} }}) }}); return [r.verdict, r.steps.map(s => s.child_processes)];')
        self.assertEqual(result['out'][0], 'pass')  # a scenario that may start a process is not stopped by one
        self.assertEqual(set(result['out'][1]), {1})  # and the child it allowed is recorded, not reported as none

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

    def test_a_failed_view_keeps_its_message_and_each_cause_whole_and_nothing_else(self):
        # As the supplier's client fails a cold start: its message, and the cause it attaches, which carries its own.
        result = harness('''
          const inner = new Error('Sky Computer Use native pipe connection timed out');
          const middle = new Error('the last attempt', { cause: inner });
          const outer = new Error('Sky Computer Use native pipe startup failed', { cause: middle });
          outer.secret = 'not kept'; inner.cause = middle;  // a property and a loop, neither of which may be kept or followed
          const failing = { get_app_state: async () => { throw outer; }, click: async () => {} };
          const r = await walk.run({ ...base, sky: failing });
          return [r.verdict, r.view_error, r.stopped, walk.summary(r), JSON.stringify(r).includes('not kept'), JSON.stringify(r).includes('    at ')];''')
        verdict, failed, stopped, summary, kept_property, kept_stack = result['out']
        self.assertEqual(verdict, 'inconclusive')
        self.assertEqual(failed, {'where': 'the first view before any click', 'message': 'Sky Computer Use native pipe startup failed',
                                  'causes': ['the last attempt', 'Sky Computer Use native pipe connection timed out']})
        self.assertIn('the view failed (Sky Computer Use native pipe startup failed)', stopped)
        self.assertIn('    caused by: the last attempt\n    caused by: Sky Computer Use native pipe connection timed out', summary)
        self.assertEqual((kept_property, kept_stack), (False, False))
        # A failure at a later step is kept the same way, and an error that is not an Error is kept as its text.
        result = harness('''let calls = 0;
          const failing = { get_app_state: async () => { calls += 1; if (calls > 3) throw 'plain text'; return { app: viewOf.app, text: nextView() }; }, click: async () => {} };
          const r = await walk.run({ ...base, sky: failing });
          return [r.view_error, r.steps.at(-1).error];''')
        self.assertEqual(result['out'][0], {'where': 'S2', 'message': 'plain text', 'causes': []})
        self.assertEqual(result['out'][1], 'plain text')
        # A cause with no prototype, a cause whose getter throws, and a message that is not text: the walk stops
        # where it would have, with a result, and nothing of the error is converted to text by its own code.
        result = harness('''
          const bare = new Error('top', { cause: Object.create(null) });
          const trap = new Error('top'); Object.defineProperty(trap, 'cause', { get() { throw new Error('getter'); } });
          const odd = new Error('top', { cause: { message: { toString() { return 'converted by its own code'; } } } });
          const out = [];
          for (const thrown of [bare, trap, odd]) {
            const failing = { get_app_state: async () => { throw thrown; }, click: async () => {} };
            const r = await walk.run({ ...base, sky: failing });
            out.push([r.verdict, r.stopped.startsWith('stopped at the first view before any click: the view failed (top)'), r.view_error.causes]);
          }
          return out;''')
        self.assertEqual(result['out'], [
            ['inconclusive', True, ['(a thrown object with no message text)']],
            ['inconclusive', True, ['(a cause that could not be read)']],
            ['inconclusive', True, ['(a thrown object with no message text)']]])
        # A failure whose reading breaks the collector itself (a cause getter that replaces Array.prototype.push, as
        # code in the same runtime can): the walk still returns its result, with the failure said to be unreadable.
        result = harness('''
          const push = Array.prototype.push;
          const thrown = { message: 'top', get cause() { Array.prototype.push = () => { throw new Error('broken'); }; return { message: 'inner' }; } };
          const failing = { get_app_state: async () => { throw thrown; }, click: async () => {} };
          let r;
          try { r = await walk.run({ ...base, sky: failing }); } finally { Array.prototype.push = push; }
          return [r.verdict, r.view_error];''')
        self.assertEqual(result['out'], ['inconclusive', {'where': 'the first view before any click',
                                                          'message': '(the failure could not be read)', 'causes': []}])

    def test_a_failed_click_stops_the_walk_with_its_result_and_its_message_and_causes_whole(self):
        # A click that throws: the walk does not reject; it keeps the failure as a view's is kept, calls nothing
        # further, and is inconclusive, since a call that throws has not been shown to have had no effect.
        result = harness('''
          const inner = new Error('the element is gone');
          const outer = new Error('Sky Computer Use click failed', { cause: inner });
          let clicks = 0;
          const failing = { get_app_state: async () => ({ app: viewOf.app, text: nextView() }),
                            click: async () => { clicks += 1; throw outer; } };
          const r = await walk.run({ ...base, sky: failing });
          const after = r.calls.findIndex(c => c.call === 'click');
          return [r.verdict, r.click_error, r.stopped, walk.summary(r), clicks, r.calls.length - after - 1, r.steps.at(-1).error];''')
        verdict, failed, stopped, summary, clicks, calls_after, step_error = result['out']
        self.assertEqual(verdict, 'inconclusive')
        self.assertEqual(failed, {'where': 'S2', 'message': 'Sky Computer Use click failed', 'causes': ['the element is gone']})
        self.assertEqual(stopped, 'stopped at S2: the click failed (Sky Computer Use click failed)')
        self.assertIn('    caused by: the element is gone', summary)
        self.assertEqual((clicks, calls_after, step_error), (1, 0, 'Sky Computer Use click failed'))

    def test_a_view_returned_as_differences_is_applied_to_the_view_before_it(self):
        result = harness('''
          const before = walk.parseView('Window: "Chirality", App: Chirality App v4 (development invented).\\n0 standard window Chirality\\n\\t1 button (disabled) Review setup\\n\\t2 summary Details, Value: off\\n\\t\\t3 text Details\\n\\t4 close button');
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
                 509: self.stray.NO_PATH}                                                # the system gives no path: removed
        case_ignored = os.path.exists(executable.upper()) and os.path.samefile(executable, executable.upper())
        if case_ignored:
            paths[508] = executable.upper()                                              # another letter case
        lines = [f'  {pid}     1 {when}' for pid in paths] + ['not a process line']
        found, no_path = self.stray.processes(executable, lines, path_of=paths.get)
        self.assertEqual(no_path, [509])
        expected = [501, 504] + ([508] if case_ignored else [])
        self.assertEqual([entry['pid'] for entry in found], expected)
        self.assertEqual((found[0]['parent'], found[0]['started'], found[0]['executable']), (1, when, executable))
        # The executable named through the link finds the same processes.
        again, _ = self.stray.processes(paths[504], lines, path_of=paths.get)
        self.assertEqual([entry['pid'] for entry in again], expected)

    def test_what_it_cannot_tie_to_a_file_is_a_search_not_made_never_none_found(self):
        executable = self.bundle / 'Contents/MacOS/chirality-app-v4'
        line = ['  701     1 Thu Nov 12 22:07:34 2026']
        # A path given for the process that is gone when examined (a link removed in between): not "removed".
        with self.assertRaisesRegex(OSError, 'gone when it was examined'):
            self.stray.processes(str(executable), line, path_of=lambda pid: str(self.tmp / 'gone-since'))
        # The bundle's executable with a second name: a process could be running it under that name.
        os.link(executable, self.tmp / 'second-name')
        with self.assertRaisesRegex(OSError, '2 names, not one'):
            self.stray.processes(str(executable), line, path_of=lambda pid: self.stray.NO_PATH)
        os.unlink(self.tmp / 'second-name')
        # The bundle's executable replaced during the search, by a file of the same size. A file system may give
        # the new file the inode number of the one removed (Linux did, on the hosted run), so device and inode
        # alone would not see it; its times do. The original's times are set back first, so that this holds
        # whatever the file system's time resolution.
        os.utime(executable, ns=(1_577_836_800_000_000_000, 1_577_836_800_000_000_000))
        def replaced(pid):
            executable.unlink()
            executable.write_text('INVENTED')  # the same size as the original
            return self.stray.NO_PATH
        with self.assertRaisesRegex(OSError, 'changed during the search'):
            self.stray.processes(str(executable), line, path_of=replaced)

    def test_a_file_with_the_same_device_inode_links_size_and_modification_time_still_differs_by_its_change_time(self):
        # What a replacement given a reused inode number, the same size and the same modification time leaves: the
        # change time, which a write sets and nothing a caller does can set back.
        base = dict(st_dev=1, st_ino=42, st_nlink=1, st_size=8, st_mtime_ns=10, st_ctime_ns=10)
        before, after = SimpleNamespace(**base), SimpleNamespace(**{**base, 'st_ctime_ns': 11})
        self.assertNotEqual(self.stray.fingerprint(before), self.stray.fingerprint(after))
        self.assertEqual(self.stray.fingerprint(before), self.stray.fingerprint(SimpleNamespace(**base)))

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


class ScreenLock(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('screen_lock', OPERATED / 'screen_lock.py')
        self.lock = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.lock)

    def test_the_session_key_says_locked_or_not_and_anything_else_is_not_established(self):
        lock, KEY, CONSOLE, OTHER = self.lock.locked_from, self.lock.KEY, self.lock.CONSOLE, self.lock.OTHER
        # As read on this Mac: locked, the key present at 1; unlocked, the key absent and the session on the console.
        self.assertIs(lock({KEY: 1, CONSOLE: 1}), True)
        self.assertIs(lock({KEY: None, CONSOLE: 1}), False)
        self.assertIs(lock({KEY: 0, CONSOLE: 1}), False)
        self.assertIs(lock({KEY: 1, CONSOLE: None}), True)  # locked whatever the console says
        self.assertIs(lock({KEY: -1, CONSOLE: 1}), True)  # a number that is not 0
        self.assertIsNone(lock({KEY: None, CONSOLE: 0}))  # not on the console
        self.assertIsNone(lock({KEY: 0, CONSOLE: None}))  # no console key
        self.assertIsNone(lock({KEY: None, CONSOLE: 2}))
        self.assertIsNone(lock({KEY: None, CONSOLE: None}))
        self.assertIsNone(lock({}))
        # A value that is neither a number nor a boolean is not established, whatever the other key says.
        self.assertIsNone(lock({KEY: OTHER, CONSOLE: 1}))
        self.assertIsNone(lock({KEY: None, CONSOLE: OTHER}))
        self.assertIsNone(lock({KEY: 0, CONSOLE: OTHER}))

    def test_it_reads_the_session_dictionary_by_lookup_and_parses_no_text(self):
        source = (OPERATED / 'screen_lock.py').read_text()
        self.assertIn('CFDictionaryGetValue', source)
        self.assertNotIn('CFCopyDescription', source)
        self.assertNotIn('import re', source)
        if sys.platform == 'darwin':
            values = self.lock.session_values()
            self.assertEqual(set(values), {self.lock.KEY, self.lock.CONSOLE})
            self.assertTrue(all(value is None or value == self.lock.OTHER or isinstance(value, int) for value in values.values()))

    @unittest.skipUnless(sys.platform == 'darwin', 'CoreFoundation')
    def test_the_lookup_reads_what_a_real_session_dictionary_holds(self):
        import ctypes
        import ctypes.util
        from types import SimpleNamespace
        core = ctypes.CDLL(ctypes.util.find_library('CoreFoundation'))
        core.CFStringCreateWithCString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32]
        core.CFStringCreateWithCString.restype = ctypes.c_void_p
        core.CFNumberCreate.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
        core.CFNumberCreate.restype = ctypes.c_void_p
        core.CFDictionaryCreate.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_long, ctypes.c_void_p, ctypes.c_void_p]
        core.CFDictionaryCreate.restype = ctypes.c_void_p
        core.CFRetain.argtypes = [ctypes.c_void_p]
        core.CFRetain.restype = ctypes.c_void_p
        core.CFRelease.argtypes = [ctypes.c_void_p]
        keys_cb = ctypes.addressof(ctypes.c_ubyte.in_dll(core, 'kCFTypeDictionaryKeyCallBacks'))
        values_cb = ctypes.addressof(ctypes.c_ubyte.in_dll(core, 'kCFTypeDictionaryValueCallBacks'))

        def made(value):
            if isinstance(value, str):
                return core.CFStringCreateWithCString(None, value.encode(), 0x08000100)
            if isinstance(value, bool):
                return core.CFRetain(ctypes.c_void_p.in_dll(core, 'kCFBooleanTrue' if value else 'kCFBooleanFalse').value)
            number = ctypes.c_double(value) if isinstance(value, float) else ctypes.c_int64(value)
            return core.CFNumberCreate(None, 6 if isinstance(value, float) else 4, ctypes.byref(number))

        def read(values):
            keys = [core.CFStringCreateWithCString(None, name.encode(), 0x08000100) for name in values]
            objects = [made(value) for value in values.values()]
            dictionary = core.CFDictionaryCreate(None, (ctypes.c_void_p * len(keys))(*keys), (ctypes.c_void_p * len(objects))(*objects),
                                                 len(keys), keys_cb, values_cb)
            graphics = SimpleNamespace(CGSessionCopyCurrentDictionary=lambda: core.CFRetain(dictionary))
            try:
                with mock.patch.object(self.lock.ctypes, 'CDLL', side_effect=lambda name: core if 'CoreFoundation' in name else graphics), \
                        contextlib.redirect_stdout(io.StringIO()):
                    return self.lock.session_values(), self.lock.main()
            finally:
                core.CFRelease(dictionary)
                for made_object in keys + objects:
                    core.CFRelease(made_object)

        KEY, CONSOLE, OTHER = self.lock.KEY, self.lock.CONSOLE, self.lock.OTHER
        self.assertEqual(read({KEY: 1, CONSOLE: 1}), ({KEY: 1, CONSOLE: 1}, 3))
        self.assertEqual(read({KEY: True, CONSOLE: True}), ({KEY: 1, CONSOLE: 1}, 3))
        self.assertEqual(read({CONSOLE: 1}), ({KEY: None, CONSOLE: 1}, 0))
        self.assertEqual(read({KEY: False, CONSOLE: 1}), ({KEY: 0, CONSOLE: 1}, 0))
        self.assertEqual(read({KEY: '0', CONSOLE: 1}), ({KEY: OTHER, CONSOLE: 1}, 2))
        self.assertEqual(read({KEY: 0.5, CONSOLE: 1}), ({KEY: OTHER, CONSOLE: 1}, 2))
        self.assertEqual(read({'Other' + KEY: 1, CONSOLE: 1}), ({KEY: None, CONSOLE: 1}, 0))
        self.assertEqual(read({KEY: 1}), ({KEY: 1, CONSOLE: None}, 3))
        self.assertEqual(read({}), ({KEY: None, CONSOLE: None}, 2))

    def test_its_exit_status_refuses_a_walk_unless_the_screen_is_not_locked(self):
        KEY, CONSOLE = self.lock.KEY, self.lock.CONSOLE
        for values, code in (({KEY: None, CONSOLE: 1}, 0), ({KEY: 1, CONSOLE: 1}, 3), ({KEY: None, CONSOLE: None}, 2),
                             ({KEY: self.lock.OTHER, CONSOLE: 1}, 2)):
            with self.subTest(values), mock.patch.object(self.lock, 'session_values', return_value=values), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(self.lock.main(), code)
        with mock.patch.object(self.lock, 'session_values', side_effect=OSError('not macOS')), \
                contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(self.lock.main(), 2)
        self.assertIn('could not be established (not macOS)', out.getvalue())


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
        # The list by which the App selects the environment route (lib.rs ENVIRONMENT_KEYS, read by
        # environment_selected). It names CHIRALITY_APP_DATA by its constant, APP_DATA_ENV, resolved here from that
        # constant's own line.
        source = (APP / 'src-tauri/src/lib.rs').read_text()
        list_at = re.search(r'const ENVIRONMENT_KEYS: &\[&str\] = &\[(.*?)\];', source, re.S)
        self.assertIsNotNone(list_at, 'lib.rs: const ENVIRONMENT_KEYS not found')
        constant = re.search(r'const APP_DATA_ENV: &str = "(CHIRALITY_[A-Z0-9_]+)";', source)
        self.assertIsNotNone(constant, 'lib.rs: const APP_DATA_ENV not found')
        entries = [entry.strip() for entry in list_at.group(1).split(',') if entry.strip()]
        names = set()
        for entry in entries:
            literal = re.fullmatch(r'"(CHIRALITY_[A-Z0-9_]+)"', entry)
            if literal:
                names.add(literal.group(1))
            elif entry == 'APP_DATA_ENV':
                names.add(constant.group(1))
            else:
                self.fail(f'lib.rs: ENVIRONMENT_KEYS holds an entry this test cannot resolve: {entry}')
        self.assertTrue(names, 'lib.rs: ENVIRONMENT_KEYS names nothing')
        self.assertIn('CHIRALITY_APP_DATA', names)
        self.assertEqual(set(self.env.NAMES), names)
        self.assertEqual(len(self.env.NAMES), 11)

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


SETUP = OPERATED / 'signed-out-setup.scenario.json'
RELAUNCH = OPERATED / 'signed-out-relaunch.scenario.json'
PROJECT = '/invented/homes/launch-invented/project'
DATA = '/invented/homes/launch-invented/home/Library/Application Support/dev.chirality.app-v4.candidate.invented'
SETTINGS = DATA + '/shared-settings/settings-00000000-0000-0000-0000-000000000000'
ACCOUNT = DATA + '/account-homes/account-00000000-0000-0000-0000-000000000000'
REQUEST = DATA + '/desktop-startup/request.json'
STATEMENT = '\n'.join(json.loads(SETUP.read_text())['sheets'][0]['statement']).format_map(
    {'settings': SETTINGS, 'account': ACCOUNT, 'project': PROJECT, 'request': REQUEST}) if SETUP.exists() else ''
SETUP_HARNESS = HARNESS.replace("if (name === 'click') return async () => {};",
                                "if (name === 'click' || name === 'set_value') return async () => {};").replace(
    "readWatch: watched(), sleep: async () => {} };", "readWatch: watched(), sleep: async () => {}, project: recorded.project };")


def setup_state(name):
    """A listed state of the setup scenario, filled with the invented values."""
    text = '\n'.join(json.loads(SETUP.read_text())['states'][name])
    for placeholder, value in {'{app_name}': 'Chirality App v4 (development invented)', '{project}': PROJECT,
                               '{settings}': SETTINGS, '{account}': ACCOUNT, '{request}': REQUEST, '{~number}': '0'}.items():
        text = text.replace(placeholder, value)
    return text


def setup_views(sheet=None, after=None):
    """Invented views for the signed-out setup walk: the scenario's own listed states filled with invented values, the
    recorded sheet, and the page after it. sheet: the whole view of the sheet; by default the recorded one."""
    recorded = json.loads(VIEWS.read_text())
    with_sheet = SHEET_ON_ITS_OWN if sheet is None else sheet
    done = '\n'.join(['Window: "Chirality", App: Chirality App v4 (development invented).',
                      '0 standard window Chirality, Secondary Actions: Raise', '\t1 scroll area',
                      '\t\t2 HTML content Description: Chirality, URL: tauri://localhost', "\t\t\t3 container You're set up",
                      "\t\t\t\t4 heading You're set up, Value: 1", "\t\t\t\t\t5 text You're set up", f'\t\t\t\t6 text Project: {PROJECT}',
                      '\t41 close button',
                      '\t42 full screen button Help: this button also has an action to zoom the window, Secondary Actions: zoom the window',
                      '\t43 minimize button', '\t44 text Chirality', '45 menu bar'])
    return {'app': recorded['app'], 'home': recorded['home'], 'bundle': recorded['bundle'], 'project': PROJECT,
            'views': [{'text': text} for text in (setup_state('S1'), setup_state('S2'), setup_state('S3'), setup_state('S4'),
                                                  with_sheet, after or done)]}


SHEET_ON_ITS_OWN = (APP / 'tests/group_b_operated_fixtures/signed-out-setup/sheet-on-its-own.txt').read_text()


def setup_walk(case, views=None, scenario=SETUP):
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / 'views.json'
        path.write_text(json.dumps(views or setup_views()))
        done = subprocess.run([NODE, '--input-type=module', '-e', SETUP_HARNESS.replace('CASE', case), WALK.as_uri(), str(scenario),
                               str(path)], capture_output=True, text=True)
    if done.returncode != 0:
        raise AssertionError(done.stderr)
    return json.loads(done.stdout)


RESULT = 'const r = await walk.run(OPTIONS); return [r.verdict, r.stopped, r.calls.map(c => c.call + (c.element_index ?? "") + (c.value ? "=" + c.value : ""))];'


class TheSheetAndTheTypedPath(unittest.TestCase):
    def test_the_walk_types_the_project_once_checks_the_sheet_whole_and_presses_it_once(self):
        result = setup_walk(RESULT.replace('OPTIONS', 'base'))
        verdict, stopped, calls = result['out']
        self.assertEqual((verdict, stopped), ('pass', None))
        self.assertEqual(set(result['touched']), {'get_app_state', 'click', 'set_value'})
        self.assertEqual([c for c in calls if not c.startswith('get_app_state')],
                         [f'set_value16={PROJECT}', 'click37', 'click57', 'click69', 'click4'])

    def test_a_dialog_anywhere_below_the_window_stops_an_ordinary_step(self):
        result = harness("texts[2] = texts[2].replace('\\t\\t2 HTML content', '\\t\\t\\t\\t950 sheet Confirm\\n\\t\\t2 HTML content'); "
                         'const r = await walk.run(base); return [r.verdict, r.stopped];')
        self.assertEqual(result['out'][0], 'inconclusive')
        self.assertIn('the window holds something that is not the page (sheet Confirm)', result['out'][1])

    def test_only_the_empty_field_the_page_labels_is_typed_into(self):
        field = '16 text field (settable) Project folder, Placeholder: /full/path/to/your/project'
        cases = {'a label that only begins the same way': field.replace('Project folder,', 'Project folder, another purpose,'),
                 'a label ending in words shaped like a value': field.replace('Project folder,', 'Project folder, Value: another purpose,'),
                 'a label ending in words shaped like a placeholder':
                     field.replace('Project folder,', 'Project folder, Placeholder: another purpose,'),
                 'a field already holding a value': field.replace('Project folder,', 'Project folder, Value: /elsewhere,'),
                 'another placeholder': field.replace('/full/path/to/your/project', '/another/path')}
        for name, line in cases.items():
            with self.subTest(name):
                views = setup_views()
                views['views'][0]['text'] = views['views'][0]['text'].replace(field, line)
                verdict, stopped, calls = setup_walk(RESULT.replace('OPTIONS', 'base'), views)['out']
                self.assertEqual(verdict, 'inconclusive')
                self.assertIn('stopped at S2: the view is not the listed state S1', stopped)
                self.assertIn('nothing was typed', stopped)
                self.assertFalse([c for c in calls if c.startswith('set_value')])
        views = setup_views()
        views['views'][0]['text'] = views['views'][0]['text'].replace('15 text Project folder\n', '15 text Your folder\n')
        verdict, stopped, calls = setup_walk(RESULT.replace('OPTIONS', 'base'), views)['out']
        self.assertIn('the view is not the listed state S1', stopped)
        self.assertFalse([c for c in calls if c.startswith('set_value')])

    def test_a_link_with_other_words_after_its_label_is_not_it(self):
        elements = [{'index': 1, 'depth': 0, 'content': 'link Settings & tools, Sign in'},
                    {'index': 2, 'depth': 0, 'content': 'link Settings & tools, another purpose'}]
        result = harness(f"return walk.select({json.dumps(elements)}, {{ kind: 'link', label: 'Settings & tools' }}).length;")
        self.assertEqual(result['out'], 0)

    def test_an_alert_holding_a_control_is_not_page(self):
        views = setup_views()
        views['views'][0]['text'] = views['views'][0]['text'].replace(
            '\t\t\t\t\t\t\t15 text Project folder\n\t\t\t\t\t\t\t16 text field',
            '\t\t\t\t\t\t990 alert External prompt\n\t\t\t\t\t\t\t15 text Project folder\n\t\t\t\t\t\t\t16 text field')
        self.assertIn('990 alert External prompt', views['views'][0]['text'])
        verdict, stopped, calls = setup_walk(RESULT.replace('OPTIONS', 'base'), views)['out']
        self.assertEqual(verdict, 'inconclusive')
        self.assertIn('alert External prompt', stopped)
        self.assertFalse([c for c in calls if c.startswith('set_value')])

    def test_a_field_alone_inside_a_page_alert_is_not_typed_into(self):
        views = setup_views()
        views['views'][0]['text'] = views['views'][0]['text'].replace(
            '\t\t\t\t\t\t\t15 text Project folder\n\t\t\t\t\t\t\t16 text field (settable) Project folder, Placeholder: /full/path/to/your/project\n',
            '\t\t\t\t\t\t990 alert External prompt\n\t\t\t\t\t\t\t15 text Project folder\n\t\t\t\t\t\t\t16 text field (settable) Project folder, Placeholder: /full/path/to/your/project\n'
            '\t\t\t\t\t\t991 container\n')
        self.assertIn('990 alert External prompt', views['views'][0]['text'])
        verdict, stopped, calls = setup_walk(RESULT.replace('OPTIONS', 'base'), views)['out']
        self.assertEqual(verdict, 'inconclusive')
        self.assertIn('alert External prompt', stopped)
        self.assertFalse([c for c in calls if c.startswith('set_value')])

    def test_an_alert_in_the_pages_own_content_is_page_not_prompt(self):
        result = harness("texts[2] = texts[2].replace('\\t\\t\\t3 container Welcome', '\\t\\t\\t3 container Welcome\\n\\t\\t\\t\\t990 alert Why Codex was not started'); "
                         'return (await walk.run(base)).verdict;')
        self.assertEqual(result['out'], 'pass')
        result = harness("texts[2] = texts[2].replace('\\t41 close button', '\\t989 scroll area\\n\\t\\t990 alert Allow?\\n\\t41 close button'); "
                         'const r = await walk.run(base); return [r.verdict, r.stopped];')
        self.assertEqual(result['out'][0], 'inconclusive')
        self.assertIn('alert Allow?', result['out'][1])

    def test_the_project_is_exactly_the_launch_folders_own(self):
        for project in ('/invented/homes/launch-invented/project/../../outside', '/invented/homes/launch-invented/home',
                        '/invented/homes/launch-invented/project/', '/invented/homes/launch-invented/projects'):
            with self.subTest(project):
                verdict, stopped, calls = setup_walk(f"base.project = {json.dumps(project)}; " + RESULT.replace('OPTIONS', 'base'))['out']
                self.assertEqual((verdict, calls), ('inconclusive', []), stopped)
        verdict, stopped, calls = setup_walk("base.home = '/invented/homes/x/../launch-invented/home'; base.project = '/invented/homes/x/../launch-invented/project'; "
                                             + RESULT.replace('OPTIONS', 'base'))['out']
        self.assertEqual((verdict, calls), ('inconclusive', []), stopped)

    def test_the_build_gone_while_the_sheet_was_viewed_means_no_press(self):
        case = ("let gone = false; const sheetView = texts[4]; Object.defineProperty(texts, 4, { get() { gone = true; return sheetView; } }); "
                "base.readWatch = () => (gone ? null : watched()()); " + RESULT.replace('OPTIONS', 'base'))
        verdict, stopped, calls = setup_walk(case)['out']
        self.assertEqual(verdict, 'inconclusive')
        self.assertIn('before the press', stopped)
        self.assertNotIn('click4', calls)

    def test_a_view_steps_wait_is_waited(self):
        result = setup_walk("const slept = []; base.sleep = async ms => { slept.push(ms); }; scenario.steps[0].wait_ms = 15000; "
                            "await walk.run(base); return slept;")
        self.assertEqual(result['out'][0], 15000)

    def test_the_recorded_view_is_the_scenarios_template_filled_with_the_invented_names(self):
        sheet = json.loads(SETUP.read_text())['sheets'][0]
        statement = STATEMENT
        filled = '\n'.join(sheet['view']).replace('{app_name}', 'Chirality App v4 (development invented)').replace(
            '{title}', sheet['title']).replace('{statement}', statement)
        self.assertEqual(filled, SHEET_ON_ITS_OWN)

    def test_the_view_numbered_otherwise_is_the_same_view_and_the_press_follows_its_numbers(self):
        renumbered = re.sub(r'^(\t*)(\d+) ', lambda m: f'{m.group(1)}{int(m.group(2)) + 100} ', SHEET_ON_ITS_OWN, flags=re.M).replace(
            'The focused UI element is 0 sheet', 'The focused UI element is 100 sheet')
        verdict, stopped, calls = setup_walk(RESULT.replace('OPTIONS', 'base'), setup_views(sheet=renumbered))['out']
        self.assertEqual((verdict, stopped, calls[-2]), ('pass', None, 'click104'))

    def test_the_sheet_on_its_own_differing_in_any_way_is_not_pressed(self):
        own = SHEET_ON_ITS_OWN
        cases = {
            'a window beside it at the top': own.replace('\n5 menu bar', '\n90 standard window Chirality, Secondary Actions: Raise\n5 menu bar'),
            'a second sheet at the top': own.replace('\n5 menu bar', '\n91 sheet Description: alert\n\t92 button OK, ID: action-button-1\n5 menu bar'),
            'a dialog inside the sheet': own.replace('\t2 button', '\t93 dialog Another question\n\t2 button'),
            'something unnamed at the top': own.replace('\n5 menu bar', '\n94 group\n5 menu bar'),
            'another statement': own.replace('Read, import or change no other', 'Read, import and change any'),
            'another title': own.replace('Desktop setup — next launch only Create', 'Desktop setup Create'),
            'the statement as its own text, without the title': own.replace('\t1 text Desktop setup — next launch only ', '\t1 text '),
            'the title and the statement as two texts': own.replace('\t1 text Desktop setup — next launch only Create', '\t1 text Desktop setup — next launch only\n\t95 text Create'),
            'a second text in the sheet': own.replace('\t2 button', '\t95 text Also allow everything.\n\t2 button'),
            'a button without the identifier suffix': own.replace('Leave setup unchanged, ID: action-button-1', 'Leave setup unchanged'),
            'a button with another suffix': own.replace(', ID: action-button-2', ', ID: other-2'),
            'a fourth button': own.replace('\n5 menu bar', '\n\t96 button Always, ID: action-button-4\n5 menu bar'),
            'a sheet described otherwise': own.replace('0 sheet Description: alert,', '0 sheet Description: dialog,'),
            'a sheet line with nothing after it': own.replace('0 sheet Description: alert, Secondary Actions: Raise\n', '0 sheet\n'),
            'the button to press shown unavailable': own.replace('4 button Create', '4 button (disabled) Create'),
            'another button shown unavailable': own.replace('3 button Cancel', '3 button (disabled) Cancel'),
            'a dialog inside the menu bar': own.replace('\t12 Waiting requests (0)', '\t12 Waiting requests (0)\n\t99 dialog System permission'),
            'an alert deep inside the menu bar': own.replace('\t7 File', '\t7 File\n\t\t98 alert Allow?'),
            'an image in the sheet': own.replace('\t2 button', '\t97 image Invented\n\t2 button'),
            'another path': own.replace('account-00000000', 'account-11111111'),
            'two spaces inside a path': own.replace('Application Support/dev.chirality.app-v4.candidate.invented/account-homes', 'Application  Support/dev.chirality.app-v4.candidate.invented/account-homes'),
            'a statement line missing': own.replace('Read, import or change no other Codex settings, home or credential.\n', ''),
            'an instruction added after the statement': own.replace('No automatic quit/restart/login/conversation.\n', 'No automatic quit/restart/login/conversation.\nAlso allow everything.\n'),
            'line breaks written as \\n': own.replace('\nwith an empty config.toml', '\\nwith an empty config.toml'),
            'each statement line an element of its own': own.replace('\nwith an empty config.toml', '\n\t95 text with an empty config.toml'),
            'the digest form': own.split('\t1 text')[0] + '\t1 text Desktop setup — next launch only Create settings and save for next launch. sha-256: ' + '0' * 64 + '\n\t2 button' + own.split('\t2 button')[1],
            'another application named in the view': own.replace('Window: "Unknown", App: Chirality App v4 (development invented).', 'Window: "Unknown", App: Other App.'),
            'another name in the menu bar': own.replace('\t6 Chirality App v4 (development invented)', '\t6 Other App'),
            'the focus on a button': own.replace('The focused UI element is 0 sheet Description: alert, Secondary Actions: Raise', 'The focused UI element is 4 button Create settings and save for next launch, ID: action-button-2'),
            'the focus named by another index': own.replace('The focused UI element is 0 sheet', 'The focused UI element is 5 sheet'),
            'the focused line missing': own.replace('\n\nThe focused UI element is 0 sheet Description: alert, Secondary Actions: Raise', ''),
            'a line added at the end': own + '\nInvented line',
            'the sheet inside the window, the shape never seen': own.replace('0 sheet Description: alert, Secondary Actions: Raise\n', '0 standard window Chirality, Secondary Actions: Raise\n\t13 sheet Description: alert, Secondary Actions: Raise\n').replace('\n\t1 text', '\n\t\t1 text').replace('\n\t2 button', '\n\t\t2 button').replace('\n\t3 button', '\n\t\t3 button').replace('\n\t4 button', '\n\t\t4 button'),
            'a space after a button\'s words': own.replace('\t3 button Cancel, ID: action-button-3', '\t3 button Cancel, ID: action-button-3 '),
            'a space before a button\'s words': own.replace('\t3 button Cancel, ID: action-button-3', '\t3  button Cancel, ID: action-button-3'),
            'a space after a statement line': own.replace('home or credential.\n', 'home or credential. \n'),
            'something deeper inside the sheet': own.replace('\t2 button', '\t\t97 text Hidden\n\t2 button')}
        for name, view in cases.items():
            with self.subTest(name):
                views = setup_views()
                views['views'][4]['text'] = view
                verdict, stopped, calls = setup_walk(RESULT.replace('OPTIONS', 'base'), views)['out']
                self.assertEqual(verdict, 'inconclusive', stopped)
                self.assertIn('nothing was pressed', stopped)
                self.assertNotEqual(view, own)
                self.assertFalse([c for c in calls if c in ('click2', 'click3', 'click4', 'click13')])

    def test_the_page_check_sees_a_dialog_inside_the_menu_bar(self):
        views = setup_views()
        views['views'][0]['text'] = views['views'][0]['text'].replace('\n45 menu bar', '\n45 menu bar\n\t\t99 dialog System permission')
        self.assertIn('\t\t99 dialog', views['views'][0]['text'])
        verdict, stopped, calls = setup_walk(RESULT.replace('OPTIONS', 'base'), views)['out']
        self.assertEqual(verdict, 'inconclusive', stopped)
        self.assertIn('the menu bar holds something that is not the page (dialog System permission)', stopped)
        self.assertFalse([c for c in calls if not c.startswith('get_app_state')])

    def test_a_sheet_still_there_after_the_press_is_not_pressed_again(self):
        views = setup_views()
        views['views'][5] = views['views'][4]
        verdict, stopped, calls = setup_walk(RESULT.replace('OPTIONS', 'base'), views)['out']
        self.assertEqual(verdict, 'inconclusive')
        self.assertIn('after the one press', stopped)
        self.assertIn('it is not pressed again', stopped)
        self.assertEqual(calls.count('click4'), 1)
        self.assertEqual(calls[-1], 'get_app_state')

    def test_an_earlier_failed_check_keeps_the_sheet_closed(self):
        views = setup_views()
        views['views'][3]['text'] = views['views'][3]['text'].replace(SETTINGS, '/invented/elsewhere/settings')
        verdict, stopped, calls = setup_walk(RESULT.replace('OPTIONS', 'base'), views)['out']
        self.assertEqual(verdict, 'inconclusive')
        self.assertIn('stopped at S4: the location "Settings folder" is not of the form the App makes', stopped)
        self.assertNotIn('click69', calls)
        # A path of the App's form whose check failed still keeps the sheet closed.
        verdict, stopped, calls = setup_walk("scenario.steps[3].expect.push({ text: 'Invented absent words' }); " + RESULT.replace('OPTIONS', 'base'))['out']
        self.assertEqual(verdict, 'fail')
        self.assertIn('an earlier check failed, so the sheet is not opened', stopped)
        self.assertNotIn('click69', calls)

    def test_only_the_project_is_typed_only_into_the_named_field_and_only_once(self):
        cases = {
            'two typing steps': "scenario.steps.splice(2, 0, { ...scenario.steps[1], id: 'S2b' })",
            'a value other than the project': "scenario.steps[1].value = '/invented/other'",
            'a second field named': "scenario.typed_fields.push('Find in received conversations')",
            'a second sheet named': "scenario.sheets.push({ ...scenario.sheets[0], id: 'other' })",
            'two pressing steps': "scenario.steps.push({ ...scenario.steps[4], id: 'S6' })",
            'no project given': 'base.project = undefined',
            'a project that is not beside the home': "base.project = '/invented/elsewhere/project'",
            'a relative project': "base.project = 'project'"}
        for name, change in cases.items():
            with self.subTest(name):
                verdict, stopped, calls = setup_walk(change + '; ' + RESULT.replace('OPTIONS', 'base'))['out']
                self.assertEqual((verdict, calls), ('inconclusive', []), stopped)
                self.assertTrue(stopped.startswith('refused before any call: '), stopped)
        for name, change, says in (
                ('a field the scenario does not name', "scenario.steps[1].control.label = 'Find in received conversations'", 'names no such field'),
                ('a field that is not a text field', "scenario.steps[1].control.kind = 'button'", 'names no such field'),
                ('a sheet opened by another control', "scenario.steps[4].control.label = 'Review setup'", 'names no such sheet'),
                ('a sheet the scenario does not name', "scenario.steps[4].sheet = 'other'", 'names no such sheet')):
            with self.subTest(name):
                verdict, stopped, calls = setup_walk(change + '; ' + RESULT.replace('OPTIONS', 'base'))['out']
                self.assertEqual(verdict, 'inconclusive')
                self.assertIn(says, stopped)
                self.assertNotIn('click4', calls)

    def test_a_link_is_the_one_whose_words_are_exactly_the_scenarios(self):
        elements = [{'index': 1, 'depth': 0, 'content': 'link Settings & tools'},
                    {'index': 2, 'depth': 0, 'content': 'link Settings & tools, Visited'},
                    {'index': 3, 'depth': 0, 'content': 'link Settings & tools and more'},
                    {'index': 4, 'depth': 0, 'content': 'button Settings & tools'}]
        result = harness(f"return walk.select({json.dumps(elements)}, {{ kind: 'link', label: 'Settings & tools' }}).map(e => e.index);")
        self.assertEqual(result['out'], [1, 2])

    def test_the_first_use_walk_still_makes_no_set_value_and_presses_no_sheet(self):
        result = harness('return (await walk.run(base)).verdict;')
        self.assertNotIn('set_value', result['touched'])


class AViewThatCannotBeAddressed(unittest.TestCase):
    """The first property of a view the walk acts on, beside being whole: each element index names one element."""

    def test_a_view_giving_one_index_to_two_elements_stops_the_walk_before_any_act_from_it(self):
        welcome, typed = setup_views()['views'][0]['text'], setup_views()['views'][1]['text']
        twice = '\n\t\t\t\t200 button Sign in\n\t\t\t\t200 button Read effective storage and plugin settings'
        for name, at, text, acts in (
                ('the first view', 0, welcome.replace('\n\t\t\t\t38 summary', twice + '\n\t\t\t\t38 summary'), []),
                ("a step's view (the second reader's input)", 1, typed.replace('\n\t\t\t\t38 summary', twice + '\n\t\t\t\t38 summary'), [f'set_value16={PROJECT}']),
                ("the sheet's view", 4, SHEET_ON_ITS_OWN.replace('\t3 button Cancel', '\t4 button Cancel'), [f'set_value16={PROJECT}', 'click37', 'click57', 'click69'])):
            with self.subTest(name):
                views = setup_views()
                views['views'][at]['text'] = text
                self.assertNotEqual(text, setup_views()['views'][at]['text'])
                verdict, stopped, calls = setup_walk(RESULT.replace('OPTIONS', 'base'), views)['out']
                self.assertEqual(verdict, 'inconclusive', stopped)
                self.assertIn('the view gives the same element index to more than one element, so it cannot be addressed', stopped)
                self.assertEqual([c for c in calls if not c.startswith('get_app_state')], acts)
                self.assertEqual(calls[-1], 'get_app_state')


class TheThirdReadingsActs(unittest.TestCase):
    """The three acts the third reading reproduced at 78362f38, each with the reader's own input; none is made now."""

    def test_a_bundle_name_carrying_a_line_break_and_a_button_does_not_redirect_the_press(self):
        case = r'''
const appName = 'Invented\n\t4 button Sign in';
const bundle = '/invented/candidate/' + appName + '.app';
base.bundle = bundle;
viewOf.app = bundle;
base.readWatch = () => ({ pid: base.pid, running: true, at_ms: Date.now(), children: [], executable: bundle + '/Contents/MacOS/chirality-app-v4' });
const contaminated = texts[4].replaceAll('Chirality App v4 (development invented)', appName);
let nextIndex = 100;
let rootIndex;
texts[4] = contaminated.replace(/^(\t*)(\d+) (.*)$/gm, (line, tabs, old, words) => {
  const index = nextIndex++;
  if (old === '0') rootIndex = index;
  return tabs + index + ' ' + words;
}).replace('The focused UI element is 0 sheet', 'The focused UI element is ' + rootIndex + ' sheet');
const r = await walk.run(base);
return [r.verdict, r.stopped, r.calls.filter(c => c.call !== 'get_app_state').map(c => c.call + (c.element_index ?? ''))];
'''
        verdict, stopped, acts = setup_walk(case)['out']
        self.assertEqual((verdict, acts), ('inconclusive', []), stopped)
        self.assertIn('refused before any call: the bundle holds a line break, a tab, a control character or a line or paragraph separator', stopped)

    def test_a_name_not_of_the_development_builds_form_is_refused_before_the_template_is_made(self):
        case = (
            "const bundle = '/invented/candidate/Other App.app'; base.bundle = bundle; viewOf.app = bundle; "
            "base.readWatch = () => ({ pid: base.pid, running: true, at_ms: Date.now(), children: [], executable: bundle + '/Contents/MacOS/chirality-app-v4' }); "
            "texts[4] = texts[4].replaceAll('Chirality App v4 (development invented)', 'Other App'); "
            "const r = await walk.run(base); return [r.verdict, r.stopped, r.calls.filter(c => c.call === 'click').map(c => c.element_index)];")
        verdict, stopped, clicks = setup_walk(case)['out']
        self.assertEqual((verdict, clicks), ('inconclusive', []), stopped)
        self.assertIn("stopped at S2: the view is not the listed state S1 (the candidate bundle's name is not of the development build's form", stopped)

    def test_a_row_holding_a_line_or_paragraph_separator_or_a_carriage_return_does_not_hide_a_second_index(self):
        for char, name in (('\u2028', 'line separator'), ('\u2029', 'paragraph separator'), ('\r', 'carriage return')):
            with self.subTest(name):
                views = setup_views()
                views['views'][0]['text'] = views['views'][0]['text'].replace('\n45 menu bar', '\n\t\t\t\t16 button Sign in' + char + 'other words\n45 menu bar')
                verdict, stopped, calls = setup_walk(RESULT.replace('OPTIONS', 'base'), views)['out']
                self.assertEqual(verdict, 'inconclusive', stopped)
                self.assertIn('is not one the walk recognises; nothing is clicked, typed or pressed from it', stopped)
                self.assertEqual([c for c in calls if not c.startswith('get_app_state')], [])

    def test_a_non_canonical_index_beside_the_same_index_in_canonical_form_leads_to_no_act(self):
        views = setup_views()
        views['views'][0]['text'] = views['views'][0]['text'].replace('\n45 menu bar', '\n\t\t\t\t016 button Sign in\n45 menu bar')
        self.assertIn('016 button Sign in', views['views'][0]['text'])
        verdict, stopped, calls = setup_walk(RESULT.replace('OPTIONS', 'base'), views)['out']
        self.assertEqual(verdict, 'inconclusive', stopped)
        self.assertIn('is not one the walk recognises', stopped)
        self.assertEqual([c for c in calls if not c.startswith('get_app_state')], [])

    def test_an_index_too_long_to_read_exactly_is_refused(self):
        views = setup_views()
        views['views'][0]['text'] = views['views'][0]['text'].replace('16 text field', '9007199254740993 text field')
        verdict, stopped, calls = setup_walk(RESULT.replace('OPTIONS', 'base'), views)['out']
        self.assertEqual(verdict, 'inconclusive', stopped)
        self.assertIn('is not one the walk recognises', stopped)
        self.assertEqual([c for c in calls if not c.startswith('get_app_state')], [])


class AViewRecognisedLineForLine(unittest.TestCase):
    """walk.recognise: the supplier's window line, element lines with their further lines, then at most a blank line
    and the focused-element line. Anything else is refused."""

    def recognise(self, text):
        return harness(f'const r = walk.recognise({json.dumps(text)}); return [r.refusal, r.elements.length];')['out']

    def test_the_recorded_views_are_recognised(self):
        self.assertEqual(self.recognise(SHEET_ON_ITS_OWN), [None, 13])
        for view in json.loads(VIEWS.read_text())['views']:
            self.assertIsNone(self.recognise(view['text'])[0])
        self.assertIsNone(self.recognise(json.loads(VIEWS.read_text())['views'][0]['text'] + '\n')[0])  # as a real view ends

    def test_anything_else_is_refused(self):
        own = SHEET_ON_ITS_OWN
        cases = {
            'no window line': own.split('\n', 1)[1],
            'a window line without its application': own.replace(', App: Chirality App v4 (development invented).', ''),
            'an index with a leading zero': own.replace('\t3 button Cancel', '\t03 button Cancel'),
            'a non-canonical form of an index that is also present': own.replace('\t3 button Cancel, ID: action-button-3', '\t3 button Cancel, ID: action-button-3\n\t03 button Sign in'),
            'an index of sixteen digits': own.replace('\t3 button Cancel', '\t1000000000000003 button Cancel'),
            'a further line straight after the window line': own.replace('\n0 sheet', '\nwords\n0 sheet'),
            'a further line beginning with a tab': own.replace('\nwith an empty config.toml', '\n\twith an empty config.toml'),
            'a control character in the words': own.replace('button Cancel', 'button Can\x07cel'),
            'a line after the focused line': own + '\nInvented',
            'two lines after the blank line': own.replace('\n\nThe focused', '\n\nInvented\nThe focused'),
            'the focused line naming no element': own.replace('The focused UI element is 0 sheet', 'The focused UI element is 99 sheet'),
            'a difference marker in a whole view': own.replace('\t3 button Cancel', '~\t3 button Cancel'),
            'one index given twice': own.replace('\t3 button Cancel', '\t4 button Cancel')}
        for name, text in cases.items():
            with self.subTest(name):
                self.assertNotEqual(text, own)
                refusal, _ = self.recognise(text)
                self.assertIsNotNone(refusal)


class TheSignedOutScenarioFiles(unittest.TestCase):
    def test_the_sheets_statement_is_the_apps_new_settings_statement_line_for_line(self):
        source = (APP / 'src-tauri/src/desktop_startup.rs').read_text()
        branch = source[source.index('if let PreviewKind::NewSettings { settings } = &preview.kind {'):]
        statement = re.search(r'format!\("((?:[^"\\]|\\.)*)"', branch).group(1)
        supplier = re.search(r'const SUPPLIER: &str = "([^"]+)";', source).group(1)
        named = iter(['{settings}', '{account}', '{project}', '{request}'])
        expected = re.sub(r'\{\}', lambda _: next(named), statement.replace('{SUPPLIER}', supplier)).split('\\n')
        recorded = json.loads(SETUP.read_text())['sheets'][0]['statement']
        # The scenario is as recorded on candidate 9d997626. PR 334 (main fc1b222d) changed the statement's second
        # line in the App; the recorded line stays until the scenario is re-recorded from a build of main, and the
        # README names the stale states. Every other line is still the App's, line for line.
        stale = {1: ('with an empty config.toml, an empty AGENTS.md and an empty skills folder.',
                     'with an empty config.toml, an empty AGENTS.md and a skills folder. Codex adds its own system skills '
                     'there, and its own working files to the account directory, when it starts.')}
        self.assertEqual(len(recorded), len(expected))
        for n, (was, now) in enumerate(zip(recorded, expected)):
            self.assertEqual((was, now), stale[n] if n in stale else (now, now), n)

    def test_the_sheets_title_and_buttons_are_the_apps(self):
        sheet = json.loads(SETUP.read_text())['sheets'][0]
        confirmation = (APP / 'src-tauri/src/desktop_setup_confirmation.rs').read_text()
        self.assertIn(f'"{sheet["title"]}"', confirmation)
        buttons = [re.match(r'^\t\d+ button (.*), ID: action-button-\d+$', line).group(1) for line in sheet['view'] if ' button ' in line]
        self.assertEqual(buttons, ['Leave setup unchanged', 'Cancel', 'Create settings and save for next launch'])
        self.assertIn(f'"{buttons[0]}"', confirmation)
        self.assertIn(f'"{buttons[1]}"', (APP / 'src-tauri/src/act_control.rs').read_text())
        self.assertIn(f'"affirmative"] = json!("{sheet["press"]}")', (APP / 'src-tauri/src/desktop_startup.rs').read_text())

    def test_the_walks_acts_are_the_ones_the_method_allows(self):
        setup, relaunch = json.loads(SETUP.read_text()), json.loads(RELAUNCH.read_text())
        self.assertEqual([step['act'] for step in setup['steps']], ['view', 'type', 'click', 'click', 'confirm_sheet'])
        self.assertEqual(setup['typed_fields'], ['Project folder'])
        # The setup acts only in its five listed states: four recorded views and the sheet.
        self.assertEqual({step['id']: step.get('from_state') for step in setup['steps'] if step['act'] != 'view'},
                         {'S2': 'S1', 'S3': 'S2', 'S4': 'S3', 'S5': 'S4'})
        self.assertEqual(sorted(setup['states']), ['S1', 'S2', 'S3', 'S4'])
        # The relaunch acts in no state: one view, read.
        self.assertEqual([(step['id'], step['act']) for step in relaunch['steps']], [('R1', 'view')])
        self.assertNotIn('states', relaunch)
        self.assertNotIn('typed_fields', relaunch)
        self.assertNotIn('sheets', relaunch)

    def test_the_listed_states_are_the_recorded_views_and_recognised(self):
        setup = json.loads(SETUP.read_text())
        for name in ('S1', 'S2', 'S3', 'S4'):
            with self.subTest(name):
                text = setup_state(name)
                self.assertNotIn('{', text.replace('{~', ''))  # every placeholder filled
                self.assertIsNone(harness(f'return walk.recognise({json.dumps(text)}).refusal;')['out'])
        self.assertIn('0 standard window Chirality', setup_state('S1'))
        self.assertIn('summary Exact locations, Value: on', setup_state('S4'))


class AButtonPressedOnlyIfOffered(unittest.TestCase):
    """A click step marked if_offered presses its button when the App offers it and otherwise records that it did not."""

    def walk(self, control, first=None, if_offered=True, expect=None):
        scenario = json.loads(SCENARIO.read_text())
        step = {'id': 'O1', 'act': 'click', 'control': control, 'says': 'invented', 'expect': expect or [{'no_text': 'Invented absent words'}]}
        if if_offered:
            step['if_offered'] = True
        scenario['steps'], scenario['outcomes'] = [step], {}
        views = setup_views()
        if first:
            views['views'][0]['text'] = first
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'scenario.json'
            path.write_text(json.dumps(scenario))
            return setup_walk('const r = await walk.run(base); return [r.verdict, r.stopped, '
                              'r.calls.filter(c => c.call === "click").map(c => c.element_index), r.steps.map(s => s.offered ?? null)];',
                              views, path)['out']

    def test_an_unavailable_button_is_not_pressed_and_is_recorded_as_not_offered(self):
        self.assertEqual(self.walk({'kind': 'button', 'label': 'Review setup'}), ['pass', None, [], ['unavailable; not pressed']])

    def test_an_absent_button_is_not_pressed_and_is_recorded_as_not_offered(self):
        self.assertEqual(self.walk({'kind': 'button', 'label': 'Read effective storage and plugin settings'}),
                         ['pass', None, [], ['absent; not pressed']])

    def test_an_available_button_is_pressed_once(self):
        typed = setup_views()['views'][1]['text']
        self.assertEqual(self.walk({'kind': 'button', 'label': 'Review setup'}, first=typed), ['pass', None, [37], ['available; pressed']])

    def test_the_steps_checks_still_decide_when_nothing_is_pressed(self):
        verdict, _, clicks, _ = self.walk({'kind': 'button', 'label': 'Review setup'}, expect=[{'button': 'Review setup', 'is': 'available'}])
        self.assertEqual((verdict, clicks), ('fail', []))

    def test_without_the_mark_an_unavailable_button_is_still_a_failure(self):
        verdict, stopped, clicks, _ = self.walk({'kind': 'button', 'label': 'Review setup'}, if_offered=False)
        self.assertEqual((verdict, clicks), ('fail', []))
        self.assertIn('the control to click is unavailable', stopped)

    def test_the_mark_does_not_reach_a_control_that_is_not_a_button(self):
        verdict, stopped, clicks, _ = self.walk({'kind': 'link', 'label': 'Invented link'})
        self.assertEqual((verdict, clicks), ('inconclusive', []))
        self.assertIn('only a button is pressed if offered', stopped)

    def test_the_buttons_words_on_a_control_of_another_kind_stop_the_walk(self):
        welcome = setup_views()['views'][0]['text']
        for name, line in (('a link', 'link Read effective storage and plugin settings'),
                           ('a link that has been visited', 'link Read effective storage and plugin settings, Visited'),
                           ('a text', 'text Read effective storage and plugin settings')):
            with self.subTest(name):
                view = welcome.replace('\n45 menu bar', f'\n\t\t\t\t96 {line}\n45 menu bar')
                self.assertIn(line, view)
                verdict, stopped, clicks, offered = self.walk({'kind': 'button', 'label': 'Read effective storage and plugin settings'}, first=view)
                self.assertEqual((verdict, clicks, offered), ('inconclusive', [], [None]))
                self.assertIn('are on something that is not that button', stopped)

    def test_the_mark_does_not_reach_a_button_found_twice_and_records_no_press(self):
        typed = setup_views()['views'][1]['text']
        twice = typed.replace('37 button Review setup', '37 button Review setup\n\t\t\t\t98 button Review setup')
        verdict, stopped, clicks, offered = self.walk({'kind': 'button', 'label': 'Review setup'}, first=twice)
        self.assertEqual((verdict, clicks, offered), ('inconclusive', [], [None]))
        self.assertIn('found 2 times', stopped)


if __name__ == '__main__':
    unittest.main()
