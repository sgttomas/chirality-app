"use client";

import React, { useState } from "react";
import { FileTree } from "./FileTree";
import { Resizer } from "./Resizer";
import { FilePreview } from "./FilePreview";

export function DirectLinkView() {
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [chatWidth, setChatWidth] = useState(400);
  const [sidebarWidth, setSidebarWidth] = useState(300);

  return (
    <div className="workbench-layout h-full">
      {/* Chat Panel */}
      <div className="chat-panel glass" style={{ width: `${chatWidth}px`, minWidth: '200px' }}>
        <div className="chat-messages">
          <div className="msg-agent">
            <strong>AGENT</strong>
            <br />
            Direct terminal active. Bypassing initialization protocol. Direct filesystem access enabled.
          </div>
        </div>
        <div className="chat-input">
          <input type="text" placeholder="Direct command..." className="outline-none" />
        </div>
      </div>

      <Resizer onResize={(delta) => setChatWidth((prev) => prev + delta)} />

      {/* Full Project File Tree Area */}
      <div className="right-panel flex-grow">
        <div className="fs-sidebar glass overflow-hidden flex flex-col" style={{ width: `${sidebarWidth}px`, minWidth: '150px' }}>
          <div className="panel-label shrink-0">Project Root Structure</div>
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