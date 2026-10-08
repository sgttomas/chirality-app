import json, pathlib, hashlib, tempfile, subprocess, os
base=pathlib.Path('/private/tmp/hosting-secondary-manager'); cwd=base/'projects/chirality-app-v4/app/src-tauri'
rev='938d20ef4bf0d07a7cc706d575e74f844d8caccf'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()==rev
assert not subprocess.check_output(['git','status','--porcelain'],cwd=base)
artifacts=[json.loads(x) for x in pathlib.Path('/private/tmp/lt12-committed-harness.jsonl').read_text().splitlines() if x.startswith('{')]
exe=next(x['executable'] for x in artifacts if x.get('reason')=='compiler-artifact' and x.get('executable') and x['profile']['test'])
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
exe_sha=sha(exe)
packet=pathlib.Path(tempfile.mkdtemp(prefix='lt12-committed-exports-',dir='/private/tmp'))
results=[]
for label,envkey,test in [('lt09','CHIRALITY_S4_EXPORT_ROOT','hosting::successor::tests::s4_export::export_group_b_s4_selected_and_unselected'),('terminal','CHIRALITY_TERMINAL_EXPORT_ROOT','hosting::successor::tests::terminal_export::export_group_b_terminal_selected_and_unselected')]:
 out=packet/label;out.mkdir(mode=0o700);argv=[exe,test,'--exact','--ignored','--nocapture'];env=os.environ.copy();env[envkey]=str(out);env.pop('CHIRALITY_TERMINAL_DIAGNOSTIC',None)
 with (packet/(label+'.log')).open('wb') as log:result=subprocess.run(argv,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT)
 assert result.returncode==0,(label,result.returncode)
 assert sha(exe)==exe_sha
 members=[]
 for p in sorted(out.rglob('*')):
  assert not p.is_symlink()
  if p.is_file():members.append({'path':p.relative_to(out).as_posix(),'sha256':sha(p),'size':p.stat().st_size})
 for case in ['selected','unselected']:
  exchange=json.loads((out/case/'exchange.json').read_text());assert exchange['producer']['sourceRevision']==rev;assert exchange['producer']['harnessExecutableSha256']==exe_sha;assert exchange['producer']['command']==argv;assert exchange['producer']['features']==[]
 receipt={'sourceRevision':rev,'sourceCheckout':str(base),'sourceCleanBeforeAndAfter':True,'harnessExecutable':exe,'harnessExecutableSha256':exe_sha,'command':argv,'cwd':str(cwd),'environment':{envkey:str(out)},'features':[],'outputRoot':str(out),'standing':'synthetic offline fixture exports; unchanged LT09 or LT09+LT23 format, no LT12 or qualification claim','members':members}
 (packet/(label+'-receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n');results.append({'kind':label,'outputRoot':str(out),'receipt':str(packet/(label+'-receipt.json')),'receiptSha256':sha(packet/(label+'-receipt.json'))})
assert not subprocess.check_output(['git','status','--porcelain'],cwd=base)
summary={'sourceRevision':rev,'harnessExecutable':exe,'harnessExecutableSha256':exe_sha,'exports':results}
(packet/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(str(packet));print(json.dumps(summary,indent=2))
