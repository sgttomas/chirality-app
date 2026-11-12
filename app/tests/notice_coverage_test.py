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
                'app/packaging/supplier_notices', 'app/src/fonts', 'app/src-tauri/icons')
TABLE = 'app/packaging/supplier_notices/components.json'
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

    def edit(self, relative, change, rebind=True):
        """Edit a JSON input. A curated input's review record is rebound too, as its reviewer would, unless rebind=False,
        so that each test exercises the rule after review rather than only the record's refusal."""
        path = self.repo / relative
        value = json.loads(path.read_text()); change(value); path.write_text(json.dumps(value, indent=1) + '\n')
        if rebind and relative in coverage.REVIEWED_FILES:
            self.rebind()

    def rebind(self):
        record = json.loads((self.repo / coverage.REVIEW).read_text())
        record['files_sha256'] = {f: hashlib.sha256((self.repo / f).read_bytes()).hexdigest() for f in record['files_sha256']}
        record['supplier_components'] = coverage.review_entries(json.loads((self.repo / TABLE).read_text()))
        (self.repo / coverage.REVIEW).write_text(json.dumps(record, indent=1) + '\n')


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

    def test_general_extraction_refuses_two_notice_members_for_one_name(self):
        for members in ({'LICENSE': b'one\n', 'license': b'two\n'}, {'LICENSE-MIT': b'one\n'}):
            raw = crate('invented-crate', '1.0.0', members)
            if len(members) == 1:  # the same name twice in one archive
                buffer = io.BytesIO()
                with tarfile.open(fileobj=io.BytesIO(raw)) as source, tarfile.open(fileobj=buffer, mode='w:gz') as target:
                    for member in source.getmembers():
                        target.addfile(member, source.extractfile(member))
                    info = tarfile.TarInfo('invented-crate-1.0.0/LICENSE-MIT'); info.size = 4
                    target.addfile(info, io.BytesIO(b'two\n'))
                raw = buffer.getvalue()
            with self.subTest(members=sorted(members)):
                folder = Path(tempfile.mkdtemp(dir=self.repo.parent))
                (folder / 'invented-crate-1.0.0.crate').write_bytes(raw)
                (folder / 'Cargo.lock').write_text('version = 4\n[[package]]\nname = "invented-crate"\nversion = "1.0.0"\n'
                                                   'source = "registry+https://github.com/rust-lang/crates.io-index"\n'
                                                   f'checksum = "{hashlib.sha256(raw).hexdigest()}"\n')
                with self.assertRaisesRegex(ValueError, 'two notice members'):
                    texts.crate_texts(folder / 'Cargo.lock', folder, folder / 'out')
                self.assertFalse((folder / 'out').exists())

    def test_overlay_maps_every_shipped_text_once(self):
        overlay = json.loads((ROOT / texts.OVERLAY).read_text())
        self.assertEqual(overlay, texts.overlay(ROOT))
        destinations = list(overlay['bundle']['resources'].values())
        self.assertEqual(len(destinations), len(set(destinations)))
        for relative in texts.planned(ROOT):
            self.assertEqual(overlay['bundle']['resources']['../packaging/notices/transitive/' + relative],
                             'third-party-notices/transitive/' + relative)


class Account(Copy):
    def build(self):
        (self.repo / texts.OVERLAY).write_text(json.dumps(texts.overlay(self.repo), indent=2) + '\n')
        return coverage.build(self.repo)

    def row(self, value, name, version=None):
        return next(c for c in value['components'] if c['name'] == name and (version is None or c['version'] == version))

    # Review finding 1: V8's subdirectory licences ship, and each root-text supplier row says what was looked at below the root.
    def test_v8_ships_its_third_party_licences_and_root_text_rows_state_their_extent(self):
        account = json.loads((ROOT / coverage.ACCOUNT).read_text())
        v8 = self.row(account, 'V8')
        third = sorted(t['source_path'] for t in v8['texts'] if t['source_path'].startswith('third_party/'))
        self.assertEqual(len(third), 16)
        self.assertIn('third_party/inspector_protocol/LICENSE', third)
        self.assertTrue(all(t['package_path'].startswith('third-party-notices/supplier/') for t in v8['texts']))
        for component in account['components']:
            if component['class'] == 'supplier' and component['standing'] == 'covered':
                self.assertTrue(component.get('below_root'), component['id'])
        gaps = {c['id'] for c in account['components'] if c['standing'] == 'uncovered'}
        self.assertTrue({'libcxx-credits-and-subdirectories', 'libcxxabi-credits-and-subdirectories', 'llvm-libc-subdirectories'} <= gaps)

    # Review finding 2: deleting the uncovered supplier groups cannot make the strict check pass.
    def test_deleting_compiled_dependency_rows_leaves_every_executable_uncovered(self):
        self.edit(TABLE, lambda v: v.update(components=[c for c in v['components'] if c.get('kind') != coverage.COMPILED]))
        value = self.build()
        executables = texts.executables(texts.supplier_record(self.repo)[2])
        self.assertEqual(len(executables), 5)
        open_names = {o['name'] for o in value['open']}
        for path in executables:
            self.assertIn('Dependencies compiled into ' + path, open_names)
        with self.assertRaisesRegex(ValueError, 'dropped without a reviewed statement'): coverage.generate(self.repo)

    # Round 2 finding 2: no table entry can make compiled-in dependencies covered in this change.
    def test_compiled_dependency_rows_stay_uncovered_whatever_the_table_says(self):
        lock = 'app/src-tauri/Cargo.lock'
        for item_id in ('codex-crate-dependencies', 'ripgrep-crate-dependencies'):
            self.edit(TABLE, lambda v, i=item_id: next(c for c in v['components'] if c['id'] == i).update(
                standing='covered', texts=['app/packaging/supplier_notices/codex/LICENSE'],
                lockfile={'path': lock, 'sha256': hashlib.sha256((self.repo / lock).read_bytes()).hexdigest()}))
        value = self.build()
        for item_id in ('codex-crate-dependencies', 'ripgrep-crate-dependencies'):
            self.assertEqual(next(c for c in value['components'] if c.get('id') == item_id)['standing'], coverage.UNCOVERED)

    def test_a_dropped_component_needs_a_reviewed_statement(self):
        base = self.repo.parent / 'base.json'; shutil.copyfile(ROOT / coverage.ACCOUNT, base)
        self.edit(TABLE, lambda v: v.update(components=[c for c in v['components'] if c['id'] != 'llvm-libc-subdirectories']))
        value = self.build()
        self.assertEqual(coverage.removed(json.loads(base.read_text()), value, json.loads((self.repo / texts.INPUTS).read_text())),
                         ['supplier:llvm-libc-subdirectories'])
        with self.assertRaisesRegex(ValueError, 'dropped without a reviewed statement'): coverage.generate(self.repo)
        self.edit(texts.INPUTS, lambda v: v['removed_components'].append({'key': 'supplier:llvm-libc-subdirectories', 'reason': 'invented'}))
        coverage.generate(self.repo)
        coverage.check(self.repo, base_account=base)

    # Review finding 3: only an affirmative reading in the closed form covers; nothing falls back to covered without one.
    def test_a_pending_or_missing_reading_is_pending_and_strict_refuses(self):
        self.edit(texts.INPUTS, lambda v: v['owner_licence_readings'][0].update(answer='INVENTED: pending owner reading'))
        value = self.build()
        first = json.loads((ROOT / texts.INPUTS).read_text())['owner_licence_readings'][0]['package']
        self.assertEqual(self.row(value, first)['standing'], coverage.HELD)
        self.setUp(); self.edit(texts.INPUTS, lambda v: v['owner_licence_readings'][1].update(statement='INVENTED words'))
        self.assertEqual(sum(c['standing'] == coverage.HELD for c in self.build()['components'] if c['class'] == 'cargo'), 1)
        self.setUp(); self.edit(texts.INPUTS, lambda v: v.update(owner_licence_readings=[]))
        value = self.build()
        held = {c['name'] for c in value['components'] if c['standing'] == coverage.HELD and c['class'] == 'cargo'}
        self.assertEqual(len(held), 9)
        self.assertTrue({'objc2-encode', 'objc2-exception-helper', 'objc2-core-foundation', 'objc2-web-kit'} <= held)

    def test_a_reading_cannot_be_extended_to_a_crate_that_needs_none(self):
        self.edit(texts.INPUTS, lambda v: v['owner_licence_readings'].append(
            {**v['owner_licence_readings'][0], 'package': 'serde', 'version': '1.0.229'}))
        with self.assertRaisesRegex(ValueError, 'needs none'): self.build()

    # Review finding 5: notices join by ecosystem, name and version.
    def test_direct_notices_join_by_version(self):
        account = json.loads((ROOT / coverage.ACCOUNT).read_text())
        cargo = [c for c in account['components'] if c['class'] == 'cargo']
        self.assertEqual(sum(c['relation'] == 'direct' for c in cargo), 18)
        self.assertEqual(sum(c['relation'] == 'transitive' for c in cargo), 174)
        old = self.row(account, 'getrandom', '0.3.4')
        self.assertEqual(old['relation'], 'transitive')
        self.assertTrue(all('/getrandom/0.3.4/' in t['package_path'] for t in old['texts']))
        for component in cargo + [c for c in account['components'] if c['class'] == 'npm']:
            for text in component['texts']:
                self.assertIn(f"/{component['name']}/{component['version']}/", text['package_path'])

    # Smaller finding: the bundled icon has a row, and an icon without provenance stands uncovered.
    def test_bundled_icon_needs_provenance(self):
        account = json.loads((ROOT / coverage.ACCOUNT).read_text())
        self.assertEqual(self.row(account, 'App icon icons/icon.png')['standing'], coverage.COVERED)
        (self.repo / 'app/src-tauri/icons/icon.png').write_bytes(b'INVENTED icon')
        with self.assertRaisesRegex(ValueError, 'differs from its provenance'): self.build()
        self.setUp(); self.edit(texts.INPUTS, lambda v: v.update(app_assets=[]))
        self.assertEqual(self.row(self.build(), 'App icon icons/icon.png')['standing'], coverage.UNCOVERED)

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

    def test_supplier_table_must_claim_every_member_and_justify_gaps(self):
        table = TABLE
        self.edit(table, lambda v: v['components'].pop(next(i for i, c in enumerate(v['components']) if c['id'] == 'zlib')))
        with self.assertRaisesRegex(ValueError, 'claimed by no component'): coverage.build(self.repo)
        self.setUp()
        self.edit(table, lambda v: next(c for c in v['components'] if c['id'] == 'libcxx-credits-and-subdirectories').pop('would_close'))
        with self.assertRaises((ValueError, KeyError)): coverage.build(self.repo)
        self.setUp()
        self.edit(table, lambda v: next(c for c in v['components'] if c['id'] == 'opus').update(members=['codex-resources/voice/lib/invented.dylib']))
        with self.assertRaisesRegex(ValueError, 'not in the tree'): coverage.build(self.repo)

    # Round 2 finding 1: a curated input cannot change without its review record; removals fail a test in the same change.
    def test_curated_input_changes_refuse_without_the_review_record(self):
        def drop_icu(v):
            v['components'] = [c for c in v['components'] if c['id'] != 'icu']
            v['texts'] = [t for t in v['texts'] if 'icu-d578f2e8' not in t['path']]
        self.edit(TABLE, drop_icu, rebind=False)
        shutil.rmtree(self.repo / 'app/packaging/supplier_notices/icu-d578f2e8')
        with self.assertRaisesRegex(ValueError, 'differs from the review record'): self.build()
        self.setUp(); self.edit(texts.INPUTS, lambda v: v['owner_licence_readings'].pop(), rebind=False)
        with self.assertRaisesRegex(ValueError, 'differs from the review record'): self.build()
        # A cache-made index claiming a text that was never extracted is a change the record must also make.
        self.setUp()
        self.edit('app/packaging/notices/transitive-index.json', lambda v: next(r for r in v['cargo'] if r['package'] == 'vsimd')
                  ['text'].update(kind='archive-member'), rebind=False)
        with self.assertRaisesRegex(ValueError, 'differs from the review record'): self.build()
        self.setUp()
        record = json.loads((self.repo / coverage.REVIEW).read_text())
        record['supplier_components'] = [c for c in record['supplier_components'] if c['id'] != 'icu']
        (self.repo / coverage.REVIEW).write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, 'differ from the review record'): self.build()

    def test_expected_supplier_components(self):
        expected = {
            'codex': 'covered', 'codex-skill-creator-sample': 'covered', 'codex-skill-installer-sample': 'covered',
            'codex-crate-dependencies': 'uncovered', 'ripgrep': 'covered', 'pcre2-sys': 'covered', 'pcre2-in-rg': 'covered',
            'sljit-in-rg': 'covered', 'ripgrep-crate-dependencies': 'uncovered', 'v8': 'covered', 'rusty_v8': 'covered',
            'icu': 'pending', 'libcxx': 'covered', 'libcxxabi': 'covered', 'llvm-libc': 'covered',
            'libcxx-credits-and-subdirectories': 'uncovered', 'libcxxabi-credits-and-subdirectories': 'uncovered',
            'llvm-libc-subdirectories': 'uncovered', 'highway': 'covered', 'fast_float': 'covered', 'simdutf': 'covered',
            'dragonbox': 'covered', 'fp16': 'covered', 'abseil-cpp': 'covered', 'gstreamer': 'covered',
            'gst-plugins-base': 'covered', 'gst-plugins-good': 'covered', 'glib': 'covered', 'proxy-libintl': 'covered',
            'libffi': 'covered', 'pcre2-voice': 'covered', 'opus': 'covered', 'zlib': 'covered'}
        table = json.loads((ROOT / TABLE).read_text())
        self.assertEqual({c['id']: c['standing'] for c in table['components']}, expected)
        account = json.loads((ROOT / coverage.ACCOUNT).read_text())
        standing = {'covered': coverage.COVERED, 'pending': coverage.HELD, 'uncovered': coverage.UNCOVERED}
        self.assertEqual({c['id']: c['standing'] for c in account['components'] if c['class'] == 'supplier'},
                         {k: standing[v] for k, v in expected.items()})

    # Round 2 finding 3: a supplier text is bound to its component's repository and revision.
    def test_supplier_texts_must_match_their_component(self):
        icu = 'app/packaging/supplier_notices/icu-d578f2e8/LICENSE'
        self.edit(TABLE, lambda v: next(c for c in v['components'] if c['id'] == 'v8')['texts'].append(icu))
        self.assertEqual(self.row(self.build(), 'V8')['standing'], coverage.UNCOVERED)
        self.setUp(); self.edit(TABLE, lambda v: next(c for c in v['components'] if c['id'] == 'v8').update(version='99.0', revision='c' * 40))
        self.assertEqual(self.row(self.build(), 'V8')['standing'], coverage.UNCOVERED)
        self.setUp(); self.edit(TABLE, lambda v: next(c for c in v['components'] if c['id'] == 'pcre2-sys').pop('text_exceptions'))
        self.assertEqual(self.row(self.build(), 'pcre2-sys')['standing'], coverage.UNCOVERED)

    def test_removing_a_v8_text_needs_the_review_record(self):
        self.edit(TABLE, lambda v: next(c for c in v['components'] if c['id'] == 'v8')['texts'].remove(
            'app/packaging/supplier_notices/v8-15.2.124.1/third_party/inspector_protocol/LICENSE'), rebind=False)
        with self.assertRaisesRegex(ValueError, 'review record'): self.build()

    # Round 2 finding 4: fonts without recorded upstream evidence are uncovered.
    def test_unverified_fonts_are_uncovered(self):
        def unverify(v):
            v['source']['declared_upstream_verified'] = False
            v['upstream_packages'] = []
            for entry in v['licenses'] + v['fonts']:
                entry.pop('upstream')
        self.edit('app/packaging/font_notice/index.json', unverify)
        fonts = [c for c in self.build()['components'] if c['class'] == 'font']
        self.assertEqual(len(fonts), 3)
        self.assertTrue(all(c['standing'] == coverage.UNCOVERED and not c['texts'] for c in fonts))

    # Round 2 finding 5: ICU is pending the owner's reading, and the strict check names it.
    def test_icu_is_pending_with_the_named_files_stated(self):
        account = json.loads((ROOT / coverage.ACCOUNT).read_text())
        icu = next(c for c in account['components'] if c.get('id') == 'icu')
        self.assertEqual(icu['standing'], coverage.HELD)
        for name in ('aclocal.m4', 'config.guess', 'icu.BUILD.bazel', 'not held'):
            self.assertIn(name, icu['reason'])
        self.assertEqual([o['name'] for o in account['open'] if o['standing'] == coverage.HELD], ['ICU (V8 dependency)'])
        self.assertEqual(account['counts'][coverage.UNCOVERED], 5)

    # Round 2 finding 6: the executable rule must fit the record's Mach-O count.
    def test_executable_rule_must_fit_the_record_macho_count(self):
        path = texts.supplier_record(self.repo)[1]
        record = json.loads((self.repo / path).read_text()); record['macho_files'] += 1
        (self.repo / path).write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, 'Mach-O count'): self.build()

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
