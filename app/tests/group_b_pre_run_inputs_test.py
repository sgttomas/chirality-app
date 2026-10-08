"""Exact preparation only: no executed result, installed origin or native observation."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

APP = Path(__file__).resolve().parents[1]
WRAPPER = APP / 'examination/native_forms/pre_run_form.py'
HELPER = APP / 'examination/standalone/pre_run_inputs.py'
spec = importlib.util.spec_from_file_location('b7_pre_run_wrapper_tests', WRAPPER)
wrapper = importlib.util.module_from_spec(spec); spec.loader.exec_module(wrapper)


def encoded(value): return (json.dumps(value, indent=2) + '\n').encode()


class PreRunInputsTests(unittest.TestCase):
    def setUp(self):
        self.api = wrapper.consumer(); self.inputs = self.api.PreRunInputs(); self.addCleanup(self.inputs.close)
        self.plan = encoded(self.inputs.producer.prepare())
        self.selection = self.inputs.freeze(self.plan, self.api.sha(self.plan))
        self.selected = encoded(self.selection); self.selected_sha = self.api.sha(self.selected)
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def check(self, value):
        payload = encoded(value)
        return self.inputs.check(payload, self.api.sha(payload), self.plan)

    def test_connected_all_cases_preserve_original_blank_and_missing_inputs(self):
        self.inputs.check(self.selected, self.selected_sha, self.plan)
        self.assertEqual(len(self.selection['fixture_roles']), 13)
        self.assertIsNone(self.selection['candidate_slot']['revision'])
        self.assertEqual(self.selection['missing_inputs'], self.api.parse(self.plan)['missing_inputs'])
        for case in ('V4-EXM-10', 'V4-EXM-11', 'V4-EXM-12'):
            with self.subTest(case=case):
                original = self.inputs.forms.generate(self.api.parse(self.plan), case)
                result = wrapper.generate(self.api, self.inputs, self.plan, self.selected, self.selected_sha, case)
                self.assertTrue(result.startswith(original))
                self.assertIn('Exact input preparation attachment', result)
                for field in ('Record id', 'Candidate revision', 'Build identity', 'Person operating', 'Date'):
                    self.assertIn(field + ': __________', result)
                self.assertIn(self.selected_sha, result)
                self.assertIn('J-1 starts in an empty project', result)
        self.assertFalse(self.selection['support_selection']['producer_use_verified'])
        self.assertFalse(self.selection['support_selection']['result_consumer_adoption'])

    def test_exact_plan_bytes_and_exact_selection_digest_are_required(self):
        with self.assertRaisesRegex(ValueError, 'plan digest mismatch'):
            self.inputs.freeze(self.plan + b'\n', self.api.sha(self.plan))
        with self.assertRaisesRegex(ValueError, 'plan digest mismatch'):
            self.inputs.check(self.selected, self.selected_sha, self.plan + b'\n')
        with self.assertRaisesRegex(ValueError, 'selection digest mismatch'):
            self.inputs.check(self.selected + b'\n', self.selected_sha, self.plan)
        changed = self.api.parse(self.plan); changed['candidate_slot']['revision'] = 'invented-readiness'
        data = encoded(changed)
        with self.assertRaisesRegex(ValueError, 'preserved B7 preparation'):
            self.inputs.freeze(data, self.api.sha(data))

    def test_missing_extra_or_duplicated_fixture_roles_refuse(self):
        for mutate in (lambda x: x['fixture_roles'].pop('collision_workflow'),
                       lambda x: x['fixture_roles'].update(extra=copy.deepcopy(x['fixture_roles']['initial_input'])),
                       lambda x: x['fixture_roles'].update(reuse_input=copy.deepcopy(x['fixture_roles']['initial_input']))):
            value = copy.deepcopy(self.selection); mutate(value)
            with self.assertRaisesRegex(ValueError, 'complete fixed preparation'): self.check(value)

    def test_changed_support_tuple_method_or_source_manifest_refuse(self):
        mutations = [lambda x: x['support_selection']['support_identity']['schema_ids'].update(review='different'),
                     lambda x: x['support_selection'].update(declaration_sha256='0' * 64),
                     lambda x: x['support_selection'].update(method='OTHER'),
                     lambda x: x['source_files'].pop(next(iter(x['source_files']))),
                     lambda x: x.update(source_pins_sha256='0' * 64)]
        for mutate in mutations:
            value = copy.deepcopy(self.selection); mutate(value)
            with self.assertRaises(ValueError): self.check(value)

    def test_readiness_results_and_extra_fields_cannot_be_injected(self):
        for mutate in (lambda x: x.update(examination_opened=True),
                       lambda x: x.update(result={'outcome': 'pass'}),
                       lambda x: x['support_selection'].update(producer_use_verified=True),
                       lambda x: x['fixture_roles']['initial_input'].update(installed_origin='user'),
                       lambda x: x.update(preparation_version=True)):
            value = copy.deepcopy(self.selection); mutate(value)
            with self.assertRaises(ValueError): self.check(value)

    def test_changed_fixture_bytes_refuse_even_when_new_file_is_valid(self):
        relative = self.inputs.pins['fixture_roles']['revision_1_workflow']['path']
        target = self.inputs.snapshot / relative
        target.write_bytes(target.read_bytes() + b'\n')
        with patch.object(self.api, 'ROOT', self.inputs.snapshot):
            with self.assertRaisesRegex(ValueError, 'fixture drift'): self.api.PreRunInputs()
        target.unlink()
        with patch.object(self.api, 'ROOT', self.inputs.snapshot):
            with self.assertRaises(OSError): self.api.PreRunInputs()

    def test_unlisted_fixture_companions_and_directories_refuse(self):
        directory = self.inputs.snapshot / 'projects/chirality-app-v4/app/examination/standalone/fixtures/revision-1/invented-pipe-inventory'
        extra = directory / 'extra.py'; extra.write_text('unexpected companion')
        with patch.object(self.api, 'ROOT', self.inputs.snapshot):
            with self.assertRaisesRegex(ValueError, 'unexpected fixture file'): self.api.PreRunInputs()
        extra.unlink(); extra.mkdir()
        with patch.object(self.api, 'ROOT', self.inputs.snapshot):
            with self.assertRaisesRegex(ValueError, 'unexpected fixture directory'): self.api.PreRunInputs()

    def test_actual_source_and_helper_pin_drift_refuse(self):
        target = self.inputs.snapshot / 'projects/chirality-app-v4/app/examination/standalone/prepare.py'
        target.write_bytes(target.read_bytes() + b'\n')
        with patch.object(self.api, 'ROOT', self.inputs.snapshot):
            with self.assertRaisesRegex(ValueError, 'source drift'): self.api.PreRunInputs()
        with patch.object(self.api, 'PINS_SHA256', '0' * 64):
            with self.assertRaisesRegex(ValueError, 'pins changed'): self.api.PreRunInputs()
        with patch.object(wrapper, 'PINS_SHA256', '0' * 64):
            with self.assertRaisesRegex(ValueError, 'pins changed'): wrapper.consumer()

    def test_symlink_components_special_files_and_traversal_refuse(self):
        actual = self.root / 'actual'; actual.write_bytes(self.plan)
        link = self.root / 'link'; link.symlink_to(actual)
        with self.assertRaises(OSError): self.api.read_file(link)
        folder = self.root / 'dir'; folder.mkdir(); (folder / 'plan').write_bytes(self.plan)
        alias = self.root / 'alias'; alias.symlink_to(folder, target_is_directory=True)
        with self.assertRaises(OSError): self.api.read_file(alias / 'plan')
        with self.assertRaisesRegex(ValueError, 'traversal'): self.api.read_file(folder / '..' / 'actual')
        with self.assertRaises(ValueError): self.api.relative_file(self.root, '../actual')
        fifo = self.root / 'fifo'; os.mkfifo(fifo)
        with self.assertRaisesRegex(ValueError, 'regular file'): self.api.read_file(fifo)
        # A fixture symlink with identical target bytes is not an acceptable substitute.
        relative = self.inputs.pins['fixture_roles']['initial_input']['path']
        fixture = self.inputs.snapshot / relative
        actual.write_bytes(fixture.read_bytes()); fixture.unlink(); fixture.symlink_to(actual)
        with patch.object(self.api, 'ROOT', self.inputs.snapshot):
            with self.assertRaises((OSError, ValueError)): self.api.PreRunInputs()

    def test_duplicate_json_keys_and_nonfinite_values_refuse(self):
        for data in (b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}'):
            with self.assertRaises(ValueError): self.api.parse(data)
        malicious = self.selected.replace(b'"preparation_version": 1', b'"preparation_version": 1, "preparation_version": 1')
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            self.inputs.check(malicious, self.api.sha(malicious), self.plan)

    def test_unknown_case_and_completed_form_are_not_preparation(self):
        with self.assertRaisesRegex(ValueError, 'unknown standalone case'):
            wrapper.generate(self.api, self.inputs, self.plan, self.selected, self.selected_sha, 'OTHER')
        form = wrapper.generate(self.api, self.inputs, self.plan, self.selected, self.selected_sha, 'V4-EXM-10')
        changed = form.replace('Person operating: __________', 'Person operating: invented actor')
        self.assertNotEqual(form, changed)
        self.run_cli_check(changed.encode(), expected_exit=1)

    def run_cli_check(self, form, expected_exit=0, form_sha=None):
        for name, data in [('plan.json', self.plan), ('selection.json', self.selected), ('form.md', form)]:
            (self.root / name).write_bytes(data)
        command = [sys.executable, '-B', str(WRAPPER), 'check-blank', '--plan', str(self.root / 'plan.json'),
                   '--selection', str(self.root / 'selection.json'), '--selection-sha256', self.selected_sha,
                   '--case', 'V4-EXM-10', '--form', str(self.root / 'form.md'),
                   '--form-sha256', form_sha or self.api.sha(form)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, expected_exit, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        for flag in ('native_run_observed', 'result_recorded', 'qualification_claim'): self.assertFalse(report[flag])
        return report

    def test_real_cli_connected_generation_and_exact_form_check(self):
        (self.root / 'plan.json').write_bytes(self.plan)
        result = subprocess.run([sys.executable, '-B', str(HELPER), 'freeze', '--plan', str(self.root / 'plan.json'),
                                 '--plan-sha256', self.api.sha(self.plan)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout), self.selection)
        (self.root / 'selection.json').write_bytes(self.selected)
        command = [sys.executable, '-B', str(WRAPPER), 'generate', '--plan', str(self.root / 'plan.json'),
                   '--selection', str(self.root / 'selection.json'), '--selection-sha256', self.selected_sha, '--case', 'V4-EXM-10']
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(self.run_cli_check(result.stdout.encode())['blank_preparation_matches'])
        self.run_cli_check(result.stdout.encode(), expected_exit=2, form_sha='0' * 64)


if __name__ == '__main__': unittest.main(verbosity=2)
