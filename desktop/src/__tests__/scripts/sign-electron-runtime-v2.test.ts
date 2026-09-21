import { mkdtemp, realpath, rm } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it, vi } from 'vitest';

import customMacSign, {
  CODEX_JIT_BINARY,
  createCustomMacSign,
  CODEX_SIGNED_BINARIES,
  CODE_MODE_HOST_ENTITLEMENTS,
  DEFAULT_ENTITLEMENTS,
  DEFAULT_INHERIT_ENTITLEMENTS,
  createSignOptions,
  verifySignedBundle
} from '../../../scripts/sign-electron-runtime-v2.mjs';

const cleanup: string[] = [];
afterEach(async () => {
  await Promise.all(cleanup.splice(0).map((entry) => rm(entry, { recursive: true, force: true })));
});

describe('App and stock Codex signing policy', () => {
  it('grants the hardened runtime everywhere and JIT only to the Code Mode host', () => {
    const appPath = '/tmp/candidate/Chirality.app';
    const inherited = vi.fn((filePath: string) => ({ marker: filePath }));
    const options = createSignOptions({ app: appPath, identity: 'X', optionsForFile: inherited }, { appPath });
    expect(options.app).toBe(appPath);
    expect(options.optionsForFile(appPath)).toEqual({ marker: appPath, hardenedRuntime: true, entitlements: DEFAULT_ENTITLEMENTS });
    expect(options.optionsForFile(path.join(appPath, CODEX_JIT_BINARY))).toEqual({
      marker: path.join(appPath, CODEX_JIT_BINARY),
      hardenedRuntime: true,
      entitlements: CODE_MODE_HOST_ENTITLEMENTS
    });
    expect(options.optionsForFile(path.join(appPath, 'Contents/Resources/codex/bin/codex'))).toEqual({
      marker: path.join(appPath, 'Contents/Resources/codex/bin/codex'),
      hardenedRuntime: true,
      entitlements: DEFAULT_INHERIT_ENTITLEMENTS
    });
    expect(options.optionsForFile(path.join(appPath, 'Contents/Frameworks/Chirality Helper.app'))).toMatchObject({ entitlements: DEFAULT_ENTITLEMENTS });
    expect(options.optionsForFile(path.join(appPath, 'Contents/Resources/codex/codex-path/rg'))).toMatchObject({ entitlements: DEFAULT_INHERIT_ENTITLEMENTS });
    expect([...CODEX_SIGNED_BINARIES]).toEqual(['Contents/Resources/codex/bin/codex', 'Contents/Resources/codex/bin/codex-code-mode-host']);
  });

  it('signs once through osx-sign and then verifies the bundle and both Codex binaries', async () => {
    const root = await realpath(await mkdtemp(path.join(os.tmpdir(), 'chirality-sign-')));
    cleanup.push(root);
    const sign = vi.fn(async (_options: unknown) => undefined);
    const verify = vi.fn(async (appPath: string) => ({ appPath, binaries: [] }));
    const result = await createCustomMacSign({ sign, verify })({ app: root, identity: 'X', optionsForFile: () => ({ entitlements: '/e.plist' }) });
    expect(sign).toHaveBeenCalledTimes(1);
    const passed = sign.mock.calls[0][0] as { optionsForFile: (filePath: string) => { entitlements: string } };
    expect(passed.optionsForFile(root).entitlements).toBe('/e.plist');
    expect(verify).toHaveBeenCalledWith(root);
    expect(result).toEqual({ appPath: root, binaries: [] });
  });

  it('ignores the packager electron-builder passes as the second argument', async () => {
    const root = await realpath(await mkdtemp(path.join(os.tmpdir(), 'chirality-sign-')));
    cleanup.push(root);
    const sign = vi.fn(async (_options: unknown) => undefined);
    const verify = vi.fn(async (appPath: string) => ({ appPath, binaries: [] }));
    const packager = { sign: vi.fn(async () => { throw new Error('packager.sign must not be used'); }) };
    const hook = createCustomMacSign({ sign, verify }) as unknown as (options: unknown, packager: unknown) => Promise<unknown>;
    await expect(hook({ app: root, identity: 'X' }, packager)).resolves.toEqual({ appPath: root, binaries: [] });
    expect(packager.sign).not.toHaveBeenCalled();
    expect(typeof customMacSign).toBe('function');
  });

  it('fails verification when a Codex binary lacks the hardened runtime flag', async () => {
    const execFile = vi.fn(async (_command: string, args: string[]) => {
      if (args[0] === '-d') return { stdout: '', stderr: 'Identifier=codex\nCodeDirectory v=20500 size=1 flags=0x0(none) hashes=1+1 location=embedded\n' };
      return { stdout: '', stderr: '' };
    });
    await expect(verifySignedBundle('/tmp/Chirality.app', { execFile: execFile as never })).rejects.toThrow(/not signed with the hardened runtime: Contents\/Resources\/codex\/bin\/codex/);
  });

  it('reports both binaries when the strict checks pass', async () => {
    const calls: string[][] = [];
    const execFile = vi.fn(async (_command: string, args: string[]) => {
      calls.push(args);
      if (args[0] === '-d') return { stdout: '', stderr: 'flags=0x10000(runtime)\n' };
      return { stdout: '', stderr: '' };
    });
    await expect(verifySignedBundle('/tmp/Chirality.app', { execFile: execFile as never })).resolves.toEqual({
      appPath: '/tmp/Chirality.app',
      binaries: [
        { relativePath: 'Contents/Resources/codex/bin/codex', hardenedRuntime: true },
        { relativePath: 'Contents/Resources/codex/bin/codex-code-mode-host', hardenedRuntime: true }
      ]
    });
    expect(calls.at(-1)).toEqual(['--verify', '--deep', '--strict', '--verbose=2', '/tmp/Chirality.app']);
  });
});
