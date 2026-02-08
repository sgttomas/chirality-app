import { NextRequest, NextResponse } from "next/server";

import { claudeCodeManager, sessionManager, startHarnessTurn } from "@/lib/harness";
import { SessionNotFoundError } from "@/lib/harness/session-manager";
import type { TurnOpts, UIEvent } from "@/lib/harness/types";

export const runtime = "nodejs";

type TurnRequestBody = {
  sessionId?: unknown;
  message?: unknown;
  opts?: unknown;
};

function isObject(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function normalizeTurnOpts(value: Record<string, unknown>): TurnOpts {
  const normalized = { ...value } as TurnOpts & { model?: unknown };
  if (typeof normalized.model === "string") {
    const trimmed = normalized.model.trim();
    if (trimmed) {
      normalized.model = trimmed;
    } else {
      delete normalized.model;
    }
  } else {
    delete normalized.model;
  }

  return normalized as TurnOpts;
}

function formatSseEvent(event: UIEvent): string {
  return `event: ${event.type}\ndata: ${JSON.stringify(event)}\n\n`;
}

export async function POST(req: NextRequest): Promise<Response> {
  let body: TurnRequestBody;

  try {
    body = (await req.json()) as TurnRequestBody;
  } catch {
    return NextResponse.json({ error: "Invalid JSON body." }, { status: 400 });
  }

  const sessionId = typeof body.sessionId === "string" ? body.sessionId.trim() : "";
  const message = typeof body.message === "string" ? body.message : "";
  const opts = body.opts === undefined ? undefined : isObject(body.opts) ? normalizeTurnOpts(body.opts) : null;

  if (!sessionId) {
    return NextResponse.json({ error: "sessionId is required." }, { status: 400 });
  }

  if (!message.trim()) {
    return NextResponse.json({ error: "message is required." }, { status: 400 });
  }

  if (opts === null) {
    return NextResponse.json({ error: "opts must be an object when provided." }, { status: 400 });
  }

  if (claudeCodeManager.isRunning(sessionId)) {
    return NextResponse.json({ error: "A turn is already running for this session." }, { status: 409 });
  }

  try {
    await sessionManager.resume(sessionId);
  } catch (error) {
    if (error instanceof SessionNotFoundError) {
      return NextResponse.json({ error: "Session not found." }, { status: 404 });
    }

    const messageText = error instanceof Error ? error.message : "Failed to load session.";
    return NextResponse.json({ error: messageText }, { status: 500 });
  }

  const stream = new ReadableStream<Uint8Array>({
    start(controller) {
      const encoder = new TextEncoder();

      const sendEvent = (event: UIEvent): void => {
        controller.enqueue(encoder.encode(formatSseEvent(event)));
      };

      const onAbort = (): void => {
        claudeCodeManager.interrupt(sessionId);
      };

      req.signal.addEventListener("abort", onAbort);

      void (async () => {
        try {
          for await (const event of startHarnessTurn({ sessionId, message, opts })) {
            sendEvent(event);
          }
        } catch (error) {
          const messageText = error instanceof Error ? error.message : String(error);

          sendEvent({
            type: "session:error",
            sessionId,
            error: messageText,
          });

          sendEvent({
            type: "process:exit",
            sessionId,
            code: null,
            signal: null,
          });
        } finally {
          req.signal.removeEventListener("abort", onAbort);
          controller.close();
        }
      })();
    },
    cancel() {
      claudeCodeManager.interrupt(sessionId);
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
    },
  });
}
