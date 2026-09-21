import { mkdir, mkdtemp, realpath, rm, symlink, truncate, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';

import {
  ELECTRON_SUPPLY_PIN,
  resolveElectronDistDirectory,
  runCli,
  verifyElectronDist
} from '../../../scripts/verify-electron-dist.mjs';

const cleanupPaths: string[] = [];

async function fixture({
  version = ELECTRON_SUPPLY_PIN.version,
  size = ELECTRON_SUPPLY_PIN.size
}: { version?: string; size?: number } = {}) {
  const root = await realpath(
    await mkdtemp(path.join(os.tmpdir(), 'chirality-electron-supply-'))
  );
  cleanupPaths.push(root);
  const directory = path.join(root, 'electron dist');
  await mkdir(directory);
  const archivePath = path.join(directory, ELECTRON_SUPPLY_PIN.filename);
  await writeFile(archivePath, '');
  await truncate(archivePath, size);
  const packageJsonPath = path.join(root, 'package.json');
  await writeFile(
    packageJsonPath,
    JSON.stringify({ devDependencies: { electron: version } })
  );
  return { root, directory, archivePath, packageJsonPath };
}

afterEach(async () => {
  await Promise.all(cleanupPaths.splice(0).map((entry) => rm(entry, { recursive: true })));
});

describe('verify-electron-dist', () => {
  it('accepts only the pinned archive and emits success on stdout only', async () => {
    const value = await fixture();
    const stdout: string[] = [];
    const stderr: string[] = [];
    const exitCode = await runCli({
      argv: [],
      stdout: { write: (text: string) => stdout.push(text) },
      stderr: { write: (text: string) => stderr.push(text) },
      verify: () =>
        verifyElectronDist({
          directory: value.directory,
          packageJsonPath: value.packageJsonPath,
          hashArchive: async () => ELECTRON_SUPPLY_PIN.sha256
        })
    });

    expect(exitCode).toBe(0);
    expect(stdout).toEqual([`${value.directory}\n`]);
    expect(stderr).toEqual([]);
  });

  it('fails for a missing archive', async () => {
    const value = await fixture();
    await rm(value.archivePath);
    await expect(
      verifyElectronDist({ directory: value.directory, packageJsonPath: value.packageJsonPath })
    ).rejects.toThrow();
  });

  it('fails for an archive symlink', async () => {
    const value = await fixture();
    const target = path.join(value.root, 'target.zip');
    await writeFile(target, '');
    await truncate(target, ELECTRON_SUPPLY_PIN.size);
    await rm(value.archivePath);
    await symlink(target, value.archivePath);
    await expect(
      verifyElectronDist({ directory: value.directory, packageJsonPath: value.packageJsonPath })
    ).rejects.toThrow('regular non-symlink');
  });

  it('fails for the wrong size before hashing', async () => {
    const value = await fixture({ size: 1 });
    let hashCalled = false;
    await expect(
      verifyElectronDist({
        directory: value.directory,
        packageJsonPath: value.packageJsonPath,
        hashArchive: async () => {
          hashCalled = true;
          return ELECTRON_SUPPLY_PIN.sha256;
        }
      })
    ).rejects.toThrow('size mismatch');
    expect(hashCalled).toBe(false);
  });

  it('fails for the wrong hash', async () => {
    const value = await fixture();
    await expect(
      verifyElectronDist({
        directory: value.directory,
        packageJsonPath: value.packageJsonPath,
        hashArchive: async () => '0'.repeat(64)
      })
    ).rejects.toThrow('SHA-256 mismatch');
  });

  it('fails for Electron version drift', async () => {
    const value = await fixture({ version: '43.2.1' });
    await expect(
      verifyElectronDist({ directory: value.directory, packageJsonPath: value.packageJsonPath })
    ).rejects.toThrow('Electron devDependency');
  });

  it('rejects empty, relative, NUL, root, and non-normalized paths', () => {
    const resolve = (value: string) =>
      resolveElectronDistDirectory({
        env: { NODE_ENV: 'test', CHIRALITY_ELECTRON_DIST_DIR: value }
      });
    expect(() => resolve('')).toThrow();
    expect(() => resolve('relative')).toThrow();
    expect(() => resolve('/tmp/nul\0path')).toThrow();
    expect(() => resolve('/')).toThrow();
    expect(() => resolve('/tmp/../tmp/cache')).toThrow();
  });

  it('does not expose a command-line pin bypass', async () => {
    let verifyCalled = false;
    const stderr: string[] = [];
    const exitCode = await runCli({
      argv: ['--sha256', '0'.repeat(64)],
      stdout: { write: () => undefined },
      stderr: { write: (text: string) => stderr.push(text) },
      verify: async () => {
        verifyCalled = true;
        return '/unused';
      }
    });
    expect(exitCode).toBe(1);
    expect(verifyCalled).toBe(false);
    expect(stderr.join('')).toContain('does not accept command-line arguments');
  });
});
