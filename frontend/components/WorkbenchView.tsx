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
    "DECOMP": { personaId: "PROJECT_DECOMP", fileName: "AGENT_PROJECT_DECOMP.md" },
    "ORCHESTRATE": { personaId: "ORCHESTRATOR", fileName: "AGENT_ORCHESTRATOR.md" },
    "WORKING_ITEMS": { personaId: "WORKING_ITEMS", fileName: "AGENT_WORKING_ITEMS.md" },
    "AGGREGATE": { personaId: "AGGREGATION", fileName: "AGENT_AGGREGATION.md" },
    "HELP": { personaId: "HELP_HUMAN", fileName: "AGENT_HELP_HUMAN.md" },
    "AGENTS": { personaId: "HELPS_HUMANS", fileName: "AGENT_HELPS_HUMANS.md" },
    "CHANGE": { personaId: "CHANGE", fileName: "AGENT_CHANGE.md" },
    "DEPENDENCIES": { personaId: "DEPENDENCIES", fileName: "AGENT_DEPENDENCIES.md" },
    "RECONCILING": { personaId: "RECONCILIATION", fileName: "AGENT_RECONCILIATION.md" }
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
          <div className="panel-label shrink-0 flex justify-between items-center bg-[var(--color-surface-mid)] p-4 border-b border-[var(--color-border)]">
              <span className="text-[10px] font-mono uppercase tracking-[0.2em] text-[var(--color-applying)]">Project Directory</span>
              <span className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_10px_#22c55e]"></span>
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
