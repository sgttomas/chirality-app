/**
 * Pure resolution of which body state the Document sidebar view should render,
 * given the roster + content fetch flags. Kept DOM-free and side-effect-free so
 * the branch logic (including the roster/content loading states) is unit-testable
 * without a React renderer — the component is a thin map from this state to JSX.
 */

export type DocumentViewStateInput = {
  hasProjectRoot: boolean;
  rosterLoading: boolean;
  rosterError: string | null;
  deliverableCount: number;
  contentLoading: boolean;
  contentError: string | null;
  hasContent: boolean;
};

export type DocumentViewState =
  | { kind: 'no-root' }
  | { kind: 'roster-loading' }
  | { kind: 'roster-error'; message: string }
  | { kind: 'empty' }
  | { kind: 'content-loading' }
  | { kind: 'content-error'; message: string }
  | { kind: 'content' }
  | { kind: 'idle' };

export function resolveDocumentViewState(input: DocumentViewStateInput): DocumentViewState {
  if (!input.hasProjectRoot) {
    return { kind: 'no-root' };
  }
  if (input.rosterError) {
    return { kind: 'roster-error', message: input.rosterError };
  }
  // Distinguish "still scanning" from "scanned, genuinely empty" so the empty
  // message never flashes while the roster fetch is in flight.
  if (input.rosterLoading) {
    return { kind: 'roster-loading' };
  }
  if (input.deliverableCount === 0) {
    return { kind: 'empty' };
  }
  if (input.contentLoading) {
    return { kind: 'content-loading' };
  }
  if (input.contentError) {
    return { kind: 'content-error', message: input.contentError };
  }
  if (input.hasContent) {
    return { kind: 'content' };
  }
  return { kind: 'idle' };
}
