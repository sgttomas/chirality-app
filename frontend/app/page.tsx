"use client";

import { useState, useEffect, useCallback } from "react";
import Image from "next/image";
import { HexGrid } from "@/components/HexGrid";
import { DashboardList } from "@/components/DashboardList";
import type { Deliverable } from "@/components/DashboardList";
import { WorkbenchView } from "@/components/WorkbenchView";
import { PipelineView } from "@/components/PipelineView";
import { DirectLinkView } from "@/components/DirectLinkView";
import { DirectoryPicker } from "@/components/DirectoryPicker";
import chiralityAppIcon from "@/electron/icons/icon.png";

type View = "home" | "workbench" | "session" | "pipeline";
const THEME_STORAGE_KEY = "chirality_theme_mode";

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
    "AUDIT*": ["AUDIT_AGENTS", "AUDIT_DEP_CLOSURE"],
};

export default function Home() {
  const [currentView, setCurrentView] = useState<View>("home");

  // Shared Navigation State
  const [agentName, setAgentName] = useState<string>("WORKING_ITEMS");
  const [pipelineFamily, setPipelineFamily] = useState<string>("PREP*");
  const [selectedVariant, setSelectedVariant] = useState<string | null>(null);
  const [initialWorkbenchPath, setInitialWorkbenchPath] = useState<string | null>(null);

  const [projectRoot, setProjectRoot] = useState<string | null>(null);
  const [isLightMode, setIsLightMode] = useState(() => {
    if (typeof window === "undefined") {
      return false;
    }
    const stored = window.localStorage.getItem(THEME_STORAGE_KEY);
    if (stored === "light") {
      return true;
    }
    if (stored === "dark") {
      return false;
    }
    return window.matchMedia("(prefers-color-scheme: light)").matches;
  });
  const [showDirPicker, setShowDirPicker] = useState(false);
  const [isUpdateAvailable, setIsUpdateAvailable] = useState(false);
  const [latestReleaseTag, setLatestReleaseTag] = useState<string | null>(null);

  // ---------------------------------------------------------------------------
  // Deliverables — single source of truth, fetched at page level.
  // Derived from projectRoot; both PORTAL DashboardList and PIPELINE TASK*
  // variants consume this state.
  // ---------------------------------------------------------------------------
  const [deliverables, setDeliverables] = useState<Deliverable[]>([]);
  const [deliverablesLoading, setDeliverablesLoading] = useState(false);
  const clearDeliverableVariantIfStaleKey = useCallback(() => {
    setSelectedVariant((prev) => (prev?.includes("::") ? null : prev));
  }, []);

  useEffect(() => {
    if (!projectRoot) {
      // No root → no deliverables. queueMicrotask avoids synchronous setState in effect body.
      queueMicrotask(() => {
        setDeliverables([]);
        setDeliverablesLoading(false);
        clearDeliverableVariantIfStaleKey();
      });
      return;
    }

    const controller = new AbortController();
    queueMicrotask(() => setDeliverablesLoading(true));

    fetch(`/api/project/deliverables?path=${encodeURIComponent(projectRoot)}`, {
      signal: controller.signal,
    })
      .then((res) => res.json())
      .then((data) => {
        if (!controller.signal.aborted) {
          const loaded: Deliverable[] = Array.isArray(data.deliverables) ? data.deliverables : [];
          setDeliverables(loaded);

          // Clear stale deliverable variant key if it no longer matches loaded data.
          // Done here (not in a separate effect) to avoid cascading renders.
          setSelectedVariant((prev) => {
            if (!prev?.includes("::")) return prev;
            const exists = loaded.some(d => `${d.pkg}::${d.id}` === prev);
            return exists ? prev : null;
          });
        }
      })
      .catch((err) => {
        if (!controller.signal.aborted) {
          console.error("Failed to load deliverables", err);
          setDeliverables([]);
          clearDeliverableVariantIfStaleKey();
        }
      })
      .finally(() => {
        if (!controller.signal.aborted) {
          setDeliverablesLoading(false);
        }
      });

    return () => controller.abort();
  }, [projectRoot, clearDeliverableVariantIfStaleKey]);

  useEffect(() => {
    const root = document.documentElement;
    root.classList.add("theme-switching");

    const rafId = window.requestAnimationFrame(() => {
      document.body.classList.toggle("light-mode", isLightMode);
      window.setTimeout(() => {
        root.classList.remove("theme-switching");
      }, 0);
    });

    localStorage.setItem(THEME_STORAGE_KEY, isLightMode ? "light" : "dark");

    return () => {
      window.cancelAnimationFrame(rafId);
      root.classList.remove("theme-switching");
    };
  }, [isLightMode]);

  useEffect(() => {
    const savedRoot = sessionStorage.getItem("chirality_project_root");
    if (!savedRoot || !savedRoot.trim()) {
      return;
    }
    queueMicrotask(() => setProjectRoot(savedRoot));
  }, []);

  useEffect(() => {
    let cancelled = false;

    const checkForUpdates = async () => {
      if (!window.chiralityDesktop) {
        return;
      }

      try {
        const result = await window.chiralityDesktop.checkForUpdates();
        if (cancelled || !result.ok) {
          return;
        }

        setIsUpdateAvailable(result.updateAvailable);
        setLatestReleaseTag(result.latestTag ?? null);
      } catch {
        // Keep silent status fallback for transient network failures.
      }
    };

    void checkForUpdates();

    return () => {
      cancelled = true;
    };
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

  // ---------------------------------------------------------------------------
  // Dynamic TASK* variants from deliverables; other families use static FAMILY_MAP
  // ---------------------------------------------------------------------------
  const isTaskFamily = pipelineFamily === "TASK*";
  const taskVariantKeys = deliverables.map(d => `${d.pkg}::${d.id}`);
  const variants = isTaskFamily ? taskVariantKeys : (FAMILY_MAP[pipelineFamily] || []);
  const taskLoading = isTaskFamily && deliverablesLoading;
  const taskEmpty = isTaskFamily && !deliverablesLoading && deliverables.length === 0;
  const taskVariantDisabled = taskLoading || taskEmpty;

  const title = VIEW_TITLE[currentView];

  return (
    <div className="flex h-screen flex-col overflow-hidden">
      {showDirPicker && (
        <DirectoryPicker
          onSelect={(path) => {
            setShowDirPicker(false);
            handleRootChange(path);
          }}
          onCancel={() => setShowDirPicker(false)}
        />
      )}

      {/* Consolidated Unified Header */}
      <header id="unified-header" className="shrink-0 px-3 pt-3 pb-2">
        <div className="mx-auto flex w-full max-w-[1800px] items-center justify-between gap-4 ui-panel px-4 py-2.5 shadow-lg backdrop-blur-md">

          {/* Left: Brand & Page Context */}
          <div className="flex items-center gap-5 min-w-0">
            <div className="flex items-center gap-3">
              <div
                className={`relative flex h-8 w-8 shrink-0 items-center justify-center overflow-hidden rounded-[10px] ring-1 ${
                  isLightMode
                    ? "bg-[var(--color-surface-high)] ring-[var(--color-border)]/75 shadow-sm"
                    : "bg-stone-200/10 ring-white/15 shadow-lg"
                }`}
              >
                <Image
                  src={chiralityAppIcon}
                  alt="Chirality App Icon"
                  width={32}
                  height={32}
                  priority
                  className={`h-full w-full rounded-[10px] object-cover ${
                    isLightMode ? "opacity-100" : "opacity-95"
                  }`}
                />
              </div>
              <a
                href="https://www.chirality.ai"
                target="_blank"
                rel="noopener noreferrer"
                className="text-[1.05rem] font-medium tracking-tight text-[var(--color-text-main)] italic opacity-90 hover:opacity-100 hover:text-[var(--color-accent-text)] transition-all whitespace-nowrap hidden lg:block"
                style={{ fontFamily: 'var(--font-eb)' }}
              >
                Chirality.ai
              </a>
            </div>

            <div className="h-6 w-px bg-[var(--color-border)]/50 hidden md:block" />

            <div className="flex items-center gap-3">
              <div className="ui-type-title whitespace-nowrap font-extrabold tracking-[0.12em] uppercase text-[0.9rem] lg:text-[1rem]">
                {title.lead}
                <span className="px-1 text-[var(--color-text-dim)]">{" // "}</span>
                <span className="text-[var(--color-accent-text)]">{title.accent}</span>
              </div>

              {/* Contextual Selectors (Persona/Family/Variant) */}
              {currentView === "workbench" && (
                <div className="ui-panel-soft flex items-center gap-2.5 px-3 py-1.5 ml-1">
                  <span className="ui-type-mono-meta text-[8px] font-black text-[var(--color-accent-text)] opacity-70">Persona</span>
                  <select
                    value={agentName}
                    onChange={(e) => setAgentName(e.target.value)}
                    className="ui-focus-ring min-w-[140px] cursor-pointer bg-transparent text-[10px] font-bold tracking-[0.14em] text-[var(--color-text-main)] uppercase outline-none"
                  >
                    {PERSONA_AGENTS.map((agent) => (
                      <option key={agent} value={agent} className="bg-[var(--color-surface-sunken)] text-[var(--color-text-main)]">
                        {agent}
                      </option>
                    ))}
                  </select>
                </div>
              )}

              {currentView === "pipeline" && (
                <div className="flex items-center gap-2 ml-1">
                  <div className="ui-panel-soft flex items-center gap-2.5 px-3 py-1.5">
                    <span className="ui-type-mono-meta text-[8px] font-black text-[var(--color-accent-text)] opacity-70">Family</span>
                    <select
                      value={pipelineFamily}
                      onChange={(e) => {
                        setPipelineFamily(e.target.value);
                        setSelectedVariant(null);
                      }}
                      className="ui-focus-ring min-w-[110px] cursor-pointer bg-transparent text-[10px] font-bold tracking-[0.14em] text-[var(--color-text-main)] uppercase outline-none"
                    >
                      {PIPELINE_FAMILIES.map((f) => (
                        <option key={f} value={f} className="bg-[var(--color-surface-sunken)] text-[var(--color-text-main)]">
                          {f}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="ui-panel-soft flex items-center gap-2.5 px-3 py-1.5">
                    <span className="ui-type-mono-meta text-[8px] font-black text-[var(--color-accent-text)] opacity-70">Variant</span>
                    <select
                      value={selectedVariant || ""}
                      onChange={(e) => setSelectedVariant(e.target.value || null)}
                      disabled={taskVariantDisabled}
                      className={`ui-focus-ring min-w-[130px] max-w-[280px] truncate cursor-pointer bg-transparent text-[10px] font-bold tracking-[0.14em] text-[var(--color-text-main)] uppercase outline-none ${
                        taskVariantDisabled ? "opacity-50 cursor-not-allowed" : ""
                      }`}
                    >
                      {taskLoading ? (
                        <option value="" className="bg-[var(--color-surface-sunken)] text-[var(--color-text-dim)]">
                          Loading deliverables...
                        </option>
                      ) : taskEmpty ? (
                        <option value="" className="bg-[var(--color-surface-sunken)] text-[var(--color-text-dim)]">
                          No deliverables — set root in PORTAL
                        </option>
                      ) : (
                        <>
                          <option value="" className="bg-[var(--color-surface-sunken)] text-[var(--color-text-main)] opacity-50">
                            {isTaskFamily ? "-- SELECT DELIVERABLE --" : "-- SELECT --"}
                          </option>
                          {isTaskFamily && deliverables.length > 0
                            ? deliverables.map((d) => (
                                <option
                                  key={`${d.pkg}::${d.id}`}
                                  value={`${d.pkg}::${d.id}`}
                                  className="bg-[var(--color-surface-sunken)] text-[var(--color-text-main)]"
                                >
                                  {d.id} — {d.name} ({d.pkg.replace("PKG-", "")})
                                </option>
                              ))
                            : variants.map((v) => (
                                <option key={v} value={v} className="bg-[var(--color-surface-sunken)] text-[var(--color-text-main)]">
                                  {v}
                                </option>
                              ))
                          }
                        </>
                      )}
                    </select>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Right: Navigation & Options */}
          <div className="flex items-center gap-3">
            {isUpdateAvailable && (
              <div className="mono ui-type-meta hidden xl:block mr-4 text-[9px] text-[var(--color-accent-text)]">
                {`UPDATE AVAILABLE: ${latestReleaseTag ?? "LATEST"}`}
              </div>
            )}

            <div className="flex items-center gap-2">
              {/* Page Select Dropdown */}
              <div className="ui-panel-soft flex items-center gap-2.5 px-3 py-1.5">
                <span className="ui-type-mono-meta text-[8px] font-black text-[var(--color-accent-text)] opacity-70">View</span>
                <select
                  value={currentView}
                  onChange={(e) => setCurrentView(e.target.value as View)}
                  className="ui-focus-ring min-w-[120px] cursor-pointer bg-transparent text-[10px] font-bold tracking-[0.14em] text-[var(--color-text-main)] uppercase outline-none"
                >
                  {VIEW_TABS.map((tab) => (
                    <option key={tab.id} value={tab.id} className="bg-[var(--color-surface-sunken)] text-[var(--color-text-main)]">
                      {tab.label}
                    </option>
                  ))}
                </select>
              </div>

              <div className="h-5 w-px bg-[var(--color-border)]/50 mx-1" />

              <button
                onClick={() => setIsLightMode(!isLightMode)}
                className="ui-control ui-focus-ring cursor-pointer px-3 py-1.5 text-[10px] font-bold tracking-[0.14em] uppercase text-[var(--color-text-dim)] hover:text-[var(--color-text-main)]"
              >
                {isLightMode ? "☾ DARK" : "☀ LIGHT"}
              </button>
            </div>
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
                            setPipelineFamily("TASK*");
                            setSelectedVariant(`${del.pkg}::${del.id}`);
                            setCurrentView("pipeline");
                        }}
                        onOpenProjectRootPicker={() => setShowDirPicker(true)}
                        projectRoot={projectRoot}
                        deliverables={deliverables}
                        loading={deliverablesLoading}
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
            deliverables={deliverables}
          />
        )}
      </main>
    </div>
  );
}
