/**
 * Seed extraction logic for framework runs
 * 
 * Extracts text content from matrix cells to create initialVector seeds
 * for use in semantic valley traversal prompts
 */

import { SeedOptions, SeedsResult, CachedSeedsMetadata } from './types';
import { seedsConfig } from '../../src/config/seeds';
import { loadFrameworkRun } from '../framework/ingest';
import { promises as fs } from 'fs';
import path from 'path';

/**
 * Apply heuristics to clean and filter seed text items
 */
function applyHeuristics(items: string[], options: SeedOptions, warnings: string[], matrixKind: string): string[] {
  if (!options.enableHeuristics) return items;

  const maxLen = options.maxLength ?? seedsConfig.maxLength;
  const minItems = options.minItems ?? seedsConfig.minItems;
  const maxItems = options.maxItems ?? seedsConfig.maxItems;

  const stripLeading = (s: string) => s.replace(/^[\s\-•*◦\u{1F300}-\u{1FAFF}]+/u, '');
  const firstSentence = (s: string) => {
    const m = s.match(/^[^\.?!;\n]+[\.?!]?/);
    return m ? m[0] : s;
  };

  let processed = items
    .map(s => s.trim())
    .map(stripLeading)
    .map(firstSentence)
    .map(s => s.replace(/\s+/g, ' ').trim())
    .filter(Boolean)
    .map(s => (s.length > maxLen ? s.substring(0, maxLen) + '...' : s));

  // case-insensitive dedupe, keep first
  const seenCI = new Set<string>();
  processed = processed.filter(s => {
    const key = s.toLowerCase();
    if (seenCI.has(key)) return false;
    seenCI.add(key);
    return true;
  });

  if (processed.length > maxItems) {
    processed = processed.slice(0, maxItems);
  }
  if (processed.length < minItems) {
    warnings.push(`Matrix ${matrixKind}: only ${processed.length} items after heuristics (min ${minItems}).`);
  }

  return processed;
}

/**
 * Extract seeds from a framework run
 * 
 * This function:
 * 1. Uses unified loadFrameworkRun (safe mode) to fetch matrix cells with graceful error handling
 * 2. Normalizes cells using existing normalizeMatrixCells utility
 * 3. Applies optional heuristics for text processing
 * 4. Collates all warnings and issues
 */
export async function extractSeeds(options: SeedOptions): Promise<SeedsResult> {
  const warnings: string[] = [];
  const runId = options.runId;
  
  // Log operation with runId context
  console.log(`[Seeds] Extracting seeds for run: ${runId}`);

  try {
    // Step 1: Load framework run with production-aware mode
    const isProd = process.env.NODE_ENV === 'production';
    const ingestResult = await loadFrameworkRun(runId, {
      runsDir: options.runsDir || seedsConfig.runsDir,
      mode: isProd ? 'strict' : 'safe',
      checksum: isProd ? 'fail' : 'warn',
      // Production: strict mode + fail on checksum mismatch (hard fail)
      // Development: safe mode + warn on checksum mismatch (continue with warnings)
    });
    
    // Collect warnings from ingestion
    if (ingestResult.warnings) {
      warnings.push(...ingestResult.warnings);
    }

    // Step 2: Extract text from each matrix using normalized cells
    const initialVector = {
      matrixC: [] as string[],
      matrixD: [] as string[],
      matrixX: [] as string[],
      matrixE: [] as string[],
    };

    let postTotal = 0;
    const postCounts = { C: 0, D: 0, X: 0, E: 0 };
    let preTotal = 0;
    const preCounts = { C: 0, D: 0, X: 0, E: 0 };
    const sourceFiles: string[] = [];

    // Process each matrix
    for (const [matrixKind, cells] of Object.entries(ingestResult.matrices)) {
      const matrixKey = matrixKind as keyof typeof initialVector;
      const vectorKey = `matrix${matrixKey}` as keyof typeof initialVector;
      
      if (cells.length === 0) {
        warnings.push(`Matrix '${matrixKind}' has no cells`);
        continue;
      }

      // Extract text content from cells (cells are already normalized and ordered)
      const textItems = cells.map(cell => cell.text);
      preCounts[matrixKey as keyof typeof preCounts] = textItems.length;
      preTotal += textItems.length;

      // Apply heuristics if enabled
      const processedItems = applyHeuristics(textItems, options, warnings, matrixKind);
      
      initialVector[vectorKey] = processedItems;
      postCounts[matrixKey as keyof typeof postCounts] = processedItems.length;
      postTotal += processedItems.length;

      // Track source file path
      const matrixMeta = ingestResult.manifest.matrices[matrixKind as keyof typeof ingestResult.manifest.matrices];
      sourceFiles.push(matrixMeta.path);

      console.log(`[Seeds] ${matrixKind}: ${cells.length} cells -> ${processedItems.length} seeds`);
    }

    // Step 3: Build result metadata
    // Build checksum aggregate status
    const checksums = ingestResult.checksumStatus || { C: 'unknown', D: 'unknown', X: 'unknown', E: 'unknown' };
    const checksumVerified = Object.values(checksums).every(s => s === 'ok');

    const metadata = {
      runId,
      extractedAt: new Date().toISOString(),
      totalCells: postTotal,
      counts: postCounts,
      preHeuristicsCounts: preCounts,
      postHeuristicsCounts: postCounts,
      preHeuristicsTotal: preTotal,
      postHeuristicsTotal: postTotal,
      sourceFiles,
      checksumVerified,
      checksums,
      warnings,
    };

    // Log warnings to server logs with runId context
    if (warnings.length > 0) {
      console.warn(`[Seeds] ${runId} extraction completed with warnings:`);
      warnings.forEach(warning => console.warn(`  - ${warning}`));
    } else {
      console.log(`[Seeds] ${runId} extraction completed successfully`);
    }

    return {
      seeds: {
        initialVector,
        metadata,
      }
    };

  } catch (error) {
    // For hard failures, collect the error as a warning and return null seeds
    const errorMessage = error instanceof Error ? error.message : String(error);
    warnings.push(`Fatal error during extraction: ${errorMessage}`);
    
    console.error(`[Seeds] ${runId} extraction failed:`, error);

    return {
      seeds: null
    };
  }
}

/**
 * Check cache validity by comparing source file modification times and sizes
 */
export async function isCacheValid(cachedMetadata: CachedSeedsMetadata, runsDir: string): Promise<boolean> {
  try {
    const runPath = path.join(runsDir, cachedMetadata.runId);
    
    // Check each source file's mtime and size
    for (const sourceFile of cachedMetadata.sourceFiles) {
      const filePath = path.join(runPath, sourceFile);
      
      try {
        const stats = await fs.stat(filePath);
        const currentMtime = Math.floor(stats.mtime.getTime() / 1000); // Convert to seconds
        const currentSize = stats.size;
        
        const cachedMtime = cachedMetadata.sourceMtime[sourceFile];
        const cachedSize = cachedMetadata.sourceSize[sourceFile];
        
        if (currentMtime !== cachedMtime || currentSize !== cachedSize) {
          console.log(`[Seeds] Cache invalidated: ${sourceFile} changed (mtime: ${cachedMtime}->${currentMtime}, size: ${cachedSize}->${currentSize})`);
          return false;
        }
      } catch (error) {
        // File doesn't exist or can't be accessed
        console.log(`[Seeds] Cache invalidated: ${sourceFile} not accessible`);
        return false;
      }
    }
    
    return true;
  } catch (error) {
    console.warn(`[Seeds] Cache validation failed:`, error);
    return false;
  }
}

/**
 * Build cache metadata for source files
 */
export async function buildCacheMetadata(runId: string, sourceFiles: string[], runsDir: string): Promise<{ sourceMtime: Record<string, number>; sourceSize: Record<string, number> }> {
  const sourceMtime: Record<string, number> = {};
  const sourceSize: Record<string, number> = {};
  const runPath = path.join(runsDir, runId);
  
  for (const sourceFile of sourceFiles) {
    try {
      const filePath = path.join(runPath, sourceFile);
      const stats = await fs.stat(filePath);
      sourceMtime[sourceFile] = Math.floor(stats.mtime.getTime() / 1000);
      sourceSize[sourceFile] = stats.size;
    } catch (error) {
      // If we can't stat the file, record -1 as a sentinel value
      sourceMtime[sourceFile] = -1;
      sourceSize[sourceFile] = -1;
    }
  }
  
  return { sourceMtime, sourceSize };
}
