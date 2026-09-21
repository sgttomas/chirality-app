'use client';
import React, { useEffect, useState } from 'react';
import type { WorkflowList, WorkflowPreview } from '../../app/api/working-root/workflow/workflow-read-contract';
import { WorkflowDetail } from './workflow-detail';
import styles from './workflows.module.css';
type Props = { projectRoot: string; name: string | null; refresh: number; onOpen: (name: string) => void };
export function WorkflowsView({ projectRoot, name, refresh, onOpen }: Props): JSX.Element {
  const key = JSON.stringify([projectRoot, name, refresh]);
  const [result, setResult] = useState<{ key: string; data?: WorkflowList | WorkflowPreview; error?: string } | null>(null);
  useEffect(() => {
    const controller = new AbortController(); let active = true;
    const params = new URLSearchParams({ projectRoot }); if (name) params.set('name', name);
    void fetch(`/api/working-root/workflow?${params}`, { signal: controller.signal, cache: 'no-store' })
      .then(async response => {
        const body = await response.json();
        if (!response.ok) throw new Error(body.error?.message ?? 'The plans could not be read. Refresh to try again.');
        if (body.projectRoot !== projectRoot) throw new Error('The folder changed. Refresh to read its plans.');
        if (active) setResult({ key, data: body });
      }).catch(error => { if (active) setResult({ key, error: error instanceof Error ? error.message : 'The plans could not be read. Refresh to try again.' }); });
    return () => { active = false; controller.abort(); };
  }, [projectRoot, name, refresh, key]);
  const current = result?.key === key ? result : null;
  return <div className={styles.view}>
    <p className={styles.notice}>Plan details cannot be checked yet</p>
    {!current ? <p role="status">Loading {name ? 'plan' : 'workflows'}…</p> : current.error ? <p role="alert">{current.error}</p> : current.data && 'content' in current.data ? <WorkflowDetail preview={current.data} /> : current.data && 'files' in current.data ? <>
      <p className={styles.caption}>In this folder</p>
      {current.data.files.length ? <ul className={styles.list}>{current.data.files.map(file => <li key={file.name}>
        <button type="button" className={styles.file} onClick={() => onOpen(file.name)}><span>{file.name}</span><small>{new Date(file.modifiedAt).toLocaleDateString()}</small></button>
      </li>)}</ul> : <p>No workflow files here yet. Plans are read from <code>.chirality/workflows</code> in this folder.</p>}
      <p className={styles.foot}>Read-only · {current.data.files.length} {current.data.files.length === 1 ? 'file' : 'files'}</p>
    </> : null}
  </div>;
}
