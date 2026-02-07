"use client";

import { useState } from "react";
import { HexGrid } from "@/components/HexGrid";
import { DashboardList } from "@/components/DashboardList";
import { WorkbenchView } from "@/components/WorkbenchView";
import { PipelineView } from "@/components/PipelineView";
import { DirectLinkView } from "@/components/DirectLinkView";

type View = "home" | "workbench" | "session" | "pipeline";

export default function Home() {
  const [currentView, setCurrentView] = useState<View>("home");
  const [agentFamily, setAgentFamily] = useState<string | null>(null);
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);

  const launchAgent = (name: string, tier: string, type: "persona" | "task") => {
    // List of items mapping to Workbench
    const workbenchItems = [
        "DECOMP", "ORCHESTRATE", "WORKING_ITEMS", "AGGREGATE", 
        "HELP", "AGENTS", "CHANGE", "DEPENDENCIES", "RECONCILING"
    ];

    setSelectedAgent(name);

    if (workbenchItems.includes(name)) {
      setCurrentView("workbench");
    } else {
      setAgentFamily(name); // e.g. "PREP*"
      setCurrentView("pipeline");
    }
  };

  const renderView = () => {
    switch (currentView) {
      case "home":
        return (
          <div className="flex-grow flex p-5 gap-5 overflow-hidden">
            <HexGrid onLaunch={launchAgent} />
            <div className="shrink-0">
              <DashboardList onSelect={() => {
                  setSelectedAgent("WORKING_ITEMS");
                  setCurrentView("workbench");
              }} />
            </div>
          </div>
        );
      case "workbench":
        return (
          <div className="flex-grow p-5 overflow-hidden">
            <WorkbenchView agentName={selectedAgent} />
          </div>
        );
      case "session":
        return (
          <div className="flex-grow p-5 overflow-hidden">
            <DirectLinkView />
          </div>
        );
      case "pipeline":
        return (
          <div className="flex-grow p-5 overflow-hidden">
            <PipelineView family={agentFamily} />
          </div>
        );
      default:
        return null;
    }
  };

  const getHeaderTitle = () => {
    switch (currentView) {
      case "home":
        return <>CHIRALITY // <span className="text-[var(--color-accent-orange)]">COMMAND</span></>;
      case "workbench":
        return <>WORK // <span className="text-[var(--color-accent-orange)]">BENCH</span></>;
      case "session":
        return <>DIRECT // <span className="text-[var(--color-accent-orange)]">LINK</span></>;
      case "pipeline":
        return <>TASK // <span className="text-[var(--color-accent-orange)]">PIPELINE</span></>;
    }
  };

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      {/* Wireframe Controls */}
      <div id="wireframe-controls" className="bg-black/90 border-b border-[var(--color-accent-orange)] p-2.5 text-center z-50 shrink-0">
        <button 
          onClick={() => setCurrentView("home")} 
          className={`bg-transparent text-[var(--color-text-dim)] border border-[var(--color-border)] py-1.5 px-4 mx-1.5 rounded-md cursor-pointer transition-all ${currentView === "home" ? "border-[var(--color-accent-orange)] text-[var(--color-accent-orange)] shadow-[0_0_10px_rgba(249,115,22,0.3)]" : ""}`}
        >
          PORTAL
        </button>
        <button 
          onClick={() => setCurrentView("workbench")} 
          className={`bg-transparent text-[var(--color-text-dim)] border border-[var(--color-border)] py-1.5 px-4 mx-1.5 rounded-md cursor-pointer transition-all ${currentView === "workbench" ? "border-[var(--color-accent-orange)] text-[var(--color-accent-orange)] shadow-[0_0_10px_rgba(249,115,22,0.3)]" : ""}`}
        >
          WORKBENCH
        </button>
        <button 
          onClick={() => setCurrentView("session")} 
          className={`bg-transparent text-[var(--color-text-dim)] border border-[var(--color-border)] py-1.5 px-4 mx-1.5 rounded-md cursor-pointer transition-all ${currentView === "session" ? "border-[var(--color-accent-orange)] text-[var(--color-accent-orange)] shadow-[0_0_10px_rgba(249,115,22,0.3)]" : ""}`}
        >
          DIRECT
        </button>
        <button 
          onClick={() => setCurrentView("pipeline")} 
          className={`bg-transparent text-[var(--color-text-dim)] border border-[var(--color-border)] py-1.5 px-4 mx-1.5 rounded-md cursor-pointer transition-all ${currentView === "pipeline" ? "border-[var(--color-accent-orange)] text-[var(--color-accent-orange)] shadow-[0_0_10px_rgba(249,115,22,0.3)]" : ""}`}
        >
          PIPELINE
        </button>
      </div>

      {/* Header */}
      <header className="flex justify-between items-center p-6 shrink-0">
        <div className="text-3xl font-extrabold tracking-widest uppercase">
          {getHeaderTitle()}
        </div>
        <div className="mono text-sm text-[var(--color-text-dim)] tracking-wider">
          SYSTEM_RECOVERY: SUCCESS
        </div>
      </header>

      {/* Main Content Area */}
      {renderView()}
    </div>
  );
}
