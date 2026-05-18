"use client";

import React, { useMemo, useState } from "react";
import { FileTree } from "./FileTree";
import { ResizableLayout } from "./ResizableLayout";
import type { Deliverable } from "./DashboardList";

type PipelineCategory = "DECOMP*" | "PREP*" | "TASK*" | "AUDIT*";
type TaskScopeMode = "DELIVERABLES" | "KNOWLEDGE_TYPES";

type KnowledgeTypeOption = {
  id: string;
  label: string;
  matchingDeliverableKeys: string[];
};

interface PipelineViewProps {
  category: PipelineCategory;
  pipelineType: string | null;
  taskScopeMode: TaskScopeMode | null;
  taskScopeValue: string | null;
  taskKnowledgeTargetDeliverable: string | null;
  projectRoot: string | null;
  onNavigateHome?: () => void;
  onRootChange?: (path: string) => void;
  deliverables?: Deliverable[];
  knowledgeTypes?: KnowledgeTypeOption[];
}

const STATIC_PIPELINE_PERSONA_MAPPING: Record<string, { personaId: string; fileName: string }> = {
  "DECOMP*:SOFTWARE": { personaId: "SOFTWARE_DECOMP", fileName: "AGENT_SOFTWARE_DECOMP.md" },
  "DECOMP*:PROJECT": { personaId: "PROJECT_DECOMP", fileName: "AGENT_PROJECT_DECOMP.md" },
  "DECOMP*:DOMAIN": { personaId: "DOMAIN_DECOMP", fileName: "AGENT_DOMAIN_DECOMP.md" },
  "DECOMP*:BASE": { personaId: "DECOMP_BASE", fileName: "AGENT_DECOMP_BASE.md" },

  "PREP*:PREPARATION": { personaId: "PREPARATION", fileName: "AGENT_PREPARATION.md" },
  "PREP*:4_DOCUMENTS": { personaId: "4_DOCUMENTS", fileName: "AGENT_4_DOCUMENTS.md" },
  "PREP*:CHIRALITY_FRAMEWORK": { personaId: "CHIRALITY_FRAMEWORK", fileName: "AGENT_CHIRALITY_FRAMEWORK.md" },
  "PREP*:CHIRALITY_LENS": { personaId: "CHIRALITY_LENS", fileName: "AGENT_CHIRALITY_LENS.md" },

  "TASK*:SCOPE_CHANGE": { personaId: "SCOPE_CHANGE", fileName: "AGENT_SCOPE_CHANGE.md" },
  "TASK*:ESTIMATE_PREP": { personaId: "ESTIMATE_PREP", fileName: "AGENT_ESTIMATE_PREP.md" },
  "TASK*:ESTIMATING": { personaId: "ESTIMATING", fileName: "AGENT_ESTIMATING.md" },
  "TASK*:SCHEDULING": { personaId: "SCHEDULING", fileName: "AGENT_SCHEDULING.md" },

  "AUDIT*:AGENTS": { personaId: "AUDIT_AGENTS", fileName: "AGENT_AUDIT_AGENTS.md" },
  "AUDIT*:DEPENDENCIES": { personaId: "AUDIT_DEP_CLOSURE", fileName: "AGENT_AUDIT_DEP_CLOSURE.md" },
  "AUDIT*:SCOPE": { personaId: "AUDIT_DECOMP", fileName: "AGENT_AUDIT_DECOMP.md" },
};

function toSessionToken(value: string): string {
  return value.replace(/[^A-Za-z0-9_]+/g, "_");
}

export function PipelineView({
  category,
  pipelineType,
  taskScopeMode,
  taskScopeValue,
  taskKnowledgeTargetDeliverable,
  projectRoot,
  onNavigateHome,
  onRootChange,
  deliverables,
  knowledgeTypes,
}: PipelineViewProps) {
  const [selectedFile, setSelectedFile] = useState<string | null>(null);

  const deliverableLookup = useMemo(() => {
    return new Map((deliverables ?? []).map((deliverable) => [`${deliverable.pkg}::${deliverable.id}`, deliverable]));
  }, [deliverables]);

  const selectedKnowledgeType =
    category === "TASK*" && taskScopeMode === "KNOWLEDGE_TYPES" && taskScopeValue
      ? knowledgeTypes?.find((knowledgeType) => knowledgeType.id === taskScopeValue) ?? null
      : null;

  const scopedDeliverable =
    category === "TASK*" && taskScopeMode === "DELIVERABLES" && taskScopeValue
      ? deliverableLookup.get(taskScopeValue) ?? null
      : category === "TASK*" && taskScopeMode === "KNOWLEDGE_TYPES" && taskKnowledgeTargetDeliverable
        ? deliverableLookup.get(taskKnowledgeTargetDeliverable) ?? null
        : null;

  const hasTaskScopeSelection =
    category === "TASK*" &&
    scopedDeliverable &&
    (taskScopeMode === "DELIVERABLES" || (taskScopeMode === "KNOWLEDGE_TYPES" && selectedKnowledgeType));

  const staticKey = pipelineType ? `${category}:${pipelineType}` : null;
  const staticPersonaConfig = staticKey ? STATIC_PIPELINE_PERSONA_MAPPING[staticKey] ?? null : null;

  const personaConfig = hasTaskScopeSelection ? { personaId: "TASK", fileName: "AGENT_TASK.md" } : staticPersonaConfig;

  const autoPrompt = hasTaskScopeSelection
    ? [
        `Read agents/AGENT_TASK.md and initialize according to those instructions.`,
        ``,
        `DeliverablePath: "${scopedDeliverable.path}"`,
        `ApplyEdits: false`,
        `UseSemanticLensing: false`,
        ...(taskScopeMode === "KNOWLEDGE_TYPES" && selectedKnowledgeType
          ? [`ScopeMode: KNOWLEDGE_TYPE`, `KnowledgeType: ${selectedKnowledgeType.label}`]
          : []),
      ].join("\n")
    : staticPersonaConfig
      ? `Read agents/${staticPersonaConfig.fileName} and prepare to execute the pipeline according to those instructions.`
      : null;

  const displayName = hasTaskScopeSelection
    ? taskScopeMode === "KNOWLEDGE_TYPES" && selectedKnowledgeType
      ? `${selectedKnowledgeType.label} :: ${scopedDeliverable.id}`
      : `${scopedDeliverable.id} — ${scopedDeliverable.name}`
    : pipelineType || category;

  const sessionId = hasTaskScopeSelection
    ? taskScopeMode === "KNOWLEDGE_TYPES" && selectedKnowledgeType
      ? `pipeline_TASK_KNOWLEDGE_${toSessionToken(selectedKnowledgeType.id)}_${toSessionToken(scopedDeliverable.pkg)}_${toSessionToken(scopedDeliverable.id)}`
      : `pipeline_TASK_SCOPE_${toSessionToken(scopedDeliverable.pkg)}_${toSessionToken(scopedDeliverable.id)}`
    : `pipeline_${toSessionToken(category)}_${toSessionToken(pipelineType || "none")}`;

  return (
    <ResizableLayout
      key={sessionId}
      agentName={displayName}
      sessionId={sessionId}
      autoPrompt={autoPrompt}
      selectedFile={selectedFile}
      placeholder="Execute command..."
      harnessMode="pipeline"
      personaId={personaConfig?.personaId ?? null}
      projectRoot={projectRoot}
      onNavigateHome={onNavigateHome}
      onRootChange={onRootChange}
      sidebarContent={() => (
        <>
          <div className="panel-label shrink-0 ui-panel-soft rounded-none border-t-0 border-x-0 px-4 py-3.5">
            <div className="flex items-center justify-between gap-3">
              <div className="min-w-0">
                <span className="block text-[10px] font-mono tracking-[0.2em] uppercase text-[var(--color-accent-directory)]">
                  Project Directory
                </span>
                <span className="mono mt-1 block truncate text-[9px] uppercase tracking-[0.12em] text-[var(--color-text-dim)]/85">
                  Pipeline scope // git tracked
                </span>
              </div>
              <span className="h-2 w-2 shrink-0 rounded-full bg-green-500 shadow-[0_0_10px_#22c55e]" />
            </div>
          </div>

          <div className="flex-grow overflow-y-auto p-2 min-h-0 custom-scrollbar">
            <FileTree onFileSelect={setSelectedFile} className="h-full" rootPath={projectRoot} />
          </div>
        </>
      )}
    />
  );
}
