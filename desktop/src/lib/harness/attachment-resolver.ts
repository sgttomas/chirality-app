import { constants } from 'node:fs';
import { access, lstat, stat } from 'node:fs/promises';
import path from 'node:path';
import { IAttachmentResolver, ResolvedAttachments } from '@chirality/runtime-contracts/types';

const BYTES_PER_MIB = 1024 * 1024;
const MAX_ATTACHMENT_BYTES = 10 * BYTES_PER_MIB;
const MAX_TOTAL_ATTACHMENT_BYTES = 18 * BYTES_PER_MIB;

const MIME_BY_EXTENSION: Record<string, string> = {
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.webp': 'image/webp',
  '.pdf': 'application/pdf',
  '.txt': 'text/plain',
  '.md': 'text/markdown',
  '.csv': 'text/csv'
};

const ALLOWED_EXTENSIONS = new Set(Object.keys(MIME_BY_EXTENSION));

function formatAllowedExtensions(): string {
  return Array.from(ALLOWED_EXTENSIONS).sort().join(', ');
}

function toAccessErrorReason(rawPath: string, error: unknown): string {
  const errorCode = typeof error === 'object' && error && 'code' in error ? (error.code as string) : undefined;
  if (errorCode === 'ENOENT') {
    return `Attachment file not found: ${rawPath}`;
  }
  if (errorCode === 'EACCES' || errorCode === 'EPERM') {
    return `Attachment file is not readable: ${rawPath}`;
  }
  return `Attachment file not accessible: ${rawPath}`;
}

function toStatErrorReason(rawPath: string, error: unknown): string {
  const errorCode = typeof error === 'object' && error && 'code' in error ? (error.code as string) : undefined;
  if (errorCode === 'ENOENT') {
    return `Attachment file not found: ${rawPath}`;
  }
  return `Attachment file metadata could not be read: ${rawPath}`;
}

export class AttachmentResolver implements IAttachmentResolver {
  async resolveAttachmentsToContentBlocks(
    message: string,
    attachmentPaths: string[]
  ): Promise<ResolvedAttachments> {
    const contentBlocks: ResolvedAttachments['contentBlocks'] = [];
    const errors: ResolvedAttachments['errors'] = [];
    let totalAcceptedBytes = 0;

    if (message.trim()) {
      contentBlocks.push({ type: 'text', text: message });
    }

    for (const rawPath of attachmentPaths) {
      if (!path.isAbsolute(rawPath)) {
        errors.push({ path: rawPath, reason: 'Attachment path must be absolute' });
        continue;
      }

      const extension = path.extname(rawPath).toLowerCase();
      if (!ALLOWED_EXTENSIONS.has(extension)) {
        errors.push({
          path: rawPath,
          reason: `Unsupported attachment extension '${extension || '(none)'}'. Allowed: ${formatAllowedExtensions()}`
        });
        continue;
      }

      try {
        await access(rawPath, constants.R_OK);
      } catch (error) {
        errors.push({ path: rawPath, reason: toAccessErrorReason(rawPath, error) });
        continue;
      }

      let sourceStat;
      try {
        sourceStat = await lstat(rawPath);
      } catch (error) {
        errors.push({ path: rawPath, reason: toStatErrorReason(rawPath, error) });
        continue;
      }

      if (sourceStat.isSymbolicLink()) {
        errors.push({
          path: rawPath,
          reason: 'Attachment path must reference a regular file (symbolic links are rejected)'
        });
        continue;
      }

      let fileStat;
      try {
        fileStat = await stat(rawPath);
      } catch (error) {
        errors.push({ path: rawPath, reason: toStatErrorReason(rawPath, error) });
        continue;
      }

      try {
        if (!fileStat.isFile()) {
          errors.push({ path: rawPath, reason: 'Attachment path must reference a regular file' });
          continue;
        }

        if (fileStat.size > MAX_ATTACHMENT_BYTES) {
          errors.push({
            path: rawPath,
            reason: `Attachment exceeds per-file size limit (${MAX_ATTACHMENT_BYTES} bytes)`
          });
          continue;
        }

        if (totalAcceptedBytes + fileStat.size > MAX_TOTAL_ATTACHMENT_BYTES) {
          errors.push({
            path: rawPath,
            reason: `Attachment exceeds per-turn size budget (${MAX_TOTAL_ATTACHMENT_BYTES} bytes total)`
          });
          continue;
        }

        totalAcceptedBytes += fileStat.size;

        contentBlocks.push({
          type: 'file',
          path: rawPath,
          mimeType: MIME_BY_EXTENSION[extension] || 'application/octet-stream'
        });
      } catch {
        errors.push({ path: rawPath, reason: `Attachment file not accessible: ${rawPath}` });
      }
    }

    return { contentBlocks, errors };
  }
}

export class StubAttachmentResolver extends AttachmentResolver {}
