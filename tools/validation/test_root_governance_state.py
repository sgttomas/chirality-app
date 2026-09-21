"""Strict migration state tests. Complete fixture uses real published owner Git refs."""
from pathlib import Path
import csv
import hashlib
import json
import subprocess
import shutil
import pytest
import root_governance_state as g

ROOT=Path(__file__).resolve().parents[2]
def put(root,path,data):
    out=root/path;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data if isinstance(data,bytes) else data.encode());return out

def copy(root,path): return put(root,path,(ROOT/path).read_bytes())
def ref(root,path): return dict(path=path,sha256=g.digest(root/path))
def reseal(root,state,config):
    put(root,'state.json',json.dumps(state));config['governance_state']=ref(root,'state.json')

@pytest.fixture
def complete(tmp_path):
    root=tmp_path/'fixture';root.mkdir()
    # Only exact selected manifest members and source targets; no ignored state.
    for path,base in [(g.SUBJECT,str(Path(g.SUBJECT).parent.parent)),(g.PLAN+'/FINAL_ARTIFACTS.sha256',g.PLAN)]:
        copy(root,path)
        for line in (ROOT/path).read_text().splitlines():
            _,name=line.split('  ',1);copy(root,base+'/'+name)
    targets=list(csv.DictReader((ROOT/g.PLAN/'WRITE_TARGETS.csv').open()))
    dispositions=list(csv.DictReader((ROOT/g.PLAN/'ROOT_53_DISPOSITIONS.csv').open()))
    status=[]
    for r in targets:
        if g.STATUS.fullmatch(r['Target']):
            copy(root,r['ApprovedSource']);put(root,r['Target'],(ROOT/r['ApprovedSource']).read_bytes());status.append(r)
    for r in targets:
        if r['Target'].startswith('projects/chirality-runtime/') and r['Operation']=='COPY_EXACT_APPROVED_PAYLOAD':
            copy(root,r['ApprovedSource']);put(root,r['Target'],(ROOT/r['ApprovedSource']).read_bytes())
    put(root,'authority.md','Exact approved basis '+g.GATE3_COMMIT)
    bindings=[]
    bytarget={r['Target']:r for r in targets}
    for d in dispositions:
        runtime=d['Class']=='T';path=d['Successor']+'/ScopeOfWork.md' if runtime else d['Successor']
        target='chirality-runtime::'+d['SourceID'] if runtime else Path(path).stem
        if runtime:
            source='execution/'+d['SourcePackage']+'/1_Working/'+d['SourceID']+'/ScopeOfWork.md';copy(root,source);put(root,path,(ROOT/source).read_bytes())
        else:
            p=bytarget[path]['ApprovedSource'];copy(root,p);put(root,path,(ROOT/p).read_bytes())
        bindings.append(dict(source_id=d['SourceID'],target=target,**ref(root,path),authority=ref(root,'authority.md'),write_targets=[d['Successor']+'/**' if runtime else path]))
    # Readonly worktree metadata supports genuine git show/reachability checks.
    gitdir=subprocess.check_output(['git','rev-parse','--absolute-git-dir'],cwd=ROOT,text=True).strip()
    put(root,'.git','gitdir: '+gitdir+'\n')
    commit=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip()
    state=dict(schema='root-governance-state/v1',stage='applied_pending_confirmation',selected_subject={'path':g.SUBJECT,'sha256':g.SUBJECT_SHA},propagation_plan={'path':g.PLAN+'/FINAL_ARTIFACTS.sha256','sha256':g.PLAN_SHA},gate5=None,successor_bindings=bindings,transaction={'path':'transaction.json','sha256':None})
    for gate,sha in [('gate3',g.SUBJECT_SHA),('gate4',g.PLAN_SHA)]:
        path='plans/steers/root_runtime_migration_'+gate+'_approval_2026-09-05.md';copy(root,path);state[gate]=dict(**ref(root,path),commit=commit,subject_sha256=sha)
    config={'mode':'governance-only'};reseal(root,state,config)
    return root,state,config,status

def test_complete_real_published_state(complete):
    root,state,config,_=complete;result=g.load_governance_state(root,config)
    assert len(result['source_statuses'])==53 and len(result['held_capabilities'])==9
    assert len(result['governance_ids'])==46 and len(result['runtime_ids'])==7

@pytest.mark.parametrize('mutation',['old_subject','map_edit','source_swap','status_edit','missing_binding','duplicate_binding','wrong_successor','wrong_control_hash','missing_authority','foreign_write','missing_transaction','gate4_as_gate5','wrong_charter'])
def test_adversarial_complete_state(complete,mutation):
    root,state,config,status=complete
    if mutation=='wrong_charter': put(root,'projects/chirality-runtime/docs/PRD.md','Different product charter')
    if mutation=='old_subject': state['selected_subject']['path']=g.SUBJECT.replace('V3','V2')
    if mutation=='map_edit':
        p=root/g.PLAN/'SCOPE_104_SUCCESSOR_MAP.csv';p.write_text(p.read_text().replace('SOW-047','SOW-999',1))
    if mutation=='source_swap':
        p=root/g.PLAN/'ROOT_6_PACKAGE_CLOSURE.csv';p.write_text(p.read_text().replace('DEL-01-01','DEL-01-02',1))
    if mutation=='status_edit': put(root,status[0]['Target'],'**Current State:** IN_PROGRESS\n')
    if mutation=='missing_binding': state['successor_bindings'].pop()
    if mutation=='duplicate_binding': state['successor_bindings'][1]=state['successor_bindings'][0]
    if mutation=='wrong_successor': state['successor_bindings'][0]['target']='GOV-99-99'
    if mutation=='wrong_control_hash': state['successor_bindings'][0]['sha256']='0'*64
    if mutation=='missing_authority': state['successor_bindings'][0]['authority']['path']='absent'
    if mutation=='foreign_write': state['successor_bindings'][0]['write_targets']=['projects/pec/**']
    if mutation=='missing_transaction': state['transaction']=None
    if mutation=='gate4_as_gate5': state.update(stage='effective',gate5=state['gate4'],effect_subject_sha256=g.PLAN_SHA)
    reseal(root,state,config)
    with pytest.raises(g.GovernanceError):g.load_governance_state(root,config)

def test_prepared_exact_population_not_mixed(complete):
    root,state,config,status=complete;state['stage']='prepared';state['transaction']=None
    for row in status:
        original=subprocess.check_output(['git','show','8209bc54e0d133b19437c93b184cd50ba3d43489:'+row['Target']],cwd=ROOT)
        put(root,row['Target'],original)
    reseal(root,state,config);assert g.status_verification(root,config)=='preimage'
    g.load_governance_state(root,config,verify_statuses='preimage')
    put(root,status[0]['Target'],(ROOT/status[0]['ApprovedSource']).read_bytes())
    with pytest.raises(g.GovernanceError):g.load_governance_state(root,config,verify_statuses='preimage')

@pytest.mark.parametrize('value',['../escape','/outside','x/../escape','x/**','x\\escape'])
def test_path_refusals(tmp_path,value):
    with pytest.raises(g.GovernanceError):g.safe_path(tmp_path,value,True)

def test_existing_ancestor_symlink_rejects_nonexistent_child(tmp_path):
    (tmp_path/'other').mkdir();(tmp_path/'alias').symlink_to(tmp_path/'other',target_is_directory=True)
    with pytest.raises(g.GovernanceError):g.safe_path(tmp_path,'alias/missing/file',True)

@pytest.mark.parametrize('value',['unknown','',False])
def test_unknown_mode(value):
    with pytest.raises(g.GovernanceError):g.check_mode({'mode':value})

def test_no_implicit_historical_mode():
    with pytest.raises(g.GovernanceError):g.check_mode({'governance_state':{}})

def test_effective_transition_cannot_change_confirmed_runtime_contract(complete):
    import copy
    _,prepared,_,_=complete
    effective=copy.deepcopy(prepared);effective.update(stage='effective',gate5={'actual':'later owner record'},transaction={'path':'completed journal'})
    g.compare_confirmed_state(effective,prepared)
    runtime=next(b for b in effective['successor_bindings'] if b['target'].startswith('chirality-runtime::'))
    runtime['sha256']='0'*64
    with pytest.raises(g.GovernanceError,match='successor_bindings'):g.compare_confirmed_state(effective,prepared)
