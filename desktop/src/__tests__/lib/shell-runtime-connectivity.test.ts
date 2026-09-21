import { describe, expect, it } from 'vitest';
import {
  deriveRuntimeConnectivityPresentation,
  isRuntimeConnectivitySnapshot,
  isRuntimeReconnect,
  type RuntimeConnectivitySnapshot
} from '../../lib/shell/runtime-connectivity';

function snapshot(
  overrides: Partial<RuntimeConnectivitySnapshot> = {}
): RuntimeConnectivitySnapshot {
  return {
    state: 'connected',
    failedAttempts: 0,
    lastError: null,
    changedAt: '2026-07-25T12:00:00.000Z',
    ...overrides
  };
}

describe('isRuntimeConnectivitySnapshot', () => {
  it('accepts every valid state', () => {
    for (const state of ['connecting', 'connected', 'disconnected'] as const) {
      expect(isRuntimeConnectivitySnapshot(snapshot({ state }))).toBe(true);
    }
  });

  it('rejects payloads that are not a well-formed snapshot', () => {
    expect(isRuntimeConnectivitySnapshot(null)).toBe(false);
    expect(isRuntimeConnectivitySnapshot(undefined)).toBe(false);
    expect(isRuntimeConnectivitySnapshot('connected')).toBe(false);
    expect(isRuntimeConnectivitySnapshot({ ...snapshot(), state: 'bogus' })).toBe(false);
    expect(isRuntimeConnectivitySnapshot({ ...snapshot(), failedAttempts: '2' })).toBe(false);
    expect(isRuntimeConnectivitySnapshot({ ...snapshot(), changedAt: 12 })).toBe(false);
    expect(isRuntimeConnectivitySnapshot({ ...snapshot(), lastError: 4 })).toBe(false);
  });

  it('accepts a string failure reason', () => {
    expect(isRuntimeConnectivitySnapshot(snapshot({ lastError: 'refused' }))).toBe(true);
  });
});

describe('isRuntimeReconnect', () => {
  it('reports the moment an unreachable daemon becomes reachable', () => {
    expect(
      isRuntimeReconnect(snapshot({ state: 'disconnected' }), snapshot({ state: 'connected' }))
    ).toBe(true);
  });

  it('treats a bind that was still in flight as a reconnect once it lands', () => {
    // The observed failure: panes mounted and fetched while the first bind was
    // in flight, so their requests failed and nothing ever re-issued them.
    expect(
      isRuntimeReconnect(snapshot({ state: 'connecting' }), snapshot({ state: 'connected' }))
    ).toBe(true);
  });

  it('never treats the first observed snapshot as a reconnect', () => {
    // Nothing failed before it: whatever mounted alongside it fetched under
    // exactly this state.
    expect(isRuntimeReconnect(null, snapshot({ state: 'connected' }))).toBe(false);
    expect(isRuntimeReconnect(null, snapshot({ state: 'disconnected' }))).toBe(false);
  });

  it('ignores a repeated connected report', () => {
    expect(
      isRuntimeReconnect(
        snapshot({ state: 'connected' }),
        snapshot({ state: 'connected', changedAt: '2026-07-25T12:00:09.000Z' })
      )
    ).toBe(false);
  });

  it('ignores every transition that does not end connected', () => {
    expect(
      isRuntimeReconnect(snapshot({ state: 'connected' }), snapshot({ state: 'disconnected' }))
    ).toBe(false);
    expect(
      isRuntimeReconnect(snapshot({ state: 'disconnected' }), snapshot({ state: 'connecting' }))
    ).toBe(false);
    expect(
      isRuntimeReconnect(
        snapshot({ state: 'disconnected', failedAttempts: 1 }),
        snapshot({ state: 'disconnected', failedAttempts: 2 })
      )
    ).toBe(false);
  });
});

describe('deriveRuntimeConnectivityPresentation', () => {
  it('renders nothing when there is no snapshot to report', () => {
    // The browser/SSR case: no desktop bridge, so no runtime state may be claimed.
    expect(deriveRuntimeConnectivityPresentation(null)).toBeNull();
  });

  it('reports a connected daemon with the healthy tone', () => {
    expect(deriveRuntimeConnectivityPresentation(snapshot())).toEqual({
      tone: 'ready',
      label: 'connected',
      title: 'Runtime daemon connected'
    });
  });

  it('reports an in-progress bind with the pending tone', () => {
    expect(deriveRuntimeConnectivityPresentation(snapshot({ state: 'connecting' }))).toEqual({
      tone: 'pending',
      label: 'connecting',
      title: 'Connecting to the runtime daemon'
    });
  });

  it('reports an offline daemon and surfaces the failure reason', () => {
    const presentation = deriveRuntimeConnectivityPresentation(
      snapshot({
        state: 'disconnected',
        failedAttempts: 1,
        lastError: 'daemon socket refused'
      })
    );
    expect(presentation).toEqual({
      tone: 'error',
      label: 'offline',
      title: 'Runtime daemon unreachable: daemon socket refused'
    });
  });

  it('includes the attempt count once retrying has clearly not helped', () => {
    const presentation = deriveRuntimeConnectivityPresentation(
      snapshot({ state: 'disconnected', failedAttempts: 4, lastError: 'no such file' })
    );
    expect(presentation?.title).toBe(
      'Runtime daemon unreachable after 4 attempts: no such file'
    );
  });

  it('still explains an offline daemon when no reason was captured', () => {
    const presentation = deriveRuntimeConnectivityPresentation(
      snapshot({ state: 'disconnected', failedAttempts: 3, lastError: null })
    );
    expect(presentation?.title).toBe('Runtime daemon unreachable after 3 attempts');
    expect(presentation?.tone).toBe('error');
  });
});
