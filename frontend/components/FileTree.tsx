"use client";

import React, { useState, useEffect } from "react";
import { FileNode } from "@/app/api/fs/route";

interface FileTreeProps {
  onFileSelect?: (path: string) => void;
  onDirectorySelect?: (path: string) => void;
  className?: string;
  rootPath?: string | null;
}

export function FileTree({ onFileSelect, onDirectorySelect, className, rootPath }: FileTreeProps) {
  const [nodes, setNodes] = useState<FileNode[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPath, setSelectedPath] = useState<string | null>(null);

  useEffect(() => {
    const url = rootPath ? `/api/fs?path=${encodeURIComponent(rootPath)}` : "/api/fs";
    queueMicrotask(() => setLoading(true));
    queueMicrotask(() => setSelectedPath(null));

    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        setNodes(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch file tree:", err);
        setNodes([]);
        setLoading(false);
      });
  }, [rootPath]);

  const containerClass = `h-full overflow-y-auto px-2 py-2 custom-scrollbar ${className ?? ""}`;

  if (loading) {
    return (
      <div className={containerClass}>
        <div className="ui-panel-soft rounded-md px-3 py-4 text-center">
          <span className="mono text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--color-text-dim)]">
            Scanning filesystem...
          </span>
        </div>
      </div>
    );
  }

  if (nodes.length === 0) {
    return (
      <div className={containerClass}>
        <div className="ui-panel-soft rounded-md px-3 py-4 text-center">
          <p className="mono text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--color-text-dim)]">
            No files found.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={`${containerClass} mono text-[12px] leading-relaxed text-[var(--color-text-dim)]`}>
      {nodes.map((node) => (
        <TreeNode
          key={node.path}
          node={node}
          onFileSelect={onFileSelect}
          onDirectorySelect={onDirectorySelect}
          depth={0}
          selectedPath={selectedPath}
          setSelectedPath={setSelectedPath}
        />
      ))}
    </div>
  );
}

interface TreeNodeProps {
  node: FileNode;
  onFileSelect?: (path: string) => void;
  onDirectorySelect?: (path: string) => void;
  depth: number;
  selectedPath: string | null;
  setSelectedPath: (path: string) => void;
}

function TreeNode({ node, onFileSelect, onDirectorySelect, depth, selectedPath, setSelectedPath }: TreeNodeProps) {
  const [isOpen, setIsOpen] = useState(depth < 1); // Expand first level by default
  const isSelected = selectedPath === node.path;

  const toggle = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
    setSelectedPath(node.path);
    if (node.isDirectory) {
      setIsOpen((prev) => !prev);
      onDirectorySelect?.(node.path);
      return;
    }
    onFileSelect?.(node.path);
  };

  return (
    <div className="select-none space-y-0.5">
      <button
        type="button"
        onClick={toggle}
        className={`ui-focus-ring group flex w-full items-center gap-2 rounded-md border px-2 py-1.5 text-left transition-colors ${
          isSelected
            ? "border-[var(--color-border-strong)] bg-[var(--color-surface-low)] text-[var(--color-text-main)]"
            : "border-transparent text-[var(--color-text-dim)] hover:border-[var(--color-border)] hover:bg-[var(--color-surface-low)]/75 hover:text-[var(--color-text-main)]"
        }`}
        style={{ paddingLeft: `${depth * 14 + 8}px` }}
      >
        <span
          className={`mono w-4 text-center text-[10px] ${
            node.isDirectory ? "text-[var(--color-accent-orange)]/80" : "text-[var(--color-text-dim)]/75"
          }`}
        >
          {node.isDirectory ? (isOpen ? "▾" : "▸") : "•"}
        </span>
        <span
          className={`min-w-0 flex-1 truncate text-[11px] ${
            node.isDirectory
              ? "font-semibold text-[var(--color-accent-orange)]/95 group-hover:text-[var(--color-accent-orange)]"
              : "text-[var(--color-text-main)]/85"
          }`}
          title={node.path}
        >
          {node.name || "/"}
          {node.isDirectory ? "/" : ""}
        </span>
      </button>

      {node.isDirectory && isOpen && node.children && (
        <div className="pl-1">
          {node.children.map((child) => (
            <TreeNode
              key={child.path}
              node={child}
              onFileSelect={onFileSelect}
              onDirectorySelect={onDirectorySelect}
              depth={depth + 1}
              selectedPath={selectedPath}
              setSelectedPath={setSelectedPath}
            />
          ))}
        </div>
      )}
    </div>
  );
}
