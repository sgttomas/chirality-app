import { CODEX_ENGINE_ADAPTER_ID } from '@chirality/runtime-contracts';

function present(value: unknown): boolean {
  return typeof value === 'string' && value.trim().length > 0;
}

/** Readiness records Runtime boot completion, not the first supplier turn.
 * The v3 Codex adapter declares boot:none: Runtime records the boot stamps
 * before a provider thread exists. Other/legacy adapters still require the
 * provider session evidence produced by their boot turn.
 */
export function isSessionBootConfirmed(session: {
  schemaVersion?: unknown;
  bootedAt?: unknown;
  bootFingerprint?: unknown;
  engineSessionId?: unknown;
  engineSelection?: unknown;
}): boolean {
  if (!present(session.bootedAt) || !present(session.bootFingerprint)) return false;
  if (present(session.engineSessionId)) return true;
  const selection = session.engineSelection;
  return session.schemaVersion === 'chirality.session/v3' &&
    selection !== null && typeof selection === 'object' &&
    'adapterId' in selection && selection.adapterId === CODEX_ENGINE_ADAPTER_ID;
}
