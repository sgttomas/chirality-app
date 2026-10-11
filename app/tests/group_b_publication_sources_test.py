"""Frozen publication bytes are distinct from today's documentary checkout."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

APP = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('publication_source_tests', APP / 'examination/support_identity/support_identity.py')
subject = importlib.util.module_from_spec(spec)
spec.loader.exec_module(subject)


class PublicationSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.original = b'Frozen published documentary meaning.\n'
        self.digest = subject.sha(self.original)
        (self.root / 'Design.md').write_bytes(b'Todays unrelated implementation notes.\n')

    def test_fixed_object_bytes_remain_exact_and_fetch_is_disabled(self):
        response = subprocess.CompletedProcess([], 0, self.original, b'')
        with patch.object(subject.subprocess, 'run', return_value=response) as run:
            self.assertEqual(subject.publication_source(self.root, 'Design.md', self.digest), self.original)
        args, options = run.call_args
        self.assertEqual(args[0], ['git', 'cat-file', 'blob', subject.DOCUMENTARY_SOURCE_COMMIT + ':projects/chirality-app-v4/Design.md'])
        self.assertEqual(options['env']['GIT_NO_LAZY_FETCH'], '1')
        self.assertEqual(options['env']['GIT_NO_REPLACE_OBJECTS'], '1')

    def test_changed_frozen_meaning_and_missing_objects_refuse(self):
        for code, data in ((0, b'Changed frozen meaning.\n'), (128, b'')):
            with self.subTest(code=code), patch.object(subject.subprocess, 'run', return_value=subprocess.CompletedProcess([], code, data, b'')):
                with self.assertRaisesRegex(ValueError, 'frozen documentary source missing or changed'):
                    subject.publication_source(self.root, 'Design.md', self.digest)

    def test_exact_snapshot_needs_no_git_and_executable_drift_never_falls_back(self):
        (self.root / 'Design.md').write_bytes(self.original)
        (self.root / 'validator.py').write_bytes(b'changed executable')
        with patch.object(subject.subprocess, 'run', side_effect=AssertionError('Git must not be called')):
            self.assertEqual(subject.publication_source(self.root, 'Design.md', self.digest), self.original)
            with self.assertRaisesRegex(ValueError, 'frozen source changed'):
                subject.publication_source(self.root, 'validator.py', self.digest)

    def test_link_and_traversal_do_not_select_another_publication(self):
        (self.root / 'link.md').symlink_to(self.root / 'Design.md')
        with patch.object(subject.subprocess, 'run', side_effect=AssertionError('Git must not be called')):
            for path in ('link.md', '../Design.md'):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    subject.publication_source(self.root, path, self.digest)

    def test_original_declared_validator_objects_remain_whole_and_exact(self):
        original = b'Original frozen validator bytes.\n'
        digest = subject.sha(original)
        (self.root / 'validator.py').write_bytes(b'Unrelated current implementation')
        with patch.object(subject.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, original, b'')):
            self.assertEqual(subject.frozen_publication_source(self.root, 'validator.py', digest), original)
        with patch.object(subject.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, b'wrong object bytes', b'')):
            with self.assertRaisesRegex(ValueError, 'frozen source changed or unavailable'):
                subject.frozen_publication_source(self.root, 'validator.py', digest)
