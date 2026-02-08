"use client";

import React, { useState, ReactNode } from "react";
import { Resizer } from "./Resizer";
import { ChatPanel } from "./ChatPanel";
import { FilePreview } from "./FilePreview";
import { SettingsModal } from "./SettingsModal";
import { DirectoryPicker } from "./DirectoryPicker";

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
  onRootChange?: (path: string) => void;
}

function formatFolderLabel(pathValue: string): string {
  const cleaned = pathValue.trim();
  if (!cleaned || cleaned === "~") {
    return "~";
  }

  const normalized = cleaned.replace(/\/+$/, "");
  if (!normalized) {
    return "/";
  }

  const parts = normalized.split("/").filter(Boolean);
  return parts[parts.length - 1] || "/";
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
  onNavigateHome,
  onRootChange
}: ResizableLayoutProps) {
  const [chatWidth, setChatWidth] = useState(700);
  const [sidebarWidth, setSidebarWidth] = useState(350);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [showDirPicker, setShowDirPicker] = useState(false);

  const folderLabel = formatFolderLabel(projectRoot ?? "~");
  const footerGhostButtonClass =
    "ui-control ui-focus-ring flex items-center gap-2 px-3 py-1.5 text-[10px] font-bold tracking-[0.14em] uppercase cursor-pointer";
  const footerAccentButtonClass =
    "ui-control ui-focus-ring flex items-center gap-2 px-3 py-1.5 text-[10px] font-bold tracking-[0.14em] uppercase cursor-pointer text-[var(--color-accent-orange)] border-[var(--color-accent-orange)]/25 bg-[var(--color-accent-orange)]/8 hover:bg-[var(--color-accent-orange)]/14";
  const footerTooltipClass =
    "pointer-events-none absolute bottom-full mb-2 w-52 rounded-md border border-white/10 bg-black/80 p-2 opacity-0 shadow-xl backdrop-blur-md transition-opacity group-hover:opacity-100 z-50";
  
  return (
    <div className="w-full h-full flex flex-row overflow-hidden bg-[var(--color-surface-low)]">
      {showDirPicker && (
        <DirectoryPicker 
          onSelect={(path) => {
            setShowDirPicker(false);
            onRootChange?.(path);
          }} 
          onCancel={() => setShowDirPicker(false)} 
        />
      )}
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
        className="flex h-full flex-shrink-0 flex-col overflow-hidden border-r border-[var(--color-border)] bg-[var(--color-surface-mid)]"
        style={{ width: `${sidebarWidth}px`, minWidth: '300px' }}
      >
        <div className="flex-grow flex flex-col min-h-0 overflow-hidden">
          {sidebarContent()}
        </div>

        {/* Global Actions Footer */}
        <div className="shrink-0 border-t border-[var(--color-border)] bg-[var(--color-surface-high)] px-3 py-2.5">
          <div className="grid grid-cols-[auto,minmax(0,1fr),auto] items-center gap-2">
            <div className="group relative">
            <button 
              onClick={() => onNavigateHome?.()}
              disabled={!onNavigateHome}
              className={`${footerGhostButtonClass} text-[var(--color-text-dim)] hover:text-[var(--color-text-main)]`}
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>
              </svg>
              PORTAL
            </button>
            {/* Tooltip */}
            <div className={`${footerTooltipClass} left-0`}>
              <p className="text-[10px] leading-relaxed text-white/70 font-sans normal-case tracking-normal">
                <span className="text-[var(--color-accent-orange)] font-bold">Command Portal:</span> Access the Hex Grid of agent personas and real-time project deliverable status.
              </p>
            </div>
          </div>

          <button
            onClick={() => setShowDirPicker(true)}
            className={`${footerAccentButtonClass} min-w-0 justify-center truncate`}
          >
            <span className="opacity-50 font-mono">DIR:</span>
            <span className="truncate">{folderLabel}</span>
            <span className="text-white/30 font-mono ml-1">❯</span>
          </button>

          <div className="group relative">
            <button
              onClick={() => setIsSettingsOpen(true)}
              className={footerAccentButtonClass}
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
              </svg>
              Settings
            </button>
            {/* Tooltip */}
            <div className={`${footerTooltipClass} right-0`}>
              <p className="text-[10px] leading-relaxed text-white/70 font-sans normal-case tracking-normal text-right">
                <span className="text-[var(--color-accent-orange)] font-bold">Configuration:</span> Update your Anthropic API Key and the Global Model (CLAUDE.md).
              </p>
            </div>
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
