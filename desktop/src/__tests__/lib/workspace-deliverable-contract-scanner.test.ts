import { mkdtemp, mkdir, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { scanDeliverableDocumentKitContract } from '../../lib/workspace/filesystem';

let tmpRoot = '';
let deliverablePath = '';
const ACCEPTED_MIGRATION_AUTHORITY =
  'D-GOV-16@7584718aa32b112e415331736d1a8e68c12ac176';

function statusDocument(state = 'IN_PROGRESS'): string {
  return `# Status: DEL-07-03 Deliverable Contract Scanner

**Current State:** ${state}
**Last Updated:** 2026-06-21

## History
- 2026-06-21 - State set to ${state} (WORKING_ITEMS)
`;
}

function scopeOfWorkDocument(migrationAuthority = ''): string {
  return `---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-07-03
package_id: PKG-07
decomposition_basis: execution/_Decomposition/example.md@abc1234
project_scope_refs: [SOW-026]
package_objective_refs: [OBJ-006]
---

# Scope of Work

${migrationAuthority ? `<!-- migration-authority: ${migrationAuthority} -->\n` : ''}

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

async function writeDeliverableFiles(files: Record<string, string>): Promise<void> {
  for (const [fileName, content] of Object.entries(files)) {
    await writeFile(path.join(deliverablePath, fileName), content, 'utf8');
  }
}

beforeEach(async () => {
  tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-deliverable-contract-scanner-'));
  deliverablePath = path.join(
    tmpRoot,
    'PKG-07_Filesystem_Execution_Lifecycle_and_Dependencies',
    '1_Working',
    'DEL-07-03_Deliverable_Metadata_and_Document_Kit_Contracts'
  );
  await mkdir(deliverablePath, { recursive: true });
});

afterEach(async () => {
  await rm(tmpRoot, { recursive: true, force: true });
  tmpRoot = '';
  deliverablePath = '';
});

describe('scanDeliverableDocumentKitContract', () => {
  it('accepts Scope-of-Work-only as SOW_V1 and selects the canonical document', async () => {
    await writeDeliverableFiles({
      '_STATUS.md': statusDocument('IN_PROGRESS'),
      '_CONTEXT.md': '# Context\n',
      '_DEPENDENCIES.md': '# Dependencies\n',
      '_REFERENCES.md': '# References\n',
      '_SEMANTIC.md': '# Semantic\n',
      'ScopeOfWork.md': scopeOfWorkDocument(),
      'MEMORY.md': '# Memory\n'
    });

    const result = await scanDeliverableDocumentKitContract({
      deliverableId: 'DEL-07-03',
      deliverablePath
    });
    expect(result.documentFormat).toBe('SOW_V1');
    expect(result.valid).toBe(true);
    expect(result.scopeOfWork.present).toBe(true);
    expect(result.selectedProductionDocuments.map((file) => file.fileName)).toEqual([
      'ScopeOfWork.md'
    ]);
    expect(result.findings).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ condition: 'scope_of_work_activated', severity: 'info' })
      ])
    );
  });

  it('fails ordinary dual-format ambiguity and accepts only exact authorized isolated migration dual', async () => {
    await writeDeliverableFiles({
      '_STATUS.md': statusDocument('IN_PROGRESS'),
      '_CONTEXT.md': '# Context\n',
      '_DEPENDENCIES.md': '# Dependencies\n',
      '_REFERENCES.md': '# References\n',
      '_SEMANTIC.md': '# Semantic\n',
      'Datasheet.md': '# Datasheet\n',
      'Specification.md': '# Specification\n',
      'Guidance.md': '# Guidance\n',
      'Procedure.md': '# Procedure\n',
      'ScopeOfWork.md': scopeOfWorkDocument(ACCEPTED_MIGRATION_AUTHORITY),
      'MEMORY.md': '# Memory\n'
    });

    const normal = await scanDeliverableDocumentKitContract({
      deliverableId: 'DEL-07-03',
      deliverablePath
    });
    expect(normal.documentFormat).toBe('AMBIGUOUS');
    expect(normal.valid).toBe(false);

    const migration = await scanDeliverableDocumentKitContract({
      deliverableId: 'DEL-07-03',
      deliverablePath,
      scopeOfWorkMigration: {
        mode: 'MIGRATION_DUAL',
        isolatedWorkspace: true,
        authorityRef: ACCEPTED_MIGRATION_AUTHORITY,
        allowedDeliverablePaths: [deliverablePath]
      }
    });
    expect(migration.documentFormat).toBe('MIGRATION_DUAL');
    expect(migration.valid).toBe(true);
    expect(migration.selectedProductionDocuments.map((file) => file.fileName)).toEqual([
      'ScopeOfWork.md'
    ]);
    expect(migration.findings).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ condition: 'migration_dual_authorized', severity: 'info' })
      ])
    );
  });

  it.each([
    ['unruled valid-looking authority', 'D-GOV-16@0123456', true, true],
    ['malformed authority', 'D-GOV-16@not-a-sha', true, true],
    ['missing authority', '', true, true],
    ['non-isolated mode', ACCEPTED_MIGRATION_AUTHORITY, false, true],
    ['wrong deliverable path', ACCEPTED_MIGRATION_AUTHORITY, true, false]
  ])('fails closed for %s', async (_caseName, authorityRef, isolatedWorkspace, useExactPath) => {
    await writeDeliverableFiles({
      '_STATUS.md': statusDocument('IN_PROGRESS'),
      '_CONTEXT.md': '# Context\n',
      '_DEPENDENCIES.md': '# Dependencies\n',
      '_REFERENCES.md': '# References\n',
      '_SEMANTIC.md': '# Semantic\n',
      'Datasheet.md': '# Datasheet\n',
      'Specification.md': '# Specification\n',
      'Guidance.md': '# Guidance\n',
      'Procedure.md': '# Procedure\n',
      'ScopeOfWork.md': scopeOfWorkDocument(authorityRef),
      'MEMORY.md': '# Memory\n'
    });

    const result = await scanDeliverableDocumentKitContract({
      deliverableId: 'DEL-07-03',
      deliverablePath,
      scopeOfWorkMigration: {
        mode: 'MIGRATION_DUAL',
        isolatedWorkspace: isolatedWorkspace as true,
        authorityRef,
        allowedDeliverablePaths: [
          useExactPath ? deliverablePath : path.join(tmpRoot, 'different-deliverable')
        ]
      }
    });

    expect(result.documentFormat).toBe('AMBIGUOUS');
    expect(result.valid).toBe(false);
    expect(result.selectedProductionDocuments).toEqual([]);
    expect(result.findings).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ condition: 'ambiguous_deliverable_format', severity: 'error' })
      ])
    );
  });

  it('fails closed instead of trimming a whitespace-padded accepted authority', async () => {
    await writeDeliverableFiles({
      '_STATUS.md': statusDocument('IN_PROGRESS'),
      '_CONTEXT.md': '# Context\n',
      '_DEPENDENCIES.md': '# Dependencies\n',
      '_REFERENCES.md': '# References\n',
      '_SEMANTIC.md': '# Semantic\n',
      'Datasheet.md': '# Datasheet\n',
      'Specification.md': '# Specification\n',
      'Guidance.md': '# Guidance\n',
      'Procedure.md': '# Procedure\n',
      'ScopeOfWork.md': scopeOfWorkDocument(ACCEPTED_MIGRATION_AUTHORITY),
      'MEMORY.md': '# Memory\n'
    });

    const result = await scanDeliverableDocumentKitContract({
      deliverableId: 'DEL-07-03',
      deliverablePath,
      scopeOfWorkMigration: {
        mode: 'MIGRATION_DUAL',
        isolatedWorkspace: true,
        authorityRef: ` ${ACCEPTED_MIGRATION_AUTHORITY} `,
        allowedDeliverablePaths: [deliverablePath]
      }
    });

    expect(result.documentFormat).toBe('AMBIGUOUS');
    expect(result.valid).toBe(false);
    expect(result.selectedProductionDocuments).toEqual([]);
  });

  it('refuses partial legacy coexistence and migration authority for a different path', async () => {
    await writeDeliverableFiles({
      '_STATUS.md': statusDocument('IN_PROGRESS'),
      '_CONTEXT.md': '# Context\n',
      '_DEPENDENCIES.md': '# Dependencies\n',
      '_REFERENCES.md': '# References\n',
      '_SEMANTIC.md': '# Semantic\n',
      'Datasheet.md': '# Datasheet\n',
      'ScopeOfWork.md': scopeOfWorkDocument(),
      'MEMORY.md': '# Memory\n'
    });

    const partial = await scanDeliverableDocumentKitContract({
      deliverableId: 'DEL-07-03',
      deliverablePath,
      scopeOfWorkMigration: {
        mode: 'MIGRATION_DUAL',
        isolatedWorkspace: true,
        authorityRef: ACCEPTED_MIGRATION_AUTHORITY,
        allowedDeliverablePaths: [path.join(tmpRoot, 'different-deliverable')]
      }
    });
    expect(partial.documentFormat).toBe('INVALID');
    expect(partial.valid).toBe(false);
  });

  it('rejects a structurally incomplete Scope of Work even with exact migration authority', async () => {
    await writeDeliverableFiles({
      '_STATUS.md': statusDocument('IN_PROGRESS'),
      '_CONTEXT.md': '# Context\n',
      '_DEPENDENCIES.md': '# Dependencies\n',
      '_REFERENCES.md': '# References\n',
      '_SEMANTIC.md': '# Semantic\n',
      'Datasheet.md': '# Datasheet\n',
      'Specification.md': '# Specification\n',
      'Guidance.md': '# Guidance\n',
      'Procedure.md': '# Procedure\n',
      'ScopeOfWork.md': scopeOfWorkDocument().replace('- **VER-001** — Perform the human review.\n', ''),
      'MEMORY.md': '# Memory\n'
    });

    const result = await scanDeliverableDocumentKitContract({
      deliverableId: 'DEL-07-03',
      deliverablePath,
      scopeOfWorkMigration: {
        mode: 'MIGRATION_DUAL',
        isolatedWorkspace: true,
        authorityRef: ACCEPTED_MIGRATION_AUTHORITY,
        allowedDeliverablePaths: [deliverablePath]
      }
    });
    expect(result.valid).toBe(false);
    expect(result.findings).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ condition: 'invalid_scope_of_work_candidate', severity: 'error' })
      ])
    );
  });

  it('fails closed for mismatched authority binding and a misleading requested format', async () => {
    await writeDeliverableFiles({
      '_STATUS.md': statusDocument('IN_PROGRESS'),
      '_CONTEXT.md': '# Context\n',
      '_DEPENDENCIES.md': '# Dependencies\n',
      '_REFERENCES.md': '# References\n',
      '_SEMANTIC.md': '# Semantic\n',
      'Datasheet.md': '# Datasheet\n',
      'Specification.md': '# Specification\n',
      'Guidance.md': '# Guidance\n',
      'Procedure.md': '# Procedure\n',
      'ScopeOfWork.md': scopeOfWorkDocument('D-GOV-16@0123456'),
      'MEMORY.md': '# Memory\n'
    });

    const result = await scanDeliverableDocumentKitContract({
      deliverableId: 'DEL-07-03',
      deliverablePath,
      requestedFormat: 'SOW_V1',
      scopeOfWorkMigration: {
        mode: 'MIGRATION_DUAL',
        isolatedWorkspace: true,
        authorityRef: ACCEPTED_MIGRATION_AUTHORITY,
        allowedDeliverablePaths: [deliverablePath]
      }
    });

    expect(result.documentFormat).toBe('AMBIGUOUS');
    expect(result.valid).toBe(false);
    expect(result.selectedProductionDocuments).toEqual([]);
    expect(result.findings).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ condition: 'ambiguous_deliverable_format', severity: 'error' }),
        expect.objectContaining({ condition: 'requested_format_mismatch', severity: 'error' })
      ])
    );
  });

  it('fails closed when an initialized deliverable has no production contract', async () => {
    await writeDeliverableFiles({
      '_STATUS.md': statusDocument('INITIALIZED'),
      '_CONTEXT.md': '# Context\n',
      '_DEPENDENCIES.md': '# Dependencies\n',
      '_REFERENCES.md': '# References\n',
      '_SEMANTIC.md': '# Semantic\n',
      'MEMORY.md': '# Memory\n'
    });

    const result = await scanDeliverableDocumentKitContract({
      deliverableId: 'DEL-07-03',
      deliverablePath
    });

    expect(result.documentFormat).toBe('INVALID');
    expect(result.valid).toBe(false);
    expect(result.selectedProductionDocuments).toEqual([]);
    expect(result.findings).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ condition: 'missing_production_contract', severity: 'error' })
      ])
    );
  });

  it('never reports INVALID as valid when an OPEN deliverable has no production contract', async () => {
    await writeDeliverableFiles({
      '_STATUS.md': statusDocument('OPEN'),
      '_CONTEXT.md': '# Context\n',
      '_DEPENDENCIES.md': '# Dependencies\n',
      '_REFERENCES.md': '# References\n',
      '_SEMANTIC.md': '# Semantic\n',
      'MEMORY.md': '# Memory\n'
    });

    const result = await scanDeliverableDocumentKitContract({
      deliverableId: 'DEL-07-03',
      deliverablePath
    });

    expect(result.documentFormat).toBe('INVALID');
    expect(result.errorCount).toBe(0);
    expect(result.valid).toBe(false);
    expect(result.selectedProductionDocuments).toEqual([]);
  });

  it('accepts complete metadata, document-kit, and canonical-memory files', async () => {
    await writeDeliverableFiles({
      '_STATUS.md': statusDocument('IN_PROGRESS'),
      '_CONTEXT.md': '# Context\n',
      '_DEPENDENCIES.md': '# Dependencies\n',
      '_REFERENCES.md': '# References\n\n| RefID | Status |\n|---|---|\n| REF-001 | MATCH |\n',
      '_SEMANTIC.md': '# Semantic\n',
      'Datasheet.md': '# Datasheet\n',
      'Specification.md': '# Specification\n',
      'Guidance.md': '# Guidance\n',
      'Procedure.md': '# Procedure\n',
      'MEMORY.md': '# Memory\n'
    });

    const result = await scanDeliverableDocumentKitContract({
      deliverableId: 'DEL-07-03',
      deliverablePath
    });

    expect(result.valid).toBe(true);
    expect(result.lifecycleState).toBe('IN_PROGRESS');
    expect(result.errorCount).toBe(0);
    expect(result.warningCount).toBe(0);
    expect(result.requiredMetadata.every((file) => file.present)).toBe(true);
    expect(result.preparationBaseline.every((file) => file.present)).toBe(true);
    expect(result.documentKit.every((file) => file.present)).toBe(true);
    expect(result.documentFormat).toBe('LEGACY_FOUR_DOC');
    expect(result.selectedProductionDocuments.map((file) => file.fileName)).toEqual([
      'Datasheet.md',
      'Specification.md',
      'Guidance.md',
      'Procedure.md'
    ]);
    expect(result.canonicalMemory.present).toBe(true);
    expect(result.optionalFiles.every((file) => !file.present)).toBe(true);
    expect(result.findings).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          category: 'canonical_memory',
          condition: 'canonical_memory_present',
          severity: 'info'
        })
      ])
    );
  });

  it('reports missing metadata, missing kit files, prohibited memory, and source-state warnings', async () => {
    await writeDeliverableFiles({
      '_STATUS.md': statusDocument('INITIALIZED'),
      '_DEPENDENCIES.md': '# Dependencies\n',
      '_REFERENCES.md': [
        '# References',
        '',
        '| RefID | Path | ExpectedSHA256 | ActualSHA256 | Status |',
        '|---|---|---|---|---|',
        '| REF-006 | `docs/PRD.md` | `expected` | `actual` | HASH_MISMATCH |',
        '| REF-099 | `docs/UNKNOWN.md` | `expected` | `actual` | UNKNOWN |'
      ].join('\n'),
      'Datasheet.md': '# Datasheet\n',
      'Specification.md': '# Specification\n',
      'MEMORY.md': '# Memory\n',
      '_MEMORY.md': '# Disabled memory\n',
      'HASH_VERIFICATION_BYPASS.jsonl': '{"ref":"REF-006"}\n'
    });

    const result = await scanDeliverableDocumentKitContract({
      deliverableId: 'DEL-07-03',
      deliverablePath
    });
    const conditions = result.findings.map((finding) => finding.condition);

    expect(result.valid).toBe(false);
    expect(result.errorCount).toBe(3);
    expect(conditions).toEqual(
      expect.arrayContaining([
        'missing_required_metadata',
        'missing_preparation_baseline',
        'missing_document_kit_file',
        'prohibited_memory_file',
        'reference_hash_warning',
        'reference_unknown_condition',
        'hash_verification_bypass_present',
        'canonical_memory_present'
      ])
    );
    expect(result.findings).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          path: path.join(deliverablePath, '_CONTEXT.md'),
          category: 'required_metadata',
          severity: 'error'
        }),
        expect.objectContaining({
          path: path.join(deliverablePath, '_MEMORY.md'),
          category: 'prohibited_file',
          severity: 'error'
        }),
        expect.objectContaining({
          path: path.join(deliverablePath, '_REFERENCES.md'),
          category: 'source_hash_warning',
          severity: 'warning'
        }),
        expect.objectContaining({
          path: path.join(deliverablePath, '_REFERENCES.md'),
          category: 'unknown_unsupported_condition',
          severity: 'warning'
        })
      ])
    );
  });
});
