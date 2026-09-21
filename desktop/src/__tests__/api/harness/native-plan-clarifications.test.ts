import { afterEach, describe, expect, it, vi } from 'vitest';
import { HarnessError } from '@chirality/runtime-contracts/errors';

import {
  installDaemonHarnessPort,
  resetDaemonHarnessPortForTests
} from '../../../lib/runtime-client/daemon-harness-port';
import { createFakeDaemonHarnessPort } from './fake-daemon-harness-port';
import * as clarificationsRoute from '../../../app/api/harness/session/[id]/native-plan/clarifications/route';
import * as replyRoute from '../../../app/api/harness/session/[id]/native-plan/clarifications/reply/route';

afterEach(() => {
  resetDaemonHarnessPortForTests();
  vi.restoreAllMocks();
});

describe('native Plan clarification daemon proxy', () => {
  it('returns pending clarifications from the owned session and forwards the request signal', async () => {
    const result = {
      schemaVersion: 'chirality.native-plan-clarifications/v3' as const,
      status: 'qualified' as const,
      qualification: {
        adapterId: 'codex-app-server',
        providerId: 'openai',
        qualificationId: 'native-plan-v3',
        admissionSha256: 'b'.repeat(64),
        evidenceClass: 'native-adapter-qualified' as const
      },
      clarifications: [{
        clientTurnId: 'client-turn-1',
        providerThreadId: 'thread-1',
        providerTurnId: 'turn-1',
        requestId: 'request/1',
        itemId: 'item-1',
        questions: [],
        isBlocking: true,
        autoResolutionMs: 30_000
      }]
    };
    const listNativePlanClarifications = vi.fn().mockResolvedValue(result);
    installDaemonHarnessPort({
      ...createFakeDaemonHarnessPort(),
      listNativePlanClarifications
    });
    const abortController = new AbortController();

    const response = await clarificationsRoute.GET(
      new Request('http://localhost/api/harness/session/sess-1/native-plan/clarifications', {
        signal: abortController.signal
      }),
      { params: Promise.resolve({ id: 'sess-1' }) }
    );

    expect(response.status).toBe(200);
    await expect(response.json()).resolves.toEqual(result);
    expect(listNativePlanClarifications).toHaveBeenCalledWith(
      'sess-1',
      { signal: expect.any(AbortSignal) }
    );
  });

  it('validates replies before dispatch and preserves a numeric request ID in the body', async () => {
    const result = {
      schemaVersion: 'chirality.native-plan-clarification-reply/v3' as const,
      sessionId: 'sess-1',
      requestId: 42,
      sent: true as const
    };
    const replyNativePlanClarification = vi.fn().mockResolvedValue(result);
    installDaemonHarnessPort({
      ...createFakeDaemonHarnessPort(),
      replyNativePlanClarification
    });
    const answers = { scope: { answers: ['Current'] } };

    const response = await replyRoute.POST(
      new Request('http://localhost/api/harness/session/sess-1/native-plan/clarifications/reply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ requestId: 42, answers })
      }),
      { params: Promise.resolve({ id: 'sess-1' }) }
    );

    expect(response.status).toBe(200);
    await expect(response.json()).resolves.toEqual(result);
    expect(replyNativePlanClarification).toHaveBeenCalledWith(
      'sess-1',
      42,
      answers,
      { signal: expect.any(AbortSignal) }
    );

    const invalid = await replyRoute.POST(
      new Request('http://localhost/api/harness/session/sess-1/native-plan/clarifications/reply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ requestId: 'request-1', answers: { scope: { answers: [1] } } })
      }),
      { params: Promise.resolve({ id: 'sess-1' }) }
    );
    expect(invalid.status).toBe(400);
    await expect(invalid.json()).resolves.toMatchObject({
      error: { type: 'INVALID_REQUEST' }
    });
    expect(replyNativePlanClarification).toHaveBeenCalledOnce();
  });

  it('propagates daemon errors through the existing harness error envelope', async () => {
    installDaemonHarnessPort({
      ...createFakeDaemonHarnessPort(),
      listNativePlanClarifications: vi.fn().mockRejectedValue(
        new HarnessError('SESSION_NOT_FOUND', 404, 'Session not found')
      )
    });

    const response = await clarificationsRoute.GET(
      new Request('http://localhost/api/harness/session/missing/native-plan/clarifications'),
      { params: Promise.resolve({ id: 'missing' }) }
    );

    expect(response.status).toBe(404);
    await expect(response.json()).resolves.toMatchObject({
      error: { type: 'SESSION_NOT_FOUND', message: 'Session not found' }
    });
  });
});
