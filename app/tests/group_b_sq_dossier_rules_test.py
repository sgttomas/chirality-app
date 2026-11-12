"""Illustrative SQ-v0.2 dossiers; a pass shows the rules run as written, not a qualification."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator

APP = Path(__file__).resolve().parents[1]
SQ = APP / 'examination/sq_receiving'
EXAMPLES = APP / 'tests/group_b_fixtures'
CORE_LOOP = {'planning', 'execution', 'workflow saving', 'reuse', 'approvals', 'interruption', 'restart'}


def load_rules():
    spec = importlib.util.spec_from_file_location('group_b_sq_dossier_rules', SQ / 'sq_dossier_rules.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


class SQDossierRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = load_rules()
        schema = read(SQ / 'sq.dossier.schema.json')
        Draft202012Validator.check_schema(schema)
        cls.validator = Draft202012Validator(schema)
        cls.step_map = read(SQ / 'sq.step-map.json')
        cls.steps = [step for name, steps in cls.step_map['scenarios'].items() for step in steps
                     if name not in cls.rules.JOURNEYS]
        cls.journey_steps = [step for name in cls.rules.JOURNEYS for step in cls.step_map['scenarios'][name]]
        cls.valid = read(EXAMPLES / 'sq.dossier.valid.examples.json')
        cls.invalid = read(EXAMPLES / 'sq.dossier.invalid.examples.json')
        cls.rule_violations = read(EXAMPLES / 'sq.dossier.rule-violations.examples.json')

    def violations(self, dossier):
        return self.rules.violations(dossier, self.step_map)

    def test_step_map_covers_the_core_loop_and_declares_its_stimuli(self):
        self.assertEqual(list(self.step_map['scenarios']), self.rules.SCENARIOS + self.rules.JOURNEYS)
        self.assertLessEqual(CORE_LOOP, {step['core_loop_element'] for step in self.steps})
        self.assertTrue(all(step.get('v3_reference') for step in self.steps))
        declared = {stimulus['id'] for stimulus in self.step_map['stimuli']}
        self.assertEqual(declared, {name for step in self.steps for name in step['stimuli']})
        for step in self.steps:
            with self.subTest(step=step['step']):
                # An added step is not counted and gives its reason.
                self.assertEqual(not step['counts'], step['step'].endswith('R'))
                self.assertTrue(step['counts'] or step.get('added_reason'))
                # M12-2's and M12-5's cases were API-key or three-mode cases, removed with that mode;
                # no surviving case covers the local key or the two-mode switch.
                self.assertEqual(not step['supplier_cases'], step['step'] in {'M12-2', 'M12-5'})
        cited = [case['case_id'] for step in self.steps for case in step['supplier_cases']]
        self.assertNotIn('VC-AAC-04', cited)
        for step in self.step_map['scenarios']['V4-EXM-11']:
            self.assertIn('VC-R-14', [case['case_id'] for case in step['supplier_cases']], step['step'])
        self.assertEqual({step['step'] for step in self.steps if 'ST-4' in step['stimuli']},
                         {'J-2', 'S11-1', 'S11-6'})

    def test_journey_steps_cite_governing_criteria_not_supplier_cases(self):
        self.assertEqual([s['step'] for s in self.journey_steps],
                         ['J1-%d' % n for n in range(1, 7)] + ['J2-%d' % n for n in range(1, 8)])
        for step in self.journey_steps:
            with self.subTest(step=step['step']):
                self.assertEqual(step['supplier_cases'], [])
                self.assertEqual(step['stimuli'], [])
                self.assertTrue(step['counts'])
                self.assertTrue(all(set(c) == {'deliverable', 'criterion'} for c in step['governing_criteria']))
                self.assertNotIn('core_loop_element', step)
        cited = {(c['deliverable'], c['criterion']) for s in self.journey_steps for c in s['governing_criteria']}
        self.assertLessEqual({('DEL-09-02', 'AC-009'), ('DEL-09-02', 'AC-010'), ('DEL-02-02', 'AC-010'),
                              ('DEL-02-02', 'AC-011'), ('DEL-02-02', 'AC-005'), ('DEL-01-04', 'AC-011'),
                              ('DEL-01-04', 'AC-003'), ('DEL-02-03', 'AC-001')}, cited)

    def test_valid_dossiers_pass_schema_and_every_rule(self):
        self.assertEqual([d['record_id'] for d in self.valid], ['SQ-EX-0%d' % n for n in range(1, 8)])
        for dossier in self.valid:
            with self.subTest(record=dossier['record_id']):
                self.assertEqual([s['scenario'] for s in dossier['scenarios']],
                                 self.rules.SCENARIOS + self.rules.JOURNEYS)
                self.assertEqual([e.message for e in self.validator.iter_errors(dossier)], [])
                self.assertEqual(self.violations(dossier), [])

    def test_an_agent_operated_journey_is_recorded_as_such(self):
        dossier = next(d for d in self.valid if d['record_id'] == 'SQ-EX-07')
        for journey in (s for s in dossier['scenarios'] if s['scenario'] in self.rules.JOURNEYS):
            self.assertEqual(journey['basis'], 'agent_operated')
            for step in journey['steps']:
                self.assertEqual(step['operation']['operator']['kind'], 'agent')
                self.assertEqual(step['operation']['means'], 'app_controls_by_computer_use')
        # The same journey stated as a person observed is refused, and so is one agent step in a person's journey.
        probe = copy.deepcopy(dossier)
        next(s for s in probe['scenarios'] if s['scenario'] == 'J1')['basis'] = 'person_observed'
        self.assertEqual(self.violations(probe), ['SQ-R13'])
        person = next(d for d in self.valid if d['record_id'] == 'SQ-EX-03')
        self.assertEqual({s['basis'] for s in person['scenarios'] if s['scenario'] in self.rules.JOURNEYS}, {'person_observed'})
        probe = copy.deepcopy(person)
        step = next(s for s in probe['scenarios'] if s['scenario'] == 'J2')['steps'][0]
        step['operation']['means'] = 'not_through_app_controls'
        self.assertEqual(self.violations(probe), ['SQ-R13', 'SQ-R14'])
        step['outcome'] = 'blocked'
        next(s for s in probe['scenarios'] if s['scenario'] == 'J2').update(basis='not_established', outcome='blocked')
        self.assertEqual(self.violations(probe), [])

    def test_operator_and_means_must_agree_in_the_schema(self):
        dossier = copy.deepcopy(next(d for d in self.valid if d['record_id'] == 'SQ-EX-03'))
        operation = next(s for s in dossier['scenarios'] if s['scenario'] == 'J1')['steps'][0]['operation']
        operation['means'] = 'app_controls_by_computer_use'
        self.assertTrue(list(self.validator.iter_errors(dossier)))
        operation.update(means='app_controls_by_hand', operator={'kind': 'agent', 'identity': 'ILLUSTRATIVE agent'})
        self.assertTrue(list(self.validator.iter_errors(dossier)))
        dossier = copy.deepcopy(next(d for d in self.valid if d['record_id'] == 'SQ-EX-01'))
        next(s for s in dossier['scenarios'] if s['scenario'] == 'J1').pop('basis')
        self.assertTrue(list(self.validator.iter_errors(dossier)))

    def test_invalid_dossiers_are_refused_by_the_schema(self):
        self.assertEqual(len(self.invalid), 9)
        for item in self.invalid:
            with self.subTest(record=item['record']['record_id'], why=item['why']):
                self.assertTrue(list(self.validator.iter_errors(item['record'])))

    def test_schema_valid_rule_violations_are_detected(self):
        self.assertEqual({item['rule'] for item in self.rule_violations},
                         {'SQ-R%d' % n for n in range(1, 15)} - {'SQ-R10'})
        for item in self.rule_violations:
            with self.subTest(record=item['record']['record_id'], rule=item['rule']):
                self.assertEqual([e.message for e in self.validator.iter_errors(item['record'])], [])
                self.assertIn(item['rule'], self.violations(item['record']))
        # Each journey refusal shows its own rule alone.
        for item in self.rule_violations:
            if item['rule'] in ('SQ-R11', 'SQ-R12', 'SQ-R13', 'SQ-R14'):
                self.assertEqual(self.violations(item['record']), [item['rule']], item['why'])

    def test_paired_st4_probes_at_j2_are_not_masked(self):
        # Paired probes prevent another stimulus or rule failure from masking omission.
        baseline = next(d for d in self.valid if d['record_id'] == 'SQ-EX-03')
        for produced, outcome, expected in [(None, 'pass', ['SQ-R9']),
                                            ('not_produced', 'pass', ['SQ-R9']),
                                            ('not_produced', 'blocked', []),
                                            ('replay', 'pass', [])]:
            probe = copy.deepcopy(baseline)
            scenario = next(s for s in probe['scenarios'] if s['scenario'] == 'V4-EXM-10')
            step = next(s for s in scenario['steps'] if s['step'] == 'J-2')
            step['stimuli'] = ([] if produced is None else
                               [{'id': 'ST-4', 'produced': produced,
                                 **({'cause': 'ILLUSTRATIVE delegation and recording unavailable'}
                                    if produced == 'not_produced' else
                                    {'evidence': 'ILLUSTRATIVE recorded delegation counterpart'})}])
            step['outcome'] = outcome
            scenario['outcome'] = self.rules.aggregate([s['outcome'] for s in scenario['steps'] if s['counts']])
            with self.subTest(produced=produced, outcome=outcome):
                self.assertEqual([e.message for e in self.validator.iter_errors(probe)], [])
                self.assertEqual(self.violations(probe), expected)

    def test_run_b_accepts_the_two_modes_and_refuses_a_third(self):
        two = copy.deepcopy(self.valid[0])
        modes = next(s for s in two['scenarios'] if s['scenario'] == 'V4-EXM-12')['access_modes']
        self.assertEqual([(m['kind'], m['home']) for m in modes],
                         [('chatgpt_account', 'H-acct'), ('local_provider', 'H-omlx')])
        self.assertEqual([e.message for e in self.validator.iter_errors(two)], [])
        self.assertEqual(self.violations(two), [])
        # A three-mode dossier with standalone API-key access in H-key is refused by the schema and SQ-R3.
        three = next(item['record'] for item in self.invalid if item['record']['record_id'] == 'SQ-INV-09')
        self.assertTrue(list(self.validator.iter_errors(three)))
        self.assertIn('SQ-R3', self.violations(three))
        # A third mode of an admitted kind is schema-valid and refused by SQ-R3.
        extra = next(item for item in self.rule_violations if item['record']['record_id'] == 'SQ-RV-13')
        self.assertEqual(len(next(s for s in extra['record']['scenarios'] if s['scenario'] == 'V4-EXM-12')['access_modes']), 3)
        self.assertEqual(self.violations(extra['record']), ['SQ-R3'])

    def test_an_observed_difference_is_a_failed_step_not_a_changed_declaration(self):
        # The modes stay as declared; the local conversation found in the wrong home is
        # recorded as failed M12-2 and M12-5, and the scenario fails by the aggregate rule.
        dossier = next(d for d in self.valid if d['record_id'] == 'SQ-EX-06')
        run_b = next(s for s in dossier['scenarios'] if s['scenario'] == 'V4-EXM-12')
        self.assertEqual([(m['kind'], m['home']) for m in run_b['access_modes']],
                         [('chatgpt_account', 'H-acct'), ('local_provider', 'H-omlx')])
        self.assertEqual({s['step']: s['outcome'] for s in run_b['steps']},
                         {'M12-1': 'pass', 'M12-2': 'fail', 'M12-3': 'pass',
                          'M12-4': 'pass', 'M12-5': 'fail', 'M12-6': 'pass'})
        self.assertEqual(run_b['outcome'], 'fail')
        self.assertEqual(run_b['outcome'], self.rules.aggregate([s['outcome'] for s in run_b['steps'] if s['counts']]))
        self.assertEqual([e.message for e in self.validator.iter_errors(dossier)], [])
        self.assertEqual(self.violations(dossier), [])

    def test_a_cited_case_outside_the_step_map_is_refused(self):
        dossier = copy.deepcopy(self.valid[0])
        dossier['scenarios'][0]['steps'][0]['supplier_cases'][0]['case_id'] = 'VC-NOT-IN-THE-MAP'
        self.assertEqual(self.violations(dossier), ['SQ-R6'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
