"""Image-backed operator observations never bypass existing B gates."""
import importlib.util,json,tempfile,time,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock,patch
s=importlib.util.spec_from_file_location('screen_route_test',Path(__file__).with_name('native_b_screen_route.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class ScreenTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir='/Users/ryan/dev/chirality-t3/scratch',prefix='screen-route-fixture-');self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name).resolve();self.run=SimpleNamespace(root=self.root,value={'candidate_key':'invented'},admission_sha='a'*64,cleanup_end=time.monotonic()+295,alive=Mock(),record=Mock(),report=Mock(),safe_log=Mock(),generation=None,stop_requested=False)
  self.b=SimpleNamespace(now=m.w.d.now,decode_diagnostics=Mock(side_effect=RuntimeError('missing native diagnostic strings')),ACTOR='agent')
  self.screen=m.ScreenSession(self.run,self.b)
  self.frame={'at':m.w.d.now(),'sequence':1,'sha256':'f'*64}
  self.screen.window=SimpleNamespace(last=self.frame,frames={1:self.frame},sequence=0,capture=Mock(return_value=self.frame),input=Mock())
 def control(self,**values):
  value={'candidate':'invented','admission_sha256':'a'*64,'capture_sha256':'f'*64,**values}
  def deliver(event):
   if event.get('event')=='native_screen_operator_step':
    p=Path(event['prompt']['control_file']);p.write_text(json.dumps(value));p.chmod(0o600)
  self.run.report.side_effect=deliver
 def test_no_fabricated_source_dict_or_unreadable_transcript_is_accepted(self):
  self.control(action='observe',frames=[1],strings=['ready'],generation={'invented':True},complete_sections=[],unreadable=True)
  with self.assertRaisesRegex(RuntimeError,'missing/unclear'):self.screen.observe()
  self.b.decode_diagnostics.assert_not_called()
 def test_existing_decoder_still_refuses_incomplete_displayed_json(self):
  self.control(action='observe',frames=[1],strings=['ready'],complete_sections=['state-generation','lifecycle-clientRequests','raw-envelopes'],unreadable=False)
  with self.assertRaisesRegex(RuntimeError,'missing native'):self.screen.observe()
  self.b.decode_diagnostics.assert_called_once_with(['ready'],protocol=True)
 def test_next_action_requires_actual_expected_effect_readback(self):
  self.screen.pending_effect=True;self.control(action='click-disclosure',target='host-diagnostics',point=[10,20])
  with self.assertRaisesRegex(RuntimeError,'actual expected effect'):self.screen.observe()
  self.screen.window.input.assert_not_called()
 def test_auth_and_unbound_stop_targets_are_not_available(self):
  self.control(action='click-disclosure',target='sign-in',point=[10,20])
  with self.assertRaisesRegex(RuntimeError,'non-B'):self.screen.observe()
  self.screen.window.input.assert_not_called()
 def test_transcript_cannot_reuse_previous_phase_images(self):
  self.screen.window.sequence=5;self.screen.window.frames[6]={**self.frame,'sequence':6};self.screen.window.last=self.screen.window.frames[6]
  self.control(action='observe',frames=[1],strings=['old'],complete_sections=['state-generation','lifecycle-clientRequests','raw-envelopes'],unreadable=False)
  with self.assertRaisesRegex(RuntimeError,'references unavailable'):self.screen.observe()
 def test_unreadable_effect_can_refuse_without_faking_confirmation(self):
  self.screen.pending_effect=True;self.control(action='refuse',reason='effect unclear')
  with self.assertRaisesRegex(RuntimeError,'effect unclear'):self.screen.observe()
  self.screen.window.input.assert_not_called()
 def test_ambiguous_input_failure_keeps_effect_readback_required(self):
  self.control(action='click-disclosure',target='host-diagnostics',point=[10,20])
  self.screen.window.input.side_effect=RuntimeError('helper failed after possible post')
  with self.assertRaisesRegex(RuntimeError,'helper failed'):self.screen.observe()
  self.assertTrue(self.screen.pending_effect)
 def test_prequeued_action_is_not_consumed(self):
  p=self.root/'screen-control-001.json';p.write_text('{}');p.chmod(0o600)
  with self.assertRaisesRegex(RuntimeError,'prequeued'):self.screen.observe()
  self.screen.window.input.assert_not_called()
 def test_pending_effect_can_recapture_without_claiming_success(self):
  self.screen.pending_effect=True;responses=iter([{'action':'capture'},{'action':'refuse','reason':'still unclear'}])
  def deliver(event):
   if event.get('event')=='native_screen_operator_step':
    p=Path(event['prompt']['control_file']);p.write_text(json.dumps({'candidate':'invented','admission_sha256':'a'*64,'capture_sha256':'f'*64,**next(responses)}));p.chmod(0o600)
  self.run.report.side_effect=deliver
  with self.assertRaisesRegex(RuntimeError,'still unclear'):self.screen.observe()
  self.assertTrue(self.screen.pending_effect);self.assertEqual(self.screen.window.capture.call_count,2)
  self.screen.window.input.assert_not_called()
 def test_cleanup_observation_does_not_require_raw_envelopes(self):
  self.b.decode_diagnostics.side_effect=None;self.b.decode_diagnostics.return_value={'generation':'invented'}
  self.control(action='observe',frames=[1],strings=['source and lifecycle only'],complete_sections=['state-generation','lifecycle-clientRequests'],unreadable=False)
  self.screen.observe(protocol=False)
  self.b.decode_diagnostics.assert_called_once_with(['source and lifecycle only'],protocol=False)
if __name__=='__main__':unittest.main()
