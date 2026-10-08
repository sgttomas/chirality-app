#!/usr/bin/env python3
"""Read-only, offline SQ preparation. Never opens an examination or writes results."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]


def read_json(path):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError(f"duplicate JSON key: {key}")
            obj[key] = value
        return obj
    return json.loads(path.read_text(), object_pairs_hook=unique)


def digest(path):
    return 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()


def verified_sources(root=ROOT):
    lock = read_json(HERE / 'sources.json')
    for source in lock['sources']:
        path = root / source['path']
        if not path.is_file() or digest(path) != source['sha256']:
            raise ValueError(f"source changed or missing; review preparation basis: {source['path']}")
    return lock


def section(text, heading):
    start = text.index(heading)
    end = text.find('\n## ', start + len(heading))
    return text[start:end if end != -1 else len(text)].strip()


def prepare(root=ROOT):
    lock = verified_sources(root)
    by_role = {x['role']: root / x['path'] for x in lock['sources']}
    step_map = read_json(by_role['step_map'])
    sq = by_role['sq_design'].read_text()
    operations = {}
    for line in sq.splitlines():
        match = re.match(r'^\| ((?:J-|S11-|M12-)\d+R?) \|', line)
        if match:
            cells = [cell.strip() for cell in line.strip('|').split('|')]
            operations[match[1]] = cells[1:-1]
    scenarios = []
    for name, steps in step_map['scenarios'].items():
        prepared = []
        for original in steps:
            step = copy.deepcopy(original)
            step.update(state='awaiting_input', missing_input='candidate_and_configuration',
                        required_native_route='N-1',
                        native_evidence_kinds=['native_development', 'native_packaged'],
                        source_action_observation=operations[step['step']])
            for case in step['supplier_cases']:
                key = case['deliverable'] + '/' + case['file']
                supplier = by_role[key]
                if not re.search(r'^\| ' + re.escape(case['case_id']) + r'\b', supplier.read_text(), re.M):
                    raise ValueError(f"missing supplier case: {key} {case['case_id']}")
            prepared.append(step)
        scenarios.append({'scenario': name, 'run_label': 'RUN-B' if name == 'V4-EXM-12' else 'RUN-A',
                          'candidate_slot': 'one_same_candidate', 'steps': prepared})
    return {
        'artifact_kind': 'standalone_case_preparation',
        'preparation_version': 1,
        'standing': 'test_definition_only',
        'source_basis_revision': lock['source_basis_revision'],
        'sources': lock['sources'],
        'candidate_slot': {'id': 'one_same_candidate', 'revision': None,
                           'build_identity': None, 'codex_pin': None, 'configuration': None},
        'scenarios': scenarios,
        'stimuli': step_map['stimuli'],
        'requirements': {heading: section(sq, heading) for heading in (
            '## 2. Interfaces', '## 3. Case definitions', '## 4. Route, configuration and evidence',
            '## 6. States and sequence', '## 7. Failure behaviour',
            '## 9. What the person must do', '## 12. UNRESOLVED')},
        'access_mode_requirements': {
            'kinds': ['chatgpt_account', 'api_key', 'local_provider'],
            'homes': {'chatgpt_account': 'H-acct', 'api_key': 'H-key'},
            'distinct_conversations': 3, 'configured_together': True,
            'substitute_mode_satisfies': False},
        'missing_inputs': read_json(HERE / 'missing-inputs.json'),
        'invented_material': read_json(HERE / 'invented-inputs.json'),
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
