"""Explicit current/full-document adoption and preserved historical EXP joins."""
import copy
import contextlib
import io
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

APP = Path(__file__).resolve().parents[1]
ROOT = APP.parent
HERE = APP / 'examination/admission'
spec = importlib.util.spec_from_file_location('current_admission_boundary_tests', HERE / 'current_admission.py')
current = importlib.util.module_from_spec(spec)
spec.loader.exec_module(current)
FROZEN = APP / 'examination/support_identity/frozen'


class CurrentAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pins = current.parse(current.MANIFEST.read_bytes())
        self.support = current.Support(profile=current.PROFILE)
        self.legacy = current._legacy()

    def fixture(self, name):
        return current.parse((APP / 'tests/group_b_admission_fixtures' / (name + '.json')).read_bytes())

    def copy_sources(self, historical=False):
        pins = current.parse((HERE / 'sources.json').read_bytes()) if historical else self.pins
        for source in pins['sources']:
            relative = source if historical else current.deliverable_path(ROOT, source)
            raw = ((FROZEN if historical else ROOT) / relative).read_bytes()
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        return pins

    def test_exact_current_subject_and_unchanged_exp_identity(self):
        self.assertEqual(current.sha(current.MANIFEST.read_bytes()), current.MANIFEST_SHA256)
        source = self.support.source_selection
        self.assertEqual(source['profile'], 'current-v1')
        self.assertEqual(source['basis_revision'], '7658f1bea245cb7068b681644aae86f47061ac3f')
        self.assertEqual(source['sources']['execution/PKG-09/DEL-09-01/Design/EXAMINATION_PROTOCOL.md'],
                         'c7aa2fcfcc43558cbcf9244aae576b6ad0911ab17aa1a8f52112053969e4cb83')
        self.assertEqual(source['sources']['execution/PKG-09/DEL-09-01/ScopeOfWork.md'],
                         'a60b02a8cfa40abf1819d08420a94e2539c6b1c83fa3e22f045c079dbaaa65fd')
        original = current.parse((HERE / 'sources.json').read_bytes())
        unchanged = [p for p in source['sources'] if not p.endswith('.md')]
        self.assertEqual(len(unchanged), 4)
        for path in unchanged:
            self.assertEqual(source['sources'][path], original['sources'][path])
        self.assertEqual(source['support_revision']['exp_version'], 'EXP-v0.2')
        self.assertFalse(source['producer_use_verified'])
        self.assertFalse(source['authority_authenticated'])
        source['sources'].clear()
        self.assertEqual(len(self.support.source_selection['sources']), 6)

    def test_missing_unknown_historical_and_caller_selected_profiles_refuse(self):
        for profile in (None, '', 'historical-v1', 'current-v2', {'profile': 'current-v1'}):
            with self.subTest(profile=profile), self.assertRaises(ValueError):
                current.Support(profile=profile)
        with self.assertRaises(FileNotFoundError):
            current.Support(profile=current.PROFILE, manifest=self.root / 'absent.json')
        for mutate in (lambda p: p.pop('profile'), lambda p: p.update(profile='historical-v1'),
                       lambda p: p.update(format='exp-admission-source-profile/99'),
                       lambda p: p['sources'].update({'execution/PKG-09/DEL-09-01/ScopeOfWork.md': '0' * 64}),
                       lambda p: p['reader_dependencies'].clear()):
            value = copy.deepcopy(self.pins); mutate(value)
            path = self.root / 'manifest.json'; path.write_text(json.dumps(value))
            with self.subTest(mutate=mutate), self.assertRaisesRegex(ValueError, 'profile manifest'):
                current.Support(profile=current.PROFILE, manifest=path)
        with self.assertRaisesRegex(ValueError, 'profile manifest'):
            current.Support(profile=current.PROFILE, manifest=HERE / 'sources.json')

    def test_every_full_source_missing_or_changed_refuses_without_fallback(self):
        self.copy_sources()
        current.Support(project=self.root, profile=current.PROFILE)
        for path in self.pins['sources']:
            resolved = self.root / current.deliverable_path(self.root, path)
            raw = resolved.read_bytes()
            with self.subTest(source=path):
                resolved.unlink()
                with self.assertRaises(FileNotFoundError):
                    current.Support(project=self.root, profile=current.PROFILE)
                resolved.write_bytes(raw + b'\n')
                with self.assertRaisesRegex(ValueError, 'canonical source drift'):
                    current.Support(project=self.root, profile=current.PROFILE)
                resolved.write_bytes(raw)

    def test_changed_authority_passages_are_guarded_not_only_old_projections(self):
        self.copy_sources()
        mutations = [
            ('execution/PKG-09/DEL-09-01/Work/EXAMINATION_PROTOCOL.md', b'**Current decision correspondence', b'**Changed decision correspondence'),
            ('execution/PKG-09/DEL-09-01/Work/EXAMINATION_PROTOCOL.md', b'| U-EXP-1 |', b'| U-EXP-X |'),
            ('execution/PKG-09/DEL-09-01/ScopeOfWork.md', b'- **TBD-001**', b'- **TBD-CHANGED**'),
            ('execution/PKG-09/DEL-09-01/ScopeOfWork.md', b'## Implemented documentary receiving', b'## Changed documentary receiving'),
        ]
        for name, before, after in mutations:
            target = self.root / name; raw = target.read_bytes()
            self.assertIn(before, raw)
            target.write_bytes(raw.replace(before, after, 1))
            with self.subTest(source=name, clause=before), self.assertRaisesRegex(ValueError, 'source drift'):
                current.Support(project=self.root, profile=current.PROFILE)
            target.write_bytes(raw)

    def test_current_and_frozen_profiles_cannot_substitute_for_each_other(self):
        original = self.legacy.Support(project=FROZEN)
        self.assertEqual(current.sha(original.manifest_bytes), self.pins['legacy_source_lock']['sha256'])
        with self.assertRaisesRegex(ValueError, 'source drift'):
            current.Support(project=FROZEN, profile=current.PROFILE)
        with self.assertRaisesRegex(ValueError, 'source drift'):
            self.legacy.Support(project=ROOT)
        # Identical old and current EXP rules remain usable on their actual sources.
        for reader in (original, self.support):
            self.assertEqual(reader.review_join(self.fixture('review'), self.fixture('rerun'),
                                                self.fixture('review-selection')), ([], []))
            self.assertEqual(reader.change_join(self.fixture('change'), self.fixture('before'),
                                                self.fixture('after'), self.fixture('change-selection'),
                                                self.fixture('rerun')), ([], []))
            after = self.fixture('after'); after['outcome'] = 'pass'
            errors, _ = reader.change_join(self.fixture('change'), self.fixture('before'), after,
                                            self.fixture('change-selection'), self.fixture('rerun'))
            self.assertIn('CHANGE-HISTORY-MUTATED', [e['code'] for e in errors])
        self.assertEqual(self.fixture('rerun')['support_revision']['exp_version'], 'EXP-v0.2')

    def test_imported_modules_cannot_substitute_for_pinned_legacy_or_rules(self):
        fake = types.ModuleType('admission_rules')
        fake.review_violations = fake.rule_violations = fake.impact_violations = lambda *args: []
        fake.Support = lambda *args, **kwargs: self.fail('caller module used')
        with patch.dict(sys.modules, {'admission_rules': fake, 'admission_check': fake}):
            selected = current.Support(profile=current.PROFILE)
            review = self.fixture('review')
            review['reviewer']['identity'] = review['authors'][0]['identity']
            self.assertIn('EXP-R6', [e['code'] for e in selected.validate('review', review)])
            self.assertIs(sys.modules['admission_rules'], fake)

    def test_dependency_byte_changes_refuse_before_execution(self):
        for name in current.DEPENDENCIES:
            (self.root / name).write_bytes((HERE / name).read_bytes())
        for name in current.DEPENDENCIES:
            path = self.root / name; raw = path.read_bytes()
            path.write_bytes(raw + b'\nraise AssertionError("untrusted dependency executed")\n')
            with patch.object(current, 'HERE', self.root):
                with self.assertRaisesRegex(ValueError, 'dependency drift'):
                    current.Support(profile=current.PROFILE)
            path.write_bytes(raw)

    def test_internal_errors_are_not_relabelled_as_bad_input(self):
        args = ['--profile', current.PROFILE, 'validate', 'review',
                str(APP / 'tests/group_b_admission_fixtures/review.json')]
        for error in (TypeError('invented internal type failure'), KeyError('invented internal lookup')):
            output = io.StringIO()
            with self.subTest(error=type(error)), patch.object(current, 'Support', side_effect=error):
                with contextlib.redirect_stdout(output), self.assertRaises(type(error)):
                    current.main(args)
                self.assertEqual(output.getvalue(), '')

    def test_cli_requires_profile_and_reports_current_selection_without_new_acts(self):
        cli = [sys.executable, '-B', str(HERE / 'current_admission.py')]
        args = ['validate', 'review', str(APP / 'tests/group_b_admission_fixtures/review.json')]
        for prefix in ([], ['--profile', 'historical-v1'], ['--profile', 'unknown']):
            result = subprocess.run(cli + prefix + args, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
        result = subprocess.run(cli + ['--profile', current.PROFILE] + args, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['source_selection'], self.support.source_selection)
        self.assertFalse(report['review_or_repair_verified'])
        self.assertEqual(report['route_admission'], 'not_established')
        self.assertNotIn('qualification_established', report)
        # Caller-supplied record metadata cannot choose this source profile.
        review = self.fixture('review'); review['source_selection'] = self.support.source_selection
        self.assertIn('SCHEMA', [e['code'] for e in self.support.validate('review', review)])


if __name__ == '__main__':
    unittest.main()
