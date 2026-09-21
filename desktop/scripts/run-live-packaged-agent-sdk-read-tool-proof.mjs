#!/usr/bin/env node

import { createHash, randomUUID } from 'node:crypto';
import { existsSync } from 'node:fs';
import { lstat, mkdir, mkdtemp, readFile, readdir, realpath, stat, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const scriptPath = fileURLToPath(import.meta.url);

const SDK_PLATFORM_PACKAGE_BY_RUNTIME = new Map([
  ['darwin:arm64', '@anthropic-ai/claude-agent-sdk-darwin-arm64'],
  ['darwin:x64', '@anthropic-ai/claude-agent-sdk-darwin-x64'],
  ['linux:arm64', '@anthropic-ai/claude-agent-sdk-linux-arm64'],
  ['linux:x64', '@anthropic-ai/claude-agent-sdk-linux-x64'],
  ['win32:arm64', '@anthropic-ai/claude-agent-sdk-win32-arm64'],
  ['win32:x64', '@anthropic-ai/claude-agent-sdk-win32-x64']
]);

const DEFAULT_MODEL = 'claude-sonnet-4-20250514';
const DEFAULT_TIMEOUT_MS = 180_000;
const MAX_SCAN_FILE_BYTES = 2 * 1024 * 1024;
const READ_TARGET_NAME = 'proof-read-target.txt';

function nowIso() {
  return new Date().toISOString();
}

function printUsage(log) {
  log(`Usage: node ./scripts/run-live-packaged-agent-sdk-read-tool-proof.mjs [options]

Options:
  --bundle-root <path>       Packaged Resources root (default: dist/mac-arm64/Chirality.app/Contents/Resources)
  --output-root <path>       Output directory for summary.json (default: artifacts/harness/packaged-agent-sdk-live/latest)
  --api-key-file <path>      File containing the live ANTHROPIC_API_KEY or CHIRALITY_ANTHROPIC_API_KEY value
  --allow-env-api-key        Permit reading CHIRALITY_ANTHROPIC_API_KEY or ANTHROPIC_API_KEY from the process env
  --project-root <path>      Project root passed to the SDK cwd (default: temp proof project)
  --config-dir <path>        CLAUDE_CONFIG_DIR passed to the SDK subprocess (default: temp proof config)
  --home-dir <path>          HOME passed to the SDK subprocess (default: temp proof home)
  --model <name>             Model for the live proof (default: ${DEFAULT_MODEL})
  --max-turns <number>       SDK maxTurns for the proof (default: 3)
  --timeout-ms <number>      Abort timeout for the proof (default: ${DEFAULT_TIMEOUT_MS})
  --help                     Show this message
`);
}

function readArgValue(argv, index, flagName) {
  const value = argv[index];
  if (!value || value.startsWith('--')) {
    throw new Error(`Missing value for ${flagName}`);
  }
  return value;
}

function parsePositiveInteger(raw, flagName) {
  const parsed = Number.parseInt(raw, 10);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    throw new Error(`${flagName} must be a positive integer.`);
  }
  return parsed;
}

function parseArgs(argv) {
  const options = {};

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];

    if (token === '--help') {
      options.help = true;
      continue;
    }

    if (token === '--bundle-root') {
      options.bundleRoot = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    if (token === '--output-root') {
      options.outputRoot = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    if (token === '--api-key-file') {
      options.apiKeyFile = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    if (token === '--allow-env-api-key') {
      options.allowEnvApiKey = true;
      continue;
    }

    if (token === '--project-root') {
      options.projectRoot = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    if (token === '--config-dir') {
      options.configDir = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    if (token === '--home-dir') {
      options.homeDir = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    if (token === '--model') {
      options.model = readArgValue(argv, index + 1, token);
      index += 1;
      continue;
    }

    if (token === '--max-turns') {
      options.maxTurns = parsePositiveInteger(readArgValue(argv, index + 1, token), token);
      index += 1;
      continue;
    }

    if (token === '--timeout-ms') {
      options.timeoutMs = parsePositiveInteger(readArgValue(argv, index + 1, token), token);
      index += 1;
      continue;
    }

    throw new Error(`Unknown argument: ${token}`);
  }

  return options;
}

function sha256(value) {
  return createHash('sha256').update(value).digest('hex');
}

function toPosix(filePath) {
  return filePath.split(path.sep).join('/');
}

function isPathWithin(childPath, parentPath) {
  const relative = path.relative(parentPath, childPath);
  return relative === '' || (!relative.startsWith('..') && !path.isAbsolute(relative));
}

function resolvePlatformPackageName() {
  return SDK_PLATFORM_PACKAGE_BY_RUNTIME.get(`${process.platform}:${process.arch}`) ?? null;
}

async function readPackageJson(packageRoot) {
  const raw = await readFile(path.join(packageRoot, 'package.json'), 'utf8');
  return JSON.parse(raw);
}

async function readApiKey(args) {
  if (args.apiKeyFile) {
    const apiKeyFile = path.resolve(args.apiKeyFile);
    const apiKey = (await readFile(apiKeyFile, 'utf8')).trim();
    if (!apiKey) {
      throw new Error(`API key file is empty: ${apiKeyFile}`);
    }
    return {
      apiKey,
      source: 'api-key-file',
      sourcePath: apiKeyFile
    };
  }

  if (args.allowEnvApiKey) {
    const apiKey = (process.env.CHIRALITY_ANTHROPIC_API_KEY ?? process.env.ANTHROPIC_API_KEY ?? '').trim();
    if (!apiKey) {
      throw new Error(
        '--allow-env-api-key was set, but neither CHIRALITY_ANTHROPIC_API_KEY nor ANTHROPIC_API_KEY is populated.'
      );
    }
    return {
      apiKey,
      source: process.env.CHIRALITY_ANTHROPIC_API_KEY ? 'CHIRALITY_ANTHROPIC_API_KEY' : 'ANTHROPIC_API_KEY',
      sourcePath: null
    };
  }

  throw new Error('Live proof requires --api-key-file <path> or explicit --allow-env-api-key.');
}

function redactString(value, secrets) {
  let redacted = value;
  for (const secret of secrets) {
    if (secret) {
      redacted = redacted.split(secret).join('[REDACTED_API_KEY]');
    }
  }
  return redacted;
}

function collectToolNames(value, found = new Set()) {
  if (!value || typeof value !== 'object') {
    return found;
  }

  if (
    (value.type === 'tool_use' || value.type === 'server_tool_use' || value.type === 'tool_use_summary') &&
    typeof value.name === 'string'
  ) {
    found.add(value.name);
  }

  if (typeof value.tool_name === 'string') {
    found.add(value.tool_name);
  }

  if (Array.isArray(value)) {
    for (const item of value) {
      collectToolNames(item, found);
    }
    return found;
  }

  for (const item of Object.values(value)) {
    collectToolNames(item, found);
  }

  return found;
}

function summarizeSdkMessage(message, proofToken, secrets) {
  const raw = redactString(JSON.stringify(message ?? null), secrets);
  const toolNames = [...collectToolNames(message)].sort();

  if (!message || typeof message !== 'object') {
    return {
      type: typeof message,
      rawSizeBytes: Buffer.byteLength(raw),
      toolNames,
      containsProofToken: raw.includes(proofToken)
    };
  }

  return {
    type: typeof message.type === 'string' ? message.type : 'unknown',
    subtype: typeof message.subtype === 'string' ? message.subtype : undefined,
    session_id: typeof message.session_id === 'string' ? message.session_id : undefined,
    uuid: typeof message.uuid === 'string' ? message.uuid : undefined,
    is_error: typeof message.is_error === 'boolean' ? message.is_error : undefined,
    toolNames,
    containsProofToken: raw.includes(proofToken),
    rawSizeBytes: Buffer.byteLength(raw)
  };
}

async function inspectExpectedCommand(sdkPackageRoot, unpackedNodeModulesRoot) {
  const platformPackageName = resolvePlatformPackageName();
  const binaryName = process.platform === 'win32' ? 'claude.exe' : 'claude';
  const expectedCommand = platformPackageName
    ? path.join(sdkPackageRoot, 'node_modules', platformPackageName, binaryName)
    : null;

  if (!expectedCommand) {
    return {
      platformPackageName,
      command: null,
      commandRealpath: null,
      exists: false,
      isFile: false,
      executableBitSet: false,
      commandUnderUnpackedNodeModules: false
    };
  }

  const absoluteCommand = path.resolve(expectedCommand);
  let commandRealpath = absoluteCommand;
  let exists = false;
  let isFile = false;
  let mode = null;
  let sizeBytes = null;

  try {
    const commandStat = await stat(absoluteCommand);
    exists = true;
    isFile = commandStat.isFile();
    mode = commandStat.mode;
    sizeBytes = commandStat.size;
    commandRealpath = await realpath(absoluteCommand);
  } catch {
    commandRealpath = absoluteCommand;
  }

  const unpackedRootRealpath = existsSync(unpackedNodeModulesRoot)
    ? await realpath(unpackedNodeModulesRoot)
    : path.resolve(unpackedNodeModulesRoot);

  return {
    platformPackageName,
    command: absoluteCommand,
    commandRealpath,
    exists,
    isFile,
    executableBitSet: typeof mode === 'number' ? (mode & 0o111) !== 0 : false,
    sizeBytes,
    unpackedNodeModulesRoot: unpackedRootRealpath,
    commandUnderUnpackedNodeModules: isPathWithin(commandRealpath, unpackedRootRealpath)
  };
}

async function writeJson(filePath, value) {
  await writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
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

    if (currentStat.isSymbolicLink()) {
      return;
    }

    if (currentStat.isDirectory()) {
      const entries = await readdir(currentPath, { withFileTypes: true });
      for (const entry of entries) {
        await visit(path.join(currentPath, entry.name));
      }
      return;
    }

    if (!currentStat.isFile()) {
      return;
    }

    if (currentStat.size > MAX_SCAN_FILE_BYTES) {
      skipped.push({
        path: currentPath,
        reason: `larger than ${MAX_SCAN_FILE_BYTES} bytes`,
        sizeBytes: currentStat.size
      });
      return;
    }

    const raw = await readFile(currentPath, 'utf8').catch(() => null);
    if (raw !== null && raw.includes(secret)) {
      findings.push({
        scope: label,
        path: currentPath,
        sizeBytes: currentStat.size
      });
    }
  }

  if (existsSync(root)) {
    await visit(root);
  }

  return {
    root,
    findings,
    skipped
  };
}

async function scanAllRedactionTargets(targets, secret) {
  const results = [];
  for (const target of targets) {
    results.push(await scanPathForSecret(target.path, secret, target.label));
  }

  const findings = results.flatMap((result) => result.findings);
  const skipped = results.flatMap((result) => result.skipped.map((item) => ({ ...item, scope: result.root })));
  return {
    passed: findings.length === 0,
    findings,
    skipped,
    scannedRoots: results.map((result) => result.root)
  };
}

function buildPrompt() {
  return [
    `Use the Read tool exactly once to read ./${READ_TARGET_NAME}.`,
    'Report only the exact PROOF_TOKEN value from that file.',
    'Do not use Bash, Write, Edit, web tools, MCP tools, plugins, or subagents.'
  ].join(' ');
}

async function runProof(args, { cwd, log, logError }) {
  const apiKeyInput = await readApiKey(args);
  const secrets = [apiKeyInput.apiKey];
  const bundleRoot = path.resolve(
    args.bundleRoot ?? path.join(cwd, 'dist', 'mac-arm64', 'Chirality.app', 'Contents', 'Resources')
  );
  const outputRoot = path.resolve(
    args.outputRoot ?? path.join(cwd, 'artifacts', 'harness', 'packaged-agent-sdk-live', 'latest')
  );
  const tempRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-live-packaged-agent-sdk-proof-'));
  const projectRoot = path.resolve(args.projectRoot ?? path.join(tempRoot, 'project-root'));
  const configDir = path.resolve(args.configDir ?? path.join(tempRoot, 'claude-config'));
  const homeDir = path.resolve(args.homeDir ?? path.join(tempRoot, 'home'));
  const model = args.model ?? process.env.CHIRALITY_LIVE_PACKAGED_AGENTSDK_MODEL ?? DEFAULT_MODEL;
  const maxTurns = args.maxTurns ?? 3;
  const timeoutMs = args.timeoutMs ?? DEFAULT_TIMEOUT_MS;
  const sdkPackageRoot = path.join(
    bundleRoot,
    'app.asar.unpacked',
    'node_modules',
    '@anthropic-ai',
    'claude-agent-sdk'
  );
  const sdkModulePath = path.join(sdkPackageRoot, 'sdk.mjs');
  const unpackedNodeModulesRoot = path.join(bundleRoot, 'app.asar.unpacked', 'node_modules');
  const proofToken = `chirality-live-packaged-read-proof-${randomUUID()}`;
  const proofTargetPath = path.join(projectRoot, READ_TARGET_NAME);
  const prompt = buildPrompt();
  const abortController = new AbortController();
  const failures = [];
  const messageSummaries = [];
  const startedAt = nowIso();

  await mkdir(outputRoot, { recursive: true });
  await mkdir(projectRoot, { recursive: true });
  await mkdir(configDir, { recursive: true });
  await mkdir(homeDir, { recursive: true });
  await writeFile(
    proofTargetPath,
    [
      'This file exists only for the D-APP-15 bounded live packaged agentSdk read-tool proof.',
      `PROOF_TOKEN=${proofToken}`,
      ''
    ].join('\n'),
    'utf8'
  );

  if (!existsSync(sdkModulePath)) {
    throw new Error(`Packaged SDK module not found: ${sdkModulePath}`);
  }

  const sdkPackage = await readPackageJson(sdkPackageRoot);
  const expectedCommand = await inspectExpectedCommand(sdkPackageRoot, unpackedNodeModulesRoot);
  if (!expectedCommand.exists || !expectedCommand.isFile) {
    failures.push(`Expected packaged SDK native command is not a file: ${expectedCommand.command ?? 'unresolved'}`);
  }
  if (!expectedCommand.commandUnderUnpackedNodeModules) {
    failures.push(
      `Expected packaged SDK native command is outside app.asar.unpacked/node_modules: ${
        expectedCommand.commandRealpath ?? 'unresolved'
      }`
    );
  }

  const sdkModule = await import(`${pathToFileURL(sdkModulePath).href}?liveProof=${Date.now()}`);
  if (typeof sdkModule.query !== 'function') {
    throw new Error(`Packaged SDK module does not export query(): ${sdkModulePath}`);
  }

  const timeout = setTimeout(() => {
    abortController.abort(new Error(`Live proof exceeded timeout ${timeoutMs}ms.`));
  }, timeoutMs);

  try {
    const stream = sdkModule.query({
      prompt,
      options: {
        abortController,
        cwd: projectRoot,
        model,
        maxTurns,
        permissionMode: 'dontAsk',
        tools: ['Read'],
        allowedTools: ['Read'],
        disallowedTools: [
          'Bash',
          'Write',
          'Edit',
          'MultiEdit',
          'NotebookEdit',
          'WebFetch',
          'WebSearch',
          'Agent',
          'Task'
        ],
        settingSources: [],
        env: {
          CLAUDE_CONFIG_DIR: configDir,
          HOME: homeDir,
          ANTHROPIC_API_KEY: apiKeyInput.apiKey
        }
      }
    });

    for await (const message of stream) {
      messageSummaries.push(summarizeSdkMessage(message, proofToken, secrets));
    }
  } catch (error) {
    failures.push(redactString(error instanceof Error ? error.message : String(error), secrets));
  } finally {
    clearTimeout(timeout);
  }

  const readToolObserved = messageSummaries.some((message) => message.toolNames.includes('Read'));
  const proofTokenObserved = messageSummaries.some((message) => message.containsProofToken);
  const sdkReportedError = messageSummaries.some((message) => message.is_error === true || message.subtype === 'error');

  if (!readToolObserved) {
    failures.push('SDK stream did not report a Read tool use.');
  }
  if (!proofTokenObserved) {
    failures.push('SDK stream did not report the proof token read from the target file.');
  }
  if (sdkReportedError) {
    failures.push('SDK stream reported an error result.');
  }

  const summaryPath = path.join(outputRoot, 'summary.json');
  const baseSummary = {
    generatedAt: nowIso(),
    startedAt,
    status: 'pending-redaction-scan',
    proofMode: 'live-packaged-read-tool',
    oneRunScope: 'D-APP-15 Option A permits one bounded live packaged provider proof run only.',
    bundleRoot,
    sdkPackage: {
      root: sdkPackageRoot,
      module: sdkModulePath,
      name: sdkPackage.name ?? null,
      version: sdkPackage.version ?? null,
      claudeCodeVersion: sdkPackage.claudeCodeVersion ?? null,
      platformPackageName: expectedCommand.platformPackageName
    },
    expectedPackagedCommand: expectedCommand,
    apiKey: {
      source: apiKeyInput.source,
      sourcePath: apiKeyInput.sourcePath,
      redacted: true
    },
    environment: {
      projectRoot,
      claudeConfigDir: configDir,
      homeDir,
      claudeConfigDirHash: sha256(configDir),
      homeDirHash: sha256(homeDir),
      policy: 'CLAUDE_CONFIG_DIR and HOME are controlled proof paths. API key is supplied only through SDK env.'
    },
    liveRun: {
      model,
      maxTurns,
      timeoutMs,
      permissionMode: 'dontAsk',
      allowedTools: ['Read'],
      disallowedTools: ['Bash', 'Write', 'Edit', 'MultiEdit', 'NotebookEdit', 'WebFetch', 'WebSearch', 'Agent', 'Task'],
      settingSources: [],
      promptHash: sha256(prompt),
      proofTarget: {
        relativePath: READ_TARGET_NAME,
        path: proofTargetPath,
        proofTokenHash: sha256(proofToken)
      }
    },
    observations: {
      messageCount: messageSummaries.length,
      readToolObserved,
      proofTokenObserved,
      sdkReportedError
    },
    sdkMessages: messageSummaries,
    failures
  };

  await writeJson(summaryPath, baseSummary);

  const redaction = await scanAllRedactionTargets(
    [
      { label: 'proof-output', path: outputRoot },
      { label: 'proof-project-root', path: projectRoot },
      { label: 'proof-claude-config-dir', path: configDir },
      { label: 'proof-home-dir', path: homeDir }
    ],
    apiKeyInput.apiKey
  );
  if (!redaction.passed) {
    failures.push('API key string was found in proof artifacts or controlled temp directories.');
  }

  const status = failures.length === 0 ? 'pass' : 'fail';
  const summary = {
    ...baseSummary,
    generatedAt: nowIso(),
    status,
    redaction
  };

  await writeJson(summaryPath, summary);

  log(`live packaged agentSdk read-tool proof status: ${status}`);
  log(`proof mode: ${summary.proofMode}`);
  log(`bundle root: ${bundleRoot}`);
  log(`summary: ${summaryPath}`);
  log(`project root: ${projectRoot}`);
  log(`claude config dir: ${configDir}`);
  log(`home dir: ${homeDir}`);
  if (expectedCommand.commandRealpath) {
    log(`expected packaged command: ${toPosix(expectedCommand.commandRealpath)}`);
  }
  if (status !== 'pass') {
    for (const failure of failures) {
      logError(`- ${redactString(failure, secrets)}`);
    }
    return 1;
  }
  return 0;
}

/**
 * Runs the bounded live packaged agentSdk read-tool proof. Returns the
 * process exit code (0 pass, 1 fail). `opts.cwd` overrides the working
 * directory and `opts.log` / `opts.logError` override the output writers so
 * tests can call this in-process instead of spawning node.
 */
export async function run(argv = process.argv.slice(2), opts = {}) {
  const cwd = opts.cwd ?? process.cwd();
  const log = opts.log ?? ((line) => console.log(line));
  const logError = opts.logError ?? ((line) => console.error(line));

  try {
    const args = parseArgs(argv);
    if (args.help) {
      printUsage(log);
      return 0;
    }
    return await runProof(args, { cwd, log, logError });
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    logError(`live packaged agentSdk read-tool proof failed: ${message}`);
    return 1;
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === scriptPath) {
  process.exitCode = await run();
}
