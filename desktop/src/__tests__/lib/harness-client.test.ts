import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
  HarnessApiClientError,
  bootHarnessSession,
  createHarnessSession,
  listDirectChatPersonas,
  listHarnessSessions,
  replaySessionEvents,
  scaffoldHarnessExecutionRoot,
  streamHarnessTurn
} from '../../lib/harness/client';

function jsonResponse(payload: unknown, status = 200): Response {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      'Content-Type': 'application/json'
    }
  });
}

function sseResponse(chunks: string[]): Response {
  const encoder = new TextEncoder();
  let index = 0;

  const stream = new ReadableStream<Uint8Array>({
    pull(controller) {
      if (index >= chunks.length) {
        controller.close();
        return;
      }

      controller.enqueue(encoder.encode(chunks[index]));
      index += 1;
    }
  });

  return new Response(stream, {
    status: 200,
    headers: {
      'Content-Type': 'text/event-stream; charset=utf-8'
    }
  });
}

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn());
});

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

describe('harness client helpers', () => {
  it('creates sessions through create route', async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValueOnce(
      jsonResponse({
        session: {
          sessionId: 'sess_1',
          projectRoot: '/tmp/project',
          persona: 'WORKING_ITEMS',
          mode: 'WORKBENCH',
          createdAt: '2026-02-23T00:00:00.000Z',
          updatedAt: '2026-02-23T00:00:00.000Z'
        }
      })
    );

    const session = await createHarnessSession({
      projectRoot: '/tmp/project',
      persona: 'WORKING_ITEMS',
      mode: 'WORKBENCH'
    });

    expect(session.sessionId).toBe('sess_1');
    const [input, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(input).toBe('/api/harness/session/create');
    expect(init.method).toBe('POST');
  });

  it('surfaces typed boot errors for non-2xx responses', async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValueOnce(
      jsonResponse(
        {
          error: {
            type: 'PERSONA_NOT_FOUND',
            message: 'Persona not found'
          }
        },
        404
      )
    );

    await expect(bootHarnessSession({ sessionId: 'sess_1' })).rejects.toEqual(
      expect.objectContaining({
        name: 'HarnessApiClientError',
        status: 404,
        code: 'PERSONA_NOT_FOUND'
      }) satisfies Partial<HarnessApiClientError>
    );
  });

  it('parses SSE frames for streaming turns', async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValueOnce(
      sseResponse([
        'event: chat:delta\ndata: {"text":"Hel"}\n\n',
        'event: chat:delta\ndata: {"text":"lo"}\n\n',
        'event: chat:complete\ndata: {"text":"Hello"}\n\n',
        'event: process:exit\ndata: {"exitCode":0}\n\n'
      ])
    );

    const events: Array<{ event: string; data: unknown }> = [];

    await streamHarnessTurn(
      {
        sessionId: 'sess_1',
        message: 'hello'
      },
      (event) => {
        events.push(event);
      }
    );

    expect(events.map((entry) => entry.event)).toEqual([
      'chat:delta',
      'chat:delta',
      'chat:complete',
      'process:exit'
    ]);
    expect(fetchMock).toHaveBeenCalledWith(
      '/api/harness/turn',
      expect.objectContaining({
        method: 'POST'
      })
    );
  });

  it('supports attachment-only turn payloads with string path arrays', async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValueOnce(
      sseResponse([
        'event: process:exit\\ndata: {\"exitCode\":0}\\n\\n'
      ])
    );

    await streamHarnessTurn(
      {
        sessionId: 'sess_1',
        message: '',
        attachments: ['/tmp/sample.txt'],
        opts: {
          model: 'claude-test',
          maxTurns: 3
        }
      },
      () => {
        // no-op
      }
    );

    const [, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(init.body).toBe(
      JSON.stringify({
        sessionId: 'sess_1',
        message: '',
        attachments: ['/tmp/sample.txt'],
        opts: {
          model: 'claude-test',
          maxTurns: 3
        }
      })
    );
  });

  it('parses typed process-exit error payloads from SSE responses', async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValueOnce(
      sseResponse([
        'event: session:init\ndata: {"claudeSessionId":"claude_1","model":"claude-test"}\n\n',
        'event: process:exit\ndata: {"exitCode":1,"error":"Turn failed before completion","errorType":"SDK_FAILURE","status":500,"errorDetails":{"marker":"TURN_SDK_FAIL_TEST"}}\n\n'
      ])
    );

    const events: Array<{ event: string; data: unknown }> = [];

    await streamHarnessTurn(
      {
        sessionId: 'sess_1',
        message: 'TURN_SDK_FAIL_TEST'
      },
      (event) => {
        events.push(event);
      }
    );

    expect(events).toHaveLength(2);
    expect(events[1].event).toBe('process:exit');
    expect(events[1].data).toMatchObject({
      exitCode: 1,
      errorType: 'SDK_FAILURE',
      status: 500,
      errorDetails: {
        marker: 'TURN_SDK_FAIL_TEST'
      }
    });
  });

  it('parses typed turn:error payloads from SSE responses', async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValueOnce(
      sseResponse([
        'event: turn:error\ndata: {"phase":"mid-stream","errorType":"SDK_FAILURE","message":"Turn failed before completion","status":500,"severity":"error","fatal":true,"details":{"marker":"TURN_SDK_FAIL_TEST"}}\n\n',
        'event: process:exit\ndata: {"exitCode":1,"errorType":"SDK_FAILURE","status":500}\n\n'
      ])
    );

    const events: Array<{ event: string; data: unknown }> = [];

    await streamHarnessTurn(
      {
        sessionId: 'sess_1',
        message: 'TURN_SDK_FAIL_TEST'
      },
      (event) => {
        events.push(event);
      }
    );

    expect(events).toHaveLength(2);
    expect(events[0].event).toBe('turn:error');
    expect(events[0].data).toMatchObject({
      phase: 'mid-stream',
      errorType: 'SDK_FAILURE',
      status: 500,
      severity: 'error',
      fatal: true,
      details: {
        marker: 'TURN_SDK_FAIL_TEST'
      }
    });
  });

  it('scaffolds execution roots through scaffold route', async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValueOnce(
      jsonResponse({
        executionRoot: '/tmp/execution',
        decompositionPath: '/tmp/decomposition.md',
        copiedDecompositionPath: '/tmp/execution/_Decomposition/decomposition.md',
        projectName: 'Example',
        coordinationMode: 'DEPENDENCY_TRACKED',
        packageCount: 1,
        deliverableCount: 1,
        created: {
          directories: ['/tmp/execution/_Coordination'],
          files: ['/tmp/execution/INIT.md']
        },
        layoutValidation: {
          valid: true,
          executionRoot: {
            path: '/tmp/execution',
            valid: true,
            missing: []
          },
          packages: [],
          deliverables: []
        },
        preparationCompatibility: {
          ready: true,
          deliverablesChecked: 1,
          issueCount: 0,
          deliverables: []
        }
      })
    );

    const result = await scaffoldHarnessExecutionRoot({
      executionRoot: '/tmp/execution',
      decompositionPath: '/tmp/decomposition.md'
    });

    expect(result.layoutValidation.valid).toBe(true);
    expect(result.preparationCompatibility.ready).toBe(true);
    const [input, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(input).toBe('/api/harness/scaffold');
    expect(init.method).toBe('POST');
  });

  it('lists direct-chat personas through the Type-0/Type-1 filtered route', async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValueOnce(
      jsonResponse({
        agents: [
          { name: 'HELPS_HUMANS', type: 0, class: 'PERSONA' },
          { name: 'WORKING_ITEMS', type: 1, class: 'PERSONA' }
        ]
      })
    );

    const agents = await listDirectChatPersonas();

    expect(agents.map((agent) => agent.name)).toEqual(['HELPS_HUMANS', 'WORKING_ITEMS']);
    const [input, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(input).toBe('/api/harness/agents?directChat=1');
    expect(init.method).toBe('GET');
  });

  it('lists sessions for a working root', async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValueOnce(
      jsonResponse({
        sessions: [
          {
            sessionId: 'sess_1',
            projectRoot: '/tmp/project',
            persona: 'WORKING_ITEMS',
            mode: 'CHAT',
            createdAt: '2026-06-18T00:00:00.000Z',
            updatedAt: '2026-06-18T00:00:00.000Z'
          }
        ]
      })
    );

    const sessions = await listHarnessSessions('/tmp/project');

    expect(sessions.map((session) => session.sessionId)).toEqual(['sess_1']);
    const [input, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(input).toBe('/api/harness/session/list?projectRoot=%2Ftmp%2Fproject');
    expect(init.method).toBe('GET');
  });

  it('replays a session event log through the events route', async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockResolvedValueOnce(
      jsonResponse({
        events: [
          {
            schemaVersion: 1,
            eventId: 'e1',
            sessionId: 'sess_1',
            timestamp: '2026-06-18T00:00:00.000Z',
            type: 'tool.started',
            data: { toolUseId: 't1', toolName: 'Read' }
          }
        ],
        malformedLineCount: 2,
        summary: { eventCount: 1, malformedLineCount: 2, eventTypeCounts: { 'tool.started': 1 } }
      })
    );

    const replay = await replaySessionEvents('sess_1');

    expect(replay.events).toHaveLength(1);
    expect(replay.malformedLineCount).toBe(2);
    const [input, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(input).toBe('/api/harness/session/sess_1/events');
    expect(init.method).toBe('GET');
  });
});
