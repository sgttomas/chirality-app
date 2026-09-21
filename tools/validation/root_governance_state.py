"""Strict, migration-specific Root state. Owner records remain semantic authority.

No fixture-authority flag exists. The selected immutable migration subjects are
pinned deliberately; another migration requires a separately reviewed change.
"""
from __future__ import annotations
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath

PLAN = 'execution/_ScopeChange/SCA-005_2026-09-06_GATE4_PLAN'
SUBJECT = 'execution/_ScopeChange/SCA-005_2026-09-05_2344/FINAL_INTEGRATION_V3/COMBINED_ARTIFACTS.sha256'
SUBJECT_SHA = '547d1f3369e71aa96d1b61561f6b1603b978016c7335fca39f86df97ddd73fc3'
PLAN_SHA = '917656f3a828d7e05e2feaf22e14394f1f6dc9fbb26bb99760b633e0ceb17efd'
GATE3_COMMIT = '1aadcc61b2739fdca25c4b07259655836516baa4'
MODE = 'governance-only'
SHA = re.compile(r'^[0-9a-f]{64}$')
STATUS = re.compile(r'^execution/(PKG-[^/]+)/1_Working/(DEL-[^/]+)/_STATUS\.md$')

class GovernanceError(ValueError):
    """Fail-closed invalid governance evidence or path."""

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def safe_path(root: Path, relative: str, allow_missing: bool = False) -> Path:
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise GovernanceError('path must be a nonempty POSIX repository-relative path')
    p = PurePosixPath(relative)
    if p.is_absolute() or any(x in {'.','..'} for x in relative.split('/')):
        raise GovernanceError('absolute or traversal path rejected')
    if any(c in relative for c in '*?['):
        raise GovernanceError('file path cannot contain glob syntax')
    base = root.resolve(); out = base.joinpath(*p.parts)
    try:
        out.resolve().relative_to(base)
    except ValueError as exc:
        raise GovernanceError('path escapes canonical checkout') from exc
    # A symlink inside the checkout can still select a sibling project.
    cursor = base
    for part in p.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise GovernanceError('symlink in governed path')
    if not allow_missing and not out.is_file():
        raise GovernanceError('governed file is absent: '+relative)
    return out

def reference(root: Path, ref: dict) -> Path:
    if not isinstance(ref, dict) or not SHA.fullmatch(str(ref.get('sha256',''))):
        raise GovernanceError('reference requires exact SHA256')
    p = safe_path(root, ref.get('path'))
    if digest(p) != ref['sha256']:
        raise GovernanceError('reference hash mismatch: '+ref['path'])
    return p

def verify_owner_act(root: Path, ref: dict, expected_subject_sha: str) -> None:
    p = reference(root, ref)
    commit = ref.get('commit','')
    if not re.fullmatch(r'[0-9a-f]{40}', str(commit)):
        raise GovernanceError('owner record requires full published commit')
    if not SHA.fullmatch(str(expected_subject_sha)) or ref.get('subject_sha256') != expected_subject_sha:
        raise GovernanceError('owner record subject mismatch')
    def git(*args):
        return subprocess.run(['git','-C',str(root),*args],capture_output=True,check=False)
    if git('merge-base','--is-ancestor',commit,'origin/main').returncode:
        raise GovernanceError('owner record commit is not published on origin/main')
    stored = git('show',f'{commit}:{ref["path"]}')
    if stored.returncode or stored.stdout != p.read_bytes():
        raise GovernanceError('owner record differs from published record')
    if expected_subject_sha not in stored.stdout.decode('utf-8',errors='strict'):
        raise GovernanceError('published owner record does not identify expected subject')

def check_mode(config: dict) -> bool:
    mode = config.get('mode')
    if mode is None:
        if 'governance_state' in config or config.get('parser_dialect') == 'root-historical-v1':
            raise GovernanceError('governance shape requires explicit mode')
        return False
    if mode != MODE:
        raise GovernanceError('unknown Root mode')
    return True

def _csv(root: Path, path: str) -> list[dict]:
    return list(csv.DictReader(safe_path(root,path).open(encoding='utf-8',newline='')))

def _verify_manifest(root: Path, ref: dict, expected_path: str, expected_sha: str) -> None:
    if ref != {'path':expected_path,'sha256':expected_sha}:
        raise GovernanceError('unselected immutable subject')
    p = reference(root,ref)
    # Manifest members resolve beside the manifest except combined V3's
    # explicitly repository-relative member names (its accepted serialization).
    for line in p.read_text().splitlines():
        if not line.strip():
            continue
        try: expected, name = line.split('  ',1)
        except ValueError as exc: raise GovernanceError('malformed subject manifest') from exc
        if expected_path == SUBJECT:
            rel = name if name.startswith(('execution/','docs/','projects/','plans/')) else str(p.parent.parent.relative_to(root)/name)
        else:
            rel = str(p.parent.relative_to(root)/name)
        member = safe_path(root, rel)
        if digest(member) != expected:
            raise GovernanceError('immutable selected member mismatch: '+rel)

def _target_prefix(root: Path, target: str) -> str:
    if not isinstance(target,str): raise GovernanceError('write target must be string')
    bare=target[:-3] if target.endswith('/**') else target
    safe_path(root,bare,allow_missing=True)
    return bare

def _allowed_target(target: str, allowed: set[str]) -> bool:
    for base in allowed:
        if target == base: return True
        if base.endswith('/**') and target.startswith(base[:-3]+'/'): return True
    return False

def compare_confirmed_state(state: dict, confirmed: dict) -> None:
    for key in ['selected_subject','propagation_plan','gate3','gate4','successor_bindings']:
        if state.get(key)!=confirmed.get(key):
            raise GovernanceError('effective state changed confirmed '+key)

def load_governance_state(root: Path, config: dict, require_effective: bool = False,
                          verify_statuses: str = 'postimage') -> dict:
    root = root.resolve()
    if not check_mode(config): raise GovernanceError('explicit governance mode required')
    path = reference(root, config.get('governance_state'))
    try: state=json.loads(path.read_text())
    except (ValueError,OSError) as exc: raise GovernanceError('invalid governance state JSON') from exc
    if not isinstance(state,dict) or state.get('schema')!='root-governance-state/v1':
        raise GovernanceError('unknown governance state schema')
    if state.get('stage') not in {'prepared','applied_pending_confirmation','effective'}:
        raise GovernanceError('unknown governance application stage')
    _verify_manifest(root,state.get('selected_subject'),SUBJECT,SUBJECT_SHA)
    _verify_manifest(root,state.get('propagation_plan'),PLAN+'/FINAL_ARTIFACTS.sha256',PLAN_SHA)
    for gate,sha in [('gate3',SUBJECT_SHA),('gate4',PLAN_SHA)]:
        if state.get(gate,{}).get('path') != 'plans/steers/root_runtime_migration_'+gate+'_approval_2026-09-05.md':
            raise GovernanceError('wrong owning approval record')
        verify_owner_act(root,state[gate],sha)
    if state['stage']=='effective':
        effect=state.get('gate5')
        if not isinstance(effect,dict) or not re.fullmatch(r'plans/steers/root_runtime_migration_gate5_confirmation_\d{4}-\d{2}-\d{2}\.md',str(effect.get('path',''))):
            raise GovernanceError('effective state requires a distinct Gate5 confirmation record')
        verify_owner_act(root,effect,state.get('effect_subject_sha256'))
    elif state.get('gate5') is not None:
        raise GovernanceError('unconfirmed stage cannot claim Gate5 act')
    if require_effective and state['stage']!='effective':
        raise GovernanceError('effective Gate5 confirmation required for production dispatch')
    dispositions=_csv(root,PLAN+'/ROOT_53_DISPOSITIONS.csv')
    parents=_csv(root,PLAN+'/ROOT_6_PACKAGE_CLOSURE.csv')
    scopes=_csv(root,PLAN+'/SCOPE_104_SUCCESSOR_MAP.csv')
    targets=_csv(root,PLAN+'/WRITE_TARGETS.csv')
    source_ids={x['SourceID'] for x in dispositions}
    if len(dispositions)!=53 or len(source_ids)!=53 or len(parents)!=6:
        raise GovernanceError('source identity census mismatch')
    if {x['SourceScopeID'] for x in scopes}!={f'SOW-{i:03}' for i in range(1,105)} or len(scopes)!=104:
        raise GovernanceError('scope identity census mismatch')
    seen=set()
    for parent in parents:
        children=set(parent['Children'].split(';'))
        actual={x['SourceID'] for x in dispositions if x['SourcePackage']==parent['SourcePackage']}
        if children!=actual or len(children)!=int(parent['ChildCount']) or children & seen:
            raise GovernanceError('exact parent/child identity mismatch')
        seen |= children
    if seen!=source_ids: raise GovernanceError('orphan source identity')
    status_rows=[]
    for r in targets:
        match=STATUS.fullmatch(r['Target'])
        if match:
            source=next((d for d in dispositions if d['SourceID']==match[2]),None)
            if not source or source['SourcePackage']!=match[1]: raise GovernanceError('source target identity mismatch')
            reference(root,{'path':r['ApprovedSource'],'sha256':r['ApprovedSHA256']})
            status_rows.append(dict(path=r['Target'],source_id=match[2],source_package=match[1],
                preimage_sha256=r['CurrentSHA256'],postimage_sha256=r['ApprovedSHA256'],
                postimage_path=r['ApprovedSource'],successor=source['Successor']))
    if len(status_rows)!=53 or {r['source_id'] for r in status_rows}!=source_ids:
        raise GovernanceError('status allowlist mismatch')
    if verify_statuses not in {'preimage','postimage','either'}: raise GovernanceError('unknown status verification mode')
    for row in status_rows:
        actual=digest(safe_path(root,row['path']))
        choices={row['preimage_sha256'],row['postimage_sha256']} if verify_statuses=='either' else {row[verify_statuses+'_sha256']}
        if actual not in choices: raise GovernanceError('source status hash mismatch: '+row['path'])
    bindings=state.get('successor_bindings')
    if not isinstance(bindings,list) or len(bindings)!=53: raise GovernanceError('exact53 successor bindings required')
    by_source={b.get('source_id'):b for b in bindings if isinstance(b,dict)}
    if len(by_source)!=53 or set(by_source)!=source_ids: raise GovernanceError('successor binding identity mismatch')
    runtime_authorities={'projects/chirality-runtime/docs/PRD.md'} | {
        'projects/chirality-runtime/execution/_Decomposition/'+name for name in [
            'Chirality_Runtime_SOFTWARE_DECOMP_v1_0.md','RUNTIME_DELIVERABLE_REGISTER.csv',
            'RUNTIME_OBJECTIVE_REGISTER.csv','RUNTIME_SCOPE_LEDGER.csv']}
    runtime_baseline = {}
    for required in runtime_authorities:
        pin=next((r for r in targets if r['Target']==required),None)
        if not pin or not pin['ApprovedSHA256']: raise GovernanceError('runtime authority missing approved binding')
        # The migration postimage stays historical truth; current owning
        # revisions are checked separately through exact Root adoption.
        reference(root,{'path':pin['ApprovedSource'],'sha256':pin['ApprovedSHA256']})
        runtime_baseline[required] = pin['ApprovedSHA256']
    approved_targets={r['Target']:r for r in targets}
    gov_allowed={r['Target'] for r in targets if not r['Target'].startswith('projects/') and not STATUS.fullmatch(r['Target'])}
    guard_inventory=_csv(root,PLAN+'/GUARDS/WRITE_PATH_INVENTORY.csv')
    gov_allowed|={r['Path'] for r in guard_inventory if r['IntegrationOwner']!='none' and not r['Path'].startswith('projects/')}
    successors=[];gov_ids=[];runtime_ids=[]
    for source in dispositions:
        binding=by_source[source['SourceID']];runtime=source['Class']=='T'
        target=('chirality-runtime::'+source['SourceID']) if runtime else Path(source['Successor']).stem
        wanted_path=source['Successor']+'/ScopeOfWork.md' if runtime else source['Successor']
        if binding.get('target')!=target or binding.get('path')!=wanted_path:
            raise GovernanceError('wrong successor path or qualified identity')
        if runtime:
            runtime_baseline[wanted_path] = binding['sha256']
            if state['stage'] == 'effective':
                historical = subprocess.run(['git','-C',str(root),'show',
                    state['gate5']['commit']+':'+wanted_path], capture_output=True, check=False)
                safe_path(root, wanted_path)
                if historical.returncode or hashlib.sha256(historical.stdout).hexdigest() != binding['sha256']:
                    raise GovernanceError('historical Runtime successor mismatch: '+wanted_path)
            else:
                reference(root, binding)
        else:
            reference(root,binding)
        if not runtime:
            approved=approved_targets.get(wanted_path)
            if not approved or approved['ApprovedSHA256']!=binding['sha256']:
                raise GovernanceError('governance control not exact approved subject')
        authority=reference(root,binding.get('authority'))
        if GATE3_COMMIT not in authority.read_text(): raise GovernanceError('successor authority lacks accepted Gate3 basis')
        allowed={source['Successor']+'/**'} if runtime else gov_allowed|{source['Successor'],'execution/_Coordination/GovernanceControls/evidence/'+target+'/**'}
        writes=binding.get('write_targets')
        if not isinstance(writes,list) or not writes: raise GovernanceError('successor requires declared write targets')
        for value in writes:
            _target_prefix(root,value)
            if not _allowed_target(value,allowed): raise GovernanceError('successor write target outside approved migration scope')
            if not runtime and (value.startswith('projects/') or any(value.startswith(str(Path(r['path']).parent)) for r in status_rows)):
                raise GovernanceError('Root governance grant enters product/historical source')
        item=dict(binding);item['project']='chirality-runtime' if runtime else 'root';item['kind']='runtime-carrier' if runtime else 'governance-control';successors.append(item)
        (runtime_ids if runtime else gov_ids).append(target)
    if len(gov_ids)!=46 or len(runtime_ids)!=7 or len(set(gov_ids+runtime_ids))!=53:
        raise GovernanceError('successor partition mismatch')
    from root_runtime_successors import recognize
    runtime_recognition = recognize(root, runtime_baseline)
    transaction=state.get('transaction')
    if state['stage'] in {'applied_pending_confirmation','effective'} and transaction is None:
        raise GovernanceError('applied state requires transaction reference')
    if transaction is not None:
        if not isinstance(transaction,dict): raise GovernanceError('invalid transaction reference')
        journal=safe_path(root,transaction.get('path'),allow_missing=True)
        if journal.exists():
            if transaction.get('sha256') is not None: reference(root,transaction)
            try: payload=json.loads(journal.read_text())
            except ValueError as exc: raise GovernanceError('invalid transaction journal') from exc
            if (require_effective or state['stage']=='effective') and payload.get('state') != 'APPLIED':
                raise GovernanceError('incomplete transaction blocks production dispatch')
        elif require_effective or state['stage']=='effective':
            raise GovernanceError('transaction journal absent')
    if state['stage']=='effective':
        if not SHA.fullmatch(str(transaction.get('sha256',''))): raise GovernanceError('effective state requires immutable completed journal hash')
        effect_subject=reference(root,state.get('effect_subject'))
        if digest(effect_subject)!=state.get('effect_subject_sha256') or payload.get('subject_sha256')!=state['effect_subject_sha256']:
            raise GovernanceError('Gate5 subject does not match completed application journal')
        try: application=json.loads(effect_subject.read_text())
        except ValueError as exc: raise GovernanceError('invalid confirmed application subject') from exc
        if application.get('schema')!='root-retirement-application/v1': raise GovernanceError('wrong confirmed application kind')
        prepared=reference(root,application.get('governance_state'))
        try: confirmed=json.loads(prepared.read_text())
        except ValueError as exc: raise GovernanceError('invalid confirmed prepared state') from exc
        compare_confirmed_state(state,confirmed)
        tested=application.get('tested_files',[])
        if not isinstance(tested,list) or not tested: raise GovernanceError('confirmed application lacks tested implementation')
        configs={f'execution/_harness/{name}.yaml' for name in ['root_guards','adapter','surface_ownership','work_graph']}
        snapshots=state.get('effect_configuration',[])
        by_target={r.get('target'):r for r in snapshots if isinstance(r,dict)}
        if set(by_target)!=configs or len(snapshots)!=4: raise GovernanceError('effective configuration transform requires exact four snapshots')
        import yaml
        for item in tested:
            if item.get('path') not in configs:
                if item.get('path', '').startswith('tools/'):
                    # Gate5 tested implementation is historical proof, not a
                    # perpetual lock on later owner-authorized M2 tool work.
                    historical = subprocess.run(['git','-C',str(root),'show',
                        state['gate5']['commit']+':'+item['path']], capture_output=True, check=False)
                    safe_path(root, item['path'])
                    if historical.returncode or hashlib.sha256(historical.stdout).hexdigest() != item['sha256']:
                        raise GovernanceError('historical tested implementation mismatch: '+item['path'])
                else:
                    reference(root,item)
                continue
            original=reference(root,by_target[item['path']])
            if digest(original)!=item.get('sha256'): raise GovernanceError('configuration snapshot differs from tested bytes')
            before=yaml.safe_load(original.read_text());after=yaml.safe_load(safe_path(root,item['path']).read_text())
            if not isinstance(before,dict) or not isinstance(after,dict): raise GovernanceError('invalid confirmed configuration')
            before_state=json.loads(reference(root,before.get('governance_state')).read_text())
            for key in ['selected_subject','propagation_plan','gate3','gate4','successor_bindings']:
                if before_state.get(key)!=confirmed.get(key): raise GovernanceError('tested configuration changed accepted intent')
            before.pop('governance_state',None);after.pop('governance_state',None)
            if before!=after: raise GovernanceError('effective configuration changed confirmed intent')
        entries=payload.get('entries',[])
        expected={(r['path'],r['preimage_sha256'],r['postimage_sha256']) for r in status_rows}
        actual={(r.get('path'),r.get('preimage_sha256'),r.get('postimage_sha256')) for r in entries if isinstance(r,dict)}
        if len(entries)!=53 or actual!=expected: raise GovernanceError('effective journal does not bind exact53 applied entries')
        if payload.get('blocked') or payload.get('state')!='APPLIED': raise GovernanceError('effective journal incomplete')
        act=reference(root,state['gate5']).read_text()
        if transaction['sha256'] not in act: raise GovernanceError('Gate5 record does not bind completed journal')
    holds=_csv(root,PLAN+'/HOLD_SUCCESSOR_MAP.csv')
    held=[h['SourceJSONPointer'] for h in holds if h['CurrentDisposition']=='HELD_UNAVAILABLE']
    if len(held)!=9: raise GovernanceError('approved nine-hold partition mismatch')
    return dict(state,held_capabilities=held,source_statuses=status_rows,source_ids=sorted(source_ids),governance_ids=gov_ids,
                runtime_ids=runtime_ids,successors=successors, runtime_successor_recognition=runtime_recognition)


def status_verification(root: Path, config: dict) -> str:
    """Select the one exact status population appropriate to a sealed stage."""
    p=reference(root,config.get('governance_state'))
    try: stage=json.loads(p.read_text()).get('stage')
    except (ValueError,AttributeError) as exc: raise GovernanceError('invalid state stage') from exc
    if stage=='prepared': return 'preimage'
    if stage in {'applied_pending_confirmation','effective'}: return 'postimage'
    raise GovernanceError('unknown governance stage')
