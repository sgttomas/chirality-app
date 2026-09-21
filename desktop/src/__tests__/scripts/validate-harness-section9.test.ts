import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import {
  collectUniqueTestFiles,
  isReusableFullTestResult,
  run
} from '../../../scripts/validate-harness-section9.mjs';

const MANIFEST_PATH = path.resolve(process.cwd(), 'scripts', 'harness-section9-manifest.json');

const REQUIRED_IDS = [
  'section9.runtime_engine_contract',
  'section9.adapter_turn_engine_event_log',
  'section9.adapter_message_mapper',
  'section9.session_event_replay',
  'section9.reliance_boundary_register',
  'section9.settingsources_isolation',
  'section9.sdk_session_link_resume',
  'section9.permission_overlay_hard_deny_precedence',
  'section9.tool_runtime_read_file',
  'section9.chirality_mcp_status_dependencies',
  'section9.path_containment_hook',
  'section9.instruction_root_protection_hook',
  'section9.tool_result_budget',
  'section9.context_compaction_boundary',
  'section9.subagent_governance_hook',
  'section9.domain_profile_validation'
];

type ManifestCheck = {
  id: string;
  sourceReferences: string[];
  testFiles: string[];
  evidenceFiles: string[];
  warnings: string[];
  blockers: string[];
};

describe('Section 9 governed manifest', () => {
  it('pins the exact source-defined inventory and review metadata', async () => {
    const manifest = JSON.parse(await readFile(MANIFEST_PATH, 'utf8')) as {
      schemaVersion: number;
      checks: ManifestCheck[];
    };

    expect(manifest.schemaVersion).toBe(1);
    expect(manifest.checks.map((check) => check.id)).toEqual(REQUIRED_IDS);
    for (const check of manifest.checks) {
      expect(check.sourceReferences.length).toBeGreaterThan(0);
      expect(check.testFiles.length).toBeGreaterThan(0);
      expect(check.evidenceFiles.length).toBeGreaterThan(0);
      expect(Array.isArray(check.warnings)).toBe(true);
      expect(Array.isArray(check.blockers)).toBe(true);
    }
  });

  it('deduplicates shared test files for one Section 9 invocation', async () => {
    const manifest = JSON.parse(await readFile(MANIFEST_PATH, 'utf8')) as {
      checks: ManifestCheck[];
    };
    const allTestFiles = manifest.checks.flatMap((check) => check.testFiles);

    expect(allTestFiles).toHaveLength(29);
    expect(collectUniqueTestFiles(manifest)).toHaveLength(20);
  });

  it('reuses only a passing full-suite report that covers every required file without skips', async () => {
    const manifest = JSON.parse(await readFile(MANIFEST_PATH, 'utf8')) as {
      checks: ManifestCheck[];
    };
    const suites = collectUniqueTestFiles(manifest).map((testFile) => ({
      name: path.resolve(process.cwd(), testFile),
      status: 'passed',
      assertionResults: [{ status: 'passed' }]
    }));
    const result = {
      id: 'full_test',
      status: 'pass',
      exitCode: 0,
      command: 'npm run test -- --testTimeout=15000 --reporter=json --outputFile.json=/tmp/current.json',
      startedAt: '2026-09-09T00:00:00.000Z',
      endedAt: '2026-09-09T00:01:00.000Z',
      vitestReport: { testResults: suites }
    };

    expect(isReusableFullTestResult(result, manifest, process.cwd())).toBe(true);
    expect(isReusableFullTestResult({ ...result, exitCode: 1 }, manifest, process.cwd())).toBe(false);
    expect(isReusableFullTestResult(
      { ...result, vitestReport: { testResults: suites.slice(1) } },
      manifest,
      process.cwd()
    )).toBe(false);
    expect(isReusableFullTestResult(
      {
        ...result,
        vitestReport: {
          testResults: suites.map((suite, index) => index === 0
            ? { ...suite, assertionResults: [{ status: 'skipped' }] }
            : suite)
        }
      },
      manifest,
      process.cwd()
    )).toBe(false);
  });

  it('materializes Section 9 from current full-suite coverage and fails closed without it', async () => {
    const fixtureRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-section9-reuse-'));
    const cwd = path.join(fixtureRoot, 'frontend');
    const manifest = JSON.parse(await readFile(MANIFEST_PATH, 'utf8')) as {
      checks: ManifestCheck[];
    };
    try {
      for (const file of new Set(manifest.checks.flatMap((check) => [
        ...check.testFiles,
        ...check.evidenceFiles
      ]))) {
        const filePath = path.resolve(cwd, file);
        await mkdir(path.dirname(filePath), { recursive: true });
        await writeFile(filePath, 'fixture\n');
      }
      const result = {
        id: 'full_test',
        status: 'pass',
        exitCode: 0,
        command: 'npm run test -- --testTimeout=15000 --reporter=json --outputFile.json=/tmp/current.json',
        startedAt: '2026-09-09T00:00:00.000Z',
        endedAt: '2026-09-09T00:01:00.000Z',
        durationMs: 60_000,
        vitestReport: {
          testResults: collectUniqueTestFiles(manifest).map((testFile) => ({
            name: path.resolve(cwd, testFile),
            status: 'passed',
            assertionResults: [{ status: 'passed' }]
          }))
        }
      };
      const quiet = { cwd, log: () => undefined, logError: () => undefined };

      expect(await run([], { ...quiet, reuseFullTestResult: result })).toBe(0);
      const summary = JSON.parse(await readFile(
        path.join(cwd, 'artifacts', 'harness', 'section9', 'latest', 'summary.json'),
        'utf8'
      ));
      expect(summary.status).toBe('pass');
      expect(summary.results).toHaveLength(16);

      expect(await run([], {
        ...quiet,
        reuseFullTestResult: { ...result, vitestReport: undefined }
      })).toBe(1);
    } finally {
      await rm(fixtureRoot, { recursive: true, force: true });
    }
  });

  // The runner/wrapper substring pins ("emits the stable manifest and makes
  // the release-quality wrapper validate it") moved to the consolidated
  // src/__tests__/contract-pins.manifest.ts (checked by contract-pins.test.ts).
});
