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
        self.assertEqual(prep.validate(self.plan), [])

    def test_dropped_reordered_and_recounted_steps(self):
        self.assertEqual([s['scenario'] for s in self.plan['scenarios']], ['V4-EXM-10', 'V4-EXM-11', 'V4-EXM-12', 'J1', 'J2'])
        self.assertEqual([len(s['steps']) for s in self.plan['scenarios']], [11, 6, 6, 6, 7])
        for scenario in range(5):
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
        self.assertEqual([s['run_label'] for s in self.plan['scenarios']], ['RUN-A', 'RUN-A', 'RUN-B', 'RUN-J1', 'RUN-J2'])
        self.rejects(lambda p: p['scenarios'][1].update(run_label='different-run'))
        self.rejects(lambda p: p['scenarios'][3].update(run_label='RUN-A'))
        for index in (2, 3, 4):
            self.rejects(lambda p: p['scenarios'][index].update(candidate_slot='another-candidate'))
        self.assertEqual({s['candidate_slot'] for s in self.plan['scenarios']}, {'one_same_candidate'})
        self.rejects(lambda p: p['candidate_slot'].update(build_identity='INVENTED-BUILD'))
        self.rejects(lambda p: p['access_mode_requirements'].update(distinct_conversations=2))
        self.rejects(lambda p: p['access_mode_requirements']['kinds'].append('local_provider'))

    def test_run_b_for_4_0_0_has_the_account_mode_alone(self):
        # The step map takes the local model server's steps out of 4.0.0, so run B declares the ChatGPT
        # account in H-acct alone, its conversation observed in run A (DEL-09-02).
        modes = self.plan['access_mode_requirements']
        self.assertEqual(modes['kinds'], ['chatgpt_account'])
        self.assertEqual(modes['homes'], {'chatgpt_account': 'H-acct'})
        self.assertEqual(modes['out_of_release'], ['M12-2', 'M12-3', 'M12-5'])
        self.assertIn('run A on the same candidate', modes['conversation'])
        self.assertIs(modes['substitute_mode_satisfies'], False)
        self.assertIn('account_mode', [item['id'] for item in self.plan['missing_inputs']])
        self.assertNotIn('two_modes', [item['id'] for item in self.plan['missing_inputs']])
        # Standalone API-key access is outside 4.0.0: a further mode or its key home is refused.
        self.rejects(lambda p: p['access_mode_requirements']['kinds'].insert(1, 'api_key'))
        self.rejects(lambda p: p['access_mode_requirements']['homes'].update(api_key='H-key'))
        self.rejects(lambda p: p['access_mode_requirements']['homes'].update(local_provider='H-omlx'))
        self.rejects(lambda p: p['access_mode_requirements']['homes'].update(chatgpt_account='H-omlx'))
        # The local key step stays defined for the later update, as the step map keeps it.
        key_step = self.plan['scenarios'][2]['steps'][1]
        self.assertEqual(key_step['step'], 'M12-2')
        self.assertIn('dedicated local home H-omlx', key_step['source_action_observation'][0])

    def test_the_two_modes_return_with_the_local_steps(self):
        step_map = json.loads((APP / 'examination/sq_receiving/sq.step-map.json').read_text())
        later = {key: value for key, value in step_map.items() if key != 'out_of_release'}
        modes = prep.access_mode_requirements(later)
        self.assertEqual(modes['kinds'], ['chatgpt_account', 'local_provider'])
        self.assertEqual(modes['homes'], {'chatgpt_account': 'H-acct', 'local_provider': 'H-omlx'})
        self.assertEqual(modes['distinct_conversations'], 2)

    def test_step_operations_and_insertion_points(self):
        self.assertIn('delegates one bounded sub-task', self.plan['scenarios'][0]['steps'][1]['source_action_observation'][0])
        insertions = self.plan['scenarios'][1]['steps']
        self.assertIn("During J-2", insertions[0]['source_action_observation'][0])
        self.assertIn("During J-8's try conversation", insertions[4]['source_action_observation'][0])
        self.rejects(lambda p: p['scenarios'][1]['steps'][4].update(source_action_observation=['after RUN-A']))

    def test_journeys_cite_criteria_mark_sessions_and_act_control(self):
        j1, j2 = self.plan['scenarios'][3], self.plan['scenarios'][4]
        self.assertEqual([s['step'] for s in j1['steps']], ['J1-%d' % n for n in range(1, 7)])
        self.assertEqual([s['step'] for s in j2['steps']], ['J2-%d' % n for n in range(1, 8)])
        for step in j1['steps'] + j2['steps']:
            with self.subTest(step=step['step']):
                # Journey steps cite governing acceptance criteria, never invented supplier cases.
                self.assertEqual(step['supplier_cases'], [])
                self.assertTrue(step['governing_criteria'])
                self.assertTrue(step['counts'])
                self.assertEqual(step['required_native_route'], 'native_app_controls')
                self.assertEqual(len(step['source_action_observation']), 2)
        self.assertEqual([s.get('session') for s in j2['steps']], ['first'] * 5 + ['first_to_later', 'later'])
        self.assertEqual({s['step']: s['act_control'] for s in j1['steps'] + j2['steps'] if 'act_control' in s},
                         {'J1-2': 'when_required', 'J1-5': 'when_required', 'J2-5': 'always', 'J2-7': 'when_required'})
        # Both approval policies and the changed-file condition are planned parts that cannot disappear.
        self.assertEqual([p['part'] for p in j2['steps'][6]['parts']], ['allow-disk-records', 'require-verified-approval'])
        self.assertIn('"Allow disk records" and "Require verified approval"', j2['steps'][6]['source_action_observation'][0])
        self.assertEqual([p['part'] for p in j1['steps'][3]['parts']], ['supplied-as-selected', 'changed-file-held'])
        self.assertNotIn('where the changed-file condition is arranged', j1['steps'][3]['source_action_observation'][0])
        self.assertEqual({s['step']: [(o['id'], o['kind'], o['expected']) for o in s['required_observations']]
                          for s in j1['steps'] + j2['steps'] if 'required_observations' in s},
                         {'J1-4': [('file-changed-after-selection', 'preparation', 'arranged')],
                          'J1-5': [('run-turn-matches-run-text', 'independent_observation', 'equal'),
                                   ('workflow-body-matches-stored-file', 'independent_observation', 'equal')],
                          'J2-7': [(p + '/' + c, 'independent_observation', 'equal')
                                   for p in ('allow-disk-records', 'require-verified-approval')
                                   for c in ('run-turn-matches-run-text', 'workflow-body-matches-stored-file')]})
        self.assertTrue(all(p['needs_native'] for s in j1['steps'] + j2['steps'] for p in s.get('parts', [])))
        self.assertIn({'deliverable': 'DEL-02-02', 'criterion': 'AC-010'}, j1['steps'][2]['governing_criteria'])
        for index, step in ((4, j1['steps'][4]), (6, j2['steps'][6])):
            self.assertIn('two comparisons', step['source_action_observation'][1])
        self.assertIn('recorded under J1-5', j1['steps'][1]['source_action_observation'][0])
        self.assertIn({'deliverable': 'DEL-02-03', 'criterion': 'AC-002'}, j1['steps'][4]['governing_criteria'])
        self.assertIn({'deliverable': 'DEL-02-02', 'criterion': 'AC-009'}, j2['steps'][2]['governing_criteria'])
        self.rejects(lambda p: p['scenarios'][4]['steps'][6]['parts'].pop())
        self.rejects(lambda p: p['scenarios'][3]['steps'][3].pop('parts'))
        self.rejects(lambda p: p['scenarios'][3]['steps'][4].pop('required_observations'))
        self.rejects(lambda p: p['scenarios'][4]['steps'][6]['parts'][1].update(needs_native=False))
        self.rejects(lambda p: p['scenarios'][3]['steps'][4]['required_observations'][0].update(expected='differs'))
        self.rejects(lambda p: p['scenarios'][4]['steps'][4].pop('act_control'))
        self.rejects(lambda p: p['scenarios'][4]['steps'][6].update(session='first'))
        self.rejects(lambda p: p['scenarios'][3]['steps'][0]['governing_criteria'].pop())
        self.rejects(lambda p: p['scenarios'][3]['steps'][0].update(required_native_route='N-1'))

    def test_journey_record_requirements_are_carried(self):
        need = self.plan['journey_record_requirements']
        self.assertEqual(need['step_operation']['means'],
                         ['app_controls_by_hand', 'app_controls_by_computer_use', 'not_through_app_controls'])
        self.assertEqual(need['step_operation']['operator']['agent_requires'], ['provider', 'model', 'session'])
        self.assertEqual(need['step_operation']['outside_controls'], ['preparation', 'independent_observation'])
        self.assertIs(need['not_through_app_controls_can_pass'], False)
        self.assertIn('examination_limits', need['step_operation'])
        self.assertIn('actor', need['step_operation']['interventions'])
        self.assertIn('attempted', need['basis_from'])
        self.assertIn('SQ-R18', need['outcome_rule'])
        self.assertEqual(need['step_operation']['observations']['status'], ['made', 'not_made'])
        self.assertEqual(need['basis'], ['person_observed', 'agent_operated', 'not_established'])
        self.assertIn('journey_operation', [item['id'] for item in self.plan['missing_inputs']])
        self.rejects(lambda p: p.pop('journey_record_requirements'))
        self.rejects(lambda p: p['journey_record_requirements'].update(not_through_app_controls_can_pass=True))
        self.rejects(lambda p: p['journey_record_requirements']['step_operation']['means'].pop())

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

    def test_local_inventory_and_missing_input_bytes_are_bound(self):
        roles = {source['role'] for source in prep.verified_sources()['sources']}
        self.assertEqual(roles, {'step_map', 'step_operations', 'missing-inputs.json', 'invented-inputs.json'})

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
