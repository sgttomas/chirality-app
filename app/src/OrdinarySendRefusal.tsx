// An ordinary text send whose failure is definite: nothing was started, so
// sending is not held. The host names the class (lib.rs conversation_send_text,
// hosting.rs TurnStartFailure); this module only reads that structured value
// and never classifies from an error's text. Any other rejection is an
// unknown outcome and stays with the unconfirmed-send handling in App.tsx.

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Json = any;

export type DefiniteSendRefusal =
  /** The App refused before writing anything to Codex; `reason` is the host's. */
  | { kind: "before-write"; reason: string }
  /** Codex's own correlated JSON-RPC error, exactly as received. */
  | { kind: "codex"; nativeError: Json };

const plainObject = (v: unknown): v is Record<string, unknown> =>
  v !== null && typeof v === "object" && !Array.isArray(v) && Object.getPrototypeOf(v) === Object.prototype;
const keysAre = (v: Record<string, unknown>, keys: string[]) => {
  const own = Object.keys(v).sort(), want = [...keys].sort();
  return own.length === want.length && own.every((k, i) => k === want[i]);
};

/** The definite refusal a send command rejected with, or null for anything
 * else (a string, an Error, a missing or malformed value): those are unknown. */
export function definiteSendRefusal(rejection: unknown): DefiniteSendRefusal | null {
  if (!plainObject(rejection)) return null;
  if (rejection.sendOutcome === "refused-before-write" && keysAre(rejection, ["sendOutcome", "reason"])
    && typeof rejection.reason === "string" && rejection.reason) return { kind: "before-write", reason: rejection.reason };
  if (rejection.sendOutcome === "refused-by-codex" && keysAre(rejection, ["sendOutcome", "nativeError"])) {
    const error = rejection.nativeError;
    if (plainObject(error) && Number.isInteger(error.code) && typeof error.message === "string") return { kind: "codex", nativeError: error };
  }
  return null;
}

/** What was refused and why: Codex's message and error data as received, or the host's reason. */
export function DefiniteSendRefusalNotice({ refusal }: { refusal: DefiniteSendRefusal }) {
  if (refusal.kind === "codex") {
    return <div role="alert" aria-label="Message refused by Codex">
      <p><strong>Codex refused this message and started no turn.</strong> Nothing is held: your text and model choice are kept, and you can send again.</p>
      <p>Codex's message: <span style={{ whiteSpace: "pre-wrap" }}>{refusal.nativeError.message}</span></p>
      <details><summary>Codex's error, as received</summary><pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(refusal.nativeError, null, 2)}</pre></details>
    </div>;
  }
  return <div role="alert" aria-label="Message not sent">
    <p><strong>Not sent: the App refused this message before writing anything to Codex.</strong> Nothing is held: your text and model choice are kept, and you can send again.</p>
    <p>The App's reason: <span style={{ whiteSpace: "pre-wrap" }}>{refusal.reason}</span></p>
  </div>;
}
