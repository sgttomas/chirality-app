import { NextResponse } from 'next/server';
import { isRecord, requireServerRequestAnswer } from '../../../../../../../../lib/harness/server-request-answer';
import { errorResponse, readJsonBody, requireNonEmptyString } from '../../../../../../../../lib/harness/http';
import { getDaemonHarnessPort } from '../../../../../../../../lib/runtime-client/daemon-harness-port';

type RouteContext = { params: Promise<{ id: string; requestId: string }> };

export async function POST(request: Request, context: RouteContext): Promise<Response> {
  try {
    const params = await context.params;
    const sessionId = requireNonEmptyString(params.id, 'id');
    const requestId = requireNonEmptyString(params.requestId, 'requestId');
    const body = await readJsonBody<{ answer?: unknown }>(request);
    const answer = requireServerRequestAnswer(isRecord(body) ? body.answer : undefined);
    const result = await getDaemonHarnessPort().answerRequest(sessionId, requestId, answer, {
      signal: request.signal
    });
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
