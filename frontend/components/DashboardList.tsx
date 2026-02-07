"use client";

import React from "react";

type Deliverable = {
  id: string;
  name: string;
  status: "open" | "in-progress" | "checking" | "issued";
};

const deliverables: Deliverable[] = [
  { id: "DEL-01.01", name: "Site General Layout", status: "in-progress" },
  { id: "DEL-01.02", name: "Grading & Drainage Plan", status: "checking" },
  { id: "DEL-02.01", name: "Structural Foundation Calcs", status: "issued" },
  { id: "DEL-02.02", name: "Anchor Bolt Plan", status: "open" },
  { id: "DEL-03.01", name: "Electrical Single Line Diagram", status: "in-progress" },
];

interface DashboardListProps {
    onSelect: () => void;
}

export function DashboardList({ onSelect }: DashboardListProps) {
  return (
    <div className="dashboard-panel glass w-[550px] flex flex-col p-6 gap-5 h-full">
      <div className="dashboard-title">
        <span>Deliverables</span>
        <span className="mono text-sm text-[var(--color-text-dim)]">
          COUNT: 142
        </span>
      </div>
      <div className="dashboard-list flex-grow overflow-y-auto flex flex-col gap-3 pr-2">
        {deliverables.map((del) => (
          <div key={del.id} className="deliverable-card glass" onClick={onSelect}>
            <div className={`del-status-dot status-${del.status}`}></div>
            <div className="del-id">{del.id}</div>
            <div className="del-name">{del.name}</div>
          </div>
        ))}
      </div>
    </div>
  );
}