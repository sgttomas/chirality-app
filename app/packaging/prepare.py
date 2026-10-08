#!/usr/bin/env python3
"""Offline supplier staging and unsigned package input account; never build/sign/launch."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

from inventory import anchored, compare, inspect_signatures, scan, sha256

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parent.parent
LIMITS=[
    'Unsigned supplier staging only: no App package, installer, signing or notarisation produced.',
    'Copy comparison is not FP-1(a) after Tauri bundling or FP-1(b) after signing.',
    'FP-2/W-4 runtime full-distribution verification and M2/M3 native witnesses remain unperformed.',
    'SIGN-1 Option B selected; no reliance before actual FP-1(a/b) and FP-3 pass. OI-011 SWB part remains open.',
]


def parse_json(data):
    def unique(pairs):
        d={}
        for k,v in pairs:
            if k in d: raise ValueError(f'duplicate JSON field: {k}')
            d[k]=v
        return d
    return json.loads(data,object_pairs_hook=unique)


def read_json(path):
    return parse_json(Path(path).read_bytes())


def check_basis():
    pins=read_json(HERE/'sources.json')
    for name,digest in pins['sources'].items():
        if sha256((PROJECT/name).read_bytes())!=digest:
            raise ValueError(f'canonical packaging source changed: {name}')
    return sha256((HERE/'sources.json').read_bytes())


def inputs_account(path):
    raw=Path(path).read_bytes()
    config=parse_json(raw)
    allowed={'bundle_id','version','minimum_macos','signing_identity','notary_profile','app_binary','workflows','shipped_revision_manifest','guidance','role_files','role_set'}
    if not isinstance(config,dict) or set(config)-allowed:
        raise ValueError('input account contains unknown fields')
    if any(v is not None and (not isinstance(v,str) or not v.strip()) for v in config.values()):
        raise ValueError('each input is an explicit nonempty string or null')
    config={k:config.get(k) for k in sorted(allowed)}
    # These are reported choices only; this tool never adopts a production identity.
    if config['bundle_id'] and not re.fullmatch(r'[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+',config['bundle_id']):
        raise ValueError('invalid bundle identifier syntax')
    if config['minimum_macos'] and not re.fullmatch(r'[0-9]+\.[0-9]+(?:\.[0-9]+)?',config['minimum_macos']):
        raise ValueError('invalid minimum macOS syntax')
    items={}
    for name in ('app_binary','workflows','shipped_revision_manifest','guidance','role_files','role_set'):
        source=config[name]
        if source is None:
            items[name]={'state':'missing'}; continue
        source=anchored(source)
        if source.is_dir():
            if name not in ('workflows','role_files'): raise ValueError(f'{name} must be a file')
            tree=scan(source)
            if any(e['kind'] not in ('dir','file') for e in tree['entries']):
                raise ValueError(f'unsafe input tree: {name}')
            items[name]={'state':'inspected_not_staged','tree':tree}
        else:
            if name in ('workflows','role_files'): raise ValueError(f'{name} must be a directory')
            # Read a regular file without following a substituted link or blocking on a FIFO.
            fd=os.open(source,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
            try:
                start=os.fstat(fd)
                if not stat.S_ISREG(start.st_mode): raise ValueError(f'{name} must be a regular file')
                h=hashlib.sha256()
                while chunk:=os.read(fd,1024*1024): h.update(chunk)
                end=os.fstat(fd)
                if (start.st_size,start.st_mtime_ns,start.st_ctime_ns)!=(end.st_size,end.st_mtime_ns,end.st_ctime_ns):
                    raise ValueError(f'{name} mutated during read')
                items[name]={'state':'inspected_not_staged','source':str(source),'sha256':h.hexdigest(),'mode':oct(stat.S_IMODE(start.st_mode))}
            finally: os.close(fd)
    return {'declared':config,'items':items,'input_sha256':sha256(raw),
            'missing':[k for k,v in config.items() if v is None]}


def copy_supplier(inventory,destination):
    """Copy regular files from descriptor-anchored source paths and verify the result."""
    root=Path(inventory['root']); destination=Path(destination)
    destination.mkdir(parents=True,exist_ok=False)
    rootfd=os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        for entry in inventory['entries']:
            target=destination/entry['path']
            if entry['kind']=='dir':
                target.mkdir(); continue
            if entry['kind']!='file': raise ValueError('supplier contains a link or special file')
            fd=os.dup(rootfd)
            try:
                pieces=entry['path'].split('/')
                for part in pieces[:-1]:
                    nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd)
                    os.close(fd); fd=nxt
                source=os.open(pieces[-1],os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
                try:
                    if not stat.S_ISREG(os.fstat(source).st_mode): raise ValueError('supplier file type changed')
                    with target.open('xb') as writer:
                        while chunk:=os.read(source,1024*1024): writer.write(chunk)
                    target.chmod(int(entry['mode'],8))
                finally: os.close(source)
            finally: os.close(fd)
        # Set directory modes last so a read-only source tree can still be copied.
        for entry in reversed(inventory['entries']):
            if entry['kind']=='dir': (destination/entry['path']).chmod(int(entry['mode'],8))
        destination.chmod(int(inventory['root_mode'],8))
    finally: os.close(rootfd)
    copied=scan(destination)
    result=compare(copied,inventory)
    if not result['equal'] or not compare(scan(root),inventory)['equal']:
        raise ValueError('supplier changed or copied tree differs; staging incomplete')
    return copied,result


def prepare(vendor,expected_manifest,pin,revision,inputs,output):
    if not re.fullmatch(r'[0-9a-f]{64}',expected_manifest): raise ValueError('expected manifest must be a sha256')
    if not revision.strip(): raise ValueError('candidate revision is required')
    basis=check_basis(); inventory=scan(vendor)
    if not inventory['files'] or inventory['manifest_sha256']!=expected_manifest:
        raise ValueError('supplier manifest does not match the explicit expected identity')
    if any(e['kind'] not in ('dir','file') for e in inventory['entries']):
        raise ValueError('Option B supplier staging refuses links and special files')
    metadata=read_json(Path(inventory['root'])/'codex-package.json')
    expected={'layoutVersion':1,'version':pin,'target':'aarch64-apple-darwin','variant':'codex','entrypoint':'bin/codex','resourcesDir':'codex-resources','pathDir':'codex-path'}
    if metadata!=expected: raise ValueError('supplier package metadata does not match selected pin/layout/target')
    by_path={e['path']:e for e in inventory['entries']}
    if not (by_path.get('bin/codex',{}).get('macho') and int(by_path['bin/codex']['mode'],8)&0o111):
        raise ValueError('supplier entrypoint is not an executable Mach-O file')
    for name in ('codex-path','codex-resources'):
        if by_path.get(name,{}).get('kind')!='dir': raise ValueError(f'supplier missing {name}')
    account=inputs_account(inputs)
    output=anchored(output)
    # Never create staging inside a source, nor accept a reused output directory.
    sources=[Path(inventory['root'])]+[Path(v) for k,v in account['declared'].items() if k in account['items'] and v]
    if any(output==s or s in output.parents or output in s.parents for s in sources):
        raise ValueError('staging and inspected inputs must not overlap')
    output.mkdir(exist_ok=False)
    try:
        placed,comparison=copy_supplier(inventory,output/'bundle/Contents/Resources/codex')
        report={'format':'chirality.unsigned-supplier-preparation/1','candidate_revision':revision,
                'selected_pin':pin,'expected_supplier_manifest':expected_manifest,'source':inventory,'staged':placed,
                'staging_copy_comparison':comparison,'input_account':account,
                'configuration':{'CF-1':account['declared']['signing_identity'],'CF-2':'bundler signing disabled; no bundler invoked',
                    'CF-3':{'P-1':'bundle/Contents/Resources/codex','P-0':'not staged','P-2':'not staged','P-3':'not staged','P-4':'not generated'},
                    'CF-4':'planned: sign App code and outer bundle without --deep; not performed',
                    'CF-5':{k:account['declared'][k] for k in ('bundle_id','version','minimum_macos')},
                    'CF-6':'dmg planned, not built','CF-7':{'profile_name':account['declared']['notary_profile'],'state':'not submitted'},
                    'CF-8':'not stapled'},
                'package_complete':False,'first_package_checks':{k:'not-run' for k in ('fp0','fp1a','fp1b','fp2','fp3','fp4','fp5')},
                'source_manifest_sha256':basis,'implementation_sha256':{n:sha256((HERE/n).read_bytes()) for n in ('prepare.py','inventory.py')},'limits':LIMITS}
        with (output/'preparation.json.tmp').open('x') as writer:
            writer.write(json.dumps(report,indent=2)+'\n')
        (output/'preparation.json.tmp').replace(output/'preparation.json')
        return report
    except Exception:
        # Keep failure visible. No success report is published; do not remove user files.
        (output/'INCOMPLETE.txt').write_text('Preparation did not complete. Do not use this staging directory.\n')
        raise


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    inv=commands.add_parser('inventory'); inv.add_argument('tree'); inv.add_argument('--signature-display',action='store_true')
    prep=commands.add_parser('prepare')
    for field in ('vendor','expected-manifest','pin','candidate-revision','inputs','output'): prep.add_argument('--'+field,required=True)
    args=parser.parse_args(argv)
    try:
        if args.command=='inventory':
            basis=check_basis(); result=scan(args.tree)
            result.update(source_manifest_sha256=basis,limits=LIMITS)
            if args.signature_display: result['fp0']=inspect_signatures(result)
        else:
            result=prepare(args.vendor,args.expected_manifest,args.pin,args.candidate_revision,args.inputs,args.output)
        print(json.dumps(result,indent=2))
        return 1 if 'fp0' in result and result['fp0']['outcome']!='pass' else 0
    except (OSError,ValueError,subprocess.TimeoutExpired) as error:
        print(json.dumps({'error':str(error),'preparation_complete':False,'limits':LIMITS},indent=2))
        return 2


if __name__=='__main__':
    sys.exit(main())
