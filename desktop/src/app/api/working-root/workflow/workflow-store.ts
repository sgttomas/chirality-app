import { lstat, realpath, opendir } from 'node:fs/promises';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { FilePolicyError, openDocument, TEXT_LIMIT } from '../file/file-policy';
import type { WorkflowFile, WorkflowList, WorkflowPreview } from './workflow-read-contract';

// Bound directory work, including ignored entries. Oversized scans fail explicitly,
// never return a truncated list as complete. This is a resource guard, not authority.
const SCAN_LIMIT = 500;
const changed = () => new FilePolicyError('WORKFLOW_CHANGED', 409, 'The workflow folder changed. Refresh and try again.');
export function validateWorkflowName(name: string): void {
  if (!name || !name.endsWith('.md') || /[\\/\x00-\x1f\x7f]/.test(name) || name === '.' || name === '..')
    throw new FilePolicyError('INVALID_WORKFLOW_PATH', 400, 'Choose a Markdown file directly inside .chirality/workflows.');
}
async function boundary(root: string) {
  const paths = [root, path.join(root, '.chirality'), path.join(root, '.chirality', 'workflows')];
  const entries = [];
  for (const target of paths) {
    const info = await lstat(target);
    if (info.isSymbolicLink() || !info.isDirectory() || await realpath(target) !== target)
      throw new FilePolicyError('WORKFLOW_FOLDER_INVALID', 403, 'The workflow folder must use ordinary directories inside the current folder.');
    entries.push({ target, dev: info.dev, ino: info.ino });
  }
  return entries;
}
type Boundary = Awaited<ReturnType<typeof boundary>>;
async function unchanged(root: string, before: Boundary) {
  const after = await boundary(root);
  if (after.some((item, i) => item.ino !== before[i].ino || item.dev !== before[i].dev)) throw changed();
}
async function openContained(root: string, name: string, instruction: string, before: Boundary) {
  validateWorkflowName(name);
  await unchanged(root, before);
  const target = `.chirality/workflows/${name}`;
  const expected = path.join(root, target);
  const entry = await lstat(expected);
  if (!entry.isFile() || entry.isSymbolicLink()) throw new FilePolicyError('WORKFLOW_FILE_INVALID', 403, 'Only ordinary Markdown files in the workflow folder can be opened.');
  const document = await openDocument({ projectRoot: root, target }, instruction);
  try {
    await unchanged(root, before);
    const after = await lstat(expected);
    if (document.canonicalRoot !== root || document.canonical !== expected || !after.isFile() || after.isSymbolicLink() ||
        after.ino !== document.info.ino || after.dev !== document.info.dev || entry.ino !== after.ino || entry.dev !== after.dev) throw changed();
    return document;
  } catch (error) { await document.handle.close(); throw error; }
}
function metadata(name: string, info: { size: number; mtime: Date }): WorkflowFile {
  return { name, path: `.chirality/workflows/${name}`, size: info.size, modifiedAt: info.mtime.toISOString() };
}
export async function listWorkflowFiles(root: string, instruction: string): Promise<WorkflowList> {
  let before: Boundary;
  try { before = await boundary(root); }
  catch (error) {
    if ((error as NodeJS.ErrnoException).code === 'ENOENT') {
      // A disappeared root is not an empty workflow directory.
      const rootInfo = await lstat(root);
      if (!rootInfo.isDirectory() || rootInfo.isSymbolicLink() || await realpath(root) !== root) throw changed();
      return { projectRoot: root, files: [], directoryMissing: true };
    }
    throw error;
  }
  const files: WorkflowFile[] = [];
  try {
    const directory = await opendir(before[2].target);
    let count = 0;
    for await (const entry of directory) {
      if (++count > SCAN_LIMIT) throw new FilePolicyError('WORKFLOW_SCAN_LIMIT', 413, 'This folder is too large to list safely. Keep at most 500 entries in .chirality/workflows and refresh.');
      if (!entry.name.endsWith('.md')) continue;
      // Enumeration is only candidate discovery. Never expose a candidate name
      // or its error until an independently contained regular descriptor exists.
      const document = await openContained(root, entry.name, instruction, before);
      try { files.push(metadata(entry.name, document.info)); }
      finally { await document.handle.close(); }
    }
    await unchanged(root, before);
    files.sort((a, b) => a.name.localeCompare(b.name));
    return { projectRoot: root, files, directoryMissing: false };
  } catch (error) {
    if (error instanceof FilePolicyError && error.code === 'WORKFLOW_SCAN_LIMIT') throw error;
    throw new FilePolicyError('WORKFLOW_SCAN_FAILED', 409, 'The workflow folder could not be listed safely. Check that it contains ordinary files, then refresh.');
  }
}
export async function readWorkflowFile(root: string, name: string, instruction: string): Promise<WorkflowPreview> {
  validateWorkflowName(name);
  const before = await boundary(root);
  const document = await openContained(root, name, instruction, before);
  try {
    const { handle, info } = document;
    if (info.size > TEXT_LIMIT) throw new FilePolicyError('TEXT_LIMIT_EXCEEDED', 413, 'This plan exceeds the 10 MB preview limit. Open a smaller Markdown file.');
    const bytes = Buffer.alloc(Math.min(info.size + 1, TEXT_LIMIT + 1));
    let offset = 0;
    while (offset < bytes.length) {
      const read = await handle.read(bytes, offset, bytes.length - offset, offset);
      if (!read.bytesRead) break;
      offset += read.bytesRead;
    }
    const after = await handle.stat();
    await unchanged(root, before);
    const entry = await lstat(document.canonical);
    if (!entry.isFile() || entry.isSymbolicLink() || entry.ino !== info.ino || entry.dev !== info.dev ||
        after.size !== info.size || after.mtimeMs !== info.mtimeMs || after.ctimeMs !== info.ctimeMs || offset !== info.size) throw changed();
    const contentBytes = bytes.subarray(0, offset);
    let content: string;
    try {
      if (contentBytes.includes(0)) throw new Error('binary');
      content = new TextDecoder('utf-8', { fatal: true }).decode(contentBytes);
    } catch { throw new FilePolicyError('WORKFLOW_TEXT_INVALID', 415, 'This plan is not readable UTF-8 Markdown. Save it as a text file and retry.'); }
    return { projectRoot: root, file: metadata(name, info), content, sha256: createHash('sha256').update(contentBytes).digest('hex') };
  } finally { await document.handle.close(); }
}
