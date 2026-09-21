import { mkdtemp, mkdir, readdir, readFile, realpath, rm, symlink, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createProductInstructionsHandler, createProductInstructionsStore, resolveProductInstructionsDefault } from '../../../electron/product-instructions';

let directory: string;
let defaultInstructionsPath: string;
let userDataDirectory: string;
beforeEach(async () => {
  directory = await realpath(await mkdtemp(path.join(os.tmpdir(), 'chirality-product-instructions-')));
  defaultInstructionsPath = path.join(directory, 'bundled-AGENTS.md');
  userDataDirectory = path.join(directory, 'App');
  await writeFile(defaultInstructionsPath, '# Default instructions\n');
});
afterEach(async () => { await rm(directory, { recursive: true, force: true }); });
const store = () => createProductInstructionsStore({ userDataDirectory, defaultInstructionsPath });

describe('editable product instructions', () => {
  it.each(['development', 'source override', 'staged override', 'packaged'] as const)(
    'initializes and restores the product default in %s launches', async (launch) => {
      const repositoryRoot = path.join(directory, 'source');
      const frontendRoot = path.join(repositoryRoot, 'projects', 'chirality-app-dev', 'frontend');
      const productDirectory = path.join(frontendRoot, '..', 'instructions');
      const resourcesPath = path.join(directory, 'Resources');
      const stagedRoot = path.join(resourcesPath, 'instruction-root');
      await mkdir(productDirectory, { recursive: true });
      await mkdir(stagedRoot, { recursive: true });
      await writeFile(path.join(repositoryRoot, 'AGENTS.md'), '# Repository development rules\n');
      await writeFile(path.join(productDirectory, 'AGENTS.md'), '# Source product default\n');
      await writeFile(path.join(stagedRoot, 'AGENTS.md'), '# Packaged product default\n');
      const override = launch === 'source override' ? repositoryRoot
        : launch === 'staged override' ? stagedRoot : undefined;
      const value = createProductInstructionsStore({
        userDataDirectory,
        defaultInstructionsPath: resolveProductInstructionsDefault({
          packaged: launch === 'packaged', resourcesPath, frontendRoot,
          instructionRootOverride: override
        })
      });
      const expected = launch === 'development' || launch === 'source override'
        ? '# Source product default\n' : '# Packaged product default\n';
      await value.initialize();
      expect(await readFile(value.instructionsPath, 'utf8')).toBe(expected);
      await writeFile(value.instructionsPath, '# Custom\n');
      await value.restore();
      expect(await readFile(value.instructionsPath, 'utf8')).toBe(expected);
      expect(await readFile(path.join(repositoryRoot, 'AGENTS.md'), 'utf8')).toBe('# Repository development rules\n');
    }
  );

  it('seeds once and preserves customizations across a new bundled version', async () => {
    const first = store();
    expect(await first.initialize()).toEqual({ path: first.instructionsPath, modified: false });
    await writeFile(first.instructionsPath, '# My instructions\n');
    await writeFile(defaultInstructionsPath, '# Updated default\n');
    const second = store();
    expect((await second.initialize()).modified).toBe(true);
    expect(await readFile(second.instructionsPath, 'utf8')).toBe('# My instructions\n');
    expect(await readFile(defaultInstructionsPath, 'utf8')).toBe('# Updated default\n');
  });

  it('restores the current default while retaining the previous customization', async () => {
    const value = store();
    await value.initialize();
    await writeFile(value.instructionsPath, '# Custom\n');
    expect((await value.restore()).modified).toBe(false);
    const backup = (await readdir(path.dirname(value.instructionsPath))).find(name => name.startsWith('AGENTS.backup-'));
    expect(backup).toBeDefined();
    expect(await readFile(path.join(path.dirname(value.instructionsPath), backup!), 'utf8')).toBe('# Custom\n');
    expect(await readFile(value.instructionsPath, 'utf8')).toBe('# Default instructions\n');
  });

  it('refuses an aliased instructions directory without changing the external target', async () => {
    const outside = path.join(directory, 'other-client');
    await mkdir(outside);
    await writeFile(path.join(outside, 'AGENTS.md'), 'Other client guidance');
    await mkdir(userDataDirectory);
    await symlink(outside, path.join(userDataDirectory, 'instructions'));
    await expect(store().initialize()).rejects.toThrow('regular App-owned folder');
    expect(await readFile(path.join(outside, 'AGENTS.md'), 'utf8')).toBe('Other client guidance');
  });

  it('refuses a file alias and oversized instruction content', async () => {
    const value = store();
    await value.initialize();
    await rm(value.instructionsPath);
    await symlink(defaultInstructionsPath, value.instructionsPath);
    await expect(value.get()).rejects.toThrow();
    await expect(value.restore()).rejects.toThrow();
    await rm(value.instructionsPath);
    await writeFile(value.instructionsPath, Buffer.alloc(1024 * 1024 + 1));
    await expect(value.get()).rejects.toThrow('smaller than 1 MB');
  });

  it('validates IPC origin and operation, opens only the fixed file, and respects cancelled restoration', async () => {
    const value = store();
    await value.initialize();
    await writeFile(value.instructionsPath, '# Custom');
    const open = vi.fn(async () => '');
    const confirmRestore = vi.fn(async () => false);
    const handler = createProductInstructionsHandler({ authorized: event => event === 'allowed', store: value, open, confirmRestore });
    expect(await handler('denied', 'open')).toMatchObject({ ok: false });
    expect(await handler('allowed', { operation: 'open', path: '/elsewhere' })).toMatchObject({ ok: false });
    expect(open).not.toHaveBeenCalled();
    expect(await handler('allowed', 'open')).toMatchObject({ ok: true });
    expect(open).toHaveBeenCalledExactlyOnceWith(value.instructionsPath);
    expect(await handler('allowed', 'restore')).toMatchObject({ ok: true, cancelled: true });
    expect(await readFile(value.instructionsPath, 'utf8')).toBe('# Custom');
    confirmRestore.mockResolvedValueOnce(true);
    expect(await handler('allowed', 'restore')).toMatchObject({ ok: true, state: { modified: false } });
  });
});
