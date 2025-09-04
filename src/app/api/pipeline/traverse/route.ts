import { NextRequest, NextResponse } from 'next/server';
import { createOrchestrator } from '../../../../core/orchestrator';

export interface TraverseRequest {
  problem: {
    title: string;
    statement: string;
    initialVector?: Record<string, any>;
  };
  options?: {
    mode?: 'full' | 'foundation'; // Default: 'foundation'
  };
}

export interface TraverseResponse {
  traversalId: string;
  stations: Array<{
    station: string;
    label: string;
    modality: string;
    operation: string;
    duration: number;
    output: string;
  }>;
  resolution: string;
  metadata: {
    durations: Record<string, number>;
    totalDuration: number;
    totalTokens: number;
  };
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, any>;
}

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    // Parse and validate request body
    let body: TraverseRequest;
    try {
      body = await request.json();
    } catch (error) {
      return NextResponse.json(
        { 
          code: 'ERR_INVALID_JSON', 
          message: 'Invalid JSON in request body' 
        } as ApiError,
        { status: 400 }
      );
    }

    // Validate required fields
    if (!body.problem?.title || !body.problem?.statement) {
      return NextResponse.json(
        {
          code: 'ERR_MISSING_FIELDS',
          message: 'Missing required fields: problem.title and problem.statement are required',
          details: { received: body }
        } as ApiError,
        { status: 400 }
      );
    }

    // Validate title and statement are strings
    if (typeof body.problem.title !== 'string' || typeof body.problem.statement !== 'string') {
      return NextResponse.json(
        {
          code: 'ERR_INVALID_TYPES',
          message: 'problem.title and problem.statement must be strings',
          details: { 
            titleType: typeof body.problem.title,
            statementType: typeof body.problem.statement
          }
        } as ApiError,
        { status: 400 }
      );
    }

    // Validate statement is not empty
    if (body.problem.statement.trim().length === 0) {
      return NextResponse.json(
        {
          code: 'ERR_EMPTY_STATEMENT',
          message: 'problem.statement cannot be empty',
        } as ApiError,
        { status: 400 }
      );
    }

    // Create orchestrator
    let orchestrator;
    try {
      // Allow fallback mode for foundation traversals (default)
      const mode = body.options?.mode || 'foundation';
      const allowFallback = mode === 'foundation';
      orchestrator = await createOrchestrator(undefined, allowFallback);
    } catch (error) {
      console.error('Failed to create orchestrator:', error);
      return NextResponse.json(
        {
          code: 'ERR_ORCHESTRATOR_INIT',
          message: 'Failed to initialize orchestrator. Check OpenAI API key configuration.',
          details: { error: error instanceof Error ? error.message : 'Unknown error' }
        } as ApiError,
        { status: 500 }
      );
    }

    // Run traversal
    const startTime = Date.now();
    let result;
    try {
      result = await orchestrator.runTraversal(body.problem, {
        mode: body.options?.mode || 'foundation'
      });
    } catch (error) {
      console.error('Traversal failed:', error);
      return NextResponse.json(
        {
          code: 'ERR_TRAVERSAL_FAILED',
          message: 'Semantic valley traversal failed',
          details: { error: error instanceof Error ? error.message : 'Unknown error' }
        } as ApiError,
        { status: 500 }
      );
    }

    // Format response
    const response: TraverseResponse = {
      traversalId: result.runId,
      stations: result.packets.map(packet => ({
        station: packet.station,
        label: packet.meta?.label || `Station ${packet.station}`,
        modality: packet.modality,
        operation: Object.keys(packet.payload)[0] || 'Unknown',
        duration: packet.meta?.duration || 0,
        output: packet.payload[Object.keys(packet.payload)[0]] || ''
      })),
      resolution: result.resolution,
      metadata: result.metadata
    };

    console.log(`[API] Traversal completed in ${Date.now() - startTime}ms:`, {
      traversalId: result.runId,
      stationCount: result.packets.length,
      totalTokens: result.metadata.totalTokens
    });

    return NextResponse.json(response);

  } catch (error) {
    console.error('Unexpected error in traverse endpoint:', error);
    return NextResponse.json(
      {
        code: 'ERR_INTERNAL',
        message: 'Internal server error',
        details: { error: error instanceof Error ? error.message : 'Unknown error' }
      } as ApiError,
      { status: 500 }
    );
  }
}