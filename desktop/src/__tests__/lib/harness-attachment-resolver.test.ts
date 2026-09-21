import { mkdtemp, mkdir, open, rm, symlink, writeFile, chmod } from 'node:fs/promises';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import { AttachmentResolver } from '../../lib/harness/attachment-resolver';

const BYTES_PER_MIB = 1024 * 1024;
const MAX_ATTACHMENT_BYTES = 10 * BYTES_PER_MIB;
const execFileAsync = promisify(execFile);

let tmpDir = '';

async function createTmpDir(): Promise<string> {
  tmpDir = await mkdtemp(path.join(os.tmpdir(), 'chirality-attachment-resolver-'));
  return tmpDir;
}

async function createSizedFile(filePath: string, size: number): Promise<void> {
  const handle = await open(filePath, 'w');
  try {
    await handle.truncate(size);
  } finally {
    await handle.close();
  }
}

afterEach(async () => {
  if (tmpDir) {
    await rm(tmpDir, { recursive: true, force: true });
    tmpDir = '';
  }
});

describe('AttachmentResolver', () => {
  it('resolves allowed attachments and preserves text content blocks', async () => {
    const root = await createTmpDir();
    const pngPath = path.join(root, 'fixture.png');
    await writeFile(pngPath, Buffer.from('png-fixture'));
    const resolver = new AttachmentResolver();

    const resolved = await resolver.resolveAttachmentsToContentBlocks('hello', [pngPath]);

    expect(resolved.errors).toEqual([]);
    expect(resolved.contentBlocks).toEqual([
      { type: 'text', text: 'hello' },
      { type: 'file', path: pngPath, mimeType: 'image/png' }
    ]);
  });

  it('rejects non-absolute attachment paths', async () => {
    const resolver = new AttachmentResolver();

    const resolved = await resolver.resolveAttachmentsToContentBlocks('hello', ['relative.png']);

    expect(resolved.contentBlocks).toEqual([{ type: 'text', text: 'hello' }]);
    expect(resolved.errors).toEqual([
      {
        path: 'relative.png',
        reason: 'Attachment path must be absolute'
      }
    ]);
  });

  it('rejects unsupported file extensions', async () => {
    const root = await createTmpDir();
    const filePath = path.join(root, 'fixture.bin');
    await writeFile(filePath, Buffer.from('fixture'));
    const resolver = new AttachmentResolver();

    const resolved = await resolver.resolveAttachmentsToContentBlocks('hello', [filePath]);

    expect(resolved.contentBlocks).toEqual([{ type: 'text', text: 'hello' }]);
    expect(resolved.errors[0]?.path).toBe(filePath);
    expect(resolved.errors[0]?.reason).toContain("Unsupported attachment extension '.bin'");
  });

  it('rejects non-file paths and symbolic links', async () => {
    const root = await createTmpDir();
    const dirPath = path.join(root, 'dir.txt');
    await mkdir(dirPath);
    const targetPath = path.join(root, 'target.txt');
    await writeFile(targetPath, 'target', 'utf8');
    const symlinkPath = path.join(root, 'link.txt');
    await symlink(targetPath, symlinkPath);
    const resolver = new AttachmentResolver();

    const resolved = await resolver.resolveAttachmentsToContentBlocks('hello', [dirPath, symlinkPath]);

    expect(resolved.contentBlocks).toEqual([{ type: 'text', text: 'hello' }]);
    expect(resolved.errors).toEqual([
      {
        path: dirPath,
        reason: 'Attachment path must reference a regular file'
      },
      {
        path: symlinkPath,
        reason: 'Attachment path must reference a regular file (symbolic links are rejected)'
      }
    ]);
  });

  it('rejects unreadable regular files and special files', async () => {
    const root = await createTmpDir();
    const unreadablePath = path.join(root, 'unreadable.txt');
    await writeFile(unreadablePath, 'not readable', 'utf8');
    await chmod(unreadablePath, 0o000);
    const socketPath = path.join(root, 'special.txt');
    await execFileAsync('mkfifo', [socketPath]);

    try {
      const resolver = new AttachmentResolver();
      const resolved = await resolver.resolveAttachmentsToContentBlocks('hello', [
        unreadablePath,
        socketPath
      ]);

      expect(resolved.contentBlocks).toEqual([{ type: 'text', text: 'hello' }]);
      expect(resolved.errors).toEqual([
        {
          path: unreadablePath,
          reason: `Attachment file is not readable: ${unreadablePath}`
        },
        {
          path: socketPath,
          reason: 'Attachment path must reference a regular file'
        }
      ]);
    } finally {
      await chmod(unreadablePath, 0o600);
    }
  });

  it('rejects files that exceed the per-file limit', async () => {
    const root = await createTmpDir();
    const largeFilePath = path.join(root, 'large.txt');
    await createSizedFile(largeFilePath, MAX_ATTACHMENT_BYTES + 1);
    const resolver = new AttachmentResolver();

    const resolved = await resolver.resolveAttachmentsToContentBlocks('hello', [largeFilePath]);

    expect(resolved.contentBlocks).toEqual([{ type: 'text', text: 'hello' }]);
    expect(resolved.errors).toEqual([
      {
        path: largeFilePath,
        reason: `Attachment exceeds per-file size limit (${MAX_ATTACHMENT_BYTES} bytes)`
      }
    ]);
  });

  it('enforces total per-turn byte budget using input-order sequential acceptance', async () => {
    const root = await createTmpDir();
    const nineMiB = 9 * BYTES_PER_MIB;
    const eightMiB = 8 * BYTES_PER_MIB;
    const tenMiB = 10 * BYTES_PER_MIB;
    const oneMiB = BYTES_PER_MIB;
    const fileA = path.join(root, 'a.csv');
    const fileB = path.join(root, 'b.csv');
    const fileC = path.join(root, 'c.csv');
    const fileD = path.join(root, 'd.csv');
    const fileE = path.join(root, 'e.csv');
    const fileF = path.join(root, 'f.csv');
    await createSizedFile(fileA, nineMiB);
    await createSizedFile(fileB, nineMiB);
    await createSizedFile(fileC, oneMiB);
    await createSizedFile(fileD, tenMiB);
    await createSizedFile(fileE, nineMiB);
    await createSizedFile(fileF, eightMiB);
    const resolver = new AttachmentResolver();

    const resolved = await resolver.resolveAttachmentsToContentBlocks('budget check', [fileA, fileB, fileC]);

    expect(resolved.contentBlocks).toEqual([
      { type: 'text', text: 'budget check' },
      { type: 'file', path: fileA, mimeType: 'text/csv' },
      { type: 'file', path: fileB, mimeType: 'text/csv' }
    ]);
    expect(resolved.errors).toEqual([
      {
        path: fileC,
        reason: `Attachment exceeds per-turn size budget (${18 * BYTES_PER_MIB} bytes total)`
      }
    ]);

    const reordered = await resolver.resolveAttachmentsToContentBlocks('budget check', [fileC, fileA, fileB]);

    expect(reordered.contentBlocks).toEqual([
      { type: 'text', text: 'budget check' },
      { type: 'file', path: fileC, mimeType: 'text/csv' },
      { type: 'file', path: fileA, mimeType: 'text/csv' }
    ]);
    expect(reordered.errors).toEqual([
      {
        path: fileB,
        reason: `Attachment exceeds per-turn size budget (${18 * BYTES_PER_MIB} bytes total)`
      }
    ]);

    const skipOverflowAndContinue = await resolver.resolveAttachmentsToContentBlocks('budget check', [
      fileD,
      fileE,
      fileF
    ]);

    expect(skipOverflowAndContinue.contentBlocks).toEqual([
      { type: 'text', text: 'budget check' },
      { type: 'file', path: fileD, mimeType: 'text/csv' },
      { type: 'file', path: fileF, mimeType: 'text/csv' }
    ]);
    expect(skipOverflowAndContinue.errors).toEqual([
      {
        path: fileE,
        reason: `Attachment exceeds per-turn size budget (${18 * BYTES_PER_MIB} bytes total)`
      }
    ]);
  });

  it('returns file-not-found errors for missing allowed-extension files', async () => {
    const root = await createTmpDir();
    const missingPath = path.join(root, 'missing.txt');
    const resolver = new AttachmentResolver();

    const resolved = await resolver.resolveAttachmentsToContentBlocks('hello', [missingPath]);

    expect(resolved.contentBlocks).toEqual([{ type: 'text', text: 'hello' }]);
    expect(resolved.errors).toEqual([
      {
        path: missingPath,
        reason: `Attachment file not found: ${missingPath}`
      }
    ]);
  });
});
