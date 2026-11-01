"""Prepared attended entrypoint. Preparation and bridge commands are offline.

Native --execute requires a fresh exact manifest hash and actual slot ancestry;
no preparation, simulation, bridge message or CI result authorizes invocation.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime,timezone

# Explicit source directory under isolated Python; pycache is redirected to an empty prepared directory.
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))

from native_attended_bridge import publish,read,private_directory,delivery_receipt,owner_completion,ReceiptBridge
from native_attended_sequence import AttendedSequence

HERE=Path(__file__).resolve().parent
SCRATCH=Path('/Users/ryan/dev/chirality-t3/scratch')
CANDIDATE='1f67d3822b-8c83d74ae3ce'
PLAN_SHA='f0da12bb0b631d77ee94ce0b4abdc584c2077925b2ea6d60e03871230ae292a7'

def require(ok,message):
    if not ok:raise RuntimeError(message)

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        while data:=stream.read(1024*1024):h.update(data)
    return h.hexdigest()

def dependencies():
    paths=list(HERE.glob('native*.py'))+[HERE/'native_attended_manager.js',
        Path('/Users/ryan/dev/chirality-t3/tools/t3_slot.sh'),Path('/Users/ryan/dev/chirality-t3/tools/t3_slot_run.sh')]
    import native_successor_relaunch as b
    paths.extend(Path(p) for p in b.dependencies())
    return {str(p):sha(p) for p in sorted(set(paths))}

def load_identify():
    import importlib.util
    path=HERE.parents[3]/'app/examination/candidate_identity/identify.py'
    spec=importlib.util.spec_from_file_location('attended_identify',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def prepare(build_root,state_basis=None):
    from native_attended_admission import NativeAdmissions,preflight_a
    import native_successor_relaunch as b
    build_root=Path(build_root).resolve()
    require(build_root.is_relative_to(SCRATCH),'build root outside owned scratch')
    checked=preflight_a(build_root,PLAN_SHA,load_identify(),state_basis)
    require(checked['candidate']==CANDIDATE,'wrong selected candidate')
    root=Path(tempfile.mkdtemp(prefix='app-attended-prepared-',dir=SCRATCH)).resolve()
    for name in ('A','B','bridge','manager-home','bytecode-cache'):(root/name).mkdir(mode=0o700)
    admission=NativeAdmissions(root,build_root,PLAN_SHA,b,load_identify(),time.monotonic,state_basis)
    artifacts={}
    for label in ('A','B'):
        phase=root/label
        for name in ('codex-home','tmp','helper-tmp'):(phase/name).mkdir(mode=0o700)
        b.screen_support.w.stage(phase,admission.value['window_route'])
        policy=phase/'phase.sb';policy.write_text(admission.policy(label,phase));policy.chmod(0o600)
        for path in phase.iterdir():
            if path.is_file():artifacts[str(path.relative_to(root))]=sha(path)
    manifest={'format':'attended-prepared-entry/v1','run_id':uuid.uuid4().hex,'candidate':CANDIDATE,
        'build_root':str(build_root),'state_basis':state_basis,'plan_sha256':PLAN_SHA,'controller_root':str(root),'entry_source':str(Path(__file__).resolve()),
        'dependencies':dependencies(),'manager_function_sha256':hashlib.sha256(('async function'+(HERE/'native_attended_manager.js').read_text().split('(async function',1)[1]).rstrip().removesuffix(')').encode()).hexdigest(),'artifacts':artifacts,'A_preflight':checked,'total_seconds':295,
        'autonomous_focus_route':admission.value['autonomous_focus_route'],
        'Stop_entry_reserve':135,'launch_limit':2,'Stop_confirmation':False,'PR69_active':False,
        'interpreter':{'path':str(Path(sys.executable).resolve()),'sha256':sha(Path(sys.executable).resolve())},
        'native_executed':False,'prepared_at':datetime.now(timezone.utc).isoformat()}
    publish(root/'prepared.json',manifest)
    print(json.dumps({'root':str(root),'prepared_sha256':sha(root/'prepared.json'),'candidate':CANDIDATE,
                      'standing':'UNRUN; requires review, integration and coordinated start'}))
    return root

def check(root,expected_sha):
    root=private_directory(root)
    require(root.is_relative_to(SCRATCH),'prepared root outside scratch')
    require(sha(root/'prepared.json')==expected_sha,'prepared manifest differs')
    manifest=read(root/'prepared.json')
    require(manifest['controller_root']==str(root) and manifest['entry_source']==str(Path(__file__).resolve())
            and manifest['candidate']==CANDIDATE and manifest['plan_sha256']==PLAN_SHA
            and manifest['total_seconds']==295 and manifest['Stop_entry_reserve']==135
            and manifest['launch_limit']==2 and manifest['Stop_confirmation'] is False
            and manifest['PR69_active'] is False,'prepared scope differs')
    if manifest.get('state_basis') is not None:
        from native_attended_retained_shell import selected_profile
        descriptor=manifest['state_basis']
        require(set(descriptor)=={'path','sha256'},'retained basis descriptor changed')
        try:selected_profile(descriptor['path'],descriptor['sha256'])
        except RuntimeError as error:raise RuntimeError('retained basis descriptor changed') from error
        require(sha(Path(descriptor['path']))==descriptor['sha256'],'retained basis descriptor changed')
    require(manifest['interpreter']=={'path':str(Path(sys.executable).resolve()),'sha256':sha(Path(sys.executable).resolve())},'entry interpreter differs')
    require(manifest.get('autonomous_focus_route')=={'version':'autonomous-owned-focus/v1','per_incarnation_cap_seconds':45,'mechanism':'AXRaise+AXFrontmost'},'autonomous focus route binding differs')
    require(manifest['dependencies']==dependencies(),'controller/source dependency changed')
    for relative,digest in manifest['artifacts'].items():
        path=root/relative
        require(path.resolve()==path and path.is_relative_to(root) and sha(path)==digest,'prepared artifact changed')
    return manifest

def original_custody(ports):
    result=[]
    for label,run in ports.runs.items():
        reservation=run.reservation
        if reservation is not None and not reservation.reaped:result.append((label,'original-child'))
        if run.thread is not None and run.thread.is_alive():result.append((label,'guard'))
        try:
            if not run.extra_cleanup_ready():result.append((label,'helper-unknown'))
        except BaseException:result.append((label,'helper-unknown'))
    if ports.pending_launch is not None:result.append((ports.pending_launch,'launch-unknown'))
    return result

def supervise_held(ports,bridge,sequence,clock=time.monotonic,sleep=time.sleep):
    """No UI action after fixed end; no deadline extension or automatic relaunch.

    Late actual owner completion is retained. Original normal exit may be
    observed/reaped administratively once helpers settle; alive/unknown Child
    keeps this process and the slot in supervised hold. Parent receives exact
    required recovery (not a silent hours-long orphan). An explicit later owner
    disposition is necessary for UI work outside the original fixed interval.
    """
    state_store=getattr(sequence,'_held_state',None)
    if state_store is None:
        state_store={'last':None,'late':set(),'last_heartbeat':clock(),'dispositions':{},'errors':set(),'suppressed':False}
        sequence._held_state=state_store
    last=state_store['last'];late=state_store['late'];last_heartbeat=state_store['last_heartbeat']
    dispositions=state_store['dispositions'];reported_errors=state_store['errors']
    def new_error(key):
        if key in reported_errors:return False
        if len(reported_errors)>=20:
            if not state_store['suppressed']:
                state_store['suppressed']=True
                sequence.safe_record('supervision-error-cap',{'limit':20,'additional_errors_suppressed':True,'custody':'retained'})
            return False
        reported_errors.add(key);return True
    while True:
        held=original_custody(ports)
        if not held:return
        if clock()-last_heartbeat>=5:
            try:print(json.dumps({'event':'attended-held-heartbeat','held':held,'overrun':max(0,clock()-sequence.deadline)}),flush=True)
            except (BrokenPipeError,OSError):pass
            last_heartbeat=clock();state_store['last_heartbeat']=last_heartbeat
        # Terminal nonzero/signal observations get a concrete decision offer,
        # never local self-approval. One offer/receipt per original incarnation.
        from native_attended_disposition import offer,consume
        for label,kind in held:
            if kind!='original-child':continue
            try:
                if label not in dispositions:
                    selected=offer(ports,bridge,label)
                    event_id=bridge.emit({'event':'attended-terminal-disposition-needed','incarnation':label,
                        'fixed_end':sequence.deadline,'administrative_disposition_offer':selected,
                        'instruction':'Agent0 may issue the exact one-time exited-Child reap disposition; no signal or live action.'})
                    dispositions[label]=event_id
                consume(ports,bridge,label,dispositions[label])
            except Exception as error:
                key=(label,'disposition',str(error))
                if new_error(key):
                    sequence.safe_record('disposition-observation-'+str(len(reported_errors)),{'error':str(error),'incarnation':label})
        state=tuple(held)
        if state!=last:
            try:bridge.deliver({'event':'attended-held-supervision','incarnation':sequence.current,
                'held':held,'fixed_end':sequence.deadline,'overrun':max(0,clock()-sequence.deadline),
                'instruction':'Original custody retained. No new UI input after fixed end. If App remains alive, parent must deliver an explicit recovery disposition; no signals or blind clicks.'})
            except BaseException as error:
                try:print(json.dumps({'event':'attended-delivery-failed','error':str(error),'custody':'held'}),flush=True)
                except (BrokenPipeError,OSError):pass
            last=state;state_store['last']=last
        for label,kind in held:
            for completion_kind in ('cancel','foreground'):
                completion_key=label if completion_kind=='cancel' else label+':foreground'
                if completion_key not in late and completion_key in bridge.offers:
                    try:
                        completion=bridge.late_completion(label,completion_kind)
                        if completion:
                            late.add(completion_key)
                            ports.record('late-owner-'+completion_kind+'-completion-'+label,{'actual_reply':completion,'fixed_end':sequence.deadline,
                                'received_at_monotonic':clock(),'overrun':max(0,clock()-sequence.deadline),
                                'meaning':'late completion only; no deadline rearm, input continuation or presumed native state'})
                    except BaseException as error:
                        key=(label,completion_kind,str(error))
                        if new_error(key):
                            sequence.safe_record('late-completion-error-'+label+'-'+completion_kind,{'error':str(error)})
            run=ports.runs.get(label)
            if run is None:continue
            # Reap only the original exited child. Never call a live-PID action.
            if run.reservation is not None and not run.reservation.reaped:
                try:
                    observed=run.reservation.observe()
                    if ports.b.release_support.normal_exit(observed) and run.extra_cleanup_ready():
                        offered=ports.b.release_support.request_for(run)
                        require(offered is not None,'no exact current late release offer')
                        run.act_record('late-original-exit-release-intent.json',offered)
                        rc=run.reservation.administrative_reap(offered['expected_app_exit'])
                        run.act_record('late-original-exit-release-result.json',{'wait':rc,'success':False,'overrun':max(0,clock()-sequence.deadline)})
                except BaseException as error:
                    key=(label,'exit',str(error))
                    if new_error(key):
                        run.safe_log('held_exit_refusal',error=str(error))
            elif run.reservation is None:
                # A failed spawn with no returned Child remains unknown until
                # the launch port supplies an explicit failure/closure receipt.
                continue
            else:
                try:
                    run.sample()
                    if not run.observed_processes and run.extra_cleanup_ready():run.stop.set()
                except Exception as error:
                    key=(label,'residency',str(error))
                    if new_error(key):
                        run.safe_log('held_resource_uncertainty',error=str(error))
        sleep(.2)

def run_sequence(ports,bridge,slot_start,clock=time.monotonic,sleep=time.sleep):
    sequence=AttendedSequence(ports,clock)
    try:result=sequence.run(slot_start)
    except BaseException as error:
        sequence.result.update(witness_complete=False,error=repr(error),custody_held=True)
        result=sequence.result
    while original_custody(ports):
        try:supervise_held(ports,bridge,sequence,clock,sleep)
        except BaseException as error:
            message='supervision error; custody retained: '+repr(error)
            if message not in sequence.delivery_errors and len(sequence.delivery_errors)<20:sequence.delivery_errors.append(message)
            # Never turn observer/pipe/control failure into released custody.
            try:sleep(.2)
            except BaseException:pass
    result=dict(result,initial_custody_held=result.get('custody_held'),custody_held=bool(original_custody(ports)),
                resource_custody_closed=not original_custody(ports),
                final_elapsed=clock()-slot_start,final_overrun=max(0,clock()-(slot_start+295)))
    ports.record('attended-resource-closure',result)
    return result

def slot_acquisition(root):
    """Readonly wrapper ancestry/held-lock proof; log's second is conservative.

    The START record is emitted inside lockf after acquisition, before Python
    startup. Its rounded-down UTC second is used, counting startup/imports.
    """
    import re
    parent=os.getppid()
    row=subprocess.check_output(['/bin/ps','-p',str(parent),'-o','ppid=,uid=,command='],text=True,timeout=2).strip()
    fields=row.split(None,2)
    require(len(fields)==3 and int(fields[1])==os.getuid() and
            '/Users/ryan/dev/chirality-t3/tools/t3_slot_run.sh' in fields[2], 'actual slot runner parent unavailable')
    lock_pid=int(fields[0])
    command=subprocess.check_output(['/bin/ps','-p',str(lock_pid),'-o','command='],text=True,timeout=2).strip()
    match=re.search(r'/Users/ryan/dev/chirality-t3/guard/(cargo_job(?:\.slot[234])?\.lock)(?: |$)',command)
    require(command.startswith('/usr/bin/lockf ') and match,'lockf ancestor/slot unavailable')
    slot=Path('/Users/ryan/dev/chirality-t3/guard')/match.group(1)
    locks=subprocess.run(['/usr/sbin/lsof','-a','-p',str(lock_pid),'-F','pfnl','--',str(slot)],capture_output=True,text=True,timeout=3)
    require(locks.returncode==0 and 'p'+str(lock_pid) in locks.stdout.splitlines()
            and 'n'+str(slot) in locks.stdout.splitlines(),
            'original lockf slot descriptor not observed')
    import errno,fcntl
    fd=os.open(slot,os.O_RDWR|os.O_NOFOLLOW)
    try:
        info=os.fstat(fd)
        require(stat.S_ISREG(info.st_mode) and info.st_uid==os.getuid(),'slot leaf ownership differs')
        try:fcntl.lockf(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except OSError as error:
            require(error.errno in (errno.EACCES,errno.EAGAIN),'slot contention observation failed')
        else:
            fcntl.lockf(fd,fcntl.LOCK_UN)
            raise RuntimeError('slot was not held by wrapper; refuse')
    finally:os.close(fd)
    log=Path('/Users/ryan/dev/chirality-t3/guard/cargo_jobs.log')
    with log.open('rb') as stream:
        stream.seek(0,2);size=stream.tell();stream.seek(max(0,size-1024*1024));lines=stream.read().decode().splitlines()
    selected=[line for line in lines if ' START pid='+str(parent)+' slot='+slot.name+' ' in line and str(root) in line]
    require(selected,'current root-bound slot START record unavailable')
    started=datetime.strptime(selected[-1].split(' ',1)[0],'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc).timestamp()
    age=time.time()-started
    require(0<=age<30,'slot start stale; no budget reset')
    return time.monotonic()-age,started,{'parent_pid':parent,'lockf_pid':lock_pid,'slot':str(slot),
        'START_record':selected[-1],'lock_observation':locks.stdout,'nonblocking_contention':'EACCES/EAGAIN','clock_limit':'UTC log rounded down to second; conservatively counts Python startup'}

def execute(root,expected_sha):
    manifest=check(root,expected_sha);root=Path(root)
    require(not (root/'simulation-started.json').exists(),'simulation root cannot execute natively; reprepare')
    start=read(root/'coordinated-start.json')
    require(start.get('run_id')==manifest['run_id'] and start.get('prepared_sha256')==expected_sha
            and start.get('parent_start_message_id') and start.get('resource_concurrence_message_id')
            and start.get('manager_function_sha256')==manifest['manager_function_sha256'], 'coordinated start binding unavailable')
    acquired,wall,slot_proof=slot_acquisition(root)
    require(sys.flags.isolated and sys.pycache_prefix==str(root/'bytecode-cache')
            and not list((root/'bytecode-cache').iterdir()),'isolated interpreter/empty redirected bytecode required')
    publish(root/'mode.json',{'mode':'native','prepared_sha256':expected_sha})
    publish(root/'execution-started.json',{'acquired_monotonic':acquired,'acquired_utc':datetime.fromtimestamp(wall,timezone.utc).isoformat(),
        'fixed_end_utc':datetime.fromtimestamp(wall+295,timezone.utc).isoformat(),'prepared_sha256':expected_sha,'slot_proof':slot_proof})
    import native_successor_relaunch as b
    from native_attended_admission import NativeAdmissions
    from native_attended_ports import NativePorts
    admissions=NativeAdmissions(root,Path(manifest['build_root']),manifest['plan_sha256'],b,load_identify(),time.monotonic,manifest.get('state_basis'))
    bridge=ReceiptBridge(root,manifest['candidate'],manifest['run_id'],admissions)
    ports=NativePorts(b,root,admissions.value,admissions,bridge.deliver,bridge.completion)
    original_before=admissions.before_launch
    def before(label,receipt,end):
        check(root,expected_sha)
        original_before(label,receipt,end)
    admissions.before_launch=before
    result=run_sequence(ports,bridge,acquired)
    print(json.dumps({'event':'attended-final','result':result}),flush=True)
    return 0 if result.get('witness_complete') and result.get('resource_custody_closed') and not result.get('delivery_errors') else 1

def simulate(root,expected_sha):
    """Verify actual frozen prep, then exercise only invented in-process ports.

    This consumes the preparation for native use: simulation evidence and live
    evidence must never share an execution root. Reprepare after final review.
    """
    manifest=check(root,expected_sha)
    require(not (Path(root)/'execution-started.json').exists(),'cannot simulate a used native root')
    publish(Path(root)/'mode.json',{'mode':'simulation','prepared_sha256':expected_sha})
    publish(Path(root)/'simulation-started.json',{'simulation':True,'prepared_sha256':expected_sha,
        'candidate_not_launched':manifest['candidate']})
    from test_native_attended_entry import EntryTests
    results={}
    for scenario in ('normal','autonomous-flow','owner','delivery-failure','late-owner','nonzero-exit'):
        results[scenario]=EntryTests().exercise(scenario)
    publish(Path(root)/'simulation-result.json',{'simulation':True,'native_calls':0,'App_launches':0,
        'prepared_sha256':expected_sha,'cases':results,'standing':'offline entry/custody/bridge fixtures only'})
    print(json.dumps({'simulation':True,'cases':len(results),'root':str(root),'native_calls':0,'App_launches':0}))

def main():
    parser=argparse.ArgumentParser();sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('prepare');p.add_argument('--build-root',required=True);p.add_argument('--retained-basis');p.add_argument('--retained-sha256')
    for command in ('check','execute','simulate'):
        p=sub.add_parser(command);p.add_argument('--root',required=True);p.add_argument('--prepared-sha256',required=True)
    p=sub.add_parser('record-start');p.add_argument('--root',required=True);p.add_argument('--prepared-sha256',required=True);p.add_argument('--json',required=True)
    p=sub.add_parser('record-delivery');p.add_argument('--root',required=True);p.add_argument('--event-id',required=True);p.add_argument('--json',required=True)
    p=sub.add_parser('disposition');p.add_argument('--root',required=True);p.add_argument('--event-id',required=True);p.add_argument('--parent-message-id',required=True)
    p=sub.add_parser('owner-completion');p.add_argument('--root',required=True);p.add_argument('--event-id',required=True);p.add_argument('--actual-reply',required=True);p.add_argument('--owner-message-id',required=True)
    args=parser.parse_args()
    if args.command=='prepare':
        require(bool(args.retained_basis)==bool(args.retained_sha256),'both retained basis and digest required')
        prepare(args.build_root,{'path':args.retained_basis,'sha256':args.retained_sha256} if args.retained_basis else None)
    elif args.command=='check':print(json.dumps(check(args.root,args.prepared_sha256)))
    elif args.command=='simulate':simulate(args.root,args.prepared_sha256)
    elif args.command=='execute':return execute(args.root,args.prepared_sha256)
    elif args.command=='record-start':
        manifest=check(args.root,args.prepared_sha256);value=json.loads(args.json)
        require(value.get('run_id')==manifest['run_id'] and value.get('prepared_sha256')==args.prepared_sha256
                and value.get('manager_function_sha256')==manifest['manager_function_sha256']
                and value.get('parent_start_message_id') and value.get('resource_concurrence_message_id'),'start record differs')
        publish(Path(args.root)/'coordinated-start.json',value)
    elif args.command=='record-delivery':delivery_receipt(args.root,args.event_id,json.loads(args.json))
    elif args.command=='disposition':
        from native_attended_disposition import publish_disposition
        publish_disposition(Path(args.root),args.event_id,args.parent_message_id)
    elif args.command=='owner-completion':owner_completion(args.root,args.event_id,args.actual_reply,args.owner_message_id)
    return 0
if __name__=='__main__':raise SystemExit(main())
