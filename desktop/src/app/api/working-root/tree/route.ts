import { NextResponse } from 'next/server';
import {
  normalizeProjectRoot,
  readProjectRootTree,
  workspaceErrorPayload
} from '../../../../lib/workspace/filesystem';

function parseDepth(value: string | null): number {
  if (!value) {
    return 3;
  }

  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    return 3;
  }

  return Math.max(1, Math.min(6, Math.floor(parsed)));
}

export async function GET(request: Request): Promise<Response> {
  try {
    const url = new URL(request.url);
    const rawProjectRoot = url.searchParams.get('projectRoot') ?? '';
    const depth = parseDepth(url.searchParams.get('depth'));
    const projectRoot = await normalizeProjectRoot(rawProjectRoot);
    const root = await readProjectRootTree(projectRoot, depth);

    return NextResponse.json(
      {
        projectRoot,
        depth,
        scannedAt: new Date().toISOString(),
        root
      },
      { status: 200 }
    );
  } catch (error) {
    const payload = workspaceErrorPayload(error);
    return NextResponse.json(payload.body, { status: payload.status });
  }
}
