"""Offline invented-input computation; separate from App/native examination."""
import json
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

FIXTURES = Path(__file__).resolve().parents[1] / 'examination/standalone/fixtures'

class FixtureToolTest(unittest.TestCase):
    def run_tool(self, variant, source):
        return subprocess.run([sys.executable, str(FIXTURES / variant / 'invented-pipe-inventory/tally.py'), str(source)], capture_output=True, text=True)

    def test_reuse_refinements_and_collision_have_distinct_results(self):
        for variant, source, expected in [('revision-1','initial.csv',11),('revision-1','reuse.csv',11),('revision-2','refinement-2.csv',8),('revision-3','refinement-3.csv',14)]:
            with self.subTest(variant=variant,source=source):
                result=self.run_tool(variant,FIXTURES/'inputs'/source)
                self.assertEqual(result.returncode,0,result.stderr)
                body=json.loads(result.stdout)
                self.assertEqual(body['pieces'],expected)
                self.assertEqual(body['input_sha256'],hashlib.sha256((FIXTURES/'inputs'/source).read_bytes()).hexdigest())
                if variant != 'revision-1': self.assertEqual(sum(body['by_material'].values()),expected)
        collision=json.loads(self.run_tool('user-collision',FIXTURES/'inputs/initial.csv').stdout)
        self.assertEqual(collision['rows'],2)
        self.assertNotIn('pieces',collision)

    def test_duplicate_negative_and_missing_input_refuse_without_output(self):
        for path in [FIXTURES/'inputs/duplicate-negative.csv',FIXTURES/'inputs/does-not-exist.csv']:
            result=self.run_tool('revision-3',path)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(result.stdout,'')
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'bad.csv'
            for text in ['item,material,pieces\nA,steel,-1\n','item,material,pieces\nA,steel,\n','item,pieces\nA,5\n']:
                path.write_text(text)
                result=self.run_tool('revision-1',path)
                self.assertNotEqual(result.returncode,0)
                self.assertEqual(result.stdout,'')

if __name__ == '__main__': unittest.main()
