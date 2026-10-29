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
