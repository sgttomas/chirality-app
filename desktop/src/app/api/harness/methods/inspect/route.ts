import { NextResponse } from 'next/server';
import { errorResponse, requireNonEmptyString } from '../../../../../lib/harness/http';
import { getDaemonHarnessPort } from '../../../../../lib/runtime-client/daemon-harness-port';

export async function GET(request: Request): Promise<Response> {
  try {
    const params = new URL(request.url).searchParams;
    const projectRoot = requireNonEmptyString(params.get('projectRoot'), 'projectRoot');
    const qualifiedId = requireNonEmptyString(params.get('qualifiedId'), 'qualifiedId');
    const result = await getDaemonHarnessPort().inspectMethod(
      { projectRoot, qualifiedId },
      { signal: request.signal }
    );
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
