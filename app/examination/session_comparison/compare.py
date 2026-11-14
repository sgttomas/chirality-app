#!/usr/bin/env python3
"""Session comparison, first part: one thread's turns, their outcomes and the
App's recorded interrupts, compared with Codex's own session file; and the
selected workflow's bytes, compared with what Codex recorded as the person's
input.

Codex's record is the session file Codex writes under its home
(`sessions/YYYY/MM/DD/rollout-<UTC time>-<threadId>.jsonl`). It is read only
inside an examination root (a folder the examination launcher made: `home/`,
`project/`, `record/`), never the owner's Codex home or any other. It is never
copied: each output row carries only identifiers, statuses, line numbers and
digests, never message or output text, so a lane acts on the rows without
opening the record.

The App's account is read three ways:
  - views: a saved `host_status` answer (`host-status-<checkpoint>.json`), where
    the build can save one; on a candidate, which cannot, the tool writes the
    list of what the screen must be found to say instead (`screen-list-<UTC>.jsonl`),
    for the operator to answer row by row (`answers` below);
  - the recovery ledger (SQLite, read-only): stop requests;
  - the workflow records (WR `run_text`).

The claim: a row says passed only when both sides were read, were identified as
the same subject by an identifier and not by position, and agree; every other
case is failed, inconclusive, blocked or not run; every planned comparison
yields at least one row; and no row carries message or output text.

Comparisons:
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
# What a saved view's turn status may be (the native TurnStatus), and what a
# stop request's turnOutcome may be (recovery.stop-request schema).
VIEW_STATUSES = ('inProgress', 'completed', 'failed', 'interrupted')
STOP_OUTCOMES = ('pending', 'interrupted', 'completed', 'failed', 'unknown')
# Codex's own end readings that no App reading can be compared with.
UNCOMPARABLE = ('started more than once', 'ended without a start', 'ended more than once', 'malformed end')
# The tag Codex 0.167.0 gives the person's own text; its other user-role
# messages (environment context, abort notice) are not the person's input.
PERSON = 'user.text'
EXACT = 'chirality.app.exact-bytes.sha256/v1'
MARKER = re.compile(r'<<<chirality-workflow (?P<name>[^\s@]+)@(?P<rev>[0-9a-f]{12}) begin>>>\n')
TOOL = 'app/examination/session_comparison/compare.py'


class Refused(Exception):
    """A side that cannot be read: its comparisons are blocked, with this reason."""


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def tool_digest():
    return sha256(Path(__file__).read_bytes())


def now_stamp():
    return datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')


# --- Where records may be read ---------------------------------------------

def examination_root(path):
    """The examination root, resolved; refused unless the launcher made it."""
    root = Path(path).resolve()
    record = root / 'record'
    if not (root / 'home').is_dir() or not record.is_dir():
        raise Refused(f'{root} is not an examination root (no home/ and record/)')
    if record.is_symlink() or record.resolve() != record:
        raise Refused('record/ does not resolve to the root\'s own record folder')
    if not (any(record.glob('launch-record*.json')) or (record / 'kept.json').is_file()):
        raise Refused(f'{root} has no launch record; only a folder the launcher made is read')
    codex = (Path.home() / '.codex').resolve()
    if root == codex or codex in root.parents or root in codex.parents:
        raise Refused("the owner's Codex home is never read")
    value = os.environ.get('CODEX_HOME')
    if value:
        other = Path(value).resolve()
        if other == root or root in other.parents or other in root.parents:
            raise Refused('CODEX_HOME of this process overlaps the examination root; refused')
    return root


def inside(root, path):
    """`path`, resolved, if it lies under `root`; refused otherwise."""
    real = Path(path).resolve()
    if root not in real.parents:
        raise Refused(f'{Path(path).name} resolves outside the examination root')
    return real


def candidate_key(root):
    for name in sorted((root / 'record').glob('launch-record*.json')) + [root / 'record' / 'kept.json']:
        try:
            key = json.loads(inside(root, name).read_text()).get('candidate_key')
        except (OSError, ValueError, AttributeError, Refused):
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

def end_of(payload):
    """A `task_complete`'s reading: completed with no error (absent or null),
    failed with an error object carrying a message, otherwise malformed."""
    if 'error' not in payload or payload['error'] is None:
        return 'completed'
    error = payload['error']
    if isinstance(error, dict) and isinstance(error.get('message'), str) and error['message']:
        return 'failed'
    return 'malformed end'


def read_session(path, thread):
    """Turns (in order of start) with their reported end, and the person's own
    messages, each with its line number. Refused unless its first line names
    this thread."""
    turns, order, person = {}, [], []
    try:
        raw_lines = Path(path).read_bytes().splitlines()
    except OSError as e:
        raise Refused(f'the session file could not be read ({e.__class__.__name__})')
    for number, raw in enumerate(raw_lines, 1):
        try:
            line = json.loads(raw)
        except ValueError:
            raise Refused(f'line {number} of the session file is not JSON')
        if not isinstance(line, dict) or not isinstance(line.get('payload', {}), dict):
            raise Refused(f'line {number} of the session file is not a session line')
        kind, payload = line.get('type'), line.get('payload') or {}
        if number == 1:
            if kind != 'session_meta' or payload.get('id') != thread:
                raise Refused('the session file does not begin with session_meta naming this thread')
            continue
        if kind == 'event_msg':
            event, turn = payload.get('type'), payload.get('turn_id')
            if not isinstance(turn, str) or not turn:
                continue
            if event in ('task_started', 'turn_started'):
                if turn in turns:
                    turns[turn]['starts'] += 1
                else:
                    order.append(turn)
                    turns[turn] = {'started': number, 'starts': 1, 'ends': 0, 'end': None}
            elif event in ('task_complete', 'turn_complete', 'turn_aborted'):
                entry = turns.setdefault(turn, {'started': None, 'starts': 0, 'ends': 0, 'end': None})
                if turn not in order:
                    order.append(turn)
                entry['ends'] += 1
                if event == 'turn_aborted':
                    entry['end'] = {'status': 'interrupted', 'reason': payload.get('reason'), 'line': number, 'from': event}
                else:
                    entry['end'] = {'status': end_of(payload), 'line': number, 'from': event}
        elif kind == 'response_item' and payload.get('type') == 'message' and payload.get('role') == 'user':
            meta = payload.get('internal_chat_message_metadata_passthrough') or {}
            kinds = meta.get('content_item_kinds') if isinstance(meta, dict) else None
            if kinds != [PERSON]:
                continue
            parts = [c.get('text', '') for c in payload.get('content') or [] if isinstance(c, dict) and isinstance(c.get('text', ''), str)]
            person.append({'line': number, 'turn': meta.get('turn_id'), 'parts': parts})
    return {'turns': turns, 'order': order, 'person': person}


def codex_status(turn):
    if turn['starts'] != 1:
        return 'started more than once' if turn['starts'] > 1 else 'ended without a start'
    if turn['ends'] > 1:
        return 'ended more than once'
    return turn['end']['status'] if turn['end'] else 'not reported'


def codex_side(turn):
    said = codex_status(turn)
    end = turn['end']
    side = {'says': said, 'from': end['from'] if end else 'task_started', 'line': end['line'] if end else turn['started']}
    if end and 'reason' in end:
        side['reason'] = end['reason']
    return side


# --- The App's account --------------------------------------------------------

def view_turns(view, thread):
    """Turn id to the status the view holds, for `thread`, joined by turn id as
    the App's own view joins them, never by position."""
    native = view.get('nativeView') if isinstance(view, dict) else None
    if not isinstance(native, dict):
        raise Refused('the saved view has no nativeView')
    keys, values = native.get('turnRecords'), native.get('turns')
    if not isinstance(keys, list) or not isinstance(values, list):
        raise Refused('the saved view has no readable nativeView turns')
    by_id = {}
    for value in values:
        if not isinstance(value, dict) or not isinstance(value.get('id'), str):
            raise Refused('a turn in the saved view has no identity')
        if value['id'] in by_id:
            raise Refused(f'the saved view holds turn {value["id"]} twice')
        by_id[value['id']] = value
    shown = {}
    for key in keys:
        if not isinstance(key, dict):
            raise Refused('a turn record in the saved view is not readable')
        if key.get('threadId') != thread:
            continue
        turn = key.get('turnId')
        if turn not in by_id:
            raise Refused(f'the saved view names turn {turn} with no turn of that identity')
        if turn in shown:
            raise Refused(f'the saved view names turn {turn} twice')
        shown[turn] = by_id[turn].get('status')
    return shown


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
        try:
            record = json.loads(entry).get('record')
        except (ValueError, TypeError, AttributeError):
            raise Refused(f'ledger row {seq} is not a readable stop request')
        if not isinstance(record, dict):
            raise Refused(f'ledger row {seq} carries no stop-request record')
        if record.get('threadId') == thread and record.get('stopRequestId'):
            latest[record['stopRequestId']] = (seq, record)
    return list(latest.values())


def run_text_records(root, thread):
    """WR `run_text` records of runs in `thread`, and the workflow record files
    that could not be read (which may belong to it)."""
    found, unreadable = [], []
    for path in sorted(root.rglob('*.json')):
        if 'workflow' not in path.parts or 'records' not in path.parts:
            continue
        where = path.relative_to(root).as_posix()
        try:
            value = json.loads(inside(root, path).read_text())
        except (OSError, ValueError, Refused):
            unreadable.append(where)
            continue
        records = value if isinstance(value, list) else [value.get('record', value)] if isinstance(value, dict) else None
        if records is None:
            unreadable.append(where)
            continue
        for record in records:
            if isinstance(record, dict) and record.get('record_kind') == 'run_text' and record.get('conversation') == thread:
                found.append((where, record))
    return found, unreadable


def manifest_workflow(manifest, name, revision):
    if not isinstance(manifest, dict):
        return None
    for package in manifest.get('packages', []) if isinstance(manifest.get('packages'), list) else []:
        if isinstance(package, dict) and package.get('name') == name and package.get('revision') == revision:
            for f in package.get('files', []) if isinstance(package.get('files'), list) else []:
                if isinstance(f, dict) and f.get('path') == 'WORKFLOW.md':
                    return f.get('sha256')
    return None


def workflow_bytes(text, name, rev):
    """The exact WORKFLOW.md bytes `compose_run_text` put between this
    workflow's markers, or None."""
    begin = f'<<<chirality-workflow {name}@{rev} begin>>>\n'
    end = f'\n<<<chirality-workflow {name}@{rev} end>>>'
    start = text.find(begin)
    if start < 0:
        return None
    stop = text.find(end, start + len(begin))
    return text[start + len(begin):stop] if stop >= 0 else None


# --- Comparisons --------------------------------------------------------------

def row(comparison, subject, codex, app, outcome, reason):
    assert outcome in OUTCOMES
    return {'comparison': comparison, 'subject': subject, 'codex': codex, 'app': app, 'outcome': outcome, 'reason': reason}


def compare_views(session, thread, shown, at):
    """C2 and C3 against a saved view taken after the session ended."""
    rows, turns = [], session['turns']
    view = lambda says: {'says': says, 'from': 'view:nativeView.turns', 'at': at}
    if not session['order'] and not shown:
        return [row('C2', {'thread': thread}, {'says': 'no turn'}, view('no turn'), 'not run', 'Codex recorded no turn in this thread, and the view shows none'),
                row('C3', {'thread': thread}, {'says': 'no turn'}, view('no turn'), 'not run', 'no turn to compare')]
    for turn in session['order']:
        subject = {'thread': thread, 'turn': turn}
        codex = codex_side(turns[turn])
        said = codex['says']
        if turn not in shown:
            rows.append(row('C2', subject, codex, view('absent'), 'failed', 'Codex started this turn; the App does not show it'))
            rows.append(row('C3', subject, codex, view('absent'), 'blocked', 'the view does not show this turn'))
            continue
        app = view(shown[turn])
        rows.append(row('C2', subject, codex, app, 'passed', 'both have this turn, by its identity'))
        if said in UNCOMPARABLE:
            rows.append(row('C3', subject, codex, app, 'inconclusive', f"Codex's record of this turn is not one reading: {said}"))
        elif shown[turn] not in VIEW_STATUSES:
            rows.append(row('C3', subject, codex, app, 'inconclusive', "the App's status is not one this comparison knows"))
        elif said == 'not reported':
            if shown[turn] in TERMINAL:
                rows.append(row('C3', subject, codex, app, 'failed', f'the App shows {shown[turn]}; Codex reported no end, so it must read as not known'))
            else:
                rows.append(row('C3', subject, codex, app, 'passed', 'neither reports an end'))
        elif shown[turn] == said:
            rows.append(row('C3', subject, codex, app, 'passed', f'both say {said}'))
        else:
            rows.append(row('C3', subject, codex, app, 'failed', f'the App shows {shown[turn]}; Codex recorded {said}'))
    for turn in sorted(set(shown) - set(turns)):
        subject = {'thread': thread, 'turn': turn}
        rows.append(row('C2', subject, {'says': 'absent', 'from': 'session file'}, view(shown[turn]), 'failed', 'the App shows a turn of which Codex has no record'))
        rows.append(row('C3', subject, {'says': 'absent', 'from': 'session file'}, view(shown[turn]), 'blocked', 'Codex has no record of this turn'))
    return rows


def compare_stops(session, thread, stops):
    """C4: each stop request the App recorded, against Codex's end of that turn."""
    if not stops:
        return [row('C4', {'thread': thread}, {'says': 'not compared'}, {'says': 'no stop request', 'from': 'ledger:stop_request'}, 'not run',
                    'no stop was requested in this thread')]
    rows, turns = [], session['turns']
    for seq, record in stops:
        turn = record.get('turnId')
        subject = {'thread': thread, 'turn': turn, 'stopRequest': record.get('stopRequestId')}
        recorded = record.get('turnOutcome')
        app = {'says': recorded, 'from': 'ledger:stop_request', 'seq': seq, 'state': record.get('state'), 'outcomeSource': record.get('outcomeSource')}
        if turn not in turns:
            rows.append(row('C4', subject, {'says': 'absent', 'from': 'session file'}, app, 'failed', 'the App recorded a stop of a turn of which Codex has no record'))
            continue
        codex = codex_side(turns[turn])
        said = codex['says']
        if said in UNCOMPARABLE:
            rows.append(row('C4', subject, codex, app, 'inconclusive', f"Codex's record of this turn is not one reading: {said}"))
        elif recorded not in STOP_OUTCOMES:
            rows.append(row('C4', subject, codex, app, 'inconclusive', "the App's recorded outcome is not one this comparison knows"))
        elif recorded == 'interrupted':
            if said == 'interrupted' and codex.get('reason') == 'interrupted':
                rows.append(row('C4', subject, codex, app, 'passed', 'both say interrupted'))
            elif said == 'interrupted':
                rows.append(row('C4', subject, codex, app, 'failed', f'the App recorded an interrupt; Codex aborted the turn for another reason ({codex.get("reason")})'))
            else:
                rows.append(row('C4', subject, codex, app, 'failed', f'the App recorded interrupted; Codex recorded {said}'))
        elif recorded in TERMINAL:
            if recorded == said:
                rows.append(row('C4', subject, codex, app, 'passed', f'both say {said}'))
            else:
                rows.append(row('C4', subject, codex, app, 'failed', f'the App recorded {recorded}; Codex recorded {said}'))
        elif said == 'not reported':
            rows.append(row('C4', subject, codex, app, 'passed', 'neither records an end; the App says it is not known'))
        else:
            rows.append(row('C4', subject, codex, app, 'inconclusive', f'the App recorded the outcome as {recorded}; Codex recorded {said}, which the App did not learn'))
    return rows


def compare_workflow(session, thread, records, unreadable, manifest):
    """W1: for each run, the bundled WORKFLOW.md, the run_text record and the
    bytes Codex recorded in the person's message for that run. The message is
    the run's by its identity (its whole text is the run's text) and only then
    can the row pass. Failing that, a message carrying this workflow's markers
    that no other run claims can show a difference (failed), never agreement."""
    rows, claimed, plans = [], set(), []
    for where in unreadable:
        rows.append(row('W1', {'thread': thread}, {'says': 'not compared'}, {'says': 'unreadable', 'from': where}, 'blocked',
                        'a workflow record could not be read; whether it belongs to this thread is not known'))
    for where, record in records:
        workflow = record.get('workflow') if isinstance(record.get('workflow'), dict) else {}
        name, revision = workflow.get('name'), workflow.get('revision')
        rev = revision[:12] if isinstance(revision, str) and len(revision) >= 12 else None
        identity = record.get('text_identity') if isinstance(record.get('text_identity'), dict) else {}
        found = None
        if identity.get('method') == EXACT:
            for m in session['person']:
                if m['line'] in claimed:
                    continue
                for text in m['parts'] + [''.join(m['parts'])]:
                    if sha256(text.encode()) == identity.get('value'):
                        found = (m, text, True)
                        break
                if found:
                    claimed.add(m['line'])
                    break
        plans.append([where, record, name, revision, rev, found])
    for plan in plans:
        where, record, name, revision, rev, found = plan
        if found is None and rev is not None:
            for m in session['person']:
                text = next((t for t in m['parts'] + [''.join(m['parts'])] if workflow_bytes(t, name, rev) is not None), None)
                if m['line'] not in claimed and text is not None:
                    plan[5] = (m, text, False)
                    claimed.add(m['line'])
                    break
    for where, record, name, revision, rev, found in plans:
        subject = {'thread': thread, 'run': record.get('run'), 'workflow': f'{name}@{rev}'}
        bundled = manifest_workflow(manifest, name, revision)
        content = (record.get('workflow_file') or {}).get('content') if isinstance(record.get('workflow_file'), dict) else None
        recorded = content.get('value') if isinstance(content, dict) and content.get('method') == EXACT else None
        app = {'says': {'bundled': bundled, 'runText': recorded}, 'from': f'manifest; {where}'}
        if manifest is None:
            rows.append(row('W1', subject, {'says': 'not compared'}, app, 'blocked', 'the bundled manifest could not be read'))
            continue
        if bundled is None:
            rows.append(row('W1', subject, {'says': 'not compared'}, app, 'blocked', 'the bundled manifest names no WORKFLOW.md for this workflow and revision'))
            continue
        if recorded is None or rev is None:
            rows.append(row('W1', subject, {'says': 'not compared'}, app, 'blocked', 'the run_text record carries no exact-bytes digest or no full revision'))
            continue
        if found is None:
            rows.append(row('W1', subject, {'says': 'absent', 'from': 'session file'}, app, 'blocked',
                            "no message Codex tagged as the person's carries this run's text or this workflow"))
            continue
        message, text, by_identity = found
        given_bytes = workflow_bytes(text, name, rev)
        if given_bytes is None:
            rows.append(row('W1', subject, {'says': 'no markers', 'from': 'person message', 'line': message['line']}, app, 'failed',
                            "the run's text carries no markers for this workflow and revision"))
            continue
        given = {'says': sha256(given_bytes.encode()), 'from': 'person message', 'line': message['line'],
                 'identifiedBy': 'the run text identity' if by_identity else 'this workflow\'s markers only'}
        agree = bundled == recorded == given['says']
        unequal = [n for n, v in (('bundled', bundled), ('run_text', recorded)) if v != given['says']]
        if agree and by_identity:
            rows.append(row('W1', subject, given, app, 'passed', "the three digests are equal: these bytes are what Codex recorded as the person's input"))
        elif agree:
            rows.append(row('W1', subject, given, app, 'inconclusive',
                            "the workflow's bytes agree, but no message carries this run's whole text, so the message is not identified as this run's"))
        else:
            rows.append(row('W1', subject, given, app, 'failed', f'differs from what Codex recorded: {", ".join(unequal) or "bundled and run_text disagree"}'))
    for m in session['person']:
        if m['line'] not in claimed and any(MARKER.search(t) for t in m['parts']):
            rows.append(row('W1', {'thread': thread}, {'says': 'workflow given', 'from': 'person message', 'line': m['line']},
                            {'says': 'no run_text record of it'}, 'inconclusive',
                            "Codex recorded a workflow in the person's input; the App has no run record whose text it is"))
    if not rows:
        rows.append(row('W1', {'thread': thread}, {'says': 'no workflow given'}, {'says': 'no run_text record of this thread'}, 'not run',
                        'no workflow run was started in this thread'))
    return rows


def screen_items(session, thread):
    """On a candidate, which cannot save its views: what the screen must be
    found to say, from Codex's record alone, for the operator to answer."""
    items = []
    for turn in session['order']:
        said = codex_status(session['turns'][turn])
        must = {'not reported': 'not known (the turn has no reported end)'}.get(said, said)
        items.append({'comparison': 'C2+C3', 'subject': {'thread': thread, 'turn': turn}, 'screen_must_say': f'the turn is shown, and shown as {must}'})
    others = ', '.join(session['order']) or 'none'
    items.append({'comparison': 'C2', 'subject': {'thread': thread},
                  'screen_must_say': f'the screen shows no turn of this thread other than these: {others}'})
    for item in items:
        item['digest'] = item_digest(item)
    return items


def item_digest(item):
    return sha256(json.dumps({k: item.get(k) for k in ('comparison', 'subject', 'screen_must_say')}, sort_keys=True).encode())


# --- Commands -----------------------------------------------------------------

def header(root, **extra):
    return {'header': True, 'candidate_key': candidate_key(root), 'examination_root': str(root), 'tool': TOOL, 'tool_sha256': tool_digest(), **extra}


def summary(rows):
    counts = {}
    for r in rows:
        counts.setdefault(r['comparison'], {}).setdefault(r['outcome'], 0)
        counts[r['comparison']][r['outcome']] += 1
    return {'summary': counts}


def write(root, stem, head, body, with_summary=True):
    """A new file in record/, never over an existing one (the launcher's rule).
    A summary is written only if it is derived from these rows."""
    record = root / 'record'
    if record.is_symlink() or record.resolve() != record:
        raise Refused("record/ does not resolve to the root's own record folder; nothing is written")
    lines = [head] + body
    if with_summary:
        total = summary(body)
        recount = {}
        for r in body:
            recount.setdefault(r['comparison'], {}).setdefault(r['outcome'], 0)
            recount[r['comparison']][r['outcome']] += 1
        if total['summary'] != recount or sum(sum(v.values()) for v in total['summary'].values()) != len(body):
            raise Refused('the summary does not agree with its rows; nothing is written')
        lines.append(total)
    stamp = now_stamp()
    for n in range(100):
        path = record / (f'{stem}-{stamp}.jsonl' if n == 0 else f'{stem}-{stamp}-{n}.jsonl')
        try:
            with open(path, 'x') as f:
                for line in lines:
                    f.write(json.dumps(line, sort_keys=True) + '\n')
            return path
        except FileExistsError:
            continue
    raise Refused('no new file name was free in record/; nothing is written')


def compare(root, thread, views, manifest):
    try:
        path = session_file(root, thread)
        session = read_session(path, thread)
        digest = sha256(path.read_bytes())
    except Refused as e:
        return [row(c, {'thread': thread}, {'says': 'not read'}, {'says': 'not compared'}, 'blocked', str(e)) for c in ('C2', 'C3', 'C4', 'W1')], None, None
    rows = []
    for view in views:
        try:
            saved = json.loads(inside(root, view).read_text())
            rows += compare_views(session, thread, view_turns(saved, thread), Path(view).name)
        except (Refused, OSError, ValueError) as e:
            reason = str(e) if isinstance(e, Refused) else f'the saved view could not be read ({e.__class__.__name__})'
            for c in ('C2', 'C3'):
                rows.append(row(c, {'thread': thread}, {'says': 'read'}, {'says': 'not read', 'from': Path(view).name}, 'blocked', reason))
    try:
        rows += compare_stops(session, thread, stop_records(root, thread))
    except Refused as e:
        rows.append(row('C4', {'thread': thread}, {'says': 'read'}, {'says': 'not read'}, 'blocked', str(e)))
    records, unreadable = run_text_records(root, thread)
    rows += compare_workflow(session, thread, records, unreadable, manifest)
    return rows, session, digest


def answers(root, screen_path):
    """The operator's answers to a screen list, as rows. Only an answer to an
    item the list was written with, unchanged, counts; a passed needs a note."""
    screen = inside(root, screen_path)
    try:
        lines = [json.loads(l) for l in screen.read_text().splitlines() if l.strip()]
    except (OSError, ValueError):
        raise Refused('the screen list could not be read')
    head = lines[0] if lines and isinstance(lines[0], dict) else {}
    if head.get('header') is not True or head.get('examination_root') != str(root) or head.get('candidate_key') != candidate_key(root):
        raise Refused('the screen list was not written for this examination root and candidate')
    if head.get('tool_sha256') != tool_digest():
        raise Refused('the screen list was written by another version of this tool')
    thread, listed = head.get('thread'), head.get('items')
    if not isinstance(listed, list) or not isinstance(thread, str):
        raise Refused('the screen list carries no list of its items')
    try:
        if sha256(session_file(root, thread).read_bytes()) != head.get('session_sha256'):
            raise Refused('the session file has changed since the screen list was written')
    except Refused as e:
        raise Refused(str(e))
    digests = [i.get('digest') for i in listed if isinstance(i, dict)]
    given = {}
    for item in lines[1:]:
        if not isinstance(item, dict):
            raise Refused('an item of the screen list is not readable')
        digest = item_digest(item)
        if digest not in digests or item.get('digest') != digest:
            raise Refused('the screen list holds an item it was not written with, or an edited item')
        if digest in given:
            raise Refused('the screen list holds an item twice')
        given[digest] = item
    rows = []
    for item in listed:
        answered = given.get(item.get('digest'))
        codex = {'says': item['screen_must_say'], 'from': 'session file'}
        if answered is None:
            rows.append(row(item['comparison'], item['subject'], codex, {'says': None, 'from': 'operator, against the screen'}, 'not run', 'deleted from the screen list'))
            continue
        answer, note = answered.get('answer'), answered.get('note')
        app = {'says': answer, 'note_sha256': sha256(note.encode()) if isinstance(note, str) and note else None, 'from': 'operator, against the screen'}
        if answer not in ('passed', 'failed', 'inconclusive'):
            rows.append(row(item['comparison'], item['subject'], codex, app, 'not run', 'not answered'))
        elif answer == 'passed' and app['note_sha256'] is None:
            rows.append(row(item['comparison'], item['subject'], codex, app, 'not run', 'answered passed with no note of what was seen'))
        else:
            rows.append(row(item['comparison'], item['subject'], codex, app, answer, 'answered by the operator'))
    return rows


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    sub = p.add_subparsers(dest='command', required=True)
    c = sub.add_parser('compare', help='compare one thread; with --view, the views exactly; without, write the screen list')
    c.add_argument('--root', required=True)
    c.add_argument('--thread', required=True)
    c.add_argument('--view', action='append', default=[], help='a saved host_status answer under record/, taken after the session ended')
    c.add_argument('--manifest', required=True, help='the bundled MANIFEST.json of the build examined')
    a = sub.add_parser('answers', help="turn the operator's answers to a screen list into rows")
    a.add_argument('--root', required=True)
    a.add_argument('--screen', required=True)
    args = p.parse_args(argv)
    try:
        root = examination_root(args.root)
        if args.command == 'compare':
            try:
                manifest = json.loads(Path(args.manifest).read_text())
            except (OSError, ValueError):
                manifest = None
            rows, session, digest = compare(root, args.thread, args.view, manifest)
            print(write(root, 'session-comparison', header(root), rows))
            if not args.view and session is not None:
                items = screen_items(session, args.thread)
                head = header(root, thread=args.thread, session_sha256=digest, items=items)
                print(write(root, 'screen-list', head, [{**i, 'answer': None, 'note': None} for i in items], with_summary=False))
            return 0
        rows = answers(root, args.screen)
        # The table counts only the latest answers file of one screen list.
        print(write(root, 'session-comparison', header(root, answers_of=Path(args.screen).name), rows))
        return 0
    except Refused as e:
        print(f'refused: {e}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
