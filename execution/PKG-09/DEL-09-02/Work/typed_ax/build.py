"""Offline slot-wrapped build of a tiny local observer and harmless fixture."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,subprocess
HERE=Path(__file__).resolve().parent
T3=Path('/Users/ryan/dev/chirality-t3')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(command,env):
    result=subprocess.run(command,env=env,capture_output=True,text=True,timeout=60)
    if result.returncode:raise RuntimeError(result.stderr[:10000])
    return result.stdout

def build(root):
    if not root.is_relative_to(T3/'scratch') or root.exists():raise RuntimeError('new task scratch build directory required')
    parent=subprocess.check_output(['/bin/ps','-p',str(os.getppid()),'-o','command='],text=True,timeout=2)
    if str(T3/'tools/t3_slot_run.sh') not in parent:raise RuntimeError('guarded slot parent required')
    root.mkdir(mode=0o700);(root/'tmp').mkdir(mode=0o700);(root/'codex-home').mkdir(mode=0o700)
    env={'HOME':str(Path.home()),'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','TMPDIR':str(root/'tmp'),'CODEX_HOME':str(root/'codex-home')}
    sdk=Path(run(['/usr/bin/xcrun','--show-sdk-path'],env).strip()).resolve()
    compiler=Path(run(['/usr/bin/xcrun','--find','clang'],env).strip()).resolve()
    version=run([str(compiler),'--version'],env)
    headers=[sdk/'System/Library/Frameworks/ApplicationServices.framework/Frameworks/HIServices.framework/Headers'/n for n in ('AXUIElement.h','AXError.h')]
    headers += [sdk/'System/Library/Frameworks/CoreFoundation.framework/Headers'/n for n in ('CFBase.h','CFArray.h','CFString.h','CFNumber.h')]
    sources=[HERE/'reader.c',HERE/'reader.h',HERE/'build.py',HERE.parent/'native_b_typed_ax.py',HERE.parent/'native_b_diagnostic.py']
    for fixture in (False,True):
        name='fixture' if fixture else 'reader';library=root/(name+'.dylib')
        selected=sources+([HERE/'fixture.c',HERE/'fixture_api.h'] if fixture else [])
        command=[str(compiler),'-isysroot',str(sdk),'-dynamiclib','-std=c11','-O2','-Wall','-Wextra','-Werror']
        if fixture:command+=['-DAX_COMPARE_TEST',str(HERE/'fixture.c')]
        command += [str(HERE/'reader.c'),'-framework','ApplicationServices','-framework','CoreFoundation','-o',str(library)]
        started=datetime.datetime.now(datetime.timezone.utc).isoformat();stdout=run(command,env)
        record={'format':'chirality.typed-ax-build/v1','fixture_build':fixture,'started_at':started,
                'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':command,'environment':env,
                'compiler':{'path':str(compiler),'sha256':sha(compiler),'version':version},
                'sdk':{'path':str(sdk),'settings_sha256':sha(sdk/'SDKSettings.json'),'headers':{str(p):sha(p) for p in headers}},
                'sources':{str(p):sha(p) for p in selected},'library':{'path':str(library),'sha256':sha(library)},
                'stdout':stdout,'exit_code':0,'limits':'Local offline observation-library build only. Production reader not invoked; fixture uses no real AX service. No App build/launch, download or manual signing.'}
        with (root/(name+'-build.json')).open('x') as f:json.dump(record,f,indent=2)
    print(root)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args();build(a.output.absolute())
