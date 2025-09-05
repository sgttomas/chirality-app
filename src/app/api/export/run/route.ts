import { NextRequest, NextResponse } from 'next/server';
import { Exporter } from '../../../../core/exporter';
import { ApiError } from '../../pipeline/traverse/route';
import { extractSeeds, isCacheValid, buildCacheMetadata } from '../../../../../lib/seeds/seedExtractor';
import type { SeedsResult, CachedSeedsMetadata } from '../../../../../lib/seeds/types';
import { seedsConfig } from '../../../../config/seeds';
import { promises as fs } from 'fs';
import path from 'path';

export interface ExportRunResponse {
  runId: string;
  files: {
    runJson: string;
    packetsJsonl: string;
  };
  size: {
    runJson: number;
    packetsJsonl: number;
    total: number;
  };
  seeds: SeedsResult['seeds'] | null;
}

export async function GET(request: NextRequest): Promise<NextResponse> {
  try {
    // Extract parameters from query
    const { searchParams } = new URL(request.url);
    const runId = searchParams.get('runId');
    const include = searchParams.get('include');

    if (!runId) {
      return NextResponse.json(
        {
          code: 'ERR_MISSING_RUN_ID',
          message: 'Missing required query parameter: runId'
        } as ApiError,
        { status: 400 }
      );
    }

    // Validate runId format (basic validation)
    if (!/^run_\d+_[a-z0-9]+$/.test(runId)) {
      return NextResponse.json(
        {
          code: 'ERR_INVALID_RUN_ID',
          message: 'Invalid runId format. Expected format: run_{timestamp}_{random}',
          details: { runId }
        } as ApiError,
        { status: 400 }
      );
    }

    // Use the exporter to check if run exists and get file information
    const exporter = new Exporter();
    
    try {
      // Check if the run exists
      const runExists = await exporter.runExists(runId);
      
      if (!runExists) {
        return NextResponse.json(
          {
            code: 'ERR_RUN_NOT_FOUND',
            message: `Run ${runId} not found. Files may not have been exported yet.`,
            details: { 
              runId,
              expectedFiles: [
                `runs/${runId}/run.json`,
                `runs/${runId}/packets.jsonl`
              ]
            }
          } as ApiError,
          { status: 404 }
        );
      }

      // Get file sizes
      const sizes = await exporter.getRunSize(runId);
      
      const response: ExportRunResponse = {
        runId,
        files: {
          runJson: `runs/${runId}/run.json`,
          packetsJsonl: `runs/${runId}/packets.jsonl`
        },
        size: sizes,
        seeds: null
      };

      // Handle include=seeds parameter
      if (include === 'seeds') {
        try {
          // Check for cached seeds.json
          const seedsPath = path.join(seedsConfig.runsDir, runId, 'seeds.json');
          let seedsResult: SeedsResult | null = null;
          
          try {
            // Try to load cached seeds
            const cachedContent = await fs.readFile(seedsPath, 'utf8');
            const cached = JSON.parse(cachedContent);
            
            // Validate cache freshness
            if (cached.seeds?.metadata && await isCacheValid(cached.seeds.metadata as CachedSeedsMetadata, seedsConfig.runsDir)) {
              console.log(`[Seeds API] Using cached seeds for ${runId}`);
              seedsResult = { seeds: cached.seeds };
            } else {
              console.log(`[Seeds API] Cache invalid for ${runId}, re-extracting`);
            }
          } catch (error) {
            // Cache doesn't exist or is invalid
            console.log(`[Seeds API] No valid cache for ${runId}, extracting fresh`);
          }
          
          // Extract fresh seeds if no valid cache
          if (!seedsResult) {
            seedsResult = await extractSeeds({
              runId,
              enableHeuristics: seedsConfig.enableHeuristics,
              minItems: seedsConfig.minItems,
              maxItems: seedsConfig.maxItems,
              maxLength: seedsConfig.maxLength,
              verifyChecksums: seedsConfig.verifyChecksums,
              persist: false, // We'll handle persistence here
              runsDir: seedsConfig.runsDir
            });
            
            // Persist if configured and extraction succeeded
            if (seedsConfig.persist && seedsResult.seeds) {
              try {
                // Build cache metadata
                const cacheMetadata = await buildCacheMetadata(
                  runId, 
                  seedsResult.seeds.metadata.sourceFiles,
                  seedsConfig.runsDir
                );
                
                // Combine seeds with cache metadata
                const toCache = {
                  seeds: {
                    ...seedsResult.seeds,
                    metadata: {
                      ...seedsResult.seeds.metadata,
                      ...cacheMetadata
                    }
                  }
                };
                
                // Write to seeds.json (best effort)
                await fs.writeFile(seedsPath, JSON.stringify(toCache, null, 2), 'utf8');
                console.log(`[Seeds API] Persisted seeds to ${seedsPath}`);
              } catch (persistError) {
                // Add warning but continue
                if (seedsResult.seeds) {
                  seedsResult.seeds.metadata.warnings.push(
                    `Failed to persist seeds cache: ${persistError instanceof Error ? persistError.message : 'Unknown error'}`
                  );
                }
                console.warn(`[Seeds API] Failed to persist seeds for ${runId}:`, persistError);
              }
            }
          }
          
          // Add seeds to response
          response.seeds = seedsResult.seeds || null;
          
        } catch (seedError) {
          // For soft failures, return 200 with null seeds and populate warnings
          console.error(`[Seeds API] Failed to extract seeds for ${runId}:`, seedError);
          response.seeds = null;
        }
      }

      return NextResponse.json(response);

    } catch (error) {
      console.error('Export endpoint error:', error);
      return NextResponse.json(
        {
          code: 'ERR_EXPORT_FAILED',
          message: 'Failed to retrieve run export information',
          details: { 
            runId,
            error: error instanceof Error ? error.message : 'Unknown error'
          }
        } as ApiError,
        { status: 500 }
      );
    }

  } catch (error) {
    console.error('Unexpected error in export endpoint:', error);
    return NextResponse.json(
      {
        code: 'ERR_INTERNAL',
        message: 'Internal server error',
        details: { error: error instanceof Error ? error.message : 'Unknown error' }
      } as ApiError,
      { status: 500 }
    );
  }
}
