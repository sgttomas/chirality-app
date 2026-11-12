// Keyed oMLX through the App's dedicated local Codex home (DEL-01-05
// LOCAL_PROVIDER_CUSTODY). The native commands take no key, endpoint or model:
// `prepare_local_provider()` and `submit_local_provider_key(generation)`, the
// latter opening a native secure field. This webview never receives a key; it
// shows only the named nonsecret fields of the returned view.
import { useRef, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
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

// Local model settings (DEL-01-05): the server address and the model name, both
// nonsecret. The host validates and is the authority; these two checks only
// say early what it will refuse. A key is never entered or shown here.
export const localEndpointValid = (value: string) => {
  const match = value.length <= 2048 ? /^https?:\/\/(?:127\.0\.0\.1|\[::1\])(?::([1-9][0-9]{0,4}))?(?:\/[A-Za-z0-9._~\/-]*)?$/.exec(value) : null;
  return !!match && (match[1] === undefined || Number(match[1]) <= 65535);
};
export const localModelValid = (value: string) => /^[A-Za-z0-9._:\/@+-]{1,128}$/.test(value);
type LocalSettingsView = { state: "unset" | "set" | "unavailable"; settings: { endpoint: string; model: string } | null; offered: { endpoint: string };
  inForce: { endpoint: string; model: string } | null; relaunchRequired: boolean;
  /** Why a relaunch is required, as the host establishes it; null when it gives no reason it knows. */
  relaunchReason: "settings-differ" | "change-begun" | null;
  outcome?: "saved" | "unchanged" | "cancelled";
  /** `signedOut`: Codex's sign-out ran in this save and Codex then reported no account. `keyRemoved`: and a key file was present before it. */
  signedOut?: boolean; keyRemoved?: boolean;
  /** Set only when a saved key was entered for another address than the one set; `recorded` is null when the App has no record of that address. */
  keyMismatch: { recorded: string | null } | null };
const pair = (value: Json) => typeof value?.endpoint === "string" && typeof value?.model === "string" ? { endpoint: value.endpoint as string, model: value.model as string } : null;
/** Only a complete reply is a settings view; anything else is shown as not read. */
export function localSettingsFrom(value: Json): LocalSettingsView | null {
  if (!["unset", "set", "unavailable"].includes(value?.state) || typeof value?.offered?.endpoint !== "string" || typeof value?.relaunchRequired !== "boolean") return null;
  const settings = pair(value.settings);
  // A saved key entered for another address: the host reports the settings as unavailable for use,
  // still names them, and gives the address it recorded for the key (null when it has no record).
  const mismatch = value.reason === "key-address-mismatch";
  if (!mismatch && value.reason != null) return null;
  if (mismatch ? value.state !== "unavailable" || !settings || !(value.keyAddress === null || (typeof value.keyAddress === "string" && localEndpointValid(value.keyAddress) && value.keyAddress !== settings.endpoint))
    : value.keyAddress != null || (value.state === "set") !== !!settings) return null;
  if (value.outcome !== undefined && !["saved", "unchanged", "cancelled"].includes(value.outcome)) return null;
  // A reason without a required relaunch contradicts itself; an unknown reason is not shown as known.
  const relaunchReason = value.relaunchReason === "settings-differ" || value.relaunchReason === "change-begun" ? value.relaunchReason : null;
  if (relaunchReason && !value.relaunchRequired) return null;
  return { state: value.state, settings, offered: { endpoint: value.offered.endpoint }, inForce: pair(value.inForce), relaunchRequired: value.relaunchRequired, relaunchReason,
    outcome: value.outcome, signedOut: value.signedOut === true, keyRemoved: value.keyRemoved === true, keyMismatch: mismatch ? { recorded: value.keyAddress } : null };
}

/** The local model server's address and model name: read at the person's press, saved only through the host's native question. */
export function LocalModelSettings({ disabled, changed }: { disabled: boolean; changed?: () => void }) {
  const [view, setView] = useState<LocalSettingsView | null>(null);
  const [draft, setDraft] = useState<{ endpoint: string; model: string } | null>(null);
  const [busy, setBusy] = useState(false);
  const [note, setNote] = useState<{ kind: "status" | "alert"; text: string } | null>(null);
  const pending = useRef(false);
  const run = async (command: "local_model_settings_read" | "local_model_settings_save", args?: Record<string, unknown>) => {
    if (pending.current) return;
    pending.current = true; setBusy(true); setNote(null);
    const saving = command === "local_model_settings_save";
    try {
      const next = localSettingsFrom(await invoke(command, args));
      if (!next) throw "The reply was not a local model settings reading; nothing is shown as set.";
      setView(next);
      if (command === "local_model_settings_read" || next.outcome === "saved") setDraft({ endpoint: next.settings?.endpoint ?? next.offered.endpoint, model: next.settings?.model ?? "" });
      if (next.outcome === "saved") {
        setNote({ kind: "status", text: next.keyRemoved ? "Saved. Codex removed the saved key for the earlier address; enter the key again after preparing the connection."
          : next.signedOut ? "Saved. Codex reports no saved key; enter the key after preparing the connection." : "Saved." });
        changed?.();
      } else if (next.outcome === "cancelled") setNote({ kind: "status", text: "Not saved: you cancelled. Nothing was changed." });
      else if (next.outcome === "unchanged") setNote({ kind: "status", text: "These are already the saved settings. Nothing was changed." });
    } catch (error) {
      const text = typeof error === "string" ? error : "Local model settings are unavailable.";
      if (saving) {
        // A save that did not return a reading may or may not have changed something (Codex may
        // have removed the key before a later step failed): nothing is shown as saved, and the
        // route and key state shown beside this are withdrawn until they are read again.
        setView(null); setDraft(null);
        setNote({ kind: "alert", text: `${text} Whether anything changed is not established here: read the local model settings again, and prepare the connection again to read the key state.` });
        changed?.();
      } else setNote({ kind: "alert", text: `${text} Nothing was changed.` });
    } finally { pending.current = false; setBusy(false); }
  };
  const endpointOk = !!draft && localEndpointValid(draft.endpoint), modelOk = !!draft && localModelValid(draft.model);
  const same = !!draft && !!view?.settings && draft.endpoint === view.settings.endpoint && draft.model === view.settings.model;
  return <div aria-label="Local model settings">
    <h4>Local model settings</h4>
    <p>The address of a model server on this machine and the name of its model. The server's key is not entered here; Codex keeps it.</p>
    <p><button disabled={disabled || busy} onClick={() => { void run("local_model_settings_read"); }}>{view ? "Read local model settings again" : "Show local model settings"}</button></p>
    {view && <>
      <p role="status">{view.state === "set" && view.settings ? <>Saved: server <code>{view.settings.endpoint}</code> · model <code>{view.settings.model}</code>.</>
        : view.state === "unset" ? "No local model server is set yet."
        : view.keyMismatch && view.settings ? <>The server address now set is <code>{view.settings.endpoint}</code> · model <code>{view.settings.model}</code>. The local connection is unavailable with this address, for the reason below.</>
        : "The saved local model settings could not be read, so nothing is shown as set. The local connection is unavailable until they can be."}</p>
      {view.keyMismatch && view.settings && (view.keyMismatch.recorded
        ? <><p role="alert">The saved key was entered for <code>{view.keyMismatch.recorded}</code>, and the address now set is <code>{view.settings.endpoint}</code>. The App will not use that key with another address.</p>
          <p><button disabled={disabled || busy} onClick={() => { void run("local_model_settings_save", { endpoint: view.keyMismatch!.recorded, model: view.settings!.model }); }}>Set the address back to {view.keyMismatch.recorded}…</button>{" "}
            <small>Asks you to confirm in a native question first. The saved key is kept and the model name is not changed.</small></p></>
        : <p role="alert">A key is saved, and the App has no record of the server address it was entered for, so it will not use that key at any address. This cannot be put right from the App.</p>)}
      {view.inForce && <p>In use in this session: server <code>{view.inForce.endpoint}</code> · model <code>{view.inForce.model}</code>.</p>}
      {view.relaunchRequired && <p role="status">{view.relaunchReason === "settings-differ" ? "The saved settings differ from those in use in this session. Quit and reopen the App to use the saved ones; until then the local connection is unavailable."
        : view.relaunchReason === "change-begun" ? "A change to the local model settings was begun in this session. Quit and reopen the App to use the local connection; until then it is unavailable."
        : "Quit and reopen the App to use the local connection; until then it is unavailable."}</p>}
      {view.state !== "unavailable" && draft && <>
        <p><label>Server address <input autoCapitalize="off" autoCorrect="off" autoComplete="off" spellCheck={false} value={draft.endpoint} disabled={disabled || busy}
          onChange={event => setDraft({ ...draft, endpoint: event.target.value })} aria-describedby="local-endpoint-rule" /></label>
          <br/><small id="local-endpoint-rule">On this machine only: <code>http://127.0.0.1:</code>port<code>/v1</code> (or <code>[::1]</code>). A server on another machine cannot be used.</small>
          {!endpointOk && draft.endpoint !== "" && <><br/><span role="alert">This address cannot be used: it must begin with http://127.0.0.1 or http://[::1], with a port and path only.</span></>}</p>
        <p><label>Model name on the server <input autoCapitalize="off" autoCorrect="off" autoComplete="off" spellCheck={false} value={draft.model} disabled={disabled || busy}
          onChange={event => setDraft({ ...draft, model: event.target.value })} aria-describedby="local-model-rule" /></label>
          <br/><small id="local-model-rule">Exactly as the server names it. Letters, digits and <code>. _ : / @ + -</code> only.</small>
          {!modelOk && draft.model !== "" && <><br/><span role="alert">This name cannot be used: only letters, digits and . _ : / @ + - are accepted, at most 128.</span></>}</p>
        <p><button disabled={disabled || busy || !endpointOk || !modelOk || same} onClick={() => { void run("local_model_settings_save", { endpoint: draft.endpoint, model: draft.model }); }}>Save local model settings…</button>{" "}
          <small>{same ? "No change to save." : "Asks you to confirm in a native question first. Changing the address removes a saved key, which you then enter again. A conversation already started continues only if the model name is unchanged, and then with the server at the new address."}</small></p>
      </>}
    </>}
    {busy && <p role="status">Working…</p>}
    {note && <p role={note.kind}>{note.text}</p>}
  </div>;
}

export function LocalProviderAccess({ host, view, attempted, pending, message, navigating, prepare, enterKey, useHome, settingsChanged }: {
  host: Json; view: LocalView | null; attempted: string[]; pending: boolean; message: { kind: "status" | "alert"; text: string } | null; navigating: boolean;
  prepare: () => void; enterKey: (generation: Json) => void; useHome: () => void; settingsChanged?: () => void;
}) {
  const entry = localEntry(host);
  const current = localViewCurrent(view, host);
  const used = current && attempted.includes(generationKey(view.generation));
  const active = host?.homeRouting?.activeModeHomeClass === LOCAL_MODE;
  return <div aria-label="Keyed oMLX connection">
    <p>A local model server (oMLX or another that serves the same interface) runs with Codex in a separate local home. Codex keeps the server's key there; this window never receives it.</p>
    <LocalModelSettings disabled={pending || navigating} changed={settingsChanged}/>
    <p><button disabled={pending || navigating} onClick={prepare}>Prepare the oMLX connection</button>{" "}
      <small>Sets up the local home with the saved local model settings and starts Codex there. It asks for no key and starts no conversation.</small></p>
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
