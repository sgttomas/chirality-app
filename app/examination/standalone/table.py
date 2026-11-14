#!/usr/bin/env python3
"""The examination's table: every planned step, its latest candidate and its outcome; then, kept apart, the scripted
driver's runs and the session comparison's rows (DEL-09-02 examination tooling).

    python3 -B table.py --repo <a checkout> --candidate <key> [--results <folder>] [--driver FOLDER=RUN@HEAD ...]
                        [--comparisons <record folder> ...] [--release 4.0.0]

It reads and writes nothing in the repository, and its output is never committed. What it reads:
- the planned steps, from app/examination/sq_receiving/sq.step-map.json in the checkout given;
- steps taken out of a release by a recorded decision, from that file's "out_of_release" entry for their scenario:
  the steps it lists in "steps", or every step of the scenario when it lists none. They are printed as out of that
  release, naming the decision and, when the entry has "steps_by", who read which steps it takes. They are neither
  "not run" nor dropped, and the scenario's other steps are ordinary planned steps. An entry naming a step the
  scenario does not have stops the print;
- step results, from --results, for the one candidate named by --candidate: a folder of JSON records {step,
  candidate, configuration, date, outcome, operated_by}, the outcome one of DEL-09-02 REQ-007's five (passed,
  failed, blocked, not run, inconclusive); any other outcome stops the print, and so does a results folder that is
  not there. Records for another candidate or naming none, and records that cannot be read, are named beneath the
  table and never counted. Of a step's records, the latest date decides; records of the latest date that disagree
  print as inconclusive and are named. A step with no record prints "not run (no record)". A record may cite
  session-comparison rows: "cites": [{file, sha256, rows}], the file relative to --results. A pass that cites a row
  not passed, or a citation whose file is missing or has changed, prints as "recorded passed; not counted", is
  named beneath the table, and is never counted as passed;
- the scripted driver's runs, from --driver FOLDER=RUN@HEAD: a folder holding the reports a hosted run uploaded
  (report.json, scenario-report.json, and setup-report.json when the run made one). The driver is development
  evidence on a test build and satisfies no step;
- session-comparison rows, from --comparisons FOLDER: a record folder holding session-comparison-*.jsonl files
  (one row per comparison on one subject, each with one of REQ-007's outcomes) and the launch record beside them.
  Rows are not step results. They are counted from the rows themselves, by candidate (the header's candidate_key,
  else the launch record's identifier; a file whose two disagree is named and not counted), comparison and outcome; a summary line is compared with the rows, never
  counted. Of the answers files made from one screen list (the header's "answers_of"), only the latest counts: by
  the header's "written_at" when every one has it, else by the time in the name, and two of the same time count
  for neither. When a file's header says the workflow comparison is not available ("workflow_comparison"), that
  sentence is written first beneath the section: W1 is counted only as blocked (a W1 row of that file saying
  anything else is named and not counted), and C2, C3 and C4 passing do not meet the first target.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
import sys

OUTCOMES = ('passed', 'failed', 'blocked', 'not run', 'inconclusive')
STEP_MAP = 'app/examination/sq_receiving/sq.step-map.json'


def results(folder, candidate):
    """The latest record of each step for the candidate named, by date, with what was set aside: records for another
    candidate or none, and records that cannot be read. Records of the latest date that disagree are kept apart as
    contradictory: which came last cannot be told, so neither decides."""
    if folder is not None and not Path(folder).is_dir():
        raise SystemExit(f'the results folder {folder} is not a folder that can be read')
    by_step, other, unreadable = {}, [], []
    for path in sorted(Path(folder).glob('*.json')) if folder else []:
        try:
            record = json.loads(path.read_text())
        except (OSError, ValueError) as error:
            unreadable.append(f'{path.name} ({type(error).__name__})')
            continue
        if record.get('outcome') not in OUTCOMES:
            raise SystemExit(f'{path}: outcome {record.get("outcome")!r} is not one of REQ-007\'s five')
        if record.get('candidate') != candidate:
            other.append(f"{path.name} ({record.get('candidate') or 'no candidate'})")
            continue
        by_step.setdefault(record['step'], []).append(dict(record, file=path.name))
    latest, contradictory = {}, {}
    for step, records in by_step.items():
        newest = max(record['date'] for record in records)
        last = [record for record in records if record['date'] == newest]
        if len({record['outcome'] for record in last}) > 1:
            contradictory[step] = last
        else:
            latest[step] = last[0]
    return latest, contradictory, other, unreadable


def citation_marks(record, folder):
    marks = []
    for cite in record.get('cites') or []:
        path = Path(folder) / cite['file']
        if not path.is_file() or 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest() != cite['sha256']:
            marks.append(f"citation unsupported ({cite['file']} missing or changed)")
            continue
        rows = path.read_text().splitlines()
        cited = [json.loads(rows[n - 1]) for n in cite['rows'] if 0 < n <= len(rows)]
        if len(cited) != len(cite['rows']):
            marks.append(f"citation unsupported ({cite['file']} has no such row)")
        elif record['outcome'] == 'passed' and any(row.get('outcome') != 'passed' for row in cited):
            marks.append('disagrees with the rows it cites')
    return marks


def table(repo, folder, release, candidate):
    step_map = json.loads((Path(repo) / STEP_MAP).read_text())
    out = step_map.get('out_of_release', {})
    seen, contradictory, other, unreadable = results(folder, candidate)
    known = {step['step'] for steps in step_map['scenarios'].values() for step in steps}
    stray = sorted((set(seen) | set(contradictory)) - known)
    lines = [f'EXAMINATION TABLE for {release}, candidate {candidate}, from {STEP_MAP} at the checkout given', '',
             '| Scenario | Step | Counts | Outcome (REQ-007) | Date | Operated by |',
             '| --- | --- | --- | --- | --- | --- |']
    totals = dict.fromkeys(OUTCOMES, 0)
    removed, disputed, recorded_disputed = 0, [], 0
    for scenario, steps in step_map['scenarios'].items():
        decision = out.get(scenario)
        if decision and decision.get('release') == release:
            named = decision.get('steps')
            unknown = sorted(set(named or []) - {step['step'] for step in steps})
            if unknown:
                raise SystemExit(f'out_of_release for {scenario} names steps it does not have: {unknown}')
            taken = set(named) if named else {step['step'] for step in steps}
        else:
            taken = set()
        for step in steps:
            counts = 'yes' if step.get('counts') else 'no'
            if step['step'] in taken:
                removed += 1
                why = (f"out of {release} by {decision['by']}'s decision of {decision['decided']}"
                       + (f"; steps as read by {decision['steps_by']}" if decision.get('steps_by') else '')
                       + f" ({decision['stated_in']})")
                lines.append(f"| {scenario} | {step['step']} | {counts} | {why} | — | — |")
                continue
            if step['step'] in contradictory:
                last = contradictory[step['step']]
                shown = ', '.join(f"{r['file']} {r['outcome']}" for r in last)
                disputed.append(f"{step['step']}: records of the same date disagree ({shown}); counted inconclusive")
                if step.get('counts'):
                    totals['inconclusive'] += 1
                lines.append(f"| {scenario} | {step['step']} | {counts} | inconclusive (records disagree) | {last[0]['date']} | — |")
                continue
            record = seen.get(step['step'])
            if record is None:
                if step.get('counts'):
                    totals['not run'] += 1
                lines.append(f"| {scenario} | {step['step']} | {counts} | not run (no record) | — | — |")
                continue
            outcome = record['outcome']
            marks = citation_marks(record, folder)
            shown = outcome
            if marks:
                disputed.append(f"{step['step']}: {'; '.join(marks)}")
                if outcome == 'passed':
                    # A pass its own evidence does not support is shown as recorded and never counted as passed.
                    shown = 'recorded passed; not counted (its citations do not support it)'
            if step.get('counts'):
                if shown == outcome:
                    totals[outcome] += 1
                else:
                    recorded_disputed += 1
            lines.append(f"| {scenario} | {step['step']} | {counts} | {shown} | {record['date']} | {record.get('operated_by', '—')} |")
    lines += ['', 'Counted steps in the release: ' + ', '.join(f'{totals[o]} {o}' for o in OUTCOMES)
              + (f', {recorded_disputed} recorded passed but not supported by their citations' if recorded_disputed else '')
              + f'. Steps out of {release} by a recorded decision: {removed}.']
    if stray:
        lines.append('Records naming no planned step (not counted): ' + ', '.join(stray))
    if disputed:
        lines.append('Steps whose evidence is contradictory or does not support them: ' + ' | '.join(disputed))
    if other:
        lines.append(f'Records for another candidate, or naming none (not counted for {candidate}): ' + ', '.join(other))
    if unreadable:
        lines.append('Records that could not be read (not counted): ' + ', '.join(unreadable))
    return lines


def comparisons(folders):
    lines = ['', 'SESSION COMPARISON (rows of the execution lane\'s comparison; not step results)', '',
             '| Candidate | Comparison | ' + ' | '.join(OUTCOMES) + ' |', '| --- | --- |' + ' --- |' * len(OUTCOMES)]
    counts, notes, withheld = {}, [], set()
    for folder in folders:
        folder = Path(folder)
        records = sorted(folder.glob('launch-record*.json'))
        identifiers = {json.loads(p.read_text()).get('bundle', {}).get('identifier') for p in records}
        files = [p for p in sorted(folder.glob('session-comparison-*.jsonl')) if not p.name.startswith('session-comparison-screen-')]
        # Of the answers files made from one screen list, the latest counts. Names begin with the UTC time to the
        # second, then a random suffix; two with the same time cannot be ordered, so neither counts and both are noted.
        made_from = {}
        for path in files:
            first = json.loads(path.read_text().splitlines()[0]) if path.read_text().strip() else {}
            if first.get('answers_of'):
                made_from.setdefault(first['answers_of'], []).append((path, first.get('written_at')))
        latest_answers, undecided = {}, set()
        for screen, entries in made_from.items():
            # The header's written_at (UTC, microseconds) when every file has one; otherwise the name's time.
            exact = all(written for _, written in entries)
            stamp = (lambda e: e[1]) if exact else (lambda e: e[0].name[len('session-comparison-'):].rsplit('-', 1)[0])
            newest = max(stamp(e) for e in entries)
            tied = [e[0] for e in entries if stamp(e) == newest]
            if len(tied) == 1:
                latest_answers[screen] = tied[0]
            else:
                undecided.add(screen)
                notes.append(f"{', '.join(p.name for p in tied)}: answers made from {screen} at the same second; "
                             'which is later cannot be told, so none of them is counted')
        for path in files:
            rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
            header = next((row for row in rows if row.get('header')), {})
            if header.get('answers_of') in undecided:
                continue
            if header.get('answers_of') and latest_answers.get(header['answers_of']) != path:
                notes.append(f"{path.name}: replaced by {latest_answers[header['answers_of']].name}, made from the same screen list")
                continue
            summary = next((row for row in rows if 'summary' in row), None)
            if header.get('workflow_comparison'):
                withheld.add(header['workflow_comparison'])
            keys = {re.sub(r'^dev\.chirality\.app-v4\.candidate\.', '', i or '') for i in identifiers if i}
            candidate = header.get('candidate_key')
            if candidate is not None and keys and keys != {candidate}:
                # The header and the launch record name different candidates: whose rows these are cannot be told.
                notes.append(f"{path.name}: its header names candidate {candidate} and the launch record "
                             f"{', '.join(sorted(keys))}; its rows are not counted")
                continue
            if candidate is None:
                candidate = keys.pop() if len(keys) == 1 else f'not known ({path.name})'
            seen = {}
            for row in rows:
                if row.get('header') or 'summary' in row:
                    continue
                if row.get('outcome') not in OUTCOMES:
                    notes.append(f'{path.name}: a row with outcome {row.get("outcome")!r} (not counted)')
                    continue
                if header.get('workflow_comparison') and row.get('comparison') == 'W1' and row['outcome'] != 'blocked':
                    notes.append(f"{path.name}: a W1 row says {row['outcome']} although the header says the workflow "
                                 'comparison is not available; it is not counted')
                    continue
                key = (candidate, row['comparison'])
                counts.setdefault(key, dict.fromkeys(OUTCOMES, 0))[row['outcome']] += 1
                seen.setdefault(row['comparison'], dict.fromkeys(OUTCOMES, 0))[row['outcome']] += 1
            nonzero = lambda counts: {c: {o: n for o, n in by.items() if n} for c, by in (counts or {}).items()}
            if summary is not None and nonzero(summary.get('summary')) != nonzero(seen):
                notes.append(f'{path.name}: its summary line differs from its rows; the rows are counted')
            if summary is not None and summary.get('unrecognised'):
                notes.append(f"{path.name}: {summary['unrecognised']} rows name a value the tool did not recognise "
                             '(counted under their own outcome; none passes)')
    for (candidate, comparison), by in sorted(counts.items()):
        lines.append(f'| {candidate} | {comparison} | ' + ' | '.join(str(by[o]) for o in OUTCOMES) + ' |')
    for sentence in sorted(withheld):
        # The tool's own words; a row of W1 is blocked, and passes of the other comparisons do not make up for it.
        notes.insert(0, f'W1, the workflow comparison: "{sentence}". It is counted only as blocked. C2, C3 and C4 passing '
                        'do not meet the first target; the workflow part stays unvalidated until W1 can be compared.')
    return lines + [''] + notes if notes else lines


def driver(entries):
    lines = ['', "THE SCRIPTED DRIVER (development evidence on a test build; it satisfies no step above)", '',
             '| Run | Head | Scenario | Walk verdict | Proof result | Outcomes |', '| --- | --- | --- | --- | --- | --- |']
    for entry in entries:
        folder, _, rest = entry.partition('=')
        run, _, head = rest.partition('@')
        report = json.loads((Path(folder) / 'report.json').read_text())
        scenario = Path(folder) / 'scenario-report.json'
        walked = json.loads(scenario.read_text()) if scenario.exists() else {}
        shown = '; '.join(f'{name}: {state}' for name, state in (walked.get('outcomes') or {}).items()) or '—'
        lines.append(f"| {run} | {head[:12]} | {walked.get('scenario', '—')} (v{walked.get('version', '?')}) | "
                     f"{walked.get('verdict', '—')} | {report.get('result', '—')} | {shown} |")
        setup = Path(folder) / 'setup-report.json'
        if setup.exists():
            s = json.loads(setup.read_text())
            launches = '; '.join(f"{l['id']}: {l['verdict']}" for l in s.get('launches', []))
            lines.append(f"| {run} | {head[:12]} | {s.get('scenario', '—')} (v{s.get('version', '?')}) | {s.get('verdict', '—')} | "
                         f"{report.get('result', '—')} | {launches} |")
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--repo', required=True, help='a checkout of main')
    parser.add_argument('--results', help='a folder of step result records')
    parser.add_argument('--candidate', required=True, help='the candidate key the step table is for; records of any other '
                        'candidate, or naming none, are not counted')
    parser.add_argument('--release', default='4.0.0')
    parser.add_argument('--driver', action='append', default=[], help='FOLDER=RUN@HEAD of a hosted driver run')
    parser.add_argument('--comparisons', action='append', default=[], help='a record folder holding session-comparison rows')
    args = parser.parse_args(argv)
    print('\n'.join(table(args.repo, args.results, args.release, args.candidate) + (driver(args.driver) if args.driver else [])
                    + (comparisons(args.comparisons) if args.comparisons else [])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
