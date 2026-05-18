"use client";

import React, { useState } from "react";
import { FileTree } from "./FileTree";
import { ResizableLayout } from "./ResizableLayout";

interface WorkbenchViewProps {
    agentName: string;
    initialPath?: string | null;
    projectRoot: string | null;
    onNavigateHome?: () => void;
    onRootChange?: (path: string) => void;
}

const WORKBENCH_PERSONA_MAPPING: Record<string, { personaId: string; fileName: string }> = {
  "HELP": { personaId: "HELP_HUMAN", fileName: "AGENT_HELP_HUMAN.md" },
  "ORCHESTRATE": { personaId: "ORCHESTRATOR", fileName: "AGENT_ORCHESTRATOR.md" },
  "WORKING_ITEMS": { personaId: "WORKING_ITEMS", fileName: "AGENT_WORKING_ITEMS.md" },
  "AGGREGATE": { personaId: "AGGREGATION", fileName: "AGENT_AGGREGATION.md" },
  "AGENTS": { personaId: "HELPS_HUMANS", fileName: "AGENT_HELPS_HUMANS.md" },
  "DEPENDENCIES": { personaId: "DEPENDENCIES", fileName: "AGENT_DEPENDENCIES.md" },
  "CHANGE": { personaId: "CHANGE", fileName: "AGENT_CHANGE.md" },
  "RECONCILING": { personaId: "RECONCILIATION", fileName: "AGENT_RECONCILIATION.md" },
};

export function WorkbenchView({ agentName, initialPath, projectRoot, onNavigateHome, onRootChange }: WorkbenchViewProps) {
  const [selectedFile, setSelectedFile] = useState<string | null>(initialPath || "README.md");

  const personaConfig = WORKBENCH_PERSONA_MAPPING[agentName];
  const autoPrompt = personaConfig
    ? `Read agents/${personaConfig.fileName} and initialize your persona accordingly. Output your initialization status.`
    : null;

  return (
    <ResizableLayout
      key={agentName}
      agentName={agentName}
      sessionId={`workbench_${agentName}`}
      autoPrompt={autoPrompt}
      harnessMode="workbench"
      personaId={personaConfig?.personaId ?? null}
      selectedFile={selectedFile}
      projectRoot={projectRoot}
      onNavigateHome={onNavigateHome}
      onRootChange={onRootChange}
      sidebarContent={() => (
        <>
          <div className="panel-label shrink-0 ui-panel-soft rounded-none border-t-0 border-x-0 px-4 py-3.5">
            <div className="flex items-center justify-between gap-3">
              <div className="min-w-0">
                <span className="block text-[10px] font-mono uppercase tracking-[0.2em] text-[var(--color-accent-directory)]">
                  Project Directory
                </span>
                <span className="mono mt-1 block truncate text-[9px] uppercase tracking-[0.12em] text-[var(--color-text-dim)]/85">
                  Hex route // git tracked
                </span>
              </div>
              <span className="h-2 w-2 shrink-0 rounded-full bg-green-500 shadow-[0_0_10px_#22c55e]" />
            </div>
          </div>
          
          <div className="flex-grow overflow-y-auto p-2 min-h-0 custom-scrollbar">
              <FileTree 
                  onFileSelect={setSelectedFile} 
                  className="h-full"
                  rootPath={projectRoot}
              />
          </div>
        </>
      )}
    />
  );
}
