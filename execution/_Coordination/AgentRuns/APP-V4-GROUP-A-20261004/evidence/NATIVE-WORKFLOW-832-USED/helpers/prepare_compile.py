#!/usr/bin/env python3
"""Copy/manifest/inject only by default. Cargo requires a separate explicit release."""
import argparse,io,json,pathlib,shutil,subprocess,tempfile,tarfile,difflib,os
from witness_common import *
HERE=pathlib.Path(__file__).resolve().parent
DECL='\n#[cfg(test)]\n#[path="parent_stock_workflow_witness.rs"]\nmod parent_stock_workflow_witness;\n'
def inject(app,helper):
    runtime=app/'src-tauri/src/runtime_session.rs';host=app/'src-tauri/src/hosting.rs'
    before={str(p.relative_to(app)):p.read_text() for p in (runtime,host)}
    runtime.write_text(runtime.read_text()+DECL)
    source=host.read_text();anchor='        let label = probe\n';require(source.count(anchor)==1,'probe anchor drift')
    source=source.replace(anchor,'        probe.process_group(0);\n        parent_witness_own_spawn(&mut probe, 1);\n'+anchor)
    anchor='        let mut child = match cmd.spawn() {';require(source.count(anchor)==1,'spawn anchor drift')
    source=source.replace(anchor,'        parent_witness_own_spawn(&mut cmd, 2);\n'+anchor)
    source+='\n'+(helper/'ownership_hook.rs').read_text();host.write_text(source)
    fixture=app/'src-tauri/src/parent_stock_workflow_witness.rs';shutil.copyfile(helper/'parent_stock_workflow_witness.rs',fixture)
    patch=''.join(''.join(difflib.unified_diff(before[str(p.relative_to(app))].splitlines(True),p.read_text().splitlines(True),fromfile='candidate/'+str(p.relative_to(app)),tofile='private/'+str(p.relative_to(app)))) for p in (runtime,host))
    patch+=''.join(difflib.unified_diff([],fixture.read_text().splitlines(True),fromfile='/dev/null',tofile='private/src-tauri/src/parent_stock_workflow_witness.rs'))
    return patch
def main():
    p=argparse.ArgumentParser();p.add_argument('--candidate-context',type=pathlib.Path,required=True);p.add_argument('--candidate-commit',required=True);p.add_argument('--repository',type=pathlib.Path,required=True);p.add_argument('--compile-approved',action='store_true');a=p.parse_args()
    source=a.candidate_context.resolve();root=pathlib.Path(tempfile.mkdtemp(prefix='chirality-wf-bound-compile-',dir='/private/tmp'));print(root,flush=True)
    helper=root/'helpers';shutil.copytree(HERE,helper,ignore=shutil.ignore_patterns('__pycache__','test-*','synthetic-*'))
    resolved=subprocess.check_output(['git','rev-parse',a.candidate_commit+'^{commit}'],cwd=a.repository,text=True).strip()
    archive=subprocess.check_output(['git','archive',resolved,'projects/chirality-app-v4/app'],cwd=a.repository)
    baseline=root/'candidate-archive';baseline.mkdir()
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar: tar.extractall(baseline,filter='data')
    original=manifest(source/'app',('target','node_modules','dist','.DS_Store'))
    expected=manifest(baseline/'projects/chirality-app-v4/app')
    save(root/'source-before-copy.json',original);save(root/'commit-app-manifest.json',expected)
    require(original==expected,'source app differs from resolved commit; retain and resolve candidate first')
    shutil.copytree(source/'app',root/'app',ignore=shutil.ignore_patterns('target','node_modules','dist','.DS_Store'))
    copied=manifest(root/'app');save(root/'copied-pre-injection.json',copied)
    require(copied==original and manifest(source/'app',('target','node_modules','dist','.DS_Store'))==original,'copy/source drift')
    (root/'injection.diff').write_text(inject(root/'app',helper));final=manifest(root/'app');save(root/'injected-manifest.json',final)
    binding={'resolvedCandidate':resolved,'candidateContext':str(source),'sourceBefore':original,'copiedBefore':copied,'injectedSources':final,'injectionSha256':sha(root/'injection.diff'),'helperHashes':{p.name:sha(p) for p in helper.iterdir() if p.is_file()},'fixtureSha256':sha(root/'app/src-tauri/src/parent_stock_workflow_witness.rs'),'status':'prepared; no compilation or execution'}
    save(root/'preparation-binding.json',binding)
    if not a.compile_approved: return
    toolchain=pathlib.Path('/Users/ryan/.rustup/toolchains/stable-aarch64-apple-darwin/bin')
    toolchain_record={name:{'path':str(toolchain/name),'sha256':sha(toolchain/name),'version':subprocess.check_output([str(toolchain/name),'--version'],text=True).strip()} for name in ('cargo','rustc','rustdoc')}
    save(root/'toolchain-binding.json',toolchain_record);binding['toolchain']=toolchain_record
    env={'PATH':str(toolchain)+':/usr/bin:/bin:/usr/sbin:/sbin','RUSTC':str(toolchain/'rustc'),'RUSTDOC':str(toolchain/'rustdoc'),'CARGO_HOME':'/tmp/chirality-app-v4-group-a-cargo-home','CARGO_NET_OFFLINE':'true','CHIRALITY_SKIP_CODEX':'1','HOME':str(root/'build-home'),'TMPDIR':str(root/'build-tmp')}
    for name in ('build-home','build-tmp'): (root/name).mkdir()
    command=[str(toolchain/'cargo'),'test','--offline','--locked','--lib','--no-run','--message-format=json']
    result=subprocess.run(command,cwd=root/'app/src-tauri',env=env,capture_output=True,text=True)
    (root/'compile.stdout.jsonl').write_text(result.stdout);(root/'compile.stderr.log').write_text(result.stderr);save(root/'compile-outcome.json',{'code':result.returncode,'command':command,'environment':env,'postSources':manifest(root/'app',('target',))})
    require(result.returncode==0,'compile failed; exact failure retained at '+str(root))
    post=manifest(root/'app',('target',));require(all(post.get(k)==v for k,v in final.items()),'source changed during compilation')
    generated={k:v for k,v in post.items() if k not in final};require(set(generated)<=GENERATED_SCHEMA_PATHS,'unexpected generated files; investigate retained output')
    binding['generatedOutputs']=generated;save(root/'intentional-generated-outputs.json',generated)
    artifacts=[]
    for line in result.stdout.splitlines():
        try:r=json.loads(line)
        except json.JSONDecodeError: continue
        if r.get('reason')=='compiler-artifact' and r.get('profile',{}).get('test') and r.get('executable'): artifacts.append(pathlib.Path(r['executable']))
    require(len(artifacts)==1,'ambiguous compiler artifact')
    artifact=root/'reviewed-tests';shutil.copyfile(artifacts[0],artifact);artifact.chmod(0o500)
    binding.update(status='compiled; execution unperformed',emittedExecutable=str(artifacts[0]),immutableExecutable=str(artifact),executableSha256=sha(artifact),command=command,compileLogSha256=sha(root/'compile.stdout.jsonl'))
    save(root/'compiled-binding.json',binding)
if __name__=='__main__':main()
