#!/usr/bin/env python3
"""Read-only readiness report. Native execution is hard-refused pending safety repairs."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import selectors
import time
import tempfile

VM = '2944eb77-696f-41ad-97e2-142ba0489535'
HERE = Path(__file__).resolve().parent
BLOCKERS = [
    'No continuously retained namespace guards from exclusive guest scratch creation through compilation/execution. '
    'Path attributes plus a nonce/sentinel alone do not confine later opens, compiler output, or compiler temporary files.',
    'No guest-side compiler lifetime guard that survives loss of the host command. '
    'A prlctl timeout is not compiler termination or observed cleanup. '
    'The native supervisor timer begins too late to cover compilation.',
]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--inspect', action='store_true', help='read only installed guest metadata; write host report')
    ap.add_argument('--run', action='store_true', help='always refused; retained to prevent accidentally executing an old command')
    ap.add_argument('--source-commit', help='exact saved Git revision whose fixture files must match')
    args = ap.parse_args()
    if args.run:
        ap.error('Native fixture execution withheld: ' + ' '.join(BLOCKERS))
    if not args.inspect:
        ap.error('--inspect required; no implicit guest operations')
    if not args.source_commit:
        ap.error('--source-commit is required for a recorded source identity')
    revision = subprocess.check_output(['git', 'rev-parse', '--verify', args.source_commit + '^{commit}'], cwd=HERE, text=True).strip()
    repo = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=HERE, text=True).strip())
    for name in ('ProcessFixture.cs', 'run_fixture.py', 'verify_results.py', 'README.md'):
        path = HERE / name
        saved = subprocess.check_output(['git', 'show', revision + ':' + str(path.relative_to(repo))], cwd=repo)
        if saved != path.read_bytes():
            ap.error('source differs from recorded revision: ' + name)
    host = Path(tempfile.mkdtemp(prefix='chirality-app-process-readiness-'))
    (host / 'CODEX_HOME').mkdir()
    os.environ['CODEX_HOME'] = str(host / 'CODEX_HOME')
    sources = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in
               (HERE / 'ProcessFixture.cs', HERE / 'run_fixture.py', HERE / 'verify_results.py', HERE / 'README.md')}
    command = r"""$ErrorActionPreference='Stop'; $ProgressPreference='SilentlyContinue';
$r=[System.Runtime.InteropServices.RuntimeEnvironment]::GetRuntimeDirectory();
[ordered]@{language=$ExecutionContext.SessionState.LanguageMode.ToString(); policy=(Get-ExecutionPolicy).ToString();
ps=$PSVersionTable.PSVersion.ToString(); runtime=$r; runtimeVersion=[Environment]::Version.ToString(); pointerBytes=[IntPtr]::Size;
architecture=$env:PROCESSOR_ARCHITECTURE; os=[Environment]::OSVersion.VersionString;
compiler=(Get-Item -LiteralPath ($r+'csc.exe') | Select-Object FullName,Length,@{n='Version';e={$_.VersionInfo.FileVersion}});
clrVersion=(Get-Item -LiteralPath ($r+'clr.dll')).VersionInfo.FileVersion} | ConvertTo-Json -Compress
"""
    argv = ['prlctl', 'exec', VM, 'powershell.exe', '-NoProfile', '-NonInteractive',
            '-EncodedCommand', base64.b64encode(command.encode('utf-16le')).decode('ascii')]
    report = {'vm': VM, 'sourceRevision': revision, 'sourceSha256': sources, 'blockers': BLOCKERS,
              'guestWrites': 'none requested', 'nativeCases': 'all not run',
              'commandSha256': hashlib.sha256(command.encode()).hexdigest(),
              'command': command, 'hostArtifacts': str(host)}
    # Bound both channels together, and retain the original monotonic deadline.
    chunks = {'stdout': bytearray(), 'stderr': bytearray()}
    until = time.monotonic() + 25
    limit = 32768
    with subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        selector = selectors.DefaultSelector()
        selector.register(proc.stdout, selectors.EVENT_READ, 'stdout')
        selector.register(proc.stderr, selectors.EVENT_READ, 'stderr')
        try:
            while selector.get_map():
                remaining = until - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError('read-only metadata deadline')
                for key, _ in selector.select(min(remaining, 1)):
                    block = os.read(key.fileobj.fileno(), 4096)
                    if not block:
                        selector.unregister(key.fileobj)
                        continue
                    used = sum(map(len, chunks.values()))
                    chunks[key.data].extend(block[:max(0, limit - used)])
                    if used + len(block) > limit:
                        raise ValueError('read-only metadata output exceeded 32768 bytes')
            report['returncode'] = proc.wait(timeout=max(0.01, until - time.monotonic()))
        except (TimeoutError, ValueError, subprocess.TimeoutExpired) as exc:
            # Only the local client created above, never a guest PID/name action.
            proc.kill()
            proc.wait(timeout=5)
            report.update(returncode=None, limitation=str(exc) + '; no fixture launched')
        finally:
            selector.close()
            report.update({k: bytes(v).decode('utf-8', 'replace') for k, v in chunks.items()})
            (host / 'readiness.json').write_text(json.dumps(report, indent=2))
    if report['returncode'] == 0:
        report['metadata'] = json.loads(report['stdout'])
        (host / 'readiness.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    if report['returncode'] != 0:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
