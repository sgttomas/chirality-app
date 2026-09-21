import { NextResponse } from 'next/server';
import {
  normalizeProjectRoot,
  scanProjectScopes,
  workspaceErrorPayload
} from '../../../../lib/workspace/filesystem';

export async function GET(request: Request): Promise<Response> {
  try {
    const url = new URL(request.url);
    const rawProjectRoot = url.searchParams.get('projectRoot') ?? '';
    const projectRoot = await normalizeProjectRoot(rawProjectRoot);
    const scanResult = await scanProjectScopes(projectRoot);

    return NextResponse.json(
      {
        projectRoot,
        scannedAt: new Date().toISOString(),
        ...scanResult
      },
      { status: 200 }
    );
  } catch (error) {
    const payload = workspaceErrorPayload(error);
    return NextResponse.json(payload.body, { status: payload.status });
  }
}
