"""Host-only regressions for source admission and byte-preserving transport."""
import base64
from contextlib import redirect_stderr
import io
import gzip
import hashlib
import importlib.util
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('fixture_driver', HERE / 'run_fixture.py')
DRIVER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DRIVER)


class Admission(unittest.TestCase):
    def test_private_binding_excludes_legacy_and_over_budget_guests(self):
        binding = {
            'alias': DRIVER.TARGET_ALIAS, 'created_for_builds': True, 'ram_mib': 16384,
            'vm_id': '00000000-0000-0000-0000-000000000001',
            'protected_legacy_vm_id': '00000000-0000-0000-0000-000000000002',
        }
        self.assertEqual(DRIVER.build_guest_id(binding), binding['vm_id'])
        for changed in ({'vm_id': binding['protected_legacy_vm_id']}, {'ram_mib': 16385},
                        {'created_for_builds': False}, {'alias': 'legacy'}, {'vm_id': None}):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                DRIVER.build_guest_id(dict(binding, **changed))

    def test_guest_hold_precedes_binding_contact_and_scratch(self):
        for mode in ('--inspect', '--bootstrap-check', '--run'):
            with self.subTest(mode=mode), \
                    patch('sys.argv', ['driver', mode, '--source-commit', 'a' * 40]), \
                    patch.object(DRIVER, 'bind_sources') as bind, \
                    patch.object(DRIVER.subprocess, 'Popen') as popen, \
                    patch.object(DRIVER.tempfile, 'mkdtemp') as scratch:
                with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    DRIVER.main()
                bind.assert_not_called()
                popen.assert_not_called()
                scratch.assert_not_called()

    def test_run_and_ambiguous_modes_never_contact_guest_or_make_scratch(self):
        for args in ([], ['--run'], ['--run', '--inspect'], ['--bootstrap-check'],
                     ['--inspect', '--source-commit', 'HEAD']):
            with self.subTest(args=args), patch('sys.argv', ['driver'] + args), \
                    patch.object(DRIVER.subprocess, 'Popen') as popen, \
                    patch.object(DRIVER.tempfile, 'mkdtemp') as scratch:
                with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    DRIVER.main()
                popen.assert_not_called()
                scratch.assert_not_called()

    def test_each_executable_source_is_bound_before_contact(self):
        revision = 'a' * 40
        for changed in DRIVER.SOURCE_FILES:
            def saved(argv, **kwargs):
                if argv[1] == 'rev-parse':
                    return revision if '--verify' in argv else str(HERE.parents[2])
                name = argv[-1].split('/')[-1]
                content = (HERE / name).read_bytes()
                return content + b'changed' if name == changed else content
            with self.subTest(changed=changed), \
                    patch.object(DRIVER.subprocess, 'check_output', side_effect=saved), \
                    patch.object(DRIVER.subprocess, 'run'), \
                    patch.object(DRIVER.subprocess, 'Popen') as popen:
                with self.assertRaisesRegex(ValueError, 'source differs.*' + re.escape(changed)):
                    DRIVER.bind_sources(revision)
                popen.assert_not_called()

    def test_transport_matches_exact_committed_family_bytes(self):
        verified_source = (HERE / 'Controller.ps1').read_bytes()
        # No later pathname read may replace bytes already verified from Git.
        with patch.object(Path, 'read_bytes', side_effect=AssertionError('late source reread')):
            command = DRIVER.bootstrap_command(verified_source)
        payload = re.search(r"FromBase64String\('([^']+)'\)", command)[1]
        source = gzip.decompress(base64.b64decode(payload, validate=True))
        self.assertEqual(source, (HERE / 'Controller.ps1').read_bytes())
        self.assertIn(hashlib.sha256(source).hexdigest(), command)
        self.assertIn('$count -ne ' + str(len(source)), command)
        self.assertLess(len(base64.b64encode(command.encode('utf-16le'))), 30000)
        self.assertNotIn('Invoke-FixtureContainedProcess;', command)
        self.assertNotIn(' -ExecutionPolicy ', command)

    def test_response_overflow_and_timeout_are_unknown(self):
        commands = [([sys.executable, '-c', "print('x' * 100000)"], 5),
                    ([sys.executable, '-c', 'import time; time.sleep(2)'], 0.05)]
        for command, deadline in commands:
            with self.subTest(command=command):
                result = DRIVER.capture_response(command, response_seconds=deadline)
                self.assertIsNone(result['returncode'])
                self.assertIn('guest command completion UNKNOWN', result['limitation'])
                self.assertLessEqual(len(result['stdout']) + len(result['stderr']), 32768)

    def test_failed_local_teardown_keeps_unknown_report(self):
        with patch.object(DRIVER.subprocess, 'Popen') as popen, \
                patch.object(DRIVER.selectors, 'DefaultSelector', side_effect=OSError('test selector failure')):
            popen.return_value.kill.side_effect = OSError('test kill failure')
            popen.return_value.wait.side_effect = DRIVER.subprocess.TimeoutExpired('test-client', 0)
            result = DRIVER.capture_response(['never-executed'])
            self.assertIsNone(result['returncode'])
            self.assertIn('guest command completion UNKNOWN', result['limitation'])
            self.assertIn('local exit not observed', result['limitation'])

    def test_failed_stream_or_selector_close_keeps_unknown_report(self):
        with patch.object(DRIVER.subprocess, 'Popen') as popen, \
                patch.object(DRIVER.selectors, 'DefaultSelector') as selector:
            selector.return_value.get_map.return_value = {}
            selector.return_value.close.side_effect = OSError('test selector close failure')
            popen.return_value.wait.return_value = 0
            popen.return_value.stdout.close.side_effect = OSError('test stdout close failure')
            result = DRIVER.capture_response(['never-executed'])
            self.assertIsNone(result['returncode'])
            self.assertIn('selector close failed', result['limitation'])
            self.assertIn('stdout close failed', result['limitation'])
            self.assertIn('guest command completion UNKNOWN', result['limitation'])
            popen.return_value.stderr.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
