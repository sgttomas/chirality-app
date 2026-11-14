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

    def message(self, turn, text, kind='user.text'):
        self.codex('response_item', {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': text}],
                                     'internal_chat_message_metadata_passthrough': {'turn_id': turn, 'content_item_kinds': [kind]}})

    def turn(self, turn, end=None, text='hello', **fields):
        self.codex('event_msg', {'type': 'task_started', 'turn_id': turn})
        self.message(turn, text)
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
        manifest = Path(self.root.parent) / 'MANIFEST.json'
        if getattr(self, 'written', False):
            return str(manifest)
        self.written = True
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

    def run_text_record(self, body=WORKFLOW, text=None, run='run-1'):
        text = run_text(body) if text is None else text
        self.records.append({'record_kind': 'run_text', 'run': run, 'conversation': THREAD,
                             'text_identity': {'method': 'chirality.app.exact-bytes.sha256/v1', 'value': hashlib.sha256(text.encode()).hexdigest()},
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
        self.assertEqual({k: lines[0][k] for k in ('header', 'candidate_key', 'examination_root', 'tool')},
                         {'header': True, 'candidate_key': 'invented-key', 'examination_root': str(self.r.root.resolve()), 'tool': compare.TOOL})
        self.assertEqual({r['outcome'] for r in rows(lines)}, {'passed'}, rows(lines))
        self.assertEqual([r['comparison'] for r in rows(lines)], ['C2', 'C3', 'C2', 'C3', 'C4', 'W1'])
        self.assertEqual(len(lines[0]['tool_sha256']), 64)
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
        (screen,) = (self.r.root / 'record').glob('screen-list-*.jsonl')
        items = [json.loads(l) for l in screen.read_text().splitlines()]
        self.assertTrue(items[0]['header'])
        self.assertEqual([i['screen_must_say'] for i in items[1:]],
                         ['the turn is shown, and shown as interrupted', 'the turn is shown, and shown as not known (the turn has no reported end)',
                          'the screen shows no turn of this thread other than these: turn-1, turn-2'])
        items[1]['answer'], items[1]['note'] = 'passed', 'shown interrupted'
        items[3]['answer'] = 'passed'
        screen.write_text('\n'.join(json.dumps(i) for i in items) + '\n')
        for old in (self.r.root / 'record').glob('session-comparison-2*.jsonl'):
            old.unlink()
        self.assertEqual(compare.main(['answers', '--root', str(self.r.root), '--screen', str(screen)]), 0)
        (out,) = (self.r.root / 'record').glob('session-comparison-2*.jsonl')
        lines = [json.loads(l) for l in out.read_text().splitlines()]
        self.assertEqual(lines[0]['answers_of'], screen.name, 'the table counts only the latest answers file of one screen list')
        self.assertEqual([r['outcome'] for r in rows(lines)], ['passed', 'not run', 'not run'], 'a passed with no note is not run')
        self.assertNotIn('shown interrupted', json.dumps(lines), 'a note is carried as its digest only')


class NoFalsePass(unittest.TestCase):
    """The first independent reading's findings: each way it found to a false
    passed, or a row gone missing, now reported otherwise."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = Root(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_1_each_run_is_compared_with_its_own_message(self):
        second = WORKFLOW.replace('hello', 'hellp')
        self.r.turn('turn-1', 'completed', text=run_text())
        self.r.turn('turn-2', 'completed', text=run_text(second) + ' ')
        self.r.run_text_record(run='run-1')
        self.r.run_text_record(text=run_text(second) + ' ', run='run-2')
        w1 = rows(self.r.compare(), 'W1')
        self.assertEqual([(r['subject']['run'], r['outcome']) for r in w1], [('run-1', 'passed'), ('run-2', 'failed')])

    def test_1_a_run_whose_text_codex_did_not_record_is_blocked(self):
        self.r.turn('turn-1', 'completed', text='no workflow here')
        self.r.run_text_record()
        (w1,) = rows(self.r.compare(), 'W1')
        self.assertEqual(w1['outcome'], 'blocked')

    def test_2_harness_messages_never_stand_for_the_persons_input(self):
        self.r.codex('event_msg', {'type': 'task_started', 'turn_id': 'turn-1'})
        self.r.message('turn-1', run_text(), kind='environments.environment_context')
        self.r.message('turn-1', run_text(), kind='generic.turn_aborted')
        self.r.message('turn-1', run_text(WORKFLOW.replace('hello', 'hellp')))
        self.r.run_text_record()
        (w1,) = rows(self.r.compare(), 'W1')
        self.assertEqual(w1['outcome'], 'failed', "only the person's message counts, and its bytes differ")
        self.assertEqual(w1['codex']['line'], 5, "the person's message, not a harness message")

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
        self.r.compare()
        (screen,) = (self.r.root / 'record').glob('screen-list-*.jsonl')
        self.assertIn('no turn of this thread other than these: turn-1', screen.read_text())

    def test_5_answers_are_bound_to_the_list_and_the_record(self):
        self.r.turn('turn-1', 'completed')
        self.r.compare()
        (screen,) = (self.r.root / 'record').glob('screen-list-*.jsonl')
        original = screen.read_text()
        def answer(edit):
            items = [json.loads(l) for l in original.splitlines()]
            edit(items)
            screen.write_text('\n'.join(json.dumps(i) for i in items) + '\n')
            return compare.main(['answers', '--root', str(self.r.root), '--screen', str(screen)])
        def must(items): items[1]['screen_must_say'] = 'anything'; items[1]['answer'] = 'passed'; items[1]['note'] = 'x'
        def subject(items): items[1]['subject'] = {'thread': THREAD, 'turn': 'turn-9'}; items[1]['answer'] = 'passed'; items[1]['note'] = 'x'
        def added(items): items.append({**items[1], 'screen_must_say': 'invented', 'answer': 'passed', 'note': 'x'})
        def root(items): items[0]['candidate_key'] = 'another'
        for edit in (must, subject, added, root):
            self.assertEqual(answer(edit), 2, edit.__name__)
        def removed(items): del items[1:]
        self.assertEqual(answer(removed), 0)
        (out,) = [p for p in (self.r.root / 'record').glob('session-comparison-*.jsonl') if 'answers_of' in p.read_text()]
        self.assertEqual({r['outcome'] for r in rows([json.loads(l) for l in out.read_text().splitlines()])}, {'not run'}, 'deleted items are not run, not gone')
        for path in self.r.root.rglob(f'rollout-*-{THREAD}.jsonl'):
            path.write_text(path.read_text() + '\n')
        self.assertEqual(answer(lambda items: None), 2, 'the session file changed since the list was written')

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
        manifest = self.r.write()
        for path in self.r.root.rglob(f'rollout-*-{THREAD}.jsonl'):
            lines = path.read_text().splitlines()
            lines[0] = json.dumps({'timestamp': 't', 'type': 'session_meta', 'payload': {'id': 'another-thread'}})
            path.write_text('\n'.join(lines) + '\n')
        compare.main(['compare', '--root', str(self.r.root), '--thread', THREAD, '--manifest', manifest])
        (out,) = (self.r.root / 'record').glob('session-comparison-2*.jsonl')
        self.assertEqual({r['outcome'] for r in rows([json.loads(l) for l in out.read_text().splitlines()])}, {'blocked'})

    def test_12_an_unreadable_workflow_record_is_blocked_and_an_unrecorded_workflow_inconclusive(self):
        self.r.turn('turn-1', 'completed', text=run_text())
        manifest = self.r.write()
        (self.r.data / 'records' / 'projects' / 'k' / 'workflow' / 'bad.json').write_text('{')
        compare.main(['compare', '--root', str(self.r.root), '--thread', THREAD, '--manifest', manifest])
        (out,) = (self.r.root / 'record').glob('session-comparison-2*.jsonl')
        w1 = rows([json.loads(l) for l in out.read_text().splitlines()], 'W1')
        self.assertEqual(sorted(r['outcome'] for r in w1), ['blocked', 'inconclusive'])

    def test_13_every_planned_comparison_yields_a_row(self):
        lines = self.r.compare(self.r.view({}))
        self.assertEqual(sorted({r['comparison'] for r in rows(lines)}), ['C2', 'C3', 'C4', 'W1'])
        self.assertEqual({r['outcome'] for r in rows(lines)}, {'not run'})

    def test_14_unreadable_inputs_give_blocked_rows_not_a_crash(self):
        self.r.codex('event_msg', {'type': 'task_started', 'turn_id': 'turn-1'})
        manifest = self.r.write()
        for path in self.r.root.rglob(f'rollout-*-{THREAD}.jsonl'):
            path.write_text(path.read_text() + '[]\n')
        Path(manifest).write_text('{')
        self.assertEqual(compare.main(['compare', '--root', str(self.r.root), '--thread', THREAD, '--manifest', manifest]), 0)
        (out,) = (self.r.root / 'record').glob('session-comparison-2*.jsonl')
        lines = [json.loads(l) for l in out.read_text().splitlines()]
        self.assertEqual({r['outcome'] for r in rows(lines)}, {'blocked'})
        self.assertIn('summary', lines[-1])


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
            session = compare.read_session(path, THREAD)
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
