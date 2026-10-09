import hashlib,json,pathlib,subprocess,shutil,re
root=pathlib.Path('/private/tmp/cce-call-custody'); out=pathlib.Path('/private/tmp/cce-call-evidence')
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git','-C',str(root),*a])
paths=git('diff','--cached','--name-only').decode().splitlines(); assert len(paths)==7
manifest={'format':'cce-call-custody-author-freeze.v1','base':git('rev-parse','HEAD').decode().strip(),'branch':git('branch','--show-current').decode().strip(),'source':[],'basis':[],'checks':[],'claims':'Dormant test-only original offered-call custody. No production activation, managed service, TASK, delivery, supplier/native/process execution, B adoption or qualification.'}
for p in paths:
 b=(root/p).read_bytes();assert b==git('show',':'+p)
 dest=out/'source'/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
 try:pre=sha(git('show','HEAD:'+p))
 except subprocess.CalledProcessError:pre=None
 manifest['source'].append({'path':p,'sha256':sha(b),'size':len(b),'preimageSha256':pre})
for p in pathlib.Path('/private/tmp').glob('CCE_CALL*'):
 if p.is_file():
  b=p.read_bytes();d=out/'basis'/p.name;d.parent.mkdir(exist_ok=True);d.write_bytes(b);manifest['basis'].append({'origin':str(p),'path':str(d.relative_to(out)),'sha256':sha(b)})
p=pathlib.Path('/private/tmp/cce-call-custody-build-input.json');shutil.copyfile(p,out/'BUILD_INPUT.json')
for name,features,count in [('default-r1.log',[],12),('default-r2.log',[],12),('default-r3.log',[],17),('features-r1.log',['distribution-successor','custom-protocol'],17)]:
 b=(out/name).read_bytes();assert f'{count} passed; 0 failed'.encode() in b
 manifest['checks'].append({'log':name,'sha256':sha(b),'passed':count,'features':features,'finalByteCoverage':name in ['default-r3.log','features-r1.log']})
manifest['patchSha256']=sha((out/'CANDIDATE.patch').read_bytes())
manifest['indexTree']=None # Not needed; sandbox denied Git write-tree outside writable roots.
(out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('MANIFEST',sha((out/'MANIFEST.json').read_bytes()));print('PATCH',manifest['patchSha256']);print('TREE',manifest['indexTree'])
