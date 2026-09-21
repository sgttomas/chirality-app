import { afterEach, describe, expect, it, vi } from 'vitest';

import {
  installBoundDaemonHarnessPort,
  installHostedBootstrapPort,
  resetDaemonHarnessPortForTests
} from '../../../lib/runtime-client/daemon-harness-port';
import {
  createFakeDaemonHarnessPort,
  createFakeHostedBootstrapPort
} from './fake-daemon-harness-port';
import * as statusRoute from '../../../app/api/harness/hosted-bootstrap/status/route';
import * as initializeRoute from '../../../app/api/harness/hosted-bootstrap/project/initialize/route';
import * as bindRoute from '../../../app/api/harness/hosted-bootstrap/project/bind/route';
import * as consentRoute from '../../../app/api/harness/hosted-bootstrap/provider-network-consent/route';
import * as startRoute from '../../../app/api/harness/hosted-bootstrap/login/start/route';
import * as cancelRoute from '../../../app/api/harness/hosted-bootstrap/login/cancel/route';
import * as logoutRoute from '../../../app/api/harness/hosted-bootstrap/logout/route';

afterEach(() => {
  resetDaemonHarnessPortForTests();
  vi.restoreAllMocks();
});

describe('hosted bootstrap API boundary', () => {
  it('reports an unregistered folder without invoking initialization', async () => {
    const initializeProject = vi.fn();
    installHostedBootstrapPort({
      ...createFakeHostedBootstrapPort(),
      initializeProject
    });

    const response = await statusRoute.GET(new Request(
      'http://localhost/api/harness/hosted-bootstrap/status?projectRoot=%2Fselected'
    ));

    expect(response.status).toBe(200);
    await expect(response.json()).resolves.toEqual({ registration: 'required' });
    expect(initializeProject).not.toHaveBeenCalled();
  });

  it('carries hosted account status for a registered folder through the App status route', async () => {
    const status = {
      schema: 'chirality-hosted-bootstrap-status/v1',
      projectId: 'project-one',
      ceremony: 'signed-in',
      admission: 'ready',
      canStartLogin: false
    };
    const getStatus = vi.fn().mockResolvedValue({
      registration: 'registered',
      projectId: 'project-one',
      status
    });
    installHostedBootstrapPort({ ...createFakeHostedBootstrapPort(), getStatus });

    const response = await statusRoute.GET(new Request(
      'http://localhost/api/harness/hosted-bootstrap/status?projectRoot=%2Fselected'
    ));

    expect(response.status).toBe(200);
    const payload = await response.json();
    expect(payload).toEqual({ registration: 'registered', projectId: 'project-one', status });
    expect(getStatus).toHaveBeenCalledWith('/selected', { signal: expect.any(AbortSignal) });
  });

  it('binds an existing registration without invoking explicit initialization', async () => {
    const bindProject = vi.fn().mockResolvedValue({
      registration: 'registered',
      projectId: 'project-one'
    });
    const initializeProject = vi.fn();
    installHostedBootstrapPort({
      ...createFakeHostedBootstrapPort(),
      bindProject,
      initializeProject
    });

    const response = await bindRoute.POST(new Request(
      'http://localhost/api/harness/hosted-bootstrap/project/bind',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectRoot: '/selected' })
      }
    ));

    expect(response.status).toBe(200);
    await expect(response.json()).resolves.toEqual({
      registration: 'registered',
      projectId: 'project-one'
    });
    expect(bindProject).toHaveBeenCalledWith('/selected', {
      signal: expect.any(AbortSignal)
    });
    expect(initializeProject).not.toHaveBeenCalled();
  });

  it('answers the retained consent path with the current status and forwards login actions through the bootstrap port', async () => {
    const grantProviderNetworkConsent = vi.fn().mockResolvedValue({
      schema: 'chirality-hosted-bootstrap-status/v1',
      projectId: 'project-one',
      ceremony: 'ready-to-start',
      admission: 'unavailable',
      canStartLogin: true
    });
    const startLogin = vi.fn().mockResolvedValue({
      loginId: 'login-1',
      authUrl: 'https://example.test/login'
    });
    const cancelLogin = vi.fn().mockResolvedValue({
      schema: 'chirality-hosted-bootstrap-status/v1',
      projectId: 'project-one',
      ceremony: 'cancelled',
      admission: 'unavailable',
      canStartLogin: true
    });
    installHostedBootstrapPort({
      ...createFakeHostedBootstrapPort(),
      grantProviderNetworkConsent,
      startLogin,
      cancelLogin
    });

    // No consent step exists under D-GOV-43: the route only reports status,
    // whatever the body says about consent.
    const consented = await consentRoute.POST(new Request(
      'http://localhost/api/harness/hosted-bootstrap/provider-network-consent',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectRoot: '/selected', consent: false })
      }
    ));
    expect(consented.status).toBe(200);
    await expect(consented.json()).resolves.toEqual(expect.objectContaining({ ceremony: 'ready-to-start' }));
    expect(grantProviderNetworkConsent).toHaveBeenCalledWith(
      '/selected',
      { signal: expect.any(AbortSignal) }
    );

    const started = await startRoute.POST(new Request(
      'http://localhost/api/harness/hosted-bootstrap/login/start',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectRoot: '/selected' })
      }
    ));
    expect(started.status).toBe(200);
    await expect(started.json()).resolves.toEqual({
      loginId: 'login-1',
      authUrl: 'https://example.test/login'
    });

    const cancelled = await cancelRoute.POST(new Request(
      'http://localhost/api/harness/hosted-bootstrap/login/cancel',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectRoot: '/selected' })
      }
    ));
    expect(cancelled.status).toBe(200);
    expect(cancelLogin).toHaveBeenCalledWith(
      '/selected',
      { signal: expect.any(AbortSignal) }
    );
  });

  it('forwards project-local sign-out using only the selected project root', async () => {
    const signOut = vi.fn().mockResolvedValue({
      schema: 'chirality-hosted-bootstrap-status/v1',
      projectId: 'project-one',
      ceremony: 'ready-to-start',
      admission: 'unavailable',
      canStartLogin: true
    });
    installHostedBootstrapPort({ ...createFakeHostedBootstrapPort(), signOut });
    const response = await logoutRoute.POST(new Request(
      'http://localhost/api/harness/hosted-bootstrap/logout',
      { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ projectRoot: '/selected' }) }
    ));
    expect(response.status).toBe(200);
    const payload = await response.json();
    expect(payload).toEqual(expect.objectContaining({ ceremony: 'ready-to-start', admission: 'unavailable' }));
    expect(JSON.stringify(payload)).not.toMatch(/token|credential|identity|path/i);
    expect(signOut).toHaveBeenCalledWith('/selected', { signal: expect.any(AbortSignal) });
  });

  it('keeps the verified normal port binding across separate Next route module loads', async () => {
    const roles = {
      schemaVersion: 'chirality.roles/v3' as const,
      defaultRole: 'HELP_HUMAN' as const,
      roles: []
    };
    const normalPort = {
      ...createFakeDaemonHarnessPort(),
      listRoles: vi.fn().mockResolvedValue(roles)
    };
    installHostedBootstrapPort({
      ...createFakeHostedBootstrapPort(),
      async initializeProject(projectRoot) {
        installBoundDaemonHarnessPort(
          normalPort,
          { projectId: 'project-one', projectRoot },
          true
        );
        return { registration: 'registered', projectId: 'project-one' };
      }
    });

    const initialized = await initializeRoute.POST(new Request(
      'http://localhost/api/harness/hosted-bootstrap/project/initialize',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ projectRoot: '/selected' })
      }
    ));
    expect(initialized.status).toBe(200);
    const initializedPayload = await initialized.json();
    expect(initializedPayload).toEqual({ registration: 'registered', projectId: 'project-one' });
    expect(initializedPayload).not.toHaveProperty('status');

    vi.resetModules();
    const rolesRoute = await import('../../../app/api/harness/roles/route');
    const response = await rolesRoute.GET(new Request(
      'http://localhost/api/harness/roles?projectRoot=%2Fselected'
    ));
    expect(response.status).toBe(200);
    await expect(response.json()).resolves.toEqual(roles);
    expect(normalPort.listRoles).toHaveBeenCalledWith(
      '/selected',
      { signal: expect.any(AbortSignal) }
    );
  });
});
