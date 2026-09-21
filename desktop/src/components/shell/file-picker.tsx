'use client';

import { useEffect, useMemo, useState } from 'react';
import {
  buildUiAttachment,
  isSupportedAttachmentPath,
  SUPPORTED_ATTACHMENT_EXTENSIONS,
  type UiAttachment
} from '../../lib/harness/ui-attachments';

type TreeNode = {
  name: string;
  path: string;
  kind: 'directory' | 'file';
  children?: TreeNode[];
};

type TreeResponse = {
  root: TreeNode;
};

type FilePickerProps = {
  open: boolean;
  projectRoot: string;
  existingPaths: string[];
  onClose: () => void;
  onAddAttachments: (attachments: UiAttachment[]) => void;
};

function pathParent(input: string): string {
  if (input === '/') {
    return '/';
  }

  const trimmed = input.endsWith('/') ? input.slice(0, -1) : input;
  const index = trimmed.lastIndexOf('/');
  if (index <= 0) {
    return '/';
  }
  return trimmed.slice(0, index);
}

function pathWithinRoot(candidate: string, projectRoot: string): boolean {
  if (candidate === projectRoot) {
    return true;
  }
  const rootPrefix = projectRoot.endsWith('/') ? projectRoot : `${projectRoot}/`;
  return candidate.startsWith(rootPrefix);
}

export function FilePicker({
  open,
  projectRoot,
  existingPaths,
  onClose,
  onAddAttachments
}: FilePickerProps): JSX.Element | null {
  const [currentDirectory, setCurrentDirectory] = useState(projectRoot);
  const [entries, setEntries] = useState<TreeNode[]>([]);
  const [selectedPaths, setSelectedPaths] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) {
      return;
    }
    setCurrentDirectory(projectRoot);
    setSelectedPaths([]);
    setError(null);
  }, [open, projectRoot]);

  useEffect(() => {
    if (!open) {
      return;
    }

    let cancelled = false;

    async function loadEntries(): Promise<void> {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(
          `/api/working-root/tree?projectRoot=${encodeURIComponent(currentDirectory)}&depth=1`
        );
        const payload = (await response.json()) as TreeResponse & {
          error?: { message?: string };
        };

        if (!response.ok || !payload.root) {
          throw new Error(payload.error?.message ?? 'Unable to load directory');
        }

        if (!cancelled) {
          setEntries(payload.root.children ?? []);
        }
      } catch (loadError) {
        if (!cancelled) {
          const message = loadError instanceof Error ? loadError.message : 'Unable to load directory';
          setError(message);
          setEntries([]);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadEntries();

    return () => {
      cancelled = true;
    };
  }, [open, currentDirectory]);

  useEffect(() => {
    if (!open) {
      return;
    }

    function onEscape(event: KeyboardEvent): void {
      if (event.key === 'Escape') {
        onClose();
      }
    }

    window.addEventListener('keydown', onEscape);
    return () => {
      window.removeEventListener('keydown', onEscape);
    };
  }, [open, onClose]);

  const existingPathSet = useMemo(() => new Set(existingPaths), [existingPaths]);

  const directoryEntries = useMemo(
    () => entries.filter((entry) => entry.kind === 'directory'),
    [entries]
  );

  const fileEntries = useMemo(
    () => entries.filter((entry) => entry.kind === 'file'),
    [entries]
  );

  const visibleFiles = useMemo(
    () => fileEntries.filter((entry) => isSupportedAttachmentPath(entry.path)),
    [fileEntries]
  );

  const unsupportedCount = fileEntries.length - visibleFiles.length;
  const selectedCount = selectedPaths.length;

  function toggleSelection(filePath: string): void {
    setSelectedPaths((existing) => {
      if (existing.includes(filePath)) {
        return existing.filter((path) => path !== filePath);
      }
      return [...existing, filePath];
    });
  }

  function addSelected(): void {
    if (selectedPaths.length === 0) {
      return;
    }

    const attachments = selectedPaths.map((filePath) => buildUiAttachment(filePath));
    onAddAttachments(attachments);
    setSelectedPaths([]);
    onClose();
  }

  if (!open) {
    return null;
  }

  return (
    <div className="file-picker-overlay" role="dialog" aria-modal="true" aria-label="File picker">
      <section className="file-picker-modal">
        <header className="file-picker-header">
          <h3>Select Attachments</h3>
          <button type="button" className="button-muted" onClick={onClose}>
            Close
          </button>
        </header>

        <p className="file-picker-path" title={currentDirectory}>
          {currentDirectory}
        </p>

        <div className="file-picker-actions">
          <button
            type="button"
            className="button-muted"
            onClick={() => {
              const parent = pathParent(currentDirectory);
              if (!pathWithinRoot(parent, projectRoot)) {
                return;
              }
              setCurrentDirectory(parent);
            }}
            disabled={currentDirectory === projectRoot}
          >
            Up
          </button>
          <button
            type="button"
            className="button-muted"
            onClick={() => {
              setSelectedPaths(visibleFiles.map((entry) => entry.path));
            }}
            disabled={visibleFiles.length === 0}
          >
            Select Visible
          </button>
          <button
            type="button"
            className="button-muted"
            onClick={() => {
              setSelectedPaths([]);
            }}
            disabled={selectedCount === 0}
          >
            Clear
          </button>
          <button type="button" onClick={addSelected} disabled={selectedCount === 0}>
            Add Selected ({selectedCount})
          </button>
        </div>

        <p className="file-picker-meta">
          Allowed extensions: {SUPPORTED_ATTACHMENT_EXTENSIONS.join(', ')}
        </p>

        {loading ? <p className="panel-empty">Loading directory entries...</p> : null}
        {error ? <p className="panel-error">{error}</p> : null}

        {!loading && !error ? (
          <div className="file-picker-grid">
            <section>
              <h4>Directories</h4>
              <ul className="file-picker-list">
                {directoryEntries.length === 0 ? <li className="panel-empty">No subdirectories.</li> : null}
                {directoryEntries.map((entry) => (
                  <li key={entry.path}>
                    <button
                      type="button"
                      className="file-picker-directory"
                      onClick={() => {
                        if (!pathWithinRoot(entry.path, projectRoot)) {
                          return;
                        }
                        setCurrentDirectory(entry.path);
                      }}
                    >
                      {entry.name}
                    </button>
                  </li>
                ))}
              </ul>
            </section>

            <section>
              <h4>Files</h4>
              <ul className="file-picker-list">
                {visibleFiles.length === 0 ? <li className="panel-empty">No supported files in this folder.</li> : null}
                {visibleFiles.map((entry) => {
                  const checked = selectedPaths.includes(entry.path);
                  const alreadyAttached = existingPathSet.has(entry.path);
                  return (
                    <li key={entry.path} className="file-picker-file">
                      <label>
                        <input
                          type="checkbox"
                          checked={checked}
                          onChange={() => {
                            toggleSelection(entry.path);
                          }}
                        />
                        <span>{entry.name}</span>
                      </label>
                      {alreadyAttached ? <small>already attached</small> : null}
                    </li>
                  );
                })}
              </ul>
              {unsupportedCount > 0 ? (
                <p className="file-picker-meta">{unsupportedCount} file(s) hidden by extension filter.</p>
              ) : null}
            </section>
          </div>
        ) : null}
      </section>
    </div>
  );
}
