"use client";

import React, { useState } from "react";
import { FileTree } from "./FileTree";
import { Resizer } from "./Resizer";
import { FilePreview } from "./FilePreview";
import { ChatPanel } from "./ChatPanel";

export function WorkbenchView() {
  const [selectedFile, setSelectedFile] = useState<string | null>("README.md");
  const [chatWidth, setChatWidth] = useState(400);
  const [sidebarWidth, setSidebarWidth] = useState(250);

  return (
    <div className="workbench-layout h-full relative">
      <ChatPanel 
        agentName="WORKBENCH" 
        width={chatWidth} 
        onResize={(delta) => setChatWidth(prev => prev + delta)} 
      />

      <Resizer onResize={(delta) => setChatWidth((prev) => prev + delta)} />

      {/* Right Content Panel */}
      <div className="right-panel flex-grow">
        <div className="fs-sidebar overflow-hidden flex flex-col" style={{ width: `${sidebarWidth}px`, minWidth: '150px' }}>
          <div className="panel-label shrink-0">Deliverable Tree</div>
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
