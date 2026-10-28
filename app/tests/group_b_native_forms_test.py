import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

APP = Path(__file__).resolve().parents[1]
PATH = APP / 'examination/native_forms/native_form.py'
spec = importlib.util.spec_from_file_location('group_b_native_form_subject', PATH)
forms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(forms)


class NativeForms(unittest.TestCase):
    def setUp(self):
        self.plan = forms.consumer().prepare()

    def test_all_cases_order_and_blank_rows(self):
        for scenario in self.plan['scenarios']:
            text = forms.generate(self.plan, scenario['scenario'])
            rows = [line for line in text.splitlines() if line.startswith('| ')][1:]
            self.assertEqual(rows, ['| ' + s['step'] + ' | | | | | |' for s in scenario['steps']])
            for field in ['Person operating', 'Examiner recording', 'Date', 'Time zone', 'Candidate revision', 'Build identity']:
                self.assertIn(field + ': __________', text)
            self.assertIn('not reconstructed: __________', text)

    def test_wrong_source(self):
        self.plan['sources'][0]['sha256'] = 'sha256:' + '0'*64
        with self.assertRaises(ValueError): forms.generate(self.plan, 'V4-EXM-10')

    def test_wrong_case(self):
        with self.assertRaises(ValueError): forms.generate(self.plan, 'V4-EXM-04')

    def test_order_change(self):
        self.plan['scenarios'][0]['steps'].reverse()
        with self.assertRaises(ValueError): forms.generate(self.plan, 'V4-EXM-10')

    def test_candidate_injection(self):
        self.plan['candidate_slot']['revision'] = 'invented-candidate'
        with self.assertRaises(ValueError): forms.generate(self.plan, 'V4-EXM-10')

    def test_missing_step(self):
        self.plan['scenarios'][0]['steps'].pop()
        with self.assertRaises(ValueError): forms.generate(self.plan, 'V4-EXM-10')

    def test_source_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(OSError): forms.generate(self.plan, 'V4-EXM-10', Path(tmp))

    def test_cli_actual_b7_consumption_and_refusals(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp)/'plan.json'; form = Path(tmp)/'form.md'
            prepared = subprocess.run([sys.executable, str(APP/'examination/standalone/prepare.py'), 'prepare'], capture_output=True, text=True, check=True)
            plan.write_text(prepared.stdout)
            base = [sys.executable, str(PATH)]
            selection = ['--plan', str(plan), '--case', 'V4-EXM-11']
            result = subprocess.run(base+['generate']+selection, capture_output=True, text=True, check=True)
            form.write_text(result.stdout)
            command = base+['check-blank']+selection+['--form', str(form)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            for old,new in [('S11-1 |','S11-2 |'), ('Candidate revision: __________','Candidate revision: invented'), ('| S11-1 | | | | | |','| S11-1 | | | passed | | |')]:
                form.write_text(result.stdout.replace(old,new,1))
                self.assertEqual(subprocess.run(command,capture_output=True).returncode,1)
            form.write_text(forms.generate(self.plan,'V4-EXM-10'))
            self.assertEqual(subprocess.run(command,capture_output=True).returncode,1)


if __name__ == '__main__': unittest.main()
