#!/usr/bin/env python3
"""Source-bound metadata/bootstrap checks. No compiler or fixture launch route."""
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
import gzip
import re

VM = '2944eb77-696f-41ad-97e2-142ba0489535'
HERE = Path(__file__).resolve().parent
SOURCE_FILES = ('ProcessFixture.cs', 'run_fixture.py', 'verify_results.py',
                'Controller.ps1', 'test_driver.py', 'README.md')
REQUIRED_ANCESTOR = 'ebf71ce713e4d71a2b32193fd360cfda3cd1dab9'
BLOCKERS = [
    'Sharing-only namespace guard rejected: CreateFile sharing excludes attribute/EA accesses, '
    'and MS-FSA 2.1.5.10.37 permits FSCTL_SET_REPARSE_POINT with FILE_WRITE_ATTRIBUTES. '
    'Denying FILE_SHARE_WRITE therefore does not establish reparse exclusion. '
    'Permitting FILE_SHARE_WRITE for csc pathname output supplies no stronger exclusion. '
    'No independently established replacement guard admits all compiler output/temp accesses.',
    'The in-memory controller is source preparation, not observed compiler/launch containment. '
    'Its integration, fixture stdout capture, timeout and host-loss experiments remain unrun.',
]


def bind_sources(source_commit):
    if not source_commit or not re.fullmatch(r'[0-9a-f]{40}', source_commit):
        raise ValueError('--source-commit must be a full saved Git commit')
    revision = subprocess.check_output(['git', 'rev-parse', '--verify', source_commit + '^{commit}'], cwd=HERE, text=True).strip()
    repo = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=HERE, text=True).strip())
    subprocess.run(['git', 'merge-base', '--is-ancestor', REQUIRED_ANCESTOR, revision], cwd=repo, check=True)
    verified_bytes = {}
    for name in SOURCE_FILES:
        path = HERE / name
        saved = subprocess.check_output(['git', 'show', revision + ':' + str(path.relative_to(repo))], cwd=repo)
        if saved != path.read_bytes():
            raise ValueError('source differs from recorded revision: ' + name)
        verified_bytes[name] = saved
    return revision, verified_bytes


def bootstrap_command(source):
    if not isinstance(source, bytes):
        raise ValueError('bootstrap requires verified source bytes')
    if not 1 <= len(source) <= 98304:
        raise ValueError('bootstrap source length bound')
    packed = gzip.compress(source, mtime=0)
    payload = base64.b64encode(packed).decode('ascii')
    digest = hashlib.sha256(source).hexdigest()
    # Decode a bounded exact byte stream in memory before ScriptBlock creation.
    # No .ps1 loading, compiler, policy override, file staging or shell expansion.
    command = r"""$ErrorActionPreference='Stop'; $ProgressPreference='SilentlyContinue';
$packed=[Convert]::FromBase64String('__PAYLOAD__');
if($packed.Length -gt 16384){throw 'compressed source bound'};
$inputStream=New-Object IO.MemoryStream(,$packed);
$zip=New-Object IO.Compression.GZipStream($inputStream,[IO.Compression.CompressionMode]::Decompress);
$buffer=New-Object byte[] (__LENGTH__+1); $count=0;
try { while($count -lt $buffer.Length){$n=$zip.Read($buffer,$count,$buffer.Length-$count);if($n -eq 0){break};$count+=$n} }
finally {$zip.Dispose();$inputStream.Dispose()};
if($count -ne __LENGTH__){throw 'decompressed source length mismatch'};
$bytes=New-Object byte[] $count;[Array]::Copy($buffer,$bytes,$count);
$sha=[Security.Cryptography.SHA256]::Create();
try{$actual=([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-','').ToLowerInvariant()}finally{$sha.Dispose()};
if($actual -cne '__HASH__'){throw 'decompressed source hash mismatch'};
$utf8=New-Object Text.UTF8Encoding($false,$true);
. ([ScriptBlock]::Create($utf8.GetString($bytes)));
Initialize-FixtureController;
$n=$script:FixtureControllerNative;$p=[Runtime.InteropServices.Marshal]::AllocHGlobal(4);
$machine=$null;
try{if($n::IsWow64Process2($n::GetCurrentProcess(),$p,[IntPtr]($p.ToInt64()+2)) -eq 0){throw 'IsWow64Process2 failed'};
$machine=[ordered]@{processMachine=('0x{0:x4}' -f ([Runtime.InteropServices.Marshal]::ReadInt16($p) -band 0xffff));nativeMachine=('0x{0:x4}' -f ([Runtime.InteropServices.Marshal]::ReadInt16($p,2) -band 0xffff))}}
finally{[Runtime.InteropServices.Marshal]::FreeHGlobal($p)};
$layouts=[ordered]@{};foreach($k in ($script:FixtureControllerLayouts.Keys | Sort-Object)){$layouts[$k]=[Runtime.InteropServices.Marshal]::SizeOf([Type]$script:FixtureControllerLayouts[$k])};
$runtime=[Runtime.InteropServices.RuntimeEnvironment]::GetRuntimeDirectory();
$streamCompiler=[ordered]@{};foreach($name in @('Microsoft.CodeAnalysis.dll','Microsoft.CodeAnalysis.CSharp.dll')){$streamCompiler[$name]=[IO.File]::Exists([IO.Path]::Combine($runtime,$name))};
[ordered]@{bootstrapSha256=$actual;bootstrapBytes=$count;layouts=$layouts;machine=$machine;pointerBytes=[IntPtr]::Size;
language=$ExecutionContext.SessionState.LanguageMode.ToString();policy=(Get-ExecutionPolicy).ToString();
runtime=[Environment]::Version.ToString();streamCompilerBesideFrameworkCompiler=$streamCompiler;
nativeCases='NOT RUN';guestFilesCreated=0;compilerOrFixtureProcessesCreated=0;jobObjectsCreated=0;
controllerLifecycle='NOT INVOKED';namespaceAdmission='REFUSED: sharing-only guard cannot establish reparse exclusion'} | ConvertTo-Json -Depth 5 -Compress
""".replace('__PAYLOAD__', payload).replace('__LENGTH__', str(len(source))).replace('__HASH__', digest)
    if len(packed) > 16384 or len(command.encode('utf-16le')) * 4 // 3 + 1024 > 30000:
        raise ValueError('encoded command transport bound')
    return command


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--inspect', action='store_true', help='read only installed guest metadata; write host report')
    mode.add_argument('--bootstrap-check', action='store_true', help='in-memory type/layout/API check; no scratch, compiler, Job or fixture process')
    mode.add_argument('--run', action='store_true', help='refuse before guest contact: namespace admission unsupported by selected guard')
    ap.add_argument('--source-commit', help='exact saved Git revision whose fixture files must match')
    args = ap.parse_args()
    if args.run:
        ap.error('Native fixture execution withheld: ' + ' '.join(BLOCKERS))
    try:
        revision, verified_bytes = bind_sources(args.source_commit)
        sources = {name: hashlib.sha256(data).hexdigest() for name, data in verified_bytes.items()}
    except (ValueError, subprocess.CalledProcessError) as exc:
        ap.error(str(exc))
    host = Path(tempfile.mkdtemp(prefix='chirality-app-process-readiness-'))
    (host / 'CODEX_HOME').mkdir()
    os.environ['CODEX_HOME'] = str(host / 'CODEX_HOME')
    command = r"""$ErrorActionPreference='Stop'; $ProgressPreference='SilentlyContinue';
$r=[System.Runtime.InteropServices.RuntimeEnvironment]::GetRuntimeDirectory();
[ordered]@{language=$ExecutionContext.SessionState.LanguageMode.ToString(); policy=(Get-ExecutionPolicy).ToString();
ps=$PSVersionTable.PSVersion.ToString(); runtime=$r; runtimeVersion=[Environment]::Version.ToString(); pointerBytes=[IntPtr]::Size;
architecture=$env:PROCESSOR_ARCHITECTURE; os=[Environment]::OSVersion.VersionString;
compiler=(Get-Item -LiteralPath ($r+'csc.exe') | Select-Object FullName,Length,@{n='Version';e={$_.VersionInfo.FileVersion}});
clrVersion=(Get-Item -LiteralPath ($r+'clr.dll')).VersionInfo.FileVersion} | ConvertTo-Json -Compress
"""
    if args.bootstrap_check:
        command = bootstrap_command(verified_bytes['Controller.ps1'])
    argv = ['prlctl', 'exec', VM, 'powershell.exe', '-NoProfile', '-NonInteractive',
            '-EncodedCommand', base64.b64encode(command.encode('utf-16le')).decode('ascii')]
    report = {'vm': VM, 'sourceRevision': revision, 'sourceSha256': sources, 'blockers': BLOCKERS,
              'mode': 'bootstrap-check' if args.bootstrap_check else 'inspect',
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
            report.update(returncode=None, limitation=str(exc) + '; guest command completion UNKNOWN; no fixture launched')
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
