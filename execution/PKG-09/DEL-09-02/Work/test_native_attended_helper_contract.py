"""Real emitted JSON + staged helper parser; native boundary is never entered."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace as N
from datetime import datetime,timezone
import native_b_window as window
from native_attended_admission import NativeAdmissions
from native_successor_relaunch import write_once

HARNESS=r'''
import sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import native_b_window_helper as helper
class BoundaryReached(Exception):pass
def stop_before_native():raise BoundaryReached()
helper.w.d.NativeBackend=stop_before_native
try:helper.main(Path(sys.argv[2]),sys.argv[3])
except BoundaryReached:print('ACTUAL_STAGED_PARSER_ACCEPTED_BEFORE_NATIVE')
else:raise AssertionError('must not execute native helper work')
'''

class Tests(unittest.TestCase):
    def exercise(self,label,remove_inputs=False,modal=False):
        with tempfile.TemporaryDirectory(prefix='attended-helper-contract-') as d:
            root=Path(d).resolve();root.chmod(0o700);phase=root/label;phase.mkdir(mode=0o700)
            for name in ['helper-tmp','codex-home']:(phase/name).mkdir(mode=0o700)
            executable=root/'invented-App';executable.write_text('not executable; fixture only')
            config=window.configuration();window.stage(phase,config)
            admission=NativeAdmissions.__new__(NativeAdmissions)
            admission.root=root;admission.plan={'candidate':'invented-candidate'};admission.plan_sha='f'*64
            admission.value={'candidate_key':'invented-candidate','executable':str(executable),
                             'executable_sha256':window.sha(executable),'window_route':config}
            if label=='B':admission.value['expected_generation_home']='invented-home'
            admission.policy=lambda phase,root:'invented policy';admission.receipts={};admission.b=N(write_once=write_once)
            receipt=admission._receipt(label,{'fixture':'actual production emitter'})
            value=json.loads((phase/'admission.json').read_text())
            self.assertEqual(value['inputs'],admission.value)
            if remove_inputs:
                value.pop('inputs');(phase/'admission.json').write_text(json.dumps(value));(phase/'admission.json').chmod(0o600)
            request={'action':'capture','sequence':1,'identity':{'pid':123,'executable':str(executable)},
                     'window':{'window_id':1},'admission_sha256':window.sha(phase/'admission.json'),
                     'recorded_at':datetime.now(timezone.utc).isoformat(),'target':'main','image_name':'capture-001.unverified.png'}
            if modal:
                context=phase/'stop-modal-context.json'
                context.write_text(json.dumps({'identity':request['identity'],'posted':True,'generation':{'home':'invented-home'}}));context.chmod(0o600)
                request.update(target='stop-modal',stop_context_sha256=window.sha(context))
            path=phase/'request.json';path.write_text(json.dumps(request));path.chmod(0o600)
            env={'HOME':str(Path.home()),'PATH':'/usr/bin:/bin','TMPDIR':str(phase/'helper-tmp'),
                 'CODEX_HOME':str(phase/'codex-home'),'PYTHONDONTWRITEBYTECODE':'1'}
            result=subprocess.run([sys.executable,'-I','-B','-S','-c',HARNESS,str(phase),str(path),window.sha(path)],
                                  env=env,capture_output=True,text=True,timeout=10)
            if remove_inputs:
                self.assertNotEqual(result.returncode,0);self.assertIn("KeyError: 'inputs'",result.stderr)
                self.assertNotIn('ACTUAL_STAGED_PARSER_ACCEPTED',result.stdout)
            else:
                self.assertEqual(result.returncode,0,result.stderr)
                self.assertIn('ACTUAL_STAGED_PARSER_ACCEPTED_BEFORE_NATIVE',result.stdout)
            self.assertFalse(list(phase.glob('capture*')))
    def test_A_emitted_admission_is_accepted_by_actual_staged_helper(self):self.exercise('A')
    def test_B_emitted_admission_is_accepted_by_actual_staged_helper(self):self.exercise('B')
    def test_B_modal_context_uses_emitted_generation_home(self):self.exercise('B',modal=True)
    def test_historical_missing_inputs_fails_at_actual_deserialization(self):self.exercise('A',True)
