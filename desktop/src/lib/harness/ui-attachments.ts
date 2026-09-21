export const SUPPORTED_ATTACHMENT_EXTENSIONS = [
  '.png',
  '.jpg',
  '.jpeg',
  '.gif',
  '.webp',
  '.pdf',
  '.txt',
  '.md',
  '.csv'
] as const;

const SUPPORTED_EXTENSION_SET = new Set<string>(SUPPORTED_ATTACHMENT_EXTENSIONS);

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

export type UiAttachment = {
  path: string;
  displayName: string;
  mimeType: string;
  clientType: string;
};

function readString(value: unknown): string | null {
  if (typeof value !== 'string') {
    return null;
  }

  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : null;
}

function splitPathSegments(filePath: string): string[] {
  return filePath.replace(/\\/g, '/').split('/').filter(Boolean);
}

export function attachmentFileName(filePath: string): string {
  const segments = splitPathSegments(filePath);
  return segments[segments.length - 1] ?? filePath;
}

export function attachmentExtension(filePath: string): string {
  const fileName = attachmentFileName(filePath).toLowerCase();
  const lastDot = fileName.lastIndexOf('.');
  if (lastDot < 0) {
    return '';
  }
  return fileName.slice(lastDot);
}

function resolveClientType(extension: string): string {
  if (
    extension === '.png' ||
    extension === '.jpg' ||
    extension === '.jpeg' ||
    extension === '.gif' ||
    extension === '.webp'
  ) {
    return 'image';
  }

  if (extension === '.pdf') {
    return 'pdf';
  }

  if (extension === '.md') {
    return 'markdown';
  }

  if (extension === '.csv') {
    return 'csv';
  }

  if (extension === '.txt') {
    return 'text';
  }

  return 'unknown';
}

export function isSupportedAttachmentPath(filePath: string): boolean {
  const extension = attachmentExtension(filePath);
  return SUPPORTED_EXTENSION_SET.has(extension);
}

export function buildUiAttachment(filePath: string): UiAttachment {
  const extension = attachmentExtension(filePath);
  return {
    path: filePath,
    displayName: attachmentFileName(filePath),
    mimeType: MIME_BY_EXTENSION[extension] ?? 'application/octet-stream',
    clientType: resolveClientType(extension)
  };
}

export function sanitizeStoredAttachments(value: unknown): UiAttachment[] {
  if (!Array.isArray(value)) {
    return [];
  }

  const deduped = new Map<string, UiAttachment>();
  for (const entry of value) {
    if (!entry || typeof entry !== 'object') {
      continue;
    }

    const record = entry as Record<string, unknown>;
    const path = readString(record.path);
    if (!path) {
      continue;
    }

    const fallback = buildUiAttachment(path);
    const displayName = readString(record.displayName) ?? fallback.displayName;
    const mimeType = readString(record.mimeType) ?? fallback.mimeType;
    const clientType = readString(record.clientType) ?? fallback.clientType;

    deduped.set(path, {
      path,
      displayName,
      mimeType,
      clientType
    });
  }

  return [...deduped.values()];
}
