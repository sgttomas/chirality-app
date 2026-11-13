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
import tempfile
import unittest
from pathlib import Path

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
        self.assertIn('path: ${{ runner.temp }}/driver/report.json\n', workflow)
        self.assertIn('runs-on: macos-26', workflow)
        # Nothing else leaves the runner: the npm download cache is off, and no cache is saved.
        self.assertIn("npm-cache: 'false'", workflow)
        self.assertNotIn('rust-cache-save', workflow)
        self.assertNotIn('actions/cache', workflow)
        setup = (REPO / '.github/actions/app-v4-setup/action.yml').read_text()
        self.assertIn("cache: ${{ inputs.npm-cache != 'false' && ", setup)
        self.assertNotIn('actions/cache/save', setup)
        self.assertIn('proof.py release-free', workflow)


STAND_IN = '''#!/bin/sh
mkdir -p "$HOME/scripted-driver"
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
               windows=1, dialogs=0, evaluated=True, tail='exit 0'):
        app = self.root / 'Test.app'
        executable = app / 'Contents/MacOS/chirality-app-v4'
        executable.parent.mkdir(parents=True, exist_ok=True)
        line = ''
        if evaluated:
            detail = json.dumps({'attempt': 1, 'windows': windows,
                                 'returned': {'heading': heading, 'open_dialogs': dialogs, 'title': 'Chirality'}})
            line = "printf '%s\\n' '" + json.dumps({'marker': 'chirality-scripted-driver-test-build-v1',
                                                   'stage': 'script evaluated', 'at_ms': 2,
                                                   'detail': json.loads(detail)}) + "' >> \"$S\""
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
            'an open dialog': dict(dialogs=1),
            'a failing end': dict(tail='exit 5'),
            'no stage at all': dict(stages=(), evaluated=False),
        }
        for name, change in cases.items():
            with self.subTest(name):
                code, report = self.verdict(self.bundle(**change))
                self.assertEqual((code, report['result']), (1, 'not shown'))
        code, report = self.verdict(self.bundle(evaluated=False))
        self.assertEqual(report['stopped_after'], 'page load finished')
        code, report = self.verdict(self.bundle(stages=(), evaluated=False))
        self.assertEqual(report['stopped_after'], 'nothing: no stage was written')

    def test_a_run_that_does_not_end_is_ended_and_not_shown(self):
        code, report = self.verdict(self.bundle(tail='sleep 30'), timeout=2)
        self.assertEqual((code, report['result'], report['timed_out']), (1, 'not shown', True))

    def test_a_stage_without_the_marker_is_not_shown(self):
        app = self.bundle()
        executable = app / 'Contents/MacOS/chirality-app-v4'
        executable.write_text(executable.read_text().replace('M=chirality-scripted-driver-test-build-v1', 'M=other'))
        code, report = self.verdict(app)
        self.assertEqual((code, report['result']), (1, 'not shown'))


if __name__ == '__main__':
    unittest.main()
