"""Keeper-only typed C / Python AX comparison. No CLI/PID ingress or UI actions."""
import ctypes as C
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import time

HERE=Path(__file__).resolve()
spec=importlib.util.spec_from_file_location('typed_ax_python_reference',HERE.with_name('native_b_diagnostic.py'))
reference=importlib.util.module_from_spec(spec);spec.loader.exec_module(reference)
require=reference.require

class Ref(C.Structure):
    _fields_=[('type_id',C.c_uint64),('role_type_id',C.c_uint64),
              ('owner_rc',C.c_int32),('role_rc',C.c_int32),('timeout_rc',C.c_int32),('status',C.c_int32),
              ('self_equal',C.c_uint32),('duplicate',C.c_uint32),('role',C.c_char*128)]
class Attribute(C.Structure):
    _fields_=[('type_id',C.c_uint64),('value_rc',C.c_int32),('status',C.c_int32),
              ('reference_count',C.c_uint32),('reserved',C.c_uint32),('references',Ref*64)]
class Result(C.Structure):
    _fields_=[('abi_version',C.c_uint32),('byte_size',C.c_uint32),('attribute_count',C.c_uint32),('completed',C.c_uint32),
              ('status',C.c_int32),('application_owner_rc',C.c_int32),('application_pid',C.c_int32),('application_timeout_rc',C.c_int32),
              ('application_type_id',C.c_uint64),('attributes',Attribute*4)]

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def plain(path):
    path=Path(path);info=path.lstat()
    require(path.is_absolute() and path.parent.resolve()==path.parent and stat.S_ISREG(info.st_mode)
            and info.st_uid==os.getuid() and info.st_nlink==1 and not stat.S_IMODE(info.st_mode)&0o022,'typed AX input not plain/owned')
    return path

def private_root(root):
    root=Path(root);info=root.lstat()
    require(root.is_absolute() and root.resolve()==root and stat.S_ISDIR(info.st_mode)
            and info.st_uid==os.getuid() and stat.S_IMODE(info.st_mode)==0o700,'typed AX control root not private/owned')


def production_sources():
    return {str(p) for p in (HERE, HERE.with_name('native_b_diagnostic.py'),
            HERE.parent/'typed_ax/reader.c', HERE.parent/'typed_ax/reader.h', HERE.parent/'typed_ax/build.py')}


def source_binding(manifest):
    require(set(manifest['sources'])==production_sources(), 'exact production source set required')
    for path,digest in manifest['sources'].items():require(sha(plain(path))==digest,'typed AX source changed')


def stage_build(root, manifest_path, reviewed_manifest_sha, *, isolated_sources=False):
    """Copy checked code into the existing B sandbox-denied control root prelaunch.

    Returns the binding for a NEW admission; never edits an existing admission.
    No native library is loaded here.
    """
    root=Path(root);private_root(root)
    require(not any((root/n).exists() for n in ('admission.json','execution-started.json','actions.jsonl')), 'typed reader staging requires new pre-admission root')
    source=plain(manifest_path)
    require(sha(source)==reviewed_manifest_sha,'reviewed build manifest changed')
    manifest=json.loads(source.read_text())
    require(manifest['format']=='chirality.typed-ax-build/v1' and manifest['fixture_build'] is False, 'production typed AX build required')
    source_binding(manifest)
    original=plain(manifest['library']['path']);require(original.parent==source.parent,'typed library outside build root')
    raw=original.read_bytes();require(hashlib.sha256(raw).hexdigest()==manifest['library']['sha256'],'typed AX library changed')
    copied=root/'typed-ax-reader.dylib'
    descriptor=os.open(copied,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(descriptor,'wb') as stream:stream.write(raw)
    manifest['original_build_manifest']={'path':str(source),'sha256':sha(source)}
    if isolated_sources:
        # Relocate byte-identical reviewed sources for the isolated helper's
        # loader; preserve the original compiler manifest as provenance.
        relocated={}
        for original_path,digest in manifest['sources'].items():
            original_source=plain(original_path)
            relative=original_source.relative_to(HERE.parent)
            target=root/relative;target.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
            data=original_source.read_bytes();require(hashlib.sha256(data).hexdigest()==digest,'typed source changed while staging')
            if target.exists():require(sha(plain(target))==digest,'staged typed source collision')
            else:
                fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
                with os.fdopen(fd,'wb') as stream:stream.write(data)
            relocated[str(target)]=digest
        manifest['original_source_bindings']=manifest['sources']
        manifest['sources']=relocated
    manifest['library']={'path':str(copied),'sha256':hashlib.sha256(raw).hexdigest()}
    staged=root/'typed-ax-build.json'
    descriptor=os.open(staged,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(descriptor,'w') as stream:json.dump(manifest,stream,indent=2)
    return {'version':'chirality.typed-ax-build/v1','manifest':str(staged),'sha256':sha(staged)}


def load(manifest_path, expected_sha):
    """Manifest digest comes from a reviewed admission, never caller PID input."""
    manifest_path=plain(manifest_path)
    require(manifest_path.name=='typed-ax-build.json', 'protected typed AX manifest filename required')
    require(sha(manifest_path)==expected_sha,'typed AX build manifest changed')
    manifest=json.loads(manifest_path.read_text())
    require(manifest['format']=='chirality.typed-ax-build/v1','typed AX build format differs')
    require(manifest['fixture_build'] is False,'test library cannot observe native App')
    source_binding(manifest)
    library=plain(manifest['library']['path'])
    require(library.name=='typed-ax-reader.dylib' and library.parent==manifest_path.parent
            and sha(library)==manifest['library']['sha256'],'protected typed AX library changed')
    loaded=C.CDLL(str(library),mode=os.RTLD_LOCAL)
    loaded.chirality_ax_compare_size_v1.argtypes=[];loaded.chirality_ax_compare_size_v1.restype=C.c_uint32
    require(loaded.chirality_ax_compare_size_v1()==C.sizeof(Result),'typed C output ABI differs')
    loaded.chirality_ax_compare_v1.argtypes=[C.c_void_p,C.POINTER(Result)];loaded.chirality_ax_compare_v1.restype=C.c_int
    return loaded,manifest

def decode(result):
    require(result.abi_version==1 and result.byte_size==C.sizeof(Result) and result.attribute_count<=4,'typed AX result bounds/ABI invalid')
    attrs=[]
    for index in range(result.attribute_count):
        row=result.attributes[index];require(row.reference_count<=64,'typed AX references exceed bound')
        refs=[]
        for index2 in range(row.reference_count):
            r=row.references[index2]
            refs.append({'type_id':r.type_id,'role_type_id':r.role_type_id,'owner_return_code':r.owner_rc,
                         'role_return_code':r.role_rc,'timeout_return_code':r.timeout_rc,'status':r.status,
                         'application_self_reference':bool(r.self_equal),'duplicate_reference':bool(r.duplicate),
                         'role':bytes(r.role).decode('utf-8',errors='replace'),
                         'role_text_complete':r.status not in (1,5,6) and r.role_rc==0})
        attrs.append({'attribute':reference.AX_ATTRIBUTES[index],'type_id':row.type_id,'return_code':row.value_rc,
                      'status':row.status,'references':refs})
    return {'abi_version':result.abi_version,'status':result.status,'completed':bool(result.completed),
            'application_owner_return_code':result.application_owner_rc,'application_pid':result.application_pid,
            'application_timeout_return_code':result.application_timeout_rc,'application_type_id':result.application_type_id,
            'attributes':attrs}

def capture(run, backend_factory=reference.NativeBackend, loader=load):
    """Prepared process-local comparison; caller retains the original Child.

    No WindowServer call is made. Identity checks bracket both readers. Results
    are separate observations; agreement is not proof of an OS/App cause.
    """
    require(run.reservation is not None and not run.reservation.reaped and run.reservation.observe() is None,'original Child not live/unreaped')
    require(not run.reason and not run.log_errors,'typed AX skipped for stop/evidence reason')
    require(run.cleanup_end-time.monotonic()>=57,'typed AX cleanup headroom unavailable')
    binding=run.value.get('typed_ax_comparison')
    require(isinstance(binding,dict) and binding.get('version')=='chirality.typed-ax-build/v1', 'typed AX admission binding unavailable')
    private_root(run.root)
    admission_path=plain(Path(run.root)/'admission.json')
    require(sha(admission_path)==run.admission_sha and json.loads(admission_path.read_text())['inputs']['typed_ax_comparison']==binding, 'typed AX admission changed')
    manifest_path=Path(binding['manifest']);manifest_sha=binding['sha256']
    require(manifest_path.parent==Path(run.root) and manifest_path.name=='typed-ax-build.json', 'typed AX manifest must use protected control name/root')
    policy=plain(Path(run.root)/'phase-B.sb');admitted=json.loads(admission_path.read_text())
    require(sha(policy)==admitted['policy_sha256'] and '(deny file-read* file-write* (subpath '+json.dumps(str(run.root))+'))' in policy.read_text(), 'typed AX control sandbox binding unavailable')
    backend=backend_factory()
    try:
        before=reference.bound_identity(run,backend)
        library,manifest=loader(manifest_path,manifest_sha)
        require(not run.reason and run.reservation.observe() is None,'stop/exit before typed AX call')
        app=backend.app(before['pid'])
        root_rc,owner=backend.owner(app);require(root_rc==0 and owner==before['pid'],'owned AX application unavailable')
        started=reference.now();out=Result()
        rc=library.chirality_ax_compare_v1(app,C.byref(out))
        require(out.application_owner_rc==0 and out.application_pid==before['pid'],'typed AX original owner differs/unavailable')
        try:
            typed=decode(out)
        except Exception as error:
            typed={'available':False,'decode_error':str(error),'raw_result_sha256':hashlib.sha256(bytes(out)).hexdigest(),
                   'abi_version':out.abi_version,'byte_size':out.byte_size,'application_pid':out.application_pid,'status':out.status}
        require(reference.bound_identity(run,backend)==before,'original Child changed across C reader')
        deadline=time.monotonic()+4.0
        def check():
            require(not run.reason and run.reservation.observe() is None,'stop/exit during Python comparison')
            require(time.monotonic()<deadline,'Python AX comparison deadline')
        # Same retained local app object; Python conversion is not used by C.
        python={'at':reference.now(),'source':'per-attribute Python comparison','attributes':[]}
        try:
            for name in reference.AX_ATTRIBUTES:
                check()
                try:
                    part=reference.ax_inventory(backend,before['pid'],check,application=app,attributes=(name,))
                    python['attributes'].extend(part['attributes'])
                except Exception as error:
                    python['attributes'].append({'attribute':name,'available':False,'error':str(error)})
                    check()
        except Exception as error:
            python.update(available=False,error=str(error),finished_at=reference.now())
        after=reference.bound_identity(run,backend);require(after==before,'original Child changed across comparison')
        return {'format':'chirality.owned-typed-ax-comparison/v1','started_at':started,'finished_at':reference.now(),
                'candidate':run.value['candidate_key'],'admission_sha256':run.admission_sha,'identity_before':before,'identity_after':after,
                'build_manifest_sha256':manifest_sha,'library_sha256':manifest['library']['sha256'],
                'typed_call_return':rc,'typed_c':typed,'python':python,
                'limits':'Same owned App reference, sequential reads not atomic. C has3s intercall budget/0.5s element timeouts; Python4s intercall budget. No hard cancellation guarantee; an in-process native/FFI fault can kill the keeper and lose its supervision. completed means traversal completed, not success. No actions/WindowServer/permission requests. No automatic cause or qualification inference.'}
    finally:backend.close()
