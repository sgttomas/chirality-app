import { NextRequest, NextResponse } from 'next/server';
import { runAgentOrchestration } from '@/lib/orchestrator/agent';
import { readState } from '@/chirality-core/state/store';

export const runtime = 'nodejs';

/**
 * POST /api/agent/run  
 * Execute complete four-phase agent orchestration with SSE streaming
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json().catch(() => ({}));
    const { force = false, maxSeconds = 900 } = body;
    
    const state = readState();
    
    if (!state.problem.statement) {
      return NextResponse.json(
        { error: 'Problem statement required - please set problem first' },
        { status: 400 }
      );
    }
    
    // Set up SSE streaming
    const encoder = new TextEncoder();
    const stream = new ReadableStream({
      start(controller) {
        (async () => {
          try {
            for await (const event of runAgentOrchestration({
              problem: state.problem,
              maxSeconds,
              force
            })) {
              const data = `data: ${JSON.stringify(event)}\n\n`;
              controller.enqueue(encoder.encode(data));
            }
          } catch (error) {
            const errorEvent = {
              seq: 999,
              phase: 'finalize',
              status: 'error', 
              mode: 'three_pass',
              message: `Fatal error: ${error instanceof Error ? error.message : 'Unknown error'}`,
              timestamp: new Date().toISOString(),
              error: error instanceof Error ? error.message : 'Unknown error'
            };
            const errorData = `data: ${JSON.stringify(errorEvent)}\n\n`;
            controller.enqueue(encoder.encode(errorData));
            
            const doneData = `data: {"type":"done","runId":""}\n\n`;
            controller.enqueue(encoder.encode(doneData));
          } finally {
            controller.close();
          }
        })();
      }
    });
    
    return new Response(stream, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    });
    
  } catch (error) {
    console.error('Agent run API error:', error);
    return NextResponse.json(
      {
        error: 'Failed to start agent orchestration',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

/**
 * GET /api/agent/run
 * Get information about agent orchestration capabilities and current state
 */
export async function GET() {
  try {
    const state = readState();
    
    return NextResponse.json({
      available: true,
      description: 'Four-phase agentic orchestration with framework integration',
      status: 'ready',
      currentProblem: {
        hasStatement: !!state.problem.statement,
        title: state.problem.title || null
      },
      phases: ['framework', 'ingestion', 'refinement', 'persistence'],
      configuration: {
        defaultMaxSeconds: 900,
        orchestrationMode: process.env.CHIRALITY_ORCHESTRATION_MODE || 'two_pass'
      }
    });
    
  } catch (error) {
    return NextResponse.json({
      available: false,
      error: 'Failed to get agent status',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}