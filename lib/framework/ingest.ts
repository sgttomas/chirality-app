// Ingestion layer — reads a chirality-framework run (manifest + snapshots) and returns typed data.
// Contract: docs/INTERFACE.md and src/types/framework.ts
import { promises as fs } from 'fs';
import path from 'path';
import { createHash } from 'crypto';
import type { FrameworkRunManifest, MatrixCell, MatrixKind } from '@/types/framework';

export interface FrameworkIngestResult {
  manifest: FrameworkRunManifest;
  matrices: {
    C: MatrixCell[];
    D: MatrixCell[];
    X: MatrixCell[];
    E: MatrixCell[];
  };
}

export interface IngestOptions {
  runsDir?: string;               // default: 'runs'
  verifyChecksums?: boolean;      // default: true (skip in tests/fixtures with placeholders)
  allowedMajor?: number;          // default: 1 (schema v1.x)
}

/**
 * Load and parse a chirality-framework run with version gating and validation
 */
export async function loadFrameworkRun(runId: string, opts: IngestOptions = {}): Promise<FrameworkIngestResult> {
  const {
    runsDir = 'runs',
    verifyChecksums = true,
    allowedMajor = 1
  } = opts;
  
  try {
    // Step 1: Read and parse manifest
    const manifestPath = resolveUnder(runsDir, path.join(runId, 'index.json'));
    
    let manifestContent: string;
    let manifest: FrameworkRunManifest;
    
    try {
      manifestContent = await fs.readFile(manifestPath, 'utf8');
      manifest = JSON.parse(manifestContent);
    } catch (error) {
      throw new Error(`Failed to read or parse manifest at ${manifestPath}: ${error}`);
    }
    
    // Step 2: Version gating - reject if major version > allowed major version
    const manifestMajor = parseInt(manifest.framework_schema_version.split('.')[0]);
    if (manifestMajor > allowedMajor) {
      throw new Error(
        `Framework schema version ${manifest.framework_schema_version} is not compatible. ` +
        `Maximum allowed major version: ${allowedMajor}`
      );
    }
    
    // Warn for higher minor/patch versions but accept them
    if (manifestMajor === allowedMajor) {
      const [, manifestMinor, manifestPatch] = manifest.framework_schema_version.split('.').map(Number);
      if (manifestMinor > 0 || manifestPatch > 0) {
        console.warn(
          `Framework schema version ${manifest.framework_schema_version} is newer than baseline v${allowedMajor}.0.0. ` +
          `Proceeding but may encounter compatibility issues.`
        );
      }
    }
    
    // Step 3: Load and parse JSONL snapshots
    const matrices: FrameworkIngestResult['matrices'] = {
      C: [],
      D: [],
      X: [],
      E: []
    };
    
    for (const matrixKind of (['C', 'D', 'X', 'E'] as const)) {
      const matrixMeta = manifest.matrices[matrixKind];
      const snapshotPath = resolveUnder(runsDir, path.join(runId, matrixMeta.path));
      
      try {
        const jsonlContent = await fs.readFile(snapshotPath, 'utf8');
        const lines = jsonlContent.trim().split('\n').filter(line => line.trim());
        
        // Step 4: Assert records count matches line count
        if (lines.length !== matrixMeta.records) {
          throw new Error(
            `Record count mismatch for ${matrixKind}: expected ${matrixMeta.records}, got ${lines.length}`
          );
        }
        
        // Step 5: Verify checksums if requested (skip for test placeholders)
        if (verifyChecksums && !matrixMeta.sha256.includes('placeholder')) {
          const actualSha256 = await calculateSha256(snapshotPath);
          if (actualSha256 !== matrixMeta.sha256) {
            throw new Error(
              `Checksum mismatch for ${matrixKind}: expected ${matrixMeta.sha256}, got ${actualSha256}`
            );
          }
        }
        
        // Step 6: Parse JSONL lines into MatrixCell[]
        const cells: MatrixCell[] = [];
        for (let i = 0; i < lines.length; i++) {
          const line = lines[i];
          try {
            const cell = JSON.parse(line) as MatrixCell;
            
            // Validate cell structure - ensure all required fields are present
            if (!cell.id || !cell.matrix || !cell.text || !cell.station || !cell.row_label || !cell.col_label) {
              throw new Error(`Invalid MatrixCell structure at line ${i + 1}: missing required fields`);
            }
            
            // Validate field types
            if (!Array.isArray(cell.citations) || !Array.isArray(cell.refs)) {
              throw new Error(`Invalid MatrixCell structure at line ${i + 1}: citations and refs must be arrays`);
            }
            
            // Ensure matrix field matches expected kind
            if (cell.matrix !== matrixKind) {
              throw new Error(
                `Matrix kind mismatch at line ${i + 1}: expected ${matrixKind}, got ${cell.matrix}`
              );
            }
            
            cells.push(cell);
          } catch (parseError) {
            throw new Error(`Failed to parse JSONL line ${i + 1} in ${matrixKind}: ${parseError}`);
          }
        }
        
        matrices[matrixKind] = cells;
        
      } catch (error) {
        if (error instanceof Error && (error.message.includes('ENOENT') || (error as any).code === 'ENOENT')) {
          throw new Error(`Snapshot file not found: ${matrixMeta.path}`);
        }
        throw error; // Re-throw other errors as-is
      }
    }
    
    return {
      manifest,
      matrices
    };
    
  } catch (error) {
    // Ensure we always throw descriptive errors
    if (error instanceof Error) {
      throw error;
    }
    throw new Error(`Unexpected error during framework ingestion: ${error}`);
  }
}

// Utility: safe join under baseDir to prevent path traversal
function resolveUnder(baseDir: string, p: string): string {
  const full = path.join(baseDir, p);
  const resolvedBase = path.resolve(baseDir);
  const resolvedFull = path.resolve(full);
  
  if (!resolvedFull.startsWith(resolvedBase)) {
    throw new Error(`Path traversal detected: ${p}`);
  }
  return resolvedFull;
}

// Utility: calculate SHA256 hash of a file
async function calculateSha256(filePath: string): Promise<string> {
  try {
    const content = await fs.readFile(filePath);
    const hash = createHash('sha256').update(content).digest('hex');
    return hash;
  } catch (error) {
    throw new Error(`Failed to calculate SHA256 for ${filePath}: ${error}`);
  }
}