"""The release build driver and its candidate checks, on invented trees with an injected runner.

No Tauri, Cargo, npm or Apple tool runs; the recipe build is simulated by
placing an invented bundle where Tauri would.
"""
import importlib.util
import io
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
        self.install = Result(0)

    @staticmethod
    def touch_writable(env, stage):
        (Path(env['NPM_CONFIG_LOGS_DIR']) / f'{stage}-debug.log').write_text('invented npm log')
        (Path(env['NPM_CONFIG_CACHE']) / '_logs').mkdir(exist_ok=True)
        (Path(env['NPM_CONFIG_CACHE']) / '_logs' / f'{stage}-debug.log').write_text('invented npm log')
        (Path(env['NPM_CONFIG_CACHE']) / '_update-notifier-last-checked').write_text('')
        for name in ('HOME', 'TMPDIR', 'CODEX_HOME', 'RUSTUP_HOME', 'NPM_CONFIG_PREFIX'):
            (Path(env[name]) / f'.{stage}-wrote-here').write_text(stage)

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
        if argv[:2] == ['npm', 'ci']:
            # What a real offline install writes, at the places the environment names.
            self.touch_writable(env, 'install')
            (Path(cwd) / 'node_modules/@tauri-apps/cli').mkdir(parents=True)
            return self.install
        if argv[0] == 'node':
            self.touch_writable(env, 'build')
            registry = Path(env['CARGO_HOME']) / 'registry'
            registry.mkdir(exist_ok=True)
            (registry / '.package-cache').write_text('lock')
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
        # Sentinels for what belongs to the caller: their home, and the prepared caches given as inputs.
        self.caller_home = self.root / 'caller-home'
        for relative in ('.npm/_logs', '.cargo/registry'):
            (self.caller_home / relative).mkdir(parents=True)
        (self.caller_home / '.npm/_logs/earlier.log').write_text('the caller\'s own log')
        self.cargo_cache = self.root / 'prepared-cargo-cache'
        (self.cargo_cache / 'registry/cache').mkdir(parents=True)
        (self.cargo_cache / 'registry/cache/invented.crate').write_bytes(b'INVENTED crate')
        self.npm_cache = self.root / 'prepared-npm-cache'
        (self.npm_cache / '_cacache').mkdir(parents=True)
        (self.npm_cache / '_cacache/index').write_text('invented index')
        self.environment = {'PATH': str(tools), 'LANG': 'en_US.UTF-8'}
        self.candidate = self.root / 'candidate'
        self.fake = FakeBuild(self)

    def run_build(self, **changes):
        kw = dict(source_root=self.source, revision='a' * 40, vendor=self.vendor, expected_manifest=self.kw['expected_manifest'],
                  pin='9.9.9', out=self.candidate, environment=self.environment, tools=self.tools,
                  cargo_cache=self.cargo_cache, npm_cache=self.npm_cache, runner=self.fake, host=('Darwin', 'arm64'),
                  private=self.private_writer)
        kw.update(changes)
        return build.build(**kw)

    def private_writer(self, root):
        self.private = fx.MemoryWriter(root)
        return self.private

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
        self.assertEqual(description['limitations']['bundled'], 'not observed')
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
        self.assertEqual((self.candidate / 'cargo-home/config.toml').read_text(), recipe['cargo_build_input']['text'])
        install = next(c for c in self.fake.calls if c['argv'][:2] == ['npm', 'ci'])
        self.assertEqual(install['env'], call['env'])
        self.assertEqual(Path(install['cwd']), self.candidate / 'source/app')

    def test_publisher_input_is_generated_from_the_source_keychain_selection(self):
        self.run_build()
        generated = self.candidate / 'publisher-input/publisher-build-selection.json'
        self.assertEqual(json.loads(generated.read_text()), {'format': 'publisher-build-selection.s1',
                         'production_bundle_identifier': 'com.chirality.app', 'developer_id_team_identifier': self.team})
        description = json.loads((self.candidate / 'CANDIDATE.json').read_text())
        self.assertEqual(description['build']['publisher_input_sha256'], fx.sha(generated.read_bytes()))
        self.assertEqual(description['build']['publisher_input_origin'], 'publisher-build-selection.s1 generated from the source keychain selection')
        self.assertFalse((ROOT / 'publisher-input').exists())

    def test_a_supplied_publisher_input_is_used_instead(self):
        supplied = self.root / 'owner-input'; supplied.mkdir()
        path = supplied / 'selection.json'
        path.write_text(json.dumps({'format': 'publisher-build-selection.s1', 'production_bundle_identifier': 'com.chirality.app',
                                    'developer_id_team_identifier': self.team}))
        self.run_build(publisher_input=path, publisher_sha256=fx.sha(path.read_bytes()))
        self.assertFalse((self.candidate / 'publisher-input').exists())
        self.assertEqual(json.loads((self.candidate / 'CANDIDATE.json').read_text())['build']['publisher_input_origin'], 'supplied publisher input file')

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
            'dyld_info': (dict(dyld={'chirality-app-v4': Result(1)}), 'dyld_validate'),
            'dyld_info negative with zero': (dict(dyld={'chirality-app-v4': Result(0, b'', b'malformed LINKEDIT')}), 'dyld_validate'),
            'version': (dict(mutate=wrong_version), 'info_plist_version'),
            'vendor modes': (dict(mutate=vendor_mode), 'vendor_tree'),
            'resource': (dict(mutate=resource_bytes), 'resource'),
            'developer signature': (dict(executable=fx.macho(common.CS_RUNTIME, cms=True)), 'executable_signature'),
            'already signed': (dict(mutate=presigned), 'already_signed'),
        }
        for name, (changes, check_name) in cases.items():
            with self.subTest(name):
                self.setUp()
                for key, value in changes.items():
                    setattr(self.fake, key, value)
                with self.assertRaises(common.Failure) as raised:
                    self.run_build()
                self.assertEqual(raised.exception.code, 'BUILD_CHECKS')
                refused = json.loads((self.candidate / 'BUILD_REFUSED.json').read_text())
                self.assertIn(check_name, [c['check'] for c in refused['checks']])
                self.assertFalse((self.candidate / 'CANDIDATE.json').exists())
                self.assertTrue((self.candidate / 'INCOMPLETE.txt').exists())

    def credentials_cache(self):
        cache = self.root / 'cargo-cache-with-credentials'
        cache.mkdir(exist_ok=True)
        (cache / 'credentials.toml').write_text('[registry]\n')
        return cache

    def test_install_and_build_write_only_under_the_run_folder(self):
        watched = {name: common.inventory.scan(path) for name, path in (
            ('caller home', self.caller_home), ('cargo cache', self.cargo_cache), ('npm cache', self.npm_cache),
            ('source export', self.source), ('vendor', self.vendor))}
        with patch.dict(os.environ, {'HOME': str(self.caller_home)}):
            self.run_build()
        for name, before in watched.items():
            with self.subTest(name):
                self.assertTrue(common.inventory.compare(common.inventory.scan(before['root']), before)['equal'])
        description = json.loads((self.candidate / 'CANDIDATE.json').read_text())
        out = self.candidate.resolve()
        for call in self.fake.calls:
            for name in build.WRITABLE_ENVIRONMENT:
                with self.subTest(name=name, argv=call['argv'][:2]):
                    self.assertTrue(Path(call['env'][name]).resolve().is_relative_to(out))
                    # Containment by device and inode, not by spelling.
                    common.require_inside(Path(call['env'][name]) / 'probe', self.candidate, name)
            self.assertTrue(call['cwd'] is None or Path(call['cwd']).resolve().is_relative_to(out))
        self.assertEqual(set(description['build']['writable_environment']), set(build.WRITABLE_ENVIRONMENT))
        self.assertTrue((self.candidate / 'npm-logs/install-debug.log').is_file())
        self.assertTrue((self.candidate / 'cargo-home/registry/.package-cache').is_file())
        self.assertFalse((self.source / 'app/node_modules').exists())
        # The caches were copied in, not linked: writing the run's copy cannot reach the input.
        for copied, original in ((self.candidate / 'cargo-home/registry/cache/invented.crate', self.cargo_cache / 'registry/cache/invented.crate'),
                                 (self.candidate / 'npm-cache/_cacache/index', self.npm_cache / '_cacache/index'),
                                 (self.candidate / 'source/app/src-tauri/Cargo.toml', self.source / 'app/src-tauri/Cargo.toml')):
            with self.subTest(copied=copied.name):
                self.assertEqual(copied.read_bytes(), original.read_bytes())
                self.assertFalse(copied.samefile(original))

    def test_containment_is_by_identity_and_refuses_links_out_of_the_run_folder(self):
        out = self.root / 'run'; out.mkdir()
        outside = self.root / 'outside'; outside.mkdir()
        (out / 'escape').symlink_to(outside)
        for path in (out / 'escape/file', self.root / 'elsewhere/file', out / '../outside/file'):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, 'not inside the output'):
                common.require_inside(path, out, 'a written file')
        common.require_inside(out / 'target/file', out, 'a written file')
        (self.root / 'CaseProbe').mkdir()
        if (self.root / 'caseprobe').exists():  # case-insensitive volume: a case alias is the same place
            common.require_inside(self.root / 'RUN' / 'file', out, 'a written file')

    def test_a_failed_install_or_build_never_reads_as_a_finished_candidate(self):
        for stage in ('install', 'build'):
            with self.subTest(stage):
                self.setUp()
                if stage == 'install':
                    self.fake.install = Result(1, b'', b'npm ERR! invented offline miss')
                else:
                    self.fake.dyld = {'chirality-app-v4': Result(1)}
                with self.assertRaises(common.Failure):
                    self.run_build()
                self.assertFalse((self.candidate / 'CANDIDATE.json').exists())
                self.assertTrue((self.candidate / 'INCOMPLETE.txt').exists())
                self.assertEqual(json.loads((self.candidate / 'BUILD_FAILED.json').read_text())['result'], 'failed')
                with self.assertRaisesRegex(ValueError, 'did not finish'):
                    common.load_candidate(self.candidate)
                if stage == 'install':
                    self.assertFalse(any(c['argv'][0] == 'node' for c in self.fake.calls))

    def test_refusals_before_building(self):
        cases = {
            'host': dict(host=('Darwin', 'x86_64')),
            'missing environment': dict(environment={k: v for k, v in self.environment.items() if k != 'LANG'}),
            'caller home': dict(environment=self.environment | {'HOME': str(self.caller_home)}),
            'relative PATH': dict(environment=self.environment | {'PATH': 'bin'}),
            'cargo credentials': dict(cargo_cache=self.credentials_cache()),
            'tools': dict(tools={k: v for k, v in self.tools.items() if k != 'ld'}),
            'path rustc': dict(environment=self.environment | {'PATH': '/usr/bin'}),
            'half publisher': dict(publisher_input='/nonexistent'),
            'applications': dict(out='/Applications/chirality-candidate'),
        }
        for name, changes in cases.items():
            with self.subTest(name), self.assertRaises(common.Failure):
                self.run_build(**changes)
        self.assertFalse(any(c['argv'][0] == 'node' for c in self.fake.calls))

    def test_links_that_leave_a_copied_input_are_refused(self):
        def npm_logs_link(case):
            outside = case.root / 'outside-cache'; outside.mkdir()
            (case.npm_cache / '_logs').symlink_to(outside, target_is_directory=True)
            return outside
        def cargo_registry_link(case):
            outside = case.root / 'outside-registry'; outside.mkdir()
            shutil.rmtree(case.cargo_cache / 'registry')
            (case.cargo_cache / 'registry').symlink_to(outside, target_is_directory=True)
            return outside
        def export_link(case):
            outside = case.root / 'outside-export'; outside.mkdir()
            (case.source / 'app/escape').symlink_to(outside, target_is_directory=True)
            return outside
        def absolute_link_inside_export(case):
            # The reviewer's case: source/app/dist is an absolute link to a sibling folder inside the export.
            old = case.source / 'old-dist'; old.mkdir()
            (case.source / 'app/dist').symlink_to(old.resolve(), target_is_directory=True)
            return old
        def relative_link_inside_export(case):
            (case.source / 'app/inside-link').symlink_to('src-tauri')
            empty = case.root / 'nothing-written-here'; empty.mkdir()
            return empty
        def hard_link(where):
            def make(case):
                # The reviewer's input: an ordinary outside file, hard-linked into the input before the run.
                outside = case.root / 'outside-hard'; outside.mkdir(exist_ok=True)
                (outside / 'original').write_text('outside original')
                root = {'export': case.source, 'cargo': case.cargo_cache, 'npm': case.npm_cache}[where]
                os.link(outside / 'original', root / 'hard-linked-input')
                return outside
            return make
        for name, make in (('npm _logs link', npm_logs_link), ('cargo registry link', cargo_registry_link), ('export link', export_link),
                           ('absolute link inside the export', absolute_link_inside_export),
                           ('relative link inside the export', relative_link_inside_export),
                           ('hard link in the export', hard_link('export')), ('hard link in the Cargo home', hard_link('cargo')),
                           ('hard link in the npm cache', hard_link('npm'))):
            with self.subTest(name):
                self.setUp()
                outside = make(self)
                with self.assertRaises(common.Failure) as raised:
                    self.run_build()
                self.assertEqual(raised.exception.code, 'BUILD_LINK')
                self.assertEqual(sorted(p.name for p in outside.iterdir()), [] if 'hard' not in name else ['original'])
                self.assertFalse(self.candidate.exists())

    def test_inputs_inside_a_private_folder_are_refused_by_name(self):
        hidden = self.root / common.PRIVATE_FOLDER
        for key in ('source_root', 'vendor', 'cargo_cache', 'npm_cache', 'out'):
            with self.subTest(key), self.assertRaises(common.Failure) as raised:
                self.run_build(**{key: hidden / 'input'})
            self.assertEqual(raised.exception.code, 'BUILD_PRIVATE_INPUT')
        self.assertFalse(hidden.exists())

    def walk_returnable(self, path):
        common.validate_returnable(json.loads(path.read_text()), {self.team, common.SUPPLIER_TEAM})

    def test_raw_output_and_exceptions_stay_out_of_returnable_files_and_streams(self):
        secrets = ['invented-owner@example.invalid', 'invented-secret', 'QQQQ11111Q']
        self.fake.install = Result(1, b'invented-owner@example.invalid\n', b'password=invented-secret QQQQ11111Q\n')
        out, err = io.StringIO(), io.StringIO()
        self.assertEqual(build.main(self.cli_args(), stdout=out, stderr=err, runner=self.fake, host=('Darwin', 'arm64'),
                                    private=self.private_writer), 2)
        self.assertEqual(err.getvalue(), 'FAILED: ' + common.REASONS['BUILD_INSTALL'] + '\n')
        self.assertFalse((self.candidate / 'install-stdout.log').exists())
        self.assertTrue(any(label == 'install' and b'invented-secret' in raw for label, raw in self.private.handed))
        self.assertFalse((self.candidate / common.PRIVATE_FOLDER).exists())
        failed = self.candidate / 'BUILD_FAILED.json'
        self.walk_returnable(failed)
        for secret in secrets:
            self.assertNotIn(secret, failed.read_text() + out.getvalue() + err.getvalue())
        self.setUp()
        original = self.fake
        def explode(argv, **kw):
            if argv[:2] == ['npm', 'ci']:
                raise ValueError('password=invented-secret invented-owner@example.invalid')
            return original(argv, **kw)
        out, err = io.StringIO(), io.StringIO()
        self.assertEqual(build.main(self.cli_args(), stdout=out, stderr=err, runner=explode, host=('Darwin', 'arm64'),
                                    private=self.private_writer), 2)
        self.assertEqual(err.getvalue(), 'FAILED: ' + common.REASONS['BUILD_UNEXPECTED_INSTALL'] + '\n')
        text = (self.candidate / 'BUILD_FAILED.json').read_text()
        self.assertEqual((json.loads(text)['reason_code'], json.loads(text)['stage']), ('BUILD_UNEXPECTED_INSTALL', 'INSTALL'))
        self.assertTrue(any(label == 'trace' for label, _ in self.private.handed))
        for secret in secrets:
            self.assertNotIn(secret, text + out.getvalue() + err.getvalue())

    def test_the_candidate_is_published_only_after_the_final_check(self):
        with patch.object(common, 'load_candidate', side_effect=OSError('invented transient read failure')):
            with self.assertRaises(common.Failure) as raised:
                self.run_build()
        self.assertEqual(raised.exception.code, 'BUILD_FINAL')
        self.assertFalse((self.candidate / common.CANDIDATE_FILE).exists())
        self.assertTrue((self.candidate / 'INCOMPLETE.txt').exists())
        self.assertEqual(json.loads((self.candidate / 'BUILD_FAILED.json').read_text())['reason_code'], 'BUILD_FINAL')
        with self.assertRaisesRegex(ValueError, 'did not finish'):
            common.load_candidate(self.candidate, name=common.CANDIDATE_PENDING)
        self.setUp()
        self.run_build()
        self.walk_returnable(self.candidate / common.CANDIDATE_FILE)
        self.assertFalse((self.candidate / common.CANDIDATE_PENDING).exists())
        self.assertNotIn(str(self.root), (self.candidate / common.CANDIDATE_FILE).read_text())

    def cli_args(self):
        args = ['--source-root', str(self.source), '--revision', 'a' * 40, '--vendor', str(self.vendor), '--expected-manifest',
                self.kw['expected_manifest'], '--pin', '9.9.9', '--out', str(self.candidate), '--cargo-cache', str(self.cargo_cache),
                '--npm-cache', str(self.npm_cache)]
        for k, v in self.environment.items():
            args += ['--env', k + '=' + v]
        for k, v in self.tools.items():
            args += ['--tool', k + '=' + v]
        return args


if __name__ == '__main__':
    unittest.main()
