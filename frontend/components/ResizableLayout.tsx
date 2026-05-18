"use client";

import React, { useState, useEffect, ReactNode } from "react";
import { Resizer } from "./Resizer";
import { ChatPanel } from "./ChatPanel";
import { FilePreview } from "./FilePreview";
import { SettingsModal } from "./SettingsModal";
import { DirectoryPicker } from "./DirectoryPicker";

const TOOLKIT_SIDEBAR_STORAGE_KEY = "chirality_toolkit_sidebar_enabled";

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
  const [chatWidth, setChatWidth] = useState(760);
  const [sidebarWidth, setSidebarWidth] = useState(340);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [showDirPicker, setShowDirPicker] = useState(false);
  const [isCompactLayout, setIsCompactLayout] = useState(false);
  const [compactPane, setCompactPane] = useState<"files" | "preview">("files");
  const [viewportWidth, setViewportWidth] = useState(1280);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isPreviewCollapsed, setIsPreviewCollapsed] = useState(false);
  const [isToolkitSidebarEnabled, setIsToolkitSidebarEnabled] = useState(() => {
    if (typeof window === "undefined") {
      return false;
    }
    return localStorage.getItem(TOOLKIT_SIDEBAR_STORAGE_KEY) === "true";
  });

  const folderLabel = formatFolderLabel(projectRoot ?? "~");
  const footerGhostButtonClass =
    "ui-control ui-focus-ring flex items-center gap-1.5 px-3 py-1.5 text-[11px] font-bold tracking-[0.02em] uppercase cursor-pointer";
  const footerAccentButtonClass =
    "ui-control ui-focus-ring flex items-center gap-1.5 px-3 py-1.5 text-[11px] font-bold tracking-[0.02em] uppercase cursor-pointer text-[var(--color-accent-text)] border-[var(--color-accent-orange)]/25 bg-[var(--color-accent-orange)]/8 hover:bg-[var(--color-accent-orange)]/14";
  const footerTooltipClass =
    "pointer-events-none absolute bottom-full mb-2 w-52 rounded-md border border-white/10 bg-black/80 p-2 opacity-0 shadow-xl backdrop-blur-md transition-opacity group-hover:opacity-100 z-50";
  
  useEffect(() => {
    const syncViewport = () => {
      const nextWidth = window.innerWidth;
      setViewportWidth(nextWidth);
      setIsCompactLayout(nextWidth <= 1180);
    };

    queueMicrotask(syncViewport);
    window.addEventListener("resize", syncViewport);
    return () => {
      window.removeEventListener("resize", syncViewport);
    };
  }, []);

  const renderGlobalActionsFooter = (compact = false) => (
    <div className="ui-panel-soft shrink-0 rounded-xl p-2">
      <div className={`flex gap-2 ${compact ? "flex-col" : "items-center"}`}>
        <button
          onClick={() => setShowDirPicker(true)}
          className={`${footerAccentButtonClass} min-w-0 justify-center truncate ${compact ? "w-full" : "flex-1"}`}
        >
          <span className="opacity-50 font-mono text-[11px]">DIR:</span>
          <span className="truncate ml-1">{folderLabel}</span>
          <span className="text-white/20 font-mono ml-1">❯</span>
        </button>

        <div className={`grid grid-cols-2 gap-2 ${compact ? "w-full" : "w-[185px] shrink-0"}`}>
          <div className="group relative">
            <button
              onClick={() => onNavigateHome?.()}
              disabled={!onNavigateHome}
              className={`${footerGhostButtonClass} mono text-[11px] w-full justify-center text-[var(--color-text-dim)] hover:text-[var(--color-text-main)]`}
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" /><polyline points="9 22 9 12 15 12 15 22" />
              </svg>
              Portal
            </button>
            <div className={`${footerTooltipClass} left-0`}>
              <p className="text-[10px] leading-relaxed text-white/70 font-sans normal-case tracking-normal">
                <span className="text-[var(--color-accent-text)] font-bold">Command Portal:</span> Access the Hex Grid of agent personas and real-time project deliverable status.
              </p>
            </div>
          </div>

          <div className="group relative">
            <button
              onClick={() => setIsSettingsOpen(true)}
              className={`${footerAccentButtonClass} mono text-[11px] w-full justify-center`}
            >
              <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
              </svg>
              Config
            </button>
            <div className={`${footerTooltipClass} right-0`}>
              <p className="text-[10px] leading-relaxed text-white/70 font-sans normal-case tracking-normal text-right">
                <span className="text-[var(--color-accent-text)] font-bold">Configuration:</span> Update your Anthropic API Key and the Global Model (CLAUDE.md).
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderCollapsedSidebar = () => (
    <div className="ui-panel-soft flex h-full w-12 shrink-0 flex-col items-center justify-between rounded-xl py-3">
      <button
        onClick={() => setIsSidebarCollapsed(false)}
        className="ui-control ui-focus-ring flex h-8 w-8 items-center justify-center rounded-md hover:text-[var(--color-accent-text)]"
        title="Expand Project Directory"
      >
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="13 17 18 12 13 7" /><polyline points="6 17 11 12 6 7" />
        </svg>
      </button>

      <div className="flex flex-col items-center gap-2">
        <button
          onClick={() => setShowDirPicker(true)}
          className="ui-control ui-focus-ring flex h-8 w-8 items-center justify-center rounded-md hover:text-[var(--color-accent-text)]"
          title={`Change Dir: ${folderLabel}`}
        >
          <span className="mono text-[8px] font-bold">DIR</span>
        </button>
        <button
          onClick={() => onNavigateHome?.()}
          disabled={!onNavigateHome}
          className="ui-control ui-focus-ring flex h-8 w-8 items-center justify-center rounded-md hover:text-[var(--color-accent-text)]"
          title="Portal"
        >
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
            <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
            <polyline points="9 22 9 12 15 12 15 22" />
          </svg>
        </button>
        <button
          onClick={() => setIsSettingsOpen(true)}
          className="ui-control ui-focus-ring flex h-8 w-8 items-center justify-center rounded-md hover:text-[var(--color-accent-text)]"
          title="Settings"
        >
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="3"></circle>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
          </svg>
        </button>
      </div>
    </div>
  );

  const renderCollapsedPreview = () => (
    <div className="ui-panel-soft flex h-full w-10 shrink-0 flex-col items-center rounded-xl py-3">
      <button
        onClick={() => setIsPreviewCollapsed(false)}
        className="ui-control ui-focus-ring flex h-8 w-8 items-center justify-center rounded-md hover:text-[var(--color-accent-text)]"
        title="Expand Preview"
      >
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="11 17 6 12 11 7" /><polyline points="18 17 13 12 18 7" />
        </svg>
      </button>
      <div className="mt-3 w-px flex-1 bg-[var(--color-border)]/70" />
      <span className="mono py-3 text-[8px] font-semibold uppercase tracking-[0.14em] text-[var(--color-text-dim)]/80 [writing-mode:vertical-rl] rotate-180">
        Preview
      </span>
    </div>
  );

  const compactTabBaseClass =
    "ui-control ui-focus-ring px-3 py-1.5 mono text-[10px] font-semibold uppercase tracking-[0.1em]";

  return (
    <div className="relative h-full w-full overflow-hidden bg-[var(--color-surface-low)]">
      <div
        aria-hidden
        className="ui-neural-overlay pointer-events-none absolute inset-0 opacity-70"
      />

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
        toolkitSidebarEnabled={isToolkitSidebarEnabled}
        onToolkitSidebarEnabledChange={(enabled) => {
          setIsToolkitSidebarEnabled(enabled);
          localStorage.setItem(TOOLKIT_SIDEBAR_STORAGE_KEY, enabled ? "true" : "false");
        }}
      />

      {isCompactLayout ? (
        <div className="relative flex h-full flex-col overflow-hidden gap-2 px-2.5 pb-2.5 pt-2">
          <div className="shrink-0 ui-panel-soft p-2">
            <div className="flex items-center justify-between gap-3">
              <span className="mono text-[9px] font-semibold uppercase tracking-[0.16em] text-[var(--color-accent-text)]/85">
                Operations Deck
              </span>
              <span className="mono text-[9px] uppercase tracking-[0.12em] text-[var(--color-text-dim)]/80">
                HEX ROUTE
              </span>
            </div>
          </div>

          <div className="h-[52%] min-h-[290px] shrink-0 ui-panel-strong p-1.5">
            <ChatPanel
              agentName={agentName}
              width={viewportWidth}
              onResize={() => {}}
              sessionId={sessionId}
              autoPrompt={autoPrompt}
              mode={mode}
              harnessMode={harnessMode}
              personaId={personaId}
              placeholder={placeholder}
              projectRoot={projectRoot}
              showToolkit={isToolkitSidebarEnabled}
            />
          </div>

          <div className="shrink-0 ui-panel-soft px-3 py-2">
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setCompactPane("files")}
                className={`${compactTabBaseClass} ${
                  compactPane === "files"
                    ? "border-[var(--color-accent-orange)]/35 bg-[var(--color-accent-orange)]/10 text-[var(--color-accent-text)]"
                    : "text-[var(--color-text-dim)]"
                }`}
              >
                Files
              </button>
              <button
                type="button"
                onClick={() => setCompactPane("preview")}
                className={`${compactTabBaseClass} ${
                  compactPane === "preview"
                    ? "border-[var(--color-accent-orange)]/35 bg-[var(--color-accent-orange)]/10 text-[var(--color-accent-text)]"
                    : "text-[var(--color-text-dim)]"
                }`}
              >
                Preview
              </button>
            </div>
          </div>

          <div className="min-h-0 flex-1 overflow-hidden">
            {compactPane === "files" ? (
              <div className="ui-panel flex h-full min-h-0 flex-col overflow-hidden">
                {sidebarContent()}
              </div>
            ) : (
              <div className="ui-panel-strong h-full overflow-hidden">
                <FilePreview path={selectedFile} projectRoot={projectRoot} />
              </div>
            )}
          </div>

          {renderGlobalActionsFooter(true)}
        </div>
      ) : (
        <div className="relative flex h-full flex-row items-stretch gap-3 overflow-hidden px-3 pb-3 pt-2">
          {/* Chat Panel - Flexible if others are collapsed */}
          <div
            className={`relative h-full ui-panel-strong p-1.5 ${
                isSidebarCollapsed && isPreviewCollapsed ? "flex-1" : "flex-shrink-0"
            }`}
            style={!(isSidebarCollapsed && isPreviewCollapsed) ? { width: `${chatWidth}px`, minWidth: "430px" } : { minWidth: "430px" }}
          >
            <ChatPanel
              agentName={agentName}
              width={isSidebarCollapsed && isPreviewCollapsed ? viewportWidth - 60 : chatWidth}
              onResize={() => {}}
              sessionId={sessionId}
              autoPrompt={autoPrompt}
              mode={mode}
              harnessMode={harnessMode}
              personaId={personaId}
              placeholder={placeholder}
              projectRoot={projectRoot}
              showToolkit={isToolkitSidebarEnabled}
            />
          </div>

          {!isSidebarCollapsed || !isPreviewCollapsed ? (
            <Resizer onResize={(delta) => setChatWidth((prev) => Math.max(400, prev + delta))} />
          ) : null}

          {/* Project Directory / Sidebar */}
          {isSidebarCollapsed ? (
            renderCollapsedSidebar()
          ) : (
            <div
              className={`group/sidebar ui-panel relative flex h-full flex-col overflow-hidden ${
                isPreviewCollapsed ? "flex-1" : "shrink-0"
              }`}
              style={!isPreviewCollapsed ? { width: `${sidebarWidth}px`, minWidth: "290px" } : { minWidth: "290px" }}
            >
              <button
                onClick={() => setIsSidebarCollapsed(true)}
                className="ui-control ui-focus-ring absolute right-2 top-1/2 z-10 inline-flex h-7 w-7 -translate-y-1/2 items-center justify-center rounded-md border-[var(--color-border)]/65 bg-[var(--color-surface-high)]/82 text-[var(--color-text-dim)] opacity-85 hover:opacity-100 hover:text-[var(--color-accent-text)]"
                title="Collapse Project Directory"
              >
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="13 17 8 12 13 7" />
                  <polyline points="20 17 15 12 20 7" />
                </svg>
              </button>
              <div className="flex min-h-0 flex-1 flex-col overflow-hidden">
                {sidebarContent()}
              </div>
              <div className="shrink-0 px-2.5 pb-2.5 pt-2">
                {renderGlobalActionsFooter()}
              </div>
            </div>
          )}

          {!isSidebarCollapsed && !isPreviewCollapsed && (
            <Resizer onResize={(delta) => setSidebarWidth((prev) => Math.max(250, prev + delta))} />
          )}

          {/* Preview Panel */}
          {isPreviewCollapsed ? (
            renderCollapsedPreview()
          ) : (
            <div className="group/preview ui-panel-strong relative h-full min-w-[320px] flex-1 overflow-hidden rounded-2xl">
              <button
                onClick={() => setIsPreviewCollapsed(true)}
                className="ui-control ui-focus-ring absolute left-2 top-1/2 z-10 inline-flex h-7 w-7 -translate-y-1/2 items-center justify-center rounded-md border-[var(--color-border)]/65 bg-[var(--color-surface-high)]/82 text-[var(--color-text-dim)] opacity-85 hover:opacity-100 hover:text-[var(--color-accent-text)]"
                title="Collapse Preview"
              >
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="11 17 16 12 11 7" />
                  <polyline points="4 17 9 12 4 7" />
                </svg>
              </button>
              <FilePreview path={selectedFile} projectRoot={projectRoot} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
