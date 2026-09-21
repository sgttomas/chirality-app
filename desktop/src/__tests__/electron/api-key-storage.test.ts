import { createHash } from 'node:crypto';
import { chmod, mkdtemp, mkdir, readFile, rm, stat, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

const electronMock = vi.hoisted(() => ({
  app: {
    getPath: vi.fn<(name: string) => string>()
  },
  safeStorage: {
    isEncryptionAvailable: vi.fn<() => boolean>(),
    encryptString: vi.fn<(value: string) => Buffer>(),
    decryptString: vi.fn<(value: Buffer) => string>()
  }
}));

vi.mock('electron', () => ({
  app: electronMock.app,
  safeStorage: electronMock.safeStorage
}));

import {
  SafeStorageCredentialStore,
  getProviderUiApiKey,
  getUiApiKey,
  hasStoredProviderApiKey,
  hasStoredApiKey,
  loadStoredKeyIntoGlobal,
  probeProviderCredentialStorage,
  readProviderCredential,
  removeProviderApiKey,
  removeApiKey,
  retrieveProviderApiKey,
  retrieveApiKey,
  storeProviderApiKey,
  storeApiKey
} from '../../../electron/api-key-storage';

const GLOBAL_KEY = '__CHIRALITY_UI_API_KEY__';
const PROVIDER_GLOBAL_KEY = '__CHIRALITY_PROVIDER_API_KEYS__';
const globalState = globalThis as unknown as Record<string, unknown>;

function getStoragePath(tmpDir: string): string {
  return path.join(tmpDir, 'credentials', 'api-key.enc');
}

let tmpDir = '';

beforeEach(async () => {
  tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-api-key-storage-'));
  electronMock.app.getPath.mockReturnValue(tmpDir);
  electronMock.safeStorage.isEncryptionAvailable.mockReturnValue(true);
  electronMock.safeStorage.encryptString.mockImplementation((value: string) =>
    Buffer.from(`enc:${value}`, 'utf8')
  );
  electronMock.safeStorage.decryptString.mockImplementation((value: Buffer) => {
    const raw = value.toString('utf8');
    if (!raw.startsWith('enc:')) {
      throw new Error('corrupted');
    }
    return raw.slice(4);
  });
});

afterEach(async () => {
  delete globalState[GLOBAL_KEY];
  delete globalState[PROVIDER_GLOBAL_KEY];
  vi.clearAllMocks();
  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
});

describe('electron/api-key-storage', () => {
  it('provides the daemon credential port while preserving provider isolation', async () => {
    const credentials = new SafeStorageCredentialStore();
    await credentials.set('anthropic', 'daemon-anthropic');
    await credentials.set('omlx', 'daemon-omlx');

    await expect(credentials.get('anthropic')).resolves.toBe('daemon-anthropic');
    await expect(credentials.get('omlx')).resolves.toBe('daemon-omlx');
    await expect(credentials.status('omlx')).resolves.toEqual({
      configured: true,
      source: 'ui',
      storage: 'available'
    });

    await credentials.remove('omlx');
    await expect(credentials.status('omlx')).resolves.toEqual({
      configured: false,
      source: 'none',
      storage: 'missing'
    });
    await expect(credentials.get('anthropic')).resolves.toBe('daemon-anthropic');
  });

  it('stores encrypted key material outside projectRoot and updates process global', async () => {
    await storeApiKey('ui-key-123');

    const stored = await readFile(getStoragePath(tmpDir), 'utf8');
    expect(stored).toBe('enc:ui-key-123');
    expect(getUiApiKey()).toBe('ui-key-123');
    await expect(hasStoredApiKey()).resolves.toBe(true);
  });

  it('keeps the legacy Anthropic blob while isolating provider blobs and globals', async () => {
    await storeProviderApiKey('anthropic', 'anthropic-secret');
    await storeProviderApiKey('omlx', 'omlx-secret');

    await expect(readFile(getStoragePath(tmpDir), 'utf8')).resolves.toBe('enc:anthropic-secret');
    await expect(
      readFile(path.join(tmpDir, 'credentials', 'api-key.omlx.enc'), 'utf8')
    ).resolves.toBe('enc:omlx-secret');
    expect(getUiApiKey()).toBe('anthropic-secret');
    expect(getProviderUiApiKey('omlx')).toBe('omlx-secret');

    await removeProviderApiKey('omlx');
    expect(getProviderUiApiKey('omlx')).toBeUndefined();
    expect(getUiApiKey()).toBe('anthropic-secret');
    await expect(hasStoredProviderApiKey('omlx')).resolves.toBe(false);
    await expect(retrieveProviderApiKey('anthropic')).resolves.toBe('anthropic-secret');
  });

  it('loads stored key into process global during startup', async () => {
    const storagePath = getStoragePath(tmpDir);
    await mkdir(path.dirname(storagePath), { recursive: true });
    await writeFile(storagePath, Buffer.from('enc:boot-key', 'utf8'));

    await loadStoredKeyIntoGlobal();

    expect(getUiApiKey()).toBe('boot-key');
    await expect(retrieveApiKey()).resolves.toBe('boot-key');
  });

  it('rehydrates a persisted Anthropic credential for a restarted daemon process', async () => {
    const storagePath = getStoragePath(tmpDir);
    await mkdir(path.dirname(storagePath), { recursive: true });
    await writeFile(storagePath, Buffer.from('enc:daemon-restart-key', 'utf8'));
    delete globalState[GLOBAL_KEY];
    delete globalState[PROVIDER_GLOBAL_KEY];

    const credentials = new SafeStorageCredentialStore();
    await expect(credentials.get('anthropic')).resolves.toBe('daemon-restart-key');

    expect(getUiApiKey()).toBe('daemon-restart-key');
    expect(getProviderUiApiKey('omlx')).toBeUndefined();
  });

  it('loads both legacy Anthropic and oMLX blobs during startup', async () => {
    const anthropicPath = getStoragePath(tmpDir);
    const omlxPath = path.join(tmpDir, 'credentials', 'api-key.omlx.enc');
    await mkdir(path.dirname(anthropicPath), { recursive: true });
    await writeFile(anthropicPath, Buffer.from('enc:anthropic-boot', 'utf8'));
    await writeFile(omlxPath, Buffer.from('enc:omlx-boot', 'utf8'));

    await loadStoredKeyIntoGlobal();

    expect(getUiApiKey()).toBe('anthropic-boot');
    expect(getProviderUiApiKey('omlx')).toBe('omlx-boot');
  });

  it('returns null when decrypt fails and does not throw', async () => {
    const storagePath = getStoragePath(tmpDir);
    await mkdir(path.dirname(storagePath), { recursive: true });
    await writeFile(storagePath, Buffer.from('invalid', 'utf8'));
    electronMock.safeStorage.decryptString.mockImplementation(() => {
      throw new Error('decrypt-failed');
    });

    await expect(retrieveApiKey()).resolves.toBeNull();
    await expect(hasStoredApiKey()).resolves.toBe(true);
  });

  it('removes stored key and clears process global', async () => {
    await storeApiKey('ui-key-123');
    expect(getUiApiKey()).toBe('ui-key-123');

    await removeApiKey();

    expect(getUiApiKey()).toBeUndefined();
    await expect(hasStoredApiKey()).resolves.toBe(false);
  });

  it('fails closed when secure storage is unavailable', async () => {
    electronMock.safeStorage.isEncryptionAvailable.mockReturnValue(false);

    await expect(storeApiKey('ui-key-123')).rejects.toThrow(
      'Secure storage is not available on this platform'
    );
  });

  it('stores credentials owner-only', async () => {
    await storeApiKey('ui-key-123');

    const storagePath = getStoragePath(tmpDir);
    const { mode: fileMode } = await stat(storagePath);
    const { mode: dirMode } = await stat(path.dirname(storagePath));

    expect(fileMode & 0o777).toBe(0o600);
    expect(dirMode & 0o777).toBe(0o700);
  });

  it('repairs permissions of credentials written before the mode was enforced', async () => {
    await storeApiKey('ui-key-123');

    const storagePath = getStoragePath(tmpDir);
    await chmod(path.dirname(storagePath), 0o755);
    await chmod(storagePath, 0o644);

    await expect(retrieveApiKey()).resolves.toBe('ui-key-123');

    const { mode: fileMode } = await stat(storagePath);
    const { mode: dirMode } = await stat(path.dirname(storagePath));

    expect(fileMode & 0o777).toBe(0o600);
    expect(dirMode & 0o777).toBe(0o700);
  });

  it('prefers persisted UI storage over both Anthropic environment variables', async () => {
    process.env.ANTHROPIC_API_KEY = 'canonical-environment-key';
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'compatibility-alias-key';
    try {
      const credentials = new SafeStorageCredentialStore();
      await credentials.set('anthropic', 'persisted-ui-key');

      await expect(credentials.get('anthropic')).resolves.toBe('persisted-ui-key');
      await expect(credentials.status('anthropic')).resolves.toEqual({
        configured: true,
        source: 'ui',
        storage: 'available'
      });
    } finally {
      delete process.env.ANTHROPIC_API_KEY;
      delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
    }
  });

  it.each([
    {
      canonical: 'canonical-environment-key',
      compatibility: undefined,
      expected: 'canonical-environment-key',
      caseName: 'canonical variable alone'
    },
    {
      canonical: undefined,
      compatibility: 'compatibility-alias-key',
      expected: 'compatibility-alias-key',
      caseName: 'compatibility alias alone'
    },
    {
      canonical: 'canonical-environment-key',
      compatibility: 'compatibility-alias-key',
      expected: 'canonical-environment-key',
      caseName: 'canonical variable before compatibility alias'
    },
    {
      canonical: '   ',
      compatibility: 'compatibility-alias-key',
      expected: 'compatibility-alias-key',
      caseName: 'whitespace-only canonical variable falls through'
    },
    {
      canonical: 'canonical-environment-key',
      compatibility: '   ',
      expected: 'canonical-environment-key',
      caseName: 'whitespace-only compatibility alias does not mask canonical variable'
    },
    {
      canonical: '   ',
      compatibility: '\t',
      expected: undefined,
      caseName: 'whitespace-only variables resolve as unconfigured'
    }
  ])(
    'resolves Anthropic environment keys: $caseName',
    async ({ canonical, compatibility, expected }) => {
      if (canonical === undefined) {
        delete process.env.ANTHROPIC_API_KEY;
      } else {
        process.env.ANTHROPIC_API_KEY = canonical;
      }
      if (compatibility === undefined) {
        delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
      } else {
        process.env.CHIRALITY_ANTHROPIC_API_KEY = compatibility;
      }

      try {
        const credentials = new SafeStorageCredentialStore();
        await expect(credentials.get('anthropic')).resolves.toBe(expected);
        await expect(credentials.status('anthropic')).resolves.toEqual({
          configured: expected !== undefined,
          source: expected === undefined ? 'none' : 'env',
          storage: 'missing'
        });
      } finally {
        delete process.env.ANTHROPIC_API_KEY;
        delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
      }
    }
  );

  it('reports oMLX UI, environment, and none sources without consulting Anthropic variables', async () => {
    process.env.ANTHROPIC_API_KEY = 'canonical-anthropic-key';
    process.env.CHIRALITY_ANTHROPIC_API_KEY = 'compatibility-anthropic-key';
    process.env.CHIRALITY_OMLX_API_KEY = 'omlx-environment-key';
    try {
      const credentials = new SafeStorageCredentialStore();
      await credentials.set('omlx', 'omlx-persisted-key');

      await expect(credentials.status('omlx')).resolves.toEqual({
        configured: true,
        source: 'ui',
        storage: 'available'
      });

      await credentials.remove('omlx');
      await expect(credentials.status('omlx')).resolves.toEqual({
        configured: true,
        source: 'env',
        storage: 'missing'
      });

      delete process.env.CHIRALITY_OMLX_API_KEY;
      await expect(credentials.status('omlx')).resolves.toEqual({
        configured: false,
        source: 'none',
        storage: 'missing'
      });
    } finally {
      delete process.env.ANTHROPIC_API_KEY;
      delete process.env.CHIRALITY_ANTHROPIC_API_KEY;
      delete process.env.CHIRALITY_OMLX_API_KEY;
    }
  });

  it('reports unsupported providers as unconfigured without credential material', async () => {
    process.env.ANTHROPIC_API_KEY = 'canonical-anthropic-key';
    try {
      const credentials = new SafeStorageCredentialStore();
      const status = await credentials.status('unsupported');

      expect(status).toEqual({ configured: false, source: 'none', storage: 'missing' });
      expect(JSON.stringify(status)).not.toContain('canonical-anthropic-key');
    } finally {
      delete process.env.ANTHROPIC_API_KEY;
    }
  });
});

/**
 * DEL-04-05-V3-01 — typed safeStorage states with non-destructive proof.
 *
 * Fixtures: a corrupt ciphertext (bytes safeStorage cannot decrypt) and an
 * unavailable store (encryption not available). For each failed read the
 * stored bytes are proven byte-identical before and after (SHA-256 and raw
 * buffer equality), the file still exists, no plaintext is returned, and no
 * fallback store is consulted.
 */
describe('electron/api-key-storage typed storage states', () => {
  const CORRUPT_CIPHERTEXT = Buffer.from([0x00, 0xff, 0x13, 0x37, 0x42, 0x00, 0x99, 0xab]);
  const SECRET_PLAINTEXT = 'fixture-secret-must-not-leak';

  async function fingerprint(filePath: string): Promise<{ sha256: string; bytes: Buffer }> {
    const bytes = await readFile(filePath);
    return { sha256: createHash('sha256').update(bytes).digest('hex'), bytes };
  }

  async function writeBlob(providerFile: string, bytes: Buffer): Promise<string> {
    const blobPath = path.join(tmpDir, 'credentials', providerFile);
    await mkdir(path.dirname(blobPath), { recursive: true });
    await writeFile(blobPath, bytes);
    return blobPath;
  }

  it('reports missing when no ciphertext exists, without touching the environment', async () => {
    process.env.ANTHROPIC_API_KEY = SECRET_PLAINTEXT;
    try {
      await expect(readProviderCredential('anthropic')).resolves.toEqual({ state: 'missing' });
      await expect(probeProviderCredentialStorage('anthropic')).resolves.toBe('missing');
      await expect(readProviderCredential('omlx')).resolves.toEqual({ state: 'missing' });
      expect(electronMock.safeStorage.decryptString).not.toHaveBeenCalled();
    } finally {
      delete process.env.ANTHROPIC_API_KEY;
    }
  });

  it('reports available with the plaintext only on the read path, never on the probe', async () => {
    await storeProviderApiKey('anthropic', SECRET_PLAINTEXT);

    await expect(readProviderCredential('anthropic')).resolves.toEqual({
      state: 'available',
      value: SECRET_PLAINTEXT
    });
    const probe = await probeProviderCredentialStorage('anthropic');
    expect(probe).toBe('available');
    expect(JSON.stringify(probe)).not.toContain(SECRET_PLAINTEXT);
  });

  it('decryptFailed: corrupt ciphertext is classified, retained byte-identical, and never exposed', async () => {
    const blobPath = await writeBlob('api-key.enc', CORRUPT_CIPHERTEXT);
    const before = await fingerprint(blobPath);
    electronMock.safeStorage.decryptString.mockImplementation(() => {
      throw new Error(`decrypt failed for ${SECRET_PLAINTEXT}`);
    });

    const read = await readProviderCredential('anthropic');
    const probe = await probeProviderCredentialStorage('anthropic');
    const retrieved = await retrieveProviderApiKey('anthropic');

    expect(read).toEqual({ state: 'decryptFailed' });
    expect(probe).toBe('decryptFailed');
    expect(retrieved).toBeNull();
    expect(JSON.stringify({ read, probe, retrieved })).not.toContain(SECRET_PLAINTEXT);
    expect(electronMock.safeStorage.decryptString).toHaveBeenCalledTimes(3);
    expect(electronMock.safeStorage.encryptString).not.toHaveBeenCalled();

    const after = await fingerprint(blobPath);
    expect(after.sha256).toBe(before.sha256);
    expect(after.bytes.equals(CORRUPT_CIPHERTEXT)).toBe(true);
    expect(before.bytes.equals(after.bytes)).toBe(true);
    await expect(hasStoredProviderApiKey('anthropic')).resolves.toBe(true);
  });

  it('decryptFailed: the store reports it beside the unchanged source precedence', async () => {
    const blobPath = await writeBlob('api-key.enc', CORRUPT_CIPHERTEXT);
    const before = await fingerprint(blobPath);
    electronMock.safeStorage.decryptString.mockImplementation(() => {
      throw new Error('corrupted');
    });
    const credentials = new SafeStorageCredentialStore();

    await expect(credentials.status('anthropic')).resolves.toEqual({
      configured: false,
      source: 'none',
      storage: 'decryptFailed'
    });
    await expect(credentials.get('anthropic')).resolves.toBeUndefined();
    expect(getUiApiKey()).toBeUndefined();

    process.env.ANTHROPIC_API_KEY = 'canonical-environment-key';
    try {
      await expect(credentials.status('anthropic')).resolves.toEqual({
        configured: true,
        source: 'env',
        storage: 'decryptFailed'
      });
      await expect(credentials.get('anthropic')).resolves.toBe('canonical-environment-key');
    } finally {
      delete process.env.ANTHROPIC_API_KEY;
    }

    const after = await fingerprint(blobPath);
    expect(after.sha256).toBe(before.sha256);
    expect(after.bytes.equals(CORRUPT_CIPHERTEXT)).toBe(true);
  });

  it('decryptFailed: only an explicit store or remove replaces the retained blob', async () => {
    const blobPath = await writeBlob('api-key.enc', CORRUPT_CIPHERTEXT);
    electronMock.safeStorage.decryptString.mockImplementationOnce(() => {
      throw new Error('corrupted');
    });
    const credentials = new SafeStorageCredentialStore();
    await expect(credentials.status('anthropic')).resolves.toMatchObject({ storage: 'decryptFailed' });
    expect((await readFile(blobPath)).equals(CORRUPT_CIPHERTEXT)).toBe(true);

    await credentials.set('anthropic', 'replacement-key');
    await expect(readFile(blobPath, 'utf8')).resolves.toBe('enc:replacement-key');
    await expect(credentials.status('anthropic')).resolves.toEqual({
      configured: true,
      source: 'ui',
      storage: 'available'
    });

    await credentials.remove('anthropic');
    await expect(credentials.status('anthropic')).resolves.toEqual({
      configured: false,
      source: 'none',
      storage: 'missing'
    });
  });

  it('storageUnavailable: the blob is not opened and stays byte-identical', async () => {
    const blobPath = await writeBlob('api-key.enc', Buffer.from(`enc:${SECRET_PLAINTEXT}`, 'utf8'));
    const before = await fingerprint(blobPath);
    electronMock.safeStorage.isEncryptionAvailable.mockReturnValue(false);

    const read = await readProviderCredential('anthropic');
    const probe = await probeProviderCredentialStorage('anthropic');
    const retrieved = await retrieveProviderApiKey('anthropic');

    expect(read).toEqual({ state: 'storageUnavailable' });
    expect(probe).toBe('storageUnavailable');
    expect(retrieved).toBeNull();
    expect(JSON.stringify({ read, probe, retrieved })).not.toContain(SECRET_PLAINTEXT);
    expect(electronMock.safeStorage.decryptString).not.toHaveBeenCalled();
    expect(electronMock.safeStorage.encryptString).not.toHaveBeenCalled();

    const after = await fingerprint(blobPath);
    expect(after.sha256).toBe(before.sha256);
    expect(after.bytes.equals(before.bytes)).toBe(true);
    await expect(hasStoredProviderApiKey('anthropic')).resolves.toBe(true);
  });

  it('storageUnavailable: the store reports it, keeps environment precedence, and refuses writes', async () => {
    electronMock.safeStorage.isEncryptionAvailable.mockReturnValue(false);
    const credentials = new SafeStorageCredentialStore();

    await expect(credentials.status('anthropic')).resolves.toEqual({
      configured: false,
      source: 'none',
      storage: 'storageUnavailable'
    });
    await expect(credentials.status('omlx')).resolves.toEqual({
      configured: false,
      source: 'none',
      storage: 'storageUnavailable'
    });

    process.env.CHIRALITY_OMLX_API_KEY = 'omlx-environment-key';
    try {
      await expect(credentials.status('omlx')).resolves.toEqual({
        configured: true,
        source: 'env',
        storage: 'storageUnavailable'
      });
    } finally {
      delete process.env.CHIRALITY_OMLX_API_KEY;
    }

    await expect(credentials.set('anthropic', 'new-key')).rejects.toThrow(
      'Secure storage is not available on this platform'
    );
    await expect(hasStoredProviderApiKey('anthropic')).resolves.toBe(false);
  });

  it('treats a ciphertext that decrypts to nothing usable as missing', async () => {
    await writeBlob('api-key.enc', Buffer.from('enc:   ', 'utf8'));

    await expect(readProviderCredential('anthropic')).resolves.toEqual({ state: 'missing' });
    await expect(new SafeStorageCredentialStore().status('anthropic')).resolves.toEqual({
      configured: false,
      source: 'none',
      storage: 'missing'
    });
  });

  it('keeps provider blobs independent across states', async () => {
    await storeProviderApiKey('omlx', 'omlx-secret');
    await writeBlob('api-key.enc', CORRUPT_CIPHERTEXT);
    electronMock.safeStorage.decryptString.mockImplementation((value: Buffer) => {
      const raw = value.toString('utf8');
      if (!raw.startsWith('enc:')) {
        throw new Error('corrupted');
      }
      return raw.slice(4);
    });
    const credentials = new SafeStorageCredentialStore();

    await expect(credentials.status('anthropic')).resolves.toMatchObject({ storage: 'decryptFailed' });
    await expect(credentials.status('omlx')).resolves.toEqual({
      configured: true,
      source: 'ui',
      storage: 'available'
    });
  });
});
