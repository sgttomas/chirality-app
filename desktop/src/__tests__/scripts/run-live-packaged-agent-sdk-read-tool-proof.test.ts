import { execFile } from 'node:child_process';
import { chmod, mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { promisify } from 'node:util';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { run } from '../../../scripts/run-live-packaged-agent-sdk-read-tool-proof.mjs';

const execFileAsync = promisify(execFile);
const SCRIPT_PATH = path.resolve(
  process.cwd(),
  'scripts',
  'run-live-packaged-agent-sdk-read-tool-proof.mjs'
);

const SDK_PLATFORM_PACKAGE_BY_RUNTIME: Record<string, string> = {
  'darwin:arm64': '@anthropic-ai/claude-agent-sdk-darwin-arm64',
  'darwin:x64': '@anthropic-ai/claude-agent-sdk-darwin-x64',
  'linux:arm64': '@anthropic-ai/claude-agent-sdk-linux-arm64',
  'linux:x64': '@anthropic-ai/claude-agent-sdk-linux-x64',
  'win32:arm64': '@anthropic-ai/claude-agent-sdk-win32-arm64',
  'win32:x64': '@anthropic-ai/claude-agent-sdk-win32-x64'
};

type ScriptResult = {
  code: number;
  stdout: string;
  stderr: string;
};

let tmpRoot = '';

async function writeFixtureFile(root: string, relativePath: string, content: string): Promise<void> {
  const absolutePath = path.join(root, relativePath);
  await mkdir(path.dirname(absolutePath), { recursive: true });
  await writeFile(absolutePath, content, 'utf8');
}

function sdkModuleSource(): string {
  return `
import { readFile } from 'node:fs/promises';
import path from 'node:path';

export async function* query({ options }) {
  if (!options.env?.ANTHROPIC_API_KEY) {
    throw new Error('missing api key');
  }
  const target = await readFile(path.join(options.cwd, 'proof-read-target.txt'), 'utf8');
  const proofToken = target.match(/PROOF_TOKEN=(.+)/)?.[1] ?? '';
  yield {
    type: 'system',
    subtype: 'init',
    session_id: 'live_packaged_sdk_proof_1',
    model: options.model,
    permissionMode: options.permissionMode
  };
  yield {
    type: 'assistant',
    message: {
      content: [{ type: 'tool_use', id: 'toolu_read', name: 'Read', input: { file_path: 'proof-read-target.txt' } }]
    },
    parent_tool_use_id: null,
    session_id: 'live_packaged_sdk_proof_1'
  };
  yield {
    type: 'result',
    subtype: 'success',
    is_error: false,
    result: proofToken,
    session_id: 'live_packaged_sdk_proof_1'
  };
}
`;
}

async function writePackagedSdkFixture(bundleRoot: string): Promise<void> {
  const platformPackageName = SDK_PLATFORM_PACKAGE_BY_RUNTIME[`${process.platform}:${process.arch}`];
  if (!platformPackageName) {
    throw new Error(`No test platform package mapping for ${process.platform}:${process.arch}`);
  }

  const sdkRoot = path.join(
    bundleRoot,
    'app.asar.unpacked',
    'node_modules',
    '@anthropic-ai',
    'claude-agent-sdk'
  );
  const platformRoot = path.join(sdkRoot, 'node_modules', platformPackageName);
  const binaryName = process.platform === 'win32' ? 'claude.exe' : 'claude';

  await writeFixtureFile(
    sdkRoot,
    'package.json',
    '{"name":"@anthropic-ai/claude-agent-sdk","version":"0.3.150","claudeCodeVersion":"2.1.150","type":"module"}\n'
  );
  await writeFixtureFile(sdkRoot, 'sdk.mjs', sdkModuleSource());
  await writeFixtureFile(platformRoot, 'package.json', `{"name":"${platformPackageName}"}\n`);
  const binaryPath = path.join(platformRoot, binaryName);
  await writeFile(binaryPath, '#!/bin/sh\n', 'utf8');
  await chmod(binaryPath, 0o755);
}

async function runProofInProcess(args: string[]): Promise<ScriptResult> {
  const stdout: string[] = [];
  const stderr: string[] = [];
  const code = await run(args, {
    cwd: process.cwd(),
    log: (line: string) => stdout.push(line),
    logError: (line: string) => stderr.push(line)
  });
  return { code, stdout: stdout.join('\n'), stderr: stderr.join('\n') };
}

async function runProof(args: string[], env: Record<string, string | undefined> = {}): Promise<ScriptResult> {
  try {
    const result = await execFileAsync('node', [SCRIPT_PATH, ...args], {
      cwd: process.cwd(),
      env: {
        ...process.env,
        ...env
      }
    });
    return {
      code: 0,
      stdout: result.stdout,
      stderr: result.stderr
    };
  } catch (error) {
    const failure = error as {
      code?: number;
      stdout?: string;
      stderr?: string;
    };
    return {
      code: typeof failure.code === 'number' ? failure.code : 1,
      stdout: failure.stdout ?? '',
      stderr: failure.stderr ?? ''
    };
  }
}

beforeEach(async () => {
  tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-live-packaged-sdk-proof-test-'));
});

afterEach(async () => {
  if (tmpRoot) {
    await rm(tmpRoot, { recursive: true, force: true });
  }
  tmpRoot = '';
});

describe('run-live-packaged-agent-sdk-read-tool-proof script', () => {
  it('passes with an explicit api key file and writes no key material to the summary', async () => {
    const bundleRoot = path.join(tmpRoot, 'bundle-root');
    const outputRoot = path.join(tmpRoot, 'output');
    const apiKeyFile = path.join(tmpRoot, 'anthropic_api_key');
    const apiKey = 'sk-ant-test-live-proof-redaction';

    await writePackagedSdkFixture(bundleRoot);
    await writeFile(apiKeyFile, `${apiKey}\n`, 'utf8');

    const result = await runProofInProcess([
      '--bundle-root',
      bundleRoot,
      '--output-root',
      outputRoot,
      '--api-key-file',
      apiKeyFile,
      '--model',
      'claude-test',
      '--timeout-ms',
      '30000'
    ]);

    expect(result.code, `${result.stdout}\n${result.stderr}`).toBe(0);
    expect(result.stdout).toContain('live packaged agentSdk read-tool proof status: pass');
    expect(result.stdout).not.toContain(apiKey);
    expect(result.stderr).not.toContain(apiKey);

    const summaryRaw = await readFile(path.join(outputRoot, 'summary.json'), 'utf8');
    expect(summaryRaw).not.toContain(apiKey);

    const summary = JSON.parse(summaryRaw) as {
      status: string;
      proofMode: string;
      apiKey: { source: string; redacted: boolean };
      observations: {
        readToolObserved: boolean;
        proofTokenObserved: boolean;
        sdkReportedError: boolean;
      };
      redaction: { passed: boolean; findings: unknown[] };
      liveRun: {
        allowedTools: string[];
        disallowedTools: string[];
        proofTarget: { proofTokenHash: string };
      };
    };

    expect(summary.status).toBe('pass');
    expect(summary.proofMode).toBe('live-packaged-read-tool');
    expect(summary.apiKey).toMatchObject({ source: 'api-key-file', redacted: true });
    expect(summary.observations).toMatchObject({
      readToolObserved: true,
      proofTokenObserved: true,
      sdkReportedError: false
    });
    expect(summary.redaction).toMatchObject({ passed: true, findings: [] });
    expect(summary.liveRun.allowedTools).toEqual(['Read']);
    expect(summary.liveRun.disallowedTools).toEqual(
      expect.arrayContaining(['Bash', 'Write', 'Edit', 'WebFetch', 'WebSearch', 'Agent', 'Task'])
    );
    expect(summary.liveRun.proofTarget.proofTokenHash).toMatch(/^[a-f0-9]{64}$/);
  });

  // Spawn-based CLI smoke test: proves the executable entrypoint itself
  // (main-guard, argv/env handling, non-zero process exit code) with a
  // controlled child environment; the passing-path test above calls run()
  // in-process.
  it('refuses to consume ambient API key env without explicit opt-in', async () => {
    const bundleRoot = path.join(tmpRoot, 'bundle-root');
    const outputRoot = path.join(tmpRoot, 'output');

    await writePackagedSdkFixture(bundleRoot);

    const result = await runProof(['--bundle-root', bundleRoot, '--output-root', outputRoot], {
      ANTHROPIC_API_KEY: 'sk-ant-test-ambient-refused'
    });

    expect(result.code).toBe(1);
    expect(result.stderr).toContain('Live proof requires --api-key-file <path> or explicit --allow-env-api-key.');
    expect(result.stderr).not.toContain('sk-ant-test-ambient-refused');
  });
});
