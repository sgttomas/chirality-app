import { execFile } from 'node:child_process';
import { realpath } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';

import { signAsync } from '@electron/osx-sign';

/**
 * Developer ID signing of the App and its bundled stock Codex (D-GOV-43, A2).
 *
 * electron-builder calls the default export as `mac.sign`. `@electron/osx-sign`
 * discovers every Mach-O under `Contents` on its own (`codex`,
 * `codex-code-mode-host`, `codex-path/rg`, the bundled `zsh`, the Electron
 * frameworks and helpers), so this hook only fixes the policy: the hardened
 * runtime everywhere, the App entitlements on the bundle, JIT only for the
 * Code Mode host, and the inherit entitlements for everything else. The
 * supplier digest, the native addon, the checkpoint phases and the signing
 * predicate of the supply model are gone; the packaged binary is checked
 * against the lockfile pin by `scripts/verify-codex-pin.mjs` instead.
 */

const execFileAsync = promisify(execFile);
const frontendRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

export const DEFAULT_ENTITLEMENTS = path.join(frontendRoot, 'build', 'entitlements.mac.plist');
export const DEFAULT_INHERIT_ENTITLEMENTS = path.join(frontendRoot, 'build', 'entitlements.mac.inherit.plist');
export const CODE_MODE_HOST_ENTITLEMENTS = path.join(frontendRoot, 'build', 'entitlements.mac.code-mode-host.plist');

/** Bundle-relative Codex binaries that must carry the App's signature. */
export const CODEX_SIGNED_BINARIES = Object.freeze([
  'Contents/Resources/codex/bin/codex',
  'Contents/Resources/codex/bin/codex-code-mode-host'
]);
export const CODEX_JIT_BINARY = 'Contents/Resources/codex/bin/codex-code-mode-host';

export function createSignOptions(options, {
  appPath,
  entitlements = DEFAULT_ENTITLEMENTS,
  inheritEntitlements = DEFAULT_INHERIT_ENTITLEMENTS,
  codeModeHostEntitlements = CODE_MODE_HOST_ENTITLEMENTS
}) {
  const original = options.optionsForFile;
  const jitBinary = path.join(appPath, CODEX_JIT_BINARY);
  return {
    ...options,
    optionsForFile(filePath) {
      const inherited = original?.(filePath) ?? {};
      const applicationBundle = filePath === appPath || filePath.endsWith('.app');
      return {
        ...inherited,
        hardenedRuntime: true,
        entitlements: filePath === jitBinary
          ? codeModeHostEntitlements
          : applicationBundle ? entitlements : inheritEntitlements
      };
    }
  };
}

/**
 * After signing: each Codex binary verifies strictly and carries the hardened
 * runtime flag, and the whole bundle verifies deep and strict.
 */
export async function verifySignedBundle(appPath, { execFile: run = execFileAsync } = {}) {
  const results = [];
  for (const relativePath of CODEX_SIGNED_BINARIES) {
    const target = path.join(appPath, relativePath);
    await run('/usr/bin/codesign', ['--verify', '--strict', target]);
    const { stderr } = await run('/usr/bin/codesign', ['-d', '--verbose=2', target]);
    if (!/flags=0x[0-9a-f]+\((?:[^)]*,)?runtime(?:,[^)]*)?\)/u.test(stderr)) {
      throw new Error(`Bundled Codex binary is not signed with the hardened runtime: ${relativePath}`);
    }
    results.push({ relativePath, hardenedRuntime: true });
  }
  await run('/usr/bin/codesign', ['--verify', '--deep', '--strict', '--verbose=2', appPath]);
  return { appPath, binaries: results };
}

/**
 * Builds the `mac.sign` hook. electron-builder calls the hook as
 * `sign(options, packager)`, so the injectable signer and verifier are bound
 * here rather than taken from the hook's second argument (which is the packager,
 * whose own `sign` method would otherwise be picked up unbound).
 */
export function createCustomMacSign({ sign = signAsync, verify = verifySignedBundle } = {}) {
  return async function customMacSign(options) {
    const appPath = await realpath(options.app);
    const entitlements = options.optionsForFile?.(appPath)?.entitlements ?? DEFAULT_ENTITLEMENTS;
    const inheritEntitlements =
      options.optionsForFile?.(path.join(appPath, 'Contents', 'Frameworks', 'nested'))?.entitlements
      ?? DEFAULT_INHERIT_ENTITLEMENTS;
    await sign(createSignOptions(options, { appPath, entitlements, inheritEntitlements }));
    return verify(appPath);
  };
}

export default createCustomMacSign();
