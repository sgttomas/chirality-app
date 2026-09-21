import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { mkdir, mkdtemp, writeFile, symlink, rm } from 'node:fs/promises';
import path from 'node:path';
import { createDocumentHandoffHandler } from '../../app/api/working-root/file/file-policy';
import { isAuthorizedSender, type IpcSenderEvent } from '../../../electron/ipc-sender-policy';
let base: string, root: string, instruction: string;
beforeEach(async () => {
  const dir = path.resolve('../execution/_Coordination/AgentRuns/APP_LOOP_SHELL_2026-09-05/iteration-04/instances/pkg02_t3/author/fixtures');
  await mkdir(dir, { recursive: true }); base = await mkdtemp(path.join(dir, 'ipc-')); root = path.join(base, 'root'); instruction = path.join(base, 'instruction');
  await Promise.all([mkdir(root), mkdir(instruction)]); await writeFile(path.join(root, 'report.docx'), 'office');
});
afterEach(async () => { await rm(base, { recursive: true, force: true }); });
const event = { senderFrame: { url: 'http://localhost:3000/' } };
function setup() {
  const preview = vi.fn(), open = vi.fn(async () => ''), reveal = vi.fn();
  const handler = createDocumentHandoffHandler<IpcSenderEvent>({ authorized: sender => isAuthorizedSender(sender, 'http://localhost:3000'), instructionRoot: () => instruction, preview, open, reveal });
  return { handler, preview, open, reveal };
}
it('authorizes the actual handler with the existing sender policy and dispatches bounded native paths', async () => {
  const { handler, preview, open } = setup();
  const input = { projectRoot: root, target: 'report.docx', action: 'quick-look' };
  expect(await handler(event, input)).toEqual({ ok: true }); expect(preview).toHaveBeenCalledWith(event, path.join(root, 'report.docx'));
  expect(await handler(event, { ...input, action: 'open' })).toEqual({ ok: true }); expect(open).toHaveBeenCalledWith(path.join(root, 'report.docx'));
});
it('rejects invalid senders and runtime arguments without native effects', async () => {
  const { handler, preview, open } = setup();
  for (const sender of [{}, { senderFrame: { url: 'file:///tmp/a.html' } }, { senderFrame: { url: 'https://evil.example' } }]) expect(await handler(sender, {})).toMatchObject({ ok: false, error: { code: 'UNAUTHORIZED_SENDER' } });
  for (const input of [null, [], 'path', { projectRoot: root, target: '../x', action: 'open' }, { projectRoot: root, target: 'report.docx', action: 'shell' }]) expect(await handler(event, input)).toMatchObject({ ok: false });
  expect(preview).not.toHaveBeenCalled(); expect(open).not.toHaveBeenCalled();
});
it('independently refuses canonical escapes, instruction paths, directories and native errors', async () => {
  const { handler, open } = setup();
  await writeFile(path.join(base, 'outside'), 'outside'); await symlink(path.join(base, 'outside'), path.join(root, 'escape'));
  for (const target of ['escape', 'missing']) expect(await handler(event, { projectRoot: root, target, action: 'open' })).toMatchObject({ ok: false });
  await mkdir(path.join(root, 'folder')); expect(await handler(event, { projectRoot: root, target: 'folder', action: 'open' })).toMatchObject({ ok: false });
  expect(await handler(event, { projectRoot: instruction, target: 'a', action: 'open' })).toMatchObject({ ok: false });
  expect(open).not.toHaveBeenCalled(); open.mockResolvedValue('No application');
  expect(await handler(event, { projectRoot: root, target: 'report.docx', action: 'open' })).toMatchObject({ ok: false, error: { code: 'OPEN_FAILED', message: 'No application' } });
});
it('returns native thrown failures rather than claiming success', async () => {
  const { handler, preview, open } = setup();
  preview.mockImplementation(() => { throw new Error('Preview window missing'); });
  expect(await handler(event, { projectRoot: root, target: 'report.docx', action: 'quick-look' })).toMatchObject({ ok: false, error: { code: 'PREVIEW_FAILED', message: 'Preview window missing' } });
  open.mockRejectedValue(new Error('App launch failed'));
  expect(await handler(event, { projectRoot: root, target: 'report.docx', action: 'open' })).toMatchObject({ ok: false, error: { code: 'OPEN_FAILED', message: 'App launch failed' } });
});

it('reveals regular files and separately validated root directories', async () => {
  const { handler, reveal, open, preview } = setup();
  expect(await handler(event, { projectRoot: root, target: 'report.docx', action: 'reveal' })).toEqual({ ok: true });
  expect(reveal).toHaveBeenLastCalledWith(path.join(root, 'report.docx'));
  expect(await handler(event, { projectRoot: root, action: 'reveal-root' })).toEqual({ ok: true }); expect(reveal).toHaveBeenLastCalledWith(root);
  expect(open).not.toHaveBeenCalled(); expect(preview).not.toHaveBeenCalled();
});
it('does not weaken file-only actions for Reveal root and rejects malformed/protected roots', async () => {
  const { handler, reveal } = setup(); await mkdir(path.join(root, 'folder'));
  await symlink(instruction, path.join(base, 'instruction-alias'));
  for (const input of [
    { projectRoot: root, target: 'folder', action: 'open' },
    { projectRoot: root, target: 'folder', action: 'reveal' },
    { projectRoot: root, target: '', action: 'reveal-root' },
    { projectRoot: root, target: undefined, action: 'reveal-root' },
    { projectRoot: path.join(root, 'report.docx'), action: 'reveal-root' },
    { projectRoot: path.join(base, 'instruction-alias'), action: 'reveal-root' },
    { projectRoot: 'relative', action: 'reveal-root' }
  ]) expect(await handler(event, input)).toMatchObject({ ok: false });
  expect(await handler({}, { projectRoot: root, action: 'reveal-root' })).toMatchObject({ ok: false, error: { code: 'UNAUTHORIZED_SENDER' } });
  expect(reveal).not.toHaveBeenCalled();
  reveal.mockImplementation(() => { throw new Error('Finder unavailable'); });
  expect(await handler(event, { projectRoot: root, action: 'reveal-root' })).toMatchObject({ ok: false, error: { code: 'REVEAL_FAILED', message: 'Finder unavailable' } });
});
