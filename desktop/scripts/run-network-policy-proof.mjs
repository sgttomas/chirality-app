#!/usr/bin/env node

import { spawn } from 'node:child_process';
import { lookup } from 'node:dns/promises';
import { createWriteStream } from 'node:fs';
import { appendFile, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

const SCRIPT_PATH = fileURLToPath(import.meta.url);
const FRONTEND_ROOT = path.resolve(path.dirname(SCRIPT_PATH), '..');
const REPO_ROOT = path.resolve(FRONTEND_ROOT, '..');
const DELIVERABLE_ROOT = path.resolve(
  REPO_ROOT,
  'execution/PKG-09_Validation_Packaging_Security_and_Release/1_Working/DEL-09-06_Network_Key_Attachment_and_Renderer_Security_Checks'
);

const LOOPBACK_HOSTS = new Set(['localhost', '127.0.0.1', '::1', '[::1]']);
const ALLOWLIST_DNS_HOSTS = ['api.anthropic.com'];
const ALLOWLIST_HOSTS = new Set(ALLOWLIST_DNS_HOSTS);

const DEFAULT_RUN_COUNT = 3;
const DEFAULT_IDLE_SECONDS = 600;
const DEFAULT_IDLE_SAMPLE_SECONDS = 60;
const DEFAULT_HTTP_TIMEOUT_MS = 120_000;
const DEFAULT_STARTUP_WAIT_MS = 4000;
const PROVIDER_CREDENTIAL_ENV_NAMES = [
  'ANTHROPIC_API_KEY',
  'CHIRALITY_ANTHROPIC_API_KEY',
  'CHIRALITY_OMLX_API_KEY'
];
const NON_SECRET_PROVIDER_FIXTURE = 'chirality-proof-fixture-not-a-secret';

function timestampForPath(date = new Date()) {
  return date.toISOString().replace(/[:]/g, '').replace(/\..+$/, '').replace('T', '_');
}

function parseIntegerArg(value, fallback) {
  if (value === undefined) {
    return fallback;
  }

  const parsed = Number.parseInt(value, 10);
  if (!Number.isSafeInteger(parsed) || parsed <= 0) {
    return fallback;
  }

  return parsed;
}

function parseProviderMode(value) {
  const normalized = String(value ?? '').trim();
  const lowered = normalized.toLowerCase();
  if (lowered === 'agentsdk' || lowered === 'agent-sdk' || lowered === 'claude-agent-sdk') {
    return 'agentSdk';
  }
  if (lowered === 'anthropic') {
    return 'anthropic';
  }
  if (lowered === 'stub' || lowered.length === 0) {
    return 'stub';
  }
  throw new Error(`Unsupported --provider value '${value}'. Expected stub, anthropic, or agentSdk.`);
}

function parseArgs(argv) {
  const args = {
    runs: DEFAULT_RUN_COUNT,
    idleSeconds: DEFAULT_IDLE_SECONDS,
    idleSampleSeconds: DEFAULT_IDLE_SAMPLE_SECONDS,
    provider: undefined,
    scriptedAgentSdk: false,
    outputDir: path.resolve(
      DELIVERABLE_ROOT,
      'Evidence',
      `NETWORK_POLICY_PROOF_${timestampForPath()}`
    )
  };

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];

    if (token === '--runs' && argv[index + 1]) {
      args.runs = parseIntegerArg(argv[index + 1], args.runs);
      index += 1;
      continue;
    }

    if (token === '--idle-seconds' && argv[index + 1]) {
      args.idleSeconds = parseIntegerArg(argv[index + 1], args.idleSeconds);
      index += 1;
      continue;
    }

    if (token === '--idle-sample-seconds' && argv[index + 1]) {
      args.idleSampleSeconds = parseIntegerArg(argv[index + 1], args.idleSampleSeconds);
      index += 1;
      continue;
    }

    if (token === '--provider' && argv[index + 1]) {
      args.provider = parseProviderMode(argv[index + 1]);
      index += 1;
      continue;
    }

    if (token === '--scripted-agent-sdk') {
      args.scriptedAgentSdk = true;
      continue;
    }

    if (token === '--output-dir' && argv[index + 1]) {
      args.outputDir = path.resolve(argv[index + 1]);
      index += 1;
    }
  }

  args.provider = args.provider ?? parseProviderMode(process.env.CHIRALITY_HARNESS_PROVIDER);

  if (args.scriptedAgentSdk && args.provider !== 'agentSdk') {
    throw new Error('--scripted-agent-sdk requires --provider agentSdk.');
  }

  return args;
}

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

function toIsoNow() {
  return new Date().toISOString();
}

function parseRemoteHost(remote) {
  if (!remote) {
    return '';
  }

  if (remote.startsWith('[')) {
    const close = remote.indexOf(']');
    if (close > 1) {
      return remote.slice(1, close);
    }
  }

  const lastColon = remote.lastIndexOf(':');
  if (lastColon > 0) {
    return remote.slice(0, lastColon);
  }

  return remote;
}

function classifyRemoteHost(host) {
  const normalized = host.trim().toLowerCase();
  if (!normalized) {
    return 'unknown';
  }

  if (LOOPBACK_HOSTS.has(normalized)) {
    return 'loopback';
  }

  if (ALLOWLIST_HOSTS.has(normalized)) {
    return 'allowlisted';
  }

  if (normalized.endsWith('.anthropic.com')) {
    return 'anthropic_non_allowlisted';
  }

  return 'external_non_allowlisted';
}

export function parseLsofTcp(output) {
  const lines = output.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  const remoteEndpoints = [];
  for (const line of lines) {
    if (!line.includes('->')) {
      continue;
    }

    const arrowIndex = line.indexOf('->');
    const remoteField = line.slice(arrowIndex + 2).split(' ')[0];
    const remoteHost = parseRemoteHost(remoteField);
    const pidMatch = line.match(/^\S+\s+(\d+)\s+/);
    remoteEndpoints.push({
      processId: pidMatch ? Number(pidMatch[1]) : null,
      endpoint: remoteField,
      host: remoteHost,
      class: classifyRemoteHost(remoteHost)
    });
  }

  return {
    rawLineCount: lines.length,
    remoteEndpoints
  };
}

function parseProcessTable(output) {
  return output.split(/\r?\n/).flatMap((line) => {
    const match = line.match(/^\s*(\d+)\s+(\d+)\s+(.*)$/);
    return match ? [{ pid: Number(match[1]), ppid: Number(match[2]), command: match[3] }] : [];
  });
}

export function descendantProcessIds(processRows, roots) {
  const selected = new Set(roots.filter((pid) => Number.isSafeInteger(pid) && pid > 0));
  let changed = true;
  while (changed) {
    changed = false;
    for (const row of processRows) {
      if (selected.has(row.ppid) && !selected.has(row.pid)) {
        selected.add(row.pid);
        changed = true;
      }
    }
  }
  return [...selected].sort((left, right) => left - right);
}

export function scrubProviderCredentialEnv(sourceEnv) {
  const clean = { ...sourceEnv };
  for (const name of PROVIDER_CREDENTIAL_ENV_NAMES) delete clean[name];
  return clean;
}

async function resolveAllowlistedHosts() {
  const resolved = [];
  for (const hostname of ALLOWLIST_DNS_HOSTS) {
    const addresses = await lookup(hostname, { all: true, verbatim: true });
    if (addresses.length === 0) throw new Error(`Allowlist DNS resolution returned no addresses: ${hostname}`);
    for (const { address, family } of addresses) {
      ALLOWLIST_HOSTS.add(address.toLowerCase());
      resolved.push({ hostname, address, family });
    }
  }
  return resolved;
}

async function runCommand(command, args, options = {}) {
  return new Promise((resolve) => {
    const child = spawn(command, args, {
      cwd: options.cwd,
      env: options.env,
      stdio: ['ignore', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (chunk) => {
      stdout += chunk.toString();
    });

    child.stderr.on('data', (chunk) => {
      stderr += chunk.toString();
    });

    child.on('close', (code) => {
      resolve({ code: code ?? 1, stdout, stderr });
    });
  });
}

function startLoggedProcess({ label, command, args, cwd, env, logPath }) {
  const child = spawn(command, args, {
    cwd,
    env,
    stdio: ['ignore', 'pipe', 'pipe']
  });

  const stream = createWriteStream(logPath, { flags: 'a' });
  stream.write(`[${toIsoNow()}] START ${label}: ${command} ${args.join(' ')}\n`);

  child.stdout.on('data', (chunk) => {
    stream.write(chunk);
  });

  child.stderr.on('data', (chunk) => {
    stream.write(chunk);
  });

  child.on('close', (code, signal) => {
    stream.write(`[${toIsoNow()}] EXIT ${label}: code=${code ?? 'null'} signal=${signal ?? 'null'}\n`);
  });

  return { child, stream };
}

async function stopProcess(child, label, timeoutMs = 10_000) {
  if (!child || child.exitCode !== null) {
    return;
  }

  child.kill('SIGTERM');
  const start = Date.now();

  while (child.exitCode === null && Date.now() - start < timeoutMs) {
    await sleep(100);
  }

  if (child.exitCode === null) {
    child.kill('SIGKILL');
    const hardStart = Date.now();
    while (child.exitCode === null && Date.now() - hardStart < 2000) {
      await sleep(50);
    }
  }

  if (child.exitCode === null) {
    throw new Error(`Failed to stop ${label} process`);
  }
}

async function waitForHttpReady(url, timeoutMs, processToWatch) {
  const started = Date.now();

  while (Date.now() - started < timeoutMs) {
    if (processToWatch && processToWatch.exitCode !== null) {
      throw new Error(`Observed process exit before HTTP readiness at ${url}`);
    }

    try {
      const response = await fetch(url, { method: 'GET' });
      if (response.ok || response.status === 404) {
        return;
      }
    } catch {
      // keep waiting until timeout
    }

    await sleep(500);
  }

  throw new Error(`Timed out waiting for HTTP readiness at ${url}`);
}

async function captureTcpSnapshot({ runDir, label, processLabel, pid }) {
  const capture = {
    timestamp: toIsoNow(),
    label,
    processLabel,
    rootPid: pid,
    pids: [],
    processes: [],
    usable: false,
    lsofExitCode: 0,
    raw: '',
    parsed: {
      rawLineCount: 0,
      remoteEndpoints: []
    }
  };

  if (!Number.isSafeInteger(pid) || pid <= 0) {
    capture.lsofExitCode = 1;
    capture.error = 'invalid root PID';
    await appendFile(path.resolve(runDir, 'tcp_snapshots.ndjson'), `${JSON.stringify(capture)}\n`, 'utf8');
    throw new Error(`Unusable TCP capture for ${processLabel}: invalid root PID`);
  }

  const ps = await runCommand('ps', ['-axo', 'pid=,ppid=,command=']);
  if (ps.code !== 0) throw new Error(`ps failed for ${processLabel}: ${ps.stderr.trim()}`);
  const processRows = parseProcessTable(ps.stdout);
  capture.pids = descendantProcessIds(processRows, [pid]);
  capture.processes = processRows.filter((row) => capture.pids.includes(row.pid));
  if (!capture.pids.includes(pid)) {
    capture.lsofExitCode = 1;
    capture.error = 'root PID absent from process table';
    await appendFile(path.resolve(runDir, 'tcp_snapshots.ndjson'), `${JSON.stringify(capture)}\n`, 'utf8');
    throw new Error(`Unusable TCP capture for ${processLabel}: root PID absent from process table`);
  }

  const result = await runCommand('lsof', [
    '-P',
    '-a',
    `-p${capture.pids.join(',')}`,
    '-iTCP',
    '-sTCP:LISTEN,ESTABLISHED,SYN_SENT,CLOSE_WAIT'
  ]);

  capture.lsofExitCode = result.code;
  capture.raw = `${result.stdout}${result.stderr}`.trim();

  if ((result.code === 0 || result.code === 1) && result.stdout.trim().length > 0) {
    capture.parsed = parseLsofTcp(result.stdout);
    capture.usable = capture.parsed.rawLineCount > 0;
  }

  await appendFile(
    path.resolve(runDir, 'tcp_snapshots.ndjson'),
    `${JSON.stringify(capture)}\n`,
    'utf8'
  );

  if (!capture.usable) {
    throw new Error(
      `Unusable TCP capture for ${processLabel}: lsof exit ${result.code} with no parseable output`
    );
  }

  return capture;
}

export function summarizeCaptureIntegrity(snapshots) {
  const unusableSnapshots = snapshots.filter((snapshot) => snapshot.usable !== true);
  const electronSnapshots = snapshots.filter((snapshot) => snapshot.processLabel === 'electron');
  const electronDescendantPids = [...new Set(electronSnapshots.flatMap((snapshot) =>
    (snapshot.pids ?? []).filter((pid) => pid !== snapshot.rootPid)
  ))].sort((left, right) => left - right);
  const electronDescendantTcp = electronSnapshots.flatMap((snapshot) =>
    snapshot.parsed.remoteEndpoints.filter((endpoint) =>
      Number.isSafeInteger(endpoint.processId) && endpoint.processId !== snapshot.rootPid
    )
  );
  return {
    usableSnapshotCount: snapshots.length - unusableSnapshots.length,
    unusableSnapshotCount: unusableSnapshots.length,
    electronDescendantPids,
    electronDescendantTcp,
    pass:
      snapshots.length > 0 &&
      unusableSnapshots.length === 0 &&
      electronDescendantPids.length > 0 &&
      electronDescendantTcp.length > 0
  };
}

function summarizeSnapshotEndpoints(snapshots) {
  const unique = new Map();

  for (const snapshot of snapshots) {
    for (const endpoint of snapshot.parsed.remoteEndpoints) {
      const key = `${endpoint.host}|${endpoint.endpoint}|${endpoint.class}`;
      if (!unique.has(key)) {
        unique.set(key, {
          host: endpoint.host,
          endpoint: endpoint.endpoint,
          class: endpoint.class,
          firstSeen: snapshot.timestamp,
          label: snapshot.label,
          processLabel: snapshot.processLabel
        });
      }
    }
  }

  return Array.from(unique.values());
}

function extractProbePayloads(logText) {
  const payloads = [];
  const lines = logText.split(/\r?\n/);

  for (const line of lines) {
    const markerIndex = line.indexOf('[network-policy-probe]');
    if (markerIndex === -1) {
      continue;
    }

    const jsonPart = line.slice(markerIndex + '[network-policy-probe]'.length).trim();
    if (!jsonPart) {
      continue;
    }

    try {
      payloads.push(JSON.parse(jsonPart));
    } catch {
      payloads.push({ parseError: true, raw: jsonPart });
    }
  }

  return payloads;
}

async function runProofCycle({ runIndex, args, outputDir }) {
  const runId = `run-${String(runIndex).padStart(2, '0')}`;
  const runDir = path.resolve(outputDir, runId);
  await mkdir(runDir, { recursive: true });
  const sessionRootPath = path.resolve('/tmp', `chirality-proof-sessions-${runId}-${timestampForPath()}`);
  await mkdir(sessionRootPath, { recursive: true });
  const userDataPath = path.resolve(sessionRootPath, 'user-data');
  const providerMode = args.provider;
  const scriptedAgentSdkProof =
    providerMode === 'agentSdk' &&
    (args.scriptedAgentSdk || process.env.CHIRALITY_AGENTSDK_SCRIPTED_PROOF === '1');
  const resolvedAllowlistHosts = await resolveAllowlistedHosts();

  const baseEnv = {
    ...scrubProviderCredentialEnv(process.env),
    NEXT_TELEMETRY_DISABLED: '1',
    CHIRALITY_ANTHROPIC_STREAM_TIMEOUT_MS: process.env.CHIRALITY_ANTHROPIC_STREAM_TIMEOUT_MS || '15000',
    CHIRALITY_SESSION_ROOT: sessionRootPath,
    CHIRALITY_HARNESS_PROVIDER: providerMode,
    CHIRALITY_USER_DATA: userDataPath,
    CHIRALITY_SKIP_CLI_LAUNCHER: '1'
  };
  if (providerMode !== 'stub') baseEnv.ANTHROPIC_API_KEY = NON_SECRET_PROVIDER_FIXTURE;
  if (scriptedAgentSdkProof) {
    baseEnv.CHIRALITY_AGENTSDK_SCRIPTED_PROOF = '1';
  } else {
    delete baseEnv.CHIRALITY_AGENTSDK_SCRIPTED_PROOF;
  }

  const nextLogPath = path.resolve(runDir, 'next.log');
  const electronLogPath = path.resolve(runDir, 'electron.log');
  const electronCommand = path.resolve(FRONTEND_ROOT, 'node_modules/.bin/electron');
  const nextProcess = startLoggedProcess({
    label: `${runId}:next`,
    command: path.resolve(FRONTEND_ROOT, 'node_modules/.bin/next'),
    args: ['dev', '--port', '3000', '--hostname', '127.0.0.1'],
    cwd: FRONTEND_ROOT,
    env: baseEnv,
    logPath: nextLogPath
  });

  let electronProcess;
  const snapshots = [];
  const timeline = [];

  try {
    timeline.push({ at: toIsoNow(), step: 'next_start' });
    await waitForHttpReady('http://127.0.0.1:3000', DEFAULT_HTTP_TIMEOUT_MS, nextProcess.child);
    timeline.push({ at: toIsoNow(), step: 'next_ready' });

    const probeUrls = [
      'https://example.com/chirality-network-policy-blocked-check',
      'https://api.anthropic.com/v1/messages',
      'http://127.0.0.1:3000/'
    ].join(',');

    electronProcess = startLoggedProcess({
      label: `${runId}:electron`,
      command: electronCommand,
      args: ['dist-electron/main.js'],
      cwd: FRONTEND_ROOT,
      env: {
        ...baseEnv,
        ELECTRON_RENDERER_URL: 'http://127.0.0.1:3000',
        CHIRALITY_NETWORK_POLICY_PROBE_URLS: probeUrls,
        CHIRALITY_NETWORK_POLICY_PROBE_DELAY_MS: '2500',
        CHIRALITY_NETWORK_POLICY_PROBE_TIMEOUT_MS: '8000'
      },
      logPath: electronLogPath
    });

    timeline.push({ at: toIsoNow(), step: 'electron_start' });
    await sleep(DEFAULT_STARTUP_WAIT_MS);

    snapshots.push(
      await captureTcpSnapshot({
        runDir,
        label: 'startup_next',
        processLabel: 'next',
        pid: nextProcess.child.pid
      })
    );

    snapshots.push(
      await captureTcpSnapshot({
        runDir,
        label: 'startup_electron',
        processLabel: 'electron',
        pid: electronProcess.child.pid
      })
    );

    for (
      let elapsed = args.idleSampleSeconds;
      elapsed <= args.idleSeconds;
      elapsed += args.idleSampleSeconds
    ) {
      await sleep(args.idleSampleSeconds * 1000);

      snapshots.push(
        await captureTcpSnapshot({
          runDir,
          label: `idle_${elapsed}s_next`,
          processLabel: 'next',
          pid: nextProcess.child.pid
        })
      );

      snapshots.push(
        await captureTcpSnapshot({
          runDir,
          label: `idle_${elapsed}s_electron`,
          processLabel: 'electron',
          pid: electronProcess.child.pid
        })
      );
    }

    timeline.push({ at: toIsoNow(), step: 'idle_window_complete' });

    const uniqueEndpoints = summarizeSnapshotEndpoints(snapshots);
    const captureIntegrity = summarizeCaptureIntegrity(snapshots);

    const nextLog = await readFile(nextLogPath, 'utf8').catch(() => '');
    const electronLog = await readFile(electronLogPath, 'utf8').catch(() => '');

    const blockedDiagnostics = (electronLog.match(/Blocked renderer outbound request by network policy/g) || [])
      .length;

    const probePayloads = extractProbePayloads(electronLog);

    const nonAllowlistedEndpoints = uniqueEndpoints.filter(
      (endpoint) => endpoint.class !== 'loopback' && endpoint.class !== 'allowlisted'
    );

    const anthropicAllowlistedEndpoints = uniqueEndpoints.filter(
      (endpoint) => endpoint.class === 'allowlisted'
    );

    const electronStayedRunning = electronProcess.child.exitCode === null;
    const nextStayedRunning = nextProcess.child.exitCode === null;

    const summary = {
      runId,
      generatedAt: toIsoNow(),
      timeline,
      scenario: {
        startup: true,
        providerMode,
        scriptedAgentSdkProof,
        sessionRootPath,
        userDataPath,
        providerExecution: 'not-exercised-by-renderer-egress-capture',
        resolvedAllowlistHosts,
        electronStayedRunning,
        nextStayedRunning,
        idleSeconds: args.idleSeconds,
        shutdown: true
      },
      diagnostics: {
        blockedRendererDiagnosticsCount: blockedDiagnostics,
        networkProbePayloadCount: probePayloads.length,
        networkProbePayloads: probePayloads
      },
      endpointSummary: {
        totalUniqueEndpoints: uniqueEndpoints.length,
        allowlistedAnthropicEndpoints: anthropicAllowlistedEndpoints,
        nonAllowlistedEndpoints,
        uniqueEndpoints
      },
      captureIntegrity,
      verdict: {
        noNonAllowlistedOutboundTcp: nonAllowlistedEndpoints.length === 0,
        blockedRendererDiagnosticsObserved: blockedDiagnostics > 0,
        networkProbePayloadObserved: probePayloads.length > 0,
        usableDescendantCapture: captureIntegrity.pass,
        rendererDescendantTrafficObserved: captureIntegrity.electronDescendantTcp.length > 0,
        scenarioCompleted: electronStayedRunning && nextStayedRunning
      },
      artifacts: {
        nextLogPath,
        electronLogPath,
        tcpSnapshotsPath: path.resolve(runDir, 'tcp_snapshots.ndjson')
      },
      notes: {
        unresolvedConf002:
          'CONF-002 (OCSP/CRL infrastructure carve-out) remains unresolved; TCP-level summary flags only explicit non-allowlisted external endpoints.'
      }
    };

    await writeFile(path.resolve(runDir, 'summary.json'), JSON.stringify(summary, null, 2), 'utf8');

    return summary;
  } finally {
    if (electronProcess?.child) {
      await stopProcess(electronProcess.child, `${runId}:electron`);
      electronProcess.stream.end();
    }

    await stopProcess(nextProcess.child, `${runId}:next`);
    nextProcess.stream.end();
    await rm(sessionRootPath, { recursive: true, force: true });
  }
}

function aggregateRunVerdicts(runs) {
  const failedRuns = runs.filter((run) => {
    const verdict = run.verdict;
    return !(
      verdict.noNonAllowlistedOutboundTcp &&
      verdict.blockedRendererDiagnosticsObserved &&
      verdict.networkProbePayloadObserved &&
      verdict.usableDescendantCapture &&
      verdict.rendererDescendantTrafficObserved &&
      verdict.scenarioCompleted
    );
  });

  return {
    runCount: runs.length,
    failedRunCount: failedRuns.length,
    passed: failedRuns.length === 0,
    failedRuns: failedRuns.map((run) => run.runId)
  };
}

function renderMarkdownSummary(args, outputDir, runSummaries, aggregate) {
  const lines = [];
  const providerMode = args.provider;

  lines.push('# Network Policy Proof Run Summary');
  lines.push('');
  lines.push(`- Generated: ${toIsoNow()}`);
  lines.push(`- Output directory: ${outputDir}`);
  lines.push(`- Run count: ${args.runs}`);
  lines.push(`- Provider mode: ${providerMode}`);
  lines.push(`- Scripted agentSdk subprocess: ${args.scriptedAgentSdk ? 'yes' : 'no'}`);
  lines.push(`- Idle window per run: ${args.idleSeconds} seconds`);
  lines.push('');
  lines.push('## Aggregate Verdict');
  lines.push('');
  lines.push(`- Overall: ${aggregate.passed ? 'PASS' : 'FAIL'}`);
  lines.push(`- Failed runs: ${aggregate.failedRunCount}`);
  lines.push('');
  lines.push('## Per-Run Results');
  lines.push('');
  lines.push('| Run | Scenario Completed | Blocked Diagnostics | Probe Payloads | Non-Allowlisted Endpoints | Verdict |');
  lines.push('|---|---|---|---|---|---|');

  for (const run of runSummaries) {
    const verdict =
      run.verdict.noNonAllowlistedOutboundTcp &&
      run.verdict.blockedRendererDiagnosticsObserved &&
      run.verdict.networkProbePayloadObserved &&
      run.verdict.usableDescendantCapture &&
      run.verdict.rendererDescendantTrafficObserved &&
      run.verdict.scenarioCompleted
        ? 'PASS'
        : 'FAIL';

    lines.push(
      `| ${run.runId} | ${run.verdict.scenarioCompleted ? 'yes' : 'no'} | ${run.diagnostics.blockedRendererDiagnosticsCount} | ${run.diagnostics.networkProbePayloadCount} | ${run.endpointSummary.nonAllowlistedEndpoints.length} | ${verdict} |`
    );
  }

  lines.push('');
  lines.push('## Notes');
  lines.push('');
  lines.push(
    '- CONF-002 (OCSP/CRL carve-out wording) remains unresolved; this summary reports explicit non-allowlisted TCP endpoints and renderer policy diagnostics only.'
  );

  return `${lines.join('\n')}\n`;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  await mkdir(args.outputDir, { recursive: true });

  const buildResult = await runCommand('npm', ['run', 'build:electron'], {
    cwd: FRONTEND_ROOT,
    env: {
      ...scrubProviderCredentialEnv(process.env),
      NEXT_TELEMETRY_DISABLED: '1'
    }
  });

  await writeFile(
    path.resolve(args.outputDir, 'build_electron.log'),
    `${buildResult.stdout}${buildResult.stderr}`,
    'utf8'
  );

  if (buildResult.code !== 0) {
    throw new Error('Failed to build Electron main process before proof runs');
  }

  const runSummaries = [];

  for (let index = 1; index <= args.runs; index += 1) {
    // Keep each run independent by restarting runtime processes per cycle.
    // This matches the proof standard requirement for independent runs.
    console.log(`[proof] starting run ${index}/${args.runs}`);
    const summary = await runProofCycle({ runIndex: index, args, outputDir: args.outputDir });
    runSummaries.push(summary);
    console.log(`[proof] completed run ${index}/${args.runs}`);
  }

  const aggregate = aggregateRunVerdicts(runSummaries);

  await writeFile(
    path.resolve(args.outputDir, 'summary.json'),
    JSON.stringify(
      {
        generatedAt: toIsoNow(),
        args,
        aggregate,
        runs: runSummaries
      },
      null,
      2
    ),
    'utf8'
  );

  await writeFile(
    path.resolve(args.outputDir, 'SUMMARY.md'),
    renderMarkdownSummary(args, args.outputDir, runSummaries, aggregate),
    'utf8'
  );

  console.log(`[proof] output: ${args.outputDir}`);
  console.log(`[proof] verdict: ${aggregate.passed ? 'PASS' : 'FAIL'}`);

  if (!aggregate.passed) {
    process.exitCode = 1;
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === SCRIPT_PATH) {
  main().catch((error) => {
    console.error('[proof] fatal:', error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  });
}
