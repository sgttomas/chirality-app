"use client";

import React, { useState, ReactNode } from "react";
import { Resizer } from "./Resizer";
import { ChatPanel } from "./ChatPanel";
import { FilePreview } from "./FilePreview";

interface ResizableLayoutProps {
  // Chat Props
  agentName: string;
  sessionId: string;
  autoPrompt?: string | null;
  placeholder?: string;
  mode?: "agent" | "direct";
  harnessMode: "workbench" | "pipeline" | "direct";
  personaId: string | null;
  projectRoot: string | null;
  
  // Sidebar Content (The middle pane controls)
  sidebarContent: () => ReactNode;
  
  // Preview State
  selectedFile: string | null;
}

export function ResizableLayout({
  agentName,
  sessionId,
  autoPrompt,
  placeholder,
  mode = "agent",
  harnessMode,
  personaId,
  sidebarContent,
  selectedFile,
  projectRoot
}: ResizableLayoutProps) {
  const [chatWidth, setChatWidth] = useState(700);
  const [sidebarWidth, setSidebarWidth] = useState(350);

  // Define a way to trigger file selection from inside sidebarContent if needed
  // But actually we just want to pass the setSelectedFile function up.
  // Actually, let's keep it simple and just accept the sidebarContent as a function or just trust the parent.
  
  return (
    <div className="w-full h-full flex flex-row overflow-hidden bg-black/10">
      {/* Pane 1: Chat Panel */}
      <div className="flex-shrink-0 h-full" style={{ width: `${chatWidth}px`, minWidth: '400px' }}>
        <ChatPanel 
            agentName={agentName} 
            width={chatWidth} 
            onResize={() => {}} // Controlled by Resizer now
            sessionId={sessionId}
            autoPrompt={autoPrompt}
            mode={mode}
            harnessMode={harnessMode}
            personaId={personaId}
            placeholder={placeholder}
            projectRoot={projectRoot}
        />
      </div>

      {/* Resizer 1 */}
      <Resizer onResize={(delta) => setChatWidth(prev => Math.max(400, prev + delta))} />

      {/* Pane 2: Middle Sidebar (Controls + File Tree) */}
      <div 
        className="flex flex-col h-full bg-black/20 border-r border-white/10 overflow-hidden flex-shrink-0"
        style={{ width: `${sidebarWidth}px`, minWidth: '300px' }}
      >
        {sidebarContent()}
      </div>

      {/* Resizer 2 */}
      <Resizer onResize={(delta) => setSidebarWidth(prev => Math.max(250, prev + delta))} />

      {/* Pane 3: File Preview */}
      <div className="flex-grow min-w-[300px] h-full overflow-hidden">
        <FilePreview path={selectedFile} />
      </div>
    </div>
  );
}
