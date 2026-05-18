import { NextRequest, NextResponse } from "next/server";

import { sessionManager } from "@/lib/harness";

export const runtime = "nodejs";

export async function GET(req: NextRequest): Promise<Response> {
  const projectRootParam = req.nextUrl.searchParams.get("projectRoot");
  const projectRoot = projectRootParam && projectRootParam.trim() ? projectRootParam.trim() : undefined;

  try {
    const sessions = await sessionManager.list(projectRoot);
    return NextResponse.json(sessions);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Failed to list sessions.";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
