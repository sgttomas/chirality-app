import { mkdtemp, mkdir, readFile, rm, stat, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import { parseStatusDocument } from '../../lib/lifecycle/status-parser';
import { previewScaffoldExecutionRoot, scaffoldExecutionRoot } from '../../lib/harness/scaffold';

const DECOMPOSITION_FIXTURE = `# Example System - Software Decomposition

## Packages (work-domain partitions)

| PackageID | Package Name | Description |
|---|---|---|
| PKG-01 | Build & Packaging | Build outputs |
| PKG-02 | UI : Shell | UI workflow |

## Deliverables

### PKG-01 - Build & Packaging

| DeliverableID | Name | Type |
|---|---|---|
| DEL-01-01 | DMG Build: Baseline | CI_CD_CHANGE |
| DEL-01-02 | Bundle / Integrity | CI_CD_CHANGE |

### PKG-02 - UI : Shell

| DeliverableID | Name | Type |
|---|---|---|
| DEL-02-01 | Portal   Layout | UX_UI_SLICE |
`;

let tmpDir = '';

afterEach(async () => {
  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
});

describe('scaffoldExecutionRoot', () => {
  it('previews execution-root scaffold paths without writing files', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-scaffold-preview-'));
    const executionRoot = path.join(tmpDir, 'execution');
    const decompositionPath = path.join(tmpDir, 'decomposition.md');
    await writeFile(decompositionPath, DECOMPOSITION_FIXTURE, 'utf8');

    const result = await previewScaffoldExecutionRoot({
      executionRoot,
      decompositionPath,
      coordinationMode: 'HYBRID'
    });

    expect(result.projectName).toBe('Example System');
    expect(result.packageCount).toBe(2);
    expect(result.deliverableCount).toBe(3);
    expect(result.planned.directories).toContain(
      path.join(executionRoot, 'PKG-01_Build & Packaging', '1_Working')
    );
    expect(result.planned.files).toContain(path.join(executionRoot, 'INIT.md'));
    expect(result.planned.files).toContain(
      path.join(
        executionRoot,
        'PKG-01_Build & Packaging',
        '1_Working',
        'DEL-01-01_DMG Build- Baseline',
        '_STATUS.md'
      )
    );
    await expect(stat(executionRoot)).rejects.toMatchObject({ code: 'ENOENT' });
  });

  it('creates execution-root layout, package folders, and deliverable folders from decomposition', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-scaffold-test-'));
    const executionRoot = path.join(tmpDir, 'execution');
    const decompositionPath = path.join(tmpDir, 'decomposition.md');
    await writeFile(decompositionPath, DECOMPOSITION_FIXTURE, 'utf8');

    const result = await scaffoldExecutionRoot({
      executionRoot,
      decompositionPath,
      coordinationMode: 'HYBRID'
    });

    expect(result.projectName).toBe('Example System');
    expect(result.packageCount).toBe(2);
    expect(result.deliverableCount).toBe(3);
    expect(result.layoutValidation.valid).toBe(true);
    expect(result.layoutValidation.executionRoot.valid).toBe(true);
    expect(result.preparationCompatibility.ready).toBe(true);
    expect(result.preparationCompatibility.deliverablesChecked).toBe(3);
    expect(result.preparationCompatibility.issueCount).toBe(0);

    await expect(stat(path.join(executionRoot, '_Aggregation', '_Templates'))).resolves.toBeDefined();
    await expect(stat(path.join(executionRoot, '_Decomposition', path.basename(decompositionPath)))).resolves.toBeDefined();
    await expect(stat(path.join(executionRoot, '_Coordination', '_COORDINATION.md'))).resolves.toBeDefined();

    await expect(
      stat(path.join(executionRoot, 'PKG-01_Build & Packaging', '1_Working', 'DEL-01-01_DMG Build- Baseline'))
    ).resolves.toBeDefined();
    await expect(
      stat(path.join(executionRoot, 'PKG-01_Build & Packaging', '1_Working', 'DEL-01-02_Bundle - Integrity'))
    ).resolves.toBeDefined();
    await expect(
      stat(path.join(executionRoot, 'PKG-02_UI - Shell', '1_Working', 'DEL-02-01_Portal Layout'))
    ).resolves.toBeDefined();

    const deliverablePath = path.join(
      executionRoot,
      'PKG-01_Build & Packaging',
      '1_Working',
      'DEL-01-01_DMG Build- Baseline'
    );
    for (const metadataFile of [
      '_STATUS.md',
      '_CONTEXT.md',
      '_DEPENDENCIES.md',
      '_REFERENCES.md',
      '_SEMANTIC.md'
    ]) {
      await expect(stat(path.join(deliverablePath, metadataFile))).resolves.toBeDefined();
    }

    const status = parseStatusDocument(await readFile(path.join(deliverablePath, '_STATUS.md'), 'utf8'));
    expect(status.currentState).toBe('OPEN');
    expect(status.history[0]).toMatchObject({ state: 'OPEN', actor: 'PREPARATION' });
    await expect(readFile(path.join(deliverablePath, '_CONTEXT.md'), 'utf8')).resolves.toContain(
      '| ResponsibleParty | TBD |'
    );

    const coordination = await readFile(path.join(executionRoot, '_Coordination', '_COORDINATION.md'), 'utf8');
    expect(coordination).toContain('**Representation:** HYBRID');
  });

  it('is idempotent and does not overwrite existing files on rerun', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-scaffold-idempotent-'));
    const executionRoot = path.join(tmpDir, 'execution');
    const decompositionPath = path.join(tmpDir, 'decomposition.md');
    await writeFile(decompositionPath, DECOMPOSITION_FIXTURE, 'utf8');

    await scaffoldExecutionRoot({
      executionRoot,
      decompositionPath
    });

    const initPath = path.join(executionRoot, 'INIT.md');
    const customFile = path.join(
      executionRoot,
      'PKG-01_Build & Packaging',
      '1_Working',
      'DEL-01-01_DMG Build- Baseline',
      'custom.txt'
    );
    const statusPath = path.join(
      executionRoot,
      'PKG-01_Build & Packaging',
      '1_Working',
      'DEL-01-01_DMG Build- Baseline',
      '_STATUS.md'
    );

    await writeFile(initPath, '# custom-init\n', 'utf8');
    await writeFile(customFile, 'custom-content\n', 'utf8');
    await writeFile(
      statusPath,
      `# Status: custom

**Current State:** INITIALIZED
**Last Updated:** 2026-01-01

## History

- 2026-01-01 - State set to INITIALIZED (PREPARATION) [custom]
`,
      'utf8'
    );

    const rerun = await scaffoldExecutionRoot({
      executionRoot,
      decompositionPath
    });

    expect(rerun.created.files).toHaveLength(0);
    expect(rerun.created.directories).toHaveLength(0);

    const initContent = await readFile(initPath, 'utf8');
    const customContent = await readFile(customFile, 'utf8');
    const statusContent = await readFile(statusPath, 'utf8');
    expect(initContent).toBe('# custom-init\n');
    expect(customContent).toBe('custom-content\n');
    expect(statusContent).toContain('**Current State:** INITIALIZED');
    expect(rerun.layoutValidation.valid).toBe(true);
    expect(rerun.preparationCompatibility.ready).toBe(true);
  });

  it('reseeds missing PREPARATION metadata files on rerun', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-scaffold-reseed-'));
    const executionRoot = path.join(tmpDir, 'execution');
    const decompositionPath = path.join(tmpDir, 'decomposition.md');
    await writeFile(decompositionPath, DECOMPOSITION_FIXTURE, 'utf8');

    await scaffoldExecutionRoot({
      executionRoot,
      decompositionPath
    });

    const referencesPath = path.join(
      executionRoot,
      'PKG-01_Build & Packaging',
      '1_Working',
      'DEL-01-01_DMG Build- Baseline',
      '_REFERENCES.md'
    );
    await rm(referencesPath);

    const rerun = await scaffoldExecutionRoot({
      executionRoot,
      decompositionPath
    });

    expect(rerun.created.files).toContain(referencesPath);
    expect(rerun.preparationCompatibility.ready).toBe(true);
    await expect(readFile(referencesPath, 'utf8')).resolves.toContain(
      'TBD pending governed reference discovery.'
    );
  });

  it('rejects malformed decomposition input without deliverable rows', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-scaffold-malformed-'));
    const executionRoot = path.join(tmpDir, 'execution');
    const decompositionPath = path.join(tmpDir, 'bad-decomposition.md');
    await writeFile(
      decompositionPath,
      `# Bad Decomposition

| PackageID | Package Name |
|---|---|
| PKG-01 | Build |
`,
      'utf8'
    );

    await expect(
      scaffoldExecutionRoot({
        executionRoot,
        decompositionPath
      })
    ).rejects.toMatchObject({
      type: 'INVALID_REQUEST'
    });
  });

  it('reports PREPARATION compatibility issues when metadata file targets are invalid', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-scaffold-prep-compat-'));
    const executionRoot = path.join(tmpDir, 'execution');
    const decompositionPath = path.join(tmpDir, 'decomposition.md');
    await writeFile(decompositionPath, DECOMPOSITION_FIXTURE, 'utf8');

    await scaffoldExecutionRoot({
      executionRoot,
      decompositionPath
    });

    const deliverablePath = path.join(
      executionRoot,
      'PKG-01_Build & Packaging',
      '1_Working',
      'DEL-01-01_DMG Build- Baseline'
    );
    await rm(path.join(deliverablePath, '_SEMANTIC.md'));
    await mkdir(path.join(deliverablePath, '_SEMANTIC.md'), { recursive: true });

    const rerun = await scaffoldExecutionRoot({
      executionRoot,
      decompositionPath
    });

    expect(rerun.preparationCompatibility.ready).toBe(false);
    expect(rerun.preparationCompatibility.issueCount).toBeGreaterThan(0);
    expect(
      rerun.preparationCompatibility.deliverables.find((item) => item.id === 'DEL-01-01')?.issues[0]
    ).toContain('_SEMANTIC.md');
  });

  it('fails fast with retry diagnostics when scaffolding hits a conflicting filesystem path', async () => {
    tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-scaffold-fail-fast-'));
    const executionRoot = path.join(tmpDir, 'execution');
    const decompositionPath = path.join(tmpDir, 'decomposition.md');
    await writeFile(decompositionPath, DECOMPOSITION_FIXTURE, 'utf8');
    await mkdir(executionRoot, { recursive: true });
    await writeFile(path.join(executionRoot, '_Coordination'), 'not-a-directory', 'utf8');

    await expect(
      scaffoldExecutionRoot({
        executionRoot,
        decompositionPath
      })
    ).rejects.toMatchObject({
      type: 'WORKING_ROOT_INACCESSIBLE',
      status: 409,
      details: expect.objectContaining({
        scaffoldStrategy: 'FAIL_FAST',
        stage: 'ensure_tool_root',
        targetPath: path.join(executionRoot, '_Coordination'),
        guidance: expect.stringContaining('rerun')
      })
    });
  });
});
