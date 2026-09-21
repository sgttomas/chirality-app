import { createHash } from 'node:crypto';
import { constants } from 'node:fs';
import { lstat, realpath, readdir, open, mkdir, mkdtemp, link, rm } from 'node:fs/promises';
import path from 'node:path';
import { tmpdir } from 'node:os';
import { discoverMethodCatalog, inspectMethod } from '@chirality/runtime-core';
import type { WorkflowDraft, WorkflowDraftSource } from '../../../../lib/harness/workflow-drafts';
import { FilePolicyError } from '../file/file-policy';

const NAME = /^(?=.{1,64}$)[a-z0-9]+(?:-[a-z0-9]+)*$/;
const LIMIT = 8 * 1024 * 1024;
function fail(code: string, status: number, message: string): never { throw new FilePolicyError(code, status, message); }
const hash = (bytes: Buffer | string) => createHash('sha256').update(bytes).digest('hex');
const missing = (error: unknown) => (error as NodeJS.ErrnoException).code === 'ENOENT';
export function validateDraftIdentity(name: unknown, source: unknown): asserts name is string {
  if (typeof name !== 'string' || !NAME.test(name) || !['project', 'user'].includes(String(source)))
    fail('INVALID_REQUEST', 400, 'Choose a canonical workflow name and project or user source.');
}
// Every component below the server-resolved root must be an ordinary directory.
async function directory(root: string, relative: string, create = false): Promise<string> {
  let target = root;
  for (const segment of relative.split('/').filter(Boolean)) {
    target = path.join(target, segment);
    if (create) { try { await mkdir(target); } catch (error) { if ((error as NodeJS.ErrnoException).code !== 'EEXIST') throw error; } }
    const info = await lstat(target);
    if (!info.isDirectory() || info.isSymbolicLink() || await realpath(target) !== target)
      fail('DRAFT_UNSAFE_PATH', 400, 'Workflow folders must be ordinary contained directories without symbolic links.');
  }
  return target;
}
interface CapturedFile { content: Buffer; mode: number }
type CapturedPackage = Map<string, CapturedFile>;

async function capture(root: string, relative: string): Promise<CapturedPackage> {
  const packageRoot = await directory(root, relative);
  const result: CapturedPackage = new Map();
  let size = 0;
  let entries = 0;
  async function visit(relativeDirectory: string, depth: number): Promise<void> {
    if (depth > 16) fail('DRAFT_TOO_LARGE', 413, 'Workflow package exceeds the directory depth limit.');
    const base = await directory(root, [relative, relativeDirectory].filter(Boolean).join('/'));
    for (const child of (await readdir(base)).sort()) {
      if (++entries > 256) fail('DRAFT_TOO_LARGE', 413, 'Workflow package exceeds 256 entries.');
      if (/[\\\x00-\x1f]/.test(child)) fail('DRAFT_UNSAFE_PATH', 400, 'Workflow resource names contain unsupported characters.');
      const resource = relativeDirectory ? `${relativeDirectory}/${child}` : child;
      const target = path.join(packageRoot, resource);
      const info = await lstat(target);
      if (info.isSymbolicLink()) fail('DRAFT_UNSAFE_PATH', 400, 'Workflow packages cannot include symbolic links.');
      if (info.isDirectory()) { await visit(resource, depth + 1); continue; }
      if (!info.isFile() || info.nlink !== 1) fail('DRAFT_UNSAFE_PATH', 400, 'Workflow packages require ordinary files without links.');
      size += info.size;
      if (size > LIMIT) fail('DRAFT_TOO_LARGE', 413, 'Workflow package exceeds 8 MB.');
      const handle = await open(target, constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK);
      try {
        const opened = await handle.stat();
        if (opened.ino !== info.ino || opened.dev !== info.dev || !opened.isFile()) fail('DRAFT_CHANGED', 409, 'Workflow draft changed while reading. Refresh its review.');
        const bytes = Buffer.alloc(info.size + 1);
        let offset = 0;
        while (offset < bytes.length) { const read = await handle.read(bytes, offset, bytes.length - offset, offset); if (!read.bytesRead) break; offset += read.bytesRead; }
        const after = await handle.stat();
        if (offset !== info.size || after.mtimeMs !== info.mtimeMs || after.ctimeMs !== info.ctimeMs || after.mode !== info.mode)
          fail('DRAFT_CHANGED', 409, 'Workflow draft changed while reading. Refresh its review.');
        await directory(root, [relative, relativeDirectory].filter(Boolean).join('/'));
        result.set(resource, { content: bytes.subarray(0, offset), mode: info.mode & 0o777 });
      } finally { await handle.close(); }
    }
  }
  await visit('', 0);
  return result;
}
function inventory(bytes: CapturedPackage): WorkflowDraft['files'] {
  return [...bytes].sort(([a], [b]) => a.localeCompare(b)).map(([file, { content, mode }]) => ({ path: file, sha256: hash(content), size: content.length, mode: mode.toString(8).padStart(4, '0') }));
}
function token(root: string, source: WorkflowDraftSource, name: string, bytes: CapturedPackage): string {
  return hash(JSON.stringify({ root, source, name, files: inventory(bytes) }));
}
async function writePackage(root: string, name: string, bytes: CapturedPackage): Promise<void> {
  for (const [file, { content, mode }] of bytes) {
    const target = path.join(root, name, file);
    await mkdir(path.dirname(target), { recursive: true });
    const handle = await open(target, 'wx', 0o600);
    try {
      await handle.writeFile(content);
      // Apply ordinary permissions after writing so umask cannot remove reviewed
      // executable bits. Never propagate setuid, setgid, or sticky bits.
      await handle.chmod(mode & 0o777);
    } finally { await handle.close(); }
  }
}
async function metadata(name: string, source: WorkflowDraftSource, bytes: CapturedPackage) {
  const entry = bytes.get('WORKFLOW.md')?.content;
  if (!entry || entry.includes(0) || !Buffer.from(entry.toString('utf8')).equals(entry))
    fail('INVALID_DRAFT', 400, `Draft ${name} requires a UTF-8 WORKFLOW.md entrypoint.`);
  // Parse captured bounded bytes using Runtime's canonical metadata implementation.
  const temp = await mkdtemp(path.join(await realpath(tmpdir()), 'chirality-draft-review-'));
  try {
    await writePackage(path.join(temp, 'drafts'), name, bytes);
    const catalog = await discoverMethodCatalog([{ sourceRootId: 'draft-review', source, rootPath: temp, workflowDirectory: 'drafts' }]);
    const method = catalog.entries.find(value => value.descriptor.name === name);
    if (!method || catalog.blocked.length) fail('INVALID_DRAFT', 400, `Draft ${name} has invalid workflow metadata. Correct it in chat and refresh.`);
    const inspected = await inspectMethod(method);
    return { content: inspected.entrypoint.content, description: method.descriptor.description };
  } finally { await rm(temp, { recursive: true, force: true }); }
}
async function exists(root: string, name: string): Promise<boolean> {
  try { await directory(root, '.chirality/workflows'); } catch (error) { if (missing(error)) return false; throw error; }
  try { await lstat(path.join(root, '.chirality/workflows', name)); return true; } catch (error) { if (missing(error)) return false; throw error; }
}
export async function readWorkflowDraft(root: string, name: string, source: WorkflowDraftSource): Promise<WorkflowDraft> {
  validateDraftIdentity(name, source);
  const bytes = await capture(root, `.chirality/workflow-drafts/${name}`);
  const parsed = await metadata(name, source, bytes);
  const files = inventory(bytes).map(file => {
    const resource = bytes.get(file.path)!.content;
    const content = resource.toString('utf8');
    return file.path !== 'WORKFLOW.md' && resource.length <= 512 * 1024 && !/[\x00-\x08\x0b\x0c\x0e-\x1f]/.test(content) && Buffer.from(content).equals(resource)
      ? { ...file, content } : file;
  });
  const destinationExists = await exists(root, name);
  let registered = false;
  if (destinationExists) {
    try { registered = JSON.stringify(inventory(await capture(root, `.chirality/workflows/${name}`))) === JSON.stringify(inventory(bytes)); }
    catch (error) {
      // An existing invalid or incomplete package is still a visible name conflict.
      if (!(error instanceof FilePolicyError) && !missing(error)) throw error;
    }
  }
  return { name, source, ...parsed, files, reviewToken: token(root, source, name, bytes), destinationExists, registered };
}
export async function listDrafts(root: string, source: WorkflowDraftSource): Promise<WorkflowDraft[]> {
  let folder: string;
  try { folder = await directory(root, '.chirality/workflow-drafts'); } catch (error) { if (missing(error)) return []; throw error; }
  const drafts: WorkflowDraft[] = [];
  let totalBytes = 0;
  for (const item of (await readdir(folder, { withFileTypes: true })).sort((a, b) => a.name.localeCompare(b.name))) {
    if (item.name.startsWith('.') || (!item.isDirectory() && !item.isSymbolicLink())) continue;
    const name = item.name;
    if (drafts.length >= 100) fail('DRAFT_TOO_LARGE', 413, 'There are more than 100 workflow drafts.');
    validateDraftIdentity(name, source);
    const draft = await readWorkflowDraft(root, name, source);
    totalBytes += draft.files.reduce((sum, file) => sum + file.size, 0);
    if (totalBytes > 16 * 1024 * 1024) fail('DRAFT_TOO_LARGE', 413, 'Workflow draft listing exceeds 16 MB. Inspect one draft by name or reduce the pending drafts.');
    drafts.push(draft);
  }
  return drafts;
}
export async function registerDraft(root: string, name: string, source: WorkflowDraftSource, reviewToken: string) {
  validateDraftIdentity(name, source);
  if (typeof reviewToken !== 'string' || !/^[a-f0-9]{64}$/.test(reviewToken)) fail('INVALID_REQUEST', 400, 'Review this workflow draft before registering it.');
  const bytes = await capture(root, `.chirality/workflow-drafts/${name}`);
  if (token(root, source, name, bytes) !== reviewToken) fail('DRAFT_CHANGED', 409, 'Workflow draft changed since review. Refresh and review it again.');
  await metadata(name, source, bytes);
  const control = await directory(root, '.chirality', true);
  const stage = await mkdtemp(path.join(control, '.workflow-register-'));
  let destination: string | undefined;
  try {
    await writePackage(stage, name, bytes);
    const staged = await capture(root, `.chirality/${path.basename(stage)}/${name}`);
    const current = await capture(root, `.chirality/workflow-drafts/${name}`);
    if (token(root, source, name, staged) !== reviewToken || token(root, source, name, current) !== reviewToken)
      fail('DRAFT_CHANGED', 409, 'Workflow draft changed since review. Refresh and review it again.');
    const library = await directory(root, '.chirality/workflows', true);
    const target = path.join(library, name);
    try { await mkdir(target); } catch (error) { if ((error as NodeJS.ErrnoException).code === 'EEXIST') fail('WORKFLOW_EXISTS', 409, 'A workflow with this name already exists in this source. Choose a new name for the draft.'); throw error; }
    destination = target;
    // Exclusive reservation prevents competing registrations. Publish the entrypoint
    // last, so Runtime cannot discover an incomplete package. Never overwrite bytes.
    for (const [file] of staged) {
      if (file === 'WORKFLOW.md') continue;
      await directory(root, `.chirality/workflows/${name}/${path.posix.dirname(file) === '.' ? '' : path.posix.dirname(file)}`, true);
      await link(path.join(stage, name, file), path.join(target, file));
    }
    await directory(root, `.chirality/workflows/${name}`);
    await link(path.join(stage, name, 'WORKFLOW.md'), path.join(target, 'WORKFLOW.md'));
    destination = undefined;
    return { name, source, path: `.chirality/workflows/${name}/WORKFLOW.md` };
  } finally {
    if (destination) await rm(destination, { recursive: true, force: true });
    await rm(stage, { recursive: true, force: true });
  }
}
