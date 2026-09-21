import { access, mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { FileSessionManager } from '../../lib/harness/session-manager';
import { SessionRecord } from '@chirality/runtime-contracts/types';

type PersistedSessionRecord = SessionRecord & Record<string, unknown>;

let tmpRoot = '';
let projectRoot = '';
let sessionRoot = '';

function sessionRecord(
  sessionId: string,
  overrides: Partial<PersistedSessionRecord> = {}
): PersistedSessionRecord {
  return {
    sessionId,
    projectRoot,
    persona: 'WORKING_ITEMS',
    mode: 'WORKBENCH',
    createdAt: '2026-06-21T00:00:00.000Z',
    updatedAt: '2026-06-21T00:00:00.000Z',
    ...overrides
  };
}

function canonicalPath(sessionId: string): string {
  return path.join(sessionRoot, sessionId, 'session.json');
}

function legacyPath(sessionId: string): string {
  return path.join(sessionRoot, `${sessionId}.json`);
}

async function readPersistedSession(sessionId: string): Promise<PersistedSessionRecord> {
  return JSON.parse(await readFile(canonicalPath(sessionId), 'utf8')) as PersistedSessionRecord;
}

beforeEach(async () => {
  tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-session-manager-'));
  projectRoot = path.join(tmpRoot, 'project-root');
  sessionRoot = path.join(tmpRoot, '.chirality', 'sessions');
  await mkdir(projectRoot, { recursive: true });
  process.env.CHIRALITY_SESSION_ROOT = sessionRoot;
});

afterEach(async () => {
  delete process.env.CHIRALITY_SESSION_ROOT;
  if (tmpRoot) {
    await rm(tmpRoot, { recursive: true, force: true });
    tmpRoot = '';
  }
});

describe('FileSessionManager canonical session storage', () => {
  it('creates new sessions as canonical folder records without writing legacy flat files', async () => {
    const manager = new FileSessionManager();

    const session = await manager.create({ projectRoot, persona: 'TASK', mode: 'PIPELINE' });

    await expect(access(canonicalPath(session.sessionId))).resolves.toBeUndefined();
    await expect(access(legacyPath(session.sessionId))).rejects.toThrow();
    await expect(readPersistedSession(session.sessionId)).resolves.toMatchObject({
      sessionId: session.sessionId,
      projectRoot,
      persona: 'TASK',
      mode: 'PIPELINE'
    });
  });

  it.each([
    ['empty', ''],
    ['whitespace-only', '   '],
    ['dot segment', '.'],
    ['parent segment', '..'],
    ['forward-slash traversal', '../escaped'],
    ['forward-slash nesting', 'nested/session'],
    ['backslash traversal', '..\\escaped'],
    ['backslash nesting', 'nested\\session']
  ])('rejects an unsafe session ID before resolving paths: %s', async (_caseName, sessionId) => {
    const manager = new FileSessionManager();
    const wouldBeLegacyPath = path.join(sessionRoot, `${sessionId}.json`);
    const wouldBeCanonicalPath = path.join(sessionRoot, sessionId, 'session.json');
    const seededLegacyRecord = `${JSON.stringify(sessionRecord(sessionId), null, 2)}\n`;
    await mkdir(path.dirname(wouldBeLegacyPath), { recursive: true });
    await writeFile(wouldBeLegacyPath, seededLegacyRecord, 'utf8');

    await expect(manager.getById(sessionId)).rejects.toMatchObject({
      type: 'SESSION_NOT_FOUND',
      status: 404,
      details: { sessionId }
    });
    await expect(readFile(wouldBeLegacyPath, 'utf8')).resolves.toBe(seededLegacyRecord);
    await expect(access(wouldBeCanonicalPath)).rejects.toThrow();
  });

  it('opens ambiguous legacy stub records without pinning them to Anthropic or touching the flat file', async () => {
    const manager = new FileSessionManager();
    const sessionId = 'sess_legacy';
    await mkdir(sessionRoot, { recursive: true });
    const seededLegacy = `${JSON.stringify(
      sessionRecord(sessionId, {
        claudeSessionId: 'claude_legacy',
        legacyOnly: 'preserved'
      }),
      null,
      2
    )}\n`;
    await writeFile(legacyPath(sessionId), seededLegacy, 'utf8');

    const session = (await manager.resume(sessionId)) as PersistedSessionRecord;

    expect(session).toMatchObject({
      sessionId,
      claudeSessionId: 'claude_legacy',
      legacyOnly: 'preserved'
    });
    expect(session.engineSelection).toBeUndefined();
    expect(session.adapterSession).toBeUndefined();
    await expect(readFile(legacyPath(sessionId), 'utf8')).resolves.toBe(seededLegacy);
    const persisted = await readPersistedSession(sessionId);
    expect(persisted).toMatchObject({
      claudeSessionId: 'claude_legacy',
      legacyOnly: 'preserved'
    });
    expect(persisted.engineSelection).toBeUndefined();
    expect(persisted.adapterSession).toBeUndefined();
  });

  it('migrates a legacy direct-Anthropic record when package attribution is explicit', async () => {
    const manager = new FileSessionManager();
    const sessionId = 'sess_legacy_direct';
    await mkdir(sessionRoot, { recursive: true });
    await writeFile(
      legacyPath(sessionId),
      `${JSON.stringify(
        sessionRecord(sessionId, {
          engineSessionId: 'claude_direct',
          claudeSessionId: 'claude_direct',
          model: 'claude-direct-model',
          adapterSession: {
            engineSessionId: 'claude_direct',
            packageName: '@anthropic-ai/sdk',
            packageVersion: '1.2.3'
          }
        }),
        null,
        2
      )}\n`,
      'utf8'
    );

    const session = await manager.resume(sessionId);

    expect(session.engineSelection).toEqual({
      adapterId: 'anthropic-direct',
      providerId: 'anthropic',
      model: 'claude-direct-model'
    });
    expect(session.adapterSession).toEqual({
      engineSessionId: 'claude_direct',
      packageName: '@anthropic-ai/sdk',
      packageVersion: '1.2.3'
    });
  });

  it('does not treat the SDK version once dual-written by stub boot as Claude attribution', async () => {
    const manager = new FileSessionManager();
    const sessionId = 'sess_legacy_stub_boot';
    await mkdir(sessionRoot, { recursive: true });
    await writeFile(
      legacyPath(sessionId),
      `${JSON.stringify(
        sessionRecord(sessionId, {
          engineSessionId: 'claude_shaped_stub_id',
          claudeSessionId: 'claude_shaped_stub_id',
          sdkPackageVersion: '0.3.150'
        }),
        null,
        2
      )}\n`,
      'utf8'
    );

    const session = await manager.resume(sessionId);

    expect(session.engineSelection).toBeUndefined();
    expect(session.adapterSession).toBeUndefined();
    expect(session).toMatchObject({
      engineSessionId: 'claude_shaped_stub_id',
      claudeSessionId: 'claude_shaped_stub_id',
      sdkPackageVersion: '0.3.150'
    });
  });

  it('migrates SDK-specific legacy linkage to the Claude Agent SDK adapter', async () => {
    const manager = new FileSessionManager();
    const sessionId = 'sess_legacy_sdk';
    await mkdir(sessionRoot, { recursive: true });
    await writeFile(
      legacyPath(sessionId),
      `${JSON.stringify(
        sessionRecord(sessionId, {
          claudeSessionId: 'claude_legacy',
          sdkSessionId: 'sdk_legacy',
          sdkTranscriptPath: '/tmp/transcript.jsonl',
          sdkSessionStoreKey: 'sdk-store-key',
          sdkPackageVersion: '0.3.150'
        }),
        null,
        2
      )}\n`,
      'utf8'
    );

    const session = await manager.resume(sessionId);

    expect(session.engineSelection).toEqual({
      adapterId: 'claude-agent-sdk',
      providerId: 'anthropic',
      model: ''
    });
    expect(session.adapterSession).toEqual({
      engineSessionId: 'sdk_legacy',
      transcriptPath: '/tmp/transcript.jsonl',
      storeKey: 'sdk-store-key',
      packageName: '@anthropic-ai/claude-agent-sdk',
      packageVersion: '0.3.150'
    });
  });

  it('resolves duplicate canonical and flat records with canonical precedence, no legacy field loss, and no flat-file removal', async () => {
    const manager = new FileSessionManager();
    const sessionId = 'sess_duplicate';
    await mkdir(path.dirname(canonicalPath(sessionId)), { recursive: true });
    await mkdir(sessionRoot, { recursive: true });
    const seededLegacy = `${JSON.stringify(
      sessionRecord(sessionId, {
        engineSessionId: 'engine_legacy',
        claudeSessionId: 'claude_legacy',
        sdkPackageVersion: 'legacy-sdk',
        legacyOnly: { nested: true }
      }),
      null,
      2
    )}\n`;
    await writeFile(legacyPath(sessionId), seededLegacy, 'utf8');
    await writeFile(
      canonicalPath(sessionId),
      `${JSON.stringify(
        sessionRecord(sessionId, {
          engineSessionId: 'engine_canonical',
          sdkSessionId: 'sdk_canonical',
          updatedAt: '2026-06-21T01:00:00.000Z'
        }),
        null,
        2
      )}\n`,
      'utf8'
    );

    const session = (await manager.getById(sessionId)) as PersistedSessionRecord;

    expect(session).toMatchObject({
      sessionId,
      engineSessionId: 'engine_canonical',
      sdkSessionId: 'sdk_canonical',
      claudeSessionId: 'claude_legacy',
      sdkPackageVersion: 'legacy-sdk',
      legacyOnly: { nested: true }
    });
    await expect(readFile(legacyPath(sessionId), 'utf8')).resolves.toBe(seededLegacy);
    await expect(readPersistedSession(sessionId)).resolves.toMatchObject({
      engineSessionId: 'engine_canonical',
      sdkSessionId: 'sdk_canonical',
      claudeSessionId: 'claude_legacy',
      sdkPackageVersion: 'legacy-sdk',
      legacyOnly: { nested: true }
    });
  });

  it('materializes canonical records during list traversal without touching the legacy file', async () => {
    const manager = new FileSessionManager();
    const sessionId = 'sess_listed';
    await mkdir(sessionRoot, { recursive: true });
    const seededLegacy = `${JSON.stringify(
      sessionRecord(sessionId, { model: 'claude-sonnet-4' }),
      null,
      2
    )}\n`;
    await writeFile(legacyPath(sessionId), seededLegacy, 'utf8');

    const sessions = await manager.list(projectRoot);

    expect(sessions.map((session) => session.sessionId)).toEqual([sessionId]);
    await expect(readFile(legacyPath(sessionId), 'utf8')).resolves.toBe(seededLegacy);
    await expect(readPersistedSession(sessionId)).resolves.toMatchObject({
      sessionId,
      model: 'claude-sonnet-4'
    });
  });

  it('canonicalizes legacy records before saving updates and leaves the flat file byte-identical', async () => {
    const manager = new FileSessionManager();
    const sessionId = 'sess_save';
    await mkdir(sessionRoot, { recursive: true });
    const seededLegacy = `${JSON.stringify(
      sessionRecord(sessionId, { claudeSessionId: 'claude_legacy' }),
      null,
      2
    )}\n`;
    await writeFile(legacyPath(sessionId), seededLegacy, 'utf8');

    const saved = await manager.save(sessionId, { model: 'claude-opus-4' });

    expect(saved).toMatchObject({
      sessionId,
      claudeSessionId: 'claude_legacy',
      model: 'claude-opus-4'
    });
    expect(saved.engineSelection).toBeUndefined();
    await expect(readFile(legacyPath(sessionId), 'utf8')).resolves.toBe(seededLegacy);
    const persisted = await readPersistedSession(sessionId);
    expect(persisted).toMatchObject({
      claudeSessionId: 'claude_legacy',
      model: 'claude-opus-4'
    });
    expect(persisted.engineSelection).toBeUndefined();
  });

  it('removes canonical folders and stray flat files when deleting a session', async () => {
    const manager = new FileSessionManager();
    const sessionId = 'sess_delete';
    await mkdir(path.dirname(canonicalPath(sessionId)), { recursive: true });
    await mkdir(sessionRoot, { recursive: true });
    await writeFile(
      canonicalPath(sessionId),
      `${JSON.stringify(sessionRecord(sessionId, { engineSessionId: 'engine_canonical' }), null, 2)}\n`,
      'utf8'
    );
    await writeFile(
      legacyPath(sessionId),
      `${JSON.stringify(sessionRecord(sessionId, { claudeSessionId: 'claude_legacy' }), null, 2)}\n`,
      'utf8'
    );

    await manager.delete(sessionId);

    await expect(access(path.dirname(canonicalPath(sessionId)))).rejects.toThrow();
    await expect(access(legacyPath(sessionId))).rejects.toThrow();
    await expect(manager.getById(sessionId)).rejects.toMatchObject({ type: 'SESSION_NOT_FOUND' });
  });
});
