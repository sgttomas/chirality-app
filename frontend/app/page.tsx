"use client";

import { useState, useEffect } from "react";
import { HexGrid } from "@/components/HexGrid";
import { DashboardList } from "@/components/DashboardList";
import { WorkbenchView } from "@/components/WorkbenchView";
import { PipelineView } from "@/components/PipelineView";
import { DirectLinkView } from "@/components/DirectLinkView";

type View = "home" | "workbench" | "session" | "pipeline";

const PERSONA_AGENTS = [
    "DECOMP", "ORCHESTRATE", "WORKING_ITEMS", "AGGREGATE", 
    "HELP", "AGENTS", "DEPENDENCIES", "CHANGE", "RECONCILING"
];

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
  
  const [projectRoot, setProjectRoot] = useState<string | null>(() => {
    if (typeof window === "undefined") {
      return null;
    }
    const savedRoot = sessionStorage.getItem("chirality_project_root");
    return savedRoot && savedRoot.trim() ? savedRoot : null;
  });
  const [isLightMode, setIsLightMode] = useState(false);

  useEffect(() => {
    if (isLightMode) {
      document.body.classList.add("light-mode");
    } else {
      document.body.classList.remove("light-mode");
    }
  }, [isLightMode]);

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

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      {/* Wireframe Controls */}
      <div id="wireframe-controls" className="bg-black/90 border-b border-[var(--color-accent-orange)] p-2.5 text-center z-50 shrink-0">
        <button onClick={() => setCurrentView("home")} className={`bg-transparent text-[var(--color-text-dim)] border border-[var(--color-border)] py-1.5 px-4 mx-1.5 rounded-md cursor-pointer transition-all ${currentView === "home" ? "border-[var(--color-accent-orange)] text-[var(--color-accent-orange)] shadow-[0_0_10px_rgba(249,115,22,0.3)]" : ""}`}>PORTAL</button>
        <button onClick={() => setCurrentView("workbench")} className={`bg-transparent text-[var(--color-text-dim)] border border-[var(--color-border)] py-1.5 px-4 mx-1.5 rounded-md cursor-pointer transition-all ${currentView === "workbench" ? "border-[var(--color-accent-orange)] text-[var(--color-accent-orange)] shadow-[0_0_10px_rgba(249,115,22,0.3)]" : ""}`}>WORKBENCH</button>
        <button onClick={() => setCurrentView("pipeline")} className={`bg-transparent text-[var(--color-text-dim)] border border-[var(--color-border)] py-1.5 px-4 mx-1.5 rounded-md cursor-pointer transition-all ${currentView === "pipeline" ? "border-[var(--color-accent-orange)] text-[var(--color-accent-orange)] shadow-[0_0_10px_rgba(249,115,22,0.3)]" : ""}`}>PIPELINE</button>
        <button onClick={() => setCurrentView("session")} className={`bg-transparent text-[var(--color-text-dim)] border border-[var(--color-border)] py-1.5 px-4 mx-1.5 rounded-md cursor-pointer transition-all ${currentView === "session" ? "border-[var(--color-accent-orange)] text-[var(--color-accent-orange)] shadow-[0_0_10px_rgba(249,115,22,0.3)]" : ""}`}>DIRECT</button>
        <button onClick={() => setIsLightMode(!isLightMode)} className="bg-transparent text-[var(--color-text-dim)] border border-[var(--color-border)] py-1.5 px-4 mx-1.5 rounded-md cursor-pointer hover:text-[var(--color-text-main)] transition-all ml-8">
            {isLightMode ? "☾ DARK" : "☀ LIGHT"}
        </button>
      </div>

      {/* Header */}
      <header className="flex justify-between items-center p-6 shrink-0 bg-black/20">
        <div className="flex items-center gap-8">
            <div className="text-3xl font-extrabold tracking-widest uppercase">
                {currentView === "home" && <>COMMAND // <span className="text-[var(--color-accent-orange)]">PORTAL</span></>}
                {currentView === "workbench" && <>WORK // <span className="text-[var(--color-accent-orange)]">BENCH</span></>}
                {currentView === "session" && <>DIRECT // <span className="text-[var(--color-accent-orange)]">LINK</span></>}
                {currentView === "pipeline" && <>TASK // <span className="text-[var(--color-accent-orange)]">PIPELINE</span></>}
            </div>

            {/* Contextual Selectors in Header */}
            {currentView === "workbench" && (
                <div className="flex items-center gap-3 bg-white/5 border border-white/10 px-4 py-2 rounded-lg ml-4">
                    <span className="text-[9px] font-black tracking-[0.2em] text-[var(--color-accent-orange)] uppercase opacity-60">Persona:</span>
                    <select 
                        value={agentName}
                        onChange={(e) => setAgentName(e.target.value)}
                        className="bg-transparent text-xs font-bold tracking-widest text-[var(--color-text-main)] outline-none cursor-pointer uppercase"
                    >
                        {PERSONA_AGENTS.map(agent => (
                            <option key={agent} value={agent} className="bg-slate-900">{agent}</option>
                        ))}
                    </select>
                </div>
            )}

            {currentView === "pipeline" && (
                <div className="flex items-center gap-6 ml-4">
                    <div className="flex items-center gap-3 bg-white/5 border border-white/10 px-4 py-2 rounded-lg">
                        <span className="text-[9px] font-black tracking-[0.2em] text-[var(--color-accent-orange)] uppercase opacity-60">Family:</span>
                        <select 
                            value={pipelineFamily}
                            onChange={(e) => {
                                setPipelineFamily(e.target.value);
                                setSelectedVariant(null);
                            }}
                            className="bg-transparent text-xs font-bold tracking-widest text-[var(--color-text-main)] outline-none cursor-pointer uppercase"
                        >
                            {PIPELINE_FAMILIES.map(f => (
                                <option key={f} value={f} className="bg-slate-900">{f}</option>
                            ))}
                        </select>
                    </div>

                    <div className="flex items-center gap-3 bg-white/5 border border-white/10 px-4 py-2 rounded-lg">
                        <span className="text-[9px] font-black tracking-[0.2em] text-[var(--color-accent-orange)] uppercase opacity-60">Variant:</span>
                        <select 
                            value={selectedVariant || ""}
                            onChange={(e) => setSelectedVariant(e.target.value || null)}
                            className="bg-transparent text-xs font-bold tracking-widest text-[var(--color-text-main)] outline-none cursor-pointer uppercase min-w-[120px]"
                        >
                            <option value="" className="bg-slate-900 opacity-50">-- SELECT --</option>
                            {variants.map(v => (
                                <option key={v} value={v} className="bg-slate-900">{v}</option>
                            ))}
                        </select>
                    </div>
                </div>
            )}
        </div>

        <div className="mono text-sm text-[var(--color-text-dim)] tracking-wider">
          SYSTEM_RECOVERY: SUCCESS
        </div>
      </header>

      {/* Main View Area */}
      <main className="flex-grow overflow-hidden">
        {currentView === "home" && (
            <div className="flex p-5 gap-5 h-full overflow-hidden">
                <HexGrid onLaunch={launchAgent} />
                <div className="shrink-0">
                    <DashboardList 
                        onSelect={(del) => {
                            setAgentName("WORKING_ITEMS");
                            setInitialWorkbenchPath(del.path + "/_STATUS.md");
                            setCurrentView("workbench");
                        }} 
                        projectRoot={projectRoot}
                        onRootChange={handleRootChange}
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
          />
        )}
        {currentView === "session" && (
          <DirectLinkView 
            projectRoot={projectRoot} 
            onNavigateHome={() => setCurrentView("home")}
          />
        )}
        {currentView === "pipeline" && (
          <PipelineView 
            family={pipelineFamily} 
            selectedVariant={selectedVariant} 
            projectRoot={projectRoot} 
            onNavigateHome={() => setCurrentView("home")}
          />
        )}
      </main>
    </div>
  );
}
