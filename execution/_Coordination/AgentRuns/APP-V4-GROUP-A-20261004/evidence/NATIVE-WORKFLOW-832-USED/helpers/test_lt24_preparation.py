import json,pathlib,sys,unittest
from unittest.mock import patch
from parent_launch import development_start_option,main,validate_compiled
from witness_common import sha
HERE=pathlib.Path(__file__).resolve().parent
class Controls(unittest.TestCase):
    def test_explicit_development_option_positive(self):
        self.assertEqual(development_start_option(True),{'allowUnverifiedDev':True,'transition':'LT-24','supplierStanding':'unverified-development','qualifiedDistribution':False})
    def test_omission_refuses_before_inputs_or_supplier(self):
        argv=['parent_launch.py','--execute-reviewed','--compiled-binding','/nonexistent','--reviewed-binding-sha256','unused','--supplier-manifest','/nonexistent','--approved-supplier-manifest-sha256','unused','--holding-source','/nonexistent','--keep-root','/nonexistent']
        with patch.object(sys,'argv',argv):
            with self.assertRaisesRegex(ValueError,'explicit existing LT-24'):main()
    def test_original_run_is_correct_refusal_not_source_receipt(self):
        snapshot=json.loads((HERE/'run1-evidence/host-final-snapshot.json').read_text())['beforeCleanup']
        self.assertEqual(snapshot['state'],'refused');self.assertIsNone(snapshot['generation']);self.assertEqual(snapshot['verification']['result'],'unverifiable')
        self.assertEqual([e['transitionId'] for e in snapshot['lifecycle']],['LT-01','LT-05'])
        cleanup=json.loads((HERE/'run1-evidence/cleanup.json').read_text());self.assertTrue(cleanup['clean']);self.assertEqual([e['stage'] for e in cleanup['ownedGroups']],[1])
        self.assertNotIn('cfg.allow_unverified_dev',(HERE/'lt24-preimage/parent_stock_workflow_witness.rs').read_text())
    def test_previous_artifact_binding_refuses_changed_fixture_helpers(self):
        with self.assertRaisesRegex(ValueError,'successor changes more|launcher/helper differs'):
            validate_compiled(pathlib.Path('/private/tmp/chirality-wf-bound-compile-dxb5u0js/launcher-successor-binding.json'))
    def test_original_run_files_unchanged(self):
        for path,digest in json.loads((HERE/'run1-evidence-origins.json').read_text()).items():self.assertEqual(sha(path),digest)
if __name__=='__main__':unittest.main(verbosity=2)
