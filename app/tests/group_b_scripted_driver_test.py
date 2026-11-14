"""The scripted driver's test build stays out of the shipped App, and its proof says shown only when it was.

What is checked here runs everywhere: the sources and the release recipe, and the proof's verdict on stand-in runs.
The build itself, its window and the release-features build are checked by the hosted job
(.github/workflows/app-scripted-driver.yml, proof.py release-free).
"""
import contextlib
import importlib.util
import io
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[2]
APP = REPO / 'app'
PROOF = APP / 'examination/scripted_driver/proof.py'
CFG = 'chirality_scripted_driver'
VARIABLE = 'CHIRALITY_SCRIPTED_DRIVER_BUILD'


def load_proof():
    spec = importlib.util.spec_from_file_location('scripted_driver_proof', PROOF)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class KeptOutOfTheShippedApp(unittest.TestCase):
    def test_no_manifest_lock_or_configuration_names_the_driver(self):
        for path in ('app/src-tauri/Cargo.toml', 'app/src-tauri/Cargo.lock', 'app/package.json', 'app/package-lock.json',
                     'app/src-tauri/tauri.conf.json', 'app/packaging/unsigned/tauri.development.conf.json',
                     *[str(p.relative_to(REPO)) for p in (APP / 'src-tauri/capabilities').glob('*.json')]):
            with self.subTest(path):
                text = (REPO / path).read_text()
                self.assertNotIn(CFG, text)
                self.assertNotIn(VARIABLE, text)
                self.assertNotIn('scripted', text.lower())

    def test_the_build_script_sets_the_cfg_only_for_the_variable_and_refuses_it_with_the_release_feature(self):
        build = (APP / 'src-tauri/build.rs').read_text()
        self.assertIn(f'cargo:rustc-check-cfg=cfg({CFG})', build)
        self.assertEqual(build.count(f'cargo:rustc-cfg={CFG}'), 1)
        body = build[build.index('fn scripted_driver_build'):build.index('fn main')]
        self.assertIn('value == "1"', body)
        self.assertLess(body.index('CARGO_FEATURE_DISTRIBUTION_SUCCESSOR'), body.index(f'cargo:rustc-cfg={CFG}'))
        self.assertLess(body.index('CHIRALITY_PUBLISHER_SELECTION'), body.index(f'cargo:rustc-cfg={CFG}'))
        main = build[build.index('fn main'):]
        self.assertLess(main.index('scripted_driver_build()'), main.index('publisher_build()'))

    def test_the_module_is_compiled_only_under_the_cfg_and_refuses_the_release_feature_itself(self):
        lib = (APP / 'src-tauri/src/lib.rs').read_text()
        self.assertIn(f'#[cfg({CFG})] mod scripted_driver;', lib)
        # Two uses: the builder hook, and the stand-in for desktop setup's confirmation, which is the only one there
        # is (its approval's condition): named once, inside desktop_setup_prepare, under the cfg.
        self.assertEqual(len(re.findall(r'scripted_driver::', lib)), 2)
        self.assertEqual(lib.count('setup_confirmation_stand_in'), 1)
        prepare = lib[lib.index('fn desktop_setup_prepare('):]
        prepare = prepare[:prepare.index('\n}\n')]
        self.assertIn(f'#[cfg({CFG})]\n    {{\n        let _ = &window;\n        return desktop_setup_confirmation::prepare', prepare)
        self.assertIn('scripted_driver::setup_confirmation_stand_in', prepare)
        self.assertIn(f'#[cfg(not({CFG}))]\n    desktop_setup_confirmation::prepare', prepare)
        self.assertIn(f'#[cfg({CFG})]\nfn with_scripted_driver', lib)
        self.assertIn(f'#[cfg(not({CFG}))]\nfn with_scripted_driver', lib)
        module = (APP / 'src-tauri/src/scripted_driver.rs').read_text()
        self.assertIn('#[cfg(feature = "distribution-successor")]\ncompile_error!', module)
        self.assertIn('chirality-scripted-driver-test-build-v1', module)
        self.assertNotRegex(module, r'\.click\(|dispatchEvent|\.value\s*=|invoke\(')  # it reads; it operates nothing

    def test_the_release_recipe_builds_from_an_allowlist_with_the_release_feature(self):
        prepare = (APP / 'packaging/production_inputs/prepare.py').read_text()
        self.assertIn("'inherit_environment': False", prepare)
        self.assertNotIn(VARIABLE, prepare)  # so it is never in the release build's allowlist
        self.assertIn("'--features', 'custom-protocol,distribution-successor'", prepare)
        for name in ('RUSTFLAGS', 'CARGO_ENCODED_RUSTFLAGS'):
            self.assertIn(f"'{name}'", prepare[prepare.index("'unset_environment'"):])

    def test_the_hosted_job_reads_only_holds_no_secret_and_uploads_only_the_report(self):
        workflow = (REPO / '.github/workflows/app-scripted-driver.yml').read_text()
        self.assertRegex(workflow, r'\npermissions:\n  contents: read\n\n')
        self.assertNotIn('secrets.', workflow)
        self.assertNotIn('write', re.sub(r'#.*', '', workflow).lower().replace('writes nothing back', ''))
        self.assertIn('persist-credentials: false', workflow)
        self.assertEqual(workflow.count('upload-artifact'), 1)
        self.assertIn('path: |\n            ${{ runner.temp }}/driver/report.json\n            ${{ runner.temp }}/driver/scenario-report.json\n'
                      '            ${{ runner.temp }}/driver/setup-report.json\n          if-no-files-found', workflow)
        self.assertIn('proof.py setup', workflow)
        self.assertIn('proof.py scenario', workflow)
        self.assertIn('runs-on: macos-26', workflow)
        # Nothing else leaves the runner: the npm download cache is off, and no cache is saved.
        self.assertIn("npm-cache: 'false'", workflow)
        self.assertNotIn('rust-cache-save', workflow)
        self.assertNotIn('actions/cache', workflow)
        setup = (REPO / '.github/actions/app-v4-setup/action.yml').read_text()
        self.assertIn("cache: ${{ inputs.npm-cache != 'false' && ", setup)
        self.assertNotIn('actions/cache/save', setup)
        self.assertIn('proof.py release-free', workflow)


def failing_pgrep():
    """pgrep listing the process group fails (status 3, empty output), as the census's error case."""
    real = subprocess.run

    def run(command, *args, **kwargs):
        if command[:2] == ['pgrep', '-g']:
            return subprocess.CompletedProcess(command, 3, '', 'pgrep: cannot list the group')
        return real(command, *args, **kwargs)
    return mock.patch.object(subprocess, 'run', run)


STAND_IN = '''#!/bin/sh
S="$HOME/scripted-driver/stages.jsonl"
M=chirality-scripted-driver-test-build-v1
for stage in {stages}; do
  printf '{{"marker":"%s","stage":"%s","at_ms":1,"detail":{{}}}}\\n' "$M" "$stage" >> "$S"
done
{evaluated}
{tail}
'''


class TheProofSaysShownOnlyWhenItWas(unittest.TestCase):
    def setUp(self):
        self.proof = load_proof()
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, True)

    def bundle(self, stages=('process started', 'page load started', 'page load finished'), heading='Welcome to Chirality',
               windows=1, dialogs=0, evaluated=True, tail='exec sleep 0.3', ever=1, finished=True, one=True,
               attempt=1, headings_seen=None):
        app = self.root / 'Test.app'
        executable = app / 'Contents/MacOS/chirality-app-v4'
        executable.parent.mkdir(parents=True, exist_ok=True)
        line = ''
        if evaluated:
            detail = json.dumps({'attempt': attempt, 'tries': 60, 'expected_heading': 'Welcome to Chirality',
                                 'expected_seen': heading == 'Welcome to Chirality',
                                 'headings_seen': headings_seen if headings_seen is not None else [heading],
                                 'windows': windows,
                                 'created': {'windows_ever_created': ever, 'webviews_ever_created': 1},
                                 'returned': {'heading': heading, 'open_dialogs': dialogs, 'title': 'Chirality'}})
            line = "printf '%s\\n' '" + json.dumps({'marker': 'chirality-scripted-driver-test-build-v1',
                                                   'stage': 'script evaluated', 'at_ms': 2,
                                                   'detail': json.loads(detail)}) + "' >> \"$S\""
        if finished:
            line += "\nprintf '%s\\n' '" + json.dumps({'marker': 'chirality-scripted-driver-test-build-v1', 'stage': 'proof finished',
                                                     'at_ms': 3, 'detail': {'exactly_one_each': one}}) + "' >> \"$S\""
        executable.write_text(STAND_IN.format(stages=' '.join(f'"{s}"' for s in stages), evaluated=line, tail=tail))
        executable.chmod(executable.stat().st_mode | stat.S_IXUSR)
        return app

    def verdict(self, app, timeout=20):
        out = self.root / 'out'
        if out.exists():
            shutil.rmtree(out)
        out.mkdir()
        code = self.proof.run(app, out, timeout)
        return code, json.loads((out / 'report.json').read_text())

    def test_every_stage_the_heading_one_window_no_dialog_and_its_own_end_is_shown(self):
        code, report = self.verdict(self.bundle())
        self.assertEqual((code, report['result']), (0, 'shown'))
        self.assertEqual(report['stopped_after'], 'script evaluated')
        self.assertTrue(report['limits'] and 'satisfies nothing in release criteria 1 and 2' in report['limits'][0])
        self.assertNotIn('CHIRALITY', ' '.join(report['environment']))

    def test_each_wrong_state_is_not_shown(self):
        cases = {
            'stopped after the load': dict(evaluated=False),
            'another heading': dict(heading='Something else'),
            'no heading': dict(heading=None),
            'two windows': dict(windows=2),
            'a second window created at some time': dict(ever=2),
            'an open dialog': dict(dialogs=1),
            'a failing end': dict(tail='exit 5'),
            'no stage at all': dict(stages=(), evaluated=False),
            'no finishing stage': dict(finished=False),
            'the finish counting more than one of each': dict(one=False),
            'the build started twice': dict(stages=('process started', 'process started', 'page load started', 'page load finished')),
            'a child process of the App': dict(tail='sleep 2; exit 0'),
            'a grandchild left in the App\'s group': dict(tail='( sleep 3 & ) ; sleep 1; exit 0'),
        }
        for name, change in cases.items():
            with self.subTest(name):
                code, report = self.verdict(self.bundle(**change))
                self.assertEqual((code, report['result']), (1, 'not shown'))
        code, report = self.verdict(self.bundle(evaluated=False))
        self.assertEqual(report['stopped_after'], 'page load finished')
        code, report = self.verdict(self.bundle(stages=(), evaluated=False))
        self.assertEqual(report['stopped_after'], 'nothing: no stage was written')

    def test_a_census_that_cannot_be_taken_or_none_at_all_is_not_shown(self):
        with failing_pgrep():
            code, report = self.verdict(self.bundle())
        self.assertEqual((code, report['result']), (1, 'not shown'))
        self.assertTrue(report['census'].startswith('a census could not be taken'))
        self.assertEqual(report['census_failures'][0]['exit_code'], 3)
        code, report = self.verdict(self.bundle(), timeout=0)  # ended at once: no census is made
        self.assertEqual((code, report['result'], report['census_samples']), (1, 'not shown', 0))

    def test_a_slow_page_is_waited_for_and_a_wrong_one_is_told_apart_from_it(self):
        # The page may show another heading, or none, before the first-use page (the App's first host read not yet
        # arrived): the build waits for the expected heading and says what it read on the way.
        code, report = self.verdict(self.bundle(attempt=3, headings_seen=[None, 'Chirality', 'Welcome to Chirality']))
        self.assertEqual((code, report['result']), (0, 'shown'))
        self.assertEqual(report['heading_wait'], {'expected': 'Welcome to Chirality', 'seen': True, 'tries_made': 3,
                                                  'tries_allowed': 60, 'headings_seen': [None, 'Chirality', 'Welcome to Chirality'],
                                                  'last_heading': 'Welcome to Chirality'})
        # The expected heading never came: the build ends itself with status 5 after its last try, and the report
        # says the last heading read and how many tries were made. Every other guard is unchanged.
        code, report = self.verdict(self.bundle(heading='Chirality', attempt=60, headings_seen=[None, 'Chirality'],
                                                finished=False, tail='exit 5'))
        self.assertEqual((code, report['result']), (1, 'not shown'))
        self.assertEqual((report['heading_wait']['seen'], report['heading_wait']['tries_made'], report['heading_wait']['last_heading']),
                         (False, 60, 'Chirality'))

    def test_the_build_and_the_report_expect_the_same_heading(self):
        module = (APP / 'src-tauri/src/scripted_driver.rs').read_text()
        self.assertIn(f'const EXPECTED_HEADING: &str = "{self.proof.EXPECTED_HEADING}";', module)

    def test_a_run_that_does_not_end_is_ended_and_not_shown(self):
        code, report = self.verdict(self.bundle(tail='sleep 30'), timeout=2)
        self.assertEqual((code, report['result'], report['timed_out']), (1, 'not shown', True))

    def test_a_stage_without_the_marker_is_not_shown(self):
        app = self.bundle()
        executable = app / 'Contents/MacOS/chirality-app-v4'
        executable.write_text(executable.read_text().replace('M=chirality-scripted-driver-test-build-v1', 'M=other'))
        code, report = self.verdict(app)
        self.assertEqual((code, report['result']), (1, 'not shown'))



NODE = shutil.which('node')
JUDGE = APP / 'examination/scripted_driver/judge.js'


def judge(call, model, *args):
    """Run one judge.js function under node on a model; return its JSON result."""
    # judge.js is a plain script (the page evaluates it as it is); app/ is an ES-module package, so load its source.
    script = ("const source = require('node:fs').readFileSync(process.argv[1], 'utf8');"
              "const J = new Function('module', source + '\\nreturn ChiralityJudge;')(undefined);"
              "const [call, model, ...args] = JSON.parse(process.argv[2]);"
              "process.stdout.write(JSON.stringify(J[call](model, ...args)));")
    import subprocess
    done = subprocess.run([NODE, '-e', script, str(JUDGE), json.dumps([call, model, *args])], capture_output=True, text=True)
    if done.returncode != 0:
        raise AssertionError(done.stderr)
    return json.loads(done.stdout)


def element(kind, name, state=None):
    return {'kind': kind, 'name': name, **({'state': state} if state else {})}


HOME_VALUES = {'identifier': 'dev.invented', 'home': '/h', 'app_data': '/h/Library/Application Support/dev.invented'}
PAGE = [
    element('heading', 'Welcome'), element('text', 'Welcome'),
    element('text', 'Choose the folder.'),
    element('button', 'Review setup', 'unavailable'), element('button', 'Continue', 'available'),
    element('summary', 'Technical details', 'on'), element('text', 'Technical details'),
    element('text', 'Launch: setup-required. Reason'),
    element('radio', 'New settings Detail', 'chosen'), element('radio', 'Existing settings Detail', 'not chosen'),
    element('heading', 'What setup will do'), element('text', 'What setup will do'),
    element('text', 'First effect'), element('text', 'Second effect'),
    element('summary', 'Exact locations', 'on'), element('text', 'Exact locations'),
    element('text', 'Settings folder'), element('text', '/h/Library/Application Support/dev.invented/settings'),
    element('text', 'Outside folder'), element('text', '/elsewhere/settings'),
]


@unittest.skipIf(NODE is None and not os.environ.get('CI'), 'node is not installed')
class TheJudgeDecidesEachKindBothWays(unittest.TestCase):
    """Each of the eight expectation kinds the scenario uses, shown passing on the right state and failing on a wrong one."""

    def check(self, expectation, model=PAGE):
        return judge('judgeOne', model, expectation, HOME_VALUES)

    def both(self, right, wrong, model=PAGE):
        self.assertTrue(self.check(right, model)['pass'], right)
        self.assertFalse(self.check(wrong, model)['pass'], wrong)

    def test_text_exactly_once(self):
        self.both({'text': 'Choose the folder.'}, {'text': 'Choose the folder'})  # words whole, not a prefix
        twice = PAGE + [element('text', 'Choose the folder.')]
        self.assertEqual(self.check({'text': 'Choose the folder.'}, twice), {'expectation': {'text': 'Choose the folder.'}, 'pass': False, 'found': 'present 2 times'})

    def test_text_starts(self):
        self.both({'text_starts': 'Launch: setup-required.'}, {'text_starts': 'Launch: ready.'})

    def test_heading(self):
        self.both({'heading': 'What setup will do'}, {'heading': 'What setup will happen'})

    def test_button(self):
        self.both({'button': 'Review setup', 'is': 'unavailable'}, {'button': 'Review setup', 'is': 'available'})
        self.assertEqual(self.check({'button': 'Missing', 'is': 'available'})['found'], 'absent')

    def test_summary(self):
        self.both({'summary': 'Technical details', 'is': 'on'}, {'summary': 'Technical details', 'is': 'off'})

    def test_radio(self):
        self.both({'radio': 'New settings Detail', 'is': 'chosen'}, {'radio': 'Existing settings Detail', 'is': 'chosen'})

    def test_texts_from_up_to(self):
        bounds = {'texts_from': {'kind': 'heading', 'label': 'What setup will do'}, 'up_to': {'kind': 'summary', 'label': 'Exact locations'}}
        self.both({**bounds, 'are': ['What setup will do', 'First effect', 'Second effect']},
                  {**bounds, 'are': ['What setup will do', 'First effect']})  # a text more than expected fails
        self.assertFalse(self.check({**bounds, 'are': ['What setup will do', 'Second effect', 'First effect']})['pass'])  # order

    def test_location(self):
        self.both({'location': 'Settings folder', 'under': '{app_data}'}, {'location': 'Outside folder', 'under': '{app_data}'})
        dotted = [element('text', 'Settings folder'), element('text', '/h/Library/Application Support/dev.invented/../x')]
        self.assertFalse(self.check({'location': 'Settings folder', 'under': '{app_data}'}, dotted)['pass'])

    def test_an_unknown_kind_never_passes(self):
        self.assertFalse(self.check({'something': 'else'})['pass'])

    def test_the_click_target_is_exactly_one_available_control_never_an_ellipsis_or_a_never_clicked_one(self):
        scenario = {'never_clicked': ['Browse for project folder']}
        def step(kind, label): return {'control': {'kind': kind, 'label': label}}
        self.assertEqual(judge('target', PAGE, step('button', 'Continue'), scenario), {'index': 4})
        self.assertEqual(judge('target', PAGE, step('button', 'Review setup'), scenario)['verdict'], 'fail')
        self.assertEqual(judge('target', PAGE, step('button', 'Cont'), scenario)['verdict'], 'inconclusive')
        self.assertIn('never clicked', judge('target', PAGE, step('button', 'Create settings…'), scenario)['why'])
        self.assertIn('never clicked', judge('target', PAGE + [element('button', 'Browse for project folder', 'available')],
                                             step('button', 'Browse for project folder'), scenario)['why'])
        doubled = PAGE + [element('button', 'Continue', 'available')]
        self.assertIn('found 2 times', judge('target', doubled, step('button', 'Continue'), scenario)['why'])

    def test_textbox(self):
        page = PAGE + [{'kind': 'textbox', 'name': 'Project folder', 'state': '/h/Projects/p', 'unavailable': False}]
        values = {**HOME_VALUES, 'project': '/h/Projects/p'}
        self.assertTrue(judge('judgeOne', page, {'textbox': 'Project folder', 'is': '{project}'}, values)['pass'])
        self.assertFalse(judge('judgeOne', page, {'textbox': 'Project folder', 'is': ''}, values)['pass'])
        self.assertEqual(judge('judgeOne', PAGE, {'textbox': 'Project folder', 'is': ''}, values)['found'], 'absent')

    def test_text_starts_one_of(self):
        one = {'text_starts_one_of': ['Launch: setup-required.', 'Launch: ready.']}
        self.assertEqual(self.check(one), {'expectation': one, 'pass': True, 'found': 'Launch: setup-required. Reason'})
        self.assertFalse(self.check({'text_starts_one_of': ['Launch: ready.', 'Codex is connected']})['pass'])
        two = PAGE + [element('text', 'Launch: ready. Other')]
        self.assertEqual(self.check(one, two)['found'], 'present 2 times')  # exactly one, or not

    def test_only_the_confirmation_the_scenario_names_may_end_with_an_ellipsis_and_no_unavailable_field_is_typed_into(self):
        page = PAGE + [element('button', 'Create settings and save for next launch…', 'available'),
                       element('button', 'Other action…', 'available'),
                       {'kind': 'textbox', 'name': 'Project folder', 'state': '', 'unavailable': True}]
        scenario = {'confirms': ['Create settings and save for next launch…']}
        def step(kind, label): return {'control': {'kind': kind, 'label': label}}
        self.assertEqual(judge('target', page, step('button', 'Create settings and save for next launch…'), scenario), {'index': len(PAGE)})
        self.assertIn('never clicked', judge('target', page, step('button', 'Other action…'), scenario)['why'])
        self.assertIn('never clicked', judge('target', page, step('button', 'Create settings and save for next launch…'), {})['why'])
        self.assertEqual(judge('target', page, step('textbox', 'Project folder'), scenario)['verdict'], 'fail')

    def test_the_setup_scenario_names_one_confirmation_and_only_kinds_the_judge_knows(self):
        setup = json.loads((APP / 'examination/scripted_driver/setup-complete.scenario.json').read_text())
        self.assertEqual(setup['confirms'], ['Create settings and save for next launch…'])  # the stand-in's one confirmation
        known = {'text', 'no_text', 'text_starts', 'text_starts_one_of', 'heading', 'button', 'summary', 'radio', 'textbox',
                 'texts_from', 'location'}
        for launch in setup['launches']:
            for step in launch['steps']:
                self.assertIn(step['act'], {'view', 'click', 'type', 'read_state'})
                for expectation in step.get('expect', []):
                    self.assertTrue(set(expectation) & known, expectation)
        self.assertEqual([launch['setup_answers'] for launch in setup['launches']], [['leave'], ['create'], []])

    def test_the_scenario_files_kinds_are_all_known_to_the_judge(self):
        scenario = json.loads((APP / 'examination/standalone/operated/first-use-setup.scenario.json').read_text())
        known = {'text', 'no_text', 'text_starts', 'heading', 'button', 'summary', 'radio', 'texts_from', 'location'}
        used = {next(k for k in expectation if k in known) for step in scenario['steps'] for expectation in step['expect']}
        self.assertLessEqual(used, known)
        self.assertEqual(len(used), 8)


SCENARIO_STAND_IN = '''#!/bin/sh
S="$HOME/scripted-driver/stages.jsonl"
M=chirality-scripted-driver-test-build-v1
test -f "$HOME/scripted-driver/scenario.json" || exit 9
{starts}
printf '%s\\n' '{line}' >> "$S"
{extra}
exit {code}
'''


class TheScenarioReportPassesOnlyAWholeWalk(unittest.TestCase):
    def setUp(self):
        self.proof = load_proof()
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, True)
        self.scenario = self.root / 'scenario.json'
        self.scenario.write_text(json.dumps({'scenario': 'invented', 'version': 1, 'steps': [], 'outcomes': {}}))

    def verdict(self, verdict='pass', windows=1, code=0, extra=None, ever=1, hold_awake=False, starts=1, one=True):
        # By default the stand-in stays alive briefly as the one process (exec, no child), as a real App does, so the
        # run takes at least one census.
        extra = ('exec sleep 0.3' if code == 0 else '') if extra is None else extra
        app = self.root / 'Test.app'
        executable = app / 'Contents/MacOS/chirality-app-v4'
        executable.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps({'marker': 'chirality-scripted-driver-test-build-v1', 'stage': 'scenario finished', 'at_ms': 1,
                           'detail': {'most_windows': windows, 'exactly_one_each': one,
                                      'created': {'windows_ever_created': ever, 'webviews_ever_created': 1},
                                      'result': {'verdict': verdict, 'steps': [], 'outcomes': {},
                                                                          'stopped': None}}})
        start = "printf '%s\\n' '" + json.dumps({'marker': 'chirality-scripted-driver-test-build-v1', 'stage': 'process started',
                                                  'at_ms': 0, 'detail': {}}) + "' >> \"$S\""
        executable.write_text(SCENARIO_STAND_IN.format(starts='\n'.join([start] * starts), line=line, extra=extra, code=code))
        executable.chmod(executable.stat().st_mode | stat.S_IXUSR)
        out = self.root / 'out'
        if out.exists():
            shutil.rmtree(out)
        out.mkdir()
        code = self.proof.scenario(app, out, 30, self.scenario, hold_awake=hold_awake)
        return code, json.loads((out / 'scenario-report.json').read_text())

    def test_a_passing_walk_with_one_window_no_child_and_its_own_end_passes(self):
        code, report = self.verdict()
        self.assertEqual((code, report['verdict']), (0, 'pass'))
        self.assertTrue(any('accessibility' in limit for limit in report['limits']))
        self.assertEqual(report['values']['app_data'], f"{report['values']['home']}/Library/Application Support/dev.chirality.app-v4.scripted-driver")

    def test_anything_less_does_not_pass(self):
        for name, change, expected in (('the walk failed', dict(verdict='fail', code=6), 'fail'),
                                       ('the walk was inconclusive', dict(verdict='inconclusive', code=7), 'inconclusive'),
                                       ('a second window', dict(windows=2, code=6), 'fail'),
                                       ('a failing end', dict(code=6), 'inconclusive'),
                                       ('a second window created at some time', dict(ever=2, code=6), 'fail'),
                                       ('a child process of the App', dict(extra='sleep 2'), 'fail'),
                                       ('a child naming the App executable', dict(extra='sh -c "sleep 2" "$0"'), 'fail'),
                                       ('a grandchild left in the App\'s group', dict(extra='( sleep 3 & ) ; sleep 1'), 'fail'),
                                       ('a second window ended the run', dict(extra='printf \'{"marker":"chirality-scripted-driver-test-build-v1","stage":"run ended: a second window","at_ms":2,"detail":{}}\\n\' >> "$S"', code=10), 'fail'),
                                       ('the build started twice', dict(starts=2), 'fail'),
                                       ('the finish counting more than one of each', dict(one=False, code=6), 'fail')):
            with self.subTest(name):
                code, report = self.verdict(**change)
                self.assertEqual((code, report['verdict']), (1, expected))

    def test_a_census_that_cannot_be_taken_does_not_pass(self):
        with failing_pgrep():
            code, report = self.verdict()
        self.assertEqual((code, report['verdict']), (1, 'inconclusive'))
        self.assertTrue(report['census'].startswith('a census could not be taken'))

    @unittest.skipUnless(Path('/usr/bin/caffeinate').is_file(), 'caffeinate is macOS only')
    def test_held_awake_the_app_is_still_the_launched_process_and_the_holder_is_outside_it(self):
        code, report = self.verdict(hold_awake=True)
        self.assertEqual((code, report['verdict'], report['other_processes_seen']), (0, 'pass', []))
        self.assertEqual(report['held_awake_by'][:3], ['/usr/bin/caffeinate', '-di', '-w'])
        code, report = self.verdict(hold_awake=True, extra='sleep 2')
        self.assertEqual((code, report['verdict']), (1, 'fail'))


SETUP_STAND_IN = """#!{python}
import json, os, subprocess, sys, time, uuid
from pathlib import Path
home = Path(os.environ['HOME'])
knobs = json.loads((home.parent.parent / 'knobs.json').read_text()) if (home.parent.parent / 'knobs.json').exists() else {{}}
given = json.loads((home / 'scripted-driver/scenario.json').read_text())
values, answers = given['values'], given['setup_answers']
stages = home / 'scripted-driver/stages.jsonl'
def stage(name, detail):
    with open(stages, 'a') as f:
        f.write(json.dumps({{'marker': 'chirality-scripted-driver-test-build-v1', 'stage': name, 'at_ms': 1, 'detail': detail}}) + '\\n')
stage('process started', {{}})
stage('script evaluated', {{'attempt': 1, 'tries': 60, 'expected_heading': given['expected_heading'], 'expected_seen': True,
                           'headings_seen': [given['expected_heading']], 'returned': {{'heading': given['expected_heading']}}}})
app_data = Path(values['app_data'])
for index, answer in enumerate(answers):
    settings = app_data / f'shared-settings/settings-{{uuid.uuid4()}}'
    account = app_data / f'account-homes/account-{{uuid.uuid4()}}'
    lines = [f'Create NEW App-owned settings folder: {{settings}}',
             'with an empty config.toml, an empty AGENTS.md and a skills folder. Codex adds its own system skills there, and its own working files to the account directory, when it starts.',
             f'Create NEW App-owned account directory: {{account}}',
             'Link its config.toml, AGENTS.md and skills to those new settings.',
             'Read, import or change no other Codex settings, home or credential.',
             f"Project for next launch: {{values['project']}}",
             f"Save a private pending request in {{app_data / 'desktop-startup/request.json'}}.",
             'Codex: the copy included with this App (bundled-owner-use-development).',
             'The current workspace, homes, account/model choices, records and prepared messages stay unchanged. '
             'No automatic quit/restart/login/conversation.']
    if knobs.get('drop_line') is not None:
        del lines[knobs['drop_line']]
    stage('setup confirmation stand-in', {{'index': index, 'title': knobs.get('title', 'Desktop setup — next launch only'),
          'statement': '\\n'.join(lines), 'buttons': ['Leave setup unchanged', 'Create settings and save for next launch', 'Cancel'],
          'answer': answer}})
    if knobs.get('settings_on_leave') and answer == 'leave':
        settings.mkdir(parents=True)
    if answer == 'create' or knobs.get('save_on_leave'):
        if knobs.get('save_other_ids'):
            settings, account = settings.with_name(f'settings-{{uuid.uuid4()}}'), account.with_name(f'account-{{uuid.uuid4()}}')
        (app_data / 'desktop-startup').mkdir(parents=True, exist_ok=True)
        (app_data / 'desktop-startup/request.json').write_text('{{}}')
        settings.mkdir(parents=True, exist_ok=True)
        account.mkdir(parents=True, exist_ok=True)
if knobs.get('write_outside'):
    (home / 'Elsewhere').mkdir(exist_ok=True)
if knobs.get('unreadable'):
    hidden = home / f"Library/Caches/{{values['identifier']}}/hidden"
    hidden.mkdir(parents=True, exist_ok=True)
    (hidden / 'unexpected-file').write_text('')
    hidden.chmod(0)
steps = [{{'id': s['id'], 'checks': [{{'pass': True}}]}} for s in given['scenario']['steps']]
if not answers:
    steps[-1]['app_state'] = {{'launch_state': 'saved-request'}}
    child = knobs.get('child')
    if child == 'codex':
        subprocess.Popen([str(Path(sys.argv[0]).resolve().parents[1] / 'Resources/codex/bin/codex'), '3'])
    elif child == 'other':
        subprocess.Popen(['/usr/bin/perl', '-e', 'sleep 2'])
    time.sleep(1.5)
stage('scenario finished', {{'result': {{'verdict': 'pass', 'steps': steps, 'outcomes': {{}}}}, 'most_windows': 1,
                             'created': {{'windows_ever_created': 1, 'webviews_ever_created': 1}}, 'exactly_one_each': True}})
time.sleep(0.3)
"""


class TheSetupRunPassesOnlyWhatItsScenarioSays(unittest.TestCase):
    """The setup scenario's three launches in one home, with a stand-in App: the inventory, the stand-in's sheet records
    and the relaunch's one allowance (the bundle's own Codex) each decide."""

    def setUp(self):
        self.proof = load_proof()
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, True)
        app = self.root / 'Test.app'
        (app / 'Contents/MacOS').mkdir(parents=True)
        exe = app / 'Contents/MacOS/chirality-app-v4'
        exe.write_text(SETUP_STAND_IN.format(python=sys.executable))
        exe.chmod(0o755)
        # The bundle's Codex here is a link to a system binary (a copy of one may not run): what is compared is the file
        # the process runs, by device and inode, as for the shipped Codex.
        codex = app / 'Contents/Resources/codex/bin/codex'
        codex.parent.mkdir(parents=True)
        codex.symlink_to('/bin/sleep')
        self.app = app

    def verdict(self, **knobs):
        out = self.root / 'out'
        if out.exists():
            shutil.rmtree(out)
        out.mkdir()
        (out / 'knobs.json').write_text(json.dumps(knobs))
        try:
            code = self.proof.setup(self.app, out, 30, APP / 'examination/scripted_driver/setup-complete.scenario.json', hold_awake=False)
        finally:
            for hidden in out.glob('setup-run/home/Library/Caches/*/hidden'):
                hidden.chmod(0o700)
        return code, json.loads((out / 'setup-report.json').read_text())

    def test_three_right_launches_pass_and_each_kind_is_reported_apart(self):
        code, report = self.verdict()
        self.assertEqual((code, report['verdict'], [launch['verdict'] for launch in report['launches']]),
                         (0, 'pass', ['pass', 'pass', 'pass']), json.dumps(report['launches'], indent=1)[:3000])
        relaunch = report['launches'][2]
        self.assertIn('no person-visible element was judged', relaunch['app_state_read']['standing'])
        self.assertTrue(all('app_state' not in step for step in relaunch['visible_elements']))
        self.assertIn('not exercised', report['launches'][0]['stand_in_sheets']['standing'])
        self.assertTrue(any('native confirmation for desktop setup is not exercised' in limit for limit in report['limits']))

    def test_anything_less_does_not_pass(self):
        for name, knobs, failed in (('saved although the answer was leave', {'save_on_leave': True}, 'L1'),
                                    ('settings left behind although the answer was leave', {'settings_on_leave': True}, 'L1'),
                                    ('a sheet with other words', {'title': 'Another title'}, 'L1'),
                                    ('a statement missing its account-directory line', {'drop_line': 2}, 'L1'),
                                    ('a statement missing its last line', {'drop_line': 8}, 'L1'),
                                    ('saved under other names than the sheet said', {'save_other_ids': True}, 'L2'),
                                    ('a folder the inventory could not list', {'unreadable': True}, 'L1'),
                                    ('something written outside the App data and the project', {'write_outside': True}, 'L1'),
                                    ('another process below the App on the relaunch', {'child': 'other'}, 'L3')):
            with self.subTest(name):
                code, report = self.verdict(**knobs)
                self.assertEqual((code, report['verdict']), (1, 'not passed'))
                self.assertEqual(report['launches'][-1]['id'], failed)
                self.assertEqual(report['launches'][-1]['verdict'], 'not passed')

    def test_the_console_result_says_the_native_confirmation_was_not_exercised(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code, report = self.verdict()
        self.assertEqual(code, 0)
        self.assertIn("The App's native confirmation was not exercised", out.getvalue())

    def test_the_scenarios_statement_is_the_apps_new_settings_statement_line_for_line(self):
        source = (APP / 'src-tauri/src/desktop_startup.rs').read_text()
        branch = source[source.index('if let PreviewKind::NewSettings { settings } = &preview.kind {'):]
        statement = re.search(r'format!\("((?:[^"\\]|\\.)*)"', branch).group(1)
        supplier = re.search(r'const SUPPLIER: &str = "([^"]+)";', source).group(1)
        named = iter(['{settings}', '{account}', '{project}', '{app_data}/desktop-startup/request.json'])
        expected = re.sub(r'\{\}', lambda _: next(named), statement.replace('{SUPPLIER}', supplier)).split('\\n')
        sheet = json.loads((APP / 'examination/scripted_driver/setup-complete.scenario.json').read_text())['sheet']
        self.assertEqual(sheet['statement'], expected)
        self.assertIn('const PROFILE: &str = "desktop-startup/request.json";', source)

    @unittest.skipUnless(sys.platform == 'darwin', 'the executable is asked of macOS')
    def test_the_relaunch_allows_the_bundles_own_codex_by_file_and_records_it(self):
        code, report = self.verdict(child='codex')
        self.assertEqual((code, report['verdict']), (0, 'pass'), json.dumps(report['launches'][-1], indent=1)[:3000])
        self.assertTrue(report['launches'][2]['allowed_codex_seen'])
        self.assertFalse(report['launches'][2]['other_processes_seen'])


if __name__ == '__main__':
    unittest.main()
