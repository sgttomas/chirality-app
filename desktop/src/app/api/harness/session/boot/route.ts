import { NextResponse } from 'next/server';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import {
  errorResponse,
  readJsonBody,
  requireNonEmptyString
} from '../../../../../lib/harness/http';
import { getDaemonHarnessPort } from '../../../../../lib/runtime-client/daemon-harness-port';
import { SessionBootRequest } from '@chirality/runtime-contracts/types';

export async function POST(request: Request): Promise<Response> {
  try {
    const body = await readJsonBody<SessionBootRequest>(request);
    const sessionId = requireNonEmptyString(body.sessionId, 'sessionId');

    const result = await getDaemonHarnessPort().bootSession(
      { sessionId, opts: body.opts },
      { signal: request.signal }
    );
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
