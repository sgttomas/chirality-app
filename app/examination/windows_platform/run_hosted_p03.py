#!/usr/bin/env python3
"""Separate disposable hosted-only P-03 probe; zero acquisition, no VM adapter."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import uuid

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('p03_host_utilities', HERE / 'run_hosted_fixture.py')
HOST = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HOST)
# Reuse unchanged bounded capture/admission/source-binding utilities, with a
# separate complete input set. No P01/P02 stimulus or verifier is executed.
HOST.SOURCE_PATHS = (
    '.gitattributes', '.github/workflows/windows-stop-fixtures.yml',
    'app/examination/windows_platform/run_hosted_fixture.py',
    'app/examination/windows_platform/run_hosted_p03.py',
    'app/examination/windows_platform/P03Fixture.cs',
    'app/examination/windows_platform/verify_p03.py',
)
PROFILE = 'github-hosted-native-amd64-p03-synthetic-stop/v1'


def check_trace(raw, verifier_blob, nonce, scenario):
    namespace = {'__name__': 'bound_p03_verifier'}
    exec(compile(verifier_blob, 'git-blob:verify_p03.py', 'exec'), namespace)
    return namespace['verify'](raw, nonce, scenario)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-commit', required=True)
    args = parser.parse_args()
    evidence = None
    report = {'schema': 'chirality-hosted-p03/v1', 'profile': PROFILE,
              'status': 'FAILED', 'native_execution': 'NOT_RUN'}
    try:
        report['host'] = HOST.require_context()  # Before subprocess/scratch/source reads.
        blobs, report['sources'] = HOST.bind_sources(args.source_commit)
        report['source_commit'] = args.source_commit
        report['runner_image'] = {k: os.environ.get(k) for k in ('ImageOS', 'ImageVersion')}
        runner_temp = Path(os.environ['RUNNER_TEMP']).resolve(strict=True)
        HOST.require(runner_temp.is_dir(), 'RUNNER_TEMP directory required')
        framework = Path(os.environ['SystemRoot']) / 'Microsoft.NET' / 'Framework64' / 'v4.0.30319'
        compiler = framework / 'csc.exe'
        references = [framework / n for n in ('mscorlib.dll', 'System.dll', 'System.Core.dll')]
        HOST.require(all(p.is_file() for p in [compiler, *references]),
                     'preinstalled Framework64 files unavailable; no acquisition permitted')
        report['tool_files'] = {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in [compiler, *references]}
        artifact_root = runner_temp / 'windows-stop-fixture-evidence'
        artifact_root.mkdir()  # Stale artifact reuse refuses without overwriting.
        evidence = artifact_root
        report['commands'], report['cases'] = {}, []
        for scenario in ('positive', 'wrong-slot', 'missing-observation'):
            nonce = uuid.uuid4().hex
            scratch = runner_temp / ('chirality-app-p03-' + nonce)
            scratch.mkdir()
            for name in ('TEMP', 'TMP', 'CODEX_HOME'):
                (scratch / name).mkdir()
            (scratch / 'OWNER').write_bytes(nonce.encode('ascii'))
            source = scratch / 'P03Fixture.cs'
            source.write_bytes(blobs['app/examination/windows_platform/P03Fixture.cs'])
            HOST.require(source.read_bytes() == blobs['app/examination/windows_platform/P03Fixture.cs'],
                         'scratch source changed')
            executable = scratch / 'P03Fixture.exe'
            env = dict(os.environ, **{n: str(scratch / n) for n in ('TEMP', 'TMP', 'CODEX_HOME')})

            def command(name, argv, seconds):
                result = HOST.capture(argv, seconds, cwd=scratch, env=env)
                report['commands'][scenario + '-' + name] = HOST.persist_command(
                    evidence, scenario + '-' + name, result)
                HOST.successful(result)
                HOST.require(not result['stderr'], 'unexpected stderr: ' + name)
                return result

            version = command('compiler-version', [str(compiler), '/noconfig', '/help'], 15)
            banner = re.search(rb'(?m)^.*Compiler version [0-9][^\r\n]*', version['stdout'])
            HOST.require(banner is not None, 'preinstalled compiler banner unavailable')
            compile_command = [str(compiler), '/noconfig', '/nologo', '/nostdlib+', '/platform:x64',
                               '/target:exe', '/out:' + str(executable)]
            compile_command += ['/reference:' + str(p) for p in references] + [str(source)]
            command('compile', compile_command, 60)
            HOST.require(executable.is_file(), 'no compiled executable')
            HOST.bind_sources(args.source_commit)
            report['native_execution'] = 'ATTEMPTED'
            native = command('native', [str(executable), 'supervisor', nonce, scenario,
                                        str(scratch), '0', '0'], 35)
            case = check_trace(native['stdout'], blobs['app/examination/windows_platform/verify_p03.py'],
                               nonce, scenario)
            # Wrong-slot is a deliberately broken target: its trace is admissible
            # only as a negative control, never a positive mechanism pass.
            case.update(nonce=nonce, compiler_version=banner[0].decode('ascii').strip(),
                        executable_sha256=hashlib.sha256(executable.read_bytes()).hexdigest())
            report['cases'].append(case)
        report['status'], report['native_execution'] = 'PASS', 'COMPLETED'
        return 0
    except Exception as error:
        report['error'] = type(error).__name__ + ': ' + str(error)
        print(report['error'], file=sys.stderr)
        return 1
    finally:
        if evidence is not None and evidence.is_dir():
            (evidence / 'result.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    sys.exit(main())
