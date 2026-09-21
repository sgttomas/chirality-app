import { describe, expect, it } from 'vitest';
// Imported via the package barrel: the fenced package.json exports map carries no
// './domain-profile' subpath entry (D-APP-49 leaves package.json untouched).
import {
  DETERMINISTIC_TOOL_MODES,
  DOMAIN_ENGINE_INTEGRATION_LEVELS,
  DOMAIN_ENGINE_PROFILE_STATUSES,
  isDeterministicToolContract,
  isDeterministicToolMode,
  isDomainEngineIntegrationLevel,
  isDomainEngineProfessionalBoundary,
  isDomainEngineProfile,
  isDomainEngineProfileStatus,
  isOperationProposalContract,
  OPERATION_PROPOSAL_CONTRACT_LIFECYCLE,
  OPERATION_PROPOSAL_CONTRACT_RISK_CLASSES,
  OPERATION_PROPOSAL_LIFECYCLE_STATES,
  OPERATION_PROPOSAL_RISK_CLASSES,
  type DomainEngineProfile
} from '@chirality/runtime-contracts';

function validProfile(): DomainEngineProfile {
  return {
    schema_version: '1.0',
    id: 'open_pipe_stress',
    name: 'OpenPipeStress',
    engine_type: 'pipe-stress-analysis',
    profile_version: '0.1',
    profile_status: 'DRAFT',
    integration_level: 'MANUAL_BRIDGE',
    domain_root_patterns: ['projects/chirality-piping/**'],
    authoritative_artifacts: ['projects/chirality-piping/core/**'],
    chirality_readable_artifacts: ['projects/chirality-piping/core/handoff/**'],
    protected_write_paths: ['projects/chirality-piping/core/**'],
    agent_writable_paths: ['_DomainEngines/proposals/open_pipe_stress/**'],
    deterministic_tools: [
      {
        id: 'profile.validate',
        mode: 'read_only',
        requires_human_confirmation: false,
        validate_result_schema: 'TBD',
        apply_result_schema: 'TBD'
      }
    ],
    operation_proposal_contract: {
      lifecycle: OPERATION_PROPOSAL_CONTRACT_LIFECYCLE,
      risk_classes: OPERATION_PROPOSAL_CONTRACT_RISK_CLASSES,
      deterministic_check_result_schema: 'TBD',
      accepted_or_applied_requires: [
        'human approval bound to git SHA per K-AUTH-2',
        'domain-engine-controlled apply or external terminal acceptance record'
      ]
    },
    professional_boundary: {
      agent_must_not_claim: ['code compliant for reliance', 'professionally approved']
    },
    open_issues: ['TBD: declare validate/apply result schemas']
  };
}

describe('domain profile contract constants', () => {
  it('mirrors the validator profile-status enum exactly', () => {
    expect([...DOMAIN_ENGINE_PROFILE_STATUSES]).toEqual([
      'NONE',
      'DRAFT',
      'VALIDATED',
      'ADOPTED',
      'STALE',
      'INVALID',
      'UNKNOWN'
    ]);
  });

  it('mirrors the validator integration-level enum exactly', () => {
    expect([...DOMAIN_ENGINE_INTEGRATION_LEVELS]).toEqual([
      'MANUAL_BRIDGE',
      'READ_ONLY',
      'DOMAIN_CONTROLLED_WRITE',
      'OPERATION_PROPOSAL',
      'EXTERNAL_RESULT_STATE'
    ]);
  });

  it('mirrors the validator tool-mode enum exactly', () => {
    expect([...DETERMINISTIC_TOOL_MODES]).toEqual([
      'read_only',
      'summary_write',
      'domain_controlled_write',
      'proposal_validate',
      'proposal_apply'
    ]);
  });

  it('preserves the order-exact contract lifecycle tuple', () => {
    expect([...OPERATION_PROPOSAL_CONTRACT_LIFECYCLE]).toEqual([
      'draft',
      'ready_for_review',
      'accepted',
      'rejected',
      'applied'
    ]);
  });

  it('preserves the contract risk-class tuple', () => {
    expect([...OPERATION_PROPOSAL_CONTRACT_RISK_CLASSES]).toEqual([
      'engine_checkable',
      'engine_silent'
    ]);
  });

  it('stays lockstep with the operation-proposal module vocabulary', () => {
    expect([...OPERATION_PROPOSAL_CONTRACT_LIFECYCLE]).toEqual([
      ...OPERATION_PROPOSAL_LIFECYCLE_STATES
    ]);
    expect([...OPERATION_PROPOSAL_CONTRACT_RISK_CLASSES]).toEqual([
      ...OPERATION_PROPOSAL_RISK_CLASSES
    ]);
  });
});

describe('domain profile enum guards', () => {
  it('accepts every canonical enum member', () => {
    for (const status of DOMAIN_ENGINE_PROFILE_STATUSES) {
      expect(isDomainEngineProfileStatus(status)).toBe(true);
    }
    for (const level of DOMAIN_ENGINE_INTEGRATION_LEVELS) {
      expect(isDomainEngineIntegrationLevel(level)).toBe(true);
    }
    for (const mode of DETERMINISTIC_TOOL_MODES) {
      expect(isDeterministicToolMode(mode)).toBe(true);
    }
  });

  it('rejects non-members and non-strings', () => {
    expect(isDomainEngineProfileStatus('adopted')).toBe(false);
    expect(isDomainEngineProfileStatus('PROPOSED')).toBe(false);
    expect(isDomainEngineIntegrationLevel('FULL_WRITE')).toBe(false);
    expect(isDeterministicToolMode('write')).toBe(false);
    expect(isDeterministicToolMode(1)).toBe(false);
    expect(isDomainEngineProfileStatus(undefined)).toBe(false);
  });
});

describe('isDeterministicToolContract', () => {
  it('accepts a declared tool contract', () => {
    expect(isDeterministicToolContract(validProfile().deterministic_tools[0])).toBe(true);
  });

  it('rejects invalid mode, missing boolean, and empty schema refs', () => {
    const tool = validProfile().deterministic_tools[0];
    expect(isDeterministicToolContract({ ...tool, mode: 'write' })).toBe(false);
    expect(
      isDeterministicToolContract({ ...tool, requires_human_confirmation: 'no' })
    ).toBe(false);
    expect(isDeterministicToolContract({ ...tool, validate_result_schema: '' })).toBe(false);
    expect(isDeterministicToolContract({ ...tool, apply_result_schema: '  ' })).toBe(false);
    expect(isDeterministicToolContract(null)).toBe(false);
  });
});

describe('isOperationProposalContract', () => {
  it('accepts the canonical contract block', () => {
    expect(isOperationProposalContract(validProfile().operation_proposal_contract)).toBe(true);
  });

  it('rejects lifecycle values out of canonical order', () => {
    const contract = validProfile().operation_proposal_contract;
    expect(
      isOperationProposalContract({
        ...contract,
        lifecycle: ['ready_for_review', 'draft', 'accepted', 'rejected', 'applied']
      })
    ).toBe(false);
    expect(
      isOperationProposalContract({
        ...contract,
        lifecycle: ['draft', 'ready_for_review', 'accepted', 'rejected']
      })
    ).toBe(false);
  });

  it('rejects wrong or reordered risk classes and empty requirements', () => {
    const contract = validProfile().operation_proposal_contract;
    expect(
      isOperationProposalContract({
        ...contract,
        risk_classes: ['engine_silent', 'engine_checkable']
      })
    ).toBe(false);
    expect(
      isOperationProposalContract({ ...contract, accepted_or_applied_requires: [] })
    ).toBe(false);
  });
});

describe('isDomainEngineProfile', () => {
  it('accepts the canonical snake_case profile form', () => {
    expect(isDomainEngineProfile(validProfile())).toBe(true);
  });

  it('accepts a profile without the optional fields', () => {
    const { profile_status, integration_level, open_issues, ...rest } = validProfile();
    expect(isDomainEngineProfile(rest)).toBe(true);
  });

  it('rejects missing or empty required strings', () => {
    const { id, ...withoutId } = validProfile();
    expect(isDomainEngineProfile(withoutId)).toBe(false);
    expect(isDomainEngineProfile({ ...validProfile(), engine_type: '' })).toBe(false);
    expect(isDomainEngineProfile({ ...validProfile(), profile_version: '   ' })).toBe(false);
  });

  it('rejects invalid optional enum values when present', () => {
    expect(isDomainEngineProfile({ ...validProfile(), profile_status: 'PENDING' })).toBe(false);
    expect(
      isDomainEngineProfile({ ...validProfile(), integration_level: 'READONLY' })
    ).toBe(false);
  });

  it('rejects invalid open_issues elements when present', () => {
    expect(isDomainEngineProfile({ ...validProfile(), open_issues: [42] })).toBe(false);
    expect(isDomainEngineProfile({ ...validProfile(), open_issues: [''] })).toBe(false);
  });

  it('rejects empty required path lists', () => {
    expect(isDomainEngineProfile({ ...validProfile(), domain_root_patterns: [] })).toBe(false);
    expect(
      isDomainEngineProfile({ ...validProfile(), agent_writable_paths: ['ok', 42] })
    ).toBe(false);
  });

  it('rejects an empty deterministic-tools list and invalid boundary block', () => {
    expect(isDomainEngineProfile({ ...validProfile(), deterministic_tools: [] })).toBe(false);
    expect(
      isDomainEngineProfile({
        ...validProfile(),
        professional_boundary: { agent_must_not_claim: [] }
      })
    ).toBe(false);
    expect(isDomainEngineProfessionalBoundary({ agent_must_not_claim: ['x'] })).toBe(true);
    expect(isDomainEngineProfessionalBoundary({})).toBe(false);
  });

  it('rejects non-record values', () => {
    expect(isDomainEngineProfile(null)).toBe(false);
    expect(isDomainEngineProfile([])).toBe(false);
    expect(isDomainEngineProfile('domain_profile')).toBe(false);
  });
});
