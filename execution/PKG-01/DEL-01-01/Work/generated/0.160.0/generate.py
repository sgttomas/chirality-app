from pathlib import Path
import tempfile,subprocess,os,hashlib,json,sys
supplier=Path(sys.argv[1])
expected='112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b'
assert hashlib.sha256(supplier.read_bytes()).hexdigest()==expected
scratch=Path(subprocess.check_output(['mktemp','-d',str(Path(tempfile.gettempdir())/'chirality-sup1-XXXXXX')],text=True).strip());home=scratch/'codex-home';home.mkdir();(home/'config.toml').write_text('model_provider = "sup1-local"\nmodel = "sup1-no-model"\n[model_providers.sup1-local]\nname = "SUP1 offline generation"\nbase_url = "http://127.0.0.1:9/v1"\nwire_api = "responses"\n[features]\nplugins = false\n[analytics]\nenabled = false\n')
env={k:v for k,v in os.environ.items() if k not in ('OPENAI_API_KEY','CODEX_API_KEY','CODEX_ACCESS_TOKEN','CODEX_HOME')};env['CODEX_HOME']=str(home)
version=subprocess.run([str(supplier),'--version'],env=env,check=True,capture_output=True,text=True).stdout.strip();assert version=='codex-cli 0.160.0'
log=[];stats={}
for kind,cmd in [('ts','generate-ts'),('json-schema','generate-json-schema')]:
 for variant in ['stable','experimental']:
  manifests=[]
  for run in [1,2]:
   out=scratch/kind/variant/f'run{run}';out.mkdir(parents=True)
   argv=[str(supplier),'app-server',cmd]+(['--experimental'] if variant=='experimental' else [])+['--out',str(out)]
   r=subprocess.run(argv,env=env,cwd=scratch,check=True,capture_output=True,text=True)
   rows=[hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(out)) for f in sorted(out.rglob('*')) if f.is_file()];manifest='\n'.join(rows)+'\n';manifests.append(manifest)
   log.append({'kind':kind,'variant':variant,'run':run,'command':['<approved-stock0.160.0>','app-server',cmd]+(['--experimental'] if variant=='experimental' else [])+['--out',f'<scratch>/{kind}/{variant}/run{run}'],'exitCode':r.returncode,'files':len(rows),'manifestSha256':hashlib.sha256(manifest.encode()).hexdigest(),'stderr':r.stderr})
  assert manifests[0]==manifests[1],(kind,variant)
  stats[kind+'/'+variant]={'deterministic':True,'files':len(rows),'manifestSha256':hashlib.sha256(manifests[0].encode()).hexdigest(),'manifest':manifests[0]}
(scratch/'summary.json').write_text(json.dumps({'supplierSha256':expected,'version':version,'stats':stats,'commands':log},indent=2)+'\n');print(str(scratch));print(version);print(json.dumps({k:{a:b for a,b in v.items() if a!='manifest'} for k,v in stats.items()},indent=2))
