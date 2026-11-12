"""The release build driver and its candidate checks, on invented trees with an injected runner.

No Tauri, Cargo, npm or Apple tool runs; the recipe build is simulated by
placing an invented bundle where Tauri would.
"""
import importlib.util
import json
import os
from pathlib import Path
import plistlib
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load(name, path):
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec); sys.modules[name] = module; spec.loader.exec_module(module)
    return sys.modules[name]


fx = load('release_fixtures', HERE / 'release_fixtures.py')
inputs = load('production_inputs_test_helpers', HERE / 'production_inputs_test.py')
build, common = fx.release('build'), fx.common
prepare = common.prepare
Result = common.Result
SCOPE = {'host': 'aarch64-apple-darwin', 'target': 'aarch64-apple-darwin', 'macos': '27.2', 'sdk': '27.2'}


class FakeBuild:
    """uname/sw_vers/xcrun answers, dyld_info, and a recipe build that places an invented bundle."""

    def __init__(self, case):
        self.case, self.calls, self.dyld = case, [], {}
        self.mutate = None
        self.executable = None

    def __call__(self, argv, *, env, cwd=None, timeout=None):
        self.calls.append({'argv': list(argv), 'env': dict(env), 'cwd': cwd})
        if argv == ['/usr/bin/uname', '-m']:
            return Result(0, b'arm64\n')
        if argv == ['/usr/bin/sw_vers', '-productVersion']:
            return Result(0, b'27.2\n')
        if argv[:2] == ['/usr/bin/xcrun', '--sdk']:
            return Result(0, b'27.2\n')
        if argv[0] == '/usr/bin/dyld_info':
            return self.dyld.get(Path(argv[-1]).name, Result(0))
        if argv[0] == 'node':
            self.place(env, cwd, argv)
            return Result(0, b'invented build output\n')
        raise AssertionError(argv)

    def place(self, env, cwd, argv):
        config = json.loads(Path(argv[argv.index('--config') + 1]).read_text())
        target = Path(env['CARGO_TARGET_DIR'])
        requirement = fx.REQUIREMENT.encode()
        binding = fx.binding_bytes(input_sha256=env['CHIRALITY_PUBLISHER_INPUT_SHA256'], team=self.case.team)
        out = target / 'release/build/chirality-app-v4-0123456789abcdef/out'
        out.mkdir(parents=True)
        (out / 'publisher-build-binding.s1.json').write_bytes(binding)
        (out / 'publisher-requirement.txt').write_bytes(requirement)
        (out / 'publisher-build-public-projection.s1.json').write_bytes(b'{"format":"invented projection"}')
        app = target / 'release/bundle/macos' / (config['productName'] + '.app')
        contents = app / 'Contents'
        (contents / 'MacOS').mkdir(parents=True)
        (contents / 'Info.plist').write_bytes(fx.info_plist(CFBundleIdentifier=config['identifier'], CFBundleShortVersionString=config['version'],
                                                            CFBundleVersion=config['version'],
                                                            LSMinimumSystemVersion=config['bundle']['macOS']['minimumSystemVersion']))
        exe = contents / 'MacOS/chirality-app-v4'
        exe.write_bytes(self.executable or fx.macho(payload=binding + b'\x00' + requirement)); exe.chmod(0o755)
        resources = contents / 'Resources'
        resources.mkdir()
        for source, destination in config['bundle']['resources'].items():
            path = Path(source) if Path(source).is_absolute() else Path(os.path.abspath(Path(cwd) / 'src-tauri' / source))
            placed = resources / destination.rstrip('/')
            placed.parent.mkdir(parents=True, exist_ok=True)
            if path.is_dir():
                shutil.copytree(path, placed, symlinks=True, copy_function=shutil.copy2)
            else:
                shutil.copy2(path, placed)
        if self.mutate:
            self.mutate(app)


class ReleaseBuild(unittest.TestCase):
    team = '8A7JL35U4S'
    bind_vendor_reference = inputs.ProductionInputs.bind_vendor_reference

    def setUp(self):
        inputs.ProductionInputs.setUp(self)
        for relative in ('app/src-tauri/src', 'docs'):
            (self.source / relative).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / build.KEYCHAIN_SOURCE, self.source / build.KEYCHAIN_SOURCE)
        shutil.copyfile(ROOT / common.LIMITATIONS_SOURCE, self.source / common.LIMITATIONS_SOURCE)
        tools = self.root / 'toolchain'; tools.mkdir()
        self.tools = {}
        for name in build.TOOLS:
            (tools / name).write_bytes(b'INVENTED ' + name.encode()); (tools / name).chmod(0o755)
            self.tools[name] = str(tools / name)
        contract = prepare.cargo_build_input_contract(prepare.CARGO_BUILD_PRESET)
        contract['tool_sha256'] = {name: fx.sha(Path(path).read_bytes()) for name, path in self.tools.items()}
        patcher = patch.object(prepare, 'cargo_build_input_contract', lambda preset: json.loads(json.dumps(contract)))
        patcher.start(); self.addCleanup(patcher.stop)
        for name in ('home', 'cargo-home', 'npm-cache'):
            (self.root / name).mkdir()
        (self.root / 'npmrc').write_text('')
        self.environment = {'PATH': str(tools), 'HOME': str(self.root / 'home'), 'LANG': 'en_US.UTF-8',
                            'CARGO_HOME': str(self.root / 'cargo-home'), 'NPM_CONFIG_CACHE': str(self.root / 'npm-cache'),
                            'NPM_CONFIG_USERCONFIG': str(self.root / 'npmrc'), 'NPM_CONFIG_GLOBALCONFIG': str(self.root / 'npmrc')}
        self.candidate = self.root / 'candidate'
        self.fake = FakeBuild(self)

    def run_build(self, **changes):
        kw = dict(source_root=self.source, revision='a' * 40, vendor=self.vendor, expected_manifest=self.kw['expected_manifest'],
                  pin='9.9.9', out=self.candidate, environment=self.environment, tools=self.tools,
                  runner=self.fake, host=('Darwin', 'arm64'))
        kw.update(changes)
        return build.build(**kw)

    def test_overlay_identity_is_the_release_identity(self):
        self.run_build()
        config = json.loads((self.candidate / 'plan/tauri.package-inputs.conf.json').read_text())
        self.assertEqual((config['productName'], config['identifier'], config['version']), ('Chirality', 'com.chirality.app', '4.0.0'))
        self.assertEqual(config['bundle']['macOS'], {'minimumSystemVersion': '15.0', 'signingIdentity': None})
        self.assertEqual(config['bundle']['targets'], ['app'])

    def test_build_writes_a_candidate_that_verifies(self):
        result = self.run_build()
        self.assertFalse(result['signing_executed'])
        description, app, binding, requirement = common.load_candidate(self.candidate)
        self.assertEqual(app.name, 'Chirality.app')
        self.assertEqual(description['bundle']['executable'], 'chirality-app-v4')
        self.assertEqual(binding['developer_id_team_identifier'], self.team)
        self.assertTrue(description['vendor']['equal'])
        self.assertTrue(all(r['equal'] for r in description['resources']))
        self.assertEqual(description['limitations']['sha256'], fx.sha((ROOT / common.LIMITATIONS_SOURCE).read_bytes()))
        self.assertEqual(description['limitations']['bundled'], 'not present in the bundle')
        self.assertFalse((self.candidate / 'INCOMPLETE.txt').exists())
        validated = {Path(c['argv'][-1]).name for c in self.fake.calls if c['argv'][0] == '/usr/bin/dyld_info'}
        self.assertEqual(validated, {'chirality-app-v4', 'codex'})

    def test_recipe_runs_from_exactly_the_allowlisted_environment(self):
        self.run_build()
        recipe = json.loads((self.candidate / 'plan/build-recipe.json').read_text())
        call = next(c for c in self.fake.calls if c['argv'][0] == 'node')
        self.assertEqual(call['argv'], recipe['argv'])
        self.assertIn('--no-sign', call['argv'])
        self.assertEqual(set(call['env']), set(recipe['environment_allowlist']))
        self.assertFalse(any(k.startswith(('APPLE_', 'TAURI_SIGNING_')) for k in call['env']))
        self.assertEqual(call['env']['CODEX_HOME'], str(self.candidate / 'codex-home'))
        self.assertEqual(call['env']['CHIRALITY_PUBLISHER_SELECTION'], 'production-v1')
        self.assertEqual((self.root / 'cargo-home/config.toml').read_text(), recipe['cargo_build_input']['text'])

    def test_publisher_input_is_generated_from_the_source_keychain_selection(self):
        self.run_build()
        generated = self.candidate / 'publisher-input/publisher-build-selection.json'
        self.assertEqual(json.loads(generated.read_text()), {'format': 'publisher-build-selection.s1',
                         'production_bundle_identifier': 'com.chirality.app', 'developer_id_team_identifier': self.team})
        description = json.loads((self.candidate / 'CANDIDATE.json').read_text())
        self.assertEqual(description['build']['publisher_input_sha256'], fx.sha(generated.read_bytes()))
        self.assertIn(build.KEYCHAIN_SOURCE, description['build']['publisher_input_origin'])
        self.assertFalse((ROOT / 'publisher-input').exists())

    def test_a_supplied_publisher_input_is_used_instead(self):
        supplied = self.root / 'owner-input'; supplied.mkdir()
        path = supplied / 'selection.json'
        path.write_text(json.dumps({'format': 'publisher-build-selection.s1', 'production_bundle_identifier': 'com.chirality.app',
                                    'developer_id_team_identifier': self.team}))
        self.run_build(publisher_input=path, publisher_sha256=fx.sha(path.read_bytes()))
        self.assertFalse((self.candidate / 'publisher-input').exists())
        self.assertEqual(json.loads((self.candidate / 'CANDIDATE.json').read_text())['build']['publisher_input_origin'], 'supplied file')

    def test_keychain_selection_must_be_single_and_the_release_identifier(self):
        path = self.source / build.KEYCHAIN_SOURCE
        text = path.read_text()
        path.write_text(text.replace('bundle_identifier: "com.chirality.app"', 'bundle_identifier: "com.example.other"', 1))
        with self.assertRaisesRegex(ValueError, 'release identifier'):
            build.publisher_values(self.source)
        path.write_text(text + text)
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            build.publisher_values(self.source)

    def test_post_build_checks_refuse_a_wrong_candidate(self):
        def wrong_version(app):
            (app / 'Contents/Info.plist').write_bytes(fx.info_plist(CFBundleShortVersionString='4.0.1'))
        def vendor_mode(app):
            os.chmod(app / 'Contents/Resources/codex/codex-path', 0o700)
        def resource_bytes(app):
            (app / 'Contents/Resources/instructions/roles.json').write_text('{}')
        def presigned(app):
            (app / 'Contents/_CodeSignature').mkdir()
        cases = {
            'dyld_info': (dict(dyld={'chirality-app-v4': Result(1)}), 'dyld_info'),
            'version': (dict(mutate=wrong_version), 'CFBundleShortVersionString|version'),
            'vendor modes': (dict(mutate=vendor_mode), 'vendor tree'),
            'resource': (dict(mutate=resource_bytes), 'mapped resource'),
            'developer signature': (dict(executable=fx.macho(common.CS_RUNTIME, cms=True)), 'ad hoc'),
            'already signed': (dict(mutate=presigned), '_CodeSignature'),
        }
        for name, (changes, message) in cases.items():
            with self.subTest(name):
                self.setUp()
                for key, value in changes.items():
                    setattr(self.fake, key, value)
                with self.assertRaisesRegex(ValueError, message):
                    self.run_build()
                self.assertFalse((self.candidate / 'CANDIDATE.json').exists())
                self.assertTrue((self.candidate / 'INCOMPLETE.txt').exists())

    def test_refusals_before_building(self):
        cases = {
            'host': dict(host=('Darwin', 'x86_64')),
            'missing environment': dict(environment={k: v for k, v in self.environment.items() if k != 'LANG'}),
            'codex home': dict(environment=self.environment | {'HOME': str(Path.home() / '.codex')}),
            'tools': dict(tools={k: v for k, v in self.tools.items() if k != 'ld'}),
            'path rustc': dict(environment=self.environment | {'PATH': '/usr/bin'}),
            'half publisher': dict(publisher_input='/nonexistent'),
            'applications': dict(out='/Applications/chirality-candidate'),
        }
        for name, changes in cases.items():
            with self.subTest(name), self.assertRaises(ValueError):
                self.run_build(**changes)
        self.assertFalse(any(c['argv'][0] == 'node' for c in self.fake.calls))


if __name__ == '__main__':
    unittest.main()
