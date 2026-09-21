import { describe, expect, it } from 'vitest';
// Imported via the package barrel: the fenced package.json exports map carries no
// './operation-proposal' subpath entry (D-APP-49 leaves package.json untouched).
import {
  isOperationProposal,
  isOperationProposalLifecycleState,
  isOperationProposalRiskClass,
  isOperationProposalStatus,
  OPERATION_PROPOSAL_LIFECYCLE_STATES,
  OPERATION_PROPOSAL_RISK_CLASSES,
  OPERATION_PROPOSAL_STATUS,
  type OperationProposal
} from '@chirality/runtime-contracts';

function validProposal(): OperationProposal {
  return {
    proposal_id: 'op-2026-07-04-001',
    profile_id: 'open_pipe_stress',
    base_state: 'TBD',
    operation_name: 'add_support',
    status: 'proposal_only',
    lifecycle: 'draft',
    created_at: '2026-07-04T00:00:00Z',
    created_by: 'DOMAIN_ENGINE',
    input_refs: ['projects/chirality-piping/core/handoff/manifest.json'],
    intended_changes: ['Add resting support at node N42'],
    deterministic_checks: ['proposal.schema.validate -> TBD'],
    expected_output_refs: ['_DomainEngines/proposals/open_pipe_stress/op-001-summary.md'],
    risks: ['engine cannot verify support stiffness assumption'],
    assumptions: ['support stiffness per vendor catalog'],
    blockers: [],
    boundary_notice:
      'Not approved, certified, sealed, code-compliant, or ready for construction absent a cited human authoritative record.',
    required_human_gate: 'human-accept-op-001',
    operation_risk_class: 'engine_silent',
    provenance_on_judgment_values: 'vendor catalog ref TBD',
    storage_path: '_DomainEngines/proposals/open_pipe_stress/op-001.yaml'
  };
}

describe('operation proposal contract constants', () => {
  it('preserves the order-exact lifecycle tuple', () => {
    expect([...OPERATION_PROPOSAL_LIFECYCLE_STATES]).toEqual([
      'draft',
      'ready_for_review',
      'accepted',
      'rejected',
      'applied'
    ]);
  });

  it('mirrors the validator risk-class enum exactly', () => {
    expect([...OPERATION_PROPOSAL_RISK_CLASSES]).toEqual(['engine_checkable', 'engine_silent']);
  });

  it('pins the constant proposal-only status', () => {
    expect(OPERATION_PROPOSAL_STATUS).toBe('proposal_only');
  });
});

describe('operation proposal enum guards', () => {
  it('accepts every canonical lifecycle state and risk class', () => {
    for (const state of OPERATION_PROPOSAL_LIFECYCLE_STATES) {
      expect(isOperationProposalLifecycleState(state)).toBe(true);
    }
    for (const riskClass of OPERATION_PROPOSAL_RISK_CLASSES) {
      expect(isOperationProposalRiskClass(riskClass)).toBe(true);
    }
    expect(isOperationProposalStatus('proposal_only')).toBe(true);
  });

  it('rejects non-members', () => {
    expect(isOperationProposalLifecycleState('proposed')).toBe(false);
    expect(isOperationProposalLifecycleState('DRAFT')).toBe(false);
    expect(isOperationProposalRiskClass('engine_verified')).toBe(false);
    expect(isOperationProposalStatus('accepted')).toBe(false);
    expect(isOperationProposalStatus(undefined)).toBe(false);
  });
});

describe('isOperationProposal', () => {
  it('accepts the canonical 20-field proposal form', () => {
    expect(isOperationProposal(validProposal())).toBe(true);
  });

  it('accepts every lifecycle state as the single-value lifecycle field', () => {
    for (const state of OPERATION_PROPOSAL_LIFECYCLE_STATES) {
      expect(isOperationProposal({ ...validProposal(), lifecycle: state })).toBe(true);
    }
  });

  it('accepts empty evidence lists (no risks, assumptions, or blockers recorded)', () => {
    expect(
      isOperationProposal({ ...validProposal(), risks: [], assumptions: [], blockers: [] })
    ).toBe(true);
  });

  it('rejects a missing required field', () => {
    const { storage_path, ...withoutStoragePath } = validProposal();
    expect(isOperationProposal(withoutStoragePath)).toBe(false);
    const { boundary_notice, ...withoutBoundaryNotice } = validProposal();
    expect(isOperationProposal(withoutBoundaryNotice)).toBe(false);
  });

  it('rejects empty required strings', () => {
    expect(isOperationProposal({ ...validProposal(), proposal_id: '' })).toBe(false);
    expect(isOperationProposal({ ...validProposal(), base_state: '   ' })).toBe(false);
  });

  it('rejects invalid status, lifecycle, and risk-class values', () => {
    expect(isOperationProposal({ ...validProposal(), status: 'accepted' })).toBe(false);
    expect(isOperationProposal({ ...validProposal(), lifecycle: 'in_review' })).toBe(false);
    expect(
      isOperationProposal({ ...validProposal(), operation_risk_class: 'checkable' })
    ).toBe(false);
  });

  it('rejects list fields with non-string or empty-string entries', () => {
    expect(isOperationProposal({ ...validProposal(), input_refs: [42] })).toBe(false);
    expect(isOperationProposal({ ...validProposal(), intended_changes: [''] })).toBe(false);
    expect(isOperationProposal({ ...validProposal(), blockers: 'none' })).toBe(false);
  });

  it('rejects non-record values', () => {
    expect(isOperationProposal(null)).toBe(false);
    expect(isOperationProposal([])).toBe(false);
    expect(isOperationProposal('proposal')).toBe(false);
  });
});
