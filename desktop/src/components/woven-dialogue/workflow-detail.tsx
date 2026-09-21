import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import type { WorkflowPreview } from '../../app/api/working-root/workflow/workflow-read-contract';
import styles from './workflows.module.css';
export function WorkflowDetail({ preview }: { preview: WorkflowPreview }): JSX.Element {
  return <>
    <article className={styles.markdown} aria-label="Plan file preview"><ReactMarkdown skipHtml remarkPlugins={[remarkGfm]} components={{
      // Files are untrusted input. Preview links are text, images never request
      // remote or local resources, and task checkboxes remain inert.
      a: ({ children }) => <span>{children}</span>,
      img: ({ alt }) => <span>[Image{alt ? `: ${alt}` : ''}]</span>,
      input: ({ checked }) => <input type="checkbox" disabled checked={Boolean(checked)} readOnly />
    }}>{preview.content}</ReactMarkdown></article>
    <details className={styles.provenance}><summary>File details</summary><dl>
      <dt>Path</dt><dd>{preview.file.path}</dd><dt>Modified</dt><dd>{new Date(preview.file.modifiedAt).toLocaleString()}</dd>
      <dt>Size</dt><dd>{preview.file.size.toLocaleString()} bytes</dd><dt>SHA-256</dt><dd>{preview.sha256}</dd>
    </dl><p>This is a file preview. Its content does not confirm approvals or completed work.</p></details>
  </>;
}
