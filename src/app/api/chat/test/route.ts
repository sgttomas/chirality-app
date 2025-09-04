import { NextRequest, NextResponse } from 'next/server'
import { readState } from '@/chirality-core/state/store'
import { compactDS, compactSP, compactX, compactM } from '@/chirality-core/compactor'

export const runtime = 'nodejs';

export async function POST(request: NextRequest) {
  try {
    const { testMessage = "Based on the pinned documents, what are the key considerations?" } = await request.json().catch(() => ({}))
    
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

    // Simulate the OpenAI API call payload (without actually calling)
    const openaiBody = {
      model: process.env.OPENAI_MODEL || 'gpt-4.1-nano',
      instructions: instructions.join('\n'),
      input: [
        {
          role: 'user',
          content: [{ type: 'input_text', text: testMessage }]
        }
      ],
      temperature: parseFloat(process.env.DEFAULT_TEMPERATURE || '0.6'),
      max_output_tokens: parseInt(process.env.MAX_OUTPUT_TOKENS || '800'),
      stream: true
    }

    // Count occurrences of each document type in instructions
    const instructionsText = instructions.join('\n')
    const documentMentions = {
      DS: (instructionsText.match(/DS:/g) || []).length,
      SP: (instructionsText.match(/SP:/g) || []).length,
      X: (instructionsText.match(/X:/g) || []).length,
      M: (instructionsText.match(/M:/g) || []).length
    }

    // Extract document content lengths
    const documentContentLengths = {
      DS: DS ? compactDS(DS.text).length : 0,
      SP: SP ? compactSP(SP.text).length : 0,
      X: X ? compactX(X.text).length : 0,
      M: M ? compactM(M.text).length : 0
    }

    return NextResponse.json({
      timestamp: new Date().toISOString(),
      testMessage,
      documentsDetected: {
        DS: !!DS,
        SP: !!SP,
        X: !!X,
        M: !!M,
        totalFound: [!!DS, !!SP, !!X, !!M].filter(Boolean).length
      },
      instructionsAnalysis: {
        totalLength: instructionsText.length,
        documentMentions,
        documentContentLengths,
        totalDocumentContent: Object.values(documentContentLengths).reduce((a, b) => a + b, 0)
      },
      openaiPayload: {
        model: openaiBody.model,
        instructionsLength: openaiBody.instructions.length,
        temperature: openaiBody.temperature,
        maxTokens: openaiBody.max_output_tokens,
        inputMessage: testMessage
      },
      validation: {
        hasDocuments: !!(DS || SP || X || M),
        instructionsContainDocuments: instructionsText.includes('--- Pinned Finals (compact) ---'),
        allDocumentsInjected: [!!DS, !!SP, !!X, !!M].filter(Boolean).length === 4,
        estimatedTokens: Math.ceil(instructionsText.length / 4) // Rough estimate
      }
    })

  } catch (error) {
    return NextResponse.json({
      error: 'Failed to test chat configuration',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}