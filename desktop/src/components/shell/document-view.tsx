'use client';

import React, { useEffect, useMemo, useRef, useState } from 'react';
import ReactMarkdown, { type Components } from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { resolveDocumentViewState } from '../../lib/shell/document-view-state';
import { useWorkspace } from '../workspace/workspace-provider';
import { ChatMarkdown } from './chat-markdown';

type Deliverable = {
  id: string;
  name: string;
  pkg: string;
  status: string;
  path: string;
};

type DeliverablesResponse = {
  deliverables?: Deliverable[];
  deliverableContracts?: Array<{
    path: string;
    selectedProductionDocuments: Array<{ fileName: string }>;
  }>;
  error?: { message?: string };
};

type ContentResponse = {
  content?: string;
  file?: string;
  error?: { message?: string };
};

// The well-known deliverable document files (see the knowledge buckets in
// `lib/workspace/filesystem.ts`). `_STATUS.md` is always present; the rest are
// offered so the viewer can open whichever the deliverable contains. A missing
// file simply surfaces the endpoint's 404.
const CONTROL_PLANE_DOCUMENT_FILES = [
  '_STATUS.md',
  '_CONTEXT.md',
  '_REFERENCES.md',
  '_DEPENDENCIES.md',
  '_SEMANTIC.md',
  'MEMORY.md'
];

const DEFAULT_FILE = '_STATUS.md';

function LegacyDocumentView(): JSX.Element {
  const { projectRoot } = useWorkspace();
  const [deliverables, setDeliverables] = useState<Deliverable[]>([]);
  const [canonicalDocumentsByPath, setCanonicalDocumentsByPath] = useState<
    Record<string, string[]>
  >({});
  const [rosterLoading, setRosterLoading] = useState(false);
  const [rosterError, setRosterError] = useState<string | null>(null);
  const [selectedPath, setSelectedPath] = useState<string>('');
  const [selectedFile, setSelectedFile] = useState<string>(DEFAULT_FILE);

  const [content, setContent] = useState<string | null>(null);
  const [contentLoading, setContentLoading] = useState(false);
  const [contentError, setContentError] = useState<string | null>(null);

  // Load the deliverable roster whenever the Working Root changes.
  useEffect(() => {
    let cancelled = false;
    setDeliverables([]);
    setCanonicalDocumentsByPath({});
    setRosterError(null);
    setSelectedPath('');
    setContent(null);
    setContentError(null);

    if (!projectRoot) {
      setRosterLoading(false);
      return () => {
        cancelled = true;
      };
    }

    setRosterLoading(true);

    async function loadRoster(): Promise<void> {
      try {
        const response = await fetch(
          `/api/project/deliverables?projectRoot=${encodeURIComponent(projectRoot as string)}`
        );
        const payload = (await response.json()) as DeliverablesResponse;
        if (cancelled) {
          return;
        }
        if (!response.ok || !payload.deliverables) {
          throw new Error(payload.error?.message ?? 'Unable to load deliverables.');
        }
        setDeliverables(payload.deliverables);
        setCanonicalDocumentsByPath(
          Object.fromEntries(
            (payload.deliverableContracts ?? []).map((contract) => [
              contract.path,
              contract.selectedProductionDocuments.map((file) => file.fileName)
            ])
          )
        );
        setSelectedPath(payload.deliverables[0]?.path ?? '');
      } catch (error) {
        if (cancelled) {
          return;
        }
        setRosterError(error instanceof Error ? error.message : 'Unable to load deliverables.');
      } finally {
        if (!cancelled) {
          setRosterLoading(false);
        }
      }
    }

    void loadRoster();
    return () => {
      cancelled = true;
    };
  }, [projectRoot]);

  // Fetch the selected document content.
  useEffect(() => {
    let cancelled = false;
    if (!projectRoot || !selectedPath) {
      setContent(null);
      setContentError(null);
      setContentLoading(false);
      return () => {
        cancelled = true;
      };
    }

    async function loadContent(): Promise<void> {
      setContentLoading(true);
      setContentError(null);
      try {
        const response = await fetch(
          `/api/working-root/deliverable/content?projectRoot=${encodeURIComponent(
            projectRoot as string
          )}&deliverablePath=${encodeURIComponent(selectedPath)}&file=${encodeURIComponent(
            selectedFile
          )}`
        );
        const payload = (await response.json()) as ContentResponse;
        if (cancelled) {
          return;
        }
        if (!response.ok || typeof payload.content !== 'string') {
          throw new Error(payload.error?.message ?? 'Unable to load document.');
        }
        setContent(payload.content);
      } catch (error) {
        if (cancelled) {
          return;
        }
        setContent(null);
        setContentError(error instanceof Error ? error.message : 'Unable to load document.');
      } finally {
        if (!cancelled) {
          setContentLoading(false);
        }
      }
    }

    void loadContent();
    return () => {
      cancelled = true;
    };
  }, [projectRoot, selectedPath, selectedFile]);

  const documentFiles = useMemo(
    () => [
      CONTROL_PLANE_DOCUMENT_FILES[0],
      ...(canonicalDocumentsByPath[selectedPath] ?? []),
      ...CONTROL_PLANE_DOCUMENT_FILES.slice(1)
    ],
    [canonicalDocumentsByPath, selectedPath]
  );

  const body = useMemo(() => {
    const state = resolveDocumentViewState({
      hasProjectRoot: Boolean(projectRoot),
      rosterLoading,
      rosterError,
      deliverableCount: deliverables.length,
      contentLoading,
      contentError,
      hasContent: content !== null
    });

    switch (state.kind) {
      case 'no-root':
        return <p className="panel-empty">Select a Working Root to view deliverable documents.</p>;
      case 'roster-loading':
        return <p className="panel-empty">Loading deliverables...</p>;
      case 'roster-error':
        return <p className="panel-error">{state.message}</p>;
      case 'empty':
        return <p className="panel-empty">No deliverables found in this Working Root.</p>;
      case 'content-loading':
        return <p className="panel-empty">Loading document...</p>;
      case 'content-error':
        return <p className="panel-error">{state.message}</p>;
      case 'content':
        return <ChatMarkdown source={content as string} />;
      case 'idle':
      default:
        return <p className="panel-empty">Select a deliverable and document to preview.</p>;
    }
  }, [projectRoot, rosterLoading, rosterError, deliverables, contentLoading, contentError, content]);

  return (
    <aside className="panel panel--document">
      <header className="panel-header">
        <h2>Document</h2>
        {deliverables.length > 0 ? (
          <div className="document-view-controls">
            <label className="document-view-selector">
              <span>Deliverable</span>
              <select
                value={selectedPath}
                onChange={(event) => {
                  setSelectedPath(event.target.value);
                  setSelectedFile(DEFAULT_FILE);
                }}
              >
                {deliverables.map((deliverable) => (
                  <option key={deliverable.path} value={deliverable.path}>
                    {deliverable.id} — {deliverable.name}
                  </option>
                ))}
              </select>
            </label>
            <label className="document-view-selector">
              <span>File</span>
              <select
                value={selectedFile}
                onChange={(event) => {
                  setSelectedFile(event.target.value);
                }}
              >
                {documentFiles.map((file) => (
                  <option key={file} value={file}>
                    {file}
                  </option>
                ))}
              </select>
            </label>
          </div>
        ) : null}
      </header>
      <div className="panel-body document-view-body">{body}</div>
    </aside>
  );
}


type FilePreview = {
  target: string; name: string; size: number; modifiedAt: string;
  kind: 'text' | 'pdf' | 'office' | 'image' | 'unsupported'; tooLarge: boolean; content?: string;
};
type DocumentHandoffRequest = { projectRoot: string; target: string; action: 'quick-look' | 'open' | 'reveal' } | { projectRoot: string; action: 'reveal-root' };
type DocumentBridge = { document?: { inlinePdfPreview?: boolean; handoff: (input: DocumentHandoffRequest) => Promise<{ ok: boolean; error?: { message?: string } }> } };

export async function handoffDocument(input: DocumentHandoffRequest): Promise<void> {
  const bridge = typeof window === 'undefined' ? undefined : (window as unknown as { chirality?: DocumentBridge }).chirality?.document;
  if (!bridge) throw new Error('Open the desktop app to use native document actions.');
  const result = await bridge.handoff(input);
  if (!result.ok) throw new Error(result.error?.message ?? 'Unable to open the file.');
}

// Quoted CSV fields can contain commas and newlines. Stop after 500 logical rows.
export function previewCsv(source: string): string[][] {
  const rows: string[][] = []; let row: string[] = [], field = '', quoted = false;
  const cell = () => { if (row.length < 200) row.push(field); field = ''; };
  for (let i = 0; i < source.length && rows.length < 500; i++) {
    const char = source[i];
    if (char === '"') {
      if (quoted && source[i + 1] === '"') { field += '"'; i++; }
      else quoted = !quoted;
    } else if (char === ',' && !quoted) cell();
    else if (char === '\n' && !quoted) { cell(); rows.push(row); row = []; }
    else if (char !== '\r' || quoted) field += char;
  }
  if (rows.length < 500 && (row.length || field)) { cell(); rows.push(row); }
  return rows;
}

type DocumentHeading = { id: string; title: string; level: number };

/** Only literal relative working-root paths can become local document selections. */
export function resolveLocalDocumentLink(target: string, href: string): string | null {
  let decoded: string;
  try { decoded = decodeURIComponent(href.split('#')[0]); } catch { return null; }
  if (!decoded || decoded.startsWith('/') || /[\\\x00-\x1f?:]/.test(decoded) ||
      decoded.split('/').some(segment => segment === '..' || segment === '')) return null;
  const directory = target.includes('/') ? target.slice(0, target.lastIndexOf('/') + 1) : '';
  const result = directory + decoded.split('/').filter(segment => segment !== '.').join('/');
  return result && !result.split('/').includes('..') ? result : null;
}

function PlainFileText({ content }: { content: string }): JSX.Element {
  const [line, setLine] = useState<number | null>(null);
  const [point, setPoint] = useState({ left: 0, top: 0 });
  return <div>
    <pre style={{ whiteSpace: 'pre-wrap', overflowWrap: 'anywhere' }} onMouseMove={event => {
      // Ask Chromium which text offset is under the pointer; wrapping does not
      // change the source-line number and no per-line million-node DOM is built.
      const browserDocument = document as Document & { caretRangeFromPoint?: (x: number, y: number) => Range | null };
      const caret = browserDocument.caretRangeFromPoint?.(event.clientX, event.clientY);
      if (!caret || !event.currentTarget.contains(caret.startContainer)) { setLine(null); return; }
      const prefix = document.createRange(); prefix.selectNodeContents(event.currentTarget); prefix.setEnd(caret.startContainer, caret.startOffset);
      const text = prefix.toString(); let number = 1;
      for (let index = 0; index < text.length; index++) if (text[index] === '\n') number++;
      setLine(number);
      setPoint({ left: event.clientX + 12, top: event.clientY + 12 });
    }} onMouseLeave={() => setLine(null)}>{content}</pre>
    {line !== null ? <output aria-label="Source line" style={{ position: 'fixed', ...point, padding: '2px 6px', background: 'var(--surface)', border: '1px solid var(--rule)', pointerEvents: 'none', zIndex: 20 }}>Line {line}</output> : null}
  </div>;
}

type JsonPreviewNode = { label: string; value?: string; children?: JsonPreviewNode[]; disclosure?: string };
export function buildJsonPreview(value: unknown): JsonPreviewNode {
  let remaining = 2000;
  const build = (item: unknown, label: string, depth: number): JsonPreviewNode => {
    if (--remaining < 0) return { label, disclosure: 'Item budget reached.' };
    if (item === null || typeof item !== 'object') return { label, value: JSON.stringify(item) };
    if (depth >= 12) return { label, disclosure: 'Depth limit reached.' };
    const keys = Object.keys(item);
    const children: JsonPreviewNode[] = [];
    for (const key of keys) {
      if (remaining <= 0 || children.length >= 200) break;
      children.push(build((item as Record<string, unknown>)[key], key, depth + 1));
    }
    return { label, children, ...(children.length < keys.length ? { disclosure: `Showing ${children.length} of ${keys.length} entries.` } : {}) };
  };
  return build(value, Array.isArray(value) ? 'Array' : value !== null && typeof value === 'object' ? 'Object' : 'Value', 0);
}
function JsonNode({ node, root = false }: { node: JsonPreviewNode; root?: boolean }): JSX.Element {
  if (!node.children) return <div><strong>{node.label}</strong>: <code>{node.value ?? node.disclosure}</code></div>;
  return <details open={root}><summary>{node.label}</summary><div style={{ paddingLeft: 14 }}>{node.children.map((child, index) => <JsonNode key={index} node={child} />)}{node.disclosure ? <p>{node.disclosure}</p> : null}</div></details>;
}
function JsonFile({ content }: { content: string }): JSX.Element {
  const result = useMemo(() => {
    try { return { tree: buildJsonPreview(JSON.parse(content)) }; }
    catch { return { error: 'Invalid JSON. Showing the original text.' }; }
  }, [content]);
  return result.tree ? <div aria-label="JSON tree"><p>Folded preview: up to 2,000 items, 200 entries per object and 12 levels. Limits are disclosed where reached.</p><JsonNode node={result.tree} root /></div> : <><p role="alert">{result.error}</p><PlainFileText content={content} /></>;
}

function FileMarkdown({ content, target, onOpenDocument, onHeadings }: { content: string; target: string; onOpenDocument?: (path: string) => void; onHeadings: (headings: DocumentHeading[]) => void }): JSX.Element {
  const contentRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    const headings = Array.from(contentRef.current?.querySelectorAll<HTMLHeadingElement>('h1, h2, h3, h4, h5, h6') ?? []);
    onHeadings(headings.map(heading => ({ id: heading.id, title: heading.textContent ?? '', level: Number(heading.tagName.slice(1)) })));
  }, [content, onHeadings]);
  const components: Components = {
    a: ({ href, children }) => {
      if (href && /^https?:\/\//i.test(href)) return <a href={href} target="_blank" rel="noreferrer noopener">{children}</a>;
      if (href?.startsWith('#')) return <a href={href} onClick={event => {
        event.preventDefault();
        let anchor: string; try { anchor = decodeURIComponent(href.slice(1)); } catch { return; }
        const heading = Array.from(contentRef.current?.querySelectorAll<HTMLElement>('[id]') ?? []).find(item => item.id === anchor || item.textContent?.toLowerCase().replace(/[^a-z0-9 -]/g, '').replace(/ +/g, '-') === anchor);
        heading?.scrollIntoView({ block: 'nearest' }); heading?.focus();
      }}>{children}</a>;
      const local = href ? resolveLocalDocumentLink(target, href) : null;
      return local && onOpenDocument ? <a href={href} onClick={event => { event.preventDefault(); onOpenDocument(local); }}>{children}</a> : <span title="This link cannot be opened safely.">{children}</span>;
    },
    // Untrusted Markdown cannot trigger remote image fetches in the file viewer.
    img: ({ alt }) => <span>{alt ?? 'Image'}</span>
  };
  for (const level of [1, 2, 3, 4, 5, 6] as const) {
    components[`h${level}`] = ({ node, children }) => React.createElement(`h${level}`, { id: `document-heading-${node?.position?.start.offset ?? 0}`, tabIndex: -1 }, children);
  }
  return <div className="chat-markdown" ref={contentRef}><ReactMarkdown remarkPlugins={[remarkGfm]} skipHtml components={components}>{content}</ReactMarkdown></div>;
}

function FileDocumentView({ target, onOpenDocument, expanded, presentation }: { target: string; onOpenDocument?: (path: string) => void; expanded?: boolean; presentation?: 'woven' }): JSX.Element {
  const { projectRoot } = useWorkspace();
  const [loaded, setLoaded] = useState<{ key: string; preview?: FilePreview; error?: string } | null>(null);
  const [reload, setReload] = useState(0);
  const [actionError, setActionError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [headings, setHeadings] = useState<DocumentHeading[]>([]);
  const [naturalImage, setNaturalImage] = useState(false);
  const [pdfUnavailable, setPdfUnavailable] = useState(false);
  const documentBodyRef = useRef<HTMLDivElement | null>(null);
  const key = JSON.stringify([projectRoot, target, reload]);
  const url = `/api/working-root/file?projectRoot=${encodeURIComponent(projectRoot ?? '')}&target=${encodeURIComponent(target)}`;
  useEffect(() => {
    let cancelled = false;
    setActionError(null); setHeadings([]); setNaturalImage(false); setPdfUnavailable(false);
    if (projectRoot) void fetch(url).then(async response => {
      const preview = await response.json();
      if (!response.ok) throw new Error(preview.error?.message ?? 'Unable to load file.');
      if (!cancelled) setLoaded({ key, preview });
    }).catch(error => { if (!cancelled) setLoaded({ key, error: error instanceof Error ? error.message : 'Unable to load file.' }); });
    return () => { cancelled = true; };
  }, [key, projectRoot, url]);
  const preview = loaded?.key === key ? loaded.preview : undefined;
  const error = loaded?.key === key ? loaded.error : undefined;
  const desktop = typeof window === 'undefined' ? undefined : (window as unknown as { chirality?: DocumentBridge }).chirality;
  const bridge = desktop?.document;
  const inlinePdfPreview = !desktop || bridge?.inlinePdfPreview === true;
  const handoff = async (action: 'quick-look' | 'open') => {
    if (!projectRoot || !bridge) return;
    setBusy(true); setActionError(null);
    try {
      await handoffDocument({ projectRoot, target, action });
    } catch (error) { setActionError(error instanceof Error ? error.message : 'Unable to open the file.'); }
    finally { setBusy(false); }
  };
  const markdown = /\.(md|markdown)$/i.test(target);
  const csv = /\.csv$/i.test(target);
  return <section className={`panel panel--document${presentation === 'woven' ? ' document-view--woven' : ''}`} aria-label="Document preview">
    <header className="panel-header"><h2 className={presentation === 'woven' && headings.some(heading => heading.level === 1) ? 'sr-only' : undefined}>{headings.find(heading => heading.level === 1)?.title || preview?.name || target.split('/').at(-1)}</h2>
      {presentation !== 'woven' ? <button type="button" onClick={() => setReload(value => value + 1)}>Reload</button> : null}
      {headings.length ? <details><summary>Headings</summary><nav aria-label="Document headings">{headings.map(heading => <button type="button" key={heading.id} onClick={() => {
        const element = Array.from(documentBodyRef.current?.querySelectorAll<HTMLElement>('[id]') ?? []).find(item => item.id === heading.id);
        element?.scrollIntoView({ block: 'nearest' }); element?.focus();
      }}>{heading.title}</button>)}</nav></details> : null}</header>
    <div ref={documentBodyRef} className="panel-body document-view-body" style={{ overflow: 'auto', overflowWrap: 'anywhere', minWidth: 0, ...(expanded ? { maxWidth: 640, margin: '0 auto', width: '100%', fontSize: 13.5, lineHeight: 1.6 } : {}) }}>
      {!projectRoot ? <p>Choose a folder to see its files.</p> : error ? <p role="alert">{error}</p> : !preview ? <p>Loading document…</p> : <>
        <p>{preview.name} · {preview.size.toLocaleString()} bytes · Modified {preview.modifiedAt}</p>
        {preview.kind === 'pdf' ? inlinePdfPreview && !pdfUnavailable ? <iframe title={preview.name} src={`${url}&content=pdf`} onError={() => setPdfUnavailable(true)} style={{ width: '100%', height: '65vh', border: 0 }} /> : <><p>PDF preview is unavailable here. Open this file in its default app.</p>{inlinePdfPreview ? <button type="button" onClick={() => { setPdfUnavailable(false); setReload(value => value + 1); }}>Retry PDF preview</button> : null}</> :
          preview.kind === 'image' && !preview.tooLarge ? <button type="button" aria-label={naturalImage ? 'Fit image to panel' : 'Show image at natural size'} onClick={() => setNaturalImage(value => !value)} style={{ display: 'block', padding: 0, maxWidth: naturalImage ? 'none' : '100%' }}>
            <img src={`${url}&content=image`} alt={preview.name} onError={() => setActionError('Unable to decode this image. Open it in its default app.')} style={{ display: 'block', maxWidth: naturalImage ? 'none' : '100%', height: 'auto' }} />
          </button> :
          preview.kind === 'text' && !preview.tooLarge ? (
            markdown ? <FileMarkdown content={preview.content ?? ''} target={target} onOpenDocument={onOpenDocument} onHeadings={setHeadings} /> : csv ? <>
              <p>Preview: first 500 rows, up to 200 columns.</p>
              <div style={{ overflow: 'auto' }}><table><tbody>{previewCsv(preview.content ?? '').map((row, i) => <tr key={i}>{row.map((value, j) => <td key={j}>{value}</td>)}</tr>)}</tbody></table></div>
            </> : /\.json$/i.test(target) ? <JsonFile content={preview.content ?? ''} /> : <PlainFileText content={preview.content ?? ''} />
          ) : <p>{preview.tooLarge ? preview.kind === 'image' ? 'This image exceeds the 2 MB image preview limit.' : 'This file exceeds the 10 MB text preview limit.' : preview.kind === 'office' ? 'Preview this Office document with Quick Look.' : 'This format is available in its default app.'}</p>}
        {preview.kind === 'office' ? <button type="button" disabled={!bridge || busy} onClick={() => void handoff('quick-look')}>Quick Look</button> : null}
        <button type="button" disabled={!bridge || busy} onClick={() => void handoff('open')}>Open in default app</button>
        {!bridge ? <p>Open the desktop app to use native document actions.</p> : null}
      </>}
      {actionError ? <p role="alert">{actionError}</p> : null}
    </div>
  </section>;
}

/** Optional file target extends, rather than replaces, the deliverable document viewer. */
export function DocumentView({ target, onOpenDocument, expanded, presentation }: { target?: string; onOpenDocument?: (path: string) => void; expanded?: boolean; presentation?: 'woven' } = {}): JSX.Element {
  const { projectRoot } = useWorkspace();
  return target === undefined ? <LegacyDocumentView /> : <FileDocumentView key={`${projectRoot}:${target}`} target={target} onOpenDocument={onOpenDocument} expanded={expanded} presentation={presentation} />;
}
