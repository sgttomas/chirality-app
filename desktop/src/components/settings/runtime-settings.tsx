'use client';

import React, { useMemo, type ChangeEvent } from 'react';
import { useRuntimeSettingsController, type RuntimeSettingsViewProps } from './runtime-settings-controller';
export type { RuntimeSettingsViewProps, RuntimeModel, RuntimeResidencyStatus } from './runtime-settings-controller';

export function RuntimeSettings({ controller }: { controller?: RuntimeSettingsViewProps } = {}): JSX.Element {
  return controller ? <RuntimeSettingsView {...controller} /> : <StandaloneRuntimeSettings />;
}

function StandaloneRuntimeSettings(): JSX.Element {
  const controller = useRuntimeSettingsController();
  return <RuntimeSettingsView {...controller} />;
}

/**
 * Local-model (oMLX) residency controls for the compatibility shell. The
 * Runtime service itself is App-owned and has no install, start, stop or
 * uninstall controls (D-GOV-43); its state is shown by `RuntimeStatus`.
 */
export function RuntimeSettingsView({
  bridgeAvailable,
  residency,
  selectedModel,
  busyAction,
  error,
  onRefresh,
  onSelectedModelChange,
  onActivateModel,
  showLocalModels = true
}: RuntimeSettingsViewProps & { showLocalModels?: boolean }): JSX.Element {
  const selectableModels = useMemo(
    () =>
      residency?.models.filter(
        (model) => model.kind === 'llm' || model.kind === 'unknown'
      ) ?? [],
    [residency]
  );
  const selected = selectableModels.find((model) => model.id === selectedModel);
  const modelBusy =
    busyAction === 'models' ||
    residency?.phase === 'DRAINING' ||
    residency?.phase === 'UNLOADING' ||
    residency?.phase === 'LOADING';

  return (
    <section className="runtime-settings" aria-labelledby="runtime-settings-title">
      <h3 className="api-key-settings-title" id="runtime-settings-title">
        Runtime
      </h3>

      {bridgeAvailable ? (
        <>
          {showLocalModels ? (
            <div className="runtime-model-controls">
              <p className="runtime-model-status">
                Residency: <strong>{residency?.phase ?? 'Checking'}</strong>
                {residency?.managedModelId
                  ? ` · ${residency.managedModelId}`
                  : ' · no managed model'}
                {residency ? ` · ${residency.activeTurns} active turn(s)` : ''}
              </p>
              <div className="runtime-control-row">
                <select
                  aria-label="Exact oMLX model"
                  value={selectedModel}
                  onChange={(event: ChangeEvent<HTMLSelectElement>) =>
                    onSelectedModelChange(event.target.value)
                  }
                  disabled={modelBusy || selectableModels.length === 0}
                >
                  {selectableModels.length === 0 ? (
                    <option value="">No oMLX LLMs reported</option>
                  ) : null}
                  {selectableModels.map((model) => (
                    <option key={model.id} value={model.id}>
                      {model.id}
                      {model.loaded ? ' (loaded)' : ''}
                    </option>
                  ))}
                </select>
                <button
                  type="button"
                  onClick={onActivateModel}
                  disabled={
                    modelBusy ||
                    !selectedModel ||
                    selected?.id === residency?.managedModelId
                  }
                >
                  {busyAction === 'models' ? 'Activating...' : 'Activate Explicitly'}
                </button>
                <button
                  type="button"
                  className="button-muted"
                  onClick={onRefresh}
                  disabled={busyAction !== null}
                >
                  Refresh
                </button>
              </div>
              <p className="api-key-hint">
                Activation never occurs automatically. A switch drains active local turns before
                unloading the managed model.
              </p>
            </div>
          ) : (
            <p className="api-key-hint">The Runtime service is managed by Chirality Desktop.</p>
          )}
        </>
      ) : (
        <p className="api-key-hint">
          Runtime controls are available only in Chirality Desktop.
        </p>
      )}

      {error ? <p className="api-key-error">{error}</p> : null}
    </section>
  );
}
