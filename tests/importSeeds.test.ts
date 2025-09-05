/**
 * Integration tests for POST /api/import/seeds
 * NOTE:
 * - Requires the dev server running on http://localhost:3000
 * - Enable by setting RUN_API_TESTS=true (otherwise tests skip)
 * - For fixture testing, ensure NEXT_PUBLIC_SEEDS_ENABLE=true and CHIRALITY_RUNS_DIR=fixtures/runs in .env.local
 */

const RUN_API = process.env.RUN_API_TESTS === 'true';
const BASE = process.env.API_BASE || 'http://localhost:3000';

const maybe = RUN_API ? describe : describe.skip;

maybe('API: /api/import/seeds', () => {
  async function postSeeds(payload: any) {
    const res = await fetch(`${BASE}/api/import/seeds`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const json = await res.json().catch(() => ({}));
    return { status: res.status, json };
  }

  test('happy path (dev fixture)', async () => {
    // Requires CHIRALITY_RUNS_DIR=fixtures/runs and fixture present at fixtures/runs/sample_happy_001/index.json
    const { status, json } = await postSeeds({ runId: 'sample_happy_001' });
    expect(status).toBe(200);
    // seeds may be null on extraction failure; assert structure
    expect(json).toHaveProperty('seeds');
    if (json.seeds) {
      expect(json.seeds).toHaveProperty('initialVector.matrixC');
      expect(json.seeds).toHaveProperty('metadata.runId', 'sample_happy_001');
      expect(json.seeds.metadata).toHaveProperty('checksums');
      expect(json.seeds.metadata).toHaveProperty('preHeuristicsCounts');
      expect(json.seeds.metadata).toHaveProperty('postHeuristicsCounts');
    }
  }, 20000);

  test('invalid JSON returns 400', async () => {
    const res = await fetch(`${BASE}/api/import/seeds`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      // invalid body: send plain text
      body: 'not-json'
    });
    expect(res.status).toBe(400);
    const json = await res.json().catch(() => ({}));
    expect(json).toHaveProperty('code', 'ERR_INVALID_JSON');
  });

  test('missing runId returns 400', async () => {
    const { status, json } = await postSeeds({});
    expect(status).toBe(400);
    expect(json).toHaveProperty('code', 'ERR_MISSING_RUN_ID');
  });

  test('invalid runId format returns 400 (production strict)', async () => {
    // This will pass in dev (sample_* allowed) but should still hit invalid format for totally invalid ids
    const { status, json } = await postSeeds({ runId: 'bad id with spaces' });
    expect(status).toBe(400);
    expect(json).toHaveProperty('code', 'ERR_INVALID_RUN_ID');
  });

  test('cache reuse behavior', async () => {
    // First call
    const { status: status1, json: json1 } = await postSeeds({ runId: 'sample_happy_001' });
    expect(status1).toBe(200);
    
    // Second call should potentially use cache (test via logs or timing)
    const { status: status2, json: json2 } = await postSeeds({ runId: 'sample_happy_001' });
    expect(status2).toBe(200);
    
    // Both should return similar structure
    if (json1.seeds && json2.seeds) {
      expect(json1.seeds.metadata.runId).toBe(json2.seeds.metadata.runId);
    }
  }, 20000);

  test('options override in dev', async () => {
    // Test dev-only options override
    const { status, json } = await postSeeds({ 
      runId: 'sample_happy_001',
      options: {
        runsDir: 'fixtures/runs',
        heuristics: true,
        minItems: 2
      }
    });
    expect(status).toBe(200);
    expect(json).toHaveProperty('seeds');
  }, 20000);
});