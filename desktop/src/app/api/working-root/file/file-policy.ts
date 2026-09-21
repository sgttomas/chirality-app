import { constants } from 'node:fs';
import { access, open, realpath, stat } from 'node:fs/promises';
import path from 'node:path';

export const TEXT_LIMIT = 10 * 1024 * 1024;
export class FilePolicyError extends Error {
  constructor(public code: string, public status: number, message: string) { super(message); }
}
function within(root: string, target: string): boolean {
  const relative = path.relative(root, target);
  return relative === '' || (!relative.startsWith(`..${path.sep}`) && relative !== '..' && !path.isAbsolute(relative));
}
function forbidden(root: string, target: string, instruction: string): void {
  if (!within(root, target) || within(instruction, target) ||
      path.relative(root, target).split(path.sep).includes('.git')) {
    throw new FilePolicyError('FILE_FORBIDDEN', 403, 'File is outside the allowed Working Root.');
  }
}
/** Reveal-root is a separate directory operation; file reads and file opens remain regular-file-only. */
export async function validateRevealRoot(input: unknown, instructionRoot: string): Promise<string> {
  if (!input || typeof input !== 'object' || Array.isArray(input) || Object.hasOwn(input, 'target')) {
    throw new FilePolicyError('INVALID_REQUEST', 400, 'Root reveal requires a root without a file target.');
  }
  const root = (input as Record<string, unknown>).projectRoot;
  if (typeof root !== 'string' || !path.isAbsolute(root) || /[\x00-\x1f]/.test(root)) throw new FilePolicyError('INVALID_REQUEST', 400, 'Working Root must be an absolute directory path.');
  const normalized = path.resolve(root), instruction = path.resolve(instructionRoot);
  if (within(instruction, normalized)) throw new FilePolicyError('WORKING_ROOT_CONFLICT', 409, 'Working Root cannot be inside the instruction root.');
  const [canonical, canonicalInstruction] = await Promise.all([realpath(normalized), realpath(instruction)]);
  if (within(canonicalInstruction, canonical)) throw new FilePolicyError('WORKING_ROOT_CONFLICT', 409, 'Working Root cannot be inside the instruction root.');
  if (!(await stat(canonical)).isDirectory()) throw new FilePolicyError('WORKING_ROOT_INACCESSIBLE', 404, 'Working Root must be a directory.');
  await access(canonical, constants.R_OK | constants.W_OK);
  return canonical;
}

export async function validateDocumentTarget(input: unknown, instructionRoot: string) {
  if (!input || typeof input !== 'object' || Array.isArray(input)) throw new FilePolicyError('INVALID_REQUEST', 400, 'Expected a root and relative file path.');
  const { projectRoot, target } = input as Record<string, unknown>;
  if (typeof projectRoot !== 'string' || !path.isAbsolute(projectRoot) || /[\x00-\x1f]/.test(projectRoot) ||
      typeof target !== 'string' || !target || path.isAbsolute(target) || /[\x00-\x1f\\]/.test(target) ||
      target.split('/').some(segment => segment === '..' || segment === '.' || segment === '')) {
    throw new FilePolicyError('INVALID_REQUEST', 400, 'Expected an absolute root and a relative file path without traversal.');
  }
  const root = path.resolve(projectRoot), lexical = path.resolve(root, target);
  const instruction = path.resolve(instructionRoot);
  if (within(instruction, root)) throw new FilePolicyError('WORKING_ROOT_CONFLICT', 409, 'Working Root cannot be inside the instruction root.');
  forbidden(root, lexical, instruction);
  const [canonicalRoot, canonicalInstruction, canonical] = await Promise.all([realpath(root), realpath(instruction), realpath(lexical)]);
  if (within(canonicalInstruction, canonicalRoot)) throw new FilePolicyError('WORKING_ROOT_CONFLICT', 409, 'Working Root cannot be inside the instruction root.');
  forbidden(canonicalRoot, canonical, canonicalInstruction);
  if (!(await stat(canonicalRoot)).isDirectory()) throw new FilePolicyError('WORKING_ROOT_INACCESSIBLE', 404, 'Working Root must be a directory.');
  await access(canonicalRoot, constants.R_OK | constants.W_OK);
  const info = await stat(canonical);
  if (!info.isFile()) throw new FilePolicyError('NOT_REGULAR_FILE', 400, 'Only regular files can be viewed.');
  return { canonical, canonicalRoot, target, info };
}
/** Open a validated descriptor; reads stay bound to this inode, even after rename. */
export async function openDocument(input: unknown, instructionRoot: string) {
  const before = await validateDocumentTarget(input, instructionRoot);
  const handle = await open(before.canonical, constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK);
  try {
    const info = await handle.stat();
    const after = await validateDocumentTarget(input, instructionRoot);
    if (!info.isFile() || info.dev !== before.info.dev || info.ino !== before.info.ino ||
        info.dev !== after.info.dev || info.ino !== after.info.ino || before.canonical !== after.canonical) {
      throw new FilePolicyError('FILE_CHANGED', 409, 'File changed while opening. Retry the preview.');
    }
    return { ...after, info, handle };
  } catch (error) { await handle.close(); throw error; }
}
/**
 * Detect observable descriptor mutation during streaming. Size and mtime checks
 * do not provide snapshot isolation: a same-size edit with restored mtime can
 * remain indistinguishable without a separately approved locking/snapshot design.
 */
export async function assertOpenDocumentUnchanged(
  handle: { stat(): Promise<{ size: number; mtimeMs: number }> },
  expected: { size: number; mtimeMs: number },
  message = 'File changed while reading. Retry the preview.'
): Promise<void> {
  const current = await handle.stat();
  if (current.size !== expected.size || current.mtimeMs !== expected.mtimeMs) {
    throw new FilePolicyError('FILE_CHANGED', 409, message);
  }
}
export function createCloseOnce(closeDescriptor: () => Promise<void>): () => Promise<void> {
  let closed = false;
  return async () => {
    if (closed) return;
    closed = true;
    await closeDescriptor();
  };
}
export function fileError(error: unknown): { status: number; body: { error: { code: string; message: string } } } {
  if (error instanceof FilePolicyError) return { status: error.status, body: { error: { code: error.code, message: error.message } } };
  const code = (error as NodeJS.ErrnoException)?.code;
  if (code === 'ENOENT' || code === 'ENOTDIR') return { status: 404, body: { error: { code: 'FILE_NOT_FOUND', message: 'File or Working Root no longer exists.' } } };
  if (code === 'EACCES' || code === 'EPERM') return { status: 403, body: { error: { code: 'FILE_INACCESSIBLE', message: 'File cannot be accessed.' } } };
  if (code === 'ELOOP') return { status: 409, body: { error: { code: 'FILE_CHANGED', message: 'File link changed or is circular.' } } };
  return { status: 500, body: { error: { code: 'FILE_READ_FAILED', message: 'Unable to read the file.' } } };
}
export type DocumentHandoffDependencies<E> = {
  authorized: (event: E) => boolean;
  instructionRoot: () => string;
  preview: (event: E, target: string) => void;
  open: (target: string) => Promise<string>;
  reveal: (target: string) => void;
};
/** Shared boundary used by the actual main-process registration; no shell command bridge. */
export function createDocumentHandoffHandler<E>(deps: DocumentHandoffDependencies<E>) {
  return async (event: E, input: unknown) => {
    if (!deps.authorized(event)) return { ok: false, error: { code: 'UNAUTHORIZED_SENDER', message: 'Document action rejected for this sender.' } };
    try {
      const action = (input as { action?: unknown } | null)?.action;
      if (action === 'reveal-root') {
        const root = await validateRevealRoot(input, deps.instructionRoot());
        try { deps.reveal(root); } catch (error) { throw new FilePolicyError('REVEAL_FAILED', 502, error instanceof Error ? error.message : 'Unable to reveal folder.'); }
        return { ok: true };
      }
      if (action !== 'quick-look' && action !== 'open' && action !== 'reveal') throw new FilePolicyError('INVALID_REQUEST', 400, 'Unknown document action.');
      const document = await openDocument(input, deps.instructionRoot());
      try {
        // Native APIs take a path, so validate again immediately before handing it off.
        const current = await validateDocumentTarget(input, deps.instructionRoot());
        if (current.info.ino !== document.info.ino || current.info.dev !== document.info.dev) throw new FilePolicyError('FILE_CHANGED', 409, 'File changed before opening. Retry.');
        if (action === 'reveal') {
          try { deps.reveal(current.canonical); } catch (error) { throw new FilePolicyError('REVEAL_FAILED', 502, error instanceof Error ? error.message : 'Unable to reveal file.'); }
        } else if (action === 'quick-look') {
          try { deps.preview(event, current.canonical); }
          catch (error) { throw error instanceof FilePolicyError ? error : new FilePolicyError('PREVIEW_FAILED', 502, error instanceof Error ? error.message : 'Quick Look could not open this file.'); }
        }
        else {
          try {
            const error = await deps.open(current.canonical);
            if (error) throw new FilePolicyError('OPEN_FAILED', 502, error);
          } catch (error) { throw error instanceof FilePolicyError ? error : new FilePolicyError('OPEN_FAILED', 502, error instanceof Error ? error.message : 'Default app could not open this file.'); }
        }
      } finally { await document.handle.close(); }
      return { ok: true };
    } catch (error) { return { ok: false, ...fileError(error).body }; }
  };
}
