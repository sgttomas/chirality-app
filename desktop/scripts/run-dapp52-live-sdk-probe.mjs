#!/usr/bin/env node
// D-APP-52 owner-at-screen live SDK probe (DEL-04-01 residuals).
// Captures, against the pinned dev-runtime @anthropic-ai/claude-agent-sdk:
//   phase 1 — exact observed live query() message sequence, session id,
//             subprocess version, transcript/config placement (CLM-018 3/4/8);
//   phase 2 — live SDK error object shapes: invalid-key API response error and
//             unreachable-base-url network error (DEP-04-01-013);
//   phase 3 — interrupt/abort terminal behavior (REQ-010).
// Key handling per D-APP-52 rider 2: --api-key-file only; the key reaches the
// SDK solely through its env option; every artifact is redacted and the output
// plus all controlled temp dirs are secret-scanned before the summary is final.

import { createHash, randomUUID } from 'node:crypto';
import { existsSync } from 'node:fs';
import { lstat, mkdir, mkdtemp, readFile, readdir, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const DEFAULT_MODEL = 'claude-sonnet-4-20250514';
const DEFAULT_TIMEOUT_MS = 180_000;
const MAX_SCAN_FILE_BYTES = 2 * 1024 * 1024;
const MAX_RAW_MESSAGE_CHARS = 20_000;
const READ_TARGET_NAME = 'probe-read-target.txt';

function nowIso() {
  return new Date().toISOString();
}

function sha256(value) {
  return createHash('sha256').update(value).digest('hex');
}

function parseArgs(argv) {
  const options = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    const next = () => {
      const value = argv[index + 1];
      if (!value || value.startsWith('--')) {
        throw new Error(`Missing value for ${token}`);
      }
      index += 1;
      return value;
    };
    if (token === '--api-key-file') options.apiKeyFile = next();
    else if (token === '--output-root') options.outputRoot = next();
    else if (token === '--model') options.model = next();
    else if (token === '--timeout-ms') options.timeoutMs = Number.parseInt(next(), 10);
    else throw new Error(`Unknown argument: ${token}`);
  }
  return options;
}

async function readApiKey(args) {
  if (!args.apiKeyFile) {
    throw new Error('Live probe requires --api-key-file <path> (rider 2: env-file only).');
  }
  const apiKeyFile = path.resolve(args.apiKeyFile);
  const raw = await readFile(apiKeyFile, 'utf8');
  const match = raw.match(/ANTHROPIC_API_KEY=(\S+)/);
  const apiKey = (match ? match[1] : raw).trim();
  if (!apiKey) throw new Error(`API key file is empty: ${apiKeyFile}`);
  return { apiKey, sourcePath: apiKeyFile };
}

function redactString(value, secrets) {
  let redacted = value;
  for (const secret of secrets) {
    if (secret) redacted = redacted.split(secret).join('[REDACTED_API_KEY]');
  }
  return redacted;
}

function collectToolNames(value, found = new Set()) {
  if (!value || typeof value !== 'object') return found;
  if (
    (value.type === 'tool_use' || value.type === 'server_tool_use' || value.type === 'tool_use_summary') &&
    typeof value.name === 'string'
  ) {
    found.add(value.name);
  }
  if (typeof value.tool_name === 'string') found.add(value.tool_name);
  const items = Array.isArray(value) ? value : Object.values(value);
  for (const item of items) collectToolNames(item, found);
  return found;
}

function contentBlockTypes(message) {
  const blocks = message?.message?.content;
  if (!Array.isArray(blocks)) return undefined;
  return blocks.map((block) => (block && typeof block.type === 'string' ? block.type : typeof block));
}

function summarizeMessage(message, index, secrets) {
  const rawRedacted = redactString(JSON.stringify(message ?? null), secrets);
  const base = {
    index,
    type: typeof message?.type === 'string' ? message.type : typeof message,
    subtype: typeof message?.subtype === 'string' ? message.subtype : undefined,
    session_id: typeof message?.session_id === 'string' ? message.session_id : undefined,
    uuid: typeof message?.uuid === 'string' ? message.uuid : undefined,
    parent_tool_use_id: message?.parent_tool_use_id ?? undefined,
    is_error: typeof message?.is_error === 'boolean' ? message.is_error : undefined,
    stop_reason: message?.message?.stop_reason ?? undefined,
    contentBlockTypes: contentBlockTypes(message),
    toolNames: [...collectToolNames(message)].sort(),
    topLevelKeys: message && typeof message === 'object' ? Object.keys(message).sort() : undefined,
    rawSizeBytes: Buffer.byteLength(rawRedacted),
    rawRedacted:
      rawRedacted.length > MAX_RAW_MESSAGE_CHARS
        ? `${rawRedacted.slice(0, MAX_RAW_MESSAGE_CHARS)}…[truncated]`
        : rawRedacted
  };
  return base;
}

async function listFilesRecursive(rootPath) {
  const root = path.resolve(rootPath);
  const entries = [];
  async function visit(currentPath) {
    let currentStat;
    try {
      currentStat = await lstat(currentPath);
    } catch {
      return;
    }
    if (currentStat.isSymbolicLink()) return;
    if (currentStat.isDirectory()) {
      for (const entry of await readdir(currentPath)) {
        await visit(path.join(currentPath, entry));
      }
      return;
    }
    if (currentStat.isFile()) {
      entries.push({ path: path.relative(root, currentPath), sizeBytes: currentStat.size });
    }
  }
  if (existsSync(root)) await visit(root);
  return entries.sort((a, b) => a.path.localeCompare(b.path));
}

async function scanPathForSecret(rootPath, secret, label) {
  const findings = [];
  const skipped = [];
  const root = path.resolve(rootPath);
  async function visit(currentPath) {
    let currentStat;
    try {
      currentStat = await lstat(currentPath);
    } catch {
      return;
    }
    if (currentStat.isSymbolicLink()) return;
    if (currentStat.isDirectory()) {
      for (const entry of await readdir(currentPath)) {
        await visit(path.join(currentPath, entry));
      }
      return;
    }
    if (!currentStat.isFile()) return;
    if (currentStat.size > MAX_SCAN_FILE_BYTES) {
      skipped.push({ path: currentPath, sizeBytes: currentStat.size });
      return;
    }
    const raw = await readFile(currentPath, 'utf8').catch(() => null);
    if (raw !== null && raw.includes(secret)) {
      findings.push({ scope: label, path: currentPath, sizeBytes: currentStat.size });
    }
  }
  if (existsSync(root)) await visit(root);
  return { root, findings, skipped };
}

async function runQueryPhase({ name, sdkModule, prompt, options, secrets, timeoutMs, abortAfterMessages }) {
  const abortController = new AbortController();
  const messages = [];
  const failures = [];
  let caughtError = null;
  const startedAt = nowIso();
  const timeout = setTimeout(() => {
    abortController.abort(new Error(`phase ${name} exceeded timeout ${timeoutMs}ms`));
  }, timeoutMs);
  try {
    const stream = sdkModule.query({ prompt, options: { ...options, abortController } });
    for await (const message of stream) {
      messages.push(summarizeMessage(message, messages.length, secrets));
      if (abortAfterMessages !== undefined && messages.length >= abortAfterMessages) {
        abortController.abort(new Error('probe-initiated interrupt (REQ-010 evidence)'));
      }
    }
  } catch (error) {
    caughtError = {
      name: error?.name,
      constructorName: error?.constructor?.name,
      messageRedacted: redactString(error instanceof Error ? error.message : String(error), secrets),
      ownKeys: error && typeof error === 'object' ? Object.getOwnPropertyNames(error).sort() : undefined,
      stackPresent: Boolean(error?.stack)
    };
  } finally {
    clearTimeout(timeout);
  }
  return { name, startedAt, finishedAt: nowIso(), messages, caughtError, failures };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const { apiKey, sourcePath } = await readApiKey(args);
  const secrets = [apiKey];
  const model = args.model ?? DEFAULT_MODEL;
  const timeoutMs = args.timeoutMs ?? DEFAULT_TIMEOUT_MS;
  const outputRoot = path.resolve(
    args.outputRoot ?? path.join(process.cwd(), 'artifacts', 'harness', 'dapp52-live-sdk-probe', 'latest')
  );
  const tempRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-dapp52-live-sdk-probe-'));
  const projectRoot = path.join(tempRoot, 'project-root');
  const configDir = path.join(tempRoot, 'claude-config');
  const homeDir = path.join(tempRoot, 'home');
  await mkdir(outputRoot, { recursive: true });
  for (const dir of [projectRoot, configDir, homeDir]) await mkdir(dir, { recursive: true });

  const sdkPackageRoot = path.join(process.cwd(), 'node_modules', '@anthropic-ai', 'claude-agent-sdk');
  const sdkPackage = JSON.parse(await readFile(path.join(sdkPackageRoot, 'package.json'), 'utf8'));
  const sdkModule = await import(pathToFileURL(path.join(sdkPackageRoot, 'sdk.mjs')).href);
  if (typeof sdkModule.query !== 'function') throw new Error('SDK module does not export query()');

  const proofToken = `dapp52-live-probe-${randomUUID()}`;
  await writeFile(
    path.join(projectRoot, READ_TARGET_NAME),
    `D-APP-52 live probe read target (synthetic).\nPROOF_TOKEN=${proofToken}\n`,
    'utf8'
  );

  const baseEnv = { CLAUDE_CONFIG_DIR: configDir, HOME: homeDir };
  const baseOptions = {
    cwd: projectRoot,
    model,
    maxTurns: 3,
    permissionMode: 'dontAsk',
    allowedTools: ['Read'],
    disallowedTools: ['Bash', 'Write', 'Edit', 'MultiEdit', 'NotebookEdit', 'WebFetch', 'WebSearch', 'Agent', 'Task'],
    settingSources: []
  };
  const readPrompt = [
    `Use the Read tool exactly once to read ./${READ_TARGET_NAME}.`,
    'Report only the exact PROOF_TOKEN value from that file.',
    'Do not use Bash, Write, Edit, web tools, MCP tools, plugins, or subagents.'
  ].join(' ');

  // Phase 1 — live message sequence with the real key.
  const phase1 = await runQueryPhase({
    name: 'live-message-sequence',
    sdkModule,
    prompt: readPrompt,
    options: { ...baseOptions, env: { ...baseEnv, ANTHROPIC_API_KEY: apiKey } },
    secrets,
    timeoutMs
  });

  // Transcript/config placement evidence after the live turn (CLM-018 step 8).
  const placement = {
    configDirFiles: await listFilesRecursive(configDir),
    homeDirFiles: await listFilesRecursive(homeDir),
    projectRootFiles: await listFilesRecursive(projectRoot)
  };

  // Phase 2a — invalid-key API response error shape. The token is synthetic
  // (never a real credential); "fake" marks it as an allowed fixture for the
  // repo secret scanner's committed-source gate.
  const syntheticBadKey = `sk-ant-api03-fake-invalid-${randomUUID()}`;
  const phase2a = await runQueryPhase({
    name: 'error-shape-invalid-key',
    sdkModule,
    prompt: 'Reply with the single word ok.',
    options: { ...baseOptions, maxTurns: 1, env: { ...baseEnv, ANTHROPIC_API_KEY: syntheticBadKey } },
    secrets,
    timeoutMs
  });

  // Phase 2b — network error shape: unreachable loopback base URL, real key
  // never leaves the process env and never reaches any live endpoint.
  const phase2b = await runQueryPhase({
    name: 'error-shape-network-unreachable',
    sdkModule,
    prompt: 'Reply with the single word ok.',
    options: {
      ...baseOptions,
      maxTurns: 1,
      env: { ...baseEnv, ANTHROPIC_API_KEY: apiKey, ANTHROPIC_BASE_URL: 'http://127.0.0.1:9' }
    },
    secrets,
    timeoutMs: 60_000
  });

  // Phase 3 — interrupt terminal behavior (abort after first message).
  const phase3 = await runQueryPhase({
    name: 'interrupt-terminal-behavior',
    sdkModule,
    prompt: readPrompt,
    options: { ...baseOptions, env: { ...baseEnv, ANTHROPIC_API_KEY: apiKey } },
    secrets,
    timeoutMs,
    abortAfterMessages: 1
  });

  const phases = [phase1, phase2a, phase2b, phase3];
  const failures = [];
  const phase1Result = phase1.messages.find((m) => m.type === 'result');
  if (!phase1.messages.some((m) => m.toolNames.includes('Read'))) {
    failures.push('phase 1: SDK stream did not report a Read tool use.');
  }
  if (!phase1.messages.some((m) => m.rawRedacted.includes(proofToken))) {
    failures.push('phase 1: SDK stream did not report the proof token.');
  }
  if (!phase1Result || phase1Result.is_error) {
    failures.push('phase 1: no successful terminal result message.');
  }

  const summaryPath = path.join(outputRoot, 'summary.json');
  const baseSummary = {
    generatedAt: nowIso(),
    status: 'pending-redaction-scan',
    probeMode: 'dapp52-live-dev-sdk-probe',
    authority:
      'D-APP-52 ruling O-A (riders 1-11), live-LLM demonstration owner act 2026-07-18 (owner at screen, short-lived owner-supplied key)',
    sdkPackage: {
      root: sdkPackageRoot,
      name: sdkPackage.name ?? null,
      version: sdkPackage.version ?? null,
      claudeCodeVersion: sdkPackage.claudeCodeVersion ?? null
    },
    runtime: {
      node: process.version,
      platform: `${process.platform}:${process.arch}`
    },
    apiKey: { source: 'api-key-file', sourcePathHash: sha256(sourcePath), redacted: true },
    environment: {
      projectRootHash: sha256(projectRoot),
      claudeConfigDirHash: sha256(configDir),
      homeDirHash: sha256(homeDir),
      policy:
        'CLAUDE_CONFIG_DIR and HOME are controlled temp probe paths; the key is supplied only through the SDK env option; temp roots are secret-scanned and then left to OS tmp cleanup.'
    },
    liveRun: { model, baseOptions: { ...baseOptions }, promptHash: sha256(readPrompt), proofTokenHash: sha256(proofToken) },
    phases,
    placement,
    failures
  };
  await writeFile(summaryPath, `${JSON.stringify(baseSummary, null, 2)}\n`, 'utf8');

  const redactionResults = [];
  for (const target of [
    { label: 'probe-output', path: outputRoot },
    { label: 'probe-project-root', path: projectRoot },
    { label: 'probe-claude-config-dir', path: configDir },
    { label: 'probe-home-dir', path: homeDir }
  ]) {
    redactionResults.push(await scanPathForSecret(target.path, apiKey, target.label));
  }
  const redactionFindings = redactionResults.flatMap((result) => result.findings);
  if (redactionFindings.length > 0) {
    failures.push('API key string was found in probe artifacts or controlled temp directories.');
  }

  const status = failures.length === 0 ? 'pass' : 'fail';
  const summary = {
    ...baseSummary,
    generatedAt: nowIso(),
    status,
    redaction: {
      passed: redactionFindings.length === 0,
      findings: redactionFindings.map((f) => ({ scope: f.scope, sizeBytes: f.sizeBytes })),
      scannedRoots: redactionResults.length
    }
  };
  await writeFile(summaryPath, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

  console.log(`dapp52 live sdk probe status: ${status}`);
  console.log(`summary: ${summaryPath}`);
  console.log(`phase message counts: ${phases.map((p) => `${p.name}=${p.messages.length}`).join(', ')}`);
  if (status !== 'pass') {
    for (const failure of failures) console.error(`- ${redactString(failure, secrets)}`);
    process.exitCode = 1;
  }
}

main().catch((error) => {
  console.error(`dapp52 live sdk probe failed: ${error instanceof Error ? error.message : String(error)}`);
  process.exitCode = 1;
});
