"""Prior-version data inventory (DEL-01-06 AC-009, VER-008) on invented trees only.

Never point this at a real home directory or any person's application data."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import stat
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('prior_data_inventory', ROOT / 'app/packaging/prior_data/inventory.py')
tool = importlib.util.module_from_spec(spec); spec.loader.exec_module(tool)

CANARY = 'INVENTED-CANARY-7f3a91-never-in-a-record'


class PriorData(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.base = Path(temp.name).resolve()   # /var is a link on macOS; roots must not have one
        self.home = self.base / 'home'
        self.prior = self.home / 'Library/Application Support/Chirality'
        (self.prior / 'runtime/projects').mkdir(parents=True)
        (self.prior / 'settings.json').write_text('{"invented": "' + CANARY + '"}')
        (self.prior / 'runtime/projects/notes.txt').write_text(CANARY)
        (self.prior / 'runtime/projects/notes.txt').chmod(0o600)
        os.symlink('/nonexistent/' + CANARY, self.prior / 'runtime/link')
        self.prefs = self.home / 'Library/Preferences/com.chirality.app.plist'
        self.prefs.parent.mkdir(parents=True)
        self.prefs.write_bytes(b'INVENTED preferences ' + CANARY.encode())
        self.current = self.home / 'Library/Application Support/com.chirality.app'
        self.bundle = self.base / 'Applications/Chirality.app'
        (self.bundle / 'Contents').mkdir(parents=True)
        (self.bundle / 'Contents/Info.plist').write_text('INVENTED v3 bundle')
        self.roots = [('prior-data', self.prior), ('current-data', self.current),
                      ('system-per-identifier', self.prefs), ('application-bundle', self.bundle)]
        self.records = self.base / 'records'; self.records.mkdir()
        self.n = 0

    def write(self):
        self.n += 1
        out, summary = self.records / f'record-{self.n}.json', self.records / f'summary-{self.n}.json'
        tool.write_record(self.roots, out, summary)
        return out, summary

    def compare(self, before, after):
        result = tool.compare(tool.load(before), tool.load(after))
        return result, {r['class']: r for r in result['roots']}

    def test_nothing_differing_is_the_only_unchanged(self):
        before, _ = self.write()
        after, _ = self.write()
        result, roots = self.compare(before, after)
        self.assertEqual(result['status'], 'unchanged')
        self.assertTrue(all(r['finding'] in ('unchanged', 'absent before and after') for r in roots.values()))
        self.assertEqual(tool.main(['compare', str(before), str(after)]), 0)

    def test_new_root_is_a_difference_reported_as_created(self):
        before, _ = self.write()
        (self.current / 'records').mkdir(parents=True)
        (self.current / 'records/store.db').write_bytes(b'INVENTED')
        after, _ = self.write()
        result, roots = self.compare(before, after)
        self.assertEqual(result['status'], 'differences found')
        self.assertEqual(roots['prior-data']['finding'], 'unchanged')
        self.assertEqual(roots['current-data']['finding'], 'created (absent before)')
        self.assertEqual(roots['current-data']['before'], 'absent')
        self.assertEqual(roots['current-data']['counts']['added_in_recorded_directory'], 0)
        self.assertEqual(roots['current-data']['counts']['added'], 3)
        self.assertEqual(tool.main(['compare', str(before), str(after)]), 1)
        shared = tool.shareable(result, before.read_bytes(), after.read_bytes())
        self.assertEqual(shared['by_class']['current-data']['roots_appeared'], 1)
        self.assertEqual(shared['by_class']['prior-data'], {'changed': 0, 'removed': 0, 'added': 0,
            'added_in_recorded_directory': 0, 'roots_appeared': 0, 'roots_disappeared': 0})

    # Review probes inventory-addition and inventory-appeared: each once gave exit 0, "unchanged".
    def test_addition_to_a_recorded_prior_data_folder_is_a_difference(self):
        self.roots = [('prior-data', self.prior)]
        before, _ = self.write()
        (self.prior / 'new.txt').write_bytes(b'invented')
        after, _ = self.write()
        result, roots = self.compare(before, after)
        self.assertEqual(result['status'], 'differences found')
        self.assertEqual(roots['prior-data']['finding'], 'unchanged entries; additions')
        self.assertEqual(roots['prior-data']['counts']['added_in_recorded_directory'], 1)
        self.assertEqual(tool.main(['compare', str(before), str(after)]), 1)

    def test_prior_data_root_that_appears_is_a_difference(self):
        absent = self.home / 'Library/Logs/Chirality'
        self.roots = [('prior-data', absent)]
        before, _ = self.write()
        absent.mkdir(parents=True); (absent / 'invented.log').write_bytes(b'invented')
        after, _ = self.write()
        result, roots = self.compare(before, after)
        self.assertEqual(result['status'], 'differences found')
        self.assertEqual((roots['prior-data']['before'], roots['prior-data']['finding']), ('absent', 'created (absent before)'))
        self.assertEqual(tool.main(['compare', str(before), str(after)]), 1)

    # Review probe inventory-unreadable-ancestor: refused, never recorded.
    @unittest.skipIf(os.geteuid() == 0, 'root reads everything')
    def test_unreadable_ancestor_of_a_root_is_refused(self):
        locked = self.base / 'locked'; locked.mkdir(); (locked / 'existing.txt').write_text('invented')
        locked.chmod(0o000); self.addCleanup(locked.chmod, 0o700)
        out, summary = self.records / 'r.json', self.records / 's.json'
        # Never recorded as absent: the root exists but cannot be examined.
        with self.assertRaisesRegex(tool.Refused, 'unreadable ancestor'):
            tool.record([('prior-data', locked / 'existing.txt')])
        self.assertEqual(tool.main(['record', '--root', str(locked / 'existing.txt'), '--out', str(out), '--summary', str(summary)]), 2)
        self.assertFalse(out.exists() or summary.exists())

    def test_changed_bytes_mode_deletion_and_addition_are_each_reported(self):
        before, _ = self.write()
        (self.prior / 'settings.json').write_text('{"invented": "changed"}')
        (self.prior / 'runtime/projects/notes.txt').chmod(0o644)
        os.unlink(self.prior / 'runtime/link')
        (self.prior / 'runtime/new.txt').write_text('INVENTED addition')
        after, _ = self.write()
        result, roots = self.compare(before, after)
        prior = roots['prior-data']
        self.assertEqual(result['status'], 'differences found')
        self.assertEqual(prior['finding'], 'changed')
        changed = {c['path']: c['differs_in'] for c in prior['entries']['changed']}
        self.assertEqual(changed['settings.json'], ['sha256', 'size'])
        self.assertEqual(changed['runtime/projects/notes.txt'], ['mode'])
        self.assertNotIn('runtime', changed)   # a directory differs only by its kind or mode
        self.assertEqual(prior['entries']['removed'], ['runtime/link'])
        self.assertEqual(prior['entries']['added_in_recorded_directory'], ['runtime/new.txt'])
        self.assertEqual(tool.main(['compare', str(before), str(after)]), 1)

    def test_link_target_change_and_system_root_change_stay_apart(self):
        before, _ = self.write()
        os.unlink(self.prior / 'runtime/link'); os.symlink('/nonexistent/other', self.prior / 'runtime/link')
        self.prefs.write_bytes(b'INVENTED preferences rewritten by the system')
        after, _ = self.write()
        _, roots = self.compare(before, after)
        self.assertEqual(roots['prior-data']['entries']['changed'], [{'path': 'runtime/link', 'differs_in': ['target']}])
        self.assertEqual(roots['system-per-identifier']['finding'], 'changed')
        self.assertEqual(roots['system-per-identifier']['entries']['changed'][0]['path'], '.')

    def test_replaced_bundle_is_reported_as_expected_replacement(self):
        before, _ = self.write()
        (self.bundle / 'Contents/Info.plist').write_text('INVENTED 4.0.0 bundle')
        after, _ = self.write()
        result, roots = self.compare(before, after)
        self.assertEqual(roots['application-bundle']['finding'], 'changed (replacement expected)')
        self.assertEqual(roots['prior-data']['finding'], 'unchanged')
        self.assertEqual(result['status'], 'differences found')   # the exit basis is unchanged by the class

    def test_removed_root_is_a_failure(self):
        before, _ = self.write()
        self.prefs.unlink()
        after, _ = self.write()
        result, roots = self.compare(before, after)
        self.assertEqual(roots['system-per-identifier']['finding'], 'removed')
        self.assertEqual(result['status'], 'differences found')

    def test_socket_is_recorded_by_kind_and_never_read(self):
        # AF_UNIX paths are short; the usual temporary folder is too deep for one.
        short = tempfile.TemporaryDirectory(dir='/private/tmp' if Path('/private/tmp').is_dir() else None)
        self.addCleanup(short.cleanup)
        root = Path(short.name).resolve()
        server = socket.socket(socket.AF_UNIX)
        self.addCleanup(server.close)
        server.bind(str(root / 's'))
        self.roots = [('prior-data', root)]
        out, _ = self.write()
        entries = {e['path']: e for e in json.loads(out.read_bytes())['roots'][0]['entries']}
        self.assertEqual(entries['s'], {'path': 's', 'kind': 'socket', 'mode': entries['s']['mode']})

    def test_fifo_is_recorded_by_kind_and_never_opened(self):
        os.mkfifo(self.prior / 'pipe')   # opening it for reading would block
        out, _ = self.write()
        entries = {e['path']: e for e in json.loads(out.read_bytes())['roots'][0]['entries']}
        self.assertEqual(entries['pipe']['kind'], 'fifo')
        self.assertNotIn('sha256', entries['pipe'])

    def test_canary_never_appears_in_record_summary_or_comparison_summary(self):
        before, summary = self.write()
        after, _ = self.write()
        result = tool.compare(tool.load(before), tool.load(after))
        shared = tool.shareable(result, before.read_bytes(), after.read_bytes())
        record = before.read_text()
        self.assertNotIn(CANARY.encode().hex(), record)
        # The link's target text is kept in the private record by design; content never is.
        self.assertEqual(record.count(CANARY), 1)
        self.assertIn('"target": "/nonexistent/' + CANARY, record)
        for text in (summary.read_text(), json.dumps(shared)):
            self.assertNotIn(CANARY, text)
            self.assertNotIn(str(self.home), text)
            self.assertNotIn('settings.json', text)
        self.assertEqual(stat.S_IMODE(before.stat().st_mode), 0o600)

    def test_no_content_reaches_a_record_without_a_link(self):
        os.unlink(self.prior / 'runtime/link')
        out, summary = self.write()
        for path in (out, summary):
            self.assertNotIn(CANARY, path.read_text())

    def test_absent_root_is_recorded_as_absent(self):
        out, summary = self.write()
        roots = {r['class']: r for r in json.loads(out.read_bytes())['roots']}
        self.assertEqual(roots['current-data'], {'class': 'current-data', 'path': str(self.current), 'state': 'absent'})
        self.assertEqual(json.loads(summary.read_bytes())['roots'][1]['state'], 'absent')

    # Refusals.
    def assertRefused(self, roots=None, out=None, summary=None):
        roots = roots or self.roots
        out = out or self.records / 'refused.json'
        summary = summary or self.records / 'refused-summary.json'
        with self.assertRaises(tool.Refused):
            tool.write_record(roots, out, summary)

    def test_symbolic_link_in_root_ancestry_is_refused(self):
        os.symlink(self.home / 'Library', self.base / 'alias')
        self.assertRefused([('prior-data', self.base / 'alias/Application Support/Chirality')])
        self.assertRefused([('prior-data', self.base / 'alias')])

    def test_existing_output_or_output_inside_a_root_is_refused(self):
        existing = self.records / 'exists.json'; existing.write_text('x')
        self.assertRefused(out=existing)
        self.assertRefused(out=self.prior / 'record.json')
        self.assertRefused(out=self.current / 'record.json')   # absent root: refused by path
        self.assertFalse(os.path.lexists(self.prior / 'record.json'))

    @unittest.skipIf(os.geteuid() == 0, 'root reads everything')
    def test_unreadable_entry_is_refused_not_omitted(self):
        locked = self.prior / 'runtime/projects/notes.txt'
        locked.chmod(0o000); self.addCleanup(locked.chmod, 0o600)
        self.assertRefused()
        folder = self.prior / 'runtime/projects'
        locked.chmod(0o600); folder.chmod(0o000); self.addCleanup(folder.chmod, 0o700)
        self.assertRefused()
        self.assertFalse((self.records / 'refused.json').exists())

    def test_data_changing_while_read_is_refused(self):
        scan = tool._scan_root
        calls = []
        def changing(path):
            calls.append(path)
            if len(calls) == len(self.roots) + 1:
                (self.prior / 'settings.json').write_text('changed between passes')
            return scan(path)
        with patch.object(tool, '_scan_root', side_effect=changing):
            self.assertRefused()
        self.assertFalse((self.records / 'refused.json').exists())

    def test_name_with_line_break_is_refused(self):
        (self.prior / 'bad\nname').write_text('x')
        self.assertRefused()

    # Review round 2 probes inventory-empty-roots, -incomplete-present, -incomplete-file: each once
    # compared with itself as unchanged. Now every record is validated and must be completed.
    def assertRecordRefused(self, value, completed=True):
        if completed and isinstance(value, dict) and 'format' in value and 'roots' in value:
            value = tool.completed(value)
        path = self.records / f'bad-{self.n}.json'; self.n += 1
        path.write_text(value if isinstance(value, str) else json.dumps(value))
        with self.assertRaises(tool.Refused):
            tool.load(path)
        self.assertEqual(tool.main(['compare', str(path), str(path)]), 2)

    def test_incomplete_or_impossible_records_are_refused(self):
        root = str(self.prior)
        for completed in (False, True):
            with self.subTest(completed=completed):
                self.assertRecordRefused({'format': tool.FORMAT, 'roots': []}, completed)
                self.assertRecordRefused({'format': tool.FORMAT, 'roots': [
                    {'class': 'prior-data', 'path': root, 'state': 'present', 'entries': []}]}, completed)
                self.assertRecordRefused({'format': tool.FORMAT, 'roots': [
                    {'class': 'prior-data', 'path': root, 'state': 'present', 'kind': 'file', 'mode': '0o600', 'entries': []}]}, completed)
        good, _ = self.write()
        value = json.loads(good.read_bytes())
        body = {'format': value['format'], 'roots': value['roots']}
        def variant(change):
            v = json.loads(json.dumps(body)); change(v); return v
        cases = {
            'entry without kind': lambda v: v['roots'][0]['entries'][0].pop('kind'),
            'file entry without digest': lambda v: next(e for e in v['roots'][0]['entries'] if e['kind'] == 'file').pop('sha256'),
            'entry with extra field': lambda v: v['roots'][0]['entries'][0].update(note='x'),
            'entries out of order': lambda v: v['roots'][0]['entries'].reverse(),
            'parent not recorded': lambda v: v['roots'][0]['entries'].append({'path': 'zz/orphan', 'kind': 'dir', 'mode': '0o755'}),
            'escaping path': lambda v: v['roots'][0]['entries'].append({'path': '../x', 'kind': 'dir', 'mode': '0o755'}),
            'unknown class': lambda v: v['roots'][0].update({'class': 'other'}),
            'absent root with entries': lambda v: v['roots'][1].update(entries=[]),
            'relative root path': lambda v: v['roots'][0].update(path='relative'),
            'bad mode': lambda v: v['roots'][0].update(mode='755'),
        }
        for label, change in cases.items():
            with self.subTest(case=label):
                self.assertRecordRefused(variant(change))
        self.assertRecordRefused(body, completed=False)                    # no marker
        edited = tool.completed(body); edited['roots'][0]['mode'] = '0o700'
        self.assertRecordRefused(edited, completed=False)                  # edited after completion
        self.assertRecordRefused(good.read_text()[:-40], completed=False)  # truncated
        self.assertEqual(tool.main(['compare', str(good), str(good)]), 0)
        self.assertEqual(list(value), ['format', 'roots', 'completion'])   # the marker is written last

    # Review round 3 probes nul-entry, nul-root, zero-byte-wrong-digest, noncanonical-root: each a
    # consistent, completed record that no successful observation could have produced.
    def test_values_a_successful_record_could_not_hold_are_refused(self):
        root = str(self.prior)
        empty = hashlib.sha256(b'').hexdigest()
        records = {
            'NUL in an entry path': [{'class': 'prior-data', 'path': root, 'state': 'present', 'kind': 'dir', 'mode': '0o700',
                                      'entries': [{'path': 'impossible\u0000name', 'kind': 'dir', 'mode': '0o700'}]}],
            'NUL in a root path': [{'class': 'prior-data', 'path': root + '\u0000impossible', 'state': 'absent'}],
            'control character in a path': [{'class': 'prior-data', 'path': root, 'state': 'present', 'kind': 'dir', 'mode': '0o700',
                                             'entries': [{'path': 'tab\tname', 'kind': 'dir', 'mode': '0o700'}]}],
            'zero-byte file, wrong digest': [{'class': 'prior-data', 'path': root, 'state': 'present', 'kind': 'file', 'mode': '0o600',
                                              'size': 0, 'sha256': '0' * 64, 'entries': []}],
            'non-empty file, empty digest': [{'class': 'prior-data', 'path': root, 'state': 'present', 'kind': 'file', 'mode': '0o600',
                                              'size': 3, 'sha256': empty, 'entries': []}],
            'root path not normal': [{'class': 'prior-data', 'path': root + '/../' + self.prior.name, 'state': 'absent'}],
            'mode beyond permission bits': [{'class': 'prior-data', 'path': root, 'state': 'present', 'kind': 'dir', 'mode': '0o17777', 'entries': []}],
            'mode not as written': [{'class': 'prior-data', 'path': root, 'state': 'present', 'kind': 'dir', 'mode': '0o0755', 'entries': []}],
            'directory with a digest': [{'class': 'prior-data', 'path': root, 'state': 'present', 'kind': 'dir', 'mode': '0o755',
                                         'sha256': empty, 'entries': []}],
            'file size without digest': [{'class': 'prior-data', 'path': root, 'state': 'present', 'kind': 'dir', 'mode': '0o755',
                                          'entries': [{'path': 'f', 'kind': 'file', 'mode': '0o600', 'size': 1}]}],
            'NUL in a link target': [{'class': 'prior-data', 'path': root, 'state': 'present', 'kind': 'dir', 'mode': '0o755',
                                      'entries': [{'path': 'l', 'kind': 'symlink', 'mode': '0o755', 'target': 'a\u0000b'}]}],
            'duplicate entry path': [{'class': 'prior-data', 'path': root, 'state': 'present', 'kind': 'dir', 'mode': '0o755',
                                      'entries': [{'path': 'd', 'kind': 'dir', 'mode': '0o755'}, {'path': 'd', 'kind': 'dir', 'mode': '0o755'}]}],
            'entry outside its root': [{'class': 'prior-data', 'path': root, 'state': 'present', 'kind': 'dir', 'mode': '0o755',
                                        'entries': [{'path': '../outside', 'kind': 'dir', 'mode': '0o755'}]}],
        }
        for label, roots in records.items():
            with self.subTest(case=label):
                self.assertRecordRefused({'format': tool.FORMAT, 'roots': json.loads(json.dumps(roots))})
        # A real zero-byte file records the empty digest and compares.
        (self.prior / 'empty.txt').write_bytes(b'')
        good, _ = self.write()
        self.assertEqual(tool.main(['compare', str(good), str(good)]), 0)

    def test_records_naming_different_roots_are_refused(self):
        before, _ = self.write()
        self.roots = self.roots[:2]
        after, _ = self.write()
        with self.assertRaises(tool.Refused):
            self.compare(before, after)
        self.assertEqual(tool.main(['compare', str(before), str(after)]), 2)

    def test_roots_prints_defaults_and_reads_nothing(self):
        home = self.base / 'no-such-home'
        with patch.object(os, 'scandir', side_effect=AssertionError('read')), \
             patch.object(os, 'lstat', side_effect=AssertionError('read')):
            roots = tool.default_roots(home)
        paths = {str(p): c for c, p, _ in roots}
        self.assertEqual(paths[str(home / 'Library/Application Support/Chirality')], 'prior-data')
        self.assertEqual(paths[str(home / 'Library/Application Support/com.chirality.app')], 'current-data')
        self.assertEqual(paths['/Applications/Chirality.app'], 'application-bundle')
        for system in ('Preferences/com.chirality.app.plist', 'Saved Application State/com.chirality.app.savedState',
                       'Caches/com.chirality.app', 'HTTPStorages/com.chirality.app', 'WebKit/com.chirality.app'):
            self.assertEqual(paths[str(home / 'Library' / system)], 'system-per-identifier')
        self.assertFalse(home.exists())

    def test_command_line_record_then_compare(self):
        out, summary, report = (self.records / n for n in ('cli.json', 'cli-summary.json', 'cli-report.json'))
        argv = ['record', '--root', str(self.prior), '--current-root', str(self.current),
                '--system-root', str(self.prefs), '--bundle-root', str(self.bundle)]
        self.assertEqual(tool.main(argv + ['--out', str(out), '--summary', str(summary)]), 0)
        self.assertEqual(tool.main(['compare', str(out), str(out), '--report', str(report)]), 0)
        self.assertEqual(stat.S_IMODE(report.stat().st_mode), 0o600)
        self.assertEqual(tool.main(argv + ['--out', str(out), '--summary', str(self.records / 'other.json')]), 2)


if __name__ == '__main__':
    unittest.main()
