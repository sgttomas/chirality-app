import { parseCsv } from './csv-utils';
import {
  DEPENDENCY_CORE_COLUMNS,
  DependencyRegisterRow,
  normalizeDependencyType,
  normalizeDirection,
  normalizeSchemaVersion
} from './schema';

export interface DependencyRegisterReadResult {
  headers: string[];
  rows: DependencyRegisterRow[];
  warnings: string[];
}

function toRecord(headers: string[], values: string[]): Record<string, string> {
  const record: Record<string, string> = {};
  headers.forEach((header, index) => {
    record[header] = values[index] ?? '';
  });
  return record;
}

function normalizeRow(
  row: Record<string, string>,
  hasSchemaVersionColumn: boolean,
  warnings: string[],
  rowIndex: number
): DependencyRegisterRow {
  const normalizedRow: DependencyRegisterRow = {
    RegisterSchemaVersion: normalizeSchemaVersion(row.RegisterSchemaVersion),
    DependencyID: row.DependencyID ?? '',
    FromPackageID: row.FromPackageID ?? '',
    FromDeliverableID: row.FromDeliverableID ?? '',
    FromDeliverableName: row.FromDeliverableName ?? '',
    DependencyClass: (row.DependencyClass ?? '').trim().toUpperCase(),
    AnchorType: (row.AnchorType ?? '').trim().toUpperCase(),
    Direction: (row.Direction ?? '').trim().toUpperCase(),
    DependencyType: (row.DependencyType ?? '').trim().toUpperCase(),
    TargetType: (row.TargetType ?? '').trim().toUpperCase(),
    TargetPackageID: row.TargetPackageID ?? '',
    TargetDeliverableID: row.TargetDeliverableID ?? '',
    TargetRefID: row.TargetRefID ?? '',
    TargetName: row.TargetName ?? '',
    TargetLocation: row.TargetLocation ?? '',
    Statement: row.Statement ?? '',
    EvidenceFile: row.EvidenceFile ?? '',
    SourceRef: row.SourceRef ?? '',
    EvidenceQuote: row.EvidenceQuote ?? '',
    Explicitness: (row.Explicitness ?? '').trim().toUpperCase(),
    RequiredMaturity: row.RequiredMaturity ?? '',
    ProposedMaturity: row.ProposedMaturity ?? '',
    SatisfactionStatus: (row.SatisfactionStatus ?? '').trim().toUpperCase(),
    Confidence: (row.Confidence ?? '').trim().toUpperCase(),
    Origin: (row.Origin ?? '').trim().toUpperCase(),
    FirstSeen: row.FirstSeen ?? '',
    LastSeen: row.LastSeen ?? '',
    Status: (row.Status ?? '').trim().toUpperCase(),
    Notes: row.Notes ?? ''
  };

  normalizedRow.Direction = normalizeDirection(normalizedRow.Direction);
  normalizedRow.DependencyType = normalizeDependencyType(normalizedRow.DependencyType);

  if (!hasSchemaVersionColumn) {
    warnings.push(`ROW_${rowIndex}:SCHEMA_VERSION_INFERRED`);
  }

  if (normalizedRow.Direction !== (row.Direction ?? '').trim().toUpperCase()) {
    warnings.push(`ROW_${rowIndex}:DIRECTION_NORMALIZED`);
  }

  if (normalizedRow.DependencyType !== (row.DependencyType ?? '').trim().toUpperCase()) {
    warnings.push(`ROW_${rowIndex}:DEPENDENCY_TYPE_NORMALIZED`);
  }

  for (const [key, value] of Object.entries(row)) {
    if (!(key in normalizedRow)) {
      normalizedRow[key] = value ?? '';
    }
  }

  return normalizedRow;
}

export function readDependencyRegister(csvContent: string): DependencyRegisterReadResult {
  const parsedRows = parseCsv(csvContent);
  if (parsedRows.length === 0) {
    return {
      headers: [...DEPENDENCY_CORE_COLUMNS],
      rows: [],
      warnings: []
    };
  }

  const warnings: string[] = [];
  const rawHeaders = parsedRows[0].map((header) => header.trim());
  const hasSchemaVersionColumn = rawHeaders.includes('RegisterSchemaVersion');
  const headers = hasSchemaVersionColumn
    ? rawHeaders
    : ['RegisterSchemaVersion', ...rawHeaders];

  if (!hasSchemaVersionColumn) {
    warnings.push('MISSING_SCHEMA_VERSION_COLUMN');
  }

  const rows: DependencyRegisterRow[] = [];

  for (let rowIndex = 1; rowIndex < parsedRows.length; rowIndex += 1) {
    const rowValues = parsedRows[rowIndex];
    const values = hasSchemaVersionColumn ? rowValues : ['', ...rowValues];
    const rawRow = toRecord(headers, values);
    const normalized = normalizeRow(rawRow, hasSchemaVersionColumn, warnings, rowIndex);
    rows.push(normalized);
  }

  return {
    headers,
    rows,
    warnings
  };
}
