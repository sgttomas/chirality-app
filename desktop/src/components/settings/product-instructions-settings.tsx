'use client';

import React, { useEffect, useState } from 'react';
import type { ProductInstructionsOperation, ProductInstructionsState } from '../../../electron/product-instructions-ipc-contract';

export function ProductInstructionsSettings(): JSX.Element | null {
  const bridge = typeof window === 'undefined' ? undefined : window.chirality?.instructions;
  const [state, setState] = useState<ProductInstructionsState>();
  const [error, setError] = useState<string>();
  const [busy, setBusy] = useState(false);
  useEffect(() => {
    if (!bridge) return;
    let active = true;
    const refresh = async (): Promise<void> => {
      try {
        const result = await bridge.get();
        if (!active) return;
        if (result.ok) { setState(result.state); setError(undefined); }
        else setError(result.error);
      } catch { if (active) setError('Agent instructions are unavailable.'); }
    };
    void refresh();
    window.addEventListener('focus', refresh);
    return () => { active = false; window.removeEventListener('focus', refresh); };
  }, [bridge]);
  if (!bridge) return null;
  const act = async (operation: Exclude<ProductInstructionsOperation, 'get'>): Promise<void> => {
    setBusy(true);
    try {
      const result = await bridge[operation]();
      if (result.ok) { setState(result.state); setError(undefined); }
      else setError(result.error);
    } catch { setError('Agent instructions are unavailable.'); }
    finally { setBusy(false); }
  };
  return <section data-settings-group="instructions">
    <h2>Agent instructions</h2>
    <div className="settings-actions">
      <button type="button" className="button-muted" disabled={busy} title="Open Chirality's shared AGENTS.md. Changes apply before further work at a safe execution boundary; running agents retain their instructions." onClick={() => void act('open')}>Open AGENTS.md</button>
      <button type="button" className="button-muted" disabled={busy || !state?.modified} title="Restore the bundled instructions and keep a backup of your edits." onClick={() => void act('restore')}>Restore default</button>
    </div>
    {error ? <p role="alert">{error}</p> : null}
  </section>;
}
