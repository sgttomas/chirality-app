import { NextResponse } from 'next/server';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import { errorResponse, readJsonBody, requireNonEmptyString } from '../../../../lib/harness/http';
import { getDaemonHarnessPort } from '../../../../lib/runtime-client/daemon-harness-port';

type UnparsedPermissionDecisionRequest = {
  sessionId?: unknown;
  toolUseId?: unknown;
  verdict?: unknown;
};

function requireVerdict(value: unknown): 'allow' | 'deny' {
  if (value === 'allow' || value === 'deny') {
    return value;
  }
  throw new HarnessError('INVALID_REQUEST', 400, "Field 'verdict' must be 'allow' or 'deny'");
}

export async function POST(request: Request): Promise<Response> {
  try {
    const body = await readJsonBody<UnparsedPermissionDecisionRequest>(request);
    const sessionId = requireNonEmptyString(body.sessionId, 'sessionId');
    const toolUseId = requireNonEmptyString(body.toolUseId, 'toolUseId');
    const verdict = requireVerdict(body.verdict);

    const result = await getDaemonHarnessPort().decidePermission(
      { sessionId, toolUseId, verdict },
      { signal: request.signal }
    );
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
