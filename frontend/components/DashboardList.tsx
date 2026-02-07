"use client";

import React, { useState, useEffect } from "react";
import { DirectoryPicker } from "./DirectoryPicker";

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
    onRootChange: (path: string) => void;
}

export function DashboardList({ onSelect, projectRoot, onRootChange }: DashboardListProps) {
  const [deliverables, setDeliverables] = useState<Deliverable[]>([]);
  const [showPicker, setShowPicker] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
      if (projectRoot) {
          fetchDeliverables(projectRoot);
      }
  }, [projectRoot]);

  const fetchDeliverables = async (root: string) => {
      setLoading(true);
      try {
          const res = await fetch(`/api/project/deliverables?path=${encodeURIComponent(root)}`);
          const data = await res.json();
          if (data.deliverables) {
              setDeliverables(data.deliverables);
          }
      } catch (e) {
          console.error("Failed to load deliverables", e);
      } finally {
          setLoading(false);
      }
  };

  const handleRootSelect = (path: string) => {
      onRootChange(path);
      setShowPicker(false);
      // fetchDeliverables will be triggered by useEffect when prop updates
  };

  return (
    <div className="dashboard-panel glass w-[550px] flex flex-col p-6 gap-5 h-full relative">
      {showPicker && (
          <DirectoryPicker 
            onSelect={handleRootSelect}
            onCancel={() => setShowPicker(false)}
          />
      )}

      <div className="dashboard-title flex-col gap-2 !items-start">
        <div className="flex justify-between items-center w-full">
            <span>Deliverables</span>
            <span className="mono text-sm text-[var(--color-text-dim)]">
            COUNT: {deliverables.length}
            </span>
        </div>
        <div className="flex items-center gap-2 w-full">
            <span className="text-[10px] font-mono text-[var(--color-text-dim)] uppercase tracking-widest">Project:</span>
            <button 
                onClick={() => setShowPicker(true)}
                className="text-[10px] font-mono text-[var(--color-accent-orange)] bg-[var(--color-accent-orange)]/10 px-2 py-1 rounded hover:bg-[var(--color-accent-orange)]/20 truncate max-w-[350px]"
                title={projectRoot || "Select Root"}
            >
                {projectRoot ? projectRoot.split("/").slice(-2).join("/") : "SELECT_ROOT_DIRECTORY"}
            </button>
        </div>
      </div>

      <div className="dashboard-list flex-grow overflow-y-auto flex flex-col gap-3 pr-2 custom-scrollbar">
        {loading ? (
            <div className="p-10 text-center opacity-50 font-mono text-sm animate-pulse">Scanning filesystem...</div>
        ) : deliverables.length === 0 ? (
            <div className="p-10 text-center opacity-30 font-mono text-sm italic">
                {projectRoot ? "No deliverables found in this path." : "Select a project root to begin."}
            </div>
        ) : (
            deliverables.map((del) => (
            <div key={del.id} className="deliverable-card glass group" onClick={() => onSelect(del)}>
                <div className={`del-status-dot status-${del.status}`}></div>
                <div className="del-id group-hover:text-white transition-colors">{del.id}</div>
                <div className="del-name truncate">{del.name}</div>
                <div className="text-[9px] font-mono text-[var(--color-text-dim)] border border-white/10 px-1.5 py-0.5 rounded opacity-50">{del.pkg.split("_")[0]}</div>
            </div>
            ))
        )}
      </div>
    </div>
  );
}
