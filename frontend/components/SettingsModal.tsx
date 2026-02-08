"use client";

import React, { useEffect, useState } from "react";

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  projectRoot: string | null;
}

export const SettingsModal: React.FC<SettingsModalProps> = ({ isOpen, onClose, projectRoot }) => {
  const [apiKey, setApiKey] = useState("");
  const [model, setModel] = useState("");
  const [isFetching, setIsFetching] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [status, setStatus] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      setStatus(null);
      // Load API Key from local storage
      const storedKey = localStorage.getItem("anthropic_api_key");
      if (storedKey) setApiKey(storedKey);
      else setApiKey("");

      // Load Model from server
      if (projectRoot) {
        setIsFetching(true);
        fetch(`/api/project/config?projectRoot=${encodeURIComponent(projectRoot)}`)
          .then((res) => res.json())
          .then((data) => {
            if (typeof data.model === "string") setModel(data.model);
            else setModel("");
          })
          .catch((err) => console.error("Failed to load config", err))
          .finally(() => setIsFetching(false));
      } else {
        setModel("");
      }
    }
  }, [isOpen, projectRoot]);

  const handleSave = async () => {
    setIsSaving(true);
    setStatus(null);

    try {
      // Save API Key
      if (apiKey.trim()) {
        localStorage.setItem("anthropic_api_key", apiKey.trim());
      } else {
        localStorage.removeItem("anthropic_api_key");
      }

      // Save Model
      if (projectRoot && model.trim()) {
        const res = await fetch("/api/project/config", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ projectRoot, model: model.trim() }),
        });
        
        if (!res.ok) throw new Error("Failed to save model configuration");
      }

      setStatus("Settings saved successfully.");
      setTimeout(onClose, 1000);
    } catch (error) {
      setStatus(`Error: ${error instanceof Error ? error.message : String(error)}`);
    } finally {
      setIsSaving(false);
    }
  };

  if (!isOpen) return null;

  const statusIsError = Boolean(status?.startsWith("Error"));
  const statusClass = statusIsError
    ? "border-[var(--color-normative)]/35 bg-[var(--color-normative)]/10 text-[var(--color-normative)]"
    : "border-[var(--color-judging)]/35 bg-[var(--color-judging)]/10 text-[var(--color-judging)]";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/65 p-4 backdrop-blur-sm">
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="settings-modal-title"
        className="ui-panel-strong w-[min(92vw,460px)] overflow-hidden"
      >
        <div className="border-b border-[var(--color-border)] bg-[var(--color-surface-high)]/70 px-5 py-4">
          <p className="ui-type-mono-meta text-[9px] font-semibold text-[var(--color-accent-orange)]/75">Configuration</p>
          <h2 id="settings-modal-title" className="text-[1.05rem] font-bold uppercase tracking-[0.08em] text-[var(--color-text-main)]">Settings</h2>
          <p className="mt-1 mono text-[10px] text-[var(--color-text-dim)]">
            ROOT: {projectRoot ?? "NOT_SET"}
          </p>
        </div>

        <div className="space-y-4 px-5 py-4">
          <div>
            <label className="ui-type-mono-meta mb-2 block text-[10px] font-semibold text-[var(--color-text-dim)]/80">
              Anthropic API Key
            </label>
            <input
              type="password"
              className="ui-control ui-focus-ring w-full bg-[var(--color-surface-high)] px-3 py-2 text-sm text-[var(--color-text-main)] placeholder:text-[var(--color-text-dim)]"
              placeholder="sk-ant-..."
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
            />
            <p className="mt-1 text-[11px] text-[var(--color-text-dim)]/75">Stored locally in your browser.</p>
          </div>

          <div>
            <label className="ui-type-mono-meta mb-2 block text-[10px] font-semibold text-[var(--color-text-dim)]/80">
              Global Model (CLAUDE.md)
            </label>
            <input
              type="text"
              className="ui-control ui-focus-ring w-full bg-[var(--color-surface-high)] px-3 py-2 text-sm text-[var(--color-text-main)] placeholder:text-[var(--color-text-dim)]"
              placeholder="e.g. sonnet, opus, claude-3-5-sonnet-20240620"
              value={model}
              onChange={(e) => setModel(e.target.value)}
              disabled={!projectRoot || isFetching}
            />
            {!projectRoot ? (
              <p className="mt-1 text-[11px] text-[var(--color-text-dim)]/75">
                Select a project root from the shared footer before saving model config.
              </p>
            ) : (
              <p className="mt-1 text-[11px] text-[var(--color-text-dim)]/75">Applies to all new turns.</p>
            )}
          </div>

          {status && (
            <div className={`rounded-md border px-3 py-2 text-[11px] ${statusClass}`}>
              {status}
            </div>
          )}
        </div>

        <div className="flex items-center justify-end gap-2 border-t border-[var(--color-border)] bg-[var(--color-surface-high)]/60 px-5 py-3">
          <button
            onClick={onClose}
            className="ui-control ui-focus-ring px-3 py-1.5 mono text-[10px] font-semibold uppercase tracking-[0.1em]"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            disabled={isSaving || isFetching}
            className={`ui-focus-ring px-3 py-1.5 mono text-[10px] font-bold uppercase tracking-[0.12em] ${
              isSaving || isFetching ? "ui-control text-[var(--color-text-dim)]" : "ui-button-primary"
            }`}
          >
            {isSaving ? "Saving..." : isFetching ? "Loading..." : "Save"}
          </button>
        </div>
      </div>
    </div>
  );
};
