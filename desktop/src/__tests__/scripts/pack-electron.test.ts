import type { spawn } from 'node:child_process';
import { EventEmitter } from 'node:events';
import { chmod, mkdir, mkdtemp, realpath, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it, vi } from 'vitest';

import {
  ELECTRON_OUTPUT_DIRECTORY_ENV,
  REQUIRED_BUILD_INPUTS,
  SIGNING_IDENTITY_SHA1_ENV,
  assertPackagingInputs,
  buildElectronBuilderArgs,
  expectedPackagedAppPath,
  parseArgs,
  resolveElectronOutputDirectory,
  runElectronPack,
  signingEnvironment
} from '../../../scripts/pack-electron.mjs';

const cleanup: string[] = [];
afterEach(async () => {
  await Promise.all(cleanup.splice(0).map((entry) => rm(entry, { recursive: true, force: true })));
});

function fakeSpawn(exitCode = 0) {
  const calls: Array<{ command: string; args: string[]; options: Record<string, unknown> }> = [];
  const spawnProcess = vi.fn((command: string, args: string[], options: Record<string, unknown>) => {
    calls.push({ command, args, options });
    const child = new EventEmitter();
    queueMicrotask(() => child.emit('exit', exitCode, null));
    return child;
  }) as unknown as typeof spawn;
  return { spawnProcess, calls };
}

async function fixtureRoot(options: { codexExecutable?: boolean; codexVersion?: string } = {}) {
  const root = await realpath(await mkdtemp(path.join(os.tmpdir(), 'chirality-pack-')));
  cleanup.push(root);
  for (const relativePath of REQUIRED_BUILD_INPUTS) {
    await mkdir(path.dirname(path.join(root, relativePath)), { recursive: true });
    await writeFile(path.join(root, relativePath), 'x');
  }
  const vendor = 'node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin';
  await mkdir(path.join(root, vendor, 'bin'), { recursive: true });
  await writeFile(path.join(root, vendor, 'bin', 'codex'), 'bin');
  await writeFile(path.join(root, vendor, 'bin', 'codex-code-mode-host'), 'bin');
  if (options.codexExecutable !== false) await chmod(path.join(root, vendor, 'bin', 'codex'), 0o755);
  const packageJson = {
    dependencies: { '@openai/codex': options.codexVersion ?? '0.154.0' },
    build: {
      extraResources: [
        { from: vendor, to: 'codex', filter: ['**/*'] },
        { from: 'dist-runtime/runtime-service', to: 'runtime-service', filter: ['**/*'] },
        { from: 'dist-runtime/runtime-cli', to: 'runtime-cli', filter: ['**/*'] },
        { from: 'node_modules/.cache/chirality-instruction-root', to: 'instruction-root', filter: ['**/*'] }
      ]
    }
  };
  await writeFile(path.join(root, 'package.json'), JSON.stringify(packageJson));
  return { root, packageJson };
}

describe('pack-electron', () => {
  it('passes exactly one spaces-safe electronDist argument without a shell and never discovers a keychain identity', async () => {
    const { spawnProcess, calls } = fakeSpawn();
    const result = await runElectronPack({
      verify: async () => '/Users/tester/Library/Caches/chirality/electron dist',
      spawnProcess,
      assertInputs: async () => ({ extraResources: [], codexVersion: '0.154.0' }),
      env: { NODE_ENV: 'test', [ELECTRON_OUTPUT_DIRECTORY_ENV]: '/private/tmp/candidate' }
    });
    expect(calls).toHaveLength(1);
    expect(calls[0].command).toBe('electron-builder');
    expect(calls[0].args).toEqual([
      '--mac', '--dir', '--arm64', '--publish', 'never',
      '-c.electronDist=/Users/tester/Library/Caches/chirality/electron dist',
      '-c.directories.output=/private/tmp/candidate'
    ]);
    expect(calls[0].options.shell).toBe(false);
    expect((calls[0].options.env as Record<string, string>).CSC_IDENTITY_AUTO_DISCOVERY).toBe('false');
    expect((calls[0].options.env as Record<string, string>).CSC_NAME).toBeUndefined();
    expect(result).toEqual({ appPath: '/private/tmp/candidate/mac-arm64/Chirality.app', target: 'dir', signed: false });
  });

  it('selects Developer ID signing only through an explicit identity SHA-1', async () => {
    expect(signingEnvironment({ NODE_ENV: 'test' })).toEqual({ CSC_IDENTITY_AUTO_DISCOVERY: 'false' });
    expect(signingEnvironment({ NODE_ENV: 'test', [SIGNING_IDENTITY_SHA1_ENV]: 'A'.repeat(40) })).toEqual({ CSC_NAME: 'A'.repeat(40), CSC_IDENTITY_AUTO_DISCOVERY: 'true' });
    expect(() => signingEnvironment({ NODE_ENV: 'test', [SIGNING_IDENTITY_SHA1_ENV]: 'not-a-sha1' })).toThrow(/uppercase SHA-1/);
    const { spawnProcess, calls } = fakeSpawn();
    const result = await runElectronPack({
      verify: async () => '/dist',
      spawnProcess,
      assertInputs: async () => ({ extraResources: [], codexVersion: '0.154.0' }),
      env: { NODE_ENV: 'test', [SIGNING_IDENTITY_SHA1_ENV]: 'B'.repeat(40) },
      target: 'dmg'
    });
    expect(calls[0].args.slice(0, 2)).toEqual(['--mac', 'dmg']);
    expect((calls[0].options.env as Record<string, string>).CSC_NAME).toBe('B'.repeat(40));
    expect(result.signed).toBe(true);
  });

  it('checks every packaging input before invoking the builder', async () => {
    const { root } = await fixtureRoot();
    await expect(assertPackagingInputs({ root })).resolves.toMatchObject({ codexVersion: '0.154.0' });

    const broken = await fixtureRoot({ codexExecutable: false });
    await expect(assertPackagingInputs({ root: broken.root })).rejects.toThrow(/not executable/);

    const unpinned = await fixtureRoot({ codexVersion: '^0.154.0' });
    await expect(assertPackagingInputs({ root: unpinned.root })).rejects.toThrow(/exact version/);

    const missing = await fixtureRoot();
    await rm(path.join(missing.root, 'dist-runtime', 'runtime-service', 'standalone-bin.mjs'));
    await expect(assertPackagingInputs({ root: missing.root })).rejects.toThrow(/missing build input dist-runtime\/runtime-service\/standalone-bin.mjs/);

    const { spawnProcess, calls } = fakeSpawn();
    await expect(runElectronPack({
      verify: async () => '/dist',
      spawnProcess,
      assertInputs: () => assertPackagingInputs({ root: missing.root }),
      env: { NODE_ENV: 'test' }
    })).rejects.toThrow(/Packaging inputs are incomplete/);
    expect(calls).toHaveLength(0);
  });

  it('rejects malformed output directories, targets and arguments', () => {
    expect(resolveElectronOutputDirectory({ NODE_ENV: 'test' }, '/frontend')).toBe('/frontend/dist');
    expect(resolveElectronOutputDirectory({ NODE_ENV: 'test', [ELECTRON_OUTPUT_DIRECTORY_ENV]: '/private/tmp/c' })).toBe('/private/tmp/c');
    expect(() => resolveElectronOutputDirectory({ NODE_ENV: 'test', [ELECTRON_OUTPUT_DIRECTORY_ENV]: 'relative' })).toThrow(/normalized absolute path/);
    expect(() => resolveElectronOutputDirectory({ NODE_ENV: 'test', [ELECTRON_OUTPUT_DIRECTORY_ENV]: '' })).toThrow(/normalized absolute path/);
    expect(expectedPackagedAppPath('/out')).toBe('/out/mac-arm64/Chirality.app');
    expect(() => buildElectronBuilderArgs('/dist', 'zip')).toThrow(/Unsupported Electron packaging target/);
    expect(() => buildElectronBuilderArgs('', 'dir')).toThrow(/required/);
    expect(parseArgs([])).toEqual({ target: 'dir' });
    expect(parseArgs(['--target', 'dmg'])).toEqual({ target: 'dmg' });
    expect(() => parseArgs(['--runtime-manifest', 'v2'])).toThrow(/Usage/);
  });

  it('surfaces a builder failure', async () => {
    const { spawnProcess } = fakeSpawn(3);
    await expect(runElectronPack({
      verify: async () => '/dist',
      spawnProcess,
      assertInputs: async () => ({ extraResources: [], codexVersion: '0.154.0' }),
      env: { NODE_ENV: 'test' }
    })).rejects.toThrow('electron-builder exited with status 3');
  });
});
