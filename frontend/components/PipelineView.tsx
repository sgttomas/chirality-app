"use client";

import React, { useState } from "react";
import { FileTree } from "./FileTree";
import { ResizableLayout } from "./ResizableLayout";

interface PipelineViewProps {
    family: string;
    selectedVariant: string | null;
    projectRoot: string | null;
    onNavigateHome?: () => void;
    onRootChange?: (path: string) => void;
}

const PIPELINE_PERSONA_MAPPING: Record<string, { personaId: string; fileName: string }> = {
    "PREPARATION": { personaId: "PREPARATION", fileName: "AGENT_PREPARATION.md" },
    "4_DOCUMENTS": { personaId: "4_DOCUMENTS", fileName: "AGENT_4_DOCUMENTS.md" },
    "CHIRALITY_FRAMEWORK": { personaId: "CHIRALITY_FRAMEWORK", fileName: "AGENT_CHIRALITY_FRAMEWORK.md" },
    "CHIRALITY_LENS": { personaId: "CHIRALITY_LENS", fileName: "AGENT_CHIRALITY_LENS.md" },
    "TASK_ESTIMATING": { personaId: "ESTIMATING", fileName: "AGENT_ESTIMATING.md" },
    "AUDIT_AGENTS": { personaId: "AUDIT_AGENTS", fileName: "AGENT_AUDIT_AGENTS.md" },
    "AUDIT_DEPENDENCIES": { personaId: "AUDIT_DEPENDENCIES", fileName: "AGENT_AUDIT_DEPENDENCIES.md" }
};

export function PipelineView({ family, selectedVariant, projectRoot, onNavigateHome, onRootChange }: PipelineViewProps) {
  const [selectedFile, setSelectedFile] = useState<string | null>(null);

  const personaConfig = selectedVariant
    ? (PIPELINE_PERSONA_MAPPING[selectedVariant] ?? { personaId: selectedVariant, fileName: `AGENT_${selectedVariant}.md` })
    : null;
  const autoPrompt = personaConfig
    ? `Read agents/${personaConfig.fileName} and prepare to execute the pipeline according to those instructions.`
    : null;

  return (
    <ResizableLayout
      key={`${family}_${selectedVariant}`}
      agentName={selectedVariant || family}
      sessionId={`pipeline_${family}_${selectedVariant || 'none'}`}
      autoPrompt={autoPrompt}
      selectedFile={selectedFile}
      placeholder="Execute command..."
      harnessMode="pipeline"
      personaId={personaConfig?.personaId ?? null}
      projectRoot={projectRoot}
      onNavigateHome={onNavigateHome}
      onRootChange={onRootChange}
      sidebarContent={() => (
        <>
          <div className="panel-label shrink-0 bg-[var(--color-surface-mid)] flex justify-between items-center p-4 border-b border-[var(--color-border)]">
              <span className="text-[10px] font-mono tracking-[0.2em] uppercase text-[var(--color-applying)]">Project Directory</span>
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
