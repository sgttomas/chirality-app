"use client";

import React, { useState } from "react";
import { FileTree } from "./FileTree";
import { ResizableLayout } from "./ResizableLayout";

interface WorkbenchViewProps {
    agentName: string;
    initialPath?: string | null;
    projectRoot: string | null;
}

const PERSONA_FILE_MAPPING: Record<string, string> = {
    "DECOMP": "AGENT_PROJECT_DECOMP.md",
    "ORCHESTRATE": "AGENT_ORCHESTRATOR.md",
    "WORKING_ITEMS": "AGENT_WORKING_ITEMS.md",
    "AGGREGATE": "AGENT_AGGREGATION.md",
    "HELP": "AGENT_HELP_HUMAN.md",
    "AGENTS": "AGENT_HELPS_HUMANS.md",
    "CHANGE": "AGENT_CHANGE.md",
    "DEPENDENCIES": "AGENT_DEPENDENCIES.md",
    "RECONCILING": "AGENT_RECONCILIATION.md"
};

export function WorkbenchView({ agentName, initialPath, projectRoot }: WorkbenchViewProps) {
  const [selectedFile, setSelectedFile] = useState<string | null>(initialPath || "README.md");

  const fileName = PERSONA_FILE_MAPPING[agentName];
  const autoPrompt = fileName ? `Read agents/${fileName} and initialize your persona accordingly. Output your initialization status.` : null;

  return (
    <ResizableLayout
      key={agentName}
      agentName={agentName}
      sessionId={`workbench_${agentName}`}
      autoPrompt={autoPrompt}
      selectedFile={selectedFile}
      projectRoot={projectRoot}
      sidebarContent={() => (
        <>
          <div className="panel-label shrink-0 flex justify-between items-center bg-black/20 p-4 border-b border-white/5">
              <span className="text-[10px] font-mono uppercase tracking-[0.2em] text-[var(--color-accent-orange)]">Project Directory</span>
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
