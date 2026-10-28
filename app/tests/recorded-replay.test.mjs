import test from 'node:test';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

test('recorded supplier peer preserves correlation and refuses divergent replay', {timeout: 120000}, () => {
  execFileSync('python3', ['-B', fileURLToPath(new URL('../supplier_checks/test_recorded_replay.py', import.meta.url))], {
    stdio: 'inherit', timeout: 115000,
  });
});
