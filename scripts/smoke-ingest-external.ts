// Lightweight smoke test to ingest a framework run from CHIRALITY_RUNS_DIR
// Usage: ts-node scripts/smoke-ingest-external.ts <run_id>

import { loadFrameworkRun } from '../lib/framework/ingest';

async function main() {
  const runId = process.argv[2];
  if (!runId) {
    console.error('Usage: ts-node scripts/smoke-ingest-external.ts <run_id>');
    process.exit(1);
  }

  const runsDir = process.env.CHIRALITY_RUNS_DIR || 'runs';
  console.log(`[Smoke] Ingesting run '${runId}' from runsDir='${runsDir}'`);

  try {
    const result = await loadFrameworkRun(runId, {
      runsDir,
      verifyChecksums: true,
      allowedMajor: 1,
    });

    const counts = {
      C: result.matrices.C.length,
      D: result.matrices.D.length,
      X: result.matrices.X.length,
      E: result.matrices.E.length,
    };

    console.log('[Smoke] Manifest version:', result.manifest.framework_schema_version);
    console.log('[Smoke] Problem:', result.manifest.problem?.title || '(untitled)');
    console.log('[Smoke] Cell counts:', counts);
    if (result.matrices.C[0]) {
      const c0 = result.matrices.C[0];
      console.log('[Smoke] First C cell:', {
        id: c0.id,
        row: c0.row,
        col: c0.col,
        row_label: c0.row_label,
        col_label: c0.col_label,
        meta: c0.meta,
      });
    }

    console.log('[Smoke] OK');
    process.exit(0);
  } catch (err) {
    console.error('[Smoke] FAILED:', err instanceof Error ? err.message : String(err));
    process.exit(2);
  }
}

main();

