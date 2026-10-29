"""Host-only regressions for source admission and byte-preserving transport."""
import base64
from contextlib import redirect_stderr
import io
import gzip
import hashlib
import importlib.util
from pathlib import Path
import re
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('fixture_driver', HERE / 'run_fixture.py')
DRIVER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DRIVER)


class Admission(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
