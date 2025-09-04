import { NextRequest, NextResponse } from 'next/server';
import { runDoc } from '@/chirality-core/orchestrate';
import { readState, writeState } from '@/chirality-core/state/store';
import { DocKind } from '@/chirality-core/contracts';
import { mirrorAfterWrite } from '@/lib/graph/integration';

export const runtime = 'nodejs';

export async function POST(request: NextRequest) {
  try {
    const { kind } = await request.json() as { kind: DocKind };
    if (!kind || !['DS', 'SP', 'X', 'M'].includes(kind)) {
      return NextResponse.json(
        { error: 'kind required (DS|SP|X|M)' },
        { status: 400 }
      );
    }

    const state = readState();
    
    // Check if problem is defined
    if (!state.problem.statement) {
      return NextResponse.json(
        { error: 'Problem statement required' },
        { status: 400 }
      );
    }
    
    const t0 = Date.now();
    const triple = await runDoc(kind, state.problem, state.finals);
    const latencyMs = Date.now() - t0;

    // Pin immediately
    const finals = { ...state.finals, [kind]: triple };
    writeState({ finals });

    // Mirror to graph after successful file write (non-blocking)
    mirrorAfterWrite(finals);
    
    return NextResponse.json({ kind, triple, latencyMs });
  } catch (error) {
    console.error('Run API error:', error);
    return NextResponse.json(
      { 
        error: 'Failed to generate document',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}