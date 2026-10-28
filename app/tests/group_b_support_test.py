"""Invented offline inputs; no native claim is established by these tests."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP / 'examination'))
import check as support_module
from check import Support, parse


class GroupBSupport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.support = Support()

    def setUp(self):
        self.result = json.loads((APP / 'tests/group_b_fixtures/result.json').read_text())
        self.package = json.loads((APP / 'tests/group_b_fixtures/package.json').read_text())
        self.result['support_revision']['prototype_digest'] = self.support.prototype_digest

    def link(self):
        return self.support.package_link(self.result, self.package, 'INVENTED-REVISION', 'INVENTED-BUILD', '0.160.0', 'INVENTED-PACKAGE')

    def test_not_run_pair_is_consistent_but_not_reliance(self):
        errors, gaps = self.link()
        self.assertEqual(errors, [])
        self.assertEqual(len(gaps), 4)
        self.assertTrue(any('fp3' in gap for gap in gaps))

    def test_all_canonical_examples_and_false_pass_vectors(self):
        for kind, filename in support_module.SCHEMAS.items():
            source = next(p for p in self.support.sources['sources'] if p.endswith('/' + filename))
            directory = support_module.PROJECT / Path(source).parent
            prefix = filename.removesuffix('.schema.json')
            for record in json.loads((directory / f'{prefix}.valid.examples.json').read_text()):
                with self.subTest(kind=kind, record=record['record_id']):
                    self.assertEqual(self.support.validate(kind, record), [])
            for suffix in ('invalid', 'rule-violations'):
                for item in json.loads((directory / f'{prefix}.{suffix}.examples.json').read_text()):
                    with self.subTest(kind=kind, case=item['record']['record_id']):
                        got = self.support.validate(kind, item['record'])
                        self.assertTrue(got)
                        if suffix == 'rule-violations':
                            self.assertIn(item['rule'], [e['code'] for e in got])

    def test_build_revision_pin_reference_and_support_cannot_drift(self):
        mutations = [
            ('LINK-BUILD', lambda: self.package['app'].update(build_identity='other')),
            ('LINK-REVISION', lambda: self.result['subject']['app_candidate'].update(revision='other')),
            ('LINK-PIN', lambda: self.package['codex'].update(pin='0.158.0')),
            ('LINK-PACKAGE-REFERENCE', lambda: self.result['subject']['app_candidate'].update(package_record='other')),
            ('LINK-SUPPORT-VERSION', lambda: self.package.update(support_revision='EXP-v9.9')),
            ('LINK-SUPPORT-SCHEMA', lambda: self.result['support_revision'].update(schema_id='other')),
            ('LINK-SUPPORT-DIGEST', lambda: self.result['support_revision'].pop('prototype_digest')),
            ('LINK-HISTORICAL-RESULT', lambda: self.result.update(currency={'state':'historical','change_ref':'changed'})),
        ]
        for code, mutate in mutations:
            self.setUp()
            mutate()
            with self.subTest(code=code):
                self.assertIn(code, [e['code'] for e in self.link()[0]])

    def test_claiming_fp_success_cannot_establish_native_origin(self):
        for key in ('fp1a', 'fp1b', 'fp3'):
            self.package['first_package_checks'][key]['outcome'] = 'pass'
        self.result['outcome'] = 'pass'
        self.result.pop('not_run_because')
        errors, gaps = self.link()
        self.assertEqual(errors, [])
        self.assertEqual(gaps, [])
        # The CLI must still explicitly withhold reliance even for such claims.
        with tempfile.TemporaryDirectory() as temp:
            paths = []
            for name, value in [('result',self.result), ('package',self.package)]:
                path=Path(temp)/f'{name}.json'; path.write_text(json.dumps(value)); paths.append(str(path))
            proc = subprocess.run([sys.executable, str(APP/'examination/check.py'), 'package-link', *paths,
                '--revision','INVENTED-REVISION','--build','INVENTED-BUILD','--pin','0.160.0',
                '--package-ref','INVENTED-PACKAGE'], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            output=json.loads(proc.stdout)
            self.assertEqual(output['option_b_reliance'], 'not_established_by_file_check')
            self.assertEqual(output['native_qualification'], 'not_established_by_file_check')
            self.assertEqual(len(output['inputs']), 2)

    def test_native_part_cannot_pass_on_browser_evidence(self):
        self.result['outcome']='pass'
        self.result['parts']=[{'part':'W-0','expectation':'native observation','outcome':'pass','needs_native':True,
            'evidence':[{'ref':'invented','provenance':'live_observation','route':'interface_chromium'}]}]
        self.assertIn('EXP-R4', [e['code'] for e in self.support.validate('result', self.result)])

    def test_hidden_failure_and_not_applicable_overlap(self):
        self.result['outcome']='pass'
        self.result['parts']=[{'part':'W-0','expectation':'invented','outcome':'fail'}]
        self.assertIn('EXP-R1', [e['code'] for e in self.support.validate('result',self.result)])
        self.result['parts'][0]['outcome']='pass'
        self.result['parts_not_applicable']=[{'part':'W-0','reason':'invented','declared_in':{'case_definition':'invented','identity':'sha256:'+'0'*64}}]
        self.assertIn('EXP-R1', [e['code'] for e in self.support.validate('result',self.result)])

    def test_source_drift_refuses_before_record_validation(self):
        manifest=copy.deepcopy(self.support.sources)
        first=next(iter(manifest['sources']))
        manifest['sources'][first]['sha256']='0'*64
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'sources.json'; path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError,'canonical source changed'):
                Support(manifest=path)

    def test_duplicate_keys_and_non_json_constants_refused(self):
        for data in ('{"outcome":"fail","outcome":"pass"}', '{"x":NaN}'):
            with self.assertRaises(ValueError): parse(data)

    def test_cli_schema_rejection_exit(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'invalid.json'; path.write_text('{}')
            proc=subprocess.run([sys.executable,str(APP/'examination/check.py'),'validate','result',str(path)], capture_output=True,text=True)
            self.assertEqual(proc.returncode,1)
            self.assertFalse(json.loads(proc.stdout)['file_checks_passed'])

    def test_cli_input_error_exit_and_no_rewrite(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'bad.json'; path.write_text('{')
            proc=subprocess.run([sys.executable,str(APP/'examination/check.py'),'validate','result',str(path)], capture_output=True,text=True)
            self.assertEqual(proc.returncode,2)
            self.assertFalse(json.loads(proc.stdout)['file_checks_passed'])
            self.assertEqual(path.read_text(),'{')


if __name__ == '__main__':
    unittest.main(verbosity=2)
