import { NextResponse } from 'next/server';
import { errorResponse, readJsonBody, requireNonEmptyString } from '../../../../lib/harness/http';
import { assertProjectRootAccessible } from '../../../../lib/harness/session-manager';

type ValidateRequest = {
  projectRoot: string;
};

export async function POST(request: Request): Promise<Response> {
  try {
    const body = await readJsonBody<ValidateRequest>(request);
    const requestedProjectRoot = requireNonEmptyString(body.projectRoot, 'projectRoot');
    const projectRoot = await assertProjectRootAccessible(requestedProjectRoot);
    return NextResponse.json({ ok: true, projectRoot }, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
