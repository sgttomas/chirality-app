"use client";

import React from "react";

type HexData = {
  row: MatrixRow;
  col: MatrixColumn;
  label: string;
  launchTarget: "workbench" | "pipeline";
};

export type MatrixRow = "normative" | "operative" | "evaluative";
export type MatrixColumn = "guiding" | "applying" | "judging" | "reviewing";

export type MatrixLaunchPayload = {
  row: MatrixRow;
  col: MatrixColumn;
  label: string;
  launchTarget: "workbench" | "pipeline";
};

const hexData: HexData[] = [
  // Normative Row
  { row: "normative", col: "guiding", label: "HELP", launchTarget: "workbench" },
  { row: "normative", col: "applying", label: "ORCHESTRATE", launchTarget: "workbench" },
  { row: "normative", col: "judging", label: "WORKING_ITEMS", launchTarget: "workbench" },
  { row: "normative", col: "reviewing", label: "AGGREGATE", launchTarget: "workbench" },
  
  // Operative Row
  { row: "operative", col: "guiding", label: "DECOMP*", launchTarget: "pipeline" },
  { row: "operative", col: "applying", label: "PREP*", launchTarget: "pipeline" },
  { row: "operative", col: "judging", label: "TASK*", launchTarget: "pipeline" },
  { row: "operative", col: "reviewing", label: "AUDIT*", launchTarget: "pipeline" },
  
  // Evaluative Row
  { row: "evaluative", col: "guiding", label: "AGENTS", launchTarget: "workbench" },
  { row: "evaluative", col: "applying", label: "DEPENDENCIES", launchTarget: "workbench" },
  { row: "evaluative", col: "judging", label: "CHANGE", launchTarget: "workbench" },
  { row: "evaluative", col: "reviewing", label: "RECONCILING", launchTarget: "workbench" },
];

const columns = [
  { id: "guiding", label: "GUIDING" as const },
  { id: "applying", label: "APPLYING" as const },
  { id: "judging", label: "JUDGING" as const },
  { id: "reviewing", label: "REVIEWING" as const },
];

interface HexGridProps {
    onLaunch: (payload: MatrixLaunchPayload) => void;
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
            onClick={() =>
              onLaunch({
                row: hex.row,
                col: hex.col,
                label: hex.label,
                launchTarget: hex.launchTarget,
              })
            }
            aria-label={`Launch ${hex.label}`}
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
