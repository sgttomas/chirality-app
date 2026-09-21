import { NextResponse } from 'next/server';
import { errorResponse, requireNonEmptyString } from '../../../../../../lib/harness/http';
import { getDaemonHarnessPort } from '../../../../../../lib/runtime-client/daemon-harness-port';

type RouteContext = { params: Promise<{ id: string }> };

/** GET /api/harness/session/[id]/requests: unanswered Codex server requests for the live turn. */
export async function GET(request: Request, context: RouteContext): Promise<Response> {
  try {
    const sessionId = requireNonEmptyString((await context.params).id, 'id');
    const result = await getDaemonHarnessPort().listRequests(sessionId, { signal: request.signal });
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
