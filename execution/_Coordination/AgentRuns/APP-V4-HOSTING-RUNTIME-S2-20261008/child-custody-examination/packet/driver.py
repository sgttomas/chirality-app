#!/usr/bin/env python3
"""Temporary receipt driver. No subprocess context managers or signal cleanup."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
PLAN = Path('/private/tmp/CHILD_CUSTODY_EXAMINATION_PLAN.md')
PLAN_SHA = '2d6c6bf3eaee7f6e05a9b893e0afaa41f27859a3b3d1db8dac4af4c436f3ef7f'
BASIS = 'bf795b99d1f7093178b41ca93e638450eca2d8e0'
COMPILE = ['/usr/bin/clang', '-std=c11', '-Wall', '-Wextra', '-Werror', '-pthread', str(ROOT/'examine.c'), '-o', str(ROOT/'examine')]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(name, value):
    with (ROOT/name).open('x') as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())

def event(**value):
    value['monotonic'] = time.monotonic()
    with (ROOT/'process-ledger.jsonl').open('a') as f:
        f.write(json.dumps(value, sort_keys=True)+'\n')
        f.flush()
        os.fsync(f.fileno())

def frozen(expected):
    path = ROOT/'SOURCE_FREEZE.json'
    if sha(path) != expected:
        raise RuntimeError('reviewed freeze digest mismatch')
    f = json.loads(path.read_text())
    if f['basis'] != BASIS or f['compileArgv'] != COMPILE or sha(PLAN) != PLAN_SHA:
        raise RuntimeError('basis, argv or plan changed')
    for name, digest in f['sourceSha256'].items():
        if name not in ('examine.c', 'driver.py') or sha(ROOT/name) != digest:
            raise RuntimeError('source bytes changed')
    if set(f['sourceSha256']) != {'examine.c', 'driver.py'}:
        raise RuntimeError('incomplete freeze')
    return f

def child(argv, label, timeout):
    # Regular files avoid output-pipe deadlock. Popen is deliberately not a context
    # manager; no run(timeout), terminate, kill or implicit wait-on-exit cleanup.
    with (ROOT/(label+'.stdout')).open('xb') as out, (ROOT/(label+'.stderr')).open('xb') as err:
        proc = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                cwd=ROOT, env={**os.environ, 'TMPDIR': str(ROOT)}, close_fds=True)
        event(event='directChildCreated', role=label, pid=proc.pid, argv=argv, timeoutSeconds=timeout)
        try:
            code = proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            event(event='directChildTimeout', role=label, pid=proc.pid, disposition='unresolved-no-signal-no-next-mode')
            # A passive window can produce a direct-helper wait result; it never
            # proves the native helper's own child was reaped.
            time.sleep(6)
            code = proc.poll()
            event(event='passiveGraceEnded', role=label, pid=proc.pid, directHelperReturnCode=code,
                  childCleanupClaim=False)
            return {'argv': argv, 'pid': proc.pid, 'timedOut': True, 'returnCode': code}
        event(event='directChildWaited', role=label, pid=proc.pid, returnCode=code)
        return {'argv': argv, 'pid': proc.pid, 'timedOut': False, 'returnCode': code}

def records(name):
    return [json.loads(line) for line in (ROOT/name).read_text().splitlines() if line]

def native_valid(rows):
    made = [r for r in rows if r['event']=='childCreated']
    result = [r for r in rows if r['event']=='nativeResult']
    if len(made)!=1 or len(result)!=1 or not result[0]['pass'] or not result[0]['exactChildReaped']:
        return False
    pid = made[0]['pid']
    if pid<=0 or result[0]['child']!=pid:
        return False
    obs = [r for r in rows if r['event']=='waitid']
    live = [r for r in obs if r['phase']=='live-held-at-release']
    terminal = [r for r in obs if r['phase']=='terminal-first' and r['siPid']!=0]
    repeat = [r for r in obs if r['phase']=='terminal-repeat']
    consume = [r for r in rows if r['event']=='consume']
    after = [r for r in rows if r['event']=='afterConsume']
    import errno
    return (len(live)==len(terminal)==len(repeat)==len(consume)==len(after)==1
            and live[0]['return']==0 and live[0]['siPid']==0
            and all(r['target']==pid for r in obs+consume+after)
            and terminal[0]['return']==repeat[0]['return']==0
            and terminal[0]['siPid']==repeat[0]['siPid']==pid
            and terminal[0]['siStatus']==repeat[0]['siStatus']==37
            and terminal[0]['siCode']==repeat[0]['siCode']
            and consume[0]['return']==pid
            and after[0]['return']==-1 and after[0]['errno']==errno.ECHILD
            and not any(r['event']=='cleanupWait' for r in rows))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['compile', 'run'])
    parser.add_argument('--freeze-sha256', required=True)
    args = parser.parse_args()
    frozen(args.freeze_sha256)
    if ROOT.is_symlink() or not str(ROOT).startswith('/private/tmp/child-custody-examination-'):
        raise RuntimeError('wrong owned output root')
    # Exclusive marker prevents accidental rerun/overwrite, including a failed run.
    save(args.phase+'-started.json', {'phase':args.phase, 'sourceFreezeSha256':args.freeze_sha256,
                                     'driverArgv':sys.argv, 'basis':BASIS,
                                     'kernelRelease':os.uname().release,
                                     'kernelVersion':os.uname().version,
                                     'machine':os.uname().machine,
                                     'python':sys.version, 'pythonExecutable':sys.executable,
                                     'pythonExecutableSha256':sha(Path(sys.executable)),
                                     'environmentRecorded':{'TMPDIR':str(ROOT)}})
    if args.phase=='compile':
        if (ROOT/'examine').exists():
            raise RuntimeError('executable output already exists')
        r = child(COMPILE, 'compile', 30)
        r['pass'] = not r['timedOut'] and r['returnCode']==0
        r['compilerSha256'] = sha(Path('/usr/bin/clang'))
        r['sourceFreezeSha256'] = args.freeze_sha256
        r['executableSha256'] = sha(ROOT/'examine') if r['pass'] else None
        save('compile-receipt.json', r)
        return 0 if r['pass'] else 1
    compiled = json.loads((ROOT/'compile-receipt.json').read_text())
    if not compiled['pass'] or compiled['sourceFreezeSha256']!=args.freeze_sha256 or sha(ROOT/'examine')!=compiled['executableSha256']:
        raise RuntimeError('compiled source/executable mismatch')
    native = child([str(ROOT/'examine'), 'native'], 'native', 20)
    try:
        native['pass'] = not native['timedOut'] and native['returnCode']==0 and native_valid(records('native.stdout'))
    except (ValueError, KeyError, TypeError) as exc:
        native['pass'] = False
        native['recordValidationFailure'] = str(exc)
    save('native-receipt.json', native)
    if not native['pass']:
        # Also pause on a native failure without direct-helper timeout if the
        # exact fixture reap was never established. No additional helper launch.
        if not native['timedOut']:
            time.sleep(6)
        save('RESULT.json', {'pass':False, 'native':native, 'model':'not-started',
                            'standing':'synthetic-examination-failed-no-production-inference'})
        return 1
    model = child([str(ROOT/'examine'), 'model'], 'model', 15)
    rows = records('model.stdout') if not model['timedOut'] else []
    schedules = [r for r in rows if r['event']=='modelScheduleResult']
    model['pass'] = (not model['timedOut'] and model['returnCode']==0 and len(schedules)==2
                     and all(r['pass'] for r in schedules)
                     and schedules[0]['wrongIdentitySignals']==0 and schedules[1]['wrongIdentitySignals']==1
                     and any(r['event']=='modelResult' and r['pass'] for r in rows))
    save('model-receipt.json', model)
    frozen(args.freeze_sha256)
    save('RESULT.json', {'pass':model['pass'], 'native':native, 'model':model,
                        'sourceFreezeSha256':args.freeze_sha256,
                        'executableSha256':sha(ROOT/'examine'),
                        'standing':'temporary-synthetic-observation-only-no-production-support-or-PGID-custody-proof'})
    # All outputs are now closed; this manifest intentionally excludes itself.
    save('OUTPUT_MANIFEST.json', {p.name:sha(p) for p in sorted(ROOT.iterdir()) if p.is_file()})
    return 0 if model['pass'] else 1

if __name__=='__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        event(event='driverFailure', error=str(exc), nextModeProhibited=True)
        raise
