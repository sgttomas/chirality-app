import { promises as fs } from 'fs';
import path from 'path';
import { loadFrameworkRun } from '../lib/framework/ingest';

const RUNS_BASE = 'fixtures/runs';

async function ensureDir(p: string) {
  await fs.mkdir(p, { recursive: true });
}

describe('Framework Ingest - edge cases', () => {
  const baseDir = RUNS_BASE;

  test('unsupported format is skipped with warning (safe mode)', async () => {
    const runId = 'sample_format_unsupported_001';
    const runDir = path.join(baseDir, runId);
    const snapDir = path.join(runDir, 'snapshots');
    await ensureDir(snapDir);

    // Create minimal snapshots
    await fs.writeFile(path.join(snapDir, 'C.jsonl'), '{"id":"C:1","matrix":"C","row_label":"R","col_label":"C","station":"S","text":"t1","citations":[],"refs":[],"meta":{"order":1}}\n');
    await fs.writeFile(path.join(snapDir, 'D.jsonl'), '');
    await fs.writeFile(path.join(snapDir, 'X.jsonl'), '');
    await fs.writeFile(path.join(snapDir, 'E.jsonl'), '');

    const manifest = {
      run_id: runId,
      created_at: new Date().toISOString(),
      tool: { name: 'chirality-framework', version: '1.0.0' },
      framework_schema_version: '1.0.0',
      problem: { title: 't', statement: 's' },
      durations: { total_ms: 1 },
      matrices: {
        C: { path: 'snapshots/C.jsonl', records: 1, sha256: 'placeholder', bytes: 1, format: 'cells-jsonl-v2' },
        D: { path: 'snapshots/D.jsonl', records: 0, sha256: 'placeholder', bytes: 0, format: 'cells-jsonl-v1' },
        X: { path: 'snapshots/X.jsonl', records: 0, sha256: 'placeholder', bytes: 0, format: 'cells-jsonl-v1' },
        E: { path: 'snapshots/E.jsonl', records: 0, sha256: 'placeholder', bytes: 0, format: 'cells-jsonl-v1' }
      }
    };
    await fs.writeFile(path.join(runDir, 'index.json'), JSON.stringify(manifest, null, 2));

    const res = await loadFrameworkRun(runId, { runsDir: baseDir, mode: 'safe' });
    expect(res.matrices.C.length).toBe(0); // skipped
    expect(Array.isArray(res.warnings)).toBe(true);
  });

  test('record-count mismatch warns and proceeds in safe mode', async () => {
    const runId = 'sample_count_mismatch_001';
    const runDir = path.join(baseDir, runId);
    const snapDir = path.join(runDir, 'snapshots');
    await ensureDir(snapDir);

    await fs.writeFile(path.join(snapDir, 'C.jsonl'), '{"id":"C:1","matrix":"C","row_label":"R","col_label":"C","station":"S","text":"t1","citations":[],"refs":[],"meta":{"order":1}}\n');
    await fs.writeFile(path.join(snapDir, 'D.jsonl'), '');
    await fs.writeFile(path.join(snapDir, 'X.jsonl'), '');
    await fs.writeFile(path.join(snapDir, 'E.jsonl'), '');

    const manifest = {
      run_id: runId,
      created_at: new Date().toISOString(),
      tool: { name: 'chirality-framework', version: '1.0.0' },
      framework_schema_version: '1.0.0',
      problem: { title: 't', statement: 's' },
      durations: { total_ms: 1 },
      matrices: {
        C: { path: 'snapshots/C.jsonl', records: 2, sha256: 'placeholder', bytes: 1, format: 'cells-jsonl-v1' },
        D: { path: 'snapshots/D.jsonl', records: 0, sha256: 'placeholder', bytes: 0, format: 'cells-jsonl-v1' },
        X: { path: 'snapshots/X.jsonl', records: 0, sha256: 'placeholder', bytes: 0, format: 'cells-jsonl-v1' },
        E: { path: 'snapshots/E.jsonl', records: 0, sha256: 'placeholder', bytes: 0, format: 'cells-jsonl-v1' }
      }
    };
    await fs.writeFile(path.join(runDir, 'index.json'), JSON.stringify(manifest, null, 2));

    const res = await loadFrameworkRun(runId, { runsDir: baseDir, mode: 'safe' });
    expect(res.matrices.C.length).toBe(1); // still parsed
    expect(Array.isArray(res.warnings)).toBe(true);
  });

  test('checksum modes: warn, skip, fail (strict)', async () => {
    const runId = 'sample_checksum_001';
    const runDir = path.join(baseDir, runId);
    const snapDir = path.join(runDir, 'snapshots');
    await ensureDir(snapDir);

    // create one-line file; set incorrect sha in manifest
    const cPath = path.join(snapDir, 'C.jsonl');
    await fs.writeFile(cPath, '{"id":"C:1","matrix":"C","row_label":"R","col_label":"C","station":"S","text":"t1","citations":[],"refs":[],"meta":{"order":1}}\n');
    await fs.writeFile(path.join(snapDir, 'D.jsonl'), '');
    await fs.writeFile(path.join(snapDir, 'X.jsonl'), '');
    await fs.writeFile(path.join(snapDir, 'E.jsonl'), '');

    const manifest = {
      run_id: runId,
      created_at: new Date().toISOString(),
      tool: { name: 'chirality-framework', version: '1.0.0' },
      framework_schema_version: '1.0.0',
      problem: { title: 't', statement: 's' },
      durations: { total_ms: 1 },
      matrices: {
        C: { path: 'snapshots/C.jsonl', records: 1, sha256: 'deadbeef', bytes: 1, format: 'cells-jsonl-v1' },
        D: { path: 'snapshots/D.jsonl', records: 0, sha256: 'placeholder', bytes: 0, format: 'cells-jsonl-v1' },
        X: { path: 'snapshots/X.jsonl', records: 0, sha256: 'placeholder', bytes: 0, format: 'cells-jsonl-v1' },
        E: { path: 'snapshots/E.jsonl', records: 0, sha256: 'placeholder', bytes: 0, format: 'cells-jsonl-v1' }
      }
    };
    await fs.writeFile(path.join(runDir, 'index.json'), JSON.stringify(manifest, null, 2));

    // warn mode: include with mismatch status
    const warnRes = await loadFrameworkRun(runId, { runsDir: baseDir, mode: 'safe', checksum: 'warn' });
    expect(warnRes.matrices.C.length).toBe(1);
    expect(warnRes.checksumStatus?.C).toBeDefined();

    // skip mode: skip matrix on mismatch
    const skipRes = await loadFrameworkRun(runId, { runsDir: baseDir, mode: 'safe', checksum: 'skip' });
    expect(skipRes.matrices.C.length).toBe(0);

    // fail+strict: throw
    await expect(loadFrameworkRun(runId, { runsDir: baseDir, mode: 'strict', checksum: 'fail' })).rejects.toThrow();
  });
});

describe('Seed Heuristics pipeline', () => {
  const runId = 'sample_heuristics_001';
  const runDir = path.join(RUNS_BASE, runId);
  const snapDir = path.join(runDir, 'snapshots');

  beforeAll(async () => {
    await ensureDir(snapDir);
    const lines = [
      { text: '• Alpha beta gamma. With extra text after first sentence.' },
      { text: 'alpha beta gamma! duplicate casing' },
      { text: '  *   Mixed   whitespace   and   bullets   ' },
      { text: 'Emoji 😄 leading should be stripped.' },
      { text: 'Truncate this sentence because it is very long and should be cut.' }
    ];
    const cLines = lines.map((l, i) => JSON.stringify({ id:`C:${i+1}`, matrix:'C', row_label:'R', col_label:'C', station:'S', text:l.text, citations:[], refs:[], meta:{ order: i+1 } })).join('\n') + '\n';
    await fs.writeFile(path.join(snapDir, 'C.jsonl'), cLines);
    await fs.writeFile(path.join(snapDir, 'D.jsonl'), '');
    await fs.writeFile(path.join(snapDir, 'X.jsonl'), '');
    await fs.writeFile(path.join(snapDir, 'E.jsonl'), '');
    const manifest = {
      run_id: runId,
      created_at: new Date().toISOString(),
      tool: { name: 'chirality-framework', version: '1.0.0' },
      framework_schema_version: '1.0.0',
      problem: { title: 't', statement: 's' },
      durations: { total_ms: 1 },
      matrices: {
        C: { path: 'snapshots/C.jsonl', records: lines.length, sha256: 'placeholder', bytes: 1, format: 'cells-jsonl-v1' },
        D: { path: 'snapshots/D.jsonl', records: 0, sha256: 'placeholder', bytes: 0, format: 'cells-jsonl-v1' },
        X: { path: 'snapshots/X.jsonl', records: 0, sha256: 'placeholder', bytes: 0, format: 'cells-jsonl-v1' },
        E: { path: 'snapshots/E.jsonl', records: 0, sha256: 'placeholder', bytes: 0, format: 'cells-jsonl-v1' }
      }
    };
    await fs.writeFile(path.join(runDir, 'index.json'), JSON.stringify(manifest, null, 2));
  });

  test('apply full heuristics', async () => {
    const { extractSeeds } = await import('../lib/seeds/seedExtractor');
    const result = await extractSeeds({ runId, runsDir: RUNS_BASE, enableHeuristics: true, minItems: 1, maxItems: 10, maxLength: 40 });
    expect(result.seeds).not.toBeNull();
    if (result.seeds) {
      const seeds = result.seeds.initialVector.matrixC;
      // sentence first (no long suffixes)
      seeds.forEach(s => expect(s.length).toBeLessThanOrEqual(43));
      // case-insensitive dedupe should reduce duplicates
      const uniq = new Set(seeds.map(s => s.toLowerCase()));
      expect(uniq.size).toBe(seeds.length);
    }
  });
});

describe('Streaming performance (basic)', () => {
  test('handles large JSONL without error', async () => {
    const runId = 'sample_perf_001';
    const runDir = path.join(RUNS_BASE, runId);
    const snapDir = path.join(runDir, 'snapshots');
    await ensureDir(snapDir);

    const n = 5000; // keep moderate for CI stability
    const lines = Array.from({ length: n }, (_, i) => JSON.stringify({ id:`C:${i+1}`, matrix:'C', row_label:'R', col_label:'C', station:'S', text:`row ${i+1}`, citations:[], refs:[], meta:{ order: i+1 } })).join('\n') + '\n';
    await fs.writeFile(path.join(snapDir, 'C.jsonl'), lines);
    await fs.writeFile(path.join(snapDir, 'D.jsonl'), '');
    await fs.writeFile(path.join(snapDir, 'X.jsonl'), '');
    await fs.writeFile(path.join(snapDir, 'E.jsonl'), '');
    const manifest = {
      run_id: runId,
      created_at: new Date().toISOString(),
      tool: { name: 'chirality-framework', version: '1.0.0' },
      framework_schema_version: '1.0.0',
      problem: { title: 't', statement: 's' },
      durations: { total_ms: 1 },
      matrices: {
        C: { path: 'snapshots/C.jsonl', records: n, sha256: 'placeholder', bytes: 1, format: 'cells-jsonl-v1' },
        D: { path: 'snapshots/D.jsonl', records: 0, sha256: 'placeholder', bytes: 0, format: 'cells-jsonl-v1' },
        X: { path: 'snapshots/X.jsonl', records: 0, sha256: 'placeholder', bytes: 0, format: 'cells-jsonl-v1' },
        E: { path: 'snapshots/E.jsonl', records: 0, sha256: 'placeholder', bytes: 0, format: 'cells-jsonl-v1' }
      }
    };
    await fs.writeFile(path.join(runDir, 'index.json'), JSON.stringify(manifest, null, 2));

    const before = process.memoryUsage().rss;
    const res = await loadFrameworkRun(runId, { runsDir: RUNS_BASE, mode: 'safe' });
    const after = process.memoryUsage().rss;
    expect(res.matrices.C.length).toBe(n);
    // basic sanity: memory delta should not be outrageous for moderate n
    expect(after - before).toBeLessThan(200 * 1024 * 1024);
  }, 60000);
});

