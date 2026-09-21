/**
 * Environment-driven process policy for the desktop main process.
 *
 * `main.ts` applies these decisions before `app.whenReady()` resolves, which is
 * the one place in the app that cannot be exercised from a test. Keeping the
 * decisions here — pure, `electron`-free, taking an explicit environment — makes
 * the rules themselves checkable, and leaves `main.ts` holding only the
 * side effects.
 */

import path from 'node:path';

/**
 * Minimal read-only environment shape. Deliberately not `NodeJS.ProcessEnv`:
 * that type is augmented project-wide with required keys, which would force
 * every caller (and every test) to supply unrelated variables.
 */
export type ProcessPolicyEnvironment = Readonly<Record<string, string | undefined>>;

export type UserDataOverride =
  | { kind: 'absent' }
  | { kind: 'apply'; directory: string }
  | { kind: 'rejected'; requested: string; reason: 'not-absolute' };

/**
 * Decide what `CHIRALITY_USER_DATA` should do to this process.
 *
 * A relative value is rejected rather than resolved: a Finder launch and a
 * shell launch have different working directories, so resolving one would
 * silently pick a different directory per launch path, the exact class of
 * mismatch this variable exists to eliminate.
 */
export function resolveUserDataOverride(
  environment: ProcessPolicyEnvironment = process.env
): UserDataOverride {
  const requested = environment.CHIRALITY_USER_DATA?.trim();
  if (!requested) {
    return { kind: 'absent' };
  }
  if (!path.isAbsolute(requested)) {
    return { kind: 'rejected', requested, reason: 'not-absolute' };
  }
  return { kind: 'apply', directory: path.normalize(requested) };
}
