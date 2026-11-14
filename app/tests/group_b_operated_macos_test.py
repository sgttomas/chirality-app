"""The operated method's examination tools, the parts that ask macOS itself. macOS only.

These ask the system for a process's executable (libproc), read the login session's launch domain (launchctl), and
read the names in a process's environment (sysctl KERN_PROCARGS2). Elsewhere every test here is skipped, and says why; the portable tests of the same tools are in
group_b_operated_scenario_test.py. Selected by this file's name.
"""
import importlib.util
import os
from pathlib import Path
import subprocess
import struct
import contextlib
import io
import json
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

    SLEEP = ['-c', 'import time; time.sleep(30)']

    def run_names(self, pid, args=None, required=('INVENTED_PLAIN',)):
        # The target's known arguments: by default, the interpreter started as [sys.executable] + SLEEP.
        args = [sys.executable] + self.SLEEP if args is None else args
        command = [sys.executable, '-B', str(OPERATED / 'env_names.py'), str(pid), '--expect-args', json.dumps(args)]
        for name in required:
            command += ['--require', name]
        return subprocess.run(command, capture_output=True, text=True)

    def test_the_names_of_a_process_started_with_an_invented_environment_and_no_value(self):
        # A process this test starts, not an Apple platform binary (whose environment the kernel withholds): the
        # interpreter, sleeping, with exactly the invented environment.
        child = subprocess.Popen([sys.executable] + self.SLEEP, env=self.INVENTED)
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
        done = self.run_names(child.pid, args=['/bin/sleep', '30'])
        self.assertEqual((done.returncode, done.stdout), (2, ''))

    def test_no_such_process_is_cannot_be_read(self):
        done = self.run_names(99999999)
        self.assertEqual((done.returncode, done.stdout), (2, ''))

    def started(self, argv, environment):
        child = subprocess.Popen(argv, executable=sys.executable, env=environment)
        self.addCleanup(child.wait)
        self.addCleanup(child.kill)
        return child

    def test_an_empty_argv0_and_an_empty_later_argument_do_not_hide_the_environment(self):
        # The independent reading of PR 351 (round one): an empty argv[0] was taken for padding, and the environment
        # read as empty. Each of these must read back its invented names exactly.
        cases = {'an empty argv[0]': [''] + self.SLEEP,
                 'an empty later argument': ['invented'] + self.SLEEP + [''],
                 'both': [''] + self.SLEEP + ['', '']}
        for name, argv in cases.items():
            with self.subTest(name):
                child = self.started(argv, self.INVENTED)
                done = self.run_names(child.pid, args=argv)
                self.assertEqual((done.returncode, done.stdout.split('\n')[:-1]), (0, sorted(self.INVENTED)), done.stderr)

    def test_the_target_is_checked_against_what_is_known_of_it(self):
        # The arguments must equal the known ones exactly, and a required name must be there; otherwise nothing is
        # reported, the empty environment included.
        child = self.started(['invented'] + self.SLEEP, self.INVENTED)
        self.assertEqual(self.run_names(child.pid, args=['invented'] + self.SLEEP).returncode, 0)
        cases = {'other arguments than the known ones': dict(args=['invented'] + self.SLEEP + ['extra']),
                 'the known arguments in another order': dict(args=[self.SLEEP[1], self.SLEEP[0], 'invented']),
                 'a required name that is not there': dict(args=['invented'] + self.SLEEP, required=('INVENTED_ABSENT',))}
        for name, kwargs in cases.items():
            with self.subTest(name):
                done = self.run_names(child.pid, **kwargs)
                self.assertEqual((done.returncode, done.stdout), (2, ''))
        empty = self.started(['invented'] + self.SLEEP, {})
        done = self.run_names(empty.pid, args=['invented'] + self.SLEEP)
        self.assertEqual((done.returncode, done.stdout), (2, ''), 'an empty result is not observed')
        for argv in ([], [str(child.pid)], [str(child.pid), '--expect-args', '[]'], [str(child.pid), '--require', 'X']):
            with self.subTest(usage=argv):
                done = subprocess.run([sys.executable, '-B', str(OPERATED / 'env_names.py')] + argv, capture_output=True, text=True)
                self.assertEqual((done.returncode, done.stdout), (2, ''))

    def load(self):
        spec = importlib.util.spec_from_file_location('env_names_under_test', OPERATED / 'env_names.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_the_calibration_withholds_the_real_read_when_the_parsing_is_wrong(self):
        # Put back the parsing the first reading found wrong (every NUL after the path skipped): the calibration's
        # empty-argv[0] child no longer reads back, so the real read is not made and nothing is printed.
        module = self.load()
        right = module.parse

        def skipping_every_nul(block):
            end = block.find(b'\0', 4)
            at = end
            while at < len(block) and block[at] == 0:
                at += 1
            fake = block[:end + 1] + b'\0' * ((8 - (end + 1 - 4) % 8) % 8) + block[at:]
            return right(fake)

        read = []
        real_read_block = module.read_block
        module.read_block = lambda pid: (read.append(pid), real_read_block(pid))[1]
        module.parse = skipping_every_nul
        argv = ['invented'] + self.SLEEP
        target = self.started(argv, self.INVENTED)
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = module.main([str(target.pid), '--expect-args', json.dumps(argv), '--require', 'INVENTED_PLAIN'])
        self.assertEqual((code, out.getvalue()), (2, ''))
        self.assertNotIn(target.pid, read)
        # With the right parsing back, the same target reads.
        module.parse = right
        self.assertTrue(module.calibrated())
        self.assertEqual(module.names(target.pid, [arg.encode() for arg in argv], ['INVENTED_PLAIN']), sorted(self.INVENTED))

    def test_a_buffer_that_may_be_cut_or_is_unended_is_not_read(self):
        module = self.load()
        size = 4096

        def returning(block):
            return lambda libc, mib, asked: struct.pack('i', size) if len(mib) == 2 else block

        whole = struct.pack('i', 1) + b'/x\0\0\0\0\0\0' + b'a\0N=v\0\0apple=x\0'
        module._sysctl = returning(whole)
        self.assertEqual(module.read_block(1), whole)
        for name, block in {'as long as the size asked for': whole + b'\0' * (size - len(whole)),
                            'its last string not ended': whole + b'apple2=y'}.items():
            with self.subTest(name):
                module._sysctl = returning(block)
                self.assertIsNone(module.read_block(1))

    def test_a_block_not_of_the_layout_is_not_read_as_an_environment(self):
        module = self.load()
        path = b'/invented/exe\0'
        head = path + b'\0' * ((8 - len(path) % 8) % 8)   # argc (4 bytes) + path, padded to 4 + 8k

        def block(argc, rest):
            return struct.pack('i', argc) + head + rest

        good = block(1, b'arg\0NAME=v\0\0apple=x\0')
        self.assertEqual(module.parse(good), ([b'arg'], ['NAME']))
        cases = {
            'the block ends exactly after the arguments (as for an Apple binary)': block(1, b'arg\0'),
            'the closing empty string ends the block': block(1, b'arg\0NAME=v\0\0'),
            'an entry with no "="': block(1, b'arg\0NOEQUALS\0\0apple=x\0'),
            'an entry with an empty name': block(1, b'arg\0=v\0\0apple=x\0'),
            'fewer arguments than argc': block(3, b'arg\0'),
            'padding that is not NUL': struct.pack('i', 1) + path + b'X' * ((8 - len(path) % 8) % 8 or 8) + b'arg\0N=v\0\0a=x\0',
        }
        for name, data in cases.items():
            with self.subTest(name):
                self.assertIsNone(module.parse(data))
