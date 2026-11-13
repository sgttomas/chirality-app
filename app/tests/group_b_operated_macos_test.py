"""The operated method's examination tools, the parts that ask macOS itself. macOS only.

These ask the system for a process's executable (libproc) and read the login session's launch domain
(launchctl). Elsewhere every test here is skipped, and says why; the portable tests of the same tools are in
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
    def test_the_system_is_asked_for_an_executable_by_process_number(self):
        stray = load('stray')
        own = stray.executable_of(os.getpid())
        self.assertTrue(os.path.samefile(own, sys.executable), (own, sys.executable))
        gone = subprocess.Popen(['/usr/bin/true'])
        gone.wait()
        self.assertIsNone(stray.executable_of(gone.pid))

    def test_this_users_processes_are_listed_and_this_one_is_found_by_its_executable(self):
        stray = load('stray')
        lines = [line.split() for line in stray.listing()]
        self.assertIn(str(os.getpid()), [parts[0] for parts in lines if parts])
        found, _ = stray.processes(os.path.realpath(sys.executable))
        self.assertIn(os.getpid(), [entry['pid'] for entry in found])


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
