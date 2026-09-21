import { describe, expect, it } from 'vitest';
import { readDependencyRegister } from '../../lib/dependencies/register-reader';
import { serializeDependencyRegister } from '../../lib/dependencies/register-writer';
import {
  DEPENDENCY_CORE_COLUMNS,
  DependencyContractError,
  DependencyRegisterRow
} from '../../lib/dependencies/schema';

function makeRow(overrides: Partial<DependencyRegisterRow> = {}): DependencyRegisterRow {
  return {
    RegisterSchemaVersion: 'v3.1',
    DependencyID: 'DEP-05-03-001',
    FromPackageID: 'PKG-05',
    FromDeliverableID: 'DEL-05-03',
    FromDeliverableName: 'Lifecycle State Handling',
    DependencyClass: 'EXECUTION',
    AnchorType: 'NOT_APPLICABLE',
    Direction: 'UPSTREAM',
    DependencyType: 'PREREQUISITE',
    TargetType: 'DELIVERABLE',
    TargetPackageID: 'PKG-05',
    TargetDeliverableID: 'DEL-05-02',
    TargetRefID: '',
    TargetName: 'Execution Root Scaffolding',
    TargetLocation: '',
    Statement: 'Requires scaffolding baseline before lifecycle transitions',
    EvidenceFile: 'Specification.md',
    SourceRef:
      'execution/PKG-05_Filesystem_Execution_Model/1_Working/DEL-05-03_Lifecycle_State_Handling/Specification.md#REQ-01',
    EvidenceQuote: 'Ensure lifecycle is represented by _STATUS.md.',
    Explicitness: 'EXPLICIT',
    RequiredMaturity: 'IN_PROGRESS',
    ProposedMaturity: 'IN_PROGRESS',
    SatisfactionStatus: 'PENDING',
    Confidence: 'HIGH',
    Origin: 'EXTRACTED',
    FirstSeen: '2026-02-22',
    LastSeen: '2026-02-22',
    Status: 'ACTIVE',
    Notes: '',
    ...overrides
  };
}

function buildLegacyCsv(row: DependencyRegisterRow): string {
  const headers = DEPENDENCY_CORE_COLUMNS.filter(
    (column) => column !== 'RegisterSchemaVersion'
  );
  const values = headers.map((header) => row[header] ?? '');
  return `${headers.join(',')}\n${values.join(',')}\n`;
}

describe('dependency register reader/writer', () => {
  it('reads legacy csv and normalizes direction + schema version', () => {
    const csv = buildLegacyCsv(
      makeRow({
        Direction: 'INBOUND',
        DependencyType: 'COORDINATION'
      })
    );

    const result = readDependencyRegister(csv);
    expect(result.warnings).toContain('MISSING_SCHEMA_VERSION_COLUMN');
    expect(result.rows[0].RegisterSchemaVersion).toBe('v3.1');
    expect(result.rows[0].Direction).toBe('UPSTREAM');
    expect(result.rows[0].DependencyType).toBe('OTHER');
  });

  it('serializes rows with canonical core header ordering', () => {
    const result = serializeDependencyRegister([makeRow()], {
      hostDeliverableId: 'DEL-05-03'
    });

    const [headerLine] = result.csv.split('\n');
    expect(headerLine).toBe(DEPENDENCY_CORE_COLUMNS.join(','));
    expect(result.rows[0].RegisterSchemaVersion).toBe('v3.1');
  });

  it('rejects invalid ANCHOR classification', () => {
    expect(() =>
      serializeDependencyRegister([
        makeRow({
          DependencyClass: 'ANCHOR',
          AnchorType: 'NOT_APPLICABLE',
          DependencyType: 'OTHER'
        })
      ])
    ).toThrowError(
      expect.objectContaining({
        code: 'INVALID_CLASSIFICATION'
      }) satisfies Partial<DependencyContractError>
    );
  });

  it('rejects active rows without required provenance', () => {
    expect(() =>
      serializeDependencyRegister([
        makeRow({
          EvidenceFile: '',
          SourceRef: ''
        })
      ])
    ).toThrowError(
      expect.objectContaining({
        code: 'INVALID_PROVENANCE'
      }) satisfies Partial<DependencyContractError>
    );
  });

  it('enforces target resolution rules', () => {
    expect(() =>
      serializeDependencyRegister([
        makeRow({
          TargetType: 'DELIVERABLE',
          TargetDeliverableID: ''
        })
      ])
    ).toThrowError(
      expect.objectContaining({
        code: 'INVALID_TARGET'
      }) satisfies Partial<DependencyContractError>
    );

    expect(() =>
      serializeDependencyRegister([
        makeRow({
          TargetType: 'DOCUMENT',
          TargetDeliverableID: 'DEL-05-02'
        })
      ])
    ).toThrowError(
      expect.objectContaining({
        code: 'INVALID_TARGET'
      }) satisfies Partial<DependencyContractError>
    );
  });

  it('rejects duplicate dependency ids', () => {
    expect(() =>
      serializeDependencyRegister([makeRow(), makeRow()])
    ).toThrowError(
      expect.objectContaining({
        code: 'DUPLICATE_DEPENDENCY_ID'
      }) satisfies Partial<DependencyContractError>
    );
  });

  it('rejects silent deletion of a previous dependency row', () => {
    const retained = makeRow({ DependencyID: 'DEP-05-03-011' });
    const deleted = makeRow({ DependencyID: 'DEP-05-03-012' });

    expect(() =>
      serializeDependencyRegister([retained], {
        previousRows: [retained, deleted]
      })
    ).toThrowError(
      expect.objectContaining({
        code: 'MISSING_RETIRED_ROW',
        details: {
          missingDependencyIds: ['DEP-05-03-012']
        }
      }) satisfies Partial<DependencyContractError>
    );
  });

  it('accepts retained rows when a removed dependency is represented as RETIRED', () => {
    const retained = makeRow({ DependencyID: 'DEP-05-03-013' });
    const previousActive = makeRow({ DependencyID: 'DEP-05-03-014' });
    const retired = makeRow({
      DependencyID: 'DEP-05-03-014',
      SatisfactionStatus: 'NOT_APPLICABLE',
      Status: 'RETIRED'
    });

    const result = serializeDependencyRegister([retained, retired], {
      previousRows: [retained, previousActive]
    });

    expect(result.rows).toEqual([
      expect.objectContaining({
        DependencyID: 'DEP-05-03-013',
        Status: 'ACTIVE'
      }),
      expect.objectContaining({
        DependencyID: 'DEP-05-03-014',
        SatisfactionStatus: 'NOT_APPLICABLE',
        Status: 'RETIRED'
      })
    ]);
  });

  it('enforces satisfaction status transition rules against previous rows', () => {
    const previous = makeRow({
      DependencyID: 'DEP-05-03-009',
      SatisfactionStatus: 'PENDING'
    });

    const invalidNext = makeRow({
      DependencyID: 'DEP-05-03-009',
      SatisfactionStatus: 'SATISFIED'
    });

    expect(() =>
      serializeDependencyRegister([invalidNext], {
        previousRows: [previous]
      })
    ).toThrowError(
      expect.objectContaining({
        code: 'INVALID_SATISFACTION_TRANSITION'
      }) satisfies Partial<DependencyContractError>
    );
  });

  it('accepts valid satisfaction status progression', () => {
    const previous = makeRow({
      DependencyID: 'DEP-05-03-010',
      SatisfactionStatus: 'IN_PROGRESS'
    });

    const next = makeRow({
      DependencyID: 'DEP-05-03-010',
      SatisfactionStatus: 'SATISFIED'
    });

    const result = serializeDependencyRegister([next], {
      previousRows: [previous]
    });

    expect(result.rows[0].SatisfactionStatus).toBe('SATISFIED');
  });
});
