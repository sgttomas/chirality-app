import { NextResponse } from 'next/server';
import {
  errorResponse,
  readJsonBody,
  requireNonEmptyString
} from '../../../../lib/harness/http';
import { getDaemonHarnessPort } from '../../../../lib/runtime-client/daemon-harness-port';
import { InterruptRequest } from '@chirality/runtime-contracts/types';

export async function POST(request: Request): Promise<Response> {
  try {
    const body = await readJsonBody<InterruptRequest>(request);
    const sessionId = requireNonEmptyString(body.sessionId, 'sessionId');

    const result = await getDaemonHarnessPort().interrupt(
      { sessionId },
      { signal: request.signal }
    );
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
