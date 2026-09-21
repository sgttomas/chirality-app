import { lstat } from 'node:fs/promises';
import path from 'node:path';
import { resolveAttachmentProjectRoot } from './attachment-picker';
import type { IpcSenderEvent } from './ipc-sender-policy';

import { type PlanExportTargetResult } from './plan-export-ipc-contract';

/** Chooses a path only. Runtime remains the sole writer and validates it again. */
export function createPlanExportDialogHandler(deps: {
  authorized: (event: IpcSenderEvent) => boolean;
  showSaveDialog: (options: { title: string; defaultPath: string; buttonLabel: string; filters: { name: string; extensions: string[] }[] }) => Promise<{ canceled: boolean; filePath?: string }>;
  showMessageBox: (options: { type: 'question'; message: string; buttons: string[]; defaultId: number; cancelId: number }) => Promise<{ response: number }>;
}) {
  return async (event: IpcSenderEvent, input: unknown): Promise<PlanExportTargetResult | boolean> => {
    if (!deps.authorized(event)) return { cancelled: true, error: 'Unauthorized plan export dialog.' };
    try {
      const root = await resolveAttachmentProjectRoot(input);
      const request = input as { operation?: unknown; revision?: unknown; targetRelativePath?: unknown };
      const validateTarget = async (target: string): Promise<string> => {
        const relative = path.relative(root, target);
        if (!relative || relative === '..' || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative) || /[\x00-\x1f]/u.test(relative)) throw new Error('Save the plan inside the project folder.');
        let current = root;
        for (const part of relative.split(path.sep)) {
          current = path.join(current, part);
          const info = await lstat(current).catch(error => {
            if ((error as NodeJS.ErrnoException).code === 'ENOENT') return undefined;
            throw error;
          });
          if (info?.isSymbolicLink()) throw new Error('Plan export refuses symbolic links.');
        }
        return relative;
      };
      if (request.operation === 'confirm-overwrite') {
        if (typeof request.targetRelativePath !== 'string' || path.isAbsolute(request.targetRelativePath)) return false;
        const relative = await validateTarget(path.resolve(root, request.targetRelativePath));
        return (await deps.showMessageBox({ type: 'question', message: `${relative} already exists. Replace it?`, buttons: ['Cancel', 'Replace'], defaultId: 0, cancelId: 0 })).response === 1;
      }
      if (request.operation !== 'choose' || !Number.isSafeInteger(request.revision) || (request.revision as number) < 1) throw new Error('Invalid plan revision.');
      const result = await deps.showSaveDialog({ title: 'Save plan', buttonLabel: 'Save', defaultPath: path.join(root, `native-plan-${request.revision}.md`), filters: [{ name: 'Markdown', extensions: ['md'] }] });
      if (result.canceled || !result.filePath) return { cancelled: true };
      return { cancelled: false, targetRelativePath: await validateTarget(path.resolve(result.filePath)) };
    } catch (error) {
      if ((input as { operation?: unknown } | null)?.operation === 'confirm-overwrite') return false;
      return { cancelled: true, error: error instanceof Error ? error.message : 'The save dialog could not be opened.' };
    }
  };
}
