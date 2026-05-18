import { appendFile, mkdir, rename, rm, stat } from "node:fs/promises";
import path from "node:path";

import {
  LOG_DIR_RELATIVE,
  LOG_FILE_NAME,
  LOG_ROTATED_FILE_NAME,
  LOG_ROTATE_BYTES,
} from "./defaults";
import { isSensitiveKey, redactForLogs, redactSecretsInText } from "./env-filter";
import type { LogEntry } from "./types";

function getLogPaths(projectRoot: string): { dir: string; file: string; rotated: string } {
  const dir = path.join(projectRoot, LOG_DIR_RELATIVE);
  return {
    dir,
    file: path.join(dir, LOG_FILE_NAME),
    rotated: path.join(dir, LOG_ROTATED_FILE_NAME),
  };
}

function sanitizeValue(value: unknown, keyHint?: string): unknown {
  if (typeof value === "string") {
    if (keyHint && isSensitiveKey(keyHint)) {
      return redactForLogs(value);
    }
    return redactSecretsInText(value);
  }

  if (Array.isArray(value)) {
    return value.map((item) => sanitizeValue(item, keyHint));
  }

  if (value && typeof value === "object") {
    const obj = value as Record<string, unknown>;
    const sanitized: Record<string, unknown> = {};

    for (const [key, nested] of Object.entries(obj)) {
      if (isSensitiveKey(key)) {
        sanitized[key] = typeof nested === "string" ? redactForLogs(nested) : "[REDACTED]";
      } else {
        sanitized[key] = sanitizeValue(nested, key);
      }
    }

    return sanitized;
  }

  return value;
}

function sanitizeEntry(entry: LogEntry): LogEntry {
  return {
    ...entry,
    data: entry.data ? (sanitizeValue(entry.data) as Record<string, unknown>) : undefined,
  };
}

export async function rotateIfNeeded(projectRoot: string): Promise<void> {
  const { file, rotated } = getLogPaths(projectRoot);

  let logStat;
  try {
    logStat = await stat(file);
  } catch {
    return;
  }

  if (logStat.size < LOG_ROTATE_BYTES) {
    return;
  }

  await rm(rotated, { force: true });
  await rename(file, rotated);
}

export async function appendLog(projectRoot: string, entry: LogEntry): Promise<void> {
  const { dir, file } = getLogPaths(projectRoot);

  try {
    await mkdir(dir, { recursive: true });
    await rotateIfNeeded(projectRoot);
    const sanitized = sanitizeEntry(entry);
    await appendFile(file, `${JSON.stringify(sanitized)}\n`, "utf8");
  } catch (error) {
    const msg = error instanceof Error ? error.message : String(error);
    console.warn(`[harness:logger] failed to append log: ${msg}`);
  }
}
