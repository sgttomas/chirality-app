"""The operated method's examination tools, the parts that ask macOS itself. macOS only.

These ask the system for a process's executable (libproc) and read the login session's launch domain
(launchctl). Elsewhere every test here is skipped, and says why; the portable tests of the same tools are in
group_b_operated_scenario_test.py. Selected by this file's name.
"""
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
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
        # This process too, against a second answer from the system and not the interpreter's own: lsof's first
        # program text entry of this one process (lsof -a -p <pid> -d txt -Fn; never comm, which is argv[0], and
        # never an unrestricted lsof). It must answer with a path, and the two must be the same file.
        own = stray.executable_of(os.getpid())
        self.assertTrue(os.path.isfile(own), own)
        asked = subprocess.run(['/usr/sbin/lsof', '-a', '-p', str(os.getpid()), '-d', 'txt', '-Fn'], capture_output=True, text=True,
                               env={'PATH': '/bin:/usr/bin:/usr/sbin'})
        names = [line[1:] for line in asked.stdout.splitlines() if line.startswith('n')]
        self.assertEqual(asked.returncode, 0, asked.stderr)
        self.assertTrue(names, 'lsof gave no program text entry for this process')
        self.assertTrue(os.path.samefile(own, names[0]), (own, names[0]))
        gone = subprocess.Popen(['/usr/bin/true'])
        gone.wait()
        self.assertIsNone(stray.executable_of(gone.pid))

    def test_proc_reads_executable_is_the_process_own_program(self):
        # What earns proc_read.py's field its name (App Agent 0, 15 November): the first program text entry lsof
        # reports for one process (lsof -a -p <pid> -d txt -Fn, the first n line) is that process's own program file,
        # here checked against two processes whose program is known: a /bin/sleep this test started, and this test's
        # own process, whose program the system gives by number (stray.executable_of, proc_pidpath).
        proc_read = load('proc_read')
        child = self.started()
        self.assertTrue(os.path.samefile(proc_read.executable(child.pid), self.STAND_IN))
        self.assertTrue(os.path.samefile(proc_read.executable(os.getpid()), load('stray').executable_of(os.getpid())))
        self.assertTrue(os.path.samefile(proc_read.details(child.pid)['executable'], self.STAND_IN))

    def test_this_users_processes_are_listed_by_number_and_one_this_test_started_is_found_by_its_executable(self):
        stray = load('stray')
        child = self.started()
        lines = [line.split() for line in stray.listing()]
        self.assertTrue(all(len(parts) == 1 and parts[0].isdigit() for parts in lines if parts), 'the listing holds numbers only')
        self.assertIn(str(child.pid), [parts[0] for parts in lines if parts])
        self.assertIn(str(os.getpid()), [parts[0] for parts in lines if parts])
        found, ours = stray.processes(self.STAND_IN)
        self.assertIn(child.pid, [entry['pid'] for entry in found])
        self.assertNotIn(os.getpid(), [entry['pid'] for entry in found])
        self.assertEqual(ours, [])
        self.assertEqual(set(found[0]), {'pid', 'parent', 'started', 'executable'})

    def test_only_processes_of_ours_are_kept_and_every_other_is_discarded_uncounted(self):
        # Invented numbers and paths: one runs the bundle's executable, one an executable under the candidate's
        # folder, one under the lane's folder, and two are another program and one with no path. Only the first three
        # are kept, each with what is read of it; the others leave no trace in what is returned.
        stray = load('stray')
        child = self.started()
        top = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, top, True)
        for name in ('candidate/target/release/helper', 'lane/tool'):
            os.makedirs(os.path.dirname(os.path.join(top, name)), exist_ok=True)
            Path(top, name).write_text('invented')
        paths = {child.pid: self.STAND_IN, 900001: f'{top}/candidate/target/release/helper', 900002: f'{top}/lane/tool',
                 900003: '/usr/bin/true', 900004: stray.NO_PATH}
        asked_start = []

        def started_of(pid):
            asked_start.append(pid)
            return (1, 'Sat Nov 14 12:00:00 2026')
        found, ours = stray.processes(self.STAND_IN, lines=[str(pid) for pid in paths], path_of=paths.get,
                                      folders=[f'{top}/candidate', f'{top}/lane'], started_of=started_of)
        self.assertEqual([entry['pid'] for entry in found], [child.pid])
        self.assertEqual(sorted(entry['pid'] for entry in ours), [900001, 900002])
        self.assertEqual(sorted(asked_start), sorted([child.pid, 900001, 900002]))  # nothing more is read of the others


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
