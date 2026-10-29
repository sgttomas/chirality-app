#!/usr/bin/env python3
"""Reviewed, explicitly invoked offline guest driver. No installers or credentials."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import uuid

VM = '2944eb77-696f-41ad-97e2-142ba0489535'
SOURCE = Path(__file__).with_name('ProcessFixture.cs')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', action='store_true', help='write fresh guest scratch, compile and execute once')
    args = ap.parse_args()
    if not args.run:
        ap.error('--run is required; reading this driver never executes a fixture')
    host = Path(tempfile.mkdtemp(prefix='chirality-app-process-fixture-'))
    (host / 'CODEX_HOME').mkdir()
    os.environ['CODEX_HOME'] = str(host / 'CODEX_HOME')
    nonce = uuid.uuid4().hex
    assert re.fullmatch('[a-f0-9]{32}', nonce)
    records = []
    print('Host artifacts:', host, flush=True)

    def invoke(label, command, timeout=30):
        # prlctl reparses ordinary -Command quoting. EncodedCommand preserves exact
        # individual commands, including literals; no .ps1 loading or policy override.
        payload = base64.b64encode(command.encode('utf-16le')).decode('ascii')
        argv = ['prlctl', 'exec', VM, 'powershell.exe', '-NoProfile', '-NonInteractive',
                '-EncodedCommand', payload]
        item = {'label': label, 'command_sha256': hashlib.sha256(command.encode()).hexdigest()}
        try:
            p = subprocess.run(argv, capture_output=True, timeout=timeout)
            item.update(returncode=p.returncode, stdout=p.stdout.decode('utf-8', 'replace'),
                        stderr=p.stderr.decode('utf-8', 'replace'))
        except subprocess.TimeoutExpired as e:
            item.update(returncode=None, stdout=(e.stdout or b'').decode('utf-8', 'replace'),
                        stderr=(e.stderr or b'').decode('utf-8', 'replace'),
                        unknown='Host command timed out; cleanup is NOT established. Stop all further runs.')
        records.append(item)
        (host / 'commands.json').write_text(json.dumps(records, indent=2))
        if item['returncode'] != 0:
            raise RuntimeError(f'{label} refused/unknown: {item}; artifacts {host}')
        return item['stdout'].strip()

    prefix = "$ErrorActionPreference='Stop'; $ProgressPreference='SilentlyContinue'; "
    # Read only. No user directory listing, census, PATH/profile or registry reads.
    meta = invoke('metadata', prefix + """
$r=[System.Runtime.InteropServices.RuntimeEnvironment]::GetRuntimeDirectory();
[ordered]@{language=$ExecutionContext.SessionState.LanguageMode.ToString(); policy=(Get-ExecutionPolicy).ToString();
ps=$PSVersionTable.PSVersion.ToString(); runtime=$r; pointerBytes=[IntPtr]::Size;
architecture=$env:PROCESSOR_ARCHITECTURE; os=[Environment]::OSVersion.VersionString;
compiler=(Get-Item -LiteralPath ($r+'csc.exe') | Select-Object FullName,Length,@{n='Version';e={$_.VersionInfo.FileVersion}});
clrVersion=(Get-Item -LiteralPath ($r+'clr.dll')).VersionInfo.FileVersion;
temp=$env:TEMP} | ConvertTo-Json -Compress
""")
    metadata = json.loads(meta)
    (host / 'metadata.json').write_text(json.dumps(metadata, indent=2))
    if metadata['language'] != 'FullLanguage':
        raise RuntimeError('Constrained language: do not proceed')
    temp = metadata['temp']
    # Use only this established system TEMP; unexpected peer condition stops here.
    if temp.lower() != r'c:\windows\temp':
        raise RuntimeError('Unexpected guest TEMP; no scratch created')
    root = temp + '\\chirality-app-process-fixture-' + nonce
    def lit(value):
        return "'" + value.replace("'", "''") + "'"
    root_lit = lit(root)
    check = prefix + '$root=' + root_lit + '; $nonce=' + lit(nonce) + "; " + """
if([IO.File]::ReadAllText($root+'\\OWNER') -cne $nonce){throw 'ownership mismatch'};
if(([IO.File]::GetAttributes($root) -band [IO.FileAttributes]::ReparsePoint) -ne 0){throw 'scratch reparse'};
"""
    invoke('create-owned-scratch', prefix + '$root=' + root_lit + '; $nonce=' + lit(nonce) + "; " + """
$d=New-Object IO.DriveInfo('C:\\'); if($d.DriveType -ne 'Fixed' -or $d.DriveFormat -cne 'NTFS'){throw 'require fixed local NTFS'};
foreach($p in @('C:\\','C:\\Windows','C:\\Windows\\TEMP')){
 if(([IO.File]::GetAttributes($p) -band [IO.FileAttributes]::ReparsePoint) -ne 0){throw 'TEMP ancestry reparse'}
};
if([IO.Directory]::Exists($root) -or [IO.File]::Exists($root)){throw 'scratch already exists'};
[void][IO.Directory]::CreateDirectory($root);
$f=New-Object IO.FileStream(($root+'\\OWNER'),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None);
try{$b=[Text.Encoding]::ASCII.GetBytes($nonce); $f.Write($b,0,$b.Length)}finally{$f.Dispose()};
foreach($name in @('TEMP','TMP','CODEX_HOME')){[void][IO.Directory]::CreateDirectory($root+'\\'+$name)};
[ordered]@{root=$root;nonce=$nonce;filesystem=$d.DriveFormat;driveType=$d.DriveType.ToString()} | ConvertTo-Json -Compress
""")
    source = SOURCE.read_bytes()
    sha = hashlib.sha256(source).hexdigest()
    encoded = base64.b64encode(source).decode('ascii')
    for index, start in enumerate(range(0, len(encoded), 1800)):
        chunk = encoded[start:start + 1800]
        # Chunks are base64 alphabet only. CreateNew on first, owned-file append later.
        mode = 'CreateNew' if index == 0 else 'Append'
        invoke('source-chunk-' + str(index), check +
               "$b=[Convert]::FromBase64String('" + chunk + "'); " +
               "$f=New-Object IO.FileStream(($root+'\\ProcessFixture.cs'),[IO.FileMode]::" + mode +
               ",[IO.FileAccess]::Write,[IO.FileShare]::None); try{$f.Write($b,0,$b.Length)}finally{$f.Dispose()}")
    environment = """
foreach($name in @('TEMP','TMP','CODEX_HOME')){[Environment]::SetEnvironmentVariable($name,$root+'\\'+$name,'Process')};
[Environment]::CurrentDirectory=$root; Set-Location -LiteralPath $root;
"""
    invoke('source-hash-and-compile', check + environment + """
$sha=[Security.Cryptography.SHA256]::Create();
$actual=([BitConverter]::ToString($sha.ComputeHash([IO.File]::ReadAllBytes($root+'\\ProcessFixture.cs')))).Replace('-','').ToLowerInvariant();
""" + "if($actual -cne '" + sha + "'){throw 'source hash mismatch'}; " + """
$r=[System.Runtime.InteropServices.RuntimeEnvironment]::GetRuntimeDirectory();
& ($r+'csc.exe') /nologo /noconfig /nostdlib+ /target:exe /platform:anycpu /optimize+ /utf8output ('/r:'+$r+'mscorlib.dll') ('/r:'+$r+'System.dll') ('/out:'+$root+'\\ProcessFixture.exe') ($root+'\\ProcessFixture.cs');
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE};
[ordered]@{sourceSha256=$actual;compilerSha256=([BitConverter]::ToString($sha.ComputeHash([IO.File]::ReadAllBytes($r+'csc.exe')))).Replace('-','').ToLowerInvariant();
exeSha256=([BitConverter]::ToString($sha.ComputeHash([IO.File]::ReadAllBytes($root+'\\ProcessFixture.exe')))).Replace('-','').ToLowerInvariant()} | ConvertTo-Json -Compress
""", timeout=40)
    result = invoke('native-fixture-once', check + environment +
                    "& ($root+'\\ProcessFixture.exe') supervisor $nonce suite $root; exit $LASTEXITCODE", timeout=95)
    (host / 'native.tsv').write_text(result + '\n')
    # Import only the repository-local verifier, no other environment/config inputs.
    from verify_results import verify
    checked = verify(result)
    summary = {'nonce': nonce, 'vm': VM, 'guestRoot': root, 'hostRoot': str(host),
               'sourceSha256': sha, 'driverSha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'results': checked}
    (host / 'summary.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2), flush=True)

if __name__ == '__main__':
    main()
