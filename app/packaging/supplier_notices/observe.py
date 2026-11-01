"""Read exact retained 0.160.0 files for notice/source clues; execute nothing."""
import argparse
import hashlib
import importlib.util
import json
import os
import mmap
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('notice_input_reader', ROOT/'app/packaging/static_distribution/check.py')
reader = importlib.util.module_from_spec(spec); spec.loader.exec_module(reader)
SUBJECTS = {
 'bin/codex':'112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b',
 'bin/codex-code-mode-host':'679eedaea70529aa1cffc9bc0a0788c186412663544fa76c09d63b57f383a65a',
 'codex-path/rg':'7c7d5b09c3a57de864500c65dc2e9c4d2a5e96a3fc7b7d5318480c19887a739b',
 'codex-resources/zsh/bin/zsh':'d715e06edcf1661edb2e7767d65fbd1b44af505edfb217281b701f0a6ae93b15',
}
CLUES = {
 'bin/codex': [b'/Users/runner/work/codex/codex/codex-rs/'],
 'bin/codex-code-mode-host':[b'/Users/runner/work/codex/codex/codex-rs/',b'code-mode-host/src/main.rs'],
 'codex-path/rg':[b'\x0016.0.0\x00',b'\x0010.46 2025-08-27\x00'],
 'codex-resources/zsh/bin/zsh':[b'zsh-5.9.0.3-test-87-g77045ef',b'/usr/local/share/zsh/5.9.0.3-test/functions'],
}


def inspect(vendor):
    vendor = Path(vendor).absolute()
    manifest_path = vendor/'codex-resources/voice/manifest.json'
    raw, digest, size = reader.transfer(manifest_path, retain=True)
    manifest = reader.parse(raw)
    rows=[]
    for name, expected in SUBJECTS.items():
        # Existing no-follow reader streams binary hashes; retain bytes only for
        # these explicitly named supplier inputs, never arbitrary user files.
        path = vendor/name
        actual = reader.transfer(path)[1]
        reader.require(actual == expected, 'supplier subject digest mismatch: '+name)
        fd=os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        try:
            metadata=os.fstat(fd)
            reader.require(stat.S_ISREG(metadata.st_mode) and metadata.st_nlink==1 and metadata.st_size<=512*1024*1024, 'invalid supplier file')
            with mmap.mmap(fd,0,access=mmap.ACCESS_READ) as view: data=view[:]
        finally:
            os.close(fd)
        reader.require(hashlib.sha256(data).hexdigest()==expected, 'supplier changed during clue capture')
        clues=[]
        for pattern in CLUES[name]:
            offsets=[]; start=0
            while (index:=data.find(pattern,start))!=-1:
                offsets.append(index);start=index+len(pattern)
            reader.require(bool(offsets), 'named binary clue absent')
            clues.append({'bytes_hex':pattern.hex(),'text':pattern.decode('ascii'),'offsets':offsets})
        rows.append({'path':name,'sha256':actual,'size':len(data),'manifest_binding':manifest['sha256'].get(name),
                     'manifest_declared_build_commit':manifest['buildCommit'] if manifest['sha256'].get(name)==actual else None,
                     'embedded_clues':clues,'standing':'exact byte observations; embedded strings are not authenticated source/build/license provenance'})
        reader.require(reader.transfer(path)[1]==actual,'supplier changed after inspection')
    reader.require(reader.transfer(manifest_path)[1]==digest,'manifest changed after inspection')
    return {'format':'supplier-notice-source-observations/1','supplier_pin':'0.160.0','target':'aarch64-apple-darwin',
            'manifest':{'path':'codex-resources/voice/manifest.json','sha256':digest,'size':size,'buildCommit':manifest['buildCommit']},
            'components':rows,'limits':['No supplier execution, network, source acquisition, signature inspection or legal conclusion.',
                'A manifest declaration binds main bytes to its declared commit; it does not supply that source or applicable notice texts.',
                'Version/build strings narrow the missing-source search; they do not authenticate a release artifact or downstream patch set.']}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('vendor');args=parser.parse_args()
    print(json.dumps(inspect(args.vendor),indent=2))
