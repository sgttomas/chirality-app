import { NextRequest, NextResponse } from "next/server";

import { agentSdkManager, ensureHarnessSessionBooted } from "@/lib/harness";
import { SessionNotFoundError } from "@/lib/harness/session-manager";
import type { TurnOpts } from "@/lib/harness/types";

export const runtime = "nodejs";

type BootSessionRequestBody = {
  sessionId?: unknown;
  force?: unknown;
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

export async function POST(req: NextRequest): Promise<Response> {
  let body: BootSessionRequestBody;

  try {
    body = (await req.json()) as BootSessionRequestBody;
  } catch {
    return NextResponse.json({ error: "Invalid JSON body." }, { status: 400 });
  }

  const sessionId = typeof body.sessionId === "string" ? body.sessionId.trim() : "";
  const force = body.force === true;
  const opts = body.opts === undefined ? undefined : isObject(body.opts) ? normalizeTurnOpts(body.opts) : null;

  if (!sessionId) {
    return NextResponse.json({ error: "sessionId is required." }, { status: 400 });
  }

  if (opts === null) {
    return NextResponse.json({ error: "opts must be an object when provided." }, { status: 400 });
  }

  if (agentSdkManager.isRunning(sessionId)) {
    return NextResponse.json({ error: "Cannot boot a session with an in-flight turn." }, { status: 409 });
  }

  try {
    const boot = await ensureHarnessSessionBooted({ sessionId, force, opts });
    return NextResponse.json({
      session: boot.session,
      boot: {
        booted: boot.booted,
        reason: boot.reason,
        fingerprint: boot.fingerprint,
        previousFingerprint: boot.previousFingerprint,
        previousClaudeSessionId: boot.previousClaudeSessionId,
      },
    });
  } catch (error) {
    if (error instanceof SessionNotFoundError) {
      return NextResponse.json({ error: "Session not found." }, { status: 404 });
    }

    const message = error instanceof Error ? error.message : "Failed to boot session.";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
