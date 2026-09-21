import type { RuntimeDaemon } from "./runtime-daemon.js";

export type RuntimeDaemonShutdownSignal = "SIGINT" | "SIGTERM";

export interface RuntimeDaemonSignalShutdownOptions {
  /** Signals that initiate shutdown. Defaults to SIGINT and SIGTERM. */
  signals?: readonly RuntimeDaemonShutdownSignal[];
  /** Exit code assigned when daemon cleanup fails. Defaults to 1. */
  failureExitCode?: number;
  /**
   * Receives cleanup failures. The default writes a concise diagnostic to stderr.
   * Reporting does not replace RuntimeDaemon.stop()'s cleanup attempt.
   */
  reportFailure?: (error: unknown, signal: RuntimeDaemonShutdownSignal) => void;
}

export interface RuntimeDaemonSignalShutdown {
  /** Remove the installed listeners. In-flight shutdown is never cancelled. */
  dispose(): void;
  /** True after the first handled signal starts daemon cleanup. */
  isStopping(): boolean;
  /** Settles with the one stop operation started by the first handled signal. */
  completion: Promise<void>;
}

const DEFAULT_SIGNALS = ["SIGINT", "SIGTERM"] as const;

function describeFailure(error: unknown): string {
  return error instanceof Error ? `${error.name}: ${error.message}` : String(error);
}

/**
 * Connect process signals to RuntimeDaemon's bounded graceful-stop contract.
 *
 * The first configured signal starts exactly one stop operation. Further
 * configured signals are absorbed while that operation is in flight so they
 * cannot restore the platform default and terminate cleanup prematurely. The
 * function never calls process.exit(): a successful daemon stop releases its
 * own handles and lets the process exit naturally. On cleanup failure it sets
 * process.exitCode and reports the error, preserving the daemon's retry/error
 * semantics instead of hiding them behind an unconditional exit.
 */
export function installRuntimeDaemonSignalShutdown(
  daemon: Pick<RuntimeDaemon, "stop">,
  options: RuntimeDaemonSignalShutdownOptions = {}
): RuntimeDaemonSignalShutdown {
  const signals = [...new Set(options.signals ?? DEFAULT_SIGNALS)];
  if (signals.length === 0) {
    throw new Error("Runtime daemon signal shutdown requires at least one signal");
  }
  const failureExitCode = options.failureExitCode ?? 1;
  if (!Number.isSafeInteger(failureExitCode) || failureExitCode < 1 || failureExitCode > 255) {
    throw new Error("Runtime daemon signal failureExitCode must be an integer from 1 to 255");
  }

  let stopping = false;
  let disposed = false;
  let resolveCompletion!: () => void;
  let rejectCompletion!: (error: unknown) => void;
  const completion = new Promise<void>((resolve, reject) => {
    resolveCompletion = resolve;
    rejectCompletion = reject;
  });
  // The controller owns failure reporting even when a caller does not await.
  // Consumers may still await the original promise and observe its rejection.
  void completion.catch(() => undefined);
  const handlers = new Map<RuntimeDaemonShutdownSignal, () => void>();

  const dispose = (): void => {
    if (disposed) return;
    disposed = true;
    for (const [signal, handler] of handlers) process.off(signal, handler);
    handlers.clear();
  };

  const reportFailure = (error: unknown, signal: RuntimeDaemonShutdownSignal): void => {
    process.exitCode = failureExitCode;
    if (options.reportFailure !== undefined) {
      try {
        options.reportFailure(error, signal);
        return;
      } catch (reportError) {
        process.stderr.write(
          `Runtime daemon ${signal} failure reporter failed: ${describeFailure(reportError)}\n`
        );
      }
    }
    process.stderr.write(
      `Runtime daemon shutdown after ${signal} failed: ${describeFailure(error)}\n`
    );
  };

  for (const signal of signals) {
    const handler = (): void => {
      if (stopping || disposed) return;
      stopping = true;
      void Promise.resolve().then(() => daemon.stop()).then(
        () => {
          dispose();
          resolveCompletion();
        },
        (error) => {
          reportFailure(error, signal);
          dispose();
          rejectCompletion(error);
        }
      );
    };
    handlers.set(signal, handler);
    process.on(signal, handler);
  }

  return {
    completion,
    dispose,
    isStopping: () => stopping
  };
}
