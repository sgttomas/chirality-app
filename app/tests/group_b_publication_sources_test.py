"""Frozen publication bytes are distinct from today's documentary checkout."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

APP = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('publication_source_tests', APP / 'examination/support_identity/support_identity.py')
subject = importlib.util.module_from_spec(spec)
spec.loader.exec_module(subject)


class PublicationSourceTests(unittest.TestCase):
    def test_shared_ci_setup_verifies_original_objects_with_active_reader_pins(self):
        result = subprocess.run(
            [sys.executable, '-B', str(APP / 'examination/support_identity/provision_ci_objects.py')],
            cwd=APP, capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        self.assertEqual(report['verified_objects'], 30)
        self.assertEqual(report['source_bytes'], 2128671)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'current'
        self.root.mkdir()
        self.library = Path(self.temp.name) / 'library'
        (self.library / 'frozen').mkdir(parents=True)
        here = patch.object(subject, 'HERE', self.library)
        here.start(); self.addCleanup(here.stop)
        self.original = b'Frozen published documentary meaning.\n'
        self.digest = subject.sha(self.original)
        (self.root / 'Design.md').write_bytes(b'Todays unrelated implementation notes.\n')

    def test_fixed_snapshot_bytes_remain_exact_without_git(self):
        (self.library / 'frozen/Design.md').write_bytes(self.original)
        with patch.object(subject.subprocess, 'run', side_effect=AssertionError('No Git or network')):
            self.assertEqual(subject.publication_source(self.root, 'Design.md', self.digest), self.original)

    def test_changed_frozen_meaning_and_missing_files_refuse(self):
        path = self.library / 'frozen/Design.md'
        path.write_bytes(b'Changed frozen meaning.\n')
        with self.assertRaisesRegex(ValueError, 'frozen source changed'):
            subject.publication_source(self.root, 'Design.md', self.digest)
        path.unlink()
        with self.assertRaisesRegex(ValueError, 'frozen source missing'):
            subject.publication_source(self.root, 'Design.md', self.digest)

    def test_link_in_frozen_snapshot_refuses(self):
        (self.library / 'frozen/Design.md').symlink_to(self.root / 'Design.md')
        with self.assertRaisesRegex(ValueError, 'symbolic link refused'):
            subject.publication_source(self.root, 'Design.md', self.digest)

    def test_link_at_frozen_root_refuses(self):
        frozen = self.library / 'frozen'
        frozen.rmdir()
        frozen.symlink_to(self.root, target_is_directory=True)
        (self.root / 'Design.md').unlink()
        (self.root / 'other.md').write_bytes(self.original)
        with self.assertRaisesRegex(ValueError, 'symbolic link refused'):
            subject.frozen_snapshot_source('other.md', self.digest)

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
        frozen = self.library / 'frozen/validator.py'
        frozen.write_bytes(original)
        with patch.object(subject.subprocess, 'run', side_effect=AssertionError('No Git or network')):
            self.assertEqual(subject.frozen_publication_source(self.root, 'validator.py', digest), original)
        frozen.write_bytes(b'wrong object bytes')
        with self.assertRaisesRegex(ValueError, 'frozen source changed'):
            subject.frozen_publication_source(self.root, 'validator.py', digest)
