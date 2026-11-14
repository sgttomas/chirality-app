"""Session comparison, first part, on invented sessions: each case is one
invented session file with the App's account of the same session, agreeing or
disagreeing in one named way. Nothing here is a real session."""
import hashlib
import json
import os
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compare  # noqa: E402

THREAD = '019a0000-0000-7000-8000-00000000000a'
WORKFLOW = '# Invented workflow\nSay hello.\n'
REVISION = 'abcdef0123456789' * 4


def run_text(body=WORKFLOW):
    return ('[Chirality] Workflow run start: invented.\n[Chirality] When you judge this workflow finished, end the message.\n'
            f'<<<chirality-workflow invented-workflow@{REVISION[:12]} begin>>>\n{body}\n'
            f'<<<chirality-workflow invented-workflow@{REVISION[:12]} end>>>')


class Root:
    """An invented examination root with the App's account and Codex's record."""

    def __init__(self, base):
        self.root = Path(base) / 'launch-20261114T000000Z-0000'
        (self.root / 'record').mkdir(parents=True)
        (self.root / 'project').mkdir()
        self.data = self.root / 'home' / 'Library' / 'Application Support' / 'invented.app.key'
        (self.data / 'runtime').mkdir(parents=True)
        (self.root / 'record' / 'launch-record.json').write_text(json.dumps({'candidate_key': 'invented-key'}))
        self.lines, self.stops, self.records, self.session = [], [], [], True
        self.manifest = {'packages': [{'name': 'invented-workflow', 'revision': REVISION,
                                       'files': [{'path': 'WORKFLOW.md', 'sha256': hashlib.sha256(WORKFLOW.encode()).hexdigest()}]}]}

    def codex(self, kind, payload):
        self.lines.append({'timestamp': '2026-11-14T00:00:00Z', 'type': kind, 'payload': payload})

    def turn(self, turn, end=None, text='hello', **fields):
        self.codex('event_msg', {'type': 'task_started', 'turn_id': turn})
        self.codex('response_item', {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': text}]})
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
        sessions = self.data / 'account-homes' / 'h' / 'sessions' / '2026' / '11' / '14'
        sessions.mkdir(parents=True)
        target = sessions / f'rollout-2026-11-14T00-00-00-{THREAD}.jsonl' if self.session else os.devnull
        with open(target, 'w') as f:
            for line in [{'timestamp': 't', 'type': 'session_meta', 'payload': {'id': THREAD}}] + self.lines:
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
            (workflow / f'{i}.json').write_text(json.dumps(record))
        manifest = Path(self.root.parent) / 'MANIFEST.json'
        manifest.write_text(json.dumps(self.manifest))
        return str(manifest)

    def run_text_record(self, body=WORKFLOW):
        self.records.append({'record_kind': 'run_text', 'run': 'run-1', 'conversation': THREAD,
                             'workflow': {'name': 'invented-workflow', 'revision': REVISION},
                             'workflow_file': {'path': 'WORKFLOW.md', 'content': {
                                 'method': 'chirality.app.exact-bytes.sha256/v1', 'value': hashlib.sha256(body.encode()).hexdigest()}}})

    def compare(self, *views):
        manifest = self.write()
        argv = ['compare', '--root', str(self.root), '--thread', THREAD, '--manifest', manifest]
        for v in views:
            argv += ['--view', v]
        assert compare.main(argv) == 0
        out = sorted((self.root / 'record').glob('session-comparison-2*.jsonl'))
        lines = [json.loads(l) for l in out[-1].read_text().splitlines()]
        return lines


def rows(lines, comparison=None):
    return [l for l in lines if 'comparison' in l and (comparison is None or l['comparison'] == comparison)]


class SessionComparison(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = Root(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_an_agreeing_session_passes_every_comparison(self):
        self.r.turn('turn-1', 'completed', text=run_text())
        self.r.turn('turn-2', 'interrupted')
        self.r.stop('turn-2', 'interrupted')
        self.r.run_text_record()
        lines = self.r.compare(self.r.view({'turn-1': 'completed', 'turn-2': 'interrupted'}))
        self.assertEqual(lines[0], {'header': True, 'candidate_key': 'invented-key', 'examination_root': str(self.r.root.resolve()), 'tool': compare.TOOL})
        self.assertEqual({r['outcome'] for r in rows(lines)}, {'passed'}, rows(lines))
        self.assertEqual([r['comparison'] for r in rows(lines)], ['C2', 'C3', 'C2', 'C3', 'C4', 'W1'])
        self.assertEqual(lines[-1], {'summary': {'C2': {'passed': 2}, 'C3': {'passed': 2}, 'C4': {'passed': 1}, 'W1': {'passed': 1}}})
        self.assertNotIn('Say hello', json.dumps(lines), 'no session content leaves the record')

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

    def test_workflow_bytes_changed_by_one_byte_fail(self):
        self.r.turn('turn-1', 'completed', text=run_text(WORKFLOW.replace('hello', 'hellp')))
        self.r.run_text_record()
        (w1,) = rows(self.r.compare(), 'W1')
        self.assertEqual(w1['outcome'], 'failed')
        self.assertIn('bundled', w1['reason'])
        self.assertIn('run_text', w1['reason'])
        self.assertEqual(w1['codex']['line'], 3, 'the line of the session file, not its text')

    def test_no_session_file_blocks_every_comparison(self):
        self.r.session = False
        lines = self.r.compare()
        self.assertEqual({r['outcome'] for r in rows(lines)}, {'blocked'})

    def test_a_candidate_gets_the_screen_list_and_the_operators_answers_become_rows(self):
        self.r.turn('turn-1', 'interrupted')
        self.r.turn('turn-2')
        self.r.compare()
        (screen,) = (self.r.root / 'record').glob('session-comparison-screen-*.jsonl')
        items = [json.loads(l) for l in screen.read_text().splitlines()]
        self.assertTrue(items[0]['header'])
        self.assertEqual([i['screen_must_say'] for i in items[1:]],
                         ['the turn is shown, and shown as interrupted', 'the turn is shown, and shown as not known (the turn has no reported end)'])
        items[1]['answer'], items[1]['note'] = 'passed', 'shown interrupted'
        screen.write_text('\n'.join(json.dumps(i) for i in items) + '\n')
        for old in (self.r.root / 'record').glob('session-comparison-2*.jsonl'):
            old.unlink()
        self.assertEqual(compare.main(['answers', '--root', str(self.r.root), '--screen', str(screen)]), 0)
        (out,) = (self.r.root / 'record').glob('session-comparison-2*.jsonl')
        answered = rows([json.loads(l) for l in out.read_text().splitlines()])
        self.assertEqual([r['outcome'] for r in answered], ['passed', 'not run'])


class TheRealFormat(unittest.TestCase):
    """An invented session laid out as the 0.167.0 file is: an ordinal on each
    line, a developer message and other user-role messages beside the
    person's, item_completed lines, no `error` key on a clean end or an abort,
    and an error object on a failed turn."""

    def test_turns_and_the_workflow_read_from_the_pins_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / f'rollout-2026-11-14T06-11-12-{THREAD}.jsonl'
            msg = lambda role, text, turn, kind: {'type': 'message', 'id': 'msg_x', 'role': role, 'content': [{'type': 'input_text', 'text': text}],
                                                 'internal_chat_message_metadata_passthrough': {'turn_id': turn, 'content_item_kinds': [kind]}}
            lines = [
                ('session_meta', {'id': THREAD, 'base_instructions': {'text': 'invented'}}),
                ('event_msg', {'type': 'task_started', 'turn_id': 'A', 'root_turn_id': 'A', 'started_at': 1}),
                ('response_item', msg('developer', 'Invented role guidance.', 'A', 'developer.instructions')),
                ('response_item', msg('user', '<environment_context>invented</environment_context>', 'A', 'environments.environment_context')),
                ('world_state', {}),
                ('turn_context', {'turn_id': 'A', 'cwd': '/invented'}),
                ('response_item', msg('user', run_text(), 'A', 'user.text')),
                ('event_msg', {'type': 'item_completed', 'turn_id': 'A', 'item': {'type': 'UserMessage', 'id': 'other-id', 'client_id': 'c', 'content': [{'type': 'text', 'text': run_text()}]}}),
                ('event_msg', {'type': 'task_complete', 'turn_id': 'A', 'root_turn_id': 'A', 'last_agent_message': 'hi'}),
                ('event_msg', {'type': 'task_started', 'turn_id': 'B'}),
                ('response_item', msg('user', '<turn_aborted>invented</turn_aborted>', 'B', 'generic.turn_aborted')),
                ('event_msg', {'type': 'turn_aborted', 'turn_id': 'B', 'reason': 'interrupted'}),
                ('event_msg', {'type': 'task_started', 'turn_id': 'C'}),
                ('event_msg', {'type': 'task_complete', 'turn_id': 'C', 'last_agent_message': None, 'error': {'message': 'invented', 'codex_error_info': 'other'}}),
            ]
            path.write_text(''.join(json.dumps({'timestamp': 't', 'ordinal': n, 'type': k, 'payload': p}) + '\n' for n, (k, p) in enumerate(lines)))
            session = compare.read_session(path)
            self.assertEqual([(t, compare.codex_status(session['turns'][t])) for t in session['order']],
                             [('A', 'completed'), ('B', 'interrupted'), ('C', 'failed')])
            self.assertEqual(session['turns']['B']['end']['reason'], 'interrupted')
            r = Root(tmp)
            r.lines = [{'timestamp': 't', 'type': k, 'payload': p} for k, p in lines[1:]]
            r.run_text_record()
            (w1,) = rows(r.compare(), 'W1')
            self.assertEqual((w1['outcome'], w1['codex']['line']), ('passed', 7), 'found in the person\'s message, not the others')


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


if __name__ == '__main__':
    unittest.main()
