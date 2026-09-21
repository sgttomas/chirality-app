import { HarnessError } from '@chirality/runtime-contracts/errors';
import { errorResponse, requireNonEmptyString, turnStreamResponse } from '../../../../../../../lib/harness/http';
import { getDaemonHarnessPort } from '../../../../../../../lib/runtime-client/daemon-harness-port';

type RouteContext = { params: Promise<{ id: string }> };

function readAfter(url: URL): number {
  const raw = url.searchParams.get('after');
  if (raw === null || raw.trim() === '') return 0;
  const value = Number(raw);
  if (!Number.isInteger(value) || value < 0) {
    throw new HarnessError('INVALID_REQUEST', 400, "Query 'after' must be a non-negative integer");
  }
  return value;
}

/**
 * GET /api/harness/session/[id]/turn/stream?after=<seq>: attaches to the
 * session's active (or recently finished) Runtime-owned turn. Buffered frames
 * with `seq > after` are replayed first, then live frames until the terminal
 * frame. A 404 `TURN_NOT_ACTIVE` from Runtime means there is nothing to attach
 * to. Closing the response unsubscribes only.
 */
export async function GET(request: Request, context: RouteContext): Promise<Response> {
  try {
    const sessionId = requireNonEmptyString((await context.params).id, 'id');
    const url = new URL(request.url);
    const after = readAfter(url);
    const turnId = url.searchParams.has('turnId') ? requireNonEmptyString(url.searchParams.get('turnId'), 'turnId') : undefined;
    const subscription = await getDaemonHarnessPort().attachTurn(sessionId, after, {
      signal: request.signal,
      ...(turnId === undefined ? {} : { turnId })
    });
    return turnStreamResponse(subscription);
  } catch (error) {
    return errorResponse(error);
  }
}
