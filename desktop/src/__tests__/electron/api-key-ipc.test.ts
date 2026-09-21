import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => {
  const handlers = new Map<string, (...args: unknown[]) => Promise<unknown>>();
  const ipcMain = {
    handle: vi.fn((channel: string, handler: (...args: unknown[]) => Promise<unknown>) => {
      handlers.set(channel, handler);
    }),
    removeHandler: vi.fn((channel: string) => {
      handlers.delete(channel);
    })
  };

  return {
    handlers,
    ipcMain,
    isProviderCredentialId: vi.fn((value: unknown) => value === 'anthropic' || value === 'omlx'),
    credentialStatus: vi.fn<(providerId: 'anthropic' | 'omlx') => Promise<unknown>>(),
    removeCredential: vi.fn<(providerId: 'anthropic' | 'omlx') => Promise<{ configured: boolean }>>(),
    storeCredential: vi.fn<
      (providerId: 'anthropic' | 'omlx', key: string) => Promise<{ configured: boolean }>
    >()
  };
});

vi.mock('electron', () => ({
  ipcMain: mocks.ipcMain
}));

vi.mock('../../../electron/api-key-storage', () => ({
  isProviderCredentialId: mocks.isProviderCredentialId
}));

import {
  API_KEY_REMOVE_CHANNEL,
  API_KEY_STATUS_CHANNEL,
  API_KEY_STORE_CHANNEL,
  CREDENTIAL_IPC_DENIED_EVENT,
  PROVIDER_API_KEY_REMOVE_CHANNEL,
  PROVIDER_API_KEY_STATUS_CHANNEL,
  PROVIDER_API_KEY_STORE_CHANNEL,
  registerApiKeyHandlers,
  unregisterApiKeyHandlers
} from '../../../electron/api-key-ipc';

function getHandler(channel: string): (...args: unknown[]) => Promise<unknown> {
  const handler = mocks.handlers.get(channel);
  if (!handler) {
    throw new Error(`Missing handler for ${channel}`);
  }
  return handler;
}

const credentialClient = {
  credentialStatus: mocks.credentialStatus,
  removeCredential: mocks.removeCredential,
  storeCredential: mocks.storeCredential
};

const RENDERER_ORIGIN = 'http://127.0.0.1:3000';
const trusted = { senderFrame: { url: 'http://127.0.0.1:3000/settings' } };
const foreign = { senderFrame: { url: 'https://attacker.example/' } };
const log = vi.fn<(level: 'info' | 'warn' | 'error', event: string, detail?: unknown) => void>();

function register(): void {
  registerApiKeyHandlers(credentialClient, { rendererOrigin: RENDERER_ORIGIN, log });
}

beforeEach(() => {
  mocks.handlers.clear();
  vi.clearAllMocks();
  mocks.credentialStatus.mockResolvedValue({ configured: false, source: 'none', storage: 'missing' });
  mocks.removeCredential.mockResolvedValue({ configured: false });
  mocks.storeCredential.mockResolvedValue({ configured: true });
  delete process.env.ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_OMLX_API_KEY;
});

afterEach(() => {
  delete process.env.ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
  delete process.env.CHIRALITY_OMLX_API_KEY;
});

describe('electron/api-key-ipc', () => {
  it('registers all API key handlers and unregisters previous handlers first', () => {
    register();

    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(API_KEY_STORE_CHANNEL);
    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(API_KEY_REMOVE_CHANNEL);
    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(API_KEY_STATUS_CHANNEL);
    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(PROVIDER_API_KEY_STORE_CHANNEL);
    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(PROVIDER_API_KEY_REMOVE_CHANNEL);
    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(PROVIDER_API_KEY_STATUS_CHANNEL);
    expect(mocks.handlers.has(API_KEY_STORE_CHANNEL)).toBe(true);
    expect(mocks.handlers.has(API_KEY_REMOVE_CHANNEL)).toBe(true);
    expect(mocks.handlers.has(API_KEY_STATUS_CHANNEL)).toBe(true);
    expect(mocks.handlers.has(PROVIDER_API_KEY_STORE_CHANNEL)).toBe(true);
    expect(mocks.handlers.has(PROVIDER_API_KEY_REMOVE_CHANNEL)).toBe(true);
    expect(mocks.handlers.has(PROVIDER_API_KEY_STATUS_CHANNEL)).toBe(true);
    expect(mocks.handlers.size).toBe(6);
  });

  it('trims and stores key material through the store channel', async () => {
    register();
    const handler = getHandler(API_KEY_STORE_CHANNEL);

    const result = await handler(trusted, '  sk-ant-test-key  ');

    expect(mocks.storeCredential).toHaveBeenCalledWith('anthropic', 'sk-ant-test-key');
    expect(result).toEqual({ ok: true });
  });

  it('rejects empty values on the store channel', async () => {
    register();
    const handler = getHandler(API_KEY_STORE_CHANNEL);

    const result = await handler(trusted, '   ');

    expect(mocks.storeCredential).not.toHaveBeenCalled();
    expect(result).toEqual({ ok: false, error: 'Key must be a non-empty string' });
  });

  it('consumes the daemon-owned source when UI and environment credentials coexist', async () => {
    register();
    const handler = getHandler(API_KEY_STATUS_CHANNEL);

    process.env.ANTHROPIC_API_KEY = 'canonical-environment-key';
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'compatibility-environment-key';
    mocks.credentialStatus.mockResolvedValue({ configured: true, source: 'ui', storage: 'available' });

    await expect(handler(trusted)).resolves.toEqual({
      hasKey: true,
      encryptionAvailable: true,
      source: 'ui',
      storage: 'available'
    });
  });

  it.each([
    {
      caseName: 'canonical environment credential',
      environment: { ANTHROPIC_API_KEY: 'canonical-environment-key' },
      status: { configured: true, source: 'env', storage: 'missing' }
    },
    {
      caseName: 'compatibility-alias environment credential',
      environment: { CHIRALITY_ANTHROPIC_API_KEY: 'compatibility-environment-key' },
      status: { configured: true, source: 'env', storage: 'missing' }
    },
    {
      caseName: 'no credential',
      environment: {},
      status: { configured: false, source: 'none', storage: 'missing' }
    }
  ])('reports $caseName from the daemon status', async ({ environment, status }) => {
    register();
    const handler = getHandler(API_KEY_STATUS_CHANNEL);
    Object.assign(process.env, environment);
    mocks.credentialStatus.mockResolvedValue(status);

    await expect(handler(trusted)).resolves.toEqual({
      hasKey: status.configured,
      encryptionAvailable: true,
      source: status.source,
      storage: status.storage
    });
  });

  it.each([
    { configured: true },
    { configured: true, source: 'other' },
    { configured: true, source: 'none' },
    { configured: false, source: 'ui' }
  ])('fails closed for an invalid daemon status %#', async (status) => {
    register();
    const handler = getHandler(API_KEY_STATUS_CHANNEL);
    process.env.ANTHROPIC_API_KEY = 'must-not-be-inferred-or-disclosed';
    mocks.credentialStatus.mockResolvedValue({
      ...status,
      credential: 'must-not-be-returned'
    });

    const result = await handler(trusted);

    expect(result).toEqual({
      hasKey: false,
      encryptionAvailable: false,
      source: 'none',
      error: 'Runtime daemon returned an invalid credential status'
    });
    expect(JSON.stringify(result)).not.toContain('must-not');
  });

  it('handles remove channel failures without throwing', async () => {
    register();
    const handler = getHandler(API_KEY_REMOVE_CHANNEL);
    mocks.removeCredential.mockRejectedValue(new Error('remove-failed'));

    await expect(handler(trusted)).resolves.toEqual({ ok: false, error: 'remove-failed' });
  });

  it('stores, reports, and removes an isolated oMLX credential', async () => {
    register();

    await expect(getHandler(PROVIDER_API_KEY_STORE_CHANNEL)(trusted, 'omlx', '  local-secret  '))
      .resolves.toEqual({ ok: true });
    expect(mocks.storeCredential).toHaveBeenCalledWith('omlx', 'local-secret');

    mocks.credentialStatus.mockResolvedValueOnce({ configured: true, source: 'ui', storage: 'available' });
    await expect(getHandler(PROVIDER_API_KEY_STATUS_CHANNEL)(trusted, 'omlx')).resolves.toEqual({
      hasKey: true,
      encryptionAvailable: true,
      source: 'ui',
      storage: 'available'
    });

    await expect(getHandler(PROVIDER_API_KEY_REMOVE_CHANNEL)(trusted, 'omlx')).resolves.toEqual({
      ok: true
    });
    expect(mocks.removeCredential).toHaveBeenCalledWith('omlx');
  });

  it('consumes the daemon-owned oMLX source and rejects unknown providers', async () => {
    register();
    process.env.ANTHROPIC_API_KEY = 'anthropic-only';
    process.env.CHIRALITY_OMLX_API_KEY = 'omlx-environment-key';

    await expect(getHandler(PROVIDER_API_KEY_STATUS_CHANNEL)(trusted, 'omlx')).resolves.toEqual({
      hasKey: false,
      encryptionAvailable: true,
      source: 'none',
      storage: 'missing'
    });

    mocks.credentialStatus.mockResolvedValue({ configured: true, source: 'env', storage: 'missing' });
    await expect(getHandler(PROVIDER_API_KEY_STATUS_CHANNEL)(trusted, 'omlx')).resolves.toEqual({
      hasKey: true,
      encryptionAvailable: true,
      source: 'env',
      storage: 'missing'
    });

    await expect(getHandler(PROVIDER_API_KEY_STATUS_CHANNEL)(trusted, 'other')).resolves.toEqual({
      ok: false,
      error: 'Unsupported credential provider'
    });
  });

  // A status query used to reject straight into the renderer whenever the daemon
  // was down: the client throws ENOENT on the operator token, which surfaced as an
  // unhandled "Error occurred in handler for ..." on every launch without a
  // running daemon. The state is reported as data instead.
  it('reports an unreachable daemon as a structured status rather than throwing', async () => {
    register();
    const failure = Object.assign(
      new Error("ENOENT: no such file or directory, open '/runtime/auth/tokens/operator.token'"),
      { code: 'ENOENT' }
    );
    mocks.credentialStatus.mockRejectedValue(failure);

    await expect(getHandler(API_KEY_STATUS_CHANNEL)(trusted)).resolves.toEqual({
      hasKey: false,
      encryptionAvailable: false,
      source: 'none',
      unavailable: true,
      error: failure.message
    });
  });

  it('reports an unreachable daemon on the provider status channel too', async () => {
    register();
    mocks.credentialStatus.mockRejectedValue(new Error('connect ENOENT control.sock'));

    await expect(
      getHandler(PROVIDER_API_KEY_STATUS_CHANNEL)(trusted, 'omlx')
    ).resolves.toMatchObject({ unavailable: true, hasKey: false, source: 'none' });
  });

  it('does not mark a real answer as unavailable', async () => {
    register();
    mocks.credentialStatus.mockResolvedValue({ configured: true, source: 'ui', storage: 'available' });

    const result = await getHandler(API_KEY_STATUS_CHANNEL)(trusted);

    expect(result).not.toHaveProperty('unavailable');
    expect(result).toMatchObject({ hasKey: true, encryptionAvailable: true, storage: 'available' });
  });

  it('still rejects an unsupported provider before consulting the daemon', async () => {
    register();
    mocks.credentialStatus.mockRejectedValue(new Error('should not be called'));

    await expect(getHandler(PROVIDER_API_KEY_STATUS_CHANNEL)(trusted, 'nope')).resolves.toEqual({
      ok: false,
      error: 'Unsupported credential provider'
    });
    expect(mocks.credentialStatus).not.toHaveBeenCalled();
  });

  it('unregisters all handlers', () => {
    register();
    unregisterApiKeyHandlers();

    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(API_KEY_STORE_CHANNEL);
    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(API_KEY_REMOVE_CHANNEL);
    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(API_KEY_STATUS_CHANNEL);
    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(PROVIDER_API_KEY_STORE_CHANNEL);
    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(PROVIDER_API_KEY_REMOVE_CHANNEL);
    expect(mocks.ipcMain.removeHandler).toHaveBeenCalledWith(PROVIDER_API_KEY_STATUS_CHANNEL);
    expect(mocks.handlers.size).toBe(0);
  });
});

/**
 * DEL-04-05-V3-01: the typed safeStorage state is projected from the daemon's
 * status verbatim, validated, and never inferred from the environment.
 */
describe('electron/api-key-ipc typed storage state', () => {
  it.each([
    { storage: 'missing', source: 'none', configured: false, encryptionAvailable: true },
    { storage: 'missing', source: 'env', configured: true, encryptionAvailable: true },
    { storage: 'storageUnavailable', source: 'none', configured: false, encryptionAvailable: false },
    { storage: 'storageUnavailable', source: 'env', configured: true, encryptionAvailable: false },
    { storage: 'decryptFailed', source: 'none', configured: false, encryptionAvailable: true },
    { storage: 'decryptFailed', source: 'env', configured: true, encryptionAvailable: true },
    { storage: 'available', source: 'ui', configured: true, encryptionAvailable: true }
  ])(
    'projects storage=$storage with source=$source',
    async ({ storage, source, configured, encryptionAvailable }) => {
      register();
      mocks.credentialStatus.mockResolvedValue({ configured, source, storage });

      await expect(getHandler(API_KEY_STATUS_CHANNEL)(trusted)).resolves.toEqual({
        hasKey: configured,
        encryptionAvailable,
        source,
        storage
      });
    }
  );

  it.each([
    { caseName: 'unknown storage value', status: { configured: false, source: 'none', storage: 'corrupt' } },
    { caseName: 'non-string storage value', status: { configured: false, source: 'none', storage: 4 } },
    { caseName: 'available without ui source', status: { configured: true, source: 'env', storage: 'available' } },
    { caseName: 'ui source without available storage', status: { configured: true, source: 'ui', storage: 'decryptFailed' } },
    { caseName: 'ui source with storage unavailable', status: { configured: true, source: 'ui', storage: 'storageUnavailable' } }
  ])('fails closed on $caseName', async ({ status }) => {
    register();
    mocks.credentialStatus.mockResolvedValue({ ...status, credential: 'must-not-be-returned' });

    const result = await getHandler(API_KEY_STATUS_CHANNEL)(trusted);

    expect(result).toEqual({
      hasKey: false,
      encryptionAvailable: false,
      source: 'none',
      error: 'Runtime daemon returned an invalid credential status'
    });
    expect(JSON.stringify(result)).not.toContain('must-not');
  });

  it('maps a pre-typed-state daemon answer to only what that daemon could distinguish', async () => {
    register();
    const handler = getHandler(API_KEY_STATUS_CHANNEL);

    // A `ui` source is by construction a decryptable stored blob.
    mocks.credentialStatus.mockResolvedValueOnce({ configured: true, source: 'ui' });
    await expect(handler(trusted)).resolves.toEqual({
      hasKey: true,
      encryptionAvailable: true,
      source: 'ui',
      storage: 'available'
    });

    // Anything else is left unknown: such a daemon cannot tell `missing` from
    // `decryptFailed` or `storageUnavailable`, so no state is asserted (the
    // basis shape, which the panel renders as `unknown`).
    mocks.credentialStatus.mockResolvedValueOnce({ configured: true, source: 'env' });
    const envResult = await handler(trusted);
    expect(envResult).toEqual({ hasKey: true, encryptionAvailable: true, source: 'env' });
    expect(envResult).not.toHaveProperty('storage');

    mocks.credentialStatus.mockResolvedValueOnce({ configured: false, source: 'none' });
    const noneResult = await handler(trusted);
    expect(noneResult).toEqual({ hasKey: false, encryptionAvailable: true, source: 'none' });
    expect(noneResult).not.toHaveProperty('storage');
  });
});

/**
 * DEL-09-06-V3-01: every one of the six credential channels rejects a sender
 * outside the configured renderer origin — before touching the daemon, without
 * throwing, without key material, and with a desktop-log line that carries the
 * channel and the sender origin only.
 */
describe('electron/api-key-ipc sender authorization', () => {
  const SECRET = 'sk-ant-must-never-appear';

  const channels: Array<{
    channel: string;
    args: unknown[];
    daemonCall: () => ReturnType<typeof vi.fn>;
    authorized: unknown;
    denied: unknown;
  }> = [
    {
      channel: API_KEY_STORE_CHANNEL,
      args: [SECRET],
      daemonCall: () => mocks.storeCredential,
      authorized: { ok: true },
      denied: { ok: false, error: 'Credential request was denied' }
    },
    {
      channel: API_KEY_REMOVE_CHANNEL,
      args: [],
      daemonCall: () => mocks.removeCredential,
      authorized: { ok: true },
      denied: { ok: false, error: 'Credential request was denied' }
    },
    {
      channel: API_KEY_STATUS_CHANNEL,
      args: [],
      daemonCall: () => mocks.credentialStatus,
      authorized: { hasKey: false, encryptionAvailable: true, source: 'none', storage: 'missing' },
      denied: {
        hasKey: false,
        encryptionAvailable: false,
        source: 'none',
        error: 'Credential request was denied'
      }
    },
    {
      channel: PROVIDER_API_KEY_STORE_CHANNEL,
      args: ['omlx', SECRET],
      daemonCall: () => mocks.storeCredential,
      authorized: { ok: true },
      denied: { ok: false, error: 'Credential request was denied' }
    },
    {
      channel: PROVIDER_API_KEY_REMOVE_CHANNEL,
      args: ['omlx'],
      daemonCall: () => mocks.removeCredential,
      authorized: { ok: true },
      denied: { ok: false, error: 'Credential request was denied' }
    },
    {
      channel: PROVIDER_API_KEY_STATUS_CHANNEL,
      args: ['omlx'],
      daemonCall: () => mocks.credentialStatus,
      authorized: { hasKey: false, encryptionAvailable: true, source: 'none', storage: 'missing' },
      denied: {
        hasKey: false,
        encryptionAvailable: false,
        source: 'none',
        error: 'Credential request was denied'
      }
    }
  ];

  it.each(channels)('$channel honours the configured renderer origin', async (entry) => {
    register();
    const handler = getHandler(entry.channel);

    await expect(handler(trusted, ...entry.args)).resolves.toEqual(entry.authorized);
    expect(entry.daemonCall()).toHaveBeenCalledTimes(1);
    expect(log).not.toHaveBeenCalled();
  });

  it.each(channels)('$channel rejects a foreign origin before reaching the daemon', async (entry) => {
    register();
    const handler = getHandler(entry.channel);

    const result = await handler(foreign, ...entry.args);

    expect(result).toEqual(entry.denied);
    expect(entry.daemonCall()).not.toHaveBeenCalled();
    expect(JSON.stringify(result)).not.toContain(SECRET);
    expect(log).toHaveBeenCalledTimes(1);
    expect(log).toHaveBeenCalledWith('warn', CREDENTIAL_IPC_DENIED_EVENT, {
      channel: entry.channel,
      sender: 'https://attacker.example'
    });
    expect(JSON.stringify(log.mock.calls)).not.toContain(SECRET);
  });

  it.each(channels)('$channel rejects a request with no sender frame', async (entry) => {
    register();

    await expect(getHandler(entry.channel)({}, ...entry.args)).resolves.toEqual(entry.denied);
    expect(entry.daemonCall()).not.toHaveBeenCalled();
    expect(log).toHaveBeenCalledWith('warn', CREDENTIAL_IPC_DENIED_EVENT, {
      channel: entry.channel,
      sender: 'no-sender-frame'
    });
  });

  it.each(channels)('$channel rejects a same-host different-port sender', async (entry) => {
    register();

    await expect(
      getHandler(entry.channel)({ senderFrame: { url: 'http://127.0.0.1:3001/' } }, ...entry.args)
    ).resolves.toEqual(entry.denied);
    expect(entry.daemonCall()).not.toHaveBeenCalled();
  });

  it('checks the sender before validating the provider or key arguments', async () => {
    register();

    await expect(getHandler(PROVIDER_API_KEY_STORE_CHANNEL)(foreign, 'nope', '')).resolves.toEqual({
      ok: false,
      error: 'Credential request was denied'
    });
    await expect(getHandler(API_KEY_STORE_CHANNEL)(foreign, '')).resolves.toEqual({
      ok: false,
      error: 'Credential request was denied'
    });
    expect(mocks.isProviderCredentialId).not.toHaveBeenCalled();
  });

  it('denies without a log sink as well', async () => {
    registerApiKeyHandlers(credentialClient, { rendererOrigin: RENDERER_ORIGIN });

    await expect(getHandler(API_KEY_STATUS_CHANNEL)(foreign)).resolves.toMatchObject({
      error: 'Credential request was denied'
    });
    expect(mocks.credentialStatus).not.toHaveBeenCalled();
  });
});
