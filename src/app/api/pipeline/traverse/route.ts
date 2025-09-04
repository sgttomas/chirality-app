/**
 * POST /api/pipeline/traverse - New semantic valley traversal API
 * 
 * This endpoint implements the canonical semantic valley traversal using
 * the nine-station pipeline (S0-S8) instead of the legacy V1/V2/V3 system.
 */

import { NextRequest, NextResponse } from 'next/server';
import { runTraversal } from '@/lib/orchestrator/pipeline';
import { Packet } from '@/lib/utils/packets';
import { M } from '@/types/framework';

interface TraverseRequest {
  problem: { title: string; statement: string };
  matrices?: { C?: any[]; D?: any[]; X?: any[]; E?: any[] };
  startStation?: 'S0' | 'S1' | 'S2' | 'S3' | 'S4' | 'S5' | 'S6' | 'S7' | 'S8';
  endStation?: 'S0' | 'S1' | 'S2' | 'S3' | 'S4' | 'S5' | 'S6' | 'S7' | 'S8';
}

interface TraverseResponse {
  traversalId: string;
  stations: {
    S0?: any;
    S1?: any;
    S2?: any;
    S3?: any;
    S4?: any;
    S5?: any;
    S6?: any;
    S7?: any;
    S8?: any;
  };
  resolution: Packet<M>;
  metadata: {
    durationMs: number;
    matrixInjections: string[];
  };
}

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    // Check feature flag
    const pipelineEnabled = process.env.NEW_PIPELINE_ENABLED === 'true';
    if (!pipelineEnabled) {
      return NextResponse.json(
        { 
          error: 'New pipeline is not enabled',
          hint: 'Set NEW_PIPELINE_ENABLED=true in environment'
        },
        { status: 503 }
      );
    }
    
    // Parse request body
    const body: TraverseRequest = await request.json();
    
    // Validate required fields
    if (!body.problem?.title || !body.problem?.statement) {
      return NextResponse.json(
        { error: 'Problem title and statement are required' },
        { status: 400 }
      );
    }
    
    console.log('[API] Starting semantic valley traversal via new pipeline');
    console.log(`[API] Problem: ${body.problem.title}`);
    
    const startTime = Date.now();
    
    // Run the traversal
    const traversalState = await runTraversal(body.problem, {
      matrices: body.matrices,
      startStation: body.startStation,
      endStation: body.endStation,
      onProgress: (state) => {
        console.log(`[API] Progress: Currently at station ${state.currentStation}`);
      }
    });
    
    const endTime = Date.now();
    const durationMs = endTime - startTime;
    
    // Extract resolution from S8 (final alethic station)
    const resolution: Packet<M> = traversalState.stations.S8 || {
      text: [{
        statement: 'Traversal incomplete - no resolution generated',
        residual_risk: ['Traversal did not reach S8']
      }],
      flags: { risk: true }
    };
    
    // Build response according to specification
    const response: TraverseResponse = {
      traversalId: traversalState.problemId,
      stations: traversalState.stations,
      resolution,
      metadata: {
        durationMs,
        matrixInjections: traversalState.metadata?.matrixInjections || []
      }
    };
    
    console.log(`[API] Traversal completed in ${durationMs}ms`);
    console.log(`[API] Matrix injections: ${response.metadata.matrixInjections.join(', ') || 'none'}`);
    
    return NextResponse.json(response);
    
  } catch (error) {
    console.error('[API] Traversal failed:', error);
    
    return NextResponse.json(
      { 
        error: 'Traversal failed',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

/**
 * GET /api/pipeline/traverse - Get pipeline status and configuration
 */
export async function GET(): Promise<NextResponse> {
  const pipelineEnabled = process.env.NEW_PIPELINE_ENABLED === 'true';
  
  return NextResponse.json({
    pipelineEnabled,
    version: '1.0.0',
    stations: ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8'],
    modalities: {
      S0: 'systematic',
      S1: 'systematic',
      S2: 'process',
      S3: 'epistemic',
      S4: 'process',
      S5: 'epistemic',
      S6: 'alethic',
      S7: 'epistemic',
      S8: 'alethic'
    },
    matrixInjectionPoints: {
      'C': 'S1',
      'D': 'S2', 
      'X': 'S3',
      'E': 'S6'
    }
  });
}