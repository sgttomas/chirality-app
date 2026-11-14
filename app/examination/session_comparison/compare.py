#!/usr/bin/env python3
"""Session comparison, first part: one thread's turns, their outcomes and the
App's recorded interrupts, compared with Codex's own session file; and the
selected workflow's bytes, compared with what Codex's record shows it was given.

Codex's record is the session file Codex writes under its home
(`sessions/YYYY/MM/DD/rollout-<UTC time>-<threadId>.jsonl`). It is read only
inside an examination root (a folder the examination launcher made: `home/`,
`project/`, `record/`), never the owner's Codex home or any other. It is never
copied: each output row carries only identifiers, statuses, line numbers and
digests, so a lane acts on the rows without opening the record.

The App's account is read three ways:
  - views: a saved `host_status` answer (`host-status-<checkpoint>.json`), where
    the build can save one; on a candidate, which cannot, the tool writes the
    list of what the screen must be found to say instead, for the operator to
    answer row by row (`screen` and `answers` below);
  - the recovery ledger (SQLite, read-only): stop requests;
  - the workflow records (WR `run_text`).

Each row ends in one of DEL-09-02 REQ-007's five outcomes. Comparisons:
  C2  turns, both ways (views)
  C3  each turn's outcome (views)
  C4  each interrupt the App recorded (ledger)
  W1  the selected workflow's bytes (bundled manifest, run_text record, Codex)
Standard library only; nothing is sent anywhere.
"""
import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

OUTCOMES = ('passed', 'failed', 'blocked', 'not run', 'inconclusive')
TERMINAL = ('completed', 'failed', 'interrupted')
MARKER = re.compile(r'<<<chirality-workflow (?P<name>[^\s@]+)@(?P<rev>[0-9a-f]+) begin>>>\n')
TOOL = 'app/examination/session_comparison/compare.py'


class Refused(Exception):
    """A side that cannot be read: its comparisons are blocked, with this reason."""


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def now_stamp():
    return datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')


# --- Where records may be read ---------------------------------------------

def examination_root(path):
    """The examination root, resolved; refused unless launch.py made it."""
    root = Path(path).resolve()
    record = root / 'record'
    if not (root / 'home').is_dir() or not record.is_dir():
        raise Refused(f'{root} is not an examination root (no home/ and record/)')
    if not (any(record.glob('launch-record*.json')) or (record / 'kept.json').is_file()):
        raise Refused(f'{root} has no launch record; only a folder launch.py made is read')
    codex = (Path.home() / '.codex').resolve()
    if root == codex or codex in root.parents or root in codex.parents:
        raise Refused("the owner's Codex home is never read")
    for name in ('CODEX_HOME',):
        value = os.environ.get(name)
        if value:
            other = Path(value).resolve()
            if other == root or root in other.parents or other in root.parents:
                raise Refused(f'{name} of this process overlaps the examination root; refused')
    return root


def inside(root, path):
    """`path`, resolved, if it lies under `root`; refused otherwise."""
    real = Path(path).resolve()
    if root not in real.parents:
        raise Refused(f'{path} resolves outside the examination root')
    return real


def candidate_key(root):
    for name in sorted((root / 'record').glob('launch-record*.json')) + [root / 'record' / 'kept.json']:
        try:
            key = json.loads(name.read_text()).get('candidate_key')
        except (OSError, ValueError):
            continue
        if isinstance(key, str) and key:
            return key
    return None


def session_file(root, thread):
    """The one session file of `thread` under the root's Codex homes."""
    found = [p for p in root.rglob(f'rollout-*-{thread}.jsonl') if 'sessions' in p.relative_to(root).parts]
    if not found:
        raise Refused(f'no session file of thread {thread} under the examination root')
    if len(found) > 1:
        raise Refused(f'{len(found)} session files name thread {thread}; which one is the record is not established')
    return inside(root, found[0])


# --- Codex's record ----------------------------------------------------------

def read_session(path):
    """Turns (in order of start) with their reported end, and the user messages,
    each with its line number. Only what the comparisons need is kept."""
    turns, order, messages, current = {}, [], [], None
    with open(path, 'rb') as f:
        for number, raw in enumerate(f, 1):
            try:
                line = json.loads(raw)
            except ValueError:
                raise Refused(f'line {number} of the session file is not JSON')
            kind, payload = line.get('type'), line.get('payload') or {}
            if kind == 'event_msg':
                event = payload.get('type')
                turn = payload.get('turn_id')
                if event in ('task_started', 'turn_started') and turn:
                    if turn not in turns:
                        order.append(turn)
                        turns[turn] = {'started': number, 'end': None}
                    current = turn
                elif event in ('task_complete', 'turn_complete') and turn:
                    status = 'failed' if payload.get('error') else 'completed'
                    turns.setdefault(turn, {'started': None, 'end': None})['end'] = {'status': status, 'line': number, 'from': event}
                elif event == 'turn_aborted' and turn:
                    turns.setdefault(turn, {'started': None, 'end': None})['end'] = {
                        'status': 'interrupted', 'reason': payload.get('reason'), 'line': number, 'from': event}
            elif kind == 'response_item' and payload.get('type') == 'message' and payload.get('role') == 'user':
                text = ''.join(c.get('text', '') for c in payload.get('content') or [] if isinstance(c, dict))
                messages.append({'line': number, 'turn': current, 'text': text})
    for turn in turns:
        if turn not in order:
            order.append(turn)
    return {'turns': turns, 'order': order, 'messages': messages}


def codex_status(turn):
    end = turn['end']
    return end['status'] if end else 'not reported'


# --- The App's account --------------------------------------------------------

def view_turns(view, thread):
    """Turn id to the status the view holds, for `thread`, from `nativeView`."""
    native = view.get('nativeView') if isinstance(view.get('nativeView'), dict) else view
    keys, values = native.get('turnRecords'), native.get('turns')
    if not isinstance(keys, list) or not isinstance(values, list) or len(keys) != len(values):
        raise Refused('the saved view has no readable nativeView turns')
    return {k['turnId']: v.get('status') for k, v in zip(keys, values) if k.get('threadId') == thread}


def ledger_path(root):
    found = [p for p in root.rglob('recovery.ledger.sqlite')]
    if len(found) != 1:
        raise Refused(f'{len(found)} recovery ledgers under the examination root; exactly one is read')
    return inside(root, found[0])


def stop_records(root, thread):
    """The latest stop-request record of each stop request on `thread`, with its ledger row."""
    path = ledger_path(root)
    try:
        db = sqlite3.connect(f'{path.as_uri()}?mode=ro', uri=True)
        try:
            rows = db.execute("SELECT seq, entry FROM ledger_entry WHERE kind = 'stop_request' ORDER BY seq").fetchall()
        finally:
            db.close()
    except sqlite3.Error as e:
        raise Refused(f'the recovery ledger could not be read: {e}')
    latest = {}
    for seq, entry in rows:
        record = json.loads(entry).get('record') or {}
        if record.get('threadId') == thread and record.get('stopRequestId'):
            latest[record['stopRequestId']] = (seq, record)
    return list(latest.values())


def run_text_records(root, thread):
    """WR `run_text` records of runs in `thread`, wherever the records store holds them."""
    found = []
    for path in root.rglob('*.json'):
        if 'workflow' not in path.parts or 'records' not in path.parts:
            continue
        try:
            value = json.loads(inside(root, path).read_text())
        except (OSError, ValueError):
            continue
        for record in (value if isinstance(value, list) else [value.get('record', value)] if isinstance(value, dict) else []):
            if isinstance(record, dict) and record.get('record_kind') == 'run_text' and record.get('conversation') == thread:
                found.append((path.relative_to(root).as_posix(), record))
    return found


def manifest_workflow(manifest, name, revision):
    for package in manifest.get('packages', []):
        if package.get('name') == name and package.get('revision') == revision:
            for f in package.get('files', []):
                if f.get('path') == 'WORKFLOW.md':
                    return f.get('sha256')
    return None


# --- Comparisons --------------------------------------------------------------

def row(comparison, subject, codex, app, outcome, reason):
    assert outcome in OUTCOMES
    return {'comparison': comparison, 'subject': subject, 'codex': codex, 'app': app, 'outcome': outcome, 'reason': reason}


def compare_views(session, thread, shown, at):
    """C2 and C3 against a saved view taken after the session ended."""
    rows, turns = [], session['turns']
    for turn in session['order']:
        subject = {'thread': thread, 'turn': turn}
        said = codex_status(turns[turn])
        codex = {'says': said, 'from': turns[turn]['end']['from'] if turns[turn]['end'] else 'task_started',
                 'line': turns[turn]['end']['line'] if turns[turn]['end'] else turns[turn]['started']}
        if turn not in shown:
            rows.append(row('C2', subject, codex, {'says': 'absent', 'from': 'view:nativeView.turns', 'at': at}, 'failed',
                            'Codex started this turn; the App does not show it'))
            continue
        app = {'says': shown[turn], 'from': 'view:nativeView.turns', 'at': at}
        rows.append(row('C2', subject, codex, app, 'passed', 'both have this turn'))
        if said == 'not reported':
            if shown[turn] in TERMINAL:
                rows.append(row('C3', subject, codex, app, 'failed',
                                f'the App shows {shown[turn]}; Codex reported no end, so it must read as not known'))
            else:
                rows.append(row('C3', subject, codex, app, 'passed', 'neither reports an end'))
        elif shown[turn] == said:
            rows.append(row('C3', subject, codex, app, 'passed', f'both say {said}'))
        else:
            rows.append(row('C3', subject, codex, app, 'failed', f'the App shows {shown[turn]}; Codex recorded {said}'))
    for turn in sorted(set(shown) - set(turns)):
        rows.append(row('C2', {'thread': thread, 'turn': turn}, {'says': 'absent', 'from': 'session file'},
                        {'says': shown[turn], 'from': 'view:nativeView.turns', 'at': at}, 'failed',
                        'the App shows a turn of which Codex has no record'))
    return rows


def compare_stops(session, thread, stops):
    """C4: each stop request the App recorded, against Codex's end of that turn."""
    rows, turns = [], session['turns']
    for seq, record in stops:
        turn = record.get('turnId')
        subject = {'thread': thread, 'turn': turn, 'stopRequest': record.get('stopRequestId')}
        app = {'says': record.get('turnOutcome'), 'from': 'ledger:stop_request', 'seq': seq,
               'state': record.get('state'), 'outcomeSource': record.get('outcomeSource')}
        if turn not in turns:
            rows.append(row('C4', subject, {'says': 'absent', 'from': 'session file'}, app, 'failed',
                            'the App recorded a stop of a turn of which Codex has no record'))
            continue
        said = codex_status(turns[turn])
        end = turns[turn]['end']
        codex = {'says': said, 'from': end['from'] if end else 'task_started', 'line': end['line'] if end else turns[turn]['started']}
        if end and end.get('reason'):
            codex['reason'] = end['reason']
        recorded = record.get('turnOutcome')
        if recorded in TERMINAL:
            if recorded == said:
                rows.append(row('C4', subject, codex, app, 'passed', f'both say {said}'))
            else:
                rows.append(row('C4', subject, codex, app, 'failed', f'the App recorded {recorded}; Codex recorded {said}'))
        elif said == 'not reported':
            rows.append(row('C4', subject, codex, app, 'passed', 'neither records an end; the App says it is not known'))
        else:
            rows.append(row('C4', subject, codex, app, 'inconclusive',
                            f'the App recorded the outcome as {recorded}; Codex recorded {said}, which the App did not learn'))
    return rows


def compare_workflow(session, thread, records, manifest):
    """W1: the bundled WORKFLOW.md, the run_text record and what Codex was given."""
    rows = []
    for where, record in records:
        workflow = record.get('workflow') or {}
        name, revision = workflow.get('name'), workflow.get('revision')
        subject = {'thread': thread, 'run': record.get('run'), 'workflow': f'{name}@{(revision or "")[:12]}'}
        bundled = manifest_workflow(manifest, name, revision) if manifest is not None else None
        content = (record.get('workflow_file') or {}).get('content') or {}
        recorded = content.get('value') if content.get('method') == 'chirality.app.exact-bytes.sha256/v1' else None
        app = {'says': {'bundled': bundled, 'runText': recorded}, 'from': f'manifest; {where}'}
        given = None
        for message in session['messages']:
            match = MARKER.search(message['text'])
            if not match or match['name'] != name or not (revision or '').startswith(match['rev']):
                continue
            end = f'\n<<<chirality-workflow {match["name"]}@{match["rev"]} end>>>'
            stop = message['text'].find(end, match.end())
            if stop >= 0:
                given = {'says': sha256(message['text'][match.end():stop].encode()), 'from': 'response_item user message', 'line': message['line']}
                break
        if bundled is None:
            rows.append(row('W1', subject, given or {'says': 'not read'}, app, 'blocked',
                            'the bundled manifest names no WORKFLOW.md for this workflow and revision'))
        elif recorded is None:
            rows.append(row('W1', subject, given or {'says': 'not read'}, app, 'blocked', 'the run_text record carries no exact-bytes digest'))
        elif given is None:
            rows.append(row('W1', subject, {'says': 'absent', 'from': 'session file'}, app, 'blocked',
                            "no user message in Codex's record carries this workflow between its markers"))
        elif bundled == recorded == given['says']:
            rows.append(row('W1', subject, given, app, 'passed', 'the three digests are equal; what Codex was given is not what the model adopted'))
        else:
            unequal = [n for n, v in (('bundled', bundled), ('run_text', recorded)) if v != given['says']]
            rows.append(row('W1', subject, given, app, 'failed', f'differs from what Codex was given: {", ".join(unequal)}'))
    return rows


def screen_list(session, thread):
    """On a candidate, which cannot save its views: what the screen must be found
    to say of each turn, from Codex's record alone, for the operator to answer."""
    items = []
    for turn in session['order']:
        said = codex_status(session['turns'][turn])
        must = 'not known (the turn has no reported end)' if said == 'not reported' else said
        items.append({'comparison': 'C2+C3', 'subject': {'thread': thread, 'turn': turn},
                      'screen_must_say': f'the turn is shown, and shown as {must}', 'answer': None, 'note': None})
    return items


# --- Commands -----------------------------------------------------------------

def header(root):
    return {'header': True, 'candidate_key': candidate_key(root), 'examination_root': str(root), 'tool': TOOL}


def summary(rows):
    counts = {}
    for r in rows:
        counts.setdefault(r['comparison'], {}).setdefault(r['outcome'], 0)
        counts[r['comparison']][r['outcome']] += 1
    return {'summary': counts}


def write(root, stem, lines):
    """A new file in record/, never over an existing one (the launcher's rule)."""
    path = root / 'record' / f'{stem}-{now_stamp()}.jsonl'
    with open(path, 'x') as f:
        for line in lines:
            f.write(json.dumps(line, sort_keys=True) + '\n')
    return path


def compare(root, thread, views, manifest):
    rows = []
    try:
        session = read_session(session_file(root, thread))
    except Refused as e:
        return [row(c, {'thread': thread}, {'says': 'not read'}, {'says': 'not compared'}, 'blocked', str(e)) for c in ('C2', 'C3', 'C4', 'W1')], None
    for view in views:
        try:
            saved = json.loads(inside(root, view).read_text())
            rows += compare_views(session, thread, view_turns(saved, thread), Path(view).name)
        except (Refused, OSError, ValueError) as e:
            rows.append(row('C2', {'thread': thread}, {'says': 'read'}, {'says': 'not read', 'from': str(view)}, 'blocked', str(e)))
    try:
        rows += compare_stops(session, thread, stop_records(root, thread))
    except Refused as e:
        rows.append(row('C4', {'thread': thread}, {'says': 'read'}, {'says': 'not read'}, 'blocked', str(e)))
    try:
        found = run_text_records(root, thread)
        if found:
            rows += compare_workflow(session, thread, found, manifest)
        else:
            rows.append(row('W1', {'thread': thread}, {'says': 'read'}, {'says': 'no run_text record of this thread'}, 'not run',
                            'no workflow run was started in this thread'))
    except Refused as e:
        rows.append(row('W1', {'thread': thread}, {'says': 'read'}, {'says': 'not read'}, 'blocked', str(e)))
    return rows, session


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    sub = p.add_subparsers(dest='command', required=True)
    c = sub.add_parser('compare', help='compare one thread; with --view, the views exactly; without, write the screen list')
    c.add_argument('--root', required=True)
    c.add_argument('--thread', required=True)
    c.add_argument('--view', action='append', default=[], help='a saved host_status answer under record/, taken after the session ended')
    c.add_argument('--manifest', required=True, help="the bundled MANIFEST.json of the build examined")
    a = sub.add_parser('answers', help="turn the operator's answers to a screen list into rows")
    a.add_argument('--root', required=True)
    a.add_argument('--screen', required=True)
    args = p.parse_args(argv)
    try:
        root = examination_root(args.root)
    except Refused as e:
        print(f'refused: {e}', file=sys.stderr)
        return 2
    if args.command == 'compare':
        manifest = json.loads(Path(args.manifest).read_text())
        rows, session = compare(root, args.thread, args.view, manifest)
        out = write(root, 'session-comparison', [header(root)] + rows + [summary(rows)])
        print(out)
        if not args.view and session is not None:
            print(write(root, 'session-comparison-screen', [header(root)] + screen_list(session, args.thread)))
        return 0
    rows = []
    for line in inside(root, args.screen).read_text().splitlines()[1:]:
        item = json.loads(line)
        answer = item.get('answer')
        outcome = answer if answer in ('passed', 'failed', 'inconclusive') else 'not run'
        rows.append(row(item['comparison'], item['subject'], {'says': item['screen_must_say'], 'from': 'session file'},
                        {'says': item.get('note'), 'from': 'operator, against the screen'}, outcome,
                        'answered by the operator' if outcome != 'not run' else 'not answered'))
    print(write(root, 'session-comparison', [header(root)] + rows + [summary(rows)]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
