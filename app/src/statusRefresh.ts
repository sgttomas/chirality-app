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

/** Runs the status refresh after an action. A failure calls `failed` and resolves; nothing raw escapes. */
export async function refreshAfterAction<T>(refresh: () => Promise<T>, failed: () => void): Promise<T | undefined> {
  try { return await refresh(); } catch { failed(); return undefined; }
}
