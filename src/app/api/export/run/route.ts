import { NextRequest, NextResponse } from 'next/server';
import { Exporter } from '../../../../core/exporter';
import { ApiError } from '../../pipeline/traverse/route';

export interface ExportRunResponse {
  runId: string;
  files: {
    runJson: string;
    packetsJsonl: string;
  };
  size: {
    runJson: number;
    packetsJsonl: number;
    total: number;
  };
}

export async function GET(request: NextRequest): Promise<NextResponse> {
  try {
    // Extract runId from query parameters
    const { searchParams } = new URL(request.url);
    const runId = searchParams.get('runId');

    if (!runId) {
      return NextResponse.json(
        {
          code: 'ERR_MISSING_RUN_ID',
          message: 'Missing required query parameter: runId'
        } as ApiError,
        { status: 400 }
      );
    }

    // Validate runId format (basic validation)
    if (!/^run_\d+_[a-z0-9]+$/.test(runId)) {
      return NextResponse.json(
        {
          code: 'ERR_INVALID_RUN_ID',
          message: 'Invalid runId format. Expected format: run_{timestamp}_{random}',
          details: { runId }
        } as ApiError,
        { status: 400 }
      );
    }

    // Use the exporter to check if run exists and get file information
    const exporter = new Exporter();
    
    try {
      // Check if the run exists
      const runExists = await exporter.runExists(runId);
      
      if (!runExists) {
        return NextResponse.json(
          {
            code: 'ERR_RUN_NOT_FOUND',
            message: `Run ${runId} not found. Files may not have been exported yet.`,
            details: { 
              runId,
              expectedFiles: [
                `runs/${runId}/run.json`,
                `runs/${runId}/packets.jsonl`
              ]
            }
          } as ApiError,
          { status: 404 }
        );
      }

      // Get file sizes
      const sizes = await exporter.getRunSize(runId);
      
      const response: ExportRunResponse = {
        runId,
        files: {
          runJson: `runs/${runId}/run.json`,
          packetsJsonl: `runs/${runId}/packets.jsonl`
        },
        size: sizes
      };

      return NextResponse.json(response);

    } catch (error) {
      console.error('Export endpoint error:', error);
      return NextResponse.json(
        {
          code: 'ERR_EXPORT_FAILED',
          message: 'Failed to retrieve run export information',
          details: { 
            runId,
            error: error instanceof Error ? error.message : 'Unknown error'
          }
        } as ApiError,
        { status: 500 }
      );
    }

  } catch (error) {
    console.error('Unexpected error in export endpoint:', error);
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