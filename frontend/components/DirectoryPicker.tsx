"use client";

import React, { useState } from "react";
import { SystemFileTree } from "./SystemFileTree";

interface DirectoryPickerProps {
  onSelect: (path: string) => void;
  onCancel: () => void;
}

export function DirectoryPicker({ onSelect, onCancel }: DirectoryPickerProps) {
  const [selectedPath, setSelectedPath] = useState<string | null>(null);

  const handleConfirm = () => {
    if (selectedPath) {
      onSelect(selectedPath);
    }
  };

  return (
    <div className="fixed inset-0 z-[200] flex items-center justify-center bg-black/72 p-4 backdrop-blur-sm">
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="directory-picker-title"
        className="ui-panel-strong flex h-[min(82vh,720px)] w-[min(92vw,780px)] flex-col overflow-hidden"
      >
        <div className="flex items-start justify-between gap-3 border-b border-[var(--color-border)] bg-[var(--color-surface-panel)]/75 px-5 py-4">
          <div className="min-w-0">
            <p className="ui-type-mono-meta text-[9px] font-semibold text-[var(--color-accent-text)]/75">Workspace</p>
            <h2 id="directory-picker-title" className="text-[1.05rem] font-bold tracking-[0.06em] uppercase text-[var(--color-text-main)]">
              Select Project Directory
            </h2>
            <p className="mt-1 text-[12px] text-[var(--color-text-dim)]/85">
              This root is shared by workbench, pipeline, and direct sessions.
            </p>
          </div>
          <button
            type="button"
            onClick={onCancel}
            className="ui-control ui-focus-ring px-2.5 py-1 text-[11px] font-semibold uppercase tracking-[0.1em]"
            aria-label="Close directory picker"
          >
            Close
          </button>
        </div>

        <div className="flex-grow min-h-0 overflow-hidden bg-[var(--color-surface-sunken)]/55 p-4">
          <SystemFileTree
            onSelect={(path) => setSelectedPath(path)}
            className="h-full"
          />
        </div>

        <div className="flex items-center justify-between gap-3 border-t border-[var(--color-border)] bg-[var(--color-surface-panel)]/75 px-4 py-3">
          <div className="ui-panel-soft flex min-w-0 flex-1 items-center gap-2 rounded-md px-3 py-2">
            <span className="ui-type-mono-meta text-[9px] font-semibold text-[var(--color-accent-text)]/75">
              Selected
            </span>
            <span className="mono min-w-0 truncate text-[10px] text-[var(--color-text-main)]/85" title={selectedPath ?? ""}>
              {selectedPath ?? "Choose a directory from the list."}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={onCancel}
              className="ui-control ui-focus-ring px-3 py-1.5 mono text-[10px] font-semibold uppercase tracking-[0.1em]"
            >
              Cancel
            </button>
            <button
              type="button"
              onClick={handleConfirm}
              disabled={!selectedPath}
              className={`ui-focus-ring px-3 py-1.5 mono text-[10px] font-bold uppercase tracking-[0.12em] ${
                selectedPath
                  ? "ui-button-primary"
                  : "ui-control text-[var(--color-text-dim)]"
              }`}
            >
              Use Directory
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
