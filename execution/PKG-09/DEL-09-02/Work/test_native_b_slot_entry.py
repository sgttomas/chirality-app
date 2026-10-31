"""Harmless mocked fixed slot invocation; never execs controller/App."""
from pathlib import Path
from datetime import datetime,timezone
import importlib.util,json,os,tempfile,unittest
from unittest.mock import patch
s=importlib.util.spec_from_file_location('slot_fixture',Path(__file__).with_name('native_b_slot_entry.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class SlotTests(unittest.TestCase):
 def test_fixed_after_acquisition_exec_preserves_identity_and_refuses_reuse(self,version='chirality.native-B.retained-state/v2'):
  with tempfile.TemporaryDirectory(dir=m.T3/'scratch',prefix='slot-fixture-') as name:
   root=Path(name).resolve();script=root/'native_b_slot_entry.py';script.write_text('invented copied entry source')
   controller=root/'native_successor_relaunch.py';controller.write_text('never executed')
   a={'admission_version':version,'slot_entry_sha256':m.sha(script),'controller_path':str(controller),'dependencies':{str(controller):m.sha(controller)}}
   (root/'admission.json').write_text(json.dumps(a))
   class Clock:
    @staticmethod
    def now(zone):return datetime(2026,10,31,15,0,0,tzinfo=timezone.utc)
   with patch.object(m,'__file__',str(script)),patch.object(m,'datetime',Clock),patch.object(m.subprocess,'check_output',return_value=str(m.T3/'tools/t3_slot_run.sh')),patch.object(m.os,'execve') as execute:
    m.main();record=json.loads((root/'slot-entry.json').read_text())
    self.assertEqual(record['fixed_window_end'],'2026-10-31T15:04:55+00:00')
    self.assertEqual(record['controller_pid'],os.getpid());self.assertEqual(record['slot_parent_pid'],os.getppid())
    self.assertEqual(execute.call_args.args[1],record['command'])
    with self.assertRaisesRegex(RuntimeError,'already used'):m.main()
    execute.assert_called_once()
 def test_v3_uses_same_fixed_once_only_slot_contract(self):
  self.test_fixed_after_acquisition_exec_preserves_identity_and_refuses_reuse('chirality.native-B.retained-state/v3')
 def test_v4_uses_same_fixed_once_only_slot_contract(self):
  self.test_fixed_after_acquisition_exec_preserves_identity_and_refuses_reuse('chirality.native-B.retained-state/v4')
 def test_v5_uses_same_fixed_once_only_slot_contract(self):
  self.test_fixed_after_acquisition_exec_preserves_identity_and_refuses_reuse('chirality.native-B.retained-state/v5')
 def test_v6_uses_same_fixed_once_only_slot_contract(self):
  self.test_fixed_after_acquisition_exec_preserves_identity_and_refuses_reuse('chirality.native-B.retained-state/v6')
 def test_wrong_parent_never_executes(self):
  with tempfile.TemporaryDirectory(dir=m.T3/'scratch',prefix='slot-fixture-') as name:
   with patch.object(m,'__file__',str(Path(name)/'entry.py')),patch.object(m.subprocess,'check_output',return_value='not-slot'),patch.object(m.os,'execve') as execute:
    with self.assertRaisesRegex(RuntimeError,'slot parent'):m.main()
    execute.assert_not_called()
if __name__=='__main__':unittest.main()
