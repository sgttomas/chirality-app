'use client';

import React, { useCallback, useEffect, useState } from 'react';
import {
  COMMAND_NETWORK_ON_CONFIG_LABEL,
  COMMAND_NETWORK_POSTURES,
  COMMAND_NETWORK_POSTURE_LABELS,
  CONSENT_MISMATCH_LABELS,
  INSTRUCTION_ASSERTED_EVIDENCE_LABEL,
  NETWORK_PROMPT_DECISIONS,
  NETWORK_PROMPT_DECISION_LABELS,
  PRODUCT_POSTURE_LABEL,
  ROLE_NOT_MECHANICALLY_ENFORCED_LABEL,
  ROLE_POSTURES,
  ROLE_POSTURE_LABELS,
  describeAccountIdentity,
  type CommandNetworkPosture,
  type ConsentActResult,
  type HostedEngineConsentPort,
  type HostedEngineConsentSnapshot,
  type NetworkPromptDecision,
  type RolePosture
} from '../../lib/consent/hosted-engine-consent-port';

/**
 * Hosted-engine account and consent panel (DEL-02-05-V3-02; App CONTRACT
 * K-CONSENT-1, K-NET-1, K-KEY-1, K-ROLE-2; product posture `Opt-in Preview`,
 * G0 A8).
 *
 * The panel renders whatever `HostedEngineConsentPort` it is given. With no
 * port it renders the standing explanation (per-root login, root-private
 * app-owned `CODEX_HOME`) and says the controls are not connected — it makes
 * no account claim of its own. Every state change is an explicit user act on
 * a control; the panel never calls a port method on its own initiative, and
 * `acceptForSession` exists only as a button the operator presses.
 *
 * Nothing in the rendered tree carries key material, tokens, cookies, device
 * codes, or emails: identities are shown as digest suffixes or epochs.
 */

export type AccountConsentSettingsProps = {
  /** The consent port for the active root; `null`/absent renders the not-connected state. */
  port?: HostedEngineConsentPort | null;
};

export function useAccountConsentController(port: HostedEngineConsentPort | null = null): AccountConsentSettingsViewProps {
  const [observed, setObserved] = useState(() => ({ port, snapshot: port ? port.getSnapshot() : null }));
  const snapshot = observed.port === port ? observed.snapshot : port ? port.getSnapshot() : null;
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!port) {
      setObserved({ port, snapshot: null });
      return undefined;
    }
    setObserved({ port, snapshot: port.getSnapshot() });
    return port.subscribe(snapshot => setObserved({ port, snapshot }));
  }, [port]);

  const perform = useCallback(
    async (run: (activePort: HostedEngineConsentPort) => Promise<ConsentActResult>): Promise<void> => {
      if (!port) {
        return;
      }
      setBusy(true);
      setError(null);
      try {
        const result = await run(port);
        if (!result.ok) {
          setError(result.error);
        }
      } catch {
        setError('The request could not be completed. Nothing was changed.');
      } finally {
        setBusy(false);
      }
    },
    [port]
  );

  return { snapshot, busy, error,
    onLogin: () => void perform(p => p.login()), onLogout: () => void perform(p => p.logout()),
    onGrantConsent: () => void perform(p => p.grantConsent()), onRevokeConsent: () => void perform(p => p.revokeConsent()),
    onSelectNetworkPosture: posture => void perform(p => p.selectNetworkPosture(posture)),
    onResolveNetworkPrompt: (id, decision) => void perform(p => p.resolveNetworkPrompt(id, decision)),
    onSelectRole: role => void perform(p => p.selectRole(role)) };
}

export function AccountConsentSettings({ port = null }: AccountConsentSettingsProps): JSX.Element {
  const controller = useAccountConsentController(port);
  return <AccountConsentSettingsView {...controller} />;
}

export type AccountConsentSettingsViewProps = {
  presentation?: 'combined' | 'account' | 'folder';
  snapshot: HostedEngineConsentSnapshot | null;
  busy: boolean;
  error: string | null;
  onLogin: () => void;
  onLogout: () => void;
  onGrantConsent: () => void;
  onRevokeConsent: () => void;
  onSelectNetworkPosture: (posture: CommandNetworkPosture) => void;
  onResolveNetworkPrompt: (promptId: string, decision: NetworkPromptDecision) => void;
  onSelectRole: (role: RolePosture) => void;
};

function accountLabel(snapshot: HostedEngineConsentSnapshot): string {
  if (snapshot.account.status === 'loggedOut') {
    return 'Not signed in for this root';
  }
  return `Signed in for this root as ${describeAccountIdentity(snapshot.account.identity)}`;
}

function accountIdentityMarker(snapshot: HostedEngineConsentSnapshot): string {
  return snapshot.account.status === 'loggedIn' ? snapshot.account.identity.kind : 'none';
}

function consentLabel(snapshot: HostedEngineConsentSnapshot): string {
  switch (snapshot.consent.status) {
    case 'notGranted':
      return 'Consent not granted for this root';
    case 'granted':
      return `Consent granted for this root (root generation ${snapshot.consent.scope.workerGeneration})`;
    case 'stale':
      return 'Previous consent no longer applies to this root';
    case 'revoked':
      return `Consent revoked (root generation ${snapshot.consent.retiredGeneration} retired)`;
    default:
      return 'Consent state unknown';
  }
}

function privateHomeLabel(status: HostedEngineConsentSnapshot['privateHome']['status']): string {
  switch (status) {
    case 'present':
      return 'Private home in use for this root.';
    case 'invalidated':
      return 'Private home invalidated with the retired root generation; a fresh consent creates a new one.';
    default:
      return 'Private home not created yet; it is created when you sign in for this root.';
  }
}

function rateLimitLabel(snapshot: HostedEngineConsentSnapshot): string {
  switch (snapshot.rateLimit.status) {
    case 'ok':
      return 'Rate limit: OK';
    case 'limited':
      return `Rate limited until ${snapshot.rateLimit.resetsAt}${
        snapshot.rateLimit.detail ? ` — ${snapshot.rateLimit.detail}` : ''
      }`;
    default:
      return 'Rate limit: unknown';
  }
}

function approvalsLabel(snapshot: HostedEngineConsentSnapshot): string {
  const pending = snapshot.approvals.pendingCount;
  const head =
    pending === 0
      ? 'Approvals: none pending'
      : `Approvals: ${pending} pending${pending === 1 ? ' request' : ' requests'}`;
  const last = snapshot.approvals.lastDecision;
  return last ? `${head} — last ${last.outcome} (${last.subject}) at ${last.at}` : head;
}

export function AccountConsentSettingsView({
  presentation = 'combined',
  snapshot,
  busy,
  error,
  onLogin,
  onLogout,
  onGrantConsent,
  onRevokeConsent,
  onSelectNetworkPosture,
  onResolveNetworkPrompt,
  onSelectRole
}: AccountConsentSettingsViewProps): JSX.Element {
  const loggedIn = snapshot?.account.status === 'loggedIn';
  const consentStatus = snapshot?.consent.status ?? 'unknown';
  const consentGranted = consentStatus === 'granted';
  const roleLabelApplies = snapshot !== null && snapshot.role.enforcement !== 'mechanicallyProven';
  const prompt =
    snapshot && snapshot.network.posture === 'askPerDestination'
      ? snapshot.network.pendingPrompt
      : null;

  return (
    <section className="consent-settings" data-product-posture={PRODUCT_POSTURE_LABEL}>
      <header className="consent-settings-header">
        <h3 className="api-key-settings-title">{presentation === 'account' ? 'OpenAI account' : presentation === 'folder' ? 'Consent and permissions' : 'Hosted engine account & consent'}</h3>
        <span className="consent-badge" data-posture-label="true">
          {PRODUCT_POSTURE_LABEL}
        </span>
      </header>

      {presentation === 'account' ? <p className="api-key-hint">One account for the app. Consent and permissions are per folder.</p> : <>
      {presentation === 'folder' ? <p className="api-key-hint">Consent is bound to this folder; it is never carried across roots, accounts, policies, or root generations.</p> : <p className="api-key-hint consent-explainer" data-explainer="per-root-login">
        Sign-in and consent are per working root. Signing in here applies only to the active
        root
        {snapshot ? (
          <>
            {' '}
            (<code>{snapshot.canonicalRoot}</code>)
          </>
        ) : null}
        ; every other root asks separately, and consent is never carried across roots,
        accounts, policies, or root generations.
      </p>}

      <p
        className="api-key-hint consent-explainer"
        data-explainer="private-home"
        data-private-home={snapshot?.privateHome.status ?? 'unknown'}
      >
        Chirality keeps a root-private, app-owned Codex home for this root
        {snapshot ? (
          <>
            {' '}
            (<code>CODEX_HOME</code> = <code>{snapshot.privateHome.codexHome}</code>)
          </>
        ) : (
          <>
            {' '}
            (<code>CODEX_HOME</code>)
          </>
        )}
        . It never reads, copies, or links your ambient <code>~/.codex</code> directory.
        {snapshot ? ` ${privateHomeLabel(snapshot.privateHome.status)}` : ''}
      </p>

      </>}

      {!snapshot ? (
        <p className="api-key-status" data-account="unknown" data-consent="unknown">
          {presentation === 'account' ? 'Account service unavailable in this build.' : presentation === 'folder' ? 'Folder consent controls are not connected in this build.' : 'Account and consent controls are not connected in this build.'}
        </p>
      ) : (
        <>
          {presentation !== 'folder' ? <div className="consent-section" data-section="account">
            <p
              className="api-key-status consent-status"
              data-account={snapshot.account.status}
              data-account-identity={accountIdentityMarker(snapshot)}
            >
              {presentation === 'account' ? (snapshot.account.status === 'loggedIn' ? `Signed in as ${describeAccountIdentity(snapshot.account.identity)}` : 'Not signed in') : accountLabel(snapshot)}
            </p>
            <div className="consent-actions">
              {loggedIn ? (
                <button type="button" className="button-muted" onClick={onLogout} disabled={busy}>
                  {presentation === 'account' ? 'Sign out' : 'Sign out of this root'}
                </button>
              ) : (
                <button type="button" onClick={onLogin} disabled={busy}>
                  {presentation === 'account' ? 'Sign in' : 'Sign in for this root'}
                </button>
              )}
            </div>
          </div> : null}

          {presentation !== 'account' ? <>
          <div className="consent-section" data-section="consent">
            <p className="api-key-status consent-status" data-consent={consentStatus}>
              {consentLabel(snapshot)}
            </p>

            {snapshot.consent.status === 'stale' ? (
              <p
                className="api-key-warning"
                data-consent-mismatch={snapshot.consent.mismatches.join(',')}
              >
                The consent you gave earlier was bound to a different scope:{' '}
                {snapshot.consent.mismatches
                  .map((mismatch) => CONSENT_MISMATCH_LABELS[mismatch])
                  .join('; ')}
                . It is not reused. Grant consent again for this root to continue.
              </p>
            ) : null}

            {snapshot.consent.status === 'revoked' ? (
              <p className="api-key-warning" data-consent-revoked-generation={snapshot.consent.retiredGeneration}>
                Root generation {snapshot.consent.retiredGeneration} was retired and its private
                home invalidated at {snapshot.consent.revokedAt}. Nothing from it is reused. Grant
                consent again to start root generation {snapshot.workerGeneration}.
              </p>
            ) : null}

            <div className="consent-actions">
              {consentGranted || snapshot.consent.status === 'stale' ? (
                <button type="button" className="button-muted" onClick={onRevokeConsent} disabled={busy}>
                  Revoke consent for this root
                </button>
              ) : null}
              {!consentGranted ? (
                <button type="button" onClick={onGrantConsent} disabled={busy || !loggedIn}>
                  Grant consent for this root
                </button>
              ) : null}
            </div>
            {!loggedIn && !consentGranted ? (
              <p className="api-key-hint" data-consent-hint="sign-in-first">
                Sign in for this root before granting consent.
              </p>
            ) : null}
          </div>

          <fieldset
            className="consent-section consent-network"
            data-section="network"
            data-network-posture={snapshot.network.posture}
            disabled={busy || !consentGranted}
          >
            <legend>Command network for this root</legend>
            {COMMAND_NETWORK_POSTURES.map((posture) => (
              <label key={posture} className="consent-choice" data-network-choice={posture}>
                <input
                  type="radio"
                  name="consent-network-posture"
                  value={posture}
                  checked={snapshot.network.posture === posture}
                  onChange={() => onSelectNetworkPosture(posture)}
                />
                {posture === 'on' ? (
                  <span>
                    Command network on (<code>{COMMAND_NETWORK_ON_CONFIG_LABEL}</code>)
                  </span>
                ) : (
                  <span>{COMMAND_NETWORK_POSTURE_LABELS[posture]}</span>
                )}
              </label>
            ))}

            {!consentGranted ? (
              <p className="api-key-hint" data-network-hint="consent-first">
                Grant consent for this root before choosing a command-network posture. Until then
                commands have no network.
              </p>
            ) : null}

            {snapshot.network.posture === 'on' ? (
              <p className="api-key-warning" data-network-on-label="true">
                Command network is on for this root: commands run with{' '}
                <code>{COMMAND_NETWORK_ON_CONFIG_LABEL}</code>. This label is shown wherever a
                session from this root runs.
              </p>
            ) : null}

            {prompt ? (
              <div
                className="consent-network-prompt"
                data-prompt-id={prompt.promptId}
                data-prompt-host={prompt.host}
                data-prompt-protocol={prompt.protocol}
              >
                <p className="api-key-status">
                  {prompt.requestedBy ? `${prompt.requestedBy} wants` : 'A command wants'} to reach{' '}
                  <strong>{prompt.host}</strong> over <strong>{prompt.protocol}</strong>
                  {prompt.port !== undefined ? ` (port ${prompt.port})` : ''}.
                </p>
                <p className="api-key-warning" data-queued-caveat={prompt.queuedRequestCount}>
                  {prompt.queuedRequestCount === 1
                    ? '1 request to this destination is already queued; allowing it may let that request proceed too.'
                    : `${prompt.queuedRequestCount} requests to this destination are already queued; allowing it may let those requests proceed too.`}
                </p>
                <div className="consent-actions">
                  {NETWORK_PROMPT_DECISIONS.map((decision) => (
                    <button
                      key={decision}
                      type="button"
                      className={decision === 'deny' ? 'button-muted' : ''}
                      data-prompt-decision={decision}
                      onClick={() => onResolveNetworkPrompt(prompt.promptId, decision)}
                    >
                      {NETWORK_PROMPT_DECISION_LABELS[decision]}
                    </button>
                  ))}
                </div>
              </div>
            ) : null}

            {snapshot.network.sessionAcceptedDestinations.length > 0 ? (
              <ul className="consent-session-accepted" data-session-accepted-count={snapshot.network.sessionAcceptedDestinations.length}>
                {snapshot.network.sessionAcceptedDestinations.map((destination) => (
                  <li key={destination} data-session-accepted={destination}>
                    Accepted for this session: <code>{destination}</code>
                  </li>
                ))}
              </ul>
            ) : null}
          </fieldset>

          <div className="consent-section" data-section="status">
            <p className="api-key-hint" data-rate-limit={snapshot.rateLimit.status}>
              {rateLimitLabel(snapshot)}
            </p>
            <p className="api-key-hint" data-approvals-pending={snapshot.approvals.pendingCount}>
              {approvalsLabel(snapshot)}
            </p>
          </div>

          <fieldset
            className="consent-section consent-role"
            data-section="role"
            data-role={snapshot.role.selected}
            data-role-enforcement={snapshot.role.enforcement}
            disabled={busy}
          >
            <legend>Role for sessions from this root</legend>
            {ROLE_POSTURES.map((role) => {
              const labelled = role === 'agent2' && roleLabelApplies;
              return (
                <label
                  key={role}
                  className="consent-choice"
                  data-role-choice={role}
                  data-role-label={labelled ? ROLE_NOT_MECHANICALLY_ENFORCED_LABEL : undefined}
                >
                  <input
                    type="radio"
                    name="consent-role-posture"
                    value={role}
                    checked={snapshot.role.selected === role}
                    onChange={() => onSelectRole(role)}
                  />
                  <span>{ROLE_POSTURE_LABELS[role]}</span>
                  {labelled ? (
                    <span className="consent-badge consent-badge--warn">
                      {ROLE_NOT_MECHANICALLY_ENFORCED_LABEL}
                    </span>
                  ) : null}
                </label>
              );
            })}
            {roleLabelApplies ? (
              <p className="api-key-hint" data-role-hint="not-mechanically-enforced">
                G-ROLE cannot mechanically prove non-delegation here, so Agent 2 / TASK entry is
                offered with the label <em>{ROLE_NOT_MECHANICALLY_ENFORCED_LABEL}</em> and its
                governed-workflow evidence is marked <code>{INSTRUCTION_ASSERTED_EVIDENCE_LABEL}</code>.
              </p>
            ) : null}
            <p className="api-key-hint" data-role-hint="native-descent">
              Roles describe authority, not an engine or model. Native descendants acquire no role
              by descent.
            </p>
          </fieldset>
          </> : null}
        </>
      )}

      {error ? (
        <p className="api-key-error" data-consent-error="true">
          {error}
        </p>
      ) : null}
    </section>
  );
}
