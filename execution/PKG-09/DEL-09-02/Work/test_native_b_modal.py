"""Derived modal ownership/question tests. No native APIs, capture or UI input."""
import copy,ctypes as C,importlib.util,unittest
from pathlib import Path
from types import SimpleNamespace
s=importlib.util.spec_from_file_location('modal_route_test',Path(__file__).with_name('native_b_screen_route.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);w=m.w
G={'appSession':'invented-session','home':'invented-home','spawnCounter':3}
def question(state='ready'):
 text=f'Stop Codex for this home? Home: account · App session invented-session · Codex process start 3 · state {state} '
 if state!='ready':text+=f'Codex is {state}, not ready: live work cannot be observed and nothing is sent to it; only the process is stopped. '
 return text+('Observed: no live turns, waiting requests, delegated agents or workflow runs in force. Stop Codex stops this Codex process. '
 'None observed is not none: coverage is not complete. This is your operational choice, not a recorded act. If you confirm, the App writes the stop and each interrupt to its recovery ledger before sending; what the ledger accepts can be read after a relaunch. '
 'Observed at 2026-10-31T12:00:00.000Z. Stop Codex proceeds; Keep Codex running (the default) and Cancel change nothing.')
class ModalTests(unittest.TestCase):
 def setUp(self):
  self.main={'number':10,'title':w.TITLE,'bounds':{'X':0,'Y':0,'Width':1100,'Height':800},'on_screen':True,'layer':0}
  self.modal={'number':20,'title':'Stop Codex','bounds':{'X':300,'Y':200,'Width':500,'Height':400},'on_screen':True,'layer':8}
  self.rows=[self.modal,self.main]
  self.backend=SimpleNamespace(window_rows=lambda:self.rows,owner_pid=lambda row:123,decode_owned_window=lambda row,access:row)
  main={**self.main,'window_id':10};main.pop('number')
  self.context={'posted':True,'identity':{'pid':123},'generation':G,'main':main,'before_inventory':[main]}
 def test_unique_new_owned_modal_is_derived_not_arbitrary_window(self):
  result=w.select_modal(self.backend,123,self.context)
  self.assertEqual(result['window_id'],20);self.assertEqual(result['title'],'Stop Codex')
 def test_missing_window_title_still_requires_unique_derived_modal(self):
  self.modal['title']=None
  result=w.select_modal(self.backend,123,self.context)
  self.assertIsNone(result['title']);self.assertEqual(result['window_id'],20)
  self.rows=[self.modal,self.modal,self.main]
  with self.assertRaisesRegex(RuntimeError,'ambiguous'):w.select_modal(self.backend,123,self.context)
 def test_main_substitution_missing_ambiguous_and_wrong_title_refuse(self):
  for rows in ([self.main],[self.modal,self.modal,self.main],[{**self.modal,'title':'Unrelated'},self.main],[self.modal,{**self.main,'number':11}]):
   self.rows=rows
   with self.assertRaises(RuntimeError):w.select_modal(self.backend,123,self.context)
 def test_foreign_row_is_not_decoded_or_selected(self):
  foreign={**self.modal,'number':999};self.rows=[foreign,self.main]
  self.backend.owner_pid=lambda row:999 if row is foreign else 123
  def decode(row,access):
   self.assertIsNot(row,foreign);return row
  self.backend.decode_owned_window=decode
  with self.assertRaises(w.WindowUnavailable):w.select_modal(self.backend,123,self.context)
 def test_no_posted_stop_cannot_authorize_modal(self):
  self.context['posted']=False
  with self.assertRaisesRegex(RuntimeError,'posted Stop'):w.select_modal(self.backend,123,self.context)
 def test_full_observed_question_must_match_account_generation_and_all_effects(self):
  for state in ('starting','handshaking','ready','halted-after-repeated-failure','exited-unexpectedly'):
   self.assertEqual(m.validate_stop_question('Stop Codex',question(state),G,'invented-home'),question(state))
  for text in (question().replace('account','key',1),question().replace('start 3','start 4'),question()+' Also delete another project.',question().replace('no live turns','2 live turns'),question().replace('stops this Codex process.','restarts this Codex process.')):
   with self.assertRaises(RuntimeError):m.validate_stop_question('Stop Codex',text,G,'invented-home')
  with self.assertRaises(RuntimeError):m.validate_stop_question('Stop Codex',question(),G,'foreign-home')
 def test_unavailable_ax_relation_is_reported_not_fabricated(self):
  self.assertEqual(w.modal_relation(self.backend,123,20,10)['status'],'unavailable')
 def test_exposed_modal_parent_and_contradictions(self):
  ids={2:10,3:20};roles={2:'AXWindow',3:'AXWindow'}
  class Getter:
   def __call__(self,e,out):out._obj.value=ids.get(e,0);return 0
  def attribute(e,name):
   value={'return_code':0,'type':{'name':'CFString'},'value':None};refs=[]
   if e==1:refs=[2,3]
   elif name=='AXRole':value['value']=roles[e]
   elif name=='AXModal':value['value']=True
   elif name=='AXParent':refs=[1]
   return value,refs
  backend=SimpleNamespace(a=SimpleNamespace(_AXUIElementGetWindow=Getter()),app=lambda pid:1,attribute=attribute,owner=lambda e:(0,123),equal=lambda a,b:a==b)
  result=w.modal_relation(backend,123,20,10)
  self.assertEqual(result['parent_relation'],'owned-application-parent')
  original=attribute
  backend.attribute=lambda e,n: ({'return_code':0,'value':False},[]) if e==3 and n=='AXModal' else original(e,n)
  with self.assertRaisesRegex(RuntimeError,'not modal'):w.modal_relation(backend,123,20,10)
  backend.attribute=original;roles[3]='AXSheet';ids[3]=10
  with self.assertRaisesRegex(RuntimeError,'sheet mapping'):w.modal_relation(backend,123,20,10)
 def test_confirmation_requires_modal_receipt_and_no_repeat_after_attempt(self):
  from unittest.mock import Mock
  import time
  run=SimpleNamespace(alive=Mock(),cleanup_end=time.monotonic()+295,value={'candidate_key':'invented','expected_generation_home':'invented-home'},
                      generation=G,stop_requested=True,stop_confirmed=False,record=Mock(),safe_log=Mock())
  b=SimpleNamespace(ACTOR='agent',now=w.d.now)
  session=m.ScreenSession(run,b)
  frame={'target':'stop-modal','sha256':'image','sequence':1}
  session.window=SimpleNamespace(modal_active=True,modal_confirm_attempted=False,stop_context={'posted':True,'generation':G},capture=Mock(return_value=frame),input=Mock(),last=frame)
  control={'action':'confirm-stop','complete_question':True,'unreadable':False,'button_label':'Stop Codex','question_title':'Stop Codex','question_text':question(),'point':[200,200]}
  session.next_control=Mock(return_value=(control,frame))
  session.confirm_stop(G);self.assertTrue(run.stop_confirmed);session.window.input.assert_called_once_with('click',frame,[200,200])
  session.window.modal_confirm_attempted=True
  with self.assertRaisesRegex(RuntimeError,'already attempted'):session.confirm_stop(G)
  session.window.input.assert_called_once()
 def test_confirmation_reobserve_does_not_consume_unsent_confirmation(self):
  from unittest.mock import Mock
  import time
  run=SimpleNamespace(alive=Mock(),cleanup_end=time.monotonic()+295,value={'expected_generation_home':'invented-home'},generation=G,stop_confirmed=False,record=Mock(),safe_log=Mock())
  session=m.ScreenSession(run,SimpleNamespace(ACTOR='agent',now=w.d.now));frame={'target':'stop-modal'}
  session.window=SimpleNamespace(modal_active=True,modal_confirm_attempted=False,stop_context={'posted':True,'generation':G},capture=Mock(return_value=frame),input=Mock(side_effect=w.Reobserve('changed')))
  c={'action':'confirm-stop','complete_question':True,'unreadable':False,'button_label':'Stop Codex','question_title':'Stop Codex','question_text':question(),'point':[200,200]}
  session.next_control=Mock(side_effect=[(c,frame),({'action':'refuse','reason':'test'},frame)])
  with self.assertRaisesRegex(RuntimeError,'scope refused'):session.confirm_stop(G)
  self.assertFalse(run.stop_confirmed)
if __name__=='__main__':unittest.main()
