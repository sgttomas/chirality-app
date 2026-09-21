import { afterAll, beforeAll, expect, it, vi } from 'vitest';
import { mkdtemp, mkdir, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
vi.mock('electron', () => ({ app: { whenReady: () => new Promise(() => {}), on: vi.fn() }, BrowserWindow: {}, dialog: {}, ipcMain: {}, shell: {}, Menu: {} }));
import { createDirectorySelectionHandler } from '../../../electron/main';
let base: string, home: string, folder: string, preference: string;
const beforeSignals = { SIGINT: process.listeners('SIGINT'), SIGTERM: process.listeners('SIGTERM') };
beforeAll(async () => {
  base = await mkdtemp(path.join(tmpdir(), 'chirality-directory-selection-'));
  home = path.join(base, 'home'); folder = path.join(base, 'work'); preference = path.join(base, 'preferences', 'selected-directory.json');
  await mkdir(home); await mkdir(folder);
});
afterAll(async () => {
  await rm(base, { recursive: true, force: true });
  for (const signal of ['SIGINT', 'SIGTERM'] as const) for (const listener of process.listeners(signal)) if (!beforeSignals[signal].includes(listener)) process.removeListener(signal, listener);
});
it('starts at home, remembers explicit selection across handlers, and falls back if the folder disappears', async () => {
  const choose = vi.fn().mockResolvedValueOnce({ canceled: true, filePaths: [] })
    .mockResolvedValueOnce({ canceled: false, filePaths: [folder] }).mockResolvedValue({ canceled: true, filePaths: [] });
  const select = createDirectorySelectionHandler(preference, home, choose);
  expect(await select()).toEqual({ cancelled: true });
  expect(choose).toHaveBeenLastCalledWith(expect.objectContaining({ defaultPath: home }));
  expect(await select()).toEqual({ cancelled: false, path: folder });
  expect(choose).toHaveBeenLastCalledWith(expect.objectContaining({ defaultPath: home }));
  await select();
  expect(choose).toHaveBeenLastCalledWith(expect.objectContaining({ defaultPath: folder }));
  await createDirectorySelectionHandler(preference, home, choose)();
  expect(choose).toHaveBeenLastCalledWith(expect.objectContaining({ defaultPath: folder }));
  await rm(folder, { recursive: true });
  await createDirectorySelectionHandler(preference, home, choose)();
  expect(choose).toHaveBeenLastCalledWith(expect.objectContaining({ defaultPath: home }));
});
it('ignores malformed preferences and does not remember a rejected selection', async () => {
  await writeFile(preference, 'malformed');
  const file = path.join(base, 'file'); await writeFile(file, 'fixture');
  const choose = vi.fn().mockResolvedValueOnce({ canceled: false, filePaths: [file] }).mockResolvedValue({ canceled: true, filePaths: [] });
  const select = createDirectorySelectionHandler(preference, home, choose);
  expect(await select()).toEqual({ cancelled: true, error: 'Selected path is not a directory' });
  await select();
  expect(choose).toHaveBeenLastCalledWith(expect.objectContaining({ defaultPath: home }));
});
