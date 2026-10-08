"""Preparation invariants: these tests execute no native journey or supplier."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

APP = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('standalone_preparation', APP / 'examination/standalone/prepare.py')
prep = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prep)


class StandalonePreparationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = prep.prepare()

    def rejects(self, mutate):
        changed = copy.deepcopy(self.plan)
        mutate(changed)
        self.assertTrue(prep.validate(changed))

    def test_exact_source_map_and_counts(self):
        lock = prep.verified_sources()
        path = next(x['path'] for x in lock['sources'] if x['role'] == 'step_map')
        source = json.loads((prep.ROOT / path).read_text())
        self.assertEqual(self.plan['stimuli'], source['stimuli'])
        for scenario in self.plan['scenarios']:
            steps = source['scenarios'][scenario['scenario']]
            self.assertEqual([{k: row[k] for k in original} for row, original in zip(scenario['steps'], steps)], steps)
        self.assertEqual([len(x['steps']) for x in self.plan['scenarios']], [11, 6, 6])
        self.assertEqual(sum(x['counts'] for s in self.plan['scenarios'] for x in s['steps']), 21)
        self.assertEqual(prep.validate(self.plan), [])

    def test_dropped_reordered_and_recounted_steps(self):
        for scenario in range(3):
            with self.subTest(scenario=scenario):
                self.rejects(lambda p: p['scenarios'][scenario]['steps'].pop(0))
                self.rejects(lambda p: p['scenarios'][scenario]['steps'].reverse())
        self.rejects(lambda p: p['scenarios'][0]['steps'][8].update(counts=True))

    def test_stimuli_and_supplier_case_omissions(self):
        self.rejects(lambda p: p['stimuli'].pop())
        self.assertIn('ST-4', self.plan['scenarios'][0]['steps'][1]['stimuli'])
        self.rejects(lambda p: p['scenarios'][0]['steps'][1]['stimuli'].remove('ST-4'))
        self.rejects(lambda p: p['scenarios'][1]['steps'][5]['stimuli'].remove('ST-5'))
        self.rejects(lambda p: p['scenarios'][0]['steps'][5]['supplier_cases'].pop())
        self.rejects(lambda p: p['stimuli'][4].update(replay_counterpart='constructed VC-R-04 stub'))
        for index in range(3):
            self.rejects(lambda p: p['stimuli'][index].update(replay_counterpart='recording'))

    def test_no_native_or_replay_substitution(self):
        for route in ('interface_webkit', 'interface_chromium', 'seam_replay', 'model_only'):
            self.rejects(lambda p: p['scenarios'][0]['steps'][0].update(native_evidence_kinds=[route]))
        self.rejects(lambda p: p['scenarios'][0]['steps'][0].update(required_native_route='N-2'))

    def test_no_fabricated_readiness_opening_or_outcome(self):
        for field, value in [('ready', True), ('examination_opened', '2026-10-08'), ('outcome', 'pass'),
                             ('handed_over', True), ('reported_as_independent', True)]:
            self.rejects(lambda p: p.update({field: value}))
        for state in ('planned', 'recorded', 'held', 'run'):
            self.rejects(lambda p: p['scenarios'][0]['steps'][0].update(state=state))
        self.rejects(lambda p: p['scenarios'][0]['steps'][0].update(outcome='not-run'))
        self.rejects(lambda p: p['scenarios'][0].update(outcome='pass'))
        self.rejects(lambda p: p['missing_inputs'].clear())

    def test_same_candidate_run_and_modes(self):
        self.assertEqual([s['run_label'] for s in self.plan['scenarios']], ['RUN-A', 'RUN-A', 'RUN-B'])
        self.rejects(lambda p: p['scenarios'][1].update(run_label='different-run'))
        self.rejects(lambda p: p['scenarios'][2].update(candidate_slot='another-candidate'))
        self.rejects(lambda p: p['candidate_slot'].update(build_identity=p['source_basis_revision']))
        self.rejects(lambda p: p['access_mode_requirements'].update(distinct_conversations=1))
        self.rejects(lambda p: p['access_mode_requirements']['kinds'].remove('api_key'))

    def test_prose_preconditions_and_insertion_points(self):
        cases = self.plan['requirements']['## 3. Case definitions']
        self.assertIn('no request raised', cases)
        self.assertIn('constructed', cases)
        self.assertIn('candidate', cases)
        self.assertIn('delegates one bounded sub-task', self.plan['scenarios'][0]['steps'][1]['source_action_observation'][0])
        insertions = self.plan['scenarios'][1]['steps']
        self.assertIn("During J-2", insertions[0]['source_action_observation'][0])
        self.assertIn("During J-8's try conversation", insertions[4]['source_action_observation'][0])
        self.rejects(lambda p: p['requirements'].pop('## 3. Case definitions'))
        self.rejects(lambda p: p['scenarios'][1]['steps'][4].update(source_action_observation=['after RUN-A']))

    def test_source_drift_refuses_generation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for item in prep.verified_sources()['sources']:
                target = root / item['path']
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((prep.ROOT / item['path']).read_bytes())
            self.assertEqual(prep.prepare(root), self.plan)
            target.write_text('changed source')
            with self.assertRaisesRegex(ValueError, 'source changed'):
                prep.prepare(root)

    def test_cli_roundtrip_rejection_and_duplicate_keys(self):
        command = [sys.executable, str(APP / 'examination/standalone/prepare.py')]
        result = subprocess.run(command + ['prepare'], capture_output=True, text=True, check=True)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'plan.json'
            path.write_text(result.stdout)
            good = subprocess.run(command + ['check', str(path)], capture_output=True, text=True)
            self.assertEqual(good.returncode, 0)
            self.assertFalse(json.loads(good.stdout)['qualification_claim'])
            bad = json.loads(result.stdout)
            bad['examination_opened'] = '2026-10-08'
            path.write_text(json.dumps(bad))
            self.assertEqual(subprocess.run(command + ['check', str(path)], capture_output=True).returncode, 1)
            path.write_text('{"standing":"test_definition_only","standing":"pass"}')
            self.assertEqual(subprocess.run(command + ['check', str(path)], capture_output=True).returncode, 1)


if __name__ == '__main__':
    unittest.main()
