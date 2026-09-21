import { NextResponse } from 'next/server';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import { errorResponse, requireNonEmptyString } from '../../../../../../lib/harness/http';
import { getDaemonHarnessPort } from '../../../../../../lib/runtime-client/daemon-harness-port';

type RouteContext = {
  params: Promise<{
    id: string;
  }>;
};

/**
 * GET /api/harness/session/[id]/events — replay a session's persisted
 * `events.jsonl` (D-APP-22 hydrate-on-open). Returns the parsed events plus the
 * honest `malformedLineCount` and a summary; reuses `replayHarnessEvents` (no
 * forked parser). A missing log yields an empty replay, not an error.
 */
export async function GET(request: Request, context: RouteContext): Promise<Response> {
  try {
    const { id } = await context.params;
    const sessionId = requireNonEmptyString(id, 'id');
    // The id is joined into an on-disk events path; reject separators / `..`
    // so a crafted id can never traverse outside the session store.
    if (sessionId.includes('/') || sessionId.includes('\\') || sessionId.includes('..')) {
      throw new HarnessError('INVALID_REQUEST', 400, `Invalid session id '${sessionId}'`);
    }

    const replay = await getDaemonHarnessPort().replaySession(sessionId, {
      signal: request.signal
    });
    return NextResponse.json(replay, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
