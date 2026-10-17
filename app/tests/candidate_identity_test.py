"""candidate-identity-v2: portable validation and real macOS metadata regressions.

All filesystem mutations are confined to temporary fixtures. No bundle or supplier
is executed. On non-macOS hosts only the live-metadata tests are unavailable.
"""
import contextlib
import copy
import ctypes
import errno
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import plistlib
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'examination' / 'candidate_identity'))
import identify  # noqa: E402

MAC = sys.platform == 'darwin'
IDENTIFIER = 'dev.example.test-candidate'
WHEN = '2000-01-01T00:00:00Z'  # invented fixture, never a run-date dependency


def write_bundle(root, identifier=IDENTIFIER, extra=None):
    app = Path(root) / 'Test.app'
    (app / 'Contents/MacOS').mkdir(parents=True)
    (app / 'Contents/Resources/instructions').mkdir(parents=True)
    (app / 'Contents/Info.plist').write_bytes(plistlib.dumps({
        'CFBundleExecutable': 'app', 'CFBundleIdentifier': identifier, 'CFBundleShortVersionString': '0.0.0'}))
    exe = app / 'Contents/MacOS/app'
    exe.write_bytes(b'fixture executable bytes, never executed')
    exe.chmod(0o755)
    (app / 'Contents/Resources/instructions/AGENTS.md').write_text('guidance\n')
    os.symlink('instructions/AGENTS.md', app / 'Contents/Resources/link')
    for name, data in (extra or {}).items():
        (app / name).write_bytes(data)
    return app


def portable_inventory():
    meta = {'mode': 0o755, 'uid': 1000, 'gid': 1000, 'xattrs': []}
    return {'format': identify.INVENTORY_FORMAT, 'method': identify.METHOD, 'root': copy.deepcopy(meta),
            'entries': [{'path': 'dir', 'kind': 'dir', **copy.deepcopy(meta)},
                        {'path': 'dir/file', 'kind': 'file', **copy.deepcopy(meta), 'size': 1, 'sha256': identify.sha(b'x')},
                        {'path': 'link', 'kind': 'symlink', **copy.deepcopy(meta), 'target': 'dir/file'}]}


def malformed_inventories():
    mutations = {
        'top list': lambda i: [],
        'root list': lambda i: i.update(root=[]),
        'entries object': lambda i: i.update(entries={}),
        'entries null': lambda i: i.update(entries=None),
        'entry scalar': lambda i: i['entries'].append(1),
        'entry null': lambda i: i['entries'].append(None),
        'unknown kind': lambda i: i['entries'][0].update(kind='device'),
        'kind array': lambda i: i['entries'][0].update(kind=[]),
        'unsorted': lambda i: i['entries'].reverse(),
        'duplicate': lambda i: i['entries'].append(copy.deepcopy(i['entries'][-1])),
        'missing parent': lambda i: i['entries'].pop(0),
        'extra field': lambda i: i['entries'][0].update(owner='me'),
        'missing field': lambda i: i['entries'][0].pop('mode'),
        'boolean mode': lambda i: i['root'].update(mode=True),
        'boolean uid': lambda i: i['root'].update(uid=True),
        'boolean gid': lambda i: i['entries'][0].update(gid=False),
        'boolean size': lambda i: i['entries'][1].update(size=True),
        'negative owner': lambda i: i['root'].update(uid=-1),
        'set id': lambda i: i['root'].update(mode=0o4755),
        'bad digest': lambda i: i['entries'][1].update(sha256='0' * 63),
        'other method': lambda i: i.update(method='chirality.app.bundle-tree.sha256/v1'),
        'absolute path': lambda i: i['entries'][0].update(path='/dir'),
        'path scalar': lambda i: i['entries'][0].update(path=1),
        'xattrs object': lambda i: i['root'].update(xattrs={}),
        'xattr scalar': lambda i: i['root'].update(xattrs=[1]),
        'xattr name shape': lambda i: i['root'].update(xattrs=[{'name': [], 'size': 0, 'sha256': '0' * 64}]),
        'xattr bool size': lambda i: i['root'].update(xattrs=[{'name': 'com.apple.provenance', 'size': True, 'sha256': '0' * 64}]),
        'xattr unknown': lambda i: i['root'].update(xattrs=[{'name': 'com.apple.quarantine', 'size': 0, 'sha256': '0' * 64}]),
        'target scalar': lambda i: i['entries'][2].update(target=1),
    }
    for bad in ('back\\slash', 'cr\rname', 'lf\nname', 'nul\0name', '\udcff'):
        mutations['path ' + repr(bad)] = lambda i, bad=bad: i['entries'][0].update(path=bad)
        mutations['target ' + repr(bad)] = lambda i, bad=bad: i['entries'][2].update(target=bad)
    for label, mutate in mutations.items():
        inv = portable_inventory()
        changed = mutate(inv)
        yield label, changed if label == 'top list' else inv


class Scratch(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, self.tmp)

    def run_tool(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = identify.main(list(argv))
        return code, out.getvalue(), err.getvalue()


class PortableValidation(Scratch):
    def test_validator_refuses_malformed_shapes_without_incidental_exceptions(self):
        for label, inv in malformed_inventories():
            with self.subTest(label):
                with self.assertRaises(ValueError):
                    identify.validate_inventory(inv)

    def test_identity_v2_represents_owners_provenance_and_symlink_metadata(self):
        inv = portable_inventory()
        base = identify.identity(inv)
        self.assertRegex(base, r'^chirality\.app\.bundle-tree\.sha256/v2:[0-9a-f]{64}$')
        for target in [inv['root'], *inv['entries']]:
            for key in ('mode', 'uid', 'gid'):
                old = target[key]; target[key] += 1
                self.assertNotEqual(base, identify.identity(inv))
                target[key] = old
            target['xattrs'] = [{'name': 'com.apple.provenance', 'size': 1, 'sha256': identify.sha(b'x')}]
            first = identify.identity(inv)
            self.assertNotEqual(base, first)
            target['xattrs'][0]['sha256'] = identify.sha(b'y')
            self.assertNotEqual(first, identify.identity(inv))
            target['xattrs'] = []

    def test_link_resolution_contains_all_chains_and_refuses_file_traversal(self):
        inv = portable_inventory()
        link = inv['entries'][-1]
        for target in ('../outside', '/absolute', 'missing', 'link', 'dir/file/child', 'dir/file/..',
                       'dir/file/.', 'dir/file/', '', 'dir/../../outside'):
            with self.subTest(target):
                link['target'] = target
                with self.assertRaises(ValueError): identify.validate_inventory(inv)
        for target in ('dir/file', 'dir/../dir/file', '.', 'dir/'):
            link['target'] = target
            identify.validate_inventory(inv)
        meta = {k: copy.deepcopy(inv['root'][k]) for k in ('mode', 'uid', 'gid', 'xattrs')}
        inv['entries'].insert(0, {'path': 'alias', 'kind': 'symlink', 'target': 'dir', **meta})
        link['target'] = 'alias/file'
        identify.validate_inventory(inv)  # contained directory chain
        for target in ('../outside', '/outside', 'link'):
            inv['entries'][0]['target'] = target
            with self.assertRaises(ValueError): identify.validate_inventory(inv)
        inv = portable_inventory(); meta = copy.deepcopy(inv['root'])
        for index in range(33):
            inv['entries'].append({'path': f'z{index:02}', 'kind': 'symlink', **meta,
                                   'target': f'z{index + 1:02}' if index < 32 else 'dir/file'})
        with self.assertRaisesRegex(ValueError, 'too long'): identify.validate_inventory(inv)
        inv['entries'].pop(-1); inv['entries'][-1]['target'] = 'dir/file'
        identify.validate_inventory(inv)  # exactly 32 hops

    def test_manifest_matches_independent_packaging_reader(self):
        app = write_bundle(self.tmp, extra={'Contents/Resources/é.txt': b'unicode', 'Contents/Resources/A': b'A'})
        prototype = Path(__file__).resolve().parents[2] / 'execution/PKG-01/DEL-01-06/Design/prototype/read_tree.py'
        spec = importlib.util.spec_from_file_location('packaging_read_tree', prototype)
        pkg = importlib.util.module_from_spec(spec); spec.loader.exec_module(pkg)
        entries = pkg.read(str(app), signatures=False)
        reference = pkg.manifest(entries)
        # Independent filesystem traversal on all platforms; live inventory on macOS.
        inv = identify.inventory(app) if MAC else {'entries': entries}
        self.assertEqual(identify.file_manifest(inv), reference)
        self.assertEqual(reference, hashlib.sha256(b''.join(
            hashlib.sha256(p.read_bytes()).hexdigest().encode() + b'  ' + p.relative_to(app).as_posix().encode() + b'\n'
            for p in sorted(app.rglob('*'), key=lambda p: p.relative_to(app).as_posix().encode())
            if p.is_file() and not p.is_symlink())).hexdigest())

    def test_unsupported_platform_refuses_live_scan_but_not_validation(self):
        with mock.patch.object(identify, '_libc', None):
            with self.assertRaisesRegex(OSError, 'not supported'): identify.inventory(self.tmp / 'Test.app')
            identify.validate_inventory(portable_inventory())
            self.assertEqual(self.run_tool('inventory', str(self.tmp / 'Test.app'))[0], 2)


class GitScratch(Scratch):
    def setUp(self):
        super().setUp()
        self.repo = self.tmp / 'repo'
        (self.repo / 'proj/app').mkdir(parents=True)
        (self.repo / 'proj/app/main.rs').write_text('fn main() {}\n')
        (self.repo / 'proj/README.md').write_text('readme\n')
        (self.repo / 'proj/link').symlink_to('app/main.rs')
        env = dict(os.environ, GIT_AUTHOR_NAME='Fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                   GIT_COMMITTER_NAME='Fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')
        for cmd in (['init', '-q'], ['add', '.'], ['commit', '-q', '-m', 'fixture']):
            subprocess.run(['git', '-C', str(self.repo), *cmd], check=True, env=env)
        self.export = self.tmp / 'export'; self.export.mkdir()
        archive = identify.git(self.repo, 'archive', 'HEAD', 'proj')
        subprocess.run(['tar', '-x', '-C', str(self.export)], input=archive, check=True)
        self.home = self.tmp / 'home'; self.home.mkdir()


class ExportAndData(GitScratch):
    def test_verify_export_tracks_git_symlinks_and_refuses_wrong_types_content_and_ancestors(self):
        self.assertIn(b'120000 blob', identify.git(self.repo, 'ls-tree', 'HEAD', 'proj/link'))
        self.assertEqual(identify.verify_export(self.repo, 'HEAD', 'proj', self.export)['tracked_files_verified'], 3)
        link = self.export / 'proj/link'
        link.unlink(); link.write_text('app/main.rs')
        with self.assertRaisesRegex(ValueError, 'not a link'): identify.verify_export(self.repo, 'HEAD', 'proj', self.export)
        link.unlink(); link.symlink_to('README.md')
        with self.assertRaisesRegex(ValueError, 'differs from revision'): identify.verify_export(self.repo, 'HEAD', 'proj', self.export)
        link.unlink(); link.symlink_to('app/main.rs')
        source = self.export / 'proj/app/main.rs'
        source.unlink(); source.symlink_to('../../repo/proj/app/main.rs')
        with self.assertRaisesRegex(ValueError, 'not a regular file'): identify.verify_export(self.repo, 'HEAD', 'proj', self.export)
        source.unlink(); source.write_text('changed')
        with self.assertRaisesRegex(ValueError, 'differs from revision'): identify.verify_export(self.repo, 'HEAD', 'proj', self.export)
        source.write_text('fn main() {}\n'); source.chmod(0o755)
        with self.assertRaisesRegex(ValueError, 'executable mode differs'): identify.verify_export(self.repo, 'HEAD', 'proj', self.export)
        shutil.rmtree(self.export / 'proj/app'); (self.export / 'proj/app').symlink_to(self.repo / 'proj/app')
        with self.assertRaises(OSError): identify.verify_export(self.repo, 'HEAD', 'proj', self.export)

    def test_freshness_covers_three_places_files_directories_and_dangling_links(self):
        with mock.patch.object(Path, 'home', return_value=self.home):
            expected = identify.app_data_declaration(IDENTIFIER)
            self.assertEqual(identify.app_data_state(IDENTIFIER), expected)
            self.assertEqual(len(expected['checked']), 3)
            for place in expected['checked']:
                path = self.home / place[2:]; path.parent.mkdir(parents=True, exist_ok=True)
                for kind in ('directory', 'file', 'dangling'):
                    with self.subTest(place=place, kind=kind):
                        if kind == 'directory': path.mkdir()
                        elif kind == 'file': path.write_bytes(b'x')
                        else: path.symlink_to('absent')
                        self.assertEqual(identify.app_data_state(IDENTIFIER)['present_at_identification'], [place])
                        path.rmdir() if kind == 'directory' else path.unlink()
            shutil.rmtree(self.home / 'Library/WebKit')
            (self.home / 'Library/WebKit').symlink_to('absent')
            with self.assertRaisesRegex(ValueError, 'ancestry'): identify.app_data_state(IDENTIFIER)


@unittest.skipUnless(MAC, 'live macOS ACL/xattr/flags observation requires macOS')
class BundleIdentity(Scratch):
    def ident(self, app):
        return identify.identity(identify.inventory(app))

    def set_xattr(self, path, name, data):
        libc = identify._libc
        libc.setxattr.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint32, ctypes.c_int]
        libc.setxattr.restype = ctypes.c_int
        result = libc.setxattr(os.fsencode(path), name.encode(), data, len(data), 0, identify.XATTR_NOFOLLOW)
        self.assertEqual(result, 0, f'{name}: errno {ctypes.get_errno()}')

    def native_xattr(self, path, name):
        libc = identify._libc
        size = libc.getxattr(os.fsencode(path), name.encode(), None, 0, 0, identify.XATTR_NOFOLLOW)
        self.assertGreaterEqual(size, 0)
        buf = ctypes.create_string_buffer(size)
        self.assertEqual(libc.getxattr(os.fsencode(path), name.encode(), buf, size, 0, identify.XATTR_NOFOLLOW), size)
        return buf.raw[:size]

    def test_identity_excludes_location_name_and_times_under_method_constraint(self):
        app = write_bundle(self.tmp / 'a'); before = self.ident(app)
        renamed = app.with_name('Renamed.app'); app.rename(renamed)
        for path in [renamed, *renamed.rglob('*')]:
            os.utime(path, ns=(1_000_000_000, 2_000_000_000), follow_symlinks=False)
        self.assertEqual(before, self.ident(renamed))
        moved = self.tmp / 'elsewhere.app'; renamed.rename(moved)
        self.assertEqual(before, self.ident(moved))

    def test_every_content_mode_and_structure_change_changes_identity(self):
        mutations = {
            'byte': lambda a: (a / 'Contents/MacOS/app').write_bytes(b'changed'),
            'mode': lambda a: (a / 'Contents/MacOS/app').chmod(0o744),
            'directory mode': lambda a: (a / 'Contents/Resources').chmod(0o700),
            'root mode': lambda a: a.chmod(0o700),
            'link mode': lambda a: os.chmod(a / 'Contents/Resources/link', 0o700, follow_symlinks=False),
            'link target': lambda a: ((a / 'Contents/Resources/link').unlink(), (a / 'Contents/Resources/link').symlink_to('../Info.plist')),
            'extra file': lambda a: (a / 'Contents/Resources/new.txt').write_text('x'),
            'empty directory': lambda a: (a / 'Contents/Resources/empty').mkdir(),
        }
        for name, mutate in mutations.items():
            with self.subTest(name):
                app = write_bundle(self.tmp / name); before = self.ident(app)
                mutate(app); self.assertNotEqual(before, self.ident(app))
        app = write_bundle(self.tmp / 'missing')
        (app / 'Contents/Resources/instructions/AGENTS.md').unlink()
        with self.assertRaisesRegex(ValueError, 'dangling'): self.ident(app)

    def test_ownership_is_observed_and_group_mutations_change_identity_including_links(self):
        app = write_bundle(self.tmp)
        other = next(g for g in os.getgroups() if g != app.stat().st_gid)
        for path in (app, app / 'Contents', app / 'Contents/MacOS/app', app / 'Contents/Resources/link'):
            before = self.ident(app)
            os.chown(path, -1, other, follow_symlinks=False)
            self.assertNotEqual(before, self.ident(app))
            inv = identify.inventory(app)
            entry = inv['root'] if path == app else next(e for e in inv['entries'] if e['path'] == path.relative_to(app).as_posix())
            self.assertEqual((entry['uid'], entry['gid']), (path.lstat().st_uid, path.lstat().st_gid))

    def test_nonempty_acls_refuse_on_root_directory_file_and_symlink(self):
        app = write_bundle(self.tmp)
        for path in (app, app / 'Contents/Resources', app / 'Contents/MacOS/app', app / 'Contents/Resources/link'):
            with self.subTest(path=path.relative_to(app)):
                subprocess.run(['chmod', '-h', '+a', 'everyone deny execute', str(path)], check=True)
                try:
                    if path.name == 'app':
                        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o755)
                        self.assertFalse(os.access(path, os.X_OK))
                    with self.assertRaisesRegex(ValueError, 'ACL refused'): identify.inventory(app)
                finally:
                    subprocess.run(['chmod', '-h', '-N', str(path)], check=True)
                identify.inventory(app)

    def test_nonzero_flags_refuse_on_every_entry_kind_with_cleanup(self):
        app = write_bundle(self.tmp)
        for path in (app, app / 'Contents', app / 'Contents/MacOS/app', app / 'Contents/Resources/link'):
            for flag in (stat.UF_HIDDEN, stat.UF_IMMUTABLE):
                with self.subTest(path=path.relative_to(app), flag=flag):
                    os.chflags(path, flag, follow_symlinks=False)
                    try:
                        self.assertEqual(path.lstat().st_flags, flag)
                        with self.assertRaisesRegex(ValueError, 'file flags'): identify.inventory(app)
                    finally:
                        os.chflags(path, 0, follow_symlinks=False)
        identify.inventory(app)

    def test_set_id_bits_refuse_and_sticky_bit_is_represented(self):
        app = write_bundle(self.tmp)
        for path in (app, app / 'Contents', app / 'Contents/MacOS/app', app / 'Contents/Resources/link'):
            original = stat.S_IMODE(path.lstat().st_mode)
            for bit in (stat.S_ISUID, stat.S_ISGID):
                os.chmod(path, original | bit, follow_symlinks=False)
                try:
                    self.assertTrue(path.lstat().st_mode & bit)
                    with self.assertRaisesRegex(ValueError, 'set-user-ID'): identify.inventory(app)
                finally:
                    os.chmod(path, original, follow_symlinks=False)
        before = self.ident(app); app.chmod(stat.S_IMODE(app.stat().st_mode) | stat.S_ISVTX)
        self.assertNotEqual(before, self.ident(app))

    def test_unallowlisted_xattrs_refuse_including_symlink_metadata_and_resource_fork(self):
        attributes = {'com.apple.quarantine': b'0081;0;fixture;', 'com.apple.ResourceFork': b'resource bytes',
                      'com.apple.FinderInfo': b'\1' + b'\0' * 31, 'com.apple.cs.CodeDirectory': b'fixture',
                      'com.apple.cs.test': b'fixture', 'test.chirality': b'fixture'}
        for index, (name, data) in enumerate(attributes.items()):
            app = write_bundle(self.tmp / str(index)); path = app / 'Contents/MacOS/app'
            self.set_xattr(path, name, data)
            if name == 'com.apple.ResourceFork':
                self.assertEqual((path / '..namedfork/rsrc').read_bytes(), data)
            with self.subTest(name):
                with self.assertRaisesRegex(ValueError, 'outside the allowlist'): identify.inventory(app)
        for index, relative in enumerate(('', 'Contents', 'Contents/Resources/link')):
            app = write_bundle(self.tmp / ('kind' + str(index)))
            path = app / relative
            self.set_xattr(path, 'test.chirality', b'link metadata')
            with self.assertRaisesRegex(ValueError, 'outside the allowlist'): identify.inventory(app)

    def test_provenance_value_is_observed_not_excluded_even_if_os_ignores_mutation(self):
        app = write_bundle(self.tmp)
        inv = identify.inventory(app)
        for path in (app, app / 'Contents', app / 'Contents/MacOS/app', app / 'Contents/Resources/link'):
            raw = self.native_xattr(path, 'com.apple.provenance')
            entry = inv['root'] if path == app else next(e for e in inv['entries'] if e['path'] == path.relative_to(app).as_posix())
            self.assertIn({'name': 'com.apple.provenance', 'size': len(raw), 'sha256': identify.sha(raw)}, entry['xattrs'])
            self.set_xattr(path, 'com.apple.provenance', b'attempted replacement')
            observed = self.native_xattr(path, 'com.apple.provenance')
            newer = identify.inventory(app)
            changed = newer['root'] if path == app else next(e for e in newer['entries'] if e['path'] == path.relative_to(app).as_posix())
            self.assertIn({'name': 'com.apple.provenance', 'size': len(observed), 'sha256': identify.sha(observed)}, changed['xattrs'])
            if observed != raw:
                self.assertNotEqual(identify.identity(inv), identify.identity(newer))
            inv = newer

    def test_special_files_hard_links_and_unsafe_root_ancestry_refuse(self):
        app = write_bundle(self.tmp / 'fifo'); os.mkfifo(app / 'Contents/pipe')
        with self.assertRaisesRegex(ValueError, 'special file'): identify.inventory(app)
        app = write_bundle(self.tmp / 'hard'); os.link(app / 'Contents/MacOS/app', app / 'Contents/MacOS/twin')
        with self.assertRaisesRegex(ValueError, 'hard-linked'): identify.inventory(app)
        app = write_bundle(self.tmp / 'hard-link')
        os.link(app / 'Contents/Resources/link', app / 'Contents/Resources/twin', follow_symlinks=False)
        self.assertEqual((app / 'Contents/Resources/link').lstat().st_nlink, 2)
        with self.assertRaisesRegex(ValueError, 'hard-linked symlink'): identify.inventory(app)
        real = write_bundle(self.tmp / 'real'); (self.tmp / 'Alias.app').symlink_to(real)
        with self.assertRaisesRegex(ValueError, 'symlink in bundle root'): identify.inventory(self.tmp / 'Alias.app')
        (self.tmp / 'ancestor').symlink_to(real.parent)
        with self.assertRaisesRegex(ValueError, 'ancestry'): identify.inventory(self.tmp / 'ancestor/Test.app')
        with self.assertRaisesRegex(ValueError, r'\.app'): identify.inventory(real.parent)
        (self.tmp / 'File.app').write_bytes(b'x')
        with self.assertRaises(OSError): identify.inventory(self.tmp / 'File.app')
        for name in ('bad\\name', 'bad\rname', 'bad\nname'):
            app = write_bundle(self.tmp / repr(name)); (app / name).write_bytes(b'x')
            with self.assertRaisesRegex(ValueError, 'cannot be represented'): identify.inventory(app)

    def test_live_link_escapes_and_invalid_targets_refuse(self):
        for index, target in enumerate(('../../../outside', '/absolute', 'missing', 'link', 'instructions/AGENTS.md/child',
                                        'instructions/AGENTS.md/.', 'instructions/AGENTS.md/', 'bad\\target', 'bad\r', 'bad\n')):
            app = write_bundle(self.tmp / str(index)); link = app / 'Contents/Resources/link'
            link.unlink(); link.symlink_to(target)
            with self.subTest(target=target):
                with self.assertRaises(ValueError): identify.inventory(app)
        app = write_bundle(self.tmp / 'chain'); resources = app / 'Contents/Resources'
        (resources / 'alias').symlink_to('instructions'); (resources / 'link').unlink()
        (resources / 'link').symlink_to('alias/AGENTS.md')
        identify.inventory(app)
        for target in ('../../../outside', '/outside'):
            (resources / 'alias').unlink(); (resources / 'alias').symlink_to(target)
            with self.assertRaises(ValueError): identify.inventory(app)
        for index, kind in enumerate(('name', 'target')):
            app = write_bundle(self.tmp / ('utf8' + str(index)))
            try:
                if kind == 'name':
                    fd = os.open(os.fsencode(app) + b'/bad\xff', os.O_WRONLY | os.O_CREAT, 0o600)
                    os.close(fd)
                else:
                    link = app / 'Contents/Resources/link'; link.unlink()
                    os.symlink(b'bad\xff', os.fsencode(link))
            except OSError as error:
                # APFS refuses illegal filename bytes before a fixture exists.
                # Stored-inventory surrogate refusals are tested on every host.
                self.assertEqual(error.errno, errno.EILSEQ)
                continue
            with self.assertRaisesRegex(ValueError, 'UTF-8'): identify.inventory(app)

    def test_two_pass_and_during_read_changes_refuse_including_metadata(self):
        app = write_bundle(self.tmp / 'between')
        scan = identify._scan_once
        def change_after_first(root):
            inv = scan(root)
            (app / 'Contents/MacOS/app').write_bytes(b'new bytes')
            return inv
        with mock.patch.object(identify, '_scan_once', side_effect=change_after_first):
            with self.assertRaisesRegex(ValueError, 'between identification passes'): identify.inventory(app)
        for index, mutation in enumerate(('bytes', 'mode', 'owner', 'acl', 'xattr', 'root mode', 'directory mode')):
            app = write_bundle(self.tmp / ('during' + str(index))); exe = app / 'Contents/MacOS/app'
            def mutate(relative):
                if relative != 'Contents/MacOS/app': return
                if mutation == 'bytes': exe.write_bytes(b'changed')
                elif mutation == 'mode': exe.chmod(0o700)
                elif mutation == 'owner': os.chown(exe, -1, next(g for g in os.getgroups() if g != exe.stat().st_gid))
                elif mutation == 'acl': subprocess.run(['chmod', '+a', 'everyone deny execute', str(exe)], check=True)
                elif mutation == 'xattr': self.set_xattr(exe, 'test.chirality', b'x')
                elif mutation == 'root mode': app.chmod(0o700)
                else: (app / 'Contents/MacOS').chmod(0o700)
            try:
                with self.subTest(mutation), mock.patch.object(identify, '_AFTER_FILE_READ', mutate):
                    with self.assertRaises(ValueError): identify.inventory(app)
            finally:
                if mutation == 'acl': subprocess.run(['chmod', '-N', str(exe)], check=True)

    def test_plist_field_types_and_executable_paths_refuse(self):
        app = write_bundle(self.tmp); path = app / 'Contents/Info.plist'; original = plistlib.loads(path.read_bytes())
        for key, value in [('CFBundleIdentifier', '../escape'), ('CFBundleIdentifier', True),
                           ('CFBundleExecutable', '../Info.plist'), ('CFBundleExecutable', ['app']),
                           ('CFBundleExecutable', ''), ('CFBundleVersion', 1), ('CFBundleShortVersionString', True)]:
            changed = dict(original); changed[key] = value; path.write_bytes(plistlib.dumps(changed))
            with self.subTest(key=key, value=value):
                with self.assertRaises(ValueError): identify.bundle_metadata(app, identify.inventory(app))
        for value in ([], 'text'):
            path.write_bytes(plistlib.dumps(value))
            with self.assertRaisesRegex(ValueError, 'dictionary'): identify.bundle_metadata(app, identify.inventory(app))
        original.pop('CFBundleShortVersionString'); original['CFBundleVersion'] = '42'
        path.write_bytes(plistlib.dumps(original))
        self.assertEqual(identify.bundle_metadata(app, identify.inventory(app))['version'], '42')

    def test_symlink_metadata_race_and_root_replacement_refuse(self):
        app = write_bundle(self.tmp / 'link-race'); link = app / 'Contents/Resources/link'
        original = identify._xattrs
        changed = False
        def change_during_link_metadata(fd=None, path=None):
            nonlocal changed
            result = original(fd=fd, path=path)
            if path == str(link) and not changed:
                changed = True
                os.chmod(link, 0o700, follow_symlinks=False)
            return result
        with mock.patch.object(identify, '_xattrs', change_during_link_metadata):
            with self.assertRaisesRegex(ValueError, 'symlink metadata changed'): identify.inventory(app)
        app = write_bundle(self.tmp / 'root-race')
        # Avoid path-based link metadata reads so this reaches the root binding check.
        (app / 'Contents/Resources/link').unlink()
        def replace_root(relative):
            if relative == 'Contents/MacOS/app':
                app.rename(app.with_name('Old.app'))
                write_bundle(app.parent)
        with mock.patch.object(identify, '_AFTER_FILE_READ', replace_root):
            with self.assertRaisesRegex(ValueError, 'changed|replaced'): identify.inventory(app)
        with self.assertRaisesRegex(ValueError, 'ancestry replaced'):
            with identify._open_directory(app, bundle=True):
                app.rename(app.with_name('New.app'))
                write_bundle(app.parent)

    def test_plist_reread_refuses_symlink_ancestors_and_changed_bytes(self):
        app = write_bundle(self.tmp); inv = identify.inventory(app)
        plist = app / 'Contents/Info.plist'; data = plist.read_bytes()
        plist.unlink(); plist.symlink_to('Other.plist'); (app / 'Contents/Other.plist').write_bytes(data)
        with self.assertRaises(OSError): identify.bundle_metadata(app, inv)
        plist.unlink(); plist.write_bytes(data + b' ')
        with self.assertRaisesRegex(ValueError, 'differs from the inventory'): identify.bundle_metadata(app, inv)
        (app / 'Contents').rename(app / 'RealContents'); (app / 'Contents').symlink_to('RealContents')
        with self.assertRaises(OSError): identify.bundle_metadata(app, inv)


@unittest.skipUnless(MAC, 'record creation needs live macOS metadata')
class CandidateRecord(GitScratch):
    def setUp(self):
        super().setUp()
        self.app = write_bundle(self.tmp / 'build')
        self.facts = self.tmp / 'facts.json'
        self.facts.write_text(json.dumps({
            'procedure': 'test', 'profile': 'debug', 'signing': 'none', 'features': [], 'command': ['build'],
            'config_overlays': [], 'toolchain': {}, 'lockfiles': {}, 'offline': True, 'environment': {},
            'started_at': WHEN, 'finished_at': WHEN}))
        self.home_patch = mock.patch.object(Path, 'home', return_value=self.home)
        self.home_patch.start(); self.addCleanup(self.home_patch.stop)

    def record(self, out='rec'):
        return self.run_tool('record', '--app', str(self.app), '--repo', str(self.repo), '--revision', 'HEAD',
                             '--prefix', 'proj', '--export-root', str(self.export), '--build-facts', str(self.facts),
                             '--identified-at', WHEN, '--out-dir', str(self.tmp / out))

    def check(self):
        return self.run_tool('check', '--record', str(self.tmp / 'rec/candidate-identification.json'), '--app', str(self.app))

    def test_record_binds_revision_source_and_bundle_and_check_recomputes(self):
        code, _, err = self.record(); self.assertEqual(code, 0, err)
        record = json.loads((self.tmp / 'rec/candidate-identification.json').read_text())
        head = identify.git(self.repo, 'rev-parse', 'HEAD').decode().strip()
        self.assertEqual(record['app_candidate']['revision'], head)
        self.assertEqual(record['source']['tracked_files_verified'], 3)
        self.assertFalse(record['app_candidate']['packaged'])
        self.assertTrue(record['candidate_key'].startswith(head[:10] + '-'))
        code, out, err = self.check(); self.assertEqual(code, 0, out + err)
        # Later App data must not erase the historical absence observation.
        place = self.home / identify.app_data_declaration(IDENTIFIER)['checked'][1][2:]
        place.mkdir(parents=True)
        self.assertEqual(self.check()[0], 0)
        (self.app / 'Contents/Resources/instructions/AGENTS.md').write_text('changed\n')
        code, out, _ = self.check(); self.assertEqual(code, 1)
        self.assertIn('Contents/Resources/instructions/AGENTS.md', json.loads(out)['changed'])

    def test_each_derived_record_field_tamper_is_detected_independently(self):
        self.assertEqual(self.record()[0], 0)
        path = self.tmp / 'rec/candidate-identification.json'; original = json.loads(path.read_bytes())
        mutations = {
            'executable digest': lambda r: r['bundle']['executable'].update(sha256='0' * 64),
            'executable path': lambda r: r['bundle']['executable'].update(path='Contents/MacOS/other'),
            'plist digest': lambda r: r['bundle'].update(info_plist_sha256='0' * 64),
            'manifest digest': lambda r: r['bundle'].update(file_manifest_sha256='0' * 64),
            'identifier': lambda r: r['bundle'].update(identifier='dev.example.other'),
            'name': lambda r: r['bundle'].update(name='Other.app'),
            'version': lambda r: r['bundle'].update(version='1.0'),
            'app directory': lambda r: r['app_data'].update(directory='~/forged'),
            'checked omitted': lambda r: r['app_data']['checked'].pop(),
            'checked forged': lambda r: r['app_data']['checked'].__setitem__(1, '~/forged'),
            'checked reordered': lambda r: r['app_data']['checked'].reverse(),
        }
        for kind in identify.KINDS:
            mutations['counts ' + kind] = lambda r, kind=kind: r['bundle']['counts'].__setitem__(kind, r['bundle']['counts'][kind] + 1)
        for key, value in original['bundle']['metadata_state'].items():
            mutations['metadata ' + key] = lambda r, key=key, value=value: r['bundle']['metadata_state'].__setitem__(
                key, value + 1 if type(value) is int else ([] if isinstance(value, list) else {}))
        def coherent_identifier(record):
            record['bundle']['identifier'] = 'dev.example.other'
            record['app_data'] = identify.app_data_declaration('dev.example.other')
        mutations['coherent identifier'] = coherent_identifier
        mutations['metadata owner values'] = lambda r: r['bundle']['metadata_state'].update(owners=[{'uid': 0, 'gid': 0}])
        schema_refusals = {'identifier', 'app directory', 'checked omitted', 'checked forged', 'checked reordered',
                           'metadata acl_entries', 'metadata nonzero_flags', 'metadata set_id_bits',
                           'metadata xattr_allowlist', 'metadata owners'}
        for label, mutate in mutations.items():
            record = copy.deepcopy(original); mutate(record); path.write_text(json.dumps(record))
            with self.subTest(label):
                code, out, err = self.check()
                self.assertEqual(code, 2 if label in schema_refusals else 1, out + err)
                if code == 1:
                    self.assertTrue(json.loads(out)['record_fields_mismatched'])
                self.assertNotIn('Traceback', err)
        path.write_text(json.dumps(original))
        self.assertEqual(self.check()[0], 0)

    def test_malformed_stored_inventory_cli_refuses_even_with_coherent_outer_digests(self):
        self.assertEqual(self.record()[0], 0)
        path = self.tmp / 'rec/candidate-identification.json'; original = json.loads(path.read_bytes())
        inventory_path = self.tmp / 'rec/bundle-inventory.json'
        for label, inv in malformed_inventories():
            record = copy.deepcopy(original)
            # Escaped JSON can carry a surrogate that the inventory must refuse
            # before attempting canonical UTF-8 serialization.
            data = json.dumps(inv, sort_keys=True, separators=(',', ':')).encode() + b'\n'
            inventory_path.write_bytes(data); record['bundle']['inventory']['sha256'] = identify.sha(data)
            if isinstance(inv, dict):
                body = {k: inv[k] for k in ('entries', 'method', 'root')}
                try:
                    digest = identify.sha(identify.canonical(body))
                except UnicodeEncodeError:
                    digest = '0' * 64  # no canonical identity exists for invalid UTF-8
                record['app_candidate']['build_identity'] = identify.METHOD + ':' + digest
                record['candidate_key'] = record['app_candidate']['revision'][:10] + '-' + record['app_candidate']['build_identity'].rsplit(':', 1)[1][:12]
            path.write_text(json.dumps(record))
            with self.subTest(label):
                code, _, err = self.check(); self.assertEqual(code, 2, err)
                self.assertNotIn('AttributeError', err); self.assertNotIn('Traceback', err)

    def test_tampered_outer_identity_inventory_or_source_refuses(self):
        self.assertEqual(self.record()[0], 0)
        path = self.tmp / 'rec/candidate-identification.json'; original = path.read_text()
        for mutate in (lambda r: r.update(candidate_key='0' * 10 + '-' + '0' * 12),
                       lambda r: r['source'].update(revision='0' * 40),
                       lambda r: r['app_candidate'].update(build_identity=identify.METHOD + ':' + '0' * 64)):
            record = json.loads(original); mutate(record); path.write_text(json.dumps(record))
            self.assertEqual(self.check()[0], 2)
        path.write_text(original)
        inv = self.tmp / 'rec/bundle-inventory.json'; inv.write_bytes(inv.read_bytes() + b' ')
        self.assertEqual(self.check()[0], 2)
        (self.export / 'proj/app/main.rs').write_text('changed')
        code, _, err = self.record('changed'); self.assertEqual(code, 2); self.assertIn('differs from revision', err)

    def test_malformed_xml_plist_refuses_without_traceback_or_record(self):
        (self.app / 'Contents/Info.plist').write_bytes(b'<?xml version="1.0"?><plist><dict>')
        code, _, err = self.record()
        self.assertEqual(code, 2, err)
        self.assertIn('error', json.loads(err))
        self.assertNotIn('Traceback', err)
        self.assertFalse((self.tmp / 'rec').exists())

    def test_record_timestamps_require_calendar_dates_and_explicit_timezones(self):
        self.assertEqual(self.record()[0], 0)
        path = self.tmp / 'rec/candidate-identification.json'
        original = json.loads(path.read_bytes())
        fields = (('identified_at',), ('build', 'started_at'), ('build', 'finished_at'))
        invalid = ('not-a-date', '2000-02-30T00:00:00Z', '2000-01-01T25:00:00Z',
                   '2000-01-01T00:00:00', '2000-01-01 00:00:00Z',
                   '2000-01-01T00:00:00+24:00', '2000-01-01T00:00:60Z')
        valid = (WHEN, '2000-02-29T12:34:56.123456789Z', '2000-01-01t00:00:00z',
                 '2000-01-01T00:00:00+05:30', '2000-01-01T00:00:00-00:00')
        for field in fields:
            for timestamp in (*invalid, *valid):
                record = copy.deepcopy(original)
                target = record if len(field) == 1 else record[field[0]]
                target[field[-1]] = timestamp
                path.write_text(json.dumps(record))
                with self.subTest(field=field, timestamp=timestamp):
                    code, out, err = self.check()
                    self.assertEqual(code, 2 if timestamp in invalid else 0, out + err)
                    self.assertNotIn('Traceback', err)
        facts = json.loads(self.facts.read_bytes())
        facts['started_at'] = 'not-a-date'
        self.facts.write_text(json.dumps(facts))
        code, _, err = self.record('invalid-time')
        self.assertEqual(code, 2, err)
        self.assertFalse((self.tmp / 'invalid-time').exists())

    def test_record_refuses_each_existing_app_data_location_including_dangling_links(self):
        for index, place in enumerate(identify.app_data_declaration(IDENTIFIER)['checked']):
            path = self.home / place[2:]; path.parent.mkdir(parents=True, exist_ok=True)
            path.symlink_to('missing')
            try:
                code, _, _ = self.record('r' + str(index)); self.assertEqual(code, 2)
                self.assertFalse((self.tmp / ('r' + str(index))).exists())
            finally:
                path.unlink()


if __name__ == '__main__':
    unittest.main()
