#!/usr/bin/env node

import { access, copyFile, mkdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import { constants as fsConstants } from 'node:fs';

const scriptPath = fileURLToPath(import.meta.url);

const REQUIRED_TEST_IDS = [
  'setup.server_reachable',
  'regression.session_crud',
  'section8.boot_error_taxonomy',
  'section8.smoke_stream',
  'section8.session_persistence_resume',
  'section8.permissions_dontask',
  'section8.interrupt_sigint',
  'section8.sdk_native_stream'
];

const LEGACY_REMOVED_TEST_ID = 'regression.api_chat_reachability';

function parseMachineLine(stdout, key) {
  const match = stdout
    .split('\n')
    .map((line) => line.trim())
    .find((line) => line.startsWith(`${key}=`));

  if (!match) {
    throw new Error(`Missing machine-readable output '${key}'`);
  }

  return match.slice(`${key}=`.length);
}

async function ensureReadableFile(filePath) {
  await access(filePath, fsConstants.R_OK);
}

async function runNodeScript(
  scriptToRun,
  cwd,
  echoChildOutput,
  writeChildStdout = (text) => process.stdout.write(text),
  writeChildStderr = (text) => process.stderr.write(text)
) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [scriptToRun], {
      cwd,
      env: process.env,
      stdio: ['ignore', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (chunk) => {
      const text = chunk.toString();
      stdout += text;
      if (echoChildOutput) {
        writeChildStdout(text);
      }
    });

    child.stderr.on('data', (chunk) => {
      const text = chunk.toString();
      stderr += text;
      if (echoChildOutput) {
        writeChildStderr(text);
      }
    });

    child.on('error', reject);
    child.on('close', (code) => {
      resolve({
        code: code ?? 1,
        stdout,
        stderr
      });
    });
  });
}

function parseOptionalMachineLine(stdout, key, fallback = '') {
  try {
    return parseMachineLine(stdout, key);
  } catch {
    return fallback;
  }
}

/**
 * Runs the premerge validation. Returns the process exit code (0 pass,
 * 1 fail). `opts.cwd` overrides the working directory and `opts.log` /
 * `opts.logError` override the output writers so tests can call this
 * in-process instead of spawning node.
 */
export async function run(argv = process.argv.slice(2), opts = {}) {
  void argv;
  const cwd = opts.cwd ?? process.cwd();
  const log = opts.log ?? ((line) => console.log(line));
  const logError = opts.logError ?? ((line) => console.error(line));
  // CLI runs stream child validator output live; in-process callers that
  // supply their own writers keep the host process's stdio clean.
  const echoChildOutput = opts.echoChildOutput ?? (opts.log === undefined);

  try {
    return await runPremerge({
      cwd,
      log,
      logError,
      echoChildOutput,
      completedSection9Result: opts.completedSection9Result,
      writeChildStdout: opts.writeChildStdout,
      writeChildStderr: opts.writeChildStderr
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    logError(`Harness premerge validation failed: ${message}`);
    return 1;
  }
}

async function runPremerge({
  cwd,
  log,
  logError,
  echoChildOutput,
  completedSection9Result,
  writeChildStdout,
  writeChildStderr
}) {
  const section8ScriptPath = path.resolve(cwd, 'scripts', 'validate-harness-section8.mjs');
  const section9ScriptPath = path.resolve(cwd, 'scripts', 'validate-harness-section9.mjs');
  const stableArtifactPath = path.resolve(
    cwd,
    'artifacts',
    'harness',
    'section8',
    'latest',
    'summary.json'
  );
  const stableSection9ArtifactPath = path.resolve(
    cwd,
    'artifacts',
    'harness',
    'section9',
    'latest',
    'summary.json'
  );

  try {
    await ensureReadableFile(section8ScriptPath);
  } catch {
    logError('RUNTIME_SURFACE_MISSING: frontend/scripts/validate-harness-section8.mjs');
    log(`HARNESS_PREMERGE_ARTIFACT_PATH=${stableArtifactPath}`);
    log('HARNESS_PREMERGE_SOURCE_SUMMARY_PATH=');
    log('HARNESS_PREMERGE_STATUS=fail');
    log('HARNESS_PREMERGE_TEST_COUNT=0');
    return 1;
  }

  const section8Result = await runNodeScript(
    section8ScriptPath,
    cwd,
    echoChildOutput,
    writeChildStdout,
    writeChildStderr
  );
  if (section8Result.code !== 0) {
    const sourceSummaryPath = (() => {
      try {
        return parseMachineLine(section8Result.stdout, 'HARNESS_VALIDATION_SUMMARY_PATH');
      } catch {
        return '';
      }
    })();
    let testCount = 0;
    if (sourceSummaryPath) {
      try {
        await ensureReadableFile(sourceSummaryPath);
        await mkdir(path.dirname(stableArtifactPath), { recursive: true });
        // Preserve the validator's exact failure record before interpreting it.
        // CI can therefore publish the evidence even if its schema is malformed.
        await copyFile(sourceSummaryPath, stableArtifactPath);
        await ensureReadableFile(stableArtifactPath);
        const summary = JSON.parse(await readFile(sourceSummaryPath, 'utf8'));
        testCount = Array.isArray(summary.results) ? summary.results.length : 0;
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        logError(`Section8 failure summary could not be interpreted: ${message}`);
      }
    }
    log(`HARNESS_PREMERGE_ARTIFACT_PATH=${stableArtifactPath}`);
    log(`HARNESS_PREMERGE_SOURCE_SUMMARY_PATH=${sourceSummaryPath}`);
    log('HARNESS_PREMERGE_STATUS=fail');
    log(`HARNESS_PREMERGE_TEST_COUNT=${testCount}`);
    return 1;
  }

  const sourceSummaryPath = parseMachineLine(
    section8Result.stdout,
    'HARNESS_VALIDATION_SUMMARY_PATH'
  );
  const validationStatus = parseMachineLine(section8Result.stdout, 'HARNESS_VALIDATION_STATUS');
  if (validationStatus !== 'pass') {
    throw new Error(`Section8 validation status is '${validationStatus}', expected 'pass'`);
  }

  await ensureReadableFile(sourceSummaryPath);
  const summaryRaw = await readFile(sourceSummaryPath, 'utf8');
  const summary = JSON.parse(summaryRaw);
  const resultRows = Array.isArray(summary.results) ? summary.results : [];
  const seenIds = new Set(resultRows.map((result) => result.id));

  for (const requiredId of REQUIRED_TEST_IDS) {
    if (!seenIds.has(requiredId)) {
      throw new Error(`Summary missing required test id '${requiredId}'`);
    }
  }

  if (seenIds.has(LEGACY_REMOVED_TEST_ID)) {
    throw new Error(`Summary includes legacy test id '${LEGACY_REMOVED_TEST_ID}'`);
  }

  await mkdir(path.dirname(stableArtifactPath), { recursive: true });
  await copyFile(sourceSummaryPath, stableArtifactPath);
  await ensureReadableFile(stableArtifactPath);

  const premergeStatus = resultRows.every((result) => result.status === 'pass') ? 'pass' : 'fail';
  const testCount = resultRows.length;

  let section9Status = 'fail';
  let section9SourceSummaryPath = '';
  let section9TestCount = '0';
  try {
    const section9Result = completedSection9Result ?? await (async () => {
      await ensureReadableFile(section9ScriptPath);
      return runNodeScript(
        section9ScriptPath,
        cwd,
        echoChildOutput,
        writeChildStdout,
        writeChildStderr
      );
    })();
    section9Status = parseOptionalMachineLine(
      section9Result.stdout,
      'HARNESS_SECTION9_STATUS',
      section9Result.code === 0 ? 'pass' : 'fail'
    );
    section9SourceSummaryPath = parseOptionalMachineLine(
      section9Result.stdout,
      'HARNESS_SECTION9_SOURCE_SUMMARY_PATH'
    );
    section9TestCount = parseOptionalMachineLine(
      section9Result.stdout,
      'HARNESS_SECTION9_TEST_COUNT',
      '0'
    );
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    logError(`Harness Section 9 report-only validation failed to run: ${message}`);
  }

  log(`HARNESS_PREMERGE_ARTIFACT_PATH=${stableArtifactPath}`);
  log(`HARNESS_PREMERGE_SOURCE_SUMMARY_PATH=${sourceSummaryPath}`);
  log(`HARNESS_PREMERGE_STATUS=${premergeStatus}`);
  log(`HARNESS_PREMERGE_TEST_COUNT=${testCount}`);
  log(`HARNESS_PREMERGE_SECTION9_ARTIFACT_PATH=${stableSection9ArtifactPath}`);
  log(`HARNESS_PREMERGE_SECTION9_SOURCE_SUMMARY_PATH=${section9SourceSummaryPath}`);
  log(`HARNESS_PREMERGE_SECTION9_STATUS=${section9Status}`);
  log(`HARNESS_PREMERGE_SECTION9_TEST_COUNT=${section9TestCount}`);
  log('HARNESS_PREMERGE_SECTION9_REPORT_ONLY=true');

  return premergeStatus === 'pass' ? 0 : 1;
}

if (process.argv[1] && path.resolve(process.argv[1]) === scriptPath) {
  process.exitCode = await run();
}
