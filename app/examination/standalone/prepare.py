#!/usr/bin/env python3
"""Read-only, offline SQ preparation. Never opens an examination or writes results."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN_LABELS = {'V4-EXM-12': 'RUN-B', 'J1': 'RUN-J1', 'J2': 'RUN-J2'}
JOURNEYS = ('J1', 'J2')
# What every recorded J1 or J2 step and journey states (sq.dossier.schema.json, SQ-R11 to SQ-R13 and SQ-R18).
JOURNEY_RECORD_REQUIREMENTS = {
    'journeys': list(JOURNEYS),
    'limits': 'No time or step limit applies to either journey.',
    'journey_actions': "Each journey action goes through the App's shipped controls.",
    'outside_the_controls': 'Preparing fixtures and independent observation (reading the supplier\'s events, '
                            'inspecting records on disk, verifying an export without the App) are done outside the '
                            'controls, listed for the step as preparation or independent_observation, apart from the '
                            'journey action; any operator may do them.',
    'step_operation': {
        'present_on': 'a recorded step whose outcome shows an attempt (pass, fail, blocked, inconclusive); '
                      'absent on a not-run or unrecorded step. A blocked step was attempted (DEL-09-01) and '
                      'carries the operation of whoever began it; a step no one began is not run.',
        'operator': {'kind': ['person', 'agent'], 'identity': 'required',
                     'agent_requires': ['provider', 'model', 'session']},
        'means': ['app_controls_by_hand', 'app_controls_by_computer_use', 'not_through_app_controls'],
        'observations': {'status': ['made', 'not_made'],
                         'result': {'preparation': ['arranged', 'not_arranged'],
                                    'independent_observation': ['equal', 'differs']},
                         'evidence': 'a reference, required when made'},
        'outside_controls': ['preparation', 'independent_observation'],
        'interface_gaps': "What the App's window did not give a user; empty when none; a step with any cannot pass.",
        'examination_limits': 'What the operator or its tool could not perceive or operate; empty when none; not '
                              'an interface failure; an operator that cannot tell which it was records inconclusive.',
        'interventions': {'by': ['examiner', 'agent', 'other_person'], 'actor': 'person or agent, identified',
                          'kind': ['operated_control', 'explained_control', 'other']},
    },
    'not_through_app_controls_can_pass': False,
    'planned_parts': 'A step with planned parts records each part with its own outcome in its result; none is '
                     'left out, declared not applicable or marked as not needing native evidence.',
    'outcome_rule': "SQ-R18: a step is not accepted as passed when its facts forbid it: an interface gap, an "
                    "examination limit, a step not through the App's controls, a required observation missing, not "
                    'made or not as expected, or a planned part missing, set aside, marked not native or passed '
                    "without native evidence. Which other outcome is DEL-09-01's aggregate of its parts.",
    'parts_rule': 'A step is given planned parts only when those parts are together the whole of the step: everything done and observed in carrying out the step is done and observed in carrying out one of its parts. A gap met while carrying out such a step was therefore met in carrying out one of its parts, and that part is not passed. A step whose parts would not be exhaustive must not be declared with planned parts.',
    'basis': ['person_observed', 'agent_operated', 'not_established'],
    'basis_from': 'attempted steps only; none attempted is not_established',
    'person_observed_only_when': "every attempted step was operated by a person by their own hand through the "
                                 "App's shipped controls, with no control operated or explained by anyone else",
    'agent_operated_when': 'any attempted step was operated by an agent or through computer use, or an agent '
                           'operated a control in it',
}


def read_json(path):
    return parse_json(path.read_bytes())


def parse_json(raw):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError(f"duplicate JSON key: {key}")
            obj[key] = value
        return obj
    return json.loads(raw, object_pairs_hook=unique)


def digest(path):
    return 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()


def verified_sources(root=ROOT, captured=None):
    lock = read_json(HERE / 'sources.terms-v1.json')
    for source in lock['sources']:
        path = root / source['path']
        if not path.is_file():
            raise ValueError(f"source changed or missing; review preparation basis: {source['path']}")
        raw = path.read_bytes()
        if ('sha256:' + hashlib.sha256(raw).hexdigest()) != source['sha256']:
            raise ValueError(f"source changed or missing; review preparation basis: {source['path']}")
        if captured is not None:
            captured[source['role']] = raw
    return lock


def prepare(root=ROOT):
    captured = {}
    lock = verified_sources(root, captured)
    step_map = parse_json(captured['step_map'])
    # Each step's action and observation cells, keyed by step.
    operations = parse_json(captured['step_operations'])
    scenarios = []
    for name, steps in step_map['scenarios'].items():
        prepared = []
        for original in steps:
            step = copy.deepcopy(original)
            step.update(state='awaiting_input', missing_input='candidate_and_configuration',
                        # A journey step is operated through the App's shipped controls by a person or an
                        # agent, so it names no person-operated form route; its record states the operation.
                        required_native_route='native_app_controls' if name in JOURNEYS else 'N-1',
                        native_evidence_kinds=['native_development', 'native_packaged'],
                        source_action_observation=operations[step['step']])
            prepared.append(step)
        scenarios.append({'scenario': name, 'run_label': RUN_LABELS.get(name, 'RUN-A'),
                          'candidate_slot': 'one_same_candidate', 'steps': prepared})
    return {
        'artifact_kind': 'standalone_case_preparation',
        'preparation_version': 4,
        'standing': 'test_definition_only',
        'sources': lock['sources'],
        'candidate_slot': {'id': 'one_same_candidate', 'revision': None,
                           'build_identity': None, 'codex_pin': None, 'configuration': None},
        'scenarios': scenarios,
        'stimuli': step_map['stimuli'],
        'access_mode_requirements': {
            'kinds': ['chatgpt_account', 'local_provider'],
            'homes': {'chatgpt_account': 'H-acct', 'local_provider': 'H-omlx'},
            'distinct_conversations': 2, 'configured_together': True,
            'substitute_mode_satisfies': False},
        'journey_record_requirements': JOURNEY_RECORD_REQUIREMENTS,
        'missing_inputs': parse_json(captured['missing-inputs.json']),
        'invented_material': parse_json(captured['invented-inputs.json']),
        'boundary': 'No candidate named, examination opened, run attempted, result recorded, '
                    'supplier check qualified, or qualification handed over. Source revision is not build identity.',
    }


def differences(actual, expected, path='$'):
    """Exact preparation comparison; deliberately not a validator of executed dossiers."""
    if type(actual) is not type(expected):
        return [f'{path}: type differs']
    if isinstance(expected, dict):
        errors = [f'{path}.{key}: unexpected or missing field' for key in sorted(actual.keys() ^ expected.keys())]
        for key in expected.keys() & actual.keys():
            errors.extend(differences(actual[key], expected[key], f'{path}.{key}'))
        return errors
    if isinstance(expected, list):
        if len(actual) != len(expected):
            return [f'{path}: required ordered list length differs']
        return [error for i, (a, e) in enumerate(zip(actual, expected))
                for error in differences(a, e, f'{path}[{i}]')]
    return [] if actual == expected else [f'{path}: differs from preparation basis']


def validate(plan, root=ROOT):
    return differences(plan, prepare(root))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'check'])
    parser.add_argument('plan', nargs='?', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'prepare':
            if args.plan:
                parser.error('prepare writes only to stdout')
            print(json.dumps(prepare(), indent=2, ensure_ascii=False))
        else:
            if not args.plan:
                parser.error('check requires a preparation JSON file')
            errors = validate(read_json(args.plan))
            print(json.dumps({'preparation_matches_basis': not errors, 'errors': errors,
                              'qualification_claim': False}, indent=2))
            return 1 if errors else 0
    except (ValueError, OSError, KeyError) as error:
        print(f'Preparation refused: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
