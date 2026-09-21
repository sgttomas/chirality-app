'use client';

import { usePathname, useRouter, useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { harnessApiErrorMessage } from '../../lib/harness/client';
import { resolvePersona } from '../../lib/shell/persona-resolution';
import { useRuntimeEpoch } from './runtime-connectivity-provider';
import { listRoles, type RoleDescriptor } from '../../lib/harness/method-selection-client';
import { useWorkspace } from '../workspace/workspace-provider';

type PersonaPickerProps = {
  compact?: boolean;
  buildHref?: (persona: string) => string;
  disabled?: boolean;
  onPersonaSelected?: (persona: string) => void;
};

/**
 * Direct-chat persona picker (D-APP-24). Lists Type-0/Type-1 personas only
 * (server-filtered via `listDirectChatPersonas`); selecting one drives the
 * surface by setting `?agent=`, which `chat-panel`'s route-free `resolvePersona`
 * already consumes to boot the chosen persona on the next turn. Type-2 task
 * agents are never offered — they run only via orchestration.
 */
export function PersonaPicker({
  compact = false,
  buildHref,
  disabled = false,
  onPersonaSelected
}: PersonaPickerProps): JSX.Element {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const [personas, setPersonas] = useState<RoleDescriptor[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  const runtimeEpoch = useRuntimeEpoch();
  const { projectRoot } = useWorkspace();

  // The roster is fetched once per mount and once per reconnect. A roster loaded
  // while the daemon was unreachable is the "WORKING_ITEMS (unavailable)" state
  // the operator reported: an empty list plus a permanent error, both of which
  // this re-run replaces with the real answer.
  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    if (!projectRoot) { setPersonas([]); setLoading(false); return; }
    listRoles(projectRoot)
      .then((roles) => {
        if (!cancelled) {
          setPersonas(roles.filter(role => role.directEntry));
          setLoadError(null);
        }
      })
      .catch((error) => {
        if (!cancelled) {
          setLoadError(harnessApiErrorMessage(error));
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false);
        }
      });
    return () => {
      cancelled = true;
    };
  }, [runtimeEpoch, projectRoot]);

  const selected = resolvePersona(searchParams.get('agent'));
  const selectedInRoster = personas.some((persona) => persona.id === selected);

  return (
    <div className="persona-picker">
      <label className={compact ? 'visually-hidden' : undefined} htmlFor="persona-picker-select">Role</label>
      <select
        id="persona-picker-select"
        title={compact ? selected : undefined}
        value={loading ? '' : selected}
        disabled={disabled || loading || personas.length === 0}
        onChange={(event) => {
          const persona = event.target.value;
          const href = buildHref ? buildHref(persona) : (() => {
            const params = new URLSearchParams(searchParams.toString());
            params.set('agent', persona);
            return `${pathname || '/'}?${params.toString()}`;
          })();
          router.replace(href);
          onPersonaSelected?.(persona);
        }}
      >
        {loading ? <option value="">Loading roles…</option> : null}
        {/* A `?agent=` that is not a Type-0/Type-1 persona (e.g. a hand-edited
            URL) is shown disabled so the control stays controlled without
            silently offering a non-direct-chat agent. */}
        {!loading && !selectedInRoster ? (
          <option value={selected} disabled>
            {compact ? selected.toLowerCase().split('_').map(word => word[0].toUpperCase() + word.slice(1)).join(' ') : selected} (unavailable)
          </option>
        ) : null}
        {personas.map((persona) => (
          <option key={persona.id} value={persona.id}>
            {compact ? persona.id.toLowerCase().split('_').map((word: string) => word[0].toUpperCase() + word.slice(1)).join(' ') : persona.id}
            {!compact ? ` · Type ${persona.agentType}` : null}
          </option>
        ))}
      </select>
      {loadError ? (
        <p className="persona-picker-error" role="alert">
          {loadError}
        </p>
      ) : null}
    </div>
  );
}
