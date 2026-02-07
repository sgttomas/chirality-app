"use client";

import React, { useState } from "react";
import { FileTree } from "./FileTree";
import { Resizer } from "./Resizer";
import { FilePreview } from "./FilePreview";

export function PipelineView() {
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [chatWidth, setChatWidth] = useState(400);
  const [sidebarWidth, setSidebarWidth] = useState(300);

  return (
    <div className="workbench-layout h-full">
      {/* Chat Panel */}
      <div className="chat-panel glass" style={{ width: `${chatWidth}px`, minWidth: '200px' }}>
        <div className="chat-messages">
          <div className="msg-agent">
            <strong>TASK_AGENT</strong>
            <br />
            Pipeline initialized. Awaiting execution brief validation. 
            Select target files from the manifest on the right to review proposed changes.
          </div>
          <div className="msg-agent">
            <strong>SYSTEM</strong>
            <br />
            Scan complete: 142 items found. 12 conflicts identified.
          </div>
        </div>
        <div className="chat-input">
          <input type="text" placeholder="Execute command..." className="outline-none" />
        </div>
      </div>

      <Resizer onResize={(delta) => setChatWidth((prev) => prev + delta)} />

      {/* Right Content Panel */}
      <div className="right-panel flex-grow">
        <div className="fs-sidebar glass overflow-hidden flex flex-col" style={{ width: `${sidebarWidth}px`, minWidth: '150px' }}>
          <div className="panel-label shrink-0">Task Write Manifest</div>
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