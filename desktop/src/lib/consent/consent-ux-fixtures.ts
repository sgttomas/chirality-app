/**
 * Static WP-07 account/consent UX fixtures (DEL-02-05-V3-02).
 *
 * Each fixture is one complete non-secret `HostedEngineConsentSnapshot` the
 * settings panel must render distinctly. They are static bytes: no fixture is
 * produced by a live account, a live login, a network request, or a read of
 * the ambient `~/.codex`. Hosts use the reserved `.test` TLD (RFC 2606) so no
 * fixture names a real network destination. Identities are digests and epochs
 * only — never emails, tokens, cookies, or device codes.
 *
 * The fake adapter (`fake-hosted-engine-consent-port.ts`) can be seeded from
 * any fixture; the D-APP-36 render tests iterate over all of them.
 */

import {
  DEFAULT_COMMAND_NETWORK_POSTURE,
  PRODUCT_POSTURE_LABEL,
  type AccountIdentity,
  type ConsentScope,
  type HostedEngineConsentSnapshot
} from './hosted-engine-consent-port';

/** Server-owned canonical root of the fixture project (display only). */
export const FIXTURE_CANONICAL_ROOT = '/Users/operator/Projects/fixture-root';
export const FIXTURE_PROJECT_ID = 'prj_fixture_0001';
export const FIXTURE_ADAPTER = 'delegated-harness';
export const FIXTURE_POLICY_DIGEST = 'sha256:policy-0f3a9c4d7e1b2a6f';
export const FIXTURE_ROTATED_POLICY_DIGEST = 'sha256:policy-9b2e6d1c4a7f0e83';
export const FIXTURE_CONFIG_DIGEST = 'sha256:config-5c1d8e2f9a3b7c04';

/** App-owned, root-private Codex home under the app's own user-data (never `~/.codex`). */
export const FIXTURE_CODEX_HOME =
  '/Users/operator/Library/Application Support/Chirality/codex-homes/prj_fixture_0001';

export const FIXTURE_ACCOUNT_A: AccountIdentity = {
  kind: 'digest',
  accountDigest: 'sha256:acct-a4e19c7b2d63f80e'
};

export const FIXTURE_ACCOUNT_B: AccountIdentity = {
  kind: 'digest',
  accountDigest: 'sha256:acct-b7d02e5f4c19a63b'
};

export const FIXTURE_NULL_EMAIL_ACCOUNT: AccountIdentity = {
  kind: 'nullEmailEpoch',
  epoch: 'epoch-2026-09-03T10:00:00Z-7f21'
};

/** A destination under the reserved `.test` TLD; never routable. */
export const FIXTURE_PROMPT_HOST = 'api.example.test';

export const FIXTURE_GRANTED_AT = '2026-09-03T10:05:00.000Z';

const BASE: HostedEngineConsentSnapshot = {
  productPosture: PRODUCT_POSTURE_LABEL,
  canonicalRoot: FIXTURE_CANONICAL_ROOT,
  projectId: FIXTURE_PROJECT_ID,
  adapter: FIXTURE_ADAPTER,
  policyDigest: FIXTURE_POLICY_DIGEST,
  configDigest: FIXTURE_CONFIG_DIGEST,
  workerGeneration: 1,
  account: { status: 'loggedOut' },
  privateHome: { codexHome: FIXTURE_CODEX_HOME, status: 'absent', ambientCodexRead: false },
  consent: { status: 'notGranted' },
  network: {
    posture: DEFAULT_COMMAND_NETWORK_POSTURE,
    pendingPrompt: null,
    sessionAcceptedDestinations: []
  },
  rateLimit: { status: 'ok' },
  approvals: { pendingCount: 0 },
  role: { selected: 'untyped', enforcement: 'notMechanicallyEnforced' }
};

function grantedScope(account: AccountIdentity, overrides: Partial<ConsentScope> = {}): ConsentScope {
  return {
    canonicalRoot: FIXTURE_CANONICAL_ROOT,
    projectId: FIXTURE_PROJECT_ID,
    adapter: FIXTURE_ADAPTER,
    account,
    policyDigest: FIXTURE_POLICY_DIGEST,
    rolePosture: 'untyped',
    configDigest: FIXTURE_CONFIG_DIGEST,
    workerGeneration: 1,
    ...overrides
  };
}

function snapshot(overrides: Partial<HostedEngineConsentSnapshot>): HostedEngineConsentSnapshot {
  return { ...BASE, ...overrides };
}

const loggedInA = snapshot({
  account: { status: 'loggedIn', identity: FIXTURE_ACCOUNT_A },
  privateHome: { codexHome: FIXTURE_CODEX_HOME, status: 'present', ambientCodexRead: false }
});

const grantedA = snapshot({
  ...loggedInA,
  consent: { status: 'granted', scope: grantedScope(FIXTURE_ACCOUNT_A), grantedAt: FIXTURE_GRANTED_AT }
});

export const CONSENT_UX_FIXTURES = {
  /** Fresh root: signed out, nothing granted, no command network, no private home yet. */
  loggedOutDefault: snapshot({}),

  /** Signed in for this root as account A; consent not yet granted. */
  loggedInNotGranted: loggedInA,

  /** Account A, consent granted, command network off (the default posture). */
  grantedNetworkOff: grantedA,

  /** Account A, consent granted, ask-per-destination with a prompt awaiting the operator. */
  askPerDestinationPending: snapshot({
    ...grantedA,
    network: {
      posture: 'askPerDestination',
      pendingPrompt: {
        promptId: 'prompt-0001',
        host: FIXTURE_PROMPT_HOST,
        protocol: 'https',
        port: 443,
        queuedRequestCount: 2,
        requestedBy: 'npm install'
      },
      sessionAcceptedDestinations: []
    }
  }),

  /** Account A, ask-per-destination, one destination already accepted for this session by an explicit act. */
  askPerDestinationSessionAccepted: snapshot({
    ...grantedA,
    network: {
      posture: 'askPerDestination',
      pendingPrompt: null,
      sessionAcceptedDestinations: [`https://${FIXTURE_PROMPT_HOST}:443`]
    }
  }),

  /** Account A, consent granted, command network on through `network_access = true`. */
  networkOn: snapshot({
    ...grantedA,
    network: { posture: 'on', pendingPrompt: null, sessionAcceptedDestinations: [] }
  }),

  /** Account transition A → B: the grant bound to A cannot be reused. */
  accountTransitionStale: snapshot({
    ...grantedA,
    account: { status: 'loggedIn', identity: FIXTURE_ACCOUNT_B },
    consent: {
      status: 'stale',
      grantedScope: grantedScope(FIXTURE_ACCOUNT_A),
      mismatches: ['account']
    }
  }),

  /** The notice/policy digest rotated after the grant. */
  policyRotatedStale: snapshot({
    ...grantedA,
    policyDigest: FIXTURE_ROTATED_POLICY_DIGEST,
    consent: {
      status: 'stale',
      grantedScope: grantedScope(FIXTURE_ACCOUNT_A),
      mismatches: ['policy']
    }
  }),

  /** Consent revoked: generation 1 retired, generation 2 current, private home invalidated. */
  revoked: snapshot({
    ...loggedInA,
    workerGeneration: 2,
    privateHome: { codexHome: FIXTURE_CODEX_HOME, status: 'invalidated', ambientCodexRead: false },
    consent: {
      status: 'revoked',
      retiredGeneration: 1,
      privateHomeInvalidated: true,
      revokedAt: '2026-09-03T10:20:00.000Z'
    }
  }),

  /** Signed in with an account that has no email: identified by a volatile epoch. */
  nullEmailEpoch: snapshot({
    account: { status: 'loggedIn', identity: FIXTURE_NULL_EMAIL_ACCOUNT },
    privateHome: { codexHome: FIXTURE_CODEX_HOME, status: 'present', ambientCodexRead: false },
    consent: {
      status: 'granted',
      scope: grantedScope(FIXTURE_NULL_EMAIL_ACCOUNT),
      grantedAt: FIXTURE_GRANTED_AT
    }
  }),

  /** Rate-limited with approvals pending. */
  rateLimitedApprovalsPending: snapshot({
    ...grantedA,
    rateLimit: {
      status: 'limited',
      resetsAt: '2026-09-03T10:45:00.000Z',
      detail: 'Provider rate limit reached for this account'
    },
    approvals: {
      pendingCount: 2,
      lastDecision: { outcome: 'denied', at: '2026-09-03T10:30:00.000Z', subject: 'shell' }
    }
  }),

  /** Agent 2 / TASK selected while G-ROLE cannot mechanically prove non-delegation. */
  roleAgent2NotMechanicallyEnforced: snapshot({
    ...grantedA,
    consent: {
      status: 'granted',
      scope: grantedScope(FIXTURE_ACCOUNT_A, { rolePosture: 'agent2' }),
      grantedAt: FIXTURE_GRANTED_AT
    },
    role: { selected: 'agent2', enforcement: 'notMechanicallyEnforced' }
  }),

  /** Agent 2 / TASK selected with G-ROLE proof present: no label. */
  roleAgent2MechanicallyProven: snapshot({
    ...grantedA,
    consent: {
      status: 'granted',
      scope: grantedScope(FIXTURE_ACCOUNT_A, { rolePosture: 'agent2' }),
      grantedAt: FIXTURE_GRANTED_AT
    },
    role: { selected: 'agent2', enforcement: 'mechanicallyProven' }
  })
} as const satisfies Record<string, HostedEngineConsentSnapshot>;

export type ConsentUxFixtureName = keyof typeof CONSENT_UX_FIXTURES;

export const CONSENT_UX_FIXTURE_NAMES = Object.keys(CONSENT_UX_FIXTURES) as ConsentUxFixtureName[];

/** A deep copy so a consumer can never mutate the shared fixture bytes. */
export function consentUxFixture(name: ConsentUxFixtureName): HostedEngineConsentSnapshot {
  return structuredClone(CONSENT_UX_FIXTURES[name]) as HostedEngineConsentSnapshot;
}
