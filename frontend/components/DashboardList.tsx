"use client";

import React, { useState, useEffect } from "react";

type Deliverable = {
  id: string;
  name: string;
  pkg: string;
  status: "open" | "in-progress" | "checking" | "issued";
  path: string;
};

interface DashboardListProps {
  onSelect: (del: Deliverable) => void;
  projectRoot: string | null;
}

const STATUS_LABELS: Record<Deliverable["status"], string> = {
  open: "Open",
  "in-progress": "In Progress",
  checking: "Checking",
  issued: "Issued",
};

const STATUS_BADGE_CLASSES: Record<Deliverable["status"], string> = {
  open: "text-[var(--color-text-dim)] border-[var(--color-border)] bg-[var(--color-surface-low)]/60",
  "in-progress": "text-[var(--color-guiding)] border-[var(--color-guiding)]/35 bg-[var(--color-guiding)]/10",
  checking: "text-[var(--color-judging)] border-[var(--color-judging)]/35 bg-[var(--color-judging)]/10",
  issued: "text-[var(--color-reviewing)] border-[var(--color-reviewing)]/35 bg-[var(--color-reviewing)]/10",
};

function formatRootLabel(pathValue: string): string {
  const normalized = pathValue.replace(/\/+$/, "");
  if (!normalized) {
    return "/";
  }
  const parts = normalized.split("/").filter(Boolean);
  if (parts.length <= 2) {
    return normalized;
  }
  return `${parts[parts.length - 2]}/${parts[parts.length - 1]}`;
}

export function DashboardList({ onSelect, projectRoot }: DashboardListProps) {
  const [deliverables, setDeliverables] = useState<Deliverable[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!projectRoot) {
      setDeliverables([]);
      setLoading(false);
      return;
    }
    void fetchDeliverables(projectRoot);
  }, [projectRoot]);

  const fetchDeliverables = async (root: string) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/project/deliverables?path=${encodeURIComponent(root)}`);
      const data = await res.json();
      setDeliverables(Array.isArray(data.deliverables) ? data.deliverables : []);
    } catch (e) {
      console.error("Failed to load deliverables", e);
      setDeliverables([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="dashboard-panel ui-panel relative flex h-full w-full max-w-full flex-col gap-4 overflow-hidden p-5 xl:w-[550px]">
      <header className="flex shrink-0 flex-col gap-3 border-b border-[var(--color-border)] pb-3">
        <div className="flex items-center justify-between gap-3">
          <h2 className="ui-type-title text-[1.35rem] font-black tracking-[0.12em] uppercase text-[var(--color-text-main)]">
            Deliverables
          </h2>
          <span className="ui-panel-soft mono rounded-md px-2.5 py-1 text-[10px] font-semibold tracking-[0.14em] uppercase text-[var(--color-text-dim)]">
            COUNT: {deliverables.length}
          </span>
        </div>
        <div className="ui-panel-soft flex items-center gap-2 rounded-md px-3 py-2">
          <span className="ui-type-mono-meta text-[9px] font-black text-[var(--color-accent-orange)] opacity-75">
            Project
          </span>
          <span
            className="mono min-w-0 truncate text-[11px] font-semibold tracking-[0.06em] text-[var(--color-text-main)]/90"
            title={projectRoot || "No project root selected"}
          >
            {projectRoot ? formatRootLabel(projectRoot) : "NOT_SET"}
          </span>
        </div>
        {!projectRoot && (
          <p className="mono text-[10px] font-medium tracking-[0.12em] uppercase text-[var(--color-text-dim)]/85">
            Set root from the shared footer in workbench/pipeline/direct.
          </p>
        )}
      </header>

      <div className="dashboard-list flex min-h-0 flex-1 flex-col gap-2.5 overflow-y-auto pr-2 custom-scrollbar">
        {loading ? (
          <div className="ui-panel-soft flex items-center justify-center gap-2 rounded-lg px-4 py-6 text-center">
            <span className="h-2.5 w-2.5 rounded-full bg-[var(--color-accent-orange)] animate-pulse" aria-hidden />
            <span className="mono text-[11px] font-semibold tracking-[0.12em] uppercase text-[var(--color-text-dim)]">
              Scanning deliverables...
            </span>
          </div>
        ) : deliverables.length === 0 ? (
          <div className="ui-panel-soft rounded-lg px-5 py-6 text-center">
            <p className="mono text-[11px] font-semibold tracking-[0.12em] uppercase text-[var(--color-text-dim)]">
              {projectRoot ? "No deliverables detected." : "Project root not selected."}
            </p>
            <p className="mt-2 text-sm text-[var(--color-text-dim)]/80">
              {projectRoot
                ? "No deliverable folders were found in the current root."
                : "Open workbench, pipeline, or direct and pick a root from the footer."}
            </p>
          </div>
        ) : (
          deliverables.map((del) => (
            <button
              key={del.id}
              type="button"
              onClick={() => onSelect(del)}
              className="ui-focus-ring group flex w-full items-center gap-3 rounded-lg border border-transparent bg-[var(--color-surface-low)]/55 px-4 py-3 text-left transition-all duration-200 hover:border-[var(--color-border-strong)] hover:bg-[var(--color-surface-low)]/85"
              aria-label={`Open ${del.id} ${del.name}`}
            >
              <span className={`del-status-dot status-${del.status}`} aria-hidden />
              <span className="mono min-w-[96px] text-[11px] font-semibold tracking-[0.08em] text-[var(--color-accent-orange)] group-hover:text-[var(--color-text-main)] transition-colors">
                {del.id}
              </span>
              <span className="min-w-0 flex-1 truncate text-[1.02rem] font-semibold text-[var(--color-text-main)]">
                {del.name}
              </span>
              <span className="mono rounded border border-[var(--color-border)] bg-[var(--color-surface-low)]/70 px-1.5 py-0.5 text-[9px] font-medium uppercase tracking-[0.1em] text-[var(--color-text-dim)]">
                {del.pkg.split("_")[0]}
              </span>
              <span
                className={`mono rounded border px-1.5 py-0.5 text-[9px] font-semibold uppercase tracking-[0.1em] ${STATUS_BADGE_CLASSES[del.status]}`}
              >
                {STATUS_LABELS[del.status]}
              </span>
            </button>
          ))
        )}
      </div>
    </section>
  );
}
