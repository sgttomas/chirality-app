/**
 * Shared shape of the native attachment picker IPC, imported by both preload
 * and main so the channel name and result type cannot drift between them.
 */

export const ATTACHMENT_SELECT_FILES_CHANNEL = 'chirality:attachments-select-files';

export type AttachmentSelectFilesRequest = { projectRoot: string };

export type AttachmentSelectFilesResult =
  | { cancelled: true; error?: string }
  | { cancelled: false; paths: string[] };
