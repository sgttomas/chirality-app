import React from 'react';
import renderer, { act, type ReactTestInstance, type ReactTestRenderer } from 'react-test-renderer';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import type { RuntimeConnectivitySnapshot } from '../../lib/shell/runtime-connectivity';

/**
 * The dialogue pane's own stale-error case. A send attempted while the daemon was
 * unreachable leaves a red banner under the composer, and the only thing that
 * ever cleared it was the operator typing again — so in the packaged app it
 * outlived the outage it described. It now clears when the runtime reconnects,
 * and only then: the prompt is not re-sent on the operator's behalf.
 */

const mocks = vi.hoisted(() => ({
  appendEvent: vi.fn(),
  bootHarnessSession: vi.fn(),
  clearEvents: vi.fn(),
  createHarnessSession: vi.fn(),
  interruptHarnessSession: vi.fn(),
  setStreaming: vi.fn(),
  streamHarnessTurn: vi.fn()
}));

vi.mock('next/navigation', () => ({
  usePathname: () => '/chat',
  useSearchParams: () => new URLSearchParams()
}));

vi.mock('../../components/workspace/workspace-provider', () => ({
  useWorkspace: () => ({ projectRoot: '/tmp/chirality-workroot' })
}));

vi.mock('../../components/workspace/toolkit-provider', () => ({
  useToolkit: () => ({ optsPayload: undefined })
}));

vi.mock('../../components/workspace/harness-events-provider', () => ({
  useHarnessEventActions: () => ({
    appendEvent: mocks.appendEvent,
    clearEvents: mocks.clearEvents,
    hydrateEvents: vi.fn(),
    setStreaming: mocks.setStreaming
  }),
  useHarnessEvents: () => ({ events: [], streaming: false })
}));

vi.mock('../../lib/harness/client', async (importOriginal) => {
  const original = await importOriginal<typeof import('../../lib/harness/client')>();
  return {
    ...original,
    bootHarnessSession: mocks.bootHarnessSession,
    createHarnessSession: mocks.createHarnessSession,
    interruptHarnessSession: mocks.interruptHarnessSession,
    streamHarnessTurn: mocks.streamHarnessTurn,
    getHarnessTurnState: vi.fn(async () => ({ active: false, lastSeq: 0 })),
    attachHarnessTurn: vi.fn(async () => undefined)
  };
});

vi.mock('../../components/shell/file-picker', () => ({
  FilePicker: () => null
}));

vi.mock('../../components/shell/permission-requests', () => ({
  PermissionRequests: () => null
}));

import { ChatPanel } from '../../components/shell/chat-panel';
import { HarnessApiClientError } from '../../lib/harness/client';
import { RuntimeConnectivityProvider } from '../../components/shell/runtime-connectivity-provider';

Object.assign(globalThis, { React });

const DAEMON_UNBOUND = 'Chirality runtime daemon client is not configured';

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

function installBridge(initial: RuntimeConnectivitySnapshot | null): {
  push: (next: RuntimeConnectivitySnapshot) => void;
} {
  const listeners = new Set<(value: RuntimeConnectivitySnapshot) => void>();
  Object.assign(globalThis, {
    window: {
      chirality: {
        runtime: {
          connectivity: {
            get: async () => initial,
            subscribe: (listener: (value: RuntimeConnectivitySnapshot) => void) => {
              listeners.add(listener);
              return () => {
                listeners.delete(listener);
              };
            }
          }
        }
      }
    }
  });
  return {
    push: (next) => {
      for (const listener of listeners) {
        listener(next);
      }
    }
  };
}

function byClass(root: ReactTestInstance, className: string): ReactTestInstance[] {
  return root.findAll((node) =>
    typeof node.props.className === 'string'
      ? node.props.className.split(/\s+/).includes(className)
      : false
  );
}

describe('ChatPanel stale runtime error across a reconnect', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    delete (globalThis as { window?: unknown }).window;
  });

  it('clears the failed-send banner when the runtime reconnects, without re-sending', async () => {
    const bridge = installBridge(snapshot({ state: 'disconnected', lastError: 'socket refused' }));
    mocks.createHarnessSession.mockRejectedValue(
      new HarnessApiClientError(503, 'ENGINE_UNAVAILABLE', DAEMON_UNBOUND)
    );

    let tree!: ReactTestRenderer;
    await act(async () => {
      tree = renderer.create(
        <RuntimeConnectivityProvider>
          <ChatPanel />
        </RuntimeConnectivityProvider>
      );
    });
    await act(async () => {});

    const input = tree.root.findByProps({ 'aria-label': 'Chat input' });
    await act(async () => {
      input.props.onChange({ target: { value: 'boot the loop' } });
    });
    await act(async () => {
      tree.root
        .findByProps({ className: 'chat-input-row' })
        .props.onSubmit({ preventDefault: vi.fn() });
    });

    const banner = byClass(tree.root, 'chat-runtime-error');
    expect(banner).toHaveLength(1);
    expect(banner[0].findAllByType('p').map((node) => node.children.join(''))).toEqual(
      expect.arrayContaining([`ENGINE_UNAVAILABLE: ${DAEMON_UNBOUND}`])
    );

    await act(async () => {
      bridge.push(snapshot({ changedAt: '2026-07-25T12:00:05.000Z' }));
    });
    await act(async () => {});

    expect(byClass(tree.root, 'chat-runtime-error')).toHaveLength(0);
    // The draft the failed send restored is still there, untouched: clearing a
    // stale explanation is not the same as retrying the operator's turn.
    expect(tree.root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe(
      'boot the loop'
    );
    expect(mocks.createHarnessSession).toHaveBeenCalledTimes(1);
    expect(mocks.streamHarnessTurn).not.toHaveBeenCalled();
  });
});
