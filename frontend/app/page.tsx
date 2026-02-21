"use client";

import { useState, useEffect } from "react";
import Image from "next/image";
import { HexGrid, type MatrixLaunchPayload } from "@/components/HexGrid";
import { DashboardList } from "@/components/DashboardList";
import type { Deliverable } from "@/components/DashboardList";
import { WorkbenchView } from "@/components/WorkbenchView";
import { PipelineView } from "@/components/PipelineView";
import { DirectLinkView } from "@/components/DirectLinkView";
import { DirectoryPicker } from "@/components/DirectoryPicker";
import chiralityAppIcon from "@/electron/icons/icon.png";

type View = "home" | "workbench" | "session" | "pipeline";
type PipelineCategory = "DECOMP*" | "PREP*" | "TASK*" | "AUDIT*";
type TaskScopeMode = "DELIVERABLES" | "KNOWLEDGE_TYPES";

type PipelineTypeOption = {
  id: string;
  label: string;
  disabled?: boolean;
};

type KnowledgeTypeOption = {
  id: string;
  label: string;
  matchingDeliverableKeys: string[];
};

type DeliverablesApiResponse = {
  deliverables?: Deliverable[];
  knowledgeDecomposition?: {
    enabled?: boolean;
    markerFile?: string | null;
  };
  knowledgeTypes?: KnowledgeTypeOption[];
};

const THEME_STORAGE_KEY = "chirality_theme_mode";

const WORKBENCH_AGENTS = [
  "HELP",
  "ORCHESTRATE",
  "WORKING_ITEMS",
  "AGGREGATE",
  "AGENTS",
  "DEPENDENCIES",
  "CHANGE",
  "RECONCILING",
] as const;

const PIPELINE_CATEGORIES: PipelineCategory[] = ["DECOMP*", "PREP*", "TASK*", "AUDIT*"];

const PIPELINE_TYPE_OPTIONS: Record<PipelineCategory, PipelineTypeOption[]> = {
  "DECOMP*": [
    { id: "SOFTWARE", label: "SOFTWARE" },
    { id: "PROJECT", label: "PROJECT" },
    { id: "DOMAIN", label: "DOMAIN" },
    { id: "BASE", label: "BASE (create new)" },
  ],
  "PREP*": [
    { id: "PREPARATION", label: "PREPARATION" },
    { id: "4_DOCUMENTS", label: "4_DOCUMENTS" },
    { id: "CHIRALITY_FRAMEWORK", label: "CHIRALITY_FRAMEWORK" },
    { id: "CHIRALITY_LENS", label: "CHIRALITY_LENS" },
  ],
  "TASK*": [
    { id: "SCOPE_CHANGE", label: "SCOPE_CHANGE" },
    { id: "SCOPE_PREP", label: "SCOPE_PREP", disabled: true },
    { id: "ESTIMATE_PREP", label: "ESTIMATE_PREP" },
    { id: "AUDIT_PREP", label: "AUDIT_PREP", disabled: true },
    { id: "SCHEDULE_PREP", label: "SCHEDULE_PREP", disabled: true },
    { id: "ESTIMATING", label: "ESTIMATING" },
    { id: "SCHEDULING", label: "SCHEDULING" },
  ],
  "AUDIT*": [
    { id: "AGENTS", label: "AGENTS" },
    { id: "DEPENDENCIES", label: "DEPENDENCIES" },
    { id: "ESTIMATES", label: "ESTIMATES", disabled: true },
    { id: "REFERENCES", label: "REFERENCES", disabled: true },
    { id: "SCHEDULES", label: "SCHEDULES", disabled: true },
    { id: "SCOPE", label: "SCOPE" },
  ],
};

const VIEW_TABS: Array<{ id: View; label: string }> = [
  { id: "home", label: "PORTAL" },
  { id: "workbench", label: "WORKBENCH" },
  { id: "pipeline", label: "PIPELINE" },
  { id: "session", label: "DIRECT" },
];

const VIEW_TITLE: Record<View, { lead: string; accent: string }> = {
  home: { lead: "COMMAND", accent: "PORTAL" },
  workbench: { lead: "WORK", accent: "BENCH" },
  session: { lead: "DIRECT", accent: "LINK" },
  pipeline: { lead: "TASK", accent: "PIPELINE" },
};

function getDefaultPipelineType(category: PipelineCategory): string | null {
  const firstEnabled = PIPELINE_TYPE_OPTIONS[category].find((option) => !option.disabled);
  return firstEnabled?.id ?? null;
}

export default function Home() {
  const [currentView, setCurrentView] = useState<View>("home");

  const [agentName, setAgentName] = useState<string>("WORKING_ITEMS");
  const [pipelineCategory, setPipelineCategory] = useState<PipelineCategory>("PREP*");
  const [pipelineType, setPipelineType] = useState<string | null>(getDefaultPipelineType("PREP*"));
  const [taskScopeMode, setTaskScopeMode] = useState<TaskScopeMode>("DELIVERABLES");
  const [taskScopeValue, setTaskScopeValue] = useState<string | null>(null);
  const [taskKnowledgeTargetDeliverable, setTaskKnowledgeTargetDeliverable] = useState<string | null>(null);
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

  const [deliverables, setDeliverables] = useState<Deliverable[]>([]);
  const [deliverablesLoading, setDeliverablesLoading] = useState(false);
  const [knowledgeDecompositionEnabled, setKnowledgeDecompositionEnabled] = useState(false);
  const [knowledgeDecompositionMarker, setKnowledgeDecompositionMarker] = useState<string | null>(null);
  const [knowledgeTypes, setKnowledgeTypes] = useState<KnowledgeTypeOption[]>([]);

  useEffect(() => {
    if (!projectRoot) {
      queueMicrotask(() => {
        setDeliverables([]);
        setDeliverablesLoading(false);
        setKnowledgeDecompositionEnabled(false);
        setKnowledgeDecompositionMarker(null);
        setKnowledgeTypes([]);
      });
      return;
    }

    const controller = new AbortController();
    queueMicrotask(() => setDeliverablesLoading(true));

    fetch(`/api/project/deliverables?path=${encodeURIComponent(projectRoot)}`, {
      signal: controller.signal,
    })
      .then((res) => res.json())
      .then((data: DeliverablesApiResponse) => {
        if (controller.signal.aborted) {
          return;
        }

        const loaded: Deliverable[] = Array.isArray(data.deliverables) ? data.deliverables : [];
        setDeliverables(loaded);

        const decomposition = data.knowledgeDecomposition ?? {};
        setKnowledgeDecompositionEnabled(Boolean(decomposition.enabled));
        setKnowledgeDecompositionMarker(typeof decomposition.markerFile === "string" ? decomposition.markerFile : null);

        const loadedKnowledgeTypes = Array.isArray(data.knowledgeTypes)
          ? data.knowledgeTypes.filter((entry) => {
              return (
                entry &&
                typeof entry.id === "string" &&
                typeof entry.label === "string" &&
                Array.isArray(entry.matchingDeliverableKeys)
              );
            })
          : [];
        setKnowledgeTypes(loadedKnowledgeTypes);
      })
      .catch((err) => {
        if (!controller.signal.aborted) {
          console.error("Failed to load deliverables", err);
          setDeliverables([]);
          setKnowledgeDecompositionEnabled(false);
          setKnowledgeDecompositionMarker(null);
          setKnowledgeTypes([]);
        }
      })
      .finally(() => {
        if (!controller.signal.aborted) {
          setDeliverablesLoading(false);
        }
      });

    return () => controller.abort();
  }, [projectRoot]);

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

  const pipelineTypeOptions = PIPELINE_TYPE_OPTIONS[pipelineCategory];
  const activePipelineType =
    pipelineType && pipelineTypeOptions.some((option) => option.id === pipelineType && !option.disabled)
      ? pipelineType
      : getDefaultPipelineType(pipelineCategory);

  const deliverableKeyToDeliverable = new Map<string, Deliverable>(
    deliverables.map((deliverable) => [`${deliverable.pkg}::${deliverable.id}`, deliverable]),
  );

  const effectiveTaskScopeMode: TaskScopeMode = knowledgeDecompositionEnabled ? taskScopeMode : "DELIVERABLES";
  const deliverableScopeOptions = deliverables.map((deliverable) => ({
    id: `${deliverable.pkg}::${deliverable.id}`,
    label: `${deliverable.id} — ${deliverable.name} (${deliverable.pkg.replace("PKG-", "")})`,
  }));
  const knowledgeScopeOptions = knowledgeTypes.map((knowledgeType) => ({
    id: knowledgeType.id,
    label: knowledgeType.label,
  }));

  const rawTaskScopeOptions =
    effectiveTaskScopeMode === "DELIVERABLES" ? deliverableScopeOptions : knowledgeScopeOptions;
  const activeTaskScopeValue =
    taskScopeValue && rawTaskScopeOptions.some((option) => option.id === taskScopeValue) ? taskScopeValue : null;

  const selectedKnowledgeType =
    effectiveTaskScopeMode === "KNOWLEDGE_TYPES" && activeTaskScopeValue
      ? knowledgeTypes.find((knowledgeType) => knowledgeType.id === activeTaskScopeValue) ?? null
      : null;

  const knowledgeTargetDeliverables = selectedKnowledgeType
    ? selectedKnowledgeType.matchingDeliverableKeys
        .map((key) => {
          const deliverable = deliverableKeyToDeliverable.get(key);
          if (!deliverable) {
            return null;
          }
          return {
            key,
            label: `${deliverable.id} — ${deliverable.name} (${deliverable.pkg.replace("PKG-", "")})`,
          };
        })
        .filter((entry): entry is { key: string; label: string } => entry !== null)
    : [];

  const activeTaskKnowledgeTarget =
    taskKnowledgeTargetDeliverable && knowledgeTargetDeliverables.some((entry) => entry.key === taskKnowledgeTargetDeliverable)
      ? taskKnowledgeTargetDeliverable
      : null;

  const launchFromMatrix = (payload: MatrixLaunchPayload) => {
    if (payload.launchTarget === "workbench") {
      setAgentName(payload.label);
      setInitialWorkbenchPath(null);
      setCurrentView("workbench");
      return;
    }

    const nextCategory = payload.label as PipelineCategory;
    if (!PIPELINE_CATEGORIES.includes(nextCategory)) {
      return;
    }

    setPipelineCategory(nextCategory);
    setPipelineType(getDefaultPipelineType(nextCategory));
    setTaskScopeMode("DELIVERABLES");
    setTaskScopeValue(null);
    setTaskKnowledgeTargetDeliverable(null);
    setCurrentView("pipeline");
  };

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

      <header id="unified-header" className="shrink-0 px-3 pt-3 pb-2">
        <div className="mx-auto flex w-full max-w-[1800px] items-center justify-between gap-4 ui-panel px-4 py-2.5 shadow-lg backdrop-blur-md">
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
                  className={`h-full w-full rounded-[10px] object-cover ${isLightMode ? "opacity-100" : "opacity-95"}`}
                />
              </div>
              <a
                href="https://www.chirality.ai"
                target="_blank"
                rel="noopener noreferrer"
                className="text-[1.05rem] font-medium tracking-tight text-[var(--color-text-main)] italic opacity-90 hover:opacity-100 hover:text-[var(--color-accent-text)] transition-all whitespace-nowrap hidden lg:block"
                style={{ fontFamily: "var(--font-eb)" }}
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

              {currentView === "workbench" && (
                <div className="ui-panel-soft flex items-center gap-2.5 px-3 py-1.5 ml-1">
                  <span className="ui-type-mono-meta text-[8px] font-black text-[var(--color-accent-text)] opacity-70">Agent</span>
                  <select
                    value={agentName}
                    onChange={(e) => setAgentName(e.target.value)}
                    className="ui-focus-ring min-w-[160px] cursor-pointer bg-transparent text-[10px] font-bold tracking-[0.14em] text-[var(--color-text-main)] uppercase outline-none"
                  >
                    {WORKBENCH_AGENTS.map((agent) => (
                      <option key={agent} value={agent} className="bg-[var(--color-surface-sunken)] text-[var(--color-text-main)]">
                        {agent}
                      </option>
                    ))}
                  </select>
                </div>
              )}

              {currentView === "pipeline" && (
                <div className="flex flex-wrap items-center gap-2 ml-1">
                  <div className="ui-panel-soft flex items-center gap-2.5 px-3 py-1.5">
                    <span className="ui-type-mono-meta text-[8px] font-black text-[var(--color-accent-text)] opacity-70">Category</span>
                    <select
                      value={pipelineCategory}
                      onChange={(e) => {
                        const nextCategory = e.target.value as PipelineCategory;
                        setPipelineCategory(nextCategory);
                        setPipelineType(getDefaultPipelineType(nextCategory));
                        setTaskScopeValue(null);
                        setTaskKnowledgeTargetDeliverable(null);
                      }}
                      className="ui-focus-ring min-w-[120px] cursor-pointer bg-transparent text-[10px] font-bold tracking-[0.14em] text-[var(--color-text-main)] uppercase outline-none"
                    >
                      {PIPELINE_CATEGORIES.map((category) => (
                        <option key={category} value={category} className="bg-[var(--color-surface-sunken)] text-[var(--color-text-main)]">
                          {category}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="ui-panel-soft flex items-center gap-2.5 px-3 py-1.5">
                    <span className="ui-type-mono-meta text-[8px] font-black text-[var(--color-accent-text)] opacity-70">
                      {pipelineCategory === "TASK*" ? "Task Agent" : "Type"}
                    </span>
                    <select
                      value={activePipelineType ?? ""}
                      onChange={(e) => setPipelineType(e.target.value || null)}
                      className="ui-focus-ring min-w-[180px] cursor-pointer bg-transparent text-[10px] font-bold tracking-[0.14em] text-[var(--color-text-main)] uppercase outline-none"
                    >
                      {pipelineTypeOptions.map((option) => (
                        <option
                          key={option.id}
                          value={option.id}
                          disabled={option.disabled}
                          className="bg-[var(--color-surface-sunken)] text-[var(--color-text-main)]"
                        >
                          {option.disabled ? `${option.label} (coming soon)` : option.label}
                        </option>
                      ))}
                    </select>
                  </div>

                  {pipelineCategory === "TASK*" && (
                    <>
                      <div className="ui-panel-soft flex items-center gap-2.5 px-3 py-1.5">
                        <span className="ui-type-mono-meta text-[8px] font-black text-[var(--color-accent-text)] opacity-70">Scope Mode</span>
                        <select
                          value={effectiveTaskScopeMode}
                          onChange={(e) => {
                            setTaskScopeMode(e.target.value as TaskScopeMode);
                            setTaskScopeValue(null);
                            setTaskKnowledgeTargetDeliverable(null);
                          }}
                          className="ui-focus-ring min-w-[150px] cursor-pointer bg-transparent text-[10px] font-bold tracking-[0.14em] text-[var(--color-text-main)] uppercase outline-none"
                        >
                          <option value="DELIVERABLES" className="bg-[var(--color-surface-sunken)] text-[var(--color-text-main)]">
                            DELIVERABLES
                          </option>
                          {knowledgeDecompositionEnabled && (
                            <option value="KNOWLEDGE_TYPES" className="bg-[var(--color-surface-sunken)] text-[var(--color-text-main)]">
                              KNOWLEDGE_TYPES
                            </option>
                          )}
                        </select>
                      </div>

                      <div className="ui-panel-soft flex items-center gap-2.5 px-3 py-1.5">
                        <span className="ui-type-mono-meta text-[8px] font-black text-[var(--color-accent-text)] opacity-70">Scope</span>
                        <select
                          value={activeTaskScopeValue ?? ""}
                          onChange={(e) => {
                            setTaskScopeValue(e.target.value || null);
                            if (effectiveTaskScopeMode === "KNOWLEDGE_TYPES") {
                              setTaskKnowledgeTargetDeliverable(null);
                            }
                          }}
                          disabled={deliverablesLoading || rawTaskScopeOptions.length === 0}
                          className={`ui-focus-ring min-w-[220px] max-w-[340px] truncate cursor-pointer bg-transparent text-[10px] font-bold tracking-[0.14em] text-[var(--color-text-main)] uppercase outline-none ${
                            deliverablesLoading || rawTaskScopeOptions.length === 0 ? "opacity-50 cursor-not-allowed" : ""
                          }`}
                        >
                          {deliverablesLoading ? (
                            <option value="" className="bg-[var(--color-surface-sunken)] text-[var(--color-text-dim)]">
                              Loading scope...
                            </option>
                          ) : rawTaskScopeOptions.length === 0 ? (
                            <option value="" className="bg-[var(--color-surface-sunken)] text-[var(--color-text-dim)]">
                              {effectiveTaskScopeMode === "DELIVERABLES"
                                ? "No deliverables — set root in PORTAL"
                                : knowledgeDecompositionEnabled
                                  ? "No knowledge types detected"
                                  : "Knowledge types unavailable"}
                            </option>
                          ) : (
                            <>
                              <option value="" className="bg-[var(--color-surface-sunken)] text-[var(--color-text-main)] opacity-60">
                                -- SELECT --
                              </option>
                              {rawTaskScopeOptions.map((option) => (
                                <option
                                  key={option.id}
                                  value={option.id}
                                  className="bg-[var(--color-surface-sunken)] text-[var(--color-text-main)]"
                                >
                                  {option.label}
                                </option>
                              ))}
                            </>
                          )}
                        </select>
                      </div>

                      {effectiveTaskScopeMode === "KNOWLEDGE_TYPES" && (
                        <div className="ui-panel-soft flex items-center gap-2.5 px-3 py-1.5">
                          <span className="ui-type-mono-meta text-[8px] font-black text-[var(--color-accent-text)] opacity-70">Target Deliverable</span>
                          <select
                            value={activeTaskKnowledgeTarget ?? ""}
                            onChange={(e) => setTaskKnowledgeTargetDeliverable(e.target.value || null)}
                            disabled={knowledgeTargetDeliverables.length === 0}
                            className={`ui-focus-ring min-w-[240px] max-w-[360px] truncate cursor-pointer bg-transparent text-[10px] font-bold tracking-[0.14em] text-[var(--color-text-main)] uppercase outline-none ${
                              knowledgeTargetDeliverables.length === 0 ? "opacity-50 cursor-not-allowed" : ""
                            }`}
                          >
                            {knowledgeTargetDeliverables.length === 0 ? (
                              <option value="" className="bg-[var(--color-surface-sunken)] text-[var(--color-text-dim)]">
                                Select knowledge type first
                              </option>
                            ) : (
                              <>
                                <option value="" className="bg-[var(--color-surface-sunken)] text-[var(--color-text-main)] opacity-60">
                                  -- SELECT DELIVERABLE --
                                </option>
                                {knowledgeTargetDeliverables.map((entry) => (
                                  <option
                                    key={entry.key}
                                    value={entry.key}
                                    className="bg-[var(--color-surface-sunken)] text-[var(--color-text-main)]"
                                  >
                                    {entry.label}
                                  </option>
                                ))}
                              </>
                            )}
                          </select>
                        </div>
                      )}
                    </>
                  )}
                </div>
              )}
            </div>
          </div>

          <div className="flex items-center gap-3">
            {isUpdateAvailable && (
              <div className="mono ui-type-meta hidden xl:block mr-4 text-[9px] text-[var(--color-accent-text)]">
                {`UPDATE AVAILABLE: ${latestReleaseTag ?? "LATEST"}`}
              </div>
            )}

            <div className="flex items-center gap-2">
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

      <main className="flex-grow overflow-hidden">
        {currentView === "home" && (
          <div className="flex h-full flex-col gap-4 overflow-y-auto px-3 pb-4 pt-3 xl:flex-row xl:gap-5 xl:overflow-hidden xl:px-5 xl:pb-5 xl:pt-4">
            <HexGrid onLaunch={launchFromMatrix} />
            <div className="w-full shrink-0 xl:w-auto">
              <DashboardList
                onSelect={(deliverable) => {
                  setPipelineCategory("TASK*");
                  setPipelineType(getDefaultPipelineType("TASK*"));
                  setTaskScopeMode("DELIVERABLES");
                  setTaskScopeValue(`${deliverable.pkg}::${deliverable.id}`);
                  setTaskKnowledgeTargetDeliverable(null);
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
            category={pipelineCategory}
            pipelineType={activePipelineType}
            taskScopeMode={pipelineCategory === "TASK*" ? effectiveTaskScopeMode : null}
            taskScopeValue={pipelineCategory === "TASK*" ? activeTaskScopeValue : null}
            taskKnowledgeTargetDeliverable={pipelineCategory === "TASK*" ? activeTaskKnowledgeTarget : null}
            projectRoot={projectRoot}
            onNavigateHome={() => setCurrentView("home")}
            onRootChange={handleRootChange}
            deliverables={deliverables}
            knowledgeTypes={knowledgeTypes}
          />
        )}
      </main>

      {currentView === "pipeline" && pipelineCategory === "TASK*" && !knowledgeDecompositionEnabled && (
        <div className="px-5 pb-2">
          <p className="mono text-[10px] uppercase tracking-[0.1em] text-[var(--color-text-dim)]/75">
            Knowledge type scope unavailable: no decomposition marker detected.
          </p>
          {knowledgeDecompositionMarker && (
            <p className="mono text-[10px] text-[var(--color-text-dim)]/65">Marker file: {knowledgeDecompositionMarker}</p>
          )}
        </div>
      )}
    </div>
  );
}
