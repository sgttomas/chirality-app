"""PR40 source selection and invented boundary evidence; no host/native execution."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import swbpipe_catalog_v4_pr40_receiving as selected
import swbpipe_catalog_v4_pr30_receiving as prior
from swbpipe_hash_receiving import check_hash_pair, check_batch, check_snapshot, check_retained_result
from swbpipe_projection_test import BASIS, HASH, BINDING, ARGS, RESULT
from swbpipe_projection_v4 import Pending

ENGINE=dict(HASH,value='sha256:'+HASH['value'])
CAT=selected.load_catalog()


class PR40Receiving(unittest.TestCase):
    def test_actual_integrated_identity_and_prior_separation(self):
        pins=selected.selection()
        self.assertEqual(pins['commit'],'cc91aadc9822c5c1d8ba3d883a3ee220dddc1b65')
        self.assertEqual(pins['checked_head'],'57f5028328bfa50b0a525b7186926a9da88979dc')
        self.assertEqual(len(pins['sources']),9)
        self.assertEqual(CAT,prior.load_catalog())
        self.assertNotEqual(selected.PINS_SHA256,prior.PINS_SHA256)
        self.assertEqual(prior.selection()['commit'],'a659523a75dbbf2cdfcccdf8a667b6fb482e10ea')
        with patch.object(selected,'PINS',prior.PINS):
            with self.assertRaisesRegex(ValueError,'selection changed'):selected.load_catalog()

    def test_all_source_guards_and_old_session_substitution(self):
        pins=selected.selection()
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            for s in pins['sources']:
                path=root/s['snapshot'];path.parent.mkdir(parents=True,exist_ok=True)
                path.write_bytes((selected.ROOT/s['snapshot']).read_bytes())
            with patch.object(selected,'ROOT',root):
                selected.load_catalog()
                for s in pins['sources']:
                    path=root/s['snapshot'];raw=path.read_bytes();path.write_bytes(raw+b'\n')
                    with self.subTest(path=s['path']),self.assertRaisesRegex(ValueError,'selected source changed'):selected.load_catalog()
                    path.unlink()
                    with self.assertRaises(FileNotFoundError):selected.load_catalog()
                    path.write_bytes(raw)
                session=next(s for s in pins['sources'] if s['path'].endswith('/embeddedAgentSession.ts'))
                old=next(s for s in prior.selection()['sources'] if s['path']==session['path'])
                (root/session['snapshot']).write_bytes((prior.ROOT/old['snapshot']).read_bytes())
                with self.assertRaisesRegex(ValueError,'selected source changed'):selected.load_catalog()

    def test_strict_forms_correspond_without_normalization_or_rewriting(self):
        engine=copy.deepcopy(ENGINE);catalog=copy.deepcopy(HASH)
        check_hash_pair(engine,catalog)
        self.assertEqual(engine,ENGINE);self.assertEqual(catalog,HASH)
        bad_engine=[HASH['value'],'SHA256:'+HASH['value'],'sha256:'+('A'*64),'sha256:'+('a'*63),
                    'sha256:sha256:'+HASH['value'],' sha256:'+HASH['value'],'sha256:'+HASH['value']+'\n',None,7]
        for value in bad_engine:
            with self.subTest(engine=value),self.assertRaisesRegex(ValueError,'AGENT-ENGINE-HASH-FORM-REFUSED'):
                check_hash_pair(dict(ENGINE,value=value),catalog)
        for value in [ENGINE['value'],'A'*64,'a'*63,'a'*65,' '+HASH['value'],HASH['value']+'\n',None,7]:
            with self.subTest(catalog=value),self.assertRaisesRegex(ValueError,'AGENT-CATALOG-HASH-FORM-REFUSED'):
                check_hash_pair(engine,dict(HASH,value=value))
        for field in ('canonicalization','payload_scope','payload_ref','hash_status','algorithm'):
            altered=dict(HASH);altered[field]='invented different metadata'
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'correspondence'):check_hash_pair(engine,altered)
        with self.assertRaisesRegex(ValueError,'correspondence'):check_hash_pair(engine,dict(HASH,value='b'*64))
        with self.assertRaises(ValueError):check_hash_pair(None,None)

    def test_engine_batch_keeps_its_hash_and_catalog_basis_stays_bare(self):
        check_batch(ENGINE,BASIS,ENGINE['value'],ENGINE)
        for batch,validation in [(HASH['value'],ENGINE),(ENGINE['value'],HASH),('sha256:'+'b'*64,ENGINE)]:
            with self.assertRaisesRegex(ValueError,'batch'):check_batch(ENGINE,BASIS,batch,validation)
        with self.assertRaisesRegex(ValueError,'CATALOG-HASH'):check_batch(ENGINE,dict(BASIS,modelHash=ENGINE),ENGINE['value'],ENGINE)

    def test_computed_for_revision_gate_preserves_other_ownership_checks(self):
        evidence={'generation':2,'live_generation':2,'ui_revision':1,'owner_generation':2,
                  'owner_ui_revision':1,'computed_model_revision':3,'model_revision':3,'engine_hash':ENGINE}
        publication={'generation':2,'revision':3,'hash':ENGINE}
        check_snapshot(publication,evidence) # UI counter1 need not equal model counter3.
        missing=dict(publication);missing.pop('hash')
        with self.assertRaisesRegex(ValueError,'hash evidence missing'):check_snapshot(missing,evidence)
        for field in ('owner_generation','generation','owner_ui_revision','computed_model_revision'):
            stale=copy.deepcopy(evidence);stale[field]+=1
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'stale'):check_snapshot(publication,stale)
            check_snapshot(dict(publication,hash=None),stale)
        with self.assertRaisesRegex(ValueError,'rebound'):
            check_snapshot(dict(publication,revision=True),evidence)
        pending=dict(evidence,engine_hash=None)
        check_snapshot(dict(publication,hash=None),pending)
        with self.assertRaisesRegex(ValueError,'stale'):check_snapshot(publication,pending)
        # Undo before rerender advances live model revision, not the hash owner.
        undo=dict(evidence,model_revision=4)
        check_snapshot({'generation':2,'revision':4,'hash':None},undo)
        with self.assertRaisesRegex(ValueError,'rebound'):check_snapshot(publication,undo)
        for field in ('ui_revision','computed_model_revision'):
            with self.assertRaisesRegex(ValueError,'revision evidence'):check_snapshot(publication,dict(evidence,**{field:True}))

    def test_observed_outcome_solve_and_retained_result_do_not_rebase(self):
        changed_engine=dict(ENGINE,value='sha256:'+'b'*64);changed_catalog=dict(HASH,value='b'*64)
        result=dict(RESULT,status='applied',data={'outcomeModelHash':changed_catalog})
        check_retained_result(BASIS,result,changed_engine)
        with self.assertRaisesRegex(ValueError,'correspondence'):check_retained_result(BASIS,result,ENGINE)
        with self.assertRaisesRegex(ValueError,'rebound'):check_retained_result(BASIS,dict(result,basis=dict(BASIS,modelRevision=3)),changed_engine)
        check_retained_result(BASIS,dict(RESULT,data={'outcomeModelHash':None}),None)
        with self.assertRaisesRegex(ValueError,'fabricated'):check_retained_result(BASIS,result,None)
        evaluated=dict(RESULT,data={'evaluatedModelHash':HASH})
        check_retained_result(BASIS,evaluated,ENGINE)
        # Existing wire joins receive bare hashes; engine form never enters them.
        args=copy.deepcopy(ARGS);args['runHandle']='invented:run'
        binding=dict(BINDING,tool='swbpipe_read_results')
        retained={'basis':BASIS,'handle':'invented:run'}
        later=dict(BASIS,modelRevision=9,modelHash=changed_catalog)
        pending=Pending(CAT,binding,json.dumps(args).encode(),later,retained_record=retained)
        result=dict(RESULT,data={'runHandle':'invented:run','runId':'invented:run-id','evaluatedModelHash':HASH,
            'values':[],'nextCursor':None,'standing':{'route':'invented','health':'not_assessed','checks':['not_run']}})
        proof={'binding':binding,'basis':BASIS,'result':copy.deepcopy(result)}
        self.assertTrue(pending.complete(binding,result,later,retained_record=proof)['result']['success'])
        bad=copy.deepcopy(args);bad['basis']['modelHash']=ENGINE
        with self.assertRaises(ValueError):Pending(CAT,binding,json.dumps(bad).encode(),later,retained_record=retained)

    def test_evaluated_hash_cannot_follow_a_changed_model_or_hide_in_mixed_roles(self):
        changed_engine=dict(ENGINE,value='sha256:'+'b'*64)
        changed_catalog=dict(HASH,value='b'*64)
        for data,engine in [({'evaluatedModelHash':changed_catalog},changed_engine),
                            ({'outcomeModelHash':HASH,'evaluatedModelHash':changed_catalog},ENGINE),
                            ({},ENGINE), (None,ENGINE)]:
            with self.subTest(data=data),self.assertRaises(ValueError):
                check_retained_result(BASIS,dict(RESULT,data=data),engine)
        evaluated=dict(RESULT,data={'evaluatedModelHash':HASH})
        check_retained_result(BASIS,evaluated,ENGINE)
        with self.assertRaisesRegex(ValueError,'correspondence'):
            check_retained_result(BASIS,evaluated,changed_engine)
        # A newly applied model remains a legitimate different outcome.
        check_retained_result(BASIS,dict(RESULT,data={'outcomeModelHash':changed_catalog}),changed_engine)

    def test_inspected_callsites_preserve_actual_boundary_relationships(self):
        pins=selected.selection()
        def source(suffix):return (selected.ROOT/next(s['snapshot'] for s in pins['sources'] if s['path'].endswith(suffix))).read_text()
        session=source('/embeddedAgentSession.ts');workspace=source('/workspaceSession.ts')
        for text in ['modelHash:agentHash(before.hash)','modelHash:agentHash(snap.hash)',
                     'same(catalogHash(call.basis.modelHash),agentHash(live.hash))',
                     'agentHash(standing?.outcomeModelHash)','same(agentHash(receipt.modelHash),catalogHash(call.basis.modelHash))',
                     'evaluatedModelHash:agentHash(receipt.modelHash)','evaluatedModelHash:run.basis.modelHash',
                     'source_model_hash:snap.hash!.value','validateOperationBatch(model,batch,snap.hash)']:
            self.assertIn(text,session)
        self.assertIn('modelHashOwner.current = { generation, revision, modelRevision: counted }',workspace)
        self.assertIn('currentHashOwned && modelHashOwner.current?.modelRevision === modelRevision.current && projectSessionGeneration === projectSessionGenerationRef.current',workspace)


if __name__=='__main__':unittest.main()
