"""The operated method's examination tools, the parts that ask macOS itself. macOS only.

These ask the system for a process's executable (libproc), read the login session's launch domain (launchctl), and
read the names in a process's environment (sysctl KERN_PROCARGS2). Elsewhere every test here is skipped, and says why; the portable tests of the same tools are in
group_b_operated_scenario_test.py. Selected by this file's name.
"""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import unittest

OPERATED = Path(__file__).resolve().parents[1] / 'examination/standalone/operated'
MACOS_ONLY = 'macOS only: asks libproc and launchctl, which this system does not have'


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


@unittest.skipUnless(sys.platform == 'darwin', MACOS_ONLY)
class SessionEnvironmentOnMacOS(unittest.TestCase):
    def test_the_launch_domain_is_read_or_every_name_is_said_to_be_not_established(self):
        # Never a skip: where this machine has no login session launch domain to read (a hosted runner may not),
        # the tool must say so for every name and exit 2, which is what is asserted then.
        env = load('session_env')
        done = subprocess.run(['/bin/launchctl', 'print', f'gui/{os.getuid()}'], capture_output=True, text=True)
        names, reason = env.session_names(done.stdout) if done.returncode == 0 else (None, f'launchctl print exited {done.returncode}')
        result = env.states(names, reason, set(), None)
        self.assertEqual(set(result), set(env.NAMES))
        if names is None:
            self.assertTrue(all(v.startswith('could not be established: ') for v in result.values()), result)
            self.assertEqual(env.status(result), 2)
        else:
            self.assertTrue(set(result.values()) <= {'absent', 'present'}, result)


if __name__ == '__main__':
    unittest.main()


@unittest.skipUnless(sys.platform == 'darwin', MACOS_ONLY)
class EnvironmentNamesOnMacOS(unittest.TestCase):
    """env_names.py prints exactly a process's environment names, however its values are written, and nothing of them."""

    INVENTED = {'INVENTED_PLAIN': 'one', 'INVENTED_SPACES': 'a b c = d e', 'INVENTED_BREAK': 'first\nsecond=third',
                'INVENTED_EQUALS': '=x==y', 'INVENTED_LOOKS_LIKE_A_NAME': 'NOT_A_NAME=1 ANOTHER=2'}

    def run_names(self, pid):
        return subprocess.run([sys.executable, '-B', str(OPERATED / 'env_names.py'), str(pid)], capture_output=True, text=True)

    def test_the_names_of_a_process_started_with_an_invented_environment_and_no_value(self):
        # A process this test starts, not an Apple platform binary (whose environment the kernel withholds): the
        # interpreter, sleeping, with exactly the invented environment.
        child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'], env=self.INVENTED)
        self.addCleanup(child.wait)
        self.addCleanup(child.kill)
        for _ in range(50):
            done = self.run_names(child.pid)
            if done.returncode == 0 and done.stdout:
                break
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(done.stdout.split('\n')[:-1], sorted(self.INVENTED))
        # A value that reads like further entries yields none: the output is the names alone.
        self.assertNotIn('NOT_A_NAME', done.stdout)
        self.assertNotIn('ANOTHER', done.stdout)

    def test_a_withheld_environment_is_not_reported_as_empty(self):
        # The kernel gives no environment for an Apple platform binary: that is "cannot be read", exit 2, nothing printed.
        child = subprocess.Popen(['/bin/sleep', '30'], env={'INVENTED_PLAIN': 'one'})
        self.addCleanup(child.wait)
        self.addCleanup(child.kill)
        done = self.run_names(child.pid)
        self.assertEqual((done.returncode, done.stdout), (2, ''))

    def test_no_such_process_is_cannot_be_read(self):
        done = self.run_names(99999999)
        self.assertEqual((done.returncode, done.stdout), (2, ''))
