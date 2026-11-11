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
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('examination_repin', ROOT / 'app/examination/repin.py')
repin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(repin)


def load(name, relative):
    module_spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module

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
        paths |= {reader for reader, _ in repin.FROZEN.values()}
        for profile in repin.PROFILES:
            paths |= {path for _, _, path in repin.slots(profile, read_json(ROOT, profile))}
        for path in paths:
            relative = path
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

    def write_lock(self, value):
        (self.root / repin.LOCK).write_bytes(repin.encode(value))

    def assert_check_fails(self, expected):
        before = self.snapshot()
        code, output = run(self.root, '--check')
        self.assertEqual(code, 1, output)
        self.assertIn(expected, output)
        self.assertEqual(self.snapshot(), before)

    def forge_receipt(self, root, receipt):
        target = root / receipt
        value = json.loads(target.read_bytes())
        value['adoption'] = 'FORGED-HISTORICAL-ADOPTION'
        target.write_bytes(repin.encode(value))
        return repin.sha(target.read_bytes())

    def test_forged_receipt_with_matching_lock_digest_is_refused(self):
        for receipt in repin.FROZEN:
            with self.subTest(receipt=receipt):
                self.setUp()
                digest = self.forge_receipt(self.root, receipt)
                lock = read_json(self.root, repin.LOCK)
                lock['frozen'][receipt] = digest
                self.write_lock(lock)
                self.assert_check_fails('frozen entry differs from its anchor')
                self.assertEqual(run(self.root)[0], 1)

    def test_readers_refuse_a_forged_receipt_even_with_a_matching_lock(self):
        readers = [('distribution_receiving/receive.py', 'Receiver', 'pins.build-selection-lt09-v1.json'),
                   ('distribution_receiving/terminal.py', 'TerminalReceiver', 'pins.build-selection-terminal-v1.json')]
        for relative, cls, name in readers:
            with self.subTest(reader=relative):
                module = load('repin_forgery_' + cls, 'app/examination/' + relative)
                here = self.root.resolve() / 'forged'  # the readers refuse linked components
                here.mkdir(exist_ok=True)
                source = ROOT / 'app/examination/distribution_receiving'
                for item in source.glob('pins.*.json'):
                    shutil.copyfile(item, here / item.name)
                digest = self.forge_receipt(here, name)
                lock = read_json(ROOT, repin.LOCK)
                lock['frozen']['app/examination/distribution_receiving/' + name] = digest
                forged_lock = here / 'pins.lock.json'
                forged_lock.write_bytes(repin.encode(lock))
                with patch.object(module, 'HERE', here), patch.object(module, 'PIN_LOCK_PATH', forged_lock):
                    with self.assertRaisesRegex(ValueError, 'anchor and pin lock disagree'):
                        getattr(module, cls)('build-selection')
                # Without the lock edit the receipt digest itself is refused.
                with patch.object(module, 'HERE', here):
                    with self.assertRaisesRegex(ValueError, 'pins changed'):
                        getattr(module, cls)('build-selection')

    def test_catalog_entry_deletion_is_detected(self):
        lock = read_json(self.root, repin.LOCK)
        removed = repin.CURRENT[0]
        del lock['current'][removed]
        self.write_lock(lock)
        self.assert_check_fails('current entry missing: ' + removed)
        lock = read_json(ROOT, repin.LOCK)
        removed = next(iter(repin.FROZEN))
        del lock['frozen'][removed]
        self.write_lock(lock)
        self.assert_check_fails('frozen entry missing: ' + removed)

    def test_empty_sections_are_detected(self):
        lock = read_json(self.root, repin.LOCK)
        lock['current'], lock['frozen'] = {}, {}
        self.write_lock(lock)
        self.assert_check_fails('current entry missing')
        self.assert_check_fails('frozen entry missing')
        self.assertEqual(run(self.root)[0], 1, 'frozen entries are never regenerated')

    def test_malformed_digest_is_detected(self):
        lock = read_json(self.root, repin.LOCK)
        path = repin.CURRENT[-1]
        lock['current'][path] = lock['current'][path].upper()
        self.write_lock(lock)
        self.assert_check_fails('malformed current digest: ' + path)

    def test_reclassified_historical_entry_is_detected(self):
        lock = read_json(self.root, repin.LOCK)
        path = next(iter(repin.FROZEN))
        lock['current'][path] = lock['frozen'].pop(path)
        self.write_lock(lock)
        self.assert_check_fails('historical receipt reclassified as current')
        self.assert_check_fails('frozen entry missing: ' + path)

    def test_unreadable_lock_fails_through_the_reader_report(self):
        adapter = load('repin_lock_adapter', 'app/examination/package_receiving/adapter.py')
        for content in (None, b'{not json', b'[]'):
            with self.subTest(content=content):
                lock = self.root / 'unreadable-lock.json'
                if content is None:
                    lock.unlink(missing_ok=True)
                else:
                    lock.write_bytes(content)
                with patch.object(adapter, 'PIN_LOCK_PATH', lock):
                    self.assertIsNone(adapter.locked_digest('current', repin.CURRENT[0]))
        out = io.StringIO()
        with patch.object(adapter, 'PINS_SHA256', None), contextlib.redirect_stdout(out):
            code = adapter.main(['bind', '--request', 'r.json', '--evidence-root', '.',
                                 '--configuration', 'c.json', '--configuration-sha256', '0' * 64])
        self.assertEqual(code, 2)
        report = json.loads(out.getvalue())
        self.assertIn('source profile changed', report['input_error'])
        self.assertFalse(report['file_checks_passed'])

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

    def test_the_lock_cannot_pin_itself(self):
        value = read_json(self.root, repin.LOCK)
        value['current'][repin.LOCK] = '0' * 64
        (self.root / repin.LOCK).write_bytes(repin.encode(value))
        self.assert_check_fails('unexpected current entry: ' + repin.LOCK)
        profile = 'app/examination/distribution_receiving/inputs.json'
        inputs = read_json(self.root, profile)
        inputs[repin.LOCK] = '0' * 64
        (self.root / profile).write_bytes(repin.encode(inputs))
        code, output = run(self.root, '--check')
        self.assertEqual(code, 2)
        self.assertIn('cannot itself be pinned', output)


if __name__ == '__main__':
    unittest.main()
