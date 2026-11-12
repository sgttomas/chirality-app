"""Shipped workflows against the selected Library's whole workflow set, on invented trees only.

Ordinary CI needs no Library checkout."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('library_workflow_set', ROOT / 'app/packaging/library_set.py')
tool = importlib.util.module_from_spec(spec); spec.loader.exec_module(tool)

PACKAGES = {
    'alpha': {'WORKFLOW.md': b'# Invented alpha\n', 'execution.json': b'{}\n'},
    'beta': {'WORKFLOW.md': b'# Invented beta\n', 'resources/method.md': b'invented method\n'},
}


class LibrarySet(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.base = Path(temp.name).resolve()
        self.library = self.base / 'library'
        self.shipped = self.base / 'shipped'
        self.make_library(PACKAGES)
        self.make_shipped(PACKAGES)

    def make_library(self, packages, extra_methods=()):
        workflows = self.library / 'workflows'; workflows.mkdir(parents=True)
        (workflows / 'README.md').write_text('invented')
        methods = [{'kind': 'workflow', 'name': n, 'resources': sorted(files)} for n, files in packages.items()]
        methods += [{'kind': 'skill', 'name': 'alpha', 'resources': ['SKILL.md']}, *extra_methods]
        (workflows / 'index.json').write_text(json.dumps({'schema': tool.INDEX_SCHEMA, 'methods': methods}))
        for name, files in packages.items():
            self.write_files(workflows / name, files)

    def make_shipped(self, packages):
        self.shipped.mkdir()
        listed = []
        for name, files in packages.items():
            self.write_files(self.shipped / name, files)
            listed.append({'name': name, 'revision_method': tool.REVISION_METHOD, 'revision': tool.revision(files),
                           'source_root': 'chirality-root', 'source_path': 'workflows/' + name,
                           'files': [{'path': p, 'bytes': len(r), 'sha256': hashlib.sha256(r).hexdigest()} for p, r in sorted(files.items())]})
        self.write_manifest({'schema_version': 1, 'packages': listed})

    def write_manifest(self, manifest):
        (self.shipped / 'MANIFEST.json').write_text(json.dumps(manifest))

    @staticmethod
    def write_files(folder, files):
        for path, raw in files.items():
            (folder / path).parent.mkdir(parents=True, exist_ok=True)
            (folder / path).write_bytes(raw)

    def run_compare(self):
        return tool.compare(self.library, self.shipped)

    def main(self):
        return tool.main(['compare', '--library-root', str(self.library), '--workflows', str(self.shipped)])

    def test_equal_sets_pass(self):
        result = self.run_compare()
        self.assertTrue(result['equal'])
        self.assertEqual(result['identical'], ['alpha', 'beta'])
        self.assertEqual(result['library']['tree_sha256'], result['shipped']['tree_sha256'])
        self.assertEqual(result['library']['other_methods_not_compared'], 1)   # a skill sharing a workflow's name
        self.assertEqual(self.main(), 0)

    def test_missing_extra_and_differing_packages_are_reported(self):
        self.shipped = self.base / 'shipped-2'
        self.make_shipped({'alpha': {'WORKFLOW.md': b'# Changed\n', 'execution.json': b'{}\n', 'notes.md': b'x'},
                           'gamma': {'WORKFLOW.md': b'# Invented gamma\n'}})
        result = self.run_compare()
        self.assertFalse(result['equal'])
        self.assertEqual(result['missing'], ['beta'])
        self.assertEqual(result['extra'], ['gamma'])
        [alpha] = result['differing']
        self.assertEqual((alpha['changed'], alpha['shipped_only'], alpha['library_only']), (['WORKFLOW.md'], ['notes.md'], []))
        self.assertNotEqual(alpha['library_revision'], alpha['shipped_revision'])
        self.assertEqual(self.main(), 1)

    def test_revision_matches_the_app_method(self):
        # The source manifest's recorded revision is the App's own computation over its files.
        source = ROOT / 'app/src-tauri/resources/production_workflows'
        manifest = json.loads((source / 'MANIFEST.json').read_bytes())
        fd = tool.open_dir(source); self.addCleanup(os.close, fd)
        for package in manifest['packages']:
            self.assertEqual(tool.revision(tool.read_package(fd, package['name'], package['name'])), package['revision'])

    def test_index_resources_differing_from_folder_are_reported(self):
        (self.library / 'workflows/beta/unlisted.md').write_text('x')
        (self.shipped / 'beta/unlisted.md').write_text('x')
        manifest = json.loads((self.shipped / 'MANIFEST.json').read_bytes())
        beta = manifest['packages'][1]; files = {**PACKAGES['beta'], 'unlisted.md': b'x'}
        beta['files'].append({'path': 'unlisted.md', 'bytes': 1, 'sha256': hashlib.sha256(b'x').hexdigest()})
        beta['revision'] = tool.revision(files)
        self.write_manifest(manifest)
        result = self.run_compare()
        self.assertTrue(result['equal'])   # whole folders compared
        self.assertEqual(result['library']['index_resources_differ_from_folder'], {'beta': {'listed_only': [], 'folder_only': ['unlisted.md']}})

    # Refusals.
    def assertRefused(self):
        with self.assertRaises(tool.Refused):
            self.run_compare()
        self.assertEqual(self.main(), 2)

    def test_symbolic_links_are_refused(self):
        os.symlink(self.library / 'workflows/alpha/WORKFLOW.md', self.library / 'workflows/beta/link.md')
        self.assertRefused()

    def test_symbolic_link_in_shipped_tree_or_root_is_refused(self):
        os.symlink(self.base, self.shipped / 'alpha/escape')
        self.assertRefused()
        os.unlink(self.shipped / 'alpha/escape')
        os.symlink(self.shipped, self.base / 'alias'); self.shipped = self.base / 'alias'
        self.assertRefused()

    # Review probe library-linked-workflows: a linked workflows/ beneath a clean root once compared equal.
    def test_linked_library_workflows_directory_is_refused(self):
        os.replace(self.library / 'workflows', self.base / 'elsewhere')
        os.symlink(self.base / 'elsewhere', self.library / 'workflows')
        self.assertRefused()

    def test_linked_directory_inside_a_package_is_refused(self):
        (self.base / 'outside').mkdir(); (self.base / 'outside/x.md').write_text('x')
        os.symlink(self.base / 'outside', self.shipped / 'beta/resources/linked')
        self.assertRefused()

    # Review probe library-unreadable-package: an untraversable Library package against an empty
    # shipped package with an accurate empty manifest once compared equal.
    @unittest.skipIf(os.geteuid() == 0, 'root reads everything')
    def test_untraversable_library_package_is_refused_not_skipped(self):
        self.shipped = self.base / 'shipped-empty'
        self.shipped.mkdir(); (self.shipped / 'alpha').mkdir(); (self.shipped / 'beta').mkdir()
        self.write_manifest({'schema_version': 1, 'packages': [
            {'name': n, 'source_path': 'workflows/' + n, 'files': []} for n in ('alpha', 'beta')]})
        for name in ('alpha', 'beta'):
            folder = self.library / 'workflows' / name
            folder.chmod(0o000); self.addCleanup(folder.chmod, 0o755)
        self.assertRefused()

    @unittest.skipIf(os.geteuid() == 0, 'root reads everything')
    def test_unreadable_entry_on_either_side_is_refused(self):
        for target in (self.library / 'workflows/beta/resources', self.shipped / 'beta/resources',
                       self.library / 'workflows/alpha/WORKFLOW.md', self.shipped / 'alpha/WORKFLOW.md',
                       self.library / 'workflows/index.json', self.shipped / 'MANIFEST.json'):
            original = target.stat().st_mode
            target.chmod(0o000)
            try:
                with self.subTest(target=str(target.relative_to(self.base))):
                    self.assertRefused()
            finally:
                target.chmod(original)
        self.assertTrue(self.run_compare()['equal'])

    def test_index_and_folders_disagreeing_is_refused(self):
        (self.library / 'workflows/unindexed').mkdir()
        self.assertRefused()

    def test_unknown_index_schema_is_refused(self):
        index = self.library / 'workflows/index.json'
        value = json.loads(index.read_bytes()); value['schema'] = 'chirality-method-index/v9'
        index.write_text(json.dumps(value))
        self.assertRefused()

    def test_duplicate_names_are_refused(self):
        index = self.library / 'workflows/index.json'
        value = json.loads(index.read_bytes()); value['methods'].append(dict(value['methods'][0]))
        index.write_text(json.dumps(value))
        self.assertRefused()

    def test_duplicate_manifest_package_is_refused(self):
        manifest = json.loads((self.shipped / 'MANIFEST.json').read_bytes())
        manifest['packages'].append(manifest['packages'][0])
        self.write_manifest(manifest)
        self.assertRefused()

    def test_source_path_outside_workflows_is_refused(self):
        for source in ('skills/alpha', 'workflows/../alpha', 'workflows/beta', '/workflows/alpha'):
            manifest = json.loads((self.shipped / 'MANIFEST.json').read_bytes())
            manifest['packages'][0]['source_path'] = source
            self.write_manifest(manifest)
            with self.subTest(source=source):
                self.assertRefused()

    def test_manifest_and_tree_disagreeing_is_refused(self):
        (self.shipped / 'alpha/WORKFLOW.md').write_bytes(b'# Edited after the manifest\n')
        self.assertRefused()

    def test_unlisted_shipped_folder_is_refused(self):
        (self.shipped / 'stray').mkdir()
        self.assertRefused()


if __name__ == '__main__':
    unittest.main()
