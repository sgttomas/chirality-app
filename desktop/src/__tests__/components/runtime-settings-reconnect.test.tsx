import React from 'react';
import renderer, { act, type ReactTestRenderer } from 'react-test-renderer';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import type { RuntimeConnectivitySnapshot } from '../../lib/shell/runtime-connectivity';
import { RuntimeConnectivityProvider } from '../../components/shell/runtime-connectivity-provider';
import { useRuntimeSettingsController, type RuntimeSettingsViewProps } from '../../components/settings/runtime-settings-controller';
import { RuntimeSettings } from '../../components/settings/runtime-settings';

/**
 * The local-model panel's content is a claim about the Runtime. Probed once at
 * mount, that claim would freeze for the rest of the session; it is re-probed
 * when the main process reports the Runtime is reachable again. The retired
 * `runtime.daemon` lifecycle IPC is never consulted.
 */

Object.assign(globalThis, { React });

const modelStatus = vi.fn();

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
  daemonAccessed: () => boolean;
} {
  const listeners = new Set<(value: RuntimeConnectivitySnapshot) => void>();
  let daemonAccessed = false;
  const runtime = {
    models: { status: modelStatus, activate: vi.fn() },
    connectivity: {
      get: async () => initial,
      subscribe: (listener: (value: RuntimeConnectivitySnapshot) => void) => {
        listeners.add(listener);
        return () => {
          listeners.delete(listener);
        };
      }
    }
  };
  Object.defineProperty(runtime, 'daemon', { get() { daemonAccessed = true; return undefined; } });
  Object.assign(globalThis, { window: { chirality: { runtime } } });
  return {
    push: (next) => {
      for (const listener of listeners) {
        listener(next);
      }
    },
    daemonAccessed: () => daemonAccessed
  };
}

describe('RuntimeSettings re-probe on runtime reconnect', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    delete (globalThis as { window?: unknown }).window;
  });

  it('re-probes local models exactly once per reconnect and never touches the retired daemon IPC', async () => {
    const bridge = installBridge(snapshot({ state: 'disconnected' }));
    modelStatus.mockResolvedValue({
      ok: true,
      residency: { phase: 'NO_MODEL', activeTurns: 0, acceptingLocalTurns: true, models: [] }
    });

    let tree!: ReactTestRenderer;
    await act(async () => {
      tree = renderer.create(
        <RuntimeConnectivityProvider>
          <RuntimeSettings />
        </RuntimeConnectivityProvider>
      );
    });
    await act(async () => {});
    expect(modelStatus).toHaveBeenCalledTimes(1);

    await act(async () => {
      bridge.push(snapshot({ changedAt: '2026-07-25T12:00:05.000Z' }));
    });
    await act(async () => {});
    expect(modelStatus).toHaveBeenCalledTimes(2);

    // A repeated connected report is not a transition.
    await act(async () => {
      bridge.push(snapshot({ changedAt: '2026-07-25T12:00:15.000Z' }));
    });
    await act(async () => {});
    expect(modelStatus).toHaveBeenCalledTimes(2);
    expect(bridge.daemonAccessed()).toBe(false);

    tree.unmount();
  });
});

it('does not probe or activate local models for the hosted Codex shell, including refresh', async () => {
  vi.clearAllMocks();
  const bridge = installBridge(snapshot());
  const models = (window as unknown as { chirality: { runtime: { models: { activate: ReturnType<typeof vi.fn> } } } }).chirality.runtime.models;
  let controller!: RuntimeSettingsViewProps;
  function HostedController() { controller = useRuntimeSettingsController({ localModels: false }); return null; }
  let tree!: ReactTestRenderer;
  await act(async () => { tree = renderer.create(<HostedController />); });
  await act(async () => { controller.onRefresh(); });
  await act(async () => { controller.onSelectedModelChange('irrelevant-model'); });
  await act(async () => { controller.onActivateModel(); });
  expect(modelStatus).not.toHaveBeenCalled();
  expect(models.activate).not.toHaveBeenCalled();
  expect(controller.error).toBeNull();
  expect(controller.bridgeAvailable).toBe(true);
  expect(bridge.daemonAccessed()).toBe(false);
  act(() => tree.unmount());
  delete (globalThis as { window?: unknown }).window;
});
