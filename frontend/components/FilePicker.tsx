"use client";

import React, { useState, useEffect, useCallback } from "react";
import { ATTACHMENT_EXTENSIONS } from "@/lib/harness/types";

interface SystemNode {
  name: string;
  path: string;
  isDirectory: boolean;
  hasChildren?: boolean;
}

interface FilePickerProps {
  onSelect: (paths: string[]) => void;
  onCancel: () => void;
  startPath?: string | null;
  existingPaths?: string[];
}

function isAllowedExtension(name: string): boolean {
  const lastDot = name.lastIndexOf(".");
  if (lastDot < 0) return false;
  return ATTACHMENT_EXTENSIONS.includes(name.slice(lastDot).toLowerCase());
}

export function FilePicker({ onSelect, onCancel, startPath, existingPaths }: FilePickerProps) {
  const initialPath = startPath || "/";
  const [nodes, setNodes] = useState<SystemNode[]>([]);
  const [currentPath, setCurrentPath] = useState(initialPath);
  const [manualPath, setManualPath] = useState(initialPath);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selected, setSelected] = useState<Set<string>>(() => new Set(existingPaths ?? []));

  const fetchDir = useCallback(async (pathInput: string) => {
    const targetPath = pathInput.trim() || "/";
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/system/list?path=${encodeURIComponent(targetPath)}`);
      const data = await res.json();
      if (!res.ok || data.error) {
        throw new Error(typeof data.error === "string" ? data.error : "Failed to read directory.");
      }
      setNodes(Array.isArray(data.nodes) ? data.nodes : []);
      const resolved = typeof data.current === "string" && data.current ? data.current : targetPath;
      setCurrentPath(resolved);
      setManualPath(resolved);
    } catch (e) {
      setNodes([]);
      setError(e instanceof Error ? e.message : "Unable to read directory.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void fetchDir(initialPath);
  }, [initialPath, fetchDir]);

  const handleUp = () => {
    const parts = currentPath.split("/").filter(Boolean);
    parts.pop();
    void fetchDir("/" + parts.join("/") || "/");
  };

  const handleManualSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    void fetchDir(manualPath);
  };

  const toggleFile = (filePath: string) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(filePath)) {
        next.delete(filePath);
      } else {
        next.add(filePath);
      }
      return next;
    });
  };

  const handleConfirm = () => {
    if (selected.size > 0) {
      onSelect(Array.from(selected));
    }
  };

  const atRoot = currentPath === "/";
  const selectedCount = selected.size;

  return (
    <div className="fixed inset-0 z-[200] flex items-center justify-center bg-black/72 p-4 backdrop-blur-sm">
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="file-picker-title"
        className="ui-panel-strong flex h-[min(82vh,720px)] w-[min(92vw,780px)] flex-col overflow-hidden"
      >
        {/* Header */}
        <div className="flex items-start justify-between gap-3 border-b border-[var(--color-border)] bg-[var(--color-surface-panel)]/75 px-5 py-4">
          <div className="min-w-0">
            <p className="ui-type-mono-meta text-[9px] font-semibold text-[var(--color-accent-text)]/75">Attachments</p>
            <h2 id="file-picker-title" className="text-[1.05rem] font-bold tracking-[0.06em] uppercase text-[var(--color-text-main)]">
              Attach Files
            </h2>
            <p className="mt-1 text-[12px] text-[var(--color-text-dim)]/85">
              Select images or documents to include with your message.
            </p>
          </div>
          <button
            type="button"
            onClick={onCancel}
            className="ui-control ui-focus-ring px-2.5 py-1 text-[11px] font-semibold uppercase tracking-[0.1em]"
            aria-label="Close file picker"
          >
            Close
          </button>
        </div>

        {/* Navigation bar */}
        <div className="border-b border-[var(--color-border)]/50 bg-[var(--color-surface-sunken)]/55 px-4 py-2.5">
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleUp}
              disabled={atRoot || loading}
              className="ui-control ui-focus-ring px-2 py-1 mono text-[10px] font-semibold uppercase tracking-[0.1em]"
              title="Go to parent directory"
            >
              Up
            </button>
            <form onSubmit={handleManualSubmit} className="flex-grow">
              <input
                type="text"
                value={manualPath}
                onChange={(e) => setManualPath(e.target.value)}
                className="ui-control ui-focus-ring w-full bg-[var(--color-surface-high)] px-2 py-1 mono text-[10px] text-[var(--color-text-main)]"
                placeholder="/"
                aria-label="Directory path"
              />
            </form>
            <button
              type="button"
              onClick={() => void fetchDir(manualPath)}
              disabled={loading}
              className="ui-control ui-focus-ring px-2 py-1 mono text-[10px] font-semibold uppercase tracking-[0.1em] text-[var(--color-accent-directory)] border-[var(--color-accent-directory)]/30 bg-[var(--color-accent-directory)]/10 hover:bg-[var(--color-accent-directory)]/16"
            >
              Open
            </button>
          </div>
          <div className="mt-1.5 flex items-center gap-2 px-1">
            <span className="ui-type-mono-meta text-[9px] font-semibold text-[var(--color-text-dim)]/80">Current</span>
            <span className="mono min-w-0 truncate text-[10px] text-[var(--color-text-main)]/85" title={currentPath}>
              {currentPath}
            </span>
          </div>
        </div>

        {/* File listing */}
        <div className="flex-grow min-h-0 overflow-y-auto bg-[var(--color-surface-sunken)]/55 p-3 custom-scrollbar">
          {loading ? (
            <div className="rounded-md px-3 py-4 text-center">
              <p className="mono text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--color-text-dim)]">
                Loading directory...
              </p>
            </div>
          ) : error ? (
            <div className="rounded-md border border-[var(--color-normative)]/35 bg-[var(--color-normative)]/10 px-3 py-3">
              <p className="mono text-[10px] font-semibold uppercase tracking-[0.1em] text-[var(--color-normative)]">Error</p>
              <p className="mt-1 text-[11px] leading-relaxed text-[var(--color-text-main)]/85">{error}</p>
            </div>
          ) : nodes.length === 0 ? (
            <div className="rounded-md px-3 py-4 text-center">
              <p className="mono text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--color-text-dim)]">
                Directory is empty.
              </p>
            </div>
          ) : (
            <div className="space-y-1">
              {nodes.map((node) => {
                const allowed = !node.isDirectory && isAllowedExtension(node.name);
                const isSelected = selected.has(node.path);
                const dimmed = !node.isDirectory && !allowed;

                return (
                  <button
                    type="button"
                    key={node.path}
                    disabled={dimmed}
                    className={`ui-focus-ring group flex w-full items-center gap-2 rounded-md border px-2 py-1.5 text-left transition-colors ${
                      isSelected
                        ? "border-[var(--color-accent-text)]/50 bg-[var(--color-accent-text)]/10 text-[var(--color-text-main)]"
                        : dimmed
                          ? "cursor-not-allowed border-transparent opacity-35"
                          : node.isDirectory
                            ? "border-transparent bg-transparent text-[var(--color-text-dim)] hover:border-[var(--color-border)] hover:bg-[var(--color-surface-low)]/80 hover:text-[var(--color-text-main)]"
                            : "border-transparent bg-transparent text-[var(--color-text-dim)] hover:border-[var(--color-border)] hover:bg-[var(--color-surface-low)]/80 hover:text-[var(--color-text-main)]"
                    }`}
                    onClick={() => {
                      if (node.isDirectory) {
                        void fetchDir(node.path);
                      } else if (allowed) {
                        toggleFile(node.path);
                      }
                    }}
                  >
                    {/* Selection indicator / icon */}
                    <span
                      className={`mono w-4 text-center text-[10px] ${
                        node.isDirectory
                          ? "text-[var(--color-accent-directory)]/80"
                          : isSelected
                            ? "text-[var(--color-accent-text)]"
                            : "text-[var(--color-text-dim)]/75"
                      }`}
                      aria-hidden
                    >
                      {node.isDirectory ? "▸" : isSelected ? "✓" : "•"}
                    </span>

                    {/* Name */}
                    <span
                      className={`mono min-w-0 flex-1 truncate text-[11px] ${
                        node.isDirectory
                          ? "font-semibold text-[var(--color-accent-directory)]/95 group-hover:text-[var(--color-accent-directory)]"
                          : isSelected
                            ? "font-semibold text-[var(--color-text-main)]"
                            : "text-[var(--color-text-main)]/85"
                      }`}
                      title={node.path}
                    >
                      {node.name}
                    </span>

                    {/* Badges */}
                    {node.isDirectory ? (
                      <span className="mono rounded border border-[var(--color-border)] bg-[var(--color-surface-low)] px-1.5 py-0.5 text-[9px] font-medium tracking-[0.08em] text-[var(--color-text-dim)]">
                        DIR
                      </span>
                    ) : allowed ? (
                      <span className={`mono rounded border px-1.5 py-0.5 text-[9px] font-medium uppercase tracking-[0.08em] ${
                        isSelected
                          ? "border-[var(--color-accent-text)]/30 bg-[var(--color-accent-text)]/10 text-[var(--color-accent-text)]"
                          : "border-[var(--color-border)] bg-[var(--color-surface-low)] text-[var(--color-text-dim)]"
                      }`}>
                        {node.name.slice(node.name.lastIndexOf(".") + 1).toUpperCase()}
                      </span>
                    ) : null}
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between gap-3 border-t border-[var(--color-border)] bg-[var(--color-surface-panel)]/75 px-4 py-3">
          <div className="ui-panel-soft flex min-w-0 flex-1 items-center gap-2 rounded-md px-3 py-2">
            <span className="ui-type-mono-meta text-[9px] font-semibold text-[var(--color-accent-text)]/75">
              Selected
            </span>
            <span className="mono min-w-0 truncate text-[10px] text-[var(--color-text-main)]/85">
              {selectedCount === 0
                ? "Click files to select them."
                : `${selectedCount} file${selectedCount !== 1 ? "s" : ""} selected`}
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
              disabled={selectedCount === 0}
              className={`ui-focus-ring px-3 py-1.5 mono text-[10px] font-bold uppercase tracking-[0.12em] ${
                selectedCount > 0
                  ? "ui-button-primary"
                  : "ui-control text-[var(--color-text-dim)]"
              }`}
            >
              {selectedCount > 0 ? `Attach ${selectedCount} File${selectedCount !== 1 ? "s" : ""}` : "Attach Files"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
