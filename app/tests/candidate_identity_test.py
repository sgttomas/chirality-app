"""candidate-identity v2/v3 and the candidate build recipe: portable validation and real macOS metadata regressions.

All filesystem mutations are confined to temporary fixtures. No bundle or supplier
is executed. On non-macOS hosts only the live-metadata tests are unavailable.
"""
import contextlib
import copy
import ctypes
import errno
import hashlib
import gzip
import importlib.util
import io
import json
import os
from pathlib import Path
import plistlib
import pwd
import shutil
import stat
import subprocess
import sys
import tempfile
import tarfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'examination' / 'candidate_identity'))
import build_candidate  # noqa: E402
import bundled_supplier  # noqa: E402
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


@contextlib.contextmanager
def controlled_provenance(value):
    """Control only libc xattr reads; these are not native presence witnesses.

    Protected provenance cannot reliably be created or removed by a fixture.
    Stat, ACL, content reads, inventory validation and hashing remain real.
    """
    def read(data, buf, size):
        if buf is not None:
            if size < len(data):
                ctypes.set_errno(errno.ERANGE)
                return -1
            ctypes.memmove(buf, data, len(data))
        return len(data)

    def listing(handle, buf, size, options):
        return read(b'' if value is None else b'com.apple.provenance\0', buf, size)

    def getter(handle, name, buf, size, position, options):
        if name != b'com.apple.provenance':
            raise AssertionError('unexpected controlled xattr: ' + repr(name))
        if value is None:
            ctypes.set_errno(errno.ENOATTR)
            return -1
        return read(value, buf, size)

    with contextlib.ExitStack() as stack:
        for name in ('flistxattr', 'listxattr'):
            stack.enter_context(mock.patch.object(identify._libc, name, side_effect=listing))
        for name in ('fgetxattr', 'getxattr'):
            stack.enter_context(mock.patch.object(identify._libc, name, side_effect=getter))
        yield


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

    def test_manifest_matches_independent_file_walk(self):
        app = write_bundle(self.tmp, extra={'Contents/Resources/é.txt': b'unicode', 'Contents/Resources/A': b'A'})
        files = sorted((p for p in app.rglob('*') if p.is_file() and not p.is_symlink()),
                       key=lambda p: p.relative_to(app).as_posix().encode())
        # Live inventory on macOS; the same regular-file rows elsewhere.
        inv = identify.inventory(app) if MAC else {'entries': [
            {'kind': 'file', 'path': p.relative_to(app).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in files]}
        self.assertEqual(identify.file_manifest(inv), hashlib.sha256(b''.join(
            hashlib.sha256(p.read_bytes()).hexdigest().encode() + b'  ' + p.relative_to(app).as_posix().encode() + b'\n'
            for p in files)).hexdigest())

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
    def test_repository_root_export_keeps_full_tree_identity(self):
        result = identify.verify_export(self.repo, 'HEAD', '.', self.export)
        self.assertEqual(result['tree'], identify.git(self.repo, 'rev-parse', 'HEAD^{tree}').decode().strip())
        self.assertEqual(result['tracked_files_verified'], 3)
        (self.export / 'proj/app/main.rs').write_bytes(b'changed')
        with self.assertRaises(ValueError):
            identify.verify_export(self.repo, 'HEAD', '.', self.export)

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
        if size < 0:
            code = ctypes.get_errno()
            if code == errno.ENOATTR:
                return None
            raise OSError(code, os.strerror(code))
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
        self.assert_provenance_observation(app)

    def assert_provenance_entry(self, app, path, inv, raw):
        entry = inv['root'] if path == app else next(e for e in inv['entries'] if e['path'] == path.relative_to(app).as_posix())
        expected = [] if raw is None else [{'name': 'com.apple.provenance', 'size': len(raw), 'sha256': identify.sha(raw)}]
        self.assertEqual(entry['xattrs'], expected)

    def assert_provenance_observation(self, app):
        inv = identify.inventory(app)
        for path in (app, app / 'Contents', app / 'Contents/MacOS/app', app / 'Contents/Resources/link'):
            raw = self.native_xattr(path, 'com.apple.provenance')
            self.assert_provenance_entry(app, path, inv, raw)
            # METHOD permits absence: macOS can attach provenance, but need not.
            # Do not invent a native presence witness by attempting to create it.
            if raw is None:
                continue
            self.set_xattr(path, 'com.apple.provenance', b'attempted replacement')
            observed = self.native_xattr(path, 'com.apple.provenance')
            newer = identify.inventory(app)
            self.assert_provenance_entry(app, path, newer, observed)
            if observed != raw:
                self.assertNotEqual(identify.identity(inv), identify.identity(newer))
            else:
                self.assertEqual(identify.identity(inv), identify.identity(newer))
            inv = newer
        return inv

    def test_controlled_provenance_absence_and_values_are_observed(self):
        app = write_bundle(self.tmp)
        identities = []
        for value in (None, b'', b'controlled first', b'controlled other'):
            with self.subTest(value=value), controlled_provenance(value), \
                    mock.patch.object(identify._libc, 'setxattr', return_value=0) as ignored_write:
                inv = self.assert_provenance_observation(app)
                expected = [] if value is None else [
                    {'name': 'com.apple.provenance', 'size': len(value), 'sha256': hashlib.sha256(value).hexdigest()}]
                for entry in [inv['root'], *inv['entries']]:
                    self.assertEqual(entry['xattrs'], expected)
                self.assertEqual(ignored_write.call_count, 0 if value is None else 4)
                identities.append(identify.identity(inv))
        self.assertEqual(len(set(identities)), len(identities))

    def test_native_xattr_accepts_only_missing_attribute_as_absence(self):
        def failure(*args):
            ctypes.set_errno(code)
            return -1

        for code in (errno.ENOATTR, errno.ENOENT, errno.EACCES, errno.EIO, errno.ENOTSUP, errno.ERANGE):
            with self.subTest(code=code), mock.patch.object(identify._libc, 'getxattr', side_effect=failure):
                if code == errno.ENOATTR:
                    self.assertIsNone(self.native_xattr(self.tmp, 'com.apple.provenance'))
                else:
                    with self.assertRaises(OSError) as error:
                        self.native_xattr(self.tmp, 'com.apple.provenance')
                    self.assertEqual(error.exception.errno, code)
        # Once presence was observed, a failed/short value read is not absence.
        for result in (-1, 0):
            with self.subTest(value_read=result), \
                    mock.patch.object(identify._libc, 'getxattr', side_effect=[1, result]):
                with self.assertRaises(AssertionError):
                    self.native_xattr(self.tmp, 'com.apple.provenance')

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
        self.assert_each_derived_record_field_tamper()

    def test_controlled_optional_provenance_record_tampers_are_detected(self):
        for value in (None, b'controlled provenance'):
            with self.subTest(value=value), controlled_provenance(value):
                self.assert_each_derived_record_field_tamper()
                record = json.loads((self.tmp / 'rec/candidate-identification.json').read_bytes())
                inv = json.loads((self.tmp / 'rec/bundle-inventory.json').read_bytes())
                expected = {} if value is None else {'com.apple.provenance': len(inv['entries']) + 1}
                self.assertEqual(record['bundle']['metadata_state']['extended_attributes'], expected)
                shutil.rmtree(self.tmp / 'rec')

    def assert_each_derived_record_field_tamper(self):
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
                key, value + 1 if type(value) is int else (
                    [] if isinstance(value, list) else ({} if value else {'com.apple.provenance': 1})))
        def coherent_identifier(record):
            record['bundle']['identifier'] = 'dev.example.other'
            record['app_data'] = identify.app_data_declaration('dev.example.other')
        mutations['coherent identifier'] = coherent_identifier
        owner = original['bundle']['metadata_state']['owners'][0]
        mutations['metadata owner values'] = lambda r: r['bundle']['metadata_state'].update(
            owners=[{'uid': owner['uid'] + 1, 'gid': owner['gid']}])
        schema_refusals = {'identifier', 'app directory', 'checked omitted', 'checked forged', 'checked reordered',
                           'metadata acl_entries', 'metadata nonzero_flags', 'metadata set_id_bits',
                           'metadata xattr_allowlist', 'metadata owners'}
        for label, mutate in mutations.items():
            record = copy.deepcopy(original); mutate(record)
            with self.subTest(label):
                self.assertNotEqual(record, original, 'tamper must change the record: ' + label)
                path.write_text(json.dumps(record))
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


@unittest.skipUnless(MAC, 'live bundle metadata requires macOS')
class BundledCandidateRecord(GitScratch):
    def setUp(self):
        super().setUp()
        self.app = write_bundle(self.tmp / 'build')
        self.facts = self.tmp / 'facts.json'
        self.facts.write_text(json.dumps({
            'procedure': 'test', 'profile': 'debug', 'signing': 'none', 'features': ['custom-protocol'],
            'command': ['build'], 'config_overlays': [], 'toolchain': {}, 'lockfiles': {}, 'offline': True,
            'environment': {}, 'started_at': WHEN, 'finished_at': WHEN}))
        self.home_patch = mock.patch.object(Path, 'home', return_value=self.home)
        self.home_patch.start(); self.addCleanup(self.home_patch.stop)
        self.vendor = self.app / 'Contents/Resources/codex'
        (self.vendor / 'bin').mkdir(parents=True)
        (self.vendor / 'codex-path').mkdir()
        (self.vendor / 'bin/codex').write_bytes(b'invented supplier, never executed')
        (self.vendor / 'bin/codex').chmod(0o755)
        (self.vendor / 'codex-path/rg').write_bytes(b'invented helper, never executed')
        self.archive = self.tmp / 'supplier.tgz'
        self.acquisition = self.tmp / 'acquisition.json'
        self.refresh_archive()
        facts = json.loads(self.facts.read_text()); facts['features'] = ['custom-protocol']
        self.facts.write_text(json.dumps(facts))

    def refresh_archive(self):
        with tarfile.open(self.archive, 'w:gz') as archive:
            archive.add(self.vendor, arcname='package/vendor/aarch64-apple-darwin')
        self.acquisition.write_text(json.dumps({
            'subject': {'file': 'codex-0.160.0-darwin-arm64.tgz',
                        'official_source_locator': 'https://registry.npmjs.org/@openai/codex/-/codex-0.160.0-darwin-arm64.tgz'},
            'acquisition': {'size_bytes': self.archive.stat().st_size, 'sha256': identify.sha(self.archive.read_bytes())}}))

    def record(self):
        return self.run_tool('record', '--app', str(self.app), '--repo', str(self.repo), '--revision', 'HEAD',
                             '--prefix', 'proj', '--export-root', str(self.export), '--build-facts', str(self.facts),
                             '--identified-at', WHEN, '--out-dir', str(self.tmp / 'rec'),
                             '--supplier-archive', str(self.archive), '--supplier-acquisition', str(self.acquisition))

    check = CandidateRecord.check

    def test_v3_binds_archive_provenance_and_bundle_without_executing_supplier(self):
        code, out, err = self.record(); self.assertEqual(code, 0, out + err)
        record = json.loads((self.tmp / 'rec/candidate-identification.json').read_bytes())
        self.assertEqual(record['format'], identify.BUNDLED_FORMAT)
        self.assertTrue(record['supplier']['bundled'])
        self.assertEqual(record['supplier']['standing'], 'unqualified-development')
        self.assertEqual(record['supplier']['correspondence']['files'], 2)
        self.assertEqual((self.tmp / 'rec/supplier-acquisition.json').read_bytes(), self.acquisition.read_bytes())
        self.assertFalse(record['app_candidate']['packaged'])
        self.assertFalse(any(s.startswith('The Codex supplier is not part') for s in record['limits']))
        self.assertEqual(self.check()[0], 0)
        self.archive.unlink()  # later recheck uses retained evidence, no archive reacquisition
        self.assertEqual(self.check()[0], 0)
        (self.vendor / 'bin/codex').write_bytes(b'changed')
        self.assertEqual(self.check()[0], 1)

    def test_v2_refuses_to_record_a_bundled_supplier_as_absent(self):
        code, _, err = CandidateRecord.record(self)
        self.assertEqual(code, 2); self.assertIn('v2 excludes bundled Codex', err)

    def test_archive_digest_and_complete_content_must_match(self):
        mutations = {
            'archive digest': lambda: self.archive.write_bytes(b'changed'),
            'supplier bytes': lambda: (self.vendor / 'bin/codex').write_bytes(b'changed'),
            'supplier mode': lambda: (self.vendor / 'codex-path/rg').chmod(0o755),
            'extra file': lambda: (self.vendor / 'extra').write_text('extra'),
            'extra directory': lambda: (self.vendor / 'extra-dir').mkdir(),
            'missing file': lambda: (self.vendor / 'codex-path/rg').unlink(),
            'link': lambda: (self.vendor / 'link').symlink_to('bin/codex'),
        }
        original = self.tmp / 'original'; shutil.copytree(self.vendor, original)
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                shutil.rmtree(self.vendor); shutil.copytree(original, self.vendor); self.refresh_archive()
                mutate(); code, out, err = self.record()
                self.assertEqual(code, 2, out + err); self.assertFalse((self.tmp / 'rec').exists())

    def test_v3_recheck_rejects_provenance_and_manifest_tampering(self):
        self.assertEqual(self.record()[0], 0)
        path = self.tmp / 'rec/candidate-identification.json'; original = path.read_bytes()
        for mutate in (
            lambda r: r['supplier']['correspondence'].update(file_manifest_sha256='0' * 64),
            lambda r: r['supplier'].update(pin='9.9.9'),
            lambda r: r['supplier']['archive'].update(source='https://example.invalid/claim'),
            lambda r: r['supplier']['acquisition'].update(path='../acquisition.json'),
            lambda r: r['supplier'].update(standing='verified'),
        ):
            r = json.loads(original); mutate(r); path.write_text(json.dumps(r))
            self.assertEqual(self.check()[0], 2)
        path.write_bytes(original)
        (path.parent / 'supplier-acquisition.json').write_text('{}')
        self.assertEqual(self.check()[0], 2)

    def test_duplicate_and_noncanonical_archive_paths_refuse(self):
        for path in ('bin/codex', '/bin/codex', 'bin/./codex', 'bin/../bin/codex'):
            with self.subTest(path=path):
                with tarfile.open(self.archive, 'w:gz') as archive:
                    archive.add(self.vendor, arcname='package/vendor/aarch64-apple-darwin')
                    data = (self.vendor / 'bin/codex').read_bytes()
                    entry = tarfile.TarInfo('package/vendor/aarch64-apple-darwin/' + path)
                    entry.mode = 0o755; entry.size = len(data)
                    archive.addfile(entry, io.BytesIO(data))
                acquisition = json.loads(self.acquisition.read_bytes())
                acquisition['acquisition'] = {'size_bytes': self.archive.stat().st_size,
                                            'sha256': identify.sha(self.archive.read_bytes())}
                self.acquisition.write_text(json.dumps(acquisition))
                code, out, err = self.record()
                self.assertEqual(code, 2, out + err); self.assertIn('duplicate or invalid', err)
                self.assertFalse((self.tmp / 'rec').exists())

    def test_truncated_gzip_has_structured_refusal_and_no_publication(self):
        self.archive.write_bytes(gzip.compress(b'abc')[:12])
        acquisition = json.loads(self.acquisition.read_bytes())
        acquisition['acquisition'] = {'size_bytes': self.archive.stat().st_size,
                                    'sha256': identify.sha(self.archive.read_bytes())}
        self.acquisition.write_text(json.dumps(acquisition))
        code, out, err = self.record()
        self.assertEqual(code, 2, out + err); self.assertIn('EOFError', json.loads(err)['error'])
        self.assertFalse((self.tmp / 'rec').exists())

    def test_complete_content_profile_refuses_release_or_missing_packaged_resource_feature(self):
        original = json.loads(self.facts.read_text())
        for change in ({'features': []}, {'profile': 'release'}, {'signing': 'Developer ID'}):
            self.facts.write_text(json.dumps(dict(original, **change)))
            code, _, _ = self.record(); self.assertEqual(code, 2)


def release_archive(vendor, archive, extra=None):
    """Supplier release package layout: the tree at the archive root, no root member."""
    with tarfile.open(archive, 'w:gz') as tar:
        for child in sorted(Path(vendor).iterdir()):
            tar.add(child, arcname=child.name)
        for info, data in (extra or []):
            tar.addfile(info, io.BytesIO(data) if data is not None else None)


def tree_inventory(vendor):
    vendor = Path(vendor)
    entries = []
    for path in sorted(vendor.rglob('*'), key=lambda q: q.relative_to(vendor).as_posix().encode()):
        info = path.lstat()
        entry = {'path': path.relative_to(vendor).as_posix(), 'kind': 'dir' if path.is_dir() else 'file',
                 'mode': stat.S_IMODE(info.st_mode)}
        if entry['kind'] == 'file':
            entry.update(size=info.st_size, sha256=identify.sha(path.read_bytes()))
        entries.append(entry)
    return entries


def distribution_record(archive, entries, pin='0.0.1'):
    """Invented record of the committed canonical distribution form; nothing here is a real supplier."""
    files = {e['path']: e for e in entries if e['kind'] == 'file'}
    return {'format': bundled_supplier.DISTRIBUTION_FORM, 'pin': pin, 'source_commit': '0' * 40,
            'archive': {'url': f'https://github.com/openai/codex/releases/download/rust-v{pin}/codex-package-aarch64-apple-darwin.tar.gz',
                        'size': Path(archive).stat().st_size, 'sha256': identify.sha(Path(archive).read_bytes())},
            'package_metadata': {'layoutVersion': 1, 'version': pin, 'target': 'aarch64-apple-darwin', 'entrypoint': 'bin/codex'},
            'files': len(files), 'root_mode': 'Invented: no root directory member.',
            'inventory': {'method': 'codex-vendor-tree-v1', 'algorithm': 'sha-256',
                          'manifest_sha256': bundled_supplier.manifest(files), 'entries': entries},
            'limits': ['Invented fixture record.']}


def invented_vendor(vendor):
    (vendor / 'bin').mkdir(parents=True)
    (vendor / 'codex-path').mkdir()
    (vendor / 'bin/codex').write_bytes(b'invented supplier, never executed')
    (vendor / 'bin/codex').chmod(0o755)
    (vendor / 'codex-path/rg').write_bytes(b'invented helper, never executed')
    (vendor / 'codex-path/rg').chmod(0o755)
    (vendor / 'codex-package.json').write_text('{"invented": true}\n')
    (vendor / 'codex-package.json').chmod(0o644)
    for d in (vendor / 'bin', vendor / 'codex-path'):
        d.chmod(0o755)


class ReleasePackageRecord(GitScratch):
    """The supplier release package bound by the committed canonical distribution record's form."""
    def setUp(self):
        super().setUp()
        self.app = write_bundle(self.tmp / 'build')
        self.facts = self.tmp / 'facts.json'
        self.facts.write_text(json.dumps({
            'procedure': 'test', 'profile': 'debug', 'signing': 'none', 'features': ['custom-protocol'],
            'command': ['build'], 'config_overlays': [], 'toolchain': {}, 'lockfiles': {}, 'offline': True,
            'environment': {}, 'started_at': WHEN, 'finished_at': WHEN}))
        self.home_patch = mock.patch.object(Path, 'home', return_value=self.home)
        self.home_patch.start(); self.addCleanup(self.home_patch.stop)
        self.vendor = self.app / 'Contents/Resources/codex'
        invented_vendor(self.vendor)
        self.archive = self.tmp / 'codex-package-aarch64-apple-darwin.tar.gz'
        self.distribution = self.tmp / 'CANONICAL_DISTRIBUTION.json'
        self.refresh()

    def refresh(self, extra=None, change=None):
        release_archive(self.vendor, self.archive, extra)
        record = distribution_record(self.archive, tree_inventory(self.vendor))
        if change:
            change(record)
        self.distribution.write_text(json.dumps(record, indent=1))

    def record(self):
        return self.run_tool('record', '--app', str(self.app), '--repo', str(self.repo), '--revision', 'HEAD',
                             '--prefix', 'proj', '--export-root', str(self.export), '--build-facts', str(self.facts),
                             '--identified-at', WHEN, '--out-dir', str(self.tmp / 'rec'),
                             '--supplier-archive', str(self.archive), '--supplier-acquisition', str(self.distribution))

    check = CandidateRecord.check

    def test_release_package_identifies_and_checks_without_inventing_an_acquisition_account(self):
        code, out, err = self.record(); self.assertEqual(code, 0, out + err)
        record = json.loads((self.tmp / 'rec/candidate-identification.json').read_bytes())
        supplier = record['supplier']
        self.assertEqual(record['format'], identify.BUNDLED_FORMAT)
        self.assertEqual(supplier['pin'], '0.0.1')
        self.assertEqual(supplier['archive']['file'], 'codex-package-aarch64-apple-darwin.tar.gz')
        self.assertEqual(supplier['acquisition'], {
            'path': 'supplier-canonical-distribution.json', 'sha256': identify.sha(self.distribution.read_bytes()),
            'form': 'chirality.supplier-canonical-assessment/1', 'acquirer': 'not recorded', 'authorization': 'not recorded'})
        self.assertEqual(supplier['correspondence']['method'], 'codex-package-tar-files/v1')
        self.assertEqual(supplier['correspondence']['files'], 3)
        self.assertEqual(supplier['correspondence']['inventory']['entries'], 5)
        self.assertEqual((self.tmp / 'rec/supplier-canonical-distribution.json').read_bytes(), self.distribution.read_bytes())
        self.assertFalse((self.tmp / 'rec/supplier-acquisition.json').exists())
        limits = ' '.join(record['limits'])
        self.assertIn('no acquirer or acquisition authorization is recorded', limits)
        self.assertNotIn('acquisition authorization/custody remains the supplied record', limits)
        self.assertEqual(self.check()[0], 0)
        self.archive.unlink()  # recheck uses the retained record and stored inventory only
        self.assertEqual(self.check()[0], 0)
        (self.vendor / 'codex-package.json').write_text('changed\n')
        self.assertEqual(self.check()[0], 1)

    def test_release_package_refusals_publish_nothing(self):
        def entry(path, **change):
            def apply(record):
                next(e for e in record['inventory']['entries'] if e['path'] == path).update(change)
            return apply

        def link():
            info = tarfile.TarInfo('codex-path/link'); info.type = tarfile.SYMTYPE; info.linkname = 'rg'
            return [(info, None)]

        def root_member():
            info = tarfile.TarInfo('.'); info.type = tarfile.DIRTYPE; info.mode = 0o755
            return [(info, None)]
        cases = {
            'archive digest': lambda: self.refresh(change=lambda r: r['archive'].update(sha256='0' * 64)),
            'archive size': lambda: self.refresh(change=lambda r: r['archive'].update(size=r['archive']['size'] + 1)),
            'member bytes': lambda: (self.refresh(), (self.vendor / 'bin/codex').write_bytes(b'changed')),
            'member mode': lambda: (self.refresh(), (self.vendor / 'codex-package.json').chmod(0o755)),
            'extra file': lambda: (self.refresh(), (self.vendor / 'extra').write_text('extra')),
            'missing file': lambda: (self.refresh(), (self.vendor / 'codex-path/rg').unlink()),
            'link in archive': lambda: self.refresh(extra=link()),
            'root member': lambda: self.refresh(extra=root_member()),
            'inventory mode': lambda: self.refresh(change=entry('codex-path', mode=0o700)),
            'inventory size': lambda: self.refresh(change=entry('bin/codex', size=1)),
            'inventory missing entry': lambda: self.refresh(change=lambda r: r['inventory']['entries'].pop()),
            'unknown format': lambda: self.refresh(change=lambda r: r.update(format='example.invalid/1')),
            'other platform': lambda: self.refresh(change=lambda r: r['archive'].update(
                url=r['archive']['url'].replace('aarch64-apple-darwin', 'x86_64-unknown-linux-musl'))),
            # Pin and package metadata agree with each other; only the locator's version differs.
            'pin differs from locator': lambda: self.refresh(change=lambda r: (
                r.update(pin='0.0.2'), r['package_metadata'].update(version='0.0.2'))),
        }
        original = self.tmp / 'original'; shutil.copytree(self.vendor, original)
        for name, mutate in cases.items():
            with self.subTest(name=name):
                shutil.rmtree(self.vendor); shutil.copytree(original, self.vendor)
                mutate()
                code, out, err = self.record()
                self.assertEqual(code, 2, name + out + err); self.assertFalse((self.tmp / 'rec').exists())

    def test_release_package_recheck_refuses_altered_retained_record_and_facts(self):
        self.assertEqual(self.record()[0], 0)
        path = self.tmp / 'rec/candidate-identification.json'; original = path.read_bytes()
        for name, mutate in {
            'pin': lambda r: r['supplier'].update(pin='0.0.2'),
            'archive digest': lambda r: r['supplier']['archive'].update(sha256='0' * 64),
            'archive locator': lambda r: r['supplier']['archive'].update(source='https://example.invalid/claim'),
            'acquirer': lambda r: r['supplier']['acquisition'].update(acquirer='someone'),
            'authorization dropped': lambda r: r['supplier']['acquisition'].pop('authorization'),
            'npm form claimed': lambda r: r['supplier']['acquisition'].update(path='supplier-acquisition.json'),
            'correspondence method': lambda r: r['supplier']['correspondence'].update(method='codex-platform-tar-files/v1'),
            'inventory summary': lambda r: r['supplier']['correspondence']['inventory'].update(entries=6),
            'inventory dropped': lambda r: r['supplier']['correspondence'].pop('inventory'),
        }.items():
            with self.subTest(name=name):
                r = json.loads(original); mutate(r); path.write_text(json.dumps(r))
                self.assertEqual(self.check()[0], 2)
        path.write_bytes(original)
        retained = self.tmp / 'rec/supplier-canonical-distribution.json'
        retained.write_bytes(retained.read_bytes() + b' ')
        self.assertEqual(self.check()[0], 2)

    def test_retained_record_rewritten_consistently_still_refuses_against_stored_inventory(self):
        self.assertEqual(self.record()[0], 0)
        retained = self.tmp / 'rec/supplier-canonical-distribution.json'
        record = json.loads(retained.read_bytes())
        next(e for e in record['inventory']['entries'] if e['path'] == 'codex-path')['mode'] = 0o700
        retained.write_text(json.dumps(record))
        path = self.tmp / 'rec/candidate-identification.json'
        outer = json.loads(path.read_bytes())
        outer['supplier']['acquisition']['sha256'] = identify.sha(retained.read_bytes())
        path.write_text(json.dumps(outer))
        code, _, err = self.check()
        self.assertEqual(code, 2); self.assertIn('distribution record inventory', err)


def build_schema(version):
    schema = json.loads((Path(identify.__file__).parent / f'candidate-identification.{version}.schema.json').read_text())
    return {'$schema': schema['$schema'], **schema['properties']['build'], '$defs': schema['$defs']}


def snapshot(top):
    """Every name under top with its type, mode, times and bytes: listing for listing, byte for byte."""
    seen = {}
    for current, dirs, files in os.walk(top):
        for name in sorted(dirs + files) + ['.']:
            path = os.path.join(current, name)
            info = os.lstat(path)
            data = Path(path).read_bytes() if stat.S_ISREG(info.st_mode) else None
            seen[os.path.relpath(path, top)] = (info.st_mode, info.st_size, info.st_mtime_ns, data)
    return seen


class CandidateBuild(Scratch):
    """build_candidate.py planning, containment, isolation, export, supplier extraction and facts."""
    def setUp(self):
        super().setUp()
        self.repo = self.tmp / 'repo'
        files = {'app/package-lock.json': '{"lockfileVersion": 3}\n', 'app/src-tauri/Cargo.lock': 'version = 4\n',
                 'app/packaging/unsigned/tauri.development.conf.json': '{"identifier": "dev.example.skeleton"}\n',
                 'app/run.sh': '#!/bin/sh\n'}
        for name, text in files.items():
            (self.repo / name).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / name).write_text(text)
        (self.repo / 'app/run.sh').chmod(0o755)
        env = dict(os.environ, GIT_AUTHOR_NAME='Fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                   GIT_COMMITTER_NAME='Fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')
        for cmd in (['init', '-q'], ['add', '.'], ['commit', '-q', '-m', 'fixture']):
            subprocess.run(['git', '-C', str(self.repo), *cmd], check=True, env=env)
        self.commit = identify.git(self.repo, 'rev-parse', 'HEAD').decode().strip()
        self.vendor = self.tmp / 'vendor'
        invented_vendor(self.vendor)
        self.archive = self.tmp / 'inputs/codex-package-aarch64-apple-darwin.tar.gz'
        self.archive.parent.mkdir()
        release_archive(self.vendor, self.archive)
        self.record = self.tmp / 'inputs/CANONICAL_DISTRIBUTION.json'
        self.record.write_text(json.dumps(distribution_record(self.archive, tree_inventory(self.vendor))))
        # Sentinels standing in for the caller's home, toolchain folders and prepared caches.
        self.caller = self.tmp / 'caller-home'
        for name, data in (('.npm/_cacache/index-v5/marker', b'invented cache entry'),
                           ('.npm/_logs/earlier.log', b'invented earlier log'),
                           ('.cargo/registry/cache/marker', b'invented crate'),
                           ('.npmrc', b'invented=1\n'),
                           ('toolchain/node-bin/node', b'invented, never run'), ('toolchain/node-bin/npm', b'invented'),
                           ('toolchain/rust-bin/cargo', b'invented, never run'), ('toolchain/rust-bin/rustc', b'invented')):
            (self.caller / name).parent.mkdir(parents=True, exist_ok=True)
            (self.caller / name).write_bytes(data)
        self.inputs = {'node_bin': str(self.caller / 'toolchain/node-bin'), 'rust_bin': str(self.caller / 'toolchain/rust-bin'),
                       'npm_cache': str(self.caller / '.npm'), 'cargo_home': str(self.caller / '.cargo')}
        self.environ = {'HOME': str(self.caller), 'PATH': '/usr/bin:/bin', 'LANG': 'C',
                        'APPLE_SIGNING_IDENTITY': 'invented', 'TAURI_SIGNING_PRIVATE_KEY': 'invented',
                        'APPLE_ID': 'invented@example.invalid', 'CODEX_HOME': '/invented/personal',
                        'CARGO_HOME': '/invented/cargo', 'RUSTUP_HOME': '/invented/rustup'}

    def plan(self, out='out', inputs=None, **kw):
        return build_candidate.plan(self.repo, 'HEAD', self.tmp / out, environ=self.environ,
                                    inputs=inputs or self.inputs, **kw)

    def test_plan_names_fresh_identifier_overlay_command_and_clean_environment(self):
        p = self.plan(supplier_archive=self.archive, supplier_record=self.record)
        root = str(self.tmp / 'out')
        self.assertEqual(p['commit'], self.commit)
        self.assertFalse(Path(root).exists())
        self.assertRegex(p['identifier'], r'^dev\.chirality\.app-v4\.candidate\.[0-9]{8}-' + self.commit[:8] + '-[0-9a-f]{6}$')
        self.assertEqual(p['overlay'], {'identifier': p['identifier'], 'productName': p['product'],
                                        'bundle': {'resources': {root + '/codex-package/': 'codex/'}}})
        self.assertEqual(json.loads(p['overlay_bytes']), p['overlay'])
        self.assertEqual(p['install'], ['npm', 'install', '--offline', '--no-audit', '--no-fund', '--ignore-scripts'])
        self.assertEqual(p['build'], ['node', 'node_modules/@tauri-apps/cli/tauri.js', 'build', '--debug', '--no-sign',
                                      '--bundles', 'app', '--features', 'custom-protocol',
                                      '--config', 'packaging/unsigned/tauri.development.conf.json',
                                      '--config', root + '/tauri.candidate.conf.json', '--', '--offline', '--locked'])
        self.assertEqual(p['env']['HOME'], root + '/home')
        self.assertEqual(p['env']['LANG'], 'C')
        self.assertEqual(p['env']['NPM_CONFIG_UPDATE_NOTIFIER'], 'false')
        self.assertFalse(any(k.startswith(('APPLE', 'TAURI', 'RUSTUP')) for k in p['env']))
        self.assertEqual(p['bundle'], root + '/target/debug/bundle/macos/' + p['product'] + '.app')
        again = self.plan()
        self.assertNotEqual(again['identifier'], p['identifier'])  # same revision, same day: distinct
        self.assertNotIn('bundle', again['overlay'])
        command = build_candidate.next_command(p)
        self.assertIn('identify.py record', command)
        self.assertIn('--supplier-acquisition ' + str(self.record), command)
        self.assertIn('--revision ' + self.commit, command)

    def test_every_writable_place_in_the_planned_environment_is_inside_the_output_root(self):
        p = self.plan()
        root = Path(p['root'])
        for key, value in p['env'].items():
            with self.subTest(key=key):
                if key == 'PATH':  # read-only toolchain folders and system folders only
                    self.assertEqual(value.split(':'), [self.inputs['node_bin'], self.inputs['rust_bin'],
                                                        '/usr/bin', '/bin', '/usr/sbin', '/sbin'])
                elif value.startswith('/'):
                    self.assertTrue(Path(value) == root or root in Path(value).parents, value)
        for key in ('HOME', 'TMPDIR', 'CARGO_HOME', 'CARGO_TARGET_DIR', 'CODEX_HOME', 'NPM_CONFIG_CACHE',
                    'NPM_CONFIG_USERCONFIG', 'NPM_CONFIG_GLOBALCONFIG', 'NPM_CONFIG_PREFIX', 'NPM_CONFIG_LOGS_DIR'):
            self.assertIn(key, p['env'])

    def test_planned_install_leaves_the_callers_home_and_caches_unchanged(self):
        node = shutil.which('node')
        if not node or not shutil.which('npm', path=os.path.dirname(node)):
            self.skipTest('node and npm are not on PATH; this isolation test runs the real npm install command')
        inputs = dict(self.inputs, node_bin=os.path.dirname(node))
        before = snapshot(self.caller)
        p = self.plan(inputs=inputs)
        root = Path(p['root'])
        root_id = build_candidate.create_root(p)
        build_candidate.prepare_environment(p, root_id)
        project = root / 'source/app'; project.mkdir(parents=True)
        (project / 'package.json').write_text('{"name": "invented", "version": "0.0.0", "private": true}\n')
        with open(root / 'build.log', 'xb') as log:
            build_candidate._run(p['install'], p['env'], project, log)
        self.assertTrue((project / 'package-lock.json').is_file())
        self.assertEqual(snapshot(self.caller), before)
        self.assertEqual((root / 'npm-cache/_cacache/index-v5/marker').read_bytes(), b'invented cache entry')
        self.assertFalse((root / 'npm-cache/_cacache/index-v5/marker').samefile(self.caller / '.npm/_cacache/index-v5/marker'))

    def test_names_never_collide_with_the_installed_release_app(self):
        # The 4.0.0 package installs as Chirality.app, identifier com.chirality.app.
        for identifier, product in (('com.chirality.app', 'Chirality App v4 (development x)'),
                                    ('COM.CHIRALITY.APP', 'Chirality App v4 (development x)'),
                                    ('dev.chirality.app-v4.skeleton', 'Chirality App v4 (development x)'),
                                    ('dev.chirality.app-v4.candidate.', 'Chirality App v4 (development )'),
                                    ('dev.chirality.app-v4.candidate.x.com.chirality.app', 'Chirality App v4 (development x)')):
            with self.subTest(identifier=identifier):
                with self.assertRaisesRegex(ValueError, 'development identifier'):
                    build_candidate.check_names(identifier, product)
        for product in ('Chirality', 'chirality', 'Chirality.app', 'Chirality App v4 (development y)'):
            with self.subTest(product=product):
                with self.assertRaisesRegex(ValueError, 'development product name'):
                    build_candidate.check_names('dev.chirality.app-v4.candidate.x', product)
        build_candidate.check_names('dev.chirality.app-v4.candidate.x', 'Chirality App v4 (development x)')
        for tag in ('com.chirality.app', 'x.com', 'Chirality)', ') (', '-', 'a--b', 'x y'):
            with self.subTest(tag=tag):
                with self.assertRaises(ValueError):
                    self.plan(tag=tag)
        p = self.plan(tag='x')
        self.assertEqual((p['identifier'], p['product']), ('dev.chirality.app-v4.candidate.x', 'Chirality App v4 (development x)'))
        for change in ({'identifier': 'com.chirality.app'}, {'productName': 'Chirality'}):
            with self.subTest(change=change):
                bad = dict(p, overlay=dict(p['overlay'], **change))
                with self.assertRaises(ValueError):
                    build_candidate.run(bad)
                self.assertFalse(Path(p['root']).exists())

    def test_plan_refuses_unsafe_output_roots_tags_inputs_and_half_a_supplier(self):
        (self.tmp / 'exists').mkdir()
        (self.tmp / 'real').mkdir(); (self.tmp / 'alias').symlink_to(self.tmp / 'real')
        (self.tmp / 'repo-alias').symlink_to(self.repo)
        for out, kw in (('exists', {}), ('repo/app/out', {}), ('repo', {}), ('alias/out', {}), ('missing/out', {}),
                        ('repo-alias/out', {}), ('out', {'tag': 'bad tag'}), ('out', {'supplier_archive': self.archive})):
            with self.subTest(out=out, kw=kw):
                with self.assertRaises(ValueError):
                    self.plan(out, **kw)
        for key, broken in (('rust_bin', self.tmp / 'exists'), ('npm_cache', self.caller / '.cargo'),
                            ('cargo_home', self.caller / '.npm'), ('node_bin', self.caller / 'toolchain/rust-bin')):
            with self.subTest(input=key):
                with self.assertRaises(ValueError):
                    self.plan(inputs=dict(self.inputs, **{key: str(broken)}))
        with self.assertRaisesRegex(ValueError, 'not on PATH'):
            build_candidate.plan(self.repo, 'HEAD', self.tmp / 'out', environ={'HOME': str(self.tmp), 'PATH': ''})

    def test_output_root_containment_is_by_identity_not_spelling(self):
        variant = self.tmp / 'REPO/app/out'
        if not variant.parent.exists():
            self.skipTest('the test filesystem is case-sensitive, so a case variant names a different place')
        with self.assertRaisesRegex(ValueError, 'output root is inside'):
            build_candidate.output_root(variant, self.repo)
        with self.assertRaisesRegex(ValueError, 'output root is inside'):
            build_candidate.output_root(self.tmp / 'Repo/App/out', self.repo)

    def test_output_root_refuses_reserved_roots_and_their_case_variants(self):
        # Paths only: output_root reads metadata and creates nothing.
        homes = {Path(os.path.expanduser('~')), Path(pwd.getpwuid(os.getuid()).pw_dir)}
        places = [Path('/Applications/out'), Path('/Library/out'), Path('/System/Library/out')]
        places += [h / 'Library/out' for h in homes] + [h / 'Applications/out' for h in homes if (h / 'Applications').is_dir()]
        if Path('/APPLICATIONS').exists():
            places += [Path('/applications/out'), Path('/library/out'), Path('/system/library/out')]
            places += [h / 'library/out' for h in homes]
        for out in places:
            if not out.parent.is_dir():
                continue
            with self.subTest(out=out):
                with self.assertRaisesRegex(ValueError, 'output root is inside'):
                    build_candidate.output_root(out, self.repo)
                self.assertFalse(out.exists())

    def test_a_path_inside_the_root_pointing_outside_refuses(self):
        p = self.plan()
        root = Path(p['root'])
        root_id = build_candidate.create_root(p)
        outside = self.tmp / 'outside'; outside.mkdir()
        (outside / 'file').write_bytes(b'outside')
        (root / 'source').symlink_to(outside)
        os.link(outside / 'file', root / 'build.log')
        for path, reason in ((root / 'source', 'symlink'), (root / 'source/app', 'symlink'),
                             (root / 'build.log', 'hard-linked'), (self.tmp / 'elsewhere', 'outside'),
                             (root / '../outside', 'outside')):
            with self.subTest(path=path):
                with self.assertRaisesRegex(ValueError, reason):
                    build_candidate.contained(root, root_id, path)
        build_candidate.contained(root, root_id, root / 'target/debug')

    def test_run_refuses_a_link_out_of_the_root_made_before_a_write(self):
        p = self.plan(supplier_archive=self.archive, supplier_record=self.record)
        outside = self.tmp / 'outside'; outside.mkdir()

        def export(repo, commit, source):
            os.mkdir(source)
            os.symlink(outside, Path(p['root']) / 'codex-package')
            return {'tracked_files_verified': 1}
        with mock.patch.object(build_candidate, 'export', export):
            with self.assertRaisesRegex(ValueError, 'symlink inside the output root'):
                build_candidate.run(p)
        self.assertEqual(list(outside.iterdir()), [])

    def test_facts_validate_as_the_build_object_of_v2_and_v3(self):
        from jsonschema import Draft202012Validator
        p = self.plan(supplier_archive=self.archive, supplier_record=self.record)
        facts = build_candidate.facts(p, '0' * 64, {'node': 'v0.0.0-invented', 'npm_cache_input': '/invented (copied)'},
                                      {'app/package-lock.json': '1' * 64}, WHEN, WHEN, {'tauri_build': WHEN + '/' + WHEN})
        for version in ('v2', 'v3'):
            with self.subTest(version=version):
                self.assertEqual(list(Draft202012Validator(build_schema(version)).iter_errors(facts)), [])
        overlay = facts['config_overlays'][1]
        self.assertEqual((overlay['path'], overlay['content']), (p['overlay_path'], p['overlay']))
        self.assertEqual(overlay['sha256'], identify.sha(p['overlay_bytes']))
        self.assertFalse(any(k.startswith(('APPLE', 'TAURI')) for k in facts['environment']))

    def test_prepare_supplier_extracts_exactly_the_record_inventory(self):
        tree = self.tmp / 'private/codex-package'; tree.parent.mkdir()
        previous = os.umask(0o077)  # directory modes come from the archive, not the umask
        try:
            account = build_candidate.prepare_supplier(self.archive, self.record, tree)
        finally:
            os.umask(previous)
        self.assertEqual(account['pin'], '0.0.1')
        self.assertEqual(build_candidate.tree_entries(tree), bundled_supplier.comparable(
            {e['path']: e for e in tree_inventory(self.vendor)}))
        self.assertEqual(stat.S_IMODE(tree.stat().st_mode), 0o755)

    def test_prepare_supplier_refuses_before_extracting_anything(self):
        def rewrite(change=None, extra=None, mode=None):
            with tarfile.open(self.archive, 'w:gz') as tar:
                for child in sorted(self.vendor.iterdir()):
                    tar.add(child, arcname=child.name, filter=lambda info: mode(info) if mode else info)
                for info, data in (extra or []):
                    tar.addfile(info, io.BytesIO(data) if data is not None else None)
            record = distribution_record(self.archive, tree_inventory(self.vendor))
            if change:
                change(record)
            self.record.write_text(json.dumps(record))

        def setuid(info):
            if info.name == 'bin/codex':
                info.mode = 0o4755
            return info
        link = tarfile.TarInfo('codex-path/link'); link.type = tarfile.SYMTYPE; link.linkname = 'rg'
        cases = {
            'digest': lambda: rewrite(lambda r: r['archive'].update(sha256='0' * 64)),
            'link': lambda: rewrite(extra=[(link, None)]),
            'set-id mode the data filter would clear': lambda: rewrite(mode=setuid),
            'inventory mode': lambda: rewrite(lambda r: r['inventory']['entries'][0].update(mode=0o700)),
            'inventory size': lambda: rewrite(lambda r: next(e for e in r['inventory']['entries'] if e['kind'] == 'file').update(size=1)),
            'npm form': lambda: self.record.write_text(json.dumps({'format': bundled_supplier.NPM_FORM})),
            'empty record': lambda: self.record.write_bytes(b''),
            'missing record': lambda: self.record.unlink(),
            'empty archive': lambda: self.archive.write_bytes(b''),
        }
        for index, (name, mutate) in enumerate(cases.items()):
            with self.subTest(name=name):
                release_archive(self.vendor, self.archive)
                self.record.write_text(json.dumps(distribution_record(self.archive, tree_inventory(self.vendor))))
                mutate()
                tree = self.tmp / f'private{index}/codex-package'; tree.parent.mkdir()
                with self.assertRaises((ValueError, KeyError, OSError)):
                    build_candidate.prepare_supplier(self.archive, self.record, tree)
                self.assertFalse(tree.exists(), name)

    def fake_steps(self, p, build_ok=True, bundle=True):
        calls = []

        def fake_run(command, env, cwd, log):
            calls.append((command, env, Path(cwd)))
            if command[0] == 'npm':
                cli = Path(cwd) / 'node_modules/@tauri-apps/cli'; cli.mkdir(parents=True)
                (cli / 'package.json').write_text('{"version": "0.0.0-invented"}')
            elif not build_ok:
                raise ValueError('node failed (exit 1); see build.log')
            elif bundle:
                Path(p['bundle']).mkdir(parents=True)
        return calls, mock.patch.object(build_candidate, '_run', fake_run), \
            mock.patch.object(build_candidate, '_version', lambda command, env, cwd: 'invented ' + command[0])

    def test_run_exports_verifies_and_writes_facts_with_build_steps_substituted(self):
        p = self.plan(supplier_archive=self.archive, supplier_record=self.record)
        calls, run_patch, version_patch = self.fake_steps(p)
        with run_patch, version_patch:
            facts = build_candidate.run(p)
        root = Path(p['root'])
        self.assertEqual(stat.S_IMODE(root.stat().st_mode), 0o700)
        self.assertEqual([c[0] for c in calls], [p['install'], p['build']])
        self.assertTrue(all(c[1] == p['env'] and c[2] == root / 'source/app' for c in calls))
        self.assertEqual(json.loads((root / 'build-facts.json').read_bytes()), facts)
        self.assertEqual(facts['lockfiles']['app/src-tauri/Cargo.lock'], identify.sha(b'version = 4\n'))
        self.assertEqual(facts['config_overlays'][0]['sha256'], identify.sha(b'{"identifier": "dev.example.skeleton"}\n'))
        self.assertEqual(facts['toolchain']['tauri_cli'], '0.0.0-invented')
        self.assertEqual(facts['toolchain']['npm_cache_input'], self.inputs['npm_cache'] + '/_cacache (read only; copied into the output root)')
        self.assertEqual(facts['toolchain']['cargo_home_input'], self.inputs['cargo_home'] + ': registry (read only; copied into the output root)')
        self.assertEqual((root / 'cargo-home/registry/cache/marker').read_bytes(), b'invented crate')
        self.assertEqual(json.loads((root / 'tauri.candidate.conf.json').read_bytes()), p['overlay'])
        self.assertEqual(build_candidate.tree_entries(root / 'codex-package'),
                         bundled_supplier.comparable({e['path']: e for e in tree_inventory(self.vendor)}))
        self.assertEqual(identify.verify_export(self.repo, self.commit, '.', root / 'source')['tracked_files_verified'], 4)

    def test_a_failed_or_bundleless_build_writes_no_facts_and_prints_no_next_step(self):
        for name, kw in (('build exits non-zero', {'build_ok': False}), ('no bundle produced', {'bundle': False})):
            with self.subTest(name=name):
                p = self.plan(out=name.replace(' ', '-'))
                _, run_patch, version_patch = self.fake_steps(p, **kw)
                out, err = io.StringIO(), io.StringIO()
                with run_patch, version_patch, mock.patch.object(build_candidate, 'plan', lambda *a, **k: p), \
                        contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    code = build_candidate.main(['--repo', str(self.repo), '--revision', 'HEAD', '--out', p['root']])
                self.assertEqual(code, 2)
                self.assertEqual(out.getvalue(), '')
                self.assertIn('error', json.loads(err.getvalue()))
                self.assertFalse((Path(p['root']) / 'build-facts.json').exists())

    def test_default_inputs_read_rustup_settings_without_running_a_shim(self):
        rustup = self.tmp / 'rustup'
        (rustup / 'toolchains/stable-invented/bin').mkdir(parents=True)
        (rustup / 'settings.toml').write_text('default_toolchain = "stable-invented"\n')
        shims = self.tmp / 'shims'; shims.mkdir()
        (shims / 'rustup').write_text('#!/bin/sh\nexit 99\n'); (shims / 'rustup').chmod(0o755)
        (shims / 'cargo').symlink_to(shims / 'rustup')
        node_bin = self.caller / 'toolchain/node-bin'; (node_bin / 'node').chmod(0o755)
        found = build_candidate.default_inputs({'HOME': str(self.caller), 'RUSTUP_HOME': str(rustup),
                                                'PATH': f'{node_bin}:{shims}'})
        self.assertEqual(found, {'node_bin': str(node_bin), 'rust_bin': str(rustup / 'toolchains/stable-invented/bin'),
                                 'npm_cache': str(self.caller / '.npm'), 'cargo_home': str(self.caller / '.cargo')})


if __name__ == '__main__':
    unittest.main()
