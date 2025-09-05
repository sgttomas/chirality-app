// Ingestion layer — reads a chirality-framework run (manifest + snapshots) and returns typed data.
// Contract: docs/INTERFACE.md and src/types/framework.ts
import { promises as fs } from 'fs';
import { createReadStream } from 'fs';
import * as readline from 'readline';
import path from 'path';
import { createHash } from 'crypto';
import type { FrameworkRunManifest } from '@/types/framework';
import { MatrixCell, MatrixCellRaw } from './types';
import { normalizeMatrixCells, validateRawCell } from './normalizeMatrix';
import { validateRunId } from '../utils/validation';

export interface FrameworkIngestResult {
  manifest: FrameworkRunManifest;
  matrices: {
    C: MatrixCell[];
    D: MatrixCell[];
    X: MatrixCell[];
    E: MatrixCell[];
  };
  warnings?: string[];
  checksumStatus?: { C: string; D: string; X: string; E: string };
}

export interface IngestOptions {
  runsDir?: string;               // default: 'runs'
  allowedMajor?: number;          // default: 1 (schema v1.x)
  mode?: 'strict' | 'safe';       // unified behavior control (default: strict)
  checksum?: 'warn' | 'skip' | 'fail'; // default: env-aware (prod=fail, else warn)
}

/**
 * Parse JSONL file using streaming approach to handle large files efficiently
 */
async function parseJsonlStream(
  filePath: string,
  expectedRecords: number,
  matrixKind: string,
  opts: { mode?: 'strict'|'safe' } = {}
): Promise<MatrixCellRaw[]> {
  const mode = opts.mode || 'strict';
  const rawCells: MatrixCellRaw[] = [];
  
  const fileStream = createReadStream(filePath);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });

  let lineNumber = 0;

  for await (const line of rl) {
    const trimmedLine = line.trim();
    if (!trimmedLine) continue;
    
    lineNumber++;
    
    try {
      const rawCell = JSON.parse(trimmedLine);
      
      // Validate raw cell structure
      validateRawCell(rawCell, lineNumber);
      
      // Ensure matrix field matches expected kind
      if (rawCell.matrix !== matrixKind) {
        throw new Error(
          `Matrix kind mismatch at line ${lineNumber}: expected ${matrixKind}, got ${rawCell.matrix}`
        );
      }
      
      rawCells.push(rawCell as MatrixCellRaw);
    } catch (parseError) {
      if (mode === 'strict') {
        throw new Error(`Failed to parse JSONL line ${lineNumber} in ${matrixKind}: ${parseError}`);
      }
      // safe mode: skip malformed line
      continue;
    }
  }

  // Verify record count matches expected
  if (rawCells.length !== expectedRecords) {
    const msg = `Record count mismatch for ${matrixKind}: expected ${expectedRecords}, got ${rawCells.length}`;
    if (mode === 'strict') {
      throw new Error(msg);
    }
    console.warn(`[Framework] ${msg}`);
  }

  return rawCells;
}

// Removed loadFrameworkRunSafe in favor of unified loadFrameworkRun

/**
 * Load and parse a chirality-framework run with version gating and validation
 */
export async function loadFrameworkRun(runId: string, opts: IngestOptions = {}): Promise<FrameworkIngestResult> {
  const {
    runsDir = 'runs',
    allowedMajor = 1,
    mode = 'strict',
    checksum = (process.env.NODE_ENV === 'production' ? 'fail' : 'warn'),
  } = opts;

  const warnings: string[] = [];
  const checksumStatus: { [k in 'C'|'D'|'X'|'E']: string } = { C: 'unknown', D: 'unknown', X: 'unknown', E: 'unknown' };

  // Validate run id
  const runIdValidation = validateRunId(runId);
  if (!runIdValidation.valid) {
    throw new Error(`Invalid run_id: ${runIdValidation.error}`);
  }

  // Read manifest (hard fail if missing/corrupt)
  const manifestPath = resolveUnder(runsDir, path.join(runId, 'index.json'));
  let manifest: FrameworkRunManifest;
  try {
    const content = await fs.readFile(manifestPath, 'utf8');
    manifest = JSON.parse(content);
  } catch (e) {
    throw new Error(`Failed to read or parse manifest at ${manifestPath}: ${e}`);
  }

  // Version gating
  const manifestMajor = parseInt(manifest.framework_schema_version.split('.')[0]);
  if (manifestMajor > allowedMajor) {
    throw new Error(`Framework schema version ${manifest.framework_schema_version} is not compatible. Maximum allowed major version: ${allowedMajor}`);
  }
  if (manifestMajor === allowedMajor) {
    const [, minor, patch] = manifest.framework_schema_version.split('.').map(Number);
    if ((minor ?? 0) > 0 || (patch ?? 0) > 0) {
      console.warn(`Framework schema version ${manifest.framework_schema_version} is newer than baseline v${allowedMajor}.0.0. Proceeding but may encounter compatibility issues.`);
    }
  }

  const matrices: FrameworkIngestResult['matrices'] = { C: [], D: [], X: [], E: [] };

  for (const mk of (['C','D','X','E'] as const)) {
    const matrixMeta = manifest.matrices[mk];
    if (!matrixMeta) {
      warnings.push(`Matrix '${mk}' metadata missing in manifest`);
      checksumStatus[mk] = 'skipped';
      continue;
    }
    if (matrixMeta.format && matrixMeta.format !== 'cells-jsonl-v1') {
      warnings.push(`Matrix '${mk}' has unsupported format '${matrixMeta.format}', expected 'cells-jsonl-v1'. Skipping.`);
      checksumStatus[mk] = 'skipped';
      continue;
    }

    const snapshotPath = resolveUnder(runsDir, path.join(runId, matrixMeta.path));
    // Checksum verification
    try {
      const actual = await calculateSha256(snapshotPath);
      if (matrixMeta.sha256 && !matrixMeta.sha256.includes('placeholder')) {
        if (actual !== matrixMeta.sha256) {
          const msg = `Checksum mismatch for ${mk}: expected ${matrixMeta.sha256}, got ${actual}`;
          if (checksum === 'fail' && mode === 'strict') {
            throw new Error(msg);
          } else if (checksum === 'skip') {
            warnings.push(msg);
            checksumStatus[mk] = 'skipped';
            continue;
          } else {
            warnings.push(msg);
            checksumStatus[mk] = 'mismatch';
          }
        } else {
          checksumStatus[mk] = 'ok';
        }
      } else {
        checksumStatus[mk] = 'ok';
      }
    } catch (e: any) {
      if (e?.code === 'ENOENT' || String(e).includes('ENOENT')) {
        const msg = `Matrix '${mk}' file not found: ${matrixMeta.path}`;
        if (mode === 'strict') throw new Error(msg);
        warnings.push(msg);
        checksumStatus[mk] = 'skipped';
        continue;
      }
      const msg = `Failed to verify checksum for ${mk}: ${e instanceof Error ? e.message : String(e)}`;
      if (checksum === 'fail' && mode === 'strict') throw new Error(msg);
      warnings.push(msg);
      checksumStatus[mk] = 'mismatch';
    }

    // Parse and normalize
    let raw: MatrixCellRaw[] = [];
    try {
      raw = await parseJsonlStream(snapshotPath, matrixMeta.records, mk, { mode });
    } catch (e) {
      const msg = `Failed to parse ${mk} JSONL: ${e instanceof Error ? e.message : String(e)}`;
      if (mode === 'strict') throw new Error(msg);
      warnings.push(msg);
      raw = [];
    }
    if (raw.length > 0) {
      const norm = normalizeMatrixCells(raw, mk);
      if (norm.metrics.warnings.length > 0) norm.metrics.warnings.forEach(w => warnings.push(`${mk}: ${w}`));
      matrices[mk] = norm.cells;
    }
  }

  return { manifest, matrices, warnings, checksumStatus: checksumStatus as any };
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
  const content = await fs.readFile(filePath);
  const hash = createHash('sha256').update(content).digest('hex');
  return hash;
}
