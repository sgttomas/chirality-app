import { chmod, mkdtemp, mkdir, rm, stat, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { createServer, type IncomingMessage, type ServerResponse } from 'node:http';
import os from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import { RuntimeClient } from '@chirality/runtime-client';
import type { RuntimeSessionRecordV3, SessionReplayResponse } from '@chirality/runtime-contracts';
import type {
  MethodDescriptor,
  QualifiedMethodReference,
  ResolveSelectedContextResponse,
  RoleDescriptor
} from '@chirality/runtime-contracts/v3';
import { RuntimeDaemonHarnessPort } from '../../lib/runtime-client/runtime-daemon-harness-port';
import {
  installDaemonHarnessPort,
  resetDaemonHarnessPortForTests
} from '../../lib/runtime-client/daemon-harness-port';
import * as rolesRoute from '../../app/api/harness/roles/route';
import * as methodsRoute from '../../app/api/harness/methods/route';
import * as resolveRoute from '../../app/api/harness/session/[id]/context/resolve/route';
import * as replaceRoute from '../../app/api/harness/session/[id]/methods/route';
import * as capabilityRoute from '../../app/api/harness/session/[id]/native-plan/capability/route';
import * as revisionsRoute from '../../app/api/harness/session/[id]/native-plan/revisions/route';
import * as exportRoute from '../../app/api/harness/session/[id]/native-plan/export/route';
import * as replayRoute from '../../app/api/harness/session/[id]/events/route';
import * as turnRoute from '../../app/api/harness/turn/route';

const roots: string[] = [];

async function readBody(request: IncomingMessage): Promise<unknown> {
  const chunks: Buffer[] = [];
  for await (const chunk of request) chunks.push(Buffer.from(chunk));
  return chunks.length === 0 ? undefined : JSON.parse(Buffer.concat(chunks).toString('utf8'));
}

function json(response: ServerResponse, value: unknown): void {
  response.writeHead(200, { 'content-type': 'application/json' });
  response.end(JSON.stringify(value));
}

afterEach(async () => {
  resetDaemonHarnessPortForTests();
  await Promise.all(roots.splice(0).map((root) => rm(root, { recursive: true, force: true })));
});

describe('v3 App proxy to RuntimeClient transport', () => {
  it('preserves registry identity, ordered context, attachment separation, native truth, and replay basis', async () => {
    const root = await mkdtemp(path.join(os.tmpdir(), 'chirality-v3-app-proxy-'));
    roots.push(root);
    const projectRoot = path.join(root, 'project');
    await mkdir(projectRoot);
    const instructionRoot = path.join(root, 'instruction-root');
    await mkdir(instructionRoot);
    const tokenFile = path.join(root, 'runtime.token');
    const socketPath = path.join(root, 'runtime.sock');
    await writeFile(tokenFile, 'test-token\n');
    await chmod(tokenFile, 0o600);

    const sessionId = 'sess-v3-proxy';
    const methodProject = { sourceRootId: 'project-skills', source: 'project', kind: 'skill', name: 'review' } as const satisfies QualifiedMethodReference;
    const methodUser = { sourceRootId: 'user-skills', source: 'user', kind: 'skill', name: 'review' } as const satisfies QualifiedMethodReference;
    const methodWorkflow = { sourceRootId: 'bundled-workflows', source: 'bundled', kind: 'workflow', name: 'coordinate' } as const satisfies QualifiedMethodReference;
    const descriptors = [
      { ...methodProject, qualifiedId: 'project-skills:skill:review', description: 'Project review', central: false, compatibility: 'canonical', executionRoleIds: ['HELP_HUMAN'], resources: [] },
      { ...methodUser, qualifiedId: 'user-skills:skill:review', description: 'User review', central: false, compatibility: 'canonical', executionRoleIds: ['HELP_HUMAN'], resources: [] },
      { ...methodWorkflow, qualifiedId: 'bundled-workflows:workflow:coordinate', description: 'Coordinate with a manager', central: true, compatibility: 'canonical', executionRoleIds: ['HELP_HUMAN', 'WORKING_ITEMS'], resources: [] }
    ] as const satisfies readonly MethodDescriptor[];
    const roles = [
      { id: 'HELP_HUMAN', agentType: 0, directEntry: true, defaultForNewChat: true, description: 'Dynamic helper', instruction: 'agents/AGENT_HELP_HUMAN.md' },
      { id: 'HELPS_HUMANS', agentType: 1, directEntry: true, defaultForNewChat: false, description: 'Design', instruction: 'agents/AGENT_HELPS_HUMANS.md' },
      { id: 'WORKING_ITEMS', agentType: 1, directEntry: true, defaultForNewChat: false, description: 'Work', instruction: 'agents/AGENT_WORKING_ITEMS.md' },
      { id: 'TASK', agentType: 2, directEntry: false, defaultForNewChat: false, description: 'Task', instruction: 'agents/AGENT_TASK.md' }
    ] as const satisfies readonly RoleDescriptor[];
    const captured = new Map<string, unknown>();
    const project = {
      projectId: 'chirality-app-dev', displayName: 'App', canonicalRoot: projectRoot,
      manifestPath: path.join(projectRoot, 'chirality.project.json'), manifestHash: 'hash',
      registeredAt: '2026-09-09T00:00:00.000Z', approval: { approvedBy: 'human', approvalReference: 'approved' },
      clientId: 'desktop', enabledAdapterIds: ['claude-agent-sdk'], legacySessionRoots: []
    };
    const session = {
      schemaVersion: 'chirality.session/v3', projectId: project.projectId, projectRoot,
      sessionId, createdAt: '2026-09-09T00:00:00.000Z', updatedAt: '2026-09-09T00:00:00.000Z',
      role: 'agent0', roleId: 'HELP_HUMAN', agentType: 0, persona: 'PROJECT_SETUP', mode: 'chat',
      interactionMode: 'chat', permissionMode: 'readOnly', selectedMethods: [methodWorkflow],
      methodSelectionRevision: 2, instructionBasisId: 'basis-frozen-2',
      engineSelection: { adapterId: 'claude-agent-sdk', providerId: 'anthropic', model: 'model' }, status: 'idle'
    } satisfies RuntimeSessionRecordV3;
    const resolvedContext = {
      schemaVersion: 'chirality.selected-context/v3', roleId: 'HELP_HUMAN', methods: [descriptors[2], descriptors[0]], documents: [],
      dispositions: [
        { method: methodWorkflow, selected: true, activeRoleCompatible: true, eligibleRoleIds: ['HELP_HUMAN', 'WORKING_ITEMS'], route: 'primary' },
        { method: methodProject, selected: true, activeRoleCompatible: true, eligibleRoleIds: ['HELP_HUMAN'], route: 'primary' }
      ],
      supplied: [
        { kind: 'root', id: 'AGENTS.md', content: 'root overview', sha256: 'a'.repeat(64) },
        { kind: 'role', id: 'HELP_HUMAN', content: 'only active helper body', sha256: 'b'.repeat(64) },
        { kind: 'method-body', id: descriptors[2].qualifiedId, content: 'manager coordination workflow', sha256: 'c'.repeat(64), method: methodWorkflow },
        { kind: 'method-body', id: descriptors[0].qualifiedId, content: 'project review body', sha256: 'd'.repeat(64), method: methodProject }
      ],
      executionRoots: {
        workingRoot: {
          path: projectRoot,
          origin: 'registered-project-root',
          identitySha256: createHash('sha256').update(JSON.stringify({ schema: 'chirality.execution-root/v1', path: projectRoot, origin: 'registered-project-root', dev: `${(await stat(projectRoot)).dev}`, ino: `${(await stat(projectRoot)).ino}` })).digest('hex')
        },
        toolRoot: {
          path: instructionRoot,
          origin: 'trusted-runtime-instruction-root',
          identitySha256: createHash('sha256').update(JSON.stringify({ schema: 'chirality.execution-root/v1', path: instructionRoot, origin: 'trusted-runtime-instruction-root', dev: `${(await stat(instructionRoot)).dev}`, ino: `${(await stat(instructionRoot)).ino}` })).digest('hex')
        }
      },
      basisPreview: { id: 'basis-preview', sha256: 'e'.repeat(64), instructionPolicySha256: '9'.repeat(64), sources: [], persisted: false }, compatibilityInputs: [], compatibilityMappings: []
    } as const satisfies ResolveSelectedContextResponse;

    const server = createServer(async (request, response) => {
      const url = request.url ?? '';
      if (url.endsWith('/status')) return json(response, { project, manifestDrift: false, adaptersEnabled: true });
      if (url.endsWith('/roles')) return json(response, { schemaVersion: 'chirality.roles/v3', defaultRole: 'HELP_HUMAN', roles });
      if (url.endsWith('/methods') && request.method === 'GET') return json(response, { schemaVersion: 'chirality.methods/v3', methods: descriptors, malformedPackages: [] });
      if (url.endsWith('/context/resolve')) {
        captured.set('resolve', await readBody(request));
        return json(response, resolvedContext);
      }
      if (url.endsWith('/methods') && request.method === 'PUT') {
        captured.set('replace', await readBody(request));
        return json(response, {
          schemaVersion: 'chirality.selected-methods/v3', sessionId, revision: 3,
          methods: [methodProject, methodUser],
          basisPreview: { id: 'basis-next', sha256: 'f'.repeat(64), instructionPolicySha256: '9'.repeat(64), sources: [], persisted: false },
          transition: { status: 'prepared', successorAvailable: true, preparationId: 'prepare-3' }
        });
      }
      if (url.endsWith('/native-plan/capability')) return json(response, { schemaVersion: 'chirality.native-plan-capability/v3', status: 'unavailable', reason: 'No qualified adapter' });
      if (url.endsWith('/native-plan/revisions')) return json(response, { schemaVersion: 'chirality.native-plan-revisions/v3', status: 'unavailable', reason: 'No qualified adapter', revisions: [] });
      if (url.endsWith('/native-plan/export')) {
        captured.set('export', await readBody(request));
        return json(response, { schemaVersion: 'chirality.native-plan-export/v3', sessionId, revision: 1, targetRelativePath: 'plans/current.json', sha256: '1'.repeat(64) });
      }
      if (url.endsWith('/replay')) return json(response, {
        session, events: [], malformedLineCount: 0,
        summary: { eventCount: 0, malformedLineCount: 0, eventTypeCounts: {} },
        transcript: { sessionId, itemCount: 0, items: [] },
        instructionHistory: [{ schemaVersion: 'chirality.instruction-history/v1', historyId: 'history-1', sessionId, sequence: 1, timestamp: '2026-09-09T00:00:00.000Z', type: 'instruction-basis.resolved', basisId: 'basis-frozen-2' }],
        instructionBases: [{ schemaVersion: 'chirality.instruction-basis/v1', basisId: 'basis-frozen-2', sessionId, createdAt: '2026-09-09T00:00:00.000Z', roleId: 'HELP_HUMAN', interactionMode: 'chat', permissionMode: 'readOnly', selectedMethods: [methodWorkflow], compatibilityInputs: [], compatibilityMappings: [], suppliedEntries: [], methodDispositions: [] }]
      } satisfies SessionReplayResponse);
      if (url.endsWith('/turn')) {
        captured.set('turn', await readBody(request));
        response.writeHead(200, { 'content-type': 'text/event-stream' });
        response.end('event: process:exit\ndata: {"exitCode":0}\n\n');
        return;
      }
      response.writeHead(404).end();
    });
    await new Promise<void>((resolve, reject) => { server.once('error', reject); server.listen(socketPath, resolve); });
    try {
      installDaemonHarnessPort(new RuntimeDaemonHarnessPort(
        new RuntimeClient({ socketPath, tokenFile, timeoutMs: 2_000 }),
        'chirality-app-dev', projectRoot
      ));
      const encodedRoot = encodeURIComponent(projectRoot);
      const rolesResponse = await rolesRoute.GET(new Request(`http://localhost/api/harness/roles?projectRoot=${encodedRoot}`));
      const rolesPayload = await rolesResponse.json();
      expect(rolesPayload.defaultRole).toBe('HELP_HUMAN');
      expect(rolesPayload.roles).toHaveLength(4);
      expect(rolesPayload.roles[0]).toMatchObject({ id: 'HELP_HUMAN', description: 'Dynamic helper' });
      expect(rolesPayload.roles.filter((role: { directEntry: boolean }) => role.directEntry)).toHaveLength(3);
      const methodsResponse = await methodsRoute.GET(new Request(`http://localhost/api/harness/methods?projectRoot=${encodedRoot}&kind=skill&query=review`));
      expect((await methodsResponse.json()).methods.map((method: { qualifiedId: string }) => method.qualifiedId)).toEqual([
        'project-skills:skill:review', 'user-skills:skill:review'
      ]);

      const selection = [methodWorkflow, methodProject];
      const resolveResponse = await resolveRoute.POST(new Request('http://localhost/resolve', {
        method: 'POST', headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ roleId: 'HELP_HUMAN', interactionMode: 'chat', permissionMode: 'readOnly', methods: selection })
      }), { params: Promise.resolve({ id: sessionId }) });
      const resolved = await resolveResponse.json();
      expect(resolved.roleId).toBe('HELP_HUMAN');
      expect(resolved.supplied.map((entry: { content: string }) => entry.content)).toEqual([
        'root overview', 'only active helper body', 'manager coordination workflow', 'project review body'
      ]);
      expect(captured.get('resolve')).toMatchObject({ roleId: 'HELP_HUMAN', methods: selection });

      const replaceResponse = await replaceRoute.PUT(new Request('http://localhost/methods', {
        method: 'PUT', headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ expectedBasisId: 'basis-frozen-2', expectedRevision: 2, roleId: 'WORKING_ITEMS', boundaryConfirmed: true, selectionMode: 'merge', methods: [methodProject, methodUser] })
      }), { params: Promise.resolve({ id: sessionId }) });
      expect(captured.get('replace')).toEqual({ expectedBasisId: 'basis-frozen-2', expectedRevision: 2, roleId: 'WORKING_ITEMS', boundaryConfirmed: true, selectionMode: 'merge', methods: [methodProject, methodUser] });
      expect(await replaceResponse.json()).toMatchObject({ transition: { status: 'prepared', successorAvailable: true, preparationId: 'prepare-3' } });

      const capability = await capabilityRoute.GET(new Request('http://localhost/capability'), { params: Promise.resolve({ id: sessionId }) });
      expect(await capability.json()).toMatchObject({ status: 'unavailable', reason: 'No qualified adapter' });
      const revisions = await revisionsRoute.GET(new Request('http://localhost/revisions'), { params: Promise.resolve({ id: sessionId }) });
      expect(await revisions.json()).toMatchObject({ status: 'unavailable', revisions: [] });

      await exportRoute.POST(new Request('http://localhost/export', {
        method: 'POST', headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ revision: 1, targetRelativePath: 'plans/current.json', overwrite: true })
      }), { params: Promise.resolve({ id: sessionId }) });
      expect(captured.get('export')).toEqual({ revision: 1, targetRelativePath: 'plans/current.json', overwrite: true });

      const replay = await replayRoute.GET(new Request('http://localhost/replay'), { params: Promise.resolve({ id: sessionId }) });
      const replayPayload = await replay.json();
      expect(replayPayload.session).toMatchObject({ persona: 'PROJECT_SETUP', roleId: 'HELP_HUMAN', instructionBasisId: 'basis-frozen-2' });
      expect(replayPayload.instructionHistory).toEqual([expect.objectContaining({ type: 'instruction-basis.resolved', basisId: 'basis-frozen-2' })]);
      expect(replayPayload.instructionBases).toEqual([expect.objectContaining({ basisId: 'basis-frozen-2', roleId: 'HELP_HUMAN' })]);

      const turn = await turnRoute.POST(new Request('http://localhost/turn', {
        method: 'POST', headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ sessionId, message: 'Directions typed normally', attachments: ['/tmp/report.pdf'], permissionMode: 'readOnly' })
      }));
      expect(turn.status).toBe(200);
      await turn.text();
      expect(captured.get('turn')).toEqual({ message: 'Directions typed normally', attachments: ['/tmp/report.pdf'], permissionMode: 'readOnly' });
    } finally {
      await new Promise<void>((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
    }
  });
});
