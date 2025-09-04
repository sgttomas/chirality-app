import { NextRequest, NextResponse } from 'next/server'
import { readState } from '@/chirality-core/state/store'
import { compactDS, compactSP, compactX, compactM } from '@/chirality-core/compactor'

export const runtime = 'nodejs';

export async function GET() {
  try {
    // Get current state (same as chat stream does)
    const state = readState()
    const { DS, SP, X, M } = state.finals ?? {}
    
    // Build instructions exactly as chat stream does
    const instructions = [
      'You are the Chirality Chat engine.',
      'Use pinned DS/SP/X/M as ground truth context for this session.',
      'Prefer cited evidence; include citation IDs when relevant.',
      'Be conversational but precise. Draw insights from the documents when answering.',
      ''
    ]

    if (DS || SP || X || M) {
      instructions.push('--- Pinned Finals (compact) ---')
      if (DS) instructions.push(`DS: ${compactDS(DS.text)}`)
      if (SP) instructions.push(`SP: ${compactSP(SP.text)}`)
      if (X) instructions.push(`X: ${compactX(X.text)}`)
      if (M) instructions.push(`M: ${compactM(M.text)}`)
      instructions.push('--- End Pinned ---')
      instructions.push('')
    } else {
      instructions.push('No documents pinned yet. Guide users to generate documents first using commands like "set problem: [description]" then "generate DS".')
      instructions.push('')
    }

    instructions.push('Available commands: "set problem: [description]", "generate DS", "generate SP", "generate X", "generate M"')

    // Return debug info
    return NextResponse.json({
      timestamp: new Date().toISOString(),
      state: {
        problem: state.problem,
        documentsFound: {
          DS: !!DS,
          SP: !!SP,
          X: !!X,
          M: !!M
        }
      },
      fullInstructions: instructions.join('\n'),
      instructionsLength: instructions.join('\n').length,
      compactedDocuments: {
        DS: DS ? compactDS(DS.text) : null,
        SP: SP ? compactSP(SP.text) : null,
        X: X ? compactX(X.text) : null,
        M: M ? compactM(M.text) : null
      },
      rawDocuments: {
        DS: DS?.text || null,
        SP: SP?.text || null,
        X: X?.text || null,
        M: M?.text || null
      }
    }, {
      status: 200,
      headers: {
        'Content-Type': 'application/json'
      }
    })

  } catch (error) {
    return NextResponse.json({
      error: 'Failed to read chat state',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}