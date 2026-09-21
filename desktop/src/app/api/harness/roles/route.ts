import { NextResponse } from 'next/server';
import { errorResponse, requireNonEmptyString } from '../../../../lib/harness/http';
import { getDaemonHarnessPort } from '../../../../lib/runtime-client/daemon-harness-port';

export async function GET(request: Request): Promise<Response> {
  try {
    const projectRoot = requireNonEmptyString(
      new URL(request.url).searchParams.get('projectRoot'),
      'projectRoot'
    );
    const result = await getDaemonHarnessPort().listRoles(projectRoot, {
      signal: request.signal
    });
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
