import { lstat, readFile, realpath, stat } from 'node:fs/promises';
import path from 'node:path';
import { writeTextFileAtomically } from '../atomic-write';
import { readDependencyRegister } from '../dependencies/register-reader';
import { serializeDependencyRegister } from '../dependencies/register-writer';
import {
  DELIVERABLE_ID_PATTERN,
  DependencyContractError,
  DependencyRegisterRow
} from '../dependencies/schema';
import { StatusParseError, parseStatusDocument } from '../lifecycle/status-parser';
import {
  LifecycleTransitionError,
  LifecycleTransitionOptions,
  transitionStatusFile
} from '../lifecycle/transition';
import {
  WorkspaceOperationError,
  WorkspaceValidationError,
  normalizeProjectRoot
} from './filesystem';

function requireNonEmptyPath(input: string, field: string): string {
  const trimmed = input.trim();
  if (!trimmed) {
    throw new WorkspaceValidationError('INVALID_PROJECT_ROOT', 400, `Missing or invalid '${field}'`);
  }
  if (!path.isAbsolute(trimmed)) {
    throw new WorkspaceValidationError(
      'INVALID_PROJECT_ROOT',
      400,
      `${field} must be an absolute filesystem path`
    );
  }
  return path.resolve(trimmed);
}

function assertWithinProjectRoot(projectRoot: string, candidatePath: string): void {
  const relative = path.relative(projectRoot, candidatePath);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new WorkspaceOperationError(
      'DELIVERABLE_PATH_OUTSIDE_PROJECT_ROOT',
      400,
      'deliverablePath must be inside projectRoot',
      { projectRoot, deliverablePath: candidatePath }
    );
  }
}

async function normalizeDeliverablePath(
  projectRoot: string,
  canonicalProjectRoot: string,
  deliverablePathInput: string
): Promise<string> {
  const deliverablePath = requireNonEmptyPath(deliverablePathInput, 'deliverablePath');
  assertWithinProjectRoot(projectRoot, deliverablePath);

  let deliverableStat;
  try {
    deliverableStat = await stat(deliverablePath);
  } catch {
    throw new WorkspaceOperationError(
      'DELIVERABLE_NOT_FOUND',
      404,
      'deliverablePath is not accessible',
      { deliverablePath }
    );
  }

  if (!deliverableStat.isDirectory()) {
    throw new WorkspaceOperationError(
      'DELIVERABLE_NOT_FOUND',
      404,
      'deliverablePath must point to a directory',
      { deliverablePath }
    );
  }

  let canonicalDeliverablePath: string;
  try {
    canonicalDeliverablePath = await realpath(deliverablePath);
  } catch {
    throw new WorkspaceOperationError(
      'DELIVERABLE_NOT_FOUND',
      404,
      'deliverablePath is not accessible',
      { deliverablePath }
    );
  }

  assertWithinProjectRoot(canonicalProjectRoot, canonicalDeliverablePath);
  return canonicalDeliverablePath;
}

async function normalizeCanonicalProjectRoot(projectRoot: string): Promise<string> {
  try {
    return await realpath(projectRoot);
  } catch {
    throw new WorkspaceValidationError(
      'WORKING_ROOT_INACCESSIBLE',
      404,
      'projectRoot is not accessible'
    );
  }
}

function getDeliverableIdFromPath(deliverablePath: string): string | undefined {
  const directoryName = path.basename(deliverablePath);
  const match = directoryName.match(/^DEL-\d{2,3}-\d{2}/);
  if (!match) {
    return undefined;
  }

  const candidate = match[0];
  return DELIVERABLE_ID_PATTERN.test(candidate) ? candidate : undefined;
}

function getErrnoCode(error: unknown): string | undefined {
  if (typeof error !== 'object' || error === null) {
    return undefined;
  }

  const code = (error as NodeJS.ErrnoException).code;
  return typeof code === 'string' ? code : undefined;
}

async function isRegularFilePresent(filePath: string): Promise<boolean> {
  try {
    const fileStat = await stat(filePath);
    return fileStat.isFile();
  } catch (error) {
    const errnoCode = getErrnoCode(error);
    if (errnoCode === 'ENOENT') {
      return false;
    }
    throw new WorkspaceOperationError('WORKSPACE_FILE_READ_FAILED', 500, 'Unable to inspect file', {
      filePath,
      errnoCode
    });
  }
}

async function assertDependencyWriteLeafIsNotSymlink(filePath: string): Promise<void> {
  try {
    const fileStat = await lstat(filePath);
    if (fileStat.isSymbolicLink()) {
      throw new WorkspaceOperationError(
        'SYMLINK_WRITE_DENIED',
        403,
        'Writes to a symbolic-link Dependencies.csv are not allowed',
        { file: 'Dependencies.csv' }
      );
    }
  } catch (error) {
    if (error instanceof WorkspaceOperationError) {
      throw error;
    }

    const errnoCode = getErrnoCode(error);
    if (errnoCode === 'ENOENT') {
      return;
    }

    throw new WorkspaceOperationError(
      'WORKSPACE_FILE_INSPECTION_FAILED',
      500,
      'Unable to inspect Dependencies.csv before writing',
      { file: 'Dependencies.csv', errnoCode }
    );
  }
}

async function readRequiredFile(
  filePath: string,
  notFoundCode: string,
  notFoundMessage: string
): Promise<string> {
  try {
    return await readFile(filePath, 'utf8');
  } catch (error) {
    const errnoCode = getErrnoCode(error);
    if (errnoCode === 'ENOENT') {
      throw new WorkspaceOperationError(notFoundCode, 404, notFoundMessage, { filePath });
    }
    throw new WorkspaceOperationError('WORKSPACE_FILE_READ_FAILED', 500, 'Unable to read file', {
      filePath,
      errnoCode
    });
  }
}

export interface DeliverableStatusSnapshot {
  projectRoot: string;
  deliverablePath: string;
  statusFilePath: string;
  status: ReturnType<typeof parseStatusDocument>;
}

export async function readDeliverableStatus(
  projectRootInput: string,
  deliverablePathInput: string
): Promise<DeliverableStatusSnapshot> {
  const projectRoot = await normalizeProjectRoot(projectRootInput);
  const canonicalProjectRoot = await normalizeCanonicalProjectRoot(projectRoot);
  const deliverablePath = await normalizeDeliverablePath(
    projectRoot,
    canonicalProjectRoot,
    deliverablePathInput
  );
  const statusFilePath = path.join(deliverablePath, '_STATUS.md');
  const content = await readRequiredFile(
    statusFilePath,
    'STATUS_FILE_NOT_FOUND',
    '_STATUS.md is not accessible in deliverablePath'
  );

  try {
    return {
      projectRoot,
      deliverablePath,
      statusFilePath,
      status: parseStatusDocument(content)
    };
  } catch (error) {
    if (error instanceof StatusParseError) {
      throw new WorkspaceOperationError(error.code, 400, error.message, {
        statusFilePath,
        parseDetails: error.details
      });
    }
    throw error;
  }
}

export interface DeliverableContentResult {
  projectRoot: string;
  deliverablePath: string;
  /** The relative path within the deliverable that was actually served. */
  file: string;
  filePath: string;
  content: string;
}

/** Default document served when no `file` is requested; always present per the lifecycle contract. */
export const DEFAULT_DELIVERABLE_CONTENT_FILE = '_STATUS.md';

/**
 * Read a single document file from within a deliverable directory (D-APP-20
 * Option B: read-only, keyed by `deliverablePath` + a validated relative `file`).
 * The deliverable directory is normalized and canonicalized first; the requested
 * `file` must be relative and must resolve — lexically AND after symlink
 * resolution — inside that canonical directory, so it can never escape the
 * deliverable (or the project root, which already contains it).
 */
export async function readDeliverableContent(input: {
  projectRoot: string;
  deliverablePath: string;
  file?: string;
}): Promise<DeliverableContentResult> {
  const projectRoot = await normalizeProjectRoot(input.projectRoot);
  const canonicalProjectRoot = await normalizeCanonicalProjectRoot(projectRoot);
  const deliverablePath = await normalizeDeliverablePath(
    projectRoot,
    canonicalProjectRoot,
    input.deliverablePath
  );

  const requestedFile = (input.file ?? '').trim() || DEFAULT_DELIVERABLE_CONTENT_FILE;
  if (path.isAbsolute(requestedFile)) {
    throw new WorkspaceOperationError(
      'DELIVERABLE_FILE_OUTSIDE_DELIVERABLE',
      400,
      'file must be a relative path inside the deliverable',
      { file: requestedFile }
    );
  }

  const candidatePath = path.resolve(deliverablePath, requestedFile);
  const lexicalRelative = path.relative(deliverablePath, candidatePath);
  if (lexicalRelative.startsWith('..') || path.isAbsolute(lexicalRelative)) {
    throw new WorkspaceOperationError(
      'DELIVERABLE_FILE_OUTSIDE_DELIVERABLE',
      400,
      'file must resolve inside the deliverable directory',
      { file: requestedFile }
    );
  }

  let canonicalFilePath: string;
  try {
    canonicalFilePath = await realpath(candidatePath);
  } catch {
    throw new WorkspaceOperationError(
      'DELIVERABLE_CONTENT_NOT_FOUND',
      404,
      'file is not accessible in the deliverable',
      { file: requestedFile }
    );
  }

  const canonicalRelative = path.relative(deliverablePath, canonicalFilePath);
  if (canonicalRelative.startsWith('..') || path.isAbsolute(canonicalRelative)) {
    throw new WorkspaceOperationError(
      'DELIVERABLE_FILE_OUTSIDE_DELIVERABLE',
      400,
      'file must resolve inside the deliverable directory',
      { file: requestedFile }
    );
  }

  let fileStat;
  try {
    fileStat = await stat(canonicalFilePath);
  } catch {
    // A race (e.g. the file is unlinked between realpath and stat) must surface
    // as the same typed 404 as the other not-found paths, not an opaque 500 that
    // leaks the raw error message — mirrors the realpath catch above.
    throw new WorkspaceOperationError(
      'DELIVERABLE_CONTENT_NOT_FOUND',
      404,
      'file is not accessible in the deliverable',
      { file: requestedFile }
    );
  }
  if (!fileStat.isFile()) {
    throw new WorkspaceOperationError(
      'DELIVERABLE_CONTENT_NOT_FOUND',
      404,
      'file must point to a regular file in the deliverable',
      { file: requestedFile }
    );
  }

  const content = await readRequiredFile(
    canonicalFilePath,
    'DELIVERABLE_CONTENT_NOT_FOUND',
    'file is not accessible in the deliverable'
  );

  return {
    projectRoot,
    deliverablePath,
    file: canonicalRelative,
    filePath: canonicalFilePath,
    content
  };
}

export interface DeliverableStatusTransitionInput extends LifecycleTransitionOptions {
  projectRoot: string;
  deliverablePath: string;
  targetState: string;
  actor: string;
}

export interface DeliverableStatusTransitionResult extends DeliverableStatusSnapshot {
  transition: {
    from: string;
    to: string;
    actor: string;
  };
}

export async function transitionDeliverableStatus(
  input: DeliverableStatusTransitionInput
): Promise<DeliverableStatusTransitionResult> {
  const projectRoot = await normalizeProjectRoot(input.projectRoot);
  const canonicalProjectRoot = await normalizeCanonicalProjectRoot(projectRoot);
  const deliverablePath = await normalizeDeliverablePath(
    projectRoot,
    canonicalProjectRoot,
    input.deliverablePath
  );
  const statusFilePath = path.join(deliverablePath, '_STATUS.md');

  try {
    const transition = await transitionStatusFile(
      statusFilePath,
      input.targetState,
      input.actor,
      {
        date: input.date,
        metadata: input.metadata,
        approvalSha: input.approvalSha
      }
    );

    return {
      projectRoot,
      deliverablePath,
      statusFilePath,
      transition: {
        from: transition.from,
        to: transition.to,
        actor: transition.actor
      },
      status: parseStatusDocument(transition.content)
    };
  } catch (error) {
    const errnoCode = getErrnoCode(error);
    if (errnoCode === 'ENOENT') {
      throw new WorkspaceOperationError(
        'STATUS_FILE_NOT_FOUND',
        404,
        '_STATUS.md is not accessible in deliverablePath',
        { statusFilePath }
      );
    }
    if (error instanceof LifecycleTransitionError) {
      throw new WorkspaceOperationError(error.code, 400, error.message, error.details);
    }
    if (error instanceof StatusParseError) {
      throw new WorkspaceOperationError(error.code, 400, error.message, error.details);
    }
    throw error;
  }
}

export interface DeliverableDependenciesSnapshot {
  projectRoot: string;
  deliverablePath: string;
  dependenciesFilePath: string;
  dependenciesSummaryPath?: string;
  registerPresent: boolean;
  secondarySummaryPresent: boolean;
  headers: string[];
  rows: DependencyRegisterRow[];
  warnings: string[];
}

export async function readDeliverableDependencies(
  projectRootInput: string,
  deliverablePathInput: string
): Promise<DeliverableDependenciesSnapshot> {
  const projectRoot = await normalizeProjectRoot(projectRootInput);
  const canonicalProjectRoot = await normalizeCanonicalProjectRoot(projectRoot);
  const deliverablePath = await normalizeDeliverablePath(
    projectRoot,
    canonicalProjectRoot,
    deliverablePathInput
  );
  const dependenciesFilePath = path.join(deliverablePath, 'Dependencies.csv');
  const dependenciesSummaryPath = path.join(deliverablePath, '_DEPENDENCIES.md');
  const secondarySummaryPresent = await isRegularFilePresent(dependenciesSummaryPath);
  let csv: string;

  try {
    csv = await readFile(dependenciesFilePath, 'utf8');
  } catch (error) {
    const errnoCode = getErrnoCode(error);
    if (errnoCode !== 'ENOENT') {
      throw new WorkspaceOperationError(
        'WORKSPACE_FILE_READ_FAILED',
        500,
        'Unable to read Dependencies.csv',
        { dependenciesFilePath, errnoCode }
      );
    }

    return {
      projectRoot,
      deliverablePath,
      dependenciesFilePath,
      dependenciesSummaryPath: secondarySummaryPresent ? dependenciesSummaryPath : undefined,
      registerPresent: false,
      secondarySummaryPresent,
      headers: [],
      rows: [],
      warnings: [
        secondarySummaryPresent
          ? 'DEPENDENCY_REGISTER_NOT_FOUND: Dependencies.csv is absent; _DEPENDENCIES.md is present as a secondary summary, but no structured rows were inferred.'
          : 'DEPENDENCY_REGISTER_NOT_FOUND: Dependencies.csv is absent and _DEPENDENCIES.md is absent; no structured dependency rows are available.'
      ]
    };
  }

  const parsed = readDependencyRegister(csv);
  return {
    projectRoot,
    deliverablePath,
    dependenciesFilePath,
    dependenciesSummaryPath: secondarySummaryPresent ? dependenciesSummaryPath : undefined,
    registerPresent: true,
    secondarySummaryPresent,
    headers: parsed.headers,
    rows: parsed.rows,
    warnings: parsed.warnings
  };
}

export interface WriteDeliverableDependenciesInput {
  projectRoot: string;
  deliverablePath: string;
  rows: DependencyRegisterRow[];
}

export async function writeDeliverableDependencies(
  input: WriteDeliverableDependenciesInput
): Promise<DeliverableDependenciesSnapshot> {
  const projectRoot = await normalizeProjectRoot(input.projectRoot);
  const canonicalProjectRoot = await normalizeCanonicalProjectRoot(projectRoot);
  const deliverablePath = await normalizeDeliverablePath(
    projectRoot,
    canonicalProjectRoot,
    input.deliverablePath
  );
  const dependenciesFilePath = path.join(deliverablePath, 'Dependencies.csv');
  const dependenciesSummaryPath = path.join(deliverablePath, '_DEPENDENCIES.md');
  await assertDependencyWriteLeafIsNotSymlink(dependenciesFilePath);
  const secondarySummaryPresent = await isRegularFilePresent(dependenciesSummaryPath);
  const hostDeliverableId = getDeliverableIdFromPath(deliverablePath);

  let previousRows: DependencyRegisterRow[] | undefined;
  let readWarnings: string[] = [];

  try {
    const existingCsv = await readFile(dependenciesFilePath, 'utf8');
    const existing = readDependencyRegister(existingCsv);
    previousRows = existing.rows;
    readWarnings = existing.warnings;
  } catch (error) {
    const errnoCode = getErrnoCode(error);
    if (errnoCode !== 'ENOENT') {
      throw new WorkspaceOperationError(
        'WORKSPACE_FILE_READ_FAILED',
        500,
        'Unable to read existing Dependencies.csv',
        { dependenciesFilePath, errnoCode }
      );
    }
  }

  try {
    const serialized = serializeDependencyRegister(input.rows, {
      hostDeliverableId,
      previousRows
    });
    await writeTextFileAtomically(dependenciesFilePath, serialized.csv);

    const parsed = readDependencyRegister(serialized.csv);
    return {
      projectRoot,
      deliverablePath,
      dependenciesFilePath,
      dependenciesSummaryPath: secondarySummaryPresent ? dependenciesSummaryPath : undefined,
      registerPresent: true,
      secondarySummaryPresent,
      headers: parsed.headers,
      rows: parsed.rows,
      warnings: [...readWarnings, ...serialized.warnings, ...parsed.warnings]
    };
  } catch (error) {
    if (error instanceof DependencyContractError) {
      throw new WorkspaceOperationError(error.code, 400, error.message, error.details);
    }
    throw error;
  }
}
