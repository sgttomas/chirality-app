#!/usr/bin/env python3
"""Disposable GitHub-hosted native-x64 process fixture; no guest adapter.

Trusted checkout/runner namespace only. Provider disposal is not an App cleanup
or compiler parent-death guarantee. Refusals/timeouts never produce a pass.
"""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import threading
import time
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_PATHS = (
    '.gitattributes', '.github/workflows/windows-process-fixtures.yml',
    'app/examination/windows_platform/run_hosted_fixture.py',
    'app/examination/windows_platform/ProcessFixture.cs',
    'app/examination/windows_platform/verify_results.py',
)
LIMIT = 128 * 1024
PROFILE = 'github-hosted-native-x64-trusted-checkout-process-only/v1'


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def require_context():
    # Admission precedes subprocess creation, source reads and scratch writes.
    require(os.environ.get('GITHUB_ACTIONS') == 'true' and
            os.environ.get('RUNNER_ENVIRONMENT') == 'github-hosted',
            'only disposable GitHub-hosted Actions execution is admitted')
    require(sys.platform == 'win32' and os.environ.get('RUNNER_OS') == 'Windows'
            and os.environ.get('RUNNER_ARCH') == 'X64' and struct.calcsize('P') == 8,
            'native Windows X64 with 64-bit Python required')
    require(sys.version_info >= (3, 9), 'preinstalled Python >=3.9 required')
    # Labels alone are not architecture evidence. Fail if the API is unavailable.
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.IsWow64Process2.argtypes = (ctypes.c_void_p,
                                     ctypes.POINTER(ctypes.c_ushort),
                                     ctypes.POINTER(ctypes.c_ushort))
    kernel.IsWow64Process2.restype = ctypes.c_int
    process, native = ctypes.c_ushort(), ctypes.c_ushort()
    require(kernel.IsWow64Process2(kernel.GetCurrentProcess(), ctypes.byref(process),
                                  ctypes.byref(native)), 'IsWow64Process2 failed')
    require(process.value == 0 and native.value == 0x8664,
            'Python must be native AMD64, not an emulated process')
    # Exercise verifier-required stdlib capability, rather than just a label.
    require('x'.removeprefix('x') == '' and hashlib.sha256(b'').hexdigest() ==
            'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
            'Python stdlib capability unavailable')
    return {'processMachine': process.value, 'nativeMachine': native.value,
            'pointerBytes': struct.calcsize('P'), 'python': sys.version,
            'os': list(sys.getwindowsversion())}


def capture(argv, seconds, *, cwd=None, env=None, limit=LIMIT):
    """Bound both channels and waits; kill only Popen's original process handle.

    No context-manager implicit wait and no PID/name scans. On Windows Popen.kill
    uses TerminateProcess on its retained creation handle. A timeout remains a
    failure even if subsequent termination is observed. Process creation itself
    is not interruptible here; the provider's job timeout is the outer bound.
    """
    started = time.monotonic()
    process = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               close_fds=True)
    buffers = [bytearray(), bytearray()]
    done = [threading.Event(), threading.Event()]
    overflow = threading.Event()
    errors = []
    lock = threading.Lock()

    def reader(index, stream):
        try:
            while True:
                chunk = stream.read(4096)
                if not chunk:
                    break
                with lock:
                    remaining = limit - sum(map(len, buffers))
                    buffers[index].extend(chunk[:remaining])
                    if len(chunk) > remaining:
                        overflow.set()
                        break
        except Exception as error:
            errors.append(type(error).__name__)
        finally:
            stream.close()
            done[index].set()

    for index, stream in enumerate((process.stdout, process.stderr)):
        threading.Thread(target=reader, args=(index, stream), daemon=True).start()
    deadline = started + seconds
    reason = None
    while True:
        if overflow.is_set() or errors:
            reason = 'output_limit' if overflow.is_set() else 'reader_error'
            break
        if process.poll() is not None and all(event.is_set() for event in done):
            break
        if time.monotonic() >= deadline:
            reason = 'deadline'
            break
        time.sleep(0.01)
    teardown = 'not_needed'
    if reason:
        try:
            if process.poll() is None:
                process.kill()
            process.wait(timeout=5)
            teardown = 'original_process_exit_observed;descendants_unproven'
        except Exception as error:
            teardown = 'UNKNOWN:' + type(error).__name__
    with lock:
        stdout, stderr = (bytes(buffer) for buffer in buffers)
    return {'argv': list(map(str, argv)), 'returncode': process.poll(),
            'failure': reason, 'teardown': teardown,
            'elapsed_seconds': time.monotonic() - started,
            'stdout': stdout, 'stderr': stderr}


def successful(result):
    require(not result['failure'] and result['returncode'] == 0,
            'command failed/unknown: ' + str(result['failure'] or result['returncode']))


def git_bytes(*args):
    result = capture(['git', '--no-lazy-fetch', *args], 15, cwd=ROOT)
    successful(result)
    require(not result['stderr'], 'unexpected Git stderr')
    return result['stdout']


def bind_sources(revision):
    require(re.fullmatch('[0-9a-f]{40}', revision or '') is not None,
            'full lowercase source commit required')
    require(git_bytes('rev-parse', '--verify', 'HEAD').strip().decode('ascii') == revision,
            'checkout HEAD differs from requested source commit')
    blobs, identities = {}, {}
    for name in SOURCE_PATHS:
        blob = git_bytes('show', revision + ':' + name)
        require((ROOT / name).read_bytes() == blob, 'source differs from Git blob: ' + name)
        oid = git_bytes('rev-parse', revision + ':' + name).strip().decode('ascii')
        require(hashlib.sha1(b'blob ' + str(len(blob)).encode('ascii') + b'\0' + blob)
                .hexdigest() == oid, 'Git blob identity mismatch: ' + name)
        blobs[name] = blob
        identities[name] = {'git_blob': oid, 'sha256': hashlib.sha256(blob).hexdigest(),
                            'bytes': len(blob)}
    return blobs, identities


def verify_native_trace(raw, verifier_source, nonce):
    text = raw.decode('utf-8', errors='strict')
    namespace = {'__name__': 'hosted_bound_verifier'}
    exec(compile(verifier_source, 'git-blob:verify_results.py', 'exec'), namespace)
    results = namespace['verify'](text)  # Includes actual membership and cleanup.
    rows = [line.split('\t') for line in text.splitlines()]
    require(all(row[2] == nonce for row in rows), 'trace generation differs from launch')
    identity = [row[4] for row in rows if row[3] == 'IDENTITY']
    require(len(identity) == 1, 'missing/duplicate native harness identity')
    fields = dict(item.split('=', 1) for item in identity[0].split(';'))
    require(fields.get('processMachine') == '0x0000' and
            fields.get('nativeMachine') == '0x8664' and
            fields.get('nativeSystemArchitecture') == '9' and
            fields.get('pointerBytes') == '8', 'harness is not native AMD64')
    suite = [row for row in rows if row[3] == 'SUITE']
    require(len(suite) == 1 and suite[0][1] == 'suite' and
            suite[0][4] == 'cases_complete', 'suite completion missing')
    return results, fields


def persist_command(evidence, name, result):
    metadata = {key: value for key, value in result.items() if key not in ('stdout', 'stderr')}
    for channel in ('stdout', 'stderr'):
        (evidence / (name + '.' + channel)).write_bytes(result[channel])
        metadata[channel + '_sha256'] = hashlib.sha256(result[channel]).hexdigest()
        metadata[channel + '_bytes'] = len(result[channel])
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-commit', required=True)
    args = parser.parse_args()
    evidence = None
    report = {'schema': 'chirality-hosted-process-fixture/v1', 'profile': PROFILE,
              'status': 'FAILED', 'native_execution': 'NOT_RUN'}
    try:
        report['host'] = require_context()
        report['runner_image'] = {name: os.environ.get(name) for name in ('ImageOS', 'ImageVersion')}
        blobs, report['sources'] = bind_sources(args.source_commit)
        report['source_commit'] = args.source_commit
        runner_temp = Path(os.environ['RUNNER_TEMP']).resolve(strict=True)
        require(runner_temp.is_dir(), 'RUNNER_TEMP directory required')
        # Only preinstalled Framework64 compiler and explicit framework references.
        framework = Path(os.environ['SystemRoot']) / 'Microsoft.NET' / 'Framework64' / 'v4.0.30319'
        compiler = framework / 'csc.exe'
        references = [framework / name for name in ('mscorlib.dll', 'System.dll', 'System.Core.dll')]
        require(all(path.is_file() for path in [compiler, *references]),
                'preinstalled Framework64 compiler/references missing; no acquisition allowed')
        report['tool_files'] = {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in [compiler, *references]}
        # Fixed artifact leaf, exclusive creation: stale outputs cannot be reused.
        artifact_root = runner_temp / 'windows-process-fixture-evidence'
        artifact_root.mkdir()
        evidence = artifact_root
        nonce = uuid.uuid4().hex
        scratch = runner_temp / ('chirality-app-process-fixture-' + nonce)
        scratch.mkdir()
        report['nonce'] = nonce
        for name in ('source', 'TEMP', 'TMP', 'CODEX_HOME'):
            (scratch / name).mkdir()
        (scratch / 'OWNER').write_bytes(nonce.encode('ascii'))
        source = scratch / 'source' / 'ProcessFixture.cs'
        source.write_bytes(blobs['app/examination/windows_platform/ProcessFixture.cs'])
        require(source.read_bytes() == blobs['app/examination/windows_platform/ProcessFixture.cs'],
                'scratch source copy changed bytes')
        env = dict(os.environ, TEMP=str(scratch / 'TEMP'), TMP=str(scratch / 'TMP'),
                   CODEX_HOME=str(scratch / 'CODEX_HOME'))
        report['commands'] = {}
        # The legacy Framework compiler supports /help, not Roslyn's /version.
        # Keep its banner (no /nologo) and retain the entire bounded raw response.
        version = capture([str(compiler), '/noconfig', '/help'], 15, cwd=scratch, env=env)
        report['commands']['compiler_version'] = persist_command(evidence, 'compiler-version', version)
        successful(version)
        require(version['stdout'].strip() and not version['stderr'], 'compiler version unavailable')
        banner = re.search(rb'(?m)^.*Compiler version [0-9][^\r\n]*', version['stdout'])
        require(banner is not None, 'compiler version banner unavailable')
        report['compiler_version'] = banner[0].decode('utf-8', errors='strict').strip()
        executable = scratch / 'ProcessFixture.exe'
        command = [str(compiler), '/noconfig', '/nologo', '/nostdlib+', '/platform:x64',
                   '/target:exe', '/out:' + str(executable)]
        command += ['/reference:' + str(path) for path in references] + [str(source)]
        compiled = capture(command, 60, cwd=scratch, env=env)
        report['commands']['compile'] = persist_command(evidence, 'compile', compiled)
        successful(compiled)  # Successful compiler exit is mandatory before launch.
        require(executable.is_file(), 'compiler produced no executable')
        report['executable_sha256'] = hashlib.sha256(executable.read_bytes()).hexdigest()
        # Recheck all checkout inputs immediately before launching. Trusted runner
        # profile does not purport to exclude adversarial namespace races.
        bind_sources(args.source_commit)
        report['native_execution'] = 'ATTEMPTED'
        native = capture([str(executable), 'supervisor', nonce, 'suite', str(scratch)],
                         90, cwd=scratch, env=env)
        report['commands']['native'] = persist_command(evidence, 'native', native)
        successful(native)
        require(not native['stderr'], 'unexpected native stderr')
        report['cases'], report['native_identity'] = verify_native_trace(
            native['stdout'], blobs['app/examination/windows_platform/verify_results.py'], nonce)
        report['status'] = 'PASS'
        report['native_execution'] = 'COMPLETED'
        return 0
    except Exception as error:
        report['error'] = type(error).__name__ + ': ' + str(error)
        print(report['error'], file=sys.stderr)
        return 1
    finally:
        if evidence is not None:
            (evidence / 'result.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    sys.exit(main())
