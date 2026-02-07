import path from "node:path";

import { NextRequest, NextResponse } from "next/server";

import { claudeCodeManager, getHarnessSessionStore } from "@/lib/harness/claude-code-manager";
import type { Session, SessionMode, TurnOpts, UIEvent } from "@/lib/harness/types";

export const runtime = "nodejs";

type TurnRequestBody = {
  sessionId?: unknown;
  message?: unknown;
  opts?: TurnOpts & {
    projectRoot?: string;
    persona?: string | null;
    mode?: SessionMode;
  };
};

const ALLOWED_MODES: SessionMode[] = ["workbench", "pipeline", "direct"];

function isSessionMode(value: unknown): value is SessionMode {
  return typeof value === "string" && ALLOWED_MODES.includes(value as SessionMode);
}

function getOrCreateSession(sessionId: string, opts: TurnRequestBody["opts"]): Session {
  const store = getHarnessSessionStore();
  const existing = store.get(sessionId);
  const now = new Date().toISOString();

  const projectRootFromOpts =
    typeof opts?.projectRoot === "string" && opts.projectRoot.trim()
      ? opts.projectRoot
      : path.resolve(process.cwd(), "..");

  const modeFromOpts = isSessionMode(opts?.mode) ? opts.mode : "direct";
  const personaFromOpts = typeof opts?.persona === "string" ? opts.persona : null;

  if (existing) {
    const updated: Session = {
      ...existing,
      updatedAt: now,
      projectRoot: projectRootFromOpts || existing.projectRoot,
      mode: modeFromOpts,
      persona: personaFromOpts,
    };

    store.set(sessionId, updated);
    return updated;
  }

  const session: Session = {
    id: sessionId,
    createdAt: now,
    updatedAt: now,
    projectRoot: projectRootFromOpts,
    persona: personaFromOpts,
    mode: modeFromOpts,
    claudeSessionId: null,
  };

  store.set(sessionId, session);
  return session;
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

  if (!sessionId) {
    return NextResponse.json({ error: "sessionId is required." }, { status: 400 });
  }

  if (!message.trim()) {
    return NextResponse.json({ error: "message is required." }, { status: 400 });
  }

  if (claudeCodeManager.isRunning(sessionId)) {
    return NextResponse.json({ error: "A turn is already running for this session." }, { status: 409 });
  }

  const session = getOrCreateSession(sessionId, body.opts);
  const store = getHarnessSessionStore();

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
          for await (const event of claudeCodeManager.startTurn(session, message, body.opts)) {
            if (event.type === "session:init") {
              const current = store.get(sessionId);
              if (current) {
                current.claudeSessionId = event.claudeSessionId;
                current.updatedAt = new Date().toISOString();
                store.set(sessionId, current);
              }
            }

            if (event.type === "session:complete" || event.type === "session:error" || event.type === "process:exit") {
              const current = store.get(sessionId);
              if (current) {
                current.updatedAt = new Date().toISOString();
                store.set(sessionId, current);
              }
            }

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
