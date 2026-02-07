import { NextRequest, NextResponse } from "next/server";

import { claudeCodeManager, sessionManager } from "@/lib/harness";
import { SessionNotFoundError } from "@/lib/harness/session-manager";

export const runtime = "nodejs";

type RouteContext = {
  params: Promise<{ id: string }> | { id: string };
};

async function resolveSessionId(context: RouteContext): Promise<string> {
  const params = await context.params;
  return typeof params?.id === "string" ? params.id.trim() : "";
}

export async function GET(_req: NextRequest, context: RouteContext): Promise<Response> {
  const sessionId = await resolveSessionId(context);
  if (!sessionId) {
    return NextResponse.json({ error: "sessionId is required." }, { status: 400 });
  }

  try {
    const session = await sessionManager.get(sessionId);
    return NextResponse.json({ session });
  } catch (error) {
    if (error instanceof SessionNotFoundError) {
      return NextResponse.json({ error: "Session not found." }, { status: 404 });
    }

    const message = error instanceof Error ? error.message : "Failed to load session.";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}

export async function DELETE(_req: NextRequest, context: RouteContext): Promise<Response> {
  const sessionId = await resolveSessionId(context);
  if (!sessionId) {
    return NextResponse.json({ error: "sessionId is required." }, { status: 400 });
  }

  if (claudeCodeManager.isRunning(sessionId)) {
    return NextResponse.json({ error: "Cannot delete a session with an in-flight turn." }, { status: 409 });
  }

  try {
    await sessionManager.delete(sessionId);
    return new NextResponse(null, { status: 204 });
  } catch (error) {
    if (error instanceof SessionNotFoundError) {
      return NextResponse.json({ error: "Session not found." }, { status: 404 });
    }

    const message = error instanceof Error ? error.message : "Failed to delete session.";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
