import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { POST } from '../../../app/api/harness/permission/route';
import {
  getPermissionBroker,
  resetPermissionBrokerForTests
} from '../../../lib/harness/permission-broker';
import {
  installDaemonHarnessPort,
  resetDaemonHarnessPortForTests
} from '../../../lib/runtime-client/daemon-harness-port';
import { createFakeDaemonHarnessPort } from './fake-daemon-harness-port';

beforeEach(() => {
  installDaemonHarnessPort(createFakeDaemonHarnessPort());
});

afterEach(() => {
  resetPermissionBrokerForTests();
  resetDaemonHarnessPortForTests();
});

function postPermission(body: unknown): Promise<Response> {
  return POST(
    new Request('http://localhost/api/harness/permission', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
  );
}

describe('POST /api/harness/permission', () => {
  it('delivers an operator verdict to the pending request', async () => {
    const { verdict } = getPermissionBroker().request({ sessionId: 'sess-1', toolUseId: 'tool-1' });

    const response = await postPermission({
      sessionId: 'sess-1',
      toolUseId: 'tool-1',
      verdict: 'allow'
    });

    expect(response.status).toBe(200);
    await expect(response.json()).resolves.toEqual({ ok: true, decided: true });
    await expect(verdict).resolves.toBe('allow');
  });

  it('reports decided=false when no matching request is pending', async () => {
    const response = await postPermission({
      sessionId: 'sess-1',
      toolUseId: 'missing',
      verdict: 'deny'
    });

    expect(response.status).toBe(200);
    await expect(response.json()).resolves.toEqual({ ok: true, decided: false });
  });

  it('rejects an invalid verdict with 400', async () => {
    const response = await postPermission({
      sessionId: 'sess-1',
      toolUseId: 'tool-1',
      verdict: 'maybe'
    });

    expect(response.status).toBe(400);
    const body = (await response.json()) as { error: { type: string } };
    expect(body.error.type).toBe('INVALID_REQUEST');
  });

  it('rejects a missing sessionId with 400', async () => {
    const response = await postPermission({ toolUseId: 'tool-1', verdict: 'allow' });
    expect(response.status).toBe(400);
  });
});
