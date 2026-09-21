'use client';

import { useMemo, useState, type FormEvent } from 'react';
import { useToolkit } from '../workspace/toolkit-provider';

export function OperatorToolkitPanel(): JSX.Element {
  const {
    storageWarning,
    dismissStorageWarning,
    values,
    updateValues,
    resetValues,
    presets,
    selectedPresetId,
    selectPreset,
    applySelectedPreset,
    savePreset,
    deleteSelectedPreset,
    optsPayload
  } = useToolkit();

  const [presetName, setPresetName] = useState('');
  const [presetError, setPresetError] = useState<string | null>(null);

  const payloadPreview = useMemo(() => {
    if (!optsPayload) {
      return 'No explicit opts set. Runtime fallback chains will apply.';
    }
    return JSON.stringify({ opts: optsPayload }, null, 2);
  }, [optsPayload]);

  function submitPreset(event: FormEvent<HTMLFormElement>): void {
    event.preventDefault();
    const saved = savePreset(presetName);
    if (!saved) {
      setPresetError('Preset name is required.');
      return;
    }
    setPresetName('');
    setPresetError(null);
  }

  const selectedPresetExists = Boolean(
    selectedPresetId && presets.some((preset) => preset.id === selectedPresetId)
  );

  return (
    <aside className="panel panel--toolkit">
      <header className="panel-header">
        <h2>Tool Kit</h2>
        <p className="chat-meta">Local, non-authoritative opts and presets.</p>
      </header>

      <div className="panel-body toolkit-body">
        {storageWarning ? (
          <div className="toolkit-warning" role="status" aria-live="polite">
            <p>{storageWarning}</p>
            <button type="button" className="button-muted" onClick={dismissStorageWarning}>
              Dismiss
            </button>
          </div>
        ) : null}

        <label>
          `opts.tools` (comma or newline separated)
          <textarea
            value={values.tools}
            onChange={(event) => {
              updateValues({ tools: event.target.value });
            }}
            rows={3}
            placeholder="bash, read_file"
          />
        </label>

        <label>
          `opts.maxTurns`
          <input
            value={values.maxTurns}
            type="number"
            min={1}
            onChange={(event) => {
              updateValues({ maxTurns: event.target.value });
            }}
            placeholder="6"
          />
        </label>

        <label className="toolkit-checkbox">
          <input
            type="checkbox"
            checked={values.includeSubagentGovernance}
            onChange={(event) => {
              updateValues({ includeSubagentGovernance: event.target.checked });
            }}
          />
          Include `opts.subagentGovernance`
        </label>

        {values.includeSubagentGovernance ? (
          <section className="toolkit-subagent">
            <label className="toolkit-checkbox">
              <input
                type="checkbox"
                checked={values.contextSealed}
                onChange={(event) => {
                  updateValues({ contextSealed: event.target.checked });
                }}
              />
              `contextSealed`
            </label>
            <label className="toolkit-checkbox">
              <input
                type="checkbox"
                checked={values.pipelineRunApproved}
                onChange={(event) => {
                  updateValues({ pipelineRunApproved: event.target.checked });
                }}
              />
              `pipelineRunApproved`
            </label>
            <label>
              `approvalRef`
              <input
                value={values.approvalRef}
                onChange={(event) => {
                  updateValues({ approvalRef: event.target.value });
                }}
                placeholder="approval-sha-or-record-id"
              />
            </label>
          </section>
        ) : null}

        <div className="toolkit-actions">
          <button type="button" className="button-muted" onClick={resetValues}>
            Reset opts
          </button>
        </div>

        <section className="toolkit-presets">
          <h3>Local Presets</h3>
          <form onSubmit={submitPreset} className="toolkit-preset-form">
            <input
              value={presetName}
              onChange={(event) => {
                setPresetName(event.target.value);
                if (presetError) {
                  setPresetError(null);
                }
              }}
              placeholder="Preset name"
            />
            <button type="submit">Save</button>
          </form>
          {presetError ? <p className="panel-error">{presetError}</p> : null}
          <label>
            Saved presets
            <select
              value={selectedPresetId ?? ''}
              onChange={(event) => {
                selectPreset(event.target.value);
              }}
            >
              <option value="">Select preset</option>
              {presets.map((preset) => (
                <option key={preset.id} value={preset.id}>
                  {preset.name}
                </option>
              ))}
            </select>
          </label>
          <div className="toolkit-actions">
            <button
              type="button"
              className="button-muted"
              onClick={applySelectedPreset}
              disabled={!selectedPresetExists}
            >
              Apply
            </button>
            <button
              type="button"
              className="button-muted"
              onClick={deleteSelectedPreset}
              disabled={!selectedPresetExists}
            >
              Delete
            </button>
          </div>
        </section>

        <section className="toolkit-payload-preview">
          <h3>Turn Payload Preview</h3>
          <pre>{payloadPreview}</pre>
        </section>
      </div>
    </aside>
  );
}
