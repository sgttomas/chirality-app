import { useEffect, useRef, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const text = (value: Json): string => value === null || value === undefined ? "" : typeof value === "string" ? value : JSON.stringify(value);

/** The host's built-in provider for cloud entries (access_provider: a cloud
 * entry requires the reported built-in `openai` provider). */
export const BUILT_IN_PROVIDER = "openai";
export const CLOUD_ENTRIES = ["chatgpt-account", "api-key"];
/** The host's reading of the app-server's own provider. */
export const PROVIDER_STATES = ["named", "unnamed", "not-established", "not-read"];

/** Whether a listed model may be chosen for the current choice, and how. */
export function modelMatch(packet: Json, modelProvider: string, entryId: string): "confirmed" | "unconfirmed" | "none" {
  const server = typeof packet?.serverProvider === "string" ? packet.serverProvider : null;
  if (!modelProvider) return "none";
  if (packet?.serverProviderState === "named") return server !== null && server === modelProvider ? "confirmed" : "none";
  // A null provider is never taken as the built-in one; the person may still
  // deliberately use a reported ID for the built-in route, marked unconfirmed.
  return packet?.serverProviderState === "unnamed" && modelProvider === BUILT_IN_PROVIDER && CLOUD_ENTRIES.includes(entryId) ? "unconfirmed" : "none";
}

/** Valid packets only; anything else is treated as unavailable. */
export function validModelPacket(packet: Json, generation: Json, modeHomeClass: string): boolean {
  return !!packet && (packet.state === "observed" || packet.state === "unavailable") && packet.modeHomeClass === modeHomeClass
    && JSON.stringify(packet.generation) === JSON.stringify(generation) && Array.isArray(packet.models) && Array.isArray(packet.limits)
    && PROVIDER_STATES.includes(packet.serverProviderState) && (packet.serverProviderState === "named" ? typeof packet.serverProvider === "string" && packet.serverProvider !== "" : packet.serverProvider === null)
    && typeof packet.complete === "boolean"
    && packet.models.every((row: Json) => ["id", "model", "displayName", "description"].every(key => typeof row?.[key] === "string") && typeof row.isDefault === "boolean" && row.model !== "");
}

/** How a new conversation connects: an explicit choice of an existing access route. */
export function AccessRouteChoice({ homeClass, modelProvider, entryId, disabled, choose, localHint }: {
  homeClass: string | null; modelProvider: string; entryId: string; disabled: boolean; choose: (route: { modelProvider: string; entryId: string }) => void; localHint?: string;
}) {
  const builtIn = homeClass === "api-key" ? { entryId: "api-key", label: "Use this home's API key (built-in OpenAI)" }
    : homeClass === "account" ? { entryId: "chatgpt-account", label: "Use my ChatGPT account (built-in OpenAI)" } : null;
  const chosen = builtIn && modelProvider === BUILT_IN_PROVIDER && entryId === builtIn.entryId;
  return <div aria-label="How this conversation connects">
    {builtIn ? <p><button disabled={disabled || !!chosen} aria-pressed={!!chosen} onClick={() => choose({ modelProvider: BUILT_IN_PROVIDER, entryId: builtIn.entryId })}>{builtIn.label}</button>{chosen ? " — chosen" : ""}</p>
      : <p>Choose the account or API-key home under Connection &amp; access first.</p>}
    {homeClass === "account" && <p><small>{localHint ?? "Or use a local model server: read the configured local providers below and choose one."}</small></p>}
    {entryId === "local-provider" && modelProvider && <p>Connects through configured local provider <code>{modelProvider}</code>.</p>}
  </div>;
}

/** The models Codex reports, read only when the person asks; never preselected. */
export function AvailableModels({ packet, current, reading, message, model, modelProvider, entryId, disabled, read, choose }: {
  packet: Json | null; current: boolean; reading: boolean; message: string; model: string; modelProvider: string; entryId: string;
  disabled: boolean; read: () => void; choose: (row: Json) => void;
}) {
  const match = packet && current ? modelMatch(packet, modelProvider, entryId) : "none";
  const server = typeof packet?.serverProvider === "string" ? packet.serverProvider : null;
  const rows = list(packet?.models);
  return <div aria-label="Available models">
    <button disabled={disabled || reading} onClick={read}>Read available models</button>{" "}
    <small>Asks Codex for its model list now. Nothing is chosen or started.</small>
    {reading && <p role="status">Reading the models Codex reports…</p>}
    {message && <p role="alert">{message}</p>}
    {packet && !current && <p role="status">This model list is out of date — Codex, the home or the project changed. Read it again.</p>}
    {packet && current && <div>
      <p><strong>{server ? <>Models Codex reports for provider <code>{server}</code></> : "Models Codex reports for its own provider"}</strong>{packet.readAt ? <small> · read {text(packet.readAt)}</small> : null}</p>
      {packet.providerLimit && <p role="note"><small>{text(packet.providerLimit)}.</small></p>}
      {!modelProvider ? <p role="note">Choose how this conversation connects first; then choose a model.</p>
        : match === "none" ? <p role="note">This list isn't for this conversation's provider (<code>{modelProvider}</code>{server ? <>; the list is for <code>{server}</code></> : ""}). Enter that provider's model ID under “Advanced: enter IDs yourself”.</p>
        : match === "unconfirmed" ? <p role="note">Codex's configuration doesn't name its provider, so the App can't confirm these models are for the built-in OpenAI route. You can still choose one. Start re-checks that the built-in OpenAI route is configured; it doesn't confirm this model is offered on it — if it isn't, Codex reports an error when the conversation starts or its first turn runs.</p> : null}
      {rows.length === 0 ? <p>{packet.complete ? "Codex reported no models." : "No models could be read."}</p>
        : <ul aria-label="Models Codex reports">{rows.map((row: Json) => <li key={row.id}>
          <strong>{text(row.displayName)}</strong> <code>{text(row.model)}</code>{row.isDefault ? " · Codex's default" : ""}{row.model === model ? " · chosen" : ""}
          {row.description && <><br/><small>{text(row.description)}</small></>}
          {match !== "none" && row.model !== model && <><br/><button disabled={disabled} onClick={() => choose(row)}>{match === "confirmed" ? `Use ${text(row.displayName)}` : `Use ${text(row.displayName)} (provider not confirmed)`}</button></>}
        </li>)}</ul>}
      {!packet.complete && <p role="note">The list may be incomplete: {list(packet.limits).map(text).join("; ")}.</p>}
      {packet.complete && list(packet.limits).length > 0 && <p role="note"><small>{list(packet.limits).map(text).join("; ")}.</small></p>}
      <p><small>{text(packet.standing)}</small></p>
    </div>}
  </div>;
}

export type ModelRoute = { model: string; modelProvider: string; entryId: string };
export const NO_MODEL_ROUTE: ModelRoute = { model: "", modelProvider: "", entryId: "" };
const chosenAny = (route: ModelRoute) => !!(route.model || route.modelProvider || route.entryId);

/** A model chooser bound to one composer (its owner), the home class and the
 * full Codex generation it was made for. Any change of that source starts a new
 * binding: the earlier choice and model list no longer count (and are shown as
 * out of date), so a stale choice can't be sent. The composer's text is not
 * held here and is kept. The list is read only at the person's press. */
export type BoundModelChoice = {
  route: ModelRoute; stale: boolean; revise: (patch: Partial<ModelRoute>) => void;
  packet: Json | null; current: boolean; reading: boolean; message: string; read: () => void; choose: (row: Json) => void;
  /** At a press: the choice if it is still bound to the latest source, else null. */
  bound: () => ModelRoute | null;
};
export function useBoundModelChoice({ owner, homeClass, generation, ready }: { owner: string; homeClass: string | null | undefined; generation: Json; ready: boolean }): BoundModelChoice {
  const key = JSON.stringify([owner, homeClass ?? null, generation ?? null]);
  const seen = useRef({ key, epoch: 0 });
  if (seen.current.key !== key) seen.current = { key, epoch: seen.current.epoch + 1 };
  const epoch = seen.current.epoch;
  const source = useRef({ homeClass, generation, ready }); source.current = { homeClass, generation, ready };
  const [held, setHeld] = useState<{ epoch: number; route: ModelRoute }>({ epoch, route: NO_MODEL_ROUTE });
  const heldRef = useRef(held); heldRef.current = held;
  const sequence = useRef(0);
  const pending = useRef(false);
  const mounted = useRef(true);
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; sequence.current++; }; }, []);
  const [observation, setObservation] = useState<{ packet: Json; epoch: number; sequence: number } | null>(null);
  const [reading, setReading] = useState(false);
  const [message, setMessage] = useState<{ epoch: number; text: string } | null>(null);
  const route = held.epoch === epoch ? held.route : NO_MODEL_ROUTE;
  const current = !!observation && ready && observation.epoch === epoch && observation.sequence === sequence.current;
  const revise = (patch: Partial<ModelRoute>) => setHeld(previous => {
    const now = seen.current.epoch;
    return { epoch: now, route: { ...(previous.epoch === now ? previous.route : NO_MODEL_ROUTE), ...patch } };
  });
  const read = () => {
    const { homeClass: mode, generation: original, ready: live } = source.current;
    if (pending.current || !live || !(mode === "account" || mode === "api-key")) return;
    const at = seen.current.epoch, number = ++sequence.current;
    const still = () => mounted.current && number === sequence.current && at === seen.current.epoch;
    pending.current = true; setReading(true); setObservation(null); setMessage(null);
    void Promise.resolve().then(() => invoke("read_available_models", { generation: original, modeHomeClass: mode })).then((packet: Json) => {
      if (!still()) return;
      if (!validModelPacket(packet, original, mode)) throw Error("the reply was not a model list for this Codex source");
      setObservation({ packet, epoch: at, sequence: number });
    }).catch(error => {
      if (still()) setMessage({ epoch: at, text: `Model list unavailable: ${error instanceof Error ? error.message : String(error)}. You can still enter a model ID under “Advanced: enter IDs yourself”.` });
    }).finally(() => { pending.current = false; if (mounted.current) setReading(false); });
  };
  const choose = (row: Json) => {
    const shown = observation, now = heldRef.current;
    if (!shown || !current || pending.current || now.epoch !== seen.current.epoch) return;
    if (!list(shown.packet.models).some((entry: Json) => entry.id === row?.id && entry.model === row?.model)) return;
    if (modelMatch(shown.packet, now.route.modelProvider, now.route.entryId) === "none") return;
    revise({ model: row.model });
  };
  const bound = () => {
    const now = heldRef.current;
    return source.current.ready && now.epoch === seen.current.epoch ? now.route : null;
  };
  return { route, stale: held.epoch !== epoch && chosenAny(held.route), revise, packet: observation?.packet ?? null, current, reading,
    message: message && message.epoch === epoch ? message.text : "", read, choose, bound };
}
