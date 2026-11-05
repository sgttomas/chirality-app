"""Re-derive and check the generated examination pins on a staged copy; offline."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('examination_repin', ROOT / 'app/examination/repin.py')
repin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(repin)

SUPPORT = 'app/examination/support_identity/support_identity.py'
CANONICAL_PINS = 'app/examination/support_identity/canonical-pins.terms-v1.json'
SQ_PACKAGES = 'app/examination/sq_receiving/pins.packages-v1.json'
PACKAGE_PROFILE = 'app/examination/package_receiving/sources.package-v1.json'


def run(root, *argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = repin.main(list(argv), root=root)
    return code, out.getvalue() + err.getvalue()


def read_json(root, relative):
    return json.loads((root / relative).read_bytes())


class RepinTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        lock = read_json(ROOT, repin.LOCK)
        paths = set(repin.PROFILES) | {repin.LOCK} | set(lock['current']) | set(lock['frozen'])
        for profile in repin.PROFILES:
            paths |= {path for _, _, path in repin.slots(profile, read_json(ROOT, profile))}
        for path in paths:
            relative = repin.resolve(ROOT, path)
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)

    def snapshot(self):
        return {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def test_repository_pins_agree_with_current_sources(self):
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'app/examination/repin.py'), '--check'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(run(self.root, '--check')[0], 0)

    def test_modified_pinned_source_is_detected_and_repinned_through_the_chain(self):
        source = self.root / SUPPORT
        source.write_bytes(source.read_bytes() + b'\n# reviewed change\n')
        before = self.snapshot()
        code, output = run(self.root, '--check')
        self.assertEqual(code, 1)
        self.assertIn(CANONICAL_PINS + ': ' + SUPPORT, output)
        self.assertIn(repin.LOCK + ': ' + CANONICAL_PINS, output)
        self.assertEqual(self.snapshot(), before, 'check mode must not write')

        code, output = run(self.root)
        self.assertEqual(code, 0, output)
        self.assertEqual(run(self.root, '--check')[0], 0)
        digest = repin.sha(source.read_bytes())
        self.assertEqual(read_json(self.root, CANONICAL_PINS)['sources'][SUPPORT], digest)
        packages = read_json(self.root, SQ_PACKAGES)
        self.assertEqual(packages['sources'][SUPPORT], digest)
        # Pins of pins follow without hand edits: profile -> profile -> lock.
        canonical_pins = repin.sha((self.root / CANONICAL_PINS).read_bytes())
        self.assertEqual(packages['sources'][CANONICAL_PINS], canonical_pins)
        self.assertEqual(read_json(self.root, PACKAGE_PROFILE)['sources'][CANONICAL_PINS], canonical_pins)
        profile = repin.sha((self.root / PACKAGE_PROFILE).read_bytes())
        self.assertEqual(packages['package_source_profile']['sha256'], profile)
        lock = read_json(self.root, repin.LOCK)
        self.assertEqual(lock['current'][CANONICAL_PINS], canonical_pins)
        self.assertEqual(lock['current'][SQ_PACKAGES], repin.sha((self.root / SQ_PACKAGES).read_bytes()))

    def test_hand_edited_digest_is_detected(self):
        value = read_json(self.root, PACKAGE_PROFILE)
        path = next(iter(value['sources']))
        value['sources'][path] = '0' * 64
        (self.root / PACKAGE_PROFILE).write_bytes(repin.encode(value))
        code, output = run(self.root, '--check')
        self.assertEqual(code, 1)
        self.assertIn(PACKAGE_PROFILE + ': ' + path, output)

    def test_frozen_evidence_change_fails_and_is_never_repinned(self):
        frozen = next(iter(read_json(self.root, repin.LOCK)['frozen']))
        target = self.root / frozen
        target.write_bytes(target.read_bytes() + b'\n')
        before = self.snapshot()
        for argv in (['--check'], []):
            code, output = run(self.root, *argv)
            self.assertEqual(code, 1)
            self.assertIn('frozen evidence changed: ' + frozen, output)
        self.assertEqual(self.snapshot(), before)

    def test_missing_pinned_source_writes_nothing(self):
        (self.root / SUPPORT).unlink()
        before = self.snapshot()
        code, output = run(self.root)
        self.assertEqual(code, 1)
        self.assertIn('pinned source missing: ' + SUPPORT, output)
        self.assertEqual(self.snapshot(), before)

    def test_historical_markdown_selections_are_left_as_recorded(self):
        pins = read_json(self.root, SQ_PACKAGES)
        documentary = next(p for p in pins['sources'] if p.endswith('.md'))
        target = self.root / repin.resolve(self.root, documentary)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b'changed current text\n')
        self.assertEqual(run(self.root)[0], 0)
        self.assertEqual(read_json(self.root, SQ_PACKAGES)['sources'][documentary], pins['sources'][documentary])

    def test_the_lock_cannot_pin_itself(self):
        value = read_json(self.root, repin.LOCK)
        value['current'][repin.LOCK] = '0' * 64
        (self.root / repin.LOCK).write_bytes(repin.encode(value))
        code, output = run(self.root, '--check')
        self.assertEqual(code, 2)
        self.assertIn('cannot itself be pinned', output)


if __name__ == '__main__':
    unittest.main()
