#!/usr/bin/env node

import { EventEmitter } from 'node:events';
import { createHash } from 'node:crypto';
import { existsSync } from 'node:fs';
import { mkdir, mkdtemp, readFile, realpath, stat, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { PassThrough, Writable } from 'node:stream';

const scriptPath = fileURLToPath(import.meta.url);

const SDK_PLATFORM_PACKAGE_BY_RUNTIME = new Map([
  ['darwin:arm64', '@anthropic-ai/claude-agent-sdk-darwin-arm64'],
  ['darwin:x64', '@anthropic-ai/claude-agent-sdk-darwin-x64'],
  ['linux:arm64', '@anthropic-ai/claude-agent-sdk-linux-arm64'],
  ['linux:x64', '@anthropic-ai/claude-agent-sdk-linux-x64'],
  ['win32:arm64', '@anthropic-ai/claude-agent-sdk-win32-arm64'],
  ['win32:x64', '@anthropic-ai/claude-agent-sdk-win32-x64']
]);

function nowIso() {
  return new Date().toISOString();
}

function printUsage(log) {
  log(`Usage: node ./scripts/verify-packaged-agent-sdk-runtime.mjs [options]

Options:
  --bundle-root <path>   Packaged Resources root (default: dist/mac-arm64/Chirality.app/Contents/Resources)
  --output-root <path>   Output directory for summary.json (default: artifacts/harness/packaged-agent-sdk/latest)
  --project-root <path>  Project root passed to the SDK cwd (default: temp proof project)
  --config-dir <path>    CLAUDE_CONFIG_DIR passed to the SDK subprocess (default: temp proof config)
  --home-dir <path>      HOME passed to the SDK subprocess (default: temp proof home)
  --help                 Show this message
`);
}

function readArgValue(argv, index, flagName) {
  const value = argv[index];
  if (!value || value.startsWith('--')) {
    throw new Error(`Missing value for ${flagName}`);
  }
  return value;
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

    throw new Error(`Unknown argument: ${token}`);
  }

  return options;
}

function toPosix(relativePath) {
  return relativePath.split(path.sep).join('/');
}

function isPathWithin(childPath, parentPath) {
  const relative = path.relative(parentPath, childPath);
  return relative === '' || (!relative.startsWith('..') && !path.isAbsolute(relative));
}

function sha256(value) {
  return createHash('sha256').update(value).digest('hex');
}

async function readPackageJson(packageRoot) {
  const raw = await readFile(path.join(packageRoot, 'package.json'), 'utf8');
  return JSON.parse(raw);
}

function resolvePlatformPackageName() {
  return SDK_PLATFORM_PACKAGE_BY_RUNTIME.get(`${process.platform}:${process.arch}`) ?? null;
}

class ScriptedSdkProcess extends EventEmitter {
  constructor() {
    super();
    this.stdout = new PassThrough();
    this.stdin = new Writable({
      write(_chunk, _encoding, callback) {
        callback();
      }
    });
    this.killed = false;
    this.exitCode = null;
  }

  kill(signal) {
    if (this.exitCode !== null) {
      return false;
    }
    this.killed = true;
    this.exitCode = 130;
    this.stdout.end();
    this.emit('exit', null, signal);
    return true;
  }

  writeMessage(message) {
    this.stdout.write(`${JSON.stringify(message)}\n`);
  }

  finish() {
    if (this.exitCode !== null) {
      return;
    }
    this.exitCode = 0;
    this.stdout.end();
    this.emit('exit', 0, null);
  }
}

function createScriptedSpawn(spawnRecords) {
  return (options) => {
    spawnRecords.push({
      command: options.command,
      args: options.args,
      cwd: options.cwd,
      env: {
        CLAUDE_CONFIG_DIR: options.env?.CLAUDE_CONFIG_DIR,
        HOME: options.env?.HOME,
        CLAUDE_CODE_ENTRYPOINT: options.env?.CLAUDE_CODE_ENTRYPOINT,
        CLAUDE_AGENT_SDK_VERSION: options.env?.CLAUDE_AGENT_SDK_VERSION
      }
    });

    const subprocess = new ScriptedSdkProcess();
    queueMicrotask(() => {
      subprocess.writeMessage({
        type: 'system',
        subtype: 'init',
        session_id: 'packaged_sdk_proof_1',
        uuid: '00000000-0000-0000-0000-000000000201',
        apiKeySource: 'temporary',
        claude_code_version: '2.1.150',
        cwd: options.cwd ?? '',
        tools: [],
        mcp_servers: [],
        model: 'claude-test',
        permissionMode: 'default',
        slash_commands: [],
        output_style: 'default',
        skills: [],
        plugins: []
      });
      subprocess.writeMessage({
        type: 'result',
        subtype: 'success',
        duration_ms: 1,
        duration_api_ms: 0,
        is_error: false,
        num_turns: 1,
        result: 'packaged agentSdk resolver proof',
        stop_reason: 'end_turn',
        total_cost_usd: 0,
        usage: {},
        modelUsage: {},
        permission_denials: [],
        uuid: '00000000-0000-0000-0000-000000000202',
        session_id: 'packaged_sdk_proof_1'
      });
      subprocess.finish();
    });
    return subprocess;
  };
}

async function inspectCommand(command, unpackedNodeModulesRoot) {
  const absoluteCommand = path.resolve(command);
  let commandRealpath = null;
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

function summarizeSdkMessage(message) {
  if (!message || typeof message !== 'object') {
    return { type: typeof message };
  }

  return {
    type: typeof message.type === 'string' ? message.type : 'unknown',
    subtype: typeof message.subtype === 'string' ? message.subtype : undefined,
    session_id: typeof message.session_id === 'string' ? message.session_id : undefined
  };
}

async function writeJson(filePath, value) {
  await writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

async function runProof(args, { cwd, log, logError }) {
  const bundleRoot = path.resolve(
    args.bundleRoot ?? path.join(cwd, 'dist', 'mac-arm64', 'Chirality.app', 'Contents', 'Resources')
  );
  const outputRoot = path.resolve(
    args.outputRoot ?? path.join(cwd, 'artifacts', 'harness', 'packaged-agent-sdk', 'latest')
  );
  const tempRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-packaged-agent-sdk-proof-'));
  const projectRoot = path.resolve(args.projectRoot ?? path.join(tempRoot, 'project-root'));
  const configDir = path.resolve(args.configDir ?? path.join(tempRoot, 'claude-config'));
  const homeDir = path.resolve(args.homeDir ?? path.join(tempRoot, 'home'));
  const sdkPackageRoot = path.join(
    bundleRoot,
    'app.asar.unpacked',
    'node_modules',
    '@anthropic-ai',
    'claude-agent-sdk'
  );
  const sdkModulePath = path.join(sdkPackageRoot, 'sdk.mjs');
  const unpackedNodeModulesRoot = path.join(bundleRoot, 'app.asar.unpacked', 'node_modules');
  const platformPackageName = resolvePlatformPackageName();

  await mkdir(outputRoot, { recursive: true });
  await mkdir(projectRoot, { recursive: true });
  await mkdir(configDir, { recursive: true });
  await mkdir(homeDir, { recursive: true });

  if (!existsSync(sdkModulePath)) {
    throw new Error(`Packaged SDK module not found: ${sdkModulePath}`);
  }

  const sdkPackage = await readPackageJson(sdkPackageRoot);
  const sdkModule = await import(`${pathToFileURL(sdkModulePath).href}?proof=${Date.now()}`);
  if (typeof sdkModule.query !== 'function') {
    throw new Error(`Packaged SDK module does not export query(): ${sdkModulePath}`);
  }

  const spawnRecords = [];
  const sdkMessages = [];
  const stream = sdkModule.query({
    prompt: 'Run the no-live packaged agentSdk resolver proof.',
    options: {
      cwd: projectRoot,
      model: 'claude-test',
      maxTurns: 1,
      allowedTools: [],
      disallowedTools: ['Bash', 'Write', 'Edit', 'WebFetch', 'WebSearch'],
      settingSources: [],
      env: {
        CLAUDE_CONFIG_DIR: configDir,
        HOME: homeDir,
        ANTHROPIC_API_KEY: 'test-non-live-packaged-agent-sdk-proof'
      },
      spawnClaudeCodeProcess: createScriptedSpawn(spawnRecords)
    }
  });

  for await (const message of stream) {
    sdkMessages.push(summarizeSdkMessage(message));
  }

  const failures = [];
  if (spawnRecords.length !== 1) {
    failures.push(`Expected exactly one scripted SDK subprocess spawn; observed ${spawnRecords.length}.`);
  }

  const spawnRecord = spawnRecords[0] ?? null;
  const commandInspection = spawnRecord
    ? await inspectCommand(spawnRecord.command, unpackedNodeModulesRoot)
    : null;

  if (commandInspection) {
    if (!commandInspection.exists || !commandInspection.isFile) {
      failures.push(`Resolved SDK command is not a file: ${commandInspection.command}`);
    }
    if (!commandInspection.commandUnderUnpackedNodeModules) {
      failures.push(
        `Resolved SDK command is outside app.asar.unpacked/node_modules: ${commandInspection.commandRealpath}`
      );
    }
    if (platformPackageName && !commandInspection.commandRealpath.includes(platformPackageName)) {
      failures.push(
        `Resolved SDK command does not include expected platform package ${platformPackageName}: ${commandInspection.commandRealpath}`
      );
    }
  }

  if (spawnRecord?.env?.CLAUDE_CONFIG_DIR !== configDir) {
    failures.push('Packaged SDK subprocess did not receive the controlled CLAUDE_CONFIG_DIR.');
  }
  if (spawnRecord?.env?.HOME !== homeDir) {
    failures.push('Packaged SDK subprocess did not receive the controlled HOME.');
  }

  const status = failures.length === 0 ? 'pass' : 'fail';
  const summary = {
    generatedAt: nowIso(),
    status,
    proofMode: 'scripted-no-live-provider',
    bundleRoot,
    sdkPackage: {
      root: sdkPackageRoot,
      module: sdkModulePath,
      name: sdkPackage.name ?? null,
      version: sdkPackage.version ?? null,
      claudeCodeVersion: sdkPackage.claudeCodeVersion ?? null,
      platformPackageName
    },
    resolver: commandInspection,
    environment: {
      projectRoot,
      claudeConfigDir: configDir,
      homeDir,
      claudeConfigDirHash: sha256(configDir),
      homeDirHash: sha256(homeDir),
      policy: 'CLAUDE_CONFIG_DIR and HOME are controlled temp paths for this proof.'
    },
    spawn: spawnRecord
      ? {
          command: spawnRecord.command,
          args: spawnRecord.args,
          cwd: spawnRecord.cwd,
          env: spawnRecord.env,
          argsContainStreamJson: spawnRecord.args.includes('--output-format') && spawnRecord.args.includes('stream-json')
        }
      : null,
    sdkMessages,
    failures
  };

  await writeJson(path.join(outputRoot, 'summary.json'), summary);
  log(`packaged agentSdk runtime proof status: ${status}`);
  log(`proof mode: ${summary.proofMode}`);
  log(`bundle root: ${bundleRoot}`);
  log(`summary: ${path.join(outputRoot, 'summary.json')}`);
  if (commandInspection) {
    log(`resolved command: ${toPosix(commandInspection.commandRealpath)}`);
  }
  if (status !== 'pass') {
    for (const failure of failures) {
      logError(`- ${failure}`);
    }
    return 1;
  }
  return 0;
}

/**
 * Runs the packaged agentSdk resolver proof. Returns the process exit code
 * (0 pass, 1 fail). `opts.cwd` overrides the working directory and
 * `opts.log` / `opts.logError` override the output writers so tests can call
 * this in-process instead of spawning node.
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
    logError(`packaged agentSdk runtime proof failed: ${message}`);
    return 1;
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === scriptPath) {
  process.exitCode = await run();
}
