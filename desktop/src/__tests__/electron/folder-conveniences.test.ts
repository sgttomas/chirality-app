import { afterAll, beforeAll, expect, it, vi } from 'vitest';
import { mkdtemp, mkdir, writeFile, symlink, rm, realpath } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
const native = vi.hoisted(() => ({ recent: vi.fn() }));
vi.mock('electron', () => ({ app: { whenReady: () => new Promise(() => {}), on: vi.fn(), addRecentDocument: native.recent }, BrowserWindow: {}, dialog: {}, ipcMain: {}, shell: {}, Menu: {} }));
import { registerRecentFolder } from '../../../electron/main';
let base: string, root: string, instruction: string;
const beforeSignals = { SIGINT: process.listeners('SIGINT'), SIGTERM: process.listeners('SIGTERM') };
beforeAll(async () => { base = await mkdtemp(path.join(tmpdir(), 'chirality-folder-ipc-')); root = path.join(base, 'root'); instruction = path.join(base, 'instruction'); await mkdir(root); await mkdir(instruction); await writeFile(path.join(root, 'file.txt'), 'fixture'); await symlink(instruction, path.join(base, 'instruction-link')); });
afterAll(async () => { await rm(base, { recursive: true, force: true }); for (const signal of ['SIGINT', 'SIGTERM'] as const) for (const listener of process.listeners(signal)) if (!beforeSignals[signal].includes(listener)) process.removeListener(signal, listener); });
it('registers a canonical validated directory and rejects untrusted senders before filesystem effects', async () => {
  const origin = 'http://localhost:3000'; const event = { senderFrame: { url: `${origin}/chat` } }; const register = vi.fn();
  expect(await registerRecentFolder(event, root, origin, instruction, register)).toEqual({ ok: true }); expect(register).toHaveBeenCalledWith(await realpath(root));
  register.mockClear();
  for (const sender of [{}, { senderFrame: { url: 'https://example.invalid/' } }, { senderFrame: { url: 'file:///tmp/a' } }]) expect(await registerRecentFolder(sender, root, origin, instruction, register)).toMatchObject({ ok: false });
  expect(register).not.toHaveBeenCalled();
});
it('refuses regular files, missing directories, relative paths and instruction aliases without adding recents', async () => {
  const register = vi.fn(); const origin = 'http://localhost:3000'; const event = { senderFrame: { url: origin } };
  for (const invalid of [path.join(root, 'file.txt'), path.join(root, 'missing'), 'relative', instruction, path.join(base, 'instruction-link'), null, {}, '/bad\u0000path']) expect(await registerRecentFolder(event, invalid, origin, instruction, register)).toMatchObject({ ok: false });
  expect(register).not.toHaveBeenCalled();
  expect(await registerRecentFolder(event, root, origin, instruction, () => { throw new Error('Native refusal'); })).toEqual({ ok: false, error: 'Native refusal' });
  expect(native.recent).not.toHaveBeenCalled();
});
