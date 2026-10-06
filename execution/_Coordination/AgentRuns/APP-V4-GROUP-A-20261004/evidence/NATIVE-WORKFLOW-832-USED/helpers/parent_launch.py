#!/usr/bin/env python3
"""Parent only. No supplier call on import. Execute only the reviewed compiled binding."""
import argparse,http.server,json,os,pathlib,shutil,subprocess,tempfile,threading,uuid,time
from witness_common import *
from owned_processes import Ownership
HERE=pathlib.Path(__file__).resolve().parent
def development_start_option(approved):
    require(approved,'explicit existing LT-24 development option required')
    return {'allowUnverifiedDev':True,'transition':'LT-24','supplierStanding':'unverified-development','qualifiedDistribution':False}

def create_codex_homes(root):
    records=[]
    for name in ('codex-home','probe-home'):
        destination=root/name;require(not destination.exists(),'home destination already exists')
        command=['/usr/bin/mktemp','-d',str(root/(name+'-mktemp.XXXXXX'))]
        result=subprocess.run(command,env={'PATH':'/usr/bin:/bin','TMPDIR':str(root)},capture_output=True,text=True,check=False)
        record={'command':command,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr};records.append(record);save(root/'home-creation.json',records)
        require(result.returncode==0,'mktemp home creation failed')
        created=pathlib.Path(result.stdout.strip());require(created.is_absolute() and created.parent==root and not created.is_symlink(),'unexpected mktemp home path')
        before=created.stat();require(created.is_dir() and not any(created.iterdir()),'mktemp home must be empty directory')
        require(before.st_dev==root.stat().st_dev,'home move must stay on same filesystem')
        require(before.st_mode & 0o777==0o700,'mktemp home must be private')
        created.rename(destination);after=destination.stat()
        require((before.st_dev,before.st_ino)==(after.st_dev,after.st_ino),'home move changed physical directory')
        record.update(createdBy='mktemp -d',movedFrom=str(created),usedAt=str(destination),device=after.st_dev,inode=after.st_ino,mode=oct(after.st_mode & 0o777),sameFilesystemMove=True)
        save(root/'home-creation.json',records)
    return records

def validate_compiled(path):
    bound=json.loads(path.read_text());require(bound['status']=='compiled; execution unperformed','not a compiled binding')
    base=path.parent
    if 'bindingSuccession' in bound:
        succession=bound['bindingSuccession'];require(succession['kind']=='python-only-launcher-successor','unsupported binding succession')
        predecessor_path=pathlib.Path(succession['predecessorPath']);require(predecessor_path==base/'compiled-binding.json','unexpected predecessor path')
        require(sha(predecessor_path)==succession['predecessorSha256'],'compiled predecessor drift')
        predecessor=json.loads(predecessor_path.read_text());require('bindingSuccession' not in predecessor,'nested binding succession refused')
        expected=json.loads(json.dumps(predecessor));expected['helperHashes']['parent_launch.py']=sha(HERE/'parent_launch.py');expected['bindingSuccession']=succession
        require(bound==expected,'successor changes more than reviewed Python launcher binding')
        require(succession['changedHelpers']==['parent_launch.py'],'unexpected helper replacement')
        require(sha(base/'helpers/parent_launch.py')==predecessor['helperHashes']['parent_launch.py'],'compiled launcher preimage drift')
    binary=pathlib.Path(bound['immutableExecutable']);require(binary.parent==base,'binary outside binding root');require(sha(binary)==bound['executableSha256'],'compiled executable drift')
    require(set(bound['generatedOutputs'])<=GENERATED_SCHEMA_PATHS and not (set(bound['generatedOutputs'])&set(bound['injectedSources'])),'unapproved generated output paths')
    require(manifest(base/'app',('target',))==dict(bound['injectedSources'],**bound['generatedOutputs']),'copied sources or generated outputs drift')
    require(sha(base/'injection.diff')==bound['injectionSha256'],'injection diff drift');require(sha(base/'compile.stdout.jsonl')==bound['compileLogSha256'],'compile log drift')
    for name in ('parent_launch.py','witness_common.py','owned_processes.py','parent_stock_workflow_witness.rs','ownership_hook.rs','prepare_compile.py'):
        require(sha(HERE/name)==bound['helperHashes'][name],'launcher/helper differs from compilation binding: '+name)
    require(sha(base/'app/src-tauri/src/parent_stock_workflow_witness.rs')==bound['fixtureSha256'],'copied fixture drift')
    require(bound['sourceBefore']==bound['copiedBefore'],'source/copy mismatch in binding')
    baseline=base/'candidate-archive/projects/chirality-app-v4/app'
    require(manifest(baseline)==bound['sourceBefore'],'retained candidate archive drift')
    require(json.loads((base/'commit-app-manifest.json').read_text())==bound['sourceBefore'],'resolved-commit manifest mismatch')
    import prepare_compile
    with tempfile.TemporaryDirectory(prefix='chirality-wf-revalidate-',dir='/private/tmp') as scratch:
        reconstructed=pathlib.Path(scratch)/'app';shutil.copytree(baseline,reconstructed)
        patch=prepare_compile.inject(reconstructed,HERE)
        require(patch==(base/'injection.diff').read_text(),'injection differs from approved helper operations')
        require(manifest(reconstructed)==bound['injectedSources'],'unexpected source changes beyond bounded injection')
    emitted=[]
    for line in (base/'compile.stdout.jsonl').read_text().splitlines():
        try:row=json.loads(line)
        except json.JSONDecodeError:continue
        if row.get('reason')=='compiler-artifact' and row.get('profile',{}).get('test') and row.get('executable'):emitted.append(row['executable'])
    require(emitted==[bound['emittedExecutable']],'binding not the sole emitted test executable')
    require(sha(pathlib.Path(bound['emittedExecutable']))==bound['executableSha256'],'emitted executable no longer matches retained binary')
    return bound,binary

def main():
    p=argparse.ArgumentParser();p.add_argument('--execute-reviewed',action='store_true');p.add_argument('--allow-unverified-development',action='store_true');p.add_argument('--compiled-binding',type=pathlib.Path,required=True);p.add_argument('--reviewed-binding-sha256',required=True);p.add_argument('--supplier-manifest',type=pathlib.Path,required=True);p.add_argument('--approved-supplier-manifest-sha256',required=True);p.add_argument('--holding-source',type=pathlib.Path,required=True);p.add_argument('--keep-root',type=pathlib.Path,required=True);a=p.parse_args()
    require(a.execute_reviewed,'Parent reviewed execution required');development=development_start_option(a.allow_unverified_development);require(sha(a.compiled_binding)==a.reviewed_binding_sha256,'reviewed compile binding changed');bound,binary=validate_compiled(a.compiled_binding.resolve())
    supplier,supplier_binary=validate_supplier(a.supplier_manifest,a.approved_supplier_manifest_sha256)
    require(not a.keep_root.exists(),'evidence destination must be fresh')
    root=pathlib.Path(tempfile.mkdtemp(prefix='chirality-parent-stock-wf-',dir='/private/tmp')).resolve();print(root,flush=True)
    for name in ('workspace','library','os-home','tmp','holding'):(root/name).mkdir()
    homes=create_codex_homes(root)
    package=root/'holding/coordinated-knowledge-work';holding_before=manifest(a.holding_source);shutil.copytree(a.holding_source,package);require(manifest(package)==holding_before,'holding copy mismatch')
    invocation={'id':str(uuid.uuid4()),'root':str(root),'compiledBindingSha256':sha(a.compiled_binding),'homeCreation':homes,'developmentStart':development,'candidate':bound['resolvedCandidate'],'executableSha256':sha(binary),'fixtureSha256':bound['fixtureSha256'],'launcherSha256':sha(pathlib.Path(__file__)),'supplierManifestSha256':sha(a.supplier_manifest),'holdingManifest':holding_before,'test':TEST,'providerMarker':'parent_fixture_'+uuid.uuid4().hex}
    save(root/'launch-binding.json',invocation);shutil.copyfile(a.compiled_binding,root/'compiled-binding.json');shutil.copyfile(a.supplier_manifest,root/'approved-supplier-manifest.json')
    class Reject(http.server.BaseHTTPRequestHandler):
        def log_message(self,*unused):pass
        def do_POST(self):
            body=self.rfile.read(int(self.headers.get('Content-Length','0')));observation={'path':self.path,'method':'POST','requestSha256':__import__('hashlib').sha256(body).hexdigest(),'bytes':len(body),'status':400,'marker':invocation['providerMarker'],'responseSent':False}
            payload=json.dumps({'error':{'message':invocation['providerMarker'],'type':'invalid_request_error','code':invocation['providerMarker']}}).encode()
            try:
                self.send_response(400);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload);self.wfile.flush();observation['responseSent']=True
            finally:
                with open(root/'provider-observations.jsonl','a') as f:f.write(json.dumps(observation)+'\n')
        def do_GET(self):self.send_error(400,'no discovery')
    server=None;process=None;ownership=None;code=1;failure=None;summary=None;cleanup=None
    try:
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Reject);threading.Thread(target=server.serve_forever,daemon=True).start()
        config=f'''cli_auth_credentials_store = "file"
model_provider = "parent_loopback_400"
model = "gpt-6.1-sol"
model_reasoning_effort = "medium"
[model_providers.parent_loopback_400]
name = "Parent capture-only loopback HTTP400"
base_url = "http://127.0.0.1:{server.server_address[1]}/v1"
wire_api = "responses"
requires_openai_auth = false
supports_websockets = false
[features]
plugins = false
[analytics]
enabled = false
'''
        for home in ('codex-home','probe-home'):(root/home/'config.toml').write_text(config)
        vendor=supplier_binary.parent.parent;env={'PATH':str(vendor/'codex-path')+':'+str(supplier_binary.parent)+':/usr/bin:/bin:/usr/sbin:/sbin','HOME':str(root/'os-home'),'TMPDIR':str(root/'tmp'),'LANG':'en_US.UTF-8','CODEX_HOME':str(root/'codex-home'),'CHIRALITY_PARENT_WORKFLOW_WITNESS':'reviewed-parent-only','CHIRALITY_WITNESS_ROOT':str(root),'CHIRALITY_WITNESS_BINARY':str(supplier_binary),'CHIRALITY_WITNESS_BINARY_SHA256':sha(supplier_binary)}
        ownership=Ownership(root);env.update(ownership.environment());ownership.start()
        with open(root/'test-output.log','wb') as output:
            try:process=subprocess.Popen([str(binary),TEST,'--ignored','--exact','--nocapture','--test-threads=1'],cwd=root,env=env,stdout=output,stderr=subprocess.STDOUT,pass_fds=ownership.inherited(),start_new_session=True)
            finally:ownership.handed_off()
            try:code=process.wait(timeout=110)
            except subprocess.TimeoutExpired:code=124
    except Exception as e:failure=repr(e);code=1
    finally:
        if process is not None:cleanup=ownership.cleanup(process)
        elif ownership is not None:
            ownership.worker.join(timeout=2);cleanup={'clean':not ownership.worker.is_alive(),'spawnFailed':True,'errors':ownership.errors};save(root/'cleanup.json',cleanup)
        if server is not None:server.shutdown();server.server_close()
        try:
            require(cleanup is not None and cleanup['clean'],'cleanup not established')
            summary=validate_result(root,invocation,code,(root/'test-output.log').read_text())
            require({e['stage'] for e in cleanup['ownedGroups']}=={1,2},'probe/app ownership observations incomplete')
        except Exception as e:failure=repr(e);code=1 if code==0 else code
        save(root/'launcher-result.json',{'exit':code,'failure':failure,'sourceComparison':summary,'cleanup':cleanup,'invocation':invocation,'standing':'failed/incomplete witness' if code else summary['standing']})
        shutil.copytree(root,a.keep_root)
    print(json.dumps({'exit':code,'ownedRunRoot':str(root),'savedEvidence':str(a.keep_root),'failure':failure}));return code
if __name__=='__main__':raise SystemExit(main())
