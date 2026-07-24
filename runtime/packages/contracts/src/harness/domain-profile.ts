/**
 * `DomainEngineProfile` — inert source-type mirror of the framework-root domain-engine
 * persona's "Minimal Domain Engine Profile Shape".
 *
 * Mirror source (canonical per D-T0-01):
 * `agents/AGENT_DOMAIN_ENGINE.md@77a327727605f05da5f304288f1ddd87dc09659d`.
 * App-dev conformance mirror: `docs/TYPES.md` §11.1 (canonical snake_case profile form).
 * Enum lists and the order-exact lifecycle mirror
 * `tools/validation/validate_domain_engine_profile.py` (same contract-source pin).
 *
 * Types + type guards only (D-APP-49 O-A, riders 1-2): no runtime behavior beyond the
 * guards, no persistence, no UI, no I/O, no imports. Deterministic profile validation
 * remains owned by `tools/validation/validate_domain_engine_profile.py`; the guards here
 * mirror its required-field, non-empty, and enum semantics structurally and do not
 * replace it (ASCII-token and schema-ref checks stay validator-owned).
 */

export const DOMAIN_ENGINE_PROFILE_STATUSES = [
  'NONE',
  'DRAFT',
  'VALIDATED',
  'ADOPTED',
  'STALE',
  'INVALID',
  'UNKNOWN'
] as const;

export type DomainEngineProfileStatus = (typeof DOMAIN_ENGINE_PROFILE_STATUSES)[number];

export const DOMAIN_ENGINE_INTEGRATION_LEVELS = [
  'MANUAL_BRIDGE',
  'READ_ONLY',
  'DOMAIN_CONTROLLED_WRITE',
  'OPERATION_PROPOSAL',
  'EXTERNAL_RESULT_STATE'
] as const;

export type DomainEngineIntegrationLevel = (typeof DOMAIN_ENGINE_INTEGRATION_LEVELS)[number];

export const DETERMINISTIC_TOOL_MODES = [
  'read_only',
  'summary_write',
  'domain_controlled_write',
  'proposal_validate',
  'proposal_apply'
] as const;

export type DeterministicToolMode = (typeof DETERMINISTIC_TOOL_MODES)[number];

/**
 * Canonical `operation_proposal_contract.lifecycle` value. The order is contractual:
 * the validator raises `CONTRACT_MISMATCH` unless a profile lists exactly these values
 * in exactly this order (`validate_domain_engine_profile.py` `OPERATION_LIFECYCLE_VALUES`).
 */
export const OPERATION_PROPOSAL_CONTRACT_LIFECYCLE = [
  'draft',
  'ready_for_review',
  'accepted',
  'rejected',
  'applied'
] as const;

/**
 * Canonical `operation_proposal_contract.risk_classes` value. The validator requires
 * exactly these values in this (sorted) order when checking the contract block.
 */
export const OPERATION_PROPOSAL_CONTRACT_RISK_CLASSES = [
  'engine_checkable',
  'engine_silent'
] as const;

/**
 * One declared deterministic tool contract (`deterministic_tools[]` entry).
 * `validate_result_schema` / `apply_result_schema` are schema refs or explicit `'TBD'`;
 * they are never inferred from chat.
 */
export type DeterministicToolContract = {
  id: string;
  mode: DeterministicToolMode;
  requires_human_confirmation: boolean;
  validate_result_schema: string;
  apply_result_schema: string;
};

/**
 * The profile's `operation_proposal_contract` block. `lifecycle` and `risk_classes`
 * are typed as the exact canonical tuples so order stays machine-visible.
 */
export type OperationProposalContract = {
  lifecycle: typeof OPERATION_PROPOSAL_CONTRACT_LIFECYCLE;
  risk_classes: typeof OPERATION_PROPOSAL_CONTRACT_RISK_CLASSES;
  deterministic_check_result_schema: string;
  accepted_or_applied_requires: readonly string[];
};

/**
 * The profile's `professional_boundary` block: claims agents must not make absent a
 * cited human authoritative record (K-DOMAIN-4).
 */
export type DomainEngineProfessionalBoundary = {
  agent_must_not_claim: readonly string[];
};

/**
 * Canonical snake_case domain engine profile form per `docs/TYPES.md` §11.1.
 * `profile_status`, `integration_level`, and `open_issues` are optional at the shape
 * level, matching the validator (`required=False` enums; `open_issues` unvalidated).
 */
export type DomainEngineProfile = {
  schema_version: string;
  id: string;
  name: string;
  engine_type: string;
  profile_version: string;
  profile_status?: DomainEngineProfileStatus;
  integration_level?: DomainEngineIntegrationLevel;
  domain_root_patterns: readonly string[];
  authoritative_artifacts: readonly string[];
  chirality_readable_artifacts: readonly string[];
  protected_write_paths: readonly string[];
  agent_writable_paths: readonly string[];
  deterministic_tools: readonly DeterministicToolContract[];
  operation_proposal_contract: OperationProposalContract;
  professional_boundary: DomainEngineProfessionalBoundary;
  open_issues?: readonly string[];
};

const DOMAIN_ENGINE_PROFILE_STATUS_SET = new Set<string>(DOMAIN_ENGINE_PROFILE_STATUSES);
const DOMAIN_ENGINE_INTEGRATION_LEVEL_SET = new Set<string>(DOMAIN_ENGINE_INTEGRATION_LEVELS);
const DETERMINISTIC_TOOL_MODE_SET = new Set<string>(DETERMINISTIC_TOOL_MODES);

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isNonEmptyString(value: unknown): value is string {
  return typeof value === 'string' && value.trim().length > 0;
}

function isNonEmptyStringList(value: unknown): value is readonly string[] {
  return Array.isArray(value) && value.length > 0 && value.every(isNonEmptyString);
}

function isStringList(value: unknown): value is readonly string[] {
  return Array.isArray(value) && value.every(isNonEmptyString);
}

export function isDomainEngineProfileStatus(
  value: unknown
): value is DomainEngineProfileStatus {
  return typeof value === 'string' && DOMAIN_ENGINE_PROFILE_STATUS_SET.has(value);
}

export function isDomainEngineIntegrationLevel(
  value: unknown
): value is DomainEngineIntegrationLevel {
  return typeof value === 'string' && DOMAIN_ENGINE_INTEGRATION_LEVEL_SET.has(value);
}

export function isDeterministicToolMode(value: unknown): value is DeterministicToolMode {
  return typeof value === 'string' && DETERMINISTIC_TOOL_MODE_SET.has(value);
}

export function isDeterministicToolContract(
  value: unknown
): value is DeterministicToolContract {
  if (!isRecord(value)) {
    return false;
  }
  return (
    isNonEmptyString(value.id) &&
    isDeterministicToolMode(value.mode) &&
    typeof value.requires_human_confirmation === 'boolean' &&
    isNonEmptyString(value.validate_result_schema) &&
    isNonEmptyString(value.apply_result_schema)
  );
}

export function isOperationProposalContract(
  value: unknown
): value is OperationProposalContract {
  if (!isRecord(value)) {
    return false;
  }
  const lifecycle = value.lifecycle;
  const riskClasses = value.risk_classes;
  return (
    Array.isArray(lifecycle) &&
    lifecycle.length === OPERATION_PROPOSAL_CONTRACT_LIFECYCLE.length &&
    OPERATION_PROPOSAL_CONTRACT_LIFECYCLE.every((state, index) => lifecycle[index] === state) &&
    Array.isArray(riskClasses) &&
    riskClasses.length === OPERATION_PROPOSAL_CONTRACT_RISK_CLASSES.length &&
    OPERATION_PROPOSAL_CONTRACT_RISK_CLASSES.every(
      (riskClass, index) => riskClasses[index] === riskClass
    ) &&
    isNonEmptyString(value.deterministic_check_result_schema) &&
    isNonEmptyStringList(value.accepted_or_applied_requires)
  );
}

export function isDomainEngineProfessionalBoundary(
  value: unknown
): value is DomainEngineProfessionalBoundary {
  return isRecord(value) && isNonEmptyStringList(value.agent_must_not_claim);
}

export function isDomainEngineProfile(value: unknown): value is DomainEngineProfile {
  if (!isRecord(value)) {
    return false;
  }
  if (
    !isNonEmptyString(value.schema_version) ||
    !isNonEmptyString(value.id) ||
    !isNonEmptyString(value.name) ||
    !isNonEmptyString(value.engine_type) ||
    !isNonEmptyString(value.profile_version)
  ) {
    return false;
  }
  if (value.profile_status !== undefined && !isDomainEngineProfileStatus(value.profile_status)) {
    return false;
  }
  if (
    value.integration_level !== undefined &&
    !isDomainEngineIntegrationLevel(value.integration_level)
  ) {
    return false;
  }
  if (
    !isNonEmptyStringList(value.domain_root_patterns) ||
    !isNonEmptyStringList(value.authoritative_artifacts) ||
    !isNonEmptyStringList(value.chirality_readable_artifacts) ||
    !isNonEmptyStringList(value.protected_write_paths) ||
    !isNonEmptyStringList(value.agent_writable_paths)
  ) {
    return false;
  }
  const tools = value.deterministic_tools;
  if (!Array.isArray(tools) || tools.length === 0 || !tools.every(isDeterministicToolContract)) {
    return false;
  }
  if (!isOperationProposalContract(value.operation_proposal_contract)) {
    return false;
  }
  if (!isDomainEngineProfessionalBoundary(value.professional_boundary)) {
    return false;
  }
  if (value.open_issues !== undefined && !isStringList(value.open_issues)) {
    return false;
  }
  return true;
}
