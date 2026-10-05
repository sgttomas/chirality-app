#!/usr/bin/env python3
"""Download only an explicitly owner-approved set; never invokes Cargo or installs."""
import argparse, hashlib, json, pathlib, subprocess
# The coordinator runs this only after the owner's actual approval is recorded.
p=argparse.ArgumentParser();p.add_argument('--stage',required=True);a=p.parse_args()
manifest=json.loads(pathlib.Path(__file__).with_name('DOWNLOAD_SET.json').read_text());stage=pathlib.Path(a.stage);stage.mkdir(parents=True,exist_ok=True)
for item in manifest['files']:
    if not item['url'].startswith('https://static.crates.io/crates/') or '/' in item['file']:
        raise SystemExit('Invalid source or filename')
    dest=stage/item['file'];pending=dest.with_suffix(dest.suffix+'.partial')
    if not dest.exists():
        subprocess.run(['curl','--fail','--silent','--show-error','--proto','=https','--output',str(pending),item['url']],check=True)
        data=pending.read_bytes()
        if len(data)!=item['bytes'] or hashlib.sha256(data).hexdigest()!=item['sha256']:
            raise SystemExit('Archive size/checksum mismatch: '+item['file'])
        pending.replace(dest)
    data=dest.read_bytes()
    if len(data)!=item['bytes'] or hashlib.sha256(data).hexdigest()!=item['sha256']:
        raise SystemExit('Existing stage artifact differs: '+item['file'])
    print('verified '+item['file']+' '+str(item['bytes']))
print('verified '+str(len(manifest['files']))+' files '+str(manifest['total_bytes'])+' bytes')
