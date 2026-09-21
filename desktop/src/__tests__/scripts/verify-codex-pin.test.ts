import { chmod, mkdir, mkdtemp, realpath, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';

import {
  COMPARED_BINARIES,
  hashFile,
  parseArgs,
  parseCodexVersionOutput,
  readLockfileCodexVersions,
  resolveInstalledCodexVendorRoot,
  resolvePackagedResourcesRoot,
  verifyCodexPin
} from '../../../scripts/verify-codex-pin.mjs';

const cleanup: string[] = [];
afterEach(async () => {
  await Promise.all(cleanup.splice(0).map((entry) => rm(entry, { recursive: true, force: true })));
});

function lockfile(version = '0.154.0') {
  return {
    packages: {
      'node_modules/@openai/codex': { version },
      'node_modules/@openai/codex-darwin-arm64': { name: '@openai/codex', version: `${version}-darwin-arm64` }
    }
  };
}

async function fixture({ pinned = '0.154.0', locked = '0.154.0', packagedBytes = 'codex-bytes', reportedVersion = 'codex-cli 0.154.0\n', stagedVersion = '0.154.0' } = {}) {
  const root = await realpath(await mkdtemp(path.join(os.tmpdir(), 'chirality-codex-pin-')));
  cleanup.push(root);
  await writeFile(path.join(root, 'package.json'), JSON.stringify({ dependencies: { '@openai/codex': pinned } }));
  await writeFile(path.join(root, 'package-lock.json'), JSON.stringify(lockfile(locked)));
  const installed = resolveInstalledCodexVendorRoot(root, 'darwin', 'arm64');
  const resourcesRoot = path.join(root, 'dist', 'mac-arm64', 'Chirality.app', 'Contents', 'Resources');
  const packaged = path.join(resourcesRoot, 'codex');
  for (const relativePath of COMPARED_BINARIES) {
    for (const [vendorRoot, bytes] of [[installed, 'codex-bytes'], [packaged, packagedBytes]] as const) {
      await mkdir(path.dirname(path.join(vendorRoot, relativePath)), { recursive: true });
      await writeFile(path.join(vendorRoot, relativePath), `${bytes}:${relativePath}`);
      await chmod(path.join(vendorRoot, relativePath), 0o755);
    }
  }
  await writeFile(path.join(packaged, 'codex-package.json'), JSON.stringify({ version: stagedVersion, target: 'aarch64-apple-darwin', entrypoint: 'bin/codex' }));
  const runVersion = async (executable: string) => {
    if (executable !== path.join(packaged, 'bin', 'codex')) throw new Error(`unexpected executable ${executable}`);
    return reportedVersion;
  };
  return { root, resourcesRoot, runVersion };
}

describe('verify-codex-pin', () => {
  it('reads the lockfile pin and the matching platform package', () => {
    expect(readLockfileCodexVersions(lockfile(), 'darwin', 'arm64')).toEqual({
      version: '0.154.0',
      platformVersion: '0.154.0-darwin-arm64',
      platformKey: 'node_modules/@openai/codex-darwin-arm64'
    });
    expect(() => readLockfileCodexVersions({ packages: {} }, 'darwin', 'arm64')).toThrow(/does not resolve @openai\/codex/);
    expect(() => readLockfileCodexVersions({
      packages: { 'node_modules/@openai/codex': { version: '0.154.0' }, 'node_modules/@openai/codex-darwin-arm64': { name: '@openai/codex', version: '0.153.0-darwin-arm64' } }
    }, 'darwin', 'arm64')).toThrow(/expected @openai\/codex@0.154.0-darwin-arm64/);
    expect(resolveInstalledCodexVendorRoot('/f', 'darwin', 'arm64')).toBe('/f/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin');
    expect(resolvePackagedResourcesRoot({ NODE_ENV: 'test' }, '/f')).toBe('/f/dist/mac-arm64/Chirality.app/Contents/Resources');
    expect(resolvePackagedResourcesRoot({ NODE_ENV: 'test', CHIRALITY_ELECTRON_OUTPUT_DIRECTORY: '/private/tmp/c' })).toBe('/private/tmp/c/mac-arm64/Chirality.app/Contents/Resources');
    expect(parseCodexVersionOutput('codex-cli 0.154.0\n')).toBe('0.154.0');
    expect(() => parseCodexVersionOutput('Codex CLI v1')).toThrow(/Unrecognised/);
    expect(parseArgs(['--after-signing'])).toEqual({ afterSigning: true });
    expect(() => parseArgs(['--x'])).toThrow(/Usage/);
  });

  it('passes when the packaged version, digest and staged manifest all match the lockfile', async () => {
    const f = await fixture();
    const summary = await verifyCodexPin({ root: f.root, resourcesRoot: f.resourcesRoot, platform: 'darwin', arch: 'arm64', runVersion: f.runVersion });
    expect(summary.status).toBe('PASS');
    expect(summary.failures).toEqual([]);
    expect(summary.packagedVersion).toBe('0.154.0');
    expect(summary.lockfilePlatformPackage).toBe('node_modules/@openai/codex-darwin-arm64@0.154.0-darwin-arm64');
    expect(summary.binaries.map((binary: { matches: boolean | null }) => binary.matches)).toEqual([true, true]);
    expect(summary.binaries[0].packagedSha256).toBe(await hashFile(path.join(f.resourcesRoot, 'codex', 'bin', 'codex')));
  });

  it('fails on a version drift, a digest drift or a package.json pin drift', async () => {
    const version = await fixture({ reportedVersion: 'codex-cli 0.155.0\n' });
    expect((await verifyCodexPin({ root: version.root, resourcesRoot: version.resourcesRoot, platform: 'darwin', arch: 'arm64', runVersion: version.runVersion })).failures)
      .toEqual(['packaged codex reports 0.155.0, lockfile resolves 0.154.0']);

    const digest = await fixture({ packagedBytes: 'tampered' });
    const digestSummary = await verifyCodexPin({ root: digest.root, resourcesRoot: digest.resourcesRoot, platform: 'darwin', arch: 'arm64', runVersion: digest.runVersion });
    expect(digestSummary.failures).toEqual([
      'packaged bin/codex sha256 differs from the installed @openai/codex platform package',
      'packaged bin/codex-code-mode-host sha256 differs from the installed @openai/codex platform package'
    ]);
    // After signing the bytes legitimately differ; only the version and manifest are compared.
    const signed = await verifyCodexPin({ root: digest.root, resourcesRoot: digest.resourcesRoot, platform: 'darwin', arch: 'arm64', runVersion: digest.runVersion, afterSigning: true });
    expect(signed.status).toBe('PASS');
    expect(signed.binaries[0].matches).toBe(false);

    const pin = await fixture({ pinned: '^0.154.0' });
    expect((await verifyCodexPin({ root: pin.root, resourcesRoot: pin.resourcesRoot, platform: 'darwin', arch: 'arm64', runVersion: pin.runVersion })).failures)
      .toEqual(['package.json pins @openai/codex@^0.154.0 but the lockfile resolves 0.154.0']);

    const staged = await fixture({ stagedVersion: '0.153.0' });
    expect((await verifyCodexPin({ root: staged.root, resourcesRoot: staged.resourcesRoot, platform: 'darwin', arch: 'arm64', runVersion: staged.runVersion })).failures)
      .toEqual(['staged codex-package.json records 0.153.0, lockfile resolves 0.154.0']);
  });

  it('fails when the packaged binary cannot report its version', async () => {
    const f = await fixture();
    const summary = await verifyCodexPin({
      root: f.root,
      resourcesRoot: f.resourcesRoot,
      platform: 'darwin',
      arch: 'arm64',
      runVersion: async () => {
        throw new Error('spawn EACCES');
      }
    });
    expect(summary.status).toBe('FAIL');
    expect(summary.failures).toEqual(['packaged codex --version failed: spawn EACCES']);
  });
});
