"use client";

import React, { useState } from "react";
import { FileTree } from "./FileTree";
import { ResizableLayout } from "./ResizableLayout";

interface DirectLinkViewProps {
    projectRoot: string | null;
    onNavigateHome?: () => void;
    onRootChange?: (path: string) => void;
}

export function DirectLinkView({ projectRoot, onNavigateHome, onRootChange }: DirectLinkViewProps) {
  const [selectedFile, setSelectedFile] = useState<string | null>(null);

  return (
    <ResizableLayout
      agentName="SYSTEM_SESSION"
      sessionId="direct_terminal"
      mode="direct"
      harnessMode="direct"
      personaId={null}
      selectedFile={selectedFile}
      placeholder="Enter direct command..."
      projectRoot={projectRoot}
      onNavigateHome={onNavigateHome}
      onRootChange={onRootChange}
      sidebarContent={() => (
        <>
          <div className="panel-label shrink-0 border-b border-[var(--color-border)]/60 bg-[var(--color-surface-mid)]/80 px-4 py-3.5">
            <div className="flex items-center justify-between gap-3">
              <div className="min-w-0">
                <span className="block text-[10px] font-mono uppercase tracking-[0.2em] text-[var(--color-applying)]">
                  Project Directory
                </span>
                <span className="mono mt-1 block truncate text-[9px] uppercase tracking-[0.12em] text-[var(--color-text-dim)]/85">
                  Direct link // live root
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
