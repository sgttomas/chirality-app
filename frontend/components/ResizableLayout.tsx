"use client";

import React, { useState, ReactNode } from "react";
import { Resizer } from "./Resizer";
import { ChatPanel } from "./ChatPanel";
import { FilePreview } from "./FilePreview";
import { SettingsModal } from "./SettingsModal";

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

  // Navigation
  onNavigateHome?: () => void;
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
  projectRoot,
  onNavigateHome
}: ResizableLayoutProps) {
  const [chatWidth, setChatWidth] = useState(700);
  const [sidebarWidth, setSidebarWidth] = useState(350);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  // Define a way to trigger file selection from inside sidebarContent if needed
  // But actually we just want to pass the setSelectedFile function up.
  // Actually, let's keep it simple and just accept the sidebarContent as a function or just trust the parent.
  
  return (
    <div className="w-full h-full flex flex-row overflow-hidden bg-[var(--color-surface-low)]">
      <SettingsModal 
        isOpen={isSettingsOpen} 
        onClose={() => setIsSettingsOpen(false)} 
        projectRoot={projectRoot} 
      />

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
        className="flex flex-col h-full bg-[var(--color-surface-mid)] border-r border-[var(--color-border)] overflow-hidden flex-shrink-0"
        style={{ width: `${sidebarWidth}px`, minWidth: '300px' }}
      >
        <div className="flex-grow flex flex-col min-h-0 overflow-hidden">
          {sidebarContent()}
        </div>

        {/* Global Actions Footer */}
        <div className="shrink-0 p-3 border-t border-[var(--color-border)] bg-[var(--color-surface-high)] flex items-center justify-between">
          <div className="group relative">
            <button 
              onClick={onNavigateHome}
              className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-white/5 border border-white/10 text-[10px] uppercase tracking-widest text-white/50 hover:text-white hover:bg-white/10 transition-all font-bold cursor-pointer"
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>
              </svg>
              PORTAL
            </button>
            {/* Tooltip */}
            <div className="absolute bottom-full left-0 mb-2 w-48 p-2 bg-black/80 backdrop-blur-md border border-white/10 rounded shadow-xl opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-50">
              <p className="text-[10px] leading-relaxed text-white/70 font-sans normal-case tracking-normal">
                <span className="text-[var(--color-accent-orange)] font-bold">Command Portal:</span> Access the Hex Grid of agent personas and real-time project deliverable status.
              </p>
            </div>
          </div>

          <div className="group relative">
            <button 
              className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-white/[0.02] border border-white/5 text-[10px] uppercase tracking-widest text-white/20 transition-all font-bold cursor-default"
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/>
              </svg>
              Dashboard
            </button>
            {/* Tooltip */}
            <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-48 p-2 bg-black/80 backdrop-blur-md border border-white/10 rounded shadow-xl opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-50">
              <p className="text-[10px] leading-relaxed text-white/70 font-sans normal-case tracking-normal text-center">
                <span className="text-[var(--color-accent-orange)] font-bold">Future Feature:</span> Project-specific dashboard builder and monitoring interface.
              </p>
            </div>
          </div>

          <div className="group relative">
            <button
              onClick={() => setIsSettingsOpen(true)}
              className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-[var(--color-accent-orange)]/5 border border-[var(--color-accent-orange)]/20 text-[10px] uppercase tracking-widest text-[var(--color-accent-orange)] hover:bg-[var(--color-accent-orange)]/10 transition-all font-bold shadow-[0_0_10px_rgba(249,115,22,0.05)]"
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
              </svg>
              Settings
            </button>
            {/* Tooltip */}
            <div className="absolute bottom-full right-0 mb-2 w-48 p-2 bg-black/80 backdrop-blur-md border border-white/10 rounded shadow-xl opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-50">
              <p className="text-[10px] leading-relaxed text-white/70 font-sans normal-case tracking-normal text-right">
                <span className="text-[var(--color-accent-orange)] font-bold">Configuration:</span> Update your Anthropic API Key and the Global Model (CLAUDE.md).
              </p>
            </div>
          </div>
        </div>
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
