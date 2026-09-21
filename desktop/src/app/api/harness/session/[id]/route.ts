import { NextResponse } from 'next/server';
import {
  errorResponse,
  requireNonEmptyString
} from '../../../../../lib/harness/http';
import { getDaemonHarnessPort } from '../../../../../lib/runtime-client/daemon-harness-port';

type RouteContext = {
  params: Promise<{
    id: string;
  }>;
};

export async function GET(request: Request, context: RouteContext): Promise<Response> {
  try {
    const { id } = await context.params;
    const sessionId = requireNonEmptyString(id, 'id');
    const result = await getDaemonHarnessPort().getSession(sessionId, {
      signal: request.signal
    });
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}

export async function DELETE(request: Request, context: RouteContext): Promise<Response> {
  try {
    const { id } = await context.params;
    const sessionId = requireNonEmptyString(id, 'id');
    const result = await getDaemonHarnessPort().deleteSession(sessionId, {
      signal: request.signal
    });
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
