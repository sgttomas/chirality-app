import { createHash } from 'node:crypto';
import { access, mkdir, mkdtemp, readdir, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import {
  FileSessionManager,
  SessionRecordAccessError,
  type SessionAccessFailure,
  type SessionAccessResult
} from '../../lib/harness/session-manager';

/**
 * DEL-05-01-V3-01 — representative v2 (release 2.0.0) project-local session
 * records open lazily and non-destructively with typed failure states while
 * list, resume, and delete semantics are preserved.
 *
 * Fixtures live under `src/__tests__/fixtures/sessions/v2/` and are copied
 * into a throwaway session root per test with their project-root placeholders
 * substituted. Every legacy flat file is compared byte-for-byte before and
 * after each access.
 */

const FIXTURE_ROOT = fileURLToPath(new URL('../fixtures/sessions/v2/', import.meta.url));
const PROJECT_ROOT_PLACEHOLDER = '__PROJECT_ROOT__';
const OTHER_PROJECT_ROOT_PLACEHOLDER = '__OTHER_PROJECT_ROOT__';

type FixtureManifest = {
  schema: string;
  release: string;
  fixtures: Array<{
    sessionId: string;
    files: string[];
    case: string;
    expectedKind: SessionAccessResult['kind'];
    description: string;
  }>;
};

let tmpRoot = '';
let projectRoot = '';
let otherProjectRoot = '';
let sessionRoot = '';
let manifest: FixtureManifest;
let seededBytes: Map<string, Buffer>;

function legacyPath(sessionId: string): string {
  return path.join(sessionRoot, `${sessionId}.json`);
}

function canonicalDirectory(sessionId: string): string {
  return path.join(sessionRoot, sessionId);
}

function canonicalPath(sessionId: string): string {
  return path.join(canonicalDirectory(sessionId), 'session.json');
}

async function listFilesRecursively(root: string, relativeTo = root): Promise<string[]> {
  const entries = await readdir(root, { withFileTypes: true });
  const files: string[] = [];
  for (const entry of entries) {
    const absolute = path.join(root, entry.name);
    if (entry.isDirectory()) {
      files.push(...(await listFilesRecursively(absolute, relativeTo)));
    } else if (entry.isFile()) {
      files.push(path.relative(relativeTo, absolute).split(path.sep).join('/'));
    }
  }
  return files.sort();
}

async function snapshotBytes(root: string): Promise<Map<string, Buffer>> {
  const snapshot = new Map<string, Buffer>();
  for (const relativePath of await listFilesRecursively(root)) {
    snapshot.set(relativePath, await readFile(path.join(root, ...relativePath.split('/'))));
  }
  return snapshot;
}

async function expectBytesUnchanged(
  expected: Map<string, Buffer>,
  relativePaths: Iterable<string> = expected.keys()
): Promise<void> {
  for (const relativePath of relativePaths) {
    const before = expected.get(relativePath);
    if (!before) {
      throw new Error(`no snapshot for ${relativePath}`);
    }
    const after = await readFile(path.join(sessionRoot, ...relativePath.split('/')));
    expect(after.equals(before), `${relativePath} must be byte-identical`).toBe(true);
  }
}

function legacyFlatFiles(snapshot: Map<string, Buffer>): string[] {
  return [...snapshot.keys()].filter((relativePath) => !relativePath.includes('/'));
}

function jsonStringBody(value: string): string {
  return JSON.stringify(value).slice(1, -1);
}

async function seedFixtures(): Promise<Map<string, Buffer>> {
  const files = (await listFilesRecursively(FIXTURE_ROOT)).filter(
    (relativePath) => relativePath !== 'manifest.json'
  );
  for (const relativePath of files) {
    const source = await readFile(path.join(FIXTURE_ROOT, ...relativePath.split('/')), 'utf8');
    const seeded = source
      .replaceAll(PROJECT_ROOT_PLACEHOLDER, jsonStringBody(projectRoot))
      .replaceAll(OTHER_PROJECT_ROOT_PLACEHOLDER, jsonStringBody(otherProjectRoot));
    const target = path.join(sessionRoot, ...relativePath.split('/'));
    await mkdir(path.dirname(target), { recursive: true });
    await writeFile(target, seeded, 'utf8');
  }
  return snapshotBytes(sessionRoot);
}

function fixture(sessionId: string): FixtureManifest['fixtures'][number] {
  const found = manifest.fixtures.find((candidate) => candidate.sessionId === sessionId);
  if (!found) {
    throw new Error(`fixture ${sessionId} is not in the manifest`);
  }
  return found;
}

function sortedFailures(failures: readonly SessionAccessFailure[]): SessionAccessFailure[] {
  return [...failures].sort((a, b) => a.sessionId.localeCompare(b.sessionId));
}

function sha256(bytes: Buffer): string {
  return createHash('sha256').update(bytes).digest('hex');
}

async function readCanonical(sessionId: string): Promise<Record<string, unknown>> {
  return JSON.parse(await readFile(canonicalPath(sessionId), 'utf8')) as Record<string, unknown>;
}

beforeEach(async () => {
  tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-session-v2-access-'));
  projectRoot = path.join(tmpRoot, 'project-root');
  otherProjectRoot = path.join(tmpRoot, 'other-project-root');
  sessionRoot = path.join(tmpRoot, '.chirality', 'sessions');
  await mkdir(projectRoot, { recursive: true });
  await mkdir(otherProjectRoot, { recursive: true });
  await mkdir(sessionRoot, { recursive: true });
  process.env.CHIRALITY_SESSION_ROOT = sessionRoot;
  manifest = JSON.parse(
    await readFile(path.join(FIXTURE_ROOT, 'manifest.json'), 'utf8')
  ) as FixtureManifest;
  seededBytes = await seedFixtures();
});

afterEach(async () => {
  delete process.env.CHIRALITY_SESSION_ROOT;
  if (tmpRoot) {
    await rm(tmpRoot, { recursive: true, force: true });
    tmpRoot = '';
  }
});

describe('v2 legacy session fixtures', () => {
  it('inventories every fixture file in the manifest without secrets or user data', async () => {
    const files = (await listFilesRecursively(FIXTURE_ROOT)).filter(
      (relativePath) => relativePath !== 'manifest.json'
    );
    const declared = manifest.fixtures.flatMap((entry) => entry.files).sort();

    expect(manifest.schema).toBe('chirality-app-dev/session-fixtures/v2');
    expect(manifest.release).toBe('2.0.0');
    expect(files).toEqual(declared);
    for (const relativePath of files) {
      const content = await readFile(path.join(FIXTURE_ROOT, ...relativePath.split('/')), 'utf8');
      expect(content).not.toMatch(/sk-ant|api[_-]?key|Bearer |\/Users\/|\/home\//i);
    }
  });

  it('seeds the fixture root with only the fixture files', async () => {
    expect([...seededBytes.keys()]).toEqual(
      manifest.fixtures.flatMap((entry) => entry.files).sort()
    );
    expect(legacyFlatFiles(seededBytes)).toHaveLength(6);
  });
});

describe('typed lazy access (inspect)', () => {
  it('returns the expected typed state for every fixture without throwing on record content', async () => {
    const manager = new FileSessionManager();
    const results = new Map<string, SessionAccessResult>();
    for (const entry of manifest.fixtures) {
      results.set(entry.sessionId, await manager.inspect(entry.sessionId));
    }

    for (const entry of manifest.fixtures) {
      expect(results.get(entry.sessionId)?.kind, entry.case).toBe(entry.expectedKind);
    }

    const malformed = results.get('sess_v2_malformed_truncated');
    expect(malformed).toMatchObject({
      kind: 'malformed',
      sessionId: 'sess_v2_malformed_truncated',
      failure: {
        kind: 'malformed',
        shape: 'legacy',
        filePath: legacyPath('sess_v2_malformed_truncated'),
        reason: expect.stringMatching(/^invalid JSON: /)
      }
    });

    const unsupported = results.get('sess_v2_unsupported_version');
    expect(unsupported).toMatchObject({
      kind: 'unsupportedVersion',
      failure: {
        kind: 'unsupportedVersion',
        shape: 'legacy',
        filePath: legacyPath('sess_v2_unsupported_version'),
        schemaVersion: 'chirality.session/v9',
        projectRoot,
        reason: expect.stringContaining('chirality.session/v9')
      }
    });

    const missingFields = results.get('sess_v2_missing_version_fields');
    expect(missingFields).toMatchObject({
      kind: 'unsupportedVersion',
      failure: {
        kind: 'unsupportedVersion',
        shape: 'legacy',
        schemaVersion: undefined,
        reason: expect.stringContaining('required v2 fields')
      }
    });
    expect((missingFields as { failure: SessionAccessFailure }).failure.projectRoot).toBeUndefined();

    const readable = results.get('sess_v2_readable');
    expect(readable).toMatchObject({
      kind: 'ok',
      materialized: true,
      siblingFailures: [],
      diagnostics: [],
      session: {
        legacySource: {
          sha256: sha256(seededBytes.get('sess_v2_readable.json') as Buffer),
          materializedAt: expect.stringMatching(/^\d{4}-\d{2}-\d{2}T/)
        },
        sessionId: 'sess_v2_readable',
        projectRoot,
        persona: 'WORKING_ITEMS',
        mode: 'direct',
        createdAt: '2026-08-30T12:00:00.000Z',
        engineSessionId: 'engine_fixture_readable',
        engineSelection: {
          adapterId: 'claude-agent-sdk',
          providerId: 'anthropic',
          model: 'fixture-model'
        },
        agentInstanceId: 'WI-FIXTURE-READABLE'
      }
    });

    expect(await manager.inspect('sess_v2_absent')).toEqual({
      kind: 'missing',
      sessionId: 'sess_v2_absent'
    });

    await expectBytesUnchanged(seededBytes, legacyFlatFiles(seededBytes));
    await expectBytesUnchanged(seededBytes, ['sess_v2_duplicate/events.jsonl']);
    for (const sessionId of [
      'sess_v2_malformed_truncated',
      'sess_v2_unsupported_version',
      'sess_v2_missing_version_fields'
    ]) {
      await expect(access(canonicalDirectory(sessionId))).rejects.toThrow();
    }
  });

  it('is idempotent: a second access of an already materialized record writes nothing', async () => {
    const manager = new FileSessionManager();
    const first = await manager.inspect('sess_v2_readable');
    expect(first).toMatchObject({ kind: 'ok', materialized: true });
    const afterFirst = await snapshotBytes(sessionRoot);

    const second = await manager.inspect('sess_v2_readable');

    expect(second).toMatchObject({ kind: 'ok', materialized: false });
    expect(await listFilesRecursively(sessionRoot)).toEqual([...afterFirst.keys()]);
    await expectBytesUnchanged(afterFirst);
  });
});

describe('list', () => {
  it('reports unreadable records as typed failures instead of skipping them and leaves legacy bytes intact', async () => {
    const manager = new FileSessionManager();
    const filesBefore = await listFilesRecursively(sessionRoot);

    const result = await manager.listWithDiagnostics(projectRoot);

    expect(result.sessions.map((session) => session.sessionId)).toEqual([
      'sess_v2_readable',
      'sess_v2_duplicate'
    ]);
    expect(sortedFailures(result.failures)).toEqual([
      expect.objectContaining({
        sessionId: 'sess_v2_malformed_truncated',
        kind: 'malformed',
        shape: 'legacy',
        filePath: legacyPath('sess_v2_malformed_truncated')
      }),
      expect.objectContaining({
        sessionId: 'sess_v2_missing_version_fields',
        kind: 'unsupportedVersion',
        shape: 'legacy'
      }),
      expect.objectContaining({
        sessionId: 'sess_v2_unsupported_version',
        kind: 'unsupportedVersion',
        shape: 'legacy',
        schemaVersion: 'chirality.session/v9'
      })
    ]);

    expect(result.diagnostics).toEqual([]);
    await expect(manager.list(projectRoot)).resolves.toEqual(result.sessions);

    await expectBytesUnchanged(seededBytes, legacyFlatFiles(seededBytes));
    await expectBytesUnchanged(seededBytes, ['sess_v2_duplicate/events.jsonl']);
    expect(await listFilesRecursively(sessionRoot)).toEqual(
      [...filesBefore, 'sess_v2_readable/session.json'].sort()
    );
  });

  it('does not materialize records bound to another project root', async () => {
    const manager = new FileSessionManager();

    const result = await manager.listWithDiagnostics(projectRoot);

    expect(result.sessions.map((session) => session.sessionId)).not.toContain(
      'sess_v2_other_project'
    );
    expect(result.failures.map((failure) => failure.sessionId)).not.toContain(
      'sess_v2_other_project'
    );
    await expect(access(canonicalDirectory('sess_v2_other_project'))).rejects.toThrow();
    await expectBytesUnchanged(seededBytes, ['sess_v2_other_project.json']);
  });

  it('is idempotent across repeated listings', async () => {
    const manager = new FileSessionManager();
    const first = await manager.listWithDiagnostics(projectRoot);
    const afterFirst = await snapshotBytes(sessionRoot);

    const second = await manager.listWithDiagnostics(projectRoot);

    expect(second).toEqual(first);
    expect(await listFilesRecursively(sessionRoot)).toEqual([...afterFirst.keys()]);
    await expectBytesUnchanged(afterFirst);
  });

  it('never aborts on a sibling whose materialization fails: lists it unmaterialized with a diagnostic', async () => {
    const manager = new FileSessionManager();
    const blockedId = 'sess_x';
    const blockedLegacy = `${JSON.stringify(
      {
        sessionId: blockedId,
        projectRoot,
        persona: 'WORKING_ITEMS',
        mode: 'direct',
        createdAt: '2026-08-30T11:00:00.000Z',
        updatedAt: '2026-08-30T11:00:00.000Z'
      },
      null,
      2
    )}\n`;
    await writeFile(legacyPath(blockedId), blockedLegacy, 'utf8');
    // An empty regular file occupies the canonical folder path, so mkdir fails.
    await writeFile(canonicalDirectory(blockedId), '', 'utf8');
    const filesBefore = await listFilesRecursively(sessionRoot);

    const result = await manager.listWithDiagnostics(projectRoot);

    expect(result.sessions.map((session) => session.sessionId)).toEqual([
      blockedId,
      'sess_v2_readable',
      'sess_v2_duplicate'
    ]);
    expect(result.sessions[0]).not.toHaveProperty('legacySource');
    expect(result.diagnostics).toEqual([
      expect.objectContaining({
        sessionId: blockedId,
        code: 'materializationFailed',
        shape: 'canonical',
        filePath: canonicalPath(blockedId),
        reason: expect.stringMatching(/could not be materialized/)
      })
    ]);
    expect(sortedFailures(result.failures).map((failure) => failure.sessionId)).toEqual([
      'sess_v2_malformed_truncated',
      'sess_v2_missing_version_fields',
      'sess_v2_unsupported_version'
    ]);
    await expect(readFile(legacyPath(blockedId), 'utf8')).resolves.toBe(blockedLegacy);
    await expect(readFile(canonicalDirectory(blockedId), 'utf8')).resolves.toBe('');
    expect(await listFilesRecursively(sessionRoot)).toEqual(
      [...filesBefore, 'sess_v2_readable/session.json'].sort()
    );
    await expectBytesUnchanged(seededBytes, legacyFlatFiles(seededBytes));
    // The throwing surfaces still surface the environment fault instead of hiding it.
    await expect(manager.getById(blockedId)).rejects.toThrow();
  });
});

describe('resume and getById', () => {
  it('opens a readable legacy record lazily and writes only into the canonical folder', async () => {
    const manager = new FileSessionManager();
    const filesBefore = await listFilesRecursively(sessionRoot);

    const session = await manager.resume('sess_v2_readable');

    expect(session).toMatchObject({
      sessionId: 'sess_v2_readable',
      projectRoot,
      engineSessionId: 'engine_fixture_readable',
      bootFingerprint: 'fixture-boot-fingerprint-readable',
      model: 'fixture-model',
      adapterSession: {
        engineSessionId: 'engine_fixture_readable',
        packageName: '@anthropic-ai/claude-agent-sdk',
        packageVersion: '0.3.150'
      }
    });
    await expect(manager.getById('sess_v2_readable')).resolves.toEqual(session);
    expect(JSON.parse(await readFile(canonicalPath('sess_v2_readable'), 'utf8'))).toEqual(
      JSON.parse(JSON.stringify(session))
    );
    expect(await listFilesRecursively(sessionRoot)).toEqual(
      [...filesBefore, 'sess_v2_readable/session.json'].sort()
    );
    await expectBytesUnchanged(seededBytes, legacyFlatFiles(seededBytes));
  });

  it.each([
    ['sess_v2_malformed_truncated', 'malformed', /is malformed/],
    ['sess_v2_unsupported_version', 'unsupportedVersion', /unsupported schema version/],
    ['sess_v2_missing_version_fields', 'unsupportedVersion', /unsupported schema version/]
  ] as const)(
    'rejects %s with a typed %s error and leaves every byte untouched',
    async (sessionId, kind, messagePattern) => {
      const manager = new FileSessionManager();
      const filesBefore = await listFilesRecursively(sessionRoot);

      const error: unknown = await manager.resume(sessionId).catch((caught: unknown) => caught);

      expect(error).toBeInstanceOf(SessionRecordAccessError);
      expect(error).toMatchObject({
        name: 'SessionRecordAccessError',
        type: 'SESSION_NOT_FOUND',
        status: 422,
        kind,
        sessionId,
        message: expect.stringMatching(messagePattern),
        details: {
          sessionId,
          kind,
          shape: 'legacy',
          filePath: legacyPath(sessionId)
        }
      });
      await expect(manager.getById(sessionId)).rejects.toMatchObject({ kind, status: 422 });
      expect(await listFilesRecursively(sessionRoot)).toEqual(filesBefore);
      await expectBytesUnchanged(seededBytes);
    }
  );

  it('keeps SESSION_NOT_FOUND 404 for an absent session', async () => {
    const manager = new FileSessionManager();

    await expect(manager.resume('sess_v2_absent')).rejects.toMatchObject({
      name: 'SessionRecordAccessError',
      type: 'SESSION_NOT_FOUND',
      status: 404,
      kind: 'missing',
      details: { sessionId: 'sess_v2_absent', kind: 'missing' }
    });
  });

  it('prefers the canonical duplicate, preserves legacy-only fields, and materializes them into the canonical folder only', async () => {
    const manager = new FileSessionManager();

    const session = await manager.getById('sess_v2_duplicate');

    expect(session).toMatchObject({
      sessionId: 'sess_v2_duplicate',
      engineSessionId: 'engine_fixture_duplicate_canonical',
      updatedAt: '2026-08-30T12:45:00.000Z',
      model: 'fixture-model',
      engineSelection: {
        adapterId: 'claude-agent-sdk',
        providerId: 'anthropic',
        model: 'fixture-model'
      },
      claudeSessionId: 'engine_fixture_duplicate_legacy',
      sdkPackageVersion: '0.3.150',
      instructionPath: 'agents/AGENT_WORKING_ITEMS.md',
      instructionHash: 'fixture-instruction-hash'
    });
    expect(session.adapterSession).toEqual({
      engineSessionId: 'engine_fixture_duplicate_canonical',
      packageName: '@anthropic-ai/claude-agent-sdk',
      packageVersion: '0.3.150'
    });

    const persisted = await readCanonical('sess_v2_duplicate');
    expect(persisted).toMatchObject({
      engineSessionId: 'engine_fixture_duplicate_canonical',
      instructionPath: 'agents/AGENT_WORKING_ITEMS.md',
      claudeSessionId: 'engine_fixture_duplicate_legacy',
      legacySource: {
        sha256: sha256(seededBytes.get('sess_v2_duplicate.json') as Buffer),
        materializedAt: expect.stringMatching(/^\d{4}-\d{2}-\d{2}T/)
      }
    });
    await expectBytesUnchanged(seededBytes, ['sess_v2_duplicate.json', 'sess_v2_duplicate/events.jsonl']);

    const afterFirst = await snapshotBytes(sessionRoot);
    await expect(manager.inspect('sess_v2_duplicate')).resolves.toMatchObject({
      kind: 'ok',
      materialized: false
    });
    await expectBytesUnchanged(afterFirst);
  });

  it('does not resurrect a legacy-only field removed from the canonical record once the legacy source is consumed', async () => {
    const manager = new FileSessionManager();
    const first = await manager.getById('sess_v2_duplicate');
    expect(first).toHaveProperty('instructionPath', 'agents/AGENT_WORKING_ITEMS.md');
    expect(first).toHaveProperty('legacySource');

    // A writer clears the legacy-only field on the canonical record.
    const saved = await manager.save('sess_v2_duplicate', { instructionPath: undefined });
    expect(saved.instructionPath).toBeUndefined();
    expect(await readCanonical('sess_v2_duplicate')).not.toHaveProperty('instructionPath');
    const afterSave = await snapshotBytes(sessionRoot);

    const again = await manager.getById('sess_v2_duplicate');
    const inspected = await manager.inspect('sess_v2_duplicate');
    const listed = await manager.listWithDiagnostics(projectRoot);

    expect(again).not.toHaveProperty('instructionPath');
    expect(again).toMatchObject({
      instructionHash: 'fixture-instruction-hash',
      claudeSessionId: 'engine_fixture_duplicate_legacy'
    });
    expect(inspected).toMatchObject({ kind: 'ok', materialized: false, diagnostics: [] });
    expect(listed.sessions.find((session) => session.sessionId === 'sess_v2_duplicate')).not.toHaveProperty(
      'instructionPath'
    );
    expect(listed.diagnostics).toEqual([]);
    expect(await readCanonical('sess_v2_duplicate')).not.toHaveProperty('instructionPath');
    await expectBytesUnchanged(afterSave);
    await expectBytesUnchanged(seededBytes, ['sess_v2_duplicate.json', 'sess_v2_duplicate/events.jsonl']);
  });

  it('ignores a legacy flat record edited after it was consumed and reports a legacySourceChanged diagnostic', async () => {
    const manager = new FileSessionManager();
    const consumed = await manager.getById('sess_v2_readable');
    expect(consumed).toHaveProperty('legacySource');
    const afterFirst = await snapshotBytes(sessionRoot);

    const edited = `${JSON.stringify(
      {
        ...JSON.parse(await readFile(legacyPath('sess_v2_readable'), 'utf8')),
        resurrected: true,
        model: 'edited-after-materialization'
      },
      null,
      2
    )}\n`;
    await writeFile(legacyPath('sess_v2_readable'), edited, 'utf8');

    const inspected = await manager.inspect('sess_v2_readable');
    const session = await manager.resume('sess_v2_readable');
    const listed = await manager.listWithDiagnostics(projectRoot);

    expect(inspected).toMatchObject({
      kind: 'ok',
      materialized: false,
      siblingFailures: [],
      diagnostics: [
        expect.objectContaining({
          sessionId: 'sess_v2_readable',
          code: 'legacySourceChanged',
          shape: 'legacy',
          filePath: legacyPath('sess_v2_readable'),
          reason: expect.stringContaining(sha256(Buffer.from(edited, 'utf8')).slice(0, 12))
        })
      ]
    });
    expect(session).not.toHaveProperty('resurrected');
    expect(session).toHaveProperty('model', 'fixture-model');
    expect(listed.diagnostics).toEqual([
      expect.objectContaining({ sessionId: 'sess_v2_readable', code: 'legacySourceChanged' })
    ]);
    expect(listed.sessions.find((candidate) => candidate.sessionId === 'sess_v2_readable')).not.toHaveProperty(
      'resurrected'
    );
    await expect(readFile(legacyPath('sess_v2_readable'), 'utf8')).resolves.toBe(edited);
    await expectBytesUnchanged(afterFirst, ['sess_v2_readable/session.json']);
  });

  it('fails closed on a corrupt canonical record and never overwrites it from the legacy sibling', async () => {
    const manager = new FileSessionManager();
    const corruptCanonical = '{"sessionId": "sess_v2_readable", "projectRoot": ';
    await mkdir(canonicalDirectory('sess_v2_readable'), { recursive: true });
    await writeFile(canonicalPath('sess_v2_readable'), corruptCanonical, 'utf8');
    const filesBefore = await listFilesRecursively(sessionRoot);

    await expect(manager.inspect('sess_v2_readable')).resolves.toMatchObject({
      kind: 'malformed',
      failure: { shape: 'canonical', filePath: canonicalPath('sess_v2_readable') }
    });
    await expect(manager.resume('sess_v2_readable')).rejects.toMatchObject({
      kind: 'malformed',
      status: 422,
      details: { shape: 'canonical' }
    });
    const listed = await manager.listWithDiagnostics(projectRoot);
    expect(listed.sessions.map((session) => session.sessionId)).not.toContain('sess_v2_readable');
    expect(listed.failures).toContainEqual(
      expect.objectContaining({ sessionId: 'sess_v2_readable', kind: 'malformed', shape: 'canonical' })
    );

    await expect(readFile(canonicalPath('sess_v2_readable'), 'utf8')).resolves.toBe(corruptCanonical);
    await expectBytesUnchanged(seededBytes, ['sess_v2_readable.json']);
    expect(await listFilesRecursively(sessionRoot)).toEqual(filesBefore);
  });

  it('reports an unreadable legacy sibling beside a readable canonical record without failing the session', async () => {
    const manager = new FileSessionManager();
    const garbage = 'not json at all';
    await writeFile(legacyPath('sess_v2_duplicate'), garbage, 'utf8');

    const result = await manager.inspect('sess_v2_duplicate');

    expect(result).toMatchObject({
      kind: 'ok',
      materialized: false,
      session: { engineSessionId: 'engine_fixture_duplicate_canonical' },
      siblingFailures: [
        expect.objectContaining({
          sessionId: 'sess_v2_duplicate',
          kind: 'malformed',
          shape: 'legacy',
          filePath: legacyPath('sess_v2_duplicate')
        })
      ]
    });
    const listed = await manager.listWithDiagnostics(projectRoot);
    expect(listed.sessions.map((session) => session.sessionId)).toContain('sess_v2_duplicate');
    expect(listed.failures).toContainEqual(
      expect.objectContaining({ sessionId: 'sess_v2_duplicate', kind: 'malformed', shape: 'legacy' })
    );
    await expect(readFile(legacyPath('sess_v2_duplicate'), 'utf8')).resolves.toBe(garbage);
    await expectBytesUnchanged(seededBytes, ['sess_v2_duplicate/session.json']);
  });
});

describe('save', () => {
  it('writes only the canonical folder and leaves the legacy flat file byte-identical', async () => {
    const manager = new FileSessionManager();
    const filesBefore = await listFilesRecursively(sessionRoot);

    const saved = await manager.save('sess_v2_readable', { model: 'fixture-model-2' });

    expect(saved).toMatchObject({
      sessionId: 'sess_v2_readable',
      createdAt: '2026-08-30T12:00:00.000Z',
      model: 'fixture-model-2'
    });
    expect(await readCanonical('sess_v2_readable')).toMatchObject({
      model: 'fixture-model-2',
      legacySource: { sha256: sha256(seededBytes.get('sess_v2_readable.json') as Buffer) }
    });
    expect(await listFilesRecursively(sessionRoot)).toEqual(
      [...filesBefore, 'sess_v2_readable/session.json'].sort()
    );
    await expectBytesUnchanged(seededBytes, legacyFlatFiles(seededBytes));
  });
});

describe('delete', () => {
  it('removes the deleted session in both shapes and leaves every other legacy record byte-identical', async () => {
    const manager = new FileSessionManager();
    await manager.list(projectRoot);

    await manager.delete('sess_v2_readable');

    await expect(access(canonicalDirectory('sess_v2_readable'))).rejects.toThrow();
    await expect(access(legacyPath('sess_v2_readable'))).rejects.toThrow();
    await expect(manager.inspect('sess_v2_readable')).resolves.toEqual({
      kind: 'missing',
      sessionId: 'sess_v2_readable'
    });
    await expectBytesUnchanged(
      seededBytes,
      legacyFlatFiles(seededBytes).filter((file) => file !== 'sess_v2_readable.json')
    );
    await expectBytesUnchanged(seededBytes, ['sess_v2_duplicate/events.jsonl']);

    await manager.delete('sess_v2_duplicate');

    await expect(access(canonicalDirectory('sess_v2_duplicate'))).rejects.toThrow();
    await expect(access(legacyPath('sess_v2_duplicate'))).rejects.toThrow();
    await expectBytesUnchanged(seededBytes, [
      'sess_v2_malformed_truncated.json',
      'sess_v2_unsupported_version.json',
      'sess_v2_missing_version_fields.json',
      'sess_v2_other_project.json'
    ]);

    const remaining = await manager.listWithDiagnostics(projectRoot);
    expect(remaining.sessions).toEqual([]);
    expect(sortedFailures(remaining.failures).map((failure) => failure.sessionId)).toEqual([
      'sess_v2_malformed_truncated',
      'sess_v2_missing_version_fields',
      'sess_v2_unsupported_version'
    ]);
  });

  it('refuses to delete a record it cannot open and leaves its bytes untouched', async () => {
    const manager = new FileSessionManager();
    const filesBefore = await listFilesRecursively(sessionRoot);

    await expect(manager.delete('sess_v2_malformed_truncated')).rejects.toMatchObject({
      name: 'SessionRecordAccessError',
      kind: 'malformed',
      status: 422
    });
    await expect(manager.delete('sess_v2_unsupported_version')).rejects.toMatchObject({
      kind: 'unsupportedVersion',
      status: 422
    });
    await expect(manager.delete('sess_v2_absent')).rejects.toMatchObject({
      type: 'SESSION_NOT_FOUND',
      kind: 'missing',
      status: 404
    });

    expect(await listFilesRecursively(sessionRoot)).toEqual(filesBefore);
    await expectBytesUnchanged(seededBytes);
  });
});
