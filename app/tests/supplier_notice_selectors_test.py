"""The received Codex 0.160.0 rg selector files are read, hashed and refused when missing or altered.

Reads committed supplier text only; nothing from it is executed.
"""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
NOTICES = ROOT / 'app/packaging/supplier_notices'


def load(name):
    spec = importlib.util.spec_from_file_location('selector_' + name, NOTICES / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


associate = load('associate_0167')
ripgrep = load('ripgrep_0167')
KEPT = NOTICES / 'codex-0.160.0/scripts/codex_package'


class Selectors(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.copy = Path(temp.name).resolve()
        for name in associate.SELECTOR_FILES:
            (self.copy / name).write_bytes((KEPT / name).read_bytes())

    def test_kept_selector_bytes_carry_the_recorded_identity(self):
        for name, (size, sha256, git_blob) in associate.SELECTOR_FILES.items():
            with self.subTest(name=name):
                raw, digest, length = associate.received_selector(name)
                self.assertEqual((length, digest, associate.blob(raw)), (size, sha256, git_blob))
                self.assertEqual(raw, (KEPT / name).read_bytes())
        self.assertEqual(associate.SELECTOR_FILES['rg'][1:], (ripgrep.SELECTOR_SHA256, ripgrep.SELECTOR_BLOB))

    def test_platform_row_is_read_from_the_selector(self):
        digest, platform = ripgrep.selector_platform()
        self.assertEqual(digest, ripgrep.SELECTOR_SHA256)
        self.assertEqual(platform, {
            'size': 1764284, 'hash': 'sha256',
            'digest': '3750b2e93f37e0c692657da574d7019a101c0084da05a790c83fd335bad973e4',
            'format': 'tar.gz', 'path': 'ripgrep-15.2.0-aarch64-apple-darwin/rg',
            'providers': [{'url': ripgrep.ARCHIVE_URL}]})

    def test_missing_selector_is_refused(self):
        for name in associate.SELECTOR_FILES:
            (self.copy / name).unlink()
            with self.subTest(name=name), self.assertRaises((OSError, ValueError)):
                associate.received_selector(name, self.copy)
        with self.assertRaises((OSError, ValueError)):
            ripgrep.selector_platform(self.copy / 'rg')

    def test_altered_selector_is_refused(self):
        for name in associate.SELECTOR_FILES:
            path = self.copy / name
            path.write_bytes(path.read_bytes().replace(b'15.2.0', b'15.2.1', 1) if name == 'rg' else path.read_bytes() + b'\n')
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'selector changed'):
                associate.received_selector(name, self.copy)
        with self.assertRaisesRegex(ValueError, 'selector changed'):
            ripgrep.selector_platform(self.copy / 'rg')


if __name__ == '__main__':
    unittest.main()
