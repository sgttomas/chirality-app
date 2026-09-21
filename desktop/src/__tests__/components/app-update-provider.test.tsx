import React, { useEffect } from 'react';
import renderer, { act, type ReactTestRenderer } from 'react-test-renderer';
import { afterEach, describe, expect, it, vi } from 'vitest';
import {
  AppUpdateProvider,
  isAppUpdateState,
  useAppUpdate,
  type AppUpdateContextValue,
  type AppUpdateState
} from '../../components/shell/app-update-provider';

/**
 * Conventions follow `shell-frame-runtime-connectivity.test.tsx`: node
 * environment, react-test-renderer, a fake desktop bridge assigned onto
 * `globalThis.window`, no DOM and no CSS. The provider is exercised through a
 * probe component that records every context value it observes.
 */

function state(overrides: Partial<AppUpdateState> = {}): AppUpdateState {
  return {
    currentVersion: '3.0.0-rc.1',
    status: 'idle',
    releaseSource: { configured: false, description: 'No release source is configured for this build.' },
    ...overrides
  };
}

type BridgeHarness = {
  push: (next: AppUpdateState) => void;
  showAbout: () => void;
  get: ReturnType<typeof vi.fn>;
  check: ReturnType<typeof vi.fn>;
  openDownload: ReturnType<typeof vi.fn>;
  listenerCount: () => number;
  aboutListenerCount: () => number;
  unsubscribeCalls: () => number;
};

function installBridge(initial: AppUpdateState | null): BridgeHarness {
  const listeners = new Set<(value: AppUpdateState) => void>();
  const aboutListeners = new Set<() => void>();
  let unsubscribeCalls = 0;
  const get = vi.fn(async () => initial);
  const check = vi.fn(async () => state({ status: 'failed', checkedAt: '2026-09-12T10:00:00.000Z', failure: { code: 'no-release-source', message: 'No release source is configured for this build.' } }));
  const openDownload = vi.fn(async () => ({ ok: false, error: 'No update download is available to open.' }));
  Object.assign(globalThis, {
    window: {
      chirality: {
        appUpdate: {
          get,
          check,
          openDownload,
          subscribe: (listener: (value: AppUpdateState) => void) => {
            listeners.add(listener);
            return () => { unsubscribeCalls += 1; listeners.delete(listener); };
          },
          onShowAbout: (listener: () => void) => {
            aboutListeners.add(listener);
            return () => { unsubscribeCalls += 1; aboutListeners.delete(listener); };
          }
        }
      }
    }
  });
  return {
    push: (next) => { for (const listener of listeners) listener(next); },
    showAbout: () => { for (const listener of aboutListeners) listener(); },
    get,
    check,
    openDownload,
    listenerCount: () => listeners.size,
    aboutListenerCount: () => aboutListeners.size,
    unsubscribeCalls: () => unsubscribeCalls
  };
}

function removeWindow(): void {
  delete (globalThis as { window?: unknown }).window;
}

const observed: AppUpdateContextValue[] = [];
let latest: AppUpdateContextValue | null = null;

function Probe(): null {
  const value = useAppUpdate();
  useEffect(() => { observed.push(value); latest = value; });
  return null;
}

async function mount(): Promise<ReactTestRenderer> {
  let tree: ReactTestRenderer | undefined;
  await act(async () => {
    tree = renderer.create(<AppUpdateProvider><Probe /></AppUpdateProvider>);
  });
  // Let the hydrating get() resolve.
  await act(async () => { await Promise.resolve(); });
  return tree!;
}

afterEach(() => {
  observed.length = 0;
  latest = null;
  removeWindow();
});

describe('isAppUpdateState', () => {
  it('accepts the contract shape and rejects anything else, including a denied null', () => {
    expect(isAppUpdateState(state())).toBe(true);
    expect(isAppUpdateState(state({ status: 'update-available', available: { version: '3.0.0', downloadUrl: 'https://x.test/a' } }))).toBe(true);
    expect(isAppUpdateState(null)).toBe(false);
    expect(isAppUpdateState({})).toBe(false);
    expect(isAppUpdateState({ ...state(), status: 'installing' })).toBe(false);
    expect(isAppUpdateState({ ...state(), releaseSource: { configured: 'no', description: '' } })).toBe(false);
  });
});

describe('AppUpdateProvider', () => {
  it('reports no bridge and a null state where window.chirality.appUpdate is absent', async () => {
    Object.assign(globalThis, { window: { chirality: {} } });
    const tree = await mount();
    expect(latest).toMatchObject({ bridgeAvailable: false, state: null, aboutRequests: 0 });
    await act(async () => { await latest!.check(); await latest!.openDownload(); });
    expect(latest).toMatchObject({ bridgeAvailable: false, state: null });
    await act(async () => { tree.unmount(); });
  });

  it('falls back to the same no-bridge value without a provider', async () => {
    let tree: ReactTestRenderer | undefined;
    await act(async () => { tree = renderer.create(<Probe />); });
    expect(latest).toMatchObject({ bridgeAvailable: false, state: null, aboutRequests: 0 });
    await expect(latest!.check()).resolves.toBeUndefined();
    await act(async () => { tree!.unmount(); });
  });

  it('hydrates from get(), mirrors pushed transitions, and never lets a late hydrate overwrite a push', async () => {
    let resolveGet: ((value: AppUpdateState) => void) | undefined;
    const bridge = installBridge(null);
    bridge.get.mockImplementation(() => new Promise<AppUpdateState>((resolve) => { resolveGet = resolve; }));
    const tree = await mount();
    expect(latest).toMatchObject({ bridgeAvailable: true, state: null });
    expect(bridge.listenerCount()).toBe(1);
    expect(bridge.aboutListenerCount()).toBe(1);

    const checking = state({ status: 'checking' });
    await act(async () => { bridge.push(checking); });
    expect(latest!.state).toBe(checking);

    await act(async () => { resolveGet!(state({ status: 'idle' })); await Promise.resolve(); });
    expect(latest!.state).toBe(checking);

    await act(async () => { bridge.push({ nonsense: true } as unknown as AppUpdateState); });
    expect(latest!.state).toBe(checking);

    await act(async () => { tree.unmount(); });
    expect(bridge.listenerCount()).toBe(0);
    expect(bridge.aboutListenerCount()).toBe(0);
    expect(bridge.unsubscribeCalls()).toBe(2);
  });

  it('check() invokes the bridge and adopts the settled state; openDownload() invokes the bridge', async () => {
    const bridge = installBridge(state());
    const tree = await mount();
    expect(latest!.state).toMatchObject({ status: 'idle' });
    await act(async () => { await latest!.check(); });
    expect(bridge.check).toHaveBeenCalledTimes(1);
    expect(latest!.state).toMatchObject({ status: 'failed', failure: { code: 'no-release-source' } });

    bridge.check.mockResolvedValueOnce(null as unknown as AppUpdateState);
    await act(async () => { await latest!.check(); });
    expect(latest!.state).toMatchObject({ status: 'failed' });

    await act(async () => { await latest!.openDownload(); });
    expect(bridge.openDownload).toHaveBeenCalledTimes(1);

    bridge.openDownload.mockRejectedValueOnce(new Error('bridge gone'));
    await expect(act(async () => { await latest!.openDownload(); })).resolves.toBeUndefined();
    await act(async () => { tree.unmount(); });
  });

  it('increments aboutRequests once per About signal from the application menu', async () => {
    const bridge = installBridge(state());
    const tree = await mount();
    expect(latest!.aboutRequests).toBe(0);
    await act(async () => { bridge.showAbout(); });
    expect(latest!.aboutRequests).toBe(1);
    await act(async () => { bridge.showAbout(); bridge.showAbout(); });
    expect(latest!.aboutRequests).toBe(3);
    await act(async () => { tree.unmount(); });
    bridge.showAbout();
    expect(latest!.aboutRequests).toBe(3);
  });
});
