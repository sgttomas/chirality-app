/**
 * One vocabulary for what the agent is doing right now and how the last turn
 * ended. The chat panel derives a phase from the Runtime-owned turn it
 * observes (never from wall-clock guesses), the composer status line and the
 * activity strip render it, and each assistant reply carries its outcome.
 *
 * Phases are live states; outcomes are terminal facts about one turn. A lost
 * connection is a phase (`reconnecting`), never an outcome: only a terminal
 * frame or the persisted log settles a turn, and a turn the log cannot settle
 * ends as `unknown`.
 */
export type TurnPhase = 'idle' | 'preparing' | 'working' | 'waiting' | 'reconnecting' | 'stopping';
export type TurnOutcome = 'completed' | 'interrupted' | 'failed' | 'unknown';

export const TURN_PHASES: readonly TurnPhase[] = ['idle', 'preparing', 'working', 'waiting', 'reconnecting', 'stopping'];

export function turnPhaseLabel(phase: TurnPhase): string {
  switch (phase) {
    case 'preparing': return 'Preparing';
    case 'working': return 'Working';
    case 'waiting': return 'Waiting for you';
    case 'reconnecting': return 'Reconnecting';
    case 'stopping': return 'Stopping';
    default: return 'Idle';
  }
}

export function turnOutcomeLabel(outcome: TurnOutcome): string {
  switch (outcome) {
    case 'completed': return 'Completed';
    case 'interrupted': return 'Stopped';
    case 'failed': return 'Failed';
    default: return 'Outcome unknown';
  }
}

/** Longer explanation for the outcome chip's tooltip and accessible description. */
export function turnOutcomeDescription(outcome: TurnOutcome): string {
  switch (outcome) {
    case 'completed': return 'The Runtime reported this turn complete.';
    case 'interrupted': return 'This turn was stopped before it finished. Nothing was re-sent.';
    case 'failed': return 'The Runtime reported this turn failed. Your message was kept in the composer, not re-sent.';
    default: return 'The connection to the Runtime was lost and its record does not show how this turn ended. Reopen the chat to check; nothing was re-sent.';
  }
}

/**
 * The composer status line. `detail` is the Runtime's own step text
 * ("Creating session…", "Running turn…"); a reconnect attempt count is shown
 * so a long outage reads as one, not as progress.
 */
export function turnPhaseStatusLine(phase: TurnPhase, input: { detail?: string | null; reconnectAttempt?: number; pendingRequests?: number } = {}): string | null {
  switch (phase) {
    case 'idle': return null;
    case 'preparing': return input.detail?.trim() || 'Preparing the turn…';
    case 'working': return input.detail?.trim() || 'Working…';
    case 'waiting': return input.pendingRequests && input.pendingRequests > 1
      ? `Waiting for you: ${input.pendingRequests} requests need an answer.`
      : 'Waiting for you: the agent needs an answer before it can continue.';
    case 'reconnecting': return input.reconnectAttempt && input.reconnectAttempt > 1
      ? `Reconnecting to the running turn (attempt ${input.reconnectAttempt})…`
      : 'Reconnecting to the running turn…';
    case 'stopping': return 'Stopping the turn…';
  }
}

/** Shown while a turn is live so the reader knows what closing the window does. */
export const TURN_CONTINUATION_NOTE = 'Runs in Chirality’s runtime. Closing this window keeps it running; quitting Chirality stops it.';

export function isLiveTurnPhase(phase: TurnPhase): boolean {
  return phase !== 'idle';
}

/** Preserve Runtime's recorded interruption cause in live and replay views. */
export function interruptedTurnPresentation(reason: unknown): { outcome: TurnOutcome; message: string } {
  if (reason === 'service-shutdown') return { outcome: 'failed', message: 'Chirality’s runtime stopped before this turn finished. Nothing was re-sent.' };
  if (reason === 'service-restart') return { outcome: 'unknown', message: 'Chirality’s runtime restarted without recording how this turn ended. Nothing was re-sent.' };
  return { outcome: 'interrupted', message: 'Turn interrupted by operator.' };
}
