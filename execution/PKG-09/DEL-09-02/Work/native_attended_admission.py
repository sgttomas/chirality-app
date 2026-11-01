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
    require(bundle.is_relative_to(root / 'target/release/bundle/macos'), 'bundle outside exact prepared root')
    require(identify.identity(identify.inventory(bundle)) == plan['build_identity'], 'fresh full bundle inventory differs')
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
