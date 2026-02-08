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
          <div className="panel-label shrink-0 bg-[var(--color-surface-mid)] p-3 border-b border-[var(--color-border)] flex items-center justify-between">
              <span className="text-[10px] font-mono uppercase tracking-widest text-[var(--color-accent-orange)]">Project Directory</span>
              <span className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_10px_#22c55e]"></span>
          </div>
          <div className="flex-grow overflow-y-auto p-2 min-h-0">
              <FileTree 
                  onFileSelect={setSelectedFile}
                  className="h-full text-sm" 
                  rootPath={projectRoot}
              />
          </div>
        </>
      )}
    />
  );
}
