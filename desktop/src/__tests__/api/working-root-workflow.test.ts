import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { mkdir, mkdtemp, writeFile, symlink, rm, rename, open } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { createHash } from 'node:crypto';
const state = vi.hoisted(() => ({ instruction: '', swap: undefined as undefined | (() => Promise<void>) }));
vi.mock('../../lib/harness/session-manager', () => ({ assertProjectRootAccessible: async (root: string) => root }));
vi.mock('../../lib/harness/instruction-root', () => ({ resolveInstructionRootPath: () => state.instruction }));
vi.mock('node:fs/promises', async importOriginal => {
  const actual = await importOriginal<typeof import('node:fs/promises')>();
  return { ...actual, opendir: async (...args: Parameters<typeof actual.opendir>) => {
    if (state.swap) { const callback = state.swap; state.swap = undefined; await callback(); }
    return actual.opendir(...args);
  } };
});
import { GET } from '../../app/api/working-root/workflow/route';
import * as route from '../../app/api/working-root/workflow/route';
import { TEXT_LIMIT } from '../../app/api/working-root/file/file-policy';
let base: string, root: string, workflows: string;
beforeEach(async () => {
  base = await mkdtemp(path.join(os.tmpdir(), 'chirality-workflow-test-'));
  // macOS /var and /tmp aliases must be canonical before API comparisons.
  const { realpath } = await import('node:fs/promises'); base = await realpath(base);
  root = path.join(base, 'root'); state.instruction = path.join(base, 'instruction'); workflows = path.join(root, '.chirality/workflows');
  await mkdir(root); await mkdir(state.instruction);
});
afterEach(async () => { state.swap = undefined; await rm(base, { recursive: true, force: true }); });
const get = (name?: string, selectedRoot = root) => GET(new Request(`http://localhost/api/working-root/workflow?projectRoot=${encodeURIComponent(selectedRoot)}${name === undefined ? '' : `&name=${encodeURIComponent(name)}`}`));
async function fixture(content = '# Design review\n\n1. Gather sources\n2. [gate] Review findings\n') { await mkdir(workflows, { recursive: true }); await writeFile(path.join(workflows, 'plan.md'), content); return content; }
describe('contained workflow GET', () => {
  it('is GET only and a missing workflow directory stays empty without creating it', async () => {
    expect(Object.keys(route).sort()).toEqual(['GET', 'runtime']);
    const response = await get(); expect(response.status).toBe(200); expect(await response.json()).toEqual({ projectRoot: root, files: [], directoryMissing: true });
  });
  it('lists actual file metadata and opens exact bytes with hash and no inferred workflow state', async () => {
    const content = await fixture(); const list = await (await get()).json();
    expect(list.files).toEqual([expect.objectContaining({ name: 'plan.md', path: '.chirality/workflows/plan.md', size: Buffer.byteLength(content) })]);
    const response = await get('plan.md'); expect(response.headers.get('cache-control')).toBe('no-store');
    expect(await response.json()).toEqual({ projectRoot: root, file: list.files[0], content, sha256: createHash('sha256').update(content).digest('hex') });
  });
  it.each(['../secret.md', '/secret.md', 'x/y.md', 'x\\y.md', '', 'x.txt', 'x\u0000.md'])('rejects non-basename target %s', async name => { await fixture(); expect((await get(name)).status).toBe(400); });
  it('rejects duplicate and unknown parameters', async () => {
    for (const tail of ['&name=a.md&name=b.md', '&target=a.md', '&projectRoot=other']) expect((await GET(new Request(`http://localhost/?projectRoot=${encodeURIComponent(root)}${tail}`))).status).toBe(400);
  });
  it('rejects instruction roots, aliases, missing roots and regular-file roots', async () => {
    expect((await get(undefined, state.instruction)).status).toBe(409);
    const alias = path.join(base, 'alias'); await symlink(state.instruction, alias); expect((await get(undefined, alias)).status).toBe(409);
    expect((await get(undefined, path.join(base, 'missing'))).status).toBe(404);
    await writeFile(path.join(base, 'file'), 'x'); expect((await get(undefined, path.join(base, 'file'))).status).toBe(404);
  });
  it.each(['.chirality', 'workflows', 'file'])('rejects symlink at %s, including in-root targets outside workflows', async kind => {
    await fixture(); await mkdir(path.join(root, 'other')); await writeFile(path.join(root, 'other', 'secret.md'), 'secret');
    if (kind === '.chirality') { await rm(path.join(root, '.chirality'), { recursive: true }); await symlink(path.join(root, 'other'), path.join(root, '.chirality')); }
    if (kind === 'workflows') { await rm(workflows, { recursive: true }); await symlink(path.join(root, 'other'), workflows); }
    if (kind === 'file') await symlink(path.join(root, 'other', 'secret.md'), path.join(workflows, 'escape.md'));
    expect((await get()).status).toBeGreaterThanOrEqual(400);
    if (kind === 'file') expect((await get('escape.md')).status).toBe(403);
  });
  it('never exposes foreign enumerated filenames during a directory swap', async () => {
    await fixture(); const outside = path.join(base, 'foreign'); await mkdir(outside); await writeFile(path.join(outside, 'private-customer-name.md'), 'secret');
    state.swap = async () => { await rename(workflows, `${workflows}-old`); await symlink(outside, workflows); };
    const response = await get(); const text = await response.text(); expect(response.status).toBe(409); expect(text).not.toContain('private-customer'); expect(text).not.toContain('secret'); expect(text).not.toContain(outside);
  });
  it('does not silently truncate an oversized directory scan', async () => {
    await fixture(); await Promise.all(Array.from({ length: 500 }, (_, i) => writeFile(path.join(workflows, `${i}.txt`), '')));
    const response = await get(); expect(response.status).toBe(413); expect(await response.text()).toContain('500');
  });
  it('reports invalid text and limits without reading oversized content', async () => {
    await fixture(); await writeFile(path.join(workflows, 'binary.md'), Buffer.from([0, 255])); expect((await get('binary.md')).status).toBe(415);
    await writeFile(path.join(workflows, 'bad.md'), Buffer.from([255])); expect((await get('bad.md')).status).toBe(415);
    const handle = await open(path.join(workflows, 'large.md'), 'w'); await handle.truncate(TEXT_LIMIT + 1); await handle.close(); expect((await get('large.md')).status).toBe(413);
    await mkdir(path.join(workflows, 'directory.md')); expect((await get('directory.md')).status).toBe(403);
  });
});
