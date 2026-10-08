#!/usr/bin/env python3
"""Read-only Codex tree inventory; never execute code from the inspected tree."""
import hashlib
import json
import os
from pathlib import Path
import plistlib
import stat
import subprocess
from xml.parsers.expat import ExpatError

MACHO_MAGIC = {bytes.fromhex(s) for s in ('cffaedfe','feedfacf','cefaedfe','feedface','cafebabe','bebafeca','cafebabf','bfbafeca')}
SUPPLIER_TEAM = '2DC432GLL2'


def anchored(path):
    """Reject symlink ancestry, including the selected root itself."""
    path = Path(os.path.abspath(path))
    for parent in reversed((path, *path.parents)):
        if parent.is_symlink():
            raise ValueError(f'symlink path is not an inspection/staging root: {parent}')
    return path


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def scan(root):
    root = anchored(root)
    entries = []
    flags = os.O_RDONLY | os.O_NOFOLLOW
    def visit(fd, prefix):
        before = os.fstat(fd)
        with os.scandir(fd) as listing:
            names = sorted((e.name for e in listing), key=lambda n: n.encode('utf-8'))
        for name in names:
            if '\n' in name or '\r' in name:
                raise ValueError('line break in path cannot be represented in PKG manifest')
            relative = prefix + name
            original = os.stat(name, dir_fd=fd, follow_symlinks=False)
            entry = {'path': relative, 'mode': oct(stat.S_IMODE(original.st_mode))}
            if stat.S_ISLNK(original.st_mode):
                entry.update(kind='symlink', target=os.readlink(name, dir_fd=fd))
            elif stat.S_ISDIR(original.st_mode):
                child = os.open(name, flags | os.O_DIRECTORY, dir_fd=fd)
                try:
                    if os.fstat(child).st_ino != original.st_ino:
                        raise ValueError('directory changed during inventory')
                    entry['kind'] = 'dir'
                    visit(child, relative + '/')
                finally:
                    os.close(child)
            elif stat.S_ISREG(original.st_mode):
                child = os.open(name, flags | os.O_NONBLOCK, dir_fd=fd)
                try:
                    start = os.fstat(child)
                    if (start.st_dev, start.st_ino, start.st_mode) != (original.st_dev, original.st_ino, original.st_mode):
                        raise ValueError('file changed during inventory')
                    h = hashlib.sha256(); magic = os.read(child, 4); h.update(magic)
                    while chunk := os.read(child, 1024 * 1024): h.update(chunk)
                    end = os.fstat(child)
                    if (start.st_size,start.st_mtime_ns,start.st_ctime_ns) != (end.st_size,end.st_mtime_ns,end.st_ctime_ns):
                        raise ValueError('file mutated during inventory')
                    entry.update(kind='file', sha256=h.hexdigest(), size=end.st_size, macho=magic in MACHO_MAGIC)
                finally:
                    os.close(child)
            else:
                entry['kind'] = 'other'
            entries.append(entry)
        after = os.fstat(fd)
        if (before.st_mtime_ns,before.st_ctime_ns) != (after.st_mtime_ns,after.st_ctime_ns):
            raise ValueError('directory mutated during inventory')
    fd = os.open(root, flags | os.O_DIRECTORY)
    try:
        root_mode = oct(stat.S_IMODE(os.fstat(fd).st_mode))
        visit(fd, '')
    finally:
        os.close(fd)
    entries.sort(key=lambda e: e['path'].encode('utf-8'))
    # PKG §5.2 explicitly hashes regular-file content/path lines, not modes.
    manifest = sha256(b''.join(f"{e['sha256']}  {e['path']}\n".encode('utf-8') for e in entries if e['kind']=='file'))
    return {'root': str(root), 'root_mode': root_mode, 'entries': entries, 'manifest_sha256': manifest,
            'files': sum(e['kind']=='file' for e in entries), 'macho_files': sum(e.get('macho',False) for e in entries)}


def compare(actual, expected):
    def key(e): return e['kind'],e['mode'],e.get('sha256'),e.get('target')
    a={e['path']:key(e) for e in actual['entries']}; b={e['path']:key(e) for e in expected['entries']}
    differing=sorted(p for p in a.keys() & b.keys() if a[p]!=b[p])
    missing=sorted(b.keys()-a.keys()); extra=sorted(a.keys()-b.keys())
    root_mode_equal=actual['root_mode']==expected['root_mode']
    return {'equal':not (differing or missing or extra) and root_mode_equal, 'differing':differing,
            'missing':missing,'extra':extra,'root_mode_equal':root_mode_equal}


def inspect_signatures(inventory):
    """Only Apple's signature-display commands; nonzero/unreadable output never passes."""
    records=[]
    for entry in inventory['entries']:
        if not entry.get('macho'): continue
        path=str(Path(inventory['root']) / entry['path'])
        info=subprocess.run(['/usr/bin/codesign','-dv','--verbose=2',path], capture_output=True, text=True, timeout=30)
        ent=subprocess.run(['/usr/bin/codesign','-d','--entitlements','-','--xml',path],capture_output=True,timeout=30)
        lines=info.stderr.splitlines()
        def value(prefix): return next((s.split('=',1)[1] for s in lines if s.startswith(prefix+'=')),None)
        try:
            entitlements=plistlib.loads(ent.stdout) if ent.stdout.strip() else {}
            if not isinstance(entitlements,dict): raise ValueError('entitlements are not a dictionary')
        except (plistlib.InvalidFileException,ValueError,ExpatError):
            entitlements=None
        team=value('TeamIdentifier'); authority=value('Authority')
        ok=(info.returncode==0 and ent.returncode==0 and team==SUPPLIER_TEAM
            and authority is not None and authority.startswith('Developer ID Application:')
            and authority.endswith(f'({SUPPLIER_TEAM})') and any('flags=' in l and 'runtime' in l for l in lines)
            and value('Timestamp') is not None and entitlements is not None
            and not entitlements.get('com.apple.security.get-task-allow',False))
        unknown=(info.returncode!=0 or ent.returncode!=0 or authority in (None,'(unavailable)')
                 or entitlements is None or 'warning:' in ent.stderr.decode('utf-8',errors='replace').lower())
        unsigned='code object is not signed at all' in info.stderr.lower()
        outcome='fail' if unsigned else ('inconclusive' if unknown else ('pass' if ok else 'fail'))
        records.append({'path':entry['path'],'sha256':entry['sha256'],'display_exit':info.returncode,
                        'entitlements_exit':ent.returncode,'display_stderr':info.stderr,
                        'entitlements_stderr':ent.stderr.decode('utf-8',errors='replace'),
                        'entitlements':entitlements,'outcome':outcome,'fp0_file_preconditions':outcome=='pass'})
    after=scan(inventory['root'])
    unchanged=compare(after,inventory)['equal']
    links=any(e['kind'] in ('symlink','other') for e in inventory['entries'])
    outcomes=[r['outcome'] for r in records]
    outcome='fail' if links or 'fail' in outcomes else ('pass' if records and unchanged and all(o=='pass' for o in outcomes) else 'inconclusive')
    return {'outcome':outcome,
            'method':'codesign display only, PKG §7.1 FP-0; not signature validity verification or native execution',
            'tree_unchanged':unchanged,'files':records}
