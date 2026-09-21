import { execFile } from 'node:child_process';
import { chmod, mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { promisify } from 'node:util';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { run } from '../../../scripts/verify-packaged-agent-sdk-runtime.mjs';

const execFileAsync = promisify(execFile);
const SCRIPT_PATH = path.resolve(process.cwd(), 'scripts', 'verify-packaged-agent-sdk-runtime.mjs');

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

function sdkModuleSource(mode: 'pass' | 'outside-command'): string {
  return `
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export function query({ options }) {
  const sdkRoot = path.dirname(fileURLToPath(import.meta.url));
  const command = ${
    mode === 'pass'
      ? "path.join(sdkRoot, 'node_modules', process.env.TEST_PLATFORM_PACKAGE_NAME, process.platform === 'win32' ? 'claude.exe' : 'claude')"
      : "path.join(sdkRoot, '..', '..', '..', 'outside-claude')"
  };
  options.spawnClaudeCodeProcess({
    command,
    args: ['--output-format', 'stream-json', '--input-format', 'stream-json'],
    cwd: options.cwd,
    env: options.env
  });
  return (async function* () {
    yield {
      type: 'system',
      subtype: 'init',
      session_id: 'packaged_sdk_proof_1'
    };
    yield {
      type: 'result',
      subtype: 'success',
      session_id: 'packaged_sdk_proof_1'
    };
  })();
}
`;
}

async function writePackagedSdkFixture(
  bundleRoot: string,
  mode: 'pass' | 'outside-command' = 'pass'
): Promise<void> {
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
  await writeFixtureFile(sdkRoot, 'sdk.mjs', sdkModuleSource(mode));
  await writeFixtureFile(sdkRoot, 'manifest.json', '{}\n');
  await writeFixtureFile(platformRoot, 'package.json', `{"name":"${platformPackageName}"}\n`);
  const binaryPath = path.join(platformRoot, binaryName);
  await writeFile(binaryPath, '#!/bin/sh\n', 'utf8');
  await chmod(binaryPath, 0o755);

  if (mode === 'outside-command') {
    const outsidePath = path.join(sdkRoot, '..', '..', '..', 'outside-claude');
    await writeFile(outsidePath, '#!/bin/sh\n', 'utf8');
    await chmod(outsidePath, 0o755);
  }
}

async function runProofSpawned(args: string[]): Promise<ScriptResult> {
  try {
    const result = await execFileAsync('node', [SCRIPT_PATH, ...args], {
      cwd: process.cwd(),
      env: {
        ...process.env,
        TEST_PLATFORM_PACKAGE_NAME: SDK_PLATFORM_PACKAGE_BY_RUNTIME[`${process.platform}:${process.arch}`]
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

async function runProof(args: string[]): Promise<ScriptResult> {
  const stdout: string[] = [];
  const stderr: string[] = [];
  const previous = process.env.TEST_PLATFORM_PACKAGE_NAME;
  process.env.TEST_PLATFORM_PACKAGE_NAME =
    SDK_PLATFORM_PACKAGE_BY_RUNTIME[`${process.platform}:${process.arch}`];
  try {
    const code = await run(args, {
      cwd: process.cwd(),
      log: (line: string) => stdout.push(line),
      logError: (line: string) => stderr.push(line)
    });
    return { code, stdout: stdout.join('\n'), stderr: stderr.join('\n') };
  } finally {
    if (previous === undefined) {
      delete process.env.TEST_PLATFORM_PACKAGE_NAME;
    } else {
      process.env.TEST_PLATFORM_PACKAGE_NAME = previous;
    }
  }
}

beforeEach(async () => {
  tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-packaged-sdk-proof-test-'));
});

afterEach(async () => {
  if (tmpRoot) {
    await rm(tmpRoot, { recursive: true, force: true });
  }
  tmpRoot = '';
});

describe('verify-packaged-agent-sdk-runtime script', () => {
  it('passes when the packaged SDK resolves the native command under app.asar.unpacked', async () => {
    const bundleRoot = path.join(tmpRoot, 'bundle-root');
    const outputRoot = path.join(tmpRoot, 'output');
    const projectRoot = path.join(tmpRoot, 'project');
    const configDir = path.join(tmpRoot, 'claude-config');
    const homeDir = path.join(tmpRoot, 'home');

    await writePackagedSdkFixture(bundleRoot);

    const result = await runProof([
      '--bundle-root',
      bundleRoot,
      '--output-root',
      outputRoot,
      '--project-root',
      projectRoot,
      '--config-dir',
      configDir,
      '--home-dir',
      homeDir
    ]);

    expect(result.code, `${result.stdout}\n${result.stderr}`).toBe(0);
    expect(result.stdout).toContain('packaged agentSdk runtime proof status: pass');

    const summaryRaw = await readFile(path.join(outputRoot, 'summary.json'), 'utf8');
    const summary = JSON.parse(summaryRaw) as {
      status: string;
      proofMode: string;
      resolver: {
        commandUnderUnpackedNodeModules: boolean;
        exists: boolean;
      };
      spawn: {
        env: {
          CLAUDE_CONFIG_DIR: string;
          HOME: string;
        };
        argsContainStreamJson: boolean;
      };
      sdkMessages: Array<{ type: string }>;
    };

    expect(summary.status).toBe('pass');
    expect(summary.proofMode).toBe('scripted-no-live-provider');
    expect(summary.resolver.commandUnderUnpackedNodeModules).toBe(true);
    expect(summary.resolver.exists).toBe(true);
    expect(summary.spawn.env.CLAUDE_CONFIG_DIR).toBe(path.resolve(configDir));
    expect(summary.spawn.env.HOME).toBe(path.resolve(homeDir));
    expect(summary.spawn.argsContainStreamJson).toBe(true);
    expect(summary.sdkMessages.map((message) => message.type)).toEqual(['system', 'result']);
  });

  // Spawn-based CLI smoke test: proves the executable entrypoint itself
  // (main-guard, argv handling, non-zero process exit code); the passing-path
  // test above calls run() in-process.
  it('fails when the packaged SDK resolves a command outside app.asar.unpacked', async () => {
    const bundleRoot = path.join(tmpRoot, 'bundle-root');
    const outputRoot = path.join(tmpRoot, 'output');

    await writePackagedSdkFixture(bundleRoot, 'outside-command');

    const result = await runProofSpawned(['--bundle-root', bundleRoot, '--output-root', outputRoot]);

    expect(result.code).toBe(1);
    expect(result.stdout).toContain('packaged agentSdk runtime proof status: fail');
    expect(result.stderr).toContain('outside app.asar.unpacked/node_modules');

    const summaryRaw = await readFile(path.join(outputRoot, 'summary.json'), 'utf8');
    const summary = JSON.parse(summaryRaw) as {
      status: string;
      failures: string[];
      resolver: {
        commandUnderUnpackedNodeModules: boolean;
      };
    };

    expect(summary.status).toBe('fail');
    expect(summary.resolver.commandUnderUnpackedNodeModules).toBe(false);
    expect(summary.failures).toEqual(
      expect.arrayContaining([
        expect.stringContaining('outside app.asar.unpacked/node_modules')
      ])
    );
  });
});
