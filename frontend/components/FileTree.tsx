"use client";

import React, { useState, useEffect } from "react";
import { FileNode } from "@/app/api/fs/route";

interface FileTreeProps {
  onFileSelect?: (path: string) => void;
  className?: string;
}

export function FileTree({ onFileSelect, className }: FileTreeProps) {
  const [nodes, setNodes] = useState<FileNode[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/fs")
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) setNodes(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch file tree:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="p-4 mono text-sm opacity-50">Scanning filesystem...</div>;

  return (
    <div className={`tree-view ${className}`}>
      {nodes.map((node) => (
        <TreeNode key={node.path} node={node} onFileSelect={onFileSelect} depth={0} />
      ))}
    </div>
  );
}

function TreeNode({ node, onFileSelect, depth }: { node: FileNode; onFileSelect?: (path: string) => void; depth: number }) {
  const [isOpen, setIsOpen] = useState(depth < 1); // Expand first level by default

  const toggle = (e: React.MouseEvent) => {
    if (node.isDirectory) {
      e.stopPropagation();
      setIsOpen(!isOpen);
    } else {
      onFileSelect?.(node.path);
    }
  };

  return (
    <div className="select-none">
      <div 
        onClick={toggle}
        className={`flex items-center gap-1 cursor-pointer hover:text-[var(--color-text-main)] transition-colors py-0.5 ${!node.isDirectory ? 'hover:bg-white/5' : ''}`}
        style={{ paddingLeft: `${depth * 16}px` }}
      >
        <span className="opacity-50 mono w-4 inline-block text-center">
          {node.isDirectory ? (isOpen ? "▼" : "▶") : "•"}
        </span>
        <span className={node.isDirectory ? "tree-folder" : "text-[var(--color-text-dim)]"}>
          {node.name}{node.isDirectory && "/"}
        </span>
      </div>
      
      {node.isDirectory && isOpen && node.children && (
        <div>
          {node.children.map((child) => (
            <TreeNode key={child.path} node={child} onFileSelect={onFileSelect} depth={depth + 1} />
          ))}
        </div>
      )}
    </div>
  );
}
