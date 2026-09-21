import { chmod, mkdir, mkdtemp, realpath, rm, symlink, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import {
  findForbiddenLegacyRuntimePackage,
  resolvePackagedDependencyBundlePath,
  verifyPackagedCodexTree,
  verifyPackagedRuntimeSources
} from '../../../scripts/verify-packaged-dependency-boundary.mjs';

const desktopSources = [
  '../electron/main.ts',
  '../electron/runtime-service-host.ts',
  '../electron/runtime-service-launcher.ts',
  '../../../chirality-runtime/packages/client/src/client.ts'
];
const serviceSources = [
  '../../../chirality-runtime/packages/daemon/src/standalone-bin.ts',
  '../../../chirality-runtime/packages/daemon/src/runtime-daemon.ts',
  '../../../chirality-runtime/packages/daemon/src/codex-supervisor.ts',
  '../../../chirality-runtime/packages/daemon/src/codex-app-server-client.ts',
  '../../../chirality-runtime/packages/core/src/runtime-service.ts',
  '../../../chirality-runtime/packages/core/src/delegated-runtime.ts'
];
const cliSources = [
  '../../../chirality-runtime/packages/cli/src/bin.ts',
  '../../../chirality-runtime/packages/cli/src/cli.ts',
  '../../../chirality-runtime/packages/client/src/client.ts'
];
const packagedEntries = new Set(['/dist-electron/main.js', '/dist-electron/main.js.map']);

const cleanup: string[] = [];
afterEach(async () => {
  await Promise.all(cleanup.splice(0).map((entry) => rm(entry, { recursive: true, force: true })));
});

describe('packaged App-owned runtime source proof', () => {
  it('resolves the dependency check from the shared explicit candidate output', () => {
    expect(resolvePackagedDependencyBundlePath({
      NODE_ENV: 'test',
      CHIRALITY_ELECTRON_OUTPUT_DIRECTORY: '/private/tmp/chirality candidate'
    })).toBe('/private/tmp/chirality candidate/mac-arm64/Chirality.app/Contents/Resources/app.asar');
    expect(() => resolvePackagedDependencyBundlePath({
      NODE_ENV: 'test',
      CHIRALITY_ELECTRON_OUTPUT_DIRECTORY: ''
    })).toThrow('must be a normalized absolute path');
  });

  it('accepts a main bundle without the daemon, a service bundle with the stock Codex client, and a client-only CLI', () => {
    expect(
      verifyPackagedRuntimeSources({ desktopSources, serviceSources, cliSources, packagedEntries }).failures
    ).toEqual([]);
  });

  it('fails closed when the main bundle embeds the daemon or a retired supply-model source', () => {
    const { failures } = verifyPackagedRuntimeSources({
      desktopSources: [
        ...desktopSources,
        '../../../chirality-runtime/packages/daemon/src/runtime-daemon.ts',
        '../electron/runtime-host.ts',
        '../electron/runtime-autostart.ts'
      ],
      serviceSources,
      cliSources,
      packagedEntries
    });
    expect(failures).toEqual(expect.arrayContaining([
      'desktop bundle unexpectedly embeds retired or legacy source chirality-runtime/packages/daemon/src/runtime-daemon.ts',
      'desktop bundle unexpectedly embeds retired or legacy source electron/runtime-host.ts',
      'desktop bundle unexpectedly embeds retired or legacy source electron/runtime-autostart.ts'
    ]));
  });

  it('fails closed when the service bundle lacks the stock client or carries the hosted composition', () => {
    const { failures } = verifyPackagedRuntimeSources({
      desktopSources,
      serviceSources: [
        ...serviceSources.filter((source) => !source.endsWith('codex-app-server-client.ts')),
        '../../../chirality-runtime/packages/daemon/src/hosted-private-composition.ts',
        '../../../chirality-runtime/packages/daemon/src/codex-containment.ts'
      ],
      cliSources: [...cliSources, '../../../chirality-runtime/packages/daemon/src/runtime-daemon.ts'],
      packagedEntries: new Set(['/dist-electron/main.js'])
    });
    expect(failures).toEqual(expect.arrayContaining([
      'runtime service bundle is missing source chirality-runtime/packages/daemon/src/codex-app-server-client.ts',
      'runtime service bundle unexpectedly embeds retired or legacy source chirality-runtime/packages/daemon/src/hosted-private-composition.ts',
      'runtime service bundle unexpectedly embeds retired or legacy source chirality-runtime/packages/daemon/src/codex-containment.ts',
      'CLI client bundle unexpectedly embeds server source chirality-runtime/packages/daemon/src/runtime-daemon.ts',
      'app.asar is missing /dist-electron/main.js.map'
    ]));
  });

  it('flags legacy runtime packages and Claude platform packages', () => {
    expect(findForbiddenLegacyRuntimePackage('/node_modules/@anthropic-ai/sdk/index.js')).toBe('@anthropic-ai/sdk');
    expect(findForbiddenLegacyRuntimePackage('/node_modules/@anthropic-ai/claude-agent-sdk-darwin-arm64/cli')).toBe('@anthropic-ai/claude-agent-sdk-darwin-arm64');
    expect(findForbiddenLegacyRuntimePackage('/node_modules/next/dist/server.js')).toBeNull();
  });

  it('checks the staged Codex tree for regular executable binaries and its manifest', async () => {
    const root = await realpath(await mkdtemp(path.join(os.tmpdir(), 'chirality-codex-tree-')));
    cleanup.push(root);
    const vendor = path.join(root, 'codex');
    await mkdir(path.join(vendor, 'bin'), { recursive: true });
    await writeFile(path.join(vendor, 'bin', 'codex'), 'bin');
    await writeFile(path.join(vendor, 'bin', 'codex-code-mode-host'), 'bin');
    await chmod(path.join(vendor, 'bin', 'codex'), 0o755);
    await chmod(path.join(vendor, 'bin', 'codex-code-mode-host'), 0o755);
    await writeFile(path.join(vendor, 'codex-package.json'), JSON.stringify({ entrypoint: 'bin/codex' }));
    await expect(verifyPackagedCodexTree({ resourcesRoot: root })).resolves.toEqual({ status: 'PASS', path: vendor, failures: [] });

    await rm(path.join(vendor, 'bin', 'codex'));
    await symlink(path.join(vendor, 'bin', 'codex-code-mode-host'), path.join(vendor, 'bin', 'codex'));
    await chmod(path.join(vendor, 'bin', 'codex-code-mode-host'), 0o644);
    const failed = await verifyPackagedCodexTree({ resourcesRoot: root });
    expect(failed.status).toBe('FAIL');
    expect(failed.failures).toEqual(expect.arrayContaining([
      'packaged codex/bin/codex must be a regular non-symlink file',
      'packaged codex/bin/codex-code-mode-host is not executable'
    ]));
    expect((await verifyPackagedCodexTree({ resourcesRoot: 'relative' })).failures).toEqual(['Resources root must be a normalized absolute path']);
  });
});
