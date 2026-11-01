"""Invented bytes test the bounded observation, never supplier execution."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('supplier_notice_observer',ROOT/'app/packaging/supplier_notices/observe.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class Observations(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name).resolve()
  self.name='bin/invented';path=self.root/self.name;path.parent.mkdir();self.data=b'INVENTED\0version clue\0';path.write_bytes(self.data)
  self.sha=module.reader.sha(self.data)
  self.manifest=self.root/'codex-resources/voice/manifest.json';self.manifest.parent.mkdir(parents=True)
  self.manifest.write_text(json.dumps({'buildCommit':'a'*40,'sha256':{self.name:self.sha}}))
 def run_observer(self):
  with patch.object(module,'SUBJECTS',{self.name:self.sha}),patch.object(module,'CLUES',{self.name:[b'version clue']}):
   return module.inspect(self.root)
 def test_exact_offsets_and_declared_manifest_binding(self):
  result=self.run_observer()['components'][0]
  self.assertEqual(result['embedded_clues'][0]['offsets'],[9])
  self.assertEqual(result['manifest_declared_build_commit'],'a'*40)
 def test_unlisted_binary_gets_no_commit_association(self):
  self.manifest.write_text(json.dumps({'buildCommit':'a'*40,'sha256':{}}))
  self.assertIsNone(self.run_observer()['components'][0]['manifest_declared_build_commit'])
 def test_wrong_subject_bytes_refuse(self):
  (self.root/self.name).write_bytes(b'changed')
  with self.assertRaisesRegex(ValueError,'subject digest'):self.run_observer()
 def test_link_refuses(self):
  (self.root/'real').write_bytes(self.data);(self.root/self.name).unlink();(self.root/self.name).symlink_to(self.root/'real')
  with self.assertRaises(OSError):self.run_observer()
 def test_saved_observation_is_only_matching_pin_and_clues(self):
  saved=json.loads((ROOT/'execution/PKG-01/DEL-01-06/Work/supplier-notice-associations/observations.json').read_text())
  self.assertEqual({r['path']:r['sha256'] for r in saved['components']},module.SUBJECTS)
  self.assertEqual(saved['tool_sha256'],module.reader.sha(Path(module.__file__).read_bytes()))
  for row in saved['components']:
   self.assertEqual([bytes.fromhex(c['bytes_hex']) for c in row['embedded_clues']],module.CLUES[row['path']])

if __name__=='__main__':unittest.main()
