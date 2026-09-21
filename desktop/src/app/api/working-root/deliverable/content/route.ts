import { NextResponse } from 'next/server';
import { readDeliverableContent } from '../../../../../lib/workspace/deliverable-contracts';
import { workspaceErrorPayload } from '../../../../../lib/workspace/filesystem';

// D-APP-20 Option B: read-only batch content read, keyed by deliverablePath + an
// optional relative `file` within the deliverable (defaults to _STATUS.md).
export async function GET(request: Request): Promise<Response> {
  try {
    const url = new URL(request.url);
    const projectRoot = url.searchParams.get('projectRoot') ?? '';
    const deliverablePath = url.searchParams.get('deliverablePath') ?? '';
    const fileParam = url.searchParams.get('file');
    const result = await readDeliverableContent({
      projectRoot,
      deliverablePath,
      file: fileParam ?? undefined
    });

    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    const payload = workspaceErrorPayload(error);
    return NextResponse.json(payload.body, { status: payload.status });
  }
}
