import { NextResponse } from 'next/server';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import { errorResponse, requireNonEmptyString } from '../../../../lib/harness/http';
import { getDaemonHarnessPort } from '../../../../lib/runtime-client/daemon-harness-port';

export async function GET(request: Request): Promise<Response> {
  try {
    const params = new URL(request.url).searchParams;
    const projectRoot = requireNonEmptyString(params.get('projectRoot'), 'projectRoot');
    const kind = params.get('kind');
    if (kind !== null && kind !== 'skill' && kind !== 'workflow') {
      throw new HarnessError('INVALID_REQUEST', 400, "Field 'kind' must be 'skill' or 'workflow'");
    }
    const query = params.get('query')?.trim() || undefined;
    const result = await getDaemonHarnessPort().listMethods(
      { projectRoot, ...(kind === null ? {} : { kind }), ...(query ? { query } : {}) },
      { signal: request.signal }
    );
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
