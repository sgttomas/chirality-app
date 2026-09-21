/**
 * Native attachment picker: validation and handler factory.
 *
 * The renderer names a project root; the main process shows a native
 * multi-file dialog and copies explicitly selected files into captured project
 * storage before returning contained paths. Runtime makes its final immutable
 * session copy on Send and refuses raw sources outside that session's project.
 *
 * Kept free of `electron` imports; the dialog and sender check are injected so
 * the validation is unit-testable against a real temporary directory.
 */

import { randomUUID } from 'node:crypto';
import { realpath, stat } from 'node:fs/promises';
import path from 'node:path';
import {
  SUPPORTED_ATTACHMENT_EXTENSIONS
} from '../src/lib/harness/ui-attachments';
import { assertAttachmentCount, captureAttachmentDirectory, ensureAttachmentDirectory, readAttachmentBytes, writeAttachmentCopy } from '@chirality/runtime-core';
import { RuntimeError } from '@chirality/runtime-contracts';
import type { IpcSenderEvent } from './ipc-sender-policy';
import type {
  AttachmentSelectFilesRequest,
  AttachmentSelectFilesResult
} from './attachment-ipc-contract';

export type AttachmentOpenDialogOptions = {
  title: string;
  buttonLabel: string;
  message: string;
  defaultPath: string;
  properties: Array<'openFile' | 'multiSelections'>;
  filters: Array<{ name: string; extensions: string[] }>;
};

export type AttachmentOpenDialogResult = {
  canceled: boolean;
  filePaths: string[];
};

export type AttachmentPickerDependencies = {
  authorized: (event: IpcSenderEvent) => boolean;
  showOpenDialog: (options: AttachmentOpenDialogOptions) => Promise<AttachmentOpenDialogResult>;
};

/** `SUPPORTED_ATTACHMENT_EXTENSIONS` in the dot-less form Electron filters expect. */
export function attachmentDialogExtensions(): string[] {
  return SUPPORTED_ATTACHMENT_EXTENSIONS.map((extension) => extension.replace(/^\./u, ''));
}

export function attachmentDialogOptions(projectRoot: string): AttachmentOpenDialogOptions {
  return {
    title: 'Attach files',
    buttonLabel: 'Attach',
    message: 'Selected files are copied into this project folder when attached.',
    defaultPath: projectRoot,
    properties: ['openFile', 'multiSelections'],
    filters: [{ name: 'Supported files', extensions: attachmentDialogExtensions() }]
  };
}

export class AttachmentPickerError extends Error {}

/**
 * Validate the renderer-supplied request and resolve its project root to a
 * canonical existing directory. The supplied value must already be absolute and
 * normalized — the renderer only ever holds roots produced by the folder picker
 * or by validated project bindings, so anything else is a malformed request.
 */
export async function resolveAttachmentProjectRoot(input: unknown): Promise<string> {
  if (!input || typeof input !== 'object' || Array.isArray(input)) {
    throw new AttachmentPickerError('Attachment request requires a project root.');
  }
  const root = (input as Partial<AttachmentSelectFilesRequest>).projectRoot;
  if (
    typeof root !== 'string' ||
    !path.isAbsolute(root) ||
    /[\x00-\x1f]/u.test(root) ||
    path.resolve(root) !== root
  ) {
    throw new AttachmentPickerError('Project root must be an absolute, normalized directory path.');
  }
  let canonical: string;
  try {
    canonical = await realpath(root);
  } catch {
    throw new AttachmentPickerError('Project root is not accessible.');
  }
  let info: Awaited<ReturnType<typeof stat>>;
  try {
    info = await stat(canonical);
  } catch {
    throw new AttachmentPickerError('Project root is not accessible.');
  }
  if (!info.isDirectory()) {
    throw new AttachmentPickerError('Project root must be a directory.');
  }
  return canonical;
}

/** Copy actual dialog selections; this helper is never exposed as renderer IPC. */
export async function copySelectedAttachmentInputs(projectRoot: string, selections: readonly string[], revalidate: () => Promise<void>): Promise<string[]> {
  const paths = [...new Set(selections)];
  assertAttachmentCount(paths);
  const budget = { bytes: 0 };
  const attachments = [];
  for (const selected of paths) {
    await revalidate();
    attachments.push(await readAttachmentBytes(selected, budget));
  }
  const guards = [revalidate];
  const validateDestination = async () => { for (const guard of guards) await guard(); };
  const chiralityDirectory = path.join(projectRoot, '.chirality');
  const inputDirectory = path.join(chiralityDirectory, 'attachment-inputs');
  for (const directory of [chiralityDirectory, inputDirectory]) {
    await validateDestination();
    guards.push(await ensureAttachmentDirectory(directory));
  }
  const copies: string[] = [];
  for (const attachment of attachments) {
    await validateDestination();
    const directory = path.join(inputDirectory, randomUUID());
    const directoryGuard = await ensureAttachmentDirectory(directory);
    const validateCopy = async () => { await validateDestination(); await directoryGuard(); };
    copies.push(await writeAttachmentCopy(directory, attachment.name, attachment, validateCopy));
  }
  return copies;
}

/** `ipcMain.handle` body for the attachment picker channel. */
export function createAttachmentSelectionHandler(deps: AttachmentPickerDependencies) {
  return async (event: IpcSenderEvent, input: unknown): Promise<AttachmentSelectFilesResult> => {
    if (!deps.authorized(event)) {
      return { cancelled: true, error: 'Unauthorized attachment request.' };
    }
    try {
      const projectRoot = await resolveAttachmentProjectRoot(input);
      const rootGuard = await captureAttachmentDirectory(projectRoot);
      const revalidate = async () => {
        if (!deps.authorized(event)) throw new AttachmentPickerError('Unauthorized attachment request.');
        await rootGuard();
        if (await resolveAttachmentProjectRoot(input) !== projectRoot) throw new AttachmentPickerError('The selected project folder changed.');
      };
      const dialogResult = await deps.showOpenDialog(attachmentDialogOptions(projectRoot));
      if (dialogResult.canceled || dialogResult.filePaths.length === 0) {
        return { cancelled: true };
      }
      await revalidate();
      const paths = await copySelectedAttachmentInputs(projectRoot, dialogResult.filePaths, revalidate);
      return { cancelled: false, paths };
    } catch (error) {
      return {
        cancelled: true,
        error:
          error instanceof AttachmentPickerError || error instanceof RuntimeError
            ? error.message
            : 'Unable to attach the selected files.'
      };
    }
  };
}
