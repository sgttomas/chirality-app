/**
 * Stock Codex executable resolution (D-GOV-43, topology A2).
 *
 * The App ships the lockfile-pinned `@openai/codex` platform package. In
 * development the binary is read from the installed platform package under
 * `node_modules`; in the packaged App the whole `vendor/<triple>` tree is
 * staged to `Contents/Resources/codex` so `codex-path/rg` and
 * `codex-resources` travel with the binary. This module is `electron`-free so
 * the mapping is checkable under plain Node.
 */

import path from 'node:path';

/** Must equal the exact `@openai/codex` dependency pin in `package.json`. */
export const CODEX_PINNED_VERSION = '0.154.0';

/** Packaged resources directory (relative to `Contents/Resources`) holding the vendor tree. */
export const PACKAGED_CODEX_RESOURCE_DIRECTORY = 'codex';

/**
 * Mach-O executables inside the vendor tree that carry the App's signature and
 * the hardened runtime. `codex-code-mode-host` needs JIT; `codex` does not.
 */
export const CODEX_SIGNED_BINARIES = Object.freeze(['bin/codex', 'bin/codex-code-mode-host']);
export const CODEX_JIT_BINARY = 'bin/codex-code-mode-host';

const TARGET_TRIPLES: Readonly<Record<string, string>> = Object.freeze({
  'darwin-arm64': 'aarch64-apple-darwin',
  'darwin-x64': 'x86_64-apple-darwin',
  'linux-arm64': 'aarch64-unknown-linux-musl',
  'linux-x64': 'x86_64-unknown-linux-musl',
  'win32-arm64': 'aarch64-pc-windows-msvc',
  'win32-x64': 'x86_64-pc-windows-msvc'
});

export function resolveCodexTargetTriple(platform: string, arch: string): string {
  const triple = TARGET_TRIPLES[`${platform}-${arch}`];
  if (!triple) {
    throw new Error(`Unsupported Codex platform: ${platform} (${arch})`);
  }
  return triple;
}

/** The optional platform package `@openai/codex` installs for this host. */
export function resolveCodexPlatformPackageName(platform: string, arch: string): string {
  resolveCodexTargetTriple(platform, arch);
  return `@openai/codex-${platform}-${arch}`;
}

/** `node_modules/@openai/codex-<platform>-<arch>/vendor/<triple>` (development). */
export function resolveDevelopmentCodexVendorRoot(
  nodeModulesRoot: string,
  platform: string = process.platform,
  arch: string = process.arch
): string {
  return path.join(
    nodeModulesRoot,
    '@openai',
    `codex-${platform}-${arch}`,
    'vendor',
    resolveCodexTargetTriple(platform, arch)
  );
}

/** `Contents/Resources/codex` (packaged). */
export function resolvePackagedCodexVendorRoot(resourcesPath: string): string {
  return path.join(path.resolve(resourcesPath), PACKAGED_CODEX_RESOURCE_DIRECTORY);
}

export function codexExecutablePath(vendorRoot: string, platform: string = process.platform): string {
  return path.join(vendorRoot, 'bin', platform === 'win32' ? 'codex.exe' : 'codex');
}

export type CodexExecutableResolution = {
  vendorRoot: string;
  executablePath: string;
  source: 'development-package' | 'packaged-resources';
};

export function resolveCodexExecutable(input: {
  packaged: boolean;
  resourcesPath: string;
  nodeModulesRoot: string;
  platform?: string;
  arch?: string;
}): CodexExecutableResolution {
  const platform = input.platform ?? process.platform;
  const arch = input.arch ?? process.arch;
  if (input.packaged) {
    const vendorRoot = resolvePackagedCodexVendorRoot(input.resourcesPath);
    return { vendorRoot, executablePath: codexExecutablePath(vendorRoot, platform), source: 'packaged-resources' };
  }
  const vendorRoot = resolveDevelopmentCodexVendorRoot(input.nodeModulesRoot, platform, arch);
  return { vendorRoot, executablePath: codexExecutablePath(vendorRoot, platform), source: 'development-package' };
}
