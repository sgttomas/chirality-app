import { errorResponse, readJsonBody, turnStreamResponse } from '../../../../lib/harness/http';
import {
  getDaemonHarnessPort,
  type V3TurnRequest
} from '../../../../lib/runtime-client/daemon-harness-port';

/**
 * POST /api/harness/turn: starts a Runtime-owned turn and streams the
 * Runtime's subscription to the browser as SSE (frames carry `id: <seq>`).
 * The Runtime owns the turn; cancelling this response only unsubscribes and
 * never interrupts it. Explicit Stop is `/api/harness/interrupt`.
 */
export async function POST(request: Request): Promise<Response> {
  try {
    const body = await readJsonBody<V3TurnRequest>(request);
    const runningTurn = await getDaemonHarnessPort().turn(body, {
      signal: request.signal
    });
    return turnStreamResponse(runningTurn);
  } catch (error) {
    return errorResponse(error);
  }
}
