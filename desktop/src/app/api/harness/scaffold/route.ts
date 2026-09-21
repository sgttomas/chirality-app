import { NextResponse } from 'next/server';
import { errorResponse, readJsonBody, requireNonEmptyString } from '../../../../lib/harness/http';
import { CoordinationMode } from '../../../../lib/harness/scaffold';
import { getDaemonHarnessPort } from '../../../../lib/runtime-client/daemon-harness-port';

type ScaffoldRequest = {
  executionRoot: string;
  decompositionPath: string;
  projectName?: string;
  coordinationMode?: CoordinationMode;
};

export async function POST(request: Request): Promise<Response> {
  try {
    const body = await readJsonBody<ScaffoldRequest>(request);
    const result = await getDaemonHarnessPort().scaffold(
      {
        executionRoot: requireNonEmptyString(body.executionRoot, 'executionRoot'),
        decompositionPath: requireNonEmptyString(body.decompositionPath, 'decompositionPath'),
        projectName: body.projectName?.trim(),
        coordinationMode: body.coordinationMode
      },
      { signal: request.signal }
    );

    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
