"""The scripted driver's test build stays out of the shipped App, and its proof says shown only when it was.

What is checked here runs everywhere: the sources and the release recipe, and the proof's verdict on stand-in runs.
The build itself, its window and the release-features build are checked by the hosted job
(.github/workflows/app-scripted-driver.yml, proof.py release-free).
"""
import importlib.util
import json
import os
import re
import shutil
import stat
import subprocess
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
        self.assertEqual(len(re.findall(r'scripted_driver::', lib)), 1)
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
        self.assertIn('path: |\n            ${{ runner.temp }}/driver/report.json\n            ${{ runner.temp }}/driver/scenario-report.json\n          if-no-files-found', workflow)
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
               windows=1, dialogs=0, evaluated=True, tail='exec sleep 0.3', ever=1, finished=True, one=True):
        app = self.root / 'Test.app'
        executable = app / 'Contents/MacOS/chirality-app-v4'
        executable.parent.mkdir(parents=True, exist_ok=True)
        line = ''
        if evaluated:
            detail = json.dumps({'attempt': 1, 'windows': windows,
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


if __name__ == '__main__':
    unittest.main()
