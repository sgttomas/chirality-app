import { describe, expect, it, vi } from 'vitest';
import { mkdtemp, realpath, rm, symlink } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { tmpdir } from 'node:os';

import { RuntimeError, type RuntimeSessionRecord } from '@chirality/runtime-contracts';
import { RuntimeTransportError, type RuntimeClient, type RuntimeStream } from '@chirality/runtime-client';
import type { UIEvent } from '@chirality/runtime-contracts/types';

import {
  RuntimeDaemonHarnessPort,
  RuntimeHostedBootstrapPort,
  createRuntimeDaemonHarnessPortFromEnvironment,
  createRuntimeHostedBootstrapPortFromEnvironment
} from '../../lib/runtime-client/runtime-daemon-harness-port';

const project = {
  projectId: 'chirality-app-dev',
  displayName: 'Chirality App Development',
  canonicalRoot: '/repo/projects/chirality-app-dev',
  manifestPath: '/repo/projects/chirality-app-dev/chirality.project.json',
  manifestHash: 'abc123',
  registeredAt: '2026-07-22T00:00:00.000Z',
  approval: {
    approvedBy: 'owner',
    approvalReference: 'D-APP-73'
  },
  clientId: 'desktop-chirality-app-dev',
  enabledAdapterIds: ['claude-agent-sdk', 'pi'],
  legacySessionRoots: ['frontend/.chirality/sessions']
} as const;

const session: RuntimeSessionRecord = {
  schemaVersion: 'chirality.session/v2',
  projectId: project.projectId,
  projectRoot: project.canonicalRoot,
  sessionId: 'sess-1',
  createdAt: '2026-07-22T00:00:00.000Z',
  updatedAt: '2026-07-22T00:00:00.000Z',
  role: 'agent1',
  persona: 'WORKING_ITEMS',
  mode: 'chat',
  engineSelection: {
    adapterId: 'claude-agent-sdk',
    providerId: 'anthropic',
    model: 'configured-by-daemon'
  },
  status: 'idle'
};

function client(overrides: Partial<RuntimeClient> = {}): RuntimeClient {
  return {
    resolveProjectByRoot: vi.fn().mockResolvedValue(project),
    createSession: vi.fn().mockResolvedValue(session),
    resolveSessionOwner: vi.fn().mockResolvedValue({ project, session }),
    listSessions: vi.fn().mockResolvedValue([session]),
    getSession: vi.fn().mockResolvedValue(session),
    deleteSession: vi.fn().mockResolvedValue({
      deleted: true,
      sessionId: session.sessionId
    }),
    requestJson: vi.fn(),
    bootSession: vi.fn(),
    replaySession: vi.fn(),
    turnSession: vi.fn(),
    interruptSession: vi.fn().mockResolvedValue({
      interrupted: true,
      sessionId: session.sessionId
    }),
    decidePermission: vi.fn().mockResolvedValue({
      accepted: true,
      requestId: 'tool-1',
      decision: 'allow'
    }),
    projectStatus: vi.fn().mockResolvedValue({
      project,
      manifestDrift: false,
      adaptersEnabled: true
    }),
    listProjects: vi.fn().mockResolvedValue([
      {
        project,
        manifestDrift: false,
        adaptersEnabled: true
      }
    ]),
    listRoles: vi.fn().mockResolvedValue({
      schemaVersion: 'chirality.roles/v3',
      defaultRole: 'HELP_HUMAN',
      roles: [
        { id: 'HELP_HUMAN', agentType: 0, directEntry: true, defaultForNewChat: true, description: 'help', instruction: 'agents/AGENT_HELP_HUMAN.md' },
        { id: 'WORKING_ITEMS', agentType: 1, directEntry: true, defaultForNewChat: false, description: 'work', instruction: 'agents/AGENT_WORKING_ITEMS.md' },
        { id: 'TASK', agentType: 2, directEntry: false, defaultForNewChat: false, description: 'task', instruction: 'agents/AGENT_TASK.md' }
      ]
    }),
    scaffold: vi.fn(),
    ...overrides
  } as unknown as RuntimeClient;
}

describe('RuntimeDaemonHarnessPort', () => {
  it('fails closed when the Desktop host omits daemon authentication paths', () => {
    expect(() => createRuntimeDaemonHarnessPortFromEnvironment({})).toThrowError(
      expect.objectContaining({
        type: 'ENGINE_UNAVAILABLE',
        status: 503
      })
    );
  });

  it('requires a fixed app-dev project ID and root in the Desktop environment', () => {
    expect(() =>
      createRuntimeDaemonHarnessPortFromEnvironment({
        CHIRALITY_RUNTIME_SOCKET_PATH: '/runtime/control.sock',
        CHIRALITY_RUNTIME_TOKEN_FILE: '/runtime/project.token',
        CHIRALITY_RUNTIME_PROJECT_ID: 'pec',
        CHIRALITY_RUNTIME_PROJECT_ROOT: project.canonicalRoot
      })
    ).toThrowError(expect.objectContaining({ type: 'ENGINE_UNAVAILABLE' }));

    expect(() =>
      createRuntimeDaemonHarnessPortFromEnvironment({
        CHIRALITY_RUNTIME_SOCKET_PATH: '/runtime/control.sock',
        CHIRALITY_RUNTIME_TOKEN_FILE: '/runtime/auth/tokens/operator.token',
        CHIRALITY_RUNTIME_PROJECT_ID: project.projectId,
        CHIRALITY_RUNTIME_PROJECT_ROOT: project.canonicalRoot
      })
    ).toThrowError(expect.objectContaining({ type: 'ENGINE_UNAVAILABLE' }));

    expect(() =>
      createRuntimeDaemonHarnessPortFromEnvironment({
        CHIRALITY_RUNTIME_SOCKET_PATH: '/runtime/control.sock',
        CHIRALITY_RUNTIME_TOKEN_FILE: '/runtime/project.token',
        CHIRALITY_RUNTIME_PROJECT_ID: project.projectId
      })
    ).toThrowError(expect.objectContaining({ type: 'ENGINE_UNAVAILABLE' }));

    expect(() =>
      createRuntimeDaemonHarnessPortFromEnvironment({
        CHIRALITY_RUNTIME_SOCKET_PATH: '/runtime/control.sock',
        CHIRALITY_RUNTIME_TOKEN_FILE: '/runtime/auth/tokens/project-app-dev.token',
        CHIRALITY_RUNTIME_PROJECT_ID: project.projectId,
        CHIRALITY_RUNTIME_PROJECT_ROOT: project.canonicalRoot
      })
    ).not.toThrow();
  });

  it('builds the hosted bootstrap port from the App-owned service paths', () => {
    // The App exports the per-launch client token as CHIRALITY_RUNTIME_TOKEN_FILE;
    // the retired bootstrap-token variable is not read.
    expect(() =>
      createRuntimeHostedBootstrapPortFromEnvironment({
        CHIRALITY_RUNTIME_SOCKET_PATH: '/runtime/control.sock',
        CHIRALITY_RUNTIME_TOKEN_FILE: '/runtime/client-token',
        CHIRALITY_RUNTIME_DIRECTORY: '/runtime'
      })
    ).not.toThrow();
    expect(() =>
      createRuntimeHostedBootstrapPortFromEnvironment({
        CHIRALITY_RUNTIME_SOCKET_PATH: '/runtime/control.sock',
        CHIRALITY_RUNTIME_BOOTSTRAP_TOKEN_FILE: '/runtime/client-token',
        CHIRALITY_RUNTIME_DIRECTORY: '/runtime'
      })
    ).toThrowError(expect.objectContaining({ type: 'ENGINE_UNAVAILABLE', status: 503 }));
  });

  it('resolves the registered project and leaves engine defaults to the daemon', async () => {
    const runtimeClient = client();
    const port = new RuntimeDaemonHarnessPort(runtimeClient);

    await expect(
      port.createSession({
        projectRoot: project.canonicalRoot,
        persona: 'WORKING_ITEMS',
        mode: 'chat'
      })
    ).resolves.toEqual({ session });
    expect(runtimeClient.createSession).toHaveBeenCalledWith(
      project.projectId,
      {
        projectId: project.projectId,
        persona: 'WORKING_ITEMS',
        mode: 'chat'
      },
      undefined
    );
    expect(runtimeClient.resolveProjectByRoot).not.toHaveBeenCalled();
  });

  it('passes declared context and write-target tri-state through to Runtime session creation', async () => {
    const runtimeClient = client();
    const port = new RuntimeDaemonHarnessPort(runtimeClient);

    await port.createSession({
      projectRoot: project.canonicalRoot,
      persona: 'WORKING_ITEMS',
      declaredContext: [],
      allowedWriteTargets: []
    });
    expect(runtimeClient.createSession).toHaveBeenLastCalledWith(
      project.projectId,
      expect.objectContaining({
        declaredContext: [],
        allowedWriteTargets: []
      }),
      undefined
    );

    const declaredContext = [`${project.canonicalRoot}/execution/PKG-01`];
    const allowedWriteTargets = [`${project.canonicalRoot}/execution/PKG-01/output.md`];
    await port.createSession({
      projectRoot: project.canonicalRoot,
      persona: 'WORKING_ITEMS',
      declaredContext,
      allowedWriteTargets
    });
    expect(runtimeClient.createSession).toHaveBeenLastCalledWith(
      project.projectId,
      expect.objectContaining({ declaredContext, allowedWriteTargets }),
      undefined
    );

    await port.createSession({
      projectRoot: project.canonicalRoot,
      persona: 'WORKING_ITEMS'
    });
    const finalRequest = vi.mocked(runtimeClient.createSession).mock.calls.at(-1)?.[1];
    expect(finalRequest).not.toHaveProperty('declaredContext');
    expect(finalRequest).not.toHaveProperty('allowedWriteTargets');
  });

  it('forwards the session-fixed modelSelection to Runtime createSession and keeps reasoningEffort on returned records', async () => {
    const created: RuntimeSessionRecord = {
      ...session,
      engineSelection: { adapterId: 'codex-app-server', providerId: 'openai', model: 'gpt-alt' },
      reasoningEffort: 'low'
    };
    const runtimeClient = client({
      createSession: vi.fn().mockResolvedValue(created),
      replaySession: vi.fn().mockResolvedValue({ session: created, events: [], malformedLineCount: 0 })
    });
    const port = new RuntimeDaemonHarnessPort(runtimeClient);

    const modelSelection = { model: 'gpt-alt', reasoningEffort: 'low' };
    await expect(port.createSession({
      projectRoot: project.canonicalRoot,
      persona: 'WORKING_ITEMS',
      roleId: 'WORKING_ITEMS',
      mode: 'chat',
      modelSelection
    })).resolves.toEqual({ session: created });
    expect(runtimeClient.createSession).toHaveBeenLastCalledWith(
      project.projectId,
      {
        projectId: project.projectId,
        roleId: 'WORKING_ITEMS',
        persona: 'WORKING_ITEMS',
        mode: 'chat',
        modelSelection
      },
      undefined
    );

    await port.createSession({ projectRoot: project.canonicalRoot, persona: 'WORKING_ITEMS' });
    expect(vi.mocked(runtimeClient.createSession).mock.calls.at(-1)?.[1]).not.toHaveProperty('modelSelection');

    // Replay keeps the additive field: the App renders it in the lens.
    await expect(port.replaySession('sess-1')).resolves.toMatchObject({
      session: { engineSelection: { model: 'gpt-alt' }, reasoningEffort: 'low' }
    });
  });

  it('maps legacy dontAsk creation to canonical readOnly unless permissionMode is explicit', async () => {
    const runtimeClient = client();
    const port = new RuntimeDaemonHarnessPort(runtimeClient);

    await port.createSession({
      projectRoot: project.canonicalRoot,
      persona: 'HELP_HUMAN',
      mode: 'dontAsk'
    });
    expect(runtimeClient.createSession).toHaveBeenLastCalledWith(
      project.projectId,
      expect.objectContaining({ mode: 'dontAsk', permissionMode: 'readOnly' }),
      undefined
    );

    await port.createSession({
      projectRoot: project.canonicalRoot,
      persona: 'HELP_HUMAN',
      mode: 'dontAsk',
      permissionMode: 'bypass'
    });
    expect(runtimeClient.createSession).toHaveBeenLastCalledWith(
      project.projectId,
      expect.objectContaining({ mode: 'dontAsk', permissionMode: 'bypass' }),
      undefined
    );
  });

  it('preserves canonical UI events and forwards the per-turn model pair; cancel only unsubscribes', async () => {
    const event: UIEvent = {
      type: 'chat:delta',
      data: { text: 'local evidence' }
    };
    const cancel = vi.fn();
    const stream: RuntimeStream = {
      async *[Symbol.asyncIterator]() {
        yield event;
      },
      cancel
    };
    const runtimeClient = client({
      turnSession: vi.fn().mockResolvedValue(stream)
    });
    const port = new RuntimeDaemonHarnessPort(runtimeClient);
    const running = await port.turn({
      sessionId: session.sessionId,
      message: 'inspect',
      turnId: 'submitted-turn',
      opts: { tools: ['read_file'] },
      attachments: ['/repo/fixture.txt'],
      model: 'gpt-alt',
      reasoningEffort: 'low'
    });

    const received: UIEvent[] = [];
    for await (const item of running.events) received.push(item);
    expect(received).toEqual([event]);
    expect(runtimeClient.turnSession).toHaveBeenCalledWith(
      project.projectId,
      session.sessionId,
      {
        message: 'inspect',
        turnId: 'submitted-turn',
        opts: { tools: ['read_file'] },
        attachments: ['/repo/fixture.txt'],
        model: 'gpt-alt',
        reasoningEffort: 'low'
      },
      undefined
    );

    // Runtime owns the turn (D-GOV-43): dropping the observer must not
    // interrupt Codex. Stop is a separate, explicit interrupt call.
    await running.cancel();
    expect(cancel).toHaveBeenCalledOnce();
    expect(runtimeClient.interruptSession).not.toHaveBeenCalled();

    await port.interrupt({ sessionId: session.sessionId });
    expect(runtimeClient.interruptSession).toHaveBeenCalledWith(
      project.projectId,
      session.sessionId,
      undefined
    );
  });

  it('attaches to the Runtime turn registry and proxies turn state, requests and answers', async () => {
    const frames = [
      { type: 'harness:event', data: { type: 'message.delta', text: 'partial' }, seq: 3 },
      { type: 'harness:event', data: { type: 'turn.completed' }, seq: 4 }
    ];
    const attachCancel = vi.fn();
    const attachSessionTurn = vi.fn().mockResolvedValue({
      async *[Symbol.asyncIterator]() {
        for (const frame of frames) yield frame;
      },
      cancel: attachCancel
    });
    const turnState = { active: true, turnId: 'turn-1', lastSeq: 4, startedAt: '2026-09-12T00:00:00.000Z' };
    const requests = { requests: [{ requestId: 'req-1', method: 'item/tool/requestUserInput', kind: 'userInput', request: {}, receivedAt: '2026-09-12T00:00:01.000Z' }] };
    const answered = { accepted: true, requestId: 'req-1' };
    const runtimeClient = client({
      attachSessionTurn,
      sessionTurnState: vi.fn().mockResolvedValue(turnState),
      listSessionRequests: vi.fn().mockResolvedValue(requests),
      answerSessionRequest: vi.fn().mockResolvedValue(answered)
    });
    const port = new RuntimeDaemonHarnessPort(runtimeClient);
    const controller = new AbortController();

    const subscription = await port.attachTurn(session.sessionId, 2, { signal: controller.signal, turnId: 'turn-1' });
    const received: unknown[] = [];
    for await (const item of subscription.events) received.push(item);
    expect(received).toEqual(frames);
    expect(attachSessionTurn).toHaveBeenCalledWith(project.projectId, session.sessionId, { after: 2, turnId: 'turn-1' }, controller.signal);
    await subscription.cancel();
    await subscription.cancel();
    expect(attachCancel).toHaveBeenCalledOnce();
    expect(runtimeClient.interruptSession).not.toHaveBeenCalled();

    await expect(port.turnState(session.sessionId)).resolves.toEqual(turnState);
    await expect(port.listRequests(session.sessionId)).resolves.toEqual(requests);
    const answer = { kind: 'userInput' as const, answers: { q1: { answers: ['yes'] } } };
    await expect(port.answerRequest(session.sessionId, 'req-1', answer)).resolves.toEqual(answered);
    expect(runtimeClient.answerSessionRequest).toHaveBeenCalledWith(project.projectId, session.sessionId, 'req-1', answer, undefined);
  });

  it('maps a Runtime TURN_NOT_ACTIVE rejection on attach into the route error vocabulary', async () => {
    const attachSessionTurn = vi.fn().mockRejectedValue(
      new RuntimeError('NOT_FOUND', 'No active or retained turn', 404, { reason: 'TURN_NOT_ACTIVE' })
    );
    const port = new RuntimeDaemonHarnessPort(client({ attachSessionTurn }));
    await expect(port.attachTurn(session.sessionId, 0)).rejects.toMatchObject({ status: 404 });
  });

  it('maps permission IDs and filters Type-2 agents from direct chat', async () => {
    const runtimeClient = client();
    const port = new RuntimeDaemonHarnessPort(runtimeClient);

    await expect(
      port.decidePermission({
        sessionId: session.sessionId,
        toolUseId: 'tool-1',
        verdict: 'allow'
      })
    ).resolves.toEqual({ ok: true, decided: true });
    expect(runtimeClient.decidePermission).toHaveBeenCalledWith(
      project.projectId,
      session.sessionId,
      {
        requestId: 'tool-1',
        decision: 'allow'
      },
      undefined
    );

    await expect(port.listAgents({ directChatOnly: true })).resolves.toEqual({
      agents: [
        { name: 'HELP_HUMAN', type: 0, class: 'PERSONA' },
        { name: 'WORKING_ITEMS', type: 1, class: 'PERSONA' }
      ]
    });
  });

  it('passes native Plan clarification reads and replies through the fixed project binding', async () => {
    const clarificationResponse = {
      schemaVersion: 'chirality.native-plan-clarifications/v3' as const,
      status: 'qualified' as const,
      qualification: {
        adapterId: 'codex-app-server',
        providerId: 'openai',
        qualificationId: 'native-plan-v3',
        admissionSha256: 'a'.repeat(64),
        evidenceClass: 'native-adapter-qualified' as const
      },
      clarifications: [{
        clientTurnId: 'client-turn-1',
        providerThreadId: 'thread-1',
        providerTurnId: 'turn-1',
        requestId: 17,
        itemId: 'item-1',
        questions: [{
          id: 'scope',
          header: 'Scope',
          question: 'Which scope?',
          options: [{ label: 'Current', description: 'Use the current scope.' }],
          isOther: true,
          isSecret: false
        }],
        isBlocking: true,
        autoResolutionMs: null
      }]
    };
    const replyResponse = {
      schemaVersion: 'chirality.native-plan-clarification-reply/v3' as const,
      sessionId: session.sessionId,
      requestId: 17,
      sent: true as const
    };
    const listNativePlanClarifications = vi.fn().mockResolvedValue(clarificationResponse);
    const replyNativePlanClarification = vi.fn().mockResolvedValue(replyResponse);
    const runtimeClient = client({
      listNativePlanClarifications,
      replyNativePlanClarification
    });
    const port = new RuntimeDaemonHarnessPort(
      runtimeClient,
      project.projectId,
      project.canonicalRoot
    );
    const abortController = new AbortController();

    await expect(
      port.listNativePlanClarifications(session.sessionId, {
        signal: abortController.signal
      })
    ).resolves.toEqual(clarificationResponse);
    expect(listNativePlanClarifications).toHaveBeenCalledWith(
      project.projectId,
      session.sessionId,
      abortController.signal
    );

    const answers = { scope: { answers: ['Current'] } };
    await expect(
      port.replyNativePlanClarification(
        session.sessionId,
        17,
        answers,
        { signal: abortController.signal }
      )
    ).resolves.toEqual(replyResponse);
    expect(replyNativePlanClarification).toHaveBeenCalledWith(
      project.projectId,
      session.sessionId,
      { requestId: 17, answers },
      abortController.signal
    );
    expect(runtimeClient.projectStatus).toHaveBeenCalledTimes(2);
  });

  it('keeps restart binding and hosted status read-only when the selected folder is unregistered', async () => {
    const projectRoot = await realpath(process.cwd());
    const initializeHostedBootstrapProject = vi.fn();
    const port = new RuntimeHostedBootstrapPort({
      bootstrapClient: client({
        resolveProjectByRoot: vi.fn().mockRejectedValue(
          new RuntimeError('PROJECT_NOT_FOUND', 'not registered', 404)
        ),
        initializeHostedBootstrapProject
      }),
      runtimeDirectory: '/runtime',
      socketPath: '/runtime/control.sock'
    });

    await expect(port.bindProject(projectRoot)).resolves.toEqual({
      registration: 'required'
    });
    await expect(port.getStatus(projectRoot)).resolves.toEqual({ registration: 'required' });
    expect(initializeHostedBootstrapProject).not.toHaveBeenCalled();
  });

  it('rehydrates an existing project binding on bind without reading hosted account status', async () => {
    const projectRoot = await realpath(process.cwd());
    const registered = {
      ...project,
      projectId: 'restart-project',
      canonicalRoot: projectRoot,
      manifestPath: join(projectRoot, 'chirality.project.json'),
      manifestHash: 'restart-manifest',
      clientId: 'hosted-project-restart-project'
    };
    const healthy = { project: registered, manifestDrift: false, adaptersEnabled: true };
    const hostedBootstrapStatus = vi.fn();
    const scopedClient = client({
      projectStatus: vi.fn().mockResolvedValue(healthy),
      hostedBootstrapStatus
    });
    const installBoundPort = vi.fn();
    const bootstrapClient = client({
      resolveProjectByRoot: vi.fn().mockResolvedValue(registered),
      projectStatus: vi.fn().mockResolvedValue(healthy)
    });
    const port = new RuntimeHostedBootstrapPort({
      bootstrapClient,
      runtimeDirectory: '/runtime',
      socketPath: '/runtime/control.sock',
      createScopedClient: () => scopedClient,
      installBoundPort
    });

    await expect(port.bindProject(projectRoot)).resolves.toEqual({
      registration: 'registered',
      projectId: registered.projectId
    });
    expect(bootstrapClient.resolveProjectByRoot).toHaveBeenCalledWith(projectRoot, undefined);
    expect(installBoundPort).toHaveBeenCalledWith(
      expect.any(RuntimeDaemonHarnessPort),
      { projectId: registered.projectId, projectRoot },
      false
    );
    expect(scopedClient.projectStatus).toHaveBeenCalledOnce();
    expect(hostedBootstrapStatus).not.toHaveBeenCalled();
  });

  it('does not install a restart binding when the registered project has drifted', async () => {
    const projectRoot = await realpath(process.cwd());
    const registered = {
      ...project,
      projectId: 'drifted-restart-project',
      canonicalRoot: projectRoot,
      manifestPath: join(projectRoot, 'chirality.project.json'),
      clientId: 'hosted-project-drifted-restart-project'
    };
    const installBoundPort = vi.fn();
    const port = new RuntimeHostedBootstrapPort({
      bootstrapClient: client({
        resolveProjectByRoot: vi.fn().mockResolvedValue(registered),
        projectStatus: vi.fn().mockResolvedValue({
          project: registered,
          manifestDrift: true,
          adaptersEnabled: true
        })
      }),
      runtimeDirectory: '/runtime',
      socketPath: '/runtime/control.sock',
      createScopedClient: vi.fn(),
      installBoundPort
    });

    await expect(port.bindProject(projectRoot)).rejects.toMatchObject({
      type: 'WORKING_ROOT_CONFLICT',
      status: 409
    });
    expect(installBoundPort).not.toHaveBeenCalled();
  });

  it('initializes explicitly, verifies both principals, and installs an arbitrary project binding', async () => {
    const projectRoot = await realpath(process.cwd());
    const registered = {
      ...project,
      projectId: 'user-project',
      canonicalRoot: projectRoot,
      manifestPath: join(projectRoot, 'chirality.project.json'),
      manifestHash: 'hosted-manifest',
      clientId: 'hosted-project-user-project'
    };
    const registration = {
      projectId: registered.projectId,
      manifestHash: registered.manifestHash
    };
    // The App-owned Runtime has no account-host admission step: the scoped
    // project client reads hosted status directly, and only after binding.
    const accountStatus = {
      schema: 'chirality-hosted-bootstrap-status/v1' as const,
      projectId: registered.projectId,
      ceremony: 'ready-to-start' as const,
      admission: 'unavailable' as const,
      canStartLogin: true
    };
    const hostedBootstrapStatus = vi.fn().mockResolvedValue(accountStatus);
    const bootstrapClient = client({
      initializeHostedBootstrapProject: vi.fn().mockResolvedValue(registration),
      hostedBootstrapStatus,
      projectStatus: vi.fn().mockResolvedValue({
        project: registered,
        manifestDrift: false,
        adaptersEnabled: true
      })
    });
    const scopedClient = client({
      projectStatus: vi.fn().mockResolvedValue({
        project: registered,
        manifestDrift: false,
        adaptersEnabled: true
      }),
      hostedBootstrapStatus
    });
    const createScopedClient = vi.fn().mockReturnValue(scopedClient);
    const installBoundPort = vi.fn();
    const port = new RuntimeHostedBootstrapPort({
      bootstrapClient,
      runtimeDirectory: '/runtime',
      socketPath: '/runtime/control.sock',
      createScopedClient,
      installBoundPort
    });

    const initialized = await port.initializeProject(projectRoot);
    expect(initialized).toEqual({
      registration: 'registered',
      projectId: registered.projectId
    });
    expect(initialized).not.toHaveProperty('status');
    expect(hostedBootstrapStatus).not.toHaveBeenCalled();
    await expect(port.getStatus(projectRoot)).resolves.toEqual({
      registration: 'registered',
      projectId: registered.projectId,
      status: accountStatus
    });
    expect(hostedBootstrapStatus).toHaveBeenCalledWith(registered.projectId, undefined);
    await expect(port.bindProject(projectRoot)).resolves.toEqual({
      registration: 'registered',
      projectId: registered.projectId
    });
    expect(hostedBootstrapStatus).toHaveBeenCalledTimes(1);
    expect(bootstrapClient.initializeHostedBootstrapProject).toHaveBeenCalledWith(
      { projectRoot },
      undefined
    );
    expect(createScopedClient).toHaveBeenCalledWith({
      socketPath: '/runtime/control.sock',
      tokenFile: '/runtime/auth/tokens/hosted-project-user-project.token'
    });
    expect(installBoundPort).toHaveBeenCalledWith(
      expect.any(RuntimeDaemonHarnessPort),
      { projectId: registered.projectId, projectRoot },
      true
    );

    await expect(port.getStatus(dirname(projectRoot))).rejects.toMatchObject({
      type: 'WORKING_ROOT_CONFLICT',
      status: 409
    });
    expect(installBoundPort).toHaveBeenCalledTimes(2);
  });

  it('rejects a late project initialization before it can replace the newer binding', async () => {
    const temporaryA = await mkdtemp(join(tmpdir(), 'chirality-hosted-a-'));
    const temporaryB = await mkdtemp(join(tmpdir(), 'chirality-hosted-b-'));
    const rootA = await realpath(temporaryA);
    const rootB = await realpath(temporaryB);
    let resolveA!: (value: { projectId: string; manifestHash: string }) => void;
    let resolveB!: (value: { projectId: string; manifestHash: string }) => void;
    const initializationA = new Promise<{ projectId: string; manifestHash: string }>(resolve => { resolveA = resolve; });
    const initializationB = new Promise<{ projectId: string; manifestHash: string }>(resolve => { resolveB = resolve; });
    const projects = new Map([
      ['project-a', { ...project, projectId: 'project-a', canonicalRoot: rootA, manifestPath: join(rootA, 'chirality.project.json'), manifestHash: 'manifest-a', clientId: 'hosted-project-project-a' }],
      ['project-b', { ...project, projectId: 'project-b', canonicalRoot: rootB, manifestPath: join(rootB, 'chirality.project.json'), manifestHash: 'manifest-b', clientId: 'hosted-project-project-b' }]
    ]);
    const bootstrapClient = client({
      initializeHostedBootstrapProject: vi.fn().mockImplementation(({ projectRoot }: { projectRoot: string }) => projectRoot === rootA ? initializationA : initializationB),
      projectStatus: vi.fn().mockImplementation((projectId: string) => Promise.resolve({ project: projects.get(projectId)!, manifestDrift: false, adaptersEnabled: true }))
    });
    const statusFor = (projectId: string) => ({ schema: 'chirality-hosted-bootstrap-status/v1' as const, projectId, ceremony: 'ready-to-start' as const, admission: 'unavailable' as const, canStartLogin: true });
    const scopedClients = new Map([...projects].map(([projectId, registered]) => [projectId, client({
      projectStatus: vi.fn().mockResolvedValue({ project: registered, manifestDrift: false, adaptersEnabled: true }),
      hostedBootstrapStatus: vi.fn().mockResolvedValue(statusFor(projectId))
    })]));
    const installBoundPort = vi.fn();
    const port = new RuntimeHostedBootstrapPort({
      bootstrapClient,
      runtimeDirectory: '/runtime',
      socketPath: '/runtime/control.sock',
      createScopedClient: ({ tokenFile }) => scopedClients.get(tokenFile.includes('project-a') ? 'project-a' : 'project-b')!,
      installBoundPort
    });

    try {
      const requestA = port.initializeProject(rootA);
      const requestB = port.initializeProject(rootB);
      resolveB({ projectId: 'project-b', manifestHash: 'manifest-b' });
      await expect(requestB).resolves.toEqual({ registration: 'registered', projectId: 'project-b' });
      resolveA({ projectId: 'project-a', manifestHash: 'manifest-a' });
      await expect(requestA).rejects.toMatchObject({ type: 'WORKING_ROOT_CONFLICT', status: 409 });
      expect(installBoundPort).toHaveBeenCalledTimes(1);
      expect(installBoundPort).toHaveBeenCalledWith(expect.any(RuntimeDaemonHarnessPort), { projectId: 'project-b', projectRoot: rootB }, true);
      await expect(port.getStatus(rootB)).resolves.toEqual({ registration: 'registered', projectId: 'project-b', status: statusFor('project-b') });
      expect(scopedClients.get('project-a')!.hostedBootstrapStatus).not.toHaveBeenCalled();
      expect(scopedClients.get('project-b')!.hostedBootstrapStatus).toHaveBeenCalledTimes(1);
      // A's stale selection cannot replace B, but A's verified binding remains usable.
      await expect(port.getStatus(rootA)).resolves.toMatchObject({ projectId: 'project-a' });
      await expect(port.bindProject(rootA)).resolves.toMatchObject({ projectId: 'project-a' });
      expect(installBoundPort).toHaveBeenCalledTimes(2);
    } finally {
      await rm(temporaryA, { recursive: true, force: true });
      await rm(temporaryB, { recursive: true, force: true });
    }
  });

  it('lets a newer explicit selection commit while a consent mutation finishes on the captured old binding', async () => {
    const temporaryA = await mkdtemp(join(tmpdir(), 'chirality-hosted-selected-a-'));
    const temporaryB = await mkdtemp(join(tmpdir(), 'chirality-hosted-selected-b-'));
    const rootA = await realpath(temporaryA);
    const rootB = await realpath(temporaryB);
    const registeredA = { ...project, projectId: 'selected-a', canonicalRoot: rootA, manifestPath: join(rootA, 'chirality.project.json'), manifestHash: 'selected-manifest-a', clientId: 'hosted-project-selected-a' };
    const registeredB = { ...project, projectId: 'selected-b', canonicalRoot: rootB, manifestPath: join(rootB, 'chirality.project.json'), manifestHash: 'selected-manifest-b', clientId: 'hosted-project-selected-b' };
    const registrationA = { projectId: 'selected-a', manifestHash: 'selected-manifest-a' };
    const registrationB = { projectId: 'selected-b', manifestHash: 'selected-manifest-b' };
    const consentA = { schema: 'chirality-hosted-bootstrap-status/v1' as const, projectId: 'selected-a', ceremony: 'ready-to-start' as const, admission: 'unavailable' as const, canStartLogin: true };
    let resolveB!: (value: typeof registrationB) => void;
    const pendingB = new Promise<typeof registrationB>(resolve => { resolveB = resolve; });
    const bootstrapClient = client({
      initializeHostedBootstrapProject: vi.fn().mockImplementation(({ projectRoot }: { projectRoot: string }) => projectRoot === rootA ? Promise.resolve(registrationA) : pendingB),
      projectStatus: vi.fn().mockImplementation((projectId: string) => Promise.resolve({ project: projectId === 'selected-a' ? registeredA : registeredB, manifestDrift: false, adaptersEnabled: true }))
    });
    const statusB = { ...consentA, projectId: 'selected-b' };
    const scopedA = client({
      projectStatus: vi.fn().mockResolvedValue({ project: registeredA, manifestDrift: false, adaptersEnabled: true }),
      hostedBootstrapStatus: vi.fn().mockResolvedValue(consentA),
      grantHostedProviderNetworkConsent: vi.fn()
    });
    const scopedB = client({
      projectStatus: vi.fn().mockResolvedValue({ project: registeredB, manifestDrift: false, adaptersEnabled: true }),
      hostedBootstrapStatus: vi.fn().mockResolvedValue(statusB)
    });
    const installBoundPort = vi.fn();
    const port = new RuntimeHostedBootstrapPort({
      bootstrapClient,
      runtimeDirectory: '/runtime',
      socketPath: '/runtime/control.sock',
      createScopedClient: ({ tokenFile }) => tokenFile.includes('selected-a') ? scopedA : scopedB,
      installBoundPort
    });

    try {
      await port.initializeProject(rootA);
      const selectionB = port.initializeProject(rootB);
      const lateBindingA = port.getStatus(rootA);
      const lateConsentA = port.grantProviderNetworkConsent(rootA);
      await expect(lateBindingA).resolves.toEqual({ registration: 'registered', projectId: 'selected-a', status: consentA });
      await expect(lateConsentA).resolves.toEqual(consentA);
      resolveB(registrationB);
      await expect(selectionB).resolves.toEqual({ registration: 'registered', projectId: 'selected-b' });
      await expect(port.getStatus(rootB)).resolves.toEqual({ registration: 'registered', projectId: 'selected-b', status: statusB });
      await expect(port.getStatus(rootA)).resolves.toEqual({ registration: 'registered', projectId: 'selected-a', status: consentA });
      expect(installBoundPort).toHaveBeenCalledTimes(2);
      expect(installBoundPort).toHaveBeenLastCalledWith(expect.any(RuntimeDaemonHarnessPort), { projectId: 'selected-b', projectRoot: rootB }, true);
      // The retained consent path reads status too; no consent is ever recorded.
      expect(scopedA.hostedBootstrapStatus).toHaveBeenCalledTimes(3);
      expect(scopedA.grantHostedProviderNetworkConsent).not.toHaveBeenCalled();
      expect(scopedB.hostedBootstrapStatus).toHaveBeenCalledTimes(1);
    } finally {
      await rm(temporaryA, { recursive: true, force: true });
      await rm(temporaryB, { recursive: true, force: true });
    }
  });

  it('allows a verified normal daemon port to serve a non-app-dev project ID', async () => {
    const projectRoot = await realpath(process.cwd());
    const registered = {
      ...project,
      projectId: 'user-project',
      canonicalRoot: projectRoot
    };
    const listRoles = vi.fn().mockResolvedValue({
      schemaVersion: 'chirality.roles/v3',
      defaultRole: 'HELP_HUMAN',
      roles: []
    });
    const runtimeClient = client({
      projectStatus: vi.fn().mockResolvedValue({
        project: registered,
        manifestDrift: false,
        adaptersEnabled: true
      }),
      listRoles
    });
    const port = new RuntimeDaemonHarnessPort(
      runtimeClient,
      registered.projectId,
      projectRoot
    );

    await port.listRoles(projectRoot);
    expect(listRoles).toHaveBeenCalledWith(registered.projectId, undefined);
  });

  it('revalidates a cached hosted binding before a consent mutation', async () => {
    const projectRoot = await realpath(process.cwd());
    const registered = {
      ...project,
      projectId: 'drift-project',
      canonicalRoot: projectRoot,
      manifestHash: 'before',
      clientId: 'hosted-project-drift-project'
    };
    const healthy = {
      project: registered,
      manifestDrift: false,
      adaptersEnabled: true
    };
    const bootstrapProjectStatus = vi.fn().mockResolvedValue(healthy);
    const scopedProjectStatus = vi.fn().mockResolvedValue(healthy);
    const scopedClient = client({
      projectStatus: scopedProjectStatus,
      hostedBootstrapStatus: vi.fn().mockResolvedValue({ schema: 'chirality-hosted-bootstrap-status/v1', projectId: registered.projectId, ceremony: 'ready-to-start', admission: 'unavailable', canStartLogin: true }),
      grantHostedProviderNetworkConsent: vi.fn()
    });
    const port = new RuntimeHostedBootstrapPort({
      bootstrapClient: client({
        resolveProjectByRoot: vi.fn().mockResolvedValue(registered),
        projectStatus: bootstrapProjectStatus
      }),
      runtimeDirectory: '/runtime',
      socketPath: '/runtime/control.sock',
      createScopedClient: () => scopedClient
    });
    await port.getStatus(projectRoot);
    expect(scopedClient.hostedBootstrapStatus).toHaveBeenCalledTimes(1);
    bootstrapProjectStatus.mockResolvedValueOnce({
      ...healthy,
      project: { ...registered, manifestHash: 'after' }
    });

    await expect(
      port.grantProviderNetworkConsent(projectRoot)
    ).rejects.toMatchObject({ type: 'WORKING_ROOT_CONFLICT', status: 409 });
    expect(scopedClient.grantHostedProviderNetworkConsent).not.toHaveBeenCalled();
    expect(scopedClient.hostedBootstrapStatus).toHaveBeenCalledTimes(1);
  });

  it('revalidates and preserves the selected binding for project-local sign-out', async () => {
    const projectRoot = await realpath(process.cwd());
    const registered = {
      ...project,
      projectId: 'logout-project',
      canonicalRoot: projectRoot,
      manifestHash: 'logout-manifest',
      clientId: 'hosted-project-logout-project'
    };
    const healthy = { project: registered, manifestDrift: false, adaptersEnabled: true };
    const signedOut = {
      schema: 'chirality-hosted-bootstrap-status/v1' as const,
      projectId: registered.projectId,
      ceremony: 'ready-to-start' as const,
      admission: 'unavailable' as const,
      canStartLogin: false
    };
    const signOutHostedProject = vi.fn().mockResolvedValue(signedOut);
    const scopedClient = client({
      projectStatus: vi.fn().mockResolvedValue(healthy),
      hostedBootstrapStatus: vi.fn().mockResolvedValue({ ...signedOut, ceremony: 'signed-in', admission: 'ready' }),
      signOutHostedProject: vi.fn()
    });
    // Account actions use the App-host client; the project-scoped client is never asked to sign out.
    const port = new RuntimeHostedBootstrapPort({
      bootstrapClient: client({
        resolveProjectByRoot: vi.fn().mockResolvedValue(registered),
        projectStatus: vi.fn().mockResolvedValue(healthy),
        signOutHostedProject
      }),
      runtimeDirectory: '/runtime',
      socketPath: '/runtime/control.sock',
      createScopedClient: () => scopedClient
    });
    await port.getStatus(projectRoot);
    expect(scopedClient.hostedBootstrapStatus).toHaveBeenCalledTimes(1);
    const controller = new AbortController();
    await expect(port.signOut(projectRoot, { signal: controller.signal })).resolves.toEqual(signedOut);
    expect(signOutHostedProject).toHaveBeenCalledWith(registered.projectId, controller.signal);
    expect(scopedClient.signOutHostedProject).not.toHaveBeenCalled();
    expect(scopedClient.hostedBootstrapStatus).toHaveBeenCalledTimes(1);
  });

  it('rejects a symlink alias before explicit hosted project initialization', async () => {
    const fixtureRoot = await mkdtemp(join(tmpdir(), 'chirality-hosted-root-'));
    const alias = `${fixtureRoot}-alias`;
    await symlink(fixtureRoot, alias);
    const initializeHostedBootstrapProject = vi.fn();
    const port = new RuntimeHostedBootstrapPort({
      bootstrapClient: client({ initializeHostedBootstrapProject }),
      runtimeDirectory: '/runtime',
      socketPath: '/runtime/control.sock'
    });

    try {
      await expect(port.initializeProject(alias)).rejects.toMatchObject({
        type: 'INVALID_REQUEST',
        status: 400
      });
      expect(initializeHostedBootstrapProject).not.toHaveBeenCalled();
    } finally {
      await rm(alias);
      await rm(fixtureRoot, { recursive: true, force: true });
    }
  });

  it('does not install a normal port when Runtime returns a conflicting registration', async () => {
    const projectRoot = await realpath(process.cwd());
    const registration = { projectId: 'project-one', manifestHash: 'expected' };
    const installBoundPort = vi.fn();
    const port = new RuntimeHostedBootstrapPort({
      bootstrapClient: client({
        initializeHostedBootstrapProject: vi.fn().mockResolvedValue(registration),
        projectStatus: vi.fn().mockResolvedValue({
          project: {
            ...project,
            projectId: registration.projectId,
            canonicalRoot: projectRoot,
            manifestHash: 'conflicting'
          },
          manifestDrift: false,
          adaptersEnabled: true
        })
      }),
      runtimeDirectory: '/runtime',
      socketPath: '/runtime/control.sock',
      createScopedClient: vi.fn(),
      installBoundPort
    });

    await expect(port.initializeProject(projectRoot)).rejects.toMatchObject({
      type: 'WORKING_ROOT_CONFLICT',
      status: 409
    });
    expect(installBoundPort).not.toHaveBeenCalled();
  });

  it('does not install a normal port when Runtime rejects project initialization', async () => {
    const projectRoot = await realpath(process.cwd());
    const installBoundPort = vi.fn();
    const port = new RuntimeHostedBootstrapPort({
      bootstrapClient: client({
        initializeHostedBootstrapProject: vi.fn().mockRejectedValue(
          new RuntimeError('INVALID_REQUEST', 'Malformed existing manifest', 400)
        )
      }),
      runtimeDirectory: '/runtime',
      socketPath: '/runtime/control.sock',
      createScopedClient: vi.fn(),
      installBoundPort
    });

    await expect(port.initializeProject(projectRoot)).rejects.toMatchObject({
      type: 'INVALID_REQUEST',
      status: 400,
      message: 'Malformed existing manifest'
    });
    expect(installBoundPort).not.toHaveBeenCalled();
  });

  it('uses only the fixed app-dev project for contained scaffold requests', async () => {
    const scaffoldResult = {
      executionRoot: `${project.canonicalRoot}/execution/demo`,
      decompositionPath: `${project.canonicalRoot}/execution/demo/decomposition.json`,
      copiedDecompositionPath: `${project.canonicalRoot}/execution/demo/decomposition.json`,
      projectName: 'demo',
      coordinationMode: 'HYBRID' as const,
      packageCount: 0,
      deliverableCount: 0,
      created: { directories: [], files: [] },
      layoutValidation: {
        valid: true,
        executionRoot: { path: 'execution/demo', valid: true, missing: [] },
        packages: [],
        deliverables: []
      },
      preparationCompatibility: {
        ready: true,
        deliverablesChecked: 0,
        issueCount: 0,
        deliverables: []
      }
    };
    const runtimeClient = client({
      scaffold: vi.fn().mockResolvedValue(scaffoldResult)
    });
    const port = new RuntimeDaemonHarnessPort(runtimeClient);

    await expect(
      port.scaffold({
        executionRoot: scaffoldResult.executionRoot,
        decompositionPath: scaffoldResult.decompositionPath,
        coordinationMode: 'HYBRID'
      })
    ).resolves.toEqual(scaffoldResult);
    expect(runtimeClient.scaffold).toHaveBeenCalledWith(
      project.projectId,
      {
        executionRoot: scaffoldResult.executionRoot,
        decompositionPath: scaffoldResult.decompositionPath,
        coordinationMode: 'HYBRID'
      },
      undefined
    );
    expect(runtimeClient.listProjects).not.toHaveBeenCalled();
  });

  it('translates daemon failures into the legacy route error vocabulary', async () => {
    const port = new RuntimeDaemonHarnessPort(
      client({
        turnSession: vi
          .fn()
          .mockRejectedValue(
            new RuntimeError('SESSION_TURN_IN_PROGRESS', 'turn locked', 409)
          )
      })
    );

    await expect(
      port.turn({ sessionId: session.sessionId, message: 'blocked' })
    ).rejects.toEqual(
      expect.objectContaining({
        type: 'TURN_IN_PROGRESS',
        status: 409,
        message: 'turn locked'
      })
    );
  });

  it('never enumerates projects or session owners, even with an operator-capable client', async () => {
    const runtimeClient = client({
      resolveProjectByRoot: vi.fn(() => {
        throw new Error('must not enumerate projects');
      }),
      resolveSessionOwner: vi.fn(() => {
        throw new Error('must not enumerate session owners');
      }),
      listProjects: vi.fn(() => {
        throw new Error('must not list projects');
      })
    });
    const port = new RuntimeDaemonHarnessPort(
      runtimeClient,
      project.projectId,
      project.canonicalRoot
    );

    await expect(port.getSession('foreign-looking-session-id')).resolves.toEqual({
      session
    });
    expect(runtimeClient.getSession).toHaveBeenCalledWith(
      project.projectId,
      'foreign-looking-session-id',
      undefined
    );
    expect(runtimeClient.resolveSessionOwner).not.toHaveBeenCalled();
    expect(runtimeClient.listProjects).not.toHaveBeenCalled();
  });

  it('rejects a session payload attributed to another project', async () => {
    const port = new RuntimeDaemonHarnessPort(
      client({
        getSession: vi.fn().mockResolvedValue({
          ...session,
          projectId: 'pec'
        })
      }),
      project.projectId,
      project.canonicalRoot
    );

    await expect(port.getSession(session.sessionId)).rejects.toMatchObject({
      type: 'PROVIDER_AUTH_FAILURE',
      status: 403
    });
  });

  it('rejects paths and registrations outside the fixed app-dev root', async () => {
    const runtimeClient = client();
    const port = new RuntimeDaemonHarnessPort(
      runtimeClient,
      project.projectId,
      project.canonicalRoot
    );

    await expect(
      port.createSession({
        projectRoot: '/repo/projects/pec',
        persona: 'WORKING_ITEMS',
        mode: 'chat'
      })
    ).rejects.toMatchObject({
      type: 'WORKING_ROOT_INACCESSIBLE',
      status: 404
    });
    expect(runtimeClient.createSession).not.toHaveBeenCalled();

    const mismatched = new RuntimeDaemonHarnessPort(
      client({
        projectStatus: vi.fn().mockResolvedValue({
          project: { ...project, canonicalRoot: '/repo/projects/pec' },
          manifestDrift: false,
          adaptersEnabled: true
        })
      }),
      project.projectId,
      project.canonicalRoot
    );
    await expect(mismatched.listSessions(project.canonicalRoot)).rejects.toMatchObject({
      type: 'WORKING_ROOT_CONFLICT',
      status: 409
    });
  });
});


it('preserves sanitized timeout classification and boot identity without exposing transport causes', async () => {
  const failure = Object.assign(new RuntimeTransportError('secret socket path and token'), { reason: 'timeout', operation: 'boot', sessionId: 'created-session' });
  const runtimeClient = client({ bootSession: vi.fn().mockRejectedValue(failure) });
  const port = new RuntimeDaemonHarnessPort(runtimeClient, project.projectId);
  await expect(port.bootSession({ sessionId: 'created-session' })).rejects.toMatchObject({
    status: 504, message: 'Session initialization timed out while waiting for Runtime.',
    details: { transportReason: 'timeout', operation: 'boot', sessionId: 'created-session' }
  });
});


it('routes old and uncached sessions through their verified owner across folder selection and registry restart', async () => {
  const registry = await import('../../lib/runtime-client/daemon-harness-port');
  const turnRoute = await import('../../app/api/harness/turn/route');
  const steerRoute = await import('../../app/api/harness/session/[id]/turn/steer/route');
  const temporary = await mkdtemp(join(tmpdir(), 'chirality-routing-'));
  const { mkdir } = await import('node:fs/promises');
  await mkdir(join(temporary, 'a')); await mkdir(join(temporary, 'b'));
  const rootA = await realpath(join(temporary, 'a'));
  const rootB = await realpath(join(temporary, 'b'));
  const projects = [rootA, rootB].map((root, index) => ({ ...project,
    projectId: `route-${index}`, canonicalRoot: root, manifestPath: join(root, 'chirality.project.json') }));
  const records = projects.map(p => ({ ...session, projectId: p.projectId, projectRoot: p.canonicalRoot, sessionId: `${p.projectId}-session` }));
  const stream = () => ({ cancel: vi.fn(), async *[Symbol.asyncIterator]() {} }) as unknown as RuntimeStream;
  const scoped = projects.map((p, i) => client({
    projectStatus: vi.fn().mockResolvedValue({ project: p, manifestDrift: false, adaptersEnabled: true }),
    createSession: vi.fn().mockResolvedValue(records[i]),
    listSessions: vi.fn().mockResolvedValue([records[i]]),
    getSession: vi.fn().mockImplementation(async (_projectId, id) => {
      if (id === records[i].sessionId || id.startsWith(`${p.projectId}-child`)) return { ...records[i], sessionId: id };
      throw new RuntimeError('SESSION_NOT_FOUND', `Unknown session: ${id}`, 404);
    }),
    turnSession: vi.fn().mockImplementation(async () => stream()),
    replaySession: vi.fn().mockResolvedValue({ session: records[i], events: [] }),
    sessionTurnState: vi.fn().mockResolvedValue({ state: 'running' }),
    attachSessionTurn: vi.fn().mockImplementation(async () => stream()),
    listSessionRequests: vi.fn().mockResolvedValue({ requests: [] }),
    answerSessionRequest: vi.fn().mockResolvedValue({ accepted: true }),
    sessionTurnSteer: vi.fn().mockResolvedValue({ accepted: true }),
    sessionTurnSteerReceipt: vi.fn().mockResolvedValue({ accepted: true }),
    hostedBootstrapStatus: vi.fn().mockResolvedValue({ projectId: p.projectId })
  }));
  const bootstrap = client({
    initializeHostedBootstrapProject: vi.fn().mockImplementation(async ({ projectRoot }) => {
      const p = projects.find(p => p.canonicalRoot === projectRoot)!;
      return { projectId: p.projectId, manifestHash: p.manifestHash };
    }),
    projectStatus: vi.fn().mockImplementation(async id => ({ project: projects.find(p => p.projectId === id)!, manifestDrift: false, adaptersEnabled: true })),
    resolveSessionOwner: vi.fn().mockImplementation(async id => {
      const i = records.findIndex(record => record.sessionId === id);
      if (i < 0) throw new RuntimeError('SESSION_NOT_FOUND', `Unknown session: ${id}`, 404);
      return { project: projects[i], session: records[i] };
    })
  });
  const setup = () => {
    registry.resetDaemonHarnessPortForTests();
    const hosted = new RuntimeHostedBootstrapPort({ bootstrapClient: bootstrap, runtimeDirectory: '/runtime', socketPath: '/runtime/control.sock',
      createScopedClient: ({ tokenFile }) => scoped[tokenFile.includes('route-0') ? 0 : 1], installBoundPort: registry.installBoundDaemonHarnessPort });
    registry.installHostedBootstrapPort(hosted);
    return hosted;
  };
  const request = (body: unknown) => new Request('http://localhost/api/harness/turn', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  try {
    let hosted = setup();
    await hosted.initializeProject(rootA);
    await registry.getDaemonHarnessPort().createSession({ projectRoot: rootA });
    expect((await turnRoute.POST(request({ sessionId: records[0].sessionId, message: 'first' }))).status).toBe(200);
    await hosted.initializeProject(rootB);
    await registry.getDaemonHarnessPort().createSession({ projectRoot: rootB });
    expect((await turnRoute.POST(request({ sessionId: records[1].sessionId, message: 'running' }))).status).toBe(200);
    expect((await turnRoute.POST(request({ sessionId: records[0].sessionId, message: 'correction' }))).status).toBe(200);
    expect(scoped[0].turnSession).toHaveBeenLastCalledWith(projects[0].projectId, records[0].sessionId, { message: 'correction' }, expect.any(AbortSignal));
    expect(scoped[1].turnSession).toHaveBeenCalledTimes(1);
    const port = registry.getDaemonHarnessPort();
    await port.replaySession(records[0].sessionId);
    await port.turnState(records[0].sessionId);
    await port.attachTurn(records[0].sessionId, 0);
    await port.listRequests(records[0].sessionId);
    await port.answerRequest(records[0].sessionId, 'req', { kind: 'approval', decision: 'accept' } as never);
    expect((await steerRoute.POST(request({ operationId: 'op', expectedTurnId: 'turn', text: 'steer' }), { params: Promise.resolve({ id: records[0].sessionId }) })).status).toBe(200);
    await port.steerReceipt(records[0].sessionId, { operationId: 'op', expectedTurnId: 'turn' });
    await port.interrupt({ sessionId: records[0].sessionId });
    for (const name of ['replaySession', 'sessionTurnState', 'attachSessionTurn', 'listSessionRequests', 'answerSessionRequest', 'sessionTurnSteer', 'sessionTurnSteerReceipt', 'interruptSession'] as const) {
      expect(vi.mocked(scoped[0][name]).mock.calls[0].slice(0, 2)).toEqual([projects[0].projectId, records[0].sessionId]);
      expect(scoped[1][name]).not.toHaveBeenCalled();
    }
    await port.getSession('route-0-child'); // trusted scoped lookup, no cached create/list
    expect(bootstrap.resolveSessionOwner).not.toHaveBeenCalled();
    await expect(port.listSessions(rootA)).resolves.toMatchObject({ sessions: [records[0]] });
    await port.createSession({ projectRoot: rootA });
    expect(scoped[0].createSession).toHaveBeenCalledTimes(2);
    expect(scoped[1].createSession).toHaveBeenCalledTimes(1);
    await expect(hosted.getStatus(rootA)).resolves.toMatchObject({ projectId: projects[0].projectId });
    vi.mocked(bootstrap.initializeHostedBootstrapProject).mockResolvedValueOnce({ projectId: projects[1].projectId, manifestHash: 'conflicting-hash' });
    await expect(hosted.initializeProject(rootB)).rejects.toMatchObject({ type: 'WORKING_ROOT_CONFLICT' });
    await port.turnState(records[0].sessionId); // failed replacement preserves A
    await port.turnState(records[1].sessionId); // and B
    vi.mocked(scoped[0].projectStatus).mockResolvedValueOnce({ project: projects[0], manifestDrift: true, adaptersEnabled: false });
    await expect(port.turn({ sessionId: records[0].sessionId, message: 'blocked' })).rejects.toMatchObject({ type: 'WORKING_ROOT_CONFLICT' });
    expect(scoped[0].turnSession).toHaveBeenCalledTimes(2);
    expect(scoped[1].turnSession).toHaveBeenCalledTimes(1);
    // F3: only the actual owner must be healthy; unrelated A probes may fail.
    for (const [suffix, code] of [['drift', 'PROJECT_MANIFEST_DRIFT'], ['missing', 'PROJECT_NOT_FOUND']] as const) {
      vi.mocked(scoped[0].projectStatus).mockRejectedValueOnce(new RuntimeError(code, 'unrelated A unavailable', 409));
      const childId = `route-1-child-${suffix}`;
      await expect(port.getSession(childId)).resolves.toMatchObject({ session: { sessionId: childId, projectId: projects[1].projectId } });
      expect(scoped[1].getSession).toHaveBeenLastCalledWith(projects[1].projectId, childId, undefined);
      expect(bootstrap.resolveSessionOwner).not.toHaveBeenCalled();
    }
    const blockedChild = 'route-1-child-own-drift';
    vi.mocked(scoped[1].projectStatus).mockRejectedValue(new RuntimeError('PROJECT_MANIFEST_DRIFT', 'actual B drift', 409));
    vi.mocked(bootstrap.resolveSessionOwner).mockResolvedValueOnce({ project: projects[1], session: { ...records[1], sessionId: blockedChild } });
    await expect(port.turn({ sessionId: blockedChild, message: 'must fail' })).rejects.toMatchObject({ type: 'WORKING_ROOT_CONFLICT', message: 'actual B drift' });
    expect(scoped[1].turnSession).toHaveBeenCalledTimes(1);
    vi.mocked(scoped[1].projectStatus).mockResolvedValue({ project: projects[1], manifestDrift: false, adaptersEnabled: true });
    // Auth failures are never reclassified as harmless non-owning probes.
    vi.mocked(scoped[0].projectStatus).mockRejectedValueOnce(new RuntimeError('FORBIDDEN', 'scope denied', 403));
    await expect(port.getSession('route-1-child-denied')).rejects.toMatchObject({ type: 'PROVIDER_AUTH_FAILURE' });
    expect(scoped[1].getSession).not.toHaveBeenCalledWith(projects[1].projectId, 'route-1-child-denied', undefined);
    // The selected root after restart is B; historical A ownership comes from Runtime.
    hosted = setup(); await hosted.initializeProject(rootB);
    await registry.getDaemonHarnessPort().replaySession(records[0].sessionId);
    expect(bootstrap.resolveSessionOwner).toHaveBeenCalledWith(records[0].sessionId, undefined);
    await registry.getDaemonHarnessPort().listSessions(rootA);
    await registry.getDaemonHarnessPort().turnState(records[0].sessionId);
    await expect(registry.getDaemonHarnessPort().turn({ sessionId: 'missing', message: 'no' })).rejects.toMatchObject({ type: 'SESSION_NOT_FOUND' });
    expect(scoped[1].turnSession).toHaveBeenCalledTimes(1);
  } finally {
    registry.resetDaemonHarnessPortForTests();
    await rm(temporary, { recursive: true, force: true });
  }
});

it('keeps unregistered roots inaccessible without creating or installing, while retaining real registration conflicts', async () => {
  const registry = await import('../../lib/runtime-client/daemon-harness-port');
  const createRoute = await import('../../app/api/harness/session/create/route');
  const temporary = await mkdtemp(join(tmpdir(), 'chirality-unregistered-root-'));
  const outsideRoot = await realpath(temporary);
  const existing = client();
  const bootstrap = client({
    resolveProjectByRoot: vi.fn().mockRejectedValue(new RuntimeError('PROJECT_NOT_FOUND', 'No registered project owns requested root', 404)),
    initializeHostedBootstrapProject: vi.fn()
  });
  const installBoundPort = vi.fn(registry.installBoundDaemonHarnessPort);
  const createScopedClient = vi.fn(() => client());
  registry.resetDaemonHarnessPortForTests();
  registry.installBoundDaemonHarnessPort(new RuntimeDaemonHarnessPort(existing, project.projectId, project.canonicalRoot), { projectId: project.projectId, projectRoot: project.canonicalRoot });
  registry.installHostedBootstrapPort(new RuntimeHostedBootstrapPort({ bootstrapClient: bootstrap, runtimeDirectory: '/runtime', socketPath: '/runtime/control.sock', createScopedClient, installBoundPort }));
  const attempt = () => createRoute.POST(new Request('http://localhost/api/harness/session/create', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ projectRoot: outsideRoot })
  }));
  try {
    const absent = await attempt();
    expect(absent.status).toBe(404);
    expect(await absent.json()).toMatchObject({ error: { type: 'WORKING_ROOT_INACCESSIBLE' } });
    expect(bootstrap.resolveProjectByRoot).toHaveBeenCalledWith(outsideRoot, expect.any(AbortSignal));
    // An advertised registration whose trusted status differs is still a conflict.
    vi.mocked(bootstrap.resolveProjectByRoot).mockResolvedValueOnce({ ...project, canonicalRoot: outsideRoot });
    const conflicting = await attempt();
    expect(conflicting.status).toBe(409);
    expect(await conflicting.json()).toMatchObject({ error: { type: 'WORKING_ROOT_CONFLICT' } });
    expect(bootstrap.initializeHostedBootstrapProject).not.toHaveBeenCalled();
    expect(bootstrap.createSession).not.toHaveBeenCalled();
    expect(existing.createSession).not.toHaveBeenCalled();
    expect(createScopedClient).not.toHaveBeenCalled();
    expect(installBoundPort).not.toHaveBeenCalled();
    await expect(registry.getDaemonHarnessPort().createSession({ projectRoot: project.canonicalRoot })).resolves.toMatchObject({ session });
    expect(existing.createSession).toHaveBeenCalledTimes(1);
  } finally {
    registry.resetDaemonHarnessPortForTests();
    await rm(temporary, { recursive: true, force: true });
  }
});
