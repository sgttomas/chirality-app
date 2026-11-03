"""Bundled IBM Plex notice index; local bytes only, no network, build or font execution."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('font_notice_check', ROOT / 'app/packaging/font_notice/check.py')
f = importlib.util.module_from_spec(spec); spec.loader.exec_module(f)
INDEX = 'app/packaging/font_notice/index.json'


class FontNotice(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        shutil.copytree(ROOT / 'app/src/fonts', self.root / 'app/src/fonts')
        (self.root / 'app/packaging/font_notice').mkdir(parents=True)
        for path in (INDEX, 'app/src/workspace.css', 'app/index.html'):
            shutil.copyfile(ROOT / path, self.root / path)

    def edit(self, path, change):
        target = self.root / path
        target.write_text(change(target.read_text()))

    def index(self, change):
        value = json.loads((self.root / INDEX).read_text()); change(value)
        (self.root / INDEX).write_text(json.dumps(value))

    def test_saved_index_matches_shipped_fonts_and_their_name_tables(self):
        index = f.check(ROOT)
        self.assertEqual(len(index['fonts']), 10)
        self.assertEqual(f.check_name_tables(index), 10)
        self.assertEqual({x['name_table']['license_url'] for x in index['fonts']}, {'http://scripts.sil.org/OFL'})
        self.assertEqual(len(index['copyright_notices']), 3)
        self.assertFalse(index['source']['declared_upstream_verified'])

    def test_changed_extra_or_missing_font_bytes_refuse(self):
        font = self.root / 'app/src/fonts/ibm-plex-mono-latin-400-normal.woff2'
        original = font.read_bytes()
        font.write_bytes(original + b'\0')
        with self.assertRaisesRegex(ValueError, 'bytes differ'): f.check(self.root)
        font.write_bytes(original)
        (self.root / 'app/src/fonts/extra.woff2').write_bytes(b'INVENTED')
        with self.assertRaisesRegex(ValueError, 'unindexed or missing'): f.check(self.root)
        (self.root / 'app/src/fonts/extra.woff2').unlink(); font.unlink()
        with self.assertRaisesRegex(ValueError, 'missing or linked'): f.check(self.root)

    def test_linked_font_input_refuses(self):
        font = self.root / 'app/src/fonts/ibm-plex-mono-latin-400-normal.woff2'
        moved = self.root / 'outside.woff2'; font.rename(moved); font.symlink_to(moved)
        with self.assertRaisesRegex(ValueError, 'missing or linked'): f.check(self.root)

    def test_frontend_reference_drift_refuses(self):
        self.edit('app/src/workspace.css', lambda s: s.replace('./fonts/ibm-plex-mono-latin-500-normal.woff2', './fonts/other.woff2'))
        with self.assertRaisesRegex(ValueError, '@font-face sources differ'): f.check(self.root)

    def test_remote_font_and_missing_license_link_refuse(self):
        self.edit('app/src/workspace.css', lambda s: s + '\n@font-face { font-family: X; src: url("./fonts/ibm-plex-mono-latin-400-normal.woff2"); }\n.x{background:url(https://example.invalid/a.woff2)}\n')
        with self.assertRaises(ValueError): f.check(self.root)
        self.setUp()
        self.edit('app/index.html', lambda s: s.replace('rel="license"', 'rel="stylesheet"'))
        with self.assertRaisesRegex(ValueError, 'no longer links'): f.check(self.root)

    def test_index_shape_provenance_and_notice_list_refuse(self):
        for change, message in ((lambda v: v.update(extra=True), 'shape'),
                                (lambda v: v['source'].update(declared_upstream_verified=True), 'provenance'),
                                (lambda v: v['copyright_notices'].pop(), 'notice list'),
                                (lambda v: v['fonts'].reverse(), 'unordered'),
                                (lambda v: v['license'].update(header_copyright='INVENTED'), 'header')):
            with self.subTest(message=message):
                self.setUp(); self.index(change)
                with self.assertRaisesRegex(ValueError, message): f.check(self.root)

    def test_name_table_declaration_change_refuses(self):
        self.index(lambda v: v['fonts'][0]['name_table'].update(copyright='INVENTED notice'))
        index = json.loads((self.root / INDEX).read_text())
        with self.assertRaisesRegex(ValueError, 'name-table declaration differs'): f.check_name_tables(index, self.root)

    def test_truncated_or_non_woff2_refuses(self):
        with self.assertRaises(ValueError): f.name_table(b'wOF2' + b'\0' * 10)
        with self.assertRaises(ValueError): f.name_table(b'\0' * 64)


if __name__ == '__main__':
    unittest.main()
