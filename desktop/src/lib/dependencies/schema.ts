export const DEPENDENCY_CORE_COLUMNS = [
  'RegisterSchemaVersion',
  'DependencyID',
  'FromPackageID',
  'FromDeliverableID',
  'FromDeliverableName',
  'DependencyClass',
  'AnchorType',
  'Direction',
  'DependencyType',
  'TargetType',
  'TargetPackageID',
  'TargetDeliverableID',
  'TargetRefID',
  'TargetName',
  'TargetLocation',
  'Statement',
  'EvidenceFile',
  'SourceRef',
  'EvidenceQuote',
  'Explicitness',
  'RequiredMaturity',
  'ProposedMaturity',
  'SatisfactionStatus',
  'Confidence',
  'Origin',
  'FirstSeen',
  'LastSeen',
  'Status',
  'Notes'
] as const;

export const DEPENDENCY_EXTENSION_COLUMNS = [
  'EstimateImpactClass',
  'ConsumerHint'
] as const;

export const DEPENDENCY_CLASS_VALUES = ['ANCHOR', 'EXECUTION'] as const;
export const ANCHOR_TYPE_VALUES = [
  'IMPLEMENTS_NODE',
  'TRACES_TO_REQUIREMENT',
  'NOT_APPLICABLE'
] as const;
export const DIRECTION_VALUES = ['UPSTREAM', 'DOWNSTREAM'] as const;
export const LEGACY_DIRECTION_VALUES = ['INBOUND', 'OUTBOUND'] as const;
export const DEPENDENCY_TYPE_VALUES = [
  'PREREQUISITE',
  'INTERFACE',
  'HANDOVER',
  'CONSTRAINT',
  'ENABLES',
  'OTHER'
] as const;
export const LEGACY_DEPENDENCY_TYPE_VALUES = ['COORDINATION', 'INFORMATION'] as const;
export const TARGET_TYPE_VALUES = [
  'DELIVERABLE',
  'PACKAGE',
  'WBS_NODE',
  'REQUIREMENT',
  'DOCUMENT',
  'EQUIPMENT',
  'EXTERNAL',
  'UNKNOWN'
] as const;
export const EXPLICITNESS_VALUES = ['EXPLICIT', 'IMPLICIT'] as const;
export const SATISFACTION_STATUS_VALUES = [
  'TBD',
  'PENDING',
  'IN_PROGRESS',
  'SATISFIED',
  'WAIVED',
  'NOT_APPLICABLE'
] as const;
export const CONFIDENCE_VALUES = ['HIGH', 'MEDIUM', 'LOW'] as const;
export const ORIGIN_VALUES = ['DECLARED', 'EXTRACTED'] as const;
export const ROW_STATUS_VALUES = ['ACTIVE', 'RETIRED'] as const;

export type DependencyCoreColumn = (typeof DEPENDENCY_CORE_COLUMNS)[number];
export type DependencyExtensionColumn = (typeof DEPENDENCY_EXTENSION_COLUMNS)[number];
export type DependencyClass = (typeof DEPENDENCY_CLASS_VALUES)[number];
export type AnchorType = (typeof ANCHOR_TYPE_VALUES)[number];
export type Direction = (typeof DIRECTION_VALUES)[number];
export type DependencyType = (typeof DEPENDENCY_TYPE_VALUES)[number];
export type TargetType = (typeof TARGET_TYPE_VALUES)[number];
export type Explicitness = (typeof EXPLICITNESS_VALUES)[number];
export type SatisfactionStatus = (typeof SATISFACTION_STATUS_VALUES)[number];
export type Confidence = (typeof CONFIDENCE_VALUES)[number];
export type Origin = (typeof ORIGIN_VALUES)[number];
export type RowStatus = (typeof ROW_STATUS_VALUES)[number];

export interface DependencyRegisterRow {
  RegisterSchemaVersion?: string;
  DependencyID: string;
  FromPackageID: string;
  FromDeliverableID: string;
  FromDeliverableName: string;
  DependencyClass: string;
  AnchorType: string;
  Direction: string;
  DependencyType: string;
  TargetType: string;
  TargetPackageID?: string;
  TargetDeliverableID?: string;
  TargetRefID?: string;
  TargetName?: string;
  TargetLocation?: string;
  Statement?: string;
  EvidenceFile?: string;
  SourceRef?: string;
  EvidenceQuote?: string;
  Explicitness?: string;
  RequiredMaturity?: string;
  ProposedMaturity?: string;
  SatisfactionStatus?: string;
  Confidence?: string;
  Origin: string;
  FirstSeen: string;
  LastSeen: string;
  Status: string;
  Notes?: string;
  EstimateImpactClass?: string;
  ConsumerHint?: string;
  [key: string]: string | undefined;
}

export type DependencyContractErrorCode =
  | 'INVALID_SCHEMA'
  | 'INVALID_ENUM'
  | 'INVALID_CLASSIFICATION'
  | 'INVALID_PROVENANCE'
  | 'INVALID_IDENTITY'
  | 'INVALID_TARGET'
  | 'INVALID_DATE'
  | 'DUPLICATE_DEPENDENCY_ID'
  | 'MISSING_RETIRED_ROW'
  | 'INVALID_SATISFACTION_TRANSITION';

export class DependencyContractError extends Error {
  readonly code: DependencyContractErrorCode;
  readonly details?: unknown;

  constructor(code: DependencyContractErrorCode, message: string, details?: unknown) {
    super(message);
    this.name = 'DependencyContractError';
    this.code = code;
    this.details = details;
  }
}

export const DEPENDENCY_ID_PATTERN = /^DEP-\d{2,3}-\d{2}-\d{3}$/;
export const DELIVERABLE_ID_PATTERN = /^DEL-\d{2,3}-\d{2}$/;
export const ISO_DATE_PATTERN = /^\d{4}-\d{2}-\d{2}$/;

const SATISFACTION_TRANSITION_MAP: Record<SatisfactionStatus, readonly SatisfactionStatus[]> = {
  TBD: ['PENDING', 'NOT_APPLICABLE', 'WAIVED'],
  PENDING: ['IN_PROGRESS', 'NOT_APPLICABLE', 'WAIVED'],
  IN_PROGRESS: ['SATISFIED', 'WAIVED'],
  SATISFIED: [],
  WAIVED: [],
  NOT_APPLICABLE: []
};

function toUpper(value: string | undefined): string {
  return (value ?? '').trim().toUpperCase();
}

export function normalizeSchemaVersion(value: string | undefined): string {
  return value?.trim() ? value.trim() : 'v3.1';
}

export function normalizeDirection(value: string | undefined): Direction | string {
  const normalized = toUpper(value);
  if (normalized === 'INBOUND') {
    return 'UPSTREAM';
  }
  if (normalized === 'OUTBOUND') {
    return 'DOWNSTREAM';
  }
  return normalized;
}

export function normalizeDependencyType(value: string | undefined): DependencyType | string {
  const normalized = toUpper(value);
  if (normalized === 'COORDINATION' || normalized === 'INFORMATION') {
    return 'OTHER';
  }
  return normalized;
}

export function isIsoDate(value: string | undefined): boolean {
  return ISO_DATE_PATTERN.test((value ?? '').trim());
}

export function isKnownEnumValue(value: string | undefined, allowed: readonly string[]): boolean {
  return allowed.includes(toUpper(value));
}

export function normalizeEnum(value: string | undefined): string {
  return toUpper(value);
}

export function isValidSatisfactionTransition(
  from: string | undefined,
  to: string | undefined
): boolean {
  const normalizedFrom = toUpper(from) as SatisfactionStatus;
  const normalizedTo = toUpper(to) as SatisfactionStatus;
  if (!normalizedFrom || !normalizedTo || normalizedFrom === normalizedTo) {
    return true;
  }

  if (!(normalizedFrom in SATISFACTION_TRANSITION_MAP)) {
    return false;
  }

  return SATISFACTION_TRANSITION_MAP[normalizedFrom].includes(normalizedTo);
}

export function quoteWordCount(value: string | undefined): number {
  return (value ?? '')
    .trim()
    .split(/\s+/)
    .filter(Boolean).length;
}
