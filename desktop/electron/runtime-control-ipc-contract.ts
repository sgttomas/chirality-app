import type { RuntimeServiceState } from './runtime-service-host';

/**
 * Renderer-facing runtime-control contract, shared by the main-process
 * handler and the preload bridge without pulling `ipcMain` into the preload.
 */
export const RUNTIME_SERVICE_RESTART_CHANNEL = 'chirality:runtime-service-restart';

export type RuntimeServiceControlResult =
  | { ok: true; service: RuntimeServiceState }
  | { ok: false; error: string };
