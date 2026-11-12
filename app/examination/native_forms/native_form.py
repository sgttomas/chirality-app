#!/usr/bin/env python3
"""Consume B7 source-bound preparation as an unobserved N-1 Markdown form."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def consumer(root=ROOT):
    lock = json.loads((HERE / 'sources.terms-v1.json').read_text())
    captured = {}
    for item in lock['sources']:
        raw = (root / item['path']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != item['sha256']:
            raise ValueError('standalone consumer source drift: ' + item['path'])
        captured[item['path']] = raw
    spec = importlib.util.spec_from_file_location('chirality_b7_native_form_consumer', root / lock['sources'][0]['path'])
    module = importlib.util.module_from_spec(spec)
    exec(compile(captured[lock['sources'][0]['path']], str(spec.origin), 'exec'), module.__dict__)
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
    if case in JOURNEYS:
        return journey_form(plan, case, scenario, fingerprint)
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


JOURNEYS = ('J1', 'J2')
JOURNEY_COLUMNS = ['Step', 'Outcome (pass, fail, blocked, not-run, inconclusive)', 'Time (local, with offset)',
                   'Operator (person, or agent: provider, model, session)',
                   'Means (app_controls_by_hand, app_controls_by_computer_use, not_through_app_controls)',
                   'Journey action done', 'Observed',
                   'Outside the controls (preparation or independent_observation: what)',
                   "Interface gaps (what the App's window did not give a user)",
                   'Examination limits (what the operator or its tool could not perceive or operate)',
                   'Interventions (role, who, operated_control / explained_control / other)',
                   'Captures (path, sha256)', 'Deviation or limit']


def journey_form(plan, case, scenario, fingerprint):
    """A blank J1 or J2 form: each step states its own operator and means."""
    lines = ['# Blank journey step form — ' + case, '',
             'PREPARATION ONLY. No examination opened, record assigned, run attempted or observation recorded.',
             'Blank fields are unobserved/unsupplied, not assertions of absence or not-applicability.', '',
             'Preparation SHA-256 (canonical JSON): ' + fingerprint,
             'Case: ' + case, 'Planned run label: ' + scenario['run_label'],
             'Candidate slot: one_same_candidate (unassigned)', '',
             '## Header', '']
    for field in ['Record id', 'Candidate revision', 'Build identity', 'Package record if any', 'Codex pin',
                  'WKWebView / WebKit version', 'OS version', 'Examiner recording', 'Date', 'Time zone',
                  'Work declared unfinished before the run (J2-6)' if case == 'J2' else None,
                  'Journey basis (person_observed, agent_operated, not_established)']:
        if field:
            lines.append('- ' + field + ': __________')
    lines += ['', '## Step table', '', '| ' + ' | '.join(JOURNEY_COLUMNS) + ' |',
              '|' + '---|' * len(JOURNEY_COLUMNS)]
    blank = ' |' * (len(JOURNEY_COLUMNS) - 1)
    for s in scenario['steps']:
        lines.append('| ' + s['step'] + ' |' + blank)
        lines += ['| ' + s['step'] + ' part ' + p['part'] + ' |' + blank for p in s.get('parts', [])]
    lines += ['', '## Required observations', '',
              'Kind and expected result are the definition; status, result and evidence are blank until observed.', '',
              '| Step | Observation | Kind | Expected | Status (made, not_made) | Result | Evidence reference | Note |',
              '|---|---|---|---|---|---|---|---|']
    lines += ['| ' + ' | '.join([s['step'], o['id'], o['kind'], o['expected']]) + ' | | | | |'
              for s in scenario['steps'] for o in s.get('required_observations', [])]
    lines += ['', '## Close', '', '- Steps not reached and why: __________',
              '- Examiner statement that rows were written during the run, not reconstructed: __________', '',
              'The statement above is blank; generation does not attest contemporaneous recording.',
              'Every attempted row (passed, failed, blocked or inconclusive) names who operated the step and by what means;',
              'a step no one began is not run and names no operator. A blocked step was begun and then stopped.',
              "A journey action goes through the App's shipped controls; one done not through them is at most blocked,",
              'failed, not run or inconclusive. Preparation and independent observation are listed apart from the journey',
              "action. An interface gap (what the App's window did not give) and an examination limit (what the operator",
              'or its tool could not perceive or operate) are recorded apart; either one forbids a pass for the step or',
              'the part it was met in, and neither decides which other outcome is recorded. Each planned part has its',
              'own row and outcome, and each required observation its status, result and evidence. These facts forbid a',
              'pass where SQ-R18 says so; which other outcome is the aggregate of the parts (EXP-R1), and the reviewer',
              'judges it (VER-007).',
              'One step operated by an agent or through computer use, or in which an agent operated a control, makes the',
              'journey agent_operated; person_observed needs every attempted step operated by a person by their own hand',
              "through the App's shipped controls with no control operated or explained by anyone else.",
              'Cite acts by their own records (EXP-R5).',
              'When a real record is assigned, place its completed form at forms/<record_id>-journey.md beside records,',
              'cite native_route.form_ref and digest the actual completed bytes in the record evidence.', '',
              '## Case-definition guidance — expected, not observed', '']
    for step in scenario['steps']:
        lines += ['### ' + step['step'], '', 'Counts in scenario: ' + str(step['counts']).lower(),
                  'Governing criteria: ' + ', '.join(c['deliverable'] + ' ' + c['criterion'] for c in step['governing_criteria'])]
        if 'session' in step:
            lines.append('Session: ' + step['session'])
        if 'act_control' in step:
            lines.append('At the act control: ' + step['act_control'])
        lines += ['Planned part ' + p['part'] + ' (native evidence): ' + p['expectation'] for p in step.get('parts', [])]
        lines += ['Required observation ' + o['id'] + ' (' + o['kind'] + ', expected ' + o['expected'] + '): ' + o['what']
                  for o in step.get('required_observations', [])]
        lines += ['- ' + text for text in step['source_action_observation']]
        lines.append('')
    lines += ['Full prerequisites, record requirements and missing inputs remain in the source-bound preparation.',
              'This blank-form check cannot validate a completed form or establish execution, admission, qualification or acceptance.', '']
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
