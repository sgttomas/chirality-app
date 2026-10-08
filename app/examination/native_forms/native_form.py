#!/usr/bin/env python3
"""Consume B7 source-bound preparation as an unobserved N-1 Markdown form."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]


def consumer(root=ROOT):
    lock = json.loads((HERE / 'sources.json').read_text())
    for item in lock['sources']:
        if hashlib.sha256((root / item['path']).read_bytes()).hexdigest() != item['sha256']:
            raise ValueError('standalone consumer source drift: ' + item['path'])
    spec = importlib.util.spec_from_file_location('chirality_b7_native_form_consumer', root / lock['sources'][0]['path'])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generate(plan, case, root=ROOT):
    api = consumer(root)
    errors = api.validate(plan, root)
    if errors:
        raise ValueError('not source-bound standalone preparation: ' + '; '.join(errors[:4]))
    matches = [s for s in plan['scenarios'] if s['scenario'] == case]
    if len(matches) != 1:
        raise ValueError('unknown standalone case')
    scenario = matches[0]
    fingerprint = hashlib.sha256(json.dumps(plan, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
    lines = ['# N-1 blank native-step form — ' + case, '',
             'PREPARATION ONLY. No examination opened, record assigned, run attempted or observation recorded.',
             'Blank fields are unobserved/unsupplied, not assertions of absence or not-applicability.', '',
             'Preparation SHA-256 (canonical JSON): ' + fingerprint,
             'Case: ' + case, 'Planned run label: ' + scenario['run_label'],
             'Candidate slot: one_same_candidate (unassigned)', '',
             '## Header', '']
    for field in ['Record id', 'Candidate revision', 'Build identity', 'Package record if any', 'Codex pin',
                  'WKWebView / WebKit version', 'OS version', 'Person operating', 'Examiner recording', 'Date', 'Time zone']:
        lines.append('- ' + field + ': __________')
    lines += ['', '## Step table', '',
              '| Step | Time (local, with offset) | Action and who did it | Observed | Captures (path, sha256) | Deviation or limit |',
              '|---|---|---|---|---|---|']
    lines += ['| ' + s['step'] + ' | | | | | |' for s in scenario['steps']]
    lines += ['', '## Close', '', '- Steps not reached and why: __________',
              '- Examiner statement that rows were written during the run, not reconstructed: __________', '',
              'The statement above is blank; generation does not attest contemporaneous recording.',
              'A row records what the person did, never an act on their behalf. Cite acts by their own records (EXP-R5).',
              'When a real record is assigned, place its completed form at forms/<record_id>-N1.md beside records,',
              'cite native_route.form_ref and digest the actual completed bytes in the record evidence.', '',
              '## Case-definition guidance — expected, not observed', '']
    for step in scenario['steps']:
        lines += ['### ' + step['step'], '', 'Counts in scenario: ' + str(step['counts']).lower(),
                  'Stimuli: ' + (', '.join(step['stimuli']) or 'none listed'),
                  'Supplier cases: ' + ', '.join(c['deliverable'] + '/' + c['file'] + '#' + c['case_id'] for c in step['supplier_cases'])]
        lines += ['- ' + text for text in step['source_action_observation']]
        if 'added_reason' in step:
            lines.append('Scope note: ' + step['added_reason'])
        lines.append('')
    lines += ['Full stimuli, prerequisites and missing inputs remain in the source-bound preparation.',
              'This blank-form check cannot validate a completed form or establish N-1 execution, admission, qualification or acceptance.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['generate', 'check-blank'])
    parser.add_argument('--plan', required=True, type=Path)
    parser.add_argument('--case', required=True)
    parser.add_argument('--form', type=Path)
    args = parser.parse_args()
    try:
        api = consumer()
        expected = generate(api.read_json(args.plan), args.case)
        if args.command == 'generate':
            if args.form:
                parser.error('generate writes only to stdout')
            print(expected, end='')
        else:
            if not args.form:
                parser.error('check-blank requires --form')
            matches = args.form.read_text() == expected
            print(json.dumps({'blank_form_matches_preparation': matches, 'native_run_observed': False, 'qualification_claim': False}))
            return 0 if matches else 1
    except (ValueError, OSError, KeyError, TypeError) as error:
        print('Native form refused: ' + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
