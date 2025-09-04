import { NextRequest, NextResponse } from 'next/server';
import { reindexRAG, readState } from '@/chirality-core/state/store';

export const runtime = 'nodejs';

/**
 * POST /api/core/rag/reindex
 * Manually trigger RAG reindexing with corpus management
 */
export async function POST(request: NextRequest) {
  try {
    const state = readState();
    
    // Check if there are any documents to index
    if (!state.finals || Object.keys(state.finals).length === 0) {
      return NextResponse.json(
        { 
          success: false,
          message: 'No documents available for indexing',
          documentCount: 0
        },
        { status: 200 }
      );
    }
    
    // Trigger reindexing
    await reindexRAG();
    
    return NextResponse.json({
      success: true,
      message: 'RAG reindexing completed successfully',
      documentCount: Object.keys(state.finals).length,
      documents: Object.keys(state.finals),
      problem: state.problem.title || 'Untitled',
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('RAG reindex API error:', error);
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to reindex RAG corpus',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

/**
 * GET /api/core/rag/reindex
 * Check RAG index status and configuration
 */
export async function GET(request: NextRequest) {
  try {
    const state = readState();
    const fs = await import('fs');
    const path = await import('path');
    
    const storeDir = process.env.CHIRALITY_STORE_DIR || './store';
    const ragIndexPath = path.join(storeDir, 'rag-index');
    
    // Check if RAG index exists
    const indexExists = fs.existsSync(ragIndexPath);
    let indexMetadata = null;
    let indexedDocuments: string[] = [];
    
    if (indexExists) {
      const metaPath = path.join(ragIndexPath, 'index-meta.json');
      if (fs.existsSync(metaPath)) {
        indexMetadata = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
      }
      
      // List indexed documents
      indexedDocuments = fs.readdirSync(ragIndexPath)
        .filter(f => f.endsWith('.json') && f !== 'index-meta.json')
        .map(f => f.replace('.json', ''));
    }
    
    return NextResponse.json({
      indexExists,
      indexMetadata,
      indexedDocuments,
      configuration: {
        maxCorpusDocs: process.env.MAX_CORPUS_DOCS || '100',
        maxCorpusSizeMB: process.env.MAX_CORPUS_SIZE_MB || '50',
        storeDirectory: storeDir
      },
      currentState: {
        problemTitle: state.problem.title || 'Untitled',
        documentCount: Object.keys(state.finals || {}).length,
        documents: Object.keys(state.finals || {})
      }
    });
    
  } catch (error) {
    console.error('RAG index status error:', error);
    return NextResponse.json(
      {
        error: 'Failed to get RAG index status',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
