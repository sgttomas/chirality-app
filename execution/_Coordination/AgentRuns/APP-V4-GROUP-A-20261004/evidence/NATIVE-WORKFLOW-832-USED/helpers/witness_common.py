"""Private witness evidence validators; importing performs no execution."""
import hashlib,json,pathlib,stat,re
APPROVED_SUPPLIER_MANIFEST_SHA256='04898a5adac06aecba185c2e313b4758292c2c20c24e3da441da2b6fd617791e'
GENERATED_SCHEMA_PATHS={f'src-tauri/gen/schemas/{name}.json' for name in ('acl-manifests','capabilities','macOS-schema','desktop-schema')}
TEST='runtime_session::parent_stock_workflow_witness::parent_only_stock_workflow_roundtrip'
def require(ok,message):
    if not ok: raise ValueError(message)
def sha(path): return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
def save(path,value): pathlib.Path(path).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def manifest(base,exclude=()):
    base=pathlib.Path(base); result={}
    for p in sorted(base.rglob('*')):
        relative=p.relative_to(base)
        if set(relative.parts)&set(exclude): continue
        require(not p.is_symlink(),'symlink refused: '+str(p))
        if p.is_file(): result[str(relative)]={'sha256':sha(p),'bytes':p.stat().st_size,'mode':oct(stat.S_IMODE(p.stat().st_mode))}
    return result
def validate_result(root,binding,code,output):
    require(code==0,'test failed or timed out')
    require(re.search(r'^running 1 test$',output,re.M) is not None,'not exactly one test run')
    require(re.search(r'^test result: ok\. 1 passed; 0 failed; 0 ignored;',output,re.M) is not None,'missing one-pass libtest result')
    report=json.loads((root/'witness-result.json').read_text())
    require(report.get('invocation')==binding,'result not bound to this unique invocation')
    require(report.get('adoption')=='unknown','unwarranted adoption')
    require(report.get('supply',{}).get('comparison',{}).get('state') in ('equal_claimed_text','text_differs_workflow_bytes_equal'),'source comparison absent')
    require(report.get('thread') and report.get('turn'),'missing native identities')
    turns=report.get('nativeFailedTurn',[])
    terminal=next((t.get('nativeTurn') for t in turns if t.get('threadId')==report['thread'] and t.get('turnId')==report['turn'] and t.get('generation')==report.get('sourceGeneration')),None)
    require(terminal and terminal.get('status')=='failed','matching native failed terminal absent')
    observations=[]
    if (root/'provider-observations.jsonl').exists(): observations=[json.loads(line) for line in (root/'provider-observations.jsonl').read_text().splitlines()]
    marker=binding['providerMarker']
    native_error=json.dumps(terminal.get('error'),sort_keys=True)
    causal=any(o.get('responseSent') is True and o.get('status')==400 and o.get('marker')==marker for o in observations) and marker in native_error
    return {'standing':'native failed-turn source comparison; cause '+('owned loopback HTTP400 evidenced' if causal else 'unknown'),'http400CauseEstablished':causal,'nativeError':terminal.get('error'),'providerObservations':observations}
def validate_supplier(path,approved_sha):
    path=pathlib.Path(path);require(approved_sha==APPROVED_SUPPLIER_MANIFEST_SHA256,'not the previously approved complete package record');require(sha(path)==approved_sha,'approved supplier manifest changed');r=json.loads(path.read_text());base=pathlib.Path(r['installRoot']).resolve()
    wanted={x['path']:{k:x[k] for k in ('sha256','bytes','mode')} for x in r['files']}
    require(len(wanted)==44,'not approved complete 44-file package')
    require(manifest(base)==wanted,'complete supplier package differs from approved manifest')
    binary=pathlib.Path(r['entrypoint']).resolve();require(binary.is_relative_to(base),'supplier outside package');return r,binary
