import { NextRequest, NextResponse } from 'next/server';
import { orchestrateProblem, OrchestrationProgress } from '@/chirality-core/orchestrate';
import { readState, writeState } from '@/chirality-core/state/store';
import { mirrorAfterWrite } from '@/lib/graph/integration';

/**
 * Shared three-pass orchestration logic used by both
 * /api/core/orchestrate (when three_pass mode enabled)
 * /api/core/orchestrate (unified endpoint, defaults to three_pass)
 */
export async function runThreePassOrchestration(request: NextRequest) {
  try {
    const state = readState();
    
    if (!state.problem.statement) {
      return NextResponse.json(
        { error: 'Problem statement required' },
        { status: 400 }
      );
    }

    const logs: string[] = [];
    const progressEvents: OrchestrationProgress[] = [];
    
    const addLog = (message: string) => {
      logs.push(`[${new Date().toLocaleTimeString()}] ${message}`);
      console.log(message);
    };

    addLog('Starting three-pass orchestration (V1→V2→V3)...');
    const startTime = Date.now();

    const { finals, history, U3 } = await orchestrateProblem(state.problem, {
      onProgress: (event) => {
        progressEvents.push(event);
        
        if (event.phase === 'start') {
          const deps = event.deps.length > 0 ? ` (deps: ${event.deps.join(', ')})` : ' (no deps)';
          addLog(`V${event.version} ${event.kind}: Starting generation${deps}`);
        } else if (event.phase === 'success') {
          addLog(`V${event.version} ${event.kind}: Completed in ${(event.ms! / 1000).toFixed(1)}s`);
        } else if (event.phase === 'error') {
          addLog(`V${event.version} ${event.kind}: Error - ${event.error}`);
        }
      }
    });

    const totalTime = ((Date.now() - startTime) / 1000).toFixed(1);
    addLog(`✅ Three-pass orchestration complete in ${totalTime}s`);
    
    // Log convergence status
    addLog(`Convergence: ${U3.convergence}`);
    if (U3.open_issues?.length) {
      addLog(`Open issues: ${U3.open_issues.join(', ')}`);
    }

    // Save the final state with metadata
    writeState({ 
      finals,
      metadata: {
        history,
        U3,
        generatedAt: new Date().toISOString(),
        orchestrationMode: 'three_pass',
        version: 3
      }
    });

    // Mirror to graph after successful file write (non-blocking)
    mirrorAfterWrite(finals);

    return NextResponse.json({ 
      success: true,
      orchestrationMode: 'three_pass',
      finals,
      history,
      U3,
      logs,
      progressEvents,
      totalTimeSeconds: parseFloat(totalTime)
    });

  } catch (error) {
    console.error('Three-pass orchestration error:', error);
    return NextResponse.json(
      { 
        error: 'Failed to orchestrate documents',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}