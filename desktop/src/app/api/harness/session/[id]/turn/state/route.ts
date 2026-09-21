import { NextResponse } from 'next/server';
import { errorResponse, requireNonEmptyString } from '../../../../../../../lib/harness/http';
import { getDaemonHarnessPort } from '../../../../../../../lib/runtime-client/daemon-harness-port';

type RouteContext = { params: Promise<{ id: string }> };

/** GET /api/harness/session/[id]/turn/state: Runtime-owned turn state for the session. */
export async function GET(request: Request, context: RouteContext): Promise<Response> {
  try {
    const sessionId = requireNonEmptyString((await context.params).id, 'id');
    const state = await getDaemonHarnessPort().turnState(sessionId, { signal: request.signal });
    return NextResponse.json(state, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
