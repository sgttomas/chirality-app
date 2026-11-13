// A status refresh after an action, held once for the web view. A refresh that fails never replaces
// the action's own message and never shows its raw diagnostic: the action's message stands, and the
// failure adds, once and after it, REFRESH_FAILED. Where there is no action message, REFRESH_FAILED alone.
export const REFRESH_FAILED = "The App could not read Codex's status afterwards, so what is shown may be out of date.";

/** The message shown once a status refresh has failed: `message` as it was, then REFRESH_FAILED, once. */
export function withRefreshFailure(message: string | null | undefined): string {
  const own = typeof message === "string" ? message : "";
  if (!own) return REFRESH_FAILED;
  return own.endsWith(REFRESH_FAILED) ? own : `${own} ${REFRESH_FAILED}`;
}

/** A status read after an action failed: it carries no snapshot and no raw diagnostic. */
export class StatusReadFailed extends Error {
  constructor() { super(REFRESH_FAILED); this.name = "StatusReadFailed"; }
}
/** Reads the status for an observer: a failure becomes StatusReadFailed, its raw diagnostic dropped. */
export async function readStatus<T>(read: Promise<T>): Promise<T> {
  try { return await read; } catch { throw new StatusReadFailed(); }
}
/** An observer's failure as shown: REFRESH_FAILED for a failed status read; the App's own message
 * (a supersession, for one) exactly as before. */
export function observationText(error: unknown): string {
  return error instanceof StatusReadFailed ? REFRESH_FAILED : String(error);
}
/** An observation limit as rendered: the fixed line alone, or `label` then the App's own message. */
export function observationLine(limit: string, label: string): string {
  return limit === REFRESH_FAILED ? REFRESH_FAILED : `${label}${limit}.`;
}

/** Runs the status refresh after an action. A failure calls `failed` and resolves; nothing raw escapes. */
export async function refreshAfterAction<T>(refresh: () => Promise<T>, failed: () => void): Promise<T | undefined> {
  try { return await refresh(); } catch { failed(); return undefined; }
}
