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
REVIEWED_PIN = json.loads((ROOT / 'app/packaging/supplier_notices/components.json').read_text())['reviewed_for_pin']
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
    # The pin the copy declares: None keeps the repository's declared pin. A subclass naming the table's reviewed pin
    # exercises the supplier rules where they apply, with the review record bound to that pin's distribution record.
    PIN = None

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name).resolve() / 'repo'
        for relative in COPIED_TREES:
            shutil.copytree(ROOT / relative, self.repo / relative)
        for relative in COPIED_FILES:
            (self.repo / relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, self.repo / relative)
        for item in json.loads((NOTICES / 'coverage-inputs.json').read_text())['app_resources']:
            for pair in item['mappings']:
                target = self.repo / pair['source']
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / pair['source'], target)
        declared = texts.declared_pin(ROOT)
        pin = self.PIN or declared
        record = f'app/src-tauri/resources/supplier/{pin}/CANONICAL_DISTRIBUTION.json'
        (self.repo / record).parent.mkdir(parents=True); shutil.copyfile(ROOT / record, self.repo / record)
        for content in json.loads((NOTICES / 'coverage-inputs.json').read_text())['library_content']:
            shutil.copytree(ROOT / content['resource'], self.repo / content['resource'])
        if pin != declared:
            hosting = self.repo / texts.HOSTING
            hosting.write_text(hosting.read_text().replace(f'DECLARED_PIN: &str = "{declared}"', f'DECLARED_PIN: &str = "{pin}"'))
            self.assertEqual(texts.declared_pin(self.repo), pin)
            self.rebind()

    def edit(self, relative, change, rebind=True):
        """Edit a JSON input. A curated input's review record is rebound too, as its reviewer would, unless rebind=False,
        so that each test exercises the rule after review rather than only the record's refusal."""
        path = self.repo / relative
        value = json.loads(path.read_text()); change(value); path.write_text(json.dumps(value, indent=1) + '\n')
        if rebind and relative in json.loads((self.repo / coverage.REVIEW).read_text())['files_sha256']:
            self.rebind()

    def rebind(self):
        record = json.loads((self.repo / coverage.REVIEW).read_text())
        files = [*coverage.REVIEWED_FILES, texts.supplier_record(self.repo)[1]]
        record['files_sha256'] = {f: hashlib.sha256((self.repo / f).read_bytes()).hexdigest() for f in files}
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


class Builds(Copy):
    def build(self):
        (self.repo / texts.OVERLAY).write_text(json.dumps(texts.overlay(self.repo), indent=2) + '\n')
        return coverage.build(self.repo)

    def row(self, value, name, version=None):
        return next(c for c in value['components'] if c['name'] == name and (version is None or c['version'] == version))


class DeclaredPin(Builds):
    """The repository as it stands: the declared pin, whatever the table was reviewed for."""

    def test_copied_inputs_regenerate_the_same_account(self):
        self.assertEqual(coverage.encode(coverage.build(self.repo)), (ROOT / coverage.ACCOUNT).read_bytes())

    def test_stale_account_refuses(self):
        self.edit(coverage.ACCOUNT, lambda v: v['counts'].update(covered=0))
        with self.assertRaisesRegex(ValueError, 'stale'): coverage.check(self.repo)

    # A table reviewed for another pin carries none of its associations forward: no supplier row counts as covered.
    def test_a_table_reviewed_for_another_pin_covers_no_supplier_row(self):
        other = REVIEWED_PIN
        if texts.declared_pin(self.repo) == REVIEWED_PIN:
            # The table is reviewed for the declared pin; mark it reviewed for another to exercise the rule.
            other = '0.167.0'
            self.edit(TABLE, lambda v: v.update(reviewed_for_pin=other))
        value = self.build()
        supplier = [c for c in value['components'] if c['class'] == 'supplier']
        self.assertEqual([c['id'] for c in supplier if c['standing'] != coverage.UNCOVERED], [])
        table = self.row(value, 'Supplier component table')
        self.assertEqual(table['mappings'], [coverage.vendor_mapping(texts.supplier_record(self.repo)[1],
                                                                     {m: 1 for m in table['members']})])
        for row in supplier:
            if row['id'] in coverage.DEFERRED:
                self.assertNotIn('not carried forward', row['reason'])
            elif row['id'] != 'component-table':
                self.assertIn(f'associates this row for {other}, not for the declared pin', row['reason'])
                self.assertNotIn('mappings', row)
        if other == REVIEWED_PIN:
            self.assertEqual(value, json.loads((ROOT / coverage.ACCOUNT).read_text()))

    def test_another_declared_pin_is_named_as_an_open_review_not_assumed(self):
        pin = texts.declared_pin(ROOT)
        hosting = self.repo / texts.HOSTING
        hosting.write_text(hosting.read_text().replace(f'DECLARED_PIN: &str = "{pin}"', 'DECLARED_PIN: &str = "9.9.9"'))
        record = json.loads((ROOT / f'app/src-tauri/resources/supplier/{pin}/CANONICAL_DISTRIBUTION.json').read_text())
        record['pin'] = '9.9.9'
        target = self.repo / 'app/src-tauri/resources/supplier/9.9.9/CANONICAL_DISTRIBUTION.json'
        target.parent.mkdir(parents=True); target.write_text(json.dumps(record))
        # A pin move changes which distribution record is bound, so the review record must change with it.
        with self.assertRaisesRegex(ValueError, 'declared pin\'s distribution record'): coverage.build(self.repo)
        review = json.loads((self.repo / coverage.REVIEW).read_text())
        review['files_sha256'].pop(f'app/src-tauri/resources/supplier/{pin}/CANONICAL_DISTRIBUTION.json')
        review['files_sha256']['app/src-tauri/resources/supplier/9.9.9/CANONICAL_DISTRIBUTION.json'] = hashlib.sha256(target.read_bytes()).hexdigest()
        (self.repo / coverage.REVIEW).write_text(json.dumps(review))
        value = coverage.build(self.repo)
        self.assertEqual(value['supplier_pin'], '9.9.9')
        self.assertIn('Supplier component table', {o['name'] for o in value['open']})


class Account(Builds):
    """The supplier rules where they apply: the copy declares the pin the table was reviewed for."""
    PIN = REVIEWED_PIN

    # Review finding 1: V8's subdirectory licences ship, and each root-text supplier row says what was looked at below the root.
    def test_v8_ships_its_third_party_licences_and_root_text_rows_state_their_extent(self):
        account = self.build()
        v8 = self.row(account, 'V8')
        third = sorted(t['source_path'] for t in v8['texts'] if t['source_path'].startswith('third_party/'))
        self.assertEqual(len(third), 16)
        self.assertIn('third_party/inspector_protocol/LICENSE', third)
        self.assertTrue(all(t['package_path'].startswith('third-party-notices/supplier/') for t in v8['texts']))
        for component in account['components']:
            if component['class'] == 'supplier' and component['standing'] == 'covered':
                self.assertTrue(component.get('below_root'), component['id'])
        # The LLVM rows below the root are covered by CREDITS.TXT and complete listings, and say what stays unexamined.
        for row_id in ('libcxx-credits-and-subdirectories', 'libcxxabi-credits-and-subdirectories', 'llvm-libc-subdirectories'):
            row = next(c for c in account['components'] if c.get('id') == row_id)
            self.assertEqual(row['standing'], coverage.COVERED)
            self.assertIn('Per-file terms', row['below_root'])
            self.assertIn('not excluded', row['below_root'])

    # Review finding 2: deleting the uncovered supplier groups cannot make the strict check pass.
    def test_deleting_compiled_dependency_rows_leaves_every_executable_uncovered(self):
        executables = texts.executables(texts.supplier_record(self.repo)[2])
        self.assertEqual(len(executables), 5)
        # Deleted, or kept but no longer marked as compiled dependencies, while a lockfile association still names them:
        # refused (review round 3, finding 3), rather than covered by another route.
        for change in (lambda v: v.update(components=[c for c in v['components'] if c.get('kind') != coverage.COMPILED]),
                       lambda v: [c.pop('kind') and c.update(standing='uncovered', reason='INVENTED', would_close='INVENTED')
                                  for c in v['components'] if c.get('kind') == coverage.COMPILED]):
            with self.subTest(change=change):
                self.setUp(); self.edit(TABLE, change)
                with self.assertRaisesRegex(ValueError, 'names a component that is not a compiled-dependencies row'):
                    self.build()
        # An executable moved to a row that is not compiled dependencies still gets its own uncovered row.
        def move(v):
            row = next(c for c in v['components'] if c['id'] == 'codex-crate-dependencies')
            row['members'].remove('bin/codex-exec-server')
            next(c for c in v['components'] if c['id'] == 'codex')['members'].append('bin/codex-exec-server')
        with self.subTest(change='moved'):
            self.setUp(); self.edit(TABLE, move)
            open_names = {o['name'] for o in self.build()['open']}
            self.assertIn('Dependencies compiled into bin/codex-exec-server', open_names)

    def test_empty_workspace_texts_cannot_leave_ripgrep_covered(self):
        crates = texts.supplier_crates
        row = next(c for c in self.build()['components'] if c.get('id') == 'ripgrep-crate-dependencies')
        self.assertEqual(row['standing'], coverage.COVERED)
        self.edit(crates.ASSOCIATIONS,
                  lambda v: next(w for w in v['workspaces'] if w['lock'] == 'ripgrep').update(texts=[]))
        # Even after the curated binding is updated, neither regeneration nor the gate accepts a textless package.
        for operation in (crates.packages, crates.check, coverage.build):
            with self.subTest(operation=operation.__name__):
                with self.assertRaisesRegex(ValueError, 'texts must be a non-empty list'):
                    operation(self.repo)

    # Round 2 finding 2, with the rule the 0.169.0 crate group adds: a compiled-dependencies row is covered only when every
    # package its associated lockfile locks has its text; no table entry makes it covered.
    def test_compiled_dependency_rows_are_covered_only_by_their_crate_group(self):
        crates_dir = 'app/packaging/supplier_notices/crates'
        value = self.build()
        rows = {c['id']: c for c in value['components'] if c['class'] == 'supplier'}
        codex, rg = rows['codex-crate-dependencies'], rows['ripgrep-crate-dependencies']
        self.assertEqual((rg['standing'], rg['packages']['total'], rg['packages']['gap']), (coverage.COVERED, 59, 0))
        self.assertEqual(codex['standing'], coverage.UNCOVERED)
        packages = codex['packages']
        self.assertEqual((packages['total'], packages['text'], packages['gap'], packages['held'], packages['no-publisher-text'],
                          packages['not-in-macos-package']), (1483, 1393, 53, 23, 8, 6))
        # Held, gap and no-publisher-text packages are open; recorded absence is not, and each absent package is named.
        self.assertEqual(len(codex['open_packages']), 84)
        self.assertEqual(sorted(p['name'] for p in codex['excluded_packages']),
                         ['linux-keyutils', 'rustls-platform-verifier-android', 'socks5-protocol', 'winapi-i686-pc-windows-gnu',
                          'winapi-x86_64-pc-windows-gnu', 'winsplit'])
        self.assertTrue(all(p['absence']['reverse_dependencies'] for p in codex['excluded_packages']))
        self.assertIn('some may not be compiled', codex['packages']['superset'])
        self.assertIn('objc2-foundation 0.3.2', codex['reason'])
        self.assertIn('crc32c 0.6.8', codex['reason'])
        # The table cannot claim covered for an open group.
        self.setUp(); self.edit(TABLE, lambda v: next(c for c in v['components'] if c['id'] == 'codex-crate-dependencies').update(standing='covered'))
        with self.assertRaisesRegex(ValueError, 'the table says covered'): self.build()
        # A package losing its archive notices opens the ripgrep group (and the table must say so).
        found = {}
        def drop(v):
            row = next(r for r in v['registry'] if r['locks'] == ['ripgrep'] and r['notices'])
            row['notices'] = []
            found['package'] = row['package'] + ' ' + row['version']
        self.setUp(); self.edit(crates_dir + '/index.json', drop)
        crates = texts.supplier_crates
        wanted = set(crates.wanted_texts(self.repo))
        for text in (self.repo / crates.TEXTS).iterdir():
            if text.name not in wanted:
                text.unlink()
        (self.repo / crates.PACKAGES).write_bytes(crates.encode(crates.packages(self.repo)))
        self.edit(TABLE, lambda v: next(c for c in v['components'] if c['id'] == 'ripgrep-crate-dependencies').update(
            standing='uncovered', reason='INVENTED', would_close='INVENTED'))
        row = next(c for c in self.build()['components'] if c.get('id') == 'ripgrep-crate-dependencies')
        self.assertEqual(row['standing'], coverage.UNCOVERED)
        self.assertIn(found['package'], row['reason'])
        # Dropping a lockfile's association, or naming another revision for it, refuses.
        self.setUp(); self.edit(crates_dir + '/associations.json', lambda v: v.update(locks=[l for l in v['locks'] if l['id'] != 'ripgrep']))
        with self.assertRaisesRegex(ValueError, 'crate index differs from the lockfiles'): self.build()
        # The lock alone moved: its own workspace entry no longer matches it (review round 4, finding 4).
        self.setUp(); self.edit(crates_dir + '/associations.json', lambda v: next(l for l in v['locks'] if l['id'] == 'ripgrep').update(revision='e' * 40))
        with self.assertRaisesRegex(ValueError, 'a workspace association names another repository or revision than its lockfile: ripgrep'):
            crates.packages(self.repo)
        # The lock and its workspace moved together: the component compares them as written, with main's refusal.
        def move(v):
            for item in (next(l for l in v['locks'] if l['id'] == 'ripgrep'), next(w for w in v['workspaces'] if w['lock'] == 'ripgrep')):
                item.update(revision='e' * 40)
        self.setUp(); self.edit(crates_dir + '/associations.json', move)
        (self.repo / crates.PACKAGES).write_bytes(crates.encode(crates.packages(self.repo)))
        with self.assertRaisesRegex(ValueError, "the crate group's lockfile is for another repository or revision than the component"):
            self.build()
        # A lockfile whose bytes drift refuses.
        self.setUp(); lock = self.repo / crates_dir / 'locks/ripgrep.Cargo.lock'; lock.write_bytes(lock.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'lockfile differs'): self.build()

    # App Agent 0's condition: packages that state a licence with no publisher text are open, never covered; an account
    # whose only open packages are of that kind still fails --strict.
    def test_no_publisher_text_alone_keeps_the_account_open_and_strict_refuses(self):
        from unittest.mock import patch
        crates = coverage.texts.supplier_crates  # the module coverage.py itself calls
        # Invented for this copy: the other open supplier rows ship the skill-creator text, so only the crate group is open.
        creator = 'app/packaging/supplier_notices/codex-skills-086ccc83/skill-creator/license.txt'

        def close_others(v):
            for c in v['components']:
                if c['id'] in ('codex-skill-imagegen-sample', 'codex-skill-openai-docs-sample', 'codex-vendored-bubblewrap'):
                    c.update(texts=[creator], standing='covered'); c.pop('reason'); c.pop('would_close')
        self.edit(TABLE, close_others)
        real = crates.group

        def only_no_publisher_text(repo, component):
            value = real(repo, component)
            if value is None or component != 'codex-crate-dependencies':
                return value
            donor = next(r for r in value['packages'] if r['standing'] == 'text' and r['texts'])
            rows = []
            for row in value['packages']:
                if row['standing'] in ('held', 'gap'):
                    row = {k: v for k, v in row.items() if k not in ('reason', 'would_close')}
                    row.update(standing='text', texts=row['texts'] or donor['texts'], basis='INVENTED')
                rows.append(row)
            return {**value, 'packages': rows}
        with patch.object(crates, 'group', only_no_publisher_text):
            value = self.build()
            codex = next(c for c in value['components'] if c.get('id') == 'codex-crate-dependencies')
            self.assertEqual({p['standing'] for p in codex['open_packages']}, {'no-publisher-text'})
            self.assertEqual(len(codex['open_packages']), 8)
            self.assertEqual(codex['standing'], coverage.UNCOVERED)
            self.assertEqual([o['name'] for o in value['open']], [codex['name']])
            self.assertIn('8 state a licence with no publisher text found', codex['reason'])
            # The strict check refuses this account.
            (self.repo / coverage.ACCOUNT).write_bytes(coverage.encode(value))
            real_check = coverage.check
            with patch.object(coverage, 'check', lambda **kw: real_check(self.repo, **kw)), \
                    patch.object(sys, 'argv', ['coverage.py', 'check', '--strict']), \
                    patch('sys.stdout', io.StringIO()), patch('sys.stderr', io.StringIO()) as err:
                self.assertEqual(coverage.main(), 1)
            self.assertIn('not covered: ' + codex['name'], err.getvalue())
            # Nothing turns these packages covered: the table cannot say so.
            self.edit(TABLE, lambda v: next(c for c in v['components'] if c['id'] == 'codex-crate-dependencies').update(standing='covered'))
            with self.assertRaisesRegex(ValueError, 'the table says covered'): self.build()

    def test_a_dropped_component_needs_a_reviewed_statement(self):
        # The account as the reviewed copy generates it is the base and the committed account the generator compares with.
        base = self.repo.parent / 'base.json'; base.write_bytes(coverage.encode(self.build()))
        shutil.copyfile(base, self.repo / coverage.ACCOUNT)
        self.edit(TABLE, lambda v: v.update(components=[c for c in v['components'] if c['id'] != 'fp16']))
        value = self.build()
        self.assertEqual(coverage.removed(json.loads(base.read_text()), value, json.loads((self.repo / texts.INPUTS).read_text())),
                         ['supplier:fp16'])
        with self.assertRaisesRegex(ValueError, 'dropped without a reviewed statement'): coverage.generate(self.repo)
        self.edit(texts.INPUTS, lambda v: v['removed_components'].append({'key': 'supplier:fp16', 'reason': 'invented'}))
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
        objc2 = [c for c in account['components'] if 'owner_licence_reading' in c and c['class'] == 'cargo']
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

    def test_removed_text_turns_a_crate_uncovered_rather_than_hiding_it(self):
        self.edit(texts.INPUTS, lambda v: v.update(received_texts=[t for t in v['received_texts'] if 'nugine' not in t['path']]))
        shutil.rmtree(self.repo / texts.TEXTS / 'cargo/vsimd'); shutil.rmtree(self.repo / texts.TEXTS / 'cargo/uuid-simd')
        (self.repo / texts.OVERLAY).write_text(json.dumps(texts.overlay(self.repo), indent=2) + '\n')
        value = coverage.build(self.repo)
        self.assertEqual({o['name'] for o in value['open'] if o['standing'] == coverage.UNCOVERED} & {'vsimd', 'uuid-simd'},
                         {'vsimd', 'uuid-simd'})

    def test_supplier_table_must_claim_every_member_and_justify_gaps(self):
        table = TABLE
        self.edit(table, lambda v: next(c for c in v['components'] if c['id'] == 'zlib').update(members=[]))
        with self.assertRaisesRegex(ValueError, 'claimed by no component'): coverage.build(self.repo)
        # Dropping a voice row also leaves a library of the supplier's sources.json that no row accounts for.
        self.setUp()
        self.edit(table, lambda v: v['components'].pop(next(i for i, c in enumerate(v['components']) if c['id'] == 'zlib')))
        with self.assertRaisesRegex(ValueError, 'no voice row accounts for: zlib'): coverage.build(self.repo)
        self.setUp()
        self.edit(table, lambda v: next(c for c in v['components'] if c['id'] == 'fp16').update(standing='uncovered'))
        with self.assertRaises((ValueError, KeyError)): coverage.build(self.repo)
        self.setUp()
        self.edit(table, lambda v: next(c for c in v['components'] if c['id'] == 'opus').update(members=['codex-resources/voice/lib/invented.dylib']))
        with self.assertRaisesRegex(ValueError, 'not in the tree|supplier manifest does not list'): coverage.build(self.repo)

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
        # At 0.169.0: the voice rows are established by the supplier's voice records; three rows are new and open.
        expected = {
            'codex': 'covered', 'codex-skill-creator-sample': 'covered', 'codex-skill-installer-sample': 'covered',
            'codex-skill-imagegen-sample': 'uncovered', 'codex-skill-openai-docs-sample': 'uncovered',
            'codex-vendored-bubblewrap': 'uncovered',
            'codex-crate-dependencies': 'uncovered', 'ripgrep': 'covered', 'pcre2-sys': 'covered', 'pcre2-in-rg': 'covered',
            'sljit-in-rg': 'covered', 'ripgrep-crate-dependencies': 'covered', 'v8': 'covered', 'rusty_v8': 'covered',
            'icu': 'covered', 'libcxx': 'covered', 'libcxxabi': 'covered', 'llvm-libc': 'covered',
            'libcxx-credits-and-subdirectories': 'covered', 'libcxxabi-credits-and-subdirectories': 'covered',
            'llvm-libc-subdirectories': 'covered', 'highway': 'covered', 'fast_float': 'covered', 'simdutf': 'covered',
            'dragonbox': 'covered', 'fp16': 'covered', 'abseil-cpp': 'covered', 'gstreamer': 'covered',
            'gst-plugins-base': 'covered', 'gst-plugins-good': 'covered', 'glib': 'covered', 'proxy-libintl': 'covered',
            'libffi': 'covered', 'pcre2-voice': 'covered', 'opus': 'covered', 'zlib': 'covered'}
        table = json.loads((ROOT / TABLE).read_text())
        self.assertEqual({c['id']: c['standing'] for c in table['components']}, expected)
        account = self.build()
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

    # 0.169.0: a text committed at one revision serves another only through an also_at identity for the same blob.
    def test_also_at_identities_bind_a_text_to_another_revision_only_for_its_blob(self):
        self.assertEqual(self.row(self.build(), 'Codex', '0.169.0')['standing'], coverage.COVERED)
        def strip(v):
            next(t for t in v['texts'] if t['path'] == 'app/packaging/supplier_notices/codex/LICENSE').pop('also_at')
        self.setUp(); self.edit(TABLE, strip)
        row = self.row(self.build(), 'Codex', '0.169.0')
        self.assertEqual(row['standing'], coverage.UNCOVERED)
        self.assertIn('another repository or revision', row['reason'])
        def other_blob(v):
            next(t for t in v['texts'] if t['path'] == 'app/packaging/supplier_notices/codex/LICENSE')['also_at'][0]['git_blob_sha1'] = 'a' * 40
        self.setUp(); self.edit(TABLE, other_blob)
        with self.assertRaisesRegex(ValueError, 'also_at names another blob'): self.build()

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

    # Round 2 finding 5, answered: ICU is covered only by the owner's reading of 2026-11-15 in its closed form.
    def test_icu_is_covered_only_by_the_owners_closed_form_reading(self):
        table = json.loads((ROOT / TABLE).read_text())
        icu_item = next(c for c in table['components'] if c['id'] == 'icu')
        reading = icu_item['owner_licence_reading']
        self.assertEqual((reading['decided_by'], reading['date']), ('owner', '2026-11-15'))
        self.assertEqual(reading['answer'], "ICU's licence text as published is complete")
        self.assertEqual(reading['answer_description'], 'Nothing is added. The two files are build-system files, very likely '
                                                        'not compiled into or shipped with anything.')
        for name in ('aclocal.m4', 'config.guess', 'icu.BUILD.bazel', 'not held'):
            self.assertIn(name, icu_item['reading_context'])
        # Nothing is added to the ICU notice: it is still the one committed text, with its recorded bytes.
        self.assertEqual(icu_item['texts'], ['app/packaging/supplier_notices/icu-d578f2e8/LICENSE'])
        text = next(t for t in table['texts'] if t['path'] == icu_item['texts'][0])
        self.assertEqual(hashlib.sha256((ROOT / text['path']).read_bytes()).hexdigest(), text['sha256'])
        icu = next(c for c in self.build()['components'] if c.get('id') == 'icu')
        self.assertEqual(icu['standing'], coverage.COVERED)
        self.assertIn("owner licence reading (2026-11-15): ICU's licence text as published is complete", icu['basis'])
        self.assertEqual(icu['owner_licence_reading'], reading)

        def change(**fields):
            return lambda v: next(c for c in v['components'] if c['id'] == 'icu')['owner_licence_reading'].update(fields)
        for edit in (change(answer='Ship the two GPL texts as well'), change(answer_description='INVENTED stronger claim'),
                     change(question='INVENTED'), change(decided_by='agent'), change(date='15 November'),
                     lambda v: next(c for c in v['components'] if c['id'] == 'icu').pop('owner_licence_reading'),
                     lambda v: next(c for c in v['components'] if c['id'] == 'icu').update(standing='pending')):
            with self.subTest(edit=edit):
                self.setUp(); self.edit(TABLE, edit)
                self.assertEqual(next(c for c in self.build()['components'] if c.get('id') == 'icu')['standing'], coverage.HELD)
        # The reading covers ICU only.
        self.setUp(); self.edit(TABLE, lambda v: next(c for c in v['components'] if c['id'] == 'v8').update(owner_licence_reading=reading))
        with self.assertRaisesRegex(ValueError, 'needs none'): self.build()
        self.setUp(); self.edit(TABLE, lambda v: v.update(components=[c for c in v['components'] if c['id'] != 'icu']))
        with self.assertRaisesRegex(ValueError, 'awaiting a reading is missing'): self.build()

    # Round 2 finding 6: the executable rule must fit the record's Mach-O count.
    def test_executable_rule_must_fit_the_record_macho_count(self):
        path = texts.supplier_record(self.repo)[1]
        self.edit(path, lambda v: v.update(macho_files=v['macho_files'] + 1))
        with self.assertRaisesRegex(ValueError, 'Mach-O count'): self.build()

    # Round 3 finding 1: the declared pin's distribution record is a reviewed input; its digests cannot drift unseen.
    def test_distribution_record_drift_refuses(self):
        path = texts.supplier_record(self.repo)[1]
        def zero_opus(v):
            entry = next(e for e in v['inventory']['entries'] if e['path'] == 'codex-resources/voice/licenses/Opus.txt')
            entry['sha256'] = '0' * 64
        self.edit(path, zero_opus, rebind=False)
        with self.assertRaisesRegex(ValueError, 'differs from the review record'): self.build()

    # Round 3 finding 2: a deferred row has no route to covered, whatever the table and review record say. The five 0.167.0
    # ids were each established for 0.169.0 and removed; the guard itself stays.
    def test_deferred_rows_stay_uncovered_whatever_the_table_says(self):
        self.assertEqual(coverage.DEFERRED, ())
        original = coverage.DEFERRED
        self.addCleanup(setattr, coverage, 'DEFERRED', original)
        coverage.DEFERRED = ('llvm-libc-subdirectories', 'ripgrep-crate-dependencies')
        value = self.build()
        for row_id in coverage.DEFERRED:
            self.assertEqual(next(c for c in value['components'] if c.get('id') == row_id)['standing'], coverage.UNCOVERED)
        self.setUp(); self.edit(TABLE, lambda v: v.update(components=[c for c in v['components'] if c['id'] != 'llvm-libc-subdirectories']))
        with self.assertRaisesRegex(ValueError, 'deferred supplier row is missing'): self.build()

    # Round 3 finding 3: an empty exception reason or an absent text identity is not established.
    def test_empty_exception_reason_and_absent_identity_refuse(self):
        icu = 'app/packaging/supplier_notices/icu-d578f2e8/LICENSE'
        def empty_reason(v):
            v8 = next(c for c in v['components'] if c['id'] == 'v8')
            v8['texts'].append(icu); v8['text_exceptions'] = [{'path': icu, 'reason': ''}]
        self.edit(TABLE, empty_reason)
        with self.assertRaisesRegex(ValueError, 'non-empty reason'): self.build()
        self.setUp()
        def null_identity(v):
            v8 = next(c for c in v['components'] if c['id'] == 'v8')
            v8.update(repository=None, revision=None)
            for text in v['texts']:
                if text['path'] in v8['texts']:
                    text.update(repository=None, revision=None)
        self.edit(TABLE, null_identity)
        with self.assertRaisesRegex(ValueError, 'non-empty repository and revision'): self.build()
        self.setUp(); self.edit(TABLE, lambda v: next(c for c in v['components'] if c['id'] == 'v8').update(repository=None, revision=None))
        self.assertEqual(self.row(self.build(), 'V8')['standing'], coverage.UNCOVERED)

    # Round 4 finding 3: identity is checked before any text or exception, and a supplier-tree row needs its source URL.
    def test_a_component_whose_every_text_is_an_exception_still_needs_its_own_identity(self):
        def all_exceptions(v, identity):
            item = next(c for c in v['components'] if c['id'] == 'pcre2-sys')
            item.update(identity)
            item['text_exceptions'] = [{'path': p, 'reason': 'INVENTED: every text named as an exception'} for p in item['texts']]
        self.edit(TABLE, lambda v: all_exceptions(v, {}))
        self.assertEqual(self.row(self.build(), 'pcre2-sys')['standing'], coverage.COVERED)
        for identity in ({'repository': None, 'revision': None}, {'repository': None}, {'revision': None}, {'revision': ''}):
            with self.subTest(identity=identity):
                self.setUp(); self.edit(TABLE, lambda v, i=identity: all_exceptions(v, i))
                row = self.row(self.build(), 'pcre2-sys')
                self.assertEqual(row['standing'], coverage.UNCOVERED)
                self.assertIn('own identity is incomplete', row['reason'])

    def test_a_supplier_tree_row_needs_its_source_url_but_no_invented_revision(self):
        table = json.loads((ROOT / TABLE).read_text())
        voice = [c for c in table['components'] if c['supplier_tree_texts']]
        self.assertEqual(len(voice), 9)
        self.assertTrue(all(c['revision'] is None and c['repository'].startswith('https://') for c in voice))
        # At 0.169.0 the voice rows are covered, each established by the supplier's sources.json.
        opus = self.row(self.build(), 'Opus')
        self.assertEqual(opus['standing'], coverage.COVERED)
        self.assertEqual(opus['source_statement']['url'], opus['source']['repository'])

        def reviewed(v, repository):
            next(c for c in v['components'] if c['id'] == 'opus').update(repository=repository)
        for repository in (None, '', 'opus-1.6.1.tar.gz'):
            with self.subTest(repository=repository):
                # With the supplier's voice records held, a row whose source differs from them refuses.
                self.setUp(); self.edit(TABLE, lambda v, r=repository: reviewed(v, r))
                with self.assertRaisesRegex(ValueError, 'no single native-library entry of sources.json states the source of opus'):
                    self.build()
                # Without them, the row's own identity is still checked first.
                shutil.rmtree(self.repo / coverage.voice_records.RECORDS)
                row = self.row(self.build(), 'Opus')
                self.assertEqual(row['standing'], coverage.UNCOVERED)
                self.assertIn('source URL', row['reason'])
        # Review rounds 4 and 5, finding 2: a voice row's revision key is present and null; any value, or no key, refuses by
        # name before the review record's entries index it.
        for revision in ('1' * 40, '', 'v1.6.1', 'absent'):
            with self.subTest(revision=revision):
                self.setUp()
                def change(v, r=revision):
                    opus = next(c for c in v['components'] if c['id'] == 'opus')
                    if r == 'absent':
                        del opus['revision']
                    else:
                        opus['revision'] = r
                self.edit(TABLE, change, rebind=False)
                with self.assertRaisesRegex(ValueError, "a voice component's revision must be present and null: opus"):
                    self.build()
        # Without the records, a voice row with a complete identity is open, not covered.
        self.setUp(); shutil.rmtree(self.repo / coverage.voice_records.RECORDS)
        row = self.row(self.build(), 'Opus')
        self.assertEqual(row['standing'], coverage.UNCOVERED)
        self.assertIn('voice records for', row['reason'])

    # Review round 2, finding 2: a voice component is one by where its members are, not by how its row is written; it is
    # covered only through the voice records, with its source statement, and no exception or other text covers it.
    def test_a_voice_component_is_covered_only_through_the_voice_records(self):
        def reroute(v):
            opus = next(c for c in v['components'] if c['id'] == 'opus')
            codex = next(c for c in v['components'] if c['id'] == 'codex')
            opus.update(supplier_tree_texts=[], texts=[codex['texts'][0]],
                        text_exceptions=[{'path': codex['texts'][0], 'reason': 'INVENTED reviewed exception'}],
                        members=opus['members'] + ['codex-resources/voice/licenses/Opus.txt'])
        for records in (True, False):
            with self.subTest(records=records):
                self.setUp(); self.edit(TABLE, reroute)
                if not records:
                    shutil.rmtree(self.repo / coverage.voice_records.RECORDS)
                row = self.row(self.build(), 'Opus')
                self.assertEqual(row['standing'], coverage.UNCOVERED)
                self.assertNotIn('source_statement', row)
        # Review round 5: each condition alone. A committed text alone (an exception can only name a shipped text) leaves the
        # row uncovered, by its identity check first (a voice row has no revision, which committed texts need); no tree text
        # (the licence file kept as a member) leaves it uncovered by the voice route.
        def committed_text(v):
            codex = next(c for c in v['components'] if c['id'] == 'codex')
            next(c for c in v['components'] if c['id'] == 'opus')['texts'] = [codex['texts'][0]]
        def no_tree_text(v):
            opus = next(c for c in v['components'] if c['id'] == 'opus')
            opus['members'] = opus['members'] + opus['supplier_tree_texts']
            opus['supplier_tree_texts'] = []
        for change in (committed_text, no_tree_text):
            with self.subTest(change=change.__name__):
                self.setUp(); self.edit(TABLE, change)
                row = self.row(self.build(), 'Opus')
                self.assertEqual(row['standing'], coverage.UNCOVERED)
                self.assertIn({'committed_text': "committed texts need the component's own repository and revision",
                               'no_tree_text': 'covered only by its licence texts in the supplier tree'}[change.__name__], row['reason'])
        # Moving the library into the Codex row makes that row a voice row: it records a revision, which a voice row may not
        # (review round 4, finding 2), and no native-library entry establishes it.
        def to_codex(v, keep_revision):
            codex = next(c for c in v['components'] if c['id'] == 'codex')
            codex['members'].append('codex-resources/voice/lib/libopus.0.dylib')
            next(c for c in v['components'] if c['id'] == 'opus')['members'].remove('codex-resources/voice/lib/libopus.0.dylib')
            if not keep_revision:
                codex['revision'] = None
        for keep_revision, message in ((True, "a voice component's revision must be present and null: codex"),
                                       (False, 'states the source of codex')):
            with self.subTest(keep_revision=keep_revision):
                self.setUp(); self.edit(TABLE, lambda v, k=keep_revision: to_codex(v, k))
                with self.assertRaisesRegex(ValueError, message):
                    self.build()
        # Control: the committed rows are covered, each with its source statement.
        self.setUp()
        report = self.build()
        for name in ('Opus', 'zlib'):
            row = self.row(report, name)
            self.assertEqual(row['standing'], coverage.COVERED)
            self.assertIn('source_statement', row)

    # Review round 3, finding 1: voice membership is decided before any branch; a voice member takes only the voice route
    # and belongs to one component.
    def test_a_voice_member_takes_only_the_voice_route(self):
        lib = 'codex-resources/voice/lib/libopus.0.dylib'
        def to_compiled(v):
            next(c for c in v['components'] if c['id'] == 'opus')['members'].remove(lib)
            next(c for c in v['components'] if c['id'] == 'ripgrep-crate-dependencies')['members'].append(lib)
        def to_reading(v):
            icu, opus = (next(c for c in v['components'] if c['id'] == i) for i in ('icu', 'opus'))
            for key in ('version', 'repository', 'members', 'supplier_tree_texts'):
                icu[key] = json.loads(json.dumps(opus[key]))
            icu['texts'] = []
            opus.update(members=[], supplier_tree_texts=[], repository=None, standing='uncovered', reason='INVENTED',
                        would_close='INVENTED')
        def twice(v):
            next(c for c in v['components'] if c['id'] == 'zlib')['members'].append(lib)
        for change, message in ((to_compiled, 'takes only the voice route'), (to_reading, 'takes only the voice route'),
                                (twice, 'a voice member belongs to two components')):
            with self.subTest(message=message, change=change.__name__):
                self.setUp(); self.edit(TABLE, change)
                with self.assertRaisesRegex(ValueError, message):
                    self.build()

    # Review round 3, finding 2: supplier-tree texts only on a voice component, and only under the voice licences folder.
    def test_supplier_tree_texts_belong_only_to_voice_components(self):
        def nonvoice(v):
            next(c for c in v['components'] if c['id'] == 'codex-skill-imagegen-sample').update(
                standing='covered', supplier_tree_texts=['bin/codex'])
        def outside(v):
            next(c for c in v['components'] if c['id'] == 'opus')['supplier_tree_texts'] = ['codex-resources/voice/lib/libopus.0.dylib']
        for change, message in ((nonvoice, 'only a voice component may name supplier-tree texts'),
                                (outside, 'must be a member under codex-resources/voice/licenses/')):
            with self.subTest(message=message):
                self.setUp(); self.edit(TABLE, change)
                with self.assertRaisesRegex(ValueError, message):
                    self.build()

    def test_the_vendor_check_keeps_main_s_refusal(self):
        # Review round 3, finding 2: the optional --vendor comparison refuses, as on main, a row with tree texts whose source
        # the extracted tree's sources.json does not state; the control passes.
        vendor = self.repo / 'invented-vendor'
        tree = {}
        for name, member in coverage.voice_records.MEMBERS.items():
            raw = (self.repo / coverage.voice_records.RECORDS / '0.169.0' / name).read_bytes()
            (vendor / member).parent.mkdir(parents=True, exist_ok=True)
            (vendor / member).write_bytes(raw)
            tree[member] = {'sha256': hashlib.sha256(raw).hexdigest()}
        record = json.loads((self.repo / 'app/src-tauri/resources/supplier/0.169.0/CANONICAL_DISTRIBUTION.json').read_text())
        table = json.loads((self.repo / TABLE).read_text())
        coverage.check_vendor(vendor, table, tree, '0.169.0', record)
        next(c for c in table['components'] if c['id'] == 'codex-skill-imagegen-sample').update(supplier_tree_texts=['bin/codex'])
        with self.assertRaisesRegex(ValueError, 'voice component differs from sources.json: codex-skill-imagegen-sample'):
            coverage.check_vendor(vendor, table, tree, '0.169.0', record)

    # Review round 3, finding 3: a component a lockfile association names is a compiled-dependencies row with an executable.
    def test_a_locked_component_is_compiled_and_has_an_executable(self):
        def unkind(v):
            row = next(c for c in v['components'] if c['id'] == 'codex-crate-dependencies')
            row.pop('kind')
            row.update(standing='covered', texts=[next(c for c in v['components'] if c['id'] == 'codex')['texts'][0]])
        def move(v):
            codex, rg = (next(c for c in v['components'] if c['id'] == i) for i in ('codex-crate-dependencies', 'ripgrep-crate-dependencies'))
            rg['members'].extend(codex['members'])
            codex['members'] = []
        def share(v):
            next(c for c in v['components'] if c['id'] == 'ripgrep-crate-dependencies')['members'].append('bin/codex')
        for change, message in ((unkind, 'names a component that is not a compiled-dependencies row'),
                                (move, 'has no executable member'), (share, 'belongs to two compiled-dependencies components')):
            with self.subTest(message=message):
                self.setUp(); self.edit(TABLE, change)
                with self.assertRaisesRegex(ValueError, message):
                    self.build()

    # Review round 3, finding 6: a repeated key in a keyed collection refuses rather than letting the last one win.
    def test_a_repeated_supplier_identifier_refuses(self):
        def twice_id(v):
            v['components'].append(json.loads(json.dumps(next(c for c in v['components'] if c['id'] == 'codex'))))
        def twice_text(v):
            v['texts'].append(dict(v['texts'][0]))
        for change, message in ((twice_id, 'duplicate supplier component id'), (twice_text, 'repeats a text path')):
            with self.subTest(message=message):
                self.setUp(); self.edit(TABLE, change)
                with self.assertRaisesRegex(ValueError, message):
                    self.build()

    # Review round 4, finding 1 and App Agent 0's condition: a compiled component's repository is compared with its
    # lockfile's as written, as on main, and refuses with main's message for a suffix in any case or another letter case.
    def test_a_compiled_component_s_repository_is_compared_as_written(self):
        rg = 'https://github.com/BurntSushi/ripgrep'
        for repository in (rg + '.GIT', rg + '.git', rg + '/', 'https://github.com/burntsushi/ripgrep', 'https://GitHub.com/BurntSushi/ripgrep'):
            with self.subTest(repository=repository):
                self.setUp()
                self.edit(TABLE, lambda v, r=repository: next(c for c in v['components'] if c['id'] == 'ripgrep-crate-dependencies')
                          .update(repository=r))
                with self.assertRaisesRegex(ValueError, "the crate group's lockfile is for another repository or revision than the "
                                                        'component: ripgrep-crate-dependencies'):
                    self.build()

    # Review rounds 4 and 5, finding 1: every non-voice repository field of the table is either exactly the canonical
    # GitHub form or begins with exactly https://chromium.googlesource.com/; anything else refuses, naming the field. The
    # component and its texts are respelled together, so no comparison between them refuses first.
    def test_a_repository_field_has_one_of_the_two_accepted_forms(self):
        rg = 'https://github.com/BurntSushi/ripgrep'
        def respell(v, spelling):
            for item in [next(c for c in v['components'] if c['id'] == 'ripgrep')] + v['texts']:
                if item.get('repository') == rg:
                    item['repository'] = spelling
        for spelling in (rg + '.GIT', rg + '/', 'https://github.com:443/BurntSushi/ripgrep', 'https://git@github.com/BurntSushi/ripgrep',
                         'https://GITHUB.COM/BurntSushi/ripgrep', 'https://www.github.com/BurntSushi/ripgrep',
                         'https://gitlab.com/BurntSushi/ripgrep', 'https://Chromium.googlesource.com/BurntSushi/ripgrep'):
            with self.subTest(spelling=spelling):
                self.setUp(); self.edit(TABLE, lambda v, r=spelling: respell(v, r))
                with self.assertRaisesRegex(ValueError, 'a repository field is neither exactly https://github.com/<owner>/<repository> '
                                                        'nor under https://chromium.googlesource.com/: '):
                    self.build()
        # An also_at identity is held to the same rule.
        def also_at(v):
            other = next(t for t in v['texts'] if t.get('also_at'))['also_at'][0]
            other['repository'] = other['repository'].replace('https://github.com/', 'https://github.com:443/')
        self.setUp(); self.edit(TABLE, also_at)
        with self.assertRaisesRegex(ValueError, 'a repository field is neither exactly'):
            self.build()
        # A null or missing field is not a form; each refuses or stays open as on main.
        def text_field(v, change):
            change(next(t for t in v['texts'] if t['repository'] == rg))
        for change in (lambda t: t.update(repository=None), lambda t: t.pop('repository')):
            with self.subTest(field='text', change=change):
                self.setUp(); self.edit(TABLE, lambda v, c=change: text_field(v, c))
                with self.assertRaisesRegex(ValueError, 'supplier text needs a non-empty repository and revision'):
                    self.build()
        for change in (lambda o: o.update(repository=None), lambda o: o.pop('repository')):
            with self.subTest(field='also_at', change=change):
                self.setUp(); self.edit(TABLE, lambda v, c=change: c(next(t for t in v['texts'] if t.get('also_at'))['also_at'][0]))
                with self.assertRaisesRegex(ValueError, 'an also_at identity needs repository'):
                    self.build()
        self.setUp(); self.edit(TABLE, lambda v: next(c for c in v['components'] if c['id'] == 'ripgrep').update(repository=None))
        self.assertEqual(self.row(self.build(), 'ripgrep')['standing'], coverage.UNCOVERED)
        self.setUp(); self.edit(TABLE, lambda v: next(c for c in v['components'] if c['id'] == 'ripgrep').pop('repository'))
        with self.assertRaises(KeyError):
            self.build()
        # Control: the committed table passes, with both accepted forms present.
        self.setUp()
        table = json.loads((self.repo / TABLE).read_text())
        values = [c['repository'] for c in table['components'] if not coverage.voice_records.is_voice(c)]
        self.assertTrue(any(v.startswith(coverage.OTHER_REPOSITORY_PREFIXES) for v in values))
        self.assertEqual(self.row(self.build(), 'ripgrep')['standing'], coverage.COVERED)

    # Review round 4, remaining item: a distribution record that repeats a file refuses (an invented record in the copy).
    def test_a_distribution_record_that_repeats_a_file_refuses(self):
        record = texts.supplier_record(self.repo)[1]
        def repeat(v):
            v['inventory']['entries'].append(dict(next(e for e in v['inventory']['entries'] if e['kind'] == 'file')))
        self.edit(record, repeat, rebind=False); self.rebind()
        with self.assertRaisesRegex(ValueError, 'the distribution record repeats a file'):
            self.build()

    # Review round 3, finding 5: one repository identity; another letter case is the same repository.
    def test_the_codex_commit_check_ignores_repository_case(self):
        crates_module = coverage.texts.supplier_crates
        def table(v):
            next(c for c in v['components'] if c['id'] == 'codex-crate-dependencies').update(
                repository='https://github.com/OpenAI/Codex', revision='2' * 40)
        def associations(v):
            for item in [next(l for l in v['locks'] if l['id'] == 'codex'), next(w for w in v['workspaces'] if w['lock'] == 'codex')] + [
                    m['source'] for m in v['manifests'] if m['source']['kind'] == 'workspace-file']:
                item.update(repository='https://github.com/OpenAI/Codex', revision='2' * 40)
        self.edit(TABLE, table)
        self.edit(crates_module.ASSOCIATIONS, associations)
        (self.repo / crates_module.PACKAGES).write_bytes(crates_module.encode(crates_module.packages(self.repo)))
        with self.assertRaisesRegex(ValueError, 'must be at the distribution record\'s source commit'):
            self.build()

    def test_library_content_must_match_its_bundle_source_record(self):
        self.edit(texts.INPUTS, lambda v: v['library_content'][1].update(revision='d' * 40))
        with self.assertRaisesRegex(ValueError, 'another source'): self.build()

    # Round 4 finding 2: a folder is covered only with exactly the members its reviewed source record lists.
    def test_an_added_or_changed_file_in_a_bundled_library_folder_is_open(self):
        for name, change in (('added', lambda root: (root / 'agents/AGENT_INVENTED.md').write_text('INVENTED added file\n')),
                             ('changed', lambda root: (root / 'AGENTS.md').write_text('INVENTED changed text\n')),
                             ('removed', lambda root: (root / 'roles.json').unlink())):
            with self.subTest(name=name):
                self.setUp()
                change(self.repo / 'app/src-tauri/resources/instructions')
                row = self.row(self.build(), 'Chirality instructions and role set')
                self.assertEqual(row['standing'], coverage.UNCOVERED)
                self.assertIn('differs from the members its source record lists', row['reason'])
        # Listing the added file in the bundle's own record is a change to a reviewed record, which refuses until reviewed.
        self.setUp()
        record = self.repo / 'app/src-tauri/resources/instructions/ROLE_SET_SOURCE_BINDING.json'
        value = json.loads(record.read_text()); value['guidance'].append({'path': 'agents/AGENT_INVENTED.md', 'sha256': '0' * 64, 'byteLength': 1})
        record.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError, 'differs from the reviewed one'): self.build()

    def test_a_foreign_selection_under_a_named_destination_folder_is_open(self):
        # The reviewer's probe: a supplier-directory text selected as distribution-reference/extra.txt.
        overlay = 'app/packaging/unsigned/tauri.attested-reference.conf.json'
        foreign = '../packaging/supplier_notices/INVENTED-foreign/LICENSE'
        self.edit(overlay, lambda v: v['bundle']['resources'].update({foreign: 'distribution-reference/extra.txt'}))
        value = self.build()
        row = self.row(value, 'Unnamed bundle resource distribution-reference/extra.txt')
        self.assertEqual((row['standing'], row['mappings']), (coverage.UNCOVERED, [
            {'source': 'app/packaging/supplier_notices/INVENTED-foreign/LICENSE', 'destination': 'distribution-reference/extra.txt'}]))
        self.assertEqual(len(self.row(value, 'App distribution reference records')['mappings']), 12)
        # The same for a file selected into a bundled Library folder's destination.
        self.setUp()
        self.edit(overlay, lambda v: v['bundle']['resources'].update({foreign: 'instructions/extra.txt'}))
        self.assertEqual(self.row(self.build(), 'Unnamed bundle resource instructions/extra.txt')['standing'], coverage.UNCOVERED)

    def test_app_content_names_exact_mappings_only(self):
        dist = 'app/src-tauri/resources/distribution-reference/build-selection.s2.json'
        for mapping, message in (({'source': 'app/src-tauri/resources/distribution-reference/', 'destination': 'distribution-reference/'}, 'exactly'),
                                 ({'source': 'INVENTED-folder/INVENTED.md', 'destination': 'distribution-reference/build-selection.s2.json'}, 'does not exist'),
                                 ({'source': dist, 'destination': 'distribution-reference/other.json'}, 'does not exist')):
            with self.subTest(mapping=mapping):
                self.setUp(); self.edit(texts.INPUTS, lambda v, m=mapping: v['app_resources'][0]['mappings'].append(m))
                if mapping['source'].startswith('INVENTED-'):
                    source = self.repo / mapping['source']
                    source.parent.mkdir(parents=True)
                    source.write_text('INVENTED unmapped App content\n')
                with self.assertRaisesRegex(ValueError, message): self.build()
        self.setUp(); self.edit(texts.INPUTS, lambda v: v['app_resources'][0].update(accounts_for=['distribution-reference/']))
        with self.assertRaisesRegex(ValueError, 'unknown app_resources entry shape'): self.build()

    # Round 4 finding 1: copy routes beyond resources and the icon refuse rather than escape the account.
    def test_unsupported_copy_routes_and_platform_configuration_refuse(self):
        limitations = '../../INVENTED-release/LIMITATIONS.md'
        conf = 'app/src-tauri/tauri.conf.json'
        for name, change, message in (
                ('macOS files', lambda v: v['bundle'].update(macOS={'files': {'release/INVENTED.md': limitations}}), 'bundle.macOS.files'),
                ('frameworks', lambda v: v['bundle'].update(macOS={'frameworks': [limitations]}), 'bundle.macOS.frameworks'),
                ('external binary', lambda v: v['bundle'].update(externalBin=['binaries/invented']), 'bundle.externalBin'),
                ('resource list', lambda v: v['bundle'].update(resources=[limitations]), 'must be an object')):
            with self.subTest(route=name):
                self.setUp(); self.edit(conf, change)
                with self.assertRaisesRegex(ValueError, message): self.build()
        for name in ('tauri.macos.conf.json', 'Tauri.macos.toml', 'tauri.conf.json5', 'Tauri.toml', 'TAURI.MACOS.CONF.JSON'):
            with self.subTest(config=name):
                self.setUp()
                (self.repo / 'app/src-tauri' / name).write_text(json.dumps({'bundle': {'resources': {limitations: 'release/INVENTED.md'}}}))
                with self.assertRaisesRegex(ValueError, 'platform or alternate Tauri configuration'): self.build()

    # A file claim must not expand to directory contents, or follow a replacement link.
    def test_an_app_file_claim_refuses_a_directory_or_link(self):
        target = self.repo / 'app/src-tauri/resources/distribution-reference/VERSION_ADVANCE_0.160.0.md'
        target.unlink()
        target.mkdir()
        (target / 'INVENTED-foreign.txt').write_text('INVENTED third-party content; not App-authored\n')
        with self.assertRaisesRegex(ValueError, 'App content source must be a regular non-link file'):
            self.build()
        shutil.rmtree(target)
        outside = self.repo / 'invented.txt'
        outside.write_text('INVENTED linked content\n')
        target.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'App content source must be a regular non-link file'):
            self.build()

    # The shipped limitations list is the App's own content, named by its exact source and destination.
    def test_the_shipped_limitations_list_is_app_content_by_its_exact_mapping(self):
        source, destination = coverage.bundle.LIMITATIONS
        for value in (json.loads((ROOT / coverage.ACCOUNT).read_text()), self.build()):
            row = self.row(value, 'Release limitations list')
            self.assertEqual((row['class'], row['standing']), ('app-content', coverage.COVERED))
            self.assertEqual(row['mappings'], [{'source': coverage.bundle.repository_source(source), 'destination': destination}])
            self.assertEqual(row['texts'], self.row(value, 'chirality-app')['texts'])  # the App's LICENSE.md ships as its notice
        # Another source selected for that destination refuses; the entry cannot be carried by the destination alone.
        self.edit('app/src-tauri/tauri.conf.json', lambda v: v['bundle']['resources'].update(
            {source.replace('RELEASE_LIMITATIONS', 'INVENTED_OTHER'): destination}) or v['bundle']['resources'].pop(source))
        with self.assertRaisesRegex(ValueError, 'duplicate resource destination'): self.build()
        # Without its App-content entry, the mapping stands open.
        self.setUp(); self.edit(texts.INPUTS, lambda v: v.update(app_resources=[a for a in v['app_resources'] if a['name'] != 'Release limitations list']))
        self.assertEqual(self.row(self.build(), 'Unnamed bundle resource ' + destination)['standing'], coverage.UNCOVERED)

    # Every bundle resource is named in the account; an unnamed mapping is open, a stale claim refuses.
    def test_a_mapped_resource_the_account_does_not_name_is_open(self):
        conf = 'app/src-tauri/tauri.conf.json'
        source = self.repo / 'INVENTED-release/LIMITATIONS.md'
        source.parent.mkdir(); source.write_text('INVENTED App document\n')
        # An invented App document mapped into the bundle.
        self.edit(conf, lambda v: v['bundle']['resources'].update({'../../INVENTED-release/LIMITATIONS.md': 'release/INVENTED.md'}))
        value = self.build()
        row = self.row(value, 'Unnamed bundle resource release/INVENTED.md')
        self.assertEqual(row['standing'], coverage.UNCOVERED)
        self.assertIn('Unnamed bundle resource release/INVENTED.md', {o['name'] for o in value['open']})
        # Named as the App's own content by its exact mapping, it is covered with the App's licence as its notice.
        self.edit(texts.INPUTS, lambda v: v['app_resources'].append(
            {'name': 'Invented release document', 'note': 'invented for the test',
             'mappings': [{'source': 'INVENTED-release/LIMITATIONS.md', 'destination': 'release/INVENTED.md'}]}))
        value = self.build()
        self.assertEqual(self.row(value, 'Invented release document')['standing'], coverage.COVERED)
        self.assertNotIn('Unnamed bundle resource release/INVENTED.md', {c['name'] for c in value['components']})

    def test_a_claim_on_a_mapping_that_does_not_exist_refuses(self):
        source = self.repo / 'INVENTED-release/LIMITATIONS.md'
        source.parent.mkdir(); source.write_text('INVENTED unmapped App document\n')
        self.edit(texts.INPUTS, lambda v: v['app_resources'].append(
            {'name': 'Invented release document', 'note': 'invented',
             'mappings': [{'source': 'INVENTED-release/LIMITATIONS.md', 'destination': 'release/INVENTED.md'}]}))
        with self.assertRaisesRegex(ValueError, 'claims a mapping that does not exist'): self.build()

    def test_the_vendor_tree_must_be_named(self):
        self.edit(TABLE, lambda v: next(c for c in v['components'] if c['id'] == 'codex').pop('accounts_for'))
        self.assertIn('Unnamed bundle resource codex/', {o['name'] for o in self.build()['open']})
        self.setUp(); self.edit(TABLE, lambda v: next(c for c in v['components'] if c['id'] == 'v8').update(accounts_for=['instructions/']))
        with self.assertRaisesRegex(ValueError, 'may name only the vendor tree'): self.build()

    def test_every_current_mapping_is_named(self):
        for account in (json.loads((ROOT / coverage.ACCOUNT).read_text()), self.build()):
            self.assertFalse([c for c in account['components'] if c['class'] == 'resource'])
            self.assertEqual({(c['class'], c['name'], frozenset(m['destination'] for m in c.get('mappings', []))) for c in account['components']
                              if c['class'] in ('app', 'app-asset', 'library-content', 'notices')},
                             {('app', 'chirality-app', frozenset()), ('app-asset', 'App icon icons/icon.png', frozenset()),
                              ('library-content', 'Chirality instructions and role set', frozenset({'instructions/'})),
                              ('library-content', 'Chirality Library 3.4.0 workflows', frozenset({'workflows/'})),
                              ('notices', 'Third-party notices and their indexes', frozenset(
                                  [*coverage.NOTICE_INDEX_SOURCES, *(d for _, d in coverage.SUPPLEMENT_PAIRS)]))})
        fonts = json.loads((ROOT / 'app/packaging/font_notice/index.json').read_text())
        mapped = coverage.bundle.pairs(coverage.bundle.selected(ROOT / 'app', [l['path'] for l in fonts['licenses']]))
        mapped += [(coverage.bundle.VENDOR_SOURCE, 'codex/'), *coverage.SUPPLEMENT_PAIRS]
        self.assertEqual(coverage.unaccounted(coverage.check(ROOT)['mappings'], mapped), [])

if __name__ == '__main__':
    unittest.main()
