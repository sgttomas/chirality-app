"use client";

import React from "react";

type HexData = {
  row: string;
  col: string;
  label: string;
  type: "persona" | "task";
};

const hexData: HexData[] = [
  // Normative Row
  { row: "normative", col: "guiding", label: "DECOMP", type: "persona" },
  { row: "normative", col: "applying", label: "ORCHESTRATE", type: "persona" },
  { row: "normative", col: "judging", label: "WORKING_ITEMS", type: "persona" },
  { row: "normative", col: "reviewing", label: "AGGREGATE", type: "persona" },
  
  // Operative Row
  { row: "operative", col: "guiding", label: "HELP", type: "persona" },
  { row: "operative", col: "applying", label: "PREP*", type: "task" },
  { row: "operative", col: "judging", label: "TASK*", type: "task" },
  { row: "operative", col: "reviewing", label: "AUDIT*", type: "task" },
  
  // Evaluative Row
  { row: "evaluative", col: "guiding", label: "AGENTS", type: "persona" },
  { row: "evaluative", col: "applying", label: "DEPENDENCIES", type: "persona" },
  { row: "evaluative", col: "judging", label: "CHANGE", type: "persona" },
  { row: "evaluative", col: "reviewing", label: "RECONCILING", type: "persona" },
];

const columns = [
  { id: "guiding", label: "GUIDING" },
  { id: "applying", label: "APPLYING" },
  { id: "judging", label: "JUDGING" },
  { id: "reviewing", label: "REVIEWING" },
];

interface HexGridProps {
    onLaunch: (name: string, tier: string, type: "persona" | "task") => void;
}

export function HexGrid({ onLaunch }: HexGridProps) {
  return (
    <div className="portal-container flex-1 flex items-center justify-center relative">
      <div className="hex-grid">
        {/* Column Labels */}
        {columns.map((col) => (
          <div
            key={col.id}
            className={`hex-column-label col-${col.id}`}
          >
            {col.label}
          </div>
        ))}

        {/* Grid Items */}
        {hexData.map((hex) => (
          <button
            key={`${hex.row}-${hex.col}`}
            type="button"
            className={`hex-wrapper hex-launch ui-focus-ring row-${hex.row} col-${hex.col}`}
            onClick={() => onLaunch(hex.label, hex.row, hex.type)}
            aria-label={`Launch ${hex.label} ${hex.type}`}
          >
            {/* Show Row Label only for the first column (Guiding) */}
            {hex.col === "guiding" && (
              <div className="hex-row-label">{hex.row}</div>
            )}
            
            <div className="hex">
              <div className="hex-content">{hex.label}</div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
