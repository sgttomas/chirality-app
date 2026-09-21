/**
 * UI-facing vocabulary for the hosted-engine account/consent surface
 * (DEL-02-05-V3-02, WP-07 static fixtures).
 *
 * Shaped by App `docs/CONTRACT.md`:
 *
 * - **K-CONSENT-1** — `HostedEngineConsentPort` is the sole App coordinator
 *   boundary for admitting a hosted-engine worker, thread, or turn. It
 *   validates the server-owned canonical root, project identity, adapter,
 *   exact non-secret account digest or volatile null-email epoch, notice/policy
 *   digest, selected role posture, effective configuration digest, and worker
 *   generation. Consent is per canonical root and is never reused across root,
 *   account, policy, or generation changes. Revocation retires the affected
 *   root generation and invalidates its private home. A caller-supplied `cwd`
 *   never overrides the stored canonical root.
 * - **K-NET-1** — each canonical root selects, under explicit consent, one
 *   command-network posture: no command network (the default); ask per
 *   destination (host/protocol context, the queued-request caveat, and
 *   `acceptForSession` only as an explicit user act); or command network on
 *   through `network_access = true`, visibly labelled.
 * - **K-KEY-1** — root-private login state is never copied or symlinked from
 *   ambient `~/.codex`; nothing here carries key material.
 * - **K-ROLE-2** — Agent 0/1/2 role entry is always offered for Codex
 *   sessions; when G-ROLE cannot mechanically prove non-delegation, Agent 2 /
 *   TASK entry carries the label `role not mechanically enforced` and its
 *   governed-workflow evidence is marked `instruction-asserted`.
 *
 * This module is the renderer-side *shape* the settings panel consumes. The
 * account/consent semantics themselves are Root-owned (DEP-02-05-008/009);
 * the accepted Root/App contract is not yet routed to the App, so the only
 * adapter in this tree is the fake in `fake-hosted-engine-consent-port.ts`.
 * Live consumption is DEL-02-05-V3-03 and replaces nothing here; it supplies
 * a real `HostedEngineConsentPort`. The product posture is `Opt-in Preview`
 * (G0 A8).
 */

// ---------------------------------------------------------------------------
// Product posture
// ---------------------------------------------------------------------------

/** Owner-ruled product posture label (G0 A8). Rendered verbatim. */
export const PRODUCT_POSTURE_LABEL = 'Opt-in Preview';

// ---------------------------------------------------------------------------
// Command-network postures (K-NET-1)
// ---------------------------------------------------------------------------

export const COMMAND_NETWORK_POSTURES = ['off', 'askPerDestination', 'on'] as const;

export type CommandNetworkPosture = (typeof COMMAND_NETWORK_POSTURES)[number];

/** No command network unless the operator explicitly selects otherwise. */
export const DEFAULT_COMMAND_NETWORK_POSTURE: CommandNetworkPosture = 'off';

/** The configuration key/value that posture `on` corresponds to; shown verbatim. */
export const COMMAND_NETWORK_ON_CONFIG_LABEL = 'network_access = true';

export const COMMAND_NETWORK_POSTURE_LABELS: Record<CommandNetworkPosture, string> = {
  off: 'No command network (default)',
  askPerDestination: 'Ask per destination',
  on: `Command network on (${COMMAND_NETWORK_ON_CONFIG_LABEL})`
};

export function isCommandNetworkPosture(value: unknown): value is CommandNetworkPosture {
  return (
    typeof value === 'string' &&
    (COMMAND_NETWORK_POSTURES as readonly string[]).includes(value)
  );
}

/**
 * A managed-network prompt for one destination under `askPerDestination`.
 * Carries only host/protocol context; never a URL with credentials, and never
 * a request body.
 */
export type NetworkDestinationPrompt = {
  promptId: string;
  host: string;
  protocol: string;
  port?: number;
  /**
   * Requests to the same destination that are already queued behind this
   * prompt. An upstream grant may unblock them too — the K-NET-1 caveat the
   * prompt must show.
   */
  queuedRequestCount: number;
  /** Non-secret one-line summary of what asked (a command name, not its arguments). */
  requestedBy?: string;
};

/**
 * `acceptForSession` is permitted only as an explicit user act (K-NET-1); an
 * adapter must never select it on the operator's behalf.
 */
export const NETWORK_PROMPT_DECISIONS = ['allowOnce', 'acceptForSession', 'deny'] as const;

export type NetworkPromptDecision = (typeof NETWORK_PROMPT_DECISIONS)[number];

export const NETWORK_PROMPT_DECISION_LABELS: Record<NetworkPromptDecision, string> = {
  allowOnce: 'Allow once',
  acceptForSession: 'Accept for this session',
  deny: 'Deny'
};

export type NetworkPostureState = {
  posture: CommandNetworkPosture;
  /** The prompt awaiting the operator, if the posture is `askPerDestination`. */
  pendingPrompt: NetworkDestinationPrompt | null;
  /** `host` + `protocol` keys accepted for this session — only ever by explicit user act. */
  sessionAcceptedDestinations: readonly string[];
};

export function destinationKey(destination: { host: string; protocol: string; port?: number }): string {
  const port = destination.port === undefined ? '' : `:${destination.port}`;
  return `${destination.protocol}://${destination.host}${port}`;
}

// ---------------------------------------------------------------------------
// Account identity and login state (K-CONSENT-1, K-KEY-1)
// ---------------------------------------------------------------------------

/**
 * The exact non-secret account identity the consent boundary validates: a
 * digest of the account, or a volatile epoch for an account without an email.
 * Never an email address, token, cookie, or device code.
 */
export type AccountIdentity =
  | { kind: 'digest'; accountDigest: string }
  | { kind: 'nullEmailEpoch'; epoch: string };

export type AccountState =
  | { status: 'loggedOut' }
  | { status: 'loggedIn'; identity: AccountIdentity };

export function accountIdentityEquals(a: AccountIdentity | null, b: AccountIdentity | null): boolean {
  if (a === null || b === null) {
    return a === b;
  }
  if (a.kind !== b.kind) {
    return false;
  }
  return a.kind === 'digest'
    ? a.accountDigest === (b as { accountDigest: string }).accountDigest
    : a.epoch === (b as { epoch: string }).epoch;
}

/** Short, non-secret display form of an identity (never the full digest). */
export function describeAccountIdentity(identity: AccountIdentity): string {
  if (identity.kind === 'digest') {
    return `account …${identity.accountDigest.slice(-8)}`;
  }
  return `account without an email (volatile epoch ${identity.epoch})`;
}

// ---------------------------------------------------------------------------
// Root-private, app-owned Codex home (G0 A9, K-KEY-1)
// ---------------------------------------------------------------------------

export type PrivateHomeState = {
  /** App-owned, root-private `CODEX_HOME` path (non-secret; under the app's own user-data). */
  codexHome: string;
  status: 'absent' | 'present' | 'invalidated';
  /**
   * Structural statement of K-KEY-1: the private home is never sourced from
   * the ambient `~/.codex`. The type admits only `false`.
   */
  ambientCodexRead: false;
};

// ---------------------------------------------------------------------------
// Role entry (K-ROLE-2, K-UNTYPED-1)
// ---------------------------------------------------------------------------

export const ROLE_POSTURES = ['untyped', 'agent0', 'agent1', 'agent2'] as const;

export type RolePosture = (typeof ROLE_POSTURES)[number];

export const ROLE_POSTURE_LABELS: Record<RolePosture, string> = {
  untyped: 'Untyped session',
  agent0: 'Agent 0 (supervising architect)',
  agent1: 'Agent 1 (manager)',
  agent2: 'Agent 2 / TASK (specialist)'
};

export type RoleEnforcement = 'mechanicallyProven' | 'notMechanicallyEnforced';

/** Verbatim K-ROLE-2 label for Agent 2/TASK entry when G-ROLE proof is absent. */
export const ROLE_NOT_MECHANICALLY_ENFORCED_LABEL = 'role not mechanically enforced';

/** Verbatim K-ROLE-2 marking of governed-workflow evidence when G-ROLE proof is absent. */
export const INSTRUCTION_ASSERTED_EVIDENCE_LABEL = 'instruction-asserted';

export type RoleState = {
  selected: RolePosture;
  enforcement: RoleEnforcement;
};

export function isRolePosture(value: unknown): value is RolePosture {
  return typeof value === 'string' && (ROLE_POSTURES as readonly string[]).includes(value);
}

// ---------------------------------------------------------------------------
// Consent scope and state (K-CONSENT-1)
// ---------------------------------------------------------------------------

/** Everything K-CONSENT-1 validates before worker boot, thread creation/resume, and each turn. */
export type ConsentScope = {
  /** Server-owned canonical root. A caller-supplied `cwd` never overrides it. */
  canonicalRoot: string;
  projectId: string;
  adapter: string;
  account: AccountIdentity | null;
  /** Notice/policy digest the operator consented under. */
  policyDigest: string;
  rolePosture: RolePosture;
  /** Effective configuration digest (includes the command-network posture). */
  configDigest: string;
  workerGeneration: number;
};

export const CONSENT_SCOPE_FIELDS = [
  'root',
  'project',
  'adapter',
  'account',
  'policy',
  'role',
  'config',
  'generation'
] as const;

export type ConsentMismatch = (typeof CONSENT_SCOPE_FIELDS)[number];

export const CONSENT_MISMATCH_LABELS: Record<ConsentMismatch, string> = {
  root: 'the working root changed',
  project: 'the project identity changed',
  adapter: 'the adapter changed',
  account: 'the signed-in account changed',
  policy: 'the notice or policy changed',
  role: 'the selected role changed',
  config: 'the effective configuration changed',
  generation: 'the root generation changed'
};

/** Field-by-field comparison of a granted scope against the current one. */
export function compareConsentScopes(granted: ConsentScope, current: ConsentScope): ConsentMismatch[] {
  const mismatches: ConsentMismatch[] = [];
  if (granted.canonicalRoot !== current.canonicalRoot) mismatches.push('root');
  if (granted.projectId !== current.projectId) mismatches.push('project');
  if (granted.adapter !== current.adapter) mismatches.push('adapter');
  if (!accountIdentityEquals(granted.account, current.account)) mismatches.push('account');
  if (granted.policyDigest !== current.policyDigest) mismatches.push('policy');
  if (granted.rolePosture !== current.rolePosture) mismatches.push('role');
  if (granted.configDigest !== current.configDigest) mismatches.push('config');
  if (granted.workerGeneration !== current.workerGeneration) mismatches.push('generation');
  return mismatches;
}

export type ConsentState =
  | { status: 'notGranted' }
  | { status: 'granted'; scope: ConsentScope; grantedAt: string }
  | {
      /** A previous grant exists but cannot be reused: the scope it was bound to no longer matches. */
      status: 'stale';
      grantedScope: ConsentScope;
      mismatches: readonly ConsentMismatch[];
    }
  | {
      status: 'revoked';
      retiredGeneration: number;
      privateHomeInvalidated: true;
      revokedAt: string;
    };

export const CONSENT_STATUSES = ['notGranted', 'granted', 'stale', 'revoked'] as const;

export type ConsentStatus = (typeof CONSENT_STATUSES)[number];

// ---------------------------------------------------------------------------
// Rate-limit and approval status
// ---------------------------------------------------------------------------

export type RateLimitStatus =
  | { status: 'ok' }
  | { status: 'limited'; resetsAt: string; detail?: string }
  | { status: 'unknown' };

export type ApprovalStatus = {
  pendingCount: number;
  lastDecision?: {
    outcome: 'approved' | 'denied';
    at: string;
    /** Non-secret subject (a tool or command name), never arguments or outputs. */
    subject: string;
  };
};

// ---------------------------------------------------------------------------
// Snapshot and port
// ---------------------------------------------------------------------------

/**
 * The complete non-secret view the settings panel renders. It never carries
 * tokens, cookies, device codes, emails, or any ambient `~/.codex` content.
 */
export type HostedEngineConsentSnapshot = {
  productPosture: typeof PRODUCT_POSTURE_LABEL;
  canonicalRoot: string;
  projectId: string;
  adapter: string;
  policyDigest: string;
  configDigest: string;
  workerGeneration: number;
  account: AccountState;
  privateHome: PrivateHomeState;
  consent: ConsentState;
  network: NetworkPostureState;
  rateLimit: RateLimitStatus;
  approvals: ApprovalStatus;
  role: RoleState;
};

/** The current scope K-CONSENT-1 would validate, derived from a snapshot. */
export function currentConsentScope(snapshot: HostedEngineConsentSnapshot): ConsentScope {
  return {
    canonicalRoot: snapshot.canonicalRoot,
    projectId: snapshot.projectId,
    adapter: snapshot.adapter,
    account: snapshot.account.status === 'loggedIn' ? snapshot.account.identity : null,
    policyDigest: snapshot.policyDigest,
    rolePosture: snapshot.role.selected,
    configDigest: snapshot.configDigest,
    workerGeneration: snapshot.workerGeneration
  };
}

export type ConsentActResult = { ok: true } | { ok: false; error: string };

/**
 * The renderer-facing port. Every method that changes state is an explicit
 * user act initiated from the settings panel; the port never performs one on
 * its own. A live adapter (DEL-02-05-V3-03) implements this against the
 * accepted Root/App contract; until then only the fake exists.
 */
export type HostedEngineConsentPort = {
  getSnapshot(): HostedEngineConsentSnapshot;
  subscribe(listener: (snapshot: HostedEngineConsentSnapshot) => void): () => void;
  login(): Promise<ConsentActResult>;
  logout(): Promise<ConsentActResult>;
  grantConsent(): Promise<ConsentActResult>;
  revokeConsent(): Promise<ConsentActResult>;
  selectNetworkPosture(posture: CommandNetworkPosture): Promise<ConsentActResult>;
  resolveNetworkPrompt(promptId: string, decision: NetworkPromptDecision): Promise<ConsentActResult>;
  selectRole(role: RolePosture): Promise<ConsentActResult>;
};
