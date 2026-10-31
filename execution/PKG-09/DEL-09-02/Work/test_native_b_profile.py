"""Local macOS policy fixtures; no App, supplier, auth or model execution."""
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('B_profile', Path(__file__).with_name('native_successor_relaunch.py'))
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


@unittest.skipUnless(sys.platform == 'darwin', 'macOS sandbox policy')
class Profile(unittest.TestCase):
    def run_fixture(self, allow_allocator):
        with tempfile.TemporaryDirectory(prefix='B-profile-fixture-', dir=b.T3 / 'scratch') as temp:
            root = Path(temp).resolve()
            (root / 'tmp').mkdir(mode=0o700)
            for name in ('home', 'codex-home'):
                (root / 'tmp' / name).mkdir(mode=0o700)
            (root / 'stdout.log').touch(mode=0o600)
            control = root / 'release-observer-after-app-exit.json'
            control.write_text('invented operator-only input')
            control.chmod(0o600)
            python = str(Path(sys.executable).resolve())
            value = {'executable': python, 'bundle': str(root / 'unexecuted-fixture.app')}
            rules = b.policy(value, root)
            if not allow_allocator:
                rules = rules.replace(' (literal "/usr/bin/mktemp")', '')
            program = '''import os,json,subprocess,stat
from pathlib import Path
root=Path(os.environ['TMPDIR']).parent
facts={}
try:
 result=subprocess.run(['/usr/bin/mktemp','-d',str(root/'tmp/chirality-codex-probe.XXXXXX')],capture_output=True,text=True,check=True)
 path=Path(result.stdout.strip()); info=path.stat()
 facts['allocator']={'parent_matches':path.parent==root/'tmp','mode':stat.S_IMODE(info.st_mode),'owned':info.st_uid==os.getuid()}
except PermissionError as error: facts['allocator']={'denied_errno':error.errno}
for name,operation in [('control_read',lambda:(root/'release-observer-after-app-exit.json').read_text()),('control_write',lambda:(root/'release-observer-after-app-exit.json').write_text('bad')),('output_unlink',lambda:(root/'stdout.log').unlink()),('output_rename',lambda:(root/'stdout.log').rename(root/'tmp/moved-log'))]:
 try: operation(); facts[name]='unexpectedly allowed'
 except PermissionError: facts[name]='denied'
(root/'tmp/allowed-output').write_text('invented')
(root/'stdout.log').write_text('invented App output')
print(json.dumps(facts))
'''
            result = subprocess.run(['/usr/bin/sandbox-exec', '-p', rules, python, '-c', program],
                env={'PATH': '/usr/bin:/bin', 'HOME': str(root / 'tmp/home'),
                     'CODEX_HOME': str(root / 'tmp/codex-home'), 'TMPDIR': str(root / 'tmp'),
                     'PYTHONDONTWRITEBYTECODE': '1'},
                stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(control.read_text(), 'invented operator-only input')
            self.assertEqual((root / 'stdout.log').read_text(), 'invented App output')
            facts = json.loads(result.stdout)
            self.assertEqual(facts['control_read'], 'denied')
            self.assertEqual(facts['control_write'], 'denied')
            self.assertEqual(facts['output_unlink'], 'denied')
            self.assertEqual(facts['output_rename'], 'denied')
            return facts

    def test_missing_allocator_exec_is_denied_without_freshening_any_app_state(self):
        self.assertEqual(self.run_fixture(False)['allocator'], {'denied_errno': 1})

    def test_exact_allocator_creates_private_probe_while_control_channel_stays_denied(self):
        self.assertEqual(self.run_fixture(True)['allocator'],
                         {'parent_matches': True, 'mode': 0o700, 'owned': True})


if __name__ == '__main__':
    unittest.main()
