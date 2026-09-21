'use client';

import React, { useEffect, useState } from 'react';
import type { RoleDescriptor } from '@chirality/runtime-contracts/v3';
import { listRoles } from '../../lib/harness/method-selection-client';
import { useRuntimeEpoch } from '../shell/runtime-connectivity-provider';
import { useWorkspace } from '../workspace/workspace-provider';

export function RoleDirectoryPanel({
  loading,
  error,
  roles
}: {
  loading: boolean;
  error: string | null;
  roles: readonly RoleDescriptor[];
}): JSX.Element {
  return <section className="portal-matrix portal-matrix--sidebar" aria-label="Direct-entry roles">
    <header className="portal-matrix-header">
      <div className="portal-matrix-heading">
        <h3>Roles</h3>
        <p>Choose a direct-entry role beside the composer. Your conversation remains in the same chat.</p>
      </div>
    </header>
    {loading ? <p role="status">Loading roles…</p> : null}
    {error ? <p role="alert">{error}</p> : null}
    {!loading && !error ? <ul className="method-library-list">
      {roles.map(role => <li key={role.id}>
        <strong>{role.id.toLowerCase().split('_').map(word => word[0].toUpperCase() + word.slice(1)).join(' ')}</strong>
        <p>{role.description}</p>
        <small>Type {role.agentType}{role.defaultForNewChat ? ' · new-chat default' : ''}</small>
      </li>)}
    </ul> : null}
  </section>;
}

/** Retained export name keeps legacy Portal routes on the same App surface. */
export function AgentMatrix(): JSX.Element {
  const { projectRoot } = useWorkspace();
  const runtimeEpoch = useRuntimeEpoch();
  const [roles, setRoles] = useState<RoleDescriptor[]>([]);
  const [loading, setLoading] = useState(Boolean(projectRoot));
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    if (!projectRoot) {
      setRoles([]); setLoading(false); setError(null);
      return () => controller.abort();
    }
    setRoles([]); setLoading(true); setError(null);
    void listRoles(projectRoot, controller.signal)
      .then(result => { if (!controller.signal.aborted) setRoles(result.filter(role => role.directEntry)); })
      .catch(reason => { if (!controller.signal.aborted) setError(reason instanceof Error ? reason.message : 'Roles are unavailable.'); })
      .finally(() => { if (!controller.signal.aborted) setLoading(false); });
    return () => controller.abort();
  }, [projectRoot, runtimeEpoch]);

  return <RoleDirectoryPanel loading={loading} error={error} roles={roles} />;
}

/** @deprecated Use RoleDirectoryPanel. */
export const AgentMatrixPanel = RoleDirectoryPanel;
