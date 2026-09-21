import { NextResponse } from 'next/server';
import type { SessionSteerReceiptRequest } from '@chirality/runtime-contracts';
import { errorResponse, readJsonBody, requireNonEmptyString } from '../../../../../../../../lib/harness/http';
import { getDaemonHarnessPort } from '../../../../../../../../lib/runtime-client/daemon-harness-port';

export async function POST(request: Request, context: { params: Promise<{ id: string }> }): Promise<Response> {
  try {
    const sessionId = requireNonEmptyString((await context.params).id, 'id');
    const body = await readJsonBody<SessionSteerReceiptRequest>(request);
    const result = await getDaemonHarnessPort().steerReceipt(sessionId, {
      operationId: requireNonEmptyString(body?.operationId, 'operationId'),
      expectedTurnId: requireNonEmptyString(body?.expectedTurnId, 'expectedTurnId')
    }, { signal: request.signal });
    return NextResponse.json(result);
  } catch (error) { return errorResponse(error); }
}
