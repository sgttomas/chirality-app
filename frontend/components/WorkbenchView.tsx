"use client";

import React, { useState } from "react";
import { FileTree } from "./FileTree";
import { Resizer } from "./Resizer";
import { FilePreview } from "./FilePreview";
import { ChatPanel } from "./ChatPanel";

interface WorkbenchViewProps {
    agentName: string | null;
}

const PERSONA_AGENTS = [
    "DECOMP", "ORCHESTRATE", "WORKING_ITEMS", "AGGREGATE", 
    "HELP", "AGENTS", "CHANGE", "DEPENDENCIES", "RECONCILING"
];

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

export function WorkbenchView({ agentName: initialAgent }: WorkbenchViewProps) {
  const [selectedFile, setSelectedFile] = useState<string | null>("README.md");
  const [chatWidth, setChatWidth] = useState(750);
  const [sidebarWidth, setSidebarWidth] = useState(350);
  const [currentAgent, setCurrentAgent] = useState<string>(initialAgent || "WORKING_ITEMS");

  const fileName = PERSONA_FILE_MAPPING[currentAgent];
  const autoPrompt = fileName ? `Read agents/${fileName} and initialize your persona accordingly. Output your initialization status.` : null;

  return (
    <div className="workbench-layout h-full relative" key={currentAgent}>
      <ChatPanel 
        agentName={currentAgent} 
        width={chatWidth} 
        onResize={(delta) => setChatWidth(prev => prev + delta)} 
        sessionId={`workbench_${currentAgent}`}
        autoPrompt={autoPrompt}
        mode="agent"
      />

      <Resizer onResize={(delta) => setChatWidth((prev) => prev + delta)} />

      <div className="right-panel flex-grow">
        <div className="fs-sidebar overflow-hidden flex flex-col" style={{ width: `${sidebarWidth}px`, minWidth: '300px' }}>
          {/* Agent Selector */}
          <div className="shrink-0 p-4 bg-black/40 border-b border-white/10">
              <span className="text-[9px] font-black tracking-[0.3em] text-[var(--color-accent-orange)] uppercase opacity-60 block mb-3">Persona_Link</span>
              <select 
                value={currentAgent}
                onChange={(e) => setCurrentAgent(e.target.value)}
                className="w-full bg-black/60 border border-white/10 rounded px-3 py-2 text-xs font-bold tracking-widest text-[var(--color-text-main)] focus:border-[var(--color-accent-orange)] outline-none cursor-pointer appearance-none uppercase"
              >
                  {PERSONA_AGENTS.map(agent => (
                      <option key={agent} value={agent}>{agent}</option>
                  ))}
              </select>
          </div>

          <div className="panel-label shrink-0 flex justify-between items-center bg-black/20">
              <span>Deliverable Tree</span>
          </div>
          <FileTree 
            onFileSelect={setSelectedFile} 
            className="flex-grow overflow-y-auto p-4" 
          />
        </div>

        <Resizer onResize={(delta) => setSidebarWidth((prev) => prev + delta)} />

        <FilePreview path={selectedFile} />
      </div>
    </div>
  );
}