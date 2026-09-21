import { createHash, randomUUID } from 'node:crypto';
import { mkdir, readdir, readFile, rm, stat, writeFile, access } from 'node:fs/promises';
import { constants as fsConstants } from 'node:fs';
import path from 'node:path';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import { instructionRootContainsPath, resolveInstructionRootPath } from './instruction-root';
import { ISessionManager, SessionCreateRequest, SessionRecord } from '@chirality/runtime-contracts/types';

const DEFAULT_PERSONA = 'WORKING_ITEMS';
const DEFAULT_MODE = 'direct';
const CANONICAL_SESSION_FILE = 'session.json';
const LEGACY_SOURCE_FIELD = 'legacySource';
const MAX_FAILURE_REASON_LENGTH = 200;

type RawSessionRecord = SessionRecord & Record<string, unknown>;

/**
 * Where a session record was read from. `legacy` is the flat
 * `{sessionRoot}/{sessionId}.json` shape written by releases up to 2.0.0;
 * `canonical` is `{sessionRoot}/{sessionId}/session.json`.
 */
export type SessionRecordShape = 'legacy' | 'canonical';

/** Typed reasons a present session record cannot be opened. */
export type SessionRecordFailureKind = 'malformed' | 'unsupportedVersion';

/**
 * Consumption marker written into the canonical record when a legacy flat
 * record is materialized. Once present, the flat file is no longer a read
 * input: it is merged only when the marker is absent, and a later change to
 * the flat file is reported as a diagnostic rather than merged silently.
 */
export type LegacySourceMarker = {
  sha256: string;
  materializedAt: string;
};

/** Typed outcome of reading one session record file. Never throws for record content. */
export type SessionRecordReadResult =
  | {
      kind: 'ok';
      shape: SessionRecordShape;
      filePath: string;
      record: RawSessionRecord;
      sha256: string;
    }
  | { kind: 'missing'; shape: SessionRecordShape; filePath: string }
  | { kind: 'malformed'; shape: SessionRecordShape; filePath: string; reason: string }
  | {
      kind: 'unsupportedVersion';
      shape: SessionRecordShape;
      filePath: string;
      reason: string;
      schemaVersion: unknown;
      projectRoot?: string;
    };

/** One unreadable session record, attributed to its session id and file. */
export type SessionAccessFailure = {
  sessionId: string;
  kind: SessionRecordFailureKind;
  shape: SessionRecordShape;
  filePath: string;
  reason: string;
  schemaVersion?: unknown;
  projectRoot?: string;
};

/** Non-fatal observation about a readable session, for callers to label. */
export type SessionAccessDiagnostic = {
  sessionId: string;
  code: 'legacySourceChanged' | 'materializationFailed';
  shape: SessionRecordShape;
  filePath: string;
  reason: string;
};

/**
 * Typed outcome of accessing one session by id across both record shapes.
 *
 * - `ok` carries the resolved record. `materialized` is true when this
 *   access wrote the canonical `session.json` (first touch of a legacy-only
 *   record, or the one-time merge of legacy-only fields into an existing
 *   canonical record that carries no `legacySource` marker).
 *   `siblingFailures` lists an unreadable legacy flat file that sits beside a
 *   readable canonical record; `diagnostics` lists non-fatal observations
 *   (a legacy flat file changed after it was consumed, or a materialization
 *   write that failed while the record itself was readable).
 * - `missing` means neither shape exists.
 * - `malformed` / `unsupportedVersion` carry the failing record's identity.
 *
 * Access never rewrites, truncates, or deletes a legacy flat file; the only
 * write it may perform is into the canonical session folder.
 */
export type SessionAccessResult =
  | {
      kind: 'ok';
      sessionId: string;
      session: SessionRecord;
      materialized: boolean;
      siblingFailures: SessionAccessFailure[];
      diagnostics: SessionAccessDiagnostic[];
    }
  | { kind: 'missing'; sessionId: string }
  | { kind: 'malformed'; sessionId: string; failure: SessionAccessFailure }
  | { kind: 'unsupportedVersion'; sessionId: string; failure: SessionAccessFailure };

export type SessionAccessFailureResult = Exclude<SessionAccessResult, { kind: 'ok' }>;

/** `list` with the unreadable records and diagnostics it encountered instead of silently skipping them. */
export type SessionListResult = {
  sessions: SessionRecord[];
  failures: SessionAccessFailure[];
  diagnostics: SessionAccessDiagnostic[];
};

/**
 * Thrown by the throwing `ISessionManager` surfaces (`getById`, `resume`,
 * `save`, `delete`) when a session cannot be opened. The `HarnessErrorType`
 * union is Root-owned and has no dedicated member for an unreadable record,
 * so the wire type stays `SESSION_NOT_FOUND`; the discriminator is `kind`
 * (mirrored in `details.kind`) and the status is 404 only for `missing`.
 */
export class SessionRecordAccessError extends HarnessError {
  readonly kind: SessionAccessFailureResult['kind'];
  readonly sessionId: string;
  readonly failure?: SessionAccessFailure;

  constructor(result: SessionAccessFailureResult) {
    if (result.kind === 'missing') {
      super('SESSION_NOT_FOUND', 404, `Session '${result.sessionId}' does not exist`, {
        sessionId: result.sessionId,
        kind: 'missing'
      });
    } else {
      const { failure } = result;
      const problem =
        result.kind === 'malformed' ? 'is malformed' : 'has an unsupported schema version';
      super(
        'SESSION_NOT_FOUND',
        422,
        `Session '${result.sessionId}' record ${problem} (${failure.shape} ${failure.filePath}): ${failure.reason}`,
        { ...failure }
      );
      this.failure = failure;
    }
    this.name = 'SessionRecordAccessError';
    this.kind = result.kind;
    this.sessionId = result.sessionId;
  }
}

function getSessionStoreDirectory(): string {
  return process.env.CHIRALITY_SESSION_ROOT ?? path.join(process.cwd(), '.chirality', 'sessions');
}

async function ensureDirectoryExists(dirPath: string): Promise<void> {
  await mkdir(dirPath, { recursive: true });
}

export async function assertProjectRootAccessible(projectRoot: string): Promise<string> {
  if (!path.isAbsolute(projectRoot)) {
    throw new HarnessError(
      'INVALID_REQUEST',
      400,
      'projectRoot must be an absolute filesystem path',
      { projectRoot }
    );
  }

  const normalizedProjectRoot = path.resolve(projectRoot);
  const instructionRoot = resolveInstructionRootPath();
  if (instructionRootContainsPath(normalizedProjectRoot, instructionRoot)) {
    throw new HarnessError(
      'WORKING_ROOT_CONFLICT',
      409,
      'projectRoot cannot point inside instruction root',
      {
        projectRoot: normalizedProjectRoot,
        instructionRoot
      }
    );
  }

  try {
    const directoryStat = await stat(normalizedProjectRoot);
    if (!directoryStat.isDirectory()) {
      throw new HarnessError(
        'WORKING_ROOT_INACCESSIBLE',
        404,
        'projectRoot must point to an existing directory',
        { projectRoot: normalizedProjectRoot }
      );
    }
    await access(normalizedProjectRoot, fsConstants.R_OK | fsConstants.W_OK);
  } catch (error) {
    if (error instanceof HarnessError) {
      throw error;
    }
    throw new HarnessError('WORKING_ROOT_INACCESSIBLE', 404, 'projectRoot is not accessible', {
      projectRoot: normalizedProjectRoot
    });
  }

  return normalizedProjectRoot;
}

function assertSafeSessionId(sessionId: string): void {
  if (
    sessionId.trim().length === 0 ||
    sessionId === '.' ||
    sessionId === '..' ||
    sessionId.includes('/') ||
    sessionId.includes('\\')
  ) {
    throw new HarnessError('SESSION_NOT_FOUND', 404, `Session '${sessionId}' does not exist`, {
      sessionId
    });
  }
}

function getCanonicalSessionDirectoryPath(sessionId: string): string {
  assertSafeSessionId(sessionId);
  return path.join(getSessionStoreDirectory(), sessionId);
}

function getCanonicalSessionFilePath(sessionId: string): string {
  return path.join(getCanonicalSessionDirectoryPath(sessionId), CANONICAL_SESSION_FILE);
}

function getLegacySessionFilePath(sessionId: string): string {
  assertSafeSessionId(sessionId);
  return path.join(getSessionStoreDirectory(), `${sessionId}.json`);
}

function asRecord(value: unknown): Record<string, unknown> | undefined {
  return value && typeof value === 'object' && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : undefined;
}

function truncateReason(reason: string): string {
  return reason.length > MAX_FAILURE_REASON_LENGTH
    ? `${reason.slice(0, MAX_FAILURE_REASON_LENGTH)}…`
    : reason;
}

/**
 * Project-local session records written by releases through 2.0.0 carry no
 * `schemaVersion` field, so an absent version denotes the supported v2 shape.
 * Any declared version is refused with a typed `unsupportedVersion` state
 * instead of being guessed at; the Root-accepted daemon schema is consumed by
 * a later migration item, not by this manager.
 */
function isSupportedSchemaVersion(schemaVersion: unknown): boolean {
  return schemaVersion === undefined;
}

function hasRequiredV2Fields(record: Record<string, unknown>): boolean {
  return typeof record.projectRoot === 'string' && typeof record.createdAt === 'string';
}

async function readSessionRecordFile(
  filePath: string,
  shape: SessionRecordShape
): Promise<SessionRecordReadResult> {
  let bytes: Buffer;
  try {
    bytes = await readFile(filePath);
  } catch (error) {
    const code = (error as NodeJS.ErrnoException).code;
    if (code === 'ENOENT' || code === 'ENOTDIR') {
      return { kind: 'missing', shape, filePath };
    }
    return {
      kind: 'malformed',
      shape,
      filePath,
      reason: truncateReason(`record could not be read (${code ?? 'unknown error'})`)
    };
  }

  const raw = bytes.toString('utf8');
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return {
      kind: 'malformed',
      shape,
      filePath,
      reason: truncateReason(`invalid JSON: ${message}`)
    };
  }

  const record = asRecord(parsed);
  if (!record) {
    return {
      kind: 'malformed',
      shape,
      filePath,
      reason: 'record is not a JSON object'
    };
  }

  const projectRoot = typeof record.projectRoot === 'string' ? record.projectRoot : undefined;
  if (!isSupportedSchemaVersion(record.schemaVersion)) {
    return {
      kind: 'unsupportedVersion',
      shape,
      filePath,
      reason: truncateReason(
        `declared schemaVersion ${JSON.stringify(record.schemaVersion)} is not supported by this session manager`
      ),
      schemaVersion: record.schemaVersion,
      ...(projectRoot === undefined ? {} : { projectRoot })
    };
  }
  if (!hasRequiredV2Fields(record)) {
    return {
      kind: 'unsupportedVersion',
      shape,
      filePath,
      reason:
        'record declares no schemaVersion and lacks the required v2 fields (projectRoot, createdAt)',
      schemaVersion: undefined,
      ...(projectRoot === undefined ? {} : { projectRoot })
    };
  }

  return {
    kind: 'ok',
    shape,
    filePath,
    record: record as RawSessionRecord,
    sha256: createHash('sha256').update(bytes).digest('hex')
  };
}

function describeError(error: unknown): string {
  const code = (error as NodeJS.ErrnoException | undefined)?.code;
  if (typeof code === 'string' && code.length > 0) {
    return code;
  }
  return error instanceof Error ? error.message : String(error);
}

function readLegacySourceMarker(record: RawSessionRecord): LegacySourceMarker | undefined {
  const marker = asRecord(record[LEGACY_SOURCE_FIELD]);
  if (!marker || typeof marker.sha256 !== 'string' || typeof marker.materializedAt !== 'string') {
    return undefined;
  }
  return { sha256: marker.sha256, materializedAt: marker.materializedAt };
}

function withLegacySource(record: RawSessionRecord, sha256: string): RawSessionRecord {
  return {
    ...record,
    [LEGACY_SOURCE_FIELD]: { sha256, materializedAt: new Date().toISOString() }
  };
}

function toAccessFailure(
  sessionId: string,
  result: Extract<SessionRecordReadResult, { kind: SessionRecordFailureKind }>
): SessionAccessFailure {
  const failure: SessionAccessFailure = {
    sessionId,
    kind: result.kind,
    shape: result.shape,
    filePath: result.filePath,
    reason: result.reason
  };
  if (result.kind === 'unsupportedVersion') {
    failure.schemaVersion = result.schemaVersion;
    if (result.projectRoot !== undefined) {
      failure.projectRoot = result.projectRoot;
    }
  }
  return failure;
}

function isReadFailure(
  result: SessionRecordReadResult
): result is Extract<SessionRecordReadResult, { kind: SessionRecordFailureKind }> {
  return result.kind === 'malformed' || result.kind === 'unsupportedVersion';
}

function mergeSessionRecords(
  sessionId: string,
  legacyRecord: RawSessionRecord | undefined,
  canonicalRecord: RawSessionRecord | undefined
): RawSessionRecord | undefined {
  if (!legacyRecord && !canonicalRecord) {
    return undefined;
  }

  const merged: Record<string, unknown> = legacyRecord ? { ...legacyRecord } : {};
  if (canonicalRecord) {
    for (const [key, value] of Object.entries(canonicalRecord)) {
      if (value !== undefined) {
        merged[key] = value;
      }
    }
  }
  merged.sessionId = sessionId;

  return synthesizeProviderNeutralMetadata(merged as RawSessionRecord);
}

function hasSdkAttribution(session: RawSessionRecord): boolean {
  return (
    [
      session.sdkSessionId,
      session.sdkTranscriptPath,
      session.sdkSessionStoreKey,
      session.sdkConfigDir,
      session.sdkClaudeCodeVersion
    ].some((value) => typeof value === 'string' && value.trim().length > 0) ||
    (Array.isArray(session.sdkSettingSources) && session.sdkSettingSources.length > 0)
  );
}

function inferLegacyClaudeAdapter(
  session: RawSessionRecord
): 'anthropic-direct' | 'claude-agent-sdk' | undefined {
  const explicitSelection = asRecord(session.engineSelection);
  if (explicitSelection?.providerId === 'anthropic') {
    if (explicitSelection.adapterId === 'anthropic-direct') {
      return 'anthropic-direct';
    }
    if (explicitSelection.adapterId === 'claude-agent-sdk') {
      return 'claude-agent-sdk';
    }
  }
  if (explicitSelection) {
    return undefined;
  }

  if (hasSdkAttribution(session)) {
    return 'claude-agent-sdk';
  }

  const adapterSession = asRecord(session.adapterSession);
  if (adapterSession?.packageName === '@anthropic-ai/claude-agent-sdk') {
    return 'claude-agent-sdk';
  }
  if (adapterSession?.packageName === '@anthropic-ai/sdk') {
    return 'anthropic-direct';
  }

  const runtimeFingerprint = asRecord(session.runtimeFingerprint);
  const engineAdapter = asRecord(runtimeFingerprint?.engineAdapter);
  if (engineAdapter?.providerId === 'anthropic') {
    if (engineAdapter.adapterId === 'anthropic-direct') {
      return 'anthropic-direct';
    }
    if (engineAdapter.adapterId === 'claude-agent-sdk') {
      return 'claude-agent-sdk';
    }
  }

  return undefined;
}

function synthesizeProviderNeutralMetadata(session: RawSessionRecord): RawSessionRecord {
  const legacyEngineSessionId = [
    session.engineSessionId,
    session.sdkSessionId,
    session.claudeSessionId
  ].find((value): value is string => typeof value === 'string' && value.trim().length > 0);
  const inferredAdapterId = inferLegacyClaudeAdapter(session);

  // A claudeSessionId by itself is ambiguous: historical stub sessions used the
  // same field. Keep it readable, but leave selection to the current key-aware
  // runtime default instead of silently pinning the record to Anthropic.
  if (!legacyEngineSessionId || !inferredAdapterId) {
    return session;
  }

  const existingAdapterSession = asRecord(session.adapterSession);
  const existingEngineSessionId = existingAdapterSession?.engineSessionId;

  return {
    ...session,
    ...(session.engineSelection
      ? {}
      : {
          engineSelection: {
            adapterId: inferredAdapterId,
            providerId: 'anthropic',
            model: typeof session.model === 'string' ? session.model : ''
          }
        }),
    adapterSession: {
      transcriptPath: session.sdkTranscriptPath,
      storeKey: session.sdkSessionStoreKey,
      configDir: session.sdkConfigDir,
      packageName:
        inferredAdapterId === 'claude-agent-sdk'
          ? '@anthropic-ai/claude-agent-sdk'
          : '@anthropic-ai/sdk',
      packageVersion: session.sdkPackageVersion,
      ...existingAdapterSession,
      engineSessionId:
        typeof existingEngineSessionId === 'string'
          ? existingEngineSessionId
          : legacyEngineSessionId
    }
  };
}

async function writeCanonicalSession(
  sessionId: string,
  session: SessionRecord | RawSessionRecord
): Promise<void> {
  const sessionDirectory = getCanonicalSessionDirectoryPath(sessionId);
  await ensureDirectoryExists(sessionDirectory);
  await writeFile(
    getCanonicalSessionFilePath(sessionId),
    `${JSON.stringify(session, null, 2)}\n`,
    'utf8'
  );
}

/**
 * Lazy, non-destructive access to one session across both record shapes
 * (A13 retention posture).
 *
 * Precedence: a readable canonical record wins field-by-field over the legacy
 * flat record. Legacy-only fields are merged exactly once — when the
 * canonical record carries no `legacySource` marker — and the merged record
 * is written back with the marker (sha256 of the flat file bytes). Once the
 * marker is present the flat file is not a read input: an unchanged flat
 * file is ignored, a changed one is reported as a `legacySourceChanged`
 * diagnostic and still ignored, so a field removed from the canonical record
 * is never resurrected. A legacy-only record is materialized into a new
 * canonical folder (with the marker) on first touch. The legacy flat file is
 * never written, truncated, or removed here. A canonical record that cannot
 * be opened fails closed even when a readable legacy sibling exists, so a
 * corrupt canonical file is never overwritten from the flat shape.
 */
type ResolveSessionOptions = {
  /**
   * Normalized project root that limits canonical materialization: a record
   * bound to a different project root is returned read-only, so listing one
   * project never writes into another project's session folders.
   */
  materializeOnlyFor?: string;
  /** `false` resolves read-only (no canonical write at all); default `true`. */
  materialize?: boolean;
};

function mayMaterialize(record: RawSessionRecord, options: ResolveSessionOptions): boolean {
  return (
    options.materialize !== false &&
    (options.materializeOnlyFor === undefined ||
      path.resolve(record.projectRoot) === options.materializeOnlyFor)
  );
}

async function resolveSessionRecord(
  sessionId: string,
  options: ResolveSessionOptions = {}
): Promise<SessionAccessResult> {
  const legacyFilePath = getLegacySessionFilePath(sessionId);
  const canonicalFilePath = getCanonicalSessionFilePath(sessionId);
  const [legacy, canonical] = await Promise.all([
    readSessionRecordFile(legacyFilePath, 'legacy'),
    readSessionRecordFile(canonicalFilePath, 'canonical')
  ]);

  if (isReadFailure(canonical)) {
    return { kind: canonical.kind, sessionId, failure: toAccessFailure(sessionId, canonical) };
  }

  if (canonical.kind === 'ok') {
    const siblingFailures = isReadFailure(legacy) ? [toAccessFailure(sessionId, legacy)] : [];
    const diagnostics: SessionAccessDiagnostic[] = [];
    const canonicalOnly = mergeSessionRecords(sessionId, undefined, canonical.record) as RawSessionRecord;
    if (legacy.kind !== 'ok') {
      return { kind: 'ok', sessionId, session: canonicalOnly, materialized: false, siblingFailures, diagnostics };
    }

    const marker = readLegacySourceMarker(canonical.record);
    if (marker === undefined) {
      const merged = mergeSessionRecords(sessionId, legacy.record, canonical.record) as RawSessionRecord;
      if (!mayMaterialize(merged, options)) {
        return { kind: 'ok', sessionId, session: merged, materialized: false, siblingFailures, diagnostics };
      }
      const persisted = withLegacySource(merged, legacy.sha256);
      await writeCanonicalSession(sessionId, persisted);
      return { kind: 'ok', sessionId, session: persisted, materialized: true, siblingFailures, diagnostics };
    }

    if (marker.sha256 !== legacy.sha256) {
      diagnostics.push({
        sessionId,
        code: 'legacySourceChanged',
        shape: 'legacy',
        filePath: legacy.filePath,
        reason: `legacy flat record changed after it was materialized (consumed sha256 ${marker.sha256.slice(0, 12)}…, current ${legacy.sha256.slice(0, 12)}…); the canonical record is used and the flat record is ignored`
      });
    }
    return { kind: 'ok', sessionId, session: canonicalOnly, materialized: false, siblingFailures, diagnostics };
  }

  if (legacy.kind === 'ok') {
    const merged = mergeSessionRecords(sessionId, legacy.record, undefined) as RawSessionRecord;
    if (!mayMaterialize(merged, options)) {
      return { kind: 'ok', sessionId, session: merged, materialized: false, siblingFailures: [], diagnostics: [] };
    }
    const persisted = withLegacySource(merged, legacy.sha256);
    await writeCanonicalSession(sessionId, persisted);
    return { kind: 'ok', sessionId, session: persisted, materialized: true, siblingFailures: [], diagnostics: [] };
  }
  if (legacy.kind === 'missing') {
    return { kind: 'missing', sessionId };
  }
  return { kind: legacy.kind, sessionId, failure: toAccessFailure(sessionId, legacy) };
}

async function canonicalizeSessionRecord(sessionId: string): Promise<RawSessionRecord> {
  const result = await resolveSessionRecord(sessionId);
  if (result.kind !== 'ok') {
    throw new SessionRecordAccessError(result);
  }
  return result.session as RawSessionRecord;
}

export class FileSessionManager implements ISessionManager {
  async create(input: SessionCreateRequest): Promise<SessionRecord> {
    const projectRoot = await assertProjectRootAccessible(input.projectRoot);
    await ensureDirectoryExists(getSessionStoreDirectory());

    const now = new Date().toISOString();
    const session: SessionRecord = {
      sessionId: `sess_${randomUUID()}`,
      projectRoot,
      persona: input.persona?.trim() || DEFAULT_PERSONA,
      mode: input.mode?.trim() || DEFAULT_MODE,
      createdAt: now,
      updatedAt: now
    };

    await writeCanonicalSession(session.sessionId, session);
    return session;
  }

  /**
   * Typed access to one session. Performs the same lazy first-touch
   * materialization as `getById` but returns the failure state instead of
   * throwing, so callers can label unreadable records. Unsafe session ids
   * still reject with `SESSION_NOT_FOUND` before any path is resolved.
   */
  async inspect(sessionId: string): Promise<SessionAccessResult> {
    await ensureDirectoryExists(getSessionStoreDirectory());
    return resolveSessionRecord(sessionId);
  }

  async resume(sessionId: string): Promise<SessionRecord> {
    return this.getById(sessionId);
  }

  async getById(sessionId: string): Promise<SessionRecord> {
    await ensureDirectoryExists(getSessionStoreDirectory());
    return canonicalizeSessionRecord(sessionId);
  }

  async save(sessionId: string, updates: Partial<SessionRecord>): Promise<SessionRecord> {
    await ensureDirectoryExists(getSessionStoreDirectory());
    const existing = await canonicalizeSessionRecord(sessionId);
    const updated: SessionRecord = {
      ...existing,
      ...updates,
      sessionId: existing.sessionId,
      createdAt: existing.createdAt,
      updatedAt: new Date().toISOString()
    };

    await writeCanonicalSession(sessionId, updated);
    return updated;
  }

  /**
   * `list` plus the unreadable records and diagnostics found under the
   * session root. A readable record for another project root is excluded, as
   * before; an unreadable record is reported unless it declares a different
   * project root, because a malformed file cannot prove which project it
   * belongs to. A per-candidate I/O failure never aborts the listing: a
   * readable record whose materialization failed is listed unmaterialized
   * with a `materializationFailed` diagnostic.
   */
  async listWithDiagnostics(projectRoot: string): Promise<SessionListResult> {
    const normalizedProjectRoot = await assertProjectRootAccessible(projectRoot);
    await ensureDirectoryExists(getSessionStoreDirectory());

    const entries = await readdir(getSessionStoreDirectory(), { withFileTypes: true });
    const candidateSessionIds = new Set<string>();
    const sessions: SessionRecord[] = [];
    const failures: SessionAccessFailure[] = [];
    const diagnostics: SessionAccessDiagnostic[] = [];

    for (const entry of entries) {
      if (entry.isDirectory()) {
        candidateSessionIds.add(entry.name);
      } else if (entry.isFile() && entry.name.endsWith('.json')) {
        candidateSessionIds.add(entry.name.replace(/\.json$/, ''));
      }
    }

    const belongsToProject = (candidateRoot: string | undefined): boolean =>
      candidateRoot === undefined || path.resolve(candidateRoot) === normalizedProjectRoot;

    for (const sessionId of [...candidateSessionIds].sort()) {
      let result: SessionAccessResult;
      try {
        result = await resolveSessionRecord(sessionId, {
          materializeOnlyFor: normalizedProjectRoot
        });
      } catch (error) {
        if (error instanceof HarnessError) {
          if (error.type === 'SESSION_NOT_FOUND') {
            // Directory entries that are not safe session ids are not sessions.
            continue;
          }
          throw error;
        }
        // A materialization (canonical write) failure must not abort the
        // listing: re-resolve read-only and report what happened.
        const writeFailure = describeError(error);
        try {
          result = await resolveSessionRecord(sessionId, {
            materializeOnlyFor: normalizedProjectRoot,
            materialize: false
          });
        } catch (retryError) {
          failures.push({
            sessionId,
            kind: 'malformed',
            shape: 'legacy',
            filePath: getLegacySessionFilePath(sessionId),
            reason: truncateReason(`record could not be resolved (${describeError(retryError)})`)
          });
          continue;
        }
        if (result.kind === 'ok') {
          result = {
            ...result,
            diagnostics: [
              ...result.diagnostics,
              {
                sessionId,
                code: 'materializationFailed',
                shape: 'canonical',
                filePath: getCanonicalSessionFilePath(sessionId),
                reason: truncateReason(`record could not be materialized (${writeFailure})`)
              }
            ]
          };
        }
      }

      if (result.kind === 'ok') {
        if (path.resolve(result.session.projectRoot) === normalizedProjectRoot) {
          sessions.push(result.session);
          failures.push(...result.siblingFailures);
          diagnostics.push(...result.diagnostics);
        }
        continue;
      }
      if (result.kind === 'missing') {
        // A folder without session.json (for example an events-only orphan) is not a session.
        continue;
      }
      if (belongsToProject(result.failure.projectRoot)) {
        failures.push(result.failure);
      }
    }

    sessions.sort((a, b) => a.createdAt.localeCompare(b.createdAt));
    return { sessions, failures, diagnostics };
  }

  async list(projectRoot: string): Promise<SessionRecord[]> {
    return (await this.listWithDiagnostics(projectRoot)).sessions;
  }

  /**
   * Removes the deleted session's canonical folder and its legacy flat file.
   * A session that cannot be opened is not deleted: the typed failure is
   * thrown and every byte on disk is left as found.
   */
  async delete(sessionId: string): Promise<void> {
    await ensureDirectoryExists(getSessionStoreDirectory());

    await canonicalizeSessionRecord(sessionId);
    await rm(getCanonicalSessionDirectoryPath(sessionId), { recursive: true, force: true });
    await rm(getLegacySessionFilePath(sessionId), { force: true });
  }
}
