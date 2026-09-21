import { NextResponse } from 'next/server';
import { errorResponse, requireNonEmptyString } from '../../../../../../../lib/harness/http';
import { getDaemonHarnessPort } from '../../../../../../../lib/runtime-client/daemon-harness-port';

export async function GET(
  request: Request,
  context: { params: Promise<{ id: string }> }
): Promise<Response> {
  try {
    const sessionId = requireNonEmptyString((await context.params).id, 'sessionId');
    const result = await getDaemonHarnessPort().listNativePlanClarifications(
      sessionId,
      { signal: request.signal }
    );
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
