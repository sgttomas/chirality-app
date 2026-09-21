import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, it } from 'vitest';
import {
  AccountConsentSettings,
  AccountConsentSettingsView,
  type AccountConsentSettingsViewProps
} from '../../components/settings/account-consent-settings';
import { CONSENT_UX_FIXTURE_NAMES, FIXTURE_CODEX_HOME, consentUxFixture } from '../../lib/consent/consent-ux-fixtures';
import {
  COMMAND_NETWORK_ON_CONFIG_LABEL,
  INSTRUCTION_ASSERTED_EVIDENCE_LABEL,
  PRODUCT_POSTURE_LABEL,
  ROLE_NOT_MECHANICALLY_ENFORCED_LABEL
} from '../../lib/consent/hosted-engine-consent-port';

/**
 * Static-markup copy checks for the hosted-engine account/consent panel
 * (DEL-02-05-V3-02). The react-test-renderer state/interaction evidence lives
 * in `account-consent-settings-states.test.ts`; this file pins the verbatim
 * labels the contract and the G0 rulings name, and proves the server render
 * (no effects, no port) makes no account claim.
 */

const noop = (): void => undefined;

const baseProps: AccountConsentSettingsViewProps = {
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

function renderView(overrides: Partial<AccountConsentSettingsViewProps> = {}): string {
  return renderToStaticMarkup(createElement(AccountConsentSettingsView, { ...baseProps, ...overrides }));
}

describe('AccountConsentSettings static markup', () => {
  it('server-renders the not-connected state without a port and without an account claim', () => {
    const html = renderToStaticMarkup(createElement(AccountConsentSettings));

    expect(html).toContain('Hosted engine account &amp; consent');
    expect(html).toContain(`data-product-posture="${PRODUCT_POSTURE_LABEL}"`);
    expect(html).toContain(`>${PRODUCT_POSTURE_LABEL}<`);
    expect(html).toContain('Sign-in and consent are per working root.');
    expect(html).toContain('root-private, app-owned Codex home');
    expect(html).toContain('<code>CODEX_HOME</code>');
    expect(html).toContain('never reads, copies, or links your ambient <code>~/.codex</code> directory.');
    expect(html).toContain('Account and consent controls are not connected in this build.');
    expect(html).toContain('data-account="unknown"');
    expect(html).not.toContain('Signed in');
    expect(html).not.toContain('<button');
    expect(html).not.toContain('<input');
  });

  it('pins the verbatim G0 A8 posture label on every fixture', () => {
    for (const name of CONSENT_UX_FIXTURE_NAMES) {
      const html = renderView({ snapshot: consentUxFixture(name) });
      expect(html).toContain(`<span class="consent-badge" data-posture-label="true">${PRODUCT_POSTURE_LABEL}</span>`);
      expect(html).toContain(FIXTURE_CODEX_HOME);
    }
  });

  it('pins the K-NET-1 posture labels and the network_access = true label', () => {
    const html = renderView({ snapshot: consentUxFixture('networkOn') });
    expect(html).toContain('No command network (default)');
    expect(html).toContain('Ask per destination');
    expect(html).toContain(`Command network on (<code>${COMMAND_NETWORK_ON_CONFIG_LABEL}</code>)`);
    expect(html).toContain('data-network-on-label="true"');
    expect(html).toContain(`commands run with <code>${COMMAND_NETWORK_ON_CONFIG_LABEL}</code>`);
    expect(html).toContain('value="off"');
    expect(html).toContain('value="askPerDestination"');
    expect(html).toContain('name="consent-network-posture" checked="" value="on"');
  });

  it('pins the ask-per-destination prompt copy: host, protocol, queued-request caveat, explicit acceptForSession', () => {
    const html = renderView({ snapshot: consentUxFixture('askPerDestinationPending') });
    expect(html).toContain('data-prompt-host="api.example.test"');
    expect(html).toContain('data-prompt-protocol="https"');
    expect(html).toContain('over <strong>https</strong> (port 443).');
    expect(html).toContain('already queued; allowing it may let those requests proceed too.');
    expect(html).toContain('data-prompt-decision="allowOnce"');
    expect(html).toContain('data-prompt-decision="acceptForSession"');
    expect(html).toContain('data-prompt-decision="deny"');
    expect(html).toContain('>Accept for this session</button>');
  });

  it('pins the verbatim K-ROLE-2 labels', () => {
    const html = renderView({ snapshot: consentUxFixture('roleAgent2NotMechanicallyEnforced') });
    expect(html).toContain(`data-role-label="${ROLE_NOT_MECHANICALLY_ENFORCED_LABEL}"`);
    expect(html).toContain(`<span class="consent-badge consent-badge--warn">${ROLE_NOT_MECHANICALLY_ENFORCED_LABEL}</span>`);
    expect(html).toContain(`<code>${INSTRUCTION_ASSERTED_EVIDENCE_LABEL}</code>`);
    expect(html).toContain('Untyped session');
    expect(html).toContain('Agent 0 (supervising architect)');
    expect(html).toContain('Agent 1 (manager)');
    expect(html).toContain('Agent 2 / TASK (specialist)');
    expect(ROLE_NOT_MECHANICALLY_ENFORCED_LABEL).toBe('role not mechanically enforced');
    expect(INSTRUCTION_ASSERTED_EVIDENCE_LABEL).toBe('instruction-asserted');
    expect(PRODUCT_POSTURE_LABEL).toBe('Opt-in Preview');
    expect(COMMAND_NETWORK_ON_CONFIG_LABEL).toBe('network_access = true');
  });

  it('never renders an email, token, or full account digest', () => {
    for (const name of CONSENT_UX_FIXTURE_NAMES) {
      const html = renderView({ snapshot: consentUxFixture(name) });
      expect(html).not.toContain('@');
      expect(html).not.toContain('token');
      expect(html).not.toContain('sha256:acct');
    }
  });
});
