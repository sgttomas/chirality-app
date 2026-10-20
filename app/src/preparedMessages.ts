import { conversationReference, findConversation } from "./TrialComposer";
type Json = any; // eslint-disable-line @typescript-eslint/no-explicit-any

export type PreparedMessage = { kind: "delegated" | "clean" | "bring-back"; id: string; identity: string; owner: Json; pending: Json };
const list = (value: Json): Json[] => Array.isArray(value) ? value : [];
// Object member order is not source identity. Keep the complete supplied fields,
// including a bring-back's historical source, without interpreting it as a target.
const canonical = (value: Json): Json => Array.isArray(value) ? value.map(canonical)
  : value && typeof value === "object" ? Object.fromEntries(Object.keys(value).sort().map(key => [key, canonical(value[key])])) : value ?? null;
const same = (a: Json, b: Json) => JSON.stringify(canonical(a)) === JSON.stringify(canonical(b));

/** Current host pre-fills only. The original render owner is independent of
 * the composer's locally edited Send target and of the workspace's selectors. */
export function preparedMessages(host: Json): PreparedMessage[] {
  const root = host?.workflowRoot;
  const scope = [root?.context?.sourceRef, root?.context?.generation, host?.homeRouting?.activeModeHomeClass, host?.generation];
  const make = (kind: PreparedMessage["kind"], pending: Json): PreparedMessage => {
    const id = kind === "bring-back" ? pending?.id : pending?.reference;
    const owner = kind === "delegated" ? pending?.authoring : kind === "bring-back" ? pending?.target : null;
    // Exclude changing observations (draftChanged, delegation, limits, clean
    // start progress). They must not remount the original edited composer.
    const binding = kind === "bring-back"
      ? [pending?.trial, pending?.run, pending?.source, pending?.textIdentity, pending?.transcript, pending?.prompt, pending?.includeNative]
      : [pending?.draftName, pending?.location, pending?.content, pending?.textIdentity, pending?.text, pending?.message, pending?.workFolder, pending?.authoring];
    return { kind, id, owner, pending, identity: JSON.stringify(canonical([scope, kind, id, owner, binding])) };
  };
  return [...list(root?.pendingTrials).filter(p => p?.kind === "delegated" || p?.kind === "clean").map(p => make(p.kind, p)),
    ...list(root?.pendingBringBacks).map(p => make("bring-back", p))];
}

/** A reason is a refusal, never an invitation to resolve a bare ID elsewhere. */
export function preparedMessageLimit(host: Json, original: PreparedMessage): string | null {
  if (host?.state !== "ready" || host?.generationClosed === true) return "The original generation is closed or unavailable.";
  const context = host?.workflowRoot?.context;
  if (typeof context?.sourceRef !== "string" || !context.sourceRef || !conversationReference({ generation: host?.generation, threadId: "source-check" })
    || !same(context.generation, host.generation) || !["account", "api-key"].includes(host?.homeRouting?.activeModeHomeClass)) return "The original workflow source is unavailable.";
  const matches = preparedMessages(host).filter(p => p.kind === original.kind && p.id === original.id);
  if (typeof original.id !== "string" || !original.id || matches.length !== 1) return "The original prepared message is missing or ambiguous.";
  if (matches[0].identity !== original.identity) return "The prepared message or its original source/owner has changed.";
  if (original.kind === "clean") return "A clean preparation has no existing conversation to open.";
  const owner = conversationReference(original.owner);
  if (!owner || !same(owner.generation, host.generation) || !findConversation(host?.threads, owner)) return "The original composer conversation is not loaded in its original home and generation.";
  return null;
}
