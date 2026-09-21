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
import { useWorkspace } from './workspace-provider';
import { buildDeliverableCompositeKey } from '../../lib/workspace/task-scope';

export type DeliverableListItem = {
  id: string;
  name: string;
  pkg: string;
  status: string;
  path: string;
  key: string;
};

export type KnowledgeTypeListItem = {
  id: string;
  label: string;
  matchingDeliverableKeys: string[];
};

export type DeliverablesScan = {
  projectRoot: string;
  scannedAt: string;
  truncated: boolean;
  deliverables: DeliverableListItem[];
  knowledgeDecomposition: {
    enabled: boolean;
    markerFile: string | null;
  };
  knowledgeTypes: KnowledgeTypeListItem[];
};

type DeliverablesContextValue = {
  loading: boolean;
  error: string | null;
  scan: DeliverablesScan | null;
  refresh: () => void;
};

const DeliverablesContext = createContext<DeliverablesContextValue | null>(null);

type DeliverablesResponse = {
  projectRoot: string;
  scannedAt: string;
  truncated?: boolean;
  deliverables: Array<{
    id: string;
    name: string;
    pkg: string;
    status: string;
    path: string;
  }>;
  knowledgeDecomposition?: {
    enabled?: boolean;
    markerFile?: string | null;
  };
  knowledgeTypes?: Array<{
    id: string;
    label: string;
    matchingDeliverableKeys: string[];
  }>;
  error?: {
    message?: string;
  };
};

function normalizeResponse(payload: DeliverablesResponse): DeliverablesScan {
  const deliverables = payload.deliverables.map((deliverable) => ({
    ...deliverable,
    key: buildDeliverableCompositeKey(deliverable.pkg, deliverable.id)
  }));

  return {
    projectRoot: payload.projectRoot,
    scannedAt: payload.scannedAt,
    truncated: payload.truncated ?? false,
    deliverables,
    knowledgeDecomposition: {
      enabled: payload.knowledgeDecomposition?.enabled ?? false,
      markerFile: payload.knowledgeDecomposition?.markerFile ?? null
    },
    knowledgeTypes: payload.knowledgeTypes ?? []
  };
}

export function DeliverablesProvider({ children }: { children: ReactNode }): JSX.Element {
  const { projectRoot } = useWorkspace();
  const [refreshToken, setRefreshToken] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [scan, setScan] = useState<DeliverablesScan | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadDeliverables(): Promise<void> {
      if (!projectRoot) {
        setLoading(false);
        setError(null);
        setScan(null);
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const response = await fetch(
          `/api/project/deliverables?projectRoot=${encodeURIComponent(projectRoot)}`
        );
        const payload = (await response.json()) as DeliverablesResponse;

        if (!response.ok || !payload.deliverables || !payload.projectRoot || !payload.scannedAt) {
          throw new Error(payload.error?.message ?? 'Unable to scan project deliverables');
        }

        if (cancelled) {
          return;
        }

        setScan(normalizeResponse(payload));
      } catch (scanError) {
        if (cancelled) {
          return;
        }

        const message =
          scanError instanceof Error ? scanError.message : 'Unable to scan project deliverables';
        setError(message);
        setScan(null);
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadDeliverables();

    return () => {
      cancelled = true;
    };
  }, [projectRoot, refreshToken]);

  const refresh = useCallback(() => {
    setRefreshToken((value) => value + 1);
  }, []);

  const value = useMemo<DeliverablesContextValue>(
    () => ({
      loading,
      error,
      scan,
      refresh
    }),
    [loading, error, scan, refresh]
  );

  return <DeliverablesContext.Provider value={value}>{children}</DeliverablesContext.Provider>;
}

export function useDeliverables(): DeliverablesContextValue {
  const value = useContext(DeliverablesContext);
  if (!value) {
    throw new Error('useDeliverables must be used inside DeliverablesProvider');
  }
  return value;
}
