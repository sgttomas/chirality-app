import { NextRequest, NextResponse } from 'next/server';
import { DocKind } from '@/chirality-core/contracts';

export const runtime = 'nodejs';

/**
 * POST /api/core/generate-from-matrices
 * Generate documents using matrix-driven approach with deterministic scaffolding
 */
export async function POST(request: NextRequest) {
  // TODO: Implement matrix-driven generation
  return NextResponse.json(
    { error: 'Matrix generation not yet implemented' },
    { status: 501 }
  );
}

/**
 * GET /api/core/generate-from-matrices
 * Get information about matrix generation capabilities
 */
export async function GET() {
  return NextResponse.json({
    available: false,
    description: 'Matrix-driven document generation (not yet implemented)',
    status: 'under_development'
  });
}