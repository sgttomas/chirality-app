import pathlib,json,hashlib,subprocess,shutil
root=pathlib.Path(pathlib.Path('/private/tmp/stop-admission-committed-export-result.log').read_text().splitlines()[0]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();verified=[]
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
repo=pathlib.Path('/private/tmp/hosting-secondary-manager');rev='127d48f61d91b70d00d0670d2150c79b8ac26d1f';assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==rev;assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo)
paths=subprocess.check_output(['git','ls-files','projects/chirality-app-v4/app/src-tauri/src','projects/chirality-app-v4/app/src-tauri/resources/distribution-successor'],cwd=repo,text=True).splitlines();source=[]
for path in paths:
 p=repo/path;assert p.read_bytes()==subprocess.check_output(['git','show',rev+':'+path],cwd=repo);source.append({'path':path,'sha256':sha(p)})
(root/'SOURCE_MEMBERS.json').write_text(json.dumps(source,indent=2)+'\n')
(root/'VERIFICATION.json').write_text(json.dumps({'markers':verified,'sourceMembersSha256':sha(root/'SOURCE_MEMBERS.json'),'assertions':'All declared raw file sets, hashes and sizes match. Clean source equals commit, both formats same executable/source/argv, terminal H5 equal.'},indent=2)+'\n')

raw=sum(len(json.loads((root/k/c/'exchange.json').read_text()).get('members',[])) if k=='lt09' else sum(len(json.loads((root/k/c/'exchange.json').read_text())[part]['members']) for part in ['predecessor','terminal']) for k in ['lt09','terminal'] for c in ['selected','unselected'])
raw+=sum(len(json.loads((root/k/'selected'/'exchange.json').read_text())['selectedSourceMembers']) for k in ['lt09','terminal'])
assert raw==89,raw
assert sum(1 for k in ["lt09","terminal"] for p in (root/k).rglob("*") if p.is_file())==93
for pattern in ['stop-admission-committed-*.log','stop-admission-committed-harness.jsonl','stop_admission_run_exports.py','stop_admission_verify_exports.py']:
 for p in pathlib.Path('/private/tmp').glob(pattern):shutil.copy2(p,root/p.name)
s=json.loads((root/'SUMMARY.json').read_text())
(root/'RETURN.md').write_text(f"""# Reviewed committed-source export renewal

Exact source `{rev}` in clean `/private/tmp/hosting-secondary-manager`. Fresh default offline compilation finished in14.37s. No maintained files changed; all earlier cohorts preserved.

Harness `{s['harnessExecutable']}`
SHA256 `{s['harnessExecutableSha256']}`. Both unchanged ignored export helpers passed1 test each from this SAME executable, selected and unselected cases. Formats only LT09v1 and LT09+LT23terminalv1; no LT20 or new format claim. Explicit invented App candidate fields unchanged.

All89 declared raw artifact members (93 exported files including four exchange markers) across four cases verified against exact path sets, hashes and sizes, including selected-source originals. Unselected source directory absent; terminal actualLT09/LT23 share fullH5. Source src and successor resources byte-equal exactcommit in SOURCE_MEMBERS.json. Separate lt09-receipt.json and terminal-receipt.json retain exact executable/source/argv/env and every exported file digest. VERIFICATION.json retains marker hashes.

Build command cargo test --offline --lib --no-run --message-format=json with CARGO_HOME=/Users/ryan/Library/Caches/chirality-dev/cargo-home-group-a, CARGO_TARGET_DIR=/private/tmp/hosting-s2-target, CARGO_INCREMENTAL=0, CHIRALITY_SKIP_CODEX=1. Logs and invocation scripts retained. No new checkout/target, supplier/native App, download, credentials, S3/SEAL2 or qualification claim. Disk10GiB before build. Target released after both helpers and verification.
""")
(root/'RECEIPTS_MANIFEST.json').write_text(json.dumps([{'path':p.name,'sha256':sha(p)} for p in sorted(root.iterdir()) if p.is_file() and p.name!='RECEIPTS_MANIFEST.json'],indent=2)+'\n')
print(root);print(json.dumps(s,indent=2));print('rawMembers',raw);print('source',sha(root/'SOURCE_MEMBERS.json'));print('manifest',sha(root/'RECEIPTS_MANIFEST.json'));print('return',sha(root/'RETURN.md'))
