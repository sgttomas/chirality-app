"use client";

import React, { useState, useMemo, useCallback } from "react";

import type { ToolkitOverrides, PartialMessagesSetting, ToolkitWarning } from "@/lib/toolkit-config";
import {
  EMPTY_OVERRIDES,
  countActiveOverrides,
  computeToolkitWarnings,
  normalizeStringArray,
} from "@/lib/toolkit-config";
import ToolkitPresets from "@/components/ToolkitPresets";

// ---------------------------------------------------------------------------
// Props
// ---------------------------------------------------------------------------

export interface ToolkitProps {
  overrides: ToolkitOverrides;
  onChange: (next: ToolkitOverrides) => void;
  isCollapsed: boolean;
  onToggleCollapse: () => void;
  isLoading: boolean;
}

// ---------------------------------------------------------------------------
// Field change helpers
// ---------------------------------------------------------------------------

function updateField<K extends keyof ToolkitOverrides>(
  overrides: ToolkitOverrides,
  field: K,
  value: ToolkitOverrides[K],
): ToolkitOverrides {
  return { ...overrides, [field]: value };
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function FieldLabel({ label, modified }: { label: string; modified: boolean }) {
  return (
    <label
      className={`ui-type-mono-meta mb-1.5 block text-[9px] font-semibold tracking-[0.12em] uppercase ${
        modified ? "text-[var(--color-accent-orange)]/90" : "text-[var(--color-text-dim)]/80"
      }`}
    >
      {label}
    </label>
  );
}

function HelpText({ children }: { children: React.ReactNode }) {
  return <p className="mt-1 text-[10px] leading-[1.4] text-[var(--color-text-dim)]/65">{children}</p>;
}

function WarningBanner({ warnings }: { warnings: ToolkitWarning[] }) {
  if (warnings.length === 0) return null;
  return (
    <div className="mb-3 space-y-1.5">
      {warnings.map((w) => (
        <div
          key={w.code}
          className="toolkit-warning rounded-md border border-amber-500/30 bg-amber-500/10 px-2.5 py-1.5 text-[10px] leading-[1.4] text-amber-300/90"
        >
          {w.message}
        </div>
      ))}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Governance sub-form
// ---------------------------------------------------------------------------

function GovernanceSection({
  overrides,
  onChange,
  disabled,
}: {
  overrides: ToolkitOverrides;
  onChange: (next: ToolkitOverrides) => void;
  disabled: boolean;
}) {
  const [isExpanded, setIsExpanded] = useState(true);
  const gov = overrides.subagentGovernance;
  const hasValues = gov !== undefined;

  const updateGov = useCallback(
    (patch: Partial<NonNullable<ToolkitOverrides["subagentGovernance"]>>) => {
      const current = overrides.subagentGovernance ?? {
        contextSealed: false,
        pipelineRunApproved: false,
        approvalRef: "",
      };
      onChange(updateField(overrides, "subagentGovernance", { ...current, ...patch }));
    },
    [overrides, onChange],
  );

  const clearGovernance = useCallback(() => {
    const next = { ...overrides };
    delete next.subagentGovernance;
    onChange(next);
  }, [overrides, onChange]);

  return (
    <div className={`rounded-lg border ${hasValues ? "toolkit-field-modified border-[var(--color-accent-orange)]/25" : "border-[var(--color-border)]/40"} bg-[var(--color-surface-low)]/30`}>
      <button
        type="button"
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex w-full items-center justify-between px-2.5 py-2 text-left"
        disabled={disabled}
      >
        <span className="mono text-[9px] font-semibold tracking-[0.12em] uppercase text-[var(--color-text-dim)]/80">
          Subagent Governance
        </span>
        <svg
          width="10"
          height="10"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.4"
          strokeLinecap="round"
          strokeLinejoin="round"
          className={`text-[var(--color-text-dim)]/60 transition-transform ${isExpanded ? "rotate-180" : ""}`}
        >
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </button>

      {isExpanded && (
        <div className="space-y-2.5 border-t border-[var(--color-border)]/30 px-2.5 py-2.5">
          {/* Runtime gate notice (TK-007) */}
          <p className="text-[9px] leading-[1.4] text-[var(--color-text-dim)]/55 italic">
            Setting a governance token does not force delegation. Runtime gates still apply: feature flag, persona allowlist, and persona-declared subagents.
          </p>

          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={gov?.contextSealed ?? false}
              onChange={(e) => updateGov({ contextSealed: e.target.checked })}
              disabled={disabled}
              className="ui-focus-ring h-3.5 w-3.5 rounded border-[var(--color-border)] bg-[var(--color-surface-high)] accent-[var(--color-accent-orange)]"
            />
            <span className="mono text-[9px] tracking-[0.08em] text-[var(--color-text-dim)]">contextSealed</span>
          </label>

          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={gov?.pipelineRunApproved ?? false}
              onChange={(e) => updateGov({ pipelineRunApproved: e.target.checked })}
              disabled={disabled}
              className="ui-focus-ring h-3.5 w-3.5 rounded border-[var(--color-border)] bg-[var(--color-surface-high)] accent-[var(--color-accent-orange)]"
            />
            <span className="mono text-[9px] tracking-[0.08em] text-[var(--color-text-dim)]">pipelineRunApproved</span>
          </label>

          <div>
            <FieldLabel label="approvalRef" modified={Boolean(gov?.approvalRef?.trim())} />
            <input
              type="text"
              className="ui-control ui-focus-ring w-full bg-[var(--color-surface-high)] px-2 py-1.5 text-[11px] text-[var(--color-text-main)] placeholder:text-[var(--color-text-dim)]/50"
              placeholder="e.g. PIPELINE-RUN-001"
              value={gov?.approvalRef ?? ""}
              onChange={(e) => updateGov({ approvalRef: e.target.value })}
              disabled={disabled}
            />
          </div>

          <div>
            <FieldLabel label="approvedBy" modified={Boolean(gov?.approvedBy?.trim())} />
            <input
              type="text"
              className="ui-control ui-focus-ring w-full bg-[var(--color-surface-high)] px-2 py-1.5 text-[11px] text-[var(--color-text-main)] placeholder:text-[var(--color-text-dim)]/50"
              placeholder="optional"
              value={gov?.approvedBy ?? ""}
              onChange={(e) => updateGov({ approvedBy: e.target.value })}
              disabled={disabled}
            />
          </div>

          {hasValues && (
            <button
              type="button"
              onClick={clearGovernance}
              disabled={disabled}
              className="mono text-[9px] font-semibold tracking-[0.1em] uppercase text-[var(--color-text-dim)]/60 hover:text-[var(--color-accent-orange)]"
            >
              Clear governance
            </button>
          )}
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

const Toolkit: React.FC<ToolkitProps> = ({
  overrides,
  onChange,
  isCollapsed,
  onToggleCollapse,
  isLoading,
}) => {
  const [showPresets, setShowPresets] = useState(false);

  const activeCount = useMemo(() => countActiveOverrides(overrides), [overrides]);
  const warnings = useMemo(() => computeToolkitWarnings(overrides), [overrides]);

  const disabled = isLoading;

  const handleReset = useCallback(() => {
    onChange({ ...EMPTY_OVERRIDES });
    setShowPresets(false);
  }, [onChange]);

  // --- Collapsed rail ---
  if (isCollapsed) {
    return (
      <aside className="ui-panel-soft flex h-full w-11 shrink-0 flex-col items-center justify-between rounded-xl py-2.5">
        <button
          type="button"
          onClick={onToggleCollapse}
          className="ui-control ui-focus-ring relative flex h-8 w-8 items-center justify-center rounded-md hover:text-[var(--color-accent-orange)]"
          title="Expand toolkit"
        >
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="13 17 8 12 13 7" />
            <polyline points="20 17 15 12 20 7" />
          </svg>
          {activeCount > 0 && (
            <span className="toolkit-active-indicator absolute -right-0.5 -top-0.5 flex h-3.5 w-3.5 items-center justify-center rounded-full bg-[var(--color-accent-orange)] text-[7px] font-bold text-black">
              {activeCount}
            </span>
          )}
        </button>
        <span className="mono text-[8px] font-semibold uppercase tracking-[0.14em] text-[var(--color-text-dim)]/80 [writing-mode:vertical-rl] rotate-180">
          Toolkit
        </span>
        <div className="h-8 w-8" /> {/* Spacer for visual symmetry */}
      </aside>
    );
  }

  // --- Expanded panel ---
  return (
    <aside className="ui-panel-soft flex h-full w-[260px] shrink-0 flex-col overflow-hidden rounded-xl">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-[var(--color-border)]/60 bg-[var(--color-surface-mid)]/72 px-3 py-2.5">
        <div className="flex items-center gap-2">
          <span className="mono text-[9px] font-semibold uppercase tracking-[0.14em] text-[var(--color-accent-orange)]/85">
            Toolkit
          </span>
          {activeCount > 0 && (
            <span className="flex h-4 min-w-4 items-center justify-center rounded-full bg-[var(--color-accent-orange)]/20 px-1 text-[8px] font-bold text-[var(--color-accent-orange)]">
              {activeCount}
            </span>
          )}
        </div>
        <button
          type="button"
          onClick={onToggleCollapse}
          className="ui-control ui-focus-ring flex h-7 w-7 items-center justify-center rounded-md hover:text-[var(--color-accent-orange)]"
          title="Collapse toolkit"
        >
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="11 17 16 12 11 7" />
            <polyline points="4 17 9 12 4 7" />
          </svg>
        </button>
      </div>

      {/* Body */}
      <div className="custom-scrollbar flex-1 space-y-4 overflow-y-auto p-3">
        <WarningBanner warnings={warnings} />

        {/* Model */}
        <div className={overrides.model !== undefined ? "toolkit-field-modified" : ""}>
          <FieldLabel label="Model" modified={overrides.model !== undefined} />
          <input
            type="text"
            className="ui-control ui-focus-ring w-full bg-[var(--color-surface-high)] px-2.5 py-1.5 text-[11px] text-[var(--color-text-main)] placeholder:text-[var(--color-text-dim)]/50"
            placeholder="inherit from persona / CLAUDE.md"
            value={overrides.model ?? ""}
            onChange={(e) => {
              const val = e.target.value;
              onChange(updateField(overrides, "model", val || undefined));
            }}
            disabled={disabled}
          />
          <HelpText>Per-turn model override. Leave empty to inherit.</HelpText>
        </div>

        {/* Max Turns */}
        <div className={overrides.maxTurns !== undefined ? "toolkit-field-modified" : ""}>
          <FieldLabel label="Max Turns" modified={overrides.maxTurns !== undefined} />
          <input
            type="number"
            className="ui-control ui-focus-ring w-full bg-[var(--color-surface-high)] px-2.5 py-1.5 text-[11px] text-[var(--color-text-main)] placeholder:text-[var(--color-text-dim)]/50"
            placeholder="25"
            min={1}
            max={200}
            value={overrides.maxTurns ?? ""}
            onChange={(e) => {
              const val = e.target.value;
              onChange(updateField(overrides, "maxTurns", val ? Number(val) : undefined));
            }}
            disabled={disabled}
          />
          <HelpText>Agentic loops per turn. Default: 25.</HelpText>
        </div>

        {/* Tools */}
        <div className={overrides.tools !== undefined ? "toolkit-field-modified" : ""}>
          <FieldLabel label="Tools" modified={overrides.tools !== undefined} />
          <textarea
            className="ui-control ui-focus-ring w-full resize-y bg-[var(--color-surface-high)] px-2.5 py-1.5 text-[11px] text-[var(--color-text-main)] placeholder:text-[var(--color-text-dim)]/50"
            placeholder='claude_code preset (all tools)'
            rows={2}
            value={overrides.tools ?? ""}
            onChange={(e) => {
              const val = e.target.value;
              onChange(updateField(overrides, "tools", val || undefined));
            }}
            disabled={disabled}
          />
          <HelpText>Comma-separated tool names. Leave empty for default preset.</HelpText>
        </div>

        {/* Disallowed Tools */}
        <div className={overrides.disallowedTools !== undefined && overrides.disallowedTools.length > 0 ? "toolkit-field-modified" : ""}>
          <FieldLabel label="Disallowed Tools" modified={Boolean(overrides.disallowedTools?.length)} />
          <textarea
            className="ui-control ui-focus-ring w-full resize-y bg-[var(--color-surface-high)] px-2.5 py-1.5 text-[11px] text-[var(--color-text-main)] placeholder:text-[var(--color-text-dim)]/50"
            placeholder="e.g. Bash, FileWrite"
            rows={2}
            value={overrides.disallowedTools?.join(", ") ?? ""}
            onChange={(e) => {
              const val = e.target.value;
              const arr = val ? normalizeStringArray(val) : undefined;
              onChange(updateField(overrides, "disallowedTools", arr && arr.length > 0 ? arr : undefined));
            }}
            disabled={disabled}
          />
          <HelpText>Tools the agent cannot use. Comma-separated.</HelpText>
        </div>

        {/* Auto-Approve Tools */}
        <div className={overrides.autoApproveTools !== undefined && overrides.autoApproveTools.length > 0 ? "toolkit-field-modified" : ""}>
          <FieldLabel label="Auto-Approve Tools" modified={Boolean(overrides.autoApproveTools?.length)} />
          <textarea
            className="ui-control ui-focus-ring w-full resize-y bg-[var(--color-surface-high)] px-2.5 py-1.5 text-[11px] text-[var(--color-text-main)] placeholder:text-[var(--color-text-dim)]/50"
            placeholder="e.g. FileRead, Glob, Grep"
            rows={2}
            value={overrides.autoApproveTools?.join(", ") ?? ""}
            onChange={(e) => {
              const val = e.target.value;
              const arr = val ? normalizeStringArray(val) : undefined;
              onChange(updateField(overrides, "autoApproveTools", arr && arr.length > 0 ? arr : undefined));
            }}
            disabled={disabled}
          />
          <HelpText>Tools auto-approved without permission prompt.</HelpText>
        </div>

        {/* Include Partial Messages */}
        <div className={overrides.includePartialMessages !== undefined && overrides.includePartialMessages !== "inherit" ? "toolkit-field-modified" : ""}>
          <FieldLabel
            label="Include Partial Messages"
            modified={overrides.includePartialMessages !== undefined && overrides.includePartialMessages !== "inherit"}
          />
          <select
            className="ui-control ui-focus-ring w-full bg-[var(--color-surface-high)] px-2.5 py-1.5 text-[11px] text-[var(--color-text-main)]"
            value={
              overrides.includePartialMessages === undefined
                ? "inherit"
                : String(overrides.includePartialMessages)
            }
            onChange={(e) => {
              const val = e.target.value;
              let setting: PartialMessagesSetting | undefined;
              if (val === "true") setting = true;
              else if (val === "false") setting = false;
              else setting = "inherit";
              onChange(updateField(overrides, "includePartialMessages", setting === "inherit" ? undefined : setting));
            }}
            disabled={disabled}
          >
            <option value="inherit">Inherit (SDK default)</option>
            <option value="true">Enabled</option>
            <option value="false">Disabled</option>
          </select>
          <HelpText>Include streaming partial messages in output.</HelpText>
        </div>

        {/* Subagent Governance */}
        <GovernanceSection overrides={overrides} onChange={onChange} disabled={disabled} />
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between border-t border-[var(--color-border)]/60 px-3 py-2">
        <button
          type="button"
          onClick={handleReset}
          disabled={disabled || !activeCount}
          className="mono text-[9px] font-semibold uppercase tracking-[0.1em] text-[var(--color-text-dim)]/70 hover:text-[var(--color-accent-orange)] disabled:opacity-40 disabled:hover:text-[var(--color-text-dim)]/70"
        >
          Reset All
        </button>
        <button
          type="button"
          onClick={() => setShowPresets(!showPresets)}
          disabled={disabled}
          className="mono text-[9px] font-semibold uppercase tracking-[0.1em] text-[var(--color-accent-orange)]/80 hover:text-[var(--color-accent-orange)] disabled:opacity-40"
        >
          Presets...
        </button>
      </div>

      {/* Inline presets panel */}
      {showPresets && (
        <ToolkitPresets
          currentOverrides={overrides}
          onApply={onChange}
          onClose={() => setShowPresets(false)}
        />
      )}
    </aside>
  );
};

export default Toolkit;
