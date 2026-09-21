import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

type RouteModule = typeof import('../../../app/api/project/deliverables/route');

type RouteBody = {
  projectRoot?: string;
  deliverables?: Array<{
    id: string;
    name: string;
    pkg: string;
    status: string;
    path: string;
  }>;
  deliverableContracts?: Array<{
    deliverableId: string;
    path: string;
    valid: boolean;
    documentFormat: string;
    selectedProductionDocuments: Array<{ fileName: string }>;
    errorCount: number;
    warningCount: number;
    findings: Array<{
      category: string;
      condition: string;
      path: string;
      severity: string;
    }>;
  }>;
  knowledgeDecomposition?: {
    enabled: boolean;
    markerFile: string | null;
  };
  knowledgeTypes?: Array<{
    id: string;
    label: string;
    matchingDeliverableKeys: string[];
  }>;
  error?: {
    type?: string;
    message?: string;
  };
};

let tmpRoot = '';
let projectRoot = '';

function statusDocument(state: string): string {
  return `# Status — Example

**Current State:** ${state}
**Last Updated:** 2026-02-24

## History
- 2026-02-24 - State set to ${state} (WORKING_ITEMS)
`;
}

function scopeOfWorkDocument(): string {
  return `---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-07-03
package_id: PKG-07
decomposition_basis: execution/_Decomposition/example.md@abc1234
project_scope_refs: [SOW-026]
package_objective_refs: [OBJ-006]
---

# Scope of Work

## Purpose and Objective Traceability

- **OUT-001** — Produce the declared contract.

## Deliverable Definition — Ontology

## Completion and Reliance Basis — Epistemology

- **AC-001** — Human review confirms completeness.

## Production and Verification Method — Praxeology

- **VER-001** — Perform the human review.

## Governing Values and Decisions — Axiology

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | SOW-026 OBJ-006 | OUT-001 | AC-001 | VER-001 | Review record |
`;
}

async function createDeliverable(
  pkgFolder: string,
  deliverableFolder: string,
  state: string,
  files: string[]
): Promise<string> {
  const deliverablePath = path.join(projectRoot, pkgFolder, '1_Working', deliverableFolder);
  await mkdir(deliverablePath, { recursive: true });
  await writeFile(path.join(deliverablePath, '_STATUS.md'), statusDocument(state), 'utf8');

  for (const fileName of files) {
    await writeFile(path.join(deliverablePath, fileName), `${fileName} content`, 'utf8');
  }

  return deliverablePath;
}

async function importRouteModule(): Promise<RouteModule> {
  vi.resetModules();
  return import('../../../app/api/project/deliverables/route');
}

async function requestDeliverables(rootPath: string): Promise<{ status: number; body: RouteBody }> {
  const route = await importRouteModule();
  const response = await route.GET(
    new Request(
      `http://localhost/api/project/deliverables?projectRoot=${encodeURIComponent(rootPath)}`
    )
  );

  return {
    status: response.status,
    body: (await response.json()) as RouteBody
  };
}

beforeEach(async () => {
  tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-project-deliverables-route-'));
  projectRoot = path.join(tmpRoot, 'project-root');
  await mkdir(projectRoot, { recursive: true });
});

afterEach(async () => {
  await rm(tmpRoot, { recursive: true, force: true });
  tmpRoot = '';
  projectRoot = '';
});

describe('GET /api/project/deliverables', () => {
  it('returns deliverables, knowledge marker metadata, and knowledge type mappings', async () => {
    const deliverablePath = await createDeliverable(
      'PKG-02_Desktop_UI_Workflow',
      'DEL-02-02_Portal_Pipeline_Navigation',
      'IN_PROGRESS',
      ['Datasheet.md', 'Specification.md', 'MEMORY.md']
    );

    const decompositionPath = path.join(projectRoot, '_Decomposition');
    await mkdir(decompositionPath, { recursive: true });
    await writeFile(
      path.join(decompositionPath, 'Domain_Handbook.md'),
      '# Knowledge Types\n\nKnowledge Categories and Knowledge Types are defined here.',
      'utf8'
    );

    const response = await requestDeliverables(projectRoot);

    expect(response.status).toBe(200);
    expect(response.body.projectRoot).toBe(projectRoot);
    expect(response.body.deliverables).toEqual([
      {
        id: 'DEL-02-02',
        name: 'Portal Pipeline Navigation',
        pkg: 'PKG-02_Desktop_UI_Workflow',
        status: 'in_progress',
        path: deliverablePath
      }
    ]);
    expect(response.body.knowledgeDecomposition).toEqual({
      enabled: true,
      markerFile: path.join(projectRoot, '_Decomposition', 'Domain_Handbook.md')
    });
    expect(response.body.knowledgeTypes).toEqual(
      expect.arrayContaining([
        {
          id: 'datasheet',
          label: 'Datasheet',
          matchingDeliverableKeys: ['PKG-02_Desktop_UI_Workflow::DEL-02-02']
        },
        {
          id: 'specification',
          label: 'Specification',
          matchingDeliverableKeys: ['PKG-02_Desktop_UI_Workflow::DEL-02-02']
        },
        {
          id: 'memory',
          label: 'Memory',
          matchingDeliverableKeys: ['PKG-02_Desktop_UI_Workflow::DEL-02-02']
        }
      ])
    );
  });

  it('returns marker disabled when no decomposition marker is present', async () => {
    await createDeliverable(
      'PKG-06_Agent_Suite_Governance',
      'DEL-06-03_Cross_Deliverable_Workflows',
      'SEMANTIC_READY',
      ['Guidance.md']
    );

    const decompositionPath = path.join(projectRoot, '_Decomposition');
    await mkdir(decompositionPath, { recursive: true });
    await writeFile(
      path.join(decompositionPath, 'ChiralityApp_SoftwareDecomposition.md'),
      '# Software Decomposition\n\nNo domain marker text.',
      'utf8'
    );

    const response = await requestDeliverables(projectRoot);
    expect(response.status).toBe(200);
    expect(response.body.knowledgeDecomposition).toEqual({
      enabled: false,
      markerFile: null
    });
  });

  it('returns additive deliverable contract findings for incomplete document kits', async () => {
    const deliverablePath = await createDeliverable(
      'PKG-07_Filesystem_Execution_Lifecycle_and_Dependencies',
      'DEL-07-03_Deliverable_Metadata_and_Document_Kit_Contracts',
      'INITIALIZED',
      ['_DEPENDENCIES.md', '_REFERENCES.md', 'Datasheet.md', 'MEMORY.md', '_MEMORY.md']
    );
    await writeFile(
      path.join(deliverablePath, '_REFERENCES.md'),
      [
        '# References',
        '',
        '| RefID | Path | ExpectedSHA256 | ActualSHA256 | Status |',
        '|---|---|---|---|---|',
        '| REF-006 | `docs/PRD.md` | `expected` | `actual` | HASH_MISMATCH |'
      ].join('\n'),
      'utf8'
    );

    const noStatusPath = path.join(
      projectRoot,
      'PKG-07_Filesystem_Execution_Lifecycle_and_Dependencies',
      '1_Working',
      'DEL-07-99_No_Status'
    );
    await mkdir(noStatusPath, { recursive: true });

    const invalidFolderPath = path.join(
      projectRoot,
      'PKG-07_Filesystem_Execution_Lifecycle_and_Dependencies',
      '1_Working',
      'D07-03_Invalid_Folder'
    );
    await mkdir(invalidFolderPath, { recursive: true });
    await writeFile(path.join(invalidFolderPath, '_STATUS.md'), statusDocument('INITIALIZED'), 'utf8');

    const response = await requestDeliverables(projectRoot);

    expect(response.status).toBe(200);
    expect(response.body.deliverables?.map((deliverable) => deliverable.id)).toEqual(['DEL-07-03']);

    const contract = response.body.deliverableContracts?.[0];
    expect(contract).toMatchObject({
      deliverableId: 'DEL-07-03',
      path: deliverablePath,
      valid: false,
      errorCount: 3
    });
    expect(contract?.findings).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          category: 'required_metadata',
          condition: 'missing_required_metadata',
          path: path.join(deliverablePath, '_CONTEXT.md'),
          severity: 'error'
        }),
        expect.objectContaining({
          category: 'preparation_baseline',
          condition: 'missing_preparation_baseline',
          path: path.join(deliverablePath, '_SEMANTIC.md'),
          severity: 'warning'
        }),
        expect.objectContaining({
          category: 'document_kit',
          condition: 'missing_document_kit_file',
          path: path.join(deliverablePath, 'Specification.md'),
          severity: 'warning'
        }),
        expect.objectContaining({
          category: 'prohibited_file',
          condition: 'prohibited_memory_file',
          path: path.join(deliverablePath, '_MEMORY.md'),
          severity: 'error'
        }),
        expect.objectContaining({
          category: 'source_hash_warning',
          condition: 'reference_hash_warning',
          path: path.join(deliverablePath, '_REFERENCES.md'),
          severity: 'warning'
        })
      ])
    );
  });

  it('never infers an authorized migration from a normal project route scan', async () => {
    const deliverablePath = await createDeliverable(
      'PKG-07_Filesystem_Execution_Lifecycle_and_Dependencies',
      'DEL-07-03_Deliverable_Metadata_and_Document_Kit_Contracts',
      'IN_PROGRESS',
      [
        '_CONTEXT.md',
        '_DEPENDENCIES.md',
        '_REFERENCES.md',
        '_SEMANTIC.md',
        'Datasheet.md',
        'Specification.md',
        'Guidance.md',
        'Procedure.md',
        'ScopeOfWork.md',
        'MEMORY.md'
      ]
    );
    await writeFile(path.join(deliverablePath, 'ScopeOfWork.md'), scopeOfWorkDocument(), 'utf8');

    const response = await requestDeliverables(projectRoot);
    const contract = response.body.deliverableContracts?.[0];

    expect(response.status).toBe(200);
    expect(contract).toMatchObject({
      documentFormat: 'AMBIGUOUS',
      valid: false,
      selectedProductionDocuments: []
    });
    expect(contract?.findings).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ condition: 'ambiguous_deliverable_format', severity: 'error' })
      ])
    );
  });

  it('returns typed accessibility failures for missing project roots', async () => {
    const response = await requestDeliverables(path.join(projectRoot, 'missing-root'));
    expect(response.status).toBe(404);
    expect(response.body).toMatchObject({
      error: {
        type: 'WORKING_ROOT_INACCESSIBLE'
      }
    });
  });
});
