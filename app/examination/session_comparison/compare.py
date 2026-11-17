#!/usr/bin/env python3
"""Session comparison: one thread's turns, their outcomes, the App's recorded
interrupts and, where the thread holds one workflow run, the workflow supplied,
compared with Codex's own session file.

It always compares turns (C2), outcomes (C3) and interrupts (C4). The workflow
comparison (W1) covers an examination root with one run, not the association
of a run with a message: it can pass only when the candidate's records store
in the root holds records of exactly one run (one run start, of this thread,
and otherwise only end notices and supply checks naming that run); Codex's
record of the thread holds exactly one line mentioning the workflow markers, a
message; and the one text element of that message mentioning them equals that
run text byte for byte, with the files line of the candidate's package and the
candidate's own WORKFLOW.md bytes of the selected bundled revision between its
markers, as the examiner's copy in record/selected-workflow/ gives them, tied
to the candidate's identification. Anything else, or anything unreadable or
untied, is blocked, never passed and never inferred. Several runs in a root,
and children, are not compared. Where a session has no workflow run, and W1
was not asked for by name, there is no W1 row.

Codex's record is the session file Codex writes under its home
(`sessions/YYYY/MM/DD/rollout-<UTC time>-<threadId>.jsonl`). It is read only
inside an examination root (a folder the examination launcher made: `home/`,
`project/`, `record/`), never the owner's Codex home or any other, and never
copied.

The claim: a row says passed only when both sides were read, were identified as
the same subject by an identifier and not by position (for W1, by being the
root's only run and the thread's only message mentioning the markers), and agree; every other
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
outcome, C4 each interrupt the App recorded, W1 the workflow supplied in a
root with one run. Standard library only, except that W1 runs the candidate
identification's own record validation (identify.py, which uses jsonschema);
nothing is sent anywhere.
"""
import argparse
import hashlib
import json
import os
import re
import secrets
import sqlite3
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path

MODEL_VERSION = 'session-comparison-model/2'
# The one Codex version whose session file layout this model was checked
# against, on a real session file made at that version. A file of any other
# version is blocked; a new pin needs its own check before this changes.
PINNED_CODEX = '0.169.0'
TOOL = 'app/examination/session_comparison/compare.py'
# Always made, each with at least one row. W1 is made where the session has a
# workflow run to compare, and has no row otherwise.
PLANNED = ('C2', 'C3', 'C4')
NAMED = PLANNED + ('W1',)
COMPARES = {'C2': 'turns', 'C3': 'outcomes', 'C4': 'interrupts', 'W1': 'the workflow supplied, in a root with one run'}
WORKFLOW_SCOPE = ('W1 is compared only in an examination root whose records store holds records of exactly one run: one run '
                  'start, of this thread and of a bundled workflow, and otherwise only end notices and supply checks naming that same run; '
                  'where Codex holds exactly one line in this thread mentioning the workflow markers, a message; and where '
                  "record/selected-workflow/ holds the candidate's own bytes of that workflow, tied to its identification; anything else, "
                  'or anything unreadable or untied, is blocked. Several runs in a root, and children, are not compared')
# What every workflow marker begins with, and the word in it that a line is
# searched for, case-folded: in the line's bytes and in every string and key
# once the line is read as JSON. Nothing else is decoded.
MARKER = '<<<chirality-workflow'
TOKEN = 'chirality-workflow'
CONTENT_METHOD = 'chirality.app.exact-bytes.sha256/v1'
WORKFLOW_ORIGINS = ('project', 'user', 'bundled', 'host')
RECORD_ID = re.compile(r'^wr-record:v1:([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$')
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


def row(comparison, subject, codex, app, outcome, reason, selected=None):
    """One row. `subject`, `codex`, `app` and W1's `selected` (the candidate's
    own bytes of the selected workflow) hold only allowlisted values; a row
    naming anything unrecognised can never pass."""
    assert outcome in OUTCOMES and comparison in NAMED
    if outcome == 'passed' and any(has_unrecognised(v) for v in (subject, codex, app, selected or {})):
        outcome, reason = 'inconclusive', 'a value on one side is not one this comparison recognises'
    out = {'comparison': comparison, 'subject': subject, 'codex': codex, 'app': app, 'outcome': outcome, 'reason': reason}
    if comparison == 'W1':
        out['selected'] = selected or {}
    return out


def blocked_all(thread, reason):
    """Every planned comparison blocked; and, since whether the session has a
    workflow run is then not known, the workflow comparison's row as well."""
    return [row(c, {'thread': ident(thread)}, {'says': 'not read'}, {'says': 'not compared'}, 'blocked', reason) for c in NAMED]


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


# --- Strict JSON, and the workflow markers ---------------------------------

def _unique_keys(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError('a JSON object names a key twice')
        value[key] = item
    return value


def _no_constant(name):
    raise ValueError('a JSON value is not a number JSON allows')


def strict_json(data):
    """JSON in which no object names a key twice and no NaN or Infinity
    appears: a value hidden by a later key of the same name is never read past."""
    return json.loads(data, object_pairs_hook=_unique_keys, parse_constant=_no_constant)


def strings(value, path=()):
    """Every string of a JSON value, keys included, with its path."""
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield path + ('key',), k
            yield from strings(v, path + (k,))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from strings(v, path + (i,))


def mentions(text):
    """The representation rule: a string mentions the workflow markers when it
    holds the word `chirality-workflow`, case-folded, in whatever surrounds it."""
    return TOKEN in text.casefold()


def marked_values(line):
    """(path, string) of every string or key of a decoded line that mentions
    the workflow markers."""
    return [(path, s) for path, s in strings(line) if mentions(s)]


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
    events, order, marked = {}, [], []
    for number_, raw in enumerate(lines, 1):
        try:
            line = strict_json(raw)
        except Exception:
            raise Refused('a line of the session file is not JSON, or names a key twice')
        # The markers, in the line's bytes or in any string or key of it.
        found = marked_values(line)
        if found or mentions(raw.decode('utf-8', 'replace')):
            marked.append({'line': number_, 'value': line, 'marked': found})
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
    return {'thread': thread, 'order': order, 'turns': turns, 'workflow_marked_lines': len(marked), 'workflow_lines': marked}


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


# --- The workflow comparison (W1) --------------------------------------------

class Unreadable(Exception):
    """A W1 input that cannot be read as one thing: W1 is blocked, with this
    reason (always one of the tool's own sentences)."""


class Differs(Exception):
    """With one of each side read and tied, they differ: W1 fails, with this
    reason."""


RUN_START_KEYS = {'record_kind', 'purpose', 'framing', 'run', 'conversation', 'workflow', 'holding_library', 'workflow_file',
                  'chain', 'origin_of_start', 'selection', 'lines', 'text_identity', 'text_bytes'}
RUN_START_OPTIONAL = {'other_files', 'assurance'}
ENVELOPE_KEYS = {'version', 'record_id', 'writer', 'observed_at', 'body', 'basis_records', 'source_references'}
IDENTITY_KEYS = {'kind', 'origin', 'source_root', 'name', 'revision', 'revision_method'}
LINE_KEYS = {'start_line', 'proposal_line', 'files_line', 'begin_marker', 'end_marker', 'chain_line'}
ORIGINS_OF_START = ('selected by the person', 'agent proposal confirmed by the person')
WORKFLOW_NAME = re.compile(r'^(?=[a-z0-9-]{1,64}$)[a-z0-9]+(?:-[a-z0-9]+)*$')
FILES_LINE = re.compile(r'^\[Chirality\] Other files of this revision, in the folder "([^"\n]+)": (.+)$')
STAGING = '.pending-'
# The record kinds that are records of a run: a run text (run start or end
# notice) and a supply check, each naming its run in `run`. W1 needs exactly
# one run start in the root; every other run record must be an end notice or a
# supply check of that same run. A selection record names no run and is not
# counted; it must still read.
RUN_KINDS = ('run_text', 'supply_check')
SELECTION_KEYS = {'record_kind', 'selection_id', 'identity', 'holding_library', 'standing', 'selected_by', 'how', 'conversation', 'selected_at'}
IDENTIFIER = re.compile(r'^[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$')
# The App's snapshot method for a workflow package (DEL-02-02), restated here.
PACKAGE_METHOD = 'chirality.app.workflow-package.sha256/v1'
SELECTED = 'selected-workflow'  # in record/: the examiner's copy of the candidate's selected workflow
BUNDLE_WORKFLOWS = 'Contents/Resources/workflows'
CANDIDATE_BUNDLE_FOLDER = ('target', 'debug', 'bundle', 'macos')


def text(value):
    return isinstance(value, str) and value != '' and '\n' not in value and '\r' not in value


def count(value, low=0):
    return isinstance(value, int) and not isinstance(value, bool) and value >= low


def exact_identity(value):
    return isinstance(value, dict) and set(value) == {'method', 'value'} and value['method'] == CONTENT_METHOD \
        and isinstance(value['value'], str) and bool(HEX64.match(value['value']))


def read_plain(dir_fd, name, what):
    """The bytes of one regular file named in an open directory: refused before
    it is opened if it is a link, not a regular file, or has another name (a
    second hard link); opened without following a link and checked to be the
    file examined."""
    try:
        info = os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
    except OSError:
        raise Unreadable(f'{what} could not be read')
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise Unreadable(f'{what} is a link, an alias or not a plain file')
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=dir_fd)
    except OSError:
        raise Unreadable(f'{what} could not be read')
    try:
        opened = os.fstat(fd)
        if (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino) or not stat.S_ISREG(opened.st_mode):
            raise Unreadable(f'{what} changed while it was read')
        chunks = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        return b''.join(chunks)
    finally:
        os.close(fd)


def open_dir(path, what, dir_fd=None):
    try:
        return os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=dir_fd)
    except OSError:
        raise Unreadable(f'{what} could not be opened as a folder')


def open_child(fd, name, what):
    """A folder named in an open folder, opened without following a link.
    None where it does not exist; Unreadable where it is a link, not a folder,
    or cannot be opened."""
    try:
        info = os.stat(name, dir_fd=fd, follow_symlinks=False)
    except FileNotFoundError:
        return None
    except OSError:
        raise Unreadable(f'{what} could not be examined')
    if not stat.S_ISDIR(info.st_mode):
        raise Unreadable(f'{what} is a link or not a folder')
    try:
        child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=fd)
    except OSError:
        raise Unreadable(f'{what} could not be opened as a folder')
    opened = os.fstat(child)
    if (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino):
        os.close(child)
        raise Unreadable(f'{what} changed while it was opened')
    return child


def exists_unfollowed(fd, name, what):
    try:
        os.stat(name, dir_fd=fd, follow_symlinks=False)
        return True
    except FileNotFoundError:
        return False
    except OSError:
        raise Unreadable(f'{what} could not be examined')


def launch_identifier(root):
    """The candidate's bundle identifier, as every launch record of the root
    (and kept.json) names it: the launcher's fact from which the App's data
    folder in the root follows. Unreadable unless they all name one."""
    record = root / 'record'
    names = sorted(p.name for p in record.glob('launch-record*.json')) + (['kept.json'] if (record / 'kept.json').exists() else [])
    fd = open_dir(str(record), 'record/')
    try:
        found = set()
        for name in names:
            try:
                value = strict_json(read_plain(fd, name, 'a launch record'))
            except Unreadable:
                raise
            except Exception:
                raise Unreadable('a launch record is not JSON, or names a key twice')
            found.add(value.get('identifier') if isinstance(value, dict) else None)
    finally:
        os.close(fd)
    if len(found) != 1 or not isinstance(next(iter(found)), str) or not IDENTIFIER.match(next(iter(found))):
        raise Unreadable('the launch records of the root do not name one bundle identifier')
    return next(iter(found))


def store_records(root, identifier):
    """Every WR record file of the candidate's records store in the root, and
    nothing else. The store is where the App places it for this route: the
    launcher gives the App the root's home/ as its home and no store override,
    and a build with the custom protocol is not a development build, so the
    store is <home>/Library/Application Support/<identifier>/records unless the
    person chose another (records-store.json in the App's data), which blocks.
    Records kept in place in the launcher's project (.chirality/records) are
    outside this case and block. Each folder on the way is opened without
    following a link; a link, a non-folder or a folder that cannot be opened
    blocks before any record is opened. A folder that does not exist means no
    record there. Returns [(project key, name, bytes or None)]."""
    found, opened = [], []

    def child(fd, name, what):
        c = open_child(fd, name, what)
        if c is not None:
            opened.append(c)
        return c

    try:
        top = open_dir(str(root), 'the examination root')
        opened.append(top)
        project = child(top, 'project', "the launcher's project folder")
        chirality = child(project, '.chirality', "the project's .chirality folder") if project is not None else None
        if chirality is not None and exists_unfollowed(chirality, 'records', "the project's .chirality/records"):
            raise Unreadable('records kept in place in the project are outside this comparison')
        at = top
        for name in ('home', 'Library', 'Application Support', identifier):
            at = child(at, name, "a folder on the way to the App's data")
            if at is None:
                return found
        if exists_unfollowed(at, 'records-store.json', "the App's records store choice"):
            raise Unreadable("the App's records store is not in its data folder, so where it is is not established here")
        store = child(at, 'records', "the App's records store")
        projects = child(store, 'projects', "the store's projects folder") if store is not None else None
        if projects is None:
            return found
        for key in sorted(os.listdir(projects)):
            folder = child(projects, key, 'a project folder of the store')
            if folder is None:
                continue
            workflow = child(folder, 'workflow', "a project's workflow record folder")
            if workflow is None:
                continue
            for name in sorted(os.listdir(workflow)):
                info = os.stat(name, dir_fd=workflow, follow_symlinks=False)
                if not (stat.S_ISREG(info.st_mode) and name.endswith('.json') and not name.startswith(STAGING)):
                    raise Unreadable('a workflow record folder holds something other than published records')
                try:
                    found.append((key, name, read_plain(workflow, name, 'a workflow record')))
                except Unreadable:
                    found.append((key, name, None))
        return found
    except OSError:
        raise Unreadable("a folder of the App's records store could not be listed")
    finally:
        for fd in reversed(opened):
            os.close(fd)


def envelope_body(data, stem):
    """The body of one published WR envelope, read strictly; Unreadable otherwise."""
    try:
        value = strict_json(data)
    except Exception:
        raise Unreadable('a workflow record is not JSON, or names a key twice')
    match = RECORD_ID.match(value.get('record_id', '')) if isinstance(value, dict) and isinstance(value.get('record_id'), str) else None
    if not (isinstance(value, dict) and set(value) == ENVELOPE_KEYS and count(value['version'], 1) and value['version'] == 1
            and match and match.group(1) == stem and text(value['writer']) and text(value['observed_at'])
            and isinstance(value['basis_records'], list) and all(isinstance(r, str) and RECORD_ID.match(r) for r in value['basis_records'])
            and len(set(value['basis_records'])) == len(value['basis_records'])
            and isinstance(value['source_references'], list) and all(isinstance(r, str) and r for r in value['source_references'])
            and len(set(value['source_references'])) == len(value['source_references'])
            and isinstance(value['body'], dict)):
        raise Unreadable('a workflow record is not an envelope the App publishes')
    body = value['body']
    if body.get('record_kind') not in ('selection_record', 'run_text', 'supply_check') or not text(body.get('conversation')):
        raise Unreadable('a workflow record names no kind or conversation this comparison reads')
    if body['record_kind'] == 'selection_record' and not SELECTION_KEYS <= set(body):
        raise Unreadable('a selection record lacks a field the App writes')
    return match.group(1), body


def run_start_ok(body):
    """The sole run start has every field the App's composer writes, of its
    type (see README: the fields validated)."""
    workflow, wf, lines = body.get('workflow'), body.get('workflow_file'), body.get('lines')
    keys = set(body)
    return (RUN_START_KEYS <= keys <= RUN_START_KEYS | RUN_START_OPTIONAL and body['framing'] == 'WR-FRAME-1'
            and body['purpose'] == 'run start' and text(body['conversation'])
            and text(body['run']) and text(body['holding_library']) and text(body['selection'])
            and body['origin_of_start'] in ORIGINS_OF_START and (body['chain'] is None or isinstance(body['chain'], dict))
            and isinstance(workflow, dict) and set(workflow) == IDENTITY_KEYS and workflow['kind'] == 'workflow'
            and workflow['origin'] in WORKFLOW_ORIGINS and text(workflow['source_root'])
            and isinstance(workflow['name'], str) and bool(WORKFLOW_NAME.match(workflow['name']))
            and isinstance(workflow['revision'], str) and bool(HEX64.match(workflow['revision'])) and text(workflow['revision_method'])
            and isinstance(wf, dict) and set(wf) == {'path', 'content', 'bytes'} and wf['path'] == 'WORKFLOW.md'
            and exact_identity(wf['content']) and count(wf['bytes'], 1)
            and exact_identity(body['text_identity']) and count(body['text_bytes'], 1)
            and isinstance(lines, dict) and {'start_line', 'proposal_line', 'begin_marker', 'end_marker'} <= set(lines) <= LINE_KEYS
            and all(text(v) for v in lines.values())
            and ('other_files' not in body or (isinstance(body['other_files'], list) and body['other_files'] and all(
                isinstance(f, dict) and set(f) == {'path', 'sha256'} and text(f['path']) and isinstance(f['sha256'], str)
                and HEX64.match(f['sha256']) for f in body['other_files'])))
            and ('assurance' not in body or isinstance(body['assurance'], dict)))


def run_records(root, identifier):
    """The run records of the candidate's records store, all of them, whatever
    conversation they name: every run text (run start or end notice) and every
    supply check. Returns (run records, unreadable). A record that cannot be
    read as an envelope with a known kind may be a run record and counts as
    unreadable; a selection record is not a run record."""
    runs, unreadable = [], 0
    for key, name, data in store_records(root, identifier):
        try:
            if data is None:
                raise Unreadable('a workflow record could not be read')
            record, body = envelope_body(data, name[:-len('.json')])
        except Unreadable:
            unreadable += 1
            continue
        if body['record_kind'] in RUN_KINDS:
            runs.append((record, body))
    return runs, unreadable


def marker_line(name, revision, which):
    return f'<<<chirality-workflow {name}@{revision[:12]} {which}>>>'


def valid_folder_label(label):
    """The App's rule for the folder a files line names (WR TX-7): relative to
    the project or to the home folder (`~/`), one line, with no `"`, backslash
    or control character, and no empty, `.` or `..` component."""
    rest = label[2:] if label.startswith('~/') else label
    return (rest != '' and not rest.startswith('~') and not rest.startswith('/')
            and not any(ord(c) < 32 or ord(c) == 127 or c in '"\\' for c in label)
            and all(part not in ('', '.', '..') for part in rest.split('/')))


def own_frame(body):
    """The record's own start, proposal and marker lines must be the ones the
    composer makes from its own workflow identity and run; Unreadable
    otherwise. Returns its frame: (lines before the begin marker, begin, end)."""
    workflow, lines, run = body['workflow'], body['lines'], body['run']
    name, origin, revision = workflow['name'], workflow['origin'], workflow['revision']
    if body['chain'] is not None or 'chain_line' in lines:
        raise Unreadable("the App's run text follows an earlier run, which this comparison does not compare")
    start = (f'[Chirality] Workflow run start: {name} from the {origin} library "{workflow["source_root"].replace(chr(34), chr(39))}", '
             f'revision {revision[:12]}, run {run}. Follow the workflow between the two markers below for this run, until the person ends the run.')
    proposal = (f'[Chirality] When you judge this workflow finished, end the message with a line of its own "Workflow finished: {origin}:{name}". '
                'To propose that another registered workflow runs next, end the message with a line of its own "Next workflow: <origin>:<name>", '
                'where <origin> is project, user, bundled or host; when you write both, the finished line comes just before it. '
                'The person decides; nothing ends or starts until they confirm.')
    begin, end = marker_line(name, revision, 'begin'), marker_line(name, revision, 'end')
    if (lines['start_line'], lines['proposal_line'], lines['begin_marker'], lines['end_marker']) != (start, proposal, begin, end):
        raise Unreadable("the App's run text record's lines are not the ones its workflow and run make")
    if 'files_line' in lines:
        m = FILES_LINE.match(lines['files_line'])
        if not m or not valid_folder_label(m.group(1)):
            raise Unreadable("the App's run text record's files line is not one the composer writes")
    return [start, proposal] + ([lines['files_line']] if 'files_line' in lines else []), begin, end


def files_agree(body, files):
    """The record's other files and files line are the ones the candidate's
    package makes: every file but WORKFLOW.md, in path byte order, by path and
    digest, and none where there is none."""
    others = [{'path': p, 'sha256': sha256(files[p])} for p in sorted(files, key=lambda p: p.encode('utf-8')) if p != 'WORKFLOW.md']
    if body.get('other_files', []) != others:
        return False
    if not others:
        return 'files_line' not in body['lines']
    m = FILES_LINE.match(body['lines'].get('files_line', ''))
    return bool(m) and m.group(2) == '; '.join(f"{f['path']} (sha256 {f['sha256'][:12]})" for f in others)


def codex_candidate(model):
    """The one text element of the one message mentioning the workflow markers:
    (side, element, None), or (side, None, reason) where there is not exactly
    one, or where any other line mentions them."""
    lines = model.get('workflow_lines', [])
    messages = [l for l in lines if l['value'].get('type') == 'response_item' and isinstance(l['value'].get('payload'), dict)
                and l['value']['payload'].get('type') == 'message']
    side = {'linesWithWorkflowMarkers': number(len(lines)), 'messagesWithWorkflowMarkers': number(len(messages))}
    if len(messages) != 1:
        return side, None, 'Codex does not hold exactly one message carrying the workflow markers in this thread'
    if len(lines) != 1:
        return side, None, 'a line other than the one message carries the workflow markers'
    (message,) = messages
    payload = message['value']['payload']
    side['line'] = message['line']
    meta = payload.get('internal_chat_message_metadata_passthrough')
    turn = meta.get('turn_id') if isinstance(meta, dict) else None
    if not isinstance(turn, str) or ident(turn) == UNRECOGNISED or turn not in model['turns']:
        return side, None, 'the message carrying the workflow markers names no turn of this session'
    side['turn'] = turn
    if payload.get('role') != 'user':
        return side, None, "the message carrying the workflow markers is not the person's input"
    content = payload.get('content')
    if not isinstance(content, list) or not content or not all(
            isinstance(item, dict) and set(item) == {'type', 'text'} and item['type'] == 'input_text' and isinstance(item['text'], str)
            for item in content):
        return side, None, 'an element of the message is not a text element this comparison reads'
    side['elements'] = number(len(content))
    places = {path for path, _ in message['marked']}
    if not places or not all(len(path) == 4 and path[:2] == ('payload', 'content') and path[3] == 'text' for path in places):
        return side, None, 'the workflow markers are carried elsewhere in the message than in its text elements'
    if len({path[2] for path in places}) != 1:
        return side, None, 'more than one text element of the message carries the workflow markers'
    index = next(iter(places))[2]
    element = content[index]['text']
    side['element'] = index
    if element.casefold().count(TOKEN) != 2 or element.casefold().count(MARKER) != 2:
        return side, None, 'the text Codex holds does not carry exactly one begin and one end marker and no other mention of them'
    try:
        element.encode('utf-8')
    except UnicodeEncodeError:
        return side, None, 'the text element carrying the workflow markers is not UTF-8 text'
    return side, element, None


def package_revision(files):
    """The App's package revision of a workflow package's files (path to bytes):
    the method, a NUL byte, the file count, then each file's path length, path,
    byte length and bytes, in path byte order, each length as 8 big-endian bytes."""
    preimage = PACKAGE_METHOD.encode() + b'\0' + len(files).to_bytes(8, 'big')
    for path in sorted(files, key=lambda p: p.encode('utf-8')):
        data = files[path]
        preimage += len(path.encode()).to_bytes(8, 'big') + path.encode() + len(data).to_bytes(8, 'big') + data
    return sha256(preimage)


def identification_tools():
    """identify.py, the candidate identification's own record and inventory
    validation (the route launch.py uses). Unreadable if it cannot run here."""
    folder = str(Path(__file__).resolve().parents[1] / 'candidate_identity')
    sys.path.insert(0, folder)
    try:
        import identify
        return identify
    except Exception:
        raise Unreadable("the candidate identification's validation could not be run here")
    finally:
        sys.path.remove(folder)


def launch_bindings(root, identification):
    """Every launch record of the root names the identified candidate: its key,
    its bundle identifier, and the bundle the launcher opened as the one its
    candidate folder holds under that name; and none was made before the
    candidate was identified."""
    record = root / 'record'
    launches = sorted(record.glob('launch-record*.json'))
    kept = [record / 'kept.json'] if (record / 'kept.json').exists() else []
    if not launches:
        raise Unreadable('the examination root has no launch record to tie the selected workflow to')
    fd = open_dir(str(record), 'record/')
    try:
        identified = datetime.fromisoformat(identification['identified_at'].upper().replace('Z', '+00:00'))
        for path in launches + kept:
            try:
                value = strict_json(read_plain(fd, path.name, 'a launch record'))
                assert isinstance(value, dict)
                assert value.get('candidate_key') == identification['candidate_key']
                assert value.get('identifier') == identification['bundle']['identifier']
                if path in launches:
                    assert isinstance(value.get('candidate_folder'), str) and isinstance(value.get('bundle'), str)
                    assert Path(value['bundle']) == Path(value['candidate_folder']).joinpath(*CANDIDATE_BUNDLE_FOLDER, identification['bundle']['name'])
                    made = datetime.fromisoformat(str(value.get('made_at')).replace('Z', '+00:00'))
                    assert made.tzinfo is not None and made >= identified
            except Unreadable:
                raise
            except Exception:
                raise Unreadable("a launch record does not name the candidate the selected workflow's identification names")
    finally:
        os.close(fd)


def selected_workflow(root):
    """The examiner's copy of the candidate's selected bundled workflow, from
    record/selected-workflow/, tied to the candidate's identification and to
    every launch record of the root. Returns (identity, files, manifest digest,
    candidate key); Unreadable where any part is missing or does not tie."""
    folder = root / 'record' / SELECTED
    identify = identification_tools()
    top = open_dir(str(folder), 'the selected workflow reference (record/selected-workflow/)')
    opened = [top]
    try:
        try:
            reference = strict_json(read_plain(top, 'reference.json', 'the selected workflow reference'))
        except Unreadable:
            raise
        except Exception:
            raise Unreadable('the selected workflow reference is not JSON, or names a key twice')
        if not (isinstance(reference, dict) and set(reference) == {'name', 'bundle_path'} and isinstance(reference['name'], str)
                and WORKFLOW_NAME.match(reference['name']) and reference['bundle_path'] == f"{BUNDLE_WORKFLOWS}/{reference['name']}"):
            raise Unreadable('the selected workflow reference does not name one bundled workflow')
        name = reference['name']
        ids = open_dir('identification', "the reference's identification folder", dir_fd=top)
        opened.append(ids)
        try:
            identification = strict_json(read_plain(ids, 'candidate-identification.json', "the candidate's identification record"))
            identify.validate_record(identification)
            stored = read_plain(ids, identification['bundle']['inventory']['path'], "the candidate's stored inventory")
            if sha256(stored) != identification['bundle']['inventory']['sha256']:
                raise ValueError
            inventory = identify.validate_inventory(strict_json(stored))
            if identify.identity(inventory) != identification['app_candidate']['build_identity']:
                raise ValueError
        except Unreadable:
            raise
        except Exception:
            raise Unreadable("the reference's copy of the candidate's identification and inventory does not validate")
        if 'custom-protocol' not in identification['build']['features']:
            raise Unreadable('the identified candidate is a development build, whose records are not kept in its App data')
        launch_bindings(root, identification)
        entries = {e['path']: e for e in inventory['entries']}
        prefix = reference['bundle_path'] + '/'
        expected = {p[len(prefix):]: e for p, e in entries.items() if p.startswith(prefix)}
        if any(e['kind'] == 'symlink' for e in expected.values()) or 'WORKFLOW.md' not in expected:
            raise Unreadable("the candidate's inventory does not hold the selected workflow as plain files")
        expected = {p: e for p, e in expected.items() if e['kind'] == 'file'}
        files = {}

        def copy(fd, parts):
            for entry in sorted(os.listdir(fd)):
                info = os.stat(entry, dir_fd=fd, follow_symlinks=False)
                if stat.S_ISDIR(info.st_mode):
                    child = open_dir(entry, "the reference's package copy", dir_fd=fd)
                    opened.append(child)
                    copy(child, parts + (entry,))
                else:
                    files['/'.join(parts + (entry,))] = read_plain(fd, entry, "a file of the reference's package copy")
        try:
            package = open_dir('package', "the reference's package copy", dir_fd=top)
            opened.append(package)
            copy(package, ())
        except Unreadable:
            raise
        except OSError:
            raise Unreadable("the reference's package copy could not be read")
        if set(files) != set(expected) or any(len(files[p]) != expected[p]['size'] or sha256(files[p]) != expected[p]['sha256'] for p in files):
            raise Unreadable("the reference's package copy is not the candidate's package, file for file")
        manifest_entry = entries.get(f'{BUNDLE_WORKFLOWS}/MANIFEST.json')
        manifest_bytes = read_plain(top, 'MANIFEST.json', "the reference's copy of the bundled manifest")
        if not manifest_entry or manifest_entry['kind'] != 'file' or manifest_entry['size'] != len(manifest_bytes) \
                or manifest_entry['sha256'] != sha256(manifest_bytes):
            raise Unreadable("the reference's copy of the bundled manifest is not the candidate's")
        try:
            manifest = strict_json(manifest_bytes)
            assert manifest['schema_version'] == 2 and text(manifest['release_subject'])
            (entry,) = [m for m in manifest['packages'] if isinstance(m, dict) and m.get('name') == name]
            assert entry['revision_method'] == PACKAGE_METHOD and HEX64.match(entry['revision']) and entry['source_path'] == f'workflows/{name}'
            listed = sorted(((f['path'], f['bytes'], f['sha256']) for f in entry['files']), key=lambda f: f[0].encode())
        except Exception:
            raise Unreadable("the candidate's bundled manifest does not name the selected workflow once, as the App reads it")
        if listed != sorted(((p, len(b), sha256(b)) for p, b in files.items()), key=lambda f: f[0].encode()) \
                or package_revision(files) != entry['revision']:
            raise Unreadable("the candidate's bundled manifest does not give the package's own revision and files")
        identity = {'kind': 'workflow', 'origin': 'bundled', 'source_root': manifest['release_subject'], 'name': name,
                    'revision': entry['revision'], 'revision_method': PACKAGE_METHOD}
        return identity, files, sha256(manifest_bytes), identification['candidate_key'], identification['bundle']['identifier']
    finally:
        for fd in reversed(opened):
            os.close(fd)


def workflow_rows(root, model, requested=False):
    """W1 for a single-run root. Made where the session has a workflow run to
    compare (a line of Codex's record mentions the workflow markers, a run
    record of the store names this thread, or the store cannot be read whole),
    or where W1 was asked for by name; no row otherwise.
      Blocked unless: the candidate's records store in the root holds exactly
      one run start, whatever conversation any names, and it is a readable run
      start of this thread, and every other run record is an end notice or a
      supply check naming that same run; Codex holds exactly one line in this
      thread mentioning the markers, a message; the run is of a bundled
      workflow; and the examiner's copy of that workflow ties to the candidate.
      Then failed where the markers, the text, the workflow's identity, the
      files line or the bytes between the markers differ from the candidate's
      own; passed only where none does."""
    thread = model['thread']
    lines = model.get('workflow_lines', [])
    subject = {'thread': thread}
    codex, element, refusal = codex_candidate(model)
    app, selected = {}, {}
    result = lambda outcome, reason: [row('W1', subject, codex, app, outcome, reason, selected=selected)]
    try:
        identifier = launch_identifier(root)
        runs, unreadable = run_records(root, identifier)
    except Unreadable as e:
        return result('blocked', str(e))
    is_start = lambda b: b['record_kind'] == 'run_text' and b.get('purpose') == 'run start'
    starts = [(r, b) for r, b in runs if is_start(b)]
    app.update({'runRecords': number(len(runs)), 'runStarts': number(len(starts)),
                'endNotices': number(sum(1 for _, b in runs if b['record_kind'] == 'run_text' and b.get('purpose') == 'run end notice')),
                'supplyChecks': number(sum(1 for _, b in runs if b['record_kind'] == 'supply_check')),
                'unreadableWorkflowRecords': number(unreadable)})
    if not (lines or unreadable or requested or any(b.get('conversation') == thread for _, b in runs)):
        return []
    try:
        if unreadable:
            raise Unreadable("a record of the App's records store could not be read, and it may be a record of a run")
        if len(starts) != 1:
            raise Unreadable('the examination root does not hold exactly one run start')
        record, body = starts[0]
        app['record'] = ident(record)
        try:
            readable = run_start_ok(body)
        except Exception:
            readable = False
        if not readable:
            raise Unreadable("the root's one run start is not one this comparison reads")
        # Every other run record must be of the same run: counted by kind and
        # run identity only; nothing else in it is read.
        for _, other in runs:
            if is_start(other):
                continue
            if not ((other['record_kind'] == 'run_text' and other.get('purpose') == 'run end notice') or other['record_kind'] == 'supply_check'):
                raise Unreadable('a run record of the root is not a kind the App writes for a run')
            if not text(other.get('run')):
                raise Unreadable('a run record of the root names no run identity this comparison reads')
            if other['run'] != body['run']:
                raise Unreadable('the examination root holds records of more than the one run this comparison covers')
        if body['conversation'] != thread:
            raise Unreadable("the root's one run is of another conversation")
        subject['run'] = ident(body['run'])
        app.update({'origin': one_of(body['workflow']['origin'], WORKFLOW_ORIGINS),
                    'workflow': ident(body['workflow']['name']), 'revision': digest(body['workflow']['revision']),
                    'text_sha256': body['text_identity']['value'], 'text_bytes': body['text_bytes'],
                    'workflow_sha256': body['workflow_file']['content']['value'], 'workflow_bytes': body['workflow_file']['bytes']})
        frame, begin, end = own_frame(body)
        if refusal:
            raise Unreadable(refusal)
        if body['workflow']['origin'] != 'bundled':
            raise Unreadable('only a bundled workflow is compared: its own bytes are tied to the candidate')
        identity, files, manifest_sha, key, bundle_identifier = selected_workflow(root)
        selected.update({'candidate': ident(key), 'workflow': ident(identity['name']), 'revision': digest(identity['revision']),
                         'manifest_sha256': manifest_sha, 'workflow_sha256': sha256(files['WORKFLOW.md']),
                         'workflow_bytes': len(files['WORKFLOW.md'])})
        if bundle_identifier != identifier:
            raise Unreadable("the selected workflow's identification names another candidate than the launch records")
        if body['workflow']['name'] != identity['name']:
            raise Unreadable("the App's run is of another workflow than the reference names")
        data = element.encode('utf-8')
        codex.update({'text_sha256': sha256(data), 'text_bytes': len(data)})
        split = element.split('\n')
        if split.count(begin) != 1 or split.count(end) != 1:
            raise Differs("the markers Codex holds name another workflow or revision than the App's run text")
        prefix, suffix = '\n'.join(frame + [begin]) + '\n', '\n' + end
        if element.startswith(prefix) and element.endswith(suffix) and len(element) >= len(prefix) + len(suffix):
            inner = element[len(prefix):len(element) - len(suffix)].encode('utf-8')
            codex.update({'workflow_sha256': sha256(inner), 'workflow_bytes': len(inner)})
        else:
            inner = None
            codex['workflow_sha256'] = None
        if (codex['text_sha256'], codex['text_bytes']) != (app['text_sha256'], app['text_bytes']):
            raise Differs('the text Codex holds is not the run text the App composed, byte for byte')
        if body['workflow'] != identity:
            raise Differs("the App's run names another source or revision of this workflow than the candidate's bundled manifest")
        if not files_agree(body, files):
            raise Differs("the run's other files and files line are not the ones the candidate's package makes")
        if inner != files['WORKFLOW.md']:
            raise Differs("the bytes between the markers are not the candidate's own WORKFLOW.md bytes")
        if (app['workflow_sha256'], app['workflow_bytes']) != (sha256(inner), len(inner)):
            raise Differs("the App recorded other WORKFLOW.md bytes than the ones it sent")
    except Unreadable as e:
        return result('blocked', str(e))
    except Differs as e:
        return result('failed', str(e))
    return result('passed', "the root's one run text reached Codex byte for byte as the one message carrying the markers, "
                            "with the candidate's own WORKFLOW.md bytes of the selected revision between them")


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

def fallback_header(root, **extra):
    """The header of a file of blocked rows: every field that is read from a
    file is taken only if reading it succeeds, so the header cannot fail. It
    says it is a fallback, and keeps `extra` (an answers run's `answers_of`),
    so a refused answers run still supersedes that list's earlier answers."""
    def tried(read):
        try:
            return read()
        except Exception:
            return None
    return {'header': True, 'candidate_key': tried(lambda: candidate_key(root)),
            'examination_root': str(root), 'tool': TOOL, 'tool_sha256': tried(tool_digest), 'model_version': MODEL_VERSION,
            'pinned_codex': PINNED_CODEX, 'compares': COMPARES, 'workflow_scope': WORKFLOW_SCOPE, 'fallback': True, **extra}


def header(root, **extra):
    return {'header': True, 'candidate_key': candidate_key(root), 'examination_root': str(root), 'tool': TOOL,
            'tool_sha256': tool_digest(), 'model_version': MODEL_VERSION, 'pinned_codex': PINNED_CODEX,
            'compares': COMPARES, 'workflow_scope': WORKFLOW_SCOPE, **extra}


def summary(rows):
    counts = {}
    for r in rows:
        counts.setdefault(r['comparison'], {}).setdefault(r['outcome'], 0)
        counts[r['comparison']][r['outcome']] += 1
    return {'summary': counts, 'unrecognised': sum(1 for r in rows if has_unrecognised(r)),
            'compares': COMPARES, 'workflow_scope': WORKFLOW_SCOPE}


def write(root, stem, head, body, with_summary=True, fallback=False, planned=PLANNED):
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
        lines.append({'summary': counts, 'unrecognised': 0, 'compares': COMPARES, 'workflow_scope': WORKFLOW_SCOPE})
    elif with_summary:
        total = summary(body)
        if sum(sum(v.values()) for v in total['summary'].values()) != len(body) or not {r['comparison'] for r in body} >= set(planned):
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


def run_compare(root, thread, views, requested=False):
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
    return rows + records_rows(root, model) + workflow_rows(root, model, requested), None


def screen_plan(root, screen):
    """Whether the screen list was made with W1 asked for by name. The list's
    plan can only add W1's row: W1 is always derived from the records, never
    from the list or the answers."""
    try:
        head = json.loads(inside(root, screen).read_text().splitlines()[0])
        return isinstance(head, dict) and isinstance(head.get('planned'), list) and 'W1' in head['planned']
    except Exception:
        return False


def run_answers(root, screen, requested=False):
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
    return answered_rows(model, lines[1:]) + records_rows(root, model) + workflow_rows(root, model, requested)


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
                            help='a comparison asked for by name (C2, C3, C4 or W1). C2, C3 and C4 are always made; '
                                 'W1 is made where the session has a workflow run to compare.')
    args = p.parse_args(argv)
    for name in args.comparison:
        if name not in NAMED:
            print('refused: this tool has no comparison of that name', file=sys.stderr)
            return 2
    try:
        root = examination_root(args.root)
    except Refused as e:
        print(f'refused: {e}', file=sys.stderr)
        return 2
    thread = getattr(args, 'thread', None)
    # W1 asked for by name is planned: its row is written whatever the session holds.
    requested = 'W1' in args.comparison
    planned = PLANNED + (('W1',) if requested else ())
    try:
        unnamed = unnamed_views(root, getattr(args, 'view', []))
        if unnamed:
            print(f'note: saved views in record/ not named in this run: {", ".join(unnamed)}', file=sys.stderr)
        if args.command == 'compare':
            if not args.view and unnamed:
                raise Refused('a saved view exists in record/, so the operator\'s list is not written; name it with --view')
            rows, pending = run_compare(root, args.thread, args.view, requested)
            if pending is not None:
                model, session_sha = pending
                print(write(root, 'screen-list', header(root, thread=args.thread, session_sha256=session_sha, saved_views_not_named=unnamed,
                                                        planned=list(planned)),
                            [{**i, 'answer': None, 'note': None} for i in screen_items(model)], with_summary=False))
                return 0
            print(write(root, 'session-comparison', header(root, saved_views_not_named=unnamed), rows, planned=planned))
            return 0
        if unnamed:
            raise Refused("a saved view exists in record/, so the operator's answers are not taken; compare it with --view")
        # W1 asked for when the list was made stays asked for in its answers.
        if screen_plan(root, args.screen):
            requested, planned = True, PLANNED + ('W1',)
        rows = run_answers(root, args.screen, requested)
        print(write(root, 'session-comparison', header(root, answers_of=ident(Path(args.screen).name), saved_views_not_named=unnamed), rows,
                    planned=planned))
        return 0
    except Exception as e:
        # Nothing ends without rows: the failure's kind, and no more.
        reason = str(e) if isinstance(e, Refused) else f'the comparison failed ({e.__class__.__name__})'
        try:
            extra = {'answers_of': ident(Path(args.screen).name)} if args.command == 'answers' else {}
            print(write(root, 'session-comparison', fallback_header(root, **extra), blocked_all(thread, reason), fallback=True))
            return 1
        except Exception as inner:
            print(f'refused: no result could be written ({inner.__class__.__name__})', file=sys.stderr)
            return 2


if __name__ == '__main__':
    sys.exit(main())
