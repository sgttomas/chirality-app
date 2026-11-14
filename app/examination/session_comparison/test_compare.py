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

    def codex(self, kind, payload):
        self.lines.append({'timestamp': '2026-11-14T00:00:00Z', 'type': kind, 'payload': payload})

    def message(self, turn, text, kind='user.text'):
        self.codex('response_item', {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': text}],
                                     'internal_chat_message_metadata_passthrough': {'turn_id': turn, 'content_item_kinds': [kind],
                                                                                    'provenance': {'type': 'user' if kind == 'user.text' else 'harness'}}})

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
        if getattr(self, 'written', False):
            return
        self.written = True
        sessions = self.data / 'account-homes' / 'h' / 'sessions' / '2026' / '11' / '14'
        sessions.mkdir(parents=True)
        target = sessions / f'rollout-2026-11-14T00-00-00-{THREAD}.jsonl' if self.session else os.devnull
        with open(target, 'w') as f:
            for line in [{'timestamp': 't', 'type': 'session_meta', 'payload': {'id': THREAD, 'cli_version': '0.167.0'}}] + self.lines:
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

    def run_text_record(self, body=WORKFLOW, text=None, run='run-1'):
        text = run_text(body) if text is None else text
        self.records.append({'record_kind': 'run_text', 'run': run, 'conversation': THREAD,
                             'text_identity': {'method': 'chirality.app.exact-bytes.sha256/v1', 'value': hashlib.sha256(text.encode()).hexdigest()},
                             'workflow': {'name': 'invented-workflow', 'revision': REVISION},
                             'workflow_file': {'path': 'WORKFLOW.md', 'content': {
                                 'method': 'chirality.app.exact-bytes.sha256/v1', 'value': hashlib.sha256(body.encode()).hexdigest()}}})

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
        self.assertEqual({r['outcome'] for r in rows(lines) if r['comparison'] != 'W1'}, {'passed'}, rows(lines))
        self.assertEqual([r['comparison'] for r in rows(lines)], ['C2', 'C3', 'C2', 'C3', 'C4', 'W1'])
        (w1,) = rows(lines, 'W1')
        self.assertEqual((w1['outcome'], w1['reason']), ('blocked', compare.NOT_AVAILABLE))
        self.assertNotIn('byte', json.dumps(lines).lower(), 'nothing says the workflow reached Codex byte for byte')
        self.assertEqual(len(lines[0]['tool_sha256']), 64)
        self.assertEqual(lines[-1], {'summary': {'C2': {'passed': 2}, 'C3': {'passed': 2}, 'C4': {'passed': 1}, 'W1': {'blocked': 1}},
                                     'unrecognised': 0, 'compares': compare.COMPARES, 'workflow_comparison': compare.NOT_AVAILABLE})
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
            self.assertEqual(lines[0]['pinned_codex'], '0.167.0')

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
    """An invented session laid out as the 0.167.0 file is: an ordinal on each
    line, a developer message and other user-role messages beside the
    person's, item_completed lines, no `error` key on a clean end or an abort,
    and an error object on a failed turn."""

    def test_turns_and_the_workflow_read_from_the_pins_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / f'rollout-2026-11-14T06-11-12-{THREAD}.jsonl'
            msg = lambda role, text, turn, kind: {'type': 'message', 'id': 'msg_x', 'role': role, 'content': [{'type': 'input_text', 'text': text}],
                                                 'internal_chat_message_metadata_passthrough': {'turn_id': turn, 'content_item_kinds': [kind],
                                                                                               'provenance': {'type': 'user' if kind == 'user.text' else 'harness'}}}
            lines = [
                ('session_meta', {'id': THREAD, 'cli_version': '0.167.0', 'base_instructions': {'text': 'invented'}}),
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
            session = compare.parse_session(path.read_bytes(), THREAD)
            self.assertEqual([(t, session['turns'][t]['says']) for t in session['order']],
                             [('A', 'completed'), ('B', 'interrupted'), ('C', 'failed')])
            self.assertEqual(session['turns']['B']['reason'], 'interrupted')



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



class TheWorkflowComparisonIsNotAvailable(unittest.TestCase):
    """W1 is not in this version. Where it would be made the tool says it was
    not: a blocked row, never passed and never left out, and every statement
    of what is compared names exactly three comparisons."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = Root(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def stated(self, line):
        self.assertEqual(line['compares'], {'C2': 'turns', 'C3': 'outcomes', 'C4': 'interrupts'})
        self.assertEqual(line['workflow_comparison'], compare.NOT_AVAILABLE)

    def test_workflow_markers_in_a_message_give_one_blocked_row(self):
        self.r.turn('turn-1', 'completed', text=run_text())
        lines = self.r.compare(self.r.view({'turn-1': 'completed'}))
        (w1,) = rows(lines, 'W1')
        self.assertEqual((w1['outcome'], w1['reason']), ('blocked', compare.NOT_AVAILABLE))
        self.assertEqual(w1['codex'], {'linesWithWorkflowMarkers': 1})
        self.stated(lines[0])
        self.stated(lines[-1])
        self.assertEqual(lines[-1]['summary']['W1'], {'blocked': 1})

    def test_a_run_text_record_alone_gives_one_blocked_row(self):
        self.r.turn('turn-1', 'completed')
        self.r.run_text_record()
        (w1,) = rows(self.r.compare(self.r.view({'turn-1': 'completed'})), 'W1')
        self.assertEqual((w1['outcome'], w1['app']['runTextRecords']), ('blocked', 1))

    def test_an_unreadable_workflow_record_gives_one_blocked_row(self):
        self.r.turn('turn-1', 'completed')
        self.r.write()
        (self.r.data / 'records' / 'projects' / 'k' / 'workflow' / 'bad.json').write_text('{')
        (w1,) = rows(self.r.compare(self.r.view({'turn-1': 'completed'})), 'W1')
        self.assertEqual((w1['outcome'], w1['app']['unreadableWorkflowRecords']), ('blocked', 1))

    def test_with_no_workflow_run_there_is_no_row_and_the_statement_stands(self):
        self.r.turn('turn-1', 'completed')
        lines = self.r.compare(self.r.view({'turn-1': 'completed'}))
        self.assertEqual(rows(lines, 'W1'), [])
        self.stated(lines[0])
        self.stated(lines[-1])

    def test_asking_for_it_by_name_is_refused_with_the_sentence_and_writes_nothing(self):
        self.r.turn('turn-1', 'completed', text=run_text())
        self.r.write()
        for name in ('W1', 'w1', 'workflow', 'Workflow'):
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = compare.main(['compare', '--root', str(self.r.root), '--thread', THREAD, '--comparison', name])
            self.assertEqual(code, 2)
            self.assertIn(compare.NOT_AVAILABLE, err.getvalue())
        self.assertEqual(list((self.r.root / 'record').glob('s*-2*.jsonl')), [])
        self.assertEqual(compare.main(['compare', '--root', str(self.r.root), '--thread', THREAD, '--comparison', 'C9']), 2)

    def test_the_screen_list_and_the_answers_say_it(self):
        self.r.turn('turn-1', 'completed', text=run_text())
        self.r.compare(candidate=True)
        (screen,) = (self.r.root / 'record').glob('screen-list-*.jsonl')
        head = json.loads(screen.read_text().splitlines()[0])
        self.stated(head)
        self.assertFalse(any('W1' in json.dumps(json.loads(l)) for l in screen.read_text().splitlines()[1:]))
        self.assertEqual(compare.main(['answers', '--root', str(self.r.root), '--screen', str(screen)]), 0)
        (out,) = (self.r.root / 'record').glob('session-comparison-2*.jsonl')
        lines = [json.loads(l) for l in out.read_text().splitlines()]
        self.assertEqual([r['outcome'] for r in rows(lines, 'W1')], ['blocked'])
        self.stated(lines[0])
        self.stated(lines[-1])

    def test_a_blocked_session_carries_the_row_and_the_statement(self):
        self.r.session = False
        self.r.turn('turn-1', 'completed', text=run_text())
        lines = self.r.compare(self.r.view({'turn-1': 'completed'}))
        self.assertEqual({(r['comparison'], r['outcome']) for r in rows(lines)},
                         {('C2', 'blocked'), ('C3', 'blocked'), ('C4', 'blocked'), ('W1', 'blocked')})
        self.stated(lines[-1])

    def test_the_fallback_carries_the_statement(self):
        self.r.turn('turn-1', 'completed')
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

    def test_no_output_says_passed_for_w1(self):
        with self.assertRaises(AssertionError):
            compare.row('W1', {'thread': THREAD}, {}, {}, 'passed', 'x')


if __name__ == '__main__':
    unittest.main()
