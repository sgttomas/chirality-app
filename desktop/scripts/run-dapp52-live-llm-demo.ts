/**
 * D-APP-52 live-LLM demonstration driver (the owner-gated act deferred at
 * ruling: "live-LLM demonstration through a harness model session").
 *
 * A REAL model session (live ANTHROPIC_API_KEY, owner at screen) drives the
 * two registered pec tools — mcp__chirality__domain_propose_operation and
 * mcp__chirality__domain_proposal_validate — through the in-process Chirality
 * MCP server, against a D-PEC-06-guarded scratch pec server on loopback.
 * Nothing is driven by direct handler invocation; the tool calls in the
 * captured stream are the live model's own acts.
 *
 * Riders honored: 2 (credentials local-env only; artifacts redacted and
 * secret-scanned for both the API key and the runtime agent password),
 * 3 (loopback-only client), 5 (no apply act of any kind occurs; force is
 * never used), 8 (scratch server torn down, DB deleted after capture),
 * 9 (synthetic data only; SHA-256 manifest by the curating step).
 *
 * Run from `projects/chirality-app-dev/frontend/`:
 *   npx vite-node scripts/run-dapp52-live-llm-demo.ts -- \
 *     --api-key-file <path> --output-root <path> [--model <id>]
 */
import { execSync } from 'node:child_process';
import { createHash, randomBytes, randomUUID } from 'node:crypto';
import { existsSync } from 'node:fs';
import { lstat, mkdir, mkdtemp, readdir, readFile, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { query } from '@anthropic-ai/claude-agent-sdk';
import { createChiralityMcpServers } from '../src/lib/harness/mcp/read-tools';
import {
  assertTypeStrippingNode,
  deleteScratchDb,
  hashPecPassword,
  provisionBridgeActors,
  repoRootFrom,
  seedScratchDb,
  startScratchServer
} from './pec-scratch-server.mjs';

const AGENT_EMAIL = 'pec-bridge-agent@live-demo.demo';
const PORT = 4909;
const DEFAULT_MODEL = 'claude-sonnet-5';
const TIMEOUT_MS = 300_000;
const MAX_RAW_MESSAGE_CHARS = 20_000;

const SYNTHETIC_MDL_CSV = [
  'doc_no,title,package,discipline,owner,current_rev,state,due_date,milestone,issue_purpose_plan,edms_ref,client_no,remarks,deliverable_type',
  'SYN-D-301,Live demo design basis — synthetic,SYN-PKG-301,Process,admin@aurora.dev,A,in_work,2026-10-01,Gate 2,IFR,SYN-EDMS-0301,,Synthetic D-APP-52 live-LLM demo row,Design Basis',
  'SYN-D-302,Live demo line list — synthetic,SYN-PKG-301,Piping,admin@aurora.dev,A,in_work,2026-10-08,Gate 2,IFR,SYN-EDMS-0302,,Synthetic D-APP-52 live-LLM demo row,Line List',
  ''
].join('\n');

function sha256(value: string): string {
  return createHash('sha256').update(value).digest('hex');
}

function redactString(value: string, secrets: string[]): string {
  let redacted = value;
  for (const secret of secrets) {
    if (secret) redacted = redacted.split(secret).join('[REDACTED_SECRET]');
  }
  return redacted;
}

function collectToolNames(value: unknown, found = new Set<string>()): Set<string> {
  if (!value || typeof value !== 'object') return found;
  const record = value as Record<string, unknown>;
  if (
    (record.type === 'tool_use' || record.type === 'server_tool_use') &&
    typeof record.name === 'string'
  ) {
    found.add(record.name);
  }
  const items = Array.isArray(value) ? value : Object.values(record);
  for (const item of items) collectToolNames(item, found);
  return found;
}

function summarizeMessage(message: any, index: number, secrets: string[]) {
  const rawRedacted = redactString(JSON.stringify(message ?? null), secrets);
  return {
    index,
    type: typeof message?.type === 'string' ? message.type : typeof message,
    subtype: typeof message?.subtype === 'string' ? message.subtype : undefined,
    session_id: typeof message?.session_id === 'string' ? message.session_id : undefined,
    is_error: typeof message?.is_error === 'boolean' ? message.is_error : undefined,
    toolNames: [...collectToolNames(message)].sort(),
    contentBlockTypes: Array.isArray(message?.message?.content)
      ? message.message.content.map((b: any) => b?.type ?? typeof b)
      : undefined,
    rawSizeBytes: Buffer.byteLength(rawRedacted),
    rawRedacted:
      rawRedacted.length > MAX_RAW_MESSAGE_CHARS
        ? `${rawRedacted.slice(0, MAX_RAW_MESSAGE_CHARS)}…[truncated]`
        : rawRedacted
  };
}

async function scanPathForSecrets(rootPath: string, secrets: string[]) {
  const findings: Array<{ path: string }> = [];
  const root = path.resolve(rootPath);
  async function visit(currentPath: string): Promise<void> {
    let currentStat;
    try {
      currentStat = await lstat(currentPath);
    } catch {
      return;
    }
    if (currentStat.isSymbolicLink()) return;
    if (currentStat.isDirectory()) {
      for (const entry of await readdir(currentPath)) await visit(path.join(currentPath, entry));
      return;
    }
    if (!currentStat.isFile() || currentStat.size > 2 * 1024 * 1024) return;
    const raw = await readFile(currentPath, 'utf8').catch(() => null);
    if (raw !== null && secrets.some((secret) => secret && raw.includes(secret))) {
      findings.push({ path: currentPath });
    }
  }
  if (existsSync(root)) await visit(root);
  return findings;
}

function parseArgs(argv: string[]) {
  const options: { apiKeyFile?: string; outputRoot?: string; model?: string } = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === '--') continue;
    const next = () => {
      const value = argv[index + 1];
      if (!value || value.startsWith('--')) throw new Error(`Missing value for ${token}`);
      index += 1;
      return value;
    };
    if (token === '--api-key-file') options.apiKeyFile = next();
    else if (token === '--output-root') options.outputRoot = next();
    else if (token === '--model') options.model = next();
    else throw new Error(`Unknown argument: ${token}`);
  }
  return options;
}

async function main(): Promise<void> {
  assertTypeStrippingNode();
  const args = parseArgs(process.argv.slice(2));
  if (!args.apiKeyFile) throw new Error('requires --api-key-file (rider 2)');
  const keyRaw = await readFile(path.resolve(args.apiKeyFile), 'utf8');
  const keyMatch = keyRaw.match(/ANTHROPIC_API_KEY=(\S+)/);
  const apiKey = (keyMatch ? keyMatch[1] : keyRaw).trim();
  if (!apiKey) throw new Error('API key file is empty');
  const model = args.model ?? DEFAULT_MODEL;
  const outputRoot = path.resolve(
    args.outputRoot ?? path.join(process.cwd(), 'artifacts', 'harness', 'dapp52-live-llm-demo', 'latest')
  );
  await mkdir(outputRoot, { recursive: true });

  const repoRoot = repoRootFrom(process.cwd());
  const codeSha = execSync('git rev-parse HEAD', { cwd: repoRoot, encoding: 'utf8' }).trim();

  // ---- scratch basis (script-side instance setup, not workflow acts) -------
  const scratchDir = await mkdtemp(path.join(os.tmpdir(), 'pec-scratch-live-demo-'));
  const dbPath = path.join(scratchDir, 'pec-scratch-live-demo.db');
  const agentPassword = randomBytes(16).toString('hex');
  const secrets = [apiKey, agentPassword];
  console.log('[basis] seeding scratch DB');
  seedScratchDb({ repoRoot, dbPath });
  const actors = await provisionBridgeActors({
    dbPath,
    agentEmail: AGENT_EMAIL,
    agentPasswordHash: hashPecPassword(agentPassword)
  });
  const server = await startScratchServer({ repoRoot, dbPath, port: PORT });
  console.log(`[basis] scratch server on 127.0.0.1:${PORT}; actors ${JSON.stringify(actors)}`);

  process.env.CHIRALITY_PEC_PORT = String(PORT);
  process.env.CHIRALITY_PEC_AGENT_EMAIL = AGENT_EMAIL;
  process.env.CHIRALITY_PEC_AGENT_PASSWORD = agentPassword;
  process.env.CHIRALITY_SESSION_ROOT = path.join(scratchDir, 'sessions');

  const tempRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-dapp52-live-llm-demo-'));
  const projectRoot = path.join(tempRoot, 'project-root');
  const configDir = path.join(tempRoot, 'claude-config');
  const homeDir = path.join(tempRoot, 'home');
  for (const dir of [projectRoot, configDir, homeDir]) await mkdir(dir, { recursive: true });

  const allowedMcpTools = [
    'mcp__chirality__domain_propose_operation',
    'mcp__chirality__domain_proposal_validate'
  ];
  const mcpServers = createChiralityMcpServers({
    context: { projectRoot: repoRoot, sessionId: 'sess_dapp52_live_llm_demo', mode: 'workspaceWrite' },
    allowedToolNames: allowedMcpTools,
    mode: 'workspaceWrite'
  });

  const demoToken = `dapp52-live-llm-demo-${randomUUID()}`;
  const prompt = [
    'You are performing the governed D-APP-52 live demonstration against a synthetic scratch pec instance.',
    `Demo token: ${demoToken}.`,
    'Perform exactly these registered-tool acts, in order, using only the two mcp__chirality__ domain proposal tools:',
    `1. Call domain_propose_operation with profileId "pec", projectId ${actors.projectId}, contract "mdl", sourceName "mdl-syn-live-v1.csv", and csvContent set to exactly the CSV between the CSV markers below.`,
    '2. From its JSON envelope, note engine.id (the proposalId) and engine.version.',
    `3. Call domain_proposal_validate with profileId "pec", projectId ${actors.projectId}, and that proposalId.`,
    `4. Call domain_propose_operation again in mode "refresh" with profileId "pec", projectId ${actors.projectId}, that proposalId, and expectedVersion set to the version you observed.`,
    '5. Call domain_proposal_validate once more for the same proposalId.',
    '6. Then report, as plain text: the demo token, the proposalId, the versions observed before and after refresh, and the resultSemantics string from the last validate envelope. Do not claim acceptance, application, or any domain verdict.',
    'CSV markers:',
    '<CSV>',
    SYNTHETIC_MDL_CSV,
    '</CSV>'
  ].join('\n');

  const abortController = new AbortController();
  const timeout = setTimeout(() => abortController.abort(new Error('live demo timeout')), TIMEOUT_MS);
  const messages: any[] = [];
  let caughtError: string | null = null;
  const startedAt = new Date().toISOString();
  try {
    const stream = query({
      prompt,
      options: {
        abortController,
        cwd: projectRoot,
        model,
        maxTurns: 12,
        permissionMode: 'dontAsk',
        allowedTools: allowedMcpTools,
        disallowedTools: [
          'Bash', 'Read', 'Write', 'Edit', 'MultiEdit', 'NotebookEdit', 'Glob', 'Grep',
          'WebFetch', 'WebSearch', 'Agent', 'Task'
        ],
        settingSources: [],
        mcpServers,
        env: { CLAUDE_CONFIG_DIR: configDir, HOME: homeDir, ANTHROPIC_API_KEY: apiKey }
      }
    });
    for await (const message of stream) {
      messages.push(summarizeMessage(message, messages.length, secrets));
      const label = messages[messages.length - 1];
      console.log(`[msg ${label.index}] ${label.type}${label.subtype ? `/${label.subtype}` : ''} tools=${label.toolNames.join(',') || '-'}`);
    }
  } catch (error) {
    caughtError = redactString(error instanceof Error ? error.message : String(error), secrets);
  } finally {
    clearTimeout(timeout);
  }

  // ---- teardown (rider 8) --------------------------------------------------
  await server.stop().catch(() => undefined);
  await deleteScratchDb(dbPath);
  console.log('[teardown] scratch server stopped; scratch DB (+wal/shm) deleted');

  const failures: string[] = [];
  const proposeObserved = messages.some((m) => m.toolNames.includes('mcp__chirality__domain_propose_operation'));
  const validateObserved = messages.some((m) => m.toolNames.includes('mcp__chirality__domain_proposal_validate'));
  const result = messages.find((m) => m.type === 'result');
  if (!proposeObserved) failures.push('model session never called domain_propose_operation');
  if (!validateObserved) failures.push('model session never called domain_proposal_validate');
  if (!result || result.is_error) failures.push('no successful terminal result');
  if (caughtError) failures.push(`stream error: ${caughtError}`);
  if (!messages.some((m) => m.rawRedacted.includes(demoToken) && m.type === 'assistant')) {
    failures.push('final report did not carry the demo token');
  }

  const summaryPath = path.join(outputRoot, 'summary.json');
  const summary = {
    generatedAt: new Date().toISOString(),
    startedAt,
    status: 'pending-redaction-scan',
    demoMode: 'dapp52-live-llm-model-session',
    authority:
      'D-APP-52 ruling O-A riders 1-11; the deferred live-LLM demonstration executed as the owner act 2026-07-18 (owner at screen, short-lived owner-supplied key)',
    codeSha,
    model,
    scratch: {
      port: PORT,
      loopbackOnly: true,
      agentEmail: AGENT_EMAIL,
      projectId: actors.projectId,
      dbDeletedAfterCapture: true,
      credentialPolicy:
        'agent password generated at runtime, supplied to the transport client via local env only, never in artifacts (secret-scanned); login response discarded by the client by design'
    },
    demoCastActs: 'NONE — no accept, screen act, or apply occurred in this demonstration; force was never used in any form',
    liveRun: {
      permissionMode: 'dontAsk',
      allowedTools: allowedMcpTools,
      settingSources: [],
      maxTurns: 12,
      promptSha256: sha256(prompt),
      demoTokenSha256: sha256(demoToken),
      environment: 'temp project root, CLAUDE_CONFIG_DIR, HOME; key supplied only through the SDK env option'
    },
    observations: {
      messageCount: messages.length,
      proposeObserved,
      validateObserved,
      terminalResult: result ? { subtype: result.subtype, is_error: result.is_error } : null
    },
    messages,
    failures
  };
  await writeFile(summaryPath, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

  const scanFindings = [
    ...(await scanPathForSecrets(outputRoot, secrets)),
    ...(await scanPathForSecrets(tempRoot, secrets)),
    ...(await scanPathForSecrets(scratchDir, secrets))
  ];
  if (scanFindings.length > 0) failures.push('secret material found in demo artifacts or controlled temp dirs');
  const status = failures.length === 0 ? 'pass' : 'fail';
  await writeFile(
    summaryPath,
    `${JSON.stringify({ ...summary, status, redaction: { passed: scanFindings.length === 0, findingCount: scanFindings.length } }, null, 2)}\n`,
    'utf8'
  );
  console.log(`dapp52 live-llm demo status: ${status}`);
  console.log(`summary: ${summaryPath}`);
  if (status !== 'pass') {
    for (const failure of failures) console.error(`- ${failure}`);
    process.exitCode = 1;
  }
}

main().catch((error) => {
  console.error(`dapp52 live-llm demo failed: ${error instanceof Error ? error.message : String(error)}`);
  process.exitCode = 1;
});
