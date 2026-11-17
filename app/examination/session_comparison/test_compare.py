"""Session comparison, first part, on invented sessions: each case is one
invented session file with the App's account of the same session, agreeing or
disagreeing in one named way. Nothing here is a real session."""
import contextlib
import hashlib
import io
import json
import os
import sqlite3
import sys
import tempfile
import time
import unittest
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compare  # noqa: E402

THREAD = '019a0000-0000-7000-8000-00000000000a'
WORKFLOW = '# Invented workflow\nSay hello.\n'
NAME = 'invented-workflow'
BUNDLE_NAME = 'Invented Dev.app'
RELEASE_SUBJECT = 'invented-library:invented-v1'
PACKAGE_METHOD = 'chirality.app.workflow-package.sha256/v1'
CONTENT_METHOD = 'chirality.app.exact-bytes.sha256/v1'


def package_revision(files):
    """The App's package revision, restated in the test from the App's
    snapshot method independently of the reader's own copy."""
    import struct
    pre = PACKAGE_METHOD.encode() + b'\0' + struct.pack('>Q', len(files))
    for path in sorted(files, key=lambda p: p.encode()):
        pre += struct.pack('>Q', len(path.encode())) + path.encode() + struct.pack('>Q', len(files[path])) + files[path]
    return hashlib.sha256(pre).hexdigest()


PACKAGE = {'WORKFLOW.md': WORKFLOW.encode()}
REVISION = package_revision(PACKAGE)
RUN = 'run-1'
BRIEF = 'INVENTED PERSON BRIEF'


def frame_lines(run=RUN, revision=REVISION, name=NAME, origin='bundled', source_root=RELEASE_SUBJECT):
    """The lines the App's composer writes for a run start (WR-FRAME-1)."""
    return {'start_line': f'[Chirality] Workflow run start: {name} from the {origin} library "{source_root}", revision {revision[:12]}, '
                          f'run {run}. Follow the workflow between the two markers below for this run, until the person ends the run.',
            'proposal_line': f'[Chirality] When you judge this workflow finished, end the message with a line of its own "Workflow finished: '
                             f'{origin}:{name}". To propose that another registered workflow runs next, end the message with a line of its own '
                             '"Next workflow: <origin>:<name>", where <origin> is project, user, bundled or host; when you write both, the '
                             'finished line comes just before it. The person decides; nothing ends or starts until they confirm.',
            'begin_marker': f'<<<chirality-workflow {name}@{revision[:12]} begin>>>',
            'end_marker': f'<<<chirality-workflow {name}@{revision[:12]} end>>>'}


FOLDER_LABEL = '.chirality/workflow-supply/invented'


def files_line(package):
    others = [(p, hashlib.sha256(b).hexdigest()) for p, b in sorted(package.items(), key=lambda i: i[0].encode()) if p != 'WORKFLOW.md']
    if not others:
        return None
    return f'[Chirality] Other files of this revision, in the folder "{FOLDER_LABEL}": ' + '; '.join(f'{p} (sha256 {d[:12]})' for p, d in others)


def run_text(body=WORKFLOW, run=RUN, revision=REVISION, name=NAME, files=None):
    """The run text as the App composes it (WR-FRAME-1): the frame lines (with
    the files line where `files` gives one), the WORKFLOW.md bytes exactly, and
    the end marker."""
    lines = frame_lines(run, revision, name)
    frame = [lines['start_line'], lines['proposal_line']] + ([files] if files else []) + [lines['begin_marker']]
    return '\n'.join(frame) + f"\n{body}\n{lines['end_marker']}"


def envelope(i, body):
    key = f'00000000-0000-4000-8000-{i:012d}'
    return key, {'version': 1, 'record_id': f'wr-record:v1:{key}', 'writer': 'invented', 'observed_at': 't', 'body': body,
                 'basis_records': [], 'source_references': []}


def meta(mode):
    return {'mode': mode, 'uid': 501, 'gid': 20, 'xattrs': []}


def identification_tools():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'candidate_identity'))
    try:
        import identify
        return identify
    finally:
        sys.path.pop(0)


def candidate(package=PACKAGE, name=NAME, revision=None):
    """An invented identified candidate: its bundled manifest, its stored
    inventory and its identification record, as identify.py writes them."""
    identify = identification_tools()
    revision = package_revision(package) if revision is None else revision
    manifest = json.dumps({'schema_version': 2, 'release_subject': RELEASE_SUBJECT, 'standing': 'invented', 'packages': [
        {'name': name, 'revision_method': PACKAGE_METHOD, 'revision': revision, 'source_path': f'workflows/{name}',
         'files': [{'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()} for p, b in sorted(package.items())]}]},
        indent=2).encode()
    files = {'Contents/Resources/workflows/MANIFEST.json': manifest,
             **{f'Contents/Resources/workflows/{name}/{p}': b for p, b in package.items()}}
    dirs = set()
    for path in files:
        parts = path.split('/')[:-1]
        dirs.update('/'.join(parts[:i]) for i in range(1, len(parts) + 1))
    entries = [{'path': d, 'kind': 'dir', **meta(0o755)} for d in dirs] + \
        [{'path': f, 'kind': 'file', **meta(0o644), 'size': len(b), 'sha256': hashlib.sha256(b).hexdigest()} for f, b in files.items()]
    entries.sort(key=lambda e: e['path'].encode())
    inventory = {'format': identify.INVENTORY_FORMAT, 'method': identify.METHOD, 'root': meta(0o755), 'entries': entries}
    stored = identify.canonical(inventory) + b'\n'
    build = identify.identity(inventory)
    source = '0123456789abcdef0123456789abcdef01234567'
    key = source[:10] + '-' + build.rsplit(':', 1)[1][:12]
    identifier = 'dev.chirality.app-v4.candidate.' + key  # as the launcher's candidates are named
    record = {
        'format': identify.FORMAT, 'candidate_key': key,
        'app_candidate': {'revision': source, 'build_identity': build, 'packaged': False}, 'route': 'native_development',
        'source': {'repository': 'invented', 'revision': source, 'commit_tree': 'a' * 40, 'exported_prefix': '.', 'tree': 'b' * 40,
                   'tracked_files_verified': 1},
        'build': {'procedure': 'invented', 'profile': 'debug', 'signing': 'none', 'features': ['custom-protocol'], 'command': ['invented'],
                  'config_overlays': [], 'toolchain': {}, 'lockfiles': {}, 'offline': True, 'environment': {},
                  'started_at': '2026-11-13T00:00:00Z', 'finished_at': '2026-11-13T00:10:00Z'},
        'bundle': {'name': BUNDLE_NAME, 'identifier': identifier, 'version': '0.0.0',
                   'executable': {'path': 'Contents/MacOS/invented', 'sha256': 'c' * 64}, 'info_plist_sha256': 'd' * 64,
                   'file_manifest_sha256': identify.file_manifest(inventory), 'counts': {'dir': len(dirs), 'file': len(files), 'symlink': 0},
                   'metadata_state': {'entries_including_root': len(entries) + 1, 'acl_entries': 0, 'nonzero_flags': 0, 'set_id_bits': 0,
                                      'extended_attributes': {}, 'xattr_allowlist': ['com.apple.provenance'], 'owners': [{'uid': 501, 'gid': 20}],
                                      'symlinks': 0},
                   'inventory': {'path': 'bundle-inventory.json', 'sha256': hashlib.sha256(stored).hexdigest()}},
        'app_data': identify.app_data_declaration(identifier),
        'supplier': {'bundled': False, 'binding': 'invented'},
        'identified_by': {'tool': 'invented', 'tool_sha256': 'e' * 64, 'method': identify.METHOD},
        'identified_at': '2026-11-13T00:20:00Z', 'limits': ['invented']}
    identify.validate_record(record)
    return {'record': record, 'inventory': stored, 'manifest': manifest, 'package': dict(package), 'name': name}


class Root:
    """An invented examination root with the App's account, Codex's record, the
    launcher's record and the examiner's copy of the selected workflow."""

    def __init__(self, base, package=PACKAGE):
        self.root = Path(base) / 'launch-20261114T000000Z-0000'
        (self.root / 'record').mkdir(parents=True)
        (self.root / 'project').mkdir()
        self.candidate = candidate(package=package)
        self.identifier = self.candidate['record']['bundle']['identifier']
        self.data = self.root / 'home' / 'Library' / 'Application Support' / self.identifier
        (self.data / 'runtime').mkdir(parents=True)
        self.launch_record()
        self.lines, self.stops, self.records, self.session, self.selected = [], [], [], True, True

    def launch_record(self, name='launch-record.json', **changes):
        folder = str(Path(self.root).parent / 'candidate')
        value = {'candidate_key': self.candidate['record']['candidate_key'], 'identifier': self.identifier, 'candidate_folder': folder,
                 'bundle': str(Path(folder) / 'target' / 'debug' / 'bundle' / 'macos' / BUNDLE_NAME), 'made_at': '2026-11-14T00:00:00Z',
                 **changes}
        (self.root / 'record' / name).write_text(json.dumps(value))

    def write_selected(self):
        """The examiner's preparation: byte copies of the candidate's
        identification, inventory, bundled manifest and selected package."""
        c = self.candidate
        folder = self.root / 'record' / 'selected-workflow'
        (folder / 'identification').mkdir(parents=True)
        (folder / 'identification' / 'candidate-identification.json').write_text(json.dumps(c['record']))
        (folder / 'identification' / 'bundle-inventory.json').write_bytes(c['inventory'])
        (folder / 'MANIFEST.json').write_bytes(c['manifest'])
        (folder / 'reference.json').write_text(json.dumps({'name': c['name'], 'bundle_path': f"Contents/Resources/workflows/{c['name']}"}))
        for path, data in c['package'].items():
            (folder / 'package' / path).parent.mkdir(parents=True, exist_ok=True)
            (folder / 'package' / path).write_bytes(data)
        return folder

    def codex(self, kind, payload):
        self.lines.append({'timestamp': '2026-11-14T00:00:00Z', 'type': kind, 'payload': payload})

    def message(self, turn, text, kind='user.text', brief=None, role='user'):
        content = [{'type': 'input_text', 'text': text}] + ([{'type': 'input_text', 'text': brief}] if brief is not None else [])
        self.codex('response_item', {'type': 'message', 'role': role, 'content': content,
                                     'internal_chat_message_metadata_passthrough': {'turn_id': turn, 'content_item_kinds': [kind],
                                                                                    'provenance': {'type': 'user' if kind == 'user.text' else 'harness'}}})

    def turn(self, turn, end=None, text='hello', brief=None, **fields):
        self.codex('event_msg', {'type': 'task_started', 'turn_id': turn})
        self.message(turn, text, brief=brief)
        if end == 'completed':
            self.codex('event_msg', {'type': 'task_complete', 'turn_id': turn, **fields})
        elif end == 'interrupted':
            self.codex('event_msg', {'type': 'turn_aborted', 'turn_id': turn, 'reason': 'interrupted'})

    def stop(self, turn, outcome):
        self.stops.append({'kind': 'stop_request', 'session': 's', 'at': 't', 'record': {
            'stopRequestId': f'stop:{turn}', 'threadId': THREAD, 'turnId': turn, 'turnOutcome': outcome,
            'outcomeSource': 'observed' if outcome != 'unknown' else 'not-observed', 'state': 'settled'}})

    def view(self, statuses):
        keys = [{'threadId': THREAD, 'turnId': t} for t in statuses]
        values = [{'id': t, 'status': s} for t, s in statuses.items()]
        path = self.root / 'record' / 'host-status-end.json'
        path.write_text(json.dumps({'nativeView': {'turnRecords': keys, 'turns': values}}))
        return str(path)

    def write(self):
        if getattr(self, 'written', False):
            return
        self.written = True
        sessions = self.data / 'account-homes' / 'h' / 'sessions' / '2026' / '11' / '14'
        sessions.mkdir(parents=True)
        target = sessions / f'rollout-2026-11-14T00-00-00-{THREAD}.jsonl' if self.session else os.devnull
        with open(target, 'w') as f:
            for line in [{'timestamp': 't', 'type': 'session_meta', 'payload': {'id': THREAD, 'cli_version': '0.169.0'}}] + self.lines:
                f.write(json.dumps(line) + '\n')
        db = sqlite3.connect(self.data / 'runtime' / 'recovery.ledger.sqlite')
        db.execute('CREATE TABLE ledger_entry (seq INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT NOT NULL, entry TEXT NOT NULL)')
        for entry in self.stops:
            db.execute('INSERT INTO ledger_entry (kind, entry) VALUES (?, ?)', (entry['kind'], json.dumps(entry)))
        db.commit()
        db.close()
        workflow = self.data / 'records' / 'projects' / 'k' / 'workflow'
        workflow.mkdir(parents=True)
        for i, record in enumerate(self.records):
            key, value = envelope(i, record)
            (workflow / f'{key}.json').write_text(json.dumps(value))
        if any(r.get('purpose') == 'run start' for r in self.records):
            # The person's selection, which the App records beside the run; not a record of a run.
            key, value = envelope(99, {'record_kind': 'selection_record', 'selection_id': 'selection:1', 'identity': self.records[0].get('workflow'),
                                       'holding_library': 'invented', 'standing': 'bundled', 'selected_by': 'the person (App interface)',
                                       'how': 'explicit', 'conversation': THREAD, 'selected_at': '2026-11-14T00:00:00Z'})
            (workflow / f'{key}.json').write_text(json.dumps(value))
        if self.selected:
            self.write_selected()

    def run_text_record(self, body=WORKFLOW, text=None, run=RUN, conversation=THREAD, **changes):
        """The run-start record the App publishes, in its WR shape: the record
        holds the lines and the identities of the text and of WORKFLOW.md, never
        the bytes themselves."""
        text = run_text(body, run) if text is None else text
        method = 'chirality.app.exact-bytes.sha256/v1'
        record = {'record_kind': 'run_text', 'purpose': 'run start', 'framing': 'WR-FRAME-1', 'run': run, 'conversation': conversation,
                  'workflow': {'kind': 'workflow', 'origin': 'bundled', 'source_root': RELEASE_SUBJECT, 'name': NAME,
                               'revision': REVISION, 'revision_method': PACKAGE_METHOD},
                  'holding_library': 'invented', 'chain': None, 'origin_of_start': 'selected by the person', 'selection': 'selection:1',
                  'workflow_file': {'path': 'WORKFLOW.md', 'content': {'method': method, 'value': hashlib.sha256(body.encode()).hexdigest()},
                                    'bytes': len(body.encode())},
                  'lines': frame_lines(run), 'text_identity': {'method': method, 'value': hashlib.sha256(text.encode()).hexdigest()},
                  'text_bytes': len(text.encode())}
        record.update(changes)
        self.records.append(record)
        return record

    def end_notice(self, run=RUN):
        text = f'[Chirality] Workflow run ended: {NAME} revision {REVISION[:12]} (run {run}, completed). No workflow is in force.'
        self.records.append({'record_kind': 'run_text', 'purpose': 'run end notice', 'framing': 'WR-FRAME-1', 'run': run, 'conversation': THREAD,
                             'lines': {'end_line': text}, 'text_identity': {'method': 'chirality.app.exact-bytes.sha256/v1',
                                                                            'value': hashlib.sha256(text.encode()).hexdigest()}, 'text_bytes': len(text.encode())})

    def compare(self, *views, candidate=False):
        """Rows from a saved view (an empty one where the test is about C4 or
        only); with candidate=True, the screen list only."""
        self.write()
        if not views and not candidate:
            views = (self.view({}),)
        argv = ['compare', '--root', str(self.root), '--thread', THREAD]
        for v in views:
            argv += ['--view', v]
        assert compare.main(argv) == 0
        out = sorted((self.root / 'record').glob('session-comparison-2*.jsonl'))
        if candidate:
            return None
        lines = [json.loads(l) for l in out[-1].read_text().splitlines()]
        return lines


def start_file(r):
    """The run-start record file of an invented store."""
    (path,) = [p for p in (r.data / 'records' / 'projects' / 'k' / 'workflow').glob('*.json')
               if json.loads(p.read_text())['body'].get('purpose') == 'run start']
    return path


def rows(lines, comparison=None):
    return [l for l in lines if 'comparison' in l and (comparison is None or l['comparison'] == comparison)]


class SessionComparison(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = Root(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_an_agreeing_session_passes_every_comparison(self):
        self.r.turn('turn-1', 'completed', text=run_text(), brief=BRIEF)
        self.r.turn('turn-2', 'interrupted')
        self.r.stop('turn-2', 'interrupted')
        self.r.run_text_record()
        lines = self.r.compare(self.r.view({'turn-1': 'completed', 'turn-2': 'interrupted'}))
        self.assertEqual({k: lines[0][k] for k in ('header', 'candidate_key', 'examination_root', 'tool')},
                         {'header': True, 'candidate_key': self.r.candidate['record']['candidate_key'], 'examination_root': str(self.r.root.resolve()), 'tool': compare.TOOL})
        self.assertEqual({r['outcome'] for r in rows(lines)}, {'passed'}, rows(lines))
        self.assertEqual([r['comparison'] for r in rows(lines)], ['C2', 'C3', 'C2', 'C3', 'C4', 'W1'])
        self.assertEqual(len(lines[0]['tool_sha256']), 64)
        self.assertEqual(lines[0]['model_version'], 'session-comparison-model/2')
        self.assertEqual(lines[-1], {'summary': {'C2': {'passed': 2}, 'C3': {'passed': 2}, 'C4': {'passed': 1}, 'W1': {'passed': 1}},
                                     'unrecognised': 0, 'compares': compare.COMPARES, 'workflow_scope': compare.WORKFLOW_SCOPE})
        self.assertNotIn('Say hello', json.dumps(lines), 'no session content leaves the record')
        self.assertNotIn(BRIEF, json.dumps(lines))

    def test_the_app_showing_completed_where_codex_recorded_an_abort_fails(self):
        self.r.turn('turn-1', 'interrupted')
        (c3,) = rows(self.r.compare(self.r.view({'turn-1': 'completed'})), 'C3')
        self.assertEqual((c3['outcome'], c3['codex']['says'], c3['app']['says']), ('failed', 'interrupted', 'completed'))
        self.assertEqual(c3['codex']['from'], 'turn_aborted')

    def test_a_turn_on_one_side_only_fails_both_ways(self):
        self.r.turn('turn-1', 'completed')
        c2 = rows(self.r.compare(self.r.view({'turn-9': 'completed'})), 'C2')
        self.assertEqual([(r['subject']['turn'], r['outcome']) for r in c2], [('turn-1', 'failed'), ('turn-9', 'failed')])

    def test_an_outcome_codex_did_not_report_must_read_as_not_known(self):
        self.r.turn('turn-1')
        (c3,) = rows(self.r.compare(self.r.view({'turn-1': 'completed'})), 'C3')
        self.assertEqual((c3['outcome'], c3['codex']['says']), ('failed', 'not reported'))
        self.tearDown(); self.setUp()
        self.r.turn('turn-1')
        (c3,) = rows(self.r.compare(self.r.view({'turn-1': 'inProgress'})), 'C3')
        self.assertEqual(c3['outcome'], 'passed')

    def test_a_failed_turn_is_failed_on_codex_side(self):
        self.r.turn('turn-1', 'completed', error={'message': 'invented'})
        (c3,) = rows(self.r.compare(self.r.view({'turn-1': 'failed'})), 'C3')
        self.assertEqual((c3['outcome'], c3['codex']['says']), ('passed', 'failed'))

    def test_an_interrupt_the_app_recorded_without_an_abort_fails(self):
        self.r.turn('turn-1', 'completed')
        self.r.stop('turn-1', 'interrupted')
        (c4,) = rows(self.r.compare(), 'C4')
        self.assertEqual((c4['outcome'], c4['codex']['says'], c4['app']['says']), ('failed', 'completed', 'interrupted'))

    def test_a_stop_whose_end_the_app_did_not_learn_is_inconclusive_and_one_neither_knows_passes(self):
        self.r.turn('turn-1', 'interrupted')
        self.r.turn('turn-2')
        self.r.stop('turn-1', 'unknown')
        self.r.stop('turn-2', 'unknown')
        c4 = rows(self.r.compare(), 'C4')
        self.assertEqual([(r['subject']['turn'], r['outcome']) for r in c4], [('turn-1', 'inconclusive'), ('turn-2', 'passed')])

    def test_no_session_file_blocks_every_comparison(self):
        self.r.session = False
        lines = self.r.compare()
        self.assertEqual({r['outcome'] for r in rows(lines)}, {'blocked'})

    def test_a_candidate_gets_the_screen_list_and_its_whole_result_from_the_answers(self):
        self.r.turn('turn-1', 'interrupted')
        self.r.turn('turn-2')
        self.assertIsNone(self.r.compare(candidate=True))
        self.assertEqual(list((self.r.root / 'record').glob('session-comparison-*.jsonl')), [], 'on a candidate, compare writes the list only')
        (screen,) = (self.r.root / 'record').glob('screen-list-*.jsonl')
        items = [json.loads(l) for l in screen.read_text().splitlines()]
        self.assertTrue(items[0]['header'])
        self.assertEqual([(i['comparison'], i['screen_must_say']) for i in items[1:]],
                         [('C2', 'the turn is shown'), ('C3', 'the turn is shown as interrupted'),
                          ('C2', 'the turn is shown'), ('C3', 'the turn is shown as not known (no end reported)'),
                          ('C2', 'no turn of this thread is shown other than: turn-1, turn-2')])
        items[1]['answer'], items[1]['note'] = 'passed', 'shown'
        items[2]['answer'], items[2]['note'] = 'passed', 'shown interrupted'
        items[3]['answer'] = 'passed'
        screen.write_text('\n'.join(json.dumps(i) for i in items) + '\n')
        self.assertEqual(compare.main(['answers', '--root', str(self.r.root), '--screen', str(screen)]), 0)
        (out,) = (self.r.root / 'record').glob('session-comparison-*.jsonl')
        lines = [json.loads(l) for l in out.read_text().splitlines()]
        self.assertEqual(lines[0]['answers_of'], screen.name)
        self.assertEqual([(r['comparison'], r['outcome']) for r in rows(lines)],
                         [('C2', 'passed'), ('C3', 'passed'), ('C2', 'not run'), ('C3', 'not run'), ('C2', 'not run'), ('C4', 'not run')],
                         'a passed with no note is not run; the result is whole, C4 included')
        self.assertNotIn('shown interrupted', json.dumps(lines), 'a note is carried as its digest only')


class NoFalsePass(unittest.TestCase):
    """The first independent reading's findings: each way it found to a false
    passed, or a row gone missing, now reported otherwise."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = Root(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_3_views_are_joined_by_turn_identity(self):
        self.r.turn('turn-1', 'completed')
        self.r.turn('turn-2', 'interrupted')
        path = Path(self.r.view({'turn-1': 'completed', 'turn-2': 'interrupted'}))
        saved = json.loads(path.read_text())
        saved['nativeView']['turns'].reverse()
        path.write_text(json.dumps(saved))
        c3 = rows(self.r.compare(str(path)), 'C3')
        self.assertEqual([r['outcome'] for r in c3], ['passed', 'passed'], 'joined by id, the reversed order changes nothing')
        saved['nativeView']['turns'][0]['id'] = 'turn-9'
        path.write_text(json.dumps(saved))
        for old in (self.r.root / 'record').glob('session-comparison-*.jsonl'):
            old.unlink()
        lines = self.r.compare(str(path))
        self.assertEqual({r['outcome'] for r in rows(lines, 'C2') + rows(lines, 'C3')}, {'blocked'})

    def test_4_the_screen_list_asks_about_turns_only_the_app_shows(self):
        self.r.turn('turn-1', 'completed')
        self.r.compare(candidate=True)
        (screen,) = (self.r.root / 'record').glob('screen-list-*.jsonl')
        self.assertIn('no turn of this thread is shown other than: turn-1', screen.read_text())

    def test_5_answers_count_only_for_items_derived_again_from_the_record(self):
        self.r.turn('turn-1', 'completed')
        self.r.compare(candidate=True)
        (screen,) = (self.r.root / 'record').glob('screen-list-*.jsonl')
        original = screen.read_text()
        def answer(edit):
            items = [json.loads(l) for l in original.splitlines()]
            edit(items)
            screen.write_text('\n'.join(json.dumps(i) for i in items) + '\n')
            for old in (self.r.root / 'record').glob('session-comparison-*.jsonl'):
                old.unlink()
            compare.main(['answers', '--root', str(self.r.root), '--screen', str(screen)])
            (out,) = (self.r.root / 'record').glob('session-comparison-*.jsonl')
            return [(r['comparison'], json.dumps(r['subject'], sort_keys=True), r['outcome']) for r in rows([json.loads(l) for l in out.read_text().splitlines()])
                    if r['comparison'] in ('C2', 'C3')]
        def all_passed(items):
            for i in items[1:]:
                i['answer'], i['note'] = 'passed', 'seen'
        honest = answer(all_passed)
        self.assertEqual({o for *_, o in honest}, {'passed'})
        def edited(items):
            all_passed(items)
            items[2]['screen_must_say'] = 'the turn is shown as interrupted'
        self.assertIn(('C3', json.dumps({'thread': THREAD, 'turn': 'turn-1'}, sort_keys=True), 'not run'), answer(edited), 'an edited item answers nothing')
        def invented(items):
            all_passed(items)
            items.append({**items[1], 'subject': {'thread': THREAD, 'turn': 'turn-9'}})
            items[0]['items'] = 'anything'
        self.assertNotIn('turn-9', json.dumps(answer(invented)), 'an item the record does not give is not a row')
        def removed(items):
            del items[1:]
        self.assertEqual({o for *_, o in answer(removed)}, {'not run'}, 'deleted items are not run, not gone')
        for path in self.r.root.rglob(f'rollout-*-{THREAD}.jsonl'):
            path.write_text(path.read_text().replace('task_complete', 'turn_aborted'))
        changed = answer(all_passed)
        self.assertIn(('C3', json.dumps({'thread': THREAD, 'turn': 'turn-1'}, sort_keys=True), 'not run'), changed,
                      'the list is derived again from the record as it is now: an answer about the old end answers nothing')

    def test_6_a_turn_started_twice_is_inconclusive(self):
        self.r.turn('turn-1', 'completed')
        self.r.codex('event_msg', {'type': 'task_started', 'turn_id': 'turn-1'})
        (c3,) = rows(self.r.compare(self.r.view({'turn-1': 'completed'})), 'C3')
        self.assertEqual(c3['outcome'], 'inconclusive')

    def test_7_a_malformed_error_is_not_a_completion(self):
        for error in ({}, ''):
            with self.subTest(error=error):
                r = Root(tempfile.mkdtemp(dir=self.tmp.name))
                r.turn('turn-1', 'completed', error=error)
                (c3,) = rows(r.compare(r.view({'turn-1': 'completed'})), 'C3')
                self.assertEqual(c3['outcome'], 'inconclusive')

    def test_8_an_interrupt_needs_an_abort_for_that_reason(self):
        self.r.codex('event_msg', {'type': 'task_started', 'turn_id': 'turn-1'})
        self.r.codex('event_msg', {'type': 'turn_aborted', 'turn_id': 'turn-1', 'reason': 'replaced'})
        self.r.stop('turn-1', 'interrupted')
        (c4,) = rows(self.r.compare(), 'C4')
        self.assertEqual(c4['outcome'], 'failed')

    def test_9_an_unknown_app_reading_never_passes(self):
        self.r.turn('turn-1')
        self.r.stop('turn-1', 'garbage')
        lines = self.r.compare(self.r.view({'turn-1': None}))
        self.assertEqual([r['outcome'] for r in rows(lines, 'C3') + rows(lines, 'C4')], ['inconclusive', 'inconclusive'])

    def test_10_a_launch_record_or_record_folder_outside_the_root_is_refused(self):
        with tempfile.TemporaryDirectory() as elsewhere:
            outside = Path(elsewhere) / 'launch-record.json'
            outside.write_text(json.dumps({'candidate_key': 'outside'}))
            (self.r.root / 'record' / 'launch-record.json').unlink()
            os.symlink(outside, self.r.root / 'record' / 'launch-record-1.json')
            self.assertIsNone(compare.candidate_key(self.r.root.resolve()))

    def test_11_a_session_file_of_another_thread_is_blocked(self):
        self.r.turn('turn-1', 'completed')
        self.r.write()
        for path in self.r.root.rglob(f'rollout-*-{THREAD}.jsonl'):
            lines = path.read_text().splitlines()
            lines[0] = json.dumps({'timestamp': 't', 'type': 'session_meta', 'payload': {'id': 'another-thread'}})
            path.write_text('\n'.join(lines) + '\n')
        compare.main(['compare', '--root', str(self.r.root), '--thread', THREAD])
        (out,) = (self.r.root / 'record').glob('session-comparison-2*.jsonl')
        self.assertEqual({r['outcome'] for r in rows([json.loads(l) for l in out.read_text().splitlines()])}, {'blocked'})

    def test_13_every_planned_comparison_yields_a_row(self):
        lines = self.r.compare(self.r.view({}))
        self.assertEqual(sorted({r['comparison'] for r in rows(lines)}), ['C2', 'C3', 'C4'])
        self.assertEqual({r['outcome'] for r in rows(lines)}, {'not run'})

    def test_14_unreadable_inputs_give_blocked_rows_not_a_crash(self):
        self.r.codex('event_msg', {'type': 'task_started', 'turn_id': 'turn-1'})
        self.r.write()
        for path in self.r.root.rglob(f'rollout-*-{THREAD}.jsonl'):
            path.write_text(path.read_text() + '[]\n')
        self.assertEqual(compare.main(['compare', '--root', str(self.r.root), '--thread', THREAD]), 0)
        (out,) = (self.r.root / 'record').glob('session-comparison-2*.jsonl')
        lines = [json.loads(l) for l in out.read_text().splitlines()]
        self.assertEqual({r['outcome'] for r in rows(lines)}, {'blocked'})
        self.assertIn('summary', lines[-1])


class SecondReading(unittest.TestCase):
    """The second independent reading's findings, against the strict model."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = Root(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def session_lines(self):
        (path,) = list(self.r.root.rglob(f'rollout-*-{THREAD}.jsonl'))
        return path

    def test_a_completion_followed_by_a_restart_is_not_one_reading(self):
        self.r.turn('turn-1', 'completed')
        self.r.codex('event_msg', {'type': 'task_started', 'turn_id': 'turn-1'})
        (c3,) = rows(self.r.compare(self.r.view({'turn-1': 'completed'})), 'C3')
        self.assertEqual(c3['outcome'], 'inconclusive')

    def test_an_empty_session_or_another_version_blocks_everything(self):
        self.r.write()
        path = self.session_lines()
        for text in ('', json.dumps({'type': 'session_meta', 'payload': {'id': THREAD, 'cli_version': '0.168.0'}}) + '\n'):
            path.write_text(text)
            for old in (self.r.root / 'record').glob('session-comparison-*.jsonl'):
                old.unlink()
            compare.main(['compare', '--root', str(self.r.root), '--thread', THREAD])
            (out,) = (self.r.root / 'record').glob('session-comparison-*.jsonl')
            lines = [json.loads(l) for l in out.read_text().splitlines()]
            self.assertEqual({r['outcome'] for r in rows(lines)}, {'blocked'})
            self.assertEqual(lines[0]['pinned_codex'], '0.169.0')

    def test_free_text_in_any_field_never_reaches_a_row_or_passes(self):
        secret = 'INVENTED MESSAGE TEXT'
        self.r.codex('event_msg', {'type': 'task_started', 'turn_id': 'turn-1'})
        self.r.codex('event_msg', {'type': 'turn_aborted', 'turn_id': 'turn-1', 'reason': secret})
        self.r.stops.append({'kind': 'stop_request', 'record': {'stopRequestId': 'stop:turn-1', 'threadId': THREAD, 'turnId': 'turn-1',
                             'turnOutcome': 'interrupted', 'state': secret, 'outcomeSource': secret}})
        lines = self.r.compare(self.r.view({'turn-1': secret}))
        self.assertNotIn(secret, json.dumps(lines))
        self.assertEqual([r['outcome'] for r in rows(lines, 'C3') + rows(lines, 'C4')], ['inconclusive', 'failed'])
        self.assertGreater(lines[-1]['unrecognised'], 0, 'unrecognised values are counted apart')

    def test_a_turn_of_the_view_with_no_record_blocks_the_view(self):
        self.r.turn('turn-1', 'completed')
        path = Path(self.r.view({'turn-1': 'completed'}))
        saved = json.loads(path.read_text())
        saved['nativeView']['turns'].append({'id': 'turn-extra', 'status': 'completed'})
        path.write_text(json.dumps(saved))
        lines = self.r.compare(str(path))
        self.assertEqual({r['outcome'] for r in rows(lines, 'C2') + rows(lines, 'C3')}, {'blocked'})

    def test_answers_against_a_missing_session_write_blocked_rows(self):
        self.r.turn('turn-1', 'completed')
        self.r.compare(candidate=True)
        (screen,) = (self.r.root / 'record').glob('screen-list-*.jsonl')
        self.session_lines().unlink()
        self.assertEqual(compare.main(['answers', '--root', str(self.r.root), '--screen', str(screen)]), 0)
        (out,) = (self.r.root / 'record').glob('session-comparison-*.jsonl')
        self.assertEqual({(r['comparison'], r['outcome']) for r in rows([json.loads(l) for l in out.read_text().splitlines()])},
                         {('C2', 'blocked'), ('C3', 'blocked'), ('C4', 'blocked'), ('W1', 'blocked')})

    def test_an_unexpected_failure_writes_blocked_rows_naming_only_its_kind(self):
        self.r.turn('turn-1', 'completed')
        self.r.write()
        original = compare.compare_views
        compare.compare_views = lambda *a: (_ for _ in ()).throw(RuntimeError('INVENTED TRACE TEXT'))
        try:
            self.assertEqual(compare.main(['compare', '--root', str(self.r.root), '--thread', THREAD, '--view', self.r.view({})]), 1)
        finally:
            compare.compare_views = original
        (out,) = (self.r.root / 'record').glob('session-comparison-*.jsonl')
        text = out.read_text()
        self.assertNotIn('INVENTED TRACE TEXT', text)
        self.assertIn('RuntimeError', text)
        self.assertEqual({r['outcome'] for r in rows([json.loads(l) for l in text.splitlines()])}, {'blocked'})

    def test_a_stop_with_no_usable_identity_is_blocked_not_dropped(self):
        self.r.turn('turn-1', 'completed')
        self.r.stops.append({'kind': 'stop_request', 'record': {'stopRequestId': None, 'threadId': THREAD, 'turnId': 'turn-1', 'turnOutcome': 'interrupted'}})
        (c4,) = rows(self.r.compare(), 'C4')
        self.assertEqual(c4['outcome'], 'blocked')


class ThirdReading(unittest.TestCase):
    """The third reading's findings 2 and 3, and the README's three points."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = Root(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_turn_the_view_shows_only_through_an_item_is_a_row(self):
        self.r.turn('turn-1', 'completed')
        path = Path(self.r.view({'turn-1': 'completed'}))
        saved = json.loads(path.read_text())
        saved['nativeView']['items'] = [{'threadId': THREAD, 'turnId': 'turn-ui-only', 'id': 'item-1'},
                                        {'threadId': 'another-thread', 'turnId': 'elsewhere', 'id': 'item-2'}]
        saved['nativeView']['turnErrors'] = [{'threadId': THREAD, 'turnId': 'turn-1'}]
        path.write_text(json.dumps(saved))
        lines = self.r.compare(str(path))
        c2 = {r['subject']['turn']: r['outcome'] for r in rows(lines, 'C2')}
        self.assertEqual(c2, {'turn-1': 'passed', 'turn-ui-only': 'failed'}, 'every turn the view shows is a row; another thread is not')
        (c3,) = [r for r in rows(lines, 'C3') if r['subject']['turn'] == 'turn-ui-only']
        self.assertEqual(c3['outcome'], 'blocked')

    def test_a_turn_codex_has_that_the_view_shows_with_no_status_is_inconclusive(self):
        self.r.turn('turn-1', 'completed')
        path = Path(self.r.view({}))
        saved = json.loads(path.read_text())
        saved['nativeView']['items'] = [{'threadId': THREAD, 'turnId': 'turn-1', 'id': 'item-1'}]
        path.write_text(json.dumps(saved))
        lines = self.r.compare(str(path))
        self.assertEqual([r['outcome'] for r in rows(lines, 'C2') + rows(lines, 'C3')], ['passed', 'inconclusive'])

    def test_the_fallback_writes_rows_even_when_the_summary_check_fails(self):
        self.r.turn('turn-1', 'completed')
        self.r.write()
        original = compare.summary
        compare.summary = lambda rows: (_ for _ in ()).throw(RuntimeError('invented'))
        try:
            self.assertEqual(compare.main(['compare', '--root', str(self.r.root), '--thread', THREAD, '--view', self.r.view({})]), 1)
        finally:
            compare.summary = original
        (out,) = (self.r.root / 'record').glob('session-comparison-*.jsonl')
        lines = [json.loads(l) for l in out.read_text().splitlines()]
        self.assertEqual({(r['comparison'], r['outcome']) for r in rows(lines)}, {('C2', 'blocked'), ('C3', 'blocked'), ('C4', 'blocked'), ('W1', 'blocked')})
        self.assertEqual(lines[-1]['summary'], {'C2': {'blocked': 1}, 'C3': {'blocked': 1}, 'C4': {'blocked': 1}, 'W1': {'blocked': 1}})

    def test_a_root_without_its_project_folder_is_refused(self):
        (self.r.root / 'project').rmdir()
        with self.assertRaises(compare.Refused):
            compare.examination_root(self.r.root)

    def test_a_launch_record_outside_the_root_refuses_the_root(self):
        with tempfile.TemporaryDirectory() as elsewhere:
            outside = Path(elsewhere) / 'launch-record.json'
            outside.write_text(json.dumps({'candidate_key': 'outside'}))
            os.symlink(outside, self.r.root / 'record' / 'launch-record-2.json')
            with self.assertRaises(compare.Refused):
                compare.examination_root(self.r.root)

    def test_a_saved_view_not_named_is_said(self):
        self.r.turn('turn-1', 'completed')
        named = self.r.view({'turn-1': 'completed'})
        other = self.r.root / 'record' / 'host-status-earlier.json'
        other.write_text(Path(named).read_text())
        lines = self.r.compare(named)
        self.assertEqual(lines[0]['saved_views_not_named'], ['host-status-earlier.json'])

    def test_a_saved_view_is_never_replaced_by_the_operators_list(self):
        self.r.turn('turn-1', 'completed')
        self.r.view({'turn-1': 'interrupted'})
        self.r.write()
        self.assertEqual(compare.main(['compare', '--root', str(self.r.root), '--thread', THREAD]), 1)
        self.assertEqual(list((self.r.root / 'record').glob('screen-list-*.jsonl')), [])
        (out,) = (self.r.root / 'record').glob('session-comparison-2*.jsonl')
        self.assertEqual({r['outcome'] for r in rows([json.loads(l) for l in out.read_text().splitlines()])}, {'blocked'})


class TheRealFormat(unittest.TestCase):
    """An invented session laid out as the real 0.169.0 file was: an ordinal on
    each line and a top-level `metadata` on response items; session_meta with
    `session_id` beside `id`; a developer message and other user-role messages
    beside the person's; world_state, turn_context, thread_settings_applied,
    item_completed, token_count and token_usage_record lines; `turn_id` and
    `root_turn_id` on every turn event; no `error` key on a clean end or on an
    abort; and an error object of `message` and `codex_error_info` on a failed
    turn. Every value is invented."""

    def layout(self, version='0.169.0'):
        msg = lambda role, text, turn, kind: {'type': 'message', 'id': 'msg_x', 'role': role, 'content': [{'type': 'input_text', 'text': text}],
                                             'internal_chat_message_metadata_passthrough': {'turn_id': turn, 'content_item_kinds': [kind],
                                                                                           'content_item_metadata': [{}], 'create_time': 1}}
        started = lambda turn: ('event_msg', {'type': 'task_started', 'turn_id': turn, 'root_turn_id': turn, 'started_at': 1,
                                              'model_context_window': 1, 'collaboration_mode_kind': 'default', 'turn_attribution': {}})
        context = lambda turn: ('turn_context', {'turn_id': turn, 'root_turn_id': turn, 'cwd': '/invented', 'approval_policy': 'invented',
                                                 'sandbox_policy': {}, 'model': 'invented'})
        usage = lambda turn: ('token_usage_record', {'turn_id': turn, 'root_turn_id': turn, 'thread_id': THREAD, 'session_id': THREAD,
                                                     'response_id': 'resp_x', 'usage': {}, 'turn_token_usage': {}, 'thread_token_usage': {}})
        ended = {'root_turn_id': None, 'started_at': 1, 'completed_at': 2, 'duration_ms': 1}
        lines = [
            ('session_meta', {'id': THREAD, 'session_id': THREAD, 'cli_version': version, 'source': 'invented', 'base_instructions': {'text': 'invented'}}),
            started('A'),
            ('response_item', msg('developer', 'Invented role guidance.', 'A', 'permissions.instructions')),
            ('response_item', msg('user', '<environment_context>invented</environment_context>', 'A', 'environments.environment_context')),
            ('world_state', {'full': {}, 'state': {}}),
            context('A'),
            ('event_msg', {'type': 'thread_settings_applied', 'thread_id': THREAD, 'thread_settings': {}}),
            ('response_item', msg('user', 'Invented request.', 'A', 'user.text')),
            ('event_msg', {'type': 'item_completed', 'turn_id': 'A', 'thread_id': THREAD, 'item': {'type': 'UserMessage', 'id': 'other-id'},
                           'started_at_ms': 1, 'completed_at_ms': 2}),
            ('response_item', {'type': 'message', 'id': 'msg_y', 'role': 'assistant', 'content': [{'type': 'output_text', 'text': 'Invented reply.'}],
                               'internal_chat_message_metadata_passthrough': {'turn_id': 'A', 'content_item_kinds': ['unknown']}}),
            usage('A'),
            ('event_msg', {'type': 'token_count', 'info': None, 'rate_limits': None}),
            ('event_msg', {'type': 'task_complete', 'turn_id': 'A', **ended, 'root_turn_id': 'A', 'last_agent_message': 'Invented reply.',
                           'time_to_first_token_ms': 1}),
            started('B'),
            context('B'),
            ('response_item', msg('user', 'Invented request.', 'B', 'user.text')),
            ('response_item', msg('user', '<turn_aborted>invented</turn_aborted>', 'B', 'generic.turn_aborted')),
            ('event_msg', {'type': 'turn_aborted', 'turn_id': 'B', **ended, 'root_turn_id': 'B', 'reason': 'interrupted'}),
            started('C'),
            context('C'),
            ('response_item', msg('user', 'Invented request.', 'C', 'user.text')),
            ('event_msg', {'type': 'task_complete', 'turn_id': 'C', **ended, 'root_turn_id': 'C', 'last_agent_message': None,
                           'time_to_first_token_ms': None, 'error': {'message': 'invented', 'codex_error_info': 'other'}}),
        ]
        out = []
        for n, (k, p) in enumerate(lines):
            line = {'timestamp': 't', 'ordinal': n, 'type': k, 'payload': p}
            if k == 'response_item':
                line['metadata'] = {}
            out.append(json.dumps(line) + '\n')
        return ''.join(out).encode()

    def test_turns_read_from_the_pins_layout(self):
        session = compare.parse_session(self.layout(), THREAD)
        self.assertEqual([(t, session['turns'][t]['says'], session['turns'][t]['from']) for t in session['order']],
                         [('A', 'completed', 'task_complete'), ('B', 'interrupted', 'turn_aborted'), ('C', 'failed', 'task_complete')])
        self.assertEqual(session['turns']['B']['reason'], 'interrupted')
        self.assertEqual(session['workflow_marked_lines'], 0)

    def test_the_pins_layout_compares_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = Root(tmp)
            r.write()
            (path,) = r.root.rglob(f'rollout-*-{THREAD}.jsonl')
            path.write_bytes(self.layout())
            r.stop('B', 'interrupted')
            db = sqlite3.connect(r.data / 'runtime' / 'recovery.ledger.sqlite')
            db.execute('INSERT INTO ledger_entry (kind, entry) VALUES (?, ?)', ('stop_request', json.dumps(r.stops[-1])))
            db.commit()
            db.close()
            lines = r.compare(r.view({'A': 'completed', 'B': 'interrupted', 'C': 'failed'}))
            self.assertEqual(lines[0]['pinned_codex'], '0.169.0')
            self.assertEqual(lines[-1]['summary'], {'C2': {'passed': 3}, 'C3': {'passed': 3}, 'C4': {'passed': 1}})
            self.assertNotIn('Invented reply', json.dumps(lines))

    def test_a_run_start_in_the_pins_layout_compares_w1_end_to_end(self):
        """The run text and the person's brief as two text elements of turn A's
        user message, laid out as the 0.169.0 file lays out a user message."""
        data = self.layout().replace(
            json.dumps([{'type': 'input_text', 'text': 'Invented request.'}]).encode()[1:-1],
            json.dumps([{'type': 'input_text', 'text': run_text()}, {'type': 'input_text', 'text': BRIEF}]).encode()[1:-1], 1)
        self.assertEqual(compare.parse_session(data, THREAD)['workflow_marked_lines'], 1)
        with tempfile.TemporaryDirectory() as tmp:
            r = Root(tmp)
            r.run_text_record()
            r.write()
            (path,) = r.root.rglob(f'rollout-*-{THREAD}.jsonl')
            path.write_bytes(data)
            lines = r.compare(r.view({'A': 'completed', 'B': 'interrupted', 'C': 'failed'}))
            (w1,) = rows(lines, 'W1')
            self.assertEqual((w1['outcome'], w1['codex']['turn'], w1['codex']['element']), ('passed', 'A', 0), w1)
            self.assertNotIn(BRIEF, json.dumps(lines))

    def test_the_same_layout_from_any_other_version_is_refused(self):
        for version in ('0.167.0', '0.167.2', '0.168.0', '0.169.1', '0.170.0', '0.169', '0.169.0.0', 'v0.169.0', ' 0.169.0', '0.169.0 ',
                        '0.169.0-alpha.1', '', None, 169, ['0.169.0']):
            with self.subTest(version=version):
                with self.assertRaises(compare.Refused) as refused:
                    compare.parse_session(self.layout(version), THREAD)
                self.assertEqual(str(refused.exception), 'the session file was written by a Codex version this model was not written against')
        data = self.layout().replace(b'"cli_version": "0.169.0", ', b'', 1)
        self.assertNotIn(b'cli_version', data)
        with self.assertRaises(compare.Refused):
            compare.parse_session(data, THREAD)

    def test_a_file_of_the_previous_pin_blocks_every_comparison(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = Root(tmp)
            r.write()
            (path,) = r.root.rglob(f'rollout-*-{THREAD}.jsonl')
            path.write_bytes(self.layout('0.167.0'))
            lines = r.compare(r.view({'A': 'completed', 'B': 'interrupted', 'C': 'failed'}))
            self.assertEqual({r_['outcome'] for r_ in rows(lines)}, {'blocked'})
            self.assertEqual({r_['comparison'] for r_ in rows(lines)}, {'C2', 'C3', 'C4', 'W1'})
            self.assertEqual(lines[0]['pinned_codex'], '0.169.0')
            self.assertNotIn('passed', json.dumps(lines[-1]['summary']))

    def test_a_turn_event_with_a_null_turn_identity_blocks_the_file(self):
        data = self.layout().replace(b'"type": "turn_aborted", "turn_id": "B"', b'"type": "turn_aborted", "turn_id": null', 1)
        self.assertIn(b'"turn_id": null', data)
        with self.assertRaises(compare.Refused):
            compare.parse_session(data, THREAD)


class WhereRecordsMayBeRead(unittest.TestCase):
    def test_only_a_root_launch_made_is_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / 'home').mkdir()
            (Path(tmp) / 'record').mkdir()
            with self.assertRaises(compare.Refused):
                compare.examination_root(tmp)

    def test_the_owners_codex_home_is_refused(self):
        with self.assertRaises(compare.Refused):
            compare.examination_root(Path.home() / '.codex')

    def test_a_session_file_reached_through_a_link_outside_the_root_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as elsewhere:
            r = Root(tmp)
            outside = Path(elsewhere) / f'rollout-x-{THREAD}.jsonl'
            outside.write_text('')
            sessions = r.data / 'sessions'
            sessions.mkdir(parents=True)
            os.symlink(outside, sessions / f'rollout-x-{THREAD}.jsonl')
            with self.assertRaises(compare.Refused):
                compare.session_file(r.root.resolve(), THREAD)



ONE_PAIR = 'the text Codex holds does not carry exactly one begin and one end marker and no other mention of them'
OTHER_LINE = 'a line other than the one message carries the workflow markers'


class TheWorkflowComparisonByUniqueness(unittest.TestCase):
    """W1, bounded by uniqueness: it passes only where Codex holds exactly one
    message carrying the workflow markers in the thread, the App exactly one
    run-start text for it, and the two agree byte for byte with the stored
    WORKFLOW.md bytes between the markers. Any other count, or anything
    unreadable, is blocked; a difference with one of each fails."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = Root(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def stated(self, line):
        self.assertEqual(line['compares'], {'C2': 'turns', 'C3': 'outcomes', 'C4': 'interrupts',
                                            'W1': 'the workflow supplied, in a root with one run'})
        self.assertEqual(line['workflow_scope'], compare.WORKFLOW_SCOPE)
        self.assertNotIn('workflow_comparison', line, 'the old "not available" sentence is not carried')

    def w1(self, r=None):
        r = r or self.r
        lines = r.compare(r.view({'turn-1': 'completed'}))
        found = rows(lines, 'W1')
        self.assertEqual(len(found), 1, found)
        text = json.dumps(lines)
        for secret in ('Say hello', BRIEF, 'Invented workflow', 'Workflow run start'):
            self.assertNotIn(secret, text, 'no row carries message text')
        return found[0], lines

    def run_start(self, text=None, brief=BRIEF):
        self.r.turn('turn-1', 'completed', text=run_text() if text is None else text, brief=brief)

    # The one positive case.
    def test_one_message_and_one_run_text_equal_byte_for_byte_pass(self):
        self.run_start()
        self.r.run_text_record()
        w1, lines = self.w1()
        self.assertEqual(w1['outcome'], 'passed', w1)
        self.assertEqual(w1['subject'], {'thread': THREAD, 'run': RUN})
        self.assertEqual({k: w1['app'][k] for k in ('origin', 'workflow', 'revision', 'runRecords', 'unreadableWorkflowRecords')},
                         {'origin': 'bundled', 'workflow': NAME, 'revision': REVISION, 'runRecords': 1, 'unreadableWorkflowRecords': 0})
        self.assertEqual(w1['selected'], {'candidate': self.r.candidate['record']['candidate_key'], 'workflow': NAME, 'revision': REVISION,
                                          'manifest_sha256': hashlib.sha256(self.r.candidate['manifest']).hexdigest(),
                                          'workflow_sha256': hashlib.sha256(WORKFLOW.encode()).hexdigest(), 'workflow_bytes': len(WORKFLOW.encode())})
        self.assertEqual(w1['codex']['text_sha256'], w1['app']['text_sha256'])
        self.assertEqual(w1['codex']['workflow_sha256'], hashlib.sha256(WORKFLOW.encode()).hexdigest())
        self.assertEqual((w1['codex']['messagesWithWorkflowMarkers'], w1['codex']['element'], w1['codex']['elements']), (1, 0, 2))
        self.assertEqual(lines[-1]['summary']['W1'], {'passed': 1})
        self.stated(lines[0])
        self.stated(lines[-1])

    # Content that differs, with one of each: failed.
    def test_a_text_codex_holds_other_than_the_run_text_fails(self):
        self.run_start(text=run_text('# Invented workflow\nSay goodbye.\n'))
        self.r.run_text_record()
        w1, _ = self.w1()
        self.assertEqual((w1['outcome'], w1['reason']), ('failed', 'the text Codex holds is not the run text the App composed, byte for byte'))

    def test_a_text_differing_by_one_trailing_byte_fails(self):
        self.run_start(text=run_text() + '\n')
        self.r.run_text_record()
        self.assertEqual(self.w1()[0]['outcome'], 'failed')

    def test_workflow_bytes_other_than_the_stored_ones_fail_even_where_the_text_matches(self):
        self.run_start()
        record = self.r.run_text_record()
        record['workflow_file']['content']['value'] = hashlib.sha256(b'other stored bytes').hexdigest()
        w1, _ = self.w1()
        self.assertEqual((w1['outcome'], w1['reason']), ('failed', 'the App recorded other WORKFLOW.md bytes than the ones it sent'))

    def test_markers_of_another_revision_fail(self):
        self.run_start(text=run_text(revision='f' * 64))
        self.r.run_text_record()
        w1, _ = self.w1()
        self.assertEqual((w1['outcome'], w1['reason']), ('failed', "the markers Codex holds name another workflow or revision than the App's run text"))

    # Counts other than one on either side: blocked.
    def test_no_message_carrying_the_markers_is_blocked(self):
        self.r.turn('turn-1', 'completed')
        self.r.run_text_record()
        w1, _ = self.w1()
        self.assertEqual((w1['outcome'], w1['codex']['messagesWithWorkflowMarkers']), ('blocked', 0))

    def test_two_messages_carrying_the_markers_are_blocked_even_when_both_are_exact(self):
        self.run_start()
        self.r.message('turn-1', run_text())
        self.r.run_text_record()
        w1, _ = self.w1()
        self.assertEqual((w1['outcome'], w1['codex']['messagesWithWorkflowMarkers']), ('blocked', 2))

    def test_a_reply_quoting_the_markers_is_a_second_message_and_blocks(self):
        self.run_start()
        self.r.message('turn-1', 'I read <<<chirality-workflow invented-workflow@x begin>>>', role='assistant')
        self.r.run_text_record()
        self.assertEqual(self.w1()[0]['outcome'], 'blocked')

    def test_markers_in_the_persons_brief_as_well_are_blocked(self):
        self.run_start(brief='see <<<chirality-workflow invented-workflow@x end>>>')
        self.r.run_text_record()
        w1, _ = self.w1()
        self.assertEqual((w1['outcome'], w1['reason']), ('blocked', 'more than one text element of the message carries the workflow markers'))

    def test_markers_only_in_a_developer_message_are_blocked(self):
        self.r.turn('turn-1', 'completed')
        self.r.message('turn-1', run_text(), role='developer')
        self.r.run_text_record()
        w1, _ = self.w1()
        self.assertEqual((w1['outcome'], w1['reason']), ('blocked', "the message carrying the workflow markers is not the person's input"))

    def test_no_run_text_for_the_thread_is_blocked(self):
        self.run_start()
        w1, _ = self.w1()
        self.assertEqual((w1['outcome'], w1['app']['runRecords']), ('blocked', 0))

    def test_two_run_texts_for_the_thread_are_blocked(self):
        self.run_start()
        self.r.run_text_record()
        self.r.run_text_record(run='run-2')
        w1, _ = self.w1()
        self.assertEqual((w1['outcome'], w1['app']['runRecords']), ('blocked', 2))

    def test_a_run_text_of_another_thread_does_not_count(self):
        self.run_start()
        self.r.run_text_record(conversation='019a0000-0000-7000-8000-00000000000b')
        w1, _ = self.w1()
        self.assertEqual((w1['outcome'], w1['reason'], w1['app']['runRecords']), ('blocked', "the root's one run is of another conversation", 1))

    def test_a_run_text_alone_gives_one_blocked_row(self):
        self.r.turn('turn-1', 'completed')
        self.r.run_text_record()
        self.assertEqual(self.w1()[0]['outcome'], 'blocked')

    def test_a_successor_run_is_not_compared(self):
        self.run_start()
        record = self.r.run_text_record()
        record['chain'] = {'prior_run': 'run-0', 'prior_workflow': record['workflow'], 'ended': 'completed'}
        self.assertEqual(self.w1()[0]['outcome'], 'blocked')

    def test_any_other_run_record_in_the_root_blocks_even_an_end_notice_of_the_same_run(self):
        """The root may hold one run record in total: an end notice of the same
        run, a supply check, or a run of another conversation each block."""
        def supply_check(r):
            r.records.append({'record_kind': 'supply_check', 'check': 'workflow-check:1', 'run': RUN, 'conversation': THREAD,
                              'purpose': 'run start', 'expected_text': r.records[0]['text_identity'], 'state': 'found', 'read_at': 't',
                              'evidence_limits': []})
        cases = {'end notice of the same run': lambda r: r.end_notice(),
                 'supply check of the same run': supply_check,
                 'run start of another conversation': lambda r: r.run_text_record(run='run-2', conversation='019a0000-0000-7000-8000-00000000000b'),
                 'another conversation, its frame not its own': lambda r: r.run_text_record(run='second-run', conversation='other-conversation',
                                                                                          lines=frame_lines(run=RUN)),
                 'another conversation, a chain without its fields': lambda r: r.run_text_record(run='run-2', conversation='other-conversation',
                                                                                               chain={})}
        for name, add in cases.items():
            with self.subTest(name):
                r = Root(tempfile.mkdtemp(dir=self.tmp.name))
                r.turn('turn-1', 'completed', text=run_text(), brief=BRIEF)
                r.run_text_record()
                add(r)
                w1, _ = self.w1(r)
                self.assertEqual((w1['outcome'], w1['reason'], w1['app']['runRecords']),
                                 ('blocked', 'the examination root holds more than the one run this comparison covers, or none', 2))

    # Anything unreadable: blocked.
    def test_an_unreadable_workflow_record_blocks(self):
        for bad in ('{', '[]', json.dumps({'version': 1, 'record_id': 'wr-record:v1:00000000-0000-4000-8000-999999999999', 'body': {}}),
                    json.dumps(envelope(7, {'record_kind': 'run_text', 'purpose': 'other', 'conversation': THREAD})[1])):
            with self.subTest(bad=bad[:40]):
                r = Root(tempfile.mkdtemp(dir=self.tmp.name))
                r.turn('turn-1', 'completed', text=run_text(), brief=BRIEF)
                r.run_text_record()
                r.write()
                (r.data / 'records' / 'projects' / 'k' / 'workflow' / '00000000-0000-4000-8000-000000000007.json').write_text(bad)
                w1, _ = self.w1(r)
                self.assertEqual(w1['outcome'], 'blocked')

    def test_a_record_not_identified_by_exact_bytes_blocks(self):
        self.run_start()
        record = self.r.run_text_record()
        record['text_identity']['method'] = 'another-method'
        self.assertEqual(self.w1()[0]['outcome'], 'blocked')

    def test_a_record_whose_markers_are_not_its_workflows_blocks(self):
        self.run_start()
        record = self.r.run_text_record()
        record['workflow']['name'] = 'another-workflow'
        self.assertEqual(self.w1()[0]['outcome'], 'blocked')

    def test_a_source_origin_the_comparison_does_not_know_never_passes(self):
        self.run_start()
        record = self.r.run_text_record()
        record['workflow']['origin'] = 'elsewhere'
        w1, _ = self.w1()
        self.assertEqual((w1['outcome'], w1['reason']), ('blocked', "the root's one run record is not a run start this comparison reads"))

    # Delimiters and encodings: fail closed.
    def test_a_body_holding_its_own_end_marker_is_blocked_even_when_bytes_agree(self):
        body = WORKFLOW + f'<<<chirality-workflow invented-workflow@{REVISION[:12]} end>>>\n'
        self.run_start(text=run_text(body))
        self.r.run_text_record(body=body)
        w1, _ = self.w1()
        self.assertEqual((w1['outcome'], w1['reason']), ('blocked', ONE_PAIR))

    def test_markers_only_in_an_encoded_form_are_blocked(self):
        self.run_start(text=run_text().replace('<', '&lt;'))
        self.r.run_text_record()
        w1, _ = self.w1()
        self.assertEqual((w1['outcome'], w1['reason']), ('blocked', ONE_PAIR))

    def test_markers_nested_in_another_line_are_found_and_block(self):
        for value in (json.dumps({'output': run_text()}), run_text().replace('<', '\\u003c'), urllib.parse.quote(run_text()),
                      json.dumps(json.dumps({'text': run_text().replace('<', '&lt;')}))):
            with self.subTest(value=value[:30]):
                r = Root(tempfile.mkdtemp(dir=self.tmp.name))
                r.turn('turn-1', 'completed', text=run_text(), brief=BRIEF)
                r.codex('response_item', {'type': 'function_call_output', 'call_id': 'c', 'output': value})
                r.run_text_record()
                w1, _ = self.w1(r)
                self.assertEqual((w1['outcome'], w1['reason']), ('blocked', OTHER_LINE))

    def test_an_exact_copy_of_the_text_in_an_event_line_still_blocks(self):
        """No event line is taken as a copy of the message: text equality does
        not show that it is the same message."""
        self.run_start()
        self.r.codex('event_msg', {'type': 'item_completed', 'turn_id': 'turn-1', 'item': {'type': 'UserMessage', 'id': 'u',
                                   'content': [{'type': 'text', 'text': run_text()}, {'type': 'text', 'text': BRIEF}]}})
        self.r.run_text_record()
        w1, _ = self.w1()
        self.assertEqual((w1['outcome'], w1['reason'], w1['codex']['linesWithWorkflowMarkers']), ('blocked', OTHER_LINE, 2))

    def test_an_event_line_holding_anything_else_with_the_markers_blocks(self):
        for turn, text in (('turn-1', run_text() + '\n' + BRIEF), ('turn-9', run_text()), (None, run_text()), ('turn-1', 'chirality-workflow')):
            with self.subTest(turn=turn):
                r = Root(tempfile.mkdtemp(dir=self.tmp.name))
                r.turn('turn-1', 'completed', text=run_text(), brief=BRIEF)
                r.codex('event_msg', {'type': 'user_message', 'message': text, **({'turn_id': turn} if turn else {})})
                r.run_text_record()
                self.assertEqual(self.w1(r)[0]['outcome'], 'blocked')

    # What stays as it was.
    def test_with_no_workflow_run_there_is_no_row_and_the_statement_stands(self):
        self.r.turn('turn-1', 'completed')
        lines = self.r.compare(self.r.view({'turn-1': 'completed'}))
        self.assertEqual(rows(lines, 'W1'), [])
        self.stated(lines[0])
        self.stated(lines[-1])

    def test_asking_for_it_by_name_is_taken_and_an_unknown_name_refused(self):
        self.run_start()
        self.r.run_text_record()
        self.r.write()
        view = self.r.view({'turn-1': 'completed'})
        self.assertEqual(compare.main(['compare', '--root', str(self.r.root), '--thread', THREAD, '--view', view, '--comparison', 'W1']), 0)
        for name in ('workflow', 'w1', 'C9'):
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                self.assertEqual(compare.main(['compare', '--root', str(self.r.root), '--thread', THREAD, '--comparison', name]), 2)
            self.assertIn('no comparison of that name', err.getvalue())

    def test_the_screen_list_and_the_answers_carry_it(self):
        self.run_start()
        self.r.run_text_record()
        self.r.compare(candidate=True)
        (screen,) = (self.r.root / 'record').glob('screen-list-*.jsonl')
        head = json.loads(screen.read_text().splitlines()[0])
        self.stated(head)
        self.assertFalse(any('W1' in json.dumps(json.loads(l)) for l in screen.read_text().splitlines()[1:]),
                         'W1 is read from the records, not asked of the operator')
        self.assertEqual(compare.main(['answers', '--root', str(self.r.root), '--screen', str(screen)]), 0)
        (out,) = (self.r.root / 'record').glob('session-comparison-2*.jsonl')
        lines = [json.loads(l) for l in out.read_text().splitlines()]
        self.assertEqual([r['outcome'] for r in rows(lines, 'W1')], ['passed'])
        self.stated(lines[0])
        self.stated(lines[-1])

    def test_a_blocked_session_carries_the_row_blocked(self):
        self.r.session = False
        self.run_start()
        self.r.run_text_record()
        lines = self.r.compare(self.r.view({'turn-1': 'completed'}))
        self.assertEqual({(r['comparison'], r['outcome']) for r in rows(lines)},
                         {('C2', 'blocked'), ('C3', 'blocked'), ('C4', 'blocked'), ('W1', 'blocked')})
        self.stated(lines[-1])

    def test_the_fallback_carries_the_statement_and_w1_blocked(self):
        self.run_start()
        self.r.run_text_record()
        self.r.write()
        original = compare.compare_views
        compare.compare_views = lambda *a: (_ for _ in ()).throw(RuntimeError('invented'))
        try:
            self.assertEqual(compare.main(['compare', '--root', str(self.r.root), '--thread', THREAD, '--view', self.r.view({})]), 1)
        finally:
            compare.compare_views = original
        (out,) = (self.r.root / 'record').glob('session-comparison-2*.jsonl')
        lines = [json.loads(l) for l in out.read_text().splitlines()]
        self.stated(lines[0])
        self.stated(lines[-1])
        self.assertEqual(lines[-1]['summary']['W1'], {'blocked': 1})

    def test_a_table_counts_a_w1_pass_of_this_version(self):
        self.run_start()
        self.r.run_text_record()
        self.w1()
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'standalone'))
        try:
            import table
        finally:
            sys.path.pop(0)
        text = '\n'.join(table.comparisons([self.r.root / 'record']))
        (line,) = [l for l in text.splitlines() if '| W1 |' in l]
        self.assertEqual(int(line.split('| W1 |')[1].split('|')[0]), 1, text)
        self.assertNotIn('not available', text)


class SecondW1Reading(unittest.TestCase):
    """The first independent reading of W1: each way it found to a pass that
    the inputs did not establish, now blocked or failed."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = self.fresh()

    def tearDown(self):
        self.tmp.cleanup()

    def fresh(self):
        r = Root(tempfile.mkdtemp(dir=self.tmp.name))
        r.turn('turn-1', 'completed', text=run_text(), brief=BRIEF)
        r.run_text_record()
        return r

    def outcome(self, r=None, before=None):
        r = r or self.r
        r.write()
        if before:
            before(r)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            lines = r.compare(r.view({'turn-1': 'completed'}))
        text = json.dumps(lines)
        for secret in ('Say hello', BRIEF, 'Workflow run start', 'INVENTED SENTINEL'):
            self.assertNotIn(secret, text)
        found = rows(lines, 'W1')
        return (found[0]['outcome'], found[0]['reason']) if found else ('no row', None)

    def selected(self, r):
        return r.root / 'record' / 'selected-workflow'

    def test_the_baseline_passes(self):
        self.assertEqual(self.outcome()[0], 'passed')

    # A: the candidate's own bytes of the selected workflow.
    def test_without_the_reference_w1_is_blocked(self):
        self.r.selected = False
        self.assertEqual(self.outcome()[0], 'blocked')

    def test_a_reference_not_the_candidates_is_blocked(self):
        cases = {
            'package file changed': lambda r: (self.selected(r) / 'package' / 'WORKFLOW.md').write_bytes(b'other bytes\n'),
            'package file removed': lambda r: (self.selected(r) / 'package' / 'WORKFLOW.md').unlink(),
            'package file added': lambda r: (self.selected(r) / 'package' / 'EXTRA.md').write_bytes(b'extra\n'),
            'manifest changed': lambda r: (self.selected(r) / 'MANIFEST.json').write_bytes(r.candidate['manifest'] + b' '),
            'inventory changed': lambda r: (self.selected(r) / 'identification' / 'bundle-inventory.json').write_bytes(r.candidate['inventory'] + b' '),
            'identification invalid': lambda r: (self.selected(r) / 'identification' / 'candidate-identification.json').write_text(
                json.dumps({**r.candidate['record'], 'route': 'other'})),
            'reference names another path': lambda r: (self.selected(r) / 'reference.json').write_text(
                json.dumps({'name': NAME, 'bundle_path': 'Contents/Resources/other/' + NAME})),
            'reference has another field': lambda r: (self.selected(r) / 'reference.json').write_text(
                json.dumps({'name': NAME, 'bundle_path': 'Contents/Resources/workflows/' + NAME, 'revision': REVISION})),
            'reference names another workflow': lambda r: (self.selected(r) / 'reference.json').write_text(
                json.dumps({'name': 'other-workflow', 'bundle_path': 'Contents/Resources/workflows/other-workflow'})),
            'launch record of another candidate': lambda r: r.launch_record(candidate_key='0000000000-000000000000'),
            'launch record of another identifier': lambda r: r.launch_record(identifier='dev.chirality.app-v4.candidate.other'),
            'launch record of another bundle': lambda r: r.launch_record(bundle='/invented/elsewhere/' + BUNDLE_NAME),
            'a later launch of another candidate': lambda r: r.launch_record('launch-record-2.json', candidate_key='0000000000-000000000000'),
            'launch before identification': lambda r: r.launch_record(made_at='2026-11-12T00:00:00Z'),
            'package copy holds a link': lambda r: os.symlink('WORKFLOW.md', self.selected(r) / 'package' / 'LINK.md'),
        }
        for name, change in cases.items():
            with self.subTest(name):
                self.assertEqual(self.outcome(self.fresh(), change)[0], 'blocked', name)

    def test_a_workflow_of_another_origin_is_blocked(self):
        r = Root(tempfile.mkdtemp(dir=self.tmp.name))
        lines = frame_lines(origin='project', source_root='invented project')
        text = f"{lines['start_line']}\n{lines['proposal_line']}\n{lines['begin_marker']}\n{WORKFLOW}\n{lines['end_marker']}"
        r.turn('turn-1', 'completed', text=text, brief=BRIEF)
        r.run_text_record(text=text, lines=lines,
                          workflow={'kind': 'workflow', 'origin': 'project', 'source_root': 'invented project', 'name': NAME,
                                    'revision': REVISION, 'revision_method': PACKAGE_METHOD})
        self.assertEqual(self.outcome(r), ('blocked', 'only a bundled workflow is compared: its own bytes are tied to the candidate'))

    def test_another_full_revision_source_or_method_fails(self):
        changed = {'revision': REVISION[:12] + 'f' * 52, 'source_root': 'invented-other-root', 'revision_method': 'invented-method'}
        for field, value in changed.items():
            with self.subTest(field):
                r = Root(tempfile.mkdtemp(dir=self.tmp.name))
                identity = {'kind': 'workflow', 'origin': 'bundled', 'source_root': RELEASE_SUBJECT, 'name': NAME, 'revision': REVISION,
                            'revision_method': PACKAGE_METHOD, field: value}
                lines = frame_lines(revision=identity['revision'], source_root=identity['source_root'])
                text = f"{lines['start_line']}\n{lines['proposal_line']}\n{lines['begin_marker']}\n{WORKFLOW}\n{lines['end_marker']}"
                r.turn('turn-1', 'completed', text=text, brief=BRIEF)
                r.run_text_record(text=text, lines=lines, workflow=identity)
                self.assertEqual(self.outcome(r), ('failed', "the App's run names another source or revision of this workflow than "
                                                             "the candidate's bundled manifest"))

    def test_bytes_sent_other_than_the_candidates_fail(self):
        """The App's record and Codex agree on bytes that are not the candidate's
        own WORKFLOW.md of that revision."""
        r = Root(tempfile.mkdtemp(dir=self.tmp.name))
        other = '# Invented workflow\nSay goodbye.\n'
        r.turn('turn-1', 'completed', text=run_text(other), brief=BRIEF)
        r.run_text_record(body=other)
        self.assertEqual(self.outcome(r), ('failed', "the bytes between the markers are not the candidate's own WORKFLOW.md bytes"))

    # B: no event line is a copy.
    def test_every_other_marked_line_blocks(self):
        for payload in ({'type': 'user_message', 'message': run_text()}, {'type': 'agent_message', 'message': run_text()},
                        {'type': 'item_completed', 'turn_id': 'turn-1', 'thread_id': THREAD, 'item': {'content': [{'text': run_text()}]}},
                        {'type': 'unknown_event', run_text(): 'a key'}):
            with self.subTest(payload['type']):
                r = self.fresh()
                r.codex('event_msg', payload)
                self.assertEqual(self.outcome(r)[1], OTHER_LINE)

    # C: strict reading.
    def test_a_key_named_twice_blocks(self):
        def app(r):
            path = start_file(r)
            path.write_text(path.read_text().replace('"run": "run-1"', '"run": "competing", "run": "run-1"', 1))
        self.assertEqual(self.outcome(before=app)[0], 'blocked')
        def supplier(r):
            (path,) = r.root.rglob(f'rollout-*-{THREAD}.jsonl')
            path.write_text(path.read_text().replace('"content": [', '"content": [], "content": [', 1))
        r = self.fresh()
        r.write()
        supplier(r)
        with contextlib.redirect_stdout(io.StringIO()):
            lines = r.compare(r.view({'turn-1': 'completed'}))
        self.assertEqual({x['outcome'] for x in rows(lines)}, {'blocked'}, 'a session line naming a key twice is not read')

    def test_an_envelope_or_body_not_as_published_blocks(self):
        def envelope_change(change):
            def apply(r):
                path = start_file(r)
                value = json.loads(path.read_text())
                change(value)
                path.write_text(json.dumps(value))
            return apply
        cases = {'no writer': envelope_change(lambda v: v.pop('writer')), 'version true': envelope_change(lambda v: v.update(version=True)),
                 'another field': envelope_change(lambda v: v.update(other='x')),
                 'basis not record ids': envelope_change(lambda v: v.update(basis_records=['x']))}
        for field in ('selection', 'framing', 'holding_library', 'chain', 'origin_of_start', 'text_bytes'):
            cases['no ' + field] = envelope_change(lambda v, f=field: v['body'].pop(f))
        for field in ('kind', 'source_root', 'revision_method'):
            cases['no workflow ' + field] = envelope_change(lambda v, f=field: v['body']['workflow'].pop(f))
        cases['run other than its start line'] = envelope_change(lambda v: v['body'].update(run='run-2'))
        cases['origin other than its lines'] = envelope_change(lambda v: v['body']['workflow'].update(origin='user'))
        cases['files line with no other files'] = envelope_change(lambda v: v['body']['lines'].update(files_line='[Chirality] x'))
        for name, change in cases.items():
            with self.subTest(name):
                self.assertEqual(self.outcome(self.fresh(), change)[0], 'blocked', name)

    def test_a_record_that_may_name_the_thread_is_read_before_it_is_set_aside(self):
        for extra in ({}, {'record_kind': 'run_text', 'purpose': 'run start', 'run': 'second'},
                      {'record_kind': 'run_text', 'purpose': 'run start', 'conversation': [THREAD], 'run': 'second'},
                      {'record_kind': ['run_text'], 'purpose': 'run start', 'conversation': THREAD, 'run': 'second'},
                      {'record_kind': 'run_text', 'purpose': 'run end notice', 'conversation': THREAD, 'run': RUN}):
            with self.subTest(extra=extra):
                r = self.fresh()
                r.records.append(extra)
                self.assertEqual(self.outcome(r)[0], 'blocked')

    def test_a_message_whose_turn_or_elements_are_not_readable_blocks(self):
        def message(change):
            def apply(r):
                change(r.lines[1]['payload'])
            return apply
        cases = {'no turn metadata': lambda p: p.pop('internal_chat_message_metadata_passthrough'),
                 'a turn with no turn events': lambda p: p['internal_chat_message_metadata_passthrough'].update(turn_id='turn-9'),
                 'an element not an object': lambda p: p['content'].append(42),
                 'an element of another type': lambda p: p['content'].append({'type': 'input_image', 'image_url': 'x'}),
                 'an element with another field': lambda p: p['content'][1].update(other='x')}
        for name, change in cases.items():
            with self.subTest(name):
                r = Root(tempfile.mkdtemp(dir=self.tmp.name))
                r.turn('turn-1', 'completed', text=run_text(), brief=BRIEF)
                r.run_text_record()
                change(r.lines[1]['payload'])
                self.assertEqual(self.outcome(r)[0], 'blocked', name)

    # D: every record folder read whole, no link followed, no alias opened.
    def test_a_record_folder_reached_by_a_link_blocks(self):
        def linked_folder(r):
            outside = Path(self.tmp.name) / 'outside-workflow'
            outside.mkdir(exist_ok=True)
            key, value = envelope(9, {**r.records[0], 'run': 'second'})
            (outside / f'{key}.json').write_text(json.dumps(value))
            (r.data / 'records' / 'projects' / 'k2').mkdir()
            os.symlink(outside, r.data / 'records' / 'projects' / 'k2' / 'workflow')
        def linked_records(r):
            (r.root / 'project' / '.chirality').mkdir()
            os.symlink(r.data / 'records', r.root / 'project' / '.chirality' / 'records')
        for name, change in (('workflow folder', linked_folder), ('records folder', linked_records)):
            with self.subTest(name):
                self.assertEqual(self.outcome(self.fresh(), change)[0], 'blocked')

    def test_an_alias_in_a_record_folder_is_refused_before_it_is_opened(self):
        opened = []
        original = compare.os.open
        def tracking(path, *args, **kwargs):
            opened.append(os.fsdecode(path))
            return original(path, *args, **kwargs)
        def link(r):
            sentinel = r.root / 'project' / 'notes.txt'
            sentinel.write_text('INVENTED SENTINEL, not a record')
            os.symlink(sentinel, r.data / 'records' / 'projects' / 'k' / 'workflow' / '00000000-0000-4000-8000-000000000008.json')
        def hard(r):
            sentinel = r.root / 'project' / 'notes.txt'
            sentinel.write_text('INVENTED SENTINEL, not a record')
            os.link(sentinel, r.data / 'records' / 'projects' / 'k' / 'workflow' / '00000000-0000-4000-8000-000000000008.json')
        for name, change in (('symbolic link', link), ('hard link', hard)):
            with self.subTest(name):
                opened.clear()
                compare.os.open = tracking
                try:
                    self.assertEqual(self.outcome(self.fresh(), change)[0], 'blocked')
                finally:
                    compare.os.open = original
                self.assertNotIn('00000000-0000-4000-8000-000000000008.json', opened, 'the alias was opened')

    def test_anything_but_published_records_in_a_record_folder_blocks(self):
        folder = lambda r: r.data / 'records' / 'projects' / 'k' / 'workflow'
        for name, change in (('staging file', lambda r: (folder(r) / '.pending-0001').write_text('{}')),
                             ('subfolder', lambda r: (folder(r) / 'nested').mkdir()),
                             ('other file', lambda r: (folder(r) / 'notes.txt').write_text('x'))):
            with self.subTest(name):
                self.assertEqual(self.outcome(self.fresh(), change)[0], 'blocked')

    # E: W1 asked for by name always has its row.
    def test_w1_asked_for_by_name_is_planned(self):
        r = Root(tempfile.mkdtemp(dir=self.tmp.name))
        r.turn('turn-1', 'completed')
        r.write()
        view = r.view({'turn-1': 'completed'})
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(compare.main(['compare', '--root', str(r.root), '--thread', THREAD, '--view', view, '--comparison', 'W1']), 0)
        (out,) = (r.root / 'record').glob('session-comparison-2*.jsonl')
        lines = [json.loads(l) for l in out.read_text().splitlines()]
        (w1,) = rows(lines, 'W1')
        self.assertEqual((w1['outcome'], w1['codex']['messagesWithWorkflowMarkers'], w1['app']['runRecords']), ('blocked', 0, 0))
        self.assertEqual(lines[-1]['summary']['W1'], {'blocked': 1})

    # The representation rule.
    def test_any_other_mention_of_the_markers_blocks_whatever_surrounds_it(self):
        deep = run_text()
        for _ in range(20):
            deep = deep.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        r = self.fresh()
        r.codex('event_msg', {'type': 'user_message', 'message': deep})
        self.assertEqual(self.outcome(r)[1], OTHER_LINE)
        body = WORKFLOW + '&lt;&lt;&lt;chirality-workflow second@abcdef begin&gt;&gt;&gt;\n'
        r = Root(tempfile.mkdtemp(dir=self.tmp.name))
        r.turn('turn-1', 'completed', text=run_text(body), brief=BRIEF)
        r.run_text_record(body=body)
        self.assertEqual(self.outcome(r), ('blocked', ONE_PAIR))


MULTI = {'WORKFLOW.md': WORKFLOW.encode(), 'helpers/notes.md': b'invented helper\n', 'a.txt': b'invented a\n'}


class ThirdW1Reading(unittest.TestCase):
    """The second reading's findings, under Agent 0's narrowing: one run record
    in the whole root, the files frame from the candidate's own package, the
    records store only where the App places it, and W1's plan kept across the
    screen list."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def root(self, package=PACKAGE, record_files=True, text_files=True, label=FOLDER_LABEL, others=None):
        r = Root(tempfile.mkdtemp(dir=self.tmp.name), package=package)
        revision = package_revision(package)
        line = files_line(package)
        if line and label != FOLDER_LABEL:
            line = line.replace(f'"{FOLDER_LABEL}"', f'"{label}"')
        lines = frame_lines(revision=revision)
        text = run_text(package['WORKFLOW.md'].decode(), revision=revision, files=line if text_files else None)
        r.turn('turn-1', 'completed', text=text, brief=BRIEF)
        changes = {'workflow': {'kind': 'workflow', 'origin': 'bundled', 'source_root': RELEASE_SUBJECT, 'name': NAME, 'revision': revision,
                                'revision_method': PACKAGE_METHOD}}
        listed = [{'path': p_, 'sha256': hashlib.sha256(b).hexdigest()} for p_, b in sorted(package.items(), key=lambda i: i[0].encode())
                  if p_ != 'WORKFLOW.md'] if others is None else others
        if record_files and line:
            lines['files_line'] = line
        if record_files and listed:
            changes['other_files'] = listed
        r.run_text_record(body=package['WORKFLOW.md'].decode(), text=text, lines=lines, **changes)
        return r

    def outcome(self, r, before=None, *extra):
        r.write()
        if before:
            before(r)
        argv = ['compare', '--root', str(r.root), '--thread', THREAD, '--view', r.view({'turn-1': 'completed'}), *extra]
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            compare.main(argv)
        out = max((r.root / 'record').glob('session-comparison-2*.jsonl'))
        lines = [json.loads(l) for l in out.read_text().splitlines()]
        for secret in ('Say hello', BRIEF, 'invented helper', 'INVENTED SENTINEL'):
            self.assertNotIn(secret, out.read_text())
        found = rows(lines, 'W1')
        return (found[0]['outcome'], found[0]['reason']) if found else ('no row', None)

    # 1. One run record in the whole root.
    def test_another_record_that_may_be_of_a_run_blocks(self):
        for body in ({'record_kind': 'unknown', 'conversation': THREAD}, {'record_kind': 'supply_check'},
                     {'record_kind': 'selection_record', 'conversation': THREAD}):
            with self.subTest(body=body):
                r = self.root()
                r.records.append(body)
                self.assertEqual(self.outcome(r)[0], 'blocked')

    # 2. The files frame from the candidate's package.
    def test_a_package_with_other_files_passes_with_its_files_line(self):
        self.assertEqual(self.outcome(self.root(MULTI))[0], 'passed')

    def test_a_files_frame_not_the_packages_fails(self):
        wrong = [{'path': 'a.txt', 'sha256': 'f' * 64}, {'path': 'helpers/notes.md', 'sha256': hashlib.sha256(b'invented helper\n').hexdigest()}]
        for name, kwargs in (('omitted from record and text', {'record_files': False, 'text_files': False}),
                             ('a digest not the package\'s', {'others': wrong})):
            with self.subTest(name):
                self.assertEqual(self.outcome(self.root(MULTI, **kwargs)),
                                 ('failed', "the run's other files and files line are not the ones the candidate's package makes"))

    def test_other_files_where_the_package_has_none_fail(self):
        r = self.root(PACKAGE, others=[{'path': 'extra.md', 'sha256': 'a' * 64}])
        self.assertEqual(self.outcome(r)[0], 'failed')

    def test_a_folder_label_the_composer_never_writes_is_blocked(self):
        for label in ('/absolute/folder', '../outside', 'a/./b', '~'):
            with self.subTest(label=label):
                self.assertEqual(self.outcome(self.root(MULTI, label=label))[0], 'blocked')

    # 3. The records store only where the App places it for this route.
    def test_records_outside_the_store_are_not_read(self):
        opened = []
        original = compare.os.open
        def tracking(path, *args, **kwargs):
            opened.append(os.fsdecode(path))
            return original(path, *args, **kwargs)
        def elsewhere(r):
            store = r.data / 'records' / 'projects' / 'k' / 'workflow'
            moved = r.data / 'examples' / 'records' / 'workflow'
            moved.parent.mkdir(parents=True)
            store.rename(moved)
            notes = r.root / 'project' / 'examples' / 'records' / 'workflow'
            notes.mkdir(parents=True)
            (notes / '00000000-0000-4000-8000-000000000077.json').write_text('INVENTED SENTINEL, plain project notes')
        compare.os.open = tracking
        try:
            self.assertEqual(self.outcome(self.root(), elsewhere), ('blocked', 'the examination root holds more than the one run this comparison covers, or none'))
        finally:
            compare.os.open = original
        self.assertFalse([o for o in opened if o.endswith('.json') and 'launch-record' not in o and 'kept' not in o
                          and o not in ('reference.json', 'candidate-identification.json', 'bundle-inventory.json', 'MANIFEST.json')], opened)

    def test_a_placement_not_established_blocks(self):
        def chosen(r):
            (r.data / 'records-store.json').write_text(json.dumps({'location': '/invented/elsewhere'}))
        def in_place(r):
            (r.root / 'project' / '.chirality' / 'records').mkdir(parents=True)
        def linked_ancestor(r):
            library = r.root / 'home' / 'Library'
            library.rename(r.root / 'library-moved')
            os.symlink(r.root / 'library-moved', library)
        def linked_project(r):
            os.symlink(r.root / 'project' / 'notes.txt', r.root / 'project' / '.chirality')
            (r.root / 'project' / 'notes.txt').write_text('INVENTED SENTINEL, plain project notes')
        def development_build(r):
            path = r.root / 'record' / 'selected-workflow' / 'identification' / 'candidate-identification.json'
            record = json.loads(path.read_text())
            record['build']['features'] = []
            path.write_text(json.dumps(record))
        def two_identifiers(r):
            r.launch_record('launch-record-2.json', identifier='dev.chirality.app-v4.candidate.other')
        for name, change in (('a chosen store', chosen), ('records in place in the project', in_place), ('a link on the way', linked_ancestor),
                             ('a link in the project', linked_project), ('a development build', development_build),
                             ('launch records naming two candidates', two_identifiers)):
            with self.subTest(name):
                self.assertEqual(self.outcome(self.root(), change)[0], 'blocked', name)
        self.assertEqual(self.outcome(self.root(), two_identifiers),
                         ('blocked', 'the launch records of the root do not name one bundle identifier'))

    # 4. W1's plan kept across the screen list.
    def two_step(self, r, *first):
        r.write()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(compare.main(['compare', '--root', str(r.root), '--thread', THREAD, *first]), 0)
            (screen,) = (r.root / 'record').glob('screen-list-*.jsonl')
            self.assertEqual(compare.main(['answers', '--root', str(r.root), '--screen', str(screen)]), 0)
        (out,) = (r.root / 'record').glob('session-comparison-2*.jsonl')
        lines = [json.loads(l) for l in out.read_text().splitlines()]
        return json.loads(screen.read_text().splitlines()[0]), lines

    def test_w1_asked_for_on_the_list_keeps_its_row_in_the_answers(self):
        r = Root(tempfile.mkdtemp(dir=self.tmp.name))
        r.turn('turn-1', 'completed')
        head, lines = self.two_step(r, '--comparison', 'W1')
        self.assertEqual(head['planned'], ['C2', 'C3', 'C4', 'W1'])
        self.assertEqual([x['outcome'] for x in rows(lines, 'W1')], ['blocked'])
        self.assertEqual(lines[-1]['summary']['W1'], {'blocked': 1})

    def test_without_asking_and_without_a_run_there_is_still_no_row(self):
        r = Root(tempfile.mkdtemp(dir=self.tmp.name))
        r.turn('turn-1', 'completed')
        head, lines = self.two_step(r)
        self.assertEqual(head['planned'], ['C2', 'C3', 'C4'])
        self.assertEqual(rows(lines, 'W1'), [])

    def test_the_plan_never_makes_a_pass_the_records_do(self):
        r = self.root()
        head, lines = self.two_step(r, '--comparison', 'W1')
        self.assertEqual([x['outcome'] for x in rows(lines, 'W1')], ['passed'], 'derived from the records')
        r = self.root()
        r.selected = False
        head, lines = self.two_step(r, '--comparison', 'W1')
        self.assertEqual([x['outcome'] for x in rows(lines, 'W1')], ['blocked'])


class FourthReading(unittest.TestCase):
    """The scoped reading after round 3: each of its three findings as a case."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = Root(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_answers_are_refused_once_a_saved_view_exists(self):
        self.r.turn('turn-1', 'completed')
        self.r.compare(candidate=True)
        (screen,) = (self.r.root / 'record').glob('screen-list-*.jsonl')
        lines = screen.read_text().splitlines()
        answered = [lines[0]] + [json.dumps({**json.loads(l), 'answer': 'passed', 'note': 'seen'}) for l in lines[1:]]
        screen.write_text('\n'.join(answered) + '\n')
        self.r.view({'turn-1': 'interrupted'})
        self.assertEqual(compare.main(['answers', '--root', str(self.r.root), '--screen', str(screen)]), 1)
        (out,) = (self.r.root / 'record').glob('session-comparison-2*.jsonl')
        self.assertNotIn('passed', {r['outcome'] for r in rows([json.loads(l) for l in out.read_text().splitlines()])})

    def test_json_escaped_workflow_markers_still_give_the_w1_row(self):
        self.r.turn('turn-1', 'completed')
        self.r.write()
        (path,) = self.r.root.rglob(f'rollout-*-{THREAD}.jsonl')
        line = json.dumps({'timestamp': 't', 'type': 'response_item', 'payload': {'type': 'message', 'role': 'user',
                           'content': [{'type': 'input_text', 'text': run_text()}]}}).replace('<', '\\u003c')
        self.assertNotIn('<<<', line)
        path.write_text(path.read_text() + line + '\n')
        lines = self.r.compare(self.r.view({'turn-1': 'completed'}))
        (w1,) = rows(lines, 'W1')
        self.assertEqual((w1['outcome'], w1['codex']['linesWithWorkflowMarkers'], w1['app']['runRecords']), ('blocked', 1, 0))

    def test_a_header_that_cannot_be_read_still_ends_with_blocked_rows(self):
        self.r.turn('turn-1', 'completed')
        self.r.write()
        original = compare.tool_digest
        compare.tool_digest = lambda: (_ for _ in ()).throw(OSError('invented'))
        try:
            self.assertEqual(compare.main(['compare', '--root', str(self.r.root), '--thread', THREAD, '--view', self.r.view({})]), 1)
        finally:
            compare.tool_digest = original
        (out,) = (self.r.root / 'record').glob('session-comparison-2*.jsonl')
        lines = [json.loads(l) for l in out.read_text().splitlines()]
        self.assertIsNone(lines[0]['tool_sha256'])
        self.assertEqual(lines[0]['workflow_scope'], compare.WORKFLOW_SCOPE)
        self.assertEqual({r['outcome'] for r in rows(lines)}, {'blocked'})



class FifthReading(unittest.TestCase):
    """The focused reading after round 4: a refused answers run supersedes the
    list's earlier answers at the examination table, and a fallback says so."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = Root(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def table_passes(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'standalone'))
        try:
            import table
        finally:
            sys.path.pop(0)
        text = '\n'.join(table.comparisons([self.r.root / 'record']))
        return [l for l in text.splitlines() if l.startswith('| ') and '| C3 |' in l]

    def test_a_refused_answers_run_leaves_no_earlier_pass_counted(self):
        self.r.turn('turn-1', 'completed')
        self.r.compare(candidate=True)
        (screen,) = (self.r.root / 'record').glob('screen-list-*.jsonl')
        lines = screen.read_text().splitlines()
        screen.write_text('\n'.join([lines[0]] + [json.dumps({**json.loads(l), 'answer': 'passed', 'note': 'seen'}) for l in lines[1:]]) + '\n')
        self.assertEqual(compare.main(['answers', '--root', str(self.r.root), '--screen', str(screen)]), 0)
        passed = lambda row: int(row.split('| C3 |')[1].split('|')[0])  # the first outcome column is passed
        (first,) = self.table_passes()
        self.assertEqual(passed(first), 1, first)
        # A saved view now shows the turn otherwise; the answers are revised and run again, later.
        self.r.view({'turn-1': 'interrupted'})
        time.sleep(1.1)
        screen.write_text('\n'.join([lines[0]] + [json.dumps({**json.loads(l), 'answer': 'failed', 'note': 'seen'}) for l in lines[1:]]) + '\n')
        self.assertEqual(compare.main(['answers', '--root', str(self.r.root), '--screen', str(screen)]), 1)
        refused = max((self.r.root / 'record').glob('session-comparison-2*.jsonl'))
        head = json.loads(refused.read_text().splitlines()[0])
        self.assertEqual((head['fallback'], head['answers_of']), (True, screen.name))
        (row,) = self.table_passes()
        self.assertEqual(passed(row), 0, f'the earlier operator pass is still counted: {row}')

    def test_a_fallback_header_says_it_is_one(self):
        self.r.turn('turn-1', 'completed')
        self.r.write()
        self.assertEqual(compare.main(['compare', '--root', str(self.r.root), '--thread', THREAD, '--view', '/nonexistent/host-status-x.json']), 0)
        original = compare.compare_views
        compare.compare_views = lambda *a: (_ for _ in ()).throw(RuntimeError('invented'))
        try:
            self.assertEqual(compare.main(['compare', '--root', str(self.r.root), '--thread', THREAD, '--view', self.r.view({})]), 1)
        finally:
            compare.compare_views = original
        heads = [json.loads(p.read_text().splitlines()[0]) for p in (self.r.root / 'record').glob('session-comparison-2*.jsonl')]
        self.assertEqual(sorted(h.get('fallback', False) for h in heads), [False, True])


if __name__ == '__main__':
    unittest.main()
