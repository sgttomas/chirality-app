"""Fake-HOME regressions for signed_witness_collect.sh (no App, keychain, mount or account).

Run: WITNESS_TEST_TMP=$(mktemp -d /Users/ryan/dev/chirality-t3/scratch/app-witness-tests-XXXXXXXX) \
       python3 -m unittest execution/PKG-09/DEL-09-02/Work/test_signed_witness_collect.py
Without WITNESS_TEST_TMP the tests use /Users/ryan/dev/chirality-t3/scratch, or skip if absent.
"""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

HELPER = Path(__file__).with_name('signed_witness_collect.sh')
SIGNED = Path('/Users/ryan/dev/chirality-t3/scratch/app-signed-candidate-8DnXAldk/Chirality App v4.app')
DMG = SIGNED.parent / 'Chirality-App-v4-4.0.0-f664ee1d-b3dd4145.dmg'
APPDATA_REL = 'Library/Application Support/com.chirality.app'
SCRATCH = os.environ.get('WITNESS_TEST_TMP') or '/Users/ryan/dev/chirality-t3/scratch'


class Helper(unittest.TestCase):
    def setUp(self):
        if not os.path.isdir(SCRATCH):
            self.skipTest('task scratch not present; set WITNESS_TEST_TMP')
        self.tmp = Path(tempfile.mkdtemp(prefix='witness-test-', dir=SCRATCH)).resolve()
        self.home = self.tmp / 'home'
        self.home.mkdir()
        self.out = self.tmp / 'out'
        # The admin refusal is tested once; other cases use a copy without it.
        self.na = self.tmp / 'na.sh'
        self.na.write_text(''.join(l for l in HELPER.read_text().splitlines(True) if 'grep -qx admin' not in l))
        self.env = dict(os.environ, HOME=str(self.home), CHIRALITY_WITNESS_OUT=str(self.out), TMPDIR=str(self.tmp))
        self.appdata = self.home / APPDATA_REL

    def tearDown(self):
        for p in self.tmp.rglob('*'):
            if p.is_dir() and not p.is_symlink():
                p.chmod(0o755)
        shutil.rmtree(self.tmp)

    def run_(self, *args, script=None):
        return subprocess.run(['sh', str(script or self.na), *args], env=self.env, capture_output=True, text=True)

    def prepared(self):
        self.assertEqual(self.run_('prepare').returncode, 0)
        self.prepared_after_prepare()

    def prepared_after_prepare(self):
        (self.appdata / 'records/projects/k1/captures').mkdir(parents=True)
        (self.appdata / 'records/projects/k1/captures/c.json').write_text('{}')
        (self.appdata / 'runtime/distribution/s1-a/.chirality-s1').mkdir(parents=True)
        (self.appdata / 'runtime/distribution/s1-a/.chirality-s1/observed.json').write_text('{}')
        (self.appdata / 'account-homes/account-x').mkdir(parents=True)
        (self.appdata / 'account-homes/account-x/auth.json').write_text('SECRET')
        (self.appdata / 'account-homes').chmod(0o000)

    def test_prepare_refuses_admin_and_creates_private_root(self):
        if 'admin' in subprocess.run(['id', '-Gn'], capture_output=True, text=True).stdout.split():
            self.assertEqual(self.run_('prepare', script=HELPER).returncode, 2)
        self.assertEqual(self.run_('prepare').returncode, 0)
        self.assertEqual(self.out.stat().st_mode & 0o777, 0o700)
        self.assertEqual(self.run_('prepare').returncode, 2)

    def test_checkpoints_copy_allowlist_privately_without_entering_account_homes(self):
        self.prepared()
        for c in ('c2', 'c3', 'c4'):
            self.assertEqual(self.run_(c).returncode, 0, c)
        files = {str(p.relative_to(self.out / 'c4')) for p in (self.out / 'c4').rglob('*') if p.is_file()}
        self.assertIn('appdata/records/projects/k1/captures/c.json', files)
        self.assertIn('appdata/runtime/distribution/s1-a/.chirality-s1/observed.json', files)
        self.assertIn('fixture-manifest.txt', files)
        self.assertFalse(any('SECRET' in p.read_text(errors='ignore') for p in (self.out / 'c4').rglob('*') if p.is_file()))
        self.assertEqual((self.out / 'c4/appdata/records/projects/k1/captures/c.json').stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.run_('c4').returncode, 2)  # never overwrites

    def test_fixture_root_symlink_refused(self):
        self.prepared()
        outside = self.tmp / 'outside'
        outside.mkdir()
        (outside / 'x.txt').write_text('outside')
        shutil.rmtree(self.home / 'ChiralityV4Fixtures')
        (self.home / 'ChiralityV4Fixtures').symlink_to(outside)
        r = self.run_('c4')
        self.assertEqual(r.returncode, 2)
        self.assertIn('symlink', r.stderr)

    def test_marker_directory_symlink_refused_before_metadata(self):
        self.prepared()
        outside = self.tmp / 'outside'
        outside.mkdir()
        (outside / 'continuity.s1.json').write_text('{}')
        (self.appdata / 'capture-seal-keychain').symlink_to(outside)
        r = self.run_('c2')
        self.assertEqual(r.returncode, 2)
        self.assertFalse((self.out / 'c2/marker-stat.txt').exists())

    def test_capture_and_distribution_directory_symlinks_refused(self):
        self.prepared()
        caps = self.appdata / 'records/projects/k1/captures'
        shutil.rmtree(caps)
        caps.symlink_to(self.tmp)
        self.assertEqual(self.run_('c3').returncode, 2)

    def test_manifest_rejects_newline_names_special_files_and_read_errors(self):
        tree = self.tmp / 'tree'
        tree.mkdir()
        (tree / 'a').write_text('a')
        self.assertEqual(self.run_('manifest', str(tree)).returncode, 0)
        odd = tree / 'b\nc'
        odd.write_text('x')
        self.assertEqual(self.run_('manifest', str(tree)).returncode, 2)
        odd.unlink()
        os.mkfifo(tree / 'fifo')
        self.assertEqual(self.run_('manifest', str(tree)).returncode, 2)
        (tree / 'fifo').unlink()
        (tree / 'a').chmod(0o000)
        r = self.run_('manifest', str(tree))
        self.assertEqual(r.returncode, 2)
        self.assertEqual(r.stdout.strip(), '')
        (tree / 'a').chmod(0o644)

    def test_manifest_refuses_unreadable_directory_and_symlinked_root(self):
        tree = self.tmp / 'tree'
        (tree / 'sub').mkdir(parents=True)
        (tree / 'sub/hidden').write_text('a')
        (tree / 'sub').chmod(0o000)
        r = self.run_('manifest', str(tree))
        self.assertEqual(r.returncode, 2)
        self.assertEqual(r.stdout.strip(), '')
        (tree / 'sub').chmod(0o755)
        link = self.tmp / 'link'
        link.symlink_to(tree)
        self.assertEqual(self.run_('manifest', str(link)).returncode, 2)

    def test_manifest_fails_when_find_or_sort_fails(self):
        tree = self.tmp / 'tree'
        tree.mkdir()
        (tree / 'a').write_text('a')
        for tool in ('find', 'sort'):
            shim = self.tmp / f'shim-{tool}'
            shim.mkdir()
            (shim / tool).write_text('#!/bin/sh\nexit 1\n')
            (shim / tool).chmod(0o755)
            env = dict(self.env, PATH=f'{shim}:{os.environ["PATH"]}')
            r = subprocess.run(['sh', str(self.na), 'manifest', str(tree)], env=env, capture_output=True, text=True)
            self.assertEqual(r.returncode, 2, tool)
            self.assertEqual(r.stdout.strip(), '', tool)

    def test_c1_refuses_symlinked_dmg(self):
        self.assertEqual(self.run_('prepare').returncode, 0)
        real = self.tmp / 'real.dmg'
        real.write_text('x')
        (self.home / 'Downloads').mkdir()
        link = self.home / 'Downloads/linked.dmg'
        link.symlink_to(real)
        self.assertEqual(self.run_('c1', str(link)).returncode, 2)
        self.assertFalse((self.out / 'c1').exists())

    def test_handoff_grants_one_named_account(self):
        self.prepared()
        self.assertEqual(self.run_('c2').returncode, 0)
        me = subprocess.run(['id', '-un'], capture_output=True, text=True).stdout.strip()
        self.assertEqual(self.run_('handoff', 'no-such-account-x9').returncode, 2)
        self.assertEqual(self.run_('handoff', me).returncode, 0)
        for p in (self.out, self.out / 'c2/who.txt'):
            acl = subprocess.run(['ls', '-led', str(p)], capture_output=True, text=True).stdout
            self.assertIn(f'user:{me} allow', acl)
            self.assertEqual(acl.count(' allow '), 1)

    def test_unreadable_capture_or_marker_directory_is_refused_not_absent(self):
        self.prepared()
        caps = self.appdata / 'records/projects/k1/captures'
        caps.chmod(0o000)
        self.assertNotEqual(self.run_('c2').returncode, 0)
        caps.chmod(0o755)
        shutil.rmtree(self.out / 'c2')
        marker = self.appdata / 'capture-seal-keychain'
        marker.mkdir()
        (marker / 'continuity.s1.json').write_text('{}')
        marker.chmod(0o000)
        self.assertNotEqual(self.run_('c2').returncode, 0)
        marker.chmod(0o755)

    def test_evidence_manifest_enumeration_failure_is_not_success(self):
        self.prepared()
        shim = self.tmp / 'shim-find'
        shim.mkdir()
        (shim / 'find').write_text('#!/bin/sh\ncase "$*" in *MANIFEST.sha256*) exit 1 ;; esac\nexec /usr/bin/find "$@"\n')
        (shim / 'find').chmod(0o755)
        env = dict(self.env, PATH=f'{shim}:{os.environ["PATH"]}')
        r = subprocess.run(['sh', str(self.na), 'c3'], env=env, capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn('wrote', r.stdout)
        self.assertNotIn('OK:', r.stdout)

    def test_unreadable_ancestor_is_refused_not_absent(self):
        self.prepared()
        lib = self.home / 'Library'
        lib.chmod(0o000)
        r = self.run_('c2')
        lib.chmod(0o755)
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn('OK:', r.stdout)

    def test_unexpected_evidence_types_are_refused_not_skipped(self):
        self.prepared()
        fifo = self.appdata / 'records/projects/k1/captures/failed.json'
        os.mkfifo(fifo)
        self.assertNotEqual(self.run_('c3').returncode, 0)
        fifo.unlink()
        (self.appdata / 'desktop-startup').mkdir()
        (self.appdata / 'desktop-startup/request.json').symlink_to(self.tmp / 'missing')
        self.assertNotEqual(self.run_('c4').returncode, 0)
        (self.appdata / 'desktop-startup/request.json').unlink()
        (self.appdata / 'runtime/distribution/s1-file').write_text('x')
        shutil.rmtree(self.out / 'c4')
        self.assertNotEqual(self.run_('c4').returncode, 0)

    def test_pending_captures_are_collected(self):
        self.prepared()
        pend = self.appdata / 'records/projects/k1/captures/pending'
        pend.mkdir()
        (pend / 'p.json').write_text('{}')
        self.assertEqual(self.run_('c2').returncode, 0)
        self.assertTrue((self.out / 'c2/appdata/records/projects/k1/captures/pending/p.json').is_file())

    def test_every_successful_command_ends_with_ok_line(self):
        r = self.run_('prepare')
        self.assertEqual(r.stdout.strip().splitlines()[-1], 'OK: prepare complete')
        self.prepared_after_prepare()
        r = self.run_('c2')
        self.assertEqual(r.stdout.strip().splitlines()[-1], 'OK: c2 complete')
        me = subprocess.run(['id', '-un'], capture_output=True, text=True).stdout.strip()
        r = self.run_('handoff', me)
        self.assertTrue(r.stdout.strip().splitlines()[-1].startswith('OK: handoff complete'))

    def test_checkpoint_requires_app_data(self):
        self.assertEqual(self.run_('prepare').returncode, 0)
        self.assertNotEqual(self.run_('c2').returncode, 0)

    def test_manifest_detects_content_change(self):
        tree = self.tmp / 'tree'
        tree.mkdir()
        (tree / 'a').write_text('a')
        first = self.run_('manifest', str(tree)).stdout
        (tree / 'a').write_text('b')
        self.assertNotEqual(first, self.run_('manifest', str(tree)).stdout)

    @unittest.skipUnless(SIGNED.is_dir() and DMG.is_file(), 'retained signed candidate not present')
    def test_c1_on_quarantined_clone_passes_all_but_mount_and_dmg_quarantine(self):
        self.assertEqual(self.run_('prepare').returncode, 0)
        apps = self.home / 'Applications'
        apps.mkdir()
        subprocess.run(['cp', '-cR', str(SIGNED), str(apps)], check=True)
        app = apps / SIGNED.name
        subprocess.run(['xattr', '-w', 'com.apple.quarantine', '0083;00000000;witness-test;', str(app)], check=True)
        r = self.run_('c1', str(DMG))
        self.assertEqual(r.returncode, 3)
        stops = {l.split()[1] for l in (self.out / 'c1/gate.txt').read_text().splitlines() if l.startswith('STOP')}
        self.assertEqual(stops, {'dmg-quarantine', 'mounted-gatekeeper'})
        (app / 'Contents/Resources/link').symlink_to('/etc/hosts')
        shutil.rmtree(self.out / 'c1')
        self.assertEqual(self.run_('c1', str(DMG)).returncode, 2)


if __name__ == '__main__':
    unittest.main()
