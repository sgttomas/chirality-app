"use client";

import React, { useState, useEffect } from "react";
import { SystemNode } from "@/app/api/system/list/route";

interface SystemFileTreeProps {
  onSelect: (path: string) => void;
  className?: string;
}

export function SystemFileTree({ onSelect, className }: SystemFileTreeProps) {
  const [rootNodes, setRootNodes] = useState<SystemNode[]>([]);
  const [currentPath, setCurrentPath] = useState("/");
  const [manualPath, setManualPath] = useState("/");
  const [loading, setLoading] = useState(false);

  const fetchDir = async (path: string) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/system/list?path=${encodeURIComponent(path)}`);
      const data = await res.json();
      if (data.nodes) {
        setRootNodes(data.nodes);
        setCurrentPath(data.current);
        setManualPath(data.current);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Initial load
    fetchDir("/");
  }, []);

  const handleManualSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchDir(manualPath);
  };

  const handleUp = () => {
    const parts = currentPath.split("/").filter(Boolean);
    parts.pop();
    const parent = "/" + parts.join("/");
    fetchDir(parent);
  };

  return (
    <div className={`flex flex-col h-full ${className}`}>
      {/* Navigation Bar */}
      <div className="flex gap-2 mb-2">
        <button 
            onClick={handleUp}
            className="px-2 py-1 bg-white/10 hover:bg-white/20 rounded text-xs font-mono"
            title="Go Up"
        >
            ..
        </button>
        <form onSubmit={handleManualSubmit} className="flex-grow">
            <input 
                type="text" 
                value={manualPath} 
                onChange={(e) => setManualPath(e.target.value)}
                className="w-full bg-black/40 border border-white/10 rounded px-2 py-1 text-xs font-mono text-[var(--color-text-main)] focus:border-[var(--color-accent-orange)] outline-none"
            />
        </form>
        <button 
            onClick={() => fetchDir(manualPath)}
            className="px-2 py-1 bg-[var(--color-accent-orange)]/20 hover:bg-[var(--color-accent-orange)]/40 text-[var(--color-accent-orange)] rounded text-xs font-bold"
        >
            GO
        </button>
      </div>

      {/* File List */}
      <div className="flex-grow overflow-y-auto border border-white/5 rounded bg-black/20 p-2 custom-scrollbar">
        {loading ? (
            <div className="p-4 text-xs opacity-50 font-mono">Loading...</div>
        ) : (
            <div>
                {rootNodes.map(node => (
                    <div 
                        key={node.path}
                        className={`flex items-center gap-2 p-1.5 cursor-pointer hover:bg-white/10 rounded ${node.path === manualPath ? 'bg-white/5' : ''}`}
                        onClick={() => {
                            if (node.isDirectory) {
                                fetchDir(node.path);
                            } 
                            onSelect(node.path);
                        }}
                    >
                        <span className="text-[10px] opacity-50 w-4 text-center">
                            {node.isDirectory ? "📁" : "📄"}
                        </span>
                        <span className={`text-xs font-mono truncate ${node.isDirectory ? 'text-[var(--color-accent-orange)]' : 'text-[var(--color-text-dim)]'}`}>
                            {node.name}
                        </span>
                    </div>
                ))}
                {rootNodes.length === 0 && (
                    <div className="p-4 text-xs opacity-30 font-mono italic">Empty directory</div>
                )}
            </div>
        )}
      </div>
    </div>
  );
}
