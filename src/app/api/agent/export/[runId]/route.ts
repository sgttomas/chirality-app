import { NextRequest, NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';
import { validateRunId } from '@/lib/utils/validation';
import { createReadStream } from 'fs';
import archiver from 'archiver';
import { PassThrough } from 'stream';

export const runtime = 'nodejs';

/**
 * GET /api/agent/export/[runId]
 * Export a complete run bundle as a ZIP archive
 * Includes manifest, index.json, snapshots, and generated documents
 */
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ runId: string }> }
) {
  try {
    const resolvedParams = await params;
    const runId = resolvedParams.runId;
    
    // Validate run_id format for security
    const validation = validateRunId(runId);
    if (!validation.valid) {
      return NextResponse.json(
        { error: `Invalid run_id: ${validation.error}` },
        { status: 400 }
      );
    }
    
    // RBAC check - ensure user has at least viewer role
    const userRole = request.headers.get('X-Role') || process.env.DEFAULT_ROLE || 'viewer';
    const allowedRoles = (process.env.ALLOWED_VIEWER_ROLES || 'viewer,operator,approver,admin').split(',');
    if (!allowedRoles.includes(userRole)) {
      // Log unauthorized access attempt for audit
      console.log(JSON.stringify({
        level: 'warn',
        event: 'unauthorized_export_attempt',
        runId,
        timestamp: new Date().toISOString(),
        user: request.headers.get('X-User') || 'anonymous',
        role: userRole,
        ip: request.headers.get('X-Forwarded-For') || 'unknown'
      }));
      
      return NextResponse.json(
        { error: 'Insufficient permissions to export runs' },
        { status: 403 }
      );
    }
    
    const runsDir = process.env.CHIRALITY_RUNS_DIR || './runs';
    const runPath = path.join(runsDir, runId);
    
    // Verify run directory exists
    try {
      await fs.access(runPath);
    } catch {
      return NextResponse.json(
        { error: `Run not found: ${runId}` },
        { status: 404 }
      );
    }
    
    // Create streaming ZIP archive using PassThrough
    const archive = archiver('zip', {
      zlib: { level: 6 } // Balanced compression for streaming
    });
    
    const passThrough = new PassThrough();
    
    // Pipe archive to PassThrough stream for web streaming
    archive.pipe(passThrough);
    
    // Handle archive errors
    archive.on('error', (err) => {
      console.error('Archive error:', err);
      passThrough.destroy(err);
    });
    
    // Add run_manifest.json if exists
    const manifestPath = path.join(runPath, 'run_manifest.json');
    try {
      await fs.access(manifestPath);
      archive.file(manifestPath, { name: 'run_manifest.json' });
    } catch {
      // run_manifest.json is optional
    }
    
    // Add index.json (framework manifest)
    const indexPath = path.join(runPath, 'index.json');
    try {
      await fs.access(indexPath);
      archive.file(indexPath, { name: 'index.json' });
    } catch {
      console.warn(`Missing index.json for run ${runId}`);
    }
    
    // Add snapshots directory
    const snapshotsPath = path.join(runPath, 'snapshots');
    try {
      await fs.access(snapshotsPath);
      archive.directory(snapshotsPath, 'snapshots');
    } catch {
      console.warn(`Missing snapshots directory for run ${runId}`);
    }
    
    // Add drafts directory if exists
    const draftsPath = path.join(runPath, 'drafts');
    try {
      await fs.access(draftsPath);
      archive.directory(draftsPath, 'drafts');
    } catch {
      // Drafts are optional
    }
    
    // Add finals directory if exists
    const finalsPath = path.join(runPath, 'finals');
    try {
      await fs.access(finalsPath);
      archive.directory(finalsPath, 'finals');
    } catch {
      // Finals are optional
    }
    
    // Add generated documents (DS, SP, X, M) if they exist
    const documents = ['DS.json', 'SP.json', 'X.json', 'M.json'];
    for (const doc of documents) {
      const docPath = path.join(runPath, doc);
      try {
        await fs.access(docPath);
        archive.file(docPath, { name: doc });
      } catch {
        // Individual documents are optional
      }
    }
    
    // Add metadata file with export information
    const exportMetadata = {
      runId,
      exportedAt: new Date().toISOString(),
      exportedBy: request.headers.get('X-User') || 'anonymous',
      version: '1.0.0'
    };
    archive.append(JSON.stringify(exportMetadata, null, 2), { name: 'export_metadata.json' });
    
    // Finalize archive asynchronously
    const finalizationPromise = archive.finalize();
    
    // Log export event for audit
    console.log(JSON.stringify({
      level: 'info',
      event: 'run_exported',
      runId,
      timestamp: new Date().toISOString(),
      user: request.headers.get('X-User') || 'anonymous',
      mode: 'streaming'
    }));
    
    // Convert PassThrough to ReadableStream for web response
    const webReadableStream = new ReadableStream({
      start(controller) {
        passThrough.on('data', (chunk) => {
          controller.enqueue(new Uint8Array(chunk));
        });
        
        passThrough.on('end', () => {
          controller.close();
        });
        
        passThrough.on('error', (err) => {
          controller.error(err);
        });
      },
      cancel() {
        passThrough.destroy();
      }
    });
    
    // Return streaming ZIP response
    return new Response(webReadableStream, {
      status: 200,
      headers: {
        'Content-Type': 'application/zip',
        'Content-Disposition': `attachment; filename="run_${runId}.zip"`,
        'Cache-Control': 'private, no-cache'
      }
    });
    
    // Ensure finalization completes
    await finalizationPromise;
    
  } catch (error) {
    console.error('Export error:', error);
    return NextResponse.json(
      {
        error: 'Failed to export run',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}