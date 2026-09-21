'use client';

import React from 'react';
import type { HostedAccountStatus, HostedBootstrapController, HostedProjectState } from './hosted-bootstrap-controller';

/**
 * The account row's neutral label. Authentication state never leaks into the
 * label itself; it is reported by the summary line and the popover detail.
 */
export function hostedBootstrapTitle(_controller: HostedBootstrapController): string {
  return 'Account';
}

export type HostedBootstrapAuthState = 'signed-in' | 'pending' | 'failed' | 'cancelled' | 'signed-out' | 'setup-required' | 'no-folder' | 'checking';
export type HostedBootstrapReadinessState = 'ready' | 'establishing' | 'unavailable' | 'not-applicable';
export type HostedBootstrapProjectState = HostedProjectState['state'];

type HostedBootstrapStateSource = Pick<HostedBootstrapController, 'projectRoot' | 'loading' | 'snapshot' | 'signOutUncertain'> & Partial<Pick<HostedBootstrapController, 'account' | 'project'>>;

function authFromStatus(status: HostedAccountStatus, signOutUncertain: boolean): HostedBootstrapAuthState {
  const { ceremony } = status;
  if (ceremony === 'signed-in') return 'signed-in';
  if (ceremony === 'pending') return 'pending';
  // An unconfirmed sign-out leaves the ceremony `failed` without a failed sign-in attempt; report it as signed out.
  if (ceremony === 'failed') return signOutUncertain ? 'signed-out' : 'failed';
  if (ceremony === 'cancelled') return 'cancelled';
  return 'signed-out';
}

/**
 * Authentication, Runtime readiness and the folder's project standing, kept
 * separate so the UI never blends them. Sign-in is an account fact of the Codex
 * host: while a folder is being checked, is unregistered, is bound behind
 * another folder, or is unreadable, the last reported account status still
 * answers "am I signed in", and only readiness is withheld until the folder is
 * registered. A folder problem therefore never reads as "Sign in required".
 */
export function hostedBootstrapStates(controller: HostedBootstrapStateSource): { auth: HostedBootstrapAuthState; readiness: HostedBootstrapReadinessState; project: HostedBootstrapProjectState } {
  // A registered snapshot is authoritative for the folder; the controller's
  // project axis explains the other cases (checking, conflict, unavailable).
  const project: HostedBootstrapProjectState = controller.snapshot?.registration === 'registered' ? 'registered'
    : controller.project?.state ?? (!controller.projectRoot ? 'none' : controller.loading ? 'checking' : 'setup-required');
  if (!controller.projectRoot) return { auth: 'no-folder', readiness: 'not-applicable', project };
  if (controller.snapshot?.registration === 'registered') {
    const status = controller.snapshot.status;
    const auth = authFromStatus(status, controller.signOutUncertain);
    return { auth, readiness: auth === 'signed-in' ? status.admission : 'not-applicable', project };
  }
  if (controller.account) return { auth: authFromStatus(controller.account, controller.signOutUncertain), readiness: 'not-applicable', project };
  if (controller.loading) return { auth: 'checking', readiness: 'not-applicable', project };
  return { auth: 'setup-required', readiness: 'not-applicable', project };
}

export function projectStateLabel(project: HostedBootstrapProjectState): string {
  switch (project) {
    case 'registered': return 'Ready';
    case 'checking': return 'Checking folder…';
    case 'setup-required': return 'Setup required';
    case 'conflict': return 'Another folder is active';
    case 'unavailable': return 'Folder unavailable';
    default: return 'No folder chosen';
  }
}

export function authStateLabel(auth: HostedBootstrapAuthState): string {
  switch (auth) {
    case 'signed-in': return 'Signed in';
    case 'pending': return 'Waiting for sign-in…';
    case 'failed': return 'Sign-in failed';
    case 'cancelled': return 'Sign-in cancelled';
    case 'signed-out': return 'Not signed in';
    case 'setup-required': return 'Project setup required';
    case 'no-folder': return 'No folder chosen';
    default: return 'Checking…';
  }
}

export function readinessStateLabel(readiness: HostedBootstrapReadinessState): string {
  switch (readiness) {
    case 'ready': return 'Ready to work';
    case 'establishing': return 'Preparing engine';
    case 'unavailable': return 'Engine unavailable';
    default: return 'Not ready';
  }
}

/**
 * One line for the account row: authentication, then readiness when it
 * applies, or the folder's standing when the folder rather than the account
 * is what stands in the way.
 */
export function hostedBootstrapSummary(controller: HostedBootstrapStateSource): string {
  const { auth, readiness, project } = hostedBootstrapStates(controller);
  if (auth === 'no-folder') return 'Choose a folder to get started';
  if (auth === 'checking') return 'Checking this project…';
  if (auth === 'setup-required') return 'Project setup required';
  const folder = project === 'registered' ? null : projectStateLabel(project);
  if (auth === 'signed-in') return `Signed in · ${folder ?? readinessStateLabel(readiness)}`;
  if (auth === 'pending') return 'Waiting for sign-in…';
  if (auth === 'failed') return 'Sign-in failed';
  if (auth === 'cancelled') return 'Sign-in cancelled';
  return folder ? `Not signed in · ${folder}` : 'Sign in required';
}

const PROJECT_EXPLANATIONS: Record<Exclude<HostedBootstrapProjectState, 'registered' | 'none'>, string> = {
  checking: 'Chirality is checking this folder with the Runtime.',
  'setup-required': 'This folder is not a Chirality project yet. Setting it up registers it; your sign-in is not affected.',
  conflict: 'The Runtime is still working in another folder from this session. Using this folder moves it here; your sign-in is not affected.',
  unavailable: 'This folder could not be read or registered. Your sign-in is not affected; fix the folder or choose another one.'
};

// Explanations live on the action they qualify (hover / accessible description)
// so the surface reads as one status line plus one action.
const SETUP_EXPLANATION = (folder: string | null | undefined) => `Use ${folder ?? 'this folder'} as the Chirality project. This writes one minimal chirality.project.json configuration if it is missing. Existing malformed or conflicting configuration is never replaced.`;
const PENDING_EXPLANATION = 'Finish signing in with your ChatGPT account in the browser. Chirality is waiting for OpenAI to confirm.';
const SIGN_IN_EXPLANATION = 'Opens the OpenAI sign-in page in your browser. Codex keeps the credentials; Chirality only waits for the result.';

function signedInExplanation(admission: 'unavailable' | 'establishing' | 'ready', busy: boolean): string {
  if (busy) return 'Signing out of Codex in Chirality…';
  if (admission === 'ready') return 'Codex is ready. Signing out affects only Chirality; other Codex clients keep their own sign-in.';
  if (admission === 'establishing') return 'Your account is signed in. Codex is still preparing.';
  return 'Your account is signed in, but Codex is not yet ready for work.';
}

export function HostedBootstrapView({ controller, compact = false }: { controller: HostedBootstrapController; compact?: boolean }): JSX.Element {
  const { projectRoot, snapshot, loading, busyAction, error, authUrl, signOutUncertain } = controller;
  const status = snapshot?.registration === 'registered' ? snapshot.status : null;
  const folderName = projectRoot?.split('/').filter(Boolean).pop() || projectRoot;
  const states = hostedBootstrapStates(controller);
  const showReadiness = states.auth === 'signed-in' && states.project === 'registered';
  const showProject = states.project !== 'none' && states.project !== 'registered';
  const projectExplanation = states.project === 'registered' || states.project === 'none' ? null : PROJECT_EXPLANATIONS[states.project];
  return <section className="hosted-bootstrap" aria-label="Account" data-bootstrap-registration={snapshot?.registration ?? 'unknown'} data-bootstrap-ceremony={status?.ceremony ?? 'unknown'} data-bootstrap-admission={status?.admission ?? 'unavailable'} data-bootstrap-project={states.project}>
    {!compact ? <h3>Account</h3> : null}
    {compact
      ? <dl className="hosted-bootstrap-states">
          <div><dt>Sign-in</dt><dd data-auth-state={states.auth}>{authStateLabel(states.auth)}</dd></div>
          {showReadiness ? <div><dt>Runtime</dt><dd data-readiness-state={states.readiness}>{readinessStateLabel(states.readiness)}</dd></div> : null}
          {showProject ? <div><dt>Folder</dt><dd data-project-state={states.project} title={projectExplanation ?? undefined}>{projectStateLabel(states.project)}</dd></div> : null}
        </dl>
      : <p className="api-key-status"><strong>{hostedBootstrapSummary(controller)}</strong></p>}
    {!compact && projectExplanation && (states.project === 'conflict' || states.project === 'unavailable') ? <p className="hosted-bootstrap-project" data-project-state={states.project}>{projectExplanation}</p> : null}
    {!projectRoot || loading ? null : snapshot?.registration !== 'registered' ?
      <button type="button" disabled={busyAction !== null} title={SETUP_EXPLANATION(folderName)} onClick={controller.onSetup}>{busyAction === 'setup' ? 'Setting up…' : 'Use this folder'}</button>
    : status?.ceremony === 'pending' ? <>
      <p className="hosted-bootstrap-pending" role="status">{PENDING_EXPLANATION}</p>
      <div className="hosted-bootstrap-actions">
        {authUrl ? <button type="button" className="button-muted" disabled={busyAction !== null} title="Open the same OpenAI sign-in page again in your browser." onClick={controller.onReopenLogin}>Open sign-in page again</button> : null}
        <button type="button" className="button-muted" disabled={busyAction !== null} title="Stop waiting and cancel this sign-in attempt." onClick={controller.onCancelLogin}>{busyAction === 'cancel' ? 'Cancelling…' : 'Cancel'}</button>
      </div>
    </> : status?.ceremony === 'signed-in' ?
      <button type="button" className="button-muted" disabled={busyAction !== null} title={signedInExplanation(status.admission, busyAction === 'logout')} onClick={controller.onSignOut}>{busyAction === 'logout' ? 'Signing out…' : 'Sign out'}</button>
    : <>
      {status?.ceremony === 'failed' && !signOutUncertain ? <p role="alert">Sign-in failed. You can start a new sign-in attempt.</p> : null}
      {status?.ceremony === 'cancelled' ? <p>The previous sign-in was cancelled.</p> : null}
      <button type="button" disabled={busyAction !== null || !status?.canStartLogin} title={SIGN_IN_EXPLANATION} onClick={controller.onStartLogin}>{busyAction === 'login' ? 'Opening sign-in…' : 'Sign in with your ChatGPT account'}</button>
    </>}
    {error ? <p role="alert">{error}</p> : null}
  </section>;
}
