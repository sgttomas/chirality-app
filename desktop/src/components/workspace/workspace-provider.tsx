'use client';

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode
} from 'react';

const PROJECT_ROOT_STORAGE_KEY = 'chirality.projectRoot';

/**
 * The most recent project root the user chose explicitly in this session
 * (native picker or a manually applied path). A root restored from storage on
 * startup is never a selection. `sequence` increases on every explicit choice,
 * including re-selecting the same folder, so consumers can act once per choice.
 */
export type WorkspaceSelection = { path: string; explicit: true; sequence: number };

type WorkspaceContextValue = {
  projectRoot: string | null;
  lastSelection: WorkspaceSelection | null;
  hasElectronDirectoryPicker: boolean;
  errorMessage: string | null;
  clearError: () => void;
  applyProjectRoot: (candidate: string) => Promise<boolean>;
  chooseProjectRoot: () => Promise<boolean>;
  clearProjectRoot: () => void;
};

const WorkspaceContext = createContext<WorkspaceContextValue | null>(null);

async function validateProjectRoot(projectRoot: string): Promise<string> {
  const response = await fetch('/api/working-root/validate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ projectRoot })
  });

  const payload = (await response.json()) as {
    ok?: boolean;
    projectRoot?: string;
    error?: {
      message?: string;
    };
  };

  if (!response.ok || !payload.projectRoot) {
    throw new Error(payload.error?.message ?? 'Working root validation failed');
  }

  return payload.projectRoot;
}

export function WorkspaceProvider({ children }: { children: ReactNode }): JSX.Element {
  const [projectRoot, setProjectRoot] = useState<string | null>(null);
  const [lastSelection, setLastSelection] = useState<WorkspaceSelection | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const hasElectronDirectoryPicker = typeof window !== 'undefined' && typeof window.chirality?.selectDirectory === 'function';

  useEffect(() => {
    if (typeof window === 'undefined') {
      return;
    }

    const stored = window.localStorage.getItem(PROJECT_ROOT_STORAGE_KEY);
    if (stored) {
      setProjectRoot(stored);
    }
  }, []);

  const clearError = useCallback(() => {
    setErrorMessage(null);
  }, []);

  const storeProjectRoot = useCallback((nextProjectRoot: string | null) => {
    setProjectRoot(nextProjectRoot);
    if (typeof window === 'undefined') {
      return;
    }

    if (nextProjectRoot) {
      window.localStorage.setItem(PROJECT_ROOT_STORAGE_KEY, nextProjectRoot);
    } else {
      window.localStorage.removeItem(PROJECT_ROOT_STORAGE_KEY);
    }
  }, []);

  const applyProjectRoot = useCallback(
    async (candidate: string): Promise<boolean> => {
      try {
        const normalized = await validateProjectRoot(candidate);
        storeProjectRoot(normalized);
        setLastSelection(current => ({
          path: normalized,
          explicit: true,
          sequence: (current?.sequence ?? 0) + 1
        }));
        setErrorMessage(null);
        return true;
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Unable to set project root';
        setErrorMessage(message);
        return false;
      }
    },
    [storeProjectRoot]
  );

  const clearProjectRoot = useCallback(() => {
    storeProjectRoot(null);
    setLastSelection(null);
    setErrorMessage(null);
  }, [storeProjectRoot]);

  const chooseProjectRoot = useCallback(async (): Promise<boolean> => {
    if (typeof window === 'undefined' || typeof window.chirality?.selectDirectory !== 'function') {
      setErrorMessage('Native directory picker is unavailable. Enter an absolute path manually.');
      return false;
    }

    try {
      const result = await window.chirality.selectDirectory();
      if (result.cancelled) {
        if (result.error) {
          setErrorMessage(result.error);
          return false;
        }

        return false;
      }

      if (!result.path) {
        setErrorMessage('Directory picker returned no path.');
        return false;
      }

      return applyProjectRoot(result.path);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Directory picker failed';
      setErrorMessage(message);
      return false;
    }
  }, [applyProjectRoot]);

  const value = useMemo<WorkspaceContextValue>(
    () => ({
      projectRoot,
      lastSelection,
      hasElectronDirectoryPicker,
      errorMessage,
      clearError,
      applyProjectRoot,
      chooseProjectRoot,
      clearProjectRoot
    }),
    [
      projectRoot,
      lastSelection,
      hasElectronDirectoryPicker,
      errorMessage,
      clearError,
      applyProjectRoot,
      chooseProjectRoot,
      clearProjectRoot
    ]
  );

  return <WorkspaceContext.Provider value={value}>{children}</WorkspaceContext.Provider>;
}

export function useWorkspace(): WorkspaceContextValue {
  const value = useContext(WorkspaceContext);
  if (!value) {
    throw new Error('useWorkspace must be used inside WorkspaceProvider');
  }

  return value;
}

/**
 * Tolerant read of the current explicit selection. Outside a
 * WorkspaceProvider (hosts that pass a root directly) there is no selection,
 * so callers fall back to manual-only behaviour instead of throwing.
 */
export function useWorkspaceSelection(): WorkspaceSelection | null {
  return useContext(WorkspaceContext)?.lastSelection ?? null;
}
