import { copyFile, mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { afterEach, describe, expect, it } from 'vitest';

import { run } from '../../../scripts/validate-harness-premerge.mjs';

let fixtureRoot = '';

afterEach(async () => {
  if (fixtureRoot) await rm(fixtureRoot, { recursive: true, force: true });
  fixtureRoot = '';
});

async function makeFixture(): Promise<string> {
  fixtureRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-premerge-'));
  await mkdir(path.join(fixtureRoot, 'scripts'), { recursive: true });
  await copyFile(
    path.resolve(process.cwd(), 'scripts', 'validate-harness-premerge.mjs'),
    path.join(fixtureRoot, 'scripts', 'validate-harness-premerge.mjs')
  );
  return fixtureRoot;
}

async function runWrapperSpawned(cwd: string): Promise<{ code: number; output: string }> {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, ['scripts/validate-harness-premerge.mjs'], {
      cwd,
      stdio: ['ignore', 'pipe', 'pipe']
    });
    let output = '';
    child.stdout.on('data', (chunk) => { output += chunk.toString(); });
    child.stderr.on('data', (chunk) => { output += chunk.toString(); });
    child.on('error', reject);
    child.on('close', (code) => resolve({ code: code ?? 1, output }));
  });
}

async function runWrapperInProcess(cwd: string): Promise<{ code: number; output: string }> {
  const lines: string[] = [];
  const code = await run([], {
    cwd,
    log: (line: string) => lines.push(line),
    logError: (line: string) => lines.push(line)
  });
  return { code, output: lines.join('\n') };
}

describe('validate-harness-premerge wrapper failures', () => {
  // Spawn-based CLI smoke test: proves the executable entrypoint itself
  // (main-guard, argv handling, process exit code), which the in-process
  // run() calls below deliberately do not cover.
  it('fails closed with RUNTIME_SURFACE_MISSING when the Section 8 script is absent', async () => {
    const cwd = await makeFixture();
    const result = await runWrapperSpawned(cwd);

    expect(result.code).not.toBe(0);
    expect(result.output).toContain(
      'RUNTIME_SURFACE_MISSING: frontend/scripts/validate-harness-section8.mjs'
    );
    expect(result.output).toContain('HARNESS_PREMERGE_STATUS=fail');
  });

  it('rejects a Section 8 summary containing the removed regression key', async () => {
    const cwd = await makeFixture();
    const summaryPath = path.join(cwd, 'section8-summary.json');
    const requiredIds = [
      'setup.server_reachable',
      'regression.session_crud',
      'section8.boot_error_taxonomy',
      'section8.smoke_stream',
      'section8.session_persistence_resume',
      'section8.permissions_dontask',
      'section8.interrupt_sigint',
      'section8.sdk_native_stream',
      'regression.api_chat_reachability'
    ];
    await writeFile(
      summaryPath,
      JSON.stringify({ results: requiredIds.map((id) => ({ id, status: 'pass' })) })
    );
    await writeFile(
      path.join(cwd, 'scripts', 'validate-harness-section8.mjs'),
      `console.log('HARNESS_VALIDATION_SUMMARY_PATH=${summaryPath}');\nconsole.log('HARNESS_VALIDATION_STATUS=pass');\n`
    );

    const result = await runWrapperInProcess(cwd);
    expect(result.code).not.toBe(0);
    expect(result.output).toContain(
      "Summary includes legacy test id 'regression.api_chat_reachability'"
    );
  });

  it('publishes the exact Section 8 summary and count when validation fails', async () => {
    const cwd = await makeFixture();
    const summaryPath = path.join(cwd, 'section8-failure-summary.json');
    const summary = {
      status: 'fail',
      results: [
        { id: 'setup.server_reachable', status: 'pass' },
        {
          id: 'section8.boot_error_taxonomy',
          status: 'fail',
          error: 'Shared-runtime boot should complete: HTTP 503; payload={"error":{"type":"ENGINE_UNAVAILABLE"}}'
        }
      ]
    };
    await writeFile(summaryPath, `${JSON.stringify(summary)}\n`);
    await writeFile(
      path.join(cwd, 'scripts', 'validate-harness-section8.mjs'),
      [
        `console.log('HARNESS_VALIDATION_SUMMARY_PATH=${summaryPath}');`,
        "console.log('HARNESS_VALIDATION_STATUS=fail');",
        'process.exitCode = 1;'
      ].join('\n')
    );

    const result = await runWrapperInProcess(cwd);
    const stablePath = path.join(cwd, 'artifacts', 'harness', 'section8', 'latest', 'summary.json');
    expect(result.code).toBe(1);
    expect(result.output).toContain(`HARNESS_PREMERGE_ARTIFACT_PATH=${stablePath}`);
    expect(result.output).toContain('HARNESS_PREMERGE_STATUS=fail');
    expect(result.output).toContain('HARNESS_PREMERGE_TEST_COUNT=2');
    expect(JSON.parse(await readFile(stablePath, 'utf8'))).toEqual(summary);
  });

  it('preserves a malformed failure summary while failing with a zero count', async () => {
    const cwd = await makeFixture();
    const summaryPath = path.join(cwd, 'section8-malformed-summary.json');
    const malformed = '{"status":"fail","results":[';
    await writeFile(summaryPath, malformed);
    await writeFile(
      path.join(cwd, 'scripts', 'validate-harness-section8.mjs'),
      [
        `console.log('HARNESS_VALIDATION_SUMMARY_PATH=${summaryPath}');`,
        'process.exitCode = 1;'
      ].join('\n')
    );

    const result = await runWrapperInProcess(cwd);
    const stablePath = path.join(cwd, 'artifacts', 'harness', 'section8', 'latest', 'summary.json');
    expect(result.code).toBe(1);
    expect(result.output).toContain('Section8 failure summary could not be interpreted:');
    expect(result.output).toContain('HARNESS_PREMERGE_STATUS=fail');
    expect(result.output).toContain('HARNESS_PREMERGE_TEST_COUNT=0');
    expect(await readFile(stablePath, 'utf8')).toBe(malformed);
  });

  it('reuses the current caller Section 9 outcome after still running Section 8', async () => {
    const cwd = await makeFixture();
    const summaryPath = path.join(cwd, 'section8-summary.json');
    const requiredIds = [
      'setup.server_reachable',
      'regression.session_crud',
      'section8.boot_error_taxonomy',
      'section8.smoke_stream',
      'section8.session_persistence_resume',
      'section8.permissions_dontask',
      'section8.interrupt_sigint',
      'section8.sdk_native_stream'
    ];
    await writeFile(
      summaryPath,
      JSON.stringify({ results: requiredIds.map((id) => ({ id, status: 'pass' })) })
    );
    await writeFile(
      path.join(cwd, 'scripts', 'validate-harness-section8.mjs'),
      `console.log('HARNESS_VALIDATION_SUMMARY_PATH=${summaryPath}');\nconsole.log('HARNESS_VALIDATION_STATUS=pass');\n`
    );
    const lines: string[] = [];
    let childStdout = '';

    const code = await run([], {
      cwd,
      log: (line: string) => lines.push(line),
      logError: (line: string) => lines.push(line),
      echoChildOutput: true,
      writeChildStdout: (text: string) => { childStdout += text; },
      completedSection9Result: {
        code: 0,
        stdout: [
          'HARNESS_SECTION9_STATUS=pass',
          'HARNESS_SECTION9_SOURCE_SUMMARY_PATH=/tmp/current-section9-summary.json',
          'HARNESS_SECTION9_TEST_COUNT=16'
        ].join('\n'),
        stderr: ''
      }
    });

    expect(code).toBe(0);
    expect(childStdout).toContain('HARNESS_VALIDATION_STATUS=pass');
    expect(lines.join('\n')).toContain('HARNESS_PREMERGE_SECTION9_STATUS=pass');
    expect(lines.join('\n')).toContain('HARNESS_PREMERGE_SECTION9_TEST_COUNT=16');
  });
});
