"use client";

import React, { useState, useEffect } from "react";
import { SystemNode } from "@/app/api/system/list/route";

interface SystemFileTreeProps {
  onSelect: (path: string) => void;
  className?: string;
}

export function SystemFileTree({ onSelect, className }: SystemFileTreeProps) {
  const [rootNodes, setRootNodes] = useState<SystemNode[]>([]);
  const [currentPath, setCurrentPath] = useState("/");
  const [manualPath, setManualPath] = useState("/");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchDir = async (pathInput: string) => {
    const targetPath = pathInput.trim() || "/";
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/system/list?path=${encodeURIComponent(targetPath)}`);
      const data = await res.json();
      if (!res.ok || data.error) {
        throw new Error(typeof data.error === "string" ? data.error : "Failed to read directory.");
      }
      setRootNodes(Array.isArray(data.nodes) ? data.nodes : []);
      const resolvedCurrent = typeof data.current === "string" && data.current ? data.current : targetPath;
      setCurrentPath(resolvedCurrent);
      setManualPath(resolvedCurrent);
    } catch (e) {
      console.error("Failed to fetch system path:", e);
      setRootNodes([]);
      setError(e instanceof Error ? e.message : "Unable to read directory.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void fetchDir("/");
  }, []);

  const handleManualSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    void fetchDir(manualPath);
  };

  const handleUp = () => {
    const parts = currentPath.split("/").filter(Boolean);
    parts.pop();
    const parent = "/" + parts.join("/");
    void fetchDir(parent || "/");
  };

  const atRoot = currentPath === "/";

  return (
    <div className={`flex h-full min-h-0 flex-col ${className ?? ""}`}>
      <div className="ui-panel-soft mb-2 flex items-center gap-2 rounded-md p-2">
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
            aria-label="System path"
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

      <div className="mb-2 flex items-center gap-2 px-1">
        <span className="ui-type-mono-meta text-[9px] font-semibold text-[var(--color-text-dim)]/80">Current</span>
        <span className="mono min-w-0 truncate text-[10px] text-[var(--color-text-main)]/85" title={currentPath}>
          {currentPath}
        </span>
      </div>

      <div className="ui-panel-soft flex-grow min-h-0 overflow-y-auto rounded-md p-2 custom-scrollbar">
        {loading ? (
          <div className="rounded-md px-3 py-4 text-center">
            <p className="mono text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--color-text-dim)]">
              Loading directory...
            </p>
          </div>
        ) : error ? (
          <div className="rounded-md border border-[var(--color-normative)]/35 bg-[var(--color-normative)]/10 px-3 py-3">
            <p className="mono text-[10px] font-semibold uppercase tracking-[0.1em] text-[var(--color-normative)]">
              Error
            </p>
            <p className="mt-1 text-[11px] leading-relaxed text-[var(--color-text-main)]/85">{error}</p>
          </div>
        ) : rootNodes.length === 0 ? (
          <div className="rounded-md px-3 py-4 text-center">
            <p className="mono text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--color-text-dim)]">
              Directory is empty.
            </p>
          </div>
        ) : (
          <div className="space-y-1">
            {rootNodes.map((node) => (
              <button
                type="button"
                key={node.path}
                className={`ui-focus-ring group flex w-full items-center gap-2 rounded-md border px-2 py-1.5 text-left transition-colors ${
                  node.path === manualPath
                    ? "border-[var(--color-border-strong)] bg-[var(--color-surface-low)] text-[var(--color-text-main)]"
                    : "border-transparent bg-transparent text-[var(--color-text-dim)] hover:border-[var(--color-border)] hover:bg-[var(--color-surface-low)]/80 hover:text-[var(--color-text-main)]"
                }`}
                onClick={() => {
                  setManualPath(node.path);
                  if (node.isDirectory) {
                    void fetchDir(node.path);
                  }
                  onSelect(node.path);
                }}
              >
                <span
                  className={`mono w-4 text-center text-[10px] ${
                    node.isDirectory ? "text-[var(--color-accent-directory)]/80" : "text-[var(--color-text-dim)]/75"
                  }`}
                  aria-hidden
                >
                  {node.isDirectory ? "▸" : "•"}
                </span>
                <span
                  className={`mono min-w-0 flex-1 truncate text-[11px] ${
                    node.isDirectory
                      ? "font-semibold text-[var(--color-accent-directory)]/95 group-hover:text-[var(--color-accent-directory)]"
                      : "text-[var(--color-text-main)]/85"
                  }`}
                  title={node.path}
                >
                  {node.name}
                </span>
                {node.isDirectory && (
                  <span className="mono rounded border border-[var(--color-border)] bg-[var(--color-surface-low)] px-1.5 py-0.5 text-[9px] font-medium tracking-[0.08em] text-[var(--color-text-dim)]">
                    DIR
                  </span>
                )}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
