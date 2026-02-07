"use client";

import React, { useState } from "react";
import { FileTree } from "./FileTree";
import { Resizer } from "./Resizer";
import { FilePreview } from "./FilePreview";

export function WorkbenchView() {
  const [selectedFile, setSelectedFile] = useState<string | null>("README.md");
  
  // Panel Widths
  const [chatWidth, setChatWidth] = useState(400);
  const [sidebarWidth, setSidebarWidth] = useState(250);

  return (
    <div className="workbench-layout h-full">
      {/* Chat Panel */}
      <div className="chat-panel glass" style={{ width: `${chatWidth}px`, minWidth: '200px' }}>
        <div className="chat-messages">
          <div className="msg-agent">
            <strong>SYSTEM_AGENT</strong>
            <br />
            Neural link established. Filesystem mapped. I found 3 distinct deliverables. See the proposal on the right.
          </div>
          <div className="text-right italic text-[var(--color-text-dim)] mb-5">
            Wait, &quot;Grading Plan&quot; should be in Package 02.
          </div>
          <div className="msg-agent">
            <strong>SYSTEM_AGENT</strong>
            <br />
            Understood. Moving [DEL-02] Grading Plan to [PKG-02]. Updating proposal...
          </div>
        </div>
        <div className="chat-input">
          <input type="text" placeholder="Send instruction..." className="outline-none" />
        </div>
      </div>

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