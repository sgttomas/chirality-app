#!/usr/bin/env python3
"""Session comparison, first part: one thread's turns, their outcomes and the
App's recorded interrupts, compared with Codex's own session file.

It compares exactly three things: turns (C2), outcomes (C3) and interrupts
(C4). The workflow comparison (W1) is not available in this version: its
association of a run with a message needed a new rule in each of three
readings, and it comes in its own change with its own reading. Where a session
has a workflow run to compare, a W1 row says so with the outcome blocked; W1 is
never passed and never left out, and asking for it by name is refused.

Codex's record is the session file Codex writes under its home
(`sessions/YYYY/MM/DD/rollout-<UTC time>-<threadId>.jsonl`). It is read only
inside an examination root (a folder the examination launcher made: `home/`,
`project/`, `record/`), never the owner's Codex home or any other, and never
copied.

The claim: a row says passed only when both sides were read, were identified as
the same subject by an identifier and not by position, and agree; every other
case is failed, inconclusive, blocked or not run; every planned comparison
yields at least one row; and no row carries message or output text.

How it holds:
  - A strict model. The session file's bytes are read once; their digest and
    the model are made from those same bytes. Every line must be a session
    line, the first must name this thread and the pinned Codex version, and
    every turn event must carry a turn identity; otherwise every comparison
    is blocked. A turn whose events are not one start and at most one end is
    not one reading, and is never compared as agreeing.
  - Values by allowlist. Every value written into a row is from a closed set,
    or an identifier, a digest or a number of its pattern; anything else is
    written as "unrecognised", which never passes and is counted apart.
    Reasons are the tool's own sentences. No text from any input reaches a row.
  - A candidate's result comes whole from `answers`, which derives the screen
    list again from the session file as it is then, takes only the answers to
    items it derives identically, and computes C4 from the same bytes.
  - Nothing ends without rows: after the root is admitted, any refusal or
    failure writes blocked rows for every planned comparison, naming at most
    the kind of failure.

Comparisons: C2 turns (both ways, every turn the view shows), C3 each turn's
outcome, C4 each interrupt the App recorded. Standard library only; nothing is
sent anywhere.
"""
import argparse
import hashlib
import json
import os
import re
import secrets
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

MODEL_VERSION = 'session-comparison-model/1'
# The Codex version whose session file layout this model was written against.
PINNED_CODEX = '0.167.0'
TOOL = 'app/examination/session_comparison/compare.py'
PLANNED = ('C2', 'C3', 'C4')
COMPARES = {'C2': 'turns', 'C3': 'outcomes', 'C4': 'interrupts'}
NOT_AVAILABLE = 'the workflow comparison is not available in this version'
WORKFLOW_NAMES = ('w1', 'workflow')
WORKFLOW_MARKER = b'<<<chirality-workflow '
OUTCOMES = ('passed', 'failed', 'blocked', 'not run', 'inconclusive')
TERMINAL = ('completed', 'failed', 'interrupted')
VIEW_STATUSES = ('inProgress', 'completed', 'failed', 'interrupted')
STOP_OUTCOMES = ('pending', 'interrupted', 'completed', 'failed', 'unknown')
STOP_STATES = ('requested', 'sent', 'not-sent', 'accepted', 'refused', 'settled', 'outcome-unknown', 'outcome-recovered', 'send-unknown')
OUTCOME_SOURCES = ('observed', 'recovered-from-supplier', 'not-observed')
ABORT_REASONS = ('interrupted', 'replaced', 'review_ended', 'budget_limited')
UNRECOGNISED = 'unrecognised'
# A turn the view shows with no native turn behind it (by an item, a checklist
# or an error notice only): shown, but with no status.
NO_STATUS = 'shown with no status'
ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._:@-]{0,159}$')
HEX64 = re.compile(r'^[0-9a-f]{64}$')
START_EVENTS = ('task_started', 'turn_started')
END_EVENTS = ('task_complete', 'turn_complete', 'turn_aborted')


class Refused(Exception):
    """A side that cannot be read: its comparisons are blocked, with this reason
    (always one of the tool's own sentences)."""


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def tool_digest():
    return sha256(Path(__file__).read_bytes())


# --- Values by allowlist -------------------------------------------------------

def ident(value):
    return value if isinstance(value, str) and ID.match(value) else UNRECOGNISED


def digest(value):
    return value if isinstance(value, str) and HEX64.match(value) else UNRECOGNISED


def one_of(value, allowed):
    return value if value in allowed else UNRECOGNISED


def number(value):
    return value if isinstance(value, int) and not isinstance(value, bool) else UNRECOGNISED


def has_unrecognised(value):
    if isinstance(value, dict):
        return any(has_unrecognised(v) for v in value.values())
    return value == UNRECOGNISED


def row(comparison, subject, codex, app, outcome, reason):
    """One row. `subject`, `codex` and `app` hold only allowlisted values; a row
    naming anything unrecognised can never pass."""
    assert outcome in OUTCOMES and (comparison in PLANNED or (comparison == 'W1' and outcome == 'blocked'))
    if outcome == 'passed' and (has_unrecognised(subject) or has_unrecognised(codex) or has_unrecognised(app)):
        outcome, reason = 'inconclusive', 'a value on one side is not one this comparison recognises'
    return {'comparison': comparison, 'subject': subject, 'codex': codex, 'app': app, 'outcome': outcome, 'reason': reason}


def blocked_all(thread, reason):
    """Every planned comparison blocked; and, since whether the session has a
    workflow run is then not known, the workflow comparison's row as well."""
    return [row(c, {'thread': ident(thread)}, {'says': 'not read'}, {'says': 'not compared'}, 'blocked', reason) for c in PLANNED] + \
        [row('W1', {'thread': ident(thread)}, {'says': 'not read'}, {'says': 'not compared'}, 'blocked', NOT_AVAILABLE)]


# --- Where records may be read ---------------------------------------------

def examination_root(path):
    """The examination root, resolved; refused unless the launcher made it."""
    root = Path(path).resolve()
    record = root / 'record'
    if not (root / 'home').is_dir() or not (root / 'project').is_dir() or not record.is_dir():
        raise Refused('the folder is not an examination root (no home/, project/ and record/)')
    if record.is_symlink() or record.resolve() != record:
        raise Refused("record/ does not resolve to the root's own record folder")
    launch = sorted(record.glob('launch-record*.json')) + ([record / 'kept.json'] if (record / 'kept.json').exists() else [])
    if not launch:
        raise Refused('the folder has no launch record; only a folder the launcher made is read')
    for name in launch:
        if name.is_symlink() or root not in name.resolve().parents:
            raise Refused('a launch record resolves outside the examination root')
    codex = (Path.home() / '.codex').resolve()
    if root == codex or codex in root.parents or root in codex.parents:
        raise Refused("the owner's Codex home is never read")
    value = os.environ.get('CODEX_HOME')
    if value:
        other = Path(value).resolve()
        if other == root or root in other.parents or other in root.parents:
            raise Refused('the CODEX_HOME of this process overlaps the examination root')
    return root


def inside(root, path):
    real = Path(path).resolve()
    if root not in real.parents:
        raise Refused('a file resolves outside the examination root')
    return real


def candidate_key(root):
    for name in sorted((root / 'record').glob('launch-record*.json')) + [root / 'record' / 'kept.json']:
        try:
            key = json.loads(inside(root, name).read_text()).get('candidate_key')
        except Exception:
            continue
        if ident(key) != UNRECOGNISED:
            return key
    return None


def session_file(root, thread):
    if ident(thread) == UNRECOGNISED:
        raise Refused('the thread given is not an identifier')
    found = [p for p in root.rglob(f'rollout-*-{thread}.jsonl') if 'sessions' in p.relative_to(root).parts]
    if not found:
        raise Refused('no session file of this thread under the examination root')
    if len(found) > 1:
        raise Refused('more than one session file names this thread')
    return inside(root, found[0])


# --- The strict model of Codex's record ----------------------------------------

def read_session(root, thread):
    """(model, digest) from one read of the session file's bytes."""
    path = session_file(root, thread)
    try:
        data = path.read_bytes()
    except OSError:
        raise Refused('the session file could not be read')
    return parse_session(data, thread), sha256(data)


def parse_session(data, thread):
    lines = data.splitlines()
    if not lines:
        raise Refused('the session file is empty')
    events, order = {}, []
    for number_, raw in enumerate(lines, 1):
        try:
            line = json.loads(raw)
        except Exception:
            raise Refused('a line of the session file is not JSON')
        if not isinstance(line, dict) or not isinstance(line.get('type'), str) or not isinstance(line.get('payload'), dict):
            raise Refused('a line of the session file is not a session line')
        kind, payload = line['type'], line['payload']
        if number_ == 1:
            if kind != 'session_meta' or payload.get('id') != thread:
                raise Refused('the session file does not begin with session_meta naming this thread')
            if payload.get('cli_version') != PINNED_CODEX:
                raise Refused('the session file was written by a Codex version this model was not written against')
            continue
        if kind == 'event_msg':
            event = payload.get('type')
            if event in START_EVENTS or event in END_EVENTS:
                turn = payload.get('turn_id')
                if ident(turn) == UNRECOGNISED:
                    raise Refused('a turn event of the session file carries no turn identity')
                if turn not in events:
                    events[turn] = []
                    order.append(turn)
                events[turn].append((number_, event, payload))
    turns = {turn: reading(events[turn]) for turn in order}
    marked = sum(1 for raw in lines if WORKFLOW_MARKER in raw)
    return {'thread': thread, 'order': order, 'turns': turns, 'workflow_marked_lines': marked}


def reading(events):
    """One turn's reading: one start, then at most one end; anything else is
    not one reading."""
    kinds = [e[1] for e in events]
    first = events[0][0]
    if len(events) > 2 or kinds[0] not in START_EVENTS or (len(events) == 2 and kinds[1] not in END_EVENTS):
        return {'says': 'not one reading', 'line': first, 'from': 'turn events'}
    if len(events) == 1:
        return {'says': 'not reported', 'line': first, 'from': 'task_started'}
    line, event, payload = events[1]
    if event == 'turn_aborted':
        return {'says': 'interrupted', 'reason': one_of(payload.get('reason'), ABORT_REASONS), 'line': line, 'from': 'turn_aborted'}
    if 'error' not in payload or payload['error'] is None:
        return {'says': 'completed', 'line': line, 'from': 'task_complete'}
    error = payload['error']
    if isinstance(error, dict) and isinstance(error.get('message'), str) and error['message']:
        return {'says': 'failed', 'line': line, 'from': 'task_complete'}
    return {'says': 'not one reading', 'line': line, 'from': 'task_complete'}


# --- The App's account --------------------------------------------------------

def view_turns(root, view, thread):
    """Turn id to the status the view holds, for every turn the App's view shows
    in this thread: as the panel does, the union of its turn records and the
    turns its items, checklists and error notices name. Joined by identity,
    never by position. A turn shown with no native turn has no status."""
    try:
        saved = json.loads(inside(root, view).read_text())
    except Refused:
        raise
    except Exception:
        raise Refused('the saved view could not be read')
    native = saved.get('nativeView') if isinstance(saved, dict) else None
    if not isinstance(native, dict) or not isinstance(native.get('turnRecords'), list) or not isinstance(native.get('turns'), list):
        raise Refused('the saved view has no readable nativeView turns')
    by_id = {}
    for value in native['turns']:
        if not isinstance(value, dict) or ident(value.get('id')) == UNRECOGNISED or value['id'] in by_id:
            raise Refused('a turn of the saved view has no identity, or appears twice')
        by_id[value['id']] = value
    shown, recorded = {}, set()
    for key in native['turnRecords']:
        if not isinstance(key, dict) or ident(key.get('threadId')) == UNRECOGNISED or ident(key.get('turnId')) == UNRECOGNISED:
            raise Refused('a turn record of the saved view is not readable')
        turn = key['turnId']
        if turn not in by_id or turn in recorded:
            raise Refused('a turn record of the saved view names no single turn of that identity')
        recorded.add(turn)
        if key['threadId'] == thread:
            shown[turn] = one_of(by_id[turn].get('status'), VIEW_STATUSES)
    if set(by_id) != recorded:
        raise Refused('a turn of the saved view has no turn record, so its thread is not known')
    for name in ('items', 'revisions', 'turnErrors', 'unreadableTurnErrors'):
        entries = native.get(name, [])
        if not isinstance(entries, list):
            raise Refused('a list of the saved view is not readable')
        for entry in entries:
            if not isinstance(entry, dict):
                raise Refused('an entry of the saved view is not readable')
            if name == 'revisions' and entry.get('kind') != 'checklist':
                continue
            if entry.get('threadId') != thread:
                continue
            turn = entry.get('turnId')
            if ident(turn) == UNRECOGNISED:
                raise Refused('an entry of the saved view names no turn this comparison can read')
            shown.setdefault(turn, NO_STATUS)
    return shown


def stop_records(root, thread):
    found = [p for p in root.rglob('recovery.ledger.sqlite')]
    if len(found) != 1:
        raise Refused('there is not exactly one recovery ledger under the examination root')
    path = inside(root, found[0])
    try:
        db = sqlite3.connect(f'{path.as_uri()}?mode=ro', uri=True)
        try:
            rows = db.execute("SELECT seq, entry FROM ledger_entry WHERE kind = 'stop_request' ORDER BY seq").fetchall()
        finally:
            db.close()
    except Exception:
        raise Refused('the recovery ledger could not be read')
    latest, unreadable = {}, 0
    for seq, entry in rows:
        try:
            record = json.loads(entry)['record']
            assert isinstance(record, dict)
        except Exception:
            raise Refused('a stop request in the ledger is not readable')
        if record.get('threadId') != thread:
            continue
        stop = record.get('stopRequestId')
        if not (isinstance(stop, str) and stop.startswith('stop:') and ident(stop[5:]) != UNRECOGNISED) or ident(record.get('turnId')) == UNRECOGNISED:
            unreadable += 1
            continue
        latest[stop] = (seq, record)
    return list(latest.values()), unreadable


# --- Comparisons --------------------------------------------------------------

def codex_of(model, turn):
    r = model['turns'][turn]
    side = {'says': r['says'], 'from': r['from'], 'line': r['line']}
    if 'reason' in r:
        side['reason'] = r['reason']
    return side


def compare_views(model, shown, at):
    thread, rows = model['thread'], []
    view = lambda says: {'says': says, 'from': 'view:nativeView.turns', 'at': at}
    if not model['order'] and not shown:
        return [row('C2', {'thread': thread}, {'says': 'no turn'}, view('no turn'), 'not run', 'Codex recorded no turn in this thread, and the view shows none'),
                row('C3', {'thread': thread}, {'says': 'no turn'}, view('no turn'), 'not run', 'there is no turn to compare')]
    for turn in model['order']:
        subject = {'thread': thread, 'turn': turn}
        codex = codex_of(model, turn)
        if turn not in shown:
            rows.append(row('C2', subject, codex, view('absent'), 'failed', 'Codex started this turn; the App does not show it'))
            rows.append(row('C3', subject, codex, view('absent'), 'blocked', 'the view does not show this turn'))
            continue
        app = view(shown[turn])
        rows.append(row('C2', subject, codex, app, 'passed', 'both have this turn, by its identity'))
        said = codex['says']
        if said == 'not one reading':
            rows.append(row('C3', subject, codex, app, 'inconclusive', "Codex's record of this turn is not one start and at most one end"))
        elif shown[turn] == UNRECOGNISED:
            rows.append(row('C3', subject, codex, app, 'inconclusive', "the App's status is not one this comparison knows"))
        elif shown[turn] == NO_STATUS:
            rows.append(row('C3', subject, codex, app, 'inconclusive', 'the view shows this turn with no native status'))
        elif said == 'not reported':
            failed = shown[turn] in TERMINAL
            rows.append(row('C3', subject, codex, app, 'failed' if failed else 'passed',
                            'the App shows an end Codex did not report' if failed else 'neither reports an end'))
        elif shown[turn] == said:
            rows.append(row('C3', subject, codex, app, 'passed', 'both give the same end'))
        else:
            rows.append(row('C3', subject, codex, app, 'failed', 'the App shows a different end from the one Codex recorded'))
    for turn in sorted(set(shown) - set(model['turns'])):
        subject = {'thread': thread, 'turn': turn}
        absent = {'says': 'absent', 'from': 'session file'}
        rows.append(row('C2', subject, absent, view(shown[turn]), 'failed', 'the App shows a turn of which Codex has no record'))
        rows.append(row('C3', subject, absent, view(shown[turn]), 'blocked', 'Codex has no record of this turn'))
    return rows


def compare_stops(model, stops, unreadable):
    thread, rows = model['thread'], []
    for _ in range(unreadable):
        rows.append(row('C4', {'thread': thread}, {'says': 'not compared'}, {'says': UNRECOGNISED, 'from': 'ledger:stop_request'}, 'blocked',
                        'a stop request of this thread names no stop or turn this comparison can read'))
    for seq, record in stops:
        turn = record['turnId']
        subject = {'thread': thread, 'turn': turn, 'stopRequest': record['stopRequestId'][5:]}
        recorded = one_of(record.get('turnOutcome'), STOP_OUTCOMES)
        app = {'says': recorded, 'from': 'ledger:stop_request', 'seq': number(seq), 'state': one_of(record.get('state'), STOP_STATES),
               'outcomeSource': one_of(record.get('outcomeSource'), OUTCOME_SOURCES)}
        if turn not in model['turns']:
            rows.append(row('C4', subject, {'says': 'absent', 'from': 'session file'}, app, 'failed', 'the App recorded a stop of a turn of which Codex has no record'))
            continue
        codex = codex_of(model, turn)
        said = codex['says']
        if said == 'not one reading':
            rows.append(row('C4', subject, codex, app, 'inconclusive', "Codex's record of this turn is not one start and at most one end"))
        elif recorded == UNRECOGNISED:
            rows.append(row('C4', subject, codex, app, 'inconclusive', "the App's recorded outcome is not one this comparison knows"))
        elif recorded == 'interrupted':
            agree = said == 'interrupted' and codex.get('reason') == 'interrupted'
            rows.append(row('C4', subject, codex, app, 'passed' if agree else 'failed',
                            'both record an interrupt' if agree else 'the App recorded an interrupt; Codex recorded no abort for that reason'))
        elif recorded in TERMINAL:
            agree = recorded == said
            rows.append(row('C4', subject, codex, app, 'passed' if agree else 'failed',
                            'both record the same end' if agree else 'the App recorded a different end from Codex'))
        elif said == 'not reported':
            rows.append(row('C4', subject, codex, app, 'passed', 'neither records an end; the App says it is not known'))
        else:
            rows.append(row('C4', subject, codex, app, 'inconclusive', 'Codex recorded an end the App did not learn'))
    if not rows:
        rows.append(row('C4', {'thread': thread}, {'says': 'not compared'}, {'says': 'no stop request', 'from': 'ledger:stop_request'}, 'not run',
                        'no stop was requested in this thread'))
    return rows


def records_rows(root, model):
    """C4, blocked on its own if the ledger cannot be read."""
    try:
        stops, bad = stop_records(root, model['thread'])
        return compare_stops(model, stops, bad)
    except Refused as e:
        return [row('C4', {'thread': model['thread']}, {'says': 'read'}, {'says': 'not read'}, 'blocked', str(e))]


def run_text_records(root, thread):
    """How many of the App's run text records name `thread`, and how many
    workflow record files could not be read (any of which may)."""
    found = unreadable = 0
    for path in sorted(root.rglob('*.json')):
        parts = path.relative_to(root).parts
        if 'records' not in parts or 'workflow' not in parts:
            continue
        try:
            value = json.loads(inside(root, path).read_text())
        except Exception:
            unreadable += 1
            continue
        records = value if isinstance(value, list) else [value.get('record', value)] if isinstance(value, dict) else None
        if records is None or not all(isinstance(r, dict) for r in records):
            unreadable += 1
            continue
        found += sum(1 for r in records if r.get('record_kind') == 'run_text' and r.get('conversation') == thread)
    return found, unreadable


def workflow_rows(root, model):
    """One blocked W1 row where the session has a workflow run to compare (a
    line of Codex's record carries the workflow markers, or a run text record
    names the thread, or a workflow record could not be read), and none
    otherwise. W1 is never compared, so it never passes."""
    try:
        found, unreadable = run_text_records(root, model['thread'])
    except Exception:
        found, unreadable = 0, 1
    marked = model.get('workflow_marked_lines', 0)
    if not (marked or found or unreadable):
        return []
    return [row('W1', {'thread': model['thread']}, {'linesWithWorkflowMarkers': number(marked)},
                {'runTextRecords': number(found), 'unreadableWorkflowRecords': number(unreadable)}, 'blocked', NOT_AVAILABLE)]


# --- The candidate's screen list ------------------------------------------------

def screen_items(model):
    """What the screen must be found to say, derived from Codex's record alone."""
    thread, items = model['thread'], []
    for turn in model['order']:
        said = model['turns'][turn]['says']
        items.append({'comparison': 'C2', 'subject': {'thread': thread, 'turn': turn}, 'screen_must_say': 'the turn is shown'})
        must = {'not reported': 'not known (no end reported)', 'not one reading': None}.get(said, said)
        if must:
            items.append({'comparison': 'C3', 'subject': {'thread': thread, 'turn': turn}, 'screen_must_say': f'the turn is shown as {must}'})
    shown = ', '.join(model['order']) or 'none'
    items.append({'comparison': 'C2', 'subject': {'thread': thread}, 'screen_must_say': f'no turn of this thread is shown other than: {shown}'})
    for item in items:
        item['digest'] = item_digest(item)
    return items


def item_digest(item):
    try:
        return sha256(json.dumps({k: item[k] for k in ('comparison', 'subject', 'screen_must_say')}, sort_keys=True).encode())
    except Exception:
        return None


def answered_rows(model, answers):
    """The screen list derived now, each item taking the operator's answer only
    from one line identical to it. Nothing in the list file is trusted."""
    by_digest = {}
    for line in answers:
        d = item_digest(line) if isinstance(line, dict) else None
        if d is not None and line.get('digest') == d:
            by_digest.setdefault(d, []).append(line)
    rows = []
    for item in screen_items(model):
        lines = by_digest.get(item['digest'], [])
        codex = {'says': 'derived from the session file', 'from': 'session file', 'item': item['digest']}
        operator = {'says': None, 'from': 'operator, against the screen'}
        if len(lines) != 1:
            rows.append(row(item['comparison'], item['subject'], codex, operator, 'not run', 'no single answer to this item'))
            continue
        answer, note = lines[0].get('answer'), lines[0].get('note')
        noted = isinstance(note, str) and note.strip() != ''
        if answer not in ('passed', 'failed', 'inconclusive'):
            rows.append(row(item['comparison'], item['subject'], codex, operator, 'not run', 'not answered'))
            continue
        app = {'says': answer, 'note': sha256(note.encode('utf-8', 'replace')) if noted else None, 'from': 'operator, against the screen'}
        if answer == 'passed' and not noted:
            rows.append(row(item['comparison'], item['subject'], codex, app, 'not run', 'answered passed with no note of what was seen'))
        else:
            rows.append(row(item['comparison'], item['subject'], codex, app, answer, 'answered by the operator against the screen'))
    return rows


# --- Output -------------------------------------------------------------------

def header(root, **extra):
    return {'header': True, 'candidate_key': candidate_key(root), 'examination_root': str(root), 'tool': TOOL,
            'tool_sha256': tool_digest(), 'model_version': MODEL_VERSION, 'pinned_codex': PINNED_CODEX,
            'compares': COMPARES, 'workflow_comparison': NOT_AVAILABLE, **extra}


def summary(rows):
    counts = {}
    for r in rows:
        counts.setdefault(r['comparison'], {}).setdefault(r['outcome'], 0)
        counts[r['comparison']][r['outcome']] += 1
    return {'summary': counts, 'unrecognised': sum(1 for r in rows if has_unrecognised(r)),
            'compares': COMPARES, 'workflow_comparison': NOT_AVAILABLE}


def write(root, stem, head, body, with_summary=True, fallback=False):
    """A new file in record/, never over an existing one. A summary is written
    only if it agrees with its rows and every planned comparison has one. The
    fallback's summary is counted from its own blocked rows alone, with none
    of that checking to fail."""
    record = root / 'record'
    if record.is_symlink() or record.resolve() != record:
        raise Refused("record/ does not resolve to the root's own record folder")
    lines = [head] + body
    if fallback:
        counts = {}
        for r in body:
            counts.setdefault(r['comparison'], {'blocked': 0})['blocked'] += 1
        lines.append({'summary': counts, 'unrecognised': 0, 'compares': COMPARES, 'workflow_comparison': NOT_AVAILABLE})
    elif with_summary:
        total = summary(body)
        if sum(sum(v.values()) for v in total['summary'].values()) != len(body) or not {r['comparison'] for r in body} >= set(PLANNED):
            raise Refused('the summary would not agree with the rows, or a planned comparison has no row')
        lines.append(total)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    for _ in range(8):
        path = record / f'{stem}-{stamp}-{secrets.token_hex(4)}.jsonl'
        try:
            with open(path, 'x') as f:
                for line in lines:
                    f.write(json.dumps(line, sort_keys=True) + '\n')
            return path
        except FileExistsError:
            continue
    raise Refused('no new file name was free in record/')


def unnamed_views(root, named):
    """Saved views in record/ that this run was not given: said, never silently passed over."""
    given = {Path(v).resolve() for v in named}
    return sorted(ident(p.name) for p in (root / 'record').glob('host-status-*.json') if p.resolve() not in given)


def run_compare(root, thread, views):
    """(rows, None) with a saved view; (None, (model, digest)) on a candidate."""
    try:
        model, session_sha = read_session(root, thread)
    except Refused as e:
        return blocked_all(thread, str(e)), None
    if not views:
        return None, (model, session_sha)
    rows = []
    for view in views:
        at = ident(Path(view).name)
        try:
            rows += compare_views(model, view_turns(root, view, thread), at)
        except Refused as e:
            for c in ('C2', 'C3'):
                rows.append(row(c, {'thread': thread}, {'says': 'read'}, {'says': 'not read', 'from': 'view', 'at': at}, 'blocked', str(e)))
    return rows + records_rows(root, model) + workflow_rows(root, model), None


def run_answers(root, screen):
    try:
        lines = [json.loads(l) for l in inside(root, screen).read_text().splitlines() if l.strip()]
        thread = lines[0]['thread']
    except Refused as e:
        return blocked_all(None, str(e))
    except Exception:
        return blocked_all(None, 'the screen list could not be read')
    try:
        model, _ = read_session(root, thread)
    except Refused as e:
        return blocked_all(thread, str(e))
    return answered_rows(model, lines[1:]) + records_rows(root, model) + workflow_rows(root, model)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    sub = p.add_subparsers(dest='command', required=True)
    c = sub.add_parser('compare', help='with --view, compare exactly and write rows; without, write the screen list for a candidate')
    c.add_argument('--root', required=True)
    c.add_argument('--thread', required=True)
    c.add_argument('--view', action='append', default=[], help='a saved host_status answer under record/, taken after the session ended')
    a = sub.add_parser('answers', help="the candidate's complete result: the operator's answers, with C4")
    a.add_argument('--root', required=True)
    a.add_argument('--screen', required=True)
    for parser in (c, a):
        parser.add_argument('--comparison', action='append', default=[],
                            help='a comparison asked for by name (C2, C3 or C4; all three are always made). '
                                 'The workflow comparison is not available in this version.')
    args = p.parse_args(argv)
    for name in args.comparison:
        if name.strip().lower() in WORKFLOW_NAMES:
            print(f'refused: {NOT_AVAILABLE}', file=sys.stderr)
            return 2
        if name not in PLANNED:
            print('refused: this tool has no comparison of that name', file=sys.stderr)
            return 2
    try:
        root = examination_root(args.root)
    except Refused as e:
        print(f'refused: {e}', file=sys.stderr)
        return 2
    thread = getattr(args, 'thread', None)
    try:
        unnamed = unnamed_views(root, getattr(args, 'view', []))
        if unnamed:
            print(f'note: saved views in record/ not named in this run: {", ".join(unnamed)}', file=sys.stderr)
        if args.command == 'compare':
            if not args.view and unnamed:
                raise Refused('a saved view exists in record/, so the operator\'s list is not written; name it with --view')
            rows, pending = run_compare(root, args.thread, args.view)
            if pending is not None:
                model, session_sha = pending
                print(write(root, 'screen-list', header(root, thread=args.thread, session_sha256=session_sha, saved_views_not_named=unnamed),
                            [{**i, 'answer': None, 'note': None} for i in screen_items(model)], with_summary=False))
                return 0
            print(write(root, 'session-comparison', header(root, saved_views_not_named=unnamed), rows))
            return 0
        rows = run_answers(root, args.screen)
        print(write(root, 'session-comparison', header(root, answers_of=ident(Path(args.screen).name), saved_views_not_named=unnamed), rows))
        return 0
    except Exception as e:
        # Nothing ends without rows: the failure's kind, and no more.
        reason = str(e) if isinstance(e, Refused) else f'the comparison failed ({e.__class__.__name__})'
        try:
            print(write(root, 'session-comparison', header(root), blocked_all(thread, reason), fallback=True))
            return 1
        except Exception as inner:
            print(f'refused: no result could be written ({inner.__class__.__name__})', file=sys.stderr)
            return 2


if __name__ == '__main__':
    sys.exit(main())
