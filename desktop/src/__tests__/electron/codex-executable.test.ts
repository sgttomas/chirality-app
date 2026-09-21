import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import {
  CODEX_JIT_BINARY,
  CODEX_PINNED_VERSION,
  CODEX_SIGNED_BINARIES,
  codexExecutablePath,
  resolveCodexExecutable,
  resolveCodexPlatformPackageName,
  resolveCodexTargetTriple,
  resolveDevelopmentCodexVendorRoot,
  resolvePackagedCodexVendorRoot
} from '../../../electron/codex-executable';

describe('codex executable resolution', () => {
  it('pins the same exact version as package.json and the lockfile', async () => {
    const packageJson = JSON.parse(await readFile(path.resolve(process.cwd(), 'package.json'), 'utf8'));
    const lockfile = JSON.parse(await readFile(path.resolve(process.cwd(), 'package-lock.json'), 'utf8'));
    expect(packageJson.dependencies['@openai/codex']).toBe(CODEX_PINNED_VERSION);
    expect(lockfile.packages['node_modules/@openai/codex'].version).toBe(CODEX_PINNED_VERSION);
    expect(packageJson.dependencies['@chirality/native-admission']).toBeUndefined();
  });

  it('maps every supported host to the upstream target triple and platform package', () => {
    expect(resolveCodexTargetTriple('darwin', 'arm64')).toBe('aarch64-apple-darwin');
    expect(resolveCodexTargetTriple('darwin', 'x64')).toBe('x86_64-apple-darwin');
    expect(resolveCodexTargetTriple('linux', 'x64')).toBe('x86_64-unknown-linux-musl');
    expect(resolveCodexTargetTriple('linux', 'arm64')).toBe('aarch64-unknown-linux-musl');
    expect(resolveCodexTargetTriple('win32', 'x64')).toBe('x86_64-pc-windows-msvc');
    expect(resolveCodexPlatformPackageName('darwin', 'arm64')).toBe('@openai/codex-darwin-arm64');
    expect(() => resolveCodexTargetTriple('sunos', 'x64')).toThrow(/Unsupported Codex platform/);
  });

  it('reads the development binary from the installed platform package', () => {
    const vendorRoot = resolveDevelopmentCodexVendorRoot('/repo/frontend/node_modules', 'darwin', 'arm64');
    expect(vendorRoot).toBe('/repo/frontend/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin');
    expect(codexExecutablePath(vendorRoot, 'darwin')).toBe(`${vendorRoot}/bin/codex`);
    expect(codexExecutablePath(vendorRoot, 'win32')).toBe(`${vendorRoot}/bin/codex.exe`);
    expect(resolveCodexExecutable({ packaged: false, resourcesPath: '/unused', nodeModulesRoot: '/repo/frontend/node_modules', platform: 'darwin', arch: 'arm64' })).toEqual({
      vendorRoot,
      executablePath: `${vendorRoot}/bin/codex`,
      source: 'development-package'
    });
  });

  it('reads the packaged binary from Contents/Resources/codex', () => {
    const resources = '/Applications/Chirality.app/Contents/Resources';
    expect(resolvePackagedCodexVendorRoot(resources)).toBe(`${resources}/codex`);
    expect(resolveCodexExecutable({ packaged: true, resourcesPath: resources, nodeModulesRoot: '/unused', platform: 'darwin', arch: 'arm64' })).toEqual({
      vendorRoot: `${resources}/codex`,
      executablePath: `${resources}/codex/bin/codex`,
      source: 'packaged-resources'
    });
  });

  it('names the two signed binaries and the one that needs JIT', () => {
    expect([...CODEX_SIGNED_BINARIES]).toEqual(['bin/codex', 'bin/codex-code-mode-host']);
    expect(CODEX_JIT_BINARY).toBe('bin/codex-code-mode-host');
  });
});
