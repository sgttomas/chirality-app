"""Synthetic examples only. Runs entirely offline without supplier/native execution."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from jsonschema import Draft202012Validator, ValidationError
import model


def fixtures(directory):
    def put(name, value):
        raw = (json.dumps(value,indent=2)+'\n').encode()
        (directory/name).write_bytes(raw)
        return {'path':name,'sha256':hashlib.sha256(raw).hexdigest()}
    evidence=put('synthetic-evidence.json',{'standing':'synthetic; no actual observation, review or adoption'})
    entries=[{'path':p,'kind':'dir','mode':493} for p in ['.','bin','codex-path','codex-resources']]
    entries += [{'path':p,'kind':'file','mode':493 if p=='bin/codex' else 420,'size':1,'sha256':hashlib.sha256(p.encode()).hexdigest()} for p in ['bin/codex','codex-package.json']]
    inv={'method':'codex-vendor-tree-v1','algorithm':'sha-256','entries':entries,'manifest_sha256':model.inventory.manifest(entries)}
    launcher={'kind':'direct-vendor','relative_executable':'bin/codex','path_prefix_relative':'codex-path','removed_wrapper_variables':['CODEX_MANAGED_PACKAGE_ROOT','CODEX_MANAGED_BY_NPM']}
    gen={'pin':'9.9.9','kind':'json-schema','variant':'experimental','formatter_policy':'synthetic fixed policy','manifest_sha256':'1'*64,'provenance':evidence,'version_advance':evidence}
    expected={'format':'expected-reference.s1','method':'codex-vendor-tree-v1','pin':'9.9.9','platform':'macOS arm64','archive':{'official_source_locator':'synthetic-archive','sha256':'2'*64,'acquisition_authorization':evidence,'custody':evidence,'extraction_procedure':evidence,'source_subtree':'vendor/synthetic'},'inventory':inv,'launcher':launcher,'generated':gen,'label_evidence':evidence,'generation_correspondence':evidence,'author':'synthetic author'}
    er=put('expected.json',expected)
    att={'format':'adoption-attestation.s1','expected_reference':er,'author':'synthetic author','independent_reviewer':'synthetic reviewer','reviewed_revision':'synthetic revision','review_evidence':evidence,'adoption':{'actor':'synthetic implementation owner','through_help_human':evidence,'decision':'adopt-for-supplier-reference','evidence':evidence},'limits':['Synthetic demonstration; never a qualified reference.']}
    ar=put('attestation.json',att)
    observed={'format':'observed-verification.s1','expected_reference':er,'adoption_attestation':ar,'pin':'9.9.9','platform':'macOS arm64','observed_label':'9.9.9','raw_version_label':'codex-cli 9.9.9','candidate_subject':{'app_revision':'ILLUSTRATIVE','build_identity':'ILLUSTRATIVE','package_record_id':'PKG-EX-01','installer_sha256_before_notarisation':'0'*64},'generated':gen,'inventory':inv,'launcher':launcher,'configuration':{'resolved_root':'/synthetic/vendor','resolved_executable':'/synthetic/vendor/bin/codex','working_directory':'/synthetic','argv':['app-server'],'path_prefix':'/synthetic/vendor/codex-path','path_remainder_provenance':'synthetic inherited PATH; value omitted','app_supplied_nonsecret':{},'removed_environment_names':launcher['removed_wrapper_variables'],'probe_home':'synthetic probe','account_home':'synthetic account','home_link_states':'synthetic isolated','k12_flags':['synthetic flag'],'secret_redactions':[]},'generation':{'appSession':'synthetic session','home':'synthetic account','spawnCounter':1},'at':'synthetic time','phase':'pre-spawn','checks':{k:{'outcome':'pass','evidence':evidence,'reason':'synthetic test input'} for k in ['tree','label','generated','custody','reference']},'outcome':'verified','limits':['Synthetic claims only; stable trusted custody and residual check-to-exec race must be evidenced in implementation.']}
    oref=put('observed.json',observed)
    life={'format':'lifecycle-event.s1','legacy_event':{'recordKind':'lifecycle-event','sequence':1,'transitionId':'LT-04','generation':observed['generation'],'fromState':'verifying','event':'verification-passed','toState':'spawning','at':'synthetic time','verificationResult':{'result':'verified'}},'verification_artifact':oref,'verification_generation':copy.deepcopy(observed['generation'])}
    put('lifecycle.json',life)
    source=next((model.ROOT/'projects/chirality-app-v4/execution').glob('PKG-01*/DEL-01-06*/Design/pkg.identity-record.valid.examples.json'))
    old=json.loads(source.read_text())[0]
    old['codex']['pin']='9.9.9'
    old['codex']['executables']=old['codex']['executables'][:1]
    for key in ['sha256_published','sha256_packaged']: old['codex']['executables'][0][key]=entries[4]['sha256']
    for key in ['published','packaged']: old['codex'][key]={'manifest_sha256':inv['manifest_sha256'],'files':2,'macho_files':1}
    iref=put('inventory.json',{'format':'inventory-artifact.s1','inventory':inv})
    pkg={'format':'pkg-identity.s1','distribution_status':'reference-equal','legacy_package':old,'expected_reference':er,'adoption_attestation':ar,'published_inventory':iref,'packaged_inventory':iref,'verification_artifact':oref,'mach_o_paths':['bin/codex']}
    put('package.json',pkg)
    return observed,life,pkg,ar['sha256'],put

class Cases(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.directory=Path(self.tmp.name)
        self.o,self.l,self.p,self.trust,self.put=fixtures(self.directory)
    def tearDown(self): self.tmp.cleanup()
    def test_all_schemas_and_positive_join(self):
        for p in model.HERE.glob('*.schema.json'): Draft202012Validator.check_schema(json.loads(p.read_text()))
        self.assertEqual(model.observed(self.o,self.directory,self.trust),'verified')
        self.assertEqual(model.lifecycle(self.l,self.directory,self.trust),'verified')
        self.assertEqual('reference-equal',model.package(self.p,self.directory,self.trust))
    def test_package_pending_and_candidate_join(self):
        self.p['verification_artifact']=None
        self.assertEqual(model.package(self.p,self.directory,self.trust),'reference-equal')
        self.p['expected_reference']=None;self.p['adoption_attestation']=None;self.p['distribution_status']='unverifiable'
        self.assertEqual(model.package(self.p,self.directory,None),'unverifiable')
        self.o['candidate_subject']['build_identity']='other'
        self.p['verification_artifact']=self.put('observed.json',self.o)
        with self.assertRaises(ValueError):model.package(self.p,self.directory,self.trust)
    def test_lt24_requires_pre_spawn(self):
        self.o['expected_reference']=None;self.o['adoption_attestation']=None;self.o['outcome']='unverifiable'
        self.l['legacy_event'].update(transitionId='LT-24',event='development-start-authorized',supplierStanding='unverified-development',reason='U-06 development run: unverified distribution, not the pinned supplier',verificationResult={'result':'unverifiable','reason':'fixture'})
        self.l['verification_artifact']=self.put('observed.json',self.o)
        self.assertEqual(model.lifecycle(self.l,self.directory,self.trust),'unverifiable')
        self.o['phase']='pre-probe'
        self.l['verification_artifact']=self.put('observed.json',self.o)
        with self.assertRaises(ValueError):model.lifecycle(self.l,self.directory,self.trust)
    def test_lt24_missing_label(self):
        self.o['raw_version_label']=None;self.o['observed_label']=None;self.o['outcome']='unverifiable'
        self.l['verification_artifact']=self.put('observed.json',self.o)
        self.l['legacy_event'].update(transitionId='LT-24',event='development-start-authorized',supplierStanding='unverified-development',reason='U-06 development run: unverified distribution, not the pinned supplier',verificationResult={'result':'unverifiable','reason':'fixture'})
        with self.assertRaises(ValueError):model.lifecycle(self.l,self.directory,self.trust)
    def test_early_event_and_transition_table(self):
        self.l['verification_artifact']=None
        self.l['verification_generation']=None
        self.l['legacy_event'].update(transitionId='LT-01',fromState='absent',event='start-requested',toState='verifying',generation=None)
        del self.l['legacy_event']['verificationResult']
        self.assertEqual(model.lifecycle(self.l,self.directory,self.trust),'verification-not-yet-available')
        self.l['legacy_event']['fromState']='ready'
        with self.assertRaises(ValueError):model.lifecycle(self.l,self.directory,self.trust)
    def test_exact_bytes(self):
        p=self.directory/'expected.json';p.write_bytes(p.read_bytes()+b' ')
        with self.assertRaises(ValueError): model.observed(self.o,self.directory,self.trust)
    def test_unselected_attestation(self):
        with self.assertRaises(ValueError): model.observed(self.o,self.directory,'0'*64)
    def test_missing_and_known_mismatch_precedence(self):
        self.o['expected_reference']=None;self.o['adoption_attestation']=None;self.o['outcome']='unverifiable'
        self.assertEqual(model.observed(self.o,self.directory,None),'unverifiable')
        self.o['observed_label']='9.9.8';self.o['outcome']='mismatch'
        self.assertEqual(model.observed(self.o,self.directory,None),'mismatch')
    def test_lt24_cannot_waive_mismatch(self):
        self.o['observed_label']='9.9.8';self.o['outcome']='mismatch'
        self.l['verification_artifact']=self.put('observed.json',self.o)
        self.l['legacy_event'].update(transitionId='LT-24',event='development-start-authorized',supplierStanding='unverified-development',reason='U-06 development run: unverified distribution, not the pinned supplier',verificationResult={'result':'unverifiable','reason':'fixture'})
        with self.assertRaises(ValueError): model.lifecycle(self.l,self.directory,self.trust)
    def test_tree_mode_and_generated_mutations(self):
        for mutate in [lambda o:o['inventory']['entries'][0].update(mode=448),lambda o:o['generated'].update(formatter_policy='different'),lambda o:o['generated'].update(pin='9.9.8')]:
            o=copy.deepcopy(self.o);mutate(o)
            with self.assertRaises(ValueError): model.observed(o,self.directory,self.trust)
    def test_package_full_tree_and_old_rules(self):
        inv=copy.deepcopy(self.o['inventory']);inv['entries'][0]['mode']=448
        self.p['packaged_inventory']=self.put('changed.json',{'format':'inventory-artifact.s1','inventory':inv})
        with self.assertRaises(ValueError): model.package(self.p,self.directory,self.trust)
        self.p['packaged_inventory']=self.p['published_inventory']
        self.p['legacy_package']['codex']['executables'][0]['signature']['timestamp']=False
        with self.assertRaisesRegex(ValueError,'PK-R1'):model.package(self.p,self.directory,self.trust)
    def test_generation_and_schema_versions(self):
        self.l['legacy_event']['generation']['spawnCounter']=2
        with self.assertRaises(ValueError):model.lifecycle(self.l,self.directory,self.trust)
        self.o['format']='observed-verification.future'
        with self.assertRaises(ValidationError):model.observed(self.o,self.directory,self.trust)
    def test_no_caller_qualified_flag(self):
        self.o['qualified']=True
        with self.assertRaises(ValidationError):model.observed(self.o,self.directory,self.trust)

if __name__=='__main__': unittest.main(verbosity=2)
