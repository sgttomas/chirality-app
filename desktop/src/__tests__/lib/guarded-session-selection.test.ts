import { describe, expect, it } from 'vitest';
import type {
  SelectedSessionReplayProjection,
  SelectedSessionReplayState
} from '../../lib/woven-dialogue/contracts';
import {
  acceptGuardedReplayProjection,
  guardRecordedSessionSelection,
  rejectGuardedReplayProjection,
  returnToPrimaryDialogue
} from '../../lib/woven-dialogue/guarded-session-selection';

const idle: SelectedSessionReplayState = { status: 'IDLE' };

function replayProjection(sessionId: string): SelectedSessionReplayProjection {
  return {
    selectedSessionId: sessionId,
    sourceReference: `session:${sessionId}`,
    observedAt: '2026-07-23T10:00:00Z',
    disclosure: 'EMPTY',
    currency: 'CURRENT',
    transcript: {
      sessionId,
      itemCount: 0,
      items: []
    },
    instructionHistory: [],
    instructionBases: [],
    malformedLineCount: 0,
    sourceEventCount: 0,
    renderedItemCount: 0,
    diagnostics: []
  };
}

describe('guarded recorded-session selection', () => {
  it('blocks replay selection while a live turn is active', () => {
    expect(
      guardRecordedSessionSelection({
        currentState: idle,
        requestedSessionId: 'child',
        primarySessionId: 'primary',
        recordedSessionIds: ['primary', 'child'],
        liveTurnActive: true,
        replayIsolationAvailable: true
      })
    ).toEqual({
      outcome: 'BLOCKED',
      reason: 'LIVE_TURN_ACTIVE',
      state: idle
    });
  });

  it('allows the persistent return to primary even while a live turn is active', () => {
    const current: SelectedSessionReplayState = {
      status: 'READY',
      projection: replayProjection('child')
    };
    expect(
      guardRecordedSessionSelection({
        currentState: current,
        requestedSessionId: 'primary',
        primarySessionId: 'primary',
        recordedSessionIds: ['primary', 'child'],
        liveTurnActive: true,
        replayIsolationAvailable: true
      })
    ).toEqual({
      outcome: 'RETURN_TO_PRIMARY',
      state: { status: 'IDLE' }
    });
  });

  it('requires an admitted session and isolated replay state', () => {
    const unavailableIsolation = guardRecordedSessionSelection({
      currentState: idle,
      requestedSessionId: 'child',
      primarySessionId: 'primary',
      recordedSessionIds: ['child'],
      liveTurnActive: false,
      replayIsolationAvailable: false
    });
    const unrecorded = guardRecordedSessionSelection({
      currentState: idle,
      requestedSessionId: 'unknown',
      primarySessionId: 'primary',
      recordedSessionIds: ['child'],
      liveTurnActive: false,
      replayIsolationAvailable: true
    });

    expect(unavailableIsolation).toEqual({
      outcome: 'BLOCKED',
      reason: 'REPLAY_ISOLATION_UNAVAILABLE',
      state: idle
    });
    expect(unrecorded).toEqual({
      outcome: 'BLOCKED',
      reason: 'SESSION_NOT_RECORDED',
      state: idle
    });
  });

  it('changes only replay presentation state for an allowed selection', () => {
    const primaryState = {
      draft: 'unchanged',
      attachments: ['a.md'],
      contextReferences: ['ref-1'],
      permissionTarget: 'primary'
    };
    const before = structuredClone(primaryState);
    const decision = guardRecordedSessionSelection({
      currentState: idle,
      requestedSessionId: 'child',
      primarySessionId: 'primary',
      recordedSessionIds: ['primary', 'child'],
      liveTurnActive: false,
      replayIsolationAvailable: true
    });

    expect(decision).toEqual({
      outcome: 'SELECT_REPLAY',
      state: {
        status: 'LOADING',
        selectedSessionId: 'child'
      }
    });
    expect(primaryState).toEqual(before);
  });

  it('ignores stale replay completion and failure results', () => {
    const loading: SelectedSessionReplayState = {
      status: 'LOADING',
      selectedSessionId: 'new-child'
    };

    expect(acceptGuardedReplayProjection(loading, replayProjection('old-child'))).toBe(
      loading
    );
    expect(rejectGuardedReplayProjection(loading, 'old-child', 'late failure')).toBe(
      loading
    );
    expect(acceptGuardedReplayProjection(loading, replayProjection('new-child'))).toEqual({
      status: 'READY',
      projection: replayProjection('new-child')
    });
  });

  it('returns to an idle primary-dialogue presentation without runtime callbacks', () => {
    expect(returnToPrimaryDialogue()).toEqual({ status: 'IDLE' });
  });
});
