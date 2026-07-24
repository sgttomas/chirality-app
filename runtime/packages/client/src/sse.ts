import type { IncomingMessage } from "node:http";
import { RuntimeError, type RuntimeSseFrame } from "@chirality/runtime-contracts";

export interface SseFrame {
  event?: string;
  data: string;
  id?: string;
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
  return {
    data: data.join("\n"),
    ...(event === undefined ? {} : { event }),
    ...(id === undefined ? {} : { id })
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

const uiEventTypes = new Set([
  "session:init",
  "chat:delta",
  "chat:complete",
  "tool:result",
  "session:complete",
  "turn:error",
  "process:exit",
  "harness:event"
]);

export function parseUiEvent(frame: SseFrame): RuntimeSseFrame {
  if (frame.event === undefined || !uiEventTypes.has(frame.event)) {
    throw new RuntimeError(
      "INTERNAL_FAILURE",
      "Runtime SSE frame has an unknown UI event type",
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
  if (typeof value !== "object" || value === null) {
    throw new RuntimeError(
      "INTERNAL_FAILURE",
      "Runtime UI event data must be a JSON object",
      502
    );
  }
  return { type: frame.event, data: value } as RuntimeSseFrame;
}
