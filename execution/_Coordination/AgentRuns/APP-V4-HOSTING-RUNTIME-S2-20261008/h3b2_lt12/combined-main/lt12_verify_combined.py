import pathlib,json,hashlib,subprocess,shutil
root=pathlib.Path(pathlib.Path('/private/tmp/lt12-combined-export-result.log').read_text().splitlines()[0]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();verified=[]
def check(base,items):
 assert items==sorted(items,key=lambda x:x['path']);actual={p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file()};assert actual=={i['path'] for i in items}
 for i in items:
  p=base/i['path'];assert sha(p)==i['sha256'];assert p.stat().st_size==i['size']
for kind in ['lt09','terminal']:
 for case in ['selected','unselected']:
  base=root/kind/case;p=base/'exchange.json';v=json.loads(p.read_text())
  if kind=='lt09':check(base/'publication',v['members']);assert v['actualLt09']['transitionId']=='LT-09'
  else:
   for part in ['predecessor','terminal']:check(base/part/'publication',v[part]['members'])
   assert v['predecessor']['actualLt09']['transitionId']=='LT-09';assert v['terminal']['actualLt23']['transitionId']=='LT-23';assert v['predecessor']['actualLt09']['generation']==v['terminal']['actualLt23']['generation']
  if case=='selected':check(base/'selected-source',v['selectedSourceMembers'])
  else:assert v['selectedSourceMembers'] is None;assert not (base/'selected-source').exists()
  verified.append({'format':v['format'],'case':case,'marker':str(p),'sha256':sha(p)})
repo=pathlib.Path('/private/tmp/hosting-secondary-manager');rev='2377becab65791fcd91177fcf4ab15abcf4c1742';assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==rev;assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo)
paths=subprocess.check_output(['git','ls-files','projects/chirality-app-v4/app/src-tauri/src','projects/chirality-app-v4/app/src-tauri/resources/distribution-successor'],cwd=repo,text=True).splitlines();source=[]
for path in paths:
 p=repo/path;assert p.read_bytes()==subprocess.check_output(['git','show',rev+':'+path],cwd=repo);source.append({'path':path,'sha256':sha(p)})
(root/'SOURCE_MEMBERS.json').write_text(json.dumps(source,indent=2)+'\n')
(root/'VERIFICATION.json').write_text(json.dumps({'markers':verified,'sourceMembersSha256':sha(root/'SOURCE_MEMBERS.json'),'assertions':'All declared raw file sets, hashes and sizes match. Clean source equals commit, both formats same executable/source/argv, terminal H5 equal.'},indent=2)+'\n')
for pattern in ['lt12-combined-*.log','lt12-combined-harness.jsonl','lt12_run_combined_exports.py','lt12_verify_combined.py']:
 for p in pathlib.Path('/private/tmp').glob(pattern):shutil.copy2(p,root/p.name)
s=json.loads((root/'SUMMARY.json').read_text())
(root/'RETURN.md').write_text(f'''# Combined-source renewal\n\nExact source `{rev}` in clean `/private/tmp/hosting-secondary-manager`, incorporating additive C3 #1155. No maintained source changes; prior 938d20 cohorts preserved.\n\nDefault and distribution-successor,custom-protocol bounded `successor::tests::lt12 connector_reconstruction` matrix each passed 22 tests (15 LT12 + 7 connector reconstruction), zero failed/ignored. Logs retain first production compile failure: missing frontendDist. Rerun used newly created ignored `projects/chirality-app-v4/app/dist/index.html`, SHA256 3bdbdb72ac6c1c06209e7fbe295ff834bdc8ae540bdffc4afe9e9d1b942d162d, exact bytes `<!doctype html><title>Synthetic offline Rust harness input only</title>Not an App bundle or frontend build witness.` followed by LF. This is Rust harness input only, no frontend/build/bundle qualification. It remains ignored and labelled.\n\nDefault no-run recompilation followed both-feature checks. Both unchanged explicit export helpers passed one test each, selected+unselected. Harness `{s['harnessExecutable']}`, SHA256 `{s['harnessExecutableSha256']}` unchanged across both invocations. Exact argv/env/source/executable/member identities are in separate receipts. Formats are only LT09 v1 and LT09+LT23 terminal v1; no LT12 exchange claim.\n\nEnvironment: offline CARGO_HOME=/Users/ryan/Library/Caches/chirality-dev/cargo-home-group-a; existing CARGO_TARGET_DIR=/private/tmp/hosting-s2-target; CARGO_INCREMENTAL=0; CHIRALITY_SKIP_CODEX=1. No new checkout/target, native App/supplier, download or credentials. Disk10GiB at start. Source/src and successor resource bytes equal commit (SOURCE_MEMBERS.json); all marker/raw-member checks in VERIFICATION.json. This is synthetic evidence, no S3/SEAL2/qualification. Shared target released after validation.\n''')
(root/'RECEIPTS_MANIFEST.json').write_text(json.dumps([{'path':p.name,'sha256':sha(p)} for p in sorted(root.iterdir()) if p.is_file() and p.name!='RECEIPTS_MANIFEST.json'],indent=2)+'\n')
print(root);print(json.dumps(s,indent=2));print(json.dumps(verified,indent=2));print('source',sha(root/'SOURCE_MEMBERS.json'));print('manifest',sha(root/'RECEIPTS_MANIFEST.json'));print('return',sha(root/'RETURN.md'))
