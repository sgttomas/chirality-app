"""Invented EXP review/change fixtures; these tests perform no actual examination."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

APP=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(APP/'examination/admission'))
import admission_check as check


class AdmissionFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.support=check.Support()

    def setUp(self):
        fixtures=APP/'tests/group_b_admission_fixtures'
        for name in ('before','after','rerun','change','review','review-selection','change-selection'):
            setattr(self,name.replace('-','_'),json.loads((fixtures/(name+'.json')).read_text()))

    def review_join(self): return self.support.review_join(self.review,self.rerun,self.review_selection)
    def change_join(self): return self.support.change_join(self.change,self.before,self.after,self.change_selection,self.rerun)

    def test_canonical_review_and_change_examples(self):
        sources=check.parse((APP/'examination/admission/sources.json').read_bytes())['sources']
        design=check.PROJECT/Path(next(p for p in sources if p.endswith('/exam.review-record.schema.json'))).parent
        results=json.loads((design/'exam.result-record.valid.examples.json').read_text())
        errors,index=self.support.index_results(results); self.assertEqual(errors,[])
        for kind,prefix in [('review','exam.review-record'),('change','exam.change-impact')]:
            for record in json.loads((design/(prefix+'.valid.examples.json')).read_text()):
                with self.subTest(record=record['record_id']): self.assertEqual(self.support.validate(kind,record,index),[])
            for suffix in ('invalid','rule-violations'):
                for item in json.loads((design/(prefix+'.'+suffix+'.examples.json')).read_text()):
                    with self.subTest(record=item['record']['record_id']):
                        errors=self.support.validate(kind,item['record'],index); self.assertTrue(errors)
                        if suffix=='rule-violations': self.assertIn(item['rule'],[e['code'] for e in errors])

    def test_exact_review_join_keeps_declared_scope(self):
        self.assertEqual(self.review_join(),([],[]))
        self.review['evidence_set'].append('other-capture')
        errors,unresolved=self.review_join(); self.assertEqual(errors,[]); self.assertEqual(unresolved,['other-capture'])

    def test_review_rejects_other_build_configuration_criterion_and_reviewer(self):
        mutations=[lambda:self.rerun['subject']['app_candidate'].update(build_identity='OTHER'),
                   lambda:self.rerun['configuration'].update(model='not_observed'),
                   lambda:self.rerun['criterion'].update(identity='sha256:'+'f'*64),
                   lambda:self.review['reviewer'].update(identity='OTHER'),
                   lambda:self.review['authors'][0].update(identity='OTHER'),
                   lambda:self.review['subject'].update(identity='OTHER')]
        for mutate in mutations:
            self.setUp(); mutate(); self.assertTrue(self.review_join()[0])

    def test_repair_confirmation_must_name_the_selected_reviewer(self):
        self.review['findings'][0]['disposition']['confirmed_by']='different reviewer'
        self.assertIn('REVIEW-REPAIR-CONFIRMER',[e['code'] for e in self.review_join()[0]])

    def test_non_independent_record_is_honest_not_upgraded(self):
        self.review['reported_as_independent']=False
        self.review['reviewer']['separation']='not_separate'
        self.review_selection['reported_as_independent']=False
        self.assertEqual(self.review_join(),([],[]))
        self.review_selection['reported_as_independent']=True
        self.assertIn('REVIEW-INDEPENDENCE-CLAIM',[e['code'] for e in self.review_join()[0]])

    def test_additional_person_does_not_replace_requested_review_kind(self):
        self.review['review_kind']='additional_person'; self.review['reviewer']['kind']='person'
        self.review['reviewer']['model_identity']='not_applicable'; self.review['family_claim']='not_established'
        self.review.pop('preference')
        self.assertIn('REVIEW-KIND',[e['code'] for e in self.review_join()[0]])

    def test_current_prior_result_and_duplicate_result_ids_refused(self):
        self.after['currency']={'state':'current'}
        self.assertIn('EXP-R8',[e['code'] for e in self.change_join()[0]])
        errors,_=self.support.index_results([self.before,self.before]); self.assertIn('DUPLICATE-RESULT-ID',[e['code'] for e in errors])

    def test_historical_outcome_evidence_and_identity_cannot_be_rewritten(self):
        for field,value in [('outcome','pass'),('evidence',[]),('record_id','OTHER')]:
            self.setUp(); self.after[field]=value
            self.assertIn('CHANGE-HISTORY-MUTATED',[e['code'] for e in self.change_join()[0]])

    def test_repair_pair_checks_rerun_case_candidate_and_change_citation(self):
        self.assertEqual(self.change_join(),([],[]))
        mutations=[lambda:self.rerun['case'].update(case_id='other'),
                   lambda:self.rerun['subject']['app_candidate'].update(revision='other'),
                   lambda:self.rerun['currency'].update(change_ref='other'),
                   lambda:self.change['affected'][0].update(rerun_result='other'),
                   lambda:self.change.update(to='other')]
        for mutate in mutations:
            self.setUp(); mutate(); self.assertTrue(self.change_join()[0])

    def test_criterion_change_requires_matching_disposition_citation(self):
        self.rerun['criterion']['identity']='sha256:'+'f'*64
        self.change_selection['rerun_basis']['criterion']=copy.deepcopy(self.rerun['criterion'])
        self.assertIn('CHANGE-CRITERION-DISPOSITION',[e['code'] for e in self.change_join()[0]])
        self.change['change'].update(kind='criterion_disposition',disposition_ref='INVENTED-DISPOSITION')
        self.rerun['criterion']['disposition_ref']='OTHER'
        self.change_selection['rerun_basis']['criterion']=copy.deepcopy(self.rerun['criterion'])
        self.assertIn('CHANGE-CRITERION-DISPOSITION',[e['code'] for e in self.change_join()[0]])
        self.rerun['criterion']['disposition_ref']='INVENTED-DISPOSITION'
        self.change_selection['rerun_basis']['criterion']=copy.deepcopy(self.rerun['criterion'])
        self.assertEqual(self.change_join(),([],[])) # Citation consistency only, not authorization.

    def test_unrun_rerun_stays_pending_and_other_affected_rows_unresolved(self):
        self.change['affected'][0].pop('rerun_result'); self.change_selection['rerun_basis']=None
        self.change['affected'].append({'case_id':'other','prior_result':'OTHER','reason':'unknown reliance'})
        errors,unresolved=self.support.change_join(self.change,self.before,self.after,self.change_selection)
        self.assertEqual(errors,[]); self.assertEqual(unresolved,['OTHER'])
        self.assertIn('EXP-R8',[e['code'] for e in self.support.validate('change',self.change,{self.after['record_id']:self.after})])

    def test_cited_but_missing_rerun_is_refused(self):
        errors,_=self.support.change_join(self.change,self.before,self.after,self.change_selection)
        self.assertIn('CHANGE-RERUN-MISSING',[e['code'] for e in errors])

    def test_duplicate_finding_and_unknown_selection_fields_refused(self):
        self.review['findings'].append(copy.deepcopy(self.review['findings'][0]))
        self.assertIn('REVIEW-DUPLICATE-FINDING',[e['code'] for e in self.review_join()[0]])
        self.review_selection['approve']=True
        with self.assertRaises(ValueError): self.review_join()

    def test_changed_source_lock_and_ambiguous_json_fail_closed(self):
        manifest=check.parse((APP/'examination/admission/sources.json').read_bytes())
        first=next(iter(manifest['sources'])); manifest['sources'][first]='0'*64
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'pins.json'; path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError,'source drift'): check.Support(manifest=path)
        for value in ('{"x":1,"x":2}','{"x":NaN}'):
            with self.assertRaises(ValueError): check.parse(value)

    def test_b1_b3_import_orders_are_isolated(self):
        # Each order runs in its own interpreter, as test collectors may load
        # either suite first. B1's generic check/rules must remain untouched.
        tests=APP/'tests'
        for order in (['group_b_support_test','group_b_admission_test'],
                      ['group_b_admission_test','group_b_support_test']):
            code="import sys; sys.path.insert(0,"+repr(str(tests))+"); "
            code+="import importlib; mods=[importlib.import_module(n) for n in "+repr(order)+"]; "
            code+="import group_b_support_test as b1, group_b_admission_test as b3; "
            code+="assert b1.Support is not b3.check.Support; assert b1.Support().prototype_digest; assert b3.check.Support().validators['review']"
            result=subprocess.run([sys.executable,'-c',code],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)

    def test_cli_real_file_join_reports_no_verification_or_admission(self):
        fixtures=APP/'tests/group_b_admission_fixtures'
        cmd=[sys.executable,str(APP/'examination/admission/admission_check.py'),'change-join']
        for field in ('change','before','after','rerun'): cmd+=['--'+field,str(fixtures/(field+'.json'))]
        cmd+=['--selection',str(fixtures/'change-selection.json')]
        output=subprocess.run(cmd,capture_output=True,text=True)
        self.assertEqual(output.returncode,0,output.stderr)
        report=json.loads(output.stdout); self.assertTrue(report['file_checks_passed'])
        self.assertFalse(report['review_or_repair_verified']); self.assertEqual(report['route_admission'],'not_established')
        self.assertEqual(len(report['inputs']),5)


if __name__=='__main__': unittest.main(verbosity=2)
