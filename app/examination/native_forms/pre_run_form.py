#!/usr/bin/env python3
"""Preserved blank N-1 form plus labelled exact-input preparation attachment."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PINS_SHA256 = '27c7e13ea76595ef5bb86ca98a675d7838dae1957906ce3ed19187ac8be0d737'


def consumer():
    data = (HERE / 'pre_run_form.pins.json').read_bytes()
    if hashlib.sha256(data).hexdigest() != PINS_SHA256:
        raise ValueError('pre-run form dependency pins changed')
    pins = json.loads(data)
    captured = {}
    for path, expected in pins['sources'].items():
        target = ROOT / path
        if target.is_symlink(): raise ValueError('helper link refused')
        payload = target.read_bytes()
        if hashlib.sha256(payload).hexdigest() != expected:
            raise ValueError('pre-run form dependency drift')
        captured[path] = payload
    path = 'projects/chirality-app-v4/app/examination/standalone/pre_run_inputs.py'
    spec = importlib.util.spec_from_file_location('_pre_run_form_inputs', ROOT / path)
    api = importlib.util.module_from_spec(spec)
    exec(compile(captured[path], str(ROOT / path), 'exec'), api.__dict__)
    return api


def generate(api, inputs, plan_bytes, selection_bytes, selection_sha256, case):
    selection = inputs.check(selection_bytes, selection_sha256, plan_bytes)
    # Preserve every original blank field, step and guidance byte. The appended
    # material is a preparation attachment, not a completed form or EXP sidecar.
    blank = inputs.forms.generate(api.parse(plan_bytes), case)
    support = selection['support_selection']
    lines = ['', '## Exact input preparation attachment', '',
             'PREPARATION ONLY. This attachment is not an EXP result binding or an observation.',
             'The candidate slot remains unassigned. All original form fields remain blank.',
             'No examination, workflow installation, collision registration, trial, review or A15 occurred.',
             'J-1 starts in an empty project. These are examiner examples for later drafting;',
             'they do not replace the person’s plan or later native work. Changed actual drafts need fresh exact binding.', '',
             'Exact selection SHA-256: ' + selection_sha256,
             'Exact plan-file SHA-256: ' + selection['plan_sha256'],
             'Source-pins SHA-256: ' + selection['source_pins_sha256'],
             'Preparation wrapper pins SHA-256: ' + PINS_SHA256,
             'Selected support method: ' + support['method'],
             'Selected support declaration SHA-256: ' + support['declaration_sha256'],
             'EXP version: ' + support['support_identity']['exp_version'],
             'EXP prototype SHA-256: ' + support['support_identity']['prototype_sha256']]
    for kind, schema_id in support['support_identity']['schema_ids'].items():
        lines.append('EXP ' + kind + ' schema ID: ' + schema_id)
    lines += ['', 'Selected support is source correspondence only; producer use and result-consumer adoption are unverified.',
              'All existing missing inputs remain in the exact plan and selection.', '',
              '| Maintained fixture role | Repository-relative source | SHA-256 |', '|---|---|---|']
    for role, ref in selection['fixture_roles'].items():
        lines.append('| ' + role + ' | ' + ref['path'] + ' | ' + ref['sha256'] + ' |')
    lines += ['', 'Fixture hashes identify unregistered invented material, not selected runnable revisions or installed origins.',
              'A passing blank check proves preparation fidelity only; completed/edited forms refuse this check.', '']
    return blank + '\n'.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('generate', 'check-blank'))
    for name in ('plan', 'selection', 'selection-sha256', 'case'): parser.add_argument('--' + name, required=True)
    parser.add_argument('--form'); parser.add_argument('--form-sha256')
    args = parser.parse_args(argv)
    try:
        api = consumer()
        with api.PreRunInputs() as inputs:
            plan = api.read_file(args.plan); selected = api.read_file(args.selection)
            expected = generate(api, inputs, plan, selected, args.selection_sha256, args.case)
            if args.command == 'generate':
                if args.form or args.form_sha256: parser.error('generate writes only stdout')
                print(expected, end=''); return 0
            if not args.form or not args.form_sha256: parser.error('check-blank requires --form and --form-sha256')
            api.digest_value(args.form_sha256)
            actual = api.read_file(args.form)
            api.require(api.sha(actual) == args.form_sha256, 'exact form digest mismatch')
            matches = actual == expected.encode('utf-8')
            print(json.dumps({'blank_preparation_matches': matches, 'selection_sha256': args.selection_sha256,
                              'form_sha256': args.form_sha256, 'native_run_observed': False,
                              'result_recorded': False, 'qualification_claim': False}))
            return 0 if matches else 1
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({'blank_preparation_matches': False, 'input_error': str(error),
                          'native_run_observed': False, 'result_recorded': False, 'qualification_claim': False}))
        return 2


if __name__ == '__main__': sys.exit(main())
