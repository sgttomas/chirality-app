#!/usr/bin/env python3
"""Read-only readiness report. Native execution is hard-refused pending safety repairs."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
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
    args = ap.parse_args()
    if args.run:
        ap.error('Native fixture execution withheld: ' + ' '.join(BLOCKERS))
    if not args.inspect:
        ap.error('--inspect required; no implicit guest operations')
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
clrVersion=(Get-Item -LiteralPath ($r+'clr.dll')).VersionInfo.FileVersion;
temp=$env:TEMP} | ConvertTo-Json -Compress
"""
    argv = ['prlctl', 'exec', VM, 'powershell.exe', '-NoProfile', '-NonInteractive',
            '-EncodedCommand', base64.b64encode(command.encode('utf-16le')).decode('ascii')]
    report = {'vm': VM, 'sourceSha256': sources, 'blockers': BLOCKERS,
              'guestWrites': 'none requested', 'nativeCases': 'all not run',
              'commandSha256': hashlib.sha256(command.encode()).hexdigest(),
              'command': command, 'hostArtifacts': str(host)}
    try:
        p = subprocess.run(argv, capture_output=True, timeout=25)
        report.update(returncode=p.returncode, stdout=p.stdout.decode('utf-8', 'replace'),
                      stderr=p.stderr.decode('utf-8', 'replace'))
        if p.returncode == 0:
            report['metadata'] = json.loads(report['stdout'])
    except subprocess.TimeoutExpired as e:
        report.update(returncode=None, stdout=(e.stdout or b'').decode('utf-8', 'replace'),
                      stderr=(e.stderr or b'').decode('utf-8', 'replace'),
                      limitation='Read-only metadata invocation timed out; no fixture launched.')
    finally:
        (host / 'readiness.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    if report['returncode'] != 0:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
