type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any
const list = (value: Json): Json[] => (Array.isArray(value) ? value : []);
const text = (value: Json): string => value === null || value === undefined ? "" : typeof value === "string" ? value : JSON.stringify(value);

/** The host's built-in provider for cloud entries (access_provider: a cloud
 * entry requires the reported built-in `openai` provider). */
export const BUILT_IN_PROVIDER = "openai";
export const CLOUD_ENTRIES = ["chatgpt-account", "api-key"];
/** The host's own wording when the app-server's configuration names no provider. */
export const NO_PROVIDER_LIMIT = "the app-server's configuration names no provider; the list is not matched to any conversation provider";

/** Whether a listed model may be chosen for the current choice, and how. */
export function modelMatch(packet: Json, modelProvider: string, entryId: string): "confirmed" | "unconfirmed" | "none" {
  const server = typeof packet?.serverProvider === "string" ? packet.serverProvider : null;
  if (!modelProvider) return "none";
  if (server !== null) return server === modelProvider ? "confirmed" : "none";
  // A null provider is never taken as the built-in one; the person may still
  // deliberately use a reported ID for the built-in route, marked unconfirmed.
  return packet?.providerLimit === NO_PROVIDER_LIMIT && modelProvider === BUILT_IN_PROVIDER && CLOUD_ENTRIES.includes(entryId) ? "unconfirmed" : "none";
}

/** Valid packets only; anything else is treated as unavailable. */
export function validModelPacket(packet: Json, generation: Json, modeHomeClass: string): boolean {
  return !!packet && (packet.state === "observed" || packet.state === "unavailable") && packet.modeHomeClass === modeHomeClass
    && JSON.stringify(packet.generation) === JSON.stringify(generation) && Array.isArray(packet.models) && Array.isArray(packet.limits)
    && (packet.serverProvider === null || typeof packet.serverProvider === "string") && typeof packet.complete === "boolean"
    && packet.models.every((row: Json) => ["id", "model", "displayName", "description"].every(key => typeof row?.[key] === "string") && typeof row.isDefault === "boolean" && row.model !== "");
}

/** How a new conversation connects: an explicit choice of an existing access route. */
export function AccessRouteChoice({ homeClass, modelProvider, entryId, disabled, choose }: {
  homeClass: string | null; modelProvider: string; entryId: string; disabled: boolean; choose: (route: { modelProvider: string; entryId: string }) => void;
}) {
  const builtIn = homeClass === "api-key" ? { entryId: "api-key", label: "Use this home's API key (built-in OpenAI)" }
    : homeClass === "account" ? { entryId: "chatgpt-account", label: "Use my ChatGPT account (built-in OpenAI)" } : null;
  const chosen = builtIn && modelProvider === BUILT_IN_PROVIDER && entryId === builtIn.entryId;
  return <div aria-label="How this conversation connects">
    {builtIn ? <p><button disabled={disabled || !!chosen} aria-pressed={!!chosen} onClick={() => choose({ modelProvider: BUILT_IN_PROVIDER, entryId: builtIn.entryId })}>{builtIn.label}</button>{chosen ? " — chosen" : ""}</p>
      : <p>Choose the account or API-key home under Connection &amp; access first.</p>}
    {homeClass === "account" && <p><small>Or use a local model server: read the configured local providers below and choose one.</small></p>}
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
        : match === "unconfirmed" ? <p role="note">Codex's configuration doesn't name its provider, so the App can't confirm these models are for the built-in OpenAI route. You can still choose one; Start checks the configuration again.</p> : null}
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
