import type {
  SelectedSessionReplayProjection,
  SelectedSessionReplayState
} from './contracts';

export type SessionSelectionBlockReason =
  | 'INVALID_SESSION_ID'
  | 'SESSION_NOT_RECORDED'
  | 'LIVE_TURN_ACTIVE'
  | 'REPLAY_ISOLATION_UNAVAILABLE';

export type GuardedSessionSelectionDecision =
  | {
      outcome: 'RETURN_TO_PRIMARY';
      state: Extract<SelectedSessionReplayState, { status: 'IDLE' }>;
    }
  | {
      outcome: 'SELECT_REPLAY';
      state: Extract<SelectedSessionReplayState, { status: 'LOADING' }>;
    }
  | {
      outcome: 'UNCHANGED';
      state: SelectedSessionReplayState;
    }
  | {
      outcome: 'BLOCKED';
      reason: SessionSelectionBlockReason;
      state: SelectedSessionReplayState;
    };

export type GuardedSessionSelectionInput = {
  currentState: SelectedSessionReplayState;
  requestedSessionId: string | null | undefined;
  primarySessionId?: string | null;
  recordedSessionIds: readonly string[];
  liveTurnActive: boolean;
  replayIsolationAvailable: boolean;
};

function normalizedId(value: string | null | undefined): string | undefined {
  const normalized = value?.trim();
  return normalized ? normalized : undefined;
}

function selectedSessionId(
  state: SelectedSessionReplayState
): string | undefined {
  switch (state.status) {
    case 'LOADING':
    case 'UNAVAILABLE':
      return state.selectedSessionId;
    case 'READY':
      return state.projection.selectedSessionId;
    case 'IDLE':
      return undefined;
  }
}

export function guardRecordedSessionSelection(
  input: GuardedSessionSelectionInput
): GuardedSessionSelectionDecision {
  const requestedSessionId = normalizedId(input.requestedSessionId);
  if (!requestedSessionId) {
    return {
      outcome: 'BLOCKED',
      reason: 'INVALID_SESSION_ID',
      state: input.currentState
    };
  }

  const primarySessionId = normalizedId(input.primarySessionId);
  if (primarySessionId && requestedSessionId === primarySessionId) {
    return {
      outcome: 'RETURN_TO_PRIMARY',
      state: { status: 'IDLE' }
    };
  }

  if (selectedSessionId(input.currentState) === requestedSessionId) {
    return {
      outcome: 'UNCHANGED',
      state: input.currentState
    };
  }

  if (input.liveTurnActive) {
    return {
      outcome: 'BLOCKED',
      reason: 'LIVE_TURN_ACTIVE',
      state: input.currentState
    };
  }

  if (!input.replayIsolationAvailable) {
    return {
      outcome: 'BLOCKED',
      reason: 'REPLAY_ISOLATION_UNAVAILABLE',
      state: input.currentState
    };
  }

  const recordedSessionIds = new Set(
    input.recordedSessionIds.flatMap((sessionId) => {
      const normalized = normalizedId(sessionId);
      return normalized ? [normalized] : [];
    })
  );
  if (!recordedSessionIds.has(requestedSessionId)) {
    return {
      outcome: 'BLOCKED',
      reason: 'SESSION_NOT_RECORDED',
      state: input.currentState
    };
  }

  return {
    outcome: 'SELECT_REPLAY',
    state: {
      status: 'LOADING',
      selectedSessionId: requestedSessionId
    }
  };
}

export function acceptGuardedReplayProjection(
  state: SelectedSessionReplayState,
  projection: SelectedSessionReplayProjection
): SelectedSessionReplayState {
  if (
    state.status !== 'LOADING' ||
    state.selectedSessionId !== projection.selectedSessionId
  ) {
    return state;
  }
  return {
    status: 'READY',
    projection
  };
}

export function rejectGuardedReplayProjection(
  state: SelectedSessionReplayState,
  selectedSessionId: string,
  message: string
): SelectedSessionReplayState {
  if (
    state.status !== 'LOADING' ||
    state.selectedSessionId !== selectedSessionId
  ) {
    return state;
  }
  return {
    status: 'UNAVAILABLE',
    selectedSessionId,
    message
  };
}

export function returnToPrimaryDialogue(): SelectedSessionReplayState {
  return { status: 'IDLE' };
}
