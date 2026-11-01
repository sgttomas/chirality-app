"""Fresh candidate/invented-input preflight. Never makes saved state or a ledger.

A passing A preflight is not B admission or permission to launch. B requires
actual ordinary setup and original A closure, followed by read-only state checks.
"""
import hashlib
import json
import os
from pathlib import Path
import stat


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        while chunk := stream.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def plain(path, directory=False):
    path = Path(path)
    require(path.is_absolute() and path.resolve() == path, 'linked/nonabsolute admission path')
    info = path.lstat()
    require(info.st_uid == os.getuid() and (stat.S_ISDIR(info.st_mode) if directory else
            stat.S_ISREG(info.st_mode) and info.st_nlink == 1), 'foreign/nonplain admission input')
    return info


def preflight_a(root, expected_plan_sha, identify):
    root = Path(root); plain(root, True)
    plan_path = root / 'witness-inputs/input-plan.json'; plain(plan_path)
    require(sha(plan_path) == expected_plan_sha, 'invented input plan changed')
    plan = json.loads(plan_path.read_bytes())
    require(plan['format'] == 'attended-invented-input-plan/v1' and plan['launch_ready'] is False
            and plan['saved_A'] is None and plan['ledger'] is None and plan['launch_limit'] == 2
            and plan['total_seconds'] == 295 and plan['minimum_remaining_before_Stop'] == 135
            and plan['Stop_confirmation_allowed'] is False and plan['PR69_active'] is False,
            'unexpected attended input scope')
    plain(root / 'build-observation.json')
    observed = json.loads((root / 'build-observation.json').read_bytes())
    require(observed['candidate_key'] == plan['candidate'] and observed['source_revision'] == plan['source_revision']
            and observed['build_identity'] == plan['build_identity'] and observed['identifier'] == plan['identifier'],
            'candidate/input identities differ')
    bundle = Path(observed['bundle']); plain(bundle, True)
    require(bundle.is_relative_to(root / 'target/debug/bundle/macos'), 'bundle outside exact prepared root')
    require(identify.identity(identify.inventory(bundle)) == plan['build_identity'], 'fresh full bundle inventory differs')
    require(plan.get('build_profile') == 'debug' and plan.get('features') == ['custom-protocol'],
            'ordinary owner-use route requires exact debug/default distribution selection')
    invocation=root/'build-invocation.json';plain(invocation)
    require(sha(invocation)==plan['build_invocation_sha256'],'build provenance changed')
    build=json.loads(invocation.read_bytes())
    require(build['exit_code']==0 and build['profile']=='debug' and build['features']==['custom-protocol']
            and '--debug' in build['command'] and build['source_revision']==plan['source_revision'],
            'compiled owner-use route evidence differs')
    executable = Path(plan['executable']); plain(executable)
    require(executable.is_relative_to(bundle / 'Contents/MacOS') and sha(executable) == plan['executable_sha256'],
            'candidate executable differs')
    expected = {'shared_config':'shared/config.toml','shared_agents':'shared/AGENTS.md',
                'shared_skills':'shared/skills','project':'project'}
    require(plan['input_paths'] == {k:str(root/'witness-inputs'/v) for k,v in expected.items()}, 'invented paths differ')
    require(set(plan['files']) == {'shared/config.toml','shared/AGENTS.md'}, 'unexpected fixture files')
    for relative,digest in plan['files'].items():
        path=root/'witness-inputs'/relative;plain(path)
        require(sha(path)==digest, 'invented input bytes changed')
    for name in ('fallback-codex-home','tmp'):
        path=root/'witness-inputs'/name;plain(path,True)
        require(not list(path.iterdir()), 'fallback home/tmp not empty; no auth read permitted')
    for key in ('shared_skills','project'):
        path=Path(plan['input_paths'][key]);plain(path,True)
        require(not list(path.iterdir()), 'invented input directory not empty')
    namespaces=identify.app_data_state(plan['identifier'])
    for relative in ('Library/Preferences/'+plan['identifier']+'.plist',
                     'Library/Saved Application State/'+plan['identifier']+'.savedState',
                     'Library/HTTPStorages/'+plan['identifier']):
        require(not os.path.lexists(Path.home()/relative), 'additional candidate namespace exists; preserve/reassess')
    require(not namespaces['present_at_identification'], 'candidate namespace no longer empty; preserve and reassess')
    return {'kind':'empty-candidate-A-preflight','candidate':plan['candidate'],'plan_sha256':expected_plan_sha,
            'namespace':namespaces,'B_admitted':False,'saved_A':None,'launch_authorized':False,
            'limits':'Guard/slot/current review and actual setup/closure still required; no native observation.'}


def require_setup_only_ledger_absent(app_data):
    """Initial setup has no configured host/namespace ledger; never invent rows.

    NewHome saves pending references only and does not reconfigure current
    owners. Unexpected ledger evidence requires inspection, not flexible rows.
    """
    runtime=Path(app_data)/'runtime'
    for name in ('recovery.ledger.jsonl','recovery.ledger.sqlite'):
        for suffix in ('','-wal','-shm','-journal'):
            require(not os.path.lexists(runtime/(name+suffix)), 'unexpected initial setup ledger/sidecar; preserve and assess')


def validate_saved_setup(request, account, value, saved_sha):
    """Read the actual ordinary saved request after A closure; supplier opaque.

    Fresh descriptor/source references must match each declared input. This
    does not manufacture a ledger or predict B's runtime generation.
    """
    import importlib.util
    path=Path(__file__).with_name('native_setup_continuation.py')
    spec=importlib.util.spec_from_file_location('attended_setup_validator',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    request=Path(request);account=Path(account)
    plain(request);plain(account,True)
    before=request.stat()
    raw,record=module.validate_request(request,account,value)
    require(hashlib.sha256(raw).hexdigest()==saved_sha,'actual saved request changed after A closure')
    after=request.stat()
    stamp=lambda s:tuple(getattr(s,k) for k in ('st_dev','st_ino','st_mode','st_uid','st_nlink','st_size','st_mtime_ns','st_ctime_ns'))
    require(stamp(before)==stamp(after),'saved request changed during readmission')
    require_setup_only_ledger_absent(value['expected_app_data'])
    for name,key in [('config.toml','shared_config'),('AGENTS.md','shared_agents'),('skills','shared_skills')]:
        link=account/name
        require(link.is_symlink() and link.resolve(strict=True)==Path(value['native_input_paths'][key]),
                'saved account link changed')
    return {'request_sha256':saved_sha,'account':str(account),'ledger_standing':'absent setup-only',
            'saved_reference_record':record,'B_generation':'not observed; requires fresh native ready'}


class NativeAdmissions:
    """Fixed prepared-root validator; never synthesizes A's saved state.

    Prepared manifest and runtime receipts are distinct. Before-launch checks
    revalidate full bundle and exact sources; new state is read only after A
    closure. The actual native entrypoint must supply/check the slot start.
    """
    def __init__(self, root, build_root, plan_sha, b, identify, clock):
        self.root,self.build_root=Path(root),Path(build_root)
        self.plan_sha,self.b,self.identify,self.clock=plan_sha,b,identify,clock
        self.plan=json.loads((self.build_root/'witness-inputs/input-plan.json').read_bytes())
        self.observed=json.loads((self.build_root/'build-observation.json').read_bytes())
        self.saved=None;self.births={};self.receipts={}
        self.value={'candidate_key':self.plan['candidate'],'bundle_identifier':self.plan['identifier'],
            'bundle':self.observed['bundle'],'executable':self.plan['executable'],
            'executable_sha256':self.plan['executable_sha256'],
            'expected_app_data':str(Path.home()/'Library/Application Support'/self.plan['identifier']),
            'native_input_paths':dict(self.plan['input_paths']),
            'files':dict(self.plan['files']),'window_route':b.screen_support.w.configuration()}

    def environment(self,label):
        phase=self.root/label
        return {'HOME':str(Path.home()),'PATH':str(Path(self.value['bundle'])/'Contents/Resources/codex/codex-path')+':/usr/bin:/bin:/usr/sbin:/sbin',
                'LANG':'en_US.UTF-8','CODEX_HOME':str(phase/'codex-home'),'TMPDIR':str(phase/'tmp')}

    def policy(self,label,phase):
        result=self.b.policy(self.value,phase)
        if label=='A':result=result.replace('(allow process-fork)','(deny process-fork)')
        for path in (self.build_root,Path(__file__).resolve().parents[4]):
            result+='(deny file-write* (subpath '+json.dumps(str(path))+'))\n'
        return result

    def _receipt(self,label,facts):
        path=self.root/label/'admission.json'
        record={'format':'attended-native-admission/v1','incarnation':label,'candidate':self.plan['candidate'],
                'plan_sha256':self.plan_sha,'facts':facts,'policy_sha256':hashlib.sha256(self.policy(label,self.root/label).encode()).hexdigest()}
        self.b.write_once(path,record)
        receipt={'admission_id':label+':'+sha(path),'admission_sha256':sha(path),**facts}
        self.receipts[label]=receipt
        return receipt

    def empty(self,end):
        require(self.clock()<end-135,'A admission missed setup budget')
        self.recheck_inputs()
        return self._receipt('A',preflight_a(self.build_root,self.plan_sha,self.identify))

    def recheck_inputs(self):
        require(sha(self.build_root/'witness-inputs/input-plan.json')==self.plan_sha,'prepared input plan changed')
        for relative,digest in self.plan['files'].items():
            path=self.build_root/'witness-inputs'/relative;plain(path)
            require(sha(path)==digest,'invented inputs changed')
        for key in ('project','shared_skills'):
            path=Path(self.plan['input_paths'][key]);plain(path,True)
            require(not list(path.iterdir()),'invented directory acquired activity')
        return self.value

    def saved_after_closure(self,a,saved,closure,end):
        require(closure.get('normal_exit')==0 and closure.get('helpers_settled') is True
                and closure.get('reaped') is True and closure.get('released') is True,
                'A original custody not closed before state admission')
        self.recheck_inputs()
        request=Path(self.value['expected_app_data'])/'desktop-startup/request.json'
        account=Path(saved['account'])
        require(account.parent==Path(self.value['expected_app_data'])/'account-homes','saved account outside exact namespace')
        proof=validate_saved_setup(request,account,self.value,saved['request_sha256'])
        require(set(p.name for p in account.iterdir())=={'config.toml','AGENTS.md','skills'},'unexpected account content; no reads permitted')
        require(list(account.parent.iterdir())==[account],'unexpected additional account')
        require(set(p.name for p in request.parent.iterdir())=={'request.json'},'unexpected pending startup artifacts')
        # Full namespace metadata remains opaque except the explicit request.
        from native_b_retained import metadata
        links={str(account/name):self.value['native_input_paths'][key]
               for name,key in [('config.toml','shared_config'),('AGENTS.md','shared_agents'),('skills','shared_skills')]}
        roots={'AppData':Path(self.value['expected_app_data'])}
        for name,relative in [('WebKit','Library/WebKit'),('Caches','Library/Caches'),
                              ('SavedState','Library/Saved Application State'),('HTTPStorages','Library/HTTPStorages')]:
            suffix='.savedState' if name=='SavedState' else ''
            path=Path.home()/relative/(self.plan['identifier']+suffix)
            if os.path.lexists(path):roots[name]=path
        proof['opaque_metadata']=metadata(roots,links)
        require(self.clock()<end,'actual saved-state admission exceeded cutoff')
        self.saved=saved
        self.value['expected_generation_home']='app-home:'+hashlib.sha256(os.fsencode(account)).hexdigest()
        return self._receipt('B',{'fresh_after_closure':True,'a_release_id':closure['release_id'],
            'request_sha256':saved['request_sha256'],'account':str(account),'ledger_standing':'absent setup-only',
            'actual_state':proof})

    def before_launch(self,label,admission,end):
        require(admission==self.receipts.get(label),'current incarnation admission differs')
        self.recheck_inputs()
        require(self.identify.identity(self.identify.inventory(Path(self.value['bundle'])))==self.plan['build_identity'],
                'fresh full bundle changed before launch')
        require(self.clock()<end-135,'launch missed combined setup/readiness cutoff')
        phase=self.root/label
        for directory in ('tmp','helper-tmp','codex-home'):
            plain(phase/directory,True);require(not list((phase/directory).iterdir()),'phase scratch not empty')
        for filename,digest in self.value['window_route']['helper_sources'].items():
            require(sha(phase/filename)==digest,'phase helper source changed')
        require((phase/'phase.sb').read_text()==self.policy(label,phase),'phase sandbox policy changed')
        if label=='B':
            require(self.saved is not None,'B has no actual A setup')
            validate_saved_setup(Path(self.value['expected_app_data'])/'desktop-startup/request.json',
                                 Path(self.saved['account']),self.value,self.saved['request_sha256'])

    def bind_birth(self,label,run):
        backend=self.b.screen_support.w.d.NativeBackend()
        try:self.births[label]=self.b.screen_support.w.d.bound_identity(run,backend)
        finally:backend.close()
        require(label!='B' or self.births['B']!=self.births['A'],'B reused original Child birth')

    def check_birth(self,label,run):
        # Exited Child remains reserved; normal-exit verification belongs to the
        # keeper. This method is only for actions requiring a still-live Child.
        backend=self.b.screen_support.w.d.NativeBackend()
        try:require(self.b.screen_support.w.d.bound_identity(run,backend)==self.births[label],
                    'original Child birth/executable binding changed')
        finally:backend.close()
