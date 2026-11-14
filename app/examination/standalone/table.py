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
  not there or cannot be read, and an empty candidate. Records for another candidate or naming none, and records
  that cannot be read, are named beneath the table and never counted. A record that is not a JSON object, names no
  step, or has a date that is neither a calendar date (YYYY-MM-DD) nor a time with its zone (ISO 8601, Z or an
  offset) cannot be read. Dates are compared as dates or as instants, so one time written with two zones is the same
  date; a step whose records mix calendar dates and times cannot be ordered and prints as inconclusive.

  THE CLAIM (App Agent 0, 14 November 2026). A step prints as passed only when a result record for that step, on the
  candidate named, says passed, and no other record for that step on that candidate of the same latest date says
  otherwise. Every other state prints as what it is: a step with no record prints "not run (no record)", and records
  of the latest date that disagree print as inconclusive, with the disagreement printed directly under the counts.
  A record may cite session-comparison rows ("cites": [{file, sha256, rows}], the file relative to --results). Cited
  rows are listed beneath the table as cited, with whether each file exists, whether it is unchanged (its digest is
  the one cited) and what each cited row's outcome is. They never raise, lower or protect a step's outcome or any
  count, and nothing in a citation can stop the print: one that is not a list, points outside the results folder
  (by .. or an absolute path; listed, not read) or names a file that cannot be read is listed as such. The driver's runs and the comparison's rows are never counted as steps;
- the scripted driver's runs, from --driver FOLDER=RUN@HEAD: a folder holding the reports a hosted run uploaded
  (report.json, scenario-report.json, and setup-report.json when the run made one). The driver is development
  evidence on a test build and satisfies no step;
- session-comparison rows, from --comparisons FOLDER: a record folder holding session-comparison-*.jsonl files
  (one row per comparison on one subject, each with one of REQ-007's outcomes) and the launch record beside them.
  Rows are not step results. They are counted from the rows themselves, by candidate, comparison and outcome. The
  candidate is the header's candidate_key alone: a file whose header names none (a fallback file written after a
  refusal or failure, say) is counted under "not known", and never resolved through another field such as the
  launch record's identifier; a file whose header names a candidate the launch record beside it contradicts is named
  and not counted. A launch record is read in the launcher's shape (candidate_key, or identifier, at its top level);
  one that cannot be read withholds its folder's rows. A comparison folder that is not there, and a file that is not
  one JSON object per line or is empty, are noted and contribute nothing. A summary line is compared with the rows,
  never counted. Of the answers files made from one screen list (the header's "answers_of"), only the latest counts: by
  the header's "written_at" when every one has it, else by the time in the name, and two of the same time count
  for neither. A fallback file carrying "answers_of" takes part like any other, so a refused answers run replaces
  the answers its list had before. When a file's header says the workflow comparison is not available ("workflow_comparison"), that
  sentence is written first beneath the section: W1 is counted only as blocked (a W1 row of that file saying
  anything else is named and not counted), and C2, C3 and C4 passing do not meet the first target. --comparison-standing
  prints a sentence at the head of the section, for the comparison tool's own standing.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
from pathlib import Path
import sys

OUTCOMES = ('passed', 'failed', 'blocked', 'not run', 'inconclusive')
STEP_MAP = 'app/examination/sq_receiving/sq.step-map.json'


def when(text):
    """A record's date as something that orders: ('date', a calendar date) for YYYY-MM-DD, or ('instant', the UTC time)
    for an ISO 8601 time with its zone (Z or an offset). Anything else, a time without a zone among it, is None: the
    record cannot be placed in time and is set aside as unreadable."""
    if not isinstance(text, str):
        return None
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', text):
        try:
            return ('date', datetime.date.fromisoformat(text))
        except ValueError:
            return None
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2})', text):
        return None
    try:
        moment = datetime.datetime.fromisoformat(text.replace('Z', '+00:00'))
    except ValueError:
        return None
    return ('instant', moment.astimezone(datetime.timezone.utc))


def results(folder, candidate):
    """The latest record of each step for the candidate named, by date, with what was set aside: records for another
    candidate or none, and records that cannot be read. Records of the latest date that disagree are kept apart as
    contradictory: which came last cannot be told, so neither decides."""
    if folder is not None:
        try:
            os.listdir(folder)
        except OSError as error:
            raise SystemExit(f'the results folder {folder} cannot be read ({type(error).__name__})') from None
    by_step, other, unreadable = {}, [], []
    for path in sorted(Path(folder).glob('*.json')) if folder else []:
        try:
            record = json.loads(path.read_text())
        except (OSError, ValueError) as error:
            unreadable.append(f'{path.name} ({type(error).__name__})')
            continue
        if not isinstance(record, dict):
            unreadable.append(f'{path.name} (not a record)')
            continue
        if record.get('outcome') not in OUTCOMES:
            raise SystemExit(f'{path}: outcome {record.get("outcome")!r} is not one of REQ-007\'s five')
        if record.get('candidate') != candidate:
            other.append(f"{path.name} ({record.get('candidate') or 'no candidate'})")
            continue
        if not isinstance(record.get('step'), str) or not record['step']:
            unreadable.append(f'{path.name} (names no step)')
            continue
        moment = when(record.get('date'))
        if moment is None:
            unreadable.append(f"{path.name} (its date {record.get('date')!r} is not a calendar date or a time with its zone)")
            continue
        by_step.setdefault(record['step'], []).append(dict(record, file=path.name, moment=moment))
    latest, contradictory = {}, {}
    for step, records in by_step.items():
        if len({record['moment'][0] for record in records}) > 1:
            # Calendar dates and times cannot be ordered against each other: which came last cannot be told.
            contradictory[step] = (records, 'dates of different forms cannot be ordered')
            continue
        newest = max(record['moment'][1] for record in records)
        last = [record for record in records if record['moment'][1] == newest]
        if len({record['outcome'] for record in last}) > 1:
            contradictory[step] = (last, 'records of the same date disagree')
        else:
            latest[step] = last  # every record of the latest date, all with one outcome
    return latest, contradictory, other, unreadable


def cited(record, folder):
    """What a record cites, as listed beneath the table: for each citation, whether its file exists, whether it is
    unchanged (the digest cited), and each cited row's outcome. Listing only: nothing here bears on any outcome."""
    shown = []
    cites = record.get('cites')
    if cites is None:
        return shown
    if not isinstance(cites, list):
        return [f'citations not given as a list: {json.dumps(cites)}']
    for cite in cites:
        if not isinstance(cite, dict) or not isinstance(cite.get('file'), str) or not isinstance(cite.get('rows'), list):
            shown.append(f'a citation not of the form {{file, sha256, rows}}: {json.dumps(cite)}')
            continue
        root = Path(folder).resolve()
        path = (root / cite['file']).resolve()
        if not path.is_relative_to(root):
            shown.append(f"{cite['file']}: outside the results folder; not read")
            continue
        exists = path.is_file()
        try:
            data = path.read_bytes() if exists else b''
        except OSError as error:
            shown.append(f"{cite['file']}: exists; cannot be read ({type(error).__name__})")
            continue
        unchanged = exists and 'sha256:' + hashlib.sha256(data).hexdigest() == cite.get('sha256')
        lines = data.decode('utf-8', errors='replace').splitlines()
        rows = []
        for n in cite['rows'][:50]:
            if not isinstance(n, int) or not 0 < n <= len(lines):
                rows.append(f'row {n}: no such row')
                continue
            try:
                rows.append(f"row {n}: {json.loads(lines[n - 1]).get('outcome', 'no outcome')}")
            except (ValueError, AttributeError):
                rows.append(f'row {n}: not readable')
        shown.append(f"{cite['file']}: {'exists' if exists else 'does not exist'}; "
                     f"{'unchanged' if unchanged else 'not the file cited (digest differs)' if exists else 'unchanged: not known'}"
                     + (f"; {', '.join(rows)}" if rows else ''))
    return shown


def table(repo, folder, release, candidate):
    if not str(candidate or '').strip():
        raise SystemExit('the candidate named is empty; the table is for one named candidate')
    step_map = json.loads((Path(repo) / STEP_MAP).read_text())
    out = step_map.get('out_of_release', {})
    seen, contradictory, other, unreadable = results(folder, candidate)
    known = {step['step'] for steps in step_map['scenarios'].values() for step in steps}
    stray = sorted((set(seen) | set(contradictory)) - known)
    lines = [f'EXAMINATION TABLE for {release}, candidate {candidate}, from {STEP_MAP} at the checkout given', '',
             '| Scenario | Step | Counts | Outcome (REQ-007) | Date | Operated by |',
             '| --- | --- | --- | --- | --- | --- |']
    totals = dict.fromkeys(OUTCOMES, 0)
    removed, disputed, citations = 0, [], []
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
                last, why = contradictory[step['step']]
                shown = ', '.join(f"{r['file']} {r['outcome']}" for r in last)
                disputed.append(f"{step['step']}: {why} ({shown}); counted inconclusive")
                citations += [f"{step['step']} ({r['file']}) cites {c}" for r in last for c in cited(r, folder)]
                if step.get('counts'):
                    totals['inconclusive'] += 1
                lines.append(f"| {scenario} | {step['step']} | {counts} | inconclusive (records disagree) | {last[0]['date']} | — |")
                continue
            tied = seen.get(step['step'])
            record = tied[0] if tied else None
            if record is None:
                if step.get('counts'):
                    totals['not run'] += 1
                lines.append(f"| {scenario} | {step['step']} | {counts} | not run (no record) | — | — |")
                continue
            outcome = record['outcome']
            citations += [f"{step['step']} ({r['file']}) cites {c}" for r in tied for c in cited(r, folder)]
            if step.get('counts'):
                totals[outcome] += 1
            lines.append(f"| {scenario} | {step['step']} | {counts} | {outcome} | {record['date']} | {record.get('operated_by', '—')} |")
    lines += ['', 'Counted steps in the release: ' + ', '.join(f'{totals[o]} {o}' for o in OUTCOMES)
              + f'. Steps out of {release} by a recorded decision: {removed}.']
    if disputed:
        lines.append('Records that disagree: ' + ' | '.join(disputed))
    if stray:
        lines.append('Records naming no planned step (not counted): ' + ', '.join(stray))
    if citations:
        lines += ['', 'Cited rows, listed as cited (they never raise, lower or protect a step\'s outcome or any count):',
                  *(f'- {c}' for c in citations)]
    if other:
        lines.append(f'Records for another candidate, or naming none (not counted for {candidate}): ' + ', '.join(other))
    if unreadable:
        lines.append('Records that could not be read (not counted): ' + ', '.join(unreadable))
    return lines


def jsonl(path):
    """The rows of a .jsonl file, each a JSON object, or None if it cannot be read as that."""
    try:
        rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    except (OSError, ValueError):
        return None
    return rows if all(isinstance(row, dict) for row in rows) else None


def launch_keys(folder):
    """The candidate keys the launch records in a folder name, and the records that cannot be read. A launch record is
    read in the launcher's shape: candidate_key, or else identifier, at the top level; a nested bundle.identifier is
    read too."""
    keys, unread = set(), []
    for path in sorted(Path(folder).glob('launch-record*.json')):
        try:
            record = json.loads(path.read_text())
        except (OSError, ValueError) as error:
            unread.append(f'{path.name} ({type(error).__name__})')
            continue
        if not isinstance(record, dict):
            unread.append(f'{path.name} (not a record)')
            continue
        bundle = record.get('bundle') if isinstance(record.get('bundle'), dict) else {}
        named = record.get('candidate_key') if isinstance(record.get('candidate_key'), str) else None
        identifier = next((i for i in (record.get('identifier'), bundle.get('identifier')) if isinstance(i, str)), None)
        from_identifier = re.sub(r'^dev\.chirality\.app-v4\.candidate\.', '', identifier) if identifier else None
        if named and from_identifier and named != from_identifier:
            unread.append(f'{path.name} (its candidate_key and identifier disagree)')
        elif named or from_identifier:
            keys.add(named or from_identifier)
    return keys, unread


def comparisons(folders, standing=None):
    lines = ['', 'SESSION COMPARISON (rows of the execution lane\'s comparison; not step results)', '',
             *([f'Standing: {standing}', ''] if standing else []),
             '| Candidate | Comparison | ' + ' | '.join(OUTCOMES) + ' |', '| --- | --- |' + ' --- |' * len(OUTCOMES)]
    counts, notes, withheld = {}, [], set()
    for folder in folders:
        folder = Path(folder)
        if not folder.is_dir():
            notes.append(f'{folder}: not a folder that can be read; nothing from it is counted')
            continue
        keys, unread = launch_keys(folder)
        if unread:
            notes.append(f"{folder.name}: a launch record that cannot be read ({', '.join(unread)}); none of this folder's "
                         'rows is counted, since whose launch they were cannot be checked')
            continue
        files = []
        for p in sorted(folder.glob('session-comparison-*.jsonl')):
            if p.name.startswith('session-comparison-screen-'):
                continue
            rows = jsonl(p)
            if rows is None:
                notes.append(f'{p.name}: cannot be read as one JSON object per line; its rows are not counted')
            elif not rows:
                notes.append(f'{p.name}: empty; nothing in it is counted')
            else:
                files.append((p, rows))
        # Of the answers files made from one screen list, the latest counts. Names begin with the UTC time to the
        # second, then a random suffix; two with the same time cannot be ordered, so neither counts and both are noted.
        made_from = {}
        for path, rows in files:
            first = rows[0]
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
        for path, rows in files:
            header = next((row for row in rows if row.get('header')), {})
            if header.get('answers_of') in undecided:
                continue
            if header.get('answers_of') and latest_answers.get(header['answers_of']) != path:
                notes.append(f"{path.name}: replaced by {latest_answers[header['answers_of']].name}, made from the same screen list")
                continue
            summary = next((row for row in rows if 'summary' in row), None)
            if header.get('workflow_comparison'):
                withheld.add(header['workflow_comparison'])
            candidate = header.get('candidate_key')
            if candidate is not None and keys and keys != {candidate}:
                # The header and the launch record name different candidates: whose rows these are cannot be told.
                notes.append(f"{path.name}: its header names candidate {candidate} and the launch record "
                             f"{', '.join(sorted(keys))}; its rows are not counted")
                continue
            if candidate is None:
                # Never resolved through another field: the launch record beside it may be another launch's.
                candidate = f'not known ({path.name})'
            if header.get('fallback'):
                notes.append(f'{path.name}: written after a refusal or failure (fallback)'
                             + ('; it names no candidate, so its rows are counted under "not known"' if header.get('candidate_key') is None else ''))
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
                key = (candidate, str(row.get('comparison')))
                counts.setdefault(key, dict.fromkeys(OUTCOMES, 0))[row['outcome']] += 1
                seen.setdefault(str(row.get('comparison')), dict.fromkeys(OUTCOMES, 0))[row['outcome']] += 1
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
    parser.add_argument('--comparison-standing', help='a sentence printed at the head of the comparison section, for the '
                        'comparison tool\'s own standing (for example, a reading still out)')
    args = parser.parse_args(argv)
    print('\n'.join(table(args.repo, args.results, args.release, args.candidate) + (driver(args.driver) if args.driver else [])
                    + (comparisons(args.comparisons, args.comparison_standing) if args.comparisons else [])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
