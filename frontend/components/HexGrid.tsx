"use client";

import React from "react";

type HexData = {
  row: string;
  col: string;
  label: string;
  isTask?: boolean;
};

const hexData: HexData[] = [
  // Normative Row
  { row: "normative", col: "guiding", label: "Decomp" },
  { row: "normative", col: "applying", label: "Orchestrate" },
  { row: "normative", col: "judging", label: "Items" },
  { row: "normative", col: "reviewing", label: "Aggregate" },
  
  // Operative Row
  { row: "operative", col: "guiding", label: "Help" },
  { row: "operative", col: "applying", label: "Prep*" },
  { row: "operative", col: "judging", label: "Task*" },
  { row: "operative", col: "reviewing", label: "Audit*" },
  
  // Evaluative Row
  { row: "evaluative", col: "guiding", label: "Humans" },
  { row: "evaluative", col: "applying", label: "Change" },
  { row: "evaluative", col: "judging", label: "Deps*" },
  { row: "evaluative", col: "reviewing", label: "Recon" },
];

const columns = [
  { id: "guiding", label: "Guiding" },
  { id: "applying", label: "Applying" },
  { id: "judging", label: "Judging" },
  { id: "reviewing", label: "Reviewing" },
];

const rows = ["normative", "operative", "evaluative"];

export function HexGrid() {
  return (
    <div className="portal-container flex-1 flex items-center justify-center relative">
      <div className="hex-grid">
        {/* Column Labels */}
        {columns.map((col) => (
          <div
            key={col.id}
            className={`hex-column-label col-${col.id}`}
            style={{ color: `var(--color-${col.id})` }}
          >
            {col.label}
          </div>
        ))}

        {/* Grid Items */}
        {hexData.map((hex, index) => (
          <div
            key={`${hex.row}-${hex.col}`}
            className={`hex-wrapper row-${hex.row} col-${hex.col}`}
            onClick={() => console.log(`Clicked ${hex.label}`)}
          >
            {/* Show Row Label only for the first column (Guiding) */}
            {hex.col === "guiding" && (
              <div className="hex-row-label">{hex.row}</div>
            )}
            
            <div className="hex">
              <div className="hex-content">{hex.label}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
