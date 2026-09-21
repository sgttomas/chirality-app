import { beforeEach, describe, expect, it, vi } from 'vitest';
const mocks = vi.hoisted(() => ({ accessible: vi.fn(async (root: string) => root), reveal: vi.fn(async ({ projectRoot }: { projectRoot: string }) => projectRoot), list: vi.fn(async () => []), read: vi.fn(), register: vi.fn(), home: vi.fn(() => '/server/home'), realpath: vi.fn(async (root: string) => root) }));
vi.mock('../../../lib/harness/session-manager', () => ({ assertProjectRootAccessible: mocks.accessible }));
vi.mock('../../../lib/harness/instruction-root', () => ({ resolveInstructionRootPath: () => '/instructions' }));
vi.mock('node:os', () => ({ homedir: mocks.home }));
vi.mock('node:fs/promises', async importOriginal => ({ ...await importOriginal<object>(), realpath: mocks.realpath }));
vi.mock('../../../app/api/working-root/file/file-policy', async importOriginal => ({ ...await importOriginal<object>(), validateRevealRoot: mocks.reveal }));
vi.mock('../../../app/api/working-root/workflow-drafts/workflow-draft-store', async importOriginal => ({ ...await importOriginal<object>(), listDrafts: mocks.list, readWorkflowDraft: mocks.read, registerDraft: mocks.register }));
import { GET, POST } from '../../../app/api/working-root/workflow-drafts/route';
import { FilePolicyError } from '../../../app/api/working-root/file/file-policy';
const base = 'http://localhost:3000/api/working-root/workflow-drafts';
const input = { projectRoot: '/project', name: 'sample', source: 'user', reviewToken: 'a'.repeat(64) };
function post(body: unknown = input, origin = 'http://localhost:3000') { return new Request(base, { method: 'POST', headers: { origin, 'content-type': 'application/json' }, body: JSON.stringify(body) }); }
beforeEach(() => { vi.clearAllMocks(); });
describe('workflow draft route scope and mutation checks', () => {
  it('lists only an authorized project and server-resolved user home', async () => {
    expect((await GET(new Request(`${base}?projectRoot=/project`))).status).toBe(200);
    expect(mocks.accessible).toHaveBeenCalledWith('/project');
    expect(mocks.reveal).toHaveBeenCalledWith({ projectRoot: '/project' }, '/instructions');
    expect(mocks.list.mock.calls).toEqual([['/project', 'project'], ['/server/home', 'user']]);
  });
  it('does not accept renderer-provided user roots or bundled sources', async () => {
    expect((await GET(new Request(`${base}?projectRoot=/project&userRoot=/outside`))).status).toBe(400);
    expect((await POST(post({ ...input, source: 'bundled' }))).status).toBe(400);
    expect((await POST(post({ ...input, userRoot: '/outside' }))).status).toBe(400);
    expect(mocks.register).not.toHaveBeenCalled();
  });
  it('rejects cross-origin registration and missing origin', async () => {
    expect((await POST(post(input, 'https://hostile.example'))).status).toBe(403);
    expect((await POST(post(input, ''))).status).toBe(403);
    expect(mocks.register).not.toHaveBeenCalled();
  });
  it('matches the renderer Host when Next normalizes Request.url, while rejecting other hosts and ports', async () => {
    mocks.register.mockResolvedValue({ name: 'sample', source: 'user', path: '.chirality/workflows/sample/WORKFLOW.md' });
    const incoming = (origin: string, host: string, site = 'same-origin') => new Request(base, {
      method: 'POST', headers: { origin, host, 'sec-fetch-site': site, 'content-type': 'application/json' }, body: JSON.stringify(input)
    });
    expect((await POST(incoming('http://127.0.0.1:3000', '127.0.0.1:3000'))).status).toBe(200);
    expect((await POST(incoming('http://127.0.0.1:4000', '127.0.0.1:3000'))).status).toBe(403);
    expect((await POST(incoming('http://hostile.example:3000', 'hostile.example:3000'))).status).toBe(403);
    expect((await POST(incoming('http://127.0.0.1:3000', '127.0.0.1:3000', 'cross-site'))).status).toBe(403);
    expect(mocks.register).toHaveBeenCalledTimes(1);
  });
  it('uses the server home for registration and forwards a readable stale review error', async () => {
    mocks.register.mockRejectedValueOnce(new FilePolicyError('DRAFT_CHANGED', 409, 'Refresh and review it again.'));
    const response = await POST(post());
    expect(response.status).toBe(409);
    expect(await response.json()).toEqual({ error: { code: 'DRAFT_CHANGED', message: 'Refresh and review it again.' } });
    expect(mocks.register).toHaveBeenCalledWith('/server/home', 'sample', 'user', input.reviewToken);
  });
  it('rejects duplicate selectors and invalid inspection names', async () => {
    expect((await GET(new Request(`${base}?projectRoot=/project&projectRoot=/outside`))).status).toBe(400);
    expect((await GET(new Request(`${base}?projectRoot=/project&name=../bad&source=project`))).status).toBe(400);
    expect(mocks.read).not.toHaveBeenCalled();
  });
  it('surfaces malformed draft failures instead of reporting an empty successful list', async () => {
    mocks.list.mockRejectedValueOnce(new FilePolicyError('INVALID_DRAFT', 400, 'Draft metadata needs correction.'));
    const response = await GET(new Request(`${base}?projectRoot=/project`));
    expect(response.status).toBe(400);
    expect(await response.json()).toEqual({ error: { code: 'INVALID_DRAFT', message: 'Draft metadata needs correction.' } });
  });
});
