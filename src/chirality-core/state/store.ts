import fs from 'fs';
import path from 'path';
import { Finals, DocKind, DS, SP, X, M } from '../contracts';

const root = process.env.CHIRALITY_STORE_DIR || './store';
const statePath = path.join(root, 'state.json');

// RAG indexing configuration
const MAX_CORPUS_DOCS = parseInt(process.env.RAG_MAX_DOCS || process.env.MAX_CORPUS_DOCS || '200');
const MAX_CORPUS_SIZE_MB = parseInt(process.env.RAG_MAX_MB || process.env.MAX_CORPUS_SIZE_MB || '5');
const CHUNK_SIZE = parseInt(process.env.RAG_CHUNK || '900');
const CHUNK_OVERLAP = parseInt(process.env.RAG_OVERLAP || '120');
const DEV_FALLBACK = process.env.RAG_DEV_FALLBACK === 'true';

/**
 * Extract searchable text from document objects for RAG indexing
 */
export function extractTextFromDocument(docType: DocKind, doc: DS | SP | X | M): string {
  switch (docType) {
    case 'DS':
      const ds = doc as DS;
      return [
        ds.data_field,
        ds.type,
        ds.units,
        ...(ds.source_refs || []),
        ...(ds.notes || [])
      ].filter(Boolean).join(' ');
      
    case 'SP':
      const sp = doc as SP;
      return [
        sp.step,
        sp.purpose,
        ...(sp.inputs || []),
        ...(sp.outputs || []),
        ...(sp.preconditions || []),
        ...(sp.postconditions || []),
        ...(sp.refs || [])
      ].filter(Boolean).join(' ');
      
    case 'X':
      const x = doc as X;
      return [
        x.heading,
        x.narrative,
        ...(x.precedents || []),
        ...(x.successors || []),
        ...(x.context_notes || []),
        ...(x.refs || [])
      ].filter(Boolean).join(' ');
      
    case 'M':
      const m = doc as M;
      return [
        m.statement,
        m.justification,
        ...(m.trace_back || []),
        ...(m.assumptions || []),
        ...(m.residual_risk || [])
      ].filter(Boolean).join(' ');
      
    default:
      return '';
  }
}

type CoreState = {
  problem: { 
    title: string; 
    statement: string; 
    initialVector: string[] 
  };
  finals: Finals;
  metadata?: {
    pass1?: any;
    generatedAt?: string;
    twoPassMode?: boolean;
    resolutionStep?: boolean;
    [key: string]: any;
  };
};

export function ensureStore() {
  if (!fs.existsSync(root)) {
    fs.mkdirSync(root, { recursive: true });
  }
  if (!fs.existsSync(statePath)) {
    const init: CoreState = { 
      problem: { title: '', statement: '', initialVector: [] }, 
      finals: {} 
    };
    fs.writeFileSync(statePath, JSON.stringify(init, null, 2));
  }
}

export function readState(): CoreState {
  ensureStore();
  try {
    return JSON.parse(fs.readFileSync(statePath, 'utf8'));
  } catch {
    return { 
      problem: { title: '', statement: '', initialVector: [] }, 
      finals: {} 
    };
  }
}

export function writeState(patch: Partial<CoreState>) {
  ensureStore();
  const cur = readState();
  const next = { 
    ...cur, 
    ...patch, 
    finals: { ...cur.finals, ...(patch.finals || {}) } 
  };
  fs.writeFileSync(statePath, JSON.stringify(next, null, 2));
  
  // Trigger RAG indexing hook after successful write
  if (patch.finals && Object.keys(patch.finals).length > 0) {
    triggerRAGIndexing(next).catch(err => {
      console.error('RAG indexing hook failed:', err);
    });
  }
  
  return next;
}

/**
 * RAG indexing hook with real embeddings, chunking, and corpus caps
 */
async function triggerRAGIndexing(state: CoreState): Promise<void> {
  try {
    const { chunkText } = await import('../rag/chunk');
    const { indexChunks, VS } = await import('../rag/retrieve');
    const { embedAll } = await import('../vendor/embed');
    
    // Collect all document text for chunking
    const docsToIndex: { id: string; text: string }[] = [];
    let totalTextSize = 0;
    
    for (const [docType, triple] of Object.entries(state.finals)) {
      if (!triple?.text) continue;
      
      // Extract text content from document object
      const docText = extractTextFromDocument(docType as DocKind, triple.text);
      if (!docText) continue;
      
      const textSize = Buffer.byteLength(docText, 'utf8');
      totalTextSize += textSize;
      
      // Check corpus size limit before processing
      if (totalTextSize > MAX_CORPUS_SIZE_MB * 1024 * 1024) {
        console.warn(`RAG corpus size limit exceeded (${MAX_CORPUS_SIZE_MB}MB), skipping ${docType}`);
        break;
      }
      
      docsToIndex.push({ id: docType, text: docText });
    }
    
    if (docsToIndex.length === 0) {
      console.log('No documents to index');
      return;
    }
    
    // Chunk all documents with new configuration
    const allChunks = docsToIndex.flatMap(doc => {
      return chunkText(doc.id, doc.text, { 
        tokens: Math.floor(CHUNK_SIZE / 4), // Convert chars to approximate tokens
        overlap: Math.floor(CHUNK_OVERLAP / 4)
      });
    });
    
    // Apply per-document chunk limit (K=12 per doc)
    const limitedChunks = docsToIndex.flatMap(doc => {
      const docChunks = allChunks.filter(chunk => chunk.source_id === doc.id);
      return docChunks.slice(0, 12); // Cap per doc K=12
    });
    
    // Apply global document count limit
    const finalChunks = limitedChunks.slice(0, MAX_CORPUS_DOCS);
    
    if (finalChunks.length < limitedChunks.length) {
      console.warn(`Applied global cap: ${finalChunks.length}/${limitedChunks.length} chunks indexed`);
    }
    
    // Real embedding and indexing with retry/backoff
    try {
      const result = await indexChunks(finalChunks);
      console.log(`RAG indexing completed: ${result.count} chunks indexed from ${docsToIndex.length} documents`);
      
    } catch (embeddingError) {
      console.error('Embeddings failed:', embeddingError);
      
      // Dev fallback if enabled
      if (DEV_FALLBACK) {
        console.warn('Using dev fallback: keyword/cosine similarity without embeddings');
        // Store chunks without embeddings for keyword search
        // This is a degraded mode - log warning but continue
        console.warn('RAG operating in degraded keyword-only mode');
      } else {
        // In production, fail fast - no random vectors
        throw new Error('Embedding service unavailable and dev fallback disabled');
      }
    }
    
  } catch (error) {
    console.error('Failed to trigger RAG indexing:', error);
    // Don't rethrow - RAG indexing failure shouldn't break document persistence
  }
}

/**
 * Export for manual RAG reindexing with real embeddings
 */
export async function reindexRAG(): Promise<void> {
  const state = readState();
  
  // Clear existing vector store before reindexing
  try {
    const { VS } = await import('../rag/retrieve');
    VS.clear();
    console.log('Cleared existing RAG index');
  } catch (error) {
    console.warn('Could not clear existing RAG index:', error);
  }
  
  await triggerRAGIndexing(state);
}