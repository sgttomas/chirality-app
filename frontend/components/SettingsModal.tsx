"use client";

import React, { useEffect, useState } from "react";
import type { DesktopUpdateCheckResult } from "@/types/desktop-update";

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  projectRoot: string | null;
  toolkitSidebarEnabled: boolean;
  onToolkitSidebarEnabledChange: (enabled: boolean) => void;
}

export const SettingsModal: React.FC<SettingsModalProps> = ({
  isOpen,
  onClose,
  projectRoot,
  toolkitSidebarEnabled,
  onToolkitSidebarEnabledChange,
}) => {
  const [apiKey, setApiKey] = useState("");
  const [model, setModel] = useState("");
  const [toolkitEnabled, setToolkitEnabled] = useState(false);
  const [instructionRoot, setInstructionRoot] = useState<string | null>(null);
  const [instructionWritable, setInstructionWritable] = useState(true);
  const [isFetching, setIsFetching] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [status, setStatus] = useState<string | null>(null);
  const [isCheckingUpdate, setIsCheckingUpdate] = useState(false);
  const [isOpeningDownload, setIsOpeningDownload] = useState(false);
  const [updateResult, setUpdateResult] = useState<DesktopUpdateCheckResult | null>(null);

  useEffect(() => {
    if (isOpen) {
      setStatus(null);
      setUpdateResult(null);
      // Load API Key from local storage
      const storedKey = localStorage.getItem("anthropic_api_key");
      if (storedKey) setApiKey(storedKey);
      else setApiKey("");
      setToolkitEnabled(toolkitSidebarEnabled);

      // Load Model from server
      setIsFetching(true);
      fetch("/api/project/config")
        .then((res) => res.json())
        .then((data) => {
          if (typeof data.model === "string") {
            setModel(data.model);
          } else {
            setModel("");
          }

          setInstructionRoot(typeof data.instructionRoot === "string" ? data.instructionRoot : null);
          setInstructionWritable(Boolean(data.writable));
        })
        .catch((err) => {
          console.error("Failed to load config", err);
          setInstructionRoot(null);
          setInstructionWritable(false);
        })
        .finally(() => setIsFetching(false));
    }
  }, [isOpen, toolkitSidebarEnabled]);

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
      if (model.trim()) {
        const res = await fetch("/api/project/config", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ model: model.trim() }),
        });
        
        if (!res.ok) throw new Error("Failed to save model configuration");
      }

      onToolkitSidebarEnabledChange(toolkitEnabled);
      setStatus("Settings saved successfully.");
      setTimeout(onClose, 1000);
    } catch (error) {
      setStatus(`Error: ${error instanceof Error ? error.message : String(error)}`);
    } finally {
      setIsSaving(false);
    }
  };

  const handleCheckForUpdates = async () => {
    if (!window.chiralityDesktop) {
      setUpdateResult({
        ok: false,
        currentVersion: "unknown",
        latestVersion: null,
        latestTag: null,
        updateAvailable: false,
        downloadUrl: "https://github.com/sgttomas/chirality-app/releases/latest",
        publishedAt: null,
        error: "Update checks are only available in the desktop app build.",
      });
      return;
    }

    setIsCheckingUpdate(true);
    try {
      const result = await window.chiralityDesktop.checkForUpdates();
      setUpdateResult(result);
    } catch (error) {
      setUpdateResult({
        ok: false,
        currentVersion: "unknown",
        latestVersion: null,
        latestTag: null,
        updateAvailable: false,
        downloadUrl: "https://github.com/sgttomas/chirality-app/releases/latest",
        publishedAt: null,
        error: error instanceof Error ? error.message : "Failed to check for updates.",
      });
    } finally {
      setIsCheckingUpdate(false);
    }
  };

  const handleOpenDownload = async () => {
    const downloadUrl = updateResult?.downloadUrl ?? "https://github.com/sgttomas/chirality-app/releases/latest";
    if (!window.chiralityDesktop) {
      window.open(downloadUrl, "_blank", "noopener,noreferrer");
      return;
    }

    setIsOpeningDownload(true);
    try {
      await window.chiralityDesktop.openDownloadPage(downloadUrl);
    } finally {
      setIsOpeningDownload(false);
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
          <p className="ui-type-mono-meta text-[9px] font-semibold text-[var(--color-accent-text)]/75">Configuration</p>
          <h2 id="settings-modal-title" className="text-[1.05rem] font-bold uppercase tracking-[0.08em] text-[var(--color-text-main)]">Settings</h2>
          <p className="mt-1 mono text-[10px] text-[var(--color-text-dim)]">
            PROJECT ROOT: {projectRoot ?? "NOT_SET"}
          </p>
          <p className="mono text-[10px] text-[var(--color-text-dim)]">
            INSTRUCTION ROOT: {instructionRoot ?? "UNRESOLVED"}
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
              disabled={isFetching || !instructionWritable}
            />
            {!instructionWritable ? (
              <p className="mt-1 text-[11px] text-[var(--color-text-dim)]/75">
                Instruction root is read-only. Model changes must ship through a formal release.
              </p>
            ) : (
              <p className="mt-1 text-[11px] text-[var(--color-text-dim)]/75">
                Applies to all new turns and all project roots.
              </p>
            )}
          </div>

          <div>
            <label className="ui-type-mono-meta mb-2 block text-[10px] font-semibold text-[var(--color-text-dim)]/80">
              App Updates
            </label>
            <div className="flex flex-wrap items-center gap-2">
              <button
                type="button"
                onClick={handleCheckForUpdates}
                disabled={isCheckingUpdate}
                className={`ui-focus-ring px-3 py-1.5 mono text-[10px] font-bold uppercase tracking-[0.12em] ${
                  isCheckingUpdate ? "ui-control text-[var(--color-text-dim)]" : "ui-button-primary"
                }`}
              >
                {isCheckingUpdate ? "Checking..." : "Check for updates"}
              </button>

              {updateResult && (
                <button
                  type="button"
                  onClick={handleOpenDownload}
                  disabled={isOpeningDownload}
                  className="ui-control ui-focus-ring px-3 py-1.5 mono text-[10px] font-semibold uppercase tracking-[0.1em] text-[var(--color-accent-text)]"
                >
                  {isOpeningDownload ? "Opening..." : "Open download page"}
                </button>
              )}
            </div>

            {updateResult ? (
              <div className="mt-2 rounded-md border border-[var(--color-border)]/70 bg-[var(--color-surface-high)]/45 px-3 py-2 text-[11px] text-[var(--color-text-dim)]/90">
                {updateResult.ok ? (
                  <>
                    <p>Current: v{updateResult.currentVersion}</p>
                    <p>Latest: {updateResult.latestTag ?? "unknown"}</p>
                    <p className={updateResult.updateAvailable ? "text-[var(--color-accent-text)]" : ""}>
                      {updateResult.updateAvailable ? "Update available." : "You are up to date."}
                    </p>
                  </>
                ) : (
                  <p className="text-[var(--color-normative)]">{updateResult.error ?? "Update check failed."}</p>
                )}
              </div>
            ) : (
              <p className="mt-1 text-[11px] text-[var(--color-text-dim)]/75">
                Checks GitHub Releases and compares with the installed app version.
              </p>
            )}
          </div>

          <div>
            <label className="ui-type-mono-meta mb-2 block text-[10px] font-semibold text-[var(--color-text-dim)]/80">
              UI Panels
            </label>
            <label className="ui-control ui-focus-ring flex items-center justify-between gap-3 bg-[var(--color-surface-high)]/45 px-3 py-2">
              <span className="text-[12px] text-[var(--color-text-main)]">Show Tool Kit sidebar</span>
              <input
                type="checkbox"
                checked={toolkitEnabled}
                onChange={(event) => setToolkitEnabled(event.target.checked)}
                className="h-4 w-4 accent-[var(--color-accent-orange)]"
              />
            </label>
            <p className="mt-1 text-[11px] text-[var(--color-text-dim)]/75">
              When off, the Tool Kit panel is hidden from chat sessions.
            </p>
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
