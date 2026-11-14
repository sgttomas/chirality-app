#!/usr/bin/env python3
"""The examination table (app/examination/standalone/table.py) on invented step maps, results and rows.

Each test makes its own folders; nothing is read from a real run.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
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
        self.results({'step': 'A-2', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'shown'})
        with self.assertRaises(SystemExit):
            table.main(['--repo', str(repo), '--results', str(results), '--candidate', 'c2'])

    def test_cited_rows_are_listed_as_cited_and_never_change_an_outcome(self):
        repo = self.repo()
        results = self.results()
        rows = results / 'rows.jsonl'
        rows.write_text(json.dumps({'header': True, 'candidate_key': 'c'}) + '\n'
                        + json.dumps({'comparison': 'C3', 'outcome': 'failed'}) + '\n')
        digest = 'sha256:' + hashlib.sha256(rows.read_bytes()).hexdigest()
        self.results({'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'passed',
                      'cites': [{'file': 'rows.jsonl', 'sha256': digest, 'rows': [2, 9]}]},
                     {'step': 'A-2', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'passed',
                      'cites': [{'file': 'rows.jsonl', 'sha256': 'sha256:' + '0' * 64, 'rows': [2]}]},
                     {'step': 'B-1', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'failed',
                      'cites': [{'file': 'absent.jsonl', 'sha256': digest, 'rows': [1]}, 'not a citation']})
        text = self.printed('--repo', str(repo), '--results', str(results), '--candidate', 'c')
        self.assertIn('| passed | 2026-11-14 |', self.row(text, 'A-1'))
        self.assertIn('| passed | 2026-11-14 |', self.row(text, 'A-2'))
        self.assertIn('| failed | 2026-11-14 |', self.row(text, 'B-1'))
        self.assertIn('Counted steps in the release: 2 passed, 1 failed, 0 blocked, 2 not run, 0 inconclusive.', text)
        listing = text[text.index('Cited rows, listed as cited'):]
        self.assertIn("they never raise, lower or protect a step's outcome or any count", listing)
        self.assertIn('- A-1 (r0.json) cites rows.jsonl: exists; unchanged; row 2: failed, row 9: no such row', listing)
        self.assertIn('- A-2 (r1.json) cites rows.jsonl: exists; not the file cited (digest differs); row 2: failed', listing)
        self.assertIn('- B-1 (r2.json) cites absent.jsonl: does not exist; unchanged: not known; row 1: no such row', listing)
        self.assertIn('- B-1 (r2.json) cites a citation not of the form {file, sha256, rows}: "not a citation"', listing)


class TheClaim(Fixture):
    """App Agent 0's claim: a step prints as passed only when a result record for it, on the candidate named, says
    passed, and no other record of the same latest date says otherwise; every other state prints as what it is."""

    def row(self, text, step):
        return next(line for line in text.splitlines() if f'| {step} |' in line)

    def test_records_for_another_candidate_or_none_never_pass_for_the_one_named(self):
        repo = self.repo()
        results = self.results({'step': 'A-1', 'candidate': 'other', 'date': '2026-11-14', 'outcome': 'passed'},
                               {'step': 'A-2', 'candidate': None, 'date': '2026-11-14', 'outcome': 'passed'},
                               {'step': 'B-1', 'candidate': '', 'date': '2026-11-14', 'outcome': 'passed'},
                               {'step': 'B-2', 'date': '2026-11-14', 'outcome': 'passed'})
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
        results = self.results({'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'passed'})
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


class TheClaimAgain(Fixture):
    """Citations are listed, never decided on; an empty candidate or an unreadable folder stops the print."""

    def cite(self, results, lines, rows):
        (results / 'rows').mkdir(exist_ok=True)
        path = results / 'rows/rows.jsonl'
        path.write_text(''.join(json.dumps(line) + '\n' for line in lines))
        return {'file': 'rows/rows.jsonl', 'sha256': 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest(), 'rows': rows}

    def test_an_empty_candidate_stops_the_print(self):
        results = self.results({'step': 'A-1', 'candidate': '', 'date': '2026-11-14', 'outcome': 'passed'})
        for empty in ('', '  '):
            with self.subTest(repr(empty)), self.assertRaises(SystemExit):
                table.main(['--repo', str(self.repo()), '--results', str(results), '--candidate', empty])

    def test_records_of_one_date_that_agree_pass_once_and_each_ones_citations_are_listed(self):
        results = self.results()
        self.results({'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'passed'},
                     {'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'passed',
                      'cites': [{'file': 'absent.jsonl', 'sha256': 'sha256:' + '0' * 64, 'rows': [1]}]})
        text = self.printed('--repo', str(self.repo()), '--results', str(results), '--candidate', 'c')
        self.assertIn('1 passed', text)
        self.assertIn('- A-1 (r1.json) cites absent.jsonl: does not exist', text)

    def test_citations_never_raise_lower_or_protect_an_outcome_or_a_count(self):
        results = self.results()
        passed = self.cite(results, [{'header': True, 'candidate_key': 'c'}, {'comparison': 'C2', 'outcome': 'passed'}], [2])
        failed = dict(self.cite(results, [{'header': True, 'candidate_key': 'other', 'workflow_comparison': 'not available'},
                                          {'comparison': 'W1', 'outcome': 'failed'}], [2]))
        records = [{'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'failed'},
                   {'step': 'A-2', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'passed'},
                   {'step': 'B-1', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'blocked'},
                   {'step': 'B-2', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'inconclusive'}]
        bare = self.printed('--repo', str(self.repo()), '--results', str(self.results(*records)), '--candidate', 'c')
        for record, cite in zip(records, (passed, failed, passed, passed)):
            record['cites'] = [cite]
        cited = self.printed('--repo', str(self.repo()), '--results', str(self.results(*records)), '--candidate', 'c')
        table_of = lambda text: text[:text.index('Cited rows') if 'Cited rows' in text else len(text)].rstrip()
        self.assertEqual(table_of(cited), table_of(bare))
        self.assertIn('Counted steps in the release: 1 passed, 1 failed, 1 blocked, 1 not run, 1 inconclusive.', bare)

    def test_a_disagreement_is_printed_directly_under_the_counts(self):
        results = self.results({'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'failed'},
                               {'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'passed'},
                               {'step': 'Z-9', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'passed'})
        lines = self.printed('--repo', str(self.repo()), '--results', str(results), '--candidate', 'c').splitlines()
        counts = next(n for n, line in enumerate(lines) if line.startswith('Counted steps in the release:'))
        self.assertEqual(lines[counts + 1], 'Records that disagree: A-1: records of the same date disagree '
                                            '(r0.json failed, r1.json passed); counted inconclusive')

    def test_an_unreadable_results_folder_stops_the_print(self):
        results = self.results()
        results.chmod(0)
        self.addCleanup(results.chmod, 0o700)
        if os.access(results, os.R_OK):
            self.skipTest('this user can read a folder without permission (root)')
        with self.assertRaises(SystemExit):
            table.main(['--repo', str(self.repo()), '--results', str(results), '--candidate', 'c'])

    def test_the_comparisons_standing_heads_its_section(self):
        folder = self.rows('session-comparison-20261114T080000Z-00000001.jsonl', [
            {'header': True, 'candidate_key': 'k1'}, {'comparison': 'C2', 'outcome': 'passed'}])
        text = self.printed('--repo', str(self.repo()), '--candidate', 'c', '--comparisons', str(folder),
                            '--comparison-standing', 'session comparison: a reading is still out')
        section = text[text.index('SESSION COMPARISON'):]
        self.assertIn('Standing: session comparison: a reading is still out', section.splitlines()[2])


class TheSecondReading(Fixture):
    """The first reading of the smaller claim found three ways its inputs could defeat it; each is repaired here with
    the reader's own input."""

    def row(self, text, step):
        return next(line for line in text.splitlines() if f'| {step} |' in line)

    def test_the_launchers_own_record_shape_is_read_and_the_table_still_prints(self):
        folder = self.rows('session-comparison-20261114T080000Z-aaaaaaaa.jsonl',
                           [{'header': True, 'candidate_key': 'c'}, {'comparison': 'C2', 'outcome': 'passed'}])
        (folder / 'launch-record.json').write_text(json.dumps(
            {'candidate_key': 'c', 'identifier': 'dev.chirality.app-v4.candidate.c', 'bundle': '/invented/Candidate.app'}))
        text = self.printed('--repo', str(self.repo()), '--candidate', 'c', '--comparisons', str(folder))
        self.assertIn('Counted steps in the release:', text)
        self.assertIn('| c | C2 | 1 | 0 | 0 | 0 | 0 |', text)

    def test_a_launch_record_naming_another_candidate_at_its_top_level_withholds_the_rows(self):
        folder = self.rows('session-comparison-20261114T080000Z-aaaaaaaa.jsonl',
                           [{'header': True, 'candidate_key': 'A'}, {'comparison': 'C2', 'outcome': 'passed'}])
        (folder / 'launch-record.json').write_text(json.dumps({'candidate_key': 'B', 'identifier': 'dev.chirality.app-v4.candidate.B'}))
        section = self.printed('--repo', str(self.repo()), '--candidate', 'c', '--comparisons', str(folder))
        self.assertNotIn('| A | C2 |', section)
        self.assertIn('its header names candidate A and the launch record B; its rows are not counted', section)

    def test_the_later_time_decides_whatever_its_zone_and_equal_times_disagree(self):
        results = self.results(
            {'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14T12:00:00+02:00', 'outcome': 'passed'},
            {'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14T11:00:00Z', 'outcome': 'failed'},
            {'step': 'A-2', 'candidate': 'c', 'date': '2026-11-14T10:00:00Z', 'outcome': 'passed'},
            {'step': 'A-2', 'candidate': 'c', 'date': '2026-11-14T10:00:00+00:00', 'outcome': 'failed'})
        text = self.printed('--repo', str(self.repo()), '--results', str(results), '--candidate', 'c')
        self.assertIn('| failed | 2026-11-14T11:00:00Z |', self.row(text, 'A-1'))
        self.assertIn('| inconclusive (records disagree) |', self.row(text, 'A-2'))
        self.assertIn('0 passed, 1 failed, 0 blocked, 3 not run, 1 inconclusive', text)

    def test_dates_that_cannot_be_placed_or_ordered_never_decide(self):
        results = self.results(
            {'step': 'A-1', 'candidate': 'c', 'date': '20261113', 'outcome': 'passed'},
            {'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'failed'},
            {'step': 'A-2', 'candidate': 'c', 'date': '2026-11-14T10:00:00', 'outcome': 'passed'},
            {'step': 'B-1', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'passed'},
            {'step': 'B-1', 'candidate': 'c', 'date': '2026-11-14T10:00:00Z', 'outcome': 'passed'})
        text = self.printed('--repo', str(self.repo()), '--results', str(results), '--candidate', 'c')
        self.assertIn('| failed | 2026-11-14 |', self.row(text, 'A-1'))
        self.assertIn('not run (no record)', self.row(text, 'A-2'))
        self.assertIn('| inconclusive (records disagree) |', self.row(text, 'B-1'))
        self.assertIn("r0.json (its date '20261113' is not a calendar date or a time with its zone)", text)
        self.assertIn("r2.json (its date '2026-11-14T10:00:00' is not a calendar date or a time with its zone)", text)
        self.assertIn('B-1: dates of different forms cannot be ordered', text)

    def test_no_citation_can_stop_the_print_or_change_what_is_above_its_listing(self):
        base = {'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'passed'}
        bare = self.printed('--repo', str(self.repo()), '--results', str(self.results(base)), '--candidate', 'c')
        outside = self.root / 'outside.jsonl'
        outside.write_text(json.dumps({'comparison': 'C2', 'outcome': 'failed'}) + '\n')
        for name, cites in (('not a list', 1), ('outside the folder', [{'file': '../outside.jsonl', 'sha256': 'x', 'rows': [1]}]),
                            ('an absolute path', [{'file': str(outside), 'sha256': 'x', 'rows': [1]}]),
                            ('a file that cannot be read', [{'file': 'rows.jsonl', 'sha256': 'sha256:' + '0' * 64, 'rows': [1]}])):
            with self.subTest(name):
                results = self.results(dict(base, cites=cites))
                locked = results / 'rows.jsonl'
                if locked.exists():
                    locked.chmod(0o600)
                locked.write_text(json.dumps({'comparison': 'C2', 'outcome': 'failed'}) + '\n')
                locked.chmod(0)
                self.addCleanup(locked.chmod, 0o600)
                text = self.printed('--repo', str(self.repo()), '--results', str(results), '--candidate', 'c')
                self.assertEqual(text[:text.index('Cited rows')].rstrip(), bare.rstrip())
                listing = text[text.index('Cited rows'):]
                expected = {'not a list': 'citations not given as a list: 1', 'outside the folder': 'outside the results folder; not read',
                            'an absolute path': 'outside the results folder; not read',
                            'a file that cannot be read': 'rows.jsonl: exists; cannot be read (PermissionError)'}[name]
                if name == 'a file that cannot be read' and os.access(locked, os.R_OK):
                    continue  # root reads a file without permission
                self.assertIn(expected, listing)

    def test_a_record_that_is_not_one_is_set_aside_and_bad_comparison_inputs_are_noted(self):
        results = self.results([], {'candidate': 'c', 'date': '2026-11-14', 'outcome': 'passed'},
                               {'step': 'A-1', 'candidate': 'c', 'outcome': 'passed'})
        folder = self.rows('session-comparison-20261114T080000Z-aaaaaaaa.jsonl', [])
        (folder / 'session-comparison-20261114T080000Z-aaaaaaaa.jsonl').write_text('{bad\n')
        self.rows('session-comparison-20261114T080000Z-bbbbbbbb.jsonl', [[]], folder)
        text = self.printed('--repo', str(self.repo()), '--results', str(results), '--candidate', 'c',
                            '--comparisons', str(folder), '--comparisons', str(self.root / 'absent'))
        self.assertIn('0 passed, 0 failed, 0 blocked, 5 not run', text)
        self.assertIn('r0.json (not a record)', text)
        self.assertIn('r1.json (names no step)', text)
        self.assertIn("r2.json (its date None is not a calendar date or a time with its zone)", text)
        self.assertIn('session-comparison-20261114T080000Z-aaaaaaaa.jsonl: cannot be read as one JSON object per line', text)
        self.assertIn('session-comparison-20261114T080000Z-bbbbbbbb.jsonl: cannot be read as one JSON object per line', text)
        self.assertIn(f"{self.root / 'absent'}: not a folder that can be read; nothing from it is counted", text)


class TheThirdReading(Fixture):
    """The second reading of the smaller claim found five more ways its inputs could defeat it; each is repaired here
    with the reader's own input."""

    def row(self, text, step):
        return [line for line in text.splitlines() if f'| {step} |' in line]

    def test_a_nul_in_a_citation_path_is_listed_and_the_table_prints(self):
        results = self.results({'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'passed',
                                'cites': [{'file': 'bad\u0000name', 'sha256': 'x', 'rows': [1]}]})
        text = self.printed('--repo', str(self.repo()), '--results', str(results), '--candidate', 'c')
        self.assertIn('1 passed', text)
        self.assertIn('not a path that can be read (ValueError)', text)

    def test_a_line_break_in_any_field_makes_no_row_of_its_own(self):
        results = self.results({'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'failed',
                                'operated_by': 'invented reader\n| S-A | A-2 | yes | passed | 2026-11-14 | invented reader |'})
        text = self.printed('--repo', str(self.repo()), '--results', str(results), '--candidate', 'c')
        self.assertEqual(len(self.row(text, 'A-2')), 1)
        self.assertIn('not run (no record)', self.row(text, 'A-2')[0])
        self.assertIn('invented reader\\n\\| S-A \\| A-2', self.row(text, 'A-1')[0])
        for line in text.splitlines():
            self.assertFalse(any(ch in line for ch in '\u2028\u2029\r'))

    def test_every_cited_row_is_listed(self):
        results = self.results()
        rows = results / 'rows.jsonl'
        rows.write_text(''.join(json.dumps({'comparison': 'C2', 'outcome': 'passed' if n < 50 else 'failed'}) + '\n' for n in range(51)))
        self.results({'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14', 'outcome': 'passed',
                      'cites': [{'file': 'rows.jsonl', 'sha256': 'x', 'rows': list(range(1, 52))}]})
        text = self.printed('--repo', str(self.repo()), '--results', str(results), '--candidate', 'c')
        self.assertIn('row 51: failed', text)

    def test_times_are_compared_to_the_precision_written_and_far_dates_do_not_stop_the_print(self):
        results = self.results(
            {'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14T10:00:00.0000001Z', 'outcome': 'passed'},
            {'step': 'A-1', 'candidate': 'c', 'date': '2026-11-14T10:00:00.0000002Z', 'outcome': 'failed'},
            {'step': 'A-2', 'candidate': 'c', 'date': '0001-01-01T00:00:00+01:00', 'outcome': 'passed'})
        text = self.printed('--repo', str(self.repo()), '--results', str(results), '--candidate', 'c')
        self.assertIn('| failed | 2026-11-14T10:00:00.0000002Z |', self.row(text, 'A-1')[0])
        self.assertIn('| passed | 0001-01-01T00:00:00+01:00 |', self.row(text, 'A-2')[0])
        self.assertIn('1 passed, 1 failed', text)

    def test_written_at_is_compared_as_an_instant_so_a_refused_run_replaces_earlier_answers(self):
        head = {'header': True, 'candidate_key': 'k1', 'answers_of': 'screen-list-x.jsonl'}
        folder = self.rows('session-comparison-20261114T080000Z-aaaaaaaa.jsonl',
                           [dict(head, written_at='2026-11-14T08:00:00Z'), {'comparison': 'C2', 'outcome': 'passed'}])
        self.rows('session-comparison-20261114T080000Z-bbbbbbbb.jsonl',
                  [{'header': True, 'candidate_key': None, 'fallback': True, 'answers_of': 'screen-list-x.jsonl',
                    'written_at': '2026-11-14T08:00:00.900000Z'}, {'comparison': 'C2', 'outcome': 'blocked'}], folder)
        section = self.printed('--repo', str(self.repo()), '--candidate', 'c', '--comparisons', str(folder))
        self.assertNotIn('| k1 |', section)
        self.assertIn('session-comparison-20261114T080000Z-aaaaaaaa.jsonl: replaced by session-comparison-20261114T080000Z-bbbbbbbb.jsonl', section)

    def test_a_summary_of_another_form_and_launch_records_that_disagree_or_name_none_do_not_count_or_stop(self):
        folder = self.rows('session-comparison-20261114T080000Z-aaaaaaaa.jsonl', [
            {'header': True, 'candidate_key': 'c', 'answers_of': 'screen-list-x.jsonl', 'written_at': 7},
            {'comparison': 'C2', 'outcome': 'passed'}, {'summary': {'C2': 5}}])
        text = self.printed('--repo', str(self.repo()), '--candidate', 'c', '--comparisons', str(folder))
        self.assertIn('| c | C2 | 1 | 0 | 0 | 0 | 0 |', text)
        self.assertIn('its summary line is not of the form the tool writes; the rows are counted', text)
        for name, launch in (('fields that disagree', {'candidate_key': 'c', 'identifier': 'dev.chirality.app-v4.candidate.c',
                                                         'bundle': {'identifier': 'dev.chirality.app-v4.candidate.other'}}),
                             ('no identity', {})):
            with self.subTest(name):
                (folder / 'launch-record-0.json').write_text(json.dumps(launch))
                text = self.printed('--repo', str(self.repo()), '--candidate', 'c', '--comparisons', str(folder))
                self.assertNotIn('| c | C2 |', text)
                self.assertIn("none of this folder's rows is counted", text)


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

    def test_a_header_naming_no_candidate_is_not_known_and_never_read_from_the_launch_record(self):
        for launches in (['k9'], ['k9', 'k8']):
            with self.subTest(launches):
                folder = self.root / ('record-' + '-'.join(launches))
                self.rows('session-comparison-20261114T080000Z-00000001.jsonl', [
                    {'header': True, 'candidate_key': None, 'fallback': True}, {'comparison': 'C2', 'outcome': 'blocked'}], folder)
                for n, key in enumerate(launches):
                    (folder / f'launch-record-{n}.json').write_text(
                        json.dumps({'bundle': {'identifier': f'dev.chirality.app-v4.candidate.{key}'}}))
                section = self.section(folder)
                self.assertIn('| not known (session-comparison-20261114T080000Z-00000001.jsonl) | C2 | 0 | 0 | 1 | 0 | 0 |', section)
                self.assertNotIn('| k9 |', section)
                self.assertNotIn('| k8 |', section)
                self.assertIn('written after a refusal or failure (fallback); it names no candidate', section)

    def test_a_refused_answers_run_replaces_the_answers_its_list_had_before(self):
        head = {'header': True, 'candidate_key': 'k1', 'answers_of': 'screen-list-x.jsonl'}
        folder = self.rows('session-comparison-20261114T080000Z-aaaaaaaa.jsonl',
                           [head, {'comparison': 'C2', 'outcome': 'passed'}, {'comparison': 'C3', 'outcome': 'passed'}])
        self.rows('session-comparison-20261114T090000Z-bbbbbbbb.jsonl',
                  [{'header': True, 'candidate_key': None, 'fallback': True, 'answers_of': 'screen-list-x.jsonl'},
                   {'comparison': 'C2', 'outcome': 'blocked'}], folder)
        section = self.section(folder)
        self.assertNotIn('| k1 |', section)  # the earlier passes no longer count
        self.assertIn('session-comparison-20261114T080000Z-aaaaaaaa.jsonl: replaced by '
                      'session-comparison-20261114T090000Z-bbbbbbbb.jsonl', section)
        self.assertIn('| not known (session-comparison-20261114T090000Z-bbbbbbbb.jsonl) | C2 | 0 | 0 | 1 | 0 | 0 |', section)

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
