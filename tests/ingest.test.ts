import path from 'path';
import { promises as fs, mkdtempSync } from 'fs';
import os from 'os';
import { loadFrameworkRun } from '@/lib/framework/ingest';
import type { FrameworkRunManifest, MatrixCell } from '@/types/framework';

describe('framework ingestion', () => {
  let tempDir: string;
  
  beforeEach(() => {
    // Create temporary directory for each test
    tempDir = mkdtempSync(path.join(os.tmpdir(), 'ingest-test-'));
  });
  
  afterEach(async () => {
    // Cleanup temporary directory
    try {
      await fs.rm(tempDir, { recursive: true, force: true });
    } catch (error) {
      console.warn('Failed to cleanup temp dir:', tempDir, error);
    }
  });
  
  // Helper to create test fixtures dynamically
  async function createTestFixture(runId: string, manifest: any, matrices?: Record<string, MatrixCell[]>) {
    const runDir = path.join(tempDir, 'runs', runId);
    const snapshotsDir = path.join(runDir, 'snapshots');
    
    await fs.mkdir(snapshotsDir, { recursive: true });
    
    // Write manifest
    await fs.writeFile(path.join(runDir, 'index.json'), JSON.stringify(manifest, null, 2));
    
    // Always create all JSONL files, even if empty
    const allMatrixTypes = ['C', 'D', 'X', 'E'];
    for (const matrixType of allMatrixTypes) {
      const cells = matrices?.[matrixType] || [];
      const jsonlContent = cells.map(cell => JSON.stringify(cell)).join('\n');
      await fs.writeFile(path.join(snapshotsDir, `${matrixType}.jsonl`), jsonlContent);
    }
    
    return runDir;
  }
  
  test('happy path parses manifest and snapshots', async () => {
    // Arrange - create valid test fixture
    const runId = 'sample_happy_001';
    const manifest = {
      run_id: runId,
      created_at: '2024-01-01T10:00:00Z',
      tool: { name: 'chirality-framework', version: '1.0.0' },
      framework_schema_version: '1.0.0',
      problem: { title: 'Test Problem', statement: 'Test statement for validation' },
      durations: { total_ms: 45000 },
      matrices: {
        C: { path: 'snapshots/C.jsonl', records: 1, sha256: 'placeholder' },
        D: { path: 'snapshots/D.jsonl', records: 1, sha256: 'placeholder' },
        X: { path: 'snapshots/X.jsonl', records: 0, sha256: 'placeholder' },
        E: { path: 'snapshots/E.jsonl', records: 0, sha256: 'placeholder' }
      }
    };
    
    const matrices = {
      C: [{
        id: 'c1', matrix: 'C' as const, row: 0, col: 0, text: 'System requirements text',
        refs: [], citations: [], row_label: 'Row1', col_label: 'Col1', station: 'Problem Requirements'
      }],
      D: [{
        id: 'd1', matrix: 'D' as const, row: 0, col: 0, text: 'Design specification text',
        refs: [], citations: [], row_label: 'Row1', col_label: 'Col1', station: 'Solution Objectives'
      }]
    };
    
    await createTestFixture(runId, manifest, matrices);
    const runsDir = path.join(tempDir, 'runs');
    
    // Act
    const result = await loadFrameworkRun(runId, { 
      runsDir, 
      verifyChecksums: false
    });
    
    // Assert manifest structure
    expect(result.manifest.run_id).toBe(runId);
    expect(result.manifest.framework_schema_version).toBe('1.0.0');
    expect(result.manifest.problem.title).toBeDefined();
    expect(result.manifest.problem.statement).toBeDefined();
    
    // Assert matrices are loaded
    expect(result.matrices.C).toBeInstanceOf(Array);
    expect(result.matrices.D).toBeInstanceOf(Array);
    expect(result.matrices.X).toBeInstanceOf(Array);
    expect(result.matrices.E).toBeInstanceOf(Array);
    
    // Check at least one matrix has content
    const totalCells = result.matrices.C.length + result.matrices.D.length + 
                      result.matrices.X.length + result.matrices.E.length;
    expect(totalCells).toBeGreaterThan(0);
    
    // Validate MatrixCell structure for non-empty matrices
    if (result.matrices.C.length > 0) {
      const cell = result.matrices.C[0];
      expect(cell.id).toBeDefined();
      expect(cell.matrix).toBe('C');
      expect(cell.text).toBeDefined();
      expect(cell.citations).toBeInstanceOf(Array);
      expect(cell.refs).toBeInstanceOf(Array);
    }
  });
  
  test('fails on missing manifest file', async () => {
    // Arrange - don't create any fixtures, just use temp directory
    const runId = 'nonexistent_run';
    const runsDir = path.join(tempDir, 'runs');
    
    // Act & Assert
    await expect(loadFrameworkRun(runId, { runsDir }))
      .rejects
      .toThrow(/Failed to read or parse manifest/);
  });
  
  test('fails on missing snapshot file', async () => {
    // Arrange - create manifest but no snapshot files
    const runId = 'sample_edge_001';
    const manifest = {
      run_id: runId,
      created_at: '2024-01-01T10:00:00Z',
      tool: { name: 'chirality-framework', version: '1.0.0' },
      framework_schema_version: '1.0.0',
      problem: { title: 'Test', statement: 'Test' },
      durations: { total_ms: 1000 },
      matrices: {
        C: { path: 'snapshots/C.jsonl', records: 1, sha256: 'placeholder' },
        D: { path: 'snapshots/D.jsonl', records: 0, sha256: 'placeholder' },
        X: { path: 'snapshots/X.jsonl', records: 0, sha256: 'placeholder' },
        E: { path: 'snapshots/E.jsonl', records: 0, sha256: 'placeholder' }
      }
    };
    
    // Only create manifest, no snapshot files (but create snapshots dir)
    const runDir = path.join(tempDir, 'runs', runId);
    const snapshotsDir = path.join(runDir, 'snapshots');
    await fs.mkdir(snapshotsDir, { recursive: true });
    await fs.writeFile(path.join(runDir, 'index.json'), JSON.stringify(manifest, null, 2));
    // Deliberately don't create C.jsonl to trigger "snapshot file not found"
    
    const runsDir = path.join(tempDir, 'runs');
    
    // Act & Assert - should fail because C.jsonl file doesn't exist
    await expect(loadFrameworkRun(runId, { runsDir }))
      .rejects
      .toThrow(/Snapshot file not found|ENOENT/);
  });
  
  test('fails on malformed JSONL line', async () => {
    // Arrange - create fixture with invalid JSON in snapshot
    const runId = 'sample_malformed';
    const manifest = {
      run_id: runId,
      created_at: '2024-01-01T10:00:00Z',
      tool: { name: 'chirality-framework', version: '1.0.0' },
      framework_schema_version: '1.0.0',
      problem: { title: 'Test', statement: 'Test' },
      durations: { total_ms: 1000 },
      matrices: {
        C: { path: 'snapshots/C.jsonl', records: 1, sha256: 'placeholder' },
        D: { path: 'snapshots/D.jsonl', records: 0, sha256: 'placeholder' },
        X: { path: 'snapshots/X.jsonl', records: 0, sha256: 'placeholder' },
        E: { path: 'snapshots/E.jsonl', records: 0, sha256: 'placeholder' }
      }
    };
    
    const runDir = path.join(tempDir, 'runs', runId);
    const snapshotsDir = path.join(runDir, 'snapshots');
    await fs.mkdir(snapshotsDir, { recursive: true });
    
    // Write manifest
    await fs.writeFile(path.join(runDir, 'index.json'), JSON.stringify(manifest, null, 2));
    
    // Write malformed JSONL
    await fs.writeFile(path.join(snapshotsDir, 'C.jsonl'), '{invalid json missing quote}');
    
    const runsDir = path.join(tempDir, 'runs');
    
    // Act & Assert
    await expect(loadFrameworkRun(runId, { runsDir }))
      .rejects
      .toThrow(/Failed to parse JSONL line/);
  });
  
  test('fails on major schema version mismatch', async () => {
    // Arrange - create manifest with incompatible major version
    const runId = 'sample_version_2';
    const manifest = {
      run_id: runId,
      created_at: '2024-01-01T10:00:00Z',
      tool: { name: 'chirality-framework', version: '2.0.0' },
      framework_schema_version: '2.0.0', // Incompatible major version
      problem: { title: 'Test', statement: 'Test' },
      durations: { total_ms: 1000 },
      matrices: {
        C: { path: 'snapshots/C.jsonl', records: 0, sha256: 'placeholder' },
        D: { path: 'snapshots/D.jsonl', records: 0, sha256: 'placeholder' },
        X: { path: 'snapshots/X.jsonl', records: 0, sha256: 'placeholder' },
        E: { path: 'snapshots/E.jsonl', records: 0, sha256: 'placeholder' }
      }
    };
    
    await createTestFixture(runId, manifest, {});
    const runsDir = path.join(tempDir, 'runs');
    
    // Act & Assert
    await expect(loadFrameworkRun(runId, { runsDir, allowedMajor: 1 }))
      .rejects
      .toThrow(/Framework schema version .* is not compatible/);
  });
  
  test('warns on minor/patch version differences but accepts', async () => {
    // Arrange - create manifest with newer minor version
    const runId = 'sample_version_11';
    const manifest = {
      run_id: runId,
      created_at: '2024-01-01T10:00:00Z',
      tool: { name: 'chirality-framework', version: '1.1.0' },
      framework_schema_version: '1.1.0', // Newer minor version
      problem: { title: 'Test', statement: 'Test' },
      durations: { total_ms: 1000 },
      matrices: {
        C: { path: 'snapshots/C.jsonl', records: 0, sha256: 'placeholder' },
        D: { path: 'snapshots/D.jsonl', records: 0, sha256: 'placeholder' },
        X: { path: 'snapshots/X.jsonl', records: 0, sha256: 'placeholder' },
        E: { path: 'snapshots/E.jsonl', records: 0, sha256: 'placeholder' }
      }
    };
    
    await createTestFixture(runId, manifest, {});
    const runsDir = path.join(tempDir, 'runs');
    
    // Mock console.warn to capture warnings
    const originalWarn = console.warn;
    const warnings: string[] = [];
    console.warn = (message: string) => warnings.push(message);
    
    try {
      // Act
      const result = await loadFrameworkRun(runId, { 
        runsDir, 
        verifyChecksums: false,
        allowedMajor: 1 
      });
      
      // Assert - should succeed with warning
      expect(result.manifest.framework_schema_version).toBe('1.1.0');
      expect(warnings.some(w => w.includes('newer than baseline'))).toBe(true);
      
    } finally {
      console.warn = originalWarn;
    }
  });
  
  test('validates record counts match JSONL line counts', async () => {
    // Arrange - manifest says 5 records but file has 3 lines
    const runId = 'sample_count_mismatch';
    const manifest = {
      run_id: runId,
      created_at: '2024-01-01T10:00:00Z',
      tool: { name: 'chirality-framework', version: '1.0.0' },
      framework_schema_version: '1.0.0',
      problem: { title: 'Test', statement: 'Test' },
      durations: { total_ms: 1000 },
      matrices: {
        C: { path: 'snapshots/C.jsonl', records: 5, sha256: 'placeholder' }, // Claims 5 records
        D: { path: 'snapshots/D.jsonl', records: 0, sha256: 'placeholder' },
        X: { path: 'snapshots/X.jsonl', records: 0, sha256: 'placeholder' },
        E: { path: 'snapshots/E.jsonl', records: 0, sha256: 'placeholder' }
      }
    };
    
    // Create matrices with only 3 cells (mismatch)
    const matrices = {
      C: [
        { id: 'c1', matrix: 'C' as const, row: 0, col: 0, text: 'Cell 1', refs: [], citations: [], row_label: 'R1', col_label: 'C1', station: 'Problem Requirements' },
        { id: 'c2', matrix: 'C' as const, row: 0, col: 1, text: 'Cell 2', refs: [], citations: [], row_label: 'R1', col_label: 'C2', station: 'Problem Requirements' },
        { id: 'c3', matrix: 'C' as const, row: 0, col: 2, text: 'Cell 3', refs: [], citations: [], row_label: 'R1', col_label: 'C3', station: 'Problem Requirements' }
      ] // 3 actual records vs 5 claimed
    };
    
    await createTestFixture(runId, manifest, matrices);
    const runsDir = path.join(tempDir, 'runs');
    
    // Act & Assert
    await expect(loadFrameworkRun(runId, { runsDir }))
      .rejects
      .toThrow(/Record count mismatch/);
  });
  
  test('validates checksum when enabled', async () => {
    // Arrange - create fixture with wrong checksum
    const runId = 'sample_checksum_fail';
    const manifest = {
      run_id: runId,
      created_at: '2024-01-01T10:00:00Z',
      tool: { name: 'chirality-framework', version: '1.0.0' },
      framework_schema_version: '1.0.0',
      problem: { title: 'Test', statement: 'Test' },
      durations: { total_ms: 1000 },
      matrices: {
        C: { path: 'snapshots/C.jsonl', records: 1, sha256: 'wrong_checksum_here' },
        D: { path: 'snapshots/D.jsonl', records: 0, sha256: 'placeholder' },
        X: { path: 'snapshots/X.jsonl', records: 0, sha256: 'placeholder' },
        E: { path: 'snapshots/E.jsonl', records: 0, sha256: 'placeholder' }
      }
    };
    
    const matrices = {
      C: [{
        id: 'c1', matrix: 'C' as const, row: 0, col: 0, text: 'Test content',
        refs: [], citations: [], row_label: 'R1', col_label: 'C1', station: 'Problem Requirements'
      }]
    };
    
    await createTestFixture(runId, manifest, matrices);
    const runsDir = path.join(tempDir, 'runs');
    
    // Act & Assert
    await expect(loadFrameworkRun(runId, { runsDir, verifyChecksums: true }))
      .rejects
      .toThrow(/Checksum mismatch/);
  });
  
  test('skips checksum validation when disabled', async () => {
    // Arrange - create fixture with wrong checksum but checksum validation disabled
    const runId = 'sample_checksum_skip';
    const manifest = {
      run_id: runId,
      created_at: '2024-01-01T10:00:00Z',
      tool: { name: 'chirality-framework', version: '1.0.0' },
      framework_schema_version: '1.0.0',
      problem: { title: 'Test', statement: 'Test' },
      durations: { total_ms: 1000 },
      matrices: {
        C: { path: 'snapshots/C.jsonl', records: 1, sha256: 'deliberately_wrong_checksum' },
        D: { path: 'snapshots/D.jsonl', records: 0, sha256: 'placeholder' },
        X: { path: 'snapshots/X.jsonl', records: 0, sha256: 'placeholder' },
        E: { path: 'snapshots/E.jsonl', records: 0, sha256: 'placeholder' }
      }
    };
    
    const matrices = {
      C: [{
        id: 'c1', matrix: 'C' as const, row: 0, col: 0, text: 'Content with wrong checksum',
        refs: [], citations: [], row_label: 'R1', col_label: 'C1', station: 'Problem Requirements'
      }]
    };
    
    await createTestFixture(runId, manifest, matrices);
    const runsDir = path.join(tempDir, 'runs');
    
    // Act - should succeed despite wrong checksum when validation disabled
    const result = await loadFrameworkRun(runId, { 
      runsDir, 
      verifyChecksums: false 
    });
    
    // Assert
    expect(result.manifest.run_id).toBe(runId);
    expect(result.matrices.C).toHaveLength(1);
  });
  
  test('validates matrix cell structure', async () => {
    // Arrange - create fixture with invalid MatrixCell (missing required field)
    const runId = 'sample_invalid_cell';
    const manifest = {
      run_id: runId,
      created_at: '2024-01-01T10:00:00Z',
      tool: { name: 'chirality-framework', version: '1.0.0' },
      framework_schema_version: '1.0.0',
      problem: { title: 'Test', statement: 'Test' },
      durations: { total_ms: 1000 },
      matrices: {
        C: { path: 'snapshots/C.jsonl', records: 1, sha256: 'placeholder' },
        D: { path: 'snapshots/D.jsonl', records: 0, sha256: 'placeholder' },
        X: { path: 'snapshots/X.jsonl', records: 0, sha256: 'placeholder' },
        E: { path: 'snapshots/E.jsonl', records: 0, sha256: 'placeholder' }
      }
    };
    
    const runDir = path.join(tempDir, 'runs', runId);
    const snapshotsDir = path.join(runDir, 'snapshots');
    await fs.mkdir(snapshotsDir, { recursive: true });
    
    // Write manifest
    await fs.writeFile(path.join(runDir, 'index.json'), JSON.stringify(manifest, null, 2));
    
    // Write invalid MatrixCell (missing station field) and empty files for others
    const invalidCell = { id: 'c1', matrix: 'C', text: 'Test' }; // Missing required fields
    await fs.writeFile(path.join(snapshotsDir, 'C.jsonl'), JSON.stringify(invalidCell));
    await fs.writeFile(path.join(snapshotsDir, 'D.jsonl'), '');
    await fs.writeFile(path.join(snapshotsDir, 'X.jsonl'), '');
    await fs.writeFile(path.join(snapshotsDir, 'E.jsonl'), '');
    
    const runsDir = path.join(tempDir, 'runs');
    
    // Act & Assert
    await expect(loadFrameworkRun(runId, { runsDir }))
      .rejects
      .toThrow(/Invalid MatrixCell structure/);
  });
  
  test('prevents path traversal attacks', async () => {
    // Arrange - malicious runId attempting path traversal
    const maliciousRunId = '../../../etc/passwd';
    const runsDir = path.join(tempDir, 'runs');
    
    // Act & Assert
    await expect(loadFrameworkRun(maliciousRunId, { runsDir }))
      .rejects
      .toThrow(/Path traversal detected|Failed to read or parse manifest/);
  });
});

// Dynamic fixture creation ensures tests are self-contained and reliable