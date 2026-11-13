#!/usr/bin/env python3
"""The operated scenario's walk and checks, replayed on recorded views (DEL-09-02 examination tooling).

Nothing here starts an application or touches a screen: walk.mjs is given a stand-in for the supplier's window
service. The wrong-state files show the unchanged walk and checks rejecting states that are known to be wrong.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

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
const texts = recorded.views.map(view => view.text);
const touched = [];
let next = 0;
const service = new Proxy({}, { get(_, name) {
  if (name === 'then') return undefined;
  touched.push(String(name));
  if (name === 'get_app_state') return async () => ({ text: texts[next++] });
  if (name === 'click') return async () => {};
  throw new Error('a method the walk must never use: ' + String(name));
} });
const watched = (change = {}) => () => ({ pid: process.pid, running: true, at_ms: Date.now(), children: [], ...change });
const base = { sky: service, scenario, app: recorded.app, home: recorded.home, pid: process.pid, readWatch: watched(), sleep: async () => {} };
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
                         ['get_app_state'] + ['click', 'get_app_state'] * 7)
        self.assertEqual({call['app'] for call in report['calls']}, {'dev.chirality.app-v4.candidate.invented'})

    def test_each_known_wrong_state_is_rejected_at_its_step_and_only_there(self):
        wrong = sorted(FIXTURES.glob('wrong.*.json'))
        self.assertEqual(len(wrong), 4)
        for path in wrong:
            with self.subTest(path.name):
                expected = json.loads(path.read_text())
                code, report, said = replay(SCENARIO, VIEWS, path)
                self.assertEqual((code, report['verdict']), (1, 'fail'), said)
                failed = {step['id']: [check['expectation'] for check in step['checks'] if not check['pass']]
                          for step in report['steps'] if any(not check['pass'] for check in step['checks'])}
                self.assertEqual(failed, {step: [expectation] for step, expectation in expected['fails'].items()})
                self.assertEqual({name for name, state in report['outcomes'].items() if state != 'shown'},
                                 {expected['outcome_not_shown']})
                self.assertIn('found:', said)

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
                self.assertTrue(stopped.startswith('refused before any call: '), stopped)

    def test_it_stops_without_a_further_call_when_a_view_holds_something_that_is_not_the_page(self):
        for name, line in (('a sheet', '\\t1 sheet Confirm'), ('a dialog', '\\t1 dialog'), ('an alert', '\\t1 alert Allow?')):
            with self.subTest(name):
                result = harness("texts[2] = texts[2] + '\\n" + line + "'; const r = await walk.run(base); "
                                 'return [r.verdict, r.stopped, r.calls.length];')
                verdict, stopped, calls = result['out']
                self.assertEqual((verdict, calls), ('inconclusive', 5), stopped)  # three views, two clicks, then nothing
                self.assertIn('S3', stopped)
                self.assertIn('no agent answers it', stopped)

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
        self.assertIn('not of the window "Chirality"', result['out'][1])
        self.assertEqual(result['out'][2], 3)
        result = harness('let asked = 0; const r = await walk.run({ ...base, readWatch: () => watched({ running: ++asked < 4 })() }); '
                         'return [r.verdict, r.stopped];')
        self.assertEqual(result['out'][0], 'inconclusive')
        self.assertIn('no longer shows the build running', result['out'][1])

    def test_a_child_process_of_the_app_stops_the_walk_and_fails_it(self):
        child = "[{ pid: 4242, command: '/invented/codex' }]"
        result = harness(f'let asked = 0; const r = await walk.run({{ ...base, readWatch: () => watched({{ children: ++asked > 4 ? {child} : [] }})() }}); '
                         'return [r.verdict, r.stopped, r.calls.length, r.steps.map(s => s.child_processes)];')
        verdict, stopped, calls, counts = result['out']
        self.assertEqual((verdict, calls, counts), ('fail', 3, [0, 1]), stopped)  # seen at the reading after the first click's view; nothing more is called
        self.assertIn('the App has a child process (1), and this scenario starts none', stopped)
        result = harness(f'scenario.starts_no_process = false; return (await walk.run({{ ...base, readWatch: watched({{ children: {child} }}) }})).verdict;')
        self.assertEqual(result['out'], 'pass')  # a scenario that may start a process is not stopped by one

    def test_it_never_clicks_a_control_whose_words_end_with_an_ellipsis_or_one_it_cannot_find_exactly_once(self):
        result = harness("scenario.steps[4] = { id: 'S5', act: 'click', control: { kind: 'button', label: 'Create settings and save for next launch\\u2026' } }; "
                         'const r = await walk.run(base); return [r.verdict, r.stopped, r.calls.filter(c => c.call === "click").length];')
        self.assertEqual(result['out'][0], 'inconclusive')
        self.assertIn('never clicked', result['out'][1])
        self.assertEqual(result['out'][2], 3)  # the three clicks before it, and not this one
        result = harness("scenario.steps[1].control.label = 'Not On The Page'; const r = await walk.run(base); "
                         'return [r.verdict, r.stopped, r.calls.length];')
        self.assertEqual((result['out'][0], result['out'][2]), ('inconclusive', 1))
        self.assertIn('found 0 times', result['out'][1])

    def test_an_unavailable_control_is_not_clicked_and_that_is_a_failure(self):
        result = harness("scenario.steps.splice(1, 2); const r = await walk.run(base); "  # S4 straight after S1: Review setup is unavailable
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
