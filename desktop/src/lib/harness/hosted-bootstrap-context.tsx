'use client';

import React, { createContext, useContext, useMemo, type ReactNode } from 'react';
import type { HostedBootstrapStatus, HostedModelCatalogEntry, HostedModelSelection } from '@chirality/runtime-contracts';
import type { HostedBootstrapStatusResponse } from './hosted-bootstrap-client';
import type { HostedProjectState } from '../../components/settings/hosted-bootstrap-controller';

/**
 * Read-only view of the single hosted-bootstrap controller instance owned by
 * the shell frame. Surfaces rendered inside the frame (the chat panel's model
 * and reasoning selectors) consume it without a second controller or a second
 * status poll. Outside a provider the value reads as "not signed in".
 */
export type HostedBootstrapContextValue = {
  snapshot: HostedBootstrapStatusResponse | null;
  loading: boolean;
  /** Last account status reported for any folder this session; survives folder changes. */
  account?: HostedBootstrapStatus | null;
  /** The selected folder's standing with the Runtime, separate from the account. */
  project?: HostedProjectState;
  /** Re-reads Runtime status; a failed turn may have fenced the account underneath a "ready" snapshot. */
  refresh?: () => void;
};

/** The authenticated Codex catalog as exposed by Runtime status while admission is ready. */
export type HostedModelCatalogView = {
  models: readonly HostedModelCatalogEntry[];
  selection: HostedModelSelection;
};

const HostedBootstrapContext = createContext<HostedBootstrapContextValue>({ snapshot: null, loading: false });

export function HostedBootstrapProvider({ snapshot, loading, account, project, refresh, children }: HostedBootstrapContextValue & { children: ReactNode }): JSX.Element {
  const value = useMemo(() => ({ snapshot, loading, ...(account !== undefined ? { account } : {}), ...(project ? { project } : {}), ...(refresh ? { refresh } : {}) }), [snapshot, loading, account, project, refresh]);
  return <HostedBootstrapContext.Provider value={value}>{children}</HostedBootstrapContext.Provider>;
}

export function useHostedBootstrap(): HostedBootstrapContextValue {
  return useContext(HostedBootstrapContext);
}

/**
 * The catalog is usable only while the account is signed in and the engine is
 * admitted; Runtime publishes `models`/`selection` together in exactly that
 * state. Any other snapshot yields null so the selectors stay disabled rather
 * than offering a stale or empty list.
 */
export function selectHostedModelCatalog(snapshot: HostedBootstrapStatusResponse | null): HostedModelCatalogView | null {
  if (snapshot?.registration !== 'registered') return null;
  return selectAccountModelCatalog(snapshot.status);
}

/** The same catalog read from an account status alone (the last one reported for any folder). */
export function selectAccountModelCatalog(status: HostedBootstrapStatus | null | undefined): HostedModelCatalogView | null {
  if (!status || status.ceremony !== 'signed-in' || status.admission !== 'ready') return null;
  if (!status.models || status.models.length === 0 || !status.selection) return null;
  return { models: status.models, selection: status.selection };
}

/**
 * Why the model selectors are disabled, in the user's terms: a folder problem
 * is named as such rather than as a sign-in problem.
 */
export function modelSelectorUnavailableTitle(value: Pick<HostedBootstrapContextValue, 'snapshot' | 'account' | 'project'>): string {
  const status = value.snapshot?.registration === 'registered' ? value.snapshot.status : value.account ?? null;
  const project = value.project?.state;
  if (status?.ceremony === 'signed-in') {
    if (project === 'conflict' || project === 'unavailable' || project === 'setup-required') return 'This folder is not available to Codex yet. Set it up from the account menu to choose a model.';
    if (project === 'checking') return 'Checking this folder. Models load once it is ready.';
    if (status.admission === 'establishing') return 'Codex is preparing. Models load once it is ready.';
    if (status.admission === 'ready') return 'Codex reported no model catalog for this folder yet.';
    return 'Codex is not ready in this folder yet. Models load once it is.';
  }
  if (status?.ceremony === 'pending') return 'Finish signing in to Codex to choose a model';
  return 'Sign in to Codex to choose a model';
}

/** True when the pair names a catalog model and one of that model's supported efforts. */
export function isSelectionInCatalog(catalog: HostedModelCatalogView, selection: HostedModelSelection | null | undefined): selection is HostedModelSelection {
  if (!selection) return false;
  const entry = catalog.models.find(model => model.model === selection.model);
  return Boolean(entry && entry.supportedReasoningEfforts.includes(selection.reasoningEffort));
}
