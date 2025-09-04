export const runtime = 'nodejs';

import { NextRequest, NextResponse } from 'next/server';
import { runDoc } from '@/chirality-core/orchestrate';
import { readState, writeState } from '@/chirality-core/state/store';
import { DocKind, Triple } from '@/chirality-core/contracts';
import { mirrorAfterWrite } from '@/lib/graph/integration';
import { runThreePassOrchestration } from '@/lib/orchestrator/threePassOrchestrator';

/**
 * Orchestration endpoint that can switch between two-pass and three-pass modes
 * based on CHIRALITY_ORCHESTRATION_MODE environment variable.
 */
export async function POST(request: NextRequest) {
  // Check orchestration mode from environment
  const orchestrationMode = process.env.CHIRALITY_ORCHESTRATION_MODE || 'three_pass';
  
  // If three_pass mode is enabled, delegate to the three-pass orchestrator
  if (orchestrationMode === 'three_pass') {
    return runThreePassOrchestration(request);
  }
  
  // Otherwise, run the legacy two-pass orchestration
  return runTwoPassOrchestration(request);
}

async function runTwoPassOrchestration(request: NextRequest) {
  try {
    const state = readState();
    
    // Check if problem is defined
    if (!state.problem.statement) {
      return NextResponse.json(
        { error: 'Problem statement required' },
        { status: 400 }
      );
    }

    const logs: string[] = [];
    const addLog = (message: string) => {
      logs.push(`[${new Date().toLocaleTimeString()}] ${message}`);
      console.log(message);
    };

    // Track all versions
    const pass1: Record<DocKind, Triple<any>> = {} as any;
    const pass2: Record<DocKind, Triple<any>> = {} as any;

    // ========== PASS 1: Initial Sequential Generation ==========
    addLog('Starting Pass 1: Initial document generation...');
    
    // Generate DS
    addLog('Pass 1: Generating DS...');
    const t0_ds = Date.now();
    pass1.DS = await runDoc('DS', state.problem, {});
    addLog(`Pass 1: DS generated in ${((Date.now() - t0_ds) / 1000).toFixed(1)}s`);

    // Generate SP (using DS)
    addLog('Pass 1: Generating SP...');
    const t0_sp = Date.now();
    pass1.SP = await runDoc('SP', state.problem, { DS: pass1.DS });
    addLog(`Pass 1: SP generated in ${((Date.now() - t0_sp) / 1000).toFixed(1)}s`);

    // Generate X (using DS, SP)
    addLog('Pass 1: Generating X...');
    const t0_x = Date.now();
    pass1.X = await runDoc('X', state.problem, { DS: pass1.DS, SP: pass1.SP });
    addLog(`Pass 1: X generated in ${((Date.now() - t0_x) / 1000).toFixed(1)}s`);

    // Generate M (using DS, SP, X)
    addLog('Pass 1: Generating M...');
    const t0_m = Date.now();
    pass1.M = await runDoc('M', state.problem, { DS: pass1.DS, SP: pass1.SP, X: pass1.X });
    addLog(`Pass 1: M generated in ${((Date.now() - t0_m) / 1000).toFixed(1)}s`);

    addLog('Pass 1 complete!');

    // ========== PASS 2: Refinement with Cross-References ==========
    addLog('Starting Pass 2: Refinement with cross-references...');

    // Refine DS using insights from SP, X, M
    addLog('Pass 2: Refining DS with insights from SP, X, M...');
    const t1_ds = Date.now();
    pass2.DS = await runDoc('DS', state.problem, pass1, {
      extraConstraints: [
        'Refine based on procedural requirements from SP',
        'Incorporate solution insights from X',
        'Address guidance considerations from M'
      ]
    });
    addLog(`Pass 2: DS refined in ${((Date.now() - t1_ds) / 1000).toFixed(1)}s`);

    // Refine SP using new DS + original X, M
    addLog('Pass 2: Refining SP with new DS and insights from X, M...');
    const t1_sp = Date.now();
    pass2.SP = await runDoc('SP', state.problem, { 
      DS: pass2.DS,  // Use refined DS
      X: pass1.X,    // Original X
      M: pass1.M     // Original M
    }, {
      extraConstraints: [
        'Align with refined data specifications from DS',
        'Consider solution approach from X',
        'Incorporate guidance requirements from M'
      ]
    });
    addLog(`Pass 2: SP refined in ${((Date.now() - t1_sp) / 1000).toFixed(1)}s`);

    // Refine X using new DS, SP + original M
    addLog('Pass 2: Refining X with new DS, SP and insights from M...');
    const t1_x = Date.now();
    pass2.X = await runDoc('X', state.problem, { 
      DS: pass2.DS,  // Refined DS
      SP: pass2.SP,  // Refined SP
      M: pass1.M     // Original M
    }, {
      extraConstraints: [
        'Build on refined data and procedures',
        'Maintain alignment with guidance constraints from M'
      ]
    });
    addLog(`Pass 2: X refined in ${((Date.now() - t1_x) / 1000).toFixed(1)}s`);

    // Refine M using all refined documents
    addLog('Pass 2: Refining M with all refined documents...');
    const t1_m = Date.now();
    pass2.M = await runDoc('M', state.problem, { 
      DS: pass2.DS,  // Refined DS
      SP: pass2.SP,  // Refined SP
      X: pass2.X     // Refined X
    }, {
      extraConstraints: [
        'Synthesize guidance from all refined documents',
        'Ensure consistency across the entire document set'
      ]
    });
    addLog(`Pass 2: M refined in ${((Date.now() - t1_m) / 1000).toFixed(1)}s`);

    addLog('Pass 2 complete!');

    // ========== FINAL RESOLUTION: Update X with refined M ==========
    addLog('Final Resolution: Updating X with refined M guidance...');

    const t2_x = Date.now();
    const finalX = await runDoc('X', state.problem, { 
      DS: pass2.DS,  // Refined DS
      SP: pass2.SP,  // Refined SP
      M: pass2.M     // Refined M (the key addition!)
    }, {
      extraConstraints: [
        'Final resolution step: integrate the refined guidance from M',
        'Ensure the solution template fully aligns with the updated guidance',
        'Create the most coherent final solution considering all refined documents'
      ]
    });
    addLog(`Final Resolution: X updated with refined M in ${((Date.now() - t2_x) / 1000).toFixed(1)}s`);

    // Update pass2 with the final X
    pass2.X = finalX;

    // Save the final refined versions with resolution step
    writeState({ 
      finals: pass2,
      metadata: {
        pass1,  // Keep pass 1 for reference
        generatedAt: new Date().toISOString(),
        twoPassMode: true,
        resolutionStep: true
      }
    });

    // Mirror to graph after successful file write (non-blocking)
    mirrorAfterWrite(pass2);

    const totalTime = (
      (Date.now() - t0_ds) / 1000
    ).toFixed(1);

    addLog(`✅ Two-pass generation with final resolution complete in ${totalTime}s`);

    return NextResponse.json({
      success: true,
      orchestrationMode: 'two_pass',
      pass1,
      pass2,
      logs,
      totalTimeSeconds: parseFloat(totalTime)
    });

  } catch (error) {
    console.error('Two-pass orchestration error:', error);
    return NextResponse.json(
      { 
        error: 'Failed to orchestrate documents',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

/**
 * GET endpoint to check current orchestration mode
 */
export async function GET() {
  const mode = process.env.CHIRALITY_ORCHESTRATION_MODE || 'three_pass';
  
  return NextResponse.json({
    currentMode: mode,
    availableModes: ['two_pass', 'three_pass'],
    description: mode === 'three_pass' 
      ? 'Three-pass orchestration with V1→V2→V3 generation'
      : 'Two-pass orchestration with refinement and resolution'
  });
}