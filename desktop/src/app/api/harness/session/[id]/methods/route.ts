import { NextResponse } from 'next/server';
import type { ReplaceSelectedMethodsRequest } from '@chirality/runtime-contracts/v3';
import { errorResponse, readJsonBody, requireNonEmptyString } from '../../../../../../lib/harness/http';
import { getDaemonHarnessPort } from '../../../../../../lib/runtime-client/daemon-harness-port';

export async function PUT(
  request: Request,
  context: { params: Promise<{ id: string }> }
): Promise<Response> {
  try {
    const sessionId = requireNonEmptyString((await context.params).id, 'sessionId');
    const body = await readJsonBody<ReplaceSelectedMethodsRequest>(request);
    const result = await getDaemonHarnessPort().replaceSelectedMethods(sessionId, body, {
      signal: request.signal
    });
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
