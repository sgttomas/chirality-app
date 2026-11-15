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
const rawWalk = await import(process.argv[1]);
const scenarioModule = await import(new URL('./scenario.mjs', process.argv[1]).href);
// The harness stands where replay and the operator stand: a scenario is validated by its only constructor before the
// walk is given it, and the walk is given only what that made. A scenario it refuses is given as it is, so that the
// walk's own refusal of anything validateScenario did not make is what the test sees; the refusal is kept beside it.
let lastRefusal = null;
const validated = options => {
  lastRefusal = null;
  if (scenarioModule.isValidScenario(options.scenario)) return options;
  const made = scenarioModule.parseScenario(JSON.stringify(options.scenario));
  lastRefusal = made.refusal ?? null;
  return { ...options, scenario: made.scenario ?? options.scenario };
};
const walkModule = { ...rawWalk, run: options => rawWalk.run(validated(options)) };
// A scenario that names no listed states (the first-use scenario, kept for the hosted driver) is given, for these
// tests of the walk's mechanics, the views it is fed as its states, read when the walk starts: each acting step's
// from_state, and each step's own judged state (the view it is fed after it), so that a pass here rests on equality
// with a recorded state as the verdict rule requires.
const listAll = () => {
  // Only a scenario that acts and lists no states: a view-only scenario gets none, and stays captured, not judged.
  if (scenario.states || !scenario.steps.some(step => ['type', 'click', 'confirm_sheet'].includes(step.act))) return;
  scenario.states = {};
  scenario.steps.forEach((step, n) => {
    if (['type', 'click', 'confirm_sheet'].includes(step.act)) {
      step.from_state = 'V' + (n - 1);
      scenario.states[step.from_state] = String(texts[Math.max(n - 1, 0)] ?? '').split('\\n');
    }
    step.state = 'V' + n;
    scenario.states[step.state] = String(texts[n] ?? '').split('\\n');
  });
};
// Each listed state is bound, as record_state.mjs binds a recorded one, to the build the walk is given.
const bindAll = options => {
  if (!scenario.states || scenario.state_records) return;
  const app_name = String(options.bundle ?? '').split('/').pop().replace(/\\.app$/, '');
  scenario.state_records = Object.fromEntries(Object.keys(scenario.states).map(id =>
    [id, { recorded_on: { candidate_key: 'invented-key', identifier: options.app, app_name }, judged: { result: 'every expectation held' } }]));
};
// For these tests of the walk's mechanics, a view joining the attempt log and the result (test-only: the walk returns
// them apart, and nothing in the walk reads the one from the other). The result itself is kept whole as r.result.
// Test-only: where validateScenario refused the scenario, its reason is added to the walk's own refusal, labelled.
const testView = (verdict, log) => ({ ...log, verdict, log, scenario_refused: lastRefusal,
  stopped: lastRefusal ? `${log.stopped} (validateScenario: ${lastRefusal})` : log.stopped });
const walk = { ...walkModule, run: async options => {
  listAll(); bindAll(options);
  let log = null;
  const result = await walkModule.run({ ...options, onLog: given => { log = given; } });
  return testView(result, log);
} };
const scenario = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const recorded = JSON.parse(readFileSync(process.argv[3], 'utf8'));
// The views these tests are fed are invented. Most were rebuilt from the differences a walk received, and differences
// keep an element's index when others come and go; every whole view the supplier has returned numbers its element
// lines 0 to N in order. So each view is given that numbering before the walk reads it (the focused line follows).
const inOrder = text => {
  const map = new Map(); let k = 0;
  const lines = String(text).split('\\n').map((line, n) => {
    const m = n === 0 ? null : /^(\\t*)(0|[1-9][0-9]*) (.*)$/.exec(line);
    if (!m) return line;
    if (!map.has(m[2])) map.set(m[2], String(k));
    return `${m[1]}${k++} ${m[3]}`;
  });
  return lines.map(line => { const f = /^The focused UI element is (0|[1-9][0-9]*) (.*)$/.exec(line);
    return f && map.has(f[1]) ? `The focused UI element is ${map.get(f[1])} ${f[2]}` : line; }).join('\\n');
};
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
  readWatch: watched(), readIdentification: () => ({ candidate_key: 'invented-key' }), sleep: async () => {} };
const out = await (async () => { CASE })();
console.log(JSON.stringify({ out, touched }));
'''


def setUpModule():
    if NODE is None:
        if os.environ.get('CI'):
            raise RuntimeError('node is required for the operated scenario tests in CI')
        raise unittest.SkipTest('node is not installed')


def joined_view(verdict, log):
    """The attempt log with the walk's verdict beside it, for tests of the walk's mechanics (as the harness's testView)."""
    return {**(log or {}), 'verdict': verdict, 'log': log}


def replay(*paths):
    with tempfile.TemporaryDirectory() as folder:
        log_path = Path(folder) / 'attempt-log.json'
        done = subprocess.run([NODE, str(REPLAY), *map(str, paths), '--log', str(log_path)], capture_output=True, text=True)
        log = json.loads(log_path.read_text()) if log_path.exists() else None
    if not done.stdout.strip():
        return done.returncode, None, done.stderr
    return done.returncode, joined_view(json.loads(done.stdout), log), done.stderr


def in_order(text):
    """A view numbered as every whole view the supplier has returned is: element lines 0 to N in order (the focused
    line follows). views.json's later views were rebuilt from the differences a walk received, and differences keep an
    element's index when others come and go, so they are given this numbering before the walk is fed them."""
    numbers, lines, k = {}, [], 0
    for n, line in enumerate(text.split('\n')):
        found = None if n == 0 else re.match(r'^(\t*)(0|[1-9][0-9]*) (.*)$', line)
        if found:
            numbers.setdefault(found.group(2), str(k))
            line = f'{found.group(1)}{k} {found.group(3)}'
            k += 1
        lines.append(line)
    focused = re.compile(r'^The focused UI element is (0|[1-9][0-9]*) (.*)$')
    return '\n'.join(focused.sub(lambda m: f'The focused UI element is {numbers.get(m.group(1), m.group(1))} {m.group(2)}', line)
                     for line in lines)


def harness_views():
    """The first-use views, renumbered as whole views are (in_order). Invented fixtures for the walk's mechanics; not
    evidence of the supplier's output."""
    views = json.loads(VIEWS.read_text())
    return {**views, 'views': [{**view, 'text': in_order(view['text'])} for view in views['views']]}


def harness(case):
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / 'views.json'
        path.write_text(json.dumps(harness_views()))
        done = subprocess.run([NODE, '--input-type=module', '-e', HARNESS.replace('CASE', case), WALK.as_uri(), str(SCENARIO),
                               str(path)], capture_output=True, text=True)
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
        with tempfile.TemporaryDirectory() as folder:
            code, report, said = replay(rebound(SETUP, folder), self.views_file())
        self.assertEqual((code, report['verdict'], report['stopped']), (0, 'pass', None), said)
        self.assertEqual([step['id'] for step in report['steps']], ['S1', 'S2', 'S3', 'S4', 'S5'])
        self.assertEqual([call['call'] for call in report['calls'] if call['call'] != 'get_app_state'],
                         ['set_value', 'click', 'click', 'click', 'click'])
        self.assertEqual({call['app'] for call in report['calls']}, {'dev.chirality.app-v4.candidate.invented'})

    def test_states_recorded_on_another_build_are_not_used(self):
        # The committed scenario's states are bound to the build they were recorded on (1023908b); on the fixture
        # views' invented build the walk uses none of them: it stops at the first step, judging and acting on nothing.
        code, report, said = replay(SETUP, self.views_file())
        self.assertEqual((code, report['verdict']), (2, 'inconclusive'), said)
        self.assertIn('the recorded state S1 was recorded on another build', report['stopped'])
        self.assertEqual([call['call'] for call in report['calls'] if call['call'] != 'get_app_state'], [])
        # And a state with no record of being judged is not used either: through replay, nothing is acted on.
        with tempfile.TemporaryDirectory() as folder:
            scenario = json.loads(rebound(SETUP, folder).read_text())
            scenario['state_records']['S1']['judged']['result'] = 'not judged'
            path = Path(folder) / 'unjudged.scenario.json'
            path.write_text(json.dumps(scenario))
            code, report, said = replay(path, self.views_file())
        self.assertEqual((code, report['verdict']), (2, 'inconclusive'), said)
        self.assertIn('the recorded state S1 was not judged before it was recorded', report['stopped'])
        self.assertEqual([call['call'] for call in report['calls'] if call['call'] != 'get_app_state'], [])

    def test_a_scenario_that_acts_and_names_no_listed_state_is_refused_before_any_call(self):
        code, report, said = replay(SCENARIO, VIEWS)  # the first-use scenario, kept for the hosted driver
        self.assertEqual((code, report['verdict'], report['calls']), (2, 'inconclusive', []), said)
        self.assertIn('not made by validateScenario', report['stopped'])
        self.assertIn('the scenario is not of the closed form: step 2 (click) has no from_state', said)
        self.assertEqual(report['replayed']['scenario_refused'], 'step 2 (click) has no from_state')

    def test_the_whole_result_arrives_through_a_pipe_and_the_long_attempt_log_apart(self):
        views = setup_views()
        # The page after the press, given a long text: the attempt log outgrows a pipe, and the view no longer equals
        # the recorded state S5, so the verdict is fail. The verdict arrives on its own; the long log goes apart.
        views['views'][5]['text'] = in_order(views['views'][5]['text'].replace(f'\t\t\t\t\t\t12 text Project: {PROJECT}',
                                                                      f'\t\t\t\t\t\t12 text Project: {PROJECT}\n\t\t\t\t\t\t13 text ' + 'invented words ' * 5000))
        with tempfile.TemporaryDirectory() as folder:
            log = Path(folder) / 'attempt-log.json'
            done = subprocess.run([NODE, str(REPLAY), str(rebound(SETUP, folder)), str(self.views_file(views)), '--log', str(log)],
                                  capture_output=True, text=True)
            self.assertGreater(log.stat().st_size, 65536)  # longer than a pipe holds at once
            self.assertTrue(log.read_text().startswith('{\n  "note": "ATTEMPT LOG. This is not a result'))
        self.assertEqual((done.returncode, json.loads(done.stdout)), (1, 'fail'))

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
                result = harness(f"texts[2] = inOrder(texts[2].replace('{window}', '{window}\\n{line}')); const r = await walk.run(base); "
                                 'return [r.verdict, r.stopped, r.calls.length];')
                verdict, stopped, calls = result['out']
                self.assertEqual((verdict, calls), ('inconclusive', 7), stopped)  # five views, two clicks, then nothing
                self.assertIn('stopped at S3: the window holds something that is not the page', stopped)
                self.assertIn('no agent answers a prompt or a dialog', stopped)
        beside = {'a second window': '900 standard window Confirm', 'a system dialog beside it': '900 system dialog Allow?',
                  'something unnamed beside it': '900 group'}
        for name, line in beside.items():
            with self.subTest(name):
                result = harness(f"texts[2] = inOrder(texts[2].replace(/\\n(\\d+) menu bar/, '\\n{line}\\n$1 menu bar')); const r = await walk.run(base); "
                                 'return [r.verdict, r.stopped, r.calls.length];')
                verdict, stopped, calls = result['out']
                self.assertEqual((verdict, calls), ('inconclusive', 7), stopped)
                # Refused at recognition now (the anchor: the top level is exactly element 0 and the menu bar), before
                # the page check that used to refuse it; still nothing further is called.
                self.assertIn('stopped at S3: its top level is not exactly its first element and the menu bar; nothing is clicked, typed or pressed from it', stopped)
        for name, change in (('a window whose title only begins the same way', "'standard window Chirality Setup, Secondary Actions: Raise'"),
                             ('no window', "'group'")):
            with self.subTest(name):
                result = harness(f"texts[0] = texts[0].replace('standard window Chirality, Secondary Actions: Raise', {change}); "
                                 'const r = await walk.run(base); return [r.verdict, r.stopped, r.calls.length];')
                self.assertEqual((result['out'][0], result['out'][2]), ('inconclusive', 1), result['out'][1])

    def test_page_words_about_a_dialog_do_not_stop_it(self):
        text = json.loads(VIEWS.read_text())['views'][3]['text']
        self.assertNotIn('dialog', ' '.join(line.strip().split(' ')[1] for line in text.split('\n')[1:] if line.strip()))
        result = harness("texts[3] = inOrder(texts[3].replace(/\\n(\\t\\d+ close button)/, '\\n\\t\\t\\t\\t\\t\\t\\t999 text The App asks you to confirm in its own dialog.\\n$1')); "
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
                result = harness(f"texts[{view}] = inOrder(texts[{view}].replace(/\\n(\\t\\d+ close button)/, '\\n{lines}\\n$1')); "
                                 'const r = await walk.run(base); '
                                 'return [r.verdict, r.steps.filter(s => s.expectations_not_found?.length).map(s => s.id), '
                                 'r.steps.flatMap(s => (s.expectations_not_found ?? []).map(c => String(c.found)))];')
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
                         'return [r.verdict, r.stopped, r.calls.map(c => c.call).join(" "), r.steps.map(s => s.id), '
                         'typeof r.steps.at(-1).rebuilt_for_reading, r.steps.at(-1).returned.slice(0, 30)];')
        verdict, stopped, calls, steps, rebuilt, returned = result['out']
        self.assertEqual(verdict, 'inconclusive', stopped)
        self.assertIn('stopped at S2: the view came back as differences although the whole window was asked for;', stopped)
        self.assertEqual(calls, 'get_app_state get_app_state get_app_state click get_app_state')  # and none after it
        self.assertEqual(steps[-1], 'S2')
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
        # The causes are kept whole in the attempt log's error record (failed, above); the summary reads only the result.
        self.assertNotIn('caused by', summary)
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
        self.assertNotIn('caused by', summary)  # kept in the attempt log's click_error (failed, above)
        self.assertEqual((clicks, calls_after, step_error), (1, 0, 'Sky Computer Use click failed'))

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
    "sleep: async () => {} };", "sleep: async () => {}, project: recorded.project };")


def setup_state(name):
    """A listed state of the setup scenario, filled with the invented values."""
    text = '\n'.join(json.loads(SETUP.read_text())['states'][name])
    for placeholder, value in {'{app_name}': 'Chirality App v4 (development invented)', '{project}': PROJECT,
                               '{settings}': SETTINGS, '{account}': ACCOUNT, '{request}': REQUEST, '{~number}': '0'}.items():
        text = text.replace(placeholder, value)
    return text


# The invented identity every fixture view carries.
INVENTED = {'app': 'dev.chirality.app-v4.candidate.invented', 'home': '/invented/homes/launch-invented/home',
            'bundle': '/invented/candidate/target/debug/bundle/macos/Chirality App v4 (development invented).app'}
INVENTED_APP = 'Chirality App v4 (development invented)'  # the launched build's name, from the bundle above
# The page after the setup confirmation, as the supplier returned it whole on candidate 9d997626 (14 November 2026,
# 12:23 UTC), with the project path and the build's name made invented.
AFTER_THE_PRESS = (APP / 'tests/group_b_operated_fixtures/signed-out-setup/after-the-press.txt').read_text()


def setup_views(sheet=None, after=None):
    """Whole views for the signed-out setup walk: the scenario's own listed states filled with invented values, the
    recorded sheet, and the recorded page after it. sheet: the whole view of the sheet; by default the recorded one."""
    with_sheet = SHEET_ON_ITS_OWN if sheet is None else sheet
    return {**INVENTED, 'project': PROJECT, 'candidate_key': 'invented-key',
            'views': [{'text': text} for text in (setup_state('S1'), setup_state('S2'), setup_state('S3'), setup_state('S4'),
                                                  with_sheet, after or AFTER_THE_PRESS)]}


SHEET_ON_ITS_OWN = (APP / 'tests/group_b_operated_fixtures/signed-out-setup/sheet-on-its-own.txt').read_text()


def rebound(scenario_path, folder):
    """A copy of a committed scenario whose recorded states are bound to the invented build of the fixture views, so
    that its walk's mechanics can be tested on them. The committed file stays bound to the build it was recorded on."""
    scenario = json.loads(Path(scenario_path).read_text())
    for record in [*(scenario.get('state_records') or {}).values(), *(scenario.get('sheet_records') or {}).values()]:
        record['recorded_on'] = {**record['recorded_on'], 'candidate_key': 'invented-key', 'identifier': INVENTED['app'], 'app_name': INVENTED_APP}
    path = Path(folder) / ('rebound-' + Path(scenario_path).name)
    path.write_text(json.dumps(scenario))
    return path


def setup_walk(case, views=None, scenario=SETUP, rebind=True):
    with tempfile.TemporaryDirectory() as folder:
        if rebind:
            scenario = rebound(scenario, folder)
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
                         [f'set_value16={PROJECT}', 'click37', 'click57', 'click76', 'click4'])

    def test_a_sheet_step_with_no_press_captures_the_sheet_and_presses_nothing(self):
        # The re-recording's capture: the sheet is opened from S4, captured whole and not pressed, whatever it says.
        capture = json.loads(SETUP.read_text())
        next(s for s in capture['steps'] if s['act'] == 'confirm_sheet')['press'] = False
        for name, sheet in (('the recorded sheet', None), ('a sheet that differs', SHEET_ON_ITS_OWN.replace('Leave setup unchanged', 'Leave it'))):
            with self.subTest(name), tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / 'capture.scenario.json'
                path.write_text(json.dumps(capture))
                result = setup_walk('const r = await walk.run(base); return [r.verdict, r.stopped, r.calls.map(c => c.call + (c.element_index ?? "")), r.steps.at(-1).sheet_view];',
                                    setup_views(sheet=sheet), path)
                verdict, stopped, calls, captured = result['out']
                self.assertEqual((verdict, stopped), ('inconclusive', 'stopped at S5: the sheet is captured, and this step has no press'))
                self.assertEqual([c for c in calls if not c.startswith('get_app_state')], ['set_value16', 'click37', 'click57', 'click76'])
                self.assertEqual(captured, sheet or SHEET_ON_ITS_OWN)

    def test_the_sheet_capture_scenario_is_the_setup_scenario_with_no_press(self):
        # The re-recording's capture differs from the setup walk only in its name, its own sentence and the one
        # sheet step marked "press": false, so it captures exactly the views the setup walk acts from, and presses nothing.
        setup = json.loads(SETUP.read_text())
        capture = json.loads((OPERATED / 'signed-out-setup-sheet-capture.scenario.json').read_text())
        sheet_step = next(s for s in capture['steps'] if s['act'] == 'confirm_sheet')
        self.assertIs(sheet_step.pop('press'), False)
        for field in ('scenario', 'what_it_is'):
            self.assertNotEqual(capture.pop(field), setup.pop(field))
        # Only the setup walk reaches the view after the press, so only it holds S5 and judges its last step by it.
        setup['states'].pop('S5')
        setup['state_records'].pop('S5')
        setup.pop('sheet_records')  # only the setup walk presses the sheet, so only it holds the template's record
        next(s for s in setup['steps'] if s['id'] == 'S5').pop('state')
        capture.pop('states_recorded'), setup.pop('states_recorded')
        self.assertEqual(capture, setup)

    def test_a_dialog_anywhere_below_the_window_stops_an_ordinary_step(self):
        result = harness("texts[2] = inOrder(texts[2].replace('\\t\\t2 HTML content', '\\t\\t\\t\\t950 sheet Confirm\\n\\t\\t2 HTML content')); "
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

    def test_an_alert_holding_a_control_is_not_page(self):
        views = setup_views()
        views['views'][0]['text'] = in_order(views['views'][0]['text'].replace(
            '\t\t\t\t\t\t\t15 text Project folder\n\t\t\t\t\t\t\t16 text field',
            '\t\t\t\t\t\t990 alert External prompt\n\t\t\t\t\t\t\t15 text Project folder\n\t\t\t\t\t\t\t16 text field'))
        self.assertIn(' alert External prompt', views['views'][0]['text'])
        verdict, stopped, calls = setup_walk(RESULT.replace('OPTIONS', 'base'), views)['out']
        self.assertEqual(verdict, 'inconclusive')
        self.assertIn('alert External prompt', stopped)
        self.assertFalse([c for c in calls if c.startswith('set_value')])

    def test_a_field_alone_inside_a_page_alert_is_not_typed_into(self):
        views = setup_views()
        views['views'][0]['text'] = in_order(views['views'][0]['text'].replace(
            '\t\t\t\t\t\t\t15 text Project folder\n\t\t\t\t\t\t\t16 text field (settable) Project folder, Placeholder: /full/path/to/your/project\n',
            '\t\t\t\t\t\t990 alert External prompt\n\t\t\t\t\t\t\t15 text Project folder\n\t\t\t\t\t\t\t16 text field (settable) Project folder, Placeholder: /full/path/to/your/project\n'
            '\t\t\t\t\t\t991 container\n'))
        self.assertIn(' alert External prompt', views['views'][0]['text'])
        verdict, stopped, calls = setup_walk(RESULT.replace('OPTIONS', 'base'), views)['out']
        self.assertEqual(verdict, 'inconclusive')
        self.assertIn('alert External prompt', stopped)
        self.assertFalse([c for c in calls if c.startswith('set_value')])

    def test_an_alert_in_the_pages_own_content_is_page_not_prompt(self):
        result = harness("texts[2] = inOrder(texts[2].replace('\\t\\t\\t3 container Welcome', '\\t\\t\\t3 container Welcome\\n\\t\\t\\t\\t990 alert Why Codex was not started')); "
                         'return (await walk.run(base)).verdict;')
        self.assertEqual(result['out'], 'pass')
        result = harness("texts[2] = inOrder(texts[2].replace(/\\n(\\t\\d+ close button)/, '\\n\\t989 scroll area\\n\\t\\t990 alert Allow?\\n$1')); "
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

    def test_a_view_numbered_otherwise_than_0_to_n_in_order_is_refused_and_nothing_is_pressed(self):
        # Every whole view the supplier has returned numbers its elements 0 to N in order (the anchor), so a sheet
        # numbered from 100 is not that view: it is refused, and the press is not made.
        renumbered = re.sub(r'^(\t*)(\d+) ', lambda m: f'{m.group(1)}{int(m.group(2)) + 100} ', SHEET_ON_ITS_OWN, flags=re.M).replace(
            'The focused UI element is 0 sheet', 'The focused UI element is 100 sheet')
        verdict, stopped, calls = setup_walk(RESULT.replace('OPTIONS', 'base'), setup_views(sheet=renumbered))['out']
        self.assertEqual(verdict, 'inconclusive', stopped)
        self.assertIn('not in index order from 0', stopped)
        self.assertNotIn('click4', calls[-1:])
        self.assertEqual([c for c in calls if not c.startswith('get_app_state')], ['set_value16=' + PROJECT, 'click37', 'click57', 'click76'])

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
        views['views'][0]['text'] = in_order(views['views'][0]['text'].replace('\n45 menu bar', '\n45 menu bar\n\t\t99 dialog System permission'))
        self.assertIn('\t\t46 dialog', views['views'][0]['text'])
        verdict, stopped, calls = setup_walk(RESULT.replace('OPTIONS', 'base'), views)['out']
        self.assertEqual(verdict, 'inconclusive', stopped)
        # The menu bar is no longer the App's own block, so the view is refused before the page is looked at.
        self.assertIn("does not end with the App window's own menu bar", stopped)
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
        self.assertNotIn('click76', calls)
        # A path of the App's form whose check failed still keeps the sheet closed.
        verdict, stopped, calls = setup_walk("scenario.steps[3].expect.push({ text: 'Invented absent words' }); " + RESULT.replace('OPTIONS', 'base'))['out']
        self.assertEqual(verdict, 'fail')
        self.assertIn('an earlier check failed, so the sheet is not opened', stopped)
        self.assertNotIn('click76', calls)

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
                ('a field the scenario does not name', "scenario.steps[1].control.label = 'Find in received conversations'", 'types into a field the scenario does not name in typed_fields'),
                ('a field that is not a text field', "scenario.steps[1].control.kind = 'button'", 'is not a text field named by text'),
                ('a sheet opened by another control', "scenario.steps[4].control.label = 'Review setup'", 'is not the button that opens its sheet'),
                ('a sheet the scenario does not name', "scenario.steps[4].sheet = 'other'", 'sheet is not one the scenario names')):
            with self.subTest(name):
                verdict, stopped, calls = setup_walk(change + '; ' + RESULT.replace('OPTIONS', 'base'))['out']
                self.assertEqual(verdict, 'inconclusive')
                self.assertIn(says, stopped)
                self.assertNotIn('click4', calls)

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
                ("the sheet's view", 4, SHEET_ON_ITS_OWN.replace('\t3 button Cancel', '\t4 button Cancel'), [f'set_value16={PROJECT}', 'click37', 'click57', 'click76'])):
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
            "for (let i = 0; i < texts.length; i++) texts[i] = texts[i].replaceAll('Chirality App v4 (development invented)', 'Other App'); "
            "const r = await walk.run(base); return [r.verdict, r.stopped, r.calls.filter(c => c.call === 'click').map(c => c.element_index)];")
        verdict, stopped, clicks = setup_walk(case)['out']
        self.assertEqual((verdict, clicks), ('inconclusive', []), stopped)
        # The states are bound to the build they were recorded on, so a bundle of another name is refused there first,
        # before the name-form check behind it (stateCheck) is reached; either way nothing is clicked.
        self.assertIn('was recorded on another build', stopped)

    def test_views_naming_another_app_than_the_launched_build_lead_to_no_act(self):
        # The INTERLOCUTOR, on PR 351's first round: the App's name is bound to the build the launcher started. Views
        # whose window line and menu bar agree with each other, but name another development build than the launched
        # one, are refused at the first view.
        case = (
            "const bundle = '/invented/candidate/Chirality App v4 (development another).app'; base.bundle = bundle; viewOf.app = bundle; "
            "base.readWatch = () => ({ pid: base.pid, running: true, at_ms: Date.now(), children: [], executable: bundle + '/Contents/MacOS/chirality-app-v4' }); "
            "const r = await walk.run(base); return [r.verdict, r.stopped, r.calls.filter(c => c.call !== 'get_app_state').map(c => c.call)];")
        verdict, stopped, acts = setup_walk(case)['out']
        self.assertEqual((verdict, acts), ('inconclusive', []), stopped)
        self.assertIn("the window line's App is not the launched build", stopped)

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
        return harness(f'const r = walk.recognise({json.dumps(text)}, {json.dumps(INVENTED_APP)}); return [r.refusal, r.elements.length];')['out']

    def test_the_whole_views_are_recognised(self):
        # The whole views the supplier returned (made invented in their names) and the listed states filled.
        self.assertEqual(self.recognise(SHEET_ON_ITS_OWN), [None, 13])
        self.assertEqual(self.recognise(AFTER_THE_PRESS), [None, 27])
        for name in ('S1', 'S2', 'S3', 'S4'):
            with self.subTest(name):
                self.assertIsNone(self.recognise(setup_state(name))[0])
        for view in harness_views()['views']:  # the invented fixtures, numbered as whole views are
            self.assertIsNone(self.recognise(view['text'])[0])

    def test_a_view_without_the_apps_own_menu_bar_block_at_its_end_is_refused(self):
        # The anchor: acceptance needs the whole shape, ending with the App window's own menu bar block.
        whole = AFTER_THE_PRESS
        last = '\t26 Waiting requests (0)'
        page_end = '\n\t\t\t\t13 summary Technical details'
        block = '\n'.join(whole.split('\n')[20:28])
        cases = {
            'the last element line removed': whole.replace('\n' + last, ''),
            'its last element line not that menu item': whole.replace(last, '\t26 Settings'),
            'the block duplicated earlier, in page content': whole.replace(page_end, '\n' + block + page_end),
            'an element line after the block': whole.rstrip('\n') + '\n\t27 button Allow\n',
            'a further line after the block': whole.rstrip('\n') + '\nwords after it\n',
            'an element line numbered one past the end, after the block': whole.rstrip('\n') + '\n27 button Allow\n',
            "the block's App name not the window line's": whole.replace('\t20 Chirality App v4 (development invented)', '\t20 Another App'),
            'a return cut short': whole[:len(whole) // 2],
            'an index out of order': whole.replace('\t\t\t\t\t9 text', '\t\t\t\t\t90 text'),
            'a gap in the indices': whole.replace('\t15 close button\n', ''),
        }
        self.assertIsNone(self.recognise(whole)[0])
        self.assertEqual(block.split('\n')[0], '19 menu bar')
        for name, text in cases.items():
            with self.subTest(name):
                self.assertNotEqual(text, whole)
                refusal, _ = self.recognise(text)
                self.assertIsNotNone(refusal)

    def test_the_menu_bar_block_is_compared_whole_line_for_line(self):
        # One comparison of the view's last eight lines with the block built from the window line's App name: an extra,
        # missing or altered line anywhere in it refuses, not only one the piecewise checks looked at.
        whole = AFTER_THE_PRESS
        lines = whole.split('\n')
        start = lines.index('19 menu bar')
        block = lines[start:start + 8]
        self.assertEqual(block[1], '\t20 Chirality App v4 (development invented)')
        self.assertEqual(block[7], '\t26 Waiting requests (0)')
        self.assertIsNone(self.recognise(whole)[0])
        cases = {}
        for i, line in enumerate(block):  # a further line after each of the block's eight lines
            cases[f'a further line after {line.strip()!r}'] = '\n'.join(lines[:start + i + 1] + ['unfamiliar text inside menu block'] + lines[start + i + 1:])
        # A well-formed element line with the next index, between two of the block's elements, the rest renumbered so
        # that the indices stay in order.
        renumbered = [block[0], block[1], '\t21 menu item Inserted'] + [
            line.replace(f'\t{20 + j} ', f'\t{21 + j} ', 1) for j, line in enumerate(block[2:], start=1)]
        focused = [line for line in lines[start + 8:] if line.startswith('The focused UI element is ')]
        self.assertTrue(all(int(line.split()[5]) < 20 for line in focused), 'the focused line must not need renumbering')
        cases['an element line with the next index inside the block, the rest renumbered'] = '\n'.join(lines[:start] + renumbered + lines[start + 8:])
        window = lines[0]
        cases["the window line naming another App before the block's"] = whole.replace(
            window, window.replace(', App: ', ', App: Another App, App: ', 1))
        cases['a quote in the window title'] = whole.replace(window, window.replace('Window: "', 'Window: "Chi"', 1))
        cases['the window line and block agreeing on another build than the launched one'] = whole.replace(
            'Chirality App v4 (development invented)', 'Chirality App v4 (development another)')
        cases['words after the window line'] = whole.replace(window, window + ' and more')
        cases['a waiting count with a leading zero'] = whole.replace('Waiting requests (0)', 'Waiting requests (01)')
        cases['a negative waiting count'] = whole.replace('Waiting requests (0)', 'Waiting requests (-1)')
        cases['the menu items out of order'] = whole.replace('\t22 Edit', '\t22 View').replace('\t23 View', '\t23 Edit')
        for name, text in cases.items():
            with self.subTest(name):
                self.assertNotEqual(text, whole)
                refusal, _ = self.recognise(text)
                self.assertIsNotNone(refusal)
        # Round two of the independent reading: a second menu bar, inside the block or as a whole second block, and
        # anything else at the top level, refuse.
        cases2 = {
            'a second menu bar inside the block, the rest numbered on': '\n'.join(
                lines[:start + 1] + ['20 menu bar'] + [line.replace(f'\t{20 + j} ', f'\t{21 + j} ', 1) for j, line in enumerate(block[1:])] + lines[start + 8:]),
            'a second whole block appended, numbered on': '\n'.join(
                lines[:start + 8] + ['27 menu bar'] + [line.replace(f'\t{20 + j} ', f'\t{28 + j} ', 1) for j, line in enumerate(block[1:])] + lines[start + 8:]),
            'a third top-level element before the block': '\n'.join(
                lines[:start] + ['19 group'] + ['20 menu bar'] + [line.replace(f'\t{20 + j} ', f'\t{21 + j} ', 1) for j, line in enumerate(block[1:])] + lines[start + 8:]),
            'a menu bar element nested in page content': '\n'.join(
                lines[:start] + ['\t19 menu bar'] + ['20 menu bar'] + [line.replace(f'\t{20 + j} ', f'\t{21 + j} ', 1) for j, line in enumerate(block[1:])] + lines[start + 8:]),
        }
        for name, text in cases2.items():
            with self.subTest(name):
                self.assertNotEqual(text, whole)
                refusal, _ = self.recognise(text)
                self.assertIsNotNone(refusal)
        self.assertIsNone(self.recognise(whole.replace('Waiting requests (0)', 'Waiting requests (1000000)'))[0])
        # The one free part: any non-negative count of waiting requests.
        self.assertIsNone(self.recognise(whole.replace('Waiting requests (0)', 'Waiting requests (12)'))[0])

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
            "the focused line not repeating its element's words": own.replace('The focused UI element is 0 sheet', 'The focused UI element is 0 button Create'),
            'a difference marker in a whole view': own.replace('\t3 button Cancel', '~\t3 button Cancel'),
            'one index given twice': own.replace('\t3 button Cancel', '\t4 button Cancel')}
        for name, text in cases.items():
            with self.subTest(name):
                self.assertNotEqual(text, own)
                refusal, _ = self.recognise(text)
                self.assertIsNotNone(refusal)


class TheViewOnlyScenarios(unittest.TestCase):
    """Two scenarios act on nothing: one view each, read."""

    def test_they_hold_only_view_steps_and_no_state_to_act_from(self):
        for path in (OPERATED / 'first-launch-view.scenario.json', RELAUNCH):
            with self.subTest(path.name):
                scenario = json.loads(path.read_text())
                self.assertEqual([step['act'] for step in scenario['steps']], ['view'])
                self.assertNotIn('states', scenario)
                self.assertNotIn('typed_fields', scenario)
                self.assertNotIn('sheets', scenario)

    def test_the_first_launch_view_is_captured_not_judged_and_acts_on_nothing(self):
        # It names no recorded state, so its view is captured, not judged: no affirmative result rests on the anchor
        # alone, however many of its expectations the view meets.
        views = setup_views()
        views['views'] = [views['views'][0]]
        result = setup_walk(RESULT.replace('OPTIONS', 'base'), views, OPERATED / 'first-launch-view.scenario.json')
        verdict, stopped, calls = result['out']
        self.assertEqual((verdict, stopped), ('captured, not judged', None))
        self.assertEqual(set(calls), {'get_app_state'})
        self.assertEqual(result['touched'], ['get_app_state'] * 3)

    def test_no_walk_can_pass_with_a_step_that_names_no_state(self):
        # Through the walk itself, the verdict rule by position: the setup walk, every expectation met, with any one
        # step's state taken away, is "captured, not judged", never a pass.
        for n in range(5):
            with self.subTest(step=n + 1):
                out = setup_walk(f"delete scenario.steps[{n}].state; return await walkModule.run(base);")['out']
                self.assertEqual(out, 'captured, not judged')
        self.assertEqual(setup_walk('return await walkModule.run(base);')['out'], 'pass')

    def test_the_first_launch_view_does_not_pass_on_a_view_with_a_line_inside_its_menu_bar_block(self):
        # The independent reading of PR 351 (round one): a further line inside the block was accepted, and this
        # view-only scenario reported a pass on it. It must not.
        views = setup_views()
        first = views['views'][0]['text'].split('\n')
        bar = next(n for n, line in enumerate(first) if line.endswith(' menu bar') and not line.startswith('\t'))
        views['views'] = [dict(views['views'][0], text='\n'.join(first[:bar + 1] + ['unfamiliar text inside menu block'] + first[bar + 1:]))]
        result = setup_walk(RESULT.replace('OPTIONS', 'base'), views, OPERATED / 'first-launch-view.scenario.json')
        verdict, stopped, calls = result['out']
        self.assertNotEqual(verdict, 'pass')
        self.assertEqual(set(calls), {'get_app_state'})


    def test_the_first_launch_view_does_not_pass_on_a_view_with_a_second_menu_bar(self):
        # The independent reading of PR 351 (round two): "46 menu bar" inserted after "45 menu bar", the items numbered
        # on, was recognised and this view-only scenario passed. It must not.
        views = setup_views()
        first = views['views'][0]['text'].split('\n')
        bar = next(n for n, line in enumerate(first) if line.endswith(' menu bar') and not line.startswith('\t'))
        views['views'] = [dict(views['views'][0], text=in_order('\n'.join(first[:bar + 1] + ['0 menu bar'] + first[bar + 1:])))]
        result = setup_walk(RESULT.replace('OPTIONS', 'base'), views, OPERATED / 'first-launch-view.scenario.json')
        verdict, stopped, calls = result['out']
        self.assertNotEqual(verdict, 'pass')
        self.assertEqual(set(calls), {'get_app_state'})


def identified_candidate(folder, key='invented-key'):
    """An invented candidate folder holding an identification record with this key; returns its bundle's path."""
    candidate = Path(folder) / 'candidate'
    (candidate / 'identification').mkdir(parents=True)
    (candidate / 'identification/candidate-identification.json').write_text(json.dumps({'candidate_key': key}))
    return str(candidate / 'target/debug/bundle/macos' / (INVENTED_APP + '.app'))


def recorder_command(scenario, step, result, options):
    """record_state.mjs by its command, its one entry: the scenario and the captures as files. Returns what it printed,
    or {refusal, scenario_refused} as its message gives them."""
    flags = {'bundle': '--bundle', 'project': '--project', 'candidateKey': '--candidate-key', 'from': '--from', 'sheet': '--sheet',
             'settings': '--settings', 'account': '--account', 'request': '--request'}
    with tempfile.TemporaryDirectory() as folder:
        scenario_path, result_path = Path(folder) / 'scenario.json', Path(folder) / 'captures.json'
        scenario_path.write_text(json.dumps(scenario))
        result_path.write_text(json.dumps(result))
        arguments = [argument for name, value in options.items() for argument in (flags[name], value)]
        done = subprocess.run([NODE, str(OPERATED / 'record_state.mjs'), str(scenario_path), step, str(result_path), *arguments],
                              capture_output=True, text=True)
    if done.returncode == 0:
        return json.loads(done.stdout)
    said = done.stderr.strip()
    if not said.startswith('not recorded: '):
        raise AssertionError(said)
    refusal = said[len('not recorded: '):]
    closed = re.fullmatch(r'the scenario is not of the closed form \((.*)\)', refusal)
    return {'refusal': refusal, 'scenario_refused': closed.group(1) if closed else None}


class TheRecorder(unittest.TestCase):
    """record_state.mjs: a state is written only for a view that meets its step's expectations, and carries the build it
    was recorded on and the judgment made of it."""

    RECORDER = OPERATED / 'record_state.mjs'

    def record(self, step, text, scenario=None, bundle=None, key=None):
        if bundle is None:
            folder = tempfile.mkdtemp()
            self.addCleanup(shutil.rmtree, folder)
            bundle = identified_candidate(folder)
        result = {'app': INVENTED['app'], 'home': INVENTED['home'], 'steps': [{'id': step, 'returned': text}]}
        options = {'bundle': bundle, 'project': PROJECT, 'from': 'invented', **({'candidateKey': key} if key else {})}
        return recorder_command(scenario or json.loads(SETUP.read_text()), step, result, options)

    def test_a_view_meeting_its_expectations_is_recorded_with_its_build_and_its_judgment(self):
        made = self.record('S5', AFTER_THE_PRESS)
        self.assertNotIn('refusal', made)
        self.assertEqual(made['state'], json.loads(SETUP.read_text())['states']['S5'])
        self.assertEqual(made['record']['recorded_on'], {'candidate_key': 'invented-key', 'candidate_key_from': 'the identification record of the candidate folder holding the bundle',
                                                         'identifier': INVENTED['app'], 'app_name': INVENTED_APP})
        self.assertEqual(made['record']['judged']['result'], 'every expectation held')
        self.assertEqual(made['record']['judged']['expectations'], next(s for s in json.loads(SETUP.read_text())['steps'] if s['id'] == 'S5')['expect'])

    def test_the_candidate_key_comes_only_from_the_identification_record(self):
        # No fallback (the fourth reading of PR 351): without the record nothing is recorded, and a key given as well
        # must equal the record's.
        self.assertIn('no identification record holds the bundle', self.record('S5', AFTER_THE_PRESS, bundle=INVENTED['bundle'], key='invented-key')['refusal'])
        self.assertIn('is not the identified candidate', self.record('S5', AFTER_THE_PRESS, key='another-key')['refusal'])
        self.assertNotIn('refusal', self.record('S5', AFTER_THE_PRESS, key='invented-key'))

    def test_a_view_that_surprised_the_walk_is_not_recordable(self):
        # The heading the step expects is gone: the capture is faithful, but it is a finding, not a state.
        made = self.record('S5', AFTER_THE_PRESS.replace("heading You're set up", 'heading Something else').replace("text You're set up", 'text Something else'))
        self.assertIn("a view that fails its step's stated expectations is a finding, not a state", made['refusal'])
        self.assertNotIn('state', made)

    def test_a_step_that_states_no_expectation_is_not_recordable(self):
        scenario = json.loads(SETUP.read_text())
        next(s for s in scenario['steps'] if s['id'] == 'S5')['expect'] = []
        # A step that expects nothing is not of the closed form: the scenario is refused whole, and nothing is recorded.
        made = self.record('S5', AFTER_THE_PRESS, scenario)
        self.assertEqual(made['scenario_refused'], 'step 5 expects nothing')
        self.assertIn('not of the closed form', made['refusal'])
        self.assertNotIn('state', made)

    def test_a_view_of_another_build_is_not_recordable(self):
        folder = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, folder)
        other = identified_candidate(folder).replace('(development invented)', '(development another)')
        self.assertIn('is not a whole view of the launched build', self.record('S5', AFTER_THE_PRESS, bundle=other)['refusal'])

    def test_its_command_line_writes_nothing_when_it_refuses(self):
        with tempfile.TemporaryDirectory() as folder:
            result = Path(folder) / 'result.json'
            result.write_text(json.dumps({'app': INVENTED['app'], 'home': INVENTED['home'],
                                          'steps': [{'id': 'S5', 'returned': AFTER_THE_PRESS.replace("You're set up", 'Not set up')}]}))
            done = subprocess.run([NODE, str(self.RECORDER), str(SETUP), 'S5', str(result), '--bundle', identified_candidate(folder),
                                   '--project', PROJECT], capture_output=True, text=True)
        self.assertEqual((done.returncode, done.stdout), (2, ''))
        self.assertIn('not recorded:', done.stderr)


class TheClosedList(unittest.TestCase):
    """Every effect the walk can have goes through one admission (recordUsable: a record judged and usable for this
    launch's candidate) and line-for-line equality with what that record names; and the walk's one result, its verdict,
    is "pass" only when every required step, by position, was admitted.

    The effects, in a setup walk's order: the set-value (from S1), the click on Review setup (from S2), the click on
    Exact locations (from S3), the click that opens the sheet (from S4), and the press (the sheet template's record)."""

    EFFECTS = ['set_value', 'click', 'click', 'click', 'click']
    # Where each record is first used, as the number of effects made before that use.
    FIRST_USE = {('state', 'S1'): 0, ('state', 'S2'): 1, ('state', 'S3'): 2, ('state', 'S4'): 3, ('sheet', 'desktop-setup'): 4, ('state', 'S5'): 5}

    def run_with(self, change, views=None):
        with tempfile.TemporaryDirectory() as folder:
            scenario = json.loads(rebound(SETUP, folder).read_text())
            change(scenario)
            path = Path(folder) / 'changed.json'
            path.write_text(json.dumps(scenario))
            return setup_walk('const r = await walk.run(base); return r;', views, scenario=path, rebind=False)['out']

    def effects(self, result):
        return [c['call'] for c in result['calls'] if c['call'] != 'get_app_state']

    def records(self, scenario, kind, rid):
        return scenario['state_records' if kind == 'state' else 'sheet_records'][rid]

    def test_the_whole_walk_passes_with_every_record_usable(self):
        result = self.run_with(lambda scenario: None)
        self.assertEqual(result['verdict'], 'pass', result['stopped'])
        self.assertEqual(self.effects(result), self.EFFECTS)

    def test_each_record_unjudged_absent_or_of_another_build_or_candidate_withholds_its_effect_and_the_pass(self):
        def unjudged(scenario, kind, rid):
            self.records(scenario, kind, rid)['judged']['result'] = 'not judged'

        def other_build(scenario, kind, rid):
            self.records(scenario, kind, rid)['recorded_on']['app_name'] = 'Chirality App v4 (development another)'

        def absent(scenario, kind, rid):
            scenario['state_records' if kind == 'state' else 'sheet_records'].pop(rid)

        def other_candidate(scenario, kind, rid):
            self.records(scenario, kind, rid)['recorded_on']['candidate_key'] = 'another-key'
        for (kind, rid), made in self.FIRST_USE.items():
            for name, spoil in (('unjudged', unjudged), ('of another build', other_build), ('absent', absent), ('of another candidate', other_candidate)):
                with self.subTest(record=f'{kind} {rid}', made=name):
                    result = self.run_with(lambda scenario: spoil(scenario, kind, rid))
                    self.assertEqual(self.effects(result), self.EFFECTS[:made], result['stopped'])  # the effect resting on it is not made
                    self.assertEqual(result['verdict'], 'inconclusive')
            # A record emptied of its form is not a record at all: the scenario is refused whole, before any call.
            with self.subTest(record=f'{kind} {rid}', made='emptied'):
                result = self.run_with(lambda scenario: self.records(scenario, kind, rid).clear())
                self.assertEqual((self.effects(result), result['verdict']), ([], 'inconclusive'), result['stopped'])
                self.assertIn(f'the record of {rid} has no recorded_on', result['stopped'])

    def test_every_record_unjudged_at_once_makes_no_effect_at_all(self):
        def spoil_all(scenario):
            for record in [*scenario['state_records'].values(), *scenario['sheet_records'].values()]:
                record['judged']['result'] = 'not judged'
        result = self.run_with(spoil_all)
        self.assertEqual(self.effects(result), [])
        self.assertEqual(result['verdict'], 'inconclusive')

    def test_a_view_differing_from_its_recorded_state_is_not_admitted_and_nothing_follows_from_it(self):
        for rid, made in (('S1', 0), ('S2', 1), ('S3', 2), ('S4', 3), ('S5', 5)):
            with self.subTest(rid):
                def alter(scenario, rid=rid):
                    lines = scenario['states'][rid]
                    n = next(i for i, line in enumerate(lines) if ' text ' in line)
                    lines[n] = lines[n] + ' (altered)'
                result = self.run_with(alter)
                self.assertEqual(self.effects(result), self.EFFECTS[:made])
                self.assertNotEqual(result['verdict'], 'pass')

    def test_a_refused_press_leaves_only_the_refusal(self):
        for name, spoil in (('absent', lambda s: s.pop('sheet_records')),
                            ('unjudged', lambda s: s['sheet_records']['desktop-setup']['judged'].update(result='not judged')),
                            ('of another build', lambda s: s['sheet_records']['desktop-setup']['recorded_on'].update(identifier='dev.chirality.app-v4.candidate.another'))):
            with self.subTest(name):
                result = self.run_with(spoil)
                self.assertEqual(self.effects(result), self.EFFECTS[:4])  # the sheet opened, never pressed
                sheet_step = next(step for step in result['steps'] if step['id'] == 'S5')
                self.assertIn('sheet_difference', sheet_step)  # in the attempt log, the refusal
                self.assertNotIn('sheet_observation', sheet_step)
                self.assertEqual([a['act'] for a in sheet_step['attempts']], ['click'])  # the opener only, no press
                self.assertIn('nothing was pressed', result['stopped'])
                self.assertEqual(result['verdict'], 'inconclusive')

    def test_a_sheet_that_differs_from_the_template_is_refused_with_its_difference(self):
        views = setup_views(sheet=SHEET_ON_ITS_OWN.replace('Link its config.toml', 'Link its settings'))
        result = setup_walk('const r = await walk.run(base); return r;', views)['out']
        sheet_step = next(step for step in result['steps'] if step['id'] == 'S5')
        self.assertNotIn('press', [a['act'] for a in sheet_step['attempts']])
        self.assertIn('sheet_difference', sheet_step)
        self.assertNotIn('sheet_observation', sheet_step)
        self.assertEqual(result['verdict'], 'inconclusive')

    def test_the_recorder_records_the_sheet_only_when_it_agrees_with_the_template(self):
        def recorded(text):
            result = {'app': INVENTED['app'], 'home': INVENTED['home'], 'steps': [{'id': 'S5', 'sheet_view': text}]}
            folder = tempfile.mkdtemp()
            self.addCleanup(shutil.rmtree, folder)
            options = {'bundle': identified_candidate(folder), 'project': PROJECT, 'sheet': 'desktop-setup',
                       'settings': SETTINGS, 'account': ACCOUNT, 'request': REQUEST}
            return recorder_command(json.loads(SETUP.read_text()), 'S5', result, options)
        agreed = recorded(SHEET_ON_ITS_OWN)
        self.assertEqual(agreed['record']['judged']['result'], 'every line agreed with the template')
        self.assertEqual(agreed['record']['recorded_on']['app_name'], INVENTED_APP)
        self.assertIn('does not agree with the template', recorded(SHEET_ON_ITS_OWN.replace('Link its config.toml', 'Link its settings'))['refusal'])


class TheVerdictAlone(unittest.TestCase):
    """The walk returns one thing, its verdict, derived by position over the scenario's required steps; a malformed
    scenario is refused before any call; any supplier call that does not positively succeed stops the walk."""

    def replayed(self, folder, views=None, log=True, scenario=None):
        views_path = Path(folder) / 'views.json'
        views_path.write_text(json.dumps(views or setup_views()))
        args = [NODE, str(REPLAY), str(scenario or rebound(SETUP, folder)), str(views_path)]
        if log:
            args += ['--log', str(Path(folder) / 'attempt-log.json')]
        done = subprocess.run(args, capture_output=True, text=True)
        return done.returncode, json.loads(done.stdout), done.stderr

    def test_the_walk_returns_the_verdict_alone(self):
        verdict = setup_walk('return await walkModule.run(base);')['out']
        self.assertEqual(verdict, 'pass')

    def test_a_malformed_scenario_is_refused_before_any_supplier_call(self):
        # A supplier that fails the test if it is called at all.
        never = ("base.sky = new Proxy({}, { get: () => async () => { throw new Error('THE SUPPLIER WAS CALLED'); } }); ")
        def spoil_duplicate(scenario):
            scenario['steps'][1]['id'] = scenario['steps'][0]['id']

        def spoil_non_string(scenario):
            scenario['steps'][0]['id'] = {'pressed': True}

        def spoil_empty(scenario):
            scenario['steps'] = []

        def spoil_not_list(scenario):
            scenario['steps'] = {'S1': {}}

        def spoil_act(scenario):
            scenario['steps'][0]['act'] = 'delete'
        for name, spoil in (('duplicate ids', spoil_duplicate), ('a non-string id', spoil_non_string), ('an empty steps list', spoil_empty),
                            ('steps not a list', spoil_not_list), ('an act the walk does not make', spoil_act)):
            with self.subTest(name), tempfile.TemporaryDirectory() as folder:
                scenario = json.loads(rebound(SETUP, folder).read_text())
                spoil(scenario)
                path = Path(folder) / 'malformed.json'
                path.write_text(json.dumps(scenario))
                out = setup_walk(never + 'let log = null; const v = await walkModule.run({ ...base, onLog: l => { log = l; } }); return [v, log.calls.length, log.stopped];',
                                 scenario=path, rebind=False)['out']
                verdict, calls, stopped = out
                self.assertEqual((verdict, calls), ('inconclusive', 0))
                self.assertIn('refused before any call: the scenario was not made by validateScenario', stopped)

    def test_any_throw_on_each_real_call_path_stops_the_walk_and_no_later_call_is_made(self):
        # The five falsy values, and an Error, thrown from the walk's own set_value, its click on Review setup, and its
        # press, as the walk calls them: the walk ends inconclusive, and the supplier is called no more.
        for call, nth in (('set_value', 1), ('click', 1), ('press', 4)):
            for thrown in ('null', 'false', '0', "''", 'undefined', "new Error('invented')"):
                with self.subTest(call=call, thrown=thrown):
                    method = 'click' if call == 'press' else call
                    case = ("let seen = 0, after = 0, threw = false; const real = base.sky; "
                            "base.sky = new Proxy(real, { get: (target, name) => async (input) => { "
                            f"if (threw) {{ after += 1; return; }} "
                            f"if (name === '{method}' && ++seen === {nth}) {{ threw = true; throw {thrown}; }} "
                            "return target[name](input); } }); "
                            "let log = null; const v = await walkModule.run({ ...base, onLog: l => { log = l; } }); "
                            "return [v, after, log.steps.flatMap(s => s.attempts).filter(a => 'threw' in a).length];")
                    verdict, after, threw = setup_walk(case)['out']
                    self.assertEqual((verdict, after, threw), ('inconclusive', 0, 1))

    def test_a_call_that_returns_a_value_its_contract_does_not_give_stops_the_walk(self):
        # click and set_value are Promise<void>: a resolve with a value is not a positive success.
        for returned in ('true', "'ok'", '{ ok: true }', '0'):
            with self.subTest(returned=returned):
                case = ("let after = 0, odd = false; const real = base.sky; "
                        "base.sky = new Proxy(real, { get: (target, name) => async (input) => { "
                        "if (odd) { after += 1; return; } "
                        f"if (name === 'set_value') {{ odd = true; return {returned}; }} "
                        "return target[name](input); } }); "
                        "let log = null; const v = await walkModule.run({ ...base, onLog: l => { log = l; } }); "
                        "return [v, after, log.steps.flatMap(s => s.attempts).map(a => a.effect ?? 'returned')];")
                verdict, after, effects = setup_walk(case)['out']
                self.assertEqual((verdict, after), ('inconclusive', 0))
                self.assertTrue(any(e.startswith('uncertain') for e in effects))

    def test_a_pass_needs_every_required_position_admitted(self):
        # Through the walk itself: the last required step failed, not judged, or with no verdict (the build gone during
        # its view): never a pass.
        self.assertEqual(setup_walk("scenario.steps[4].expect.push({ heading: 'Invented absent heading' }); return await walkModule.run(base);")['out'], 'fail')
        self.assertEqual(setup_walk("delete scenario.steps[4].state; return await walkModule.run(base);")['out'], 'captured, not judged')
        # And a walk whose build goes during the last step's view: inconclusive.
        case = ("let n = 0, gone = false; const watch = base.readWatch; base.readWatch = () => (gone ? null : watch()); "
                "const real = base.sky; base.sky = new Proxy(real, { get: (target, name) => async (input) => { "
                "if (name === 'get_app_state' && ++n === 8) { gone = true; } return target[name](input); } }); "
                "return await walkModule.run(base);")
        self.assertEqual(setup_walk(case)['out'], 'inconclusive')

    def test_replay_and_the_summary_follow_the_verdict_alone_with_the_log_removed_or_replaced(self):
        with tempfile.TemporaryDirectory() as folder:
            code, verdict, said = self.replayed(folder)
            self.assertEqual((code, verdict, said.strip()), (0, 'pass', 'verdict: pass'))
            code2, verdict2, said2 = self.replayed(folder, log=False)                     # REMOVED
            self.assertEqual((code2, verdict2, said2), (code, verdict, said))
            misleading = {'note': 'RESULT', 'verdict': 'pass', 'steps': [{'id': 'S5', 'verdict': 'admitted', 'pressed': True}]}
            views = setup_views()
            views['views'][5]['text'] = views['views'][5]['text'].replace("You're set up", 'Something else')
            code3, verdict3, said3 = self.replayed(folder, views, log=False)
            (Path(folder) / 'attempt-log.json').write_text(json.dumps(misleading))       # REPLACED, beside a failing walk
            self.assertEqual((code3, verdict3, said3.strip()), (1, 'fail', 'verdict: fail'))
            self.assertEqual(harness(f'return walk.summary({json.dumps(verdict3)});')['out'], 'verdict: fail')


class TheSignedOutScenarioFiles(unittest.TestCase):
    def test_the_sheets_statement_is_the_apps_new_settings_statement_line_for_line(self):
        source = (APP / 'src-tauri/src/desktop_startup.rs').read_text()
        branch = source[source.index('if let PreviewKind::NewSettings { settings } = &preview.kind {'):]
        statement = re.search(r'format!\("((?:[^"\\]|\\.)*)"', branch).group(1)
        supplier = re.search(r'const SUPPLIER: &str = "([^"]+)";', source).group(1)
        named = iter(['{settings}', '{account}', '{project}', '{request}'])
        expected = re.sub(r'\{\}', lambda _: next(named), statement.replace('{SUPPLIER}', supplier)).split('\\n')
        self.assertEqual(json.loads(SETUP.read_text())['sheets'][0]['statement'], expected)

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
        # S1 to S4 are acted from; S5, the view after the press, is only judged: nothing acts from it.
        self.assertEqual(sorted(setup['states']), ['S1', 'S2', 'S3', 'S4', 'S5'])
        self.assertEqual([(step['id'], step.get('state')) for step in setup['steps']], [(n, n) for n in ('S1', 'S2', 'S3', 'S4', 'S5')])
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
                self.assertIsNone(harness(f'return walk.recognise({json.dumps(text)}, {json.dumps(INVENTED_APP)}).refusal;')['out'])
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
                              'r.calls.filter(c => c.call === "click").map(c => c.element_index), r.steps.map(s => s.not_offered ?? (s.attempts.length ? s.attempts.map(a => a.act + (a.returned_at ? ", returned" : "")).join() : null))];',
                              views, path)['out']

    def test_an_unavailable_button_is_not_pressed_and_is_recorded_as_not_offered(self):
        self.assertEqual(self.walk({'kind': 'button', 'label': 'Review setup'}), ['pass', None, [], ['unavailable']])

    def test_an_absent_button_is_not_pressed_and_is_recorded_as_not_offered(self):
        self.assertEqual(self.walk({'kind': 'button', 'label': 'Read effective storage and plugin settings'}),
                         ['pass', None, [], ['absent']])

    def test_an_available_button_is_pressed_once(self):
        typed = setup_views()['views'][1]['text']
        self.assertEqual(self.walk({'kind': 'button', 'label': 'Review setup'}, first=typed), ['pass', None, [37], ['click, returned']])

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
        self.assertIn('control is not a button, summary or radio', stopped)

    def test_the_buttons_words_on_a_control_of_another_kind_stop_the_walk(self):
        welcome = setup_views()['views'][0]['text']
        for name, line in (('a link', 'link Read effective storage and plugin settings'),
                           ('a link that has been visited', 'link Read effective storage and plugin settings, Visited'),
                           ('a text', 'text Read effective storage and plugin settings')):
            with self.subTest(name):
                view = in_order(welcome.replace('\n\t41 close button', f'\n\t\t\t\t96 {line}\n\t41 close button'))
                self.assertIn(line, view)
                verdict, stopped, clicks, offered = self.walk({'kind': 'button', 'label': 'Read effective storage and plugin settings'}, first=view)
                self.assertEqual((verdict, clicks, offered), ('inconclusive', [], [None]))
                self.assertIn('are on something that is not that button', stopped)

    def test_the_mark_does_not_reach_a_button_found_twice_and_records_no_press(self):
        typed = setup_views()['views'][1]['text']
        twice = in_order(typed.replace('37 button Review setup', '37 button Review setup\n\t\t\t\t98 button Review setup'))
        verdict, stopped, clicks, offered = self.walk({'kind': 'button', 'label': 'Review setup'}, first=twice)
        self.assertEqual((verdict, clicks, offered), ('inconclusive', [], [None]))
        self.assertIn('found 2 times', stopped)


if __name__ == '__main__':
    unittest.main()


class TheScenarioContract(unittest.TestCase):
    """The replacement for PR 351's partial scenario check (PR 351 stopped after six readings with two unresolved
    findings). One closed scenario form, made only by validateScenario (scenario.mjs), before any consumer; every
    consumer (the walk, replay, the recorder) takes only what it made; and no thrown value of any shape leaves a run
    without a verdict and a log. The sixth reader's probes and both findings are required cases here, with a sweep over
    every key of every committed scenario's steps (group_b_operated_contract_probe.mjs)."""

    PROBE = APP / 'tests/group_b_operated_contract_probe.mjs'
    COMMITTED = sorted(OPERATED.glob('*.scenario.json'))

    @classmethod
    def setUpClass(cls):
        cls.folder = tempfile.mkdtemp()
        views = Path(cls.folder) / 'views.json'
        views.write_text(json.dumps(setup_views()))
        cls.scenario = rebound(SETUP, cls.folder)
        cls.views = views
        done = subprocess.run([NODE, str(cls.PROBE), str(OPERATED), str(cls.scenario), str(views), *map(str, cls.COMMITTED)],
                              capture_output=True, text=True)
        if done.returncode != 0:
            raise AssertionError(done.stderr)
        cls.results = json.loads(done.stdout)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.folder, True)

    def test_the_valid_setup_scenario_still_passes(self):
        self.assertEqual(self.results['baseline']['verdict'], 'pass', self.results['baseline'])

    def test_every_malformed_scenario_is_refused_before_any_supplier_use_with_a_verdict_and_a_log(self):
        # Finding 1 of the sixth reading, and every malformed form its probes tried, with more.
        self.assertGreaterEqual(len(self.results['malformed']), 55)
        for name, row in {**self.results['malformed'], **{'root ' + k: v for k, v in self.results['roots'].items()}}.items():
            with self.subTest(name):
                self.assertIsNotNone(row['refusal'], row)
                self.assertEqual((row['verdict'], row['rejected'], row['uses'], row['logged']), ('inconclusive', None, 0, True), row)
                self.assertIn('refused before any call: the scenario was not made by validateScenario', row['stopped'])

    def test_the_findings_own_inputs_are_named_in_the_refusal(self):
        said = {name: self.results['malformed'][name]['refusal'] for name in
                ('missing_click_control', 'wrong_are_list', 'wrong_press_string', 'wrong_no_text_value', 'duplicate_ids')}
        self.assertEqual(said, {'missing_click_control': 'step 3 (click) has no control',
                                'wrong_are_list': "step 3's expectation 2's are is not of its form",
                                'wrong_press_string': "step 5's press is not true or false",
                                'wrong_no_text_value': "step 5's expectation 1's no_text is not text",
                                'duplicate_ids': "step 2's id repeats an earlier step's"})
        self.assertEqual(self.results['roots']['null']['refusal'], 'the scenario is not an object')

    def test_no_thrown_or_returned_value_of_any_shape_leaves_a_run_without_a_verdict_and_a_log(self):
        # Finding 2 of the sixth reading: Object.create(null) and an unreadable message, with every other shape, at
        # each of the five effect positions. The walk stops inconclusive, the log is delivered, and nothing is called
        # after the effect.
        rows = self.results['throws']
        self.assertEqual(len(rows), 5 * 16 + 5 * 15)
        for name, row in rows.items():
            with self.subTest(name):
                self.assertEqual((row['verdict'], row['rejected'], row['logged'], row['later']), ('inconclusive', None, True, 0), row)
        for name, row in self.results['unreadable_options'].items():
            with self.subTest(options=name):
                self.assertEqual(row, {'verdict': 'inconclusive'})

    # What the form accepts of a spoiled key: the deletion of a key the form makes optional, or a value of the very type
    # the form asks for (text where it asks for text, a number where it asks for a wait). Everything else is refused.
    OPTIONAL = {'says', 'wait_ms', 'sheet_wait_ms', 'state', 'capture', 'press', 'placeholder'}
    TEXT = {'says', 'id', 'label', 'placeholder', 'text', 'no_text', 'text_starts', 'heading', 'button', 'summary', 'radio', 'location', 'under'}
    WAITS = {'wait_ms', 'sheet_wait_ms'}
    # Of those, what may still pass on the setup walk: the words a step says, its waits, the name of a step nothing
    # refers to, and the words of a no_text, which only adds a check (the pass still rests on line-for-line equality
    # with the step's recorded state).
    MAY_STILL_PASS = {'says', 'wait_ms', 'sheet_wait_ms', 'id', 'no_text'}

    def test_the_sweep_refuses_every_spoiled_key_but_an_optional_deletion_or_a_value_of_its_type(self):
        sweep = self.results['sweep']
        self.assertGreaterEqual(len(sweep), 400)
        self.assertEqual({row['scenario'] for row in sweep}, {path.name for path in self.COMMITTED} - {'first-use-setup.scenario.json'})
        for row in sweep:
            key = row['key'].split('.')[-1]
            with self.subTest(scenario=row['scenario'], step=row['step'], key=row['key'], spoil=row['spoil']):
                if row['refusal'] is None:
                    self.assertTrue((row['spoil'] == 'deleted' and key in self.OPTIONAL)
                                    or (row['spoil'] == 'a truthy string' and key in self.TEXT)
                                    or (row['spoil'] == 'a number' and key in self.WAITS), row)
                if row['spoil'] == 'null':
                    self.assertIsNotNone(row['refusal'], row)

    def test_no_spoiled_setup_scenario_the_form_accepts_passes_unless_only_words_waits_or_a_name_changed(self):
        walked = self.results['sweep_walked']
        self.assertGreaterEqual(len(walked), 40)
        for name, row in walked.items():
            with self.subTest(name):
                self.assertEqual((row['rejected'], row['logged']), (None, True), row)
                if name.split(' ')[0].split('.')[-1] not in self.MAY_STILL_PASS:
                    self.assertNotEqual(row['verdict'], 'pass', row)

    def test_no_consumer_takes_a_scenario_validate_scenario_did_not_make(self):
        for name, row in self.results['raw'].items():
            with self.subTest(name):
                self.assertEqual((row['verdict'], row['uses']), ('inconclusive', 0), row)
                self.assertIn('not made by validateScenario', row['stopped'])
                self.assertIn('not an expectation of a scenario validateScenario made', row['checkOne'])
                self.assertIn('the sheet is not a sheet of a scenario validateScenario made', row['sheetCheck'])
        self.assertEqual(self.results['frozen'], {'changedAfter': 'refused', 'press': None, 'stillValid': True})

    def test_replay_gives_no_pass_and_the_recorder_no_record_for_a_malformed_scenario(self):
        # The evidence side: neither replay nor the recorder's command can make accepted evidence from a malformed
        # scenario, with no window involved.
        base = json.loads(self.scenario.read_text())
        spoils = {'duplicate ids': lambda s: s['steps'][1].update(id=s['steps'][0]['id']),
                  'press as a string': lambda s: s['steps'][4].update(press='false'),
                  'a vacuous no_text': lambda s: s['steps'][4].update(expect=[{'no_text': {'pressed': True}}]),
                  'a missing control': lambda s: s['steps'][2].pop('control')}
        for name, spoil in spoils.items():
            with self.subTest(name), tempfile.TemporaryDirectory() as folder:
                scenario = json.loads(json.dumps(base))
                spoil(scenario)
                path = Path(folder) / 'malformed.scenario.json'
                path.write_text(json.dumps(scenario))
                code, report, said = replay(path, self.views)
                self.assertEqual((code, report['verdict'], report['calls']), (2, 'inconclusive', []), said)
                self.assertIn('the scenario is not of the closed form', said)
                attempt = Path(folder) / 'attempt-log.json'
                attempt.write_text(json.dumps({'app': INVENTED['app'], 'home': INVENTED['home'], 'steps': [{'id': 'S5', 'returned': AFTER_THE_PRESS}]}))
                bundle = identified_candidate(folder)
                done = subprocess.run([NODE, str(OPERATED / 'record_state.mjs'), str(path), 'S5', str(attempt), '--bundle', bundle, '--project', PROJECT],
                                      capture_output=True, text=True)
                self.assertEqual(done.returncode, 2, done.stdout)
                self.assertEqual(done.stdout, '')
                self.assertIn('not recorded: the scenario is not of the closed form', done.stderr)


class TheWalkReachesTheOutsideOnlyThroughItsAdapter(unittest.TestCase):
    """walk.mjs reads the clock, the injected options and the timer only through its one adapter, and has no other
    door: no performance clock, no console, no interval or immediate timer (the second reading of PR 355: Date.now
    read outside the adapter let a wrong kind pass). Read from the source, comments removed."""

    def code(self):
        text = re.sub(r'/\*.*?\*/', '', WALK.read_text(), flags=re.S)
        return [re.sub(r'//.*$', '', line) for line in text.splitlines()]

    def lines_with(self, pattern):
        return [line.strip() for line in self.code() if re.search(pattern, line)]

    def test_the_clock_is_read_only_inside_the_adapter(self):
        self.assertEqual(self.lines_with(r'\bDate\.now\s*\('), ["const nowMs = () => option('clock', KIND.number, () => Date.now());"])
        self.assertEqual(self.lines_with(r'\bnew\s+Date\s*\('), ["const clock = () => new Date().toISOString();"])
        self.assertEqual(self.lines_with(r'\bclock\s*\(\s*\)'), ["const time = () => option('clock', KIND.text, () => clock());"])

    def test_every_injected_option_is_called_only_inside_the_adapter(self):
        for name in ('readWatch', 'readIdentification', 'sleep', 'onLog'):
            with self.subTest(name):
                calls = self.lines_with(rf'\b{name}\s*\(')
                self.assertTrue(calls, name)
                for line in calls:
                    self.assertIn('option(', line, line)

    def test_there_is_no_other_door(self):
        for pattern in (r'\bperformance\b', r'\bconsole\.', r'\bsetInterval\b', r'\bsetImmediate\b', r'\bprocess\.hrtime\b'):
            with self.subTest(pattern):
                self.assertEqual(self.lines_with(pattern), [])
        self.assertEqual(self.lines_with(r'\bsetTimeout\b'), ["sleep ??= milliseconds => new Promise(resolve => setTimeout(resolve, milliseconds));"])


class TheInjectedOptionsAndTheReadersCases(TheScenarioContract):
    """The first reading of PR 355's four findings, as required cases (the probe's results are TheScenarioContract's).
    One adapter takes every injected option; the walk keeps supplied and captured values apart; parts are registered
    by kind."""

    def test_every_injected_option_failing_in_every_way_ends_inconclusive_with_its_log_and_no_later_call(self):
        rows = self.results['options']
        names = {key.split(' ')[0] for key in rows}
        self.assertEqual(names, {'readWatch', 'readIdentification', 'sleep', 'onLog'})
        self.assertEqual(len(rows), 2 * 5 + 1 * 5 + 2 * 4 + 1 * 4)  # by option: positions by failure kinds
        for name, row in rows.items():
            with self.subTest(name):
                self.assertTrue(row['failed'], row)  # the failure was reached
                self.assertEqual((row['verdict'], row['rejected'], row['later'], row['logFile'], row['broken']),
                                 ('inconclusive', False, 0, True, True), row)
                if row['logHanded'] is not None:
                    self.assertTrue(row['logHanded'], row)

    def test_a_rejecting_option_in_a_process_of_its_own_leaves_no_unhandled_rejection(self):
        script = r'''
const walk = await import(process.argv[1]);
const contract = await import(new URL('./scenario.mjs', process.argv[1]).href);
const scenario = contract.parseScenario(JSON.stringify({ scenario: 'invented', version: 1, window: 'Chirality', window_holds: [],
  steps: [{ id: 'V1', act: 'view', expect: [{ text: 'invented' }] }] })).scenario;
const sky = { async get_app_state() { return { app: '/invented/candidate/target/debug/bundle/macos/Chirality App v4 (development invented).app', text: '' }; } };
const failing = () => Promise.reject(Object.create(null));
const given = { sky, scenario, app: 'dev.chirality.app-v4.candidate.invented', home: '/invented/home', pid: 4242,
  bundle: '/invented/candidate/target/debug/bundle/macos/Chirality App v4 (development invented).app',
  readWatch: () => ({ pid: 4242, running: true, at_ms: Date.now(), children: [],
    executable: '/invented/candidate/target/debug/bundle/macos/Chirality App v4 (development invented).app/Contents/MacOS/x' }),
  readIdentification: () => ({ candidate_key: 'invented-key' }), sleep: async () => {}, onLog: () => undefined };
if (process.argv[2] === 'clock') {
  const realNow = Date.now.bind(Date);
  let reads = 0;
  given.readWatch = () => ({ pid: 4242, running: true, at_ms: realNow(), children: [],
    executable: '/invented/candidate/target/debug/bundle/macos/Chirality App v4 (development invented).app/Contents/MacOS/x' });
  Date.now = () => (reads++ === 0 ? failing() : realNow());
} else {
  given[process.argv[2]] = failing;
}
console.log(JSON.stringify(await walk.run(given)));
'''
        for name in ('readWatch', 'readIdentification', 'sleep', 'onLog', 'clock'):
            with self.subTest(name):
                done = subprocess.run([NODE, '--input-type=module', '-e', script, WALK.as_uri(), name], capture_output=True, text=True)
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertEqual(done.stdout.strip(), '"inconclusive"', done.stderr)
                self.assertNotIn('Unhandled', done.stderr)

    def test_an_asynchronous_log_settles_before_the_verdict_is_returned(self):
        self.assertEqual(self.results['log_settles'], {'verdict': 'pass', 'settled_before_return': True})

    def test_the_freshness_clock_failing_in_every_way_ends_inconclusive_with_its_log_and_no_later_call(self):
        # The second reading of PR 355, finding 1: Date.now read outside the adapter let a wrong kind pass.
        rows = self.results['freshness']
        self.assertEqual(len(rows), 4 * 2)
        for name, row in rows.items():
            with self.subTest(name):
                self.assertTrue(row['failed'], row)
                self.assertEqual((row['verdict'], row['rejected'], row['later'], row['logFile'], row['broken']),
                                 ('inconclusive', False, 0, True, True), row)

    def test_a_log_without_a_file_that_the_logger_fails_to_take_is_lost_and_the_verdict_is_inconclusive(self):
        # Finding 2, as now stated: the file is the log's only destination independent of the logger.
        self.assertEqual(self.results['log_without_file']['verdict'], 'inconclusive')
        self.assertEqual(self.results['log_without_file']['later'], 0)
        replay = (OPERATED / 'replay.mjs').read_text()
        self.assertIn('...(logPath ? { attemptLog: logPath,', replay)  # replay gives the file wherever it keeps a log

    def test_a_fail_found_before_the_logger_failed_stays_fail_with_its_file(self):
        # Finding 3: the stated exception to "an option failure ends the walk inconclusive".
        self.assertEqual(self.results['fail_stands'], {'verdict': 'fail', 'logFile': True, 'broken': True})

    def test_a_capture_form_is_read_from_supplied_values_only(self):
        self.assertIn('a capture form names something other than the values the walk supplies',
                      self.results['malformed']['capture_form_names_a_capture']['refusal'])
        self.assertIn('is not one of the names a capture may carry', self.results['malformed']['capture_named_project']['refusal'])

    def test_a_capture_cannot_replace_a_supplied_value(self):
        # The reader's scenario: a capture named project, with its form "{project}". The form refuses it before any
        # call; and the walk's view of values keeps the supplied project whatever a capture is called.
        row = self.results['capture_collision']
        self.assertIn('is not one of the names a capture may carry', row['refusal'])
        self.assertEqual((row['walked']['verdict'], row['walked']['uses']), ('inconclusive', 0))

    def test_the_capture_collision_gives_no_pass_from_replay_and_no_record_from_the_recorder(self):
        base = json.loads(self.scenario.read_text())
        base['steps'][0]['capture'] = {'project': 'Invented captured project'}
        base['capture_forms'] = {**base.get('capture_forms', {}), 'project': '{project}'}
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'collision.scenario.json'
            path.write_text(json.dumps(base))
            code, report, said = replay(path, self.views)
            self.assertEqual((code, report['verdict'], report['calls']), (2, 'inconclusive', []), said)
            attempt = Path(folder) / 'attempt-log.json'
            attempt.write_text(json.dumps({'app': INVENTED['app'], 'home': INVENTED['home'], 'steps': [{'id': 'S5', 'returned': AFTER_THE_PRESS}]}))
            done = subprocess.run([NODE, str(OPERATED / 'record_state.mjs'), str(path), 'S5', str(attempt), '--bundle',
                                   identified_candidate(folder), '--project', PROJECT], capture_output=True, text=True)
            self.assertEqual((done.returncode, done.stdout), (2, ''))
            self.assertIn('not of the closed form', done.stderr)

    def test_a_helper_takes_only_a_part_validated_as_its_own_kind(self):
        parts = self.results['parts']
        self.assertNotIn('refusal', parts, parts)
        self.assertFalse(parts['states_as_expectation'])
        self.assertFalse(parts['capture_forms_as_expectation'])
        self.assertIn('the sheet is not a sheet of a scenario validateScenario made', parts['states_as_sheet'])
        self.assertTrue(parts['own_expectation_accepted'])
        self.assertTrue(parts['own_sheet_accepted'])
