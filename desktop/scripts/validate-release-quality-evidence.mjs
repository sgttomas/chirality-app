#!/usr/bin/env node

import { spawn } from 'node:child_process';
import { constants as fsConstants } from 'node:fs';
import { access, mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { run as runPremerge } from './validate-harness-premerge.mjs';
import { run as runSection9 } from './validate-harness-section9.mjs';

const REQUIRED_SECTION8_IDS = [
  'setup.server_reachable',
  'regression.session_crud',
  'section8.boot_error_taxonomy',
  'section8.smoke_stream',
  'section8.session_persistence_resume',
  'section8.permissions_dontask',
  'section8.interrupt_sigint',
  'section8.sdk_native_stream'
];

const LEGACY_REMOVED_SECTION8_ID = 'regression.api_chat_reachability';
const OUTPUT_ROOT = path.resolve(
  process.cwd(),
  'artifacts',
  'harness',
  'release-quality',
  'latest'
);
const SUMMARY_PATH = path.join(OUTPUT_ROOT, 'summary.json');
const LOG_ROOT = path.join(OUTPUT_ROOT, 'logs');
const SECTION8_SUMMARY_PATH = path.resolve(
  process.cwd(),
  'artifacts',
  'harness',
  'section8',
  'latest',
  'summary.json'
);
const SECTION9_SUMMARY_PATH = path.resolve(
  process.cwd(),
  'artifacts',
  'harness',
  'section9',
  'latest',
  'summary.json'
);
const SECTION9_MANIFEST_PATH = path.resolve(
  process.cwd(),
  'artifacts',
  'harness',
  'section9',
  'latest',
  'manifest.json'
);
const REQUIRED_SECTION9_IDS = [
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

function printUsage() {
  console.log(`Usage: node ./scripts/validate-release-quality-evidence.mjs [options]

Runs the runtime-premerge evidence profile and writes:
  artifacts/harness/release-quality/latest/summary.json

Options:
  --skip-premerge <reason>   Record a justified premerge skip instead of running
                             npm run harness:validate:premerge.
  --help                     Show this help.

The wrapper collects software validation evidence only. It does not publish,
issue, certify, seal, authenticate, notarize, or approve a release.`);
}

function readValue(argv, index, flagName) {
  const value = argv[index];
  if (!value || value.startsWith('--')) {
    throw new Error(`Missing value for ${flagName}`);
  }
  return value;
}

function parseArgs(argv) {
  const options = {
    help: false,
    skipPremergeReason: ''
  };

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];

    if (token === '--help') {
      options.help = true;
      continue;
    }

    if (token === '--skip-premerge') {
      options.skipPremergeReason = readValue(argv, index + 1, token).trim();
      index += 1;
      continue;
    }

    if (token.startsWith('--skip-premerge=')) {
      options.skipPremergeReason = token.slice('--skip-premerge='.length).trim();
      continue;
    }

    throw new Error(`Unknown option: ${token}`);
  }

  if (options.skipPremergeReason.length === 0 && process.env.RELEASE_QUALITY_SKIP_PREMERGE_REASON) {
    options.skipPremergeReason = process.env.RELEASE_QUALITY_SKIP_PREMERGE_REASON.trim();
  }

  return options;
}

function safeSegment(value) {
  return value.replace(/[^A-Za-z0-9_.-]/g, '_').slice(0, 120);
}

function runCommand({ id, args, vitestReportPath }) {
  return new Promise((resolve, reject) => {
    const startedAt = nowIso();
    const startedMs = Date.now();
    const commandArgs = vitestReportPath
      ? [...args, '--reporter=default', '--reporter=json', `--outputFile.json=${vitestReportPath}`]
      : args;
    const child = spawn(npmCommand(), commandArgs, {
      cwd: process.cwd(),
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
        id,
        status: code === 0 ? 'pass' : 'fail',
        command: `${npmCommand()} ${commandArgs.join(' ')}`,
        exitCode: code ?? 1,
        startedAt,
        endedAt: nowIso(),
        durationMs: Date.now() - startedMs,
        stdout,
        stderr
      });
    });
  });
}

async function runModuleCommand({ id, command, executionMode, execute }) {
  const startedAt = nowIso();
  const startedMs = Date.now();
  let stdout = '';
  let stderr = '';
  const log = (line) => {
    const text = `${line}\n`;
    stdout += text;
    process.stdout.write(text);
  };
  const logError = (line) => {
    const text = `${line}\n`;
    stderr += text;
    process.stderr.write(text);
  };
  const writeStdout = (text) => {
    stdout += text;
    process.stdout.write(text);
  };
  const writeStderr = (text) => {
    stderr += text;
    process.stderr.write(text);
  };
  const exitCode = await execute({ log, logError, writeStdout, writeStderr });
  return {
    id,
    status: exitCode === 0 ? 'pass' : 'fail',
    command,
    executionMode,
    exitCode,
    startedAt,
    endedAt: nowIso(),
    durationMs: Date.now() - startedMs,
    stdout,
    stderr
  };
}

async function writeCommandLogs(result) {
  const logBase = path.join(LOG_ROOT, safeSegment(result.id));
  const stdoutLog = `${logBase}.stdout.log`;
  const stderrLog = `${logBase}.stderr.log`;
  await mkdir(LOG_ROOT, { recursive: true });
  await writeFile(stdoutLog, result.stdout, 'utf8');
  await writeFile(stderrLog, result.stderr, 'utf8');
  return {
    id: result.id,
    status: result.status,
    command: result.command,
    exitCode: result.exitCode,
    startedAt: result.startedAt,
    endedAt: result.endedAt,
    durationMs: result.durationMs,
    stdoutLog,
    stderrLog
  };
}

async function readJson(filePath) {
  await access(filePath, fsConstants.R_OK);
  return JSON.parse(await readFile(filePath, 'utf8'));
}

function validateSection9Summary(summary, manifest) {
  const errors = [];
  if (!['pass', 'fail'].includes(summary.status)) {
    errors.push('Section 9 summary status must be pass or fail.');
  }
  if (!Number.isInteger(summary.testCount)) {
    errors.push('Section 9 summary testCount must be an integer.');
  }
  if (!Array.isArray(summary.results)) {
    errors.push('Section 9 summary results must be an array.');
  } else {
    const seen = new Set(summary.results.map((result) => result?.id));
    if (
      seen.size !== REQUIRED_SECTION9_IDS.length ||
      REQUIRED_SECTION9_IDS.some((id) => !seen.has(id))
    ) {
      errors.push('Section 9 summary must contain the exact governed 16-ID inventory.');
    }
    if (summary.results.length !== summary.testCount) {
      errors.push('Section 9 summary testCount must equal results.length.');
    }
    for (const result of summary.results) {
      if (!result || typeof result.id !== 'string' || result.id.length === 0) {
        errors.push('Every Section 9 result must have an id.');
      }
      if (!['pass', 'fail'].includes(result?.status)) {
        errors.push(`Section 9 result ${result?.id ?? '<unknown>'} has invalid status.`);
      }
      if (!Array.isArray(result?.testFiles) || result.testFiles.length === 0) {
        errors.push(`Section 9 result ${result?.id ?? '<unknown>'} must list testFiles.`);
      }
      for (const field of ['sourceReferences', 'evidenceFiles']) {
        if (!Array.isArray(result?.[field]) || result[field].length === 0) {
          errors.push(`Section 9 result ${result?.id ?? '<unknown>'} must list ${field}.`);
        }
      }
      for (const field of ['warnings', 'blockers']) {
        if (!Array.isArray(result?.[field])) {
          errors.push(`Section 9 result ${result?.id ?? '<unknown>'} must declare ${field}.`);
        }
      }
    }
  }
  if (summary.manifestPath !== SECTION9_MANIFEST_PATH) {
    errors.push('Section 9 summary manifestPath must identify the stable manifest artifact.');
  }
  if (manifest?.schemaVersion !== 1 || !Array.isArray(manifest?.checks)) {
    errors.push('Section 9 manifest must use schemaVersion 1 and declare checks.');
  } else {
    const manifestIds = new Set(manifest.checks.map((check) => check?.id));
    if (
      manifestIds.size !== REQUIRED_SECTION9_IDS.length ||
      REQUIRED_SECTION9_IDS.some((id) => !manifestIds.has(id))
    ) {
      errors.push('Section 9 manifest must contain the exact governed 16-ID inventory.');
    }
  }
  return errors;
}

function validateSection8Summary(summary) {
  const errors = [];
  const results = Array.isArray(summary.results) ? summary.results : [];
  const seen = new Set(results.map((result) => result.id));

  if (summary.status !== 'pass') {
    errors.push(`Section 8 summary status is ${String(summary.status)}, expected pass.`);
  }
  for (const requiredId of REQUIRED_SECTION8_IDS) {
    if (!seen.has(requiredId)) {
      errors.push(`Section 8 summary missing required id ${requiredId}.`);
    }
  }
  if (seen.has(LEGACY_REMOVED_SECTION8_ID)) {
    errors.push(`Section 8 summary contains removed legacy id ${LEGACY_REMOVED_SECTION8_ID}.`);
  }
  if (results.length !== REQUIRED_SECTION8_IDS.length) {
    errors.push('Section 8 summary result count differs from required ID count.');
  }
  return errors;
}

async function validateSummaries({ premergeSkipped }) {
  const checks = [];

  try {
    const section9Summary = await readJson(SECTION9_SUMMARY_PATH);
    const section9Manifest = await readJson(SECTION9_MANIFEST_PATH);
    const errors = validateSection9Summary(section9Summary, section9Manifest);
    checks.push({
      id: 'summary.section9',
      status: errors.length === 0 ? 'pass' : 'fail',
      artifactPath: SECTION9_SUMMARY_PATH,
      errors
    });
  } catch (error) {
    checks.push({
      id: 'summary.section9',
      status: 'fail',
      artifactPath: SECTION9_SUMMARY_PATH,
      errors: [error instanceof Error ? error.message : String(error)]
    });
  }

  if (premergeSkipped) {
    checks.push({
      id: 'summary.section8',
      status: 'skipped',
      artifactPath: SECTION8_SUMMARY_PATH,
      errors: []
    });
  } else {
    try {
      const section8Summary = await readJson(SECTION8_SUMMARY_PATH);
      const errors = validateSection8Summary(section8Summary);
      checks.push({
        id: 'summary.section8',
        status: errors.length === 0 ? 'pass' : 'fail',
        artifactPath: SECTION8_SUMMARY_PATH,
        errors
      });
    } catch (error) {
      checks.push({
        id: 'summary.section8',
        status: 'fail',
        artifactPath: SECTION8_SUMMARY_PATH,
        errors: [error instanceof Error ? error.message : String(error)]
      });
    }
  }

  const failCount = checks.filter((check) => check.status === 'fail').length;
  return {
    id: 'summary.consistency',
    status: failCount === 0 ? 'pass' : 'fail',
    checks
  };
}

function skippedResult(id, reason) {
  return {
    id,
    status: 'skipped',
    command: 'npm run harness:validate:premerge',
    reason,
    startedAt: nowIso(),
    endedAt: nowIso(),
    durationMs: 0
  };
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    printUsage();
    return;
  }

  await mkdir(OUTPUT_ROOT, { recursive: true });

  const rawCommands = [];
  const reportRoot = await mkdtemp(path.join(process.env.TMPDIR ?? os.tmpdir(), 'chirality-full-test-'));
  const vitestReportPath = path.join(reportRoot, 'vitest-report.json');
  const fullTestResult = await runCommand({
    id: 'full_test',
    args: ['run', 'test', '--', '--testTimeout=15000'],
    vitestReportPath
  });
  try {
    fullTestResult.vitestReport = JSON.parse(await readFile(vitestReportPath, 'utf8'));
  } catch {
    fullTestResult.vitestReport = undefined;
  }
  await rm(reportRoot, { recursive: true, force: true });
  fullTestResult.stdoutLog = path.join(LOG_ROOT, 'full_test.stdout.log');
  fullTestResult.stderrLog = path.join(LOG_ROOT, 'full_test.stderr.log');
  await writeCommandLogs(fullTestResult);
  rawCommands.push(fullTestResult);
  rawCommands.push(await runCommand({ id: 'typecheck', args: ['run', 'typecheck'] }));
  const section9Result = await runModuleCommand({
    id: 'section9',
    command: 'in-process validate-harness-section9.mjs (reuse full_test)',
    executionMode: 'in_process_reuse',
    execute: ({ log, logError }) => runSection9([], {
      cwd: process.cwd(),
      log,
      logError,
      reuseFullTestResult: fullTestResult
    })
  });
  rawCommands.push(section9Result);

  if (options.skipPremergeReason) {
    rawCommands.push(skippedResult('premerge', options.skipPremergeReason));
  } else {
    rawCommands.push(await runModuleCommand({
      id: 'premerge',
      command: 'in-process validate-harness-premerge.mjs (reuse section9)',
      executionMode: 'in_process_reuse',
      execute: ({ log, logError, writeStdout, writeStderr }) => runPremerge([], {
        cwd: process.cwd(),
        log,
        logError,
        echoChildOutput: true,
        writeChildStdout: writeStdout,
        writeChildStderr: writeStderr,
        completedSection9Result: {
          code: section9Result.exitCode,
          stdout: section9Result.stdout,
          stderr: section9Result.stderr
        }
      })
    }));
  }

  const commandResults = [];
  for (const result of rawCommands) {
    if (result.status === 'skipped') {
      commandResults.push(result);
      continue;
    }
    commandResults.push(await writeCommandLogs(result));
  }

  const summaryConsistency = await validateSummaries({
    premergeSkipped: Boolean(options.skipPremergeReason)
  });
  const failedCommands = commandResults.filter((result) => result.status === 'fail');
  const skippedCommands = commandResults.filter((result) => result.status === 'skipped');
  const failedConsistency = summaryConsistency.status === 'fail';
  const status =
    failedCommands.length > 0 || failedConsistency
      ? 'fail'
      : skippedCommands.length > 0
        ? 'pass_with_skips'
        : 'pass';

  const summary = {
    generatedAt: nowIso(),
    profile: 'runtime-premerge-evidence',
    status,
    releaseClaim: false,
    section9Policy: {
      standaloneSection9IsBlockingForThisWrapper: true,
      premergeSection9IsReportOnly: true
    },
    commands: commandResults,
    summaryConsistency,
    artifacts: {
      releaseQualitySummary: SUMMARY_PATH,
      section8Summary: SECTION8_SUMMARY_PATH,
      section9Summary: SECTION9_SUMMARY_PATH,
      section9Manifest: SECTION9_MANIFEST_PATH
    },
    boundaries: [
      'No release publication authorization.',
      'No lifecycle issuance.',
      'No professional approval.',
      'No certification, sealing, authentication, notarization, code-compliance acceptance, or release-readiness claim.'
    ]
  };

  await writeFile(SUMMARY_PATH, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

  console.log(`RELEASE_QUALITY_SUMMARY_PATH=${SUMMARY_PATH}`);
  console.log(`RELEASE_QUALITY_STATUS=${status}`);
  console.log(`RELEASE_QUALITY_PREMERGE_SKIPPED=${options.skipPremergeReason ? 'true' : 'false'}`);
  console.log(`RELEASE_QUALITY_SECTION9_POLICY=standalone-blocking,premerge-report-only`);

  process.exitCode = status === 'fail' ? 1 : 0;
}

main().catch((error) => {
  const message = error instanceof Error ? error.message : String(error);
  console.error(`Release-quality evidence validation failed: ${message}`);
  process.exitCode = 1;
});
