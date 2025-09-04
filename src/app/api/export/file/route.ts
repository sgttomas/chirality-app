import { NextRequest, NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';

function badRequest(message: string, details?: Record<string, any>) {
  return NextResponse.json({ code: 'ERR_BAD_REQUEST', message, details }, { status: 400 });
}

export async function GET(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const runId = searchParams.get('runId') || '';
    const name = searchParams.get('name') || '';

    if (!runId || !name) {
      return badRequest('Missing required query params: runId and name');
    }

    // Only allow the two known export files
    const allowed = new Set(['run.json', 'packets.jsonl']);
    if (!allowed.has(name)) {
      return badRequest('Invalid file name. Allowed: run.json, packets.jsonl', { name });
    }

    const runsDir = path.join(process.cwd(), 'runs');
    const runDir = path.join(runsDir, runId);
    const filePath = path.join(runDir, name);

    try {
      const stat = await fs.stat(filePath);
      if (!stat.isFile()) {
        return NextResponse.json(
          { code: 'ERR_RUN_NOT_FOUND', message: `File not found for run ${runId}`, details: { runId, name } },
          { status: 404 }
        );
      }
    } catch {
      return NextResponse.json(
        { code: 'ERR_RUN_NOT_FOUND', message: `File not found for run ${runId}`, details: { runId, name } },
        { status: 404 }
      );
    }

    const file = await fs.readFile(filePath);
    const contentType = name.endsWith('.json') ? 'application/json' : 'application/octet-stream';
    return new NextResponse(new Uint8Array(file), {
      status: 200,
      headers: {
        'Content-Type': contentType,
        'Content-Disposition': `attachment; filename="${name}"`,
      },
    });
  } catch (error) {
    return NextResponse.json(
      { code: 'ERR_EXPORT_FAILED', message: 'Failed to read export file', details: { error: error instanceof Error ? error.message : 'Unknown error' } },
      { status: 500 }
    );
  }
}

