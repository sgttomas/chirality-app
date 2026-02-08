"use client";

import React, { useState } from "react";
import { SystemFileTree } from "./SystemFileTree";

interface DirectoryPickerProps {
  onSelect: (path: string) => void;
  onCancel: () => void;
}

export function DirectoryPicker({ onSelect, onCancel }: DirectoryPickerProps) {
  const [selectedPath, setSelectedPath] = useState<string | null>(null);

  const handleConfirm = () => {
    if (selectedPath) {
      onSelect(selectedPath);
    }
  };

  return (
    <div className="fixed inset-0 z-[200] flex items-center justify-center bg-black/70 backdrop-blur-md">
      <div className="glass w-[600px] h-[700px] flex flex-col shadow-2xl border-[var(--color-accent-orange)]/30">
        <div className="p-4 border-b border-[var(--color-border)] flex justify-between items-center bg-[var(--color-surface-high)]">
          <h2 className="text-sm font-bold text-[var(--color-accent-orange)] tracking-widest uppercase">Select Directory</h2>
          <button onClick={onCancel} className="text-[var(--color-text-dim)] hover:text-[var(--color-text-main)] transition-colors">✕</button>
        </div>
        
        <div className="flex-grow overflow-hidden p-4 bg-[var(--color-surface-mid)]">
            <SystemFileTree 
                onSelect={(path) => setSelectedPath(path)}
                className="h-full"
            />
        </div>

        <div className="p-4 border-t border-[var(--color-border)] bg-[var(--color-surface-high)] flex justify-between items-center">
            <div className="text-[10px] font-mono text-[var(--color-text-dim)] truncate max-w-[350px]">
                {selectedPath ? `Selected: ${selectedPath}` : "Select a target..."}
            </div>
            <div className="flex gap-3">
                <button onClick={onCancel} className="px-4 py-2 hover:bg-white/10 rounded transition-colors text-[10px] uppercase font-bold tracking-widest">Cancel</button>
                <button 
                    onClick={handleConfirm} 
                    disabled={!selectedPath}
                    className={`px-6 py-2 rounded font-black transition-all text-[10px] uppercase tracking-widest ${selectedPath ? 'bg-[var(--color-accent-orange)] text-black hover:brightness-110 shadow-[0_0_15px_rgba(249,115,22,0.2)]' : 'bg-white/5 text-white/20 cursor-not-allowed'}`}
                >
                    Set_CWD
                </button>
            </div>
        </div>
      </div>
    </div>
  );
}
