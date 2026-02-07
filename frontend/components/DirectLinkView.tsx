"use client";

import React, { useState } from "react";
import { FileTree } from "./FileTree";
import { Resizer } from "./Resizer";
import { FilePreview } from "./FilePreview";
import { ChatPanel } from "./ChatPanel";

export function DirectLinkView() {
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [chatWidth, setChatWidth] = useState(700);
  const [sidebarWidth, setSidebarWidth] = useState(350);

  return (
    <div className="workbench-layout h-full">
      <ChatPanel 
        agentName="SYSTEM_SESSION" 
        width={chatWidth} 
        onResize={(delta) => setChatWidth(prev => prev + delta)} 
        placeholder="Enter direct command..."
        sessionId="direct_terminal"
        mode="direct"
      />

      <Resizer onResize={(delta) => setChatWidth((prev) => prev + delta)} />

      {/* Full Project File Tree Area */}
      <div className="right-panel flex-grow">
        <div className="fs-sidebar glass overflow-hidden flex flex-col" style={{ width: `${sidebarWidth}px`, minWidth: '300px' }}>
          <div className="panel-label shrink-0 bg-black/20">Project Root Structure</div>
          <FileTree 
            onFileSelect={setSelectedFile}
            className="flex-grow overflow-y-auto p-4 text-base" 
          />
        </div>

        <Resizer onResize={(delta) => setSidebarWidth((prev) => prev + delta)} />

        <FilePreview path={selectedFile} />
      </div>
    </div>
  );
}