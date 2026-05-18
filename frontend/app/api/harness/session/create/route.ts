import { NextRequest, NextResponse } from "next/server";

import { sessionManager } from "@/lib/harness";
import { ProjectRootValidationError } from "@/lib/harness/session-manager";
import type { SessionMode } from "@/lib/harness/types";

export const runtime = "nodejs";

type CreateSessionRequestBody = {
  projectRoot?: unknown;
  persona?: unknown;
  mode?: unknown;
};

const ALLOWED_MODES: SessionMode[] = ["workbench", "pipeline", "direct"];

function isSessionMode(value: unknown): value is SessionMode {
  return typeof value === "string" && ALLOWED_MODES.includes(value as SessionMode);
}

function statusForProjectRootValidation(code: ProjectRootValidationError["code"]): number {
  if (code === "PROJECT_ROOT_NOT_ACCESSIBLE") {
    return 403;
  }

  return 400;
}

export async function POST(req: NextRequest): Promise<Response> {
  let body: CreateSessionRequestBody;

  try {
    body = (await req.json()) as CreateSessionRequestBody;
  } catch {
    return NextResponse.json({ errorType: "VALIDATION_ERROR", error: "Invalid JSON body." }, { status: 400 });
  }

  const projectRoot = typeof body.projectRoot === "string" ? body.projectRoot.trim() : "";
  if (!projectRoot) {
    return NextResponse.json({ errorType: "VALIDATION_ERROR", error: "projectRoot is required." }, { status: 400 });
  }

  if (!isSessionMode(body.mode)) {
    return NextResponse.json(
      { errorType: "VALIDATION_ERROR", error: "mode must be one of: workbench, pipeline, direct." },
      { status: 400 },
    );
  }

  if (body.persona !== undefined && body.persona !== null && typeof body.persona !== "string") {
    return NextResponse.json({ errorType: "VALIDATION_ERROR", error: "persona must be a string or null." }, { status: 400 });
  }

  const persona = typeof body.persona === "string" ? body.persona : null;

  try {
    const session = await sessionManager.create(projectRoot, persona, body.mode);
    return NextResponse.json({ session }, { status: 201 });
  } catch (error) {
    if (error instanceof ProjectRootValidationError) {
      return NextResponse.json(
        {
          errorType: error.code,
          error: error.message,
        },
        { status: statusForProjectRootValidation(error.code) },
      );
    }

    const message = error instanceof Error ? error.message : "Failed to create session.";
    return NextResponse.json({ errorType: "SESSION_CREATE_FAILED", error: message }, { status: 500 });
  }
}
