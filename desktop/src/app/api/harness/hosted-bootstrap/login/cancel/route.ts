import { NextResponse } from 'next/server';
import { errorResponse } from '../../../../../../lib/harness/http';
import { getHostedBootstrapPort } from '../../../../../../lib/runtime-client/daemon-harness-port';
import { readHostedBootstrapProjectRoot } from '../../request';

export async function POST(request: Request): Promise<Response> {
  try {
    const projectRoot = await readHostedBootstrapProjectRoot(request);
    const result = await getHostedBootstrapPort().cancelLogin(projectRoot, {
      signal: request.signal
    });
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
