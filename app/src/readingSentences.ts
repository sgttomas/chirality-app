// The two sentences a configuration reading of a Codex home ends with when it was not sent, held
// once for the web view. They equal READING_GATE and READING_WITHDRAWN in
// src-tauri/src/hosting_reading_gate.rs ("configuration" covers config/read and
// configRequirements/read); tests/reading-sentences.test.mjs compares them with the Rust source.
// Only these exact texts are shown from an error; every other diagnostic stays withheld.
export const READING_GATE = "An earlier configuration reading for this home was still pending when the wait ended. This configuration request was not sent. You can try again after that reading finishes or Codex for this home is restarted.";
export const READING_WITHDRAWN = "This configuration request was not sent because its time limit expired while waiting to write to Codex for this home.";
/** Before either sentence when the configuration reading after a confirmed provider write fails that way (WRITE_THEN_READING). */
export const WRITE_THEN_READING = "Write observed; no retry. Reading the configuration again afterwards: ";

/** The sentence an error is, exactly; null for anything else. */
export function readingSentence(error: unknown): string | null {
  const text = typeof error === "string" ? error : error instanceof Error ? error.message : null;
  return text === READING_GATE || text === READING_WITHDRAWN ? text : null;
}
/** A save's message when its reading after the write ended with either sentence; null otherwise. */
export function readingAfterWrite(message: unknown): string | null {
  return typeof message === "string" && message.startsWith(WRITE_THEN_READING) && readingSentence(message.slice(WRITE_THEN_READING.length))
    ? message : null;
}
