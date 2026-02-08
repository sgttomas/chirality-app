#!/usr/bin/env node

import { access, copyFile, mkdir } from "node:fs/promises";
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
