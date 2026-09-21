import { serializeCsv } from './csv-utils';
import {
  ANCHOR_TYPE_VALUES,
  CONFIDENCE_VALUES,
  DELIVERABLE_ID_PATTERN,
  DEPENDENCY_CLASS_VALUES,
  DEPENDENCY_CORE_COLUMNS,
  DEPENDENCY_EXTENSION_COLUMNS,
  DEPENDENCY_ID_PATTERN,
  DEPENDENCY_TYPE_VALUES,
  DIRECTION_VALUES,
  EXPLICITNESS_VALUES,
  ORIGIN_VALUES,
  ROW_STATUS_VALUES,
  SATISFACTION_STATUS_VALUES,
  TARGET_TYPE_VALUES,
  DependencyContractError,
  DependencyRegisterRow,
  isIsoDate,
  isKnownEnumValue,
  isValidSatisfactionTransition,
  normalizeDependencyType,
  normalizeDirection,
  normalizeEnum,
  normalizeSchemaVersion,
  quoteWordCount
} from './schema';

export interface DependencyRegisterWriteOptions {
  hostDeliverableId?: string;
  previousRows?: DependencyRegisterRow[];
}

export interface DependencyRegisterWriteResult {
  csv: string;
  rows: DependencyRegisterRow[];
  warnings: string[];
}

function requireNonEmpty(
  row: DependencyRegisterRow,
  field: keyof DependencyRegisterRow,
  code: DependencyContractError['code'],
  message: string
): void {
  if (!(row[field] ?? '').trim()) {
    throw new DependencyContractError(code, message, {
      field,
      dependencyId: row.DependencyID
    });
  }
}

function normalizeRow(row: DependencyRegisterRow, warnings: string[]): DependencyRegisterRow {
  const normalized: DependencyRegisterRow = { ...row };

  for (const column of DEPENDENCY_CORE_COLUMNS) {
    if (normalized[column] === undefined) {
      normalized[column] = '';
    }
  }

  normalized.RegisterSchemaVersion = normalizeSchemaVersion(normalized.RegisterSchemaVersion);
  normalized.DependencyClass = normalizeEnum(normalized.DependencyClass);
  normalized.AnchorType = normalizeEnum(normalized.AnchorType);

  const directionBefore = normalizeEnum(normalized.Direction);
  normalized.Direction = normalizeDirection(normalized.Direction);
  if (directionBefore !== normalized.Direction) {
    warnings.push(`ROW:${normalized.DependencyID}:DIRECTION_NORMALIZED`);
  }

  const dependencyTypeBefore = normalizeEnum(normalized.DependencyType);
  normalized.DependencyType = normalizeDependencyType(normalized.DependencyType);
  if (dependencyTypeBefore !== normalized.DependencyType) {
    warnings.push(`ROW:${normalized.DependencyID}:DEPENDENCY_TYPE_NORMALIZED`);
  }

  normalized.TargetType = normalizeEnum(normalized.TargetType);
  normalized.Explicitness = normalizeEnum(normalized.Explicitness);
  normalized.SatisfactionStatus = normalizeEnum(normalized.SatisfactionStatus);
  normalized.Confidence = normalizeEnum(normalized.Confidence);
  normalized.Origin = normalizeEnum(normalized.Origin);
  normalized.Status = normalizeEnum(normalized.Status);
  normalized.FirstSeen = (normalized.FirstSeen ?? '').trim();
  normalized.LastSeen = (normalized.LastSeen ?? '').trim();
  normalized.DependencyID = (normalized.DependencyID ?? '').trim();
  normalized.FromDeliverableID = (normalized.FromDeliverableID ?? '').trim();
  normalized.TargetDeliverableID = (normalized.TargetDeliverableID ?? '').trim();
  normalized.EvidenceFile = (normalized.EvidenceFile ?? '').trim();
  normalized.SourceRef = (normalized.SourceRef ?? '').trim();
  normalized.EvidenceQuote = (normalized.EvidenceQuote ?? '').trim();

  return normalized;
}

function validateRow(
  row: DependencyRegisterRow,
  options: DependencyRegisterWriteOptions,
  warnings: string[]
): void {
  if (row.RegisterSchemaVersion !== 'v3.1') {
    throw new DependencyContractError(
      'INVALID_SCHEMA',
      'RegisterSchemaVersion must be v3.1',
      { dependencyId: row.DependencyID, value: row.RegisterSchemaVersion }
    );
  }

  requireNonEmpty(row, 'DependencyID', 'INVALID_IDENTITY', 'DependencyID is required');
  requireNonEmpty(
    row,
    'FromPackageID',
    'INVALID_IDENTITY',
    'FromPackageID is required'
  );
  requireNonEmpty(
    row,
    'FromDeliverableID',
    'INVALID_IDENTITY',
    'FromDeliverableID is required'
  );
  requireNonEmpty(
    row,
    'FromDeliverableName',
    'INVALID_IDENTITY',
    'FromDeliverableName is required'
  );
  requireNonEmpty(row, 'DependencyClass', 'INVALID_ENUM', 'DependencyClass is required');
  requireNonEmpty(row, 'AnchorType', 'INVALID_ENUM', 'AnchorType is required');
  requireNonEmpty(row, 'Direction', 'INVALID_ENUM', 'Direction is required');
  requireNonEmpty(row, 'DependencyType', 'INVALID_ENUM', 'DependencyType is required');
  requireNonEmpty(row, 'TargetType', 'INVALID_ENUM', 'TargetType is required');
  requireNonEmpty(row, 'Origin', 'INVALID_ENUM', 'Origin is required');
  requireNonEmpty(row, 'FirstSeen', 'INVALID_DATE', 'FirstSeen is required');
  requireNonEmpty(row, 'LastSeen', 'INVALID_DATE', 'LastSeen is required');
  requireNonEmpty(row, 'Status', 'INVALID_ENUM', 'Status is required');

  if (!DEPENDENCY_ID_PATTERN.test(row.DependencyID)) {
    throw new DependencyContractError(
      'INVALID_IDENTITY',
      'DependencyID must match DEP-{PKG}-{DEL}-{SEQ}',
      { dependencyId: row.DependencyID }
    );
  }

  if (!DELIVERABLE_ID_PATTERN.test(row.FromDeliverableID)) {
    throw new DependencyContractError(
      'INVALID_IDENTITY',
      'FromDeliverableID must match DEL-XX-YY',
      { dependencyId: row.DependencyID, fromDeliverableId: row.FromDeliverableID }
    );
  }

  if (
    options.hostDeliverableId &&
    row.FromDeliverableID !== options.hostDeliverableId.trim()
  ) {
    throw new DependencyContractError(
      'INVALID_IDENTITY',
      'FromDeliverableID must match the host deliverable',
      {
        dependencyId: row.DependencyID,
        expected: options.hostDeliverableId,
        actual: row.FromDeliverableID
      }
    );
  }

  if (!isIsoDate(row.FirstSeen) || !isIsoDate(row.LastSeen)) {
    throw new DependencyContractError(
      'INVALID_DATE',
      'FirstSeen and LastSeen must use YYYY-MM-DD format',
      { dependencyId: row.DependencyID, firstSeen: row.FirstSeen, lastSeen: row.LastSeen }
    );
  }

  if (!isKnownEnumValue(row.DependencyClass, DEPENDENCY_CLASS_VALUES)) {
    throw new DependencyContractError('INVALID_ENUM', 'Invalid DependencyClass value', {
      dependencyId: row.DependencyID,
      value: row.DependencyClass
    });
  }

  if (!isKnownEnumValue(row.AnchorType, ANCHOR_TYPE_VALUES)) {
    throw new DependencyContractError('INVALID_ENUM', 'Invalid AnchorType value', {
      dependencyId: row.DependencyID,
      value: row.AnchorType
    });
  }

  if (!isKnownEnumValue(row.Direction, DIRECTION_VALUES)) {
    throw new DependencyContractError('INVALID_ENUM', 'Invalid Direction value', {
      dependencyId: row.DependencyID,
      value: row.Direction
    });
  }

  if (!isKnownEnumValue(row.DependencyType, DEPENDENCY_TYPE_VALUES)) {
    throw new DependencyContractError('INVALID_ENUM', 'Invalid DependencyType value', {
      dependencyId: row.DependencyID,
      value: row.DependencyType
    });
  }

  if (!isKnownEnumValue(row.TargetType, TARGET_TYPE_VALUES)) {
    throw new DependencyContractError('INVALID_ENUM', 'Invalid TargetType value', {
      dependencyId: row.DependencyID,
      value: row.TargetType
    });
  }

  if (row.Explicitness && !isKnownEnumValue(row.Explicitness, EXPLICITNESS_VALUES)) {
    throw new DependencyContractError('INVALID_ENUM', 'Invalid Explicitness value', {
      dependencyId: row.DependencyID,
      value: row.Explicitness
    });
  }

  if (
    row.SatisfactionStatus &&
    !isKnownEnumValue(row.SatisfactionStatus, SATISFACTION_STATUS_VALUES)
  ) {
    throw new DependencyContractError('INVALID_ENUM', 'Invalid SatisfactionStatus value', {
      dependencyId: row.DependencyID,
      value: row.SatisfactionStatus
    });
  }

  if (row.Confidence && !isKnownEnumValue(row.Confidence, CONFIDENCE_VALUES)) {
    throw new DependencyContractError('INVALID_ENUM', 'Invalid Confidence value', {
      dependencyId: row.DependencyID,
      value: row.Confidence
    });
  }

  if (!isKnownEnumValue(row.Origin, ORIGIN_VALUES)) {
    throw new DependencyContractError('INVALID_ENUM', 'Invalid Origin value', {
      dependencyId: row.DependencyID,
      value: row.Origin
    });
  }

  if (!isKnownEnumValue(row.Status, ROW_STATUS_VALUES)) {
    throw new DependencyContractError('INVALID_ENUM', 'Invalid Status value', {
      dependencyId: row.DependencyID,
      value: row.Status
    });
  }

  if (row.DependencyClass === 'ANCHOR') {
    if (row.AnchorType === 'NOT_APPLICABLE') {
      throw new DependencyContractError(
        'INVALID_CLASSIFICATION',
        'ANCHOR rows must use a non-NOT_APPLICABLE AnchorType',
        { dependencyId: row.DependencyID, anchorType: row.AnchorType }
      );
    }
    if (row.DependencyType !== 'OTHER') {
      throw new DependencyContractError(
        'INVALID_CLASSIFICATION',
        'ANCHOR rows must set DependencyType=OTHER',
        { dependencyId: row.DependencyID, dependencyType: row.DependencyType }
      );
    }
  }

  if (row.DependencyClass === 'EXECUTION' && row.AnchorType !== 'NOT_APPLICABLE') {
    throw new DependencyContractError(
      'INVALID_CLASSIFICATION',
      'EXECUTION rows must set AnchorType=NOT_APPLICABLE',
      { dependencyId: row.DependencyID, anchorType: row.AnchorType }
    );
  }

  if (row.TargetType === 'DELIVERABLE') {
    if (!row.TargetDeliverableID) {
      throw new DependencyContractError(
        'INVALID_TARGET',
        'DELIVERABLE targets require TargetDeliverableID',
        { dependencyId: row.DependencyID }
      );
    }
  } else if (row.TargetDeliverableID) {
    throw new DependencyContractError(
      'INVALID_TARGET',
      'Non-deliverable targets must leave TargetDeliverableID empty',
      { dependencyId: row.DependencyID, targetType: row.TargetType }
    );
  }

  if (row.Status === 'ACTIVE') {
    if (!row.EvidenceFile || !row.SourceRef) {
      throw new DependencyContractError(
        'INVALID_PROVENANCE',
        'ACTIVE rows require EvidenceFile and SourceRef',
        { dependencyId: row.DependencyID }
      );
    }
  }

  if (row.EvidenceQuote && quoteWordCount(row.EvidenceQuote) > 30) {
    warnings.push(`ROW:${row.DependencyID}:EVIDENCE_QUOTE_OVER_30_WORDS`);
  }
}

function validateSatisfactionTransitions(
  rows: DependencyRegisterRow[],
  previousRows: DependencyRegisterRow[] | undefined
): void {
  if (!previousRows || previousRows.length === 0) {
    return;
  }

  const previousById = new Map<string, DependencyRegisterRow>();
  for (const row of previousRows) {
    previousById.set(row.DependencyID, row);
  }

  for (const row of rows) {
    const previousRow = previousById.get(row.DependencyID);
    if (!previousRow) {
      continue;
    }

    if (
      !isValidSatisfactionTransition(previousRow.SatisfactionStatus, row.SatisfactionStatus)
    ) {
      throw new DependencyContractError(
        'INVALID_SATISFACTION_TRANSITION',
        'Invalid SatisfactionStatus transition',
        {
          dependencyId: row.DependencyID,
          from: previousRow.SatisfactionStatus,
          to: row.SatisfactionStatus
        }
      );
    }
  }
}

function validateRowRetention(
  rows: DependencyRegisterRow[],
  previousRows: DependencyRegisterRow[] | undefined
): void {
  if (!previousRows || previousRows.length === 0) {
    return;
  }

  const nextDependencyIds = new Set(rows.map((row) => row.DependencyID));
  const missingDependencyIds = previousRows
    .map((row) => (row.DependencyID ?? '').trim())
    .filter((dependencyId) => dependencyId && !nextDependencyIds.has(dependencyId));

  if (missingDependencyIds.length > 0) {
    throw new DependencyContractError(
      'MISSING_RETIRED_ROW',
      'Existing dependency rows must be retained and marked RETIRED instead of deleted',
      { missingDependencyIds }
    );
  }
}

function collectHeaders(rows: DependencyRegisterRow[]): string[] {
  const extensionHeaders = DEPENDENCY_EXTENSION_COLUMNS.filter((column) =>
    rows.some((row) => (row[column] ?? '').trim() !== '')
  );

  const extras = new Set<string>();
  for (const row of rows) {
    for (const key of Object.keys(row)) {
      if (
        DEPENDENCY_CORE_COLUMNS.includes(key as (typeof DEPENDENCY_CORE_COLUMNS)[number]) ||
        DEPENDENCY_EXTENSION_COLUMNS.includes(key as (typeof DEPENDENCY_EXTENSION_COLUMNS)[number])
      ) {
        continue;
      }
      extras.add(key);
    }
  }

  return [
    ...DEPENDENCY_CORE_COLUMNS,
    ...extensionHeaders,
    ...Array.from(extras).sort((a, b) => a.localeCompare(b))
  ];
}

export function serializeDependencyRegister(
  rows: DependencyRegisterRow[],
  options: DependencyRegisterWriteOptions = {}
): DependencyRegisterWriteResult {
  const warnings: string[] = [];
  const normalizedRows = rows.map((row) => normalizeRow(row, warnings));

  const seenDependencyIds = new Set<string>();
  let implementsNodeCount = 0;

  for (const row of normalizedRows) {
    if (seenDependencyIds.has(row.DependencyID)) {
      throw new DependencyContractError(
        'DUPLICATE_DEPENDENCY_ID',
        `Duplicate DependencyID '${row.DependencyID}'`,
        { dependencyId: row.DependencyID }
      );
    }
    seenDependencyIds.add(row.DependencyID);

    validateRow(row, options, warnings);
    if (row.DependencyClass === 'ANCHOR' && row.AnchorType === 'IMPLEMENTS_NODE') {
      implementsNodeCount += 1;
    }
  }

  if (implementsNodeCount !== 1 && normalizedRows.length > 0) {
    warnings.push('ANCHOR_IMPLEMENTS_NODE_COUNT_NOT_ONE');
  }

  validateRowRetention(normalizedRows, options.previousRows);
  validateSatisfactionTransitions(normalizedRows, options.previousRows);

  const headers = collectHeaders(normalizedRows);
  const csvRows = normalizedRows.map((row) => {
    const record: Record<string, string> = {};
    for (const header of headers) {
      record[header] = row[header] ?? '';
    }
    return record;
  });

  return {
    csv: serializeCsv(headers, csvRows),
    rows: normalizedRows,
    warnings
  };
}
