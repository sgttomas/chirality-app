/**
 * Append-only main-process diagnostics log.
 *
 * A packaged Electron app has no attached terminal, so `console.warn` from the
 * main process is invisible to an operator: the daemon-binding failure that
 * produced `ENGINE_UNAVAILABLE` left no trace anywhere on disk. This writes a
 * timestamped line per event under `<userData>/logs/` so the same failure is
 * diagnosable after the fact, and mirrors to the console for `npm run desktop`.
 *
 * Deliberately dependency-free and synchronous:
 * - no new npm dependency (F-APP fences),
 * - `appendFileSync` preserves event ordering and survives an `app.exit()` that
 *   would otherwise drop a queued async write — which matters precisely because
 *   the events we most need are the ones emitted around shutdown.
 *
 * Volume is a handful of lines per binding attempt, but the file is long-lived,
 * so a single size-triggered rotation keeps it bounded without turning this into
 * a log-management subsystem.
 */

import { appendFileSync, mkdirSync, renameSync, statSync } from 'node:fs';
import path from 'node:path';

export type DesktopLogLevel = 'info' | 'warn' | 'error';

export type DesktopLogger = {
  log: (level: DesktopLogLevel, event: string, detail?: unknown) => void;
  info: (event: string, detail?: unknown) => void;
  warn: (event: string, detail?: unknown) => void;
  error: (event: string, detail?: unknown) => void;
  /** Absolute path of the active log file. */
  filePath: string;
};

export type DesktopLoggerOptions = {
  /** Directory the log file lives in; created if absent. */
  directory: string;
  /** Log file name. Defaults to `desktop-main.log`. */
  fileName?: string;
  /** Mirror every line to the console. Defaults to `true`. */
  mirrorToConsole?: boolean;
  /** Rotate to `<fileName>.1` once the file exceeds this size. Defaults to 2 MiB. */
  maxBytes?: number;
  /** Injected for tests. */
  now?: () => Date;
};

const DEFAULT_FILE_NAME = 'desktop-main.log';
const DEFAULT_MAX_BYTES = 2 * 1024 * 1024;

/**
 * Account e-mail redaction, applied at the writer so no caller can forget it.
 *
 * The Runtime service's stderr and Codex's own diagnostics can carry the
 * signed-in account address; the desktop log must stay shareable with a plain
 * `grep -v '@'`, so every line is scrubbed before it reaches the file or the
 * console. Scoped package names (`@chirality/runtime-core`) have no local part
 * and are left alone.
 */
const EMAIL_PATTERN = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/gu;
export const REDACTED_EMAIL_PLACEHOLDER = '[redacted-email]';

export function redactAccountEmails(text: string): string {
  return text.replaceAll(EMAIL_PATTERN, REDACTED_EMAIL_PLACEHOLDER);
}

/** Render a detail payload without ever throwing on cycles or exotic values. */
function formatDetail(detail: unknown): string {
  if (detail === undefined) {
    return '';
  }
  if (detail instanceof Error) {
    return ` ${JSON.stringify({ error: detail.message })}`;
  }
  if (typeof detail === 'string') {
    return ` ${detail}`;
  }
  try {
    return ` ${JSON.stringify(detail)}`;
  } catch {
    return ` ${String(detail)}`;
  }
}

export function createDesktopLogger(options: DesktopLoggerOptions): DesktopLogger {
  const fileName = options.fileName ?? DEFAULT_FILE_NAME;
  const filePath = path.join(options.directory, fileName);
  const maxBytes = options.maxBytes ?? DEFAULT_MAX_BYTES;
  const mirrorToConsole = options.mirrorToConsole ?? true;
  const now = options.now ?? (() => new Date());

  const rotateIfNeeded = (): void => {
    try {
      if (statSync(filePath).size > maxBytes) {
        renameSync(filePath, `${filePath}.1`);
      }
    } catch {
      // No file yet, or an unrotatable file: appending is still correct.
    }
  };

  const log = (level: DesktopLogLevel, event: string, detail?: unknown): void => {
    const line = redactAccountEmails(
      `${now().toISOString()} [${level}] ${event}${formatDetail(detail)}`
    ) + '\n';

    if (mirrorToConsole) {
      const mirror =
        level === 'error' ? console.error : level === 'warn' ? console.warn : console.info;
      mirror(`[chirality-desktop] ${line.trimEnd()}`);
    }

    try {
      mkdirSync(options.directory, { recursive: true });
      rotateIfNeeded();
      appendFileSync(filePath, line, { encoding: 'utf8', mode: 0o600 });
    } catch (error) {
      // Logging must never take the app down. The console mirror above is the
      // fallback record that the write itself failed.
      if (mirrorToConsole) {
        console.error(
          '[chirality-desktop] failed to append to the desktop log',
          error instanceof Error ? error.message : String(error)
        );
      }
    }
  };

  return {
    filePath,
    log,
    info: (event, detail) => log('info', event, detail),
    warn: (event, detail) => log('warn', event, detail),
    error: (event, detail) => log('error', event, detail)
  };
}

/** No-op logger for code paths that run without a resolved userData directory. */
export function createNoopDesktopLogger(): DesktopLogger {
  return {
    filePath: '',
    log: () => undefined,
    info: () => undefined,
    warn: () => undefined,
    error: () => undefined
  };
}
