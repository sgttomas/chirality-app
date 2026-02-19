#!/usr/bin/env node

import { access, copyFile, mkdir, readFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const SCRIPT_PATH = fileURLToPath(import.meta.url);
const SCRIPT_DIR = path.dirname(SCRIPT_PATH);
const FRONTEND_ROOT = path.resolve(SCRIPT_DIR, "..");
const CANONICAL_SECTION8_SCRIPT = path.join(SCRIPT_DIR, "validate-harness-section8.mjs");

const SOURCE_ARTIFACT_ROOT =
  process.env.HARNESS_VALIDATION_ARTIFACT_ROOT ?? path.join(os.tmpdir(), "chirality-harness-validation");
const DEFAULT_SOURCE_SUMMARY_PATH = path.join(SOURCE_ARTIFACT_ROOT, "latest", "summary.json");

const PUBLISHED_ARTIFACT_DIR =
  process.env.HARNESS_PREMERGE_ARTIFACT_DIR ??
  path.join(FRONTEND_ROOT, "artifacts", "harness", "section8", "latest");
const PUBLISHED_SUMMARY_PATH = path.join(PUBLISHED_ARTIFACT_DIR, "summary.json");

const REQUIRED_SDK_TEST_IDS = [
  "setup.server_reachable",
  "regression.session_crud",
  "section8.session_boot_endpoint",
  "section8.boot_fingerprint_drift",
  "section8.smoke_stream",
  "section8.session_persistence_resume",
  "section8.subagents_off_parity",
  "section8.permissions_dontask",
  "section8.interrupt_sigint",
  "section8.sdk_native_stream",
];

function createLineCollector(onLine) {
  let buffer = "";

  return (chunk) => {
    buffer += chunk.toString("utf8");

    let newlineIndex = buffer.indexOf("\n");
    while (newlineIndex >= 0) {
      const line = buffer.slice(0, newlineIndex).trim();
      buffer = buffer.slice(newlineIndex + 1);
      onLine(line);
      newlineIndex = buffer.indexOf("\n");
    }
  };
}

async function fileExists(filePath) {
  try {
    await access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function runCanonicalValidation() {
  const child = spawn(process.execPath, [CANONICAL_SECTION8_SCRIPT], {
    cwd: FRONTEND_ROOT,
    env: process.env,
    stdio: ["ignore", "pipe", "pipe"],
  });

  let summaryPath = "";
  let status = "";

  const parseLine = (line) => {
    if (line.startsWith("HARNESS_VALIDATION_SUMMARY_PATH=")) {
      summaryPath = line.slice("HARNESS_VALIDATION_SUMMARY_PATH=".length).trim();
    }

    if (line.startsWith("HARNESS_VALIDATION_STATUS=")) {
      status = line.slice("HARNESS_VALIDATION_STATUS=".length).trim();
    }
  };

  const collectStdout = createLineCollector(parseLine);
  const collectStderr = createLineCollector(parseLine);

  child.stdout?.on("data", (chunk) => {
    process.stdout.write(chunk);
    collectStdout(chunk);
  });

  child.stderr?.on("data", (chunk) => {
    process.stderr.write(chunk);
    collectStderr(chunk);
  });

  const closeInfo = await new Promise((resolve, reject) => {
    child.once("error", (error) => reject(error));
    child.once("close", (code, signal) => resolve({ code, signal }));
  });

  return {
    code: closeInfo.code,
    signal: closeInfo.signal,
    summaryPath: summaryPath || DEFAULT_SOURCE_SUMMARY_PATH,
    status,
  };
}

async function publishSummary(sourceSummaryPath) {
  await mkdir(PUBLISHED_ARTIFACT_DIR, { recursive: true });
  await copyFile(sourceSummaryPath, PUBLISHED_SUMMARY_PATH);
}

async function readSummary(summaryPath) {
  const raw = await readFile(summaryPath, "utf8");
  return JSON.parse(raw);
}

function assertSdkSummaryShape(summary) {
  if (!summary || typeof summary !== "object") {
    throw new Error("Section 8 summary must be a JSON object.");
  }

  if (!Array.isArray(summary.tests)) {
    throw new Error("Section 8 summary is missing tests array.");
  }

  const observed = new Set(
    summary.tests
      .map((test) => (test && typeof test.id === "string" ? test.id : null))
      .filter((id) => typeof id === "string"),
  );

  const missing = REQUIRED_SDK_TEST_IDS.filter((id) => !observed.has(id));
  if (missing.length > 0) {
    throw new Error(`Section 8 summary missing required SDK test IDs: ${missing.join(", ")}`);
  }

  if (observed.has("regression.api_chat_reachability")) {
    throw new Error("Legacy /api/chat regression test is still present in Section 8 summary.");
  }
}

async function main() {
  const result = await runCanonicalValidation();
  const sourceSummaryPath = result.summaryPath;
  const summaryExists = await fileExists(sourceSummaryPath);

  if (!summaryExists) {
    console.error(`Missing Section 8 summary artifact: ${sourceSummaryPath}`);
    process.exitCode = result.code ?? 1;
    if (process.exitCode === 0) {
      process.exitCode = 1;
    }
    return;
  }

  let parsedSummary;
  try {
    parsedSummary = await readSummary(sourceSummaryPath);
    assertSdkSummaryShape(parsedSummary);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(`Invalid Section 8 SDK summary: ${message}`);
    process.exitCode = result.code ?? 1;
    if (process.exitCode === 0) {
      process.exitCode = 1;
    }
    return;
  }

  try {
    await publishSummary(sourceSummaryPath);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    console.error(`Failed to publish stable summary artifact: ${message}`);
    process.exitCode = result.code ?? 1;
    if (process.exitCode === 0) {
      process.exitCode = 1;
    }
    return;
  }

  console.log(`HARNESS_PREMERGE_ARTIFACT_PATH=${PUBLISHED_SUMMARY_PATH}`);
  console.log(`HARNESS_PREMERGE_SOURCE_SUMMARY_PATH=${sourceSummaryPath}`);
  console.log(`HARNESS_PREMERGE_TEST_COUNT=${Array.isArray(parsedSummary?.tests) ? parsedSummary.tests.length : 0}`);
  if (result.status) {
    console.log(`HARNESS_PREMERGE_STATUS=${result.status}`);
  }

  if (result.signal && (result.code === null || typeof result.code === "undefined")) {
    process.exitCode = 1;
    return;
  }

  process.exitCode = result.code ?? 0;
}

main().catch((error) => {
  const message = error instanceof Error ? error.stack ?? error.message : String(error);
  console.error(message);
  process.exit(1);
});
