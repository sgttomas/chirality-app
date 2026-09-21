/**
 * Fake `HostedEngineConsentPort` (DEL-02-05-V3-02).
 *
 * An in-memory, deterministic test double shaped by K-CONSENT-1 / K-NET-1 /
 * K-KEY-1 / K-ROLE-2 so the account/consent settings panel can be rendered
 * and exercised before the accepted Root/App account/consent contract is
 * routed to the App. It performs no I/O: no login ceremony, no network, no
 * filesystem, no keychain, no read of the ambient `~/.codex`. Its identities
 * are digests and epochs; it holds no token, cookie, or device code and can
 * therefore persist none.
 *
 * It is never mounted in the product shell. The live adapter is
 * DEL-02-05-V3-03's scope and replaces nothing exported here — it simply
 * supplies a real `HostedEngineConsentPort` to the same panel.
 *
 * Behaviour modelled from the contract text:
 *
 * - consent binds to the current scope at grant time and turns `stale` as
 *   soon as any validated field changes (account, policy, role, config,
 *   generation, root, project, adapter); a stale grant is never reused, its
 *   command-network posture falls back to `off`, and only a fresh explicit
 *   `grantConsent()` returns it to `granted`;
 * - revocation retires the current root generation, starts the next one, and
 *   invalidates the private home; the network posture falls back to `off`
 *   and session acceptances are cleared;
 * - the command-network posture defaults to `off`, may only be selected under
 *   a `granted` consent, and `acceptForSession` happens only through
 *   `resolveNetworkPrompt(id, 'acceptForSession')` — never by the adapter;
 * - admission (`admit`) checks the stored canonical root; a caller-supplied
 *   `cwd` is ignored.
 */

import {
  DEFAULT_COMMAND_NETWORK_POSTURE,
  compareConsentScopes,
  currentConsentScope,
  destinationKey,
  isCommandNetworkPosture,
  isRolePosture,
  type AccountIdentity,
  type ApprovalStatus,
  type CommandNetworkPosture,
  type ConsentActResult,
  type ConsentMismatch,
  type ConsentScope,
  type HostedEngineConsentPort,
  type HostedEngineConsentSnapshot,
  type NetworkDestinationPrompt,
  type NetworkPromptDecision,
  type RateLimitStatus,
  type RoleEnforcement,
  type RolePosture
} from './hosted-engine-consent-port';
import { CONSENT_UX_FIXTURES, FIXTURE_ACCOUNT_A } from './consent-ux-fixtures';

/** What a K-CONSENT-1 admission check receives before worker boot, thread creation/resume, or a turn. */
export type FakeAdmissionRequest = {
  canonicalRoot: string;
  projectId: string;
  adapter: string;
  account: AccountIdentity | null;
  policyDigest: string;
  rolePosture: RolePosture;
  configDigest: string;
  workerGeneration: number;
  /** Caller-supplied working directory. Never consulted for the root check. */
  cwd?: string;
};

export type FakeAdmissionDecision =
  | { admitted: true; scope: ConsentScope }
  | { admitted: false; reason: 'notGranted' | 'stale' | 'revoked' | 'scopeMismatch'; mismatches: readonly ConsentMismatch[] };

/** Test-only controls that stand in for the runtime side of the boundary. */
export type FakeHostedEngineConsentControls = {
  /** Simulate the runtime asking about a destination (only meaningful under `askPerDestination`). */
  enqueueNetworkPrompt(prompt: NetworkDestinationPrompt): void;
  /** Rotate the notice/policy digest (a policy change the operator has not consented to). */
  rotatePolicy(policyDigest: string): void;
  /** Change the effective configuration digest. */
  setConfigDigest(configDigest: string): void;
  setRateLimit(status: RateLimitStatus): void;
  setApprovals(status: ApprovalStatus): void;
  setRoleEnforcement(enforcement: RoleEnforcement): void;
  /** The identity the next `login()` produces (defaults to fixture account A). */
  setNextLoginIdentity(identity: AccountIdentity): void;
  /** Make the next act fail with the given error (once), to exercise the panel's error line. */
  failNextAct(error: string): void;
  /** K-CONSENT-1 admission check against the stored scope. */
  admit(request: FakeAdmissionRequest): FakeAdmissionDecision;
  /** Every act performed through the port, in order (for tests asserting explicit-act-only paths). */
  readonly actLog: readonly string[];
};

export type FakeHostedEngineConsentPort = HostedEngineConsentPort & {
  readonly control: FakeHostedEngineConsentControls;
};

export type FakeHostedEngineConsentPortOptions = {
  /** Starting snapshot; defaults to the `loggedOutDefault` fixture. */
  initial?: HostedEngineConsentSnapshot;
  /** Clock used for `grantedAt` / `revokedAt`; deterministic by default. */
  now?: () => string;
};

function clone<T>(value: T): T {
  return structuredClone(value) as T;
}

function makeClock(): () => string {
  let tick = 0;
  return () => {
    tick += 1;
    return `2026-09-03T12:00:${String(tick).padStart(2, '0')}.000Z`;
  };
}

export function createFakeHostedEngineConsentPort(
  options: FakeHostedEngineConsentPortOptions = {}
): FakeHostedEngineConsentPort {
  let state: HostedEngineConsentSnapshot = clone(options.initial ?? CONSENT_UX_FIXTURES.loggedOutDefault);
  const now = options.now ?? makeClock();
  const listeners = new Set<(snapshot: HostedEngineConsentSnapshot) => void>();
  const actLog: string[] = [];
  let nextLoginIdentity: AccountIdentity = clone(FIXTURE_ACCOUNT_A);
  let pendingFailure: string | null = null;

  function publish(): void {
    const snapshot = clone(state);
    for (const listener of listeners) {
      listener(snapshot);
    }
  }

  /** Re-derive a granted consent against the current scope; a stale grant stays stale. */
  function reconcileConsent(): void {
    if (state.consent.status !== 'granted') {
      return;
    }
    const mismatches = compareConsentScopes(state.consent.scope, currentConsentScope(state));
    if (mismatches.length > 0) {
      state = {
        ...state,
        consent: { status: 'stale', grantedScope: state.consent.scope, mismatches },
        network: {
          posture: DEFAULT_COMMAND_NETWORK_POSTURE,
          pendingPrompt: null,
          sessionAcceptedDestinations: []
        }
      };
    }
  }

  function act(name: string, mutate: () => ConsentActResult): Promise<ConsentActResult> {
    actLog.push(name);
    if (pendingFailure !== null) {
      const error = pendingFailure;
      pendingFailure = null;
      return Promise.resolve({ ok: false, error });
    }
    const result = mutate();
    if (result.ok) {
      reconcileConsent();
      publish();
    }
    return Promise.resolve(result);
  }

  const port: FakeHostedEngineConsentPort = {
    getSnapshot: () => clone(state),

    subscribe(listener) {
      listeners.add(listener);
      return () => {
        listeners.delete(listener);
      };
    },

    login: () =>
      act('login', () => {
        if (state.account.status === 'loggedIn') {
          return { ok: false, error: 'Already signed in for this root.' };
        }
        state = {
          ...state,
          account: { status: 'loggedIn', identity: clone(nextLoginIdentity) },
          privateHome: { ...state.privateHome, status: 'present', ambientCodexRead: false }
        };
        return { ok: true };
      }),

    logout: () =>
      act('logout', () => {
        if (state.account.status === 'loggedOut') {
          return { ok: false, error: 'Not signed in for this root.' };
        }
        state = { ...state, account: { status: 'loggedOut' } };
        return { ok: true };
      }),

    grantConsent: () =>
      act('grantConsent', () => {
        if (state.account.status !== 'loggedIn') {
          return { ok: false, error: 'Sign in for this root before granting consent.' };
        }
        state = {
          ...state,
          privateHome:
            state.privateHome.status === 'invalidated'
              ? { ...state.privateHome, status: 'present', ambientCodexRead: false }
              : state.privateHome,
          consent: { status: 'granted', scope: currentConsentScope(state), grantedAt: now() }
        };
        return { ok: true };
      }),

    revokeConsent: () =>
      act('revokeConsent', () => {
        if (state.consent.status === 'notGranted' || state.consent.status === 'revoked') {
          return { ok: false, error: 'There is no consent to revoke for this root.' };
        }
        const retiredGeneration = state.workerGeneration;
        state = {
          ...state,
          workerGeneration: retiredGeneration + 1,
          privateHome: { ...state.privateHome, status: 'invalidated', ambientCodexRead: false },
          consent: {
            status: 'revoked',
            retiredGeneration,
            privateHomeInvalidated: true,
            revokedAt: now()
          },
          network: {
            posture: DEFAULT_COMMAND_NETWORK_POSTURE,
            pendingPrompt: null,
            sessionAcceptedDestinations: []
          }
        };
        return { ok: true };
      }),

    selectNetworkPosture: (posture) =>
      act(`selectNetworkPosture:${String(posture)}`, () => {
        if (!isCommandNetworkPosture(posture)) {
          return { ok: false, error: 'Unknown command-network posture.' };
        }
        if (state.consent.status !== 'granted') {
          return {
            ok: false,
            error: 'Grant consent for this root before choosing a command-network posture.'
          };
        }
        state = {
          ...state,
          network: {
            posture,
            // A prompt only exists under ask-per-destination; leaving that
            // posture drops it unanswered (fail closed), never as a grant.
            pendingPrompt: posture === 'askPerDestination' ? state.network.pendingPrompt : null,
            sessionAcceptedDestinations:
              posture === 'askPerDestination' ? state.network.sessionAcceptedDestinations : []
          }
        };
        return { ok: true };
      }),

    resolveNetworkPrompt: (promptId, decision) =>
      act(`resolveNetworkPrompt:${decision}`, () => {
        if (state.consent.status !== 'granted') {
          return {
            ok: false,
            error: 'Grant consent for this root before resolving a command-network prompt.'
          };
        }
        const prompt = state.network.pendingPrompt;
        if (state.network.posture !== 'askPerDestination' || !prompt || prompt.promptId !== promptId) {
          return { ok: false, error: 'That network prompt is no longer pending.' };
        }
        const accepted =
          decision === 'acceptForSession'
            ? [...state.network.sessionAcceptedDestinations, destinationKey(prompt)]
            : state.network.sessionAcceptedDestinations;
        state = {
          ...state,
          network: {
            ...state.network,
            pendingPrompt: null,
            sessionAcceptedDestinations: accepted
          }
        };
        return { ok: true };
      }),

    selectRole: (role) =>
      act(`selectRole:${String(role)}`, () => {
        if (!isRolePosture(role)) {
          return { ok: false, error: 'Unknown role posture.' };
        }
        state = { ...state, role: { ...state.role, selected: role } };
        return { ok: true };
      }),

    control: {
      enqueueNetworkPrompt(prompt) {
        if (state.network.posture !== 'askPerDestination') {
          return;
        }
        state = { ...state, network: { ...state.network, pendingPrompt: clone(prompt) } };
        publish();
      },
      rotatePolicy(policyDigest) {
        state = { ...state, policyDigest };
        reconcileConsent();
        publish();
      },
      setConfigDigest(configDigest) {
        state = { ...state, configDigest };
        reconcileConsent();
        publish();
      },
      setRateLimit(status) {
        state = { ...state, rateLimit: clone(status) };
        publish();
      },
      setApprovals(status) {
        state = { ...state, approvals: clone(status) };
        publish();
      },
      setRoleEnforcement(enforcement) {
        state = { ...state, role: { ...state.role, enforcement } };
        publish();
      },
      setNextLoginIdentity(identity) {
        nextLoginIdentity = clone(identity);
      },
      failNextAct(error) {
        pendingFailure = error;
      },
      admit(request) {
        const consent = state.consent;
        if (consent.status === 'notGranted') {
          return { admitted: false, reason: 'notGranted', mismatches: [] };
        }
        if (consent.status === 'revoked') {
          return { admitted: false, reason: 'revoked', mismatches: [] };
        }
        if (consent.status === 'stale') {
          return { admitted: false, reason: 'stale', mismatches: consent.mismatches };
        }
        // The stored canonical root is authoritative; `request.cwd` is not read.
        const requested: ConsentScope = {
          canonicalRoot: request.canonicalRoot,
          projectId: request.projectId,
          adapter: request.adapter,
          account: request.account,
          policyDigest: request.policyDigest,
          rolePosture: request.rolePosture,
          configDigest: request.configDigest,
          workerGeneration: request.workerGeneration
        };
        const mismatches = compareConsentScopes(consent.scope, requested);
        if (mismatches.length > 0) {
          return { admitted: false, reason: 'scopeMismatch', mismatches };
        }
        return { admitted: true, scope: clone(consent.scope) };
      },
      actLog
    }
  };

  return port;
}
