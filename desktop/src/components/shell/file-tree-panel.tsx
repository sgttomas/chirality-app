'use client';

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  FILE_TREE_POLL_INTERVAL_MS,
  createRefreshScheduler,
  shouldPollWhenHidden,
  shouldRefreshForVisibilityState
} from '../../lib/workspace/file-tree-refresh';
import { useWorkspace } from '../workspace/workspace-provider';

const TREE_DEPTH = 3;

type TreeNode = {
  name: string;
  path: string;
  kind: 'directory' | 'file' | 'symlink';
  children?: TreeNode[];
  truncated?: boolean;
};

type TreeResponse = {
  root: TreeNode;
  depth: number;
  scannedAt: string;
};

export type FileCatalog = {
  root: string;
  paths: string[];
};

export function collectFilePaths(node: TreeNode): string[] {
  const paths: string[] = [];
  const visit = (candidate: TreeNode): void => {
    if (candidate.kind === 'file') {
      paths.push(candidate.path);
      return;
    }
    if (candidate.kind === 'directory') {
      candidate.children?.forEach(visit);
    }
  };
  visit(node);
  return paths.sort();
}

type TreeNodeViewProps = {
  compact?: boolean;
  node: TreeNode;
  expandedByPath: Record<string, boolean>;
  onToggle: (nodePath: string) => void;
  onOpenFile?: (filePath: string) => void;
  selectedPath?: string | null;
};

function TreeNodeView({ compact = false, node, expandedByPath, onToggle, onOpenFile, selectedPath }: TreeNodeViewProps): JSX.Element {
  const hasChildren = node.kind === 'directory' && Boolean(node.children?.length);
  const isExpanded = hasChildren ? (expandedByPath[node.path] ?? true) : true;
  const icon = node.kind === 'directory' ? 'DIR' : node.kind === 'symlink' ? 'LNK' : 'FILE';

  return (
    <li>
      <div className={`tree-item tree-item--${node.kind}`}>
        {hasChildren ? (
          <button
            type="button"
            className="tree-toggle"
            aria-label={isExpanded ? `Collapse ${node.name}` : `Expand ${node.name}`}
            onClick={() => {
              onToggle(node.path);
            }}
          >
            {isExpanded ? '-' : '+'}
          </button>
        ) : (
          <span className="tree-toggle tree-toggle--spacer" aria-hidden="true">
            {' '}
          </span>
        )}
        <span className="tree-item-icon" aria-hidden={compact || undefined}>{compact ? node.kind === 'directory' ? '▱' : node.kind === 'symlink' ? '↗' : '▤' : icon}</span>
        {node.kind === 'file' && onOpenFile ? (
          <button type="button" className="tree-item-name" title={node.path}
            aria-current={selectedPath === node.path ? 'true' : undefined}
            onClick={() => onOpenFile(node.path)}>{node.name}</button>
        ) : node.kind === 'directory' ? (
          <button type="button" className="tree-item-name" title={node.path}
            aria-expanded={isExpanded} onClick={() => onToggle(node.path)}>{node.name}</button>
        ) : <span className="tree-item-name" title={node.path}>{node.name}</span>}
      </div>
      {hasChildren && isExpanded ? (
        <ul className="tree-list">
          {node.children?.map((child) => (
            <TreeNodeView compact={compact}
              key={child.path}
              node={child}
              expandedByPath={expandedByPath}
              onToggle={onToggle}
              onOpenFile={onOpenFile}
              selectedPath={selectedPath}
            />
          ))}
        </ul>
      ) : null}
      {node.truncated ? (
        <div className="tree-truncated">Directory listing truncated for responsiveness.</div>
      ) : null}
    </li>
  );
}

export function FileTreePanel({ onOpenFile, onFileCatalog, selectedPath, presentation, folderLocked = false, onFolderSelectionPending }: { presentation?: 'woven'; onFolderSelectionPending?: (pending: boolean) => void; folderLocked?: boolean; onOpenFile?: (path: string) => void; onFileCatalog?: (catalog: FileCatalog | null) => void; selectedPath?: string | null } = {}): JSX.Element {
  const { projectRoot, chooseProjectRoot, hasElectronDirectoryPicker, errorMessage } = useWorkspace();
  // The preload capability is client-only; keep SSR and the first client render identical.
  const [mounted, setMounted] = useState(false);
  const directoryPickerAvailable = mounted && hasElectronDirectoryPicker;
  useEffect(() => { setMounted(true); }, []);
  const [tree, setTree] = useState<TreeNode | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedByPath, setExpandedByPath] = useState<Record<string, boolean>>({});
  const [refreshNonce, setRefreshNonce] = useState(0);
  const [pollingGeneration, setPollingGeneration] = useState(0);
  const latestRequestIdRef = useRef(0);
  const treeRef = useRef<TreeNode | null>(null);
  const catalogRootRef = useRef(projectRoot);

  useEffect(() => {
    treeRef.current = tree;
  }, [tree]);

  useEffect(() => {
    setExpandedByPath({});
    setTree(null);
    treeRef.current = null;
    setError(null);
    setLoading(false);
    if (catalogRootRef.current !== projectRoot) onFileCatalog?.(null);
    catalogRootRef.current = projectRoot;
  }, [projectRoot, onFileCatalog]);

  // The catalog belongs to the conversation, not this panel's visibility.
  // Root changes and failed reads still invalidate it above/below.

  const triggerRefresh = useCallback(() => {
    setRefreshNonce((current) => current + 1);
  }, []);

  const restartPolling = useCallback(() => {
    setPollingGeneration((current) => current + 1);
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function loadTree(): Promise<void> {
      if (!projectRoot) {
        setTree(null);
        setError(null);
        onFileCatalog?.(null);
        return;
      }

      const requestId = latestRequestIdRef.current + 1;
      latestRequestIdRef.current = requestId;
      const showInitialLoading = treeRef.current === null;
      if (showInitialLoading) {
        setLoading(true);
      }

      try {
        const response = await fetch(
          `/api/working-root/tree?projectRoot=${encodeURIComponent(projectRoot)}&depth=${TREE_DEPTH}`
        );
        const payload = (await response.json()) as TreeResponse & {
          error?: { message?: string };
        };

        if (!response.ok || !payload.root) {
          throw new Error(payload.error?.message ?? 'Unable to load directory tree');
        }

        if (cancelled || requestId !== latestRequestIdRef.current) {
          return;
        }

        setTree(payload.root);
        setError(null);
        onFileCatalog?.({ root: projectRoot, paths: collectFilePaths(payload.root) });
      } catch (loadError) {
        if (cancelled || requestId !== latestRequestIdRef.current) {
          return;
        }

        const message = loadError instanceof Error ? loadError.message : 'Unable to load directory tree';
        setError(message);
        setTree(null);
        onFileCatalog?.(null);
      } finally {
        if (!cancelled && requestId === latestRequestIdRef.current && showInitialLoading) {
          setLoading(false);
        }
      }
    }

    void loadTree();

    return () => {
      cancelled = true;
    };
  }, [projectRoot, refreshNonce, onFileCatalog]);

  useEffect(() => {
    if (!projectRoot) {
      return;
    }

    const intervalId = window.setInterval(() => {
      const hidden = document.visibilityState === 'hidden';
      if (!shouldPollWhenHidden(hidden)) {
        return;
      }

      triggerRefresh();
    }, FILE_TREE_POLL_INTERVAL_MS);

    return () => {
      window.clearInterval(intervalId);
    };
  }, [projectRoot, pollingGeneration, triggerRefresh]);

  useEffect(() => {
    if (!projectRoot) {
      return;
    }

    const scheduler = createRefreshScheduler({
      onRefresh: triggerRefresh,
      onAfterRefresh: restartPolling
    });

    const onVisibilityChange = (): void => {
      if (shouldRefreshForVisibilityState(document.visibilityState)) {
        scheduler.schedule();
      }
    };

    const onWindowFocus = (): void => {
      scheduler.schedule();
    };

    document.addEventListener('visibilitychange', onVisibilityChange);
    window.addEventListener('focus', onWindowFocus);

    return () => {
      scheduler.cancel();
      document.removeEventListener('visibilitychange', onVisibilityChange);
      window.removeEventListener('focus', onWindowFocus);
    };
  }, [projectRoot, restartPolling, triggerRefresh]);

  const toggleExpanded = useCallback((nodePath: string): void => {
    setExpandedByPath((current) => ({
      ...current,
      [nodePath]: !(current[nodePath] ?? true)
    }));
  }, []);

  const panelBody = useMemo(() => {
    if (!projectRoot) {
      return <p className="panel-empty">Choose a folder to see its files.</p>;
    }

    if (loading) {
      return <p className="panel-empty">Loading directory tree...</p>;
    }

    if (error) {
      return <p className="panel-error">{error}</p>;
    }

    if (!tree) {
      return <p className="panel-empty">No files available for this root.</p>;
    }

    return (
      <ul className="tree-list">
        <TreeNodeView compact={presentation === 'woven'} node={tree} expandedByPath={expandedByPath} onToggle={toggleExpanded} onOpenFile={onOpenFile} selectedPath={selectedPath} />
      </ul>
    );
  }, [projectRoot, loading, error, tree, expandedByPath, toggleExpanded, onOpenFile, selectedPath, presentation]);

  return (
    <aside className="panel panel--file-tree" style={{ display: 'grid', gridTemplateRows: 'auto minmax(0, 1fr) auto' }}>
      {presentation !== 'woven' ? <header className="panel-header" style={{ gridRow: 1 }}>
        <h2>File Tree</h2>
      </header> : null}
      <div className="panel-body" style={{ gridRow: 2 }} onKeyDown={(event) => {
        if (!['ArrowDown', 'ArrowUp'].includes(event.key)) return;
        const buttons = Array.from(event.currentTarget.querySelectorAll<HTMLButtonElement>('button.tree-item-name'));
        const index = buttons.indexOf(event.target as HTMLButtonElement);
        if (index < 0) return;
        event.preventDefault();
        buttons[Math.max(0, Math.min(buttons.length - 1, index + (event.key === 'ArrowDown' ? 1 : -1)))]?.focus();
      }}>{panelBody}</div>
      <footer style={{ gridRow: 3, padding: '0.65rem 1rem', borderTop: '1px solid var(--rule)', overflowWrap: 'anywhere' }}><button type="button" disabled={!directoryPickerAvailable || folderLocked} onClick={() => { if (!folderLocked) { onFolderSelectionPending?.(true); void chooseProjectRoot().finally(() => onFolderSelectionPending?.(false)); } }}>Choose folder</button>
        <span title={projectRoot ?? undefined}>{projectRoot ? projectRoot.split('/').filter(Boolean).at(-1) ?? '/' : 'No folder'}</span>
        {!directoryPickerAvailable ? <p>Choose a folder using the folder selector above.</p> : null}
        {errorMessage ? <p role="alert">{errorMessage}</p> : null}
      </footer>
    </aside>
  );
}
