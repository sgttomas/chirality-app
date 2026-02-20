"use client";

import React, { useState, useCallback, useMemo } from "react";

import type { ToolkitOverrides, ToolkitPreset } from "@/lib/toolkit-config";
import {
  loadPresets,
  savePresets,
  createPreset,
  hasActiveOverrides,
} from "@/lib/toolkit-config";

// ---------------------------------------------------------------------------
// Props
// ---------------------------------------------------------------------------

export interface ToolkitPresetsProps {
  currentOverrides: ToolkitOverrides;
  onApply: (overrides: ToolkitOverrides) => void;
  onClose: () => void;
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

const ToolkitPresets: React.FC<ToolkitPresetsProps> = ({ currentOverrides, onApply, onClose }) => {
  const [presets, setPresets] = useState<ToolkitPreset[]>(() => loadPresets());
  const [newName, setNewName] = useState("");
  const [isNaming, setIsNaming] = useState(false);

  const canSaveCurrent = useMemo(() => hasActiveOverrides(currentOverrides), [currentOverrides]);

  const handleSave = useCallback(() => {
    const trimmed = newName.trim();
    if (!trimmed) return;

    const preset = createPreset(trimmed, currentOverrides);
    const next = [preset, ...presets].slice(0, 20);
    savePresets(next);
    setPresets(next);
    setNewName("");
    setIsNaming(false);
  }, [newName, currentOverrides, presets]);

  const handleDelete = useCallback(
    (id: string) => {
      const next = presets.filter((p) => p.id !== id);
      savePresets(next);
      setPresets(next);
    },
    [presets],
  );

  const handleApply = useCallback(
    (preset: ToolkitPreset) => {
      onApply({ ...preset.overrides });
      onClose();
    },
    [onApply, onClose],
  );

  const formatDate = (iso: string): string => {
    try {
      return new Date(iso).toLocaleDateString(undefined, { month: "short", day: "numeric" });
    } catch {
      return "";
    }
  };

  return (
    <div className="border-t border-[var(--color-border)]/60 bg-[var(--color-surface-low)]/50">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-[var(--color-border)]/30">
        <span className="mono text-[9px] font-semibold uppercase tracking-[0.12em] text-[var(--color-text-dim)]/80">
          Presets
        </span>
        <button
          type="button"
          onClick={onClose}
          className="ui-control ui-focus-ring flex h-6 w-6 items-center justify-center rounded-md text-[var(--color-text-dim)]/70 hover:text-[var(--color-accent-orange)]"
          title="Close presets"
        >
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>

      {/* Save current */}
      <div className="px-3 py-2 border-b border-[var(--color-border)]/30">
        {isNaming ? (
          <div className="flex items-center gap-1.5">
            <input
              type="text"
              className="ui-control ui-focus-ring flex-1 bg-[var(--color-surface-high)] px-2 py-1 text-[10px] text-[var(--color-text-main)] placeholder:text-[var(--color-text-dim)]/50"
              placeholder="Preset name..."
              maxLength={60}
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") handleSave();
                if (e.key === "Escape") {
                  setIsNaming(false);
                  setNewName("");
                }
              }}
              autoFocus
            />
            <button
              type="button"
              onClick={handleSave}
              disabled={!newName.trim()}
              className="mono text-[9px] font-semibold uppercase tracking-[0.1em] text-[var(--color-accent-orange)] hover:text-[var(--color-accent-orange)] disabled:opacity-40"
            >
              Save
            </button>
          </div>
        ) : (
          <button
            type="button"
            onClick={() => setIsNaming(true)}
            disabled={!canSaveCurrent}
            className="mono text-[9px] font-semibold uppercase tracking-[0.1em] text-[var(--color-accent-orange)]/80 hover:text-[var(--color-accent-orange)] disabled:opacity-40 disabled:hover:text-[var(--color-accent-orange)]/80"
          >
            + Save Current
          </button>
        )}
      </div>

      {/* Preset list */}
      <div className="custom-scrollbar max-h-[180px] overflow-y-auto">
        {presets.length === 0 ? (
          <p className="px-3 py-3 text-center text-[10px] text-[var(--color-text-dim)]/50">
            No saved presets.
          </p>
        ) : (
          <div className="space-y-0.5 p-1.5">
            {presets.map((preset) => (
              <div
                key={preset.id}
                className="group flex items-center justify-between rounded-md border border-[var(--color-border)]/40 bg-[var(--color-surface-low)]/40 px-2.5 py-1.5"
              >
                <div className="min-w-0 flex-1">
                  <div className="truncate text-[10px] font-semibold tracking-[0.06em] text-[var(--color-text-main)]">
                    {preset.name}
                  </div>
                  <div className="mono text-[8px] text-[var(--color-text-dim)]/50">
                    {formatDate(preset.createdAt)}
                  </div>
                </div>
                <div className="flex items-center gap-1 opacity-60 group-hover:opacity-100">
                  <button
                    type="button"
                    onClick={() => handleApply(preset)}
                    className="mono text-[8px] font-semibold uppercase tracking-[0.1em] text-[var(--color-accent-orange)] hover:text-[var(--color-accent-orange)]"
                  >
                    Apply
                  </button>
                  <button
                    type="button"
                    onClick={() => handleDelete(preset.id)}
                    className="mono text-[8px] font-semibold uppercase tracking-[0.1em] text-[var(--color-text-dim)]/60 hover:text-[var(--color-normative)]"
                  >
                    Del
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ToolkitPresets;
