#!/usr/bin/env python3
"""The examination table (app/examination/standalone/table.py) on invented step maps, results and rows.

Each test makes its own folders; nothing is read from a real run.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

APP = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('table', APP / 'examination/standalone/table.py')
table = importlib.util.module_from_spec(spec)
spec.loader.exec_module(table)

STEP_MAP = {'scenarios': {
    'S-A': [{'step': 'A-1', 'counts': True}, {'step': 'A-2', 'counts': True}, {'step': 'A-2R', 'counts': False}],
    'S-B': [{'step': 'B-1', 'counts': True}, {'step': 'B-2', 'counts': True}, {'step': 'B-3', 'counts': True}],
}, 'stimuli': []}


class Fixture(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__('shutil').rmtree(self.root, True))

    def repo(self, out_of_release=None):
        repo = self.root / 'repo'
        (repo / 'app/examination/sq_receiving').mkdir(parents=True, exist_ok=True)
        content = dict(STEP_MAP, **({'out_of_release': out_of_release} if out_of_release else {}))
        (repo / table.STEP_MAP).write_text(json.dumps(content))
        return repo

    def results(self, *records):
        folder = self.root / 'results'
        folder.mkdir(exist_ok=True)
        for n, record in enumerate(records):
            (folder / f'r{n}.json').write_text(json.dumps(record))
        return folder

    def rows(self, name, lines, folder=None):
        folder = folder or self.root / 'record'
        folder.mkdir(exist_ok=True)
        (folder / name).write_text(''.join(json.dumps(line) + '\n' for line in lines))
        return folder

    def printed(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(table.main(list(argv)), 0)
        return out.getvalue()


class Steps(Fixture):
    def row(self, text, step):
        return next(line for line in text.splitlines() if f'| {step} |' in line)

    def test_a_step_out_of_the_release_names_the_decision_and_the_others_stay_planned(self):
        repo = self.repo({'S-B': {'steps': ['B-2'], 'release': '4.0.0', 'decided': '2026-11-14', 'by': 'the owner',
                                  'steps_by': 'App Agent 0', 'stated_in': 'docs/X.md'}})
        text = self.printed('--repo', str(repo), '--candidate', 'c')
        self.assertIn("out of 4.0.0 by the owner's decision of 2026-11-14; steps as read by App Agent 0 (docs/X.md)",
                      self.row(text, 'B-2'))
        self.assertIn('not run (no record)', self.row(text, 'B-1'))
        self.assertIn('not run (no record)', self.row(text, 'B-3'))
        self.assertIn('Counted steps in the release: 0 passed, 0 failed, 0 blocked, 4 not run, 0 inconclusive. '
                      'Steps out of 4.0.0 by a recorded decision: 1.', text)

    def test_an_entry_without_steps_takes_the_whole_scenario_and_without_steps_by_names_only_the_decision(self):
        repo = self.repo({'S-B': {'release': '4.0.0', 'decided': '2026-11-14', 'by': 'the owner', 'stated_in': 'docs/X.md'}})
        text = self.printed('--repo', str(repo), '--candidate', 'c')
        for step in ('B-1', 'B-2', 'B-3'):
            self.assertIn("out of 4.0.0 by the owner's decision of 2026-11-14 (docs/X.md)", self.row(text, step))
        self.assertIn('Steps out of 4.0.0 by a recorded decision: 3.', text)

    def test_a_decision_for_another_release_takes_nothing_out(self):
        repo = self.repo({'S-B': {'steps': ['B-2'], 'release': '4.1.0', 'decided': 'x', 'by': 'y', 'stated_in': 'z'}})
        self.assertIn('not run (no record)', self.row(self.printed('--repo', str(repo), '--candidate', 'c'), 'B-2'))

    def test_an_entry_naming_a_step_the_scenario_lacks_stops_the_print(self):
        repo = self.repo({'S-B': {'steps': ['B-9'], 'release': '4.0.0', 'decided': 'x', 'by': 'y', 'stated_in': 'z'}})
        with self.assertRaises(SystemExit) as stopped:
            table.main(['--repo', str(repo), '--candidate', 'c'])
        self.assertIn('B-9', str(stopped.exception))

    def test_the_latest_record_of_a_step_is_shown_and_counted_and_an_unknown_outcome_stops_the_print(self):
        repo = self.repo()
        results = self.results({'step': 'A-1', 'candidate': 'c1', 'date': '2026-11-13', 'outcome': 'failed'},
                               {'step': 'A-1', 'candidate': 'c2', 'date': '2026-11-14', 'outcome': 'passed', 'operated_by': 'agent'},
                               {'step': 'A-2R', 'candidate': 'c2', 'date': '2026-11-14', 'outcome': 'failed'})
        text = self.printed('--repo', str(repo), '--results', str(results), '--candidate', 'c2')
        self.assertIn('| passed | 2026-11-14 | agent |', self.row(text, 'A-1'))
        self.assertIn('1 passed, 0 failed, 0 blocked, 4 not run', text)  # A-2R does not count, nor the other candidate's
        self.results({'step': 'A-2', 'candidate': 'c', 'date': 'd', 'outcome': 'shown'})
        with self.assertRaises(SystemExit):
            table.main(['--repo', str(repo), '--results', str(results), '--candidate', 'c2'])

    def test_a_passed_step_citing_a_row_not_passed_or_a_changed_file_is_named(self):
        repo = self.repo()
        results = self.results()
        rows = results / 'rows.jsonl'
        rows.write_text(json.dumps({'comparison': 'C3', 'outcome': 'failed'}) + '\n')
        digest = 'sha256:' + hashlib.sha256(rows.read_bytes()).hexdigest()
        self.results({'step': 'A-1', 'candidate': 'c', 'date': 'd', 'outcome': 'passed',
                      'cites': [{'file': 'rows.jsonl', 'sha256': digest, 'rows': [1]}]},
                     {'step': 'A-2', 'candidate': 'c', 'date': 'd', 'outcome': 'passed',
                      'cites': [{'file': 'rows.jsonl', 'sha256': 'sha256:' + '0' * 64, 'rows': [1]}]})
        text = self.printed('--repo', str(repo), '--results', str(results), '--candidate', 'c')
        self.assertIn('A-1: disagrees with the rows it cites', text)
        self.assertIn('A-2: citation unsupported (rows.jsonl missing or changed)', text)
        self.assertIn('| recorded passed; not counted (its citations do not support it) |', self.row(text, 'A-1'))
        self.assertIn('0 passed, 0 failed, 0 blocked, 3 not run, 0 inconclusive, 2 recorded passed but not supported', text)


class TheClaim(Fixture):
    """A step prints as passed only when a record for it, on the candidate named, says passed; missing, changed or
    contradictory evidence is named and never improves an outcome."""

    def row(self, text, step):
        return next(line for line in text.splitlines() if f'| {step} |' in line)

    def test_records_for_another_candidate_or_none_never_pass_for_the_one_named(self):
        repo = self.repo()
        results = self.results({'step': 'A-1', 'candidate': 'other', 'date': 'd', 'outcome': 'passed'},
                               {'step': 'A-2', 'candidate': None, 'date': 'd', 'outcome': 'passed'},
                               {'step': 'B-1', 'candidate': '', 'date': 'd', 'outcome': 'passed'},
                               {'step': 'B-2', 'date': 'd', 'outcome': 'passed'})
        text = self.printed('--repo', str(repo), '--results', str(results), '--candidate', 'c')
        self.assertIn('0 passed', text)
        self.assertIn('not run (no record)', self.row(text, 'A-1'))
        self.assertIn('Records for another candidate, or naming none (not counted for c): r0.json (other), '
                      'r1.json (no candidate), r2.json (no candidate), r3.json (no candidate)', text)

    def test_records_of_the_same_date_that_disagree_are_inconclusive_whatever_their_names(self):
        repo = self.repo()
        results = self.results({'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'failed'},
                               {'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'passed'})
        text = self.printed('--repo', str(repo), '--results', str(results), '--candidate', 'c')
        self.assertIn('| inconclusive (records disagree) |', self.row(text, 'A-1'))
        self.assertIn('0 passed, 0 failed, 0 blocked, 4 not run, 1 inconclusive', text)
        self.assertIn('A-1: records of the same date disagree (r0.json failed, r1.json passed)', text)

    def test_the_later_date_decides_not_the_later_name(self):
        repo = self.repo()
        results = self.results({'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'failed'},
                               {'step': 'A-1', 'candidate': 'c', 'date': '2026-11-13', 'outcome': 'passed'})
        self.assertIn('| failed | 2026-11-14 |', self.row(self.printed('--repo', str(repo), '--results', str(results),
                                                                        '--candidate', 'c'), 'A-1'))

    def test_a_results_folder_that_is_missing_stops_and_an_unreadable_record_is_named(self):
        with self.assertRaises(SystemExit):
            table.main(['--repo', str(self.repo()), '--results', str(self.root / 'absent'), '--candidate', 'c'])
        results = self.results({'step': 'A-1', 'candidate': 'c', 'date': 'd', 'outcome': 'passed'})
        (results / 'broken.json').write_text('{ not json')
        text = self.printed('--repo', str(self.repo()), '--results', str(results), '--candidate', 'c')
        self.assertIn('Records that could not be read (not counted): broken.json (JSONDecodeError)', text)
        self.assertIn('1 passed', text)

    def test_a_comparison_whose_header_and_launch_record_disagree_is_not_counted(self):
        folder = self.rows('session-comparison-20261114T080000Z-00000001.jsonl', [
            {'header': True, 'candidate_key': 'B'}, {'comparison': 'C2', 'outcome': 'passed'}])
        (folder / 'launch-record-1.json').write_text(json.dumps({'bundle': {'identifier': 'dev.chirality.app-v4.candidate.A'}}))
        text = self.printed('--repo', str(self.repo()), '--candidate', 'c', '--comparisons', str(folder))
        section = text[text.index('SESSION COMPARISON'):]
        self.assertNotIn('| B | C2 |', section)
        self.assertIn('its header names candidate B and the launch record A; its rows are not counted', section)

    def test_a_w1_row_that_is_not_blocked_beside_a_withheld_header_is_not_counted(self):
        sentence = 'the workflow comparison is not available in this version'
        folder = self.rows('session-comparison-20261114T080000Z-00000001.jsonl', [
            {'header': True, 'candidate_key': 'k1', 'workflow_comparison': sentence}, {'comparison': 'W1', 'outcome': 'passed'}])
        text = self.printed('--repo', str(self.repo()), '--candidate', 'c', '--comparisons', str(folder))
        section = text[text.index('SESSION COMPARISON'):]
        self.assertNotIn('| k1 | W1 |', section)
        self.assertIn('a W1 row says passed although the header says the workflow comparison is not available', section)


class Comparisons(Fixture):
    def section(self, folder):
        text = self.printed('--repo', str(self.repo()), '--candidate', 'c', '--comparisons', str(folder))
        return text[text.index('SESSION COMPARISON'):]

    def test_rows_are_counted_by_candidate_comparison_and_outcome_and_the_summary_is_only_compared(self):
        folder = self.rows('session-comparison-20261114T080000Z-00000001.jsonl', [
            {'header': True, 'candidate_key': 'k1'}, {'comparison': 'C2', 'outcome': 'passed'},
            {'comparison': 'C3', 'outcome': 'inconclusive'}, {'comparison': 'C3', 'outcome': 'blocked'},
            {'summary': {'C2': {'passed': 1}, 'C3': {'inconclusive': 1, 'blocked': 1}}, 'unrecognised': 0}])
        self.rows('screen-list-20261114T080000Z-00000002.jsonl', [{'header': True}, {'screen_must_say': 'x'}], folder)
        section = self.section(folder)
        self.assertIn('| k1 | C2 | 1 | 0 | 0 | 0 | 0 |', section)
        self.assertIn('| k1 | C3 | 0 | 0 | 1 | 0 | 1 |', section)  # inconclusive and blocked never folded into passed
        self.assertNotIn('differs', section)
        self.assertNotIn('screen-list', section)

    def test_a_summary_that_disagrees_and_unrecognised_rows_are_noted(self):
        folder = self.rows('session-comparison-20261114T080000Z-00000001.jsonl', [
            {'header': True, 'candidate_key': 'k1'}, {'comparison': 'C4', 'outcome': 'failed'},
            {'summary': {'C4': {'passed': 1}}, 'unrecognised': 1}])
        section = self.section(folder)
        self.assertIn('| k1 | C4 | 0 | 1 | 0 | 0 | 0 |', section)
        self.assertIn('its summary line differs from its rows; the rows are counted', section)
        self.assertIn('1 rows name a value the tool did not recognise', section)

    def test_the_candidate_comes_from_the_launch_record_when_the_header_has_none(self):
        folder = self.rows('session-comparison-20261114T080000Z-00000001.jsonl', [
            {'header': True}, {'comparison': 'C2', 'outcome': 'passed'}])
        (folder / 'launch-record-1.json').write_text(json.dumps({'bundle': {'identifier': 'dev.chirality.app-v4.candidate.k9'}}))
        self.assertIn('| k9 | C2 |', self.section(folder))

    def test_of_the_answers_from_one_screen_list_only_the_latest_counts(self):
        head = {'header': True, 'candidate_key': 'k1', 'answers_of': 'screen-list-x.jsonl'}
        folder = self.rows('session-comparison-20261114T080000Z-aaaaaaaa.jsonl',
                           [head, {'comparison': 'C2', 'outcome': 'failed'}])
        self.rows('session-comparison-20261114T080500Z-bbbbbbbb.jsonl', [head, {'comparison': 'C2', 'outcome': 'passed'}], folder)
        section = self.section(folder)
        self.assertIn('| k1 | C2 | 1 | 0 | 0 | 0 | 0 |', section)
        self.assertIn('session-comparison-20261114T080000Z-aaaaaaaa.jsonl: replaced by', section)

    def test_answers_of_the_same_second_count_for_neither_unless_written_at_orders_them(self):
        head = {'header': True, 'candidate_key': 'k1', 'answers_of': 'screen-list-x.jsonl'}
        folder = self.rows('session-comparison-20261114T080000Z-aaaaaaaa.jsonl', [head, {'comparison': 'C2', 'outcome': 'failed'}])
        self.rows('session-comparison-20261114T080000Z-bbbbbbbb.jsonl', [head, {'comparison': 'C2', 'outcome': 'passed'}], folder)
        section = self.section(folder)
        self.assertNotIn('| k1 | C2 |', section)
        self.assertIn('which is later cannot be told, so none of them is counted', section)
        self.rows('session-comparison-20261114T080000Z-aaaaaaaa.jsonl',
                  [dict(head, written_at='2026-11-14T08:00:00.900000Z'), {'comparison': 'C2', 'outcome': 'failed'}], folder)
        self.rows('session-comparison-20261114T080000Z-bbbbbbbb.jsonl',
                  [dict(head, written_at='2026-11-14T08:00:00.100000Z'), {'comparison': 'C2', 'outcome': 'passed'}], folder)
        self.assertIn('| k1 | C2 | 0 | 1 | 0 | 0 | 0 |', self.section(folder))  # the later by written_at


class WorkflowWithheld(Fixture):
    def test_three_comparisons_passing_beside_a_blocked_w1_never_read_as_the_first_target_met(self):
        sentence = 'the workflow comparison is not available in this version'
        head = {'header': True, 'candidate_key': 'k1', 'workflow_comparison': sentence,
                'compares': {'C2': 'turns', 'C3': 'outcomes', 'C4': 'interrupts'}}
        folder = self.rows('session-comparison-20261114T080000Z-00000001.jsonl', [
            head, {'comparison': 'C2', 'outcome': 'passed'}, {'comparison': 'C3', 'outcome': 'passed'},
            {'comparison': 'C4', 'outcome': 'passed'}, {'comparison': 'W1', 'outcome': 'blocked', 'reason': sentence},
            {'summary': {'C2': {'passed': 1}, 'C3': {'passed': 1}, 'C4': {'passed': 1}, 'W1': {'blocked': 1}},
             'unrecognised': 0, 'workflow_comparison': sentence}])
        text = self.printed('--repo', str(self.repo()), '--candidate', 'c', '--comparisons', str(folder))
        section = text[text.index('SESSION COMPARISON'):]
        self.assertIn('| k1 | W1 | 0 | 0 | 1 | 0 | 0 |', section)
        self.assertIn(f'W1, the workflow comparison: "{sentence}". It is counted only as blocked. C2, C3 and C4 passing do not meet '
                      'the first target', section)
        self.assertNotIn('differs', section)

    def test_no_sentence_when_no_header_says_the_workflow_comparison_is_withheld(self):
        folder = self.rows('session-comparison-20261114T080000Z-00000001.jsonl', [
            {'header': True, 'candidate_key': 'k1'}, {'comparison': 'C2', 'outcome': 'passed'}])
        text = self.printed('--repo', str(self.repo()), '--candidate', 'c', '--comparisons', str(folder))
        self.assertNotIn('W1, the workflow comparison', text)


class Driver(Fixture):
    def test_each_run_and_its_setup_report_are_listed_apart(self):
        run = self.root / 'run'
        run.mkdir()
        (run / 'report.json').write_text(json.dumps({'result': 'shown'}))
        (run / 'scenario-report.json').write_text(json.dumps({'scenario': 'first', 'version': 2, 'verdict': 'pass',
                                                              'outcomes': {'O': 'shown'}}))
        (run / 'setup-report.json').write_text(json.dumps({'scenario': 'setup', 'version': 1, 'verdict': 'pass',
                                                           'launches': [{'id': 'L1', 'verdict': 'pass'}]}))
        text = self.printed('--repo', str(self.repo()), '--candidate', 'c', '--driver', f'{run}=123@abcdef1234567890')
        self.assertIn('THE SCRIPTED DRIVER (development evidence on a test build; it satisfies no step above)', text)
        self.assertIn('| 123 | abcdef123456 | first (v2) | pass | shown | O: shown |', text)
        self.assertIn('| 123 | abcdef123456 | setup (v1) | pass | shown | L1: pass |', text)


if __name__ == '__main__':
    unittest.main()
