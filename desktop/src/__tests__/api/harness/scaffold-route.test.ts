import { mkdtemp, mkdir, readFile, rm, stat, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it, vi } from 'vitest';

const DECOMPOSITION_FIXTURE = `# Example Execution Decomposition

## Packages (work-domain partitions)

| PackageID | Package Name | Description |
|---|---|---|
| PKG-05 | Filesystem Execution Model | scaffolding |

## Deliverables

### PKG-05 - Filesystem Execution Model

| DeliverableID | Name | Type |
|---|---|---|
| DEL-05-02 | Execution Root Scaffolding + Layout Conformance | BACKEND_FEATURE_SLICE |
`;

let tmpDir = '';

afterEach(async () => {
  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
});

describe('POST /api/harness/scaffold', () => {
  it('creates scaffolded execution-root content and returns summary payload', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-scaffold-route-'));
    const executionRoot = path.join(tmpDir, 'execution-root');
    const decompositionPath = path.join(tmpDir, 'decomposition.md');
    await writeFile(decompositionPath, DECOMPOSITION_FIXTURE, 'utf8');

    vi.resetModules();
    const [route, daemonPortModule, fakeDaemonPortModule] = await Promise.all([
      import('../../../app/api/harness/scaffold/route'),
      import('../../../lib/runtime-client/daemon-harness-port'),
      import('./fake-daemon-harness-port')
    ]);
    daemonPortModule.installDaemonHarnessPort(
      fakeDaemonPortModule.createFakeDaemonHarnessPort()
    );

    const response = await route.POST(
      new Request('http://localhost/api/harness/scaffold', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          executionRoot,
          decompositionPath,
          coordinationMode: 'SCHEDULE_FIRST'
        })
      })
    );

    expect(response.status).toBe(200);
    const body = (await response.json()) as {
      packageCount: number;
      deliverableCount: number;
      coordinationMode: string;
      layoutValidation: { valid: boolean };
      preparationCompatibility: { ready: boolean; deliverablesChecked: number };
    };

    expect(body.packageCount).toBe(1);
    expect(body.deliverableCount).toBe(1);
    expect(body.coordinationMode).toBe('SCHEDULE_FIRST');
    expect(body.layoutValidation.valid).toBe(true);
    expect(body.preparationCompatibility.ready).toBe(true);
    expect(body.preparationCompatibility.deliverablesChecked).toBe(1);

    await expect(stat(path.join(executionRoot, '_Coordination', '_COORDINATION.md'))).resolves.toBeDefined();
    await expect(
      stat(
        path.join(
          executionRoot,
          'PKG-05_Filesystem Execution Model',
          '1_Working',
          'DEL-05-02_Execution Root Scaffolding + Layout Conformance'
        )
      )
    ).resolves.toBeDefined();

    const coordination = await readFile(path.join(executionRoot, '_Coordination', '_COORDINATION.md'), 'utf8');
    expect(coordination).toContain('**Representation:** SCHEDULE_FIRST');
  });

  it('returns INVALID_REQUEST when required fields are missing', async () => {
    vi.resetModules();
    const [route, daemonPortModule, fakeDaemonPortModule] = await Promise.all([
      import('../../../app/api/harness/scaffold/route'),
      import('../../../lib/runtime-client/daemon-harness-port'),
      import('./fake-daemon-harness-port')
    ]);
    daemonPortModule.installDaemonHarnessPort(
      fakeDaemonPortModule.createFakeDaemonHarnessPort()
    );

    const response = await route.POST(
      new Request('http://localhost/api/harness/scaffold', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          executionRoot: '/tmp/example'
        })
      })
    );

    expect(response.status).toBe(400);
    expect(await response.json()).toMatchObject({
      error: {
        type: 'INVALID_REQUEST'
      }
    });
  });

  it('returns fail-fast diagnostics when filesystem conflicts prevent scaffolding', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-scaffold-route-fail-fast-'));
    const executionRoot = path.join(tmpDir, 'execution-root');
    const decompositionPath = path.join(tmpDir, 'decomposition.md');
    await mkdir(executionRoot, { recursive: true });
    await writeFile(path.join(executionRoot, '_Coordination'), 'not-a-directory', 'utf8');
    await writeFile(decompositionPath, DECOMPOSITION_FIXTURE, 'utf8');

    vi.resetModules();
    const [route, daemonPortModule, fakeDaemonPortModule] = await Promise.all([
      import('../../../app/api/harness/scaffold/route'),
      import('../../../lib/runtime-client/daemon-harness-port'),
      import('./fake-daemon-harness-port')
    ]);
    daemonPortModule.installDaemonHarnessPort(
      fakeDaemonPortModule.createFakeDaemonHarnessPort()
    );

    const response = await route.POST(
      new Request('http://localhost/api/harness/scaffold', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          executionRoot,
          decompositionPath
        })
      })
    );

    expect(response.status).toBe(409);
    expect(await response.json()).toMatchObject({
      error: {
        type: 'WORKING_ROOT_INACCESSIBLE',
        details: {
          scaffoldStrategy: 'FAIL_FAST',
          stage: 'ensure_tool_root',
          targetPath: path.join(executionRoot, '_Coordination')
        }
      }
    });
  });
});
