"""Guard regressions with mocked host observations, no real process sampling."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import tempfile,time,unittest
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('guard_controller',Path(__file__).with_name('native_successor_relaunch.py'));b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
class Guard(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=b.T3/'scratch',prefix='guard-fixture-');self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);(self.root/'guard').mkdir();(self.root/'guard/exclusive.pending').touch()
        self.run=b.Run(self.root,{'bundle':'/invented/app','executable':'/invented/app/exe'},time.monotonic()+60)
    def observe(self,memguard_ok=True):
        return patch.object(b.subprocess,'run',return_value=SimpleNamespace(returncode=0 if memguard_ok else 1,stdout='9\n' if memguard_ok else '',stderr=''))
    def test_exclusive_does_not_stale_held_samples_but_refuses_admission(self):
        with patch.object(b,'T3',self.root),self.observe(),patch.object(b.subprocess,'check_output',side_effect=['123 1 100 /invented/app/exe\n','80']):
            self.run.sample()
        self.assertEqual(self.run.reason,'exclusive pending');self.assertGreater(self.run.last_sample,0)
        self.assertEqual(self.run.sampling['ps_census_and_rss']['value']['processes'][0]['pid'],123)
        with patch.object(b,'T3',self.root),self.observe(),patch.object(b.subprocess,'check_output',side_effect=['5 1 100 /unrelated\n','80']):
            with self.assertRaisesRegex(RuntimeError,'exclusive'):self.run.sample(admission=True)
        self.assertEqual(self.run.observed_processes,[])
    def test_missing_memguard_does_not_skip_census_and_free_observation(self):
        with patch.object(b,'T3',self.root),self.observe(False),patch.object(b.subprocess,'check_output',side_effect=['5 1 100 /unrelated\n','80']):
            with self.assertRaisesRegex(RuntimeError,'memguard'):self.run.sample()
        self.assertFalse(self.run.sampling['shared_memguard_pgrep']['ok'])
        self.assertTrue(self.run.sampling['ps_census_and_rss']['ok']);self.assertTrue(self.run.sampling['sysctl_free_percent']['ok'])
    def test_census_failure_is_timestamped_without_fake_freshness(self):
        with patch.object(b,'T3',self.root),self.observe(),patch.object(b.subprocess,'check_output',side_effect=[OSError('ps refused'),'80']):
            with self.assertRaisesRegex(RuntimeError,'ps refused'):self.run.sample()
        self.assertEqual(self.run.last_sample,0);self.assertFalse(self.run.sampling['ps_census_and_rss']['ok'])
        self.assertEqual(self.run.sampling['sysctl_free_percent']['value'],80)
if __name__=='__main__':unittest.main()
