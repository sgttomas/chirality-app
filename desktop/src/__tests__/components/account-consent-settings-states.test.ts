import { createElement } from 'react';
import { act, create, type ReactTestInstance, type ReactTestRenderer } from 'react-test-renderer';
import { describe, expect, it } from 'vitest';
import {
  AccountConsentSettings,
  AccountConsentSettingsView,
  type AccountConsentSettingsViewProps
} from '../../components/settings/account-consent-settings';
import {
  createFakeHostedEngineConsentPort,
  type FakeHostedEngineConsentPort
} from '../../lib/consent/fake-hosted-engine-consent-port';
import {
  CONSENT_UX_FIXTURES,
  CONSENT_UX_FIXTURE_NAMES,
  FIXTURE_CODEX_HOME,
  FIXTURE_PROMPT_HOST,
  consentUxFixture,
  type ConsentUxFixtureName
} from '../../lib/consent/consent-ux-fixtures';
import {
  COMMAND_NETWORK_ON_CONFIG_LABEL,
  PRODUCT_POSTURE_LABEL,
  ROLE_NOT_MECHANICALLY_ENFORCED_LABEL,
  type HostedEngineConsentSnapshot
} from '../../lib/consent/hosted-engine-consent-port';

/**
 * D-APP-36 render evidence for the hosted-engine account/consent panel
 * (DEL-02-05-V3-02; WP-07 static fixtures behind the fake
 * `HostedEngineConsentPort`; fixture evidence toward the UI portions of
 * AT-008/009/010/012/016/020/023/034).
 *
 * The panel must render every fixture distinctly — login/logout and account
 * identity, consent/revocation, the three command-network postures with the
 * ask-per-destination prompt and its queued-request caveat, rate-limit and
 * approval status, the `Opt-in Preview` label, and role entry with the
 * `role not mechanically enforced` label — with controls enabled or disabled
 * as the state requires, and every state change must originate from an
 * explicit user act on a control. Assertions are structural and copy-bearing
 * where the copy is the contract; they do not assert colours or geometry.
 * Nothing here is a live account, login, or network claim.
 */

const noop = (): void => undefined;

const viewBase: AccountConsentSettingsViewProps = {
  snapshot: null,
  busy: false,
  error: null,
  onLogin: noop,
  onLogout: noop,
  onGrantConsent: noop,
  onRevokeConsent: noop,
  onSelectNetworkPosture: noop,
  onResolveNetworkPrompt: noop,
  onSelectRole: noop
};

const FORBIDDEN_DOM_FRAGMENTS = ['token', 'Bearer', 'sk-ant', 'cookie', 'device_code', '@'];

function renderView(overrides: Partial<AccountConsentSettingsViewProps>): ReactTestRenderer {
  let renderer!: ReactTestRenderer;
  act(() => {
    renderer = create(createElement(AccountConsentSettingsView, { ...viewBase, ...overrides }));
  });
  return renderer;
}

function renderFixture(name: ConsentUxFixtureName): ReactTestRenderer {
  return renderView({ snapshot: consentUxFixture(name) });
}

function renderWithPort(port: FakeHostedEngineConsentPort): ReactTestRenderer {
  let renderer!: ReactTestRenderer;
  act(() => {
    renderer = create(createElement(AccountConsentSettings, { port }));
  });
  return renderer;
}

function textOf(instance: ReactTestInstance): string {
  const parts: string[] = [];
  const walk = (node: ReactTestInstance | string): void => {
    if (typeof node === 'string') {
      parts.push(node);
      return;
    }
    for (const child of node.children) {
      walk(child);
    }
  };
  walk(instance);
  return parts.join('');
}

function json(renderer: ReactTestRenderer): string {
  return JSON.stringify(renderer.toJSON());
}

function findByProp(renderer: ReactTestRenderer, prop: string, value?: string): ReactTestInstance {
  return renderer.root.find(
    (node) => typeof node.type === 'string' && node.props[prop] !== undefined && (value === undefined || node.props[prop] === value)
  );
}

function findAllByProp(renderer: ReactTestRenderer, prop: string): ReactTestInstance[] {
  return renderer.root.findAll((node) => typeof node.type === 'string' && node.props[prop] !== undefined);
}

function section(renderer: ReactTestRenderer, name: string): ReactTestInstance {
  return findByProp(renderer, 'data-section', name);
}

function buttonLabels(instance: ReactTestInstance): string[] {
  return instance.findAllByType('button').map((button) => textOf(button));
}

function buttonByLabel(instance: ReactTestInstance, label: string): ReactTestInstance {
  return instance.find((node) => node.type === 'button' && textOf(node) === label);
}

function radio(renderer: ReactTestRenderer, name: string, value: string): ReactTestInstance {
  return renderer.root.find(
    (node) => node.type === 'input' && node.props.type === 'radio' && node.props.name === name && node.props.value === value
  );
}

function assertNoSecret(renderer: ReactTestRenderer): void {
  const html = json(renderer);
  for (const fragment of FORBIDDEN_DOM_FRAGMENTS) {
    expect(html, `rendered tree must not contain ${fragment}`).not.toContain(fragment);
  }
}

async function click(instance: ReactTestInstance): Promise<void> {
  await act(async () => {
    instance.props.onClick();
  });
}

async function choose(instance: ReactTestInstance): Promise<void> {
  await act(async () => {
    instance.props.onChange();
  });
}

describe('AccountConsentSettingsView fixtures (D-APP-36 render bar)', () => {
  it('renders every fixture with the Opt-in Preview label, the per-root and private-home explanations, and no secret', () => {
    for (const name of CONSENT_UX_FIXTURE_NAMES) {
      const renderer = renderFixture(name);
      const badge = findByProp(renderer, 'data-posture-label');
      expect(textOf(badge)).toBe(PRODUCT_POSTURE_LABEL);
      expect(renderer.root.findByType('section').props['data-product-posture']).toBe('Opt-in Preview');

      const login = findByProp(renderer, 'data-explainer', 'per-root-login');
      expect(textOf(login)).toContain('Sign-in and consent are per working root.');
      expect(textOf(login)).toContain(CONSENT_UX_FIXTURES[name].canonicalRoot);
      expect(textOf(login)).toContain('never carried across roots, accounts, policies, or root generations');

      const home = findByProp(renderer, 'data-explainer', 'private-home');
      expect(textOf(home)).toContain('root-private, app-owned Codex home');
      expect(textOf(home)).toContain('CODEX_HOME');
      expect(textOf(home)).toContain(FIXTURE_CODEX_HOME);
      expect(textOf(home)).toContain('never reads, copies, or links your ambient ~/.codex');
      expect(home.props['data-private-home']).toBe(CONSENT_UX_FIXTURES[name].privateHome.status);

      assertNoSecret(renderer);
      renderer.unmount();
    }
  });

  it('gives every fixture a distinct marker tuple (account, identity, consent, mismatch, posture, role, enforcement, prompt, acceptance, rate limit, approvals)', () => {
    const tuples = new Set<string>();
    for (const name of CONSENT_UX_FIXTURE_NAMES) {
      const renderer = renderFixture(name);
      const account = findByProp(renderer, 'data-account');
      const consent = findByProp(renderer, 'data-consent');
      const network = section(renderer, 'network');
      const role = section(renderer, 'role');
      const extras = [
        findAllByProp(renderer, 'data-consent-mismatch').map((node) => node.props['data-consent-mismatch']).join('+'),
        findAllByProp(renderer, 'data-prompt-id').length,
        findAllByProp(renderer, 'data-session-accepted').length,
        findByProp(renderer, 'data-rate-limit').props['data-rate-limit'],
        findByProp(renderer, 'data-approvals-pending').props['data-approvals-pending']
      ];
      tuples.add(
        [
          account.props['data-account'],
          account.props['data-account-identity'],
          consent.props['data-consent'],
          network.props['data-network-posture'],
          role.props['data-role'],
          role.props['data-role-enforcement'],
          ...extras
        ].join('|')
      );
      renderer.unmount();
    }
    expect(tuples.size).toBe(CONSENT_UX_FIXTURE_NAMES.length);
  });

  it('not connected: explanations only, no account claim, no controls', () => {
    const renderer = renderView({ snapshot: null });
    const status = findByProp(renderer, 'data-account', 'unknown');
    expect(textOf(status)).toBe('Account and consent controls are not connected in this build.');
    expect(status.props['data-consent']).toBe('unknown');
    expect(renderer.root.findAllByType('button')).toHaveLength(0);
    expect(renderer.root.findAllByType('input')).toHaveLength(0);
    expect(textOf(findByProp(renderer, 'data-posture-label'))).toBe(PRODUCT_POSTURE_LABEL);
    expect(json(renderer)).not.toContain('Signed in');
    assertNoSecret(renderer);
  });

  it('loggedOutDefault: sign-in offered, consent and network gated, posture off, private home absent', () => {
    const renderer = renderFixture('loggedOutDefault');
    const account = section(renderer, 'account');
    expect(textOf(findByProp(renderer, 'data-account'))).toBe('Not signed in for this root');
    expect(findByProp(renderer, 'data-account').props['data-account-identity']).toBe('none');
    expect(buttonLabels(account)).toEqual(['Sign in for this root']);

    const consent = section(renderer, 'consent');
    expect(textOf(findByProp(renderer, 'data-consent'))).toBe('Consent not granted for this root');
    const grant = buttonByLabel(consent, 'Grant consent for this root');
    expect(grant.props.disabled).toBe(true);
    expect(textOf(findByProp(renderer, 'data-consent-hint'))).toBe('Sign in for this root before granting consent.');

    const network = section(renderer, 'network');
    expect(network.props.disabled).toBe(true);
    expect(network.props['data-network-posture']).toBe('off');
    expect(radio(renderer, 'consent-network-posture', 'off').props.checked).toBe(true);
    expect(textOf(findByProp(renderer, 'data-network-hint'))).toContain('Grant consent for this root before choosing');
    expect(findByProp(renderer, 'data-explainer', 'private-home').props['data-private-home']).toBe('absent');
    assertNoSecret(renderer);
  });

  it('loggedInNotGranted: shows the digest suffix only, offers sign-out and grant, keeps network gated', () => {
    const renderer = renderFixture('loggedInNotGranted');
    const status = findByProp(renderer, 'data-account', 'loggedIn');
    // Digest suffix only: the full `sha256:acct-a4e19c7b2d63f80e` never reaches the DOM.
    expect(textOf(status)).toBe('Signed in for this root as account …2d63f80e');
    expect(json(renderer)).not.toContain('sha256:acct');
    expect(status.props['data-account-identity']).toBe('digest');
    expect(buttonLabels(section(renderer, 'account'))).toEqual(['Sign out of this root']);
    const grant = buttonByLabel(section(renderer, 'consent'), 'Grant consent for this root');
    expect(grant.props.disabled).toBe(false);
    expect(section(renderer, 'network').props.disabled).toBe(true);
    expect(findByProp(renderer, 'data-explainer', 'private-home').props['data-private-home']).toBe('present');
    assertNoSecret(renderer);
  });

  it('grantedNetworkOff: consent granted with generation, revoke offered, network enabled and off by default', () => {
    const renderer = renderFixture('grantedNetworkOff');
    expect(textOf(findByProp(renderer, 'data-consent', 'granted'))).toBe('Consent granted for this root (root generation 1)');
    expect(buttonLabels(section(renderer, 'consent'))).toEqual(['Revoke consent for this root']);
    const network = section(renderer, 'network');
    expect(network.props.disabled).toBe(false);
    expect(network.props['data-network-posture']).toBe('off');
    expect(radio(renderer, 'consent-network-posture', 'off').props.checked).toBe(true);
    expect(findAllByProp(renderer, 'data-network-hint')).toHaveLength(0);
    expect(findAllByProp(renderer, 'data-network-on-label')).toHaveLength(0);
    expect(findAllByProp(renderer, 'data-prompt-id')).toHaveLength(0);
    const choices = findAllByProp(renderer, 'data-network-choice').map((node) => textOf(node));
    expect(choices).toEqual([
      'No command network (default)',
      'Ask per destination',
      `Command network on (${COMMAND_NETWORK_ON_CONFIG_LABEL})`
    ]);
  });

  it('askPerDestinationPending: prompt shows host, protocol, port, the queued-request caveat, and the three decisions', () => {
    const renderer = renderFixture('askPerDestinationPending');
    expect(section(renderer, 'network').props['data-network-posture']).toBe('askPerDestination');
    expect(radio(renderer, 'consent-network-posture', 'askPerDestination').props.checked).toBe(true);
    const prompt = findByProp(renderer, 'data-prompt-id', 'prompt-0001');
    expect(prompt.props['data-prompt-host']).toBe(FIXTURE_PROMPT_HOST);
    expect(prompt.props['data-prompt-protocol']).toBe('https');
    const copy = textOf(prompt);
    expect(copy).toContain(`npm install wants to reach ${FIXTURE_PROMPT_HOST} over https (port 443).`);
    const caveat = findByProp(renderer, 'data-queued-caveat');
    expect(caveat.props['data-queued-caveat']).toBe(2);
    expect(textOf(caveat)).toBe('2 requests to this destination are already queued; allowing it may let those requests proceed too.');
    expect(buttonLabels(prompt)).toEqual(['Allow once', 'Accept for this session', 'Deny']);
    expect(findByProp(renderer, 'data-prompt-decision', 'acceptForSession').type).toBe('button');
    expect(findAllByProp(renderer, 'data-session-accepted')).toHaveLength(0);
  });

  it('askPerDestinationSessionAccepted: lists the explicitly accepted destination and shows no prompt', () => {
    const renderer = renderFixture('askPerDestinationSessionAccepted');
    expect(findAllByProp(renderer, 'data-prompt-id')).toHaveLength(0);
    const accepted = findByProp(renderer, 'data-session-accepted');
    expect(accepted.props['data-session-accepted']).toBe(`https://${FIXTURE_PROMPT_HOST}:443`);
    expect(textOf(accepted)).toBe(`Accepted for this session: https://${FIXTURE_PROMPT_HOST}:443`);
    expect(findByProp(renderer, 'data-session-accepted-count').props['data-session-accepted-count']).toBe(1);
  });

  it('networkOn: the on posture is checked and visibly labelled with network_access = true', () => {
    const renderer = renderFixture('networkOn');
    expect(section(renderer, 'network').props['data-network-posture']).toBe('on');
    expect(radio(renderer, 'consent-network-posture', 'on').props.checked).toBe(true);
    const label = findByProp(renderer, 'data-network-on-label');
    expect(textOf(label)).toContain(`commands run with ${COMMAND_NETWORK_ON_CONFIG_LABEL}`);
    expect(textOf(label)).toContain('shown wherever a session from this root runs');
    expect(findAllByProp(renderer, 'data-prompt-id')).toHaveLength(0);
  });

  it('accountTransitionStale: names the account change, refuses reuse, and offers a fresh grant', () => {
    const renderer = renderFixture('accountTransitionStale');
    expect(findByProp(renderer, 'data-account').props['data-account-identity']).toBe('digest');
    expect(textOf(findByProp(renderer, 'data-account'))).toContain('…4c19a63b');
    expect(textOf(findByProp(renderer, 'data-consent', 'stale'))).toBe('Previous consent no longer applies to this root');
    const warning = findByProp(renderer, 'data-consent-mismatch');
    expect(warning.props['data-consent-mismatch']).toBe('account');
    expect(textOf(warning)).toContain('the signed-in account changed');
    expect(textOf(warning)).toContain('It is not reused.');
    expect(textOf(warning)).toContain('Grant consent again for this root');
    expect(buttonLabels(section(renderer, 'consent'))).toEqual(['Revoke consent for this root', 'Grant consent for this root']);
    expect(buttonByLabel(section(renderer, 'consent'), 'Grant consent for this root').props.disabled).toBe(false);
    expect(section(renderer, 'network').props.disabled).toBe(true);
  });

  it('policyRotatedStale: names the policy change', () => {
    const renderer = renderFixture('policyRotatedStale');
    const warning = findByProp(renderer, 'data-consent-mismatch');
    expect(warning.props['data-consent-mismatch']).toBe('policy');
    expect(textOf(warning)).toContain('the notice or policy changed');
    expect(section(renderer, 'network').props.disabled).toBe(true);
  });

  it('revoked: names the retired generation and the invalidated private home; grant offered, revoke not', () => {
    const renderer = renderFixture('revoked');
    expect(textOf(findByProp(renderer, 'data-consent', 'revoked'))).toBe('Consent revoked (root generation 1 retired)');
    const warning = findByProp(renderer, 'data-consent-revoked-generation');
    expect(warning.props['data-consent-revoked-generation']).toBe(1);
    expect(textOf(warning)).toContain('Root generation 1 was retired and its private home invalidated');
    expect(textOf(warning)).toContain('Nothing from it is reused.');
    expect(textOf(warning)).toContain('start root generation 2');
    expect(buttonLabels(section(renderer, 'consent'))).toEqual(['Grant consent for this root']);
    const home = findByProp(renderer, 'data-explainer', 'private-home');
    expect(home.props['data-private-home']).toBe('invalidated');
    expect(textOf(home)).toContain('Private home invalidated with the retired root generation');
    expect(section(renderer, 'network').props.disabled).toBe(true);
    expect(section(renderer, 'network').props['data-network-posture']).toBe('off');
  });

  it('nullEmailEpoch: identifies the account by its volatile epoch, never an email', () => {
    const renderer = renderFixture('nullEmailEpoch');
    const status = findByProp(renderer, 'data-account', 'loggedIn');
    expect(status.props['data-account-identity']).toBe('nullEmailEpoch');
    expect(textOf(status)).toBe('Signed in for this root as account without an email (volatile epoch epoch-2026-09-03T10:00:00Z-7f21)');
    assertNoSecret(renderer);
  });

  it('rateLimitedApprovalsPending: shows the rate-limit reset, its detail, the pending count, and the last decision subject only', () => {
    const renderer = renderFixture('rateLimitedApprovalsPending');
    const rate = findByProp(renderer, 'data-rate-limit', 'limited');
    expect(textOf(rate)).toBe('Rate limited until 2026-09-03T10:45:00.000Z — Provider rate limit reached for this account');
    const approvals = findByProp(renderer, 'data-approvals-pending');
    expect(approvals.props['data-approvals-pending']).toBe(2);
    expect(textOf(approvals)).toBe('Approvals: 2 pending requests — last denied (shell) at 2026-09-03T10:30:00.000Z');

    const ok = renderFixture('grantedNetworkOff');
    expect(textOf(findByProp(ok, 'data-rate-limit', 'ok'))).toBe('Rate limit: OK');
    expect(textOf(findByProp(ok, 'data-approvals-pending'))).toBe('Approvals: none pending');
  });

  it('roleAgent2NotMechanicallyEnforced: Agent 2 / TASK carries the label and the instruction-asserted note', () => {
    const renderer = renderFixture('roleAgent2NotMechanicallyEnforced');
    const role = section(renderer, 'role');
    expect(role.props['data-role']).toBe('agent2');
    expect(role.props['data-role-enforcement']).toBe('notMechanicallyEnforced');
    expect(radio(renderer, 'consent-role-posture', 'agent2').props.checked).toBe(true);
    const choices = findAllByProp(renderer, 'data-role-choice');
    expect(choices.map((node) => node.props['data-role-choice'])).toEqual(['untyped', 'agent0', 'agent1', 'agent2']);
    const agent2 = findByProp(renderer, 'data-role-choice', 'agent2');
    expect(agent2.props['data-role-label']).toBe(ROLE_NOT_MECHANICALLY_ENFORCED_LABEL);
    expect(textOf(agent2)).toContain('Agent 2 / TASK (specialist)');
    expect(textOf(agent2)).toContain(ROLE_NOT_MECHANICALLY_ENFORCED_LABEL);
    for (const other of ['untyped', 'agent0', 'agent1']) {
      expect(findByProp(renderer, 'data-role-choice', other).props['data-role-label']).toBeUndefined();
    }
    const hint = findByProp(renderer, 'data-role-hint', 'not-mechanically-enforced');
    expect(textOf(hint)).toContain('G-ROLE cannot mechanically prove non-delegation');
    expect(textOf(hint)).toContain(ROLE_NOT_MECHANICALLY_ENFORCED_LABEL);
    expect(textOf(hint)).toContain('instruction-asserted');
    expect(textOf(findByProp(renderer, 'data-role-hint', 'native-descent'))).toContain('Native descendants acquire no role by descent.');
  });

  it('roleAgent2MechanicallyProven: same role, no label, no note', () => {
    const renderer = renderFixture('roleAgent2MechanicallyProven');
    expect(section(renderer, 'role').props['data-role-enforcement']).toBe('mechanicallyProven');
    expect(findByProp(renderer, 'data-role-choice', 'agent2').props['data-role-label']).toBeUndefined();
    expect(json(renderer)).not.toContain(ROLE_NOT_MECHANICALLY_ENFORCED_LABEL);
    expect(json(renderer)).not.toContain('instruction-asserted');
  });

  it('the label follows the enforcement state even when Agent 2 is not selected', () => {
    const renderer = renderFixture('grantedNetworkOff');
    expect(section(renderer, 'role').props['data-role']).toBe('untyped');
    expect(findByProp(renderer, 'data-role-choice', 'agent2').props['data-role-label']).toBe(ROLE_NOT_MECHANICALLY_ENFORCED_LABEL);
  });

  it('busy disables every control; an error renders on its own line', () => {
    const renderer = renderView({ snapshot: consentUxFixture('askPerDestinationPending'), busy: true, error: 'Consent service unavailable' });
    for (const button of renderer.root.findAllByType('button')) {
      if (button.props['data-prompt-decision'] === undefined) {
        expect(button.props.disabled).toBe(true);
      }
    }
    expect(section(renderer, 'network').props.disabled).toBe(true);
    expect(section(renderer, 'role').props.disabled).toBe(true);
    expect(textOf(findByProp(renderer, 'data-consent-error'))).toBe('Consent service unavailable');
  });
});

describe('AccountConsentSettings with the fake port (explicit user acts only)', () => {
  it('walks sign-in → grant → ask-per-destination → accept for session → revoke, re-rendering from the port', async () => {
    const port = createFakeHostedEngineConsentPort();
    const renderer = renderWithPort(port);
    expect(port.control.actLog).toEqual([]);

    await click(buttonByLabel(section(renderer, 'account'), 'Sign in for this root'));
    expect(port.getSnapshot().account.status).toBe('loggedIn');
    expect(findByProp(renderer, 'data-account').props['data-account']).toBe('loggedIn');

    await click(buttonByLabel(section(renderer, 'consent'), 'Grant consent for this root'));
    expect(findByProp(renderer, 'data-consent').props['data-consent']).toBe('granted');
    expect(section(renderer, 'network').props.disabled).toBe(false);

    await choose(radio(renderer, 'consent-network-posture', 'askPerDestination'));
    expect(port.getSnapshot().network.posture).toBe('askPerDestination');
    expect(port.getSnapshot().network.sessionAcceptedDestinations).toEqual([]);

    act(() => {
      port.control.enqueueNetworkPrompt({
        promptId: 'p-1',
        host: FIXTURE_PROMPT_HOST,
        protocol: 'https',
        port: 443,
        queuedRequestCount: 1
      });
    });
    const prompt = findByProp(renderer, 'data-prompt-id', 'p-1');
    expect(textOf(findByProp(renderer, 'data-queued-caveat'))).toBe('1 request to this destination is already queued; allowing it may let that request proceed too.');
    // Nothing accepted by the prompt's existence.
    expect(port.getSnapshot().network.sessionAcceptedDestinations).toEqual([]);

    await click(buttonByLabel(prompt, 'Accept for this session'));
    expect(port.getSnapshot().network.sessionAcceptedDestinations).toEqual([`https://${FIXTURE_PROMPT_HOST}:443`]);
    expect(findAllByProp(renderer, 'data-prompt-id')).toHaveLength(0);
    expect(findByProp(renderer, 'data-session-accepted').props['data-session-accepted']).toBe(`https://${FIXTURE_PROMPT_HOST}:443`);

    await click(buttonByLabel(section(renderer, 'consent'), 'Revoke consent for this root'));
    expect(findByProp(renderer, 'data-consent').props['data-consent']).toBe('revoked');
    expect(section(renderer, 'network').props['data-network-posture']).toBe('off');
    expect(section(renderer, 'network').props.disabled).toBe(true);
    expect(findByProp(renderer, 'data-explainer', 'private-home').props['data-private-home']).toBe('invalidated');

    expect(port.control.actLog).toEqual([
      'login',
      'grantConsent',
      'selectNetworkPosture:askPerDestination',
      'resolveNetworkPrompt:acceptForSession',
      'revokeConsent'
    ]);
    assertNoSecret(renderer);
  });

  it('never calls the port on mount or on a port-driven update', () => {
    const port = createFakeHostedEngineConsentPort({ initial: consentUxFixture('askPerDestinationPending') });
    const renderer = renderWithPort(port);
    act(() => {
      port.control.setRateLimit({ status: 'limited', resetsAt: '2026-09-03T13:00:00.000Z' });
    });
    expect(findByProp(renderer, 'data-rate-limit').props['data-rate-limit']).toBe('limited');
    expect(port.control.actLog).toEqual([]);
    expect(port.getSnapshot().network.sessionAcceptedDestinations).toEqual([]);
  });

  it('selecting the on posture labels it, and choosing a role after the grant shows the consent as stale', async () => {
    const port = createFakeHostedEngineConsentPort({ initial: consentUxFixture('grantedNetworkOff') });
    const renderer = renderWithPort(port);

    await choose(radio(renderer, 'consent-network-posture', 'on'));
    expect(section(renderer, 'network').props['data-network-posture']).toBe('on');
    expect(textOf(findByProp(renderer, 'data-network-on-label'))).toContain(COMMAND_NETWORK_ON_CONFIG_LABEL);

    await choose(radio(renderer, 'consent-role-posture', 'agent2'));
    expect(section(renderer, 'role').props['data-role']).toBe('agent2');
    expect(findByProp(renderer, 'data-consent').props['data-consent']).toBe('stale');
    expect(findByProp(renderer, 'data-consent-mismatch').props['data-consent-mismatch']).toBe('role');
    expect(section(renderer, 'network').props.disabled).toBe(true);
  });

  it('shows a failed act on the error line and leaves the state unchanged', async () => {
    const port = createFakeHostedEngineConsentPort();
    const renderer = renderWithPort(port);
    port.control.failNextAct('Consent service unavailable');
    await click(buttonByLabel(section(renderer, 'account'), 'Sign in for this root'));
    expect(textOf(findByProp(renderer, 'data-consent-error'))).toBe('Consent service unavailable');
    expect(findByProp(renderer, 'data-account').props['data-account']).toBe('loggedOut');
    await click(buttonByLabel(section(renderer, 'account'), 'Sign in for this root'));
    expect(findAllByProp(renderer, 'data-consent-error')).toHaveLength(0);
    expect(findByProp(renderer, 'data-account').props['data-account']).toBe('loggedIn');
  });

  it('renders the not-connected state without a port and stops listening when the port goes away', () => {
    const port = createFakeHostedEngineConsentPort({ initial: consentUxFixture('grantedNetworkOff') });
    let renderer!: ReactTestRenderer;
    act(() => {
      renderer = create(createElement(AccountConsentSettings, { port }));
    });
    expect(findByProp(renderer, 'data-consent').props['data-consent']).toBe('granted');
    act(() => {
      renderer.update(createElement(AccountConsentSettings, { port: null }));
    });
    expect(findByProp(renderer, 'data-account', 'unknown')).toBeDefined();
    act(() => {
      port.control.setRateLimit({ status: 'unknown' });
    });
    expect(findAllByProp(renderer, 'data-rate-limit')).toHaveLength(0);
  });
});

describe('fixture snapshot type coverage', () => {
  it('every fixture is a complete snapshot the view accepts without a runtime guard', () => {
    for (const name of CONSENT_UX_FIXTURE_NAMES) {
      const fixture: HostedEngineConsentSnapshot = CONSENT_UX_FIXTURES[name];
      expect(Object.keys(fixture).sort()).toEqual(
        [
          'account',
          'adapter',
          'approvals',
          'canonicalRoot',
          'configDigest',
          'consent',
          'network',
          'policyDigest',
          'privateHome',
          'productPosture',
          'rateLimit',
          'role',
          'workerGeneration',
          'projectId'
        ].sort()
      );
    }
  });
});
