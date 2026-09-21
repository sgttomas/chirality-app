#!/usr/bin/env node

/**
 * Persistent, test-only Runtime protocol fixture for connected browser checks.
 * It binds only a Unix socket, uses a deterministic fake provider, and never
 * reads credentials or invokes supplier/native code.
 *
 * Start from frontend/: node src/__tests__/fixtures/controlled-v3-runtime.mjs
 * Start Next with the exact environment command printed in the ready record.
 * Stop with Ctrl-C. Optional cleanup:
 *   rm -rf /tmp/chirality-v3-ui-runtime-20260909 /tmp/chirality-v3-ui-fixture-20260909
 */
import { createHash } from 'node:crypto';
import { chmod, mkdir, rm, writeFile } from 'node:fs/promises';
import { createServer } from 'node:http';
import path from 'node:path';

const projectId = 'chirality-app-dev';
const projectRoot = path.resolve(process.env.CHIRALITY_V3_FIXTURE_PROJECT_ROOT ?? '/tmp/chirality-v3-ui-fixture-20260909');
const stateRoot = path.resolve(process.env.CHIRALITY_V3_FIXTURE_STATE_ROOT ?? '/tmp/chirality-v3-ui-runtime-20260909');
const socketPath = path.join(stateRoot, 'runtime.sock');
const bootstrapTokenFile = path.join(stateRoot, 'auth', 'tokens', 'hosted-bootstrap-host.token');
const tokenFile = path.join(stateRoot, 'auth', 'tokens', `hosted-project-${projectId}.token`);
const bootstrapToken = 'controlled-v3-bootstrap-token';
const token = 'controlled-v3-runtime-token';
const now = '2026-09-09T00:00:00.000Z';
const sha = (text) => createHash('sha256').update(text).digest('hex');
const instructionPolicySha256 = sha('controlled-instruction-policy');
const nativePlanQualification = { adapterId: 'codex-app-server', providerId: 'openai', qualificationId: 'controlled-codex-native-plan', admissionSha256: sha('controlled-native-plan-admission'), evidenceClass: 'native-adapter-qualified' };

const workflowBody = '# Coordinate\n\nKeep one conversation while HELP_HUMAN coordinates bounded manager work.';
const projectWorkflowBody = '# Release Check\n\nCheck this project release through its local workflow.';
const skillBody = '# Bundled Review\n\nInspect the selected artifacts and report concrete findings.';
const workflow = {
  sourceRootId: 'bundled-workflows', source: 'bundled', kind: 'workflow', name: 'coordinate',
  qualifiedId: 'bundled-workflows:workflow:coordinate', description: 'Coordinate bounded manager work in this conversation.',
  central: true, compatibility: 'canonical', executionRoleIds: ['HELP_HUMAN', 'WORKING_ITEMS'], resources: [],
  metadata: { purpose: 'Coordinate a multi-stage undertaking', applicability: ['Cross-package work', 'Manager handoffs'] }
};
const projectWorkflow = {
  sourceRootId: 'project-workflows', source: 'project', kind: 'workflow', name: 'release-check',
  qualifiedId: 'project-workflows:workflow:release-check', description: 'Run this project’s release checks.',
  central: false, compatibility: 'canonical', executionRoleIds: ['WORKING_ITEMS'], resources: [],
  metadata: { purpose: 'Prepare this project for release', applicability: 'This project' }
};
const skill = {
  sourceRootId: 'bundled-skills', source: 'bundled', kind: 'skill', name: 'review',
  qualifiedId: 'bundled-skills:skill:review', description: 'Review project artifacts.',
  central: false, compatibility: 'canonical', executionRoleIds: ['HELP_HUMAN', 'HELPS_HUMANS', 'WORKING_ITEMS'], resources: []
};
const methods = [workflow, projectWorkflow, skill];
const methodBodies = new Map([
  [workflow.qualifiedId, workflowBody], [projectWorkflow.qualifiedId, projectWorkflowBody], [skill.qualifiedId, skillBody]
]);
const roles = [
  { id: 'HELP_HUMAN', agentType: 0, directEntry: true, defaultForNewChat: true, description: 'Coordinate work with the human.', instruction: 'agents/AGENT_HELP_HUMAN.md' },
  { id: 'HELPS_HUMANS', agentType: 1, directEntry: true, defaultForNewChat: false, description: 'Design methods and workflows.', instruction: 'agents/AGENT_HELPS_HUMANS.md' },
  { id: 'WORKING_ITEMS', agentType: 1, directEntry: true, defaultForNewChat: false, description: 'Manage bounded implementation work.', instruction: 'agents/AGENT_WORKING_ITEMS.md' },
  { id: 'TASK', agentType: 2, directEntry: false, defaultForNewChat: false, description: 'Execute a delegated bounded task.', instruction: 'agents/AGENT_TASK.md' }
];
const project = {
  projectId, displayName: 'Controlled v3 UI fixture', canonicalRoot: projectRoot,
  manifestPath: path.join(projectRoot, 'chirality.project.json'), manifestHash: sha('fixture-manifest'),
  registeredAt: now, approval: { approvedBy: 'controlled-fixture', approvalReference: 'test-only' },
  clientId: 'desktop', enabledAdapterIds: ['controlled-fixture'], legacySessionRoots: []
};
let projectRegistered = false;
let hostedStatus = { schema: 'chirality-hosted-bootstrap-status/v1', projectId, ceremony: 'ready-to-start', admission: 'unavailable', canStartLogin: true };
const sessions = new Map();
const histories = new Map();
const bases = new Map();
const transcripts = new Map();
const planRevisions = new Map();
const planClarifications = new Map();
let sequence = 0;

function qualified(reference) {
  if (reference?.sourceRootId && reference?.source && reference?.kind && reference?.name) return {
    sourceRootId: reference.sourceRootId, source: reference.source, kind: reference.kind, name: reference.name
  };
  const match = methods.find((method) => method.kind === reference?.kind && method.name === reference?.name);
  if (!match) return undefined;
  return { sourceRootId: match.sourceRootId, source: match.source, kind: match.kind, name: match.name };
}

function selectedContext(roleId, selectedMethods, interactionMode = 'chat', permissionMode = 'readOnly') {
  const selected = selectedMethods.map(qualified).filter(Boolean);
  const descriptors = selected.map((ref) => methods.find((method) => method.sourceRootId === ref.sourceRootId && method.kind === ref.kind && method.name === ref.name)).filter(Boolean);
  const supplied = [
    { kind: 'root', id: 'AGENTS.md', content: 'Central workflows are discoverable from the catalog. Load selected bodies only.', sha256: sha('root') },
    { kind: 'role', id: roleId, content: `# ${roleId}\n\nControlled active-role instructions.`, sha256: sha(roleId) },
    ...descriptors.map((method) => ({ kind: 'method-body', id: method.qualifiedId, content: methodBodies.get(method.qualifiedId), sha256: sha(method.qualifiedId), method: qualified(method) }))
  ];
  const basisId = `basis-${sha(JSON.stringify({ roleId, selected, interactionMode, permissionMode })).slice(0, 12)}`;
  return {
    schemaVersion: 'chirality.selected-context/v3', roleId, methods: descriptors, documents: [],
    dispositions: descriptors.map((method) => ({ method: qualified(method), selected: true, activeRoleCompatible: method.executionRoleIds.includes(roleId), eligibleRoleIds: method.executionRoleIds, route: 'primary' })),
    supplied, basisPreview: { id: basisId, sha256: sha(JSON.stringify(supplied)), instructionPolicySha256, sources: [], persisted: false }, compatibilityInputs: [], compatibilityMappings: []
  };
}

function orderedMethodUnion(existing, incoming) {
  const result = [...existing];
  for (const method of incoming) {
    if (!result.some((candidate) => candidate.sourceRootId === method.sourceRootId && candidate.source === method.source && candidate.kind === method.kind && candidate.name === method.name)) result.push(method);
  }
  return result;
}

function makeSession(body = {}) {
  const roleId = body.roleId ?? 'HELP_HUMAN';
  const sessionId = `sess-controlled-${++sequence}`;
  const selectedMethods = (body.selectedMethods ?? []).map(qualified).filter(Boolean);
  const initialContext = selectedContext(roleId, selectedMethods, body.interactionMode ?? 'chat', body.permissionMode ?? 'readOnly');
  const session = {
    schemaVersion: 'chirality.session/v3', projectId, projectRoot, sessionId, createdAt: now, updatedAt: now,
    role: roleId === 'HELP_HUMAN' ? 'agent0' : roleId === 'TASK' ? 'agent2' : 'agent1', roleId,
    agentType: roleId === 'HELP_HUMAN' ? 0 : roleId === 'TASK' ? 2 : 1,
    persona: body.persona ?? roleId, mode: body.mode ?? 'chat', interactionMode: body.interactionMode ?? 'chat',
    permissionMode: body.permissionMode ?? 'readOnly', selectedMethods, methodSelectionRevision: 0, instructionBasisId: initialContext.basisPreview.id,
    engineSelection: { adapterId: 'codex-app-server', providerId: 'openai', model: 'controlled-deterministic' }, status: 'idle'
  };
  sessions.set(sessionId, session);
  histories.set(sessionId, []);
  transcripts.set(sessionId, []);
  planRevisions.set(sessionId, []);
  planClarifications.set(sessionId, []);
  bases.set(sessionId, [{ schemaVersion: 'chirality.instruction-basis/v1', basisId: initialContext.basisPreview.id, sessionId, createdAt: now, roleId,
    interactionMode: session.interactionMode, permissionMode: session.permissionMode, selectedMethods, instructionPolicySha256,
    compatibilityInputs: [], compatibilityMappings: [], suppliedEntries: initialContext.supplied.map((entry) => ({ ...entry, origin: 'controlled-fixture', path: entry.id })), methodDispositions: initialContext.dispositions }]);
  return session;
}

function sendJson(response, value, status = 200) {
  response.writeHead(status, { 'content-type': 'application/json' });
  response.end(JSON.stringify(value));
}

async function readBody(request) {
  const chunks = [];
  for await (const chunk of request) chunks.push(Buffer.from(chunk));
  return chunks.length ? JSON.parse(Buffer.concat(chunks).toString('utf8')) : {};
}

await mkdir(projectRoot, { recursive: true });
await mkdir(path.join(projectRoot, '.chirality', 'workflows', 'release-check'), { recursive: true });
await writeFile(path.join(projectRoot, '.chirality', 'workflows', 'release-check', 'WORKFLOW.md'), `${projectWorkflowBody}\n`);
await mkdir(stateRoot, { recursive: true });
await mkdir(path.dirname(bootstrapTokenFile), { recursive: true });
await rm(socketPath, { force: true });
await writeFile(bootstrapTokenFile, `${bootstrapToken}\n`, { mode: 0o600 });
await chmod(bootstrapTokenFile, 0o600);
makeSession({ selectedMethods: [workflow] });

const server = createServer(async (request, response) => {
  try {
    const suppliedToken = request.headers.authorization?.replace(/^Bearer /, '');
    if (suppliedToken !== token && suppliedToken !== bootstrapToken) return sendJson(response, { code: 'UNAUTHORIZED', message: 'Fixture token required' }, 401);
    const url = new URL(request.url ?? '/', 'http://runtime.fixture');
    const pathname = url.pathname;
    const prefix = `/v1/projects/${projectId}`;
    if (pathname === '/v1/health') return sendJson(response, { apiVersion: 'v1', status: 'ok', daemonId: 'controlled-v3-fixture', pid: process.pid });
    if (pathname === '/v1/projects') return sendJson(response, { projects: projectRegistered ? [{ project, manifestDrift: false, adaptersEnabled: true }] : [] });
    if (pathname === '/v3/hosted-bootstrap/projects/initialize' && request.method === 'POST') {
      const body = await readBody(request);
      if (body.projectRoot !== projectRoot) return sendJson(response, { code: 'INVALID_REQUEST', message: 'Select the controlled fixture root' }, 400);
      const manifest = `${JSON.stringify({ schemaVersion: 'chirality.project/v1', projectId, displayName: 'Controlled v3 UI fixture' }, null, 2)}\n`;
      await writeFile(path.join(projectRoot, 'chirality.project.json'), manifest, { flag: 'wx' });
      project.manifestHash = sha(manifest);
      projectRegistered = true;
      await writeFile(tokenFile, `${token}\n`, { mode: 0o600 });
      await chmod(tokenFile, 0o600);
      return sendJson(response, { projectId, manifestHash: project.manifestHash });
    }
    if (pathname === `${prefix}/status`) return sendJson(response, { project, manifestDrift: false, adaptersEnabled: true });
    if (pathname === `/v3/projects/${projectId}/hosted-bootstrap/status`) return sendJson(response, hostedStatus);
    if (pathname === `/v3/projects/${projectId}/hosted-bootstrap/provider-network-consent` && request.method === 'POST') {
      const body = await readBody(request);
      if (body.consent !== true) return sendJson(response, { code: 'INVALID_REQUEST', message: 'Explicit consent is required' }, 400);
      hostedStatus = { ...hostedStatus, ceremony: 'ready-to-start', canStartLogin: true };
      return sendJson(response, hostedStatus);
    }
    if (pathname === `/v3/projects/${projectId}/hosted-bootstrap/login/start` && request.method === 'POST') {
      hostedStatus = { ...hostedStatus, ceremony: 'pending', admission: 'establishing', canStartLogin: false };
      return sendJson(response, { loginId: 'controlled-login', authUrl: 'https://auth.openai.com/controlled-fixture' });
    }
    if (pathname === `/v3/projects/${projectId}/hosted-bootstrap/login/cancel` && request.method === 'POST') {
      hostedStatus = { ...hostedStatus, ceremony: 'cancelled', admission: 'unavailable', canStartLogin: true };
      return sendJson(response, hostedStatus);
    }
    if (pathname === `${prefix}/roles`) return sendJson(response, { schemaVersion: 'chirality.roles/v3', defaultRole: 'HELP_HUMAN', roles });
    if (pathname === `${prefix}/methods` && request.method === 'GET') return sendJson(response, { schemaVersion: 'chirality.methods/v3', methods, malformedPackages: [] });
    if (pathname.startsWith(`${prefix}/methods/`) && request.method === 'GET') {
      const id = decodeURIComponent(pathname.slice(`${prefix}/methods/`.length));
      const method = methods.find((candidate) => candidate.qualifiedId === id);
      if (!method) return sendJson(response, { code: 'NOT_FOUND', message: 'Unknown controlled method' }, 404);
      const content = methodBodies.get(method.qualifiedId);
      return sendJson(response, { schemaVersion: 'chirality.method-inspection/v3', method, entrypoint: { content, sha256: sha(content) }, resources: [] });
    }
    if (pathname === `${prefix}/sessions` && request.method === 'GET') return sendJson(response, { sessions: [...sessions.values()] });
    if (pathname === `${prefix}/sessions` && request.method === 'POST') return sendJson(response, { session: makeSession(await readBody(request)) });
    const match = pathname.match(new RegExp(`^${prefix}/sessions/([^/]+)(.*)$`));
    if (!match) return sendJson(response, { code: 'NOT_FOUND', message: 'Unknown fixture route' }, 404);
    const sessionId = decodeURIComponent(match[1]);
    const suffix = match[2];
    const session = sessions.get(sessionId);
    if (!session) return sendJson(response, { code: 'SESSION_NOT_FOUND', message: 'Unknown controlled session' }, 404);
    if (suffix === '' && request.method === 'GET') return sendJson(response, { session });
    if (suffix === '' && request.method === 'DELETE') { sessions.delete(sessionId); return sendJson(response, { deleted: true, sessionId }); }
    if (suffix === '/boot') {
      session.status = 'idle'; session.engineSessionId ??= `engine-${sessionId}`;
      return sendJson(response, { session, boot: { engineSessionId: session.engineSessionId, adapterId: 'codex-app-server', providerId: 'openai', model: 'controlled-deterministic', bootFingerprint: sha(sessionId), runtimeFingerprint: { schemaVersion: 'controlled/v1', personaComposerVersion: 'runtime-v3', permissionPolicyVersion: 'read-only', managedDelegationPolicyVersion: 'none', subagentPolicyVersion: 'none', toolRegistryVersion: 'controlled', sdkPackageVersion: 'none' }, bootedAt: now } });
    }
    if (suffix === '/context/resolve') {
      const body = await readBody(request);
      return sendJson(response, selectedContext(body.roleId, body.methods ?? [], body.interactionMode, body.permissionMode));
    }
    if (suffix === '/methods' && request.method === 'PUT') {
      const body = await readBody(request); const nextRole = body.roleId ?? session.roleId;
      const requestedMethods = body.methods === undefined ? session.selectedMethods : body.methods.map(qualified).filter(Boolean);
      if (body.selectionMode === 'merge' && requestedMethods.length === 0) return sendJson(response, { code: 'INVALID_REQUEST', message: 'merge requires methods' }, 400);
      const nextMethods = body.selectionMode === 'merge' ? orderedMethodUnion(session.selectedMethods, requestedMethods) : requestedMethods;
      const context = selectedContext(nextRole, nextMethods, session.interactionMode, session.permissionMode);
      const changed = nextRole !== session.roleId || JSON.stringify(context.methods.map(qualified)) !== JSON.stringify(session.selectedMethods);
      session.roleId = nextRole; session.persona = nextRole; session.agentType = nextRole === 'HELP_HUMAN' ? 0 : nextRole === 'TASK' ? 2 : 1;
      session.role = nextRole === 'HELP_HUMAN' ? 'agent0' : nextRole === 'TASK' ? 'agent2' : 'agent1';
      session.selectedMethods = context.methods.map(qualified); session.methodSelectionRevision += changed ? 1 : 0;
      session.instructionBasisId = context.basisPreview.id;
      histories.get(sessionId).push({ schemaVersion: 'chirality.instruction-history/v1', historyId: `history-${session.methodSelectionRevision}`, sessionId, sequence: session.methodSelectionRevision, timestamp: now, type: 'selection.changed', roleId: nextRole, methods: session.selectedMethods });
      bases.get(sessionId).push({ schemaVersion: 'chirality.instruction-basis/v1', basisId: context.basisPreview.id, sessionId, createdAt: now, roleId: nextRole, interactionMode: session.interactionMode, permissionMode: session.permissionMode, selectedMethods: session.selectedMethods, instructionPolicySha256, compatibilityInputs: [], compatibilityMappings: [], suppliedEntries: context.supplied.map((entry) => ({ ...entry, origin: 'controlled-fixture', path: entry.id })), methodDispositions: context.dispositions });
      return sendJson(response, { schemaVersion: 'chirality.selected-methods/v3', sessionId, revision: session.methodSelectionRevision, methods: session.selectedMethods, basisPreview: context.basisPreview, transition: { status: changed ? 'prepared' : 'unchanged', successorAvailable: changed, ...(changed ? { preparationId: `prepared-${session.methodSelectionRevision}` } : {}) } });
    }
    if (suffix === '/replay') {
      const items = transcripts.get(sessionId);
      return sendJson(response, { session, events: [], malformedLineCount: 0, summary: { eventCount: 0, malformedLineCount: 0, eventTypeCounts: {} }, transcript: { sessionId, itemCount: items.length, items }, instructionHistory: histories.get(sessionId), instructionBases: bases.get(sessionId) });
    }
    if (suffix === '/native-plan/capability') return sendJson(response, { schemaVersion: 'chirality.native-plan-capability/v3', status: 'qualified', qualification: nativePlanQualification });
    if (suffix === '/native-plan/revisions') return sendJson(response, { schemaVersion: 'chirality.native-plan-revisions/v3', status: 'qualified', qualification: nativePlanQualification, revisions: planRevisions.get(sessionId) });
    if (suffix === '/native-plan/clarifications' && request.method === 'GET') return sendJson(response, { schemaVersion: 'chirality.native-plan-clarifications/v3', status: 'qualified', qualification: nativePlanQualification, clarifications: planClarifications.get(sessionId) });
    if (suffix === '/native-plan/clarifications/reply' && request.method === 'POST') {
      const body = await readBody(request);
      const pending = planClarifications.get(sessionId);
      const matchIndex = pending.findIndex((item) => item.requestId === body.requestId);
      if (matchIndex < 0) return sendJson(response, { code: 'NOT_FOUND', message: 'Unknown clarification request' }, 404);
      pending.splice(matchIndex, 1);
      return sendJson(response, { schemaVersion: 'chirality.native-plan-clarification-reply/v3', sessionId, requestId: body.requestId, sent: true });
    }
    if (suffix === '/turn') {
      const body = await readBody(request); const engineSessionId = `engine-${sessionId}-${session.methodSelectionRevision}`;
      session.engineSessionId = engineSessionId;
      session.status = 'completed';
      const items = transcripts.get(sessionId);
      const turn = items.length / 2 + 1;
      items.push({ key: `fixture-user-${turn}`, kind: 'message', role: 'user', status: 'accepted', title: 'You', timestamp: now, eventId: `fixture-user-${turn}`, eventType: 'message.accepted', turnId: `fixture-turn-${turn}`, text: body.message });
      items.push({ key: `fixture-assistant-${turn}`, kind: 'message', role: 'assistant', status: 'completed', title: 'Assistant', timestamp: now, eventId: `fixture-assistant-${turn}`, eventType: 'message.completed', turnId: `fixture-turn-${turn}`, text: `Controlled response for ${session.roleId}: ${body.message}` });
      if (body.interactionMode === 'native-plan') {
        const revision = planRevisions.get(sessionId).length + 1;
        planRevisions.get(sessionId).push({ revision, sourceEvent: { qualificationState: 'qualified', eventId: `fixture-plan-${revision}`, occurredAt: now, qualification: nativePlanQualification, plan: `# Controlled plan revision ${revision}\n\n1. Inspect the current project.\n2. Make the agreed change.\n3. Verify the result.` } });
        if (revision === 1) planClarifications.get(sessionId).push({ clientTurnId: `fixture-turn-${turn}`, providerThreadId: `thread-${sessionId}`, providerTurnId: `provider-turn-${turn}`, requestId: 7, itemId: 'fixture-clarification-7', questions: [
          { id: 'scope', header: 'Scope', question: 'Which scope should the plan cover?', options: [{ label: 'Current project', description: 'Keep the work inside the selected folder.' }, { label: 'Project and Runtime', description: 'Include the shared Runtime boundary.' }], isOther: true, isSecret: false },
          { id: 'token', header: 'Private value', question: 'Enter the test-only private value.', options: [], isOther: true, isSecret: true }
        ], isBlocking: true, autoResolutionMs: null });
      }
      response.writeHead(200, { 'content-type': 'text/event-stream', 'cache-control': 'no-cache' });
      response.end([
        `event: session:init\ndata: ${JSON.stringify({ engineSessionId, providerSpanId: `span-${session.methodSelectionRevision}`, adapterId: 'controlled-fixture', providerId: 'controlled', model: 'deterministic' })}\n`,
        `event: chat:complete\ndata: ${JSON.stringify({ text: `Controlled response for ${session.roleId}: ${body.message}` })}\n`,
        'event: session:complete\ndata: {}\n',
        'event: process:exit\ndata: {"exitCode":0}\n'
      ].join('\n'));
      return;
    }
    return sendJson(response, { code: 'NOT_FOUND', message: 'Unknown fixture route' }, 404);
  } catch (error) {
    return sendJson(response, { code: 'INVALID_REQUEST', message: error instanceof Error ? error.message : String(error) }, 400);
  }
});

await new Promise((resolve, reject) => { server.once('error', reject); server.listen(socketPath, resolve); });
await chmod(socketPath, 0o600);
process.stdout.write(`${JSON.stringify({ ready: true, socketPath, bootstrapTokenFile, runtimeDirectory: stateRoot, projectId, projectRoot, nextCommand: `CHIRALITY_RUNTIME_SOCKET_PATH=${socketPath} CHIRALITY_RUNTIME_TOKEN_FILE=${bootstrapTokenFile} CHIRALITY_RUNTIME_DIRECTORY=${stateRoot} npm run dev:next` })}\n`);

async function stop() {
  await new Promise((resolve) => server.close(resolve));
  await rm(socketPath, { force: true });
  process.exit(0);
}
process.once('SIGINT', stop);
process.once('SIGTERM', stop);
