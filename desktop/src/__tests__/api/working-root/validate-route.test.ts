import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

type Fixture = {
  tmpRoot: string;
  projectRoot: string;
  instructionRoot: string;
};

let fixture: Fixture;

async function postValidate(projectRoot: unknown): Promise<Response> {
  vi.resetModules();
  const route = await import('../../../app/api/working-root/validate/route');
  return route.POST(
    new Request('http://localhost/api/working-root/validate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ projectRoot })
    })
  );
}

beforeEach(async () => {
  const tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-working-root-validate-'));
  const projectRoot = path.join(tmpRoot, 'project-root');
  const instructionRoot = path.join(tmpRoot, 'instruction-root');
  await mkdir(projectRoot, { recursive: true });
  await mkdir(path.join(instructionRoot, 'execution'), { recursive: true });
  await writeFile(path.join(projectRoot, 'README.md'), '# project fixture\n', 'utf8');
  process.env.CHIRALITY_INSTRUCTION_ROOT = instructionRoot;
  fixture = { tmpRoot, projectRoot, instructionRoot };
});

afterEach(async () => {
  delete process.env.CHIRALITY_INSTRUCTION_ROOT;
  vi.restoreAllMocks();
  await rm(fixture.tmpRoot, { recursive: true, force: true });
});

describe('working-root validation route', () => {
  it('accepts the same readable and writable project root used by session creation', async () => {
    const response = await postValidate(fixture.projectRoot);

    expect(response.status).toBe(200);
    expect(await response.json()).toEqual({ ok: true, projectRoot: fixture.projectRoot });
  });

  it('rejects a project root inside the instruction root', async () => {
    const response = await postValidate(path.join(fixture.instructionRoot, 'execution'));

    expect(response.status).toBe(409);
    expect(await response.json()).toMatchObject({
      error: { type: 'WORKING_ROOT_CONFLICT' }
    });
  });

  it('rejects a missing project root with the session-creation error contract', async () => {
    const response = await postValidate(path.join(fixture.tmpRoot, 'missing'));

    expect(response.status).toBe(404);
    expect(await response.json()).toMatchObject({
      error: { type: 'WORKING_ROOT_INACCESSIBLE' }
    });
  });

  it('rejects relative project-root input', async () => {
    const response = await postValidate('relative/project');

    expect(response.status).toBe(400);
    expect(await response.json()).toMatchObject({
      error: { type: 'INVALID_REQUEST' }
    });
  });
});
