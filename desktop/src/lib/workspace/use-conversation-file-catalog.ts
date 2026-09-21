'use client';

import { useCallback, useEffect, useState } from 'react';
import { collectFilePaths, type FileCatalog } from '../../components/shell/file-tree-panel';

// One shared empty catalog: a fresh array per render would re-derive every
// consumer memo (the chat panel's published plan model among them) and, with
// the shell re-rendering on each publication, spin the renderer until a tree
// arrived (D-GOV-43 review F-1).
const NO_PATHS: readonly string[] = [];

/** Keep file navigation available when the Files panel is closed. */
export function useConversationFileCatalog(projectRoot: string | null, streaming: boolean, runtimeEpoch: number) {
  const [catalog, setCatalog] = useState<FileCatalog | null>(null);
  const acceptCatalog = useCallback((next: FileCatalog | null) => {
    setCatalog(next?.root === projectRoot ? next : null);
  }, [projectRoot]);

  useEffect(() => {
    if (!projectRoot || streaming) return;
    let cancelled = false;
    // Refresh after a turn as well as on initial entry: a tool may have created files.
    void (async () => {
      try {
        const response = await fetch(`/api/working-root/tree?projectRoot=${encodeURIComponent(projectRoot)}&depth=4`);
        const payload = await response.json();
        if (!response.ok || !payload.root || payload.root.path !== projectRoot) throw new Error('File catalog unavailable');
        if (!cancelled) setCatalog({ root: projectRoot, paths: collectFilePaths(payload.root) });
      } catch {
        if (!cancelled) setCatalog(null);
      }
    })();
    return () => { cancelled = true; };
  }, [projectRoot, streaming, runtimeEpoch]);

  // A stale response/catalog from another folder can never resolve a chat link.
  return { paths: catalog?.root === projectRoot ? catalog.paths : NO_PATHS, acceptCatalog };
}
