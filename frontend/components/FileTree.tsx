"use client";

import React, { useEffect, useMemo, useRef, useState } from "react";
import type { FileNode } from "@/app/api/fs/route";

type GitFileState = "modified" | "added" | "deleted" | "renamed" | "untracked" | "conflicted";
type GitLoadState = "loading" | "ready" | "not_repo" | "error";

type GitStatusResponse = {
  state?: "ready" | "not_repo";
  statuses?: Record<string, GitFileState>;
  summary?: {
    changed?: number;
  };
  error?: string;
};

type GitBadgeMeta = {
  label: string;
  badgeClass: string;
  textClass: string;
};

function getGitBadgeMeta(state: GitFileState): GitBadgeMeta {
  switch (state) {
    case "added":
      return {
        label: "A",
        badgeClass: "text-[var(--color-judging)] border-[var(--color-judging)]/35 bg-[var(--color-judging)]/10",
        textClass: "text-[var(--color-judging)]",
      };
    case "deleted":
      return {
        label: "D",
        badgeClass: "text-[var(--color-text-main)] border-[var(--color-accent-orange)]/35 bg-[var(--color-accent-orange)]/10",
        textClass: "text-[var(--color-text-main)]",
      };
    case "renamed":
      return {
        label: "R",
        badgeClass: "text-[var(--color-applying)] border-[var(--color-applying)]/35 bg-[var(--color-applying)]/10",
        textClass: "text-[var(--color-applying)]",
      };
    case "untracked":
      return {
        label: "?",
        badgeClass: "text-[var(--color-applying)] border-[var(--color-applying)]/35 bg-[var(--color-applying)]/10",
        textClass: "text-[var(--color-applying)]",
      };
    case "conflicted":
      return {
        label: "!",
        badgeClass: "text-[var(--color-text-main)] border-[var(--color-accent-orange)]/40 bg-[var(--color-accent-orange)]/12",
        textClass: "text-[var(--color-text-main)]",
      };
    case "modified":
    default:
      return {
        label: "M",
        badgeClass: "text-[var(--color-text-main)] border-[var(--color-accent-orange)]/35 bg-[var(--color-accent-orange)]/10",
        textClass: "text-[var(--color-text-main)]",
      };
  }
}

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
  const [gitStatuses, setGitStatuses] = useState<Record<string, GitFileState>>({});
  const [gitLoadState, setGitLoadState] = useState<GitLoadState>("loading");
  const [changedCount, setChangedCount] = useState(0);
  const [refreshTick, setRefreshTick] = useState(0);
  const previousTreeRootRef = useRef<string | null | undefined>(undefined);
  const previousGitRootRef = useRef<string | null | undefined>(undefined);

  useEffect(() => {
    const refreshIntervalMs = 4000;
    const refreshIfVisible = () => {
      if (document.visibilityState !== "visible") {
        return;
      }
      setRefreshTick((previous) => previous + 1);
    };

    const intervalId = window.setInterval(refreshIfVisible, refreshIntervalMs);
    window.addEventListener("focus", refreshIfVisible);
    document.addEventListener("visibilitychange", refreshIfVisible);

    return () => {
      window.clearInterval(intervalId);
      window.removeEventListener("focus", refreshIfVisible);
      document.removeEventListener("visibilitychange", refreshIfVisible);
    };
  }, []);

  useEffect(() => {
    let canceled = false;
    const rootChanged = previousTreeRootRef.current !== rootPath;
    previousTreeRootRef.current = rootPath;

    const url = rootPath ? `/api/fs?path=${encodeURIComponent(rootPath)}` : "/api/fs";
    if (rootChanged) {
      queueMicrotask(() => setLoading(true));
      queueMicrotask(() => setSelectedPath(null));
    }

    fetch(url, { cache: "no-store" })
      .then((res) => res.json())
      .then((data) => {
        if (canceled) return;
        setNodes(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch((err) => {
        if (canceled) return;
        console.error("Failed to fetch file tree:", err);
        setNodes([]);
        setLoading(false);
      });

    return () => {
      canceled = true;
    };
  }, [rootPath, refreshTick]);

  useEffect(() => {
    let canceled = false;
    const rootChanged = previousGitRootRef.current !== rootPath;
    previousGitRootRef.current = rootPath;

    const url = rootPath ? `/api/fs/git-status?path=${encodeURIComponent(rootPath)}` : "/api/fs/git-status";
    if (rootChanged) {
      queueMicrotask(() => setGitLoadState("loading"));
    }

    fetch(url, { cache: "no-store" })
      .then((res) => res.json())
      .then((data: GitStatusResponse) => {
        if (canceled) return;

        if (data.state === "ready") {
          const statuses = data.statuses ?? {};
          setGitStatuses(statuses);
          setChangedCount(
            typeof data.summary?.changed === "number" ? data.summary.changed : Object.keys(statuses).length,
          );
          setGitLoadState("ready");
          return;
        }

        if (data.state === "not_repo") {
          setGitStatuses({});
          setChangedCount(0);
          setGitLoadState("not_repo");
          return;
        }

        if (typeof data.error === "string") {
          console.error("Failed to fetch git status:", data.error);
        }
        setGitStatuses({});
        setChangedCount(0);
        setGitLoadState("error");
      })
      .catch((err) => {
        if (canceled) return;
        console.error("Failed to fetch git status:", err);
        setGitStatuses({});
        setChangedCount(0);
        setGitLoadState("error");
      });

    return () => {
      canceled = true;
    };
  }, [rootPath, refreshTick]);

  const dirtyDirectories = useMemo(() => {
    const directories = new Set<string>();
    Object.keys(gitStatuses).forEach((relativePath) => {
      const parts = relativePath.split("/").filter(Boolean);
      for (let index = 1; index < parts.length; index += 1) {
        directories.add(parts.slice(0, index).join("/"));
      }
    });
    return directories;
  }, [gitStatuses]);

  const containerClass = `h-full overflow-y-auto px-2 py-2.5 custom-scrollbar ${className ?? ""}`;

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
        <GitStatusRow gitLoadState={gitLoadState} changedCount={changedCount} />
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
      <GitStatusRow gitLoadState={gitLoadState} changedCount={changedCount} />
      {nodes.map((node) => (
        <TreeNode
          key={node.path}
          node={node}
          onFileSelect={onFileSelect}
          onDirectorySelect={onDirectorySelect}
          depth={0}
          selectedPath={selectedPath}
          setSelectedPath={setSelectedPath}
          gitStatuses={gitStatuses}
          dirtyDirectories={dirtyDirectories}
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
  gitStatuses: Record<string, GitFileState>;
  dirtyDirectories: Set<string>;
}

function TreeNode({
  node,
  onFileSelect,
  onDirectorySelect,
  depth,
  selectedPath,
  setSelectedPath,
  gitStatuses,
  dirtyDirectories,
}: TreeNodeProps) {
  const [isOpen, setIsOpen] = useState(depth < 1); // Expand first level by default
  const isSelected = selectedPath === node.path;
  const fileGitState = node.isDirectory ? undefined : gitStatuses[node.path];
  const fileGitMeta = fileGitState ? getGitBadgeMeta(fileGitState) : null;
  const hasDirtyChildren = node.isDirectory && dirtyDirectories.has(node.path);
  const hasGitSignal = Boolean(fileGitMeta) || hasDirtyChildren;

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
            ? "border-[var(--color-border-strong)] bg-[var(--color-surface-low)]/82 text-[var(--color-text-main)] shadow-[inset_0_0_0_1px_rgba(255,255,255,0.05)]"
            : hasGitSignal
              ? "border-[var(--color-accent-orange)]/20 bg-[var(--color-accent-orange)]/8 text-[var(--color-text-main)] hover:border-[var(--color-accent-orange)]/35 hover:bg-[var(--color-accent-orange)]/12"
              : "border-transparent text-[var(--color-text-dim)] hover:border-[var(--color-border)]/70 hover:bg-[var(--color-surface-low)]/72 hover:text-[var(--color-text-main)]"
        }`}
        style={{ paddingLeft: `${depth * 14 + 8}px` }}
      >
        <span
          className={`mono w-4 text-center text-[10px] ${
            node.isDirectory
              ? hasDirtyChildren
                ? "text-[var(--color-accent-directory)]"
                : "text-[var(--color-accent-directory)]/80"
              : "text-[var(--color-text-dim)]/75"
          }`}
        >
          {node.isDirectory ? (isOpen ? "▾" : "▸") : "•"}
        </span>
        <span
          className={`min-w-0 flex-1 truncate text-[11px] ${
            node.isDirectory
              ? hasDirtyChildren
                ? "font-semibold text-[var(--color-accent-directory)] group-hover:text-[var(--color-accent-directory)]"
                : "font-semibold text-[var(--color-accent-directory)]/95 group-hover:text-[var(--color-accent-directory)]"
              : fileGitMeta
                ? `${fileGitMeta.textClass} font-semibold`
                : "text-[var(--color-text-main)]/85"
          }`}
          title={node.path}
        >
          {node.name || "/"}
          {node.isDirectory ? "/" : ""}
        </span>
        {fileGitMeta ? (
          <span
            className={`mono rounded border px-1.5 py-0.5 text-[9px] font-semibold uppercase tracking-[0.08em] ${fileGitMeta.badgeClass}`}
            title={`Git status: ${fileGitState}`}
          >
            {fileGitMeta.label}
          </span>
        ) : hasDirtyChildren ? (
          <span
            className="h-1.5 w-1.5 rounded-full bg-[var(--color-accent-orange)] shadow-[0_0_8px_var(--color-accent-orange)]"
            title="Contains git changes"
          />
        ) : null}
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
              gitStatuses={gitStatuses}
              dirtyDirectories={dirtyDirectories}
            />
          ))}
        </div>
      )}
    </div>
  );
}

interface GitStatusRowProps {
  gitLoadState: GitLoadState;
  changedCount: number;
}

function GitStatusRow({ gitLoadState, changedCount }: GitStatusRowProps) {
  let label = "Loading";
  let pillClass =
    "text-[var(--color-text-main)] border-[var(--color-accent-orange)]/30 bg-[var(--color-accent-orange)]/10";

  if (gitLoadState === "ready") {
    if (changedCount > 0) {
      label = `${changedCount} Changed`;
      pillClass =
        "text-[var(--color-text-main)] border-[var(--color-accent-orange)]/35 bg-[var(--color-accent-orange)]/10";
    } else {
      label = "Clean";
      pillClass = "text-[var(--color-judging)] border-[var(--color-judging)]/35 bg-[var(--color-judging)]/10";
    }
  } else if (gitLoadState === "not_repo") {
    label = "No Repo";
    pillClass = "text-[var(--color-text-dim)] border-[var(--color-border)] bg-[var(--color-surface-low)]";
  } else if (gitLoadState === "error") {
    label = "Unavailable";
    pillClass = "text-[var(--color-text-dim)] border-[var(--color-border)] bg-[var(--color-surface-low)]";
  }

  return (
    <div className="mb-2.5 flex items-center justify-between rounded-md border border-[var(--color-border)]/70 bg-[var(--color-surface-low)]/72 px-2.5 py-1.5">
      <span className="ui-type-mono-meta text-[9px] font-semibold uppercase tracking-[0.12em] text-[var(--color-text-dim)]">
        Git State
      </span>
      <span className={`mono rounded border px-2 py-0.5 text-[9px] font-semibold uppercase tracking-[0.1em] ${pillClass}`}>
        {label}
      </span>
    </div>
  );
}
