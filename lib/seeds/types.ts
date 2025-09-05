/**
 * Types for seed extraction functionality
 */

export interface SeedOptions {
  runId: string;
  enableHeuristics?: boolean;  // Apply trimming, deduplication, etc.
  minItems?: number;           // Minimum items per matrix
  maxItems?: number;           // Maximum items per matrix
  maxLength?: number;          // Maximum length per item
  verifyChecksums?: boolean;   // Verify file checksums
  persist?: boolean;           // Persist results to seeds.json
  runsDir?: string;           // Base runs directory
}

export interface SeedsResult {
  seeds: {
    initialVector: {
      matrixC: string[];
      matrixD: string[];
      matrixX: string[];
      matrixE: string[];
    };
    metadata: {
      runId: string;
      extractedAt: string;
      // post-heuristics totals
      totalCells: number;
      counts: {
        C: number;
        D: number;
        X: number;
        E: number;
      };
      // transparency: pre/post heuristic counts
      preHeuristicsCounts?: { C: number; D: number; X: number; E: number };
      postHeuristicsCounts?: { C: number; D: number; X: number; E: number };
      preHeuristicsTotal?: number;
      postHeuristicsTotal?: number;
      sourceFiles: string[];
      checksumVerified: boolean;
      checksums?: { C: string; D: string; X: string; E: string };
      warnings: string[];
      // cache validation data (added when persisted)
      sourceMtime?: Record<string, number>;
      sourceSize?: Record<string, number>;
    };
  } | null;
}

export interface CachedSeedsMetadata {
  runId: string;
  extractedAt: string;
  totalCells: number;
  counts: {
    C: number;
    D: number;
    X: number;
    E: number;
  };
  sourceFiles: string[];
  checksumVerified: boolean;
  warnings: string[];
  // Cache validation fields
  sourceMtime: Record<string, number>; // filename -> mtime
  sourceSize: Record<string, number>;  // filename -> size
}
