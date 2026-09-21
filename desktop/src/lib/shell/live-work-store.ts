import { useSyncExternalStore } from 'react';
import { isLiveTurnPhase, type TurnPhase } from './turn-phase';

/**
 * Whether any turn is live in this window, published by the conversation
 * shell and read by surfaces outside it (the update controls warn before the
 * user quits to install). A tiny external store: no context threading through
 * the shell frame, and no second source of truth for the phase itself.
 */
let phase: TurnPhase = 'idle';
const listeners = new Set<() => void>();

export function publishLiveTurnPhase(next: TurnPhase): void {
  if (phase === next) return;
  phase = next;
  for (const listener of listeners) listener();
}

function subscribe(listener: () => void): () => void {
  listeners.add(listener);
  return () => { listeners.delete(listener); };
}

export function readLiveTurnPhase(): TurnPhase {
  return phase;
}

export function useLiveWork(): boolean {
  return useSyncExternalStore(subscribe, () => isLiveTurnPhase(phase), () => false);
}

/** Test seam: forget the published phase. */
export function resetLiveTurnPhaseForTests(): void {
  phase = 'idle';
}
