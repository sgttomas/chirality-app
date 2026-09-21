#!/usr/bin/env node

import { spawn } from 'node:child_process';
import { constants as fsConstants } from 'node:fs';
import { access, copyFile, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const TMP_ROOT = path.join(
  process.env.TMPDIR ?? os.tmpdir(),
  'chirality-harness-section9-validation',
  'latest'
);
const LOG_DIR = path.join(TMP_ROOT, 'logs');
const TMP_SUMMARY_PATH = path.join(TMP_ROOT, 'summary.json');
const SCRIPT_PATH = fileURLToPath(import.meta.url);
const SCRIPT_DIR = path.dirname(SCRIPT_PATH);
const SOURCE_MANIFEST_PATH = path.join(SCRIPT_DIR, 'harness-section9-manifest.json');

function stableSummaryPath(cwd) {
  return path.resolve(cwd, 'artifacts', 'harness', 'section9', 'latest', 'summary.json');
}

function stableManifestPath(cwd) {
  return path.resolve(cwd, 'artifacts', 'harness', 'section9', 'latest', 'manifest.json');
}

const SECTION9_IDS = [
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

function nowIso() {
  return new Date().toISOString();
}

function npmCommand() {
  return process.platform === 'win32' ? 'npm.cmd' : 'npm';
}

function fullTestCommand() {
  return `${npmCommand()} run test -- --testTimeout=15000`;
}

async function ensureReadableFile(filePath) {
  await access(filePath, fsConstants.R_OK);
}

async function ensureTestFilesExist(testFiles, cwd) {
  for (const testFile of testFiles) {
    await ensureReadableFile(path.resolve(cwd, testFile));
  }
}

function requireNonEmptyStringArray(value, label, checkId) {
  if (!Array.isArray(value) || value.length === 0 || value.some((item) => typeof item !== 'string' || item.length === 0)) {
    throw new Error(`${checkId} must declare a non-empty ${label} array.`);
  }
}

async function loadManifest(cwd) {
  const manifest = JSON.parse(await readFile(SOURCE_MANIFEST_PATH, 'utf8'));
  if (manifest.schemaVersion !== 1) {
    throw new Error('Section 9 manifest schemaVersion must be 1.');
  }
  if (!Array.isArray(manifest.checks)) {
    throw new Error('Section 9 manifest checks must be an array.');
  }

  const ids = manifest.checks.map((check) => check?.id);
  if (new Set(ids).size !== ids.length) {
    throw new Error('Section 9 manifest contains duplicate check IDs.');
  }
  if (ids.length !== SECTION9_IDS.length || SECTION9_IDS.some((id) => !ids.includes(id))) {
    throw new Error('Section 9 manifest must contain the exact governed 16-ID inventory.');
  }

  for (const check of manifest.checks) {
    requireNonEmptyStringArray(check.sourceReferences, 'sourceReferences', check.id);
    requireNonEmptyStringArray(check.testFiles, 'testFiles', check.id);
    requireNonEmptyStringArray(check.evidenceFiles, 'evidenceFiles', check.id);
    if (!Array.isArray(check.warnings) || !Array.isArray(check.blockers)) {
      throw new Error(`${check.id} must declare warnings and blockers arrays.`);
    }
    await ensureTestFilesExist([...check.testFiles, ...check.evidenceFiles], cwd);
  }

  return manifest;
}

async function writeJson(filePath, value) {
  await mkdir(path.dirname(filePath), { recursive: true });
  await writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function runVitest(testFiles, cwd, reportPath) {
  return new Promise((resolve, reject) => {
    const startedAt = nowIso();
    const startMs = Date.now();
    const child = spawn(npmCommand(), [
      'run',
      'test',
      '--',
      ...testFiles,
      '--reporter=default',
      '--reporter=json',
      `--outputFile.json=${reportPath}`
    ], {
      cwd,
      env: process.env,
      stdio: ['ignore', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (chunk) => {
      const text = chunk.toString();
      stdout += text;
      process.stdout.write(text);
    });

    child.stderr.on('data', (chunk) => {
      const text = chunk.toString();
      stderr += text;
      process.stderr.write(text);
    });

    child.on('error', reject);
    child.on('close', (code) => {
      resolve({
        code: code ?? 1,
        stdout,
        stderr,
        startedAt,
        endedAt: nowIso(),
        durationMs: Date.now() - startMs
      });
    });
  });
}

export function collectUniqueTestFiles(manifest) {
  return [...new Set(manifest.checks.flatMap((check) => check.testFiles))];
}

function fileResultsFromReport(report, testFiles, cwd, processResult) {
  const suites = new Map(
    (Array.isArray(report?.testResults) ? report.testResults : []).map((suite) => [
      path.resolve(cwd, suite.name),
      suite
    ])
  );
  return new Map(testFiles.map((testFile) => {
    const suite = suites.get(path.resolve(cwd, testFile));
    const assertions = Array.isArray(suite?.assertionResults) ? suite.assertionResults : [];
    const passed =
      (processResult.code ?? processResult.exitCode) === 0 &&
      suite?.status === 'passed' &&
      assertions.length > 0 &&
      assertions.every((assertion) => assertion.status === 'passed');
    return [testFile, {
      code: passed ? 0 : 1,
      startedAt: processResult.startedAt,
      endedAt: processResult.endedAt,
      durationMs: processResult.durationMs,
      stdoutLog: processResult.stdoutLog,
      stderrLog: processResult.stderrLog
    }];
  }));
}

export function isReusableFullTestResult(result, manifest, cwd) {
  return (
    result?.id === 'full_test' &&
    result?.status === 'pass' &&
    result?.exitCode === 0 &&
    result?.command.startsWith(fullTestCommand()) &&
    result.command.includes('--reporter=json') &&
    result.command.includes('--outputFile.json=') &&
    typeof result?.startedAt === 'string' &&
    typeof result?.endedAt === 'string' &&
    [...fileResultsFromReport(
      result.vitestReport,
      collectUniqueTestFiles(manifest),
      cwd,
      { code: result.exitCode }
    ).values()].every((fileResult) => fileResult.code === 0)
  );
}

async function runCheck(check, testResults, reusedFullTestResult) {
  const startedAt = nowIso();
  const startMs = Date.now();

  const fileResults = check.testFiles.map((testFile) => testResults.get(testFile));
  const missingResult = fileResults.some((result) => !result);
  const passed =
    !missingResult && fileResults.every((result) => (result.code ?? result.exitCode) === 0);
  const stdoutLog = fileResults.find((result) => result?.stdoutLog)?.stdoutLog;
  const stderrLog = fileResults.find((result) => result?.stderrLog)?.stderrLog;

  return {
    id: check.id,
    status: passed ? 'pass' : 'fail',
    durationMs: reusedFullTestResult ? 0 : Math.max(...fileResults.map((result) => result?.durationMs ?? 0)),
    testFiles: check.testFiles,
    sourceReferences: check.sourceReferences,
    evidenceFiles: check.evidenceFiles,
    warnings: check.warnings,
    blockers: check.blockers,
    details: {
      exitCode: passed ? 0 : 1,
      ...(stdoutLog ? { stdoutLog } : {}),
      ...(stderrLog ? { stderrLog } : {}),
      ...(reusedFullTestResult
        ? {
            reusedFrom: {
              id: reusedFullTestResult.id,
              command: reusedFullTestResult.command,
              startedAt: reusedFullTestResult.startedAt,
              endedAt: reusedFullTestResult.endedAt
            }
          }
        : { testRuns: check.testFiles })
    },
    ...(passed
      ? {}
      : { error: missingResult ? 'Current invocation has no test result.' : 'Vitest failed.' }),
    startedAt: reusedFullTestResult?.startedAt ?? startedAt,
    endedAt: reusedFullTestResult?.endedAt ?? nowIso()
  };
}

async function runValidation({ cwd, log, reuseFullTestResult }) {
  const manifest = await loadManifest(cwd);
  await rm(TMP_ROOT, { recursive: true, force: true });
  await mkdir(LOG_DIR, { recursive: true });

  const reuseRequested = reuseFullTestResult !== undefined;
  const reusableFullTestResult = isReusableFullTestResult(reuseFullTestResult, manifest, cwd)
    ? reuseFullTestResult
    : undefined;
  const uniqueTestFiles = collectUniqueTestFiles(manifest);
  let testResults;
  if (reuseRequested) {
    testResults = reusableFullTestResult
      ? fileResultsFromReport(
          reusableFullTestResult.vitestReport,
          uniqueTestFiles,
          cwd,
          reusableFullTestResult
        )
      : new Map();
  } else {
    const reportPath = path.join(TMP_ROOT, 'vitest-report.json');
    const stdoutLog = path.join(LOG_DIR, 'vitest.stdout.log');
    const stderrLog = path.join(LOG_DIR, 'vitest.stderr.log');
    log(`HARNESS_SECTION9_TEST_FILE_COUNT=${uniqueTestFiles.length}`);
    const processResult = await runVitest(uniqueTestFiles, cwd, reportPath);
    await writeFile(stdoutLog, processResult.stdout, 'utf8');
    await writeFile(stderrLog, processResult.stderr, 'utf8');
    let report;
    try {
      report = JSON.parse(await readFile(reportPath, 'utf8'));
    } catch {
      report = undefined;
    }
    testResults = fileResultsFromReport(report, uniqueTestFiles, cwd, {
      ...processResult,
      stdoutLog,
      stderrLog
    });
  }

  const results = [];
  for (const check of manifest.checks) {
    log(`HARNESS_SECTION9_CHECK_START=${check.id}`);
    results.push(await runCheck(check, testResults, reusableFullTestResult));
  }

  const status = results.every((result) => result.status === 'pass') ? 'pass' : 'fail';
  const summary = {
    generatedAt: nowIso(),
    status,
    testCount: results.length,
    manifestPath: stableManifestPath(cwd),
    results
  };

  await writeJson(TMP_SUMMARY_PATH, summary);

  // Warm read to ensure summary is parseable and stable before copying it.
  JSON.parse(await readFile(TMP_SUMMARY_PATH, 'utf8'));

  await mkdir(path.dirname(stableSummaryPath(cwd)), { recursive: true });
  await copyFile(SOURCE_MANIFEST_PATH, stableManifestPath(cwd));
  await copyFile(TMP_SUMMARY_PATH, stableSummaryPath(cwd));
  await ensureReadableFile(stableManifestPath(cwd));
  await ensureReadableFile(stableSummaryPath(cwd));

  log(`HARNESS_SECTION9_SUMMARY_PATH=${stableSummaryPath(cwd)}`);
  log(`HARNESS_SECTION9_MANIFEST_PATH=${stableManifestPath(cwd)}`);
  log(`HARNESS_SECTION9_SOURCE_SUMMARY_PATH=${TMP_SUMMARY_PATH}`);
  log(`HARNESS_SECTION9_STATUS=${status}`);
  log(`HARNESS_SECTION9_TEST_COUNT=${results.length}`);

  return status === 'pass' ? 0 : 1;
}

/**
 * Runs the Section 9 governed validation. Returns the process exit code
 * (0 pass, 1 fail). `opts.cwd` overrides the working directory and
 * `opts.log` / `opts.logError` override the output writers so tests can call
 * this in-process instead of spawning node.
 */
export async function run(argv = process.argv.slice(2), opts = {}) {
  void argv;
  const cwd = opts.cwd ?? process.cwd();
  const log = opts.log ?? ((line) => console.log(line));
  const logError = opts.logError ?? ((line) => console.error(line));

  try {
    return await runValidation({ cwd, log, reuseFullTestResult: opts.reuseFullTestResult });
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    logError(`Harness Section 9 validation failed: ${message}`);
    log(`HARNESS_SECTION9_SUMMARY_PATH=${stableSummaryPath(cwd)}`);
    log(`HARNESS_SECTION9_SOURCE_SUMMARY_PATH=${TMP_SUMMARY_PATH}`);
    log('HARNESS_SECTION9_STATUS=fail');
    log(`HARNESS_SECTION9_TEST_COUNT=${SECTION9_IDS.length}`);
    return 1;
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === SCRIPT_PATH) {
  process.exitCode = await run();
}
