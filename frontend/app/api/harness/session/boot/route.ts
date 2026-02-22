import { NextRequest, NextResponse } from "next/server";

import {
  agentSdkManager,
  ensureHarnessSessionBooted,
  SessionBootSdkError,
  SessionPersonaNotFoundError,
} from "@/lib/harness";
import { ProjectRootValidationError, SessionNotFoundError } from "@/lib/harness/session-manager";
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

function statusForProjectRootValidation(code: ProjectRootValidationError["code"]): number {
  if (code === "PROJECT_ROOT_NOT_ACCESSIBLE") {
    return 403;
  }

  return 400;
}

export async function POST(req: NextRequest): Promise<Response> {
  let body: BootSessionRequestBody;

  try {
    body = (await req.json()) as BootSessionRequestBody;
  } catch {
    return NextResponse.json({ errorType: "VALIDATION_ERROR", error: "Invalid JSON body." }, { status: 400 });
  }

  const sessionId = typeof body.sessionId === "string" ? body.sessionId.trim() : "";
  const force = body.force === true;
  const opts = body.opts === undefined ? undefined : isObject(body.opts) ? normalizeTurnOpts(body.opts) : null;

  if (!sessionId) {
    return NextResponse.json({ errorType: "VALIDATION_ERROR", error: "sessionId is required." }, { status: 400 });
  }

  if (opts === null) {
    return NextResponse.json({ errorType: "VALIDATION_ERROR", error: "opts must be an object when provided." }, { status: 400 });
  }

  if (agentSdkManager.isRunning(sessionId)) {
    return NextResponse.json(
      { errorType: "SESSION_IN_FLIGHT", error: "Cannot boot a session with an in-flight turn." },
      { status: 409 },
    );
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
      return NextResponse.json({ errorType: "SESSION_NOT_FOUND", error: "Session not found." }, { status: 404 });
    }

    if (error instanceof ProjectRootValidationError) {
      return NextResponse.json(
        {
          errorType: error.code,
          error: error.message,
        },
        { status: statusForProjectRootValidation(error.code) },
      );
    }

    if (error instanceof SessionPersonaNotFoundError) {
      return NextResponse.json(
        {
          errorType: error.code,
          error: error.message,
        },
        { status: 404 },
      );
    }

    if (error instanceof SessionBootSdkError) {
      return NextResponse.json(
        {
          errorType: error.code,
          error: error.message,
        },
        { status: 502 },
      );
    }

    const message = error instanceof Error ? error.message : "Failed to boot session.";
    return NextResponse.json({ errorType: "SESSION_BOOT_FAILED", error: message }, { status: 500 });
  }
}
