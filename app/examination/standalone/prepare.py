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
                        required_native_route='N-1',
                        native_evidence_kinds=['native_development', 'native_packaged'],
                        source_action_observation=operations[step['step']])
            prepared.append(step)
        scenarios.append({'scenario': name, 'run_label': 'RUN-B' if name == 'V4-EXM-12' else 'RUN-A',
                          'candidate_slot': 'one_same_candidate', 'steps': prepared})
    return {
        'artifact_kind': 'standalone_case_preparation',
        'preparation_version': 3,
        'standing': 'test_definition_only',
        'sources': lock['sources'],
        'candidate_slot': {'id': 'one_same_candidate', 'revision': None,
                           'build_identity': None, 'codex_pin': None, 'configuration': None},
        'scenarios': scenarios,
        'stimuli': step_map['stimuli'],
        'access_mode_requirements': {
            'kinds': ['chatgpt_account', 'api_key', 'local_provider'],
            'homes': {'chatgpt_account': 'H-acct', 'api_key': 'H-key'},
            'distinct_conversations': 3, 'configured_together': True,
            'substitute_mode_satisfies': False},
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
