import { NextResponse } from 'next/server';
import { errorResponse } from '../../../../../lib/harness/http';
import { getHostedBootstrapPort } from '../../../../../lib/runtime-client/daemon-harness-port';
import { readHostedBootstrapProjectRoot } from '../request';

/**
 * Retained path, no-op behaviour. Under D-GOV-43 there is no provider-network
 * consent step; this route reports the current account status without
 * recording anything. A `consent` field in the body is ignored.
 */
export async function POST(request: Request): Promise<Response> {
  try {
    const projectRoot = await readHostedBootstrapProjectRoot(request);
    const result = await getHostedBootstrapPort().grantProviderNetworkConsent(
      projectRoot,
      { signal: request.signal }
    );
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
