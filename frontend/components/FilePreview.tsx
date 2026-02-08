"use client";

import React, { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface FilePreviewProps {
  path: string | null;
}

export function FilePreview({ path }: FilePreviewProps) {
  const [content, setContent] = useState<string>("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!path) {
      return;
    }

    let canceled = false;
    queueMicrotask(() => setLoading(true));
    fetch(`/api/fs/read?path=${encodeURIComponent(path)}`)
      .then((res) => res.json())
      .then((data) => {
        if (canceled) return;
        if (typeof data.content === "string") setContent(data.content);
        else if (data.error) setContent(`Error: ${data.error}`);
        else setContent("");
        setLoading(false);
      })
      .catch((err) => {
        if (canceled) return;
        setContent(`Error: ${err.message}`);
        setLoading(false);
      });

    return () => {
      canceled = true;
    };
  }, [path]);

  const isMarkdown = path?.toLowerCase().endsWith(".md");
  const fileName = path ? path.split("/").filter(Boolean).pop() ?? path : "No file selected";
  const statusLabel = !path ? "Idle" : loading ? "Loading" : isMarkdown ? "Markdown" : "Text";
  const statusClass = !path
    ? "text-[var(--color-text-dim)] border-[var(--color-border)] bg-[var(--color-surface-low)]"
    : loading
      ? "text-[var(--color-accent-orange)] border-[var(--color-accent-orange)]/30 bg-[var(--color-accent-orange)]/10"
      : isMarkdown
        ? "text-[var(--color-judging)] border-[var(--color-judging)]/35 bg-[var(--color-judging)]/10"
        : "text-[var(--color-applying)] border-[var(--color-applying)]/35 bg-[var(--color-applying)]/10";

  return (
    <section className="content-area ui-panel flex h-full min-h-0 flex-col overflow-hidden">
      <header className="content-header flex items-center justify-between gap-3 border-b border-[var(--color-border)] bg-[var(--color-surface-mid)]/55 px-4 py-3">
        <div className="min-w-0">
          <p className="ui-type-mono-meta text-[9px] font-semibold text-[var(--color-accent-orange)]/80">
            File Preview
          </p>
          <p className="mono truncate text-[11px] text-[var(--color-text-main)]/90" title={path ?? "No file selected"}>
            {fileName}
          </p>
        </div>
        <span className={`mono rounded border px-2 py-1 text-[10px] font-semibold uppercase tracking-[0.1em] ${statusClass}`}>
          {statusLabel}
        </span>
      </header>

      <div className="flex-1 min-h-0 overflow-y-auto px-5 py-4 custom-scrollbar">
        {!path ? (
          <div className="ui-panel-soft flex h-full items-center justify-center rounded-md px-6 text-center">
            <p className="mono text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--color-text-dim)]">
              Select a file to preview.
            </p>
          </div>
        ) : loading ? (
          <div className="ui-panel-soft flex h-full items-center justify-center gap-2 rounded-md px-6 text-center">
            <span className="h-2.5 w-2.5 rounded-full bg-[var(--color-accent-orange)] animate-pulse" aria-hidden />
            <p className="mono text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--color-text-dim)]">
              Loading content...
            </p>
          </div>
        ) : isMarkdown ? (
          <div className="markdown-content text-[var(--color-text-main)]/92">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
          </div>
        ) : (
          <pre className="mono whitespace-pre-wrap break-words text-[13px] leading-6 text-[var(--color-text-main)]/88">
            {content}
          </pre>
        )}
      </div>
    </section>
  );
}

  
