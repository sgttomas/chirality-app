import { describe, expect, it } from 'vitest';
import {
  attachmentExtension,
  attachmentFileName,
  buildUiAttachment,
  isSupportedAttachmentPath,
  sanitizeStoredAttachments
} from '../../lib/harness/ui-attachments';

describe('ui attachment helpers', () => {
  it('extracts file names and extensions from absolute paths', () => {
    expect(attachmentFileName('/tmp/example/report.csv')).toBe('report.csv');
    expect(attachmentExtension('/tmp/example/report.csv')).toBe('.csv');
    expect(attachmentExtension('/tmp/example/no-extension')).toBe('');
  });

  it('detects supported extension paths', () => {
    expect(isSupportedAttachmentPath('/tmp/file.png')).toBe(true);
    expect(isSupportedAttachmentPath('/tmp/file.jpeg')).toBe(true);
    expect(isSupportedAttachmentPath('/tmp/file.bin')).toBe(false);
  });

  it('classifies preview metadata from path extension', () => {
    expect(buildUiAttachment('/tmp/docs/notes.md')).toEqual({
      path: '/tmp/docs/notes.md',
      displayName: 'notes.md',
      mimeType: 'text/markdown',
      clientType: 'markdown'
    });

    expect(buildUiAttachment('/tmp/docs/raw.bin')).toEqual({
      path: '/tmp/docs/raw.bin',
      displayName: 'raw.bin',
      mimeType: 'application/octet-stream',
      clientType: 'unknown'
    });
  });

  it('sanitizes stored attachment arrays and drops malformed rows', () => {
    const sanitized = sanitizeStoredAttachments([
      {
        path: '/tmp/a.txt',
        displayName: 'A text file',
        mimeType: 'text/plain',
        clientType: 'text'
      },
      {
        path: '/tmp/a.txt',
        displayName: 'A text file (updated)'
      },
      {
        path: '/tmp/b.bin'
      },
      {
        displayName: 'missing path'
      },
      42
    ]);

    expect(sanitized).toEqual([
      {
        path: '/tmp/a.txt',
        displayName: 'A text file (updated)',
        mimeType: 'text/plain',
        clientType: 'text'
      },
      {
        path: '/tmp/b.bin',
        displayName: 'b.bin',
        mimeType: 'application/octet-stream',
        clientType: 'unknown'
      }
    ]);
  });
});
