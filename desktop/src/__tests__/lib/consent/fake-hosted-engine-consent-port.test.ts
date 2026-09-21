import { describe, expect, it } from 'vitest';
import {
  createFakeHostedEngineConsentPort,
  type FakeAdmissionRequest
} from '../../../lib/consent/fake-hosted-engine-consent-port';
import {
  CONSENT_UX_FIXTURES,
  CONSENT_UX_FIXTURE_NAMES,
  FIXTURE_ACCOUNT_A,
  FIXTURE_ACCOUNT_B,
  FIXTURE_CANONICAL_ROOT,
  FIXTURE_CODEX_HOME,
  FIXTURE_NULL_EMAIL_ACCOUNT,
  FIXTURE_PROMPT_HOST,
  consentUxFixture
} from '../../../lib/consent/consent-ux-fixtures';
import {
  COMMAND_NETWORK_POSTURES,
  CONSENT_STATUSES,
  DEFAULT_COMMAND_NETWORK_POSTURE,
  PRODUCT_POSTURE_LABEL,
  ROLE_POSTURES,
  compareConsentScopes,
  currentConsentScope,
  destinationKey,
  isCommandNetworkPosture,
  isRolePosture,
  type HostedEngineConsentSnapshot,
  type NetworkDestinationPrompt
} from '../../../lib/consent/hosted-engine-consent-port';

/**
 * Consent/revocation, account-transition, network-posture, and role-entry
 * behaviour of the fake `HostedEngineConsentPort` (DEL-02-05-V3-02), modelled
 * on App CONTRACT K-CONSENT-1 / K-NET-1 / K-KEY-1 / K-ROLE-2. These are
 * fixture tests behind a fake: they prove the UI-facing state machine and the
 * fixture bytes, not any live account, login, or network behaviour.
 */

const PROMPT: NetworkDestinationPrompt = {
  promptId: 'prompt-test-1',
  host: FIXTURE_PROMPT_HOST,
  protocol: 'https',
  port: 443,
  queuedRequestCount: 3,
  requestedBy: 'curl'
};

/** Strings that must never appear in any snapshot: secrets, emails, ambient login state. */
const FORBIDDEN_SNAPSHOT_FRAGMENTS = ['token', 'Bearer', 'sk-ant', 'cookie', 'device_code', '@', '/.codex'];

function assertNoSecret(snapshot: HostedEngineConsentSnapshot): void {
  const json = JSON.stringify(snapshot);
  for (const fragment of FORBIDDEN_SNAPSHOT_FRAGMENTS) {
    expect(json, `snapshot must not contain ${fragment}`).not.toContain(fragment);
  }
}

async function loginAndGrant(port = createFakeHostedEngineConsentPort()) {
  expect(await port.login()).toEqual({ ok: true });
  expect(await port.grantConsent()).toEqual({ ok: true });
  return port;
}

describe('consent UX fixtures (static bytes)', () => {
  it('cover every consent status, every command-network posture, and both role-enforcement states', () => {
    const consentStatuses = new Set<string>();
    const postures = new Set<string>();
    const enforcement = new Set<string>();
    for (const name of CONSENT_UX_FIXTURE_NAMES) {
      const fixture = CONSENT_UX_FIXTURES[name];
      consentStatuses.add(fixture.consent.status);
      postures.add(fixture.network.posture);
      enforcement.add(fixture.role.enforcement);
      expect(fixture.productPosture).toBe(PRODUCT_POSTURE_LABEL);
      expect(fixture.privateHome.ambientCodexRead).toBe(false);
      expect(fixture.privateHome.codexHome).toBe(FIXTURE_CODEX_HOME);
      expect(isCommandNetworkPosture(fixture.network.posture)).toBe(true);
      expect(isRolePosture(fixture.role.selected)).toBe(true);
      assertNoSecret(fixture);
    }
    expect([...consentStatuses].sort()).toEqual([...CONSENT_STATUSES].sort());
    expect([...postures].sort()).toEqual([...COMMAND_NETWORK_POSTURES].sort());
    expect([...enforcement].sort()).toEqual(['mechanicallyProven', 'notMechanicallyEnforced']);
  });

  it('default to no command network and never pre-accept a destination', () => {
    expect(DEFAULT_COMMAND_NETWORK_POSTURE).toBe('off');
    expect(CONSENT_UX_FIXTURES.loggedOutDefault.network.posture).toBe('off');
    expect(CONSENT_UX_FIXTURES.loggedInNotGranted.network.posture).toBe('off');
    expect(CONSENT_UX_FIXTURES.grantedNetworkOff.network.posture).toBe('off');
    for (const name of CONSENT_UX_FIXTURE_NAMES) {
      if (name !== 'askPerDestinationSessionAccepted') {
        expect(CONSENT_UX_FIXTURES[name].network.sessionAcceptedDestinations).toEqual([]);
      }
    }
  });

  it('name only reserved-TLD hosts and app-owned paths', () => {
    const json = JSON.stringify(CONSENT_UX_FIXTURES);
    expect(json).toContain('.test');
    expect(json).not.toMatch(/\.(com|net|org|io|ai)\b/);
    expect(json).not.toContain('~/.codex');
    expect(json).not.toContain('/.codex');
  });

  it('are handed out as deep copies', () => {
    const a = consentUxFixture('askPerDestinationPending');
    a.network.pendingPrompt!.host = 'mutated.test';
    expect(CONSENT_UX_FIXTURES.askPerDestinationPending.network.pendingPrompt?.host).toBe(FIXTURE_PROMPT_HOST);
  });

  it('describe stale fixtures with the mismatches compareConsentScopes recomputes', () => {
    const transition = CONSENT_UX_FIXTURES.accountTransitionStale;
    expect(transition.consent.status).toBe('stale');
    if (transition.consent.status === 'stale') {
      expect(compareConsentScopes(transition.consent.grantedScope, currentConsentScope(transition))).toEqual(
        transition.consent.mismatches
      );
    }
    const policy = CONSENT_UX_FIXTURES.policyRotatedStale;
    if (policy.consent.status === 'stale') {
      expect(compareConsentScopes(policy.consent.grantedScope, currentConsentScope(policy))).toEqual(['policy']);
    }
    const granted = CONSENT_UX_FIXTURES.grantedNetworkOff;
    if (granted.consent.status === 'granted') {
      expect(compareConsentScopes(granted.consent.scope, currentConsentScope(granted))).toEqual([]);
    }
  });
});

describe('fake HostedEngineConsentPort — login, logout, and account identity', () => {
  it('starts signed out with no private home, nothing granted, and no command network', () => {
    const snapshot = createFakeHostedEngineConsentPort().getSnapshot();
    expect(snapshot.account).toEqual({ status: 'loggedOut' });
    expect(snapshot.privateHome).toEqual({ codexHome: FIXTURE_CODEX_HOME, status: 'absent', ambientCodexRead: false });
    expect(snapshot.consent).toEqual({ status: 'notGranted' });
    expect(snapshot.network).toEqual({ posture: 'off', pendingPrompt: null, sessionAcceptedDestinations: [] });
    expect(snapshot.canonicalRoot).toBe(FIXTURE_CANONICAL_ROOT);
    assertNoSecret(snapshot);
  });

  it('login creates the root-private app-owned home without touching ambient state; logout keeps it', async () => {
    const port = createFakeHostedEngineConsentPort();
    expect(await port.login()).toEqual({ ok: true });
    let snapshot = port.getSnapshot();
    expect(snapshot.account).toEqual({ status: 'loggedIn', identity: FIXTURE_ACCOUNT_A });
    expect(snapshot.privateHome.status).toBe('present');
    expect(snapshot.privateHome.ambientCodexRead).toBe(false);
    assertNoSecret(snapshot);

    expect(await port.login()).toEqual({ ok: false, error: 'Already signed in for this root.' });
    expect(await port.logout()).toEqual({ ok: true });
    snapshot = port.getSnapshot();
    expect(snapshot.account).toEqual({ status: 'loggedOut' });
    expect(snapshot.privateHome.status).toBe('present');
    expect(await port.logout()).toEqual({ ok: false, error: 'Not signed in for this root.' });
  });

  it('supports an account without an email through a volatile null-email epoch', async () => {
    const port = createFakeHostedEngineConsentPort();
    port.control.setNextLoginIdentity(FIXTURE_NULL_EMAIL_ACCOUNT);
    await port.login();
    const snapshot = port.getSnapshot();
    expect(snapshot.account).toEqual({ status: 'loggedIn', identity: FIXTURE_NULL_EMAIL_ACCOUNT });
    assertNoSecret(snapshot);
  });

  it('hands out snapshots that cannot mutate the port', async () => {
    const port = await loginAndGrant();
    const snapshot = port.getSnapshot();
    snapshot.network.posture = 'on';
    snapshot.account = { status: 'loggedOut' };
    expect(port.getSnapshot().network.posture).toBe('off');
    expect(port.getSnapshot().account.status).toBe('loggedIn');
  });

  it('notifies subscribers on every successful act and stops after unsubscribe', async () => {
    const port = createFakeHostedEngineConsentPort();
    const seen: string[] = [];
    const unsubscribe = port.subscribe((snapshot) => seen.push(snapshot.account.status));
    await port.login();
    await port.logout();
    unsubscribe();
    await port.login();
    expect(seen).toEqual(['loggedIn', 'loggedOut']);
  });
});

describe('fake HostedEngineConsentPort — consent, staleness, and revocation (K-CONSENT-1)', () => {
  it('refuses to grant consent while signed out', async () => {
    const port = createFakeHostedEngineConsentPort();
    expect(await port.grantConsent()).toEqual({ ok: false, error: 'Sign in for this root before granting consent.' });
    expect(port.getSnapshot().consent).toEqual({ status: 'notGranted' });
  });

  it('binds a grant to the full current scope', async () => {
    const port = await loginAndGrant();
    const snapshot = port.getSnapshot();
    expect(snapshot.consent.status).toBe('granted');
    if (snapshot.consent.status === 'granted') {
      expect(snapshot.consent.scope).toEqual(currentConsentScope(snapshot));
      expect(snapshot.consent.scope.account).toEqual(FIXTURE_ACCOUNT_A);
      expect(snapshot.consent.scope.workerGeneration).toBe(1);
      expect(snapshot.consent.grantedAt).toMatch(/^2026-09-03T12:00:\d{2}\.000Z$/);
    }
  });

  it('turns stale on logout and stays stale when a different account signs in (A → B)', async () => {
    const port = await loginAndGrant();
    await port.logout();
    let snapshot = port.getSnapshot();
    expect(snapshot.consent.status).toBe('stale');
    if (snapshot.consent.status === 'stale') {
      expect(snapshot.consent.mismatches).toEqual(['account']);
      expect(snapshot.consent.grantedScope.account).toEqual(FIXTURE_ACCOUNT_A);
    }

    port.control.setNextLoginIdentity(FIXTURE_ACCOUNT_B);
    await port.login();
    snapshot = port.getSnapshot();
    expect(snapshot.account).toEqual({ status: 'loggedIn', identity: FIXTURE_ACCOUNT_B });
    expect(snapshot.consent.status).toBe('stale');
    expect(port.control.admit(requestFor(snapshot))).toEqual({ admitted: false, reason: 'stale', mismatches: ['account'] });
  });

  it('does not silently revive a stale grant when the original account returns; a fresh grant is required', async () => {
    const port = await loginAndGrant();
    await port.logout();
    await port.login();
    expect(port.getSnapshot().consent.status).toBe('stale');
    expect(await port.grantConsent()).toEqual({ ok: true });
    const snapshot = port.getSnapshot();
    expect(snapshot.consent.status).toBe('granted');
    expect(port.control.admit(requestFor(snapshot)).admitted).toBe(true);
  });

  it('turns stale when the notice/policy digest rotates or the configuration changes', async () => {
    const policyPort = await loginAndGrant();
    policyPort.control.rotatePolicy('sha256:policy-rotated');
    const afterPolicy = policyPort.getSnapshot();
    expect(afterPolicy.consent.status).toBe('stale');
    if (afterPolicy.consent.status === 'stale') {
      expect(afterPolicy.consent.mismatches).toEqual(['policy']);
    }

    const configPort = await loginAndGrant();
    configPort.control.setConfigDigest('sha256:config-changed');
    const afterConfig = configPort.getSnapshot();
    expect(afterConfig.consent.status).toBe('stale');
    if (afterConfig.consent.status === 'stale') {
      expect(afterConfig.consent.mismatches).toEqual(['config']);
    }
  });

  it('turns stale when the selected role posture changes after the grant (K-ROLE-2 identity participation)', async () => {
    const port = await loginAndGrant();
    expect(await port.selectRole('agent2')).toEqual({ ok: true });
    const snapshot = port.getSnapshot();
    expect(snapshot.role.selected).toBe('agent2');
    expect(snapshot.consent.status).toBe('stale');
    if (snapshot.consent.status === 'stale') {
      expect(snapshot.consent.mismatches).toEqual(['role']);
    }
  });

  it('revocation retires the generation, invalidates the private home, and drops the network posture to off', async () => {
    const port = await loginAndGrant();
    await port.selectNetworkPosture('askPerDestination');
    port.control.enqueueNetworkPrompt(PROMPT);
    await port.resolveNetworkPrompt(PROMPT.promptId, 'acceptForSession');
    expect(port.getSnapshot().network.sessionAcceptedDestinations).toHaveLength(1);

    expect(await port.revokeConsent()).toEqual({ ok: true });
    const snapshot = port.getSnapshot();
    expect(snapshot.workerGeneration).toBe(2);
    expect(snapshot.privateHome.status).toBe('invalidated');
    expect(snapshot.privateHome.ambientCodexRead).toBe(false);
    expect(snapshot.consent).toMatchObject({ status: 'revoked', retiredGeneration: 1, privateHomeInvalidated: true });
    expect(snapshot.network).toEqual({ posture: 'off', pendingPrompt: null, sessionAcceptedDestinations: [] });
    expect(snapshot.account.status).toBe('loggedIn');
    expect(port.control.admit(requestFor(snapshot))).toEqual({ admitted: false, reason: 'revoked', mismatches: [] });

    expect(await port.revokeConsent()).toEqual({ ok: false, error: 'There is no consent to revoke for this root.' });
  });

  it('a fresh grant after revocation binds to the new generation', async () => {
    const port = await loginAndGrant();
    await port.revokeConsent();
    expect(await port.grantConsent()).toEqual({ ok: true });
    const snapshot = port.getSnapshot();
    expect(snapshot.consent.status).toBe('granted');
    if (snapshot.consent.status === 'granted') {
      expect(snapshot.consent.scope.workerGeneration).toBe(2);
    }
    expect(snapshot.privateHome.status).toBe('present');
  });

  it('a fresh grant recreates the invalidated private home for the new generation', async () => {
    const port = await loginAndGrant();
    await port.revokeConsent();
    expect(port.getSnapshot().privateHome.status).toBe('invalidated');

    expect(await port.grantConsent()).toEqual({ ok: true });
    const snapshot = port.getSnapshot();
    expect(snapshot.workerGeneration).toBe(2);
    expect(snapshot.account.status).toBe('loggedIn');
    expect(snapshot.privateHome).toEqual({
      codexHome: FIXTURE_CODEX_HOME,
      status: 'present',
      ambientCodexRead: false
    });
  });

  it('can revoke a stale grant', async () => {
    const port = await loginAndGrant();
    await port.logout();
    expect(await port.revokeConsent()).toEqual({ ok: true });
    expect(port.getSnapshot().consent.status).toBe('revoked');
  });
});

describe('fake HostedEngineConsentPort — admission (K-CONSENT-1)', () => {
  it('denies before any grant', () => {
    const port = createFakeHostedEngineConsentPort();
    expect(port.control.admit(requestFor(port.getSnapshot()))).toEqual({ admitted: false, reason: 'notGranted', mismatches: [] });
  });

  it('admits a request matching the granted scope and ignores the caller-supplied cwd', async () => {
    const port = await loginAndGrant();
    const snapshot = port.getSnapshot();
    const decision = port.control.admit({ ...requestFor(snapshot), cwd: '/somewhere/else/entirely' });
    expect(decision.admitted).toBe(true);
    if (decision.admitted) {
      expect(decision.scope.canonicalRoot).toBe(FIXTURE_CANONICAL_ROOT);
    }
  });

  it('denies a request whose canonical root differs even when its cwd matches the stored root', async () => {
    const port = await loginAndGrant();
    const decision = port.control.admit({
      ...requestFor(port.getSnapshot()),
      canonicalRoot: '/Users/operator/Projects/other-root',
      cwd: FIXTURE_CANONICAL_ROOT
    });
    expect(decision).toEqual({ admitted: false, reason: 'scopeMismatch', mismatches: ['root'] });
  });

  it('denies on each validated field independently', async () => {
    const port = await loginAndGrant();
    const base = requestFor(port.getSnapshot());
    const cases: Array<[Partial<FakeAdmissionRequest>, string]> = [
      [{ projectId: 'prj_other' }, 'project'],
      [{ adapter: 'other-adapter' }, 'adapter'],
      [{ account: FIXTURE_ACCOUNT_B }, 'account'],
      [{ account: null }, 'account'],
      [{ policyDigest: 'sha256:policy-other' }, 'policy'],
      [{ rolePosture: 'agent1' }, 'role'],
      [{ configDigest: 'sha256:config-other' }, 'config'],
      [{ workerGeneration: 2 }, 'generation']
    ];
    for (const [override, mismatch] of cases) {
      expect(port.control.admit({ ...base, ...override })).toEqual({
        admitted: false,
        reason: 'scopeMismatch',
        mismatches: [mismatch]
      });
    }
  });
});

describe('fake HostedEngineConsentPort — command-network postures (K-NET-1)', () => {
  it('cannot select a posture until consent is granted; the default stays off', async () => {
    const port = createFakeHostedEngineConsentPort();
    await port.login();
    expect(await port.selectNetworkPosture('on')).toEqual({
      ok: false,
      error: 'Grant consent for this root before choosing a command-network posture.'
    });
    expect(port.getSnapshot().network.posture).toBe('off');
  });

  it('rejects an unknown posture', async () => {
    const port = await loginAndGrant();
    expect(await port.selectNetworkPosture('anything' as never)).toEqual({ ok: false, error: 'Unknown command-network posture.' });
  });

  it('offers exactly the three postures and labels the on posture with network_access = true', async () => {
    const port = await loginAndGrant();
    for (const posture of COMMAND_NETWORK_POSTURES) {
      expect(await port.selectNetworkPosture(posture)).toEqual({ ok: true });
      expect(port.getSnapshot().network.posture).toBe(posture);
    }
    expect(COMMAND_NETWORK_POSTURES).toEqual(['off', 'askPerDestination', 'on']);
  });

  it('acceptForSession happens only as an explicit act on a pending prompt', async () => {
    const port = await loginAndGrant();
    await port.selectNetworkPosture('askPerDestination');
    expect(port.getSnapshot().network.sessionAcceptedDestinations).toEqual([]);

    port.control.enqueueNetworkPrompt(PROMPT);
    const pending = port.getSnapshot().network.pendingPrompt;
    expect(pending).toMatchObject({ host: FIXTURE_PROMPT_HOST, protocol: 'https', port: 443, queuedRequestCount: 3 });
    // Nothing has been accepted by the mere existence of the prompt.
    expect(port.getSnapshot().network.sessionAcceptedDestinations).toEqual([]);

    expect(await port.resolveNetworkPrompt(PROMPT.promptId, 'acceptForSession')).toEqual({ ok: true });
    const snapshot = port.getSnapshot();
    expect(snapshot.network.pendingPrompt).toBeNull();
    expect(snapshot.network.sessionAcceptedDestinations).toEqual([destinationKey(PROMPT)]);
    expect(destinationKey(PROMPT)).toBe(`https://${FIXTURE_PROMPT_HOST}:443`);
    expect(port.control.actLog.filter((entry) => entry.startsWith('resolveNetworkPrompt'))).toEqual([
      'resolveNetworkPrompt:acceptForSession'
    ]);
  });

  it('drops command networking and refuses prompt resolution when consent turns stale', async () => {
    const port = await loginAndGrant();
    await port.selectNetworkPosture('askPerDestination');
    port.control.enqueueNetworkPrompt(PROMPT);
    await port.resolveNetworkPrompt(PROMPT.promptId, 'acceptForSession');
    const nextPrompt = { ...PROMPT, promptId: 'prompt-test-stale' };
    port.control.enqueueNetworkPrompt(nextPrompt);

    port.control.rotatePolicy('sha256:policy-rotated');
    expect(port.getSnapshot().consent.status).toBe('stale');
    expect(port.getSnapshot().network).toEqual({
      posture: 'off',
      pendingPrompt: null,
      sessionAcceptedDestinations: []
    });
    expect(await port.resolveNetworkPrompt(nextPrompt.promptId, 'acceptForSession')).toEqual({
      ok: false,
      error: 'Grant consent for this root before resolving a command-network prompt.'
    });
  });

  it('allowOnce and deny resolve the prompt without a session acceptance', async () => {
    for (const decision of ['allowOnce', 'deny'] as const) {
      const port = await loginAndGrant();
      await port.selectNetworkPosture('askPerDestination');
      port.control.enqueueNetworkPrompt(PROMPT);
      expect(await port.resolveNetworkPrompt(PROMPT.promptId, decision)).toEqual({ ok: true });
      expect(port.getSnapshot().network).toEqual({ posture: 'askPerDestination', pendingPrompt: null, sessionAcceptedDestinations: [] });
    }
  });

  it('refuses to resolve a prompt that is not pending or not under ask-per-destination', async () => {
    const port = await loginAndGrant();
    expect(await port.resolveNetworkPrompt('nope', 'allowOnce')).toEqual({ ok: false, error: 'That network prompt is no longer pending.' });
    await port.selectNetworkPosture('askPerDestination');
    port.control.enqueueNetworkPrompt(PROMPT);
    expect(await port.resolveNetworkPrompt('other-id', 'acceptForSession')).toEqual({ ok: false, error: 'That network prompt is no longer pending.' });
    expect(port.getSnapshot().network.sessionAcceptedDestinations).toEqual([]);
  });

  it('leaving ask-per-destination drops the pending prompt unanswered and clears session acceptances', async () => {
    const port = await loginAndGrant();
    await port.selectNetworkPosture('askPerDestination');
    port.control.enqueueNetworkPrompt(PROMPT);
    await port.resolveNetworkPrompt(PROMPT.promptId, 'acceptForSession');
    port.control.enqueueNetworkPrompt({ ...PROMPT, promptId: 'prompt-test-2' });

    await port.selectNetworkPosture('off');
    expect(port.getSnapshot().network).toEqual({ posture: 'off', pendingPrompt: null, sessionAcceptedDestinations: [] });
    expect(port.control.actLog.filter((entry) => entry.startsWith('resolveNetworkPrompt'))).toEqual([
      'resolveNetworkPrompt:acceptForSession'
    ]);
  });

  it('only enqueues runtime prompts while ask-per-destination is selected', async () => {
    const port = await loginAndGrant();
    port.control.enqueueNetworkPrompt(PROMPT);
    expect(port.getSnapshot().network.pendingPrompt).toBeNull();

    await port.selectNetworkPosture('on');
    port.control.enqueueNetworkPrompt(PROMPT);
    expect(port.getSnapshot().network.pendingPrompt).toBeNull();

    await port.selectNetworkPosture('askPerDestination');
    port.control.enqueueNetworkPrompt(PROMPT);
    expect(port.getSnapshot().network.pendingPrompt).toEqual(PROMPT);
  });
});

describe('fake HostedEngineConsentPort — role entry (K-ROLE-2)', () => {
  it('offers all four role postures and rejects an unknown one', async () => {
    const port = createFakeHostedEngineConsentPort();
    expect(ROLE_POSTURES).toEqual(['untyped', 'agent0', 'agent1', 'agent2']);
    for (const role of ROLE_POSTURES) {
      expect(await port.selectRole(role)).toEqual({ ok: true });
      expect(port.getSnapshot().role.selected).toBe(role);
    }
    expect(await port.selectRole('agent3' as never)).toEqual({ ok: false, error: 'Unknown role posture.' });
  });

  it('carries the G-ROLE enforcement state the runtime reports', () => {
    const port = createFakeHostedEngineConsentPort();
    expect(port.getSnapshot().role.enforcement).toBe('notMechanicallyEnforced');
    port.control.setRoleEnforcement('mechanicallyProven');
    expect(port.getSnapshot().role.enforcement).toBe('mechanicallyProven');
  });
});

describe('fake HostedEngineConsentPort — status and failure surfaces', () => {
  it('reports rate-limit and approval status changes', () => {
    const port = createFakeHostedEngineConsentPort();
    port.control.setRateLimit({ status: 'limited', resetsAt: '2026-09-03T13:00:00.000Z', detail: 'quota' });
    port.control.setApprovals({ pendingCount: 2, lastDecision: { outcome: 'approved', at: '2026-09-03T12:30:00.000Z', subject: 'shell' } });
    const snapshot = port.getSnapshot();
    expect(snapshot.rateLimit).toEqual({ status: 'limited', resetsAt: '2026-09-03T13:00:00.000Z', detail: 'quota' });
    expect(snapshot.approvals.pendingCount).toBe(2);
    assertNoSecret(snapshot);
  });

  it('a failed act changes nothing and notifies nobody', async () => {
    const port = createFakeHostedEngineConsentPort();
    let notifications = 0;
    port.subscribe(() => {
      notifications += 1;
    });
    port.control.failNextAct('Consent service unavailable');
    expect(await port.login()).toEqual({ ok: false, error: 'Consent service unavailable' });
    expect(port.getSnapshot().account).toEqual({ status: 'loggedOut' });
    expect(notifications).toBe(0);
    expect(await port.login()).toEqual({ ok: true });
    expect(notifications).toBe(1);
  });

  it('can be seeded from any fixture', () => {
    for (const name of CONSENT_UX_FIXTURE_NAMES) {
      const port = createFakeHostedEngineConsentPort({ initial: consentUxFixture(name) });
      expect(port.getSnapshot()).toEqual(CONSENT_UX_FIXTURES[name]);
    }
  });
});

function requestFor(snapshot: HostedEngineConsentSnapshot): FakeAdmissionRequest {
  const scope = currentConsentScope(snapshot);
  return {
    canonicalRoot: scope.canonicalRoot,
    projectId: scope.projectId,
    adapter: scope.adapter,
    account: scope.account,
    policyDigest: scope.policyDigest,
    rolePosture: scope.rolePosture,
    configDigest: scope.configDigest,
    workerGeneration: scope.workerGeneration
  };
}
