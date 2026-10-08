"""Invented connected SQ file receiving; no actual examination or qualification."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from jsonschema import Draft202012Validator

APP = Path(__file__).resolve().parents[1]
FIXTURE = APP / 'tests/group_b_sq_receiving_fixtures/development'

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec); spec.loader.exec_module(value)
    return value

reader = module('sq_receive_test', APP / 'examination/sq_receiving/receive.py')
canonical = module('sq_canonical_test', APP / 'examination/support_identity/canonical.py')

def encoded(value): return (json.dumps(value, indent=2) + '\n').encode()
def sha(value): return hashlib.sha256(value).hexdigest()


class SQReceivingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.consumer = reader.Receiver()
        cls.support = canonical.CanonicalSupport()
        schema = next((APP.parent / 'execution').glob('PKG-09*/1_Working/DEL-09-01*/Design/exam.result-record.schema.json'))
        cls.result_validator = Draft202012Validator(json.loads(schema.read_bytes()))

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / 'case'
        shutil.copytree(FIXTURE, self.root)
        self.selected = json.loads((self.root / 'selection.json').read_bytes())
        self.dossier = json.loads((self.root / 'dossier.json').read_bytes())

    def a(self, slot): return next(x for x in self.selected['artifacts'] if x['slot'] == slot)
    def value(self, slot): return json.loads((self.root / self.a(slot)['record']['path']).read_bytes())
    def save(self, slot, value, update_basis=True):
        a = self.a(slot); raw = encoded(value)
        (self.root / a['record']['path']).write_bytes(raw); a['record']['sha256'] = sha(raw)
        binding = encoded(self.support.binding(a['kind'], raw, self.selected['purpose']))
        (self.root / a['binding']['path']).write_bytes(binding); a['binding']['sha256'] = sha(binding)
        if update_basis and self.selected['review'] and slot in self.selected['review']['results']:
            self.selected['review']['results'][slot] = {k:value[k] for k in ('subject','configuration','criterion')}

    def add(self, slot, kind, value):
        self.selected['artifacts'].append({'slot':slot,'kind':kind,'record':{'path':slot+'.json','sha256':'0'*64},'binding':{'path':slot+'.binding.json','sha256':'0'*64}})
        self.save(slot,value)

    def check(self):
        data=encoded(self.dossier);(self.root/'dossier.json').write_bytes(data);self.selected['dossier']['sha256']=sha(data)
        raw=encoded(self.selected);(self.root/'selection.json').write_bytes(raw)
        return self.consumer.check(self.root/'selection.json',sha(raw))

    def refused(self, needle):
        result=self.check();self.assertFalse(result['selection_consistent'],result)
        self.assertIn(needle,json.dumps(result));return result

    def incomplete(self, needle):
        result=self.check();self.assertEqual(result['coverage'],'incomplete',result)
        self.assertIn(needle,json.dumps(result));return result

    def schema_valid(self, value): self.assertEqual(list(self.result_validator.iter_errors(value)),[])

    def test_connected_development_full_source_validation_no_package_change(self):
        result=self.check();self.assertTrue(result['selection_consistent']);self.assertEqual(result['coverage'],'complete')
        self.assertEqual(len(self.selected['steps']),23);self.assertEqual(self.selected['packages'],[]);self.assertEqual(self.selected['changes'],[])
        self.assertEqual(set(result['reported_outcomes'].values()),{'fail','blocked','not-run'})
        self.assertTrue(any(x['scope']=='SQ' for x in result['existing_checks']))
        self.assertEqual(len([x for x in result['existing_checks'] if x['scope'].startswith('review/')]),23)
        for field in ('current_reliance','qualification_established','native_observation_verified','actual_producer_use_verified','publication_authority_authenticated','method_adoption_authenticated'):
            self.assertIs(result[field],False)

    def test_old_six_role_route_does_not_accept_new_selection(self):
        self.check()
        with self.assertRaisesRegex(ValueError,'canonical selection'):
            self.support.check(self.root/'selection.json',sha((self.root/'selection.json').read_bytes()))
        self.assertEqual(self.check()['coverage'],'complete')

    def test_ce02_rehashed_outcome_mismatch(self):
        v=self.value('result-J-1');v['outcome']='blocked';v['blocked_by']='INVENTED missing input';self.schema_valid(v);self.save('result-J-1',v)
        self.refused('step outcome mismatch')

    def test_ce03_rehashed_candidate_mismatch(self):
        v=self.value('result-J-1');v['subject']['app_candidate']['build_identity']='INVENTED-OTHER';self.schema_valid(v);self.save('result-J-1',v)
        self.refused('direct candidate mismatch')

    def test_ce04_missing_record_is_not_fabricated(self):
        (self.root/self.a('result-J-1')['record']['path']).unlink();self.incomplete('selected file missing')

    def partial(self):
        slot='result-J-3';step=next(s for s in self.dossier['scenarios'][0]['steps'] if s['step']=='J-3')
        step['state']='planned';step.pop('outcome');step.pop('result_record');self.dossier['scenarios'][0].pop('outcome')
        self.selected['steps']=[s for s in self.selected['steps'] if s['result_slot']!=slot]
        self.selected['artifacts']=[a for a in self.selected['artifacts'] if a['slot']!=slot]
        self.selected['review']['results'].pop(slot)
        self.selected['review']['evidence']=[e for e in self.selected['review']['evidence'] if e['ref']!='INVENTED-SQ-J-3']
        v=self.value('review');v['evidence_set'].remove('INVENTED-SQ-J-3');self.save('review',v)

    def test_ce05_partial_without_fabricated_outcome(self):
        self.partial();r=self.incomplete('non-recorded steps');self.assertTrue(r['selection_consistent'])

    def test_ce06_partial_handoff_refused(self):
        self.partial();self.dossier['handoff']['handed_over']=True;self.refused('SQ-R8')

    def packaged(self, slot='result-J-1'):
        v=self.value(slot);v['configuration']['route']['kind']='native_packaged';v['subject']['app_candidate'].update(packaged=True,package_record='INVENTED-PACKAGE');self.save(slot,v)
        pkg=json.loads((APP/'tests/group_b_fixtures/package.json').read_bytes());pkg['app'].update({k:self.selected['candidate'][k] for k in ('revision','build_identity')})
        self.add('package','package',pkg);self.selected['packages']=[{'ref':pkg['record_id'],'slot':'package','result_slots':[slot]}]
        return pkg

    def test_ce07_package_citation_missing_bytes(self):
        self.packaged();(self.root/'package.json').unlink();self.incomplete('selected file missing')

    def test_conditional_package_calls_existing_join_preserves_failure_gaps(self):
        self.packaged();r=self.check();self.assertTrue(r['selection_consistent'],r);self.assertEqual(r['coverage'],'complete')
        joined=next(x for x in r['existing_checks'] if x['scope']=='package/result-J-1')
        self.assertIn('linked native result reported fail',joined['reported_prerequisite_gaps'])

    def test_development_package_citation_does_not_claim_packaged_join(self):
        self.packaged();v=self.value('result-J-1');v['configuration']['route']['kind']='native_development';self.save('result-J-1',v)
        r=self.check();self.assertTrue(r['selection_consistent'],r);self.assertEqual(r['coverage'],'unsupported')

    def test_ce08_packaged_not_run_exception(self):
        v=self.value('result-J-3');v['configuration']['route']['kind']='native_packaged';self.schema_valid(v);self.save('result-J-3',v)
        self.assertEqual(self.check()['coverage'],'complete')

    def test_ce09_review_extra_citation_unmapped(self):
        v=self.value('review');v['evidence_set'].append('INVENTED-EXTRA');self.save('review',v);self.incomplete('review evidence mapping incomplete')

    def history(self, state='reopened'):
        before=self.value('result-J-1');self.add('before-J-1','result',before)
        after=copy.deepcopy(before);after['currency']={'state':state,'change_ref':'INVENTED-CHANGE'};self.save('result-J-1',after)
        change={'record_kind':'exam_change_impact','format':'EXP-v0.2','record_id':'INVENTED-CHANGE','change':{'kind':'configuration','description':'INVENTED configuration change','evidence':'INVENTED change evidence'},'from':'INVENTED-before','to':'INVENTED-after','affected':[{'case_id':'J-1','prior_result':before['record_id'],'reason':'INVENTED changed setting'}],'unaffected_basis':'INVENTED unaffected other cases','date':'2026-10-08'}
        self.add('change','change',change)
        self.selected['changes']=[{'slot':'change','from_alias':'INVENTED-before','to_alias':'INVENTED-after','pairs':[{'before_slot':'before-J-1','after_slot':'result-J-1','rerun_slot':None,'before_basis':{k:before[k] for k in ('subject','configuration','criterion')},'rerun_basis':None}]}]
        self.dossier['currency']={'state':state,'change_ref':'INVENTED-CHANGE'}

    def test_ce10_reopened_no_rerun_history_is_preserved(self):
        self.history();r=self.check();self.assertTrue(r['selection_consistent'],r);self.assertEqual(r['coverage'],'complete');self.assertFalse(r['current_reliance'])
        self.assertEqual(r['reported_outcomes']['result-J-1'],'fail')
        self.assertTrue(any(x['scope']=='change/result-J-1' for x in r['existing_checks']))

    def test_historical_missing_prior_is_incomplete(self):
        self.history('historical');(self.root/'before-J-1.json').unlink();self.incomplete('change pair bytes unavailable')

    def test_history_mutation_refused_by_existing_change_join(self):
        self.history();v=self.value('before-J-1');v['evidence'].append({'ref':'INVENTED different evidence','provenance':'test_definition'});self.save('before-J-1',v)
        self.refused('CHANGE-HISTORY-MUTATED')

    def test_review_cannot_substitute_before_snapshot_for_same_id_direct_result(self):
        self.history()
        entry=next(e for e in self.selected['review']['evidence'] if e['ref']=='INVENTED-SQ-J-1')
        entry['target']={'slot':'before-J-1'}
        self.refused('different snapshot than the direct result')

    def historical_package_pair(self, supplied=False):
        before=self.value('result-J-1');before['record_id']='INVENTED-OLD-J-1'
        before['subject']['app_candidate'].update(revision='INVENTED-OLD-REV',build_identity='INVENTED-OLD-BUILD',packaged=True,package_record='MISSING-HIST-PACKAGE')
        before['configuration']['route']['kind']='native_packaged'
        self.add('historical-before','result',before)
        after=copy.deepcopy(before);after['currency']={'state':'historical','change_ref':'INVENTED-OLD-CHANGE'};self.add('historical-after','result',after)
        change={'record_kind':'exam_change_impact','format':'EXP-v0.2','record_id':'INVENTED-OLD-CHANGE','change':{'kind':'candidate_code','description':'INVENTED candidate change','evidence':'INVENTED change evidence'},'from':'INVENTED-old','to':'INVENTED-current','affected':[{'case_id':'J-1','prior_result':before['record_id'],'reason':'INVENTED affected old candidate'}],'unaffected_basis':'INVENTED unaffected other cases','date':'2026-10-08'}
        self.add('historical-change','change',change)
        self.selected['changes']=[{'slot':'historical-change','from_alias':'INVENTED-old','to_alias':'INVENTED-current','pairs':[{'before_slot':'historical-before','after_slot':'historical-after','rerun_slot':None,'before_basis':{k:before[k] for k in ('subject','configuration','criterion')},'rerun_basis':None}]}]
        if supplied:
            pkg=json.loads((APP/'tests/group_b_fixtures/package.json').read_bytes());pkg['record_id']='MISSING-HIST-PACKAGE';pkg['app'].update(revision='INVENTED-OLD-REV',build_identity='INVENTED-OLD-BUILD')
            self.add('historical-package','package',pkg);self.selected['packages']=[{'ref':pkg['record_id'],'slot':'historical-package','result_slots':['historical-before','historical-after']}]

    def test_missing_historical_package_is_incomplete(self):
        self.historical_package_pair();self.incomplete('cited package selection missing')

    def test_supplied_historical_package_uses_its_own_candidate(self):
        self.historical_package_pair(True);r=self.check();self.assertTrue(r['selection_consistent'],r);self.assertEqual(r['coverage'],'unsupported')
        self.assertIn('package-link not evaluated: historical-after',r['unsupported_joins'])
        self.assertIn('package-link not evaluated: historical-before',r['unsupported_joins'])
        self.assertFalse(r['qualification_established'])

    def test_historical_package_cannot_use_current_candidate_identity(self):
        self.historical_package_pair(True);pkg=self.value('historical-package');pkg['app'].update({k:self.selected['candidate'][k] for k in ('revision','build_identity')});self.save('historical-package',pkg)
        self.refused('package candidate/reference mismatch')

    def test_ce11_false_independence_refused(self):
        v=self.value('review');v['reported_as_independent']=True;self.save('review',v);self.selected['review']['reported_as_independent']=True;self.refused('EXP-R6')

    def test_ce12_false_adoption_field_refused(self):
        self.selected['adopted']=True;self.refused('missing or unknown fields')

    def test_ce13_exact_bytes_substitution_refused(self):
        p=self.root/'result-J-1.json';p.write_bytes(p.read_bytes()+b' ');self.refused('exact-byte mismatch')

    def test_ce14_annotated_id_refused(self):
        self.dossier['scenarios'][0]['steps'][0]['result_record']+=' part stop';self.refused('step result ID mismatch')

    def test_ce15_result_cannot_be_opaque_evidence(self):
        target=self.selected['review']['evidence'][1];target['target']=copy.deepcopy(self.a('result-J-1')['record']);self.refused('masquerades as opaque')

    def test_ce17_exact_dossier_omission_fail_before_restore_pass_after(self):
        entry=self.selected['review']['evidence'].pop(0);v=self.value('review');v['evidence_set'].remove(self.dossier['record_id']);self.save('review',v)
        r=self.incomplete('exact dossier review citation absent');self.assertTrue(r['selection_consistent'])
        v['evidence_set'].insert(0,self.dossier['record_id']);self.save('review',v);self.selected['review']['evidence'].insert(0,entry)
        self.assertEqual(self.check()['coverage'],'complete')

    def test_dossier_contradictory_target_refused(self):
        self.selected['review']['evidence'][0]['target']={'slot':'result-J-1'};self.refused('contradictory dossier review target')

    def test_missing_review_is_incomplete_not_exempt(self):
        self.dossier['examiner'].pop('review_record');self.selected['review']=None;self.selected['artifacts']=[a for a in self.selected['artifacts'] if a['slot']!='review'];r=self.incomplete('primary review absent');self.assertTrue(r['selection_consistent'])

    def test_missing_required_outcome_reason_rejected_by_schema(self):
        v=self.value('result-J-3');v.pop('not_run_because');self.save('result-J-3',v);self.refused('SCHEMA')

    def test_mixed_purpose_binding_refused(self):
        a=self.a('review');p=self.root/a['binding']['path'];v=json.loads(p.read_bytes());v['binding_purpose']='historical_correspondence';p.write_bytes(encoded(v));a['binding']['sha256']=sha(p.read_bytes());self.refused('canonical binding identity mismatch')

    def test_missing_prototype_identity_refused_despite_schema_optionality(self):
        v=self.value('result-J-1');v['support_revision'].pop('prototype_digest');self.schema_valid(v);self.save('result-J-1',v);self.refused('support identity missing or different')

    def test_duplicate_keys_refused_even_with_updated_digest(self):
        p=self.root/'result-J-1.json';data=p.read_bytes().replace(b'"record_kind": "exam_result",',b'"record_kind": "exam_result", "record_kind": "exam_result",',1);p.write_bytes(data);self.a('result-J-1')['record']['sha256']=sha(data);self.refused('duplicate JSON key')

    def test_path_traversal_and_symlink_refused(self):
        a=self.a('result-J-1');old=a['record']['path'];a['record']['path']='../'+old;self.refused('non-canonical relative path');a['record']['path']=old
        target=self.root/old;data=target.read_bytes();target.unlink();outside=self.root.parent/'outside.json';outside.write_bytes(data);target.symlink_to(outside);self.refused('symbolic link refused')

    def test_source_drift_refuses_before_inputs(self):
        original=reader.read_relative
        def changed(root,name):
            data=original(root,name)
            return data+b'\n' if name.endswith('/sq-exp-receiving-v1/RECEIVING.md') else data
        with patch.object(reader,'read_relative',changed):
            with self.assertRaisesRegex(ValueError,'selected source changed'):
                reader.Receiver()

    def test_boolean_target_cannot_be_integer(self):
        self.selected['review']['evidence'][0]['target']={'dossier':1};self.refused('invalid evidence target flag')

    def test_opaque_review_bytes_checked_but_not_interpreted(self):
        raw=b'{"native_custody":true,"path":"not-a-dependency","sha256":"invented"}\n';(self.root/'opaque.json').write_bytes(raw)
        v=self.value('review');v['evidence_set'].append('INVENTED-OPAQUE');self.save('review',v)
        self.selected['review']['evidence'].append({'ref':'INVENTED-OPAQUE','target':{'path':'opaque.json','sha256':sha(raw)}})
        r=self.check();self.assertEqual(r['coverage'],'complete');self.assertFalse(r['native_observation_verified'])
        (self.root/'opaque.json').write_bytes(raw+b' ');self.refused('exact-byte mismatch')


if __name__=='__main__':
    unittest.main()
