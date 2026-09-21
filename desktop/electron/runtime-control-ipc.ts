import { ipcMain } from 'electron';
import { isAuthorizedSender } from './ipc-sender-policy';
import {
  RUNTIME_SERVICE_RESTART_CHANNEL,
  type RuntimeServiceControlResult
} from './runtime-control-ipc-contract';
import type { RuntimeServiceState } from './runtime-service-host';

/**
 * Runtime-control IPC for the App-owned Runtime service (D-GOV-43, A2).
 *
 * The LaunchAgent verbs (install, start, stop, uninstall) and the oMLX model
 * residency channels are retired: the service is a child of this process, so
 * the only operator action left is a retry after the host gave up.
 */
export { RUNTIME_SERVICE_RESTART_CHANNEL, type RuntimeServiceControlResult };

export type RuntimeControlDependencies = {
  rendererOrigin: string;
  restartService: () => Promise<RuntimeServiceState>;
};

function safeError(error: unknown, fallback: string): string {
  if (error instanceof Error && error.message.trim()) {
    return error.message.replaceAll(/(?:Bearer|token|credential|api[_ -]?key)\s+\S+/giu, '[redacted]');
  }
  return fallback;
}

export function registerRuntimeControlHandlers(deps: RuntimeControlDependencies): void {
  unregisterRuntimeControlHandlers();

  ipcMain.handle(
    RUNTIME_SERVICE_RESTART_CHANNEL,
    async (event): Promise<RuntimeServiceControlResult> => {
      if (!isAuthorizedSender(event, deps.rendererOrigin)) {
        return { ok: false, error: 'Runtime control request was denied' };
      }
      try {
        return { ok: true, service: await deps.restartService() };
      } catch (error) {
        return { ok: false, error: safeError(error, 'Unable to restart the runtime service') };
      }
    }
  );
}

export function unregisterRuntimeControlHandlers(): void {
  ipcMain.removeHandler(RUNTIME_SERVICE_RESTART_CHANNEL);
}
