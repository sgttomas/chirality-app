import { describe, expect, it } from 'vitest';
import {
  resolveDocumentViewState,
  type DocumentViewStateInput
} from '../../lib/shell/document-view-state';

function input(overrides: Partial<DocumentViewStateInput> = {}): DocumentViewStateInput {
  return {
    hasProjectRoot: true,
    rosterLoading: false,
    rosterError: null,
    deliverableCount: 1,
    contentLoading: false,
    contentError: null,
    hasContent: false,
    ...overrides
  };
}

describe('resolveDocumentViewState', () => {
  it('reports no-root before anything else', () => {
    expect(
      resolveDocumentViewState(input({ hasProjectRoot: false, rosterError: 'x', deliverableCount: 0 }))
    ).toEqual({ kind: 'no-root' });
  });

  it('surfaces a roster error with its message', () => {
    expect(resolveDocumentViewState(input({ rosterError: 'scan failed' }))).toEqual({
      kind: 'roster-error',
      message: 'scan failed'
    });
  });

  it('shows roster-loading instead of empty while the scan is in flight', () => {
    // The flash fix: a transient deliverableCount of 0 during loading must NOT read as empty.
    expect(resolveDocumentViewState(input({ rosterLoading: true, deliverableCount: 0 }))).toEqual({
      kind: 'roster-loading'
    });
  });

  it('reports empty only once the roster has loaded with no deliverables', () => {
    expect(
      resolveDocumentViewState(input({ rosterLoading: false, deliverableCount: 0 }))
    ).toEqual({ kind: 'empty' });
  });

  it('shows content-loading when a document fetch is in flight', () => {
    expect(resolveDocumentViewState(input({ contentLoading: true }))).toEqual({
      kind: 'content-loading'
    });
  });

  it('surfaces a content error with its message', () => {
    expect(resolveDocumentViewState(input({ contentError: 'not found' }))).toEqual({
      kind: 'content-error',
      message: 'not found'
    });
  });

  it('reports content once a document is loaded', () => {
    expect(resolveDocumentViewState(input({ hasContent: true }))).toEqual({ kind: 'content' });
  });

  it('falls back to idle when a deliverable is selected but no document is chosen yet', () => {
    expect(resolveDocumentViewState(input())).toEqual({ kind: 'idle' });
  });

  it('prefers a roster error over the loading state', () => {
    expect(
      resolveDocumentViewState(input({ rosterLoading: true, rosterError: 'boom' }))
    ).toEqual({ kind: 'roster-error', message: 'boom' });
  });
});
