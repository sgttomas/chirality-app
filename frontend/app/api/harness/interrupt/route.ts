import { NextRequest, NextResponse } from "next/server";

import { claudeCodeManager } from "@/lib/harness/claude-code-manager";

export const runtime = "nodejs";

type InterruptRequestBody = {
  sessionId?: unknown;
};

export async function POST(req: NextRequest) {
  let body: InterruptRequestBody;

  try {
    body = (await req.json()) as InterruptRequestBody;
  } catch {
    return NextResponse.json({ error: "Invalid JSON body." }, { status: 400 });
  }

  const sessionId = typeof body.sessionId === "string" ? body.sessionId.trim() : "";

  if (!sessionId) {
    return NextResponse.json({ error: "sessionId is required." }, { status: 400 });
  }

  if (!claudeCodeManager.isRunning(sessionId)) {
    return NextResponse.json({ error: "No active run for session." }, { status: 404 });
  }

  const signaled = claudeCodeManager.interrupt(sessionId);
  if (!signaled) {
    return NextResponse.json({ error: "No active run for session." }, { status: 404 });
  }

  return NextResponse.json({ ok: true });
}
