import type { IncomingMessage } from "node:http";
import { RuntimeError, type RuntimeSseFrame } from "@chirality/runtime-contracts";

export interface SseFrame {
  event?: string;
  data: string;
  id?: string;
  /** The Runtime-owned frame sequence when `id` is a non-negative integer (turn subscriptions). */
  seq?: number;
}

function sequenceOf(id: string | undefined): number | undefined {
  if (id === undefined || !/^(0|[1-9][0-9]{0,15})$/u.test(id)) return undefined;
  return Number(id);
}

function parseFrame(source: string): SseFrame | undefined {
  let event: string | undefined;
  let id: string | undefined;
  const data: string[] = [];
  for (const rawLine of source.split("\n")) {
    const line = rawLine.endsWith("\r") ? rawLine.slice(0, -1) : rawLine;
    if (line.length === 0 || line.startsWith(":")) continue;
    const separator = line.indexOf(":");
    const field = separator === -1 ? line : line.slice(0, separator);
    let value = separator === -1 ? "" : line.slice(separator + 1);
    if (value.startsWith(" ")) value = value.slice(1);
    if (field === "event") event = value;
    if (field === "id") id = value;
    if (field === "data") data.push(value);
  }
  if (data.length === 0) return undefined;
  const seq = sequenceOf(id);
  return {
    data: data.join("\n"),
    ...(event === undefined ? {} : { event }),
    ...(id === undefined ? {} : { id }),
    ...(seq === undefined ? {} : { seq })
  };
}

export async function* parseSse(
  response: IncomingMessage
): AsyncGenerator<SseFrame> {
  response.setEncoding("utf8");
  let buffer = "";
  for await (const chunk of response) {
    buffer += chunk;
    while (true) {
      const lf = buffer.indexOf("\n\n");
      const crlf = buffer.indexOf("\r\n\r\n");
      let boundary = -1;
      let width = 0;
      if (lf >= 0 && (crlf < 0 || lf < crlf)) {
        boundary = lf;
        width = 2;
      } else if (crlf >= 0) {
        boundary = crlf;
        width = 4;
      }
      if (boundary < 0) break;
      const frame = parseFrame(buffer.slice(0, boundary));
      buffer = buffer.slice(boundary + width);
      if (frame !== undefined) yield frame;
    }
  }
  const finalFrame = parseFrame(buffer);
  if (finalFrame !== undefined) yield finalFrame;
}

/**
 * Any named event is accepted: the Runtime streams the open UIEvent set and its
 * `harness:event` passthrough carries every Codex notification, so a closed
 * type list would silently drop faithful frames. `seq` mirrors the wire `id`.
 */
export function parseUiEvent(frame: SseFrame): RuntimeSseFrame {
  if (frame.event === undefined || frame.event.trim() === "") {
    throw new RuntimeError(
      "INTERNAL_FAILURE",
      "Runtime SSE frame lacks an event name",
      502
    );
  }
  let value: unknown;
  try {
    value = JSON.parse(frame.data);
  } catch {
    throw new RuntimeError(
      "INTERNAL_FAILURE",
      "Runtime UI event contains malformed JSON",
      502
    );
  }
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new RuntimeError(
      "INTERNAL_FAILURE",
      "Runtime UI event data must be a JSON object",
      502
    );
  }
  return { type: frame.event, data: value, ...(frame.seq === undefined ? {} : { seq: frame.seq }) } as RuntimeSseFrame;
}
