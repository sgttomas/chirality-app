import { NextRequest, NextResponse } from 'next/server';
import path from 'path';
import { promises as fs } from 'fs';
import { seedsConfig } from '../../../../config/seeds';
import { extractSeeds, isCacheValid, buildCacheMetadata } from '../../../../../lib/seeds/seedExtractor';
import type { SeedsResult, CachedSeedsMetadata } from '../../../../../lib/seeds/types';
import type { ApiError } from '../../pipeline/traverse/route';

function jsonError(code: string, message: string, status = 400, details?: Record<string, unknown>) {
  return NextResponse.json({ code, message, details } as ApiError, { status });
}

function isDev() {
  return process.env.NODE_ENV !== 'production';
}

function isValidRunId(runId: string) {
  // Production: strict; Dev: allow fixtures like sample_happy_001
  if (isDev()) return /^run_\d+_[a-z0-9]+$/.test(runId) || /^sample_[A-Za-z0-9_]+$/.test(runId);
  return /^run_\d+_[a-z0-9]+$/.test(runId);
}

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    let body: any;
    try {
      body = await request.json();
    } catch {
      return jsonError('ERR_INVALID_JSON', 'Request body must be valid JSON', 400);
    }

    const runId = (body?.runId || '').trim();
    if (!runId) {
      return jsonError('ERR_MISSING_RUN_ID', 'Missing required field: runId', 400);
    }

    if (!isValidRunId(runId)) {
      return jsonError(
        'ERR_INVALID_RUN_ID',
        isDev()
          ? 'Invalid runId. Expected run_{timestamp}_{random} or sample_{name} (dev only).'
          : 'Invalid runId. Expected format: run_{timestamp}_{random}',
        400,
        { runId }
      );
    }

    // Determine runs directory
    const requestedRunsDir: string | undefined = body?.options?.runsDir;
    const runsDir =
      isDev() && requestedRunsDir
        ? requestedRunsDir
        : (process.env.CHIRALITY_RUNS_DIR || seedsConfig.runsDir);

    // Try cache first
    const seedsPath = path.join(runsDir, runId, 'seeds.json');
    let seedsResult: SeedsResult | null = null;

    try {
      const cachedContent = await fs.readFile(seedsPath, 'utf8');
      const cached = JSON.parse(cachedContent);
      if (cached.seeds?.metadata) {
        const valid = await isCacheValid(cached.seeds.metadata as CachedSeedsMetadata, runsDir);
        if (valid) {
          seedsResult = { seeds: cached.seeds };
        }
      }
    } catch {
      // Cache not present or unreadable; proceed to extract
    }

    if (!seedsResult) {
      // Extract fresh seeds
      const options = body?.options || {};
      const result = await extractSeeds({
        runId,
        runsDir,
        enableHeuristics: typeof options.heuristics === 'boolean' ? options.heuristics : seedsConfig.enableHeuristics,
        minItems: typeof options.minItems === 'number' ? options.minItems : seedsConfig.minItems,
        maxItems: typeof options.maxItems === 'number' ? options.maxItems : seedsConfig.maxItems,
        maxLength: typeof options.maxLength === 'number' ? options.maxLength : seedsConfig.maxLength,
        verifyChecksums:
          typeof options.verifyChecksums === 'boolean' ? options.verifyChecksums : seedsConfig.verifyChecksums,
        persist: false
      });

      // Persist cache (best effort)
      if (seedsConfig.persist && result.seeds) {
        try {
          const cacheMeta = await buildCacheMetadata(runId, result.seeds.metadata.sourceFiles, runsDir);
          const toCache = {
            seeds: {
              ...result.seeds,
              metadata: { ...result.seeds.metadata, ...cacheMeta }
            }
          };
          await fs.mkdir(path.dirname(seedsPath), { recursive: true });
          await fs.writeFile(seedsPath, JSON.stringify(toCache, null, 2), 'utf8');
        } catch (e) {
          // Non-blocking: continue without cache
        }
      }

      seedsResult = result;
    }

    // Always respond 200 with SeedsResult ({ seeds: ... | null })
    return NextResponse.json(seedsResult);

  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown error';
    return jsonError('ERR_SEEDS_EXTRACTION_FAILED', 'Failed to extract seeds', 500, { error: message });
  }
}