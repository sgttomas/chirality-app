"""Successor A admission tests: invented files only, no native App or supplier."""
import importlib.util
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('successor_setup', Path(__file__).with_name('native_successor_setup.py'))
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)


class Admission(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='successor-A-test-', dir=controller.T3 / 'scratch')
        self.root = Path(self.temp.name).resolve()
        self.home = self.root / 'invented-home'
        self.home.mkdir()
        self.home_patch = patch.object(Path, 'home', return_value=self.home)
        self.home_patch.start()
        self.addCleanup(self.temp.cleanup)
        self.addCleanup(self.home_patch.stop)
        self.identifier = 'dev.chirality.app-v4.candidate.fixture-successor'
        self.record_path = self.root / 'identified/candidate-identification.json'
        self.manifest_path = self.root / 'witness-inputs/input-manifest.json'
        self.record_path.parent.mkdir()
        self.manifest_path.parent.mkdir()
        fixture = self.manifest_path.parent
        (fixture / 'shared').mkdir()
        for name in ['shared/config.toml', 'shared/AGENTS.md']:
            (fixture / name).write_text('# invented uncredentialed material\n')
        for name in ['shared/skills', 'project']:
            (fixture / name).mkdir()
        self.preparation = {'revision': 'a' * 40, 'identifier': self.identifier, 'root': str(self.root),
                            'configuration': {'identifier': self.identifier, 'productName': 'Invented App'}}
        self.record = {'format': 'chirality.app-v4.candidate-identification/v3',
                       'route': 'native_development', 'candidate_key': 'invented-candidate',
                       'app_candidate': {'revision': 'a' * 40, 'packaged': False},
                       'source': {'revision': 'a' * 40},
                       'bundle': {'identifier': self.identifier, 'name': 'Invented App.app',
                                  'executable': {'path': 'Contents/MacOS/invented', 'sha256': 'b' * 64}},
                       'supplier': {'bundled': True, 'pin': '0.160.0', 'standing': 'unqualified-development'}}
        bundle = self.root / 'target/debug/bundle/macos/Invented App.app'
        self.manifest = {'candidate_key': self.record['candidate_key'], 'bundle_identifier': self.identifier,
                         'bundle': str(bundle), 'executable': str(bundle / 'Contents/MacOS/invented'),
                         'executable_sha256': 'b' * 64,
                         'expected_app_data': str(self.home / 'Library/Application Support' / self.identifier),
                         'native_input_paths': {'shared_config': str(fixture / 'shared/config.toml'),
                                                'shared_agents': str(fixture / 'shared/AGENTS.md'),
                                                'shared_skills': str(fixture / 'shared/skills'),
                                                'project': str(fixture / 'project')},
                         'files': {name: controller.digest(fixture / name) for name in
                                   ['shared/config.toml', 'shared/AGENTS.md']},
                         'environment': {'HOME': str(self.home),
                                         'PATH': str(bundle / 'Contents/Resources/codex/codex-path') + ':/usr/bin:/bin:/usr/sbin:/sbin',
                                         'LANG': 'en_US.UTF-8', 'CODEX_HOME': str(fixture / 'fallback-codex-home'),
                                         'TMPDIR': str(fixture / 'tmp')}}
        self.save()

    def save(self):
        for path, data in [(self.root / 'preparation.json', self.preparation),
                           (self.record_path, self.record), (self.manifest_path, self.manifest)]:
            path.write_text(json.dumps(data))

    def context(self):
        return controller.Context(self.root, self.record_path, self.manifest_path)

    def prepared_attempt(self):
        context = self.context()
        attempt = self.root / 'attempt'
        attempt.mkdir(mode=0o700)
        with patch.object(controller.tempfile, 'mkdtemp', return_value=str(attempt)):
            controller.prepare(context)
        return attempt

    def test_binding_reuses_controller_without_mutating_historical_defaults(self):
        context = self.context()
        self.assertEqual(context.inputs(), self.manifest)
        bound = context.bind()
        original = controller.load_base()
        self.assertEqual(bound.RETAINED, self.root)
        self.assertEqual(original.IDENTIFIER, controller.OLD_IDENTIFIER)
        self.assertEqual(Path(bound.execute.__code__.co_filename).resolve(), controller.BASE)
        self.assertEqual(bound.Supervisor.settle.__code__.co_filename, str(controller.BASE))
        self.assertEqual(len(controller.dependency_digests()), 5)

    def test_source_or_namespace_mismatch_and_original_namespace_refuse(self):
        self.preparation['revision'] = 'c' * 40
        self.save()
        with self.assertRaisesRegex(RuntimeError, 'source mismatch'):
            self.context()
        self.preparation['revision'] = 'a' * 40
        self.record['bundle']['identifier'] = controller.OLD_IDENTIFIER
        self.save()
        with self.assertRaisesRegex(RuntimeError, 'distinct successor'):
            self.context()

    def test_changed_files_or_injected_startup_environment_refuse(self):
        context = self.context()
        (self.manifest_path.parent / 'shared/config.toml').write_text('changed')
        with self.assertRaisesRegex(RuntimeError, 'invented input changed'):
            context.inputs()
        self.manifest['environment']['CHIRALITY_WORKSPACE'] = 'unadmitted'
        self.manifest['files']['shared/config.toml'] = controller.digest(self.manifest_path.parent / 'shared/config.toml')
        self.save()
        with self.assertRaisesRegex(RuntimeError, 'unexpected launch environment'):
            self.context().inputs()

    def test_existing_namespace_is_preserved_and_metadata_never_follows_root_link(self):
        context = self.context()
        target = self.home / 'Library/WebKit' / self.identifier
        target.parent.mkdir(parents=True)
        elsewhere = self.root / 'invented-elsewhere'
        elsewhere.mkdir()
        (elsewhere / 'keep').write_text('preserved')
        target.symlink_to(elsewhere)
        with self.assertRaisesRegex(RuntimeError, 'already exists'):
            context.namespaces()
        with patch.object(controller.os, 'walk', side_effect=AssertionError('must not traverse root link')):
            observed = context.namespaces(require_absent=False)
        self.assertEqual(observed['WebKit']['metadata'], [])
        self.assertEqual((elsewhere / 'keep').read_text(), 'preserved')

    def test_prepare_keeps_strict_policy_and_execute_rejects_admission_tamper(self):
        attempt = self.prepared_attempt()
        policy = (attempt / 'phase-A.sb').read_text()
        for rule in ['(deny process-fork)', '(deny process-exec)', '(deny network*)']:
            self.assertIn(rule, policy)
        self.assertIn(str(self.home / '.codex'), policy)
        admission = json.loads((attempt / 'admission.json').read_text())
        admission['inputs']['environment']['CHIRALITY_WORKSPACE'] = 'injected'
        (attempt / 'admission.json').write_text(json.dumps(admission))
        with self.assertRaisesRegex(RuntimeError, 'prepared launch inputs differ'):
            controller.execute(attempt, time.time() + 120)

    def test_execute_rejects_changed_admission_sources_before_base_execution(self):
        attempt = self.prepared_attempt()
        self.manifest['candidate_key'] = 'rebound'
        self.save()
        with self.assertRaisesRegex(RuntimeError, 'admission source changed'):
            controller.execute(attempt, time.time() + 120)

    def test_bound_execute_refusal_and_retry_preserve_first_namespace_record(self):
        attempt = self.prepared_attempt()
        # Exercise the actual rebound base execute up to its slot admission;
        # no App, subprocess probe or native action can be launched here.
        with patch('subprocess.check_output', return_value='not the slot wrapper'), \
             patch('subprocess.Popen', side_effect=AssertionError('no launch')):
            with self.assertRaisesRegex(RuntimeError, 'slot wrapper missing'):
                controller.execute(attempt, time.time() + 120)
        first = (attempt / 'namespace-after.json').read_bytes()
        namespace = self.home / 'Library/Caches' / self.identifier
        namespace.mkdir(parents=True)
        (attempt / 'actions.jsonl').write_text('invented prior actions\n')
        with self.assertRaisesRegex(RuntimeError, 'attempt already used'):
            controller.execute(attempt, time.time() + 120)
        self.assertEqual((attempt / 'namespace-after.json').read_bytes(), first)
        with self.assertRaises(FileExistsError):
            controller.write_once(attempt / 'namespace-after.json', {'changed': True})
        self.assertEqual((attempt / 'namespace-after.json').read_bytes(), first)


if __name__ == '__main__':
    unittest.main()
