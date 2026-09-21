import { NextResponse } from 'next/server';
import { errorResponse, requireNonEmptyString } from '../../../../../lib/harness/http';
import { getHostedBootstrapPort } from '../../../../../lib/runtime-client/daemon-harness-port';

/**
 * Registration probe plus hosted account status for a registered folder. The
 * App-owned Runtime has no account-host admission step (D-GOV-43), so this
 * route is the renderer's only status path; the retired `runtime.hostedAccount`
 * IPC bridge no longer exists.
 */
export async function GET(request: Request): Promise<Response> {
  try {
    const projectRoot = requireNonEmptyString(
      new URL(request.url).searchParams.get('projectRoot'),
      'projectRoot'
    );
    const result = await getHostedBootstrapPort().getStatus(projectRoot, {
      signal: request.signal
    });
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
