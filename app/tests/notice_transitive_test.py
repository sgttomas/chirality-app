"""Transitive runtime notice index: cargo-free check refusals; no fetch, build or Cargo run."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('notice_transitive', ROOT / 'app/packaging/notices/transitive.py')
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)


class Transitive(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        # The checked reader requires physical paths. macOS TMPDIR can include
        # /var or another alias; resolve only our newly created fixture root.
        self.root = Path(self.tmp.name).resolve()
        self.index = self.root / 'index.json'
        shutil.copyfile(t.INDEX, self.index)
        self.value = json.loads(self.index.read_text())

    def write(self, rebind=False):
        if rebind:  # a mutator who also recomputes the receipt digests
            self.value['generation']['member_set_sha256'] = t.member_digests(self.value['cargo'], self.value['npm'])
        self.index.write_text(json.dumps(self.value))

    def refuses(self, pattern):
        with self.assertRaisesRegex(ValueError, pattern): t.check(self.index)

    def test_committed_index_matches_current_manifests_and_direct_index(self):
        index = t.check()
        s = t.summary(index)
        self.assertGreater(s['cargo_runtime_crates'], 0)
        self.assertEqual(sum(s['text_kinds'].values()), s['cargo_runtime_crates'] + s['npm_runtime_packages'])

    def test_standalone_cli_needs_no_site_packages(self):
        legacy = json.loads(t.INDEX.read_bytes())
        associations = t.local_associations(ROOT)
        for row in legacy['cargo']:
            selected = associations.get((row['package'], row['version']))
            if selected is not None:
                row['text'] = selected['prior_locator']
        legacy['format'] = t.LEGACY_FORMAT
        self.index.write_text(json.dumps(legacy))
        output = self.root / 'joined.json'
        commands = [['--help'], ['check'], ['associate-local', '--input', str(self.index), '--out', str(output)]]
        for args in commands:
            with self.subTest(command=args[0]):
                result = subprocess.run([sys.executable, '-I', '-S', '-B', str(ROOT / 'app/packaging/notices/transitive.py'), *args],
                                        capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 0, result.stderr)
        if output.exists():
            self.assertEqual(output.read_bytes(), t.INDEX.read_bytes())

    def test_moved_basis_refuses(self):
        self.value['source_basis']['app/src-tauri/Cargo.lock'] = '0' * 64; self.write()
        with self.assertRaisesRegex(ValueError, 'regenerate'): t.check(self.index)

    def test_checksum_drift_and_unlocked_crate_refuse(self):
        crate = next(e for e in self.value['cargo'] if e['source'] == 'registry')
        crate['archive_sha256'] = '0' * 64; self.write()
        with self.assertRaisesRegex(ValueError, 'checksum'): t.check(self.index)
        self.setUp(); next(e for e in self.value['cargo'] if e['source'] == 'registry')['version'] = '999.0.0'; self.write(rebind=True)
        with self.assertRaisesRegex(ValueError, 'unlocked'): t.check(self.index)

    def test_missing_direct_component_refuses(self):
        self.value['cargo'] = [e for e in self.value['cargo'] if e['package'] != 'rusqlite']; self.write(rebind=True)
        with self.assertRaisesRegex(ValueError, 'direct crate missing|unreachable'): t.check(self.index)

    def test_text_kind_must_match_members_and_received_text(self):
        member = next(e for e in self.value['cargo'] if e['source'] == 'registry' and e['notice_members'])
        member['text'] = {'kind': 'missing'}; self.write()
        with self.assertRaisesRegex(ValueError, 'contradicts'): t.check(self.index)

    def test_changed_retained_received_text_refuses(self):
        repo = self.root / 'repo'
        local = t.local_associations(ROOT)
        manifest = json.loads((ROOT / t.LOCAL_ASSOCIATIONS).read_bytes())
        retained = {n['retained_path'] for a in local.values() for n in a['text']['notices']}
        for rel in (*t.BASIS, t.OBJC2_METADATA, *t.RECEIVED_TEXTS.values(), t.LOCAL_ASSOCIATIONS, manifest['proof_path'], *retained):
            (repo / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(ROOT / rel, repo / rel)
        t.check(self.index, repo)
        text = repo / t.RECEIVED_TEXTS['https://github.com/madsmtm/objc2']
        text.write_bytes(text.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'received upstream text differs'): t.check(self.index, repo)

    def test_dropped_or_altered_rows_break_the_generation_receipt(self):
        for mutate in (lambda v: v.update(cargo=[e for e in v['cargo'] if e['package'] != 'adler2']),
                       lambda v: v.update(npm=[e for e in v['npm'] if e['package'] != 'scheduler']),
                       lambda v: v['npm'][0].update(integrity='sha512-' + 'A' * 86 + '==')):
            self.setUp(); mutate(self.value); self.write()
            self.refuses('generation receipt')

    def test_npm_rows_are_recomputed_from_the_lock_even_when_the_receipt_is_rebound(self):
        self.value['npm'] = [e for e in self.value['npm'] if e['package'] != 'scheduler']; self.write(rebind=True)
        self.refuses('package-lock')
        self.setUp(); self.value['npm'][0]['integrity'] = 'sha512-' + 'A' * 86 + '=='; self.write(rebind=True)
        self.refuses('package-lock')

    def test_cargo_text_kinds_cannot_hide_unverified_npm_packages(self):
        for package in ('scheduler', 'react'):
            row = next(e for e in self.value['npm'] if e['package'] == package)
            original = row['text']
            for kind in ('archive-member', 'received-upstream-text', 'retained-root-texts'):
                with self.subTest(package=package, kind=kind):
                    row['text'] = {'kind': kind}; self.write()
                    self.refuses('unknown npm text kind')
            row['text'] = original

    def test_unsupported_npm_lock_lookup_refuses(self):
        lock = json.loads((ROOT / 'app/package-lock.json').read_text())
        repo = self.root / 'repo'; (repo / 'app').mkdir(parents=True)
        del lock['packages']['node_modules/scheduler']
        (repo / 'app/package-lock.json').write_text(json.dumps(lock))
        with self.assertRaisesRegex(ValueError, 'unsupported lookup'): t.npm_runtime(repo)

    def test_registry_row_relabelled_as_path_refuses(self):
        crate = next(e for e in self.value['cargo'] if e['package'] == 'adler2')
        crate.update(source='path', archive_sha256='0' * 64); self.write(rebind=True)
        self.refuses('source kind contradicts Cargo.lock')

    def test_extra_locked_but_unreachable_row_refuses(self):
        lock = tomllib.loads((ROOT / 'app/src-tauri/Cargo.lock').read_text())['package']
        members = {(e['package'], e['version']) for e in self.value['cargo']}
        named = {d.split()[0] for p in lock if (p['name'], p['version']) in members for d in p.get('dependencies', [])}
        extra = next(p for p in lock if 'source' in p and p['name'] not in named and (p['name'], p['version']) not in members)
        self.value['cargo'].append({'package': extra['name'], 'version': extra['version'], 'source': 'registry',
                                    'archive_sha256': extra['checksum'], 'declared_license': 'MIT', 'notice_members': [],
                                    'native_source_paths': [], 'text': {'kind': 'missing'}}); self.write(rebind=True)
        self.refuses('unreachable')

    def test_received_text_reads_only_the_allowed_retained_source(self):
        invented = self.root / 'invented-LICENSE.md'; invented.write_bytes(b'invented text\n')
        blob = t.git_blob(invented.read_bytes())
        original = Path.read_bytes
        opened = []
        def tracking(path):
            opened.append(Path(path).resolve()); return original(path)
        for path in (str(invented), t.WORK + '/../../../../../' + str(invented).lstrip('/'),
                     t.WORK + '/approved-receipt-20261102/sources/objc2/../../../' + invented.name):
            self.setUp()
            received = next(e for e in self.value['cargo'] if e['text']['kind'] == 'received-upstream-text')
            received['text'].update(path=path, git_blob_sha1=blob); self.write(rebind=True)
            with mock.patch.object(Path, 'read_bytes', tracking):
                self.refuses('allowed retained source')
            self.assertNotIn(invented.resolve(), opened)
        self.setUp()
        received = next(e for e in self.value['cargo'] if e['text']['kind'] == 'received-upstream-text')
        received['text']['git_blob_sha1'] = blob; self.write(rebind=True)
        self.refuses('no known received-text blob')

    def test_partial_root_texts_remain_unqualified_in_summary(self):
        index = t.check()
        self.assertEqual(index['format'], t.FORMAT)
        rows = [e for e in index['cargo'] if e.get('text', {}).get('kind') == 'retained-root-texts']
        self.assertEqual(len(rows), 10)
        summary = t.summary(index)
        for row in rows:
            self.assertTrue(any(item.startswith(row['package'] + ' ') for item in summary['missing_or_unverified']))
        unic = next(e for e in rows if e['package'] == 'unic-common')
        self.assertIsNone(unic['text']['path_in_vcs'])
        self.assertIn('COPYRIGHT.md', unic['text']['unresolved'][0])
        self.assertEqual([n['root_path'] for n in unic['text']['notices']], ['LICENSE-APACHE', 'LICENSE-MIT'])
        for name in ('uuid-simd', 'vsimd'):
            self.assertEqual(next(e for e in index['cargo'] if e['package'] == name)['text']['kind'], 'missing')
        self.assertEqual(next(e for e in index['npm'] if e['package'] == 'scheduler')['text']['kind'], 'installed-tree-only')

    def test_legacy_reader_and_explicit_join_keep_original_graph_receipt(self):
        associations = t.local_associations(ROOT)
        for row in self.value['cargo']:
            selected = associations.get((row['package'], row['version']))
            if selected is not None: row['text'] = selected['prior_locator']
        self.value['format'] = t.LEGACY_FORMAT; self.write()
        old = t.check(self.index)
        self.assertEqual(sum(e.get('text', {}).get('kind') == 'missing' for e in old['cargo']), 12)
        with mock.patch.object(t, 'cargo_runtime', side_effect=AssertionError('Cargo must not run')):
            joined = t.associate_local(self.index)
        self.assertEqual(joined['generation'], old['generation'])
        self.assertEqual(joined['source_basis'], old['source_basis'])
        self.assertEqual(t.member_digests(joined['cargo'], joined['npm']), old['generation']['member_set_sha256'])
        self.assertEqual(joined['npm'], old['npm'])
        self.assertEqual(joined, json.loads(t.INDEX.read_bytes()))
        self.index.write_text(json.dumps(joined))
        self.assertEqual(t.associate_local(self.index), joined)
        # A legacy format cannot silently receive successor row labels.
        joined['format'] = t.LEGACY_FORMAT; self.index.write_text(json.dumps(joined))
        self.refuses('unknown cargo text kind')

    def test_root_row_cannot_choose_path_revision_scope_or_downgrade(self):
        for field, value in [('retained_path', '/tmp/not-an-approved-notice'), ('git_blob_sha1', '0'*40)]:
            self.setUp()
            row = next(e for e in self.value['cargo'] if e.get('text', {}).get('kind') == 'retained-root-texts')
            row['text']['notices'][0][field] = value; self.write()
            self.refuses('retained-root text association differs')
        for mutate in (lambda row: row['text'].update(vcs_revision='0'*40),
                       lambda row: row['text'].update(unresolved=[]),
                       lambda row: row.update(text={'kind': 'missing'}),
                       lambda row: row.update(declared_license='invented election')):
            self.setUp()
            row = next(e for e in self.value['cargo'] if e['package'] == 'unic-common')
            mutate(row); self.write()
            self.refuses('retained-root')

    def test_unlisted_crate_cannot_inherit_root_association(self):
        root = next(e for e in self.value['cargo'] if e.get('text', {}).get('kind') == 'retained-root-texts')
        other = next(e for e in self.value['cargo'] if e['package'] == 'uuid-simd')
        other['text'] = root['text']; self.write()
        self.refuses('retained-root subject is not allowed')

    def test_root_allowlist_and_text_tampering_or_links_refuse(self):
        repo = self.root / 'repo'
        manifest = json.loads((ROOT / t.LOCAL_ASSOCIATIONS).read_bytes())
        paths = [t.LOCAL_ASSOCIATIONS, manifest['proof_path']]
        paths += [n['retained_path'] for a in manifest['associations'] for n in a['text']['notices']]
        for rel in set(paths):
            (repo / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(ROOT / rel, repo / rel)
        selected = t.local_associations(repo)
        row = next(e for e in self.value['cargo'] if e['package'] == 'alloc-stdlib')
        self.assertEqual(t.local_text(repo, row, selected), row['text'])
        path = repo / row['text']['notices'][0]['retained_path']
        raw = path.read_bytes(); path.write_bytes(raw + b'changed')
        with self.assertRaisesRegex(ValueError, 'notice bytes differ'): t.local_text(repo, row, selected)
        path.write_bytes(raw)
        other = self.root / 'same-body'; other.write_bytes(raw)
        path.unlink(); path.symlink_to(other)
        with self.assertRaises((OSError, ValueError)): t.local_text(repo, row, selected)
        path.unlink(); path.parent.rmdir()
        path.parent.symlink_to(other.parent, target_is_directory=True)
        with self.assertRaises((OSError, ValueError)): t.local_text(repo, row, selected)
        registry = repo / t.LOCAL_ASSOCIATIONS
        registry.write_bytes(registry.read_bytes() + b' ')
        with self.assertRaisesRegex(ValueError, 'allowlist differs'): t.local_associations(repo)

    def test_local_join_checks_prior_locator_before_association(self):
        associations = t.local_associations(ROOT)
        for row in self.value['cargo']:
            selected = associations.get((row['package'], row['version']))
            if selected is not None: row['text'] = selected['prior_locator']
        self.value['format'] = t.LEGACY_FORMAT
        next(e for e in self.value['cargo'] if e['package'] == 'alloc-stdlib')['text']['vcs_revision'] = '0'*40
        self.write()
        with self.assertRaisesRegex(ValueError, 'original source locator differs'): t.associate_local(self.index)

    def test_local_join_refuses_forged_legacy_archive_provenance(self):
        associations = t.local_associations(ROOT)
        for row in self.value['cargo']:
            selected = associations.get((row['package'], row['version']))
            if selected is not None: row['text'] = selected['prior_locator']
        self.value['format'] = t.LEGACY_FORMAT
        row = next(e for e in self.value['cargo'] if e['package'] == 'alloc-stdlib')
        row['text'] = {'kind': 'archive-member'}
        row['notice_members'] = [{'member': 'LICENSE', 'size_bytes': 1483, 'sha256': '0' * 64}]
        self.write()
        with self.assertRaisesRegex(ValueError, 'original source locator differs'): t.associate_local(self.index)


if __name__ == '__main__':
    unittest.main()
