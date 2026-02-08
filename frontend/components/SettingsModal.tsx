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
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      // Load API Key from local storage
      const storedKey = localStorage.getItem("anthropic_api_key");
      if (storedKey) setApiKey(storedKey);

      // Load Model from server
      if (projectRoot) {
        setIsLoading(true);
        fetch(`/api/project/config?projectRoot=${encodeURIComponent(projectRoot)}`)
          .then((res) => res.json())
          .then((data) => {
            if (data.model) setModel(data.model);
          })
          .catch((err) => console.error("Failed to load config", err))
          .finally(() => setIsLoading(false));
      }
    }
  }, [isOpen, projectRoot]);

  const handleSave = async () => {
    setIsLoading(true);
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
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="bg-[var(--color-bg-panel)] border border-[var(--color-border)] rounded-lg shadow-2xl w-[400px] p-6 text-sm font-mono text-[var(--color-text-main)] backdrop-blur-xl">
        <h2 className="text-lg font-bold mb-4 text-[var(--color-accent-orange)] tracking-wide uppercase">Settings</h2>

        <div className="space-y-4">
          <div>
            <label className="block text-xs uppercase tracking-widest opacity-60 mb-2">Anthropic API Key</label>
            <input
              type="password"
              className="w-full bg-[var(--color-surface-high)] border border-[var(--color-border)] rounded px-3 py-2 outline-none focus:border-[var(--color-accent-orange)] transition-colors placeholder:text-[var(--color-text-dim)]"
              placeholder="sk-ant-..."
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
            />
            <p className="text-[10px] opacity-40 mt-1">Stored locally in your browser.</p>
          </div>

          <div>
            <label className="block text-xs uppercase tracking-widest opacity-60 mb-2">Global Model (CLAUDE.md)</label>
            <input
              type="text"
              className="w-full bg-[var(--color-surface-high)] border border-[var(--color-border)] rounded px-3 py-2 outline-none focus:border-[var(--color-accent-orange)] transition-colors placeholder:text-[var(--color-text-dim)]"
              placeholder="e.g. sonnet, opus, claude-3-5-sonnet-20240620"
              value={model}
              onChange={(e) => setModel(e.target.value)}
            />
             <p className="text-[10px] opacity-40 mt-1">Applies to all new turns.</p>
          </div>
        </div>

        {status && (
            <div className={`mt-4 text-xs ${status.startsWith("Error") ? "text-red-400" : "text-green-400"}`}>
                {status}
            </div>
        )}

        <div className="flex justify-end gap-3 mt-6">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded hover:bg-[var(--color-surface-mid)] transition-colors text-[var(--color-text-dim)] hover:text-[var(--color-text-main)]"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            disabled={isLoading}
            className="px-4 py-2 bg-[var(--color-accent-orange)]/10 text-[var(--color-accent-orange)] border border-[var(--color-accent-orange)]/20 rounded hover:bg-[var(--color-accent-orange)]/20 transition-all font-bold tracking-wide uppercase disabled:opacity-50"
          >
            {isLoading ? "Saving..." : "Save"}
          </button>
        </div>
      </div>
    </div>
  );
};
