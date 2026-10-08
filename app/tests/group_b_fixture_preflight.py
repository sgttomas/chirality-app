#!/usr/bin/env python3
"""Run bounded fixture checks through the actual App crate, offline only."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

APP = Path(__file__).resolve().parents[1]
FIXTURES = APP / 'examination/standalone/fixtures'

def main():
    env = dict(os.environ, CARGO_NET_OFFLINE='true', CHIRALITY_SKIP_CODEX='1', PYTHONDONTWRITEBYTECODE='1')
    commands = [
        ['cargo', 'test', '--lib', '--offline', '--locked', '--manifest-path', str(APP/'src-tauri/Cargo.toml'), 'group_b_fixture', '--', '--nocapture'],
        [sys.executable, '-m', 'unittest', 'discover', '-s', str(APP/'tests'), '-p', 'group_b_fixture_tools_test.py', '-v'],
    ]
    checks = []
    for command in commands:
        run = subprocess.run(command, env=env, text=True, capture_output=True)
        # Keep exact test-result lines; compiler environment paths are not evidence of a test.
        lines = [line for line in (run.stdout + run.stderr).splitlines()
                 if line.startswith(('test ', 'test_', 'test result:', 'Ran ', 'OK', 'FAILED', 'error:'))]
        expected_summary = '5 passed; 0 failed;' if command[0] == 'cargo' else 'Ran 2 tests'
        complete = expected_summary in (run.stdout + run.stderr)
        checks.append({'expected_tests_executed': complete, 'consumer': 'actual App crate' if command[0] == 'cargo' else 'invented tally tools',
                       'exit_code': run.returncode, 'test_output': lines})
        if run.returncode or not complete:
            print(json.dumps({'checks': checks, 'fixture_preflight_passed': False,
                              'native_examination_performed': False}, indent=2))
            return 1
    paths = sorted(p for p in FIXTURES.rglob('*') if p.is_file())
    print(json.dumps({'checks': checks, 'fixture_preflight_passed': True,
                      'native_examination_performed': False, 'candidate_build_supplied': False,
                      'standing': 'offline fixture consumption only; ST-1/2/3 unperformed',
                      'files': [{'path': str(p.relative_to(APP)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]}, indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
