// Keyed oMLX through the App's dedicated local Codex home (DEL-01-05
// LOCAL_PROVIDER_CUSTODY). The native commands take no key, endpoint or model:
// `prepare_local_provider()` and `submit_local_provider_key(generation)`, the
// latter opening a native secure field. This webview never receives a key; it
// shows only the named nonsecret fields of the returned view.
type Json = any;

export const LOCAL_MODE = "local-provider";
export const LOCAL_ENTRY = "local-provider-keyed";
// Same-role Fork in the local home depends on native PR198
// eacb1bf651d60884bbc042377865b4359930100d, whose Fork path carries the same
// effective-configuration admission as local Continue. Without that native
// dependency this must be false, which shows Fork unavailable here.
export const LOCAL_FORK_AVAILABLE = true;
export const LOCAL_FORK_UNAVAILABLE = "Fork isn't available in the local oMLX home yet: the check that a fork keeps the fixed oMLX settings is still being added.";
const STATES = ["entry-required", "configured-not-verified"] as const;
export type LocalCredentialState = typeof STATES[number];
export type LocalView = { entryId: string; providerId: string; endpoint: string; model: string; generation: Json; credentialState: LocalCredentialState };

const text = (value: unknown) => typeof value === "string" && value !== "";
const sameGeneration = (a: Json, b: Json) => !!a && !!b && a.appSession === b.appSession && a.home === b.home && a.spawnCounter === b.spawnCounter;
export const generationKey = (generation: Json) => JSON.stringify([generation?.appSession ?? null, generation?.home ?? null, generation?.spawnCounter ?? null]);

// Nonsecret generation identities whose one native key entry was dispatched.
// Kept in this window's session storage across a renderer reload; native still
// refuses any repeat for the same generation.
const ATTEMPTS = "chirality.localKeyEntryAttempts";
export function readAttemptedLocalEntries(): string[] {
  try { const value = JSON.parse(globalThis.sessionStorage?.getItem(ATTEMPTS) ?? "[]"); return Array.isArray(value) ? value.filter(item => typeof item === "string") : []; }
  catch { return []; }
}
export function recordAttemptedLocalEntry(key: string): string[] {
  const next = [...new Set([...readAttemptedLocalEntries(), key])];
  try { globalThis.sessionStorage?.setItem(ATTEMPTS, JSON.stringify(next)); } catch { /* in-memory only */ }
  return next;
}

/** Only a complete local view is admitted; any other reply is not a local status. */
export function localViewFrom(value: Json): LocalView | null {
  const g = value?.generation;
  if (value?.modeHomeClass !== LOCAL_MODE || value?.entryId !== LOCAL_ENTRY || !text(value?.providerId) || !text(value?.endpoint) || !text(value?.model)
    || !text(g?.appSession) || !text(g?.home) || !Number.isSafeInteger(g?.spawnCounter) || !STATES.includes(value?.credentialState)) return null;
  return { entryId: value.entryId, providerId: value.providerId, endpoint: value.endpoint, model: value.model,
    generation: { appSession: g.appSession, home: g.home, spawnCounter: g.spawnCounter }, credentialState: value.credentialState };
}

/** The local home as the current host routing reports it, if any. */
export const localEntry = (host: Json): Json | null =>
  (host?.homeRouting?.entries ?? []).find((entry: Json) => entry?.modeHomeClass === LOCAL_MODE) ?? null;

/** A view describes the current local source only while that source is the same ready generation. */
export function localViewCurrent(view: LocalView | null, host: Json): view is LocalView {
  const entry = localEntry(host);
  return !!view && !!entry && entry.state === "ready" && sameGeneration(entry.generation, view.generation);
}

/** The fixed route a new local conversation may use: only in the active local home of the viewed generation. */
export function localRoute(view: LocalView | null, host: Json): LocalView | null {
  return localViewCurrent(view, host) && host?.homeRouting?.activeModeHomeClass === LOCAL_MODE && host?.state === "ready"
    && !host?.generationClosed && sameGeneration(host?.generation, view.generation) ? view : null;
}

export function LocalProviderAccess({ host, view, attempted, pending, message, navigating, prepare, enterKey, useHome }: {
  host: Json; view: LocalView | null; attempted: string[]; pending: boolean; message: { kind: "status" | "alert"; text: string } | null; navigating: boolean;
  prepare: () => void; enterKey: (generation: Json) => void; useHome: () => void;
}) {
  const entry = localEntry(host);
  const current = localViewCurrent(view, host);
  const used = current && attempted.includes(generationKey(view.generation));
  const active = host?.homeRouting?.activeModeHomeClass === LOCAL_MODE;
  return <div aria-label="Keyed oMLX connection">
    <p>Keyed oMLX runs Codex in a separate local home. Codex keeps the key there; this window never receives it.</p>
    <p><button disabled={pending || navigating} onClick={prepare}>Prepare the oMLX connection</button>{" "}
      <small>Sets up the local home with its fixed settings and starts Codex there. It asks for no key and starts no conversation.</small></p>
    {current ? <>
      <p aria-label="oMLX destination">Destination <code>{view.endpoint}</code> · provider <code>{view.providerId}</code> · model <code>{view.model}</code></p>
      {view.credentialState === "configured-not-verified"
        ? <p role="status">Key saved by Codex — not verified. Whether oMLX accepts it is known only when a conversation reaches the server.</p>
        : <p role="status">Key entry required: Codex reports no saved key in the local home.</p>}
      {view.credentialState === "entry-required" && (used
        ? <p>Key entry for this Codex session has been used. Restart Codex for the oMLX home to enter a key again.</p>
        : <p><button disabled={pending || navigating} onClick={() => enterKey(view.generation)}>Enter oMLX key in a secure field…</button>{" "}
          <small>Opens a native field once for this Codex session. Cancelling still uses it.</small></p>)}
    </> : view ? <p role="status">This oMLX status is from an earlier Codex session or home. Prepare again to read the current one.</p> : null}
    {entry && !active && <p><button disabled={pending || navigating} onClick={useHome}>Use local oMLX home</button>{" "}
      <small>Switching homes never transfers an existing conversation.</small></p>}
    {entry && active && <p>The local oMLX home is in use. Start a new oMLX conversation under New conversation.</p>}
    {message && <p role={message.kind}>{message.text}</p>}
  </div>;
}
