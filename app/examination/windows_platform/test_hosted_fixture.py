"""Host-only negative/boundary tests; never native Windows fixture evidence."""
from contextlib import redirect_stderr
import hashlib
import importlib.util
import io
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('hosted_fixture', HERE / 'run_hosted_fixture.py')
DRIVER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DRIVER)
VERIFY_SPEC = importlib.util.spec_from_file_location('fixture_verifier', HERE / 'verify_results.py')
VERIFIER = importlib.util.module_from_spec(VERIFY_SPEC)
VERIFY_SPEC.loader.exec_module(VERIFIER)


class AProofBoundaries(unittest.TestCase):
    """Invented parser units only; never emit/save a purported native suite."""
    def proof(self):
        setup = 'post-managed-start-stdout/v1'
        details = [
            (101, 'A_DEADLINE', 'startQpc=100;untilQpc=8100;startMs=0;untilMs=8000;frequency=1000'),
            (105, 'CREATED_LEADER', 'suspended=True;safety=true;handle=80'),
            (112, 'HELPER_A_PIPE', f'qpc=110;setup={setup};sourceRead=91;sourceWrite=92;startupStdin=89;startupStdout=90;startupStderr=90;readNoninherit=True;writeNoninherit=True;pipeType=2'),
            (115, 'A_PIPE_READER', f'setup={setup};sourceLeaderHandle=80;sourceRead=91;sourceWrite=92;handle=70;noninherit=True;pipeType=2;sameAccess=True'),
            (116, 'A_PIPE_ACK', 'sourceLeaderHandle=80;reader=70;ownershipEstablished=True'),
            (122, 'HELPER_ENTRY', f'qpc=120;setup={setup};stdout=92;sourceRead=91;ackQpc=117;readCloseQpc=118;bindQpc=119;setOk=True;getMatch=True;pipeType=2;startupStdout=90;startupStderr=90'),
            (123, 'A_READ_START', 'handle=70;leaderHandle=80;untilMs=8000;untilQpc=8100;pendingBytes=0;length=1'),
            (126, 'A_CLOSE_CONFIRMATION', f'qpc=124;setup={setup};stdout=92;sourceRead=91;bindQpc=119;entryQpc=120;attemptQpc=121;stdoutOk=True;stdoutError=0;writeComplete=True'),
            (127, 'A_READ_RESULT', 'ok=False;bytes=0;error=109;qpc=125;completedMs=25;workerStarted=True;workerJoined=True;failure=none'),
            (128, 'A_READ_PROOF', 'closeConfirmed=True;workerJoined=True;beforeDeadline=True;originalLeaderHandle=80'),
            (129, 'OBSERVATION', 'leaderSignaled=False;exit=259;eof=True'),
        ]
        return [(time, 'P02-A', 'invented-parser-unit', kind, detail)
                for time, kind, detail in details]

    def changed(self, kind, old, new):
        return [(time, case, nonce, key, detail.replace(old, new) if key == kind else detail)
                for time, case, nonce, key, detail in self.proof()]

    def test_complete_bound_proof_parser_unit_and_close_completion_race(self):
        VERIFIER.verify_a(self.proof())
        # The read may return before the helper timestamps CloseHandle's return.
        VERIFIER.verify_a(self.changed('A_CLOSE_CONFIRMATION', 'qpc=124', 'qpc=126'))

    def test_missing_or_duplicate_new_proof_never_passes(self):
        for kind in ('A_DEADLINE', 'HELPER_A_PIPE', 'A_PIPE_READER', 'A_PIPE_ACK', 'HELPER_ENTRY',
                     'A_READ_START', 'A_CLOSE_CONFIRMATION', 'A_READ_RESULT', 'A_READ_PROOF'):
            for duplicate in (False, True):
                rows = self.proof()
                row = next(r for r in rows if r[3] == kind)
                rows = rows + [row] if duplicate else [r for r in rows if r != row]
                with self.subTest(kind=kind, duplicate=duplicate), self.assertRaises(ValueError):
                    VERIFIER.verify_a(rows)

    def test_unbound_unrelated_inherited_or_wrong_source_pipe_refused(self):
        for kind, old, new in (
                ('HELPER_A_PIPE', 'sourceWrite=92', 'sourceWrite=90'),
                ('HELPER_A_PIPE', 'sourceRead=91', 'sourceRead=92'),
                ('HELPER_A_PIPE', 'readNoninherit=True', 'readNoninherit=False'),
                ('HELPER_A_PIPE', 'writeNoninherit=True', 'writeNoninherit=False'),
                ('A_PIPE_READER', 'sourceRead=91', 'sourceRead=93'),
                ('A_PIPE_READER', 'sourceWrite=92', 'sourceWrite=93'),
                ('A_PIPE_READER', 'sourceLeaderHandle=80', 'sourceLeaderHandle=81'),
                ('A_PIPE_READER', 'noninherit=True', 'noninherit=False'),
                ('A_PIPE_READER', 'sameAccess=True', 'sameAccess=False'),
                ('A_PIPE_ACK', 'reader=70', 'reader=71'),
                ('A_PIPE_ACK', 'ownershipEstablished=True', 'ownershipEstablished=False'),
                ('HELPER_ENTRY', 'stdout=92', 'stdout=90'),
                ('HELPER_ENTRY', 'sourceRead=91', 'sourceRead=93'),
                ('HELPER_ENTRY', 'setOk=True', 'setOk=False'),
                ('HELPER_ENTRY', 'getMatch=True', 'getMatch=False'),
                ('HELPER_ENTRY', 'startupStdout=90', 'startupStdout=93'),
                ('HELPER_ENTRY', 'ackQpc=117', 'ackQpc=114'),
                ('HELPER_ENTRY', 'readCloseQpc=118', 'readCloseQpc=120'),
                ('HELPER_ENTRY', 'bindQpc=119', 'bindQpc=121'),
                ('A_READ_START', 'handle=70', 'handle=71')):
            with self.subTest(kind=kind, new=new), self.assertRaises(ValueError):
                VERIFIER.verify_a(self.changed(kind, old, new))
        for kind in ('HELPER_A_PIPE', 'A_PIPE_READER', 'HELPER_ENTRY'):
            for old, new in (('post-managed-start-stdout/v1', 'unbound/v0'), ('pipeType=2', 'pipeType=1')):
                with self.subTest(kind=kind, new=new), self.assertRaises(ValueError):
                    VERIFIER.verify_a(self.changed(kind, old, new))

    def test_read_nonproof_cancellation_late_or_unjoined_refused(self):
        for old, new in (('ok=False', 'ok=True'), ('bytes=0', 'bytes=1'),
                         ('error=109', 'error=995'), ('error=109', 'error=6'),
                         ('qpc=125', 'qpc=8100'), ('completedMs=25', 'completedMs=8000'),
                         ('workerStarted=True', 'workerStarted=False'),
                         ('workerJoined=True', 'workerJoined=False'), ('failure=none', 'failure=Exception')):
            with self.subTest(new=new), self.assertRaises(ValueError):
                VERIFIER.verify_a(self.changed('A_READ_RESULT', old, new))

    def test_close_missing_failed_stale_malformed_or_incomplete_refused(self):
        for old, new in (('stdoutOk=True', 'stdoutOk=False'), ('stdout=92', 'stdout=93'),
                         ('sourceRead=91', 'sourceRead=93'), ('bindQpc=119', 'bindQpc=118'),
                         ('entryQpc=120', 'entryQpc=119'), ('attemptQpc=121', 'attemptQpc=119'),
                         ('attemptQpc=121', 'attemptQpc=126'), ('qpc=124', 'qpc=119'),
                         ('qpc=124', 'qpc=9000'), ('qpc=124', 'qpc=0124'),
                         ('writeComplete=True', 'writeComplete=False'), ('stdoutError=0', 'stdoutError=6'),
                         ('post-managed-start-stdout/v1', 'unbound/v0')):
            with self.subTest(new=new), self.assertRaises(ValueError):
                VERIFIER.verify_a(self.changed('A_CLOSE_CONFIRMATION', old, new))

    def test_deadline_handle_partial_output_or_missing_confirmation_refused(self):
        for kind, old, new in (
                ('A_DEADLINE', 'untilQpc=8100', 'untilQpc=9100'),
                ('A_READ_START', 'leaderHandle=80', 'leaderHandle=81'),
                ('A_READ_START', 'pendingBytes=0', 'pendingBytes=1'),
                ('A_READ_START', 'length=1', 'length=0'),
                ('A_READ_PROOF', 'closeConfirmed=True', 'closeConfirmed=False'),
                ('A_READ_PROOF', 'beforeDeadline=True', 'beforeDeadline=False'),
                ('A_READ_PROOF', 'originalLeaderHandle=80', 'originalLeaderHandle=81'),
                ('OBSERVATION', 'leaderSignaled=False', 'leaderSignaled=True'),
                ('OBSERVATION', 'exit=259', 'exit=0')):
            with self.subTest(new=new), self.assertRaises(ValueError):
                VERIFIER.verify_a(self.changed(kind, old, new))

    def test_cleanup_missing_pending_or_rewritten_result_refused(self):
        rows = self.proof()
        result = next(r[4] for r in rows if r[3] == 'A_READ_RESULT')
        safety = (200, 'suite', 'invented-parser-unit', 'SAFETY_CLEANUP', 'allRetainedHandlesSignaled=true;active=0')
        cleanup = (210, 'suite', 'invented-parser-unit', 'A_READ_CLEANUP', result +
                   ';deathProofQpc=190;eofAfterDeathProof=False;liveEofOutcomeUnchanged=True')
        VERIFIER.verify_read_cleanup(rows + [safety, cleanup])
        for changed in (None, cleanup[4][len(result):],
                        cleanup[4].replace('workerJoined=True', 'workerJoined=False'),
                        cleanup[4].replace('error=109', 'error=995'),
                        cleanup[4].replace('eofAfterDeathProof=False', 'eofAfterDeathProof=True')):
            candidate = rows + [safety] + ([] if changed is None else [(*cleanup[:4], changed)])
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                VERIFIER.verify_read_cleanup(candidate)


class HostedBoundaries(unittest.TestCase):
    def test_refusal_before_source_process_or_scratch(self):
        contexts = ({}, {'GITHUB_ACTIONS': 'true', 'RUNNER_ENVIRONMENT': 'self-hosted'},
                    {'GITHUB_ACTIONS': 'true', 'RUNNER_ENVIRONMENT': 'github-hosted',
                     'RUNNER_OS': 'Windows', 'RUNNER_ARCH': 'ARM64'})
        for env in contexts:
            with self.subTest(env=env), patch.dict(os.environ, env, clear=True), \
                    patch.object(sys, 'argv', ['driver', '--source-commit', 'a' * 40]), \
                    patch.object(DRIVER, 'bind_sources') as sources, \
                    patch.object(DRIVER.subprocess, 'Popen') as process, \
                    patch.object(Path, 'mkdir') as scratch, redirect_stderr(io.StringIO()):
                self.assertEqual(DRIVER.main(), 1)
                sources.assert_not_called()
                process.assert_not_called()
                scratch.assert_not_called()

    def test_observed_architecture_overrides_x64_labels(self):
        class Kernel:
            def __init__(self):
                from unittest.mock import Mock
                self.GetCurrentProcess = Mock(return_value=1)
                def machine(handle, process, native):
                    process._obj.value = 0x8664  # x64 emulated on ARM64
                    native._obj.value = 0xaa64
                    return 1
                self.IsWow64Process2 = Mock(side_effect=machine)
        env = dict(GITHUB_ACTIONS='true', RUNNER_ENVIRONMENT='github-hosted',
                   RUNNER_OS='Windows', RUNNER_ARCH='X64')
        with patch.dict(os.environ, env, clear=True), patch.object(sys, 'platform', 'win32'), \
                patch.object(DRIVER.ctypes, 'WinDLL', return_value=Kernel(), create=True):
            with self.assertRaisesRegex(ValueError, 'not an emulated process'):
                DRIVER.require_context()

    def test_each_bound_input_rejects_byte_conversion(self):
        revision = 'a' * 40
        original = b'first\nsecond\r\n'
        def git(*args):
            if args == ('rev-parse', '--verify', 'HEAD'):
                return revision.encode() + b'\n'
            if args[0] == 'show':
                return original
            return hashlib.sha1(b'blob ' + str(len(original)).encode() + b'\0' + original).hexdigest().encode()
        for changed in DRIVER.SOURCE_PATHS:
            def read(path):
                return original.replace(b'first\n', b'first\r\n') if path == DRIVER.ROOT / changed else original
            with self.subTest(changed=changed), patch.object(DRIVER, 'git_bytes', side_effect=git), \
                    patch.object(Path, 'read_bytes', read):
                with self.assertRaisesRegex(ValueError, 'source differs from Git blob'):
                    DRIVER.bind_sources(revision)

    def test_wrong_head_and_symbolic_revision_refused(self):
        with patch.object(DRIVER, 'git_bytes', return_value=b'b' * 40):
            for revision in ('HEAD', 'a' * 40):
                with self.subTest(revision=revision), self.assertRaises(ValueError):
                    DRIVER.bind_sources(revision)

    def test_real_checkout_preserves_every_bound_input(self):
        sources = {name: (DRIVER.ROOT / name).read_bytes() for name in DRIVER.SOURCE_PATHS}
        workflow = sources['.github/workflows/windows-process-fixtures.yml'].decode()
        checkout_env = dict(re.findall(
            r"^\s+(GIT_CONFIG_(?:COUNT|KEY_0|VALUE_0)): '([^']*)'$", workflow, re.MULTILINE))
        self.assertEqual(checkout_env, {'GIT_CONFIG_COUNT': '1',
                         'GIT_CONFIG_KEY_0': 'core.autocrlf', 'GIT_CONFIG_VALUE_0': 'false'})
        with tempfile.TemporaryDirectory(prefix='chirality-hosted-checkout-') as directory:
            scratch = Path(directory)
            codex_home = scratch / 'codex-home'
            codex_home.mkdir()
            env = dict(os.environ, CODEX_HOME=str(codex_home), GIT_CONFIG_NOSYSTEM='1',
                       GIT_CONFIG_GLOBAL=os.devnull, GIT_ATTR_NOSYSTEM='1', GIT_NO_LAZY_FETCH='1')
            for name in list(env):
                if name in ('GIT_CONFIG_COUNT', 'GIT_CONFIG_PARAMETERS') or re.fullmatch(r'GIT_CONFIG_(KEY|VALUE)_\d+', name):
                    del env[name]
            def git(root, *args, data=None, override=None):
                return subprocess.run(['git', '-C', str(root), *args], input=data,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      env=dict(env, **(override or {})), timeout=15, check=True).stdout
            def checkout(name, override):
                root = scratch / name
                root.mkdir()
                git(root, 'init', '--quiet', '--template=')
                git(root, 'config', 'core.autocrlf', 'true')
                git(root, 'config', 'core.attributesFile', os.devnull)
                for path, content in sources.items():
                    oid = git(root, 'hash-object', '-w', '--stdin', data=content).decode().strip()
                    git(root, 'update-index', '--add', '--cacheinfo', '100644', oid, path)
                git(root, 'checkout-index', '--all', '--force', override=override)
                return {path for path, content in sources.items() if (root / path).read_bytes() != content}
            self.assertEqual(checkout('negative', {}),
                             {'.gitattributes', '.github/workflows/windows-process-fixtures.yml'})
            self.assertEqual(checkout('scoped-override', checkout_env), set())

    def test_empty_marker_only_refusal_and_unknown_trace_never_pass(self):
        verifier = (HERE / 'verify_results.py').read_bytes()
        for raw in (b'', b'1\tsuite\tnonce\tSUITE\tcases_complete\n',
                    b'1\tsuite\tnonce\tREFUSAL\tfailed\n',
                    b'1\tsuite\tnonce\tCLEANUP_UNKNOWN\tunknown\n'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                DRIVER.verify_native_trace(raw, verifier, 'nonce')

    def test_bounded_output_and_timeout_never_success(self):
        for code, seconds in (("import sys; sys.stdout.write('x'*200000)", 5),
                              ('import time; time.sleep(5)', 0.05)):
            with self.subTest(code=code):
                result = DRIVER.capture([sys.executable, '-I', '-c', code], seconds)
                self.assertLessEqual(len(result['stdout']) + len(result['stderr']), DRIVER.LIMIT)
                self.assertIn(result['failure'], ('deadline', 'output_limit'))
                self.assertIn('original_process_exit_observed', result['teardown'])
                with self.assertRaises(ValueError):
                    DRIVER.successful(result)

    def test_failed_original_handle_teardown_is_unknown(self):
        with patch.object(DRIVER.subprocess, 'Popen') as popen:
            popen.return_value.stdout = io.BytesIO()
            popen.return_value.stderr = io.BytesIO()
            popen.return_value.poll.return_value = None
            popen.return_value.wait.side_effect = subprocess.TimeoutExpired('test', 5)
            result = DRIVER.capture(['never executed'], 0)
            self.assertEqual(result['failure'], 'deadline')
            self.assertIn('UNKNOWN', result['teardown'])
            popen.return_value.kill.assert_called_once_with()

    def test_nonzero_exit_never_success(self):
        result = DRIVER.capture([sys.executable, '-I', '-c', 'raise SystemExit(7)'], 5)
        self.assertEqual(result['returncode'], 7)
        with self.assertRaises(ValueError):
            DRIVER.successful(result)

    def test_failed_or_unknown_compiler_never_launches_fixture(self):
        for failure, returncode in ((None, 1), ('deadline', 0), ('output_limit', 0)):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                framework = root / 'Microsoft.NET' / 'Framework64' / 'v4.0.30319'
                framework.mkdir(parents=True)
                for name in ('csc.exe', 'mscorlib.dll', 'System.dll', 'System.Core.dll'):
                    (framework / name).write_bytes(b'host-only test; never executed')
                runner = root / 'runner'
                runner.mkdir()
                def response(code, failed=None, output=b''):
                    return dict(argv=['host-only stub'], returncode=code, failure=failed,
                                teardown='not_needed', elapsed_seconds=0, stdout=output, stderr=b'')
                blobs = {'app/examination/windows_platform/ProcessFixture.cs': b'// never compiled\n'}
                with patch.dict(os.environ, {'SystemRoot': str(root), 'RUNNER_TEMP': str(runner)}), \
                        patch.object(sys, 'argv', ['driver', '--source-commit', 'a' * 40]), \
                        patch.object(DRIVER, 'require_context', return_value={}), \
                        patch.object(DRIVER, 'bind_sources', return_value=(blobs, {})), \
                        patch.object(DRIVER, 'capture', side_effect=[response(0, output=b'Microsoft (R) Visual C# Compiler version 4.8.0\r\n'),
                                     response(returncode, failure)]) as capture, \
                        redirect_stderr(io.StringIO()):
                    self.assertEqual(DRIVER.main(), 1)
                    self.assertEqual(capture.call_count, 2)
                    self.assertEqual(capture.call_args_list[0].args[0][-2:], ['/noconfig', '/help'])
                    import json
                    report = json.loads((runner / 'windows-process-fixture-evidence' / 'result.json').read_bytes())
                    self.assertEqual(report['status'], 'FAILED')
                    self.assertEqual(report['native_execution'], 'NOT_RUN')

    def test_artifacts_keep_raw_crlf(self):
        raw = b'a\r\nb\n'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            result = dict(stdout=raw, stderr=b'', failure=None, returncode=0)
            metadata = DRIVER.persist_command(path, 'trace', result)
            self.assertEqual((path / 'trace.stdout').read_bytes(), raw)
            self.assertEqual(metadata['stdout_sha256'], hashlib.sha256(raw).hexdigest())


if __name__ == '__main__':
    unittest.main()
