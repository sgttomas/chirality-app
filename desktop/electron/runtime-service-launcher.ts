/**
 * Production launcher for the Runtime service child.
 *
 * The packaged App burns the `runAsNode` fuse off (`package.json`
 * `build.electronFuses`), so `ELECTRON_RUN_AS_NODE=1` on `process.execPath`
 * is ignored there. `utilityProcess.fork` is Electron's supported way to run a
 * Node script as a child of this main process with that fuse intact: the child
 * is a plain Node process (`process.argv` is `[helper, entry, ...args]`, so the
 * service's `argv.slice(2)` contract holds), stdio is piped, the environment is
 * explicit, and Electron reaps the child when the main process exits. Signals
 * go through `process.kill(pid)` so the SIGTERM-then-SIGKILL policy of the host
 * does not depend on `UtilityProcess.kill()` semantics.
 */

import { utilityProcess } from 'electron';
import type {
  RuntimeServiceChild,
  RuntimeServiceLaunchInput,
  RuntimeServiceLauncher
} from './runtime-service-host';

export const RUNTIME_SERVICE_NAME = 'chirality-runtime-service';

export const launchRuntimeServiceChild: RuntimeServiceLauncher = (
  input: RuntimeServiceLaunchInput
): Promise<RuntimeServiceChild> =>
  new Promise((resolve, reject) => {
    const child = utilityProcess.fork(input.entry, input.args, {
      stdio: ['ignore', 'pipe', 'pipe'],
      env: input.env,
      serviceName: RUNTIME_SERVICE_NAME
    });
    let spawned = false;
    const exitListeners: Array<(exit: { code: number | null; signal: string | null }) => void> = [];
    let exitRecord: { code: number | null; signal: string | null } | undefined;
    child.once('exit', (code) => {
      // UtilityProcess reports only a code. A signal death is surfaced by the
      // host's own kill bookkeeping, so it is reported as a null code here.
      exitRecord = { code: typeof code === 'number' ? code : null, signal: null };
      for (const listener of exitListeners.splice(0)) listener(exitRecord);
      if (!spawned) reject(new Error(`Runtime service exited before spawning (code ${String(code)})`));
    });
    child.once('spawn', () => {
      spawned = true;
      const pid = child.pid;
      if (typeof pid !== 'number') {
        reject(new Error('Runtime service spawned without a pid'));
        return;
      }
      resolve({
        pid,
        stdout: child.stdout,
        stderr: child.stderr,
        onExit(listener) {
          if (exitRecord) listener(exitRecord);
          else exitListeners.push(listener);
        },
        kill(signal) {
          process.kill(pid, signal);
        }
      });
    });
  });
