import { NextResponse } from 'next/server';
import { readDeliverableStatus } from '../../../../../lib/workspace/deliverable-contracts';
import { workspaceErrorPayload } from '../../../../../lib/workspace/filesystem';

export async function GET(request: Request): Promise<Response> {
  try {
    const url = new URL(request.url);
    const projectRoot = url.searchParams.get('projectRoot') ?? '';
    const deliverablePath = url.searchParams.get('deliverablePath') ?? '';
    const snapshot = await readDeliverableStatus(projectRoot, deliverablePath);

    return NextResponse.json(snapshot, { status: 200 });
  } catch (error) {
    const payload = workspaceErrorPayload(error);
    return NextResponse.json(payload.body, { status: payload.status });
  }
}
