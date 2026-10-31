"""Fixed once-only v2 invocation after actual slot acquisition; no App control."""
from pathlib import Path
from datetime import datetime,timedelta,timezone
import hashlib,json,os,stat,subprocess,sys
T3=Path('/Users/ryan/dev/chirality-t3')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def require(ok,message):
    if not ok:raise RuntimeError(message)
def main():
    root=Path(__file__).resolve().parent;info=root.lstat()
    require(root.is_relative_to(T3/'scratch') and root.resolve()==root and info.st_uid==os.getuid()
            and stat.S_IMODE(info.st_mode)==0o700,'private prepared attempt root required')
    parent=subprocess.check_output(['/bin/ps','-p',str(os.getppid()),'-o','command='],text=True,timeout=2)
    require(str(T3/'tools/t3_slot_run.sh') in parent,'actual slot parent unavailable')
    require(not any((root/name).exists() for name in ('execution-started.json','actions.jsonl','artifact-check.json','slot-entry.json')),'attempt already used')
    admission=root/'admission.json';a=json.loads(admission.read_text())
    require(a['admission_version'] in ('chirality.native-B.retained-state/v2','chirality.native-B.retained-state/v3','chirality.native-B.retained-state/v4','chirality.native-B.retained-state/v5','chirality.native-B.retained-state/v6','chirality.native-B.retained-state/v7'),'explicit retained screen/AX profile required')
    require(sha(__file__)==a['slot_entry_sha256'],'slot-entry copy differs')
    controller=Path(a['controller_path'])
    require(controller.is_absolute() and controller.name=='native_successor_relaunch.py'
            and sha(controller)==a['dependencies'][str(controller)],'bound controller differs')
    acquired=datetime.now(timezone.utc);end=acquired+timedelta(seconds=295)
    command=[sys.executable,'-B',str(controller),'--execute',str(root),'--window-end',end.isoformat()]
    environment=dict(os.environ,CODEX_HOME=str(root/'codex-home'),PYTHONDONTWRITEBYTECODE='1')
    record={'at':acquired.isoformat(),'fixed_window_end':end.isoformat(),'allowance_seconds':295,
            'controller_pid':os.getpid(),'slot_parent_pid':os.getppid(),'slot_parent_command':parent.strip(),
            'admission_sha256':sha(admission),'slot_entry_sha256':sha(__file__),'command':command,
            'environment_overrides':{'CODEX_HOME':str(root/'codex-home'),'PYTHONDONTWRITEBYTECODE':'1'}}
    fd=os.open(root/'slot-entry.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'w') as stream:json.dump(record,stream,indent=2)
    os.execve(sys.executable,command,environment)
if __name__=='__main__':main()
