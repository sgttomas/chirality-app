import { afterEach, describe, expect, it, vi } from 'vitest';

import {
  bindHostedBootstrapProject,
  cancelHostedBootstrapLogin,
  getHostedBootstrapStatus,
  getHostedBootstrapStatusWithRetry,
  hydrateHostedBootstrapProject,
  initializeHostedBootstrapProject,
  signOutHostedBootstrapProject,
  startHostedBootstrapLogin
} from '../../lib/harness/hosted-bootstrap-client';

afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

function json(payload: unknown, status = 200): Response {
  return new Response(JSON.stringify(payload), { status, headers: { 'Content-Type': 'application/json' } });
}

function unavailable(): Response {
  return json({ error: { type: 'ENGINE_UNAVAILABLE', message: 'Runtime service is unavailable' } }, 503);
}

const readyStatus = {
  schema: 'chirality-hosted-bootstrap-status/v1' as const,
  projectId: 'project-one',
  ceremony: 'ready-to-start' as const,
  admission: 'unavailable' as const,
  canStartLogin: true
};

describe('hosted bootstrap renderer client (App routes, no desktop account IPC)', () => {
  it('reads status through the App status route with only the selected project root', async () => {
    const fetchMock = vi.fn().mockResolvedValue(json({ registration: 'required' }));
    vi.stubGlobal('fetch', fetchMock);
    vi.stubGlobal('window', { chirality: { runtime: {} } });
    await expect(getHostedBootstrapStatus('/project one')).resolves.toEqual({ registration: 'required' });
    expect(fetchMock).toHaveBeenCalledWith(
      '/api/harness/hosted-bootstrap/status?projectRoot=%2Fproject%20one',
      expect.objectContaining({ method: 'GET' })
    );
  });

  it('passes a ready status carrying the model catalog and selection through untouched', async () => {
    const result = {
      registration: 'registered',
      projectId: 'project-one',
      status: {
        ...readyStatus,
        ceremony: 'signed-in',
        admission: 'ready',
        canStartLogin: false,
        models: [
          { model: 'gpt-default', isDefault: true, defaultReasoningEffort: 'high', supportedReasoningEfforts: ['low', 'medium', 'high'] },
          { model: 'gpt-alt', isDefault: false, defaultReasoningEffort: 'medium', supportedReasoningEfforts: ['medium', 'low'] }
        ],
        selection: { model: 'gpt-default', reasoningEffort: 'high' }
      }
    };
    const fetchMock = vi.fn().mockImplementation(async () => json(result));
    vi.stubGlobal('fetch', fetchMock);
    await expect(getHostedBootstrapStatus('/project one')).resolves.toEqual(result);
    await expect(getHostedBootstrapStatusWithRetry('/project one')).resolves.toEqual(result);
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it('routes initialization and every account effect through App routes', async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(json({ registration: 'registered', projectId: 'project-one' }))
      .mockResolvedValueOnce(json({ registration: 'registered', projectId: 'project-one' }))
      .mockResolvedValueOnce(json({ loginId: 'login-1', authUrl: 'https://example.test/login' }))
      .mockResolvedValueOnce(json({ ...readyStatus, ceremony: 'cancelled' }))
      .mockResolvedValueOnce(json(readyStatus));
    vi.stubGlobal('fetch', fetchMock);

    await bindHostedBootstrapProject('/project');
    const initialized = await initializeHostedBootstrapProject('/project');
    expect(initialized).toEqual({ registration: 'registered', projectId: 'project-one' });
    expect(initialized).not.toHaveProperty('status');
    await expect(startHostedBootstrapLogin('/project')).resolves.toEqual({ loginId: 'login-1', authUrl: 'https://example.test/login' });
    await expect(cancelHostedBootstrapLogin('/project')).resolves.toEqual({ ...readyStatus, ceremony: 'cancelled' });
    await expect(signOutHostedBootstrapProject('/project')).resolves.toEqual(readyStatus);

    const urls = fetchMock.mock.calls.map((call) => call[0]);
    expect(urls).toEqual([
      '/api/harness/hosted-bootstrap/project/bind',
      '/api/harness/hosted-bootstrap/project/initialize',
      '/api/harness/hosted-bootstrap/login/start',
      '/api/harness/hosted-bootstrap/login/cancel',
      '/api/harness/hosted-bootstrap/logout'
    ]);
    for (const call of fetchMock.mock.calls) {
      expect(call[1]).toEqual(expect.objectContaining({ method: 'POST' }));
      expect(JSON.parse(call[1].body)).toEqual({ projectRoot: '/project' });
    }
  });

  it('surfaces the App error message and status on a rejected action', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(json({ error: { type: 'INVALID_REQUEST', message: 'Sign-in could not start.' } }, 400)));
    await expect(startHostedBootstrapLogin('/project')).rejects.toMatchObject({ status: 400, message: 'Sign-in could not start.' });
  });

  it('retries a 503 status read with the transient ladder and stops on other failures', async () => {
    vi.useFakeTimers();
    const recovered = { registration: 'registered' as const, projectId: 'project-one', status: readyStatus };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(unavailable())
      .mockResolvedValueOnce(json(recovered));
    vi.stubGlobal('fetch', fetchMock);

    const operation = getHostedBootstrapStatusWithRetry('/project');
    await vi.advanceTimersByTimeAsync(250);

    await expect(operation).resolves.toEqual(recovered);
    expect(fetchMock).toHaveBeenCalledTimes(2);

    fetchMock.mockResolvedValueOnce(json({ error: { type: 'INVALID_REQUEST', message: 'account unavailable' } }, 400));
    await expect(getHostedBootstrapStatusWithRetry('/project')).rejects.toThrow('account unavailable');
    expect(vi.getTimerCount()).toBe(0);
  });

  it('forwards the AbortSignal to fetch and rejects before sending once aborted', async () => {
    const fetchMock = vi.fn().mockResolvedValue(json(readyStatus));
    vi.stubGlobal('fetch', fetchMock);
    const controller = new AbortController();
    await signOutHostedBootstrapProject('/project', controller.signal);
    expect(fetchMock.mock.calls[0][1].signal).toBe(controller.signal);

    controller.abort(new DOMException('cancelled', 'AbortError'));
    await expect(signOutHostedBootstrapProject('/project', controller.signal)).rejects.toMatchObject({ name: 'AbortError' });
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it('publishes a recovered binding before an independent account-status failure', async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(json({ registration: 'registered', projectId: 'restart-project' }))
      .mockResolvedValueOnce(json({ error: { type: 'INVALID_REQUEST', message: 'account unavailable' } }, 400));
    vi.stubGlobal('fetch', fetchMock);
    const onBound = vi.fn();

    await expect(hydrateHostedBootstrapProject('/project', onBound))
      .rejects.toThrow('account unavailable');
    expect(onBound).toHaveBeenCalledWith({
      registration: 'registered',
      projectId: 'restart-project'
    });
    expect(fetchMock.mock.calls[1][0]).toBe('/api/harness/hosted-bootstrap/status?projectRoot=%2Fproject');
  });

  it('retries transient account startup failures without repeating the project bind', async () => {
    vi.useFakeTimers();
    const recovered = { registration: 'registered' as const, projectId: 'restart-project', status: { ...readyStatus, projectId: 'restart-project' } };
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(json({ registration: 'registered', projectId: 'restart-project' }))
      .mockResolvedValueOnce(unavailable())
      .mockResolvedValueOnce(unavailable())
      .mockResolvedValueOnce(unavailable())
      .mockResolvedValueOnce(json(recovered));
    vi.stubGlobal('fetch', fetchMock);

    const operation = hydrateHostedBootstrapProject('/project', vi.fn());
    await vi.advanceTimersByTimeAsync(250);
    await vi.advanceTimersByTimeAsync(1_000);
    await vi.advanceTimersByTimeAsync(5_000);

    await expect(operation).resolves.toEqual(recovered);
    const binds = fetchMock.mock.calls.filter((call) => call[0] === '/api/harness/hosted-bootstrap/project/bind');
    expect(binds).toHaveLength(1);
    expect(fetchMock).toHaveBeenCalledTimes(5);
  });

  it('aborts a pending account startup retry and clears its timer', async () => {
    vi.useFakeTimers();
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(json({ registration: 'registered', projectId: 'restart-project' }))
      .mockImplementation(async () => unavailable());
    vi.stubGlobal('fetch', fetchMock);
    const controller = new AbortController();
    const operation = hydrateHostedBootstrapProject('/project', vi.fn(), controller.signal);
    await vi.advanceTimersByTimeAsync(0);

    controller.abort(new DOMException('cancelled', 'AbortError'));

    await expect(operation).rejects.toMatchObject({ name: 'AbortError' });
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(vi.getTimerCount()).toBe(0);
  });
});
