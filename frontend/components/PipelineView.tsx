"use client";

import React, { useState } from "react";
import { FileTree } from "./FileTree";
import { Resizer } from "./Resizer";
import { FilePreview } from "./FilePreview";
import { ChatPanel } from "./ChatPanel";

interface PipelineViewProps {
    family: string | null;
}

const FAMILY_MAP: Record<string, string[]> = {
    "PREP*": ["PREPARATION", "4_DOCUMENTS", "CHIRALITY_FRAMEWORK", "CHIRALITY_LENS"],
    "AUDIT*": ["AUDIT_AGENTS", "AUDIT_DEPENDENCIES"],
    "TASK*": ["TASK_ESTIMATING"]
};

const AGENT_FILE_MAPPING: Record<string, string> = {
    "TASK_ESTIMATING": "AGENT_ESTIMATING.md",
    "AUDIT_AGENTS": "AGENT_DEPENDENCIES.md",
    "AUDIT_DEPENDENCIES": "AGENT_DEPENDENCIES.md"
};

export function PipelineView({ family }: PipelineViewProps) {
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [chatWidth, setChatWidth] = useState(700);
  const [sidebarWidth, setSidebarWidth] = useState(350);
  const [selectedVariant, setSelectedVariant] = useState<string | null>(null);

  const variants = family ? FAMILY_MAP[family] || [] : [];
  
  const fileName = selectedVariant ? (AGENT_FILE_MAPPING[selectedVariant] || `AGENT_${selectedVariant}.md`) : null;
  const autoPrompt = fileName ? `Read agents/${fileName} and prepare to execute the pipeline according to those instructions.` : null;

  return (
    <div className="workbench-layout h-full" key={selectedVariant}>
      <ChatPanel 
        agentName={selectedVariant || family || "TASK_PIPELINE"} 
        width={chatWidth} 
        onResize={(delta) => setChatWidth(prev => prev + delta)} 
        placeholder="Execute command..."
        sessionId={`pipeline_${family}_${selectedVariant}`}
        autoPrompt={autoPrompt}
        mode="agent"
      />

      <Resizer onResize={(delta) => setChatWidth((prev) => prev + delta)} />

      {/* Pipeline Variants Sidebar */}
      <div className="right-panel flex-grow">
        <div className="fs-sidebar glass overflow-hidden flex flex-col" style={{ width: `${sidebarWidth}px`, minWidth: '300px' }}>
          <div className="panel-label shrink-0 flex flex-col gap-1 p-4 bg-black/20">
              <span className="text-[var(--color-accent-orange)] font-black tracking-[0.2em]">{family || "PIPELINE"}</span>
              <span className="text-[9px] opacity-50">Select Task Variant</span>
          </div>
          <div className="flex-grow overflow-y-auto p-2">
              {variants.map(variant => (
                  <div 
                    key={variant}
                    onClick={() => setSelectedVariant(variant)}
                    className={`p-4 mb-2 border border-white/[0.05] rounded cursor-pointer transition-all ${selectedVariant === variant ? 'bg-[var(--color-accent-orange)]/20 border-[var(--color-accent-orange)]/40 text-[var(--color-accent-orange)] shadow-lg' : 'hover:bg-white/5 text-[var(--color-text-dim)]'}`}
                  >
                      <div className="text-[10px] font-mono opacity-30 mb-1">VARIANT</div>
                      <div className="text-xs font-black tracking-widest">{variant}</div>
                  </div>
              ))}
              {variants.length === 0 && (
                  <div className="p-4 text-xs opacity-30 italic">No variants defined for this family.</div>
              )}
          </div>
          
          <div className="panel-label shrink-0 mt-auto border-t border-white/10">File Context</div>
          <div className="h-1/3 min-h-[200px]">
            <FileTree 
                onFileSelect={setSelectedFile}
                className="flex-grow overflow-y-auto p-4 text-base" 
            />
          </div>
        </div>

        <Resizer onResize={(delta) => setSidebarWidth((prev) => prev + delta)} />

        <FilePreview path={selectedFile} />
      </div>
    </div>
  );
}