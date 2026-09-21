import { afterEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => {
  const handlers = new Map<string, (...args: unknown[]) => Promise<unknown>>();
  return {
    handlers,
    ipcMain: {
      handle: vi.fn((channel: string, handler: (...args: unknown[]) => Promise<unknown>) => {
        handlers.set(channel, handler);
      }),
      removeHandler: vi.fn((channel: string) => {
        handlers.delete(channel);
      })
    }
  };
});

vi.mock('electron', () => ({ ipcMain: mocks.ipcMain }));

import {
  RUNTIME_SERVICE_RESTART_CHANNEL,
  registerRuntimeControlHandlers,
  unregisterRuntimeControlHandlers
} from '../../../electron/runtime-control-ipc';
import type { RuntimeServiceState } from '../../../electron/runtime-service-host';

const rendererOrigin = 'http://127.0.0.1:43110';
const authorized = { senderFrame: { url: `${rendererOrigin}/chat` } };
const foreign = { senderFrame: { url: 'https://example.invalid/chat' } };

const readyState: RuntimeServiceState = {
  status: 'ready',
  pid: 4242,
  socketPath: '/u/runtime/control.sock',
  clientTokenFile: '/u/runtime/client-token',
  restarts: 1,
  recentFailures: 0,
  lastExit: null,
  lastError: null,
  nextRestartAt: null,
  changedAt: '2026-09-12T00:00:00.000Z'
};

afterEach(() => {
  unregisterRuntimeControlHandlers();
  mocks.handlers.clear();
  vi.clearAllMocks();
});

describe('runtime control IPC', () => {
  it('exposes only the service restart channel', () => {
    registerRuntimeControlHandlers({ rendererOrigin, restartService: async () => readyState });
    expect([...mocks.handlers.keys()]).toEqual([RUNTIME_SERVICE_RESTART_CHANNEL]);
    expect(RUNTIME_SERVICE_RESTART_CHANNEL).toBe('chirality:runtime-service-restart');
  });

  it('relaunches the owned service for the renderer origin and returns its state', async () => {
    const restartService = vi.fn(async () => readyState);
    registerRuntimeControlHandlers({ rendererOrigin, restartService });
    const handler = mocks.handlers.get(RUNTIME_SERVICE_RESTART_CHANNEL)!;
    await expect(handler(authorized)).resolves.toEqual({ ok: true, service: readyState });
    expect(restartService).toHaveBeenCalledTimes(1);
  });

  it('denies foreign senders before touching the service', async () => {
    const restartService = vi.fn(async () => readyState);
    registerRuntimeControlHandlers({ rendererOrigin, restartService });
    const handler = mocks.handlers.get(RUNTIME_SERVICE_RESTART_CHANNEL)!;
    await expect(handler(foreign)).resolves.toEqual({ ok: false, error: 'Runtime control request was denied' });
    await expect(handler({})).resolves.toEqual({ ok: false, error: 'Runtime control request was denied' });
    expect(restartService).not.toHaveBeenCalled();
  });

  it('reports a failed relaunch without secrets', async () => {
    registerRuntimeControlHandlers({
      rendererOrigin,
      restartService: async () => {
        throw new Error('spawn failed with token abc123 attached');
      }
    });
    const handler = mocks.handlers.get(RUNTIME_SERVICE_RESTART_CHANNEL)!;
    await expect(handler(authorized)).resolves.toEqual({ ok: false, error: 'spawn failed with [redacted] attached' });
  });

  it('unregisters the channel on teardown', () => {
    registerRuntimeControlHandlers({ rendererOrigin, restartService: async () => readyState });
    unregisterRuntimeControlHandlers();
    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(RUNTIME_SERVICE_RESTART_CHANNEL);
    expect(mocks.handlers.size).toBe(0);
  });
});
