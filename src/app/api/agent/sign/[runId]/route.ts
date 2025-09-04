import { validateRunId } from '@/lib/utils/validation';
import { promises as fs } from 'fs';
import { NextRequest, NextResponse } from 'next/server';
import path from 'path';

export const runtime = 'nodejs';

interface RunManifest {
  run_id: string;
  immutable?: boolean;
  signatures?: Array<{
    user: string;
    role: string;
    justification: string;
    signedAt: string;
  }>;
  [key: string]: any;
}

/**
 * POST /api/agent/sign/[runId]
 * Sign-off on a run, marking it as approved and immutable
 * Requires approver role
 */
export async function POST(
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
    
    // Parse request body
    const body = await request.json();
    const { justification } = body;
    
    if (!justification || typeof justification !== 'string' || justification.trim().length < 10) {
      return NextResponse.json(
        { error: 'Justification must be at least 10 characters' },
        { status: 400 }
      );
    }
    
    // Extract user identity and role
    // In production, this would come from your auth context (NextAuth, Clerk, etc.)
    // For now, use dev headers or env-based stub
    const user = request.headers.get('X-User') || process.env.DEFAULT_APPROVER || 'dev-approver';
    const userRole = request.headers.get('X-Role') || process.env.DEFAULT_ROLE || 'approver';
    
    // Check if user has approver role
    // In production, integrate with your RBAC system
    const allowedRoles = (process.env.ALLOWED_APPROVER_ROLES || 'approver,admin').split(',');
    if (!allowedRoles.includes(userRole)) {
      return NextResponse.json(
        { error: 'Insufficient permissions: approver role required' },
        { status: 403 }
      );
    }
    
    // Path to run manifest
    const runsDir = process.env.CHIRALITY_RUNS_DIR || './runs';
    const manifestPath = path.join(runsDir, runId, 'run_manifest.json');
    
    // Check if manifest exists
    let manifest: RunManifest;
    try {
      const manifestContent = await fs.readFile(manifestPath, 'utf8');
      manifest = JSON.parse(manifestContent);
    } catch (error) {
      return NextResponse.json(
        { error: `Run manifest not found for ${runId}` },
        { status: 404 }
      );
    }
    
    // Check if already immutable
    if (manifest.immutable) {
      return NextResponse.json(
        { error: 'Run is already immutable and cannot be modified' },
        { status: 409 }
      );
    }
    
    // Add signature block
    const signature = {
      user,
      role: userRole,
      justification: justification.trim(),
      signedAt: new Date().toISOString()
    };
    
    if (!manifest.signatures) {
      manifest.signatures = [];
    }
    manifest.signatures.push(signature);
    
    // Mark as immutable after first approval
    manifest.immutable = true;
    
    // Write back manifest (atomic write with temp file)
    const tempPath = `${manifestPath}.tmp`;
    try {
      await fs.writeFile(tempPath, JSON.stringify(manifest, null, 2), 'utf8');
      await fs.rename(tempPath, manifestPath);
    } catch (error) {
      // Cleanup temp file on error
      try {
        await fs.unlink(tempPath);
      } catch {}
      throw error;
    }
    
    // Log audit event (in production, send to audit log service)
    console.log(JSON.stringify({
      level: 'info',
      event: 'run_signed',
      runId,
      user,
      role: userRole,
      timestamp: signature.signedAt,
      details: {
        justificationLength: justification.length,
        isFirstSignature: manifest.signatures.length === 1
      }
    }));
    
    return NextResponse.json({
      success: true,
      runId,
      signature,
      immutable: manifest.immutable,
      signatureCount: manifest.signatures.length
    });
    
  } catch (error) {
    console.error('Sign-off error:', error);
    return NextResponse.json(
      { 
        error: 'Failed to sign run',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

/**
 * GET /api/agent/sign/[runId]
 * Get signature status for a run
 */
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ runId: string }> }
) {
  try {
    const resolvedParams = await params;
    const runId = resolvedParams.runId;
    
    // Validate run_id format
    const validation = validateRunId(runId);
    if (!validation.valid) {
      return NextResponse.json(
        { error: `Invalid run_id: ${validation.error}` },
        { status: 400 }
      );
    }
    
    // Path to run manifest
    const runsDir = process.env.CHIRALITY_RUNS_DIR || './runs';
    const manifestPath = path.join(runsDir, runId, 'run_manifest.json');
    
    // Check if manifest exists
    let manifest: RunManifest;
    try {
      const manifestContent = await fs.readFile(manifestPath, 'utf8');
      manifest = JSON.parse(manifestContent);
    } catch (error) {
      return NextResponse.json(
        { error: `Run manifest not found for ${runId}` },
        { status: 404 }
      );
    }
    
    return NextResponse.json({
      runId,
      immutable: manifest.immutable || false,
      signatures: manifest.signatures || [],
      signatureCount: (manifest.signatures || []).length,
      canSign: !manifest.immutable
    });
    
  } catch (error) {
    console.error('Get signature status error:', error);
    return NextResponse.json(
      { 
        error: 'Failed to get signature status',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}