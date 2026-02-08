"use client";

import { useState, useEffect } from "react";
import { HexGrid } from "@/components/HexGrid";
import { DashboardList } from "@/components/DashboardList";
import { WorkbenchView } from "@/components/WorkbenchView";
import { PipelineView } from "@/components/PipelineView";
import { DirectLinkView } from "@/components/DirectLinkView";
import { DirectoryPicker } from "@/components/DirectoryPicker";

type View = "home" | "workbench" | "session" | "pipeline";

const PERSONA_AGENTS = [
    "DECOMP", "ORCHESTRATE", "WORKING_ITEMS", "AGGREGATE", 
    "HELP", "AGENTS", "DEPENDENCIES", "CHANGE", "RECONCILING"
];

const VIEW_TABS: Array<{ id: View; label: string }> = [
  { id: "home", label: "PORTAL" },
  { id: "workbench", label: "WORKBENCH" },
  { id: "pipeline", label: "PIPELINE" },
  { id: "session", label: "DIRECT" }
];

const VIEW_TITLE: Record<View, { lead: string; accent: string }> = {
  home: { lead: "COMMAND", accent: "PORTAL" },
  workbench: { lead: "WORK", accent: "BENCH" },
  session: { lead: "DIRECT", accent: "LINK" },
  pipeline: { lead: "TASK", accent: "PIPELINE" }
};

const PIPELINE_FAMILIES = ["PREP*", "TASK*", "AUDIT*"];

const FAMILY_MAP: Record<string, string[]> = {
    "PREP*": ["PREPARATION", "4_DOCUMENTS", "CHIRALITY_FRAMEWORK", "CHIRALITY_LENS"],
    "AUDIT*": ["AUDIT_AGENTS", "AUDIT_DEPENDENCIES"],
    "TASK*": ["TASK_ESTIMATING"]
};

export default function Home() {
  const [currentView, setCurrentView] = useState<View>("home");
  
  // Shared Navigation State
  const [agentName, setAgentName] = useState<string>("WORKING_ITEMS");
  const [pipelineFamily, setPipelineFamily] = useState<string>("PREP*");
  const [selectedVariant, setSelectedVariant] = useState<string | null>(null);
  const [initialWorkbenchPath, setInitialWorkbenchPath] = useState<string | null>(null);
  
  const [projectRoot, setProjectRoot] = useState<string | null>(null);
  const [isLightMode, setIsLightMode] = useState(false);
  const [showDirPicker, setShowDirPicker] = useState(false);

  useEffect(() => {
    if (isLightMode) {
      document.body.classList.add("light-mode");
    } else {
      document.body.classList.remove("light-mode");
    }
  }, [isLightMode]);

  useEffect(() => {
    const savedRoot = sessionStorage.getItem("chirality_project_root");
    if (!savedRoot || !savedRoot.trim()) {
      return;
    }
    queueMicrotask(() => setProjectRoot(savedRoot));
  }, []);

  const handleRootChange = (path: string) => {
      setProjectRoot(path);
      sessionStorage.setItem("chirality_project_root", path);
  };

  const launchAgent = (name: string) => {
    if (PERSONA_AGENTS.includes(name)) {
      setAgentName(name);
      setInitialWorkbenchPath(null); 
      setCurrentView("workbench");
    } else {
      setPipelineFamily(name);
      setSelectedVariant(null);
      setCurrentView("pipeline");
    }
  };

  const variants = FAMILY_MAP[pipelineFamily] || [];
  const title = VIEW_TITLE[currentView];

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      {showDirPicker && (
        <DirectoryPicker
          onSelect={(path) => {
            setShowDirPicker(false);
            handleRootChange(path);
          }}
          onCancel={() => setShowDirPicker(false)}
        />
      )}

      {/* Wireframe Controls */}
      <div id="wireframe-controls" className="shrink-0 border-b border-[var(--color-border)] bg-black/70 backdrop-blur-md">
        <div className="mx-auto flex w-full max-w-[1600px] flex-wrap items-center justify-center gap-2 px-4 py-2.5">
          {VIEW_TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setCurrentView(tab.id)}
              className={`ui-control ui-focus-ring cursor-pointer px-4 py-1.5 text-[11px] font-bold tracking-[0.14em] uppercase ${
                currentView === tab.id
                  ? "border-[var(--color-accent-orange)] bg-[var(--color-accent-orange)]/6 text-[var(--color-accent-orange)] shadow-[0_0_12px_rgba(249,115,22,0.22)]"
                  : "text-[var(--color-text-dim)] hover:text-[var(--color-text-main)]"
              }`}
            >
              {tab.label}
            </button>
          ))}
          <div className="mx-1 hidden h-5 w-px bg-white/15 sm:block" />
          <button
            disabled
            className="ui-control cursor-default px-4 py-1.5 text-[11px] font-bold tracking-[0.14em] uppercase text-white/30 border-white/10"
          >
            Dashboard
          </button>
          <button
            onClick={() => setIsLightMode(!isLightMode)}
            className="ui-control ui-focus-ring ml-0 cursor-pointer px-4 py-1.5 text-[11px] font-bold tracking-[0.14em] uppercase text-[var(--color-text-dim)] hover:text-[var(--color-text-main)] sm:ml-3"
          >
            {isLightMode ? "☾ DARK" : "☀ LIGHT"}
          </button>
        </div>
      </div>

      {/* Header */}
      <header className="shrink-0 border-b border-[var(--color-border)]/60 bg-black/20">
        <div className="mx-auto flex w-full max-w-[1600px] flex-wrap items-center justify-between gap-4 px-5 py-4 md:px-6">
          <div className="flex min-w-0 flex-1 flex-wrap items-center gap-4 md:gap-6">
            <div className="ui-type-title whitespace-nowrap font-extrabold tracking-[0.14em] uppercase">
              {title.lead}
              <span className="px-1 text-[var(--color-text-dim)]">{" // "}</span>
              <span className="text-[var(--color-accent-orange)]">{title.accent}</span>
            </div>

            {/* Contextual Selectors in Header */}
            {currentView === "workbench" && (
              <div className="ui-panel-soft ml-0 flex items-center gap-2.5 rounded-lg px-3 py-2 md:ml-1">
                <span className="ui-type-mono-meta text-[9px] font-black text-[var(--color-accent-orange)] opacity-70">Persona</span>
                <select
                  value={agentName}
                  onChange={(e) => setAgentName(e.target.value)}
                  className="ui-focus-ring min-w-[180px] cursor-pointer bg-transparent text-[11px] font-bold tracking-[0.14em] text-[var(--color-text-main)] uppercase outline-none"
                >
                  {PERSONA_AGENTS.map((agent) => (
                    <option key={agent} value={agent} className="bg-slate-900">
                      {agent}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {currentView === "pipeline" && (
              <div className="ml-0 flex flex-wrap items-center gap-2.5 md:ml-1 md:gap-3">
                <div className="ui-panel-soft flex items-center gap-2.5 rounded-lg px-3 py-2">
                  <span className="ui-type-mono-meta text-[9px] font-black text-[var(--color-accent-orange)] opacity-70">Family</span>
                  <select
                    value={pipelineFamily}
                    onChange={(e) => {
                      setPipelineFamily(e.target.value);
                      setSelectedVariant(null);
                    }}
                    className="ui-focus-ring min-w-[130px] cursor-pointer bg-transparent text-[11px] font-bold tracking-[0.14em] text-[var(--color-text-main)] uppercase outline-none"
                  >
                    {PIPELINE_FAMILIES.map((f) => (
                      <option key={f} value={f} className="bg-slate-900">
                        {f}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="ui-panel-soft flex items-center gap-2.5 rounded-lg px-3 py-2">
                  <span className="ui-type-mono-meta text-[9px] font-black text-[var(--color-accent-orange)] opacity-70">Variant</span>
                  <select
                    value={selectedVariant || ""}
                    onChange={(e) => setSelectedVariant(e.target.value || null)}
                    className="ui-focus-ring min-w-[140px] cursor-pointer bg-transparent text-[11px] font-bold tracking-[0.14em] text-[var(--color-text-main)] uppercase outline-none"
                  >
                    <option value="" className="bg-slate-900 opacity-50">
                      -- SELECT --
                    </option>
                    {variants.map((v) => (
                      <option key={v} value={v} className="bg-slate-900">
                        {v}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            )}
          </div>

          <div className="mono ui-type-meta hidden sm:block">
            SYSTEM_RECOVERY: SUCCESS
          </div>
        </div>
      </header>

      {/* Main View Area */}
      <main className="flex-grow overflow-hidden">
        {currentView === "home" && (
            <div className="flex h-full flex-col gap-4 overflow-y-auto px-3 pb-4 pt-3 xl:flex-row xl:gap-5 xl:overflow-hidden xl:px-5 xl:pb-5 xl:pt-4">
                <HexGrid onLaunch={launchAgent} />
                <div className="w-full shrink-0 xl:w-auto">
                    <DashboardList 
                        onSelect={(del) => {
                            setAgentName("WORKING_ITEMS");
                            setInitialWorkbenchPath(del.path + "/_STATUS.md");
                            setCurrentView("workbench");
                        }}
                        onOpenProjectRootPicker={() => setShowDirPicker(true)}
                        projectRoot={projectRoot}
                    />
                </div>
            </div>
        )}
        {currentView === "workbench" && (
          <WorkbenchView 
            agentName={agentName} 
            initialPath={initialWorkbenchPath} 
            projectRoot={projectRoot} 
            onNavigateHome={() => setCurrentView("home")}
            onRootChange={handleRootChange}
          />
        )}
        {currentView === "session" && (
          <DirectLinkView 
            projectRoot={projectRoot} 
            onNavigateHome={() => setCurrentView("home")}
            onRootChange={handleRootChange}
          />
        )}
        {currentView === "pipeline" && (
          <PipelineView 
            family={pipelineFamily} 
            selectedVariant={selectedVariant} 
            projectRoot={projectRoot} 
            onNavigateHome={() => setCurrentView("home")}
            onRootChange={handleRootChange}
          />
        )}
      </main>
    </div>
  );
}
