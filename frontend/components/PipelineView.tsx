"use client";

import React, { useState } from "react";
import { FileTree } from "./FileTree";
import { ResizableLayout } from "./ResizableLayout";

interface PipelineViewProps {
    family: string;
    selectedVariant: string | null;
    projectRoot: string | null;
}

const AGENT_FILE_MAPPING: Record<string, string> = {
    "TASK_ESTIMATING": "AGENT_ESTIMATING.md",
    "AUDIT_AGENTS": "AGENT_DEPENDENCIES.md",
    "AUDIT_DEPENDENCIES": "AGENT_DEPENDENCIES.md"
};

export function PipelineView({ family, selectedVariant, projectRoot }: PipelineViewProps) {
  const [selectedFile, setSelectedFile] = useState<string | null>(null);

  const fileName = selectedVariant ? (AGENT_FILE_MAPPING[selectedVariant] || `AGENT_${selectedVariant}.md`) : null;
  const autoPrompt = fileName ? `Read agents/${fileName} and prepare to execute the pipeline according to those instructions.` : null;

  return (
    <ResizableLayout
      key={`${family}_${selectedVariant}`}
      agentName={selectedVariant || family}
      sessionId={`pipeline_${family}_${selectedVariant || 'none'}`}
      autoPrompt={autoPrompt}
      selectedFile={selectedFile}
      placeholder="Execute command..."
      projectRoot={projectRoot}
      sidebarContent={() => (
        <>
          <div className="panel-label shrink-0 bg-black/20 flex justify-between items-center px-4 py-3 border-b border-white/5">
              <span className="text-[10px] font-mono tracking-[0.2em] uppercase text-[var(--color-accent-orange)]">Project Directory</span>
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