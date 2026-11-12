"""Shipped notice texts and the coverage account: committed bytes, invented archives only; no cache, network or build."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
NOTICES = ROOT / 'app/packaging/notices'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


texts = load('coverage_test_package_texts', NOTICES / 'package_texts.py')
coverage = load('coverage_test_coverage', NOTICES / 'coverage.py')
COPIED_TREES = ('app/packaging/notices', 'app/packaging/unsigned', 'app/packaging/font_notice', 'app/packaging/sqlite_notice',
                'app/packaging/supplier_notices', 'app/src/fonts')
COPIED_FILES = ('LICENSE.md', 'app/package.json', 'app/package-lock.json', 'app/src-tauri/Cargo.toml', 'app/src-tauri/Cargo.lock',
                'app/src-tauri/tauri.conf.json', 'app/src/workspace.css', 'app/index.html', 'app/src-tauri/src/hosting.rs')


def crate(name, version, members):
    """An invented .crate archive (gzip tar with the <name>-<version>/ prefix)."""
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w:gz') as archive:
        files = {'Cargo.toml': f'[package]\nname = "{name}"\nversion = "{version}"\nlicense = "MIT"\n'.encode(),
                 '.cargo_vcs_info.json': b'{"git": {"sha1": "' + b'a' * 40 + b'"}, "path_in_vcs": ""}', **members}
        for member, raw in files.items():
            info = tarfile.TarInfo(f'{name}-{version}/{member}'); info.size = len(raw)
            archive.addfile(info, io.BytesIO(raw))
    return buffer.getvalue()


class Copy(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name).resolve() / 'repo'
        for relative in COPIED_TREES:
            shutil.copytree(ROOT / relative, self.repo / relative)
        for relative in COPIED_FILES:
            (self.repo / relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, self.repo / relative)
        pin = texts.declared_pin(ROOT)
        record = f'app/src-tauri/resources/supplier/{pin}/CANONICAL_DISTRIBUTION.json'
        (self.repo / record).parent.mkdir(parents=True); shutil.copyfile(ROOT / record, self.repo / record)
        for content in json.loads((NOTICES / 'coverage-inputs.json').read_text())['library_content']:
            (self.repo / content['resource']).mkdir(parents=True)

    def edit(self, relative, change):
        path = self.repo / relative
        value = json.loads(path.read_text()); change(value); path.write_text(json.dumps(value, indent=1) + '\n')


class ShippedTexts(Copy):
    def test_committed_tree_equals_the_indexed_set(self):
        result = texts.check(ROOT)
        self.assertEqual(result['transitive_texts'], len(texts.planned(ROOT)))
        index = json.loads((NOTICES / 'transitive-index.json').read_text())
        members = sum(len(r['notice_members']) for r in index['cargo'] if r.get('text', {}).get('kind') == 'archive-member')
        self.assertGreaterEqual(result['transitive_texts'], members)

    def test_changed_missing_extra_or_linked_text_refuses(self):
        tree = self.repo / texts.TEXTS
        target = tree / 'npm/scheduler/0.27.0/LICENSE'
        original = target.read_bytes()
        target.write_bytes(original + b'changed')
        with self.assertRaisesRegex(ValueError, 'bytes differ'): texts.check(self.repo)
        target.unlink()
        with self.assertRaisesRegex(ValueError, 'missing'): texts.check(self.repo)
        target.write_bytes(original); (tree / 'npm/scheduler/0.27.0/EXTRA').write_bytes(b'INVENTED')
        with self.assertRaisesRegex(ValueError, 'extra'): texts.check(self.repo)
        (tree / 'npm/scheduler/0.27.0/EXTRA').unlink()
        target.unlink(); target.symlink_to(self.repo / 'LICENSE.md')
        with self.assertRaisesRegex(ValueError, 'linked'): texts.check(self.repo)

    def test_extraction_refuses_an_archive_that_is_not_the_locked_one_and_keeps_the_tree(self):
        cache = self.repo.parent / 'cargo-cache'; cache.mkdir()
        index = json.loads((NOTICES / 'transitive-index.json').read_text())
        for row in index['cargo']:
            if row['source'] == 'registry':
                (cache / f"{row['package']}-{row['version']}.crate").write_bytes(b'INVENTED archive')
        before = texts.check(self.repo)
        with self.assertRaisesRegex(ValueError, 'differs from Cargo.lock'): texts.extract(cache, self.repo.parent / 'npm', self.repo)
        self.assertEqual(texts.check(self.repo), before)
        self.assertEqual([p.name for p in (self.repo / texts.TEXTS).parent.iterdir() if p.name.startswith('.transitive-')], [])

    def test_received_text_must_be_at_the_revision_its_crate_names(self):
        self.edit(texts.INPUTS, lambda v: v['received_texts'][0].update(revision='b' * 40))
        with self.assertRaisesRegex(ValueError, 'not at the revision'): texts.planned(self.repo)
        self.setUp(); self.edit(texts.INPUTS, lambda v: v['received_texts'][0].update(repository='https://github.com/invented/other'))
        with self.assertRaisesRegex(ValueError, 'another repository'): texts.planned(self.repo)
        self.setUp(); (self.repo / json.loads((NOTICES / 'coverage-inputs.json').read_text())['received_texts'][1]['path']).write_text('changed')
        with self.assertRaisesRegex(ValueError, 'committed text differs'): texts.planned(self.repo)

    def test_general_crate_extraction_verifies_the_lock_checksum(self):
        raw = crate('invented-crate', '1.0.0', {'LICENSE-MIT': b'INVENTED licence\n', 'src/lib.rs': b''})
        cache = self.repo.parent / 'crates'; cache.mkdir(); (cache / 'invented-crate-1.0.0.crate').write_bytes(raw)
        lock = self.repo.parent / 'Cargo.lock'
        lock.write_text('version = 4\n[[package]]\nname = "invented-crate"\nversion = "1.0.0"\n'
                        'source = "registry+https://github.com/rust-lang/crates.io-index"\n'
                        f'checksum = "{hashlib.sha256(raw).hexdigest()}"\n\n[[package]]\nname = "local"\nversion = "0.1.0"\n')
        out = self.repo.parent / 'out'
        rows = texts.crate_texts(lock, cache, out)
        self.assertEqual([r['kind'] for r in rows], ['archive-member', 'not-in-registry'])
        self.assertEqual((out / 'invented-crate/1.0.0/LICENSE-MIT').read_bytes(), b'INVENTED licence\n')
        self.assertEqual([m['member'] for m in rows[0]['notice_members']], ['LICENSE-MIT'])
        lock.write_text(lock.read_text().replace(hashlib.sha256(raw).hexdigest(), '0' * 64))
        with self.assertRaisesRegex(ValueError, 'differs from the lock'): texts.crate_texts(lock, cache, self.repo.parent / 'out2')

    def test_overlay_maps_every_shipped_text_once(self):
        overlay = json.loads((ROOT / texts.OVERLAY).read_text())
        self.assertEqual(overlay, texts.overlay(ROOT))
        destinations = list(overlay['bundle']['resources'].values())
        self.assertEqual(len(destinations), len(set(destinations)))
        for relative in texts.planned(ROOT):
            self.assertEqual(overlay['bundle']['resources']['../packaging/notices/transitive/' + relative],
                             'third-party-notices/transitive/' + relative)


class Account(Copy):
    def test_committed_account_is_current_and_counts_add_up(self):
        result = coverage.check(ROOT)
        account = json.loads((ROOT / coverage.ACCOUNT).read_text())
        self.assertEqual(sum(v for k, v in account['counts'].items() if k != 'total'), account['counts']['total'])
        self.assertEqual(len(result['open']), account['counts']['total'] - account['counts']['covered'])
        for component in account['components']:
            self.assertIn(component['standing'], account['standings'])
        objc2 = [c for c in account['components'] if 'owner_licence_reading' in c]
        self.assertEqual(len(objc2), 9)
        self.assertTrue(all(c['basis'].startswith('owner licence reading') for c in objc2))
        members = {m['path'] for m in account['supplier_members']}
        record = texts.supplier_record(ROOT)[2]
        self.assertEqual(members, {e['path'] for e in record['inventory']['entries'] if e['kind'] == 'file'})
        self.assertTrue(all(m['components'] or any(m['path'] in [t.get('supplier_member') for t in c['texts']]
                                                   for c in account['components']) for m in account['supplier_members']))

    def test_strict_mode_exits_non_zero_naming_each_open_component(self):
        script = str(NOTICES / 'coverage.py')
        self.assertEqual(subprocess.run([sys.executable, '-I', script, 'check'], capture_output=True).returncode, 0)
        strict = subprocess.run([sys.executable, '-I', script, 'check', '--strict'], capture_output=True, text=True)
        open_items = json.loads((ROOT / coverage.ACCOUNT).read_text())['open']
        self.assertEqual(strict.returncode, 1 if open_items else 0)
        for item in open_items:
            self.assertIn(item['name'], strict.stderr)

    def test_stale_account_refuses(self):
        self.edit(coverage.ACCOUNT, lambda v: v['counts'].update(covered=0))
        with self.assertRaisesRegex(ValueError, 'stale'): coverage.check(self.repo)

    def test_copied_inputs_regenerate_the_same_account(self):
        self.assertEqual(coverage.encode(coverage.build(self.repo)), (ROOT / coverage.ACCOUNT).read_bytes())

    def test_removed_text_turns_a_crate_uncovered_rather_than_hiding_it(self):
        self.edit(texts.INPUTS, lambda v: v.update(received_texts=[t for t in v['received_texts'] if 'nugine' not in t['path']]))
        shutil.rmtree(self.repo / texts.TEXTS / 'cargo/vsimd'); shutil.rmtree(self.repo / texts.TEXTS / 'cargo/uuid-simd')
        (self.repo / texts.OVERLAY).write_text(json.dumps(texts.overlay(self.repo), indent=2) + '\n')
        value = coverage.build(self.repo)
        self.assertEqual({o['name'] for o in value['open'] if o['standing'] == coverage.UNCOVERED} & {'vsimd', 'uuid-simd'},
                         {'vsimd', 'uuid-simd'})

    def test_owner_reading_cannot_cover_a_crate_without_a_held_text(self):
        self.edit(texts.INPUTS, lambda v: v['owner_licence_readings'].append(
            {**v['owner_licence_readings'][0], 'package': 'serde', 'version': '1.0.229'}))
        with self.assertRaisesRegex(ValueError, 'no held text'): coverage.build(self.repo)

    def test_supplier_table_must_claim_every_member_and_justify_gaps(self):
        table = 'app/packaging/supplier_notices/components.json'
        self.edit(table, lambda v: v['components'].pop(next(i for i, c in enumerate(v['components']) if c['id'] == 'zlib')))
        with self.assertRaisesRegex(ValueError, 'claimed by no component'): coverage.build(self.repo)
        self.setUp()
        self.edit(table, lambda v: next(c for c in v['components'] if c['standing'] == 'uncovered').pop('would_close'))
        with self.assertRaises((ValueError, KeyError)): coverage.build(self.repo)
        self.setUp()
        self.edit(table, lambda v: next(c for c in v['components'] if c['id'] == 'opus').update(members=['codex-resources/voice/lib/invented.dylib']))
        with self.assertRaisesRegex(ValueError, 'not in the tree'): coverage.build(self.repo)

    def test_another_declared_pin_is_named_as_an_open_review_not_assumed(self):
        pin = texts.declared_pin(ROOT)
        hosting = self.repo / texts.HOSTING
        hosting.write_text(hosting.read_text().replace(f'DECLARED_PIN: &str = "{pin}"', 'DECLARED_PIN: &str = "9.9.9"'))
        record = json.loads((ROOT / f'app/src-tauri/resources/supplier/{pin}/CANONICAL_DISTRIBUTION.json').read_text())
        record['pin'] = '9.9.9'
        target = self.repo / 'app/src-tauri/resources/supplier/9.9.9/CANONICAL_DISTRIBUTION.json'
        target.parent.mkdir(parents=True); target.write_text(json.dumps(record))
        value = coverage.build(self.repo)
        self.assertEqual(value['supplier_pin'], '9.9.9')
        self.assertIn('Supplier component table', {o['name'] for o in value['open']})


if __name__ == '__main__':
    unittest.main()
