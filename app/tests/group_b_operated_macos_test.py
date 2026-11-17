"""The operated method's examination tools, the parts that ask macOS itself. macOS only.

These ask the system for a process's executable (libproc). Elsewhere every test here is skipped, and says why; the
portable tests of the same tools are in group_b_operated_scenario_test.py. Selected by this file's name. The launch
domain is not asked by any test: session_env.py is tested with an injected domain only.
"""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import unittest

OPERATED = Path(__file__).resolve().parents[1] / 'examination/standalone/operated'
MACOS_ONLY = 'macOS only: asks libproc, which this system does not have'


def load(name):
    spec = importlib.util.spec_from_file_location(f'{name}_under_test', OPERATED / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@unittest.skipUnless(sys.platform == 'darwin', MACOS_ONLY)
class StraySearchOnMacOS(unittest.TestCase):
    # The process whose executable is known is one this test starts from a path it chose (STAND_IN), never the
    # interpreter running the test: a framework Python (the hosted runner's, or Xcode's) is started through a
    # launcher, so sys.executable names a file the test's own process does not run.
    STAND_IN = '/bin/sleep'

    def started(self):
        child = subprocess.Popen([self.STAND_IN, '60'])

        def end():
            child.kill()
            child.wait()
        self.addCleanup(end)
        return child

    def test_the_system_is_asked_for_an_executable_by_process_number(self):
        stray = load('stray')
        child = self.started()
        asked = stray.executable_of(child.pid)
        self.assertTrue(os.path.samefile(asked, self.STAND_IN), (asked, self.STAND_IN))
        # This process too, against a second answer from the system and not the interpreter's own: ps reports the
        # path a process was executed by. ps must answer; a failure or an empty answer fails the test. The paths are
        # compared only when ps gives an absolute one: a relative one cannot be resolved from here, and then this
        # process's executable is checked only to be a file, its identity left unexamined (the started child above
        # is the comparison that never depends on this).
        own = stray.executable_of(os.getpid())
        self.assertTrue(os.path.isfile(own), own)
        asked_ps = subprocess.run(['/bin/ps', '-p', str(os.getpid()), '-o', 'comm='], capture_output=True, text=True,
                                  env={'PATH': '/bin:/usr/bin'})
        said = asked_ps.stdout.strip()
        self.assertEqual(asked_ps.returncode, 0, asked_ps.stderr)
        self.assertTrue(said, 'ps gave no path for this process')
        if os.path.isabs(said):
            self.assertTrue(os.path.samefile(own, said), (own, said))
        gone = subprocess.Popen(['/usr/bin/true'])
        gone.wait()
        self.assertIsNone(stray.executable_of(gone.pid))

    def test_this_users_processes_are_listed_and_one_this_test_started_is_found_by_its_executable(self):
        stray = load('stray')
        child = self.started()
        lines = [line.split() for line in stray.listing()]
        self.assertIn(str(child.pid), [parts[0] for parts in lines if parts])
        self.assertIn(str(os.getpid()), [parts[0] for parts in lines if parts])
        found, _ = stray.processes(self.STAND_IN)
        self.assertIn(child.pid, [entry['pid'] for entry in found])
        self.assertNotIn(os.getpid(), [entry['pid'] for entry in found])


if __name__ == '__main__':
    unittest.main()
