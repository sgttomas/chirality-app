import json,os,signal,subprocess,time
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parent
repo=Path('/Users/ryan/.t3/worktrees/chirality-app/t3-app-v4-desktop-release-delivery')
slot='/Users/ryan/dev/chirality-t3/tools/t3_slot.sh'
exclusive=Path('/Users/ryan/dev/chirality-t3/guard/exclusive.pending')
node='/Users/ryan/.local/share/mise/installs/node/24.18.0/bin/node'
path='/Users/ryan/.local/share/mise/installs/node/24.18.0/bin:/Users/ryan/.rustup/toolchains/stable-aarch64-apple-darwin/bin:/usr/bin:/bin:/usr/sbin:/sbin'
env={'HOME':'/Users/ryan','PATH':path,'LANG':'en_US.UTF-8','CARGO_HOME':str(root/'cargo-home'),'CARGO_TARGET_DIR':str(root/'target'),'CARGO_BUILD_JOBS':'2','CARGO_NET_OFFLINE':'true','CODEX_HOME':str(root/'codex-home'),'TMPDIR':str(root/'tmp')}
command=[node,'node_modules/@tauri-apps/cli/tauri.js','build','--debug','--no-sign','--bundles','app','--features','custom-protocol','--config','packaging/unsigned/tauri.development.conf.json','--config',str(root/'supplier.development.conf.json'),'--','--offline','--locked']
def now():return datetime.now(timezone.utc).isoformat()
def snapshot():
 rows=[]
 for line in subprocess.check_output(['/bin/ps','-axo','pid=,ppid=,rss=,command='],text=True).splitlines():
  fields=line.strip().split(None,3)
  if len(fields)==4:rows.append((int(fields[0]),int(fields[1]),int(fields[2]),fields[3]))
 return rows
start=now();facts={'source_revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),'command':command,'wrapper':slot,'environment':env,'started_at':start}
(root/'build-invocation.json').write_text(json.dumps(facts,indent=2)+'\n')
if exclusive.exists():raise SystemExit('exclusive pending: build not started')
with (root/'build.log').open('w') as log:
 proc=subprocess.Popen([slot,*command],cwd=repo/'app',env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 peak=0;reason=None
 while proc.poll() is None:
  rows=snapshot();own={proc.pid,os.getpid()};changed=True
  while changed:
   before=len(own);own.update(pid for pid,ppid,rss,cmd in rows if ppid in own);changed=len(own)!=before
  rss=sum(rss for pid,ppid,rss,cmd in rows if pid in own or '/Users/ryan/dev/chirality-t3/' in cmd);peak=max(peak,rss)
  try:free=int(subprocess.check_output(['/usr/sbin/sysctl','-n','kern.memorystatus_level'],text=True))
  except (ValueError,subprocess.CalledProcessError):reason='system memory unavailable';free=0
  if exclusive.exists():reason='exclusive.pending'
  elif rss>=64*1024*1024:reason='shared RSS at 64GiB'
  elif free<22:reason='system free below 22%'
  if reason:
   os.killpg(proc.pid,signal.SIGTERM)
   try:proc.wait(timeout=3)
   except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
   break
  time.sleep(1)
 facts.update(finished_at=now(),exit_code=proc.wait(),abort_reason=reason,peak_shared_rss_kib=peak)
 (root/'build-invocation.json').write_text(json.dumps(facts,indent=2)+'\n')
 print(json.dumps(facts))
 raise SystemExit(facts['exit_code'] or (1 if reason else 0))
