"""A deliverable's former Design/ resolves to Work/ only when no Design entry exists."""
import importlib.util
import os
from pathlib import Path
import shutil
import tempfile
import unittest

APP = Path(__file__).resolve().parents[1]
READERS = ['examination/sq_receiving/receive.py', 'examination/admission/admission_check.py',
           'examination/standalone/pre_run_inputs.py', 'examination/support_identity/canonical.py',
           'examination/standalone/prepare.py', 'examination/check.py', 'packaging/prepare.py',
           'packaging/static_distribution/check.py']
FORMER = 'execution/PKG-01/DEL-01-01/Design/a.json'


def resolver_source(relative):
    source = (APP / relative).read_text()
    start = source.index('def deliverable_path(')
    return source[start:source.index('\n\n\n', start)]


def resolver(relative):
    namespace = {'os': os, 're': __import__('re')}
    exec(resolver_source(relative), namespace)
    return namespace['deliverable_path']


class DeliverablePath(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        (self.root / 'execution/PKG-01/DEL-01-01/Work').mkdir(parents=True)
        (self.root / 'execution/PKG-01/DEL-01-01/Work/a.json').write_text('{}')
        self.addCleanup(shutil.rmtree, self.root)

    def test_every_reader_carries_the_same_resolver(self):
        bodies = {resolver_source(r) for r in READERS}
        self.assertEqual(len(bodies), 1)

    def test_former_design_reads_work_only_without_any_design_entry(self):
        resolve = resolver(READERS[0])
        self.assertEqual(resolve(self.root, FORMER), 'execution/PKG-01/DEL-01-01/Work/a.json')
        for other in ('execution/PKG-01/DEL-01-01/Work/a.json', 'app/x/Design/a.json',
                      'projects/chirality-app-v4/execution/PKG-01/DEL-01-01/Design/a.json'):
            self.assertEqual(resolve(self.root, other), other)

    def test_existing_or_linked_design_keeps_the_original_path(self):
        resolve = resolver(READERS[0])
        design = self.root / 'execution/PKG-01/DEL-01-01/Design'
        design.symlink_to(self.root / 'missing-directory')
        self.assertEqual(resolve(self.root, FORMER), FORMER)
        design.unlink(); design.mkdir()
        self.assertEqual(resolve(self.root, FORMER), FORMER)

    def test_receiving_reader_still_refuses_a_linked_design(self):
        spec = importlib.util.spec_from_file_location('_receive_for_path_test', APP / READERS[0])
        receive = importlib.util.module_from_spec(spec); spec.loader.exec_module(receive)
        (self.root / 'execution/PKG-01/DEL-01-01/Design').symlink_to(self.root / 'missing-directory')
        with self.assertRaises((ValueError, FileNotFoundError)):
            receive.read_relative(self.root, FORMER)


if __name__ == '__main__':
    unittest.main()
