"use client";

import React, { useEffect, useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface FilePreviewProps {
  path: string | null;
  projectRoot: string | null;
}

type PreviewMode = "file" | "diff";
type DiffState = "changed" | "clean" | "untracked" | "ignored" | "not_repo";
type DiffRowType = "file" | "meta" | "hunk" | "add" | "del" | "ctx";
type DiffDisplayRow = DiffRow | CollapsedDiffRow;

interface DiffPayload {
  state: DiffState;
  diff: string;
  message?: string;
}

interface DiffRow {
  type: DiffRowType;
  oldLine: number | null;
  newLine: number | null;
  text: string;
}

interface CollapsedDiffRow {
  type: "collapse";
  oldLine: number | null;
  newLine: number | null;
  oldRange: string;
  newRange: string;
  hiddenCount: number;
}

const COLLAPSE_THRESHOLD = 12;
const COLLAPSE_LEADING_CONTEXT = 2;
const COLLAPSE_TRAILING_CONTEXT = 2;

function parseDiffState(value: unknown): DiffState {
  if (value === "changed" || value === "clean" || value === "untracked" || value === "ignored" || value === "not_repo") {
    return value;
  }
  return "clean";
}

function parseHunkStart(line: string): { oldStart: number; newStart: number } | null {
  const match = line.match(/^@@\s*-(\d+)(?:,\d+)?\s+\+(\d+)(?:,\d+)?\s*@@/);
  if (!match) {
    return null;
  }

  return {
    oldStart: Number.parseInt(match[1], 10),
    newStart: Number.parseInt(match[2], 10),
  };
}

function parseUnifiedDiff(diffText: string): DiffRow[] {
  if (!diffText.trim()) {
    return [];
  }

  const rows: DiffRow[] = [];
  const lines = diffText.split("\n");
  let oldLine: number | null = null;
  let newLine: number | null = null;

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    if (index === lines.length - 1 && line === "") {
      continue;
    }

    if (line.startsWith("diff --git")) {
      rows.push({ type: "file", oldLine: null, newLine: null, text: line });
      oldLine = null;
      newLine = null;
      continue;
    }

    if (
      line.startsWith("index ") ||
      line.startsWith("new file mode ") ||
      line.startsWith("deleted file mode ") ||
      line.startsWith("rename from ") ||
      line.startsWith("rename to ") ||
      line.startsWith("similarity index ") ||
      line.startsWith("old mode ") ||
      line.startsWith("new mode ") ||
      line.startsWith("Binary files ") ||
      line.startsWith("--- ") ||
      line.startsWith("+++ ")
    ) {
      rows.push({ type: "meta", oldLine: null, newLine: null, text: line });
      continue;
    }

    if (line.startsWith("@@")) {
      const hunk = parseHunkStart(line);
      if (hunk) {
        oldLine = hunk.oldStart;
        newLine = hunk.newStart;
      } else {
        oldLine = null;
        newLine = null;
      }
      rows.push({ type: "hunk", oldLine: null, newLine: null, text: line });
      continue;
    }

    if (line.startsWith("\\ ")) {
      rows.push({ type: "meta", oldLine: null, newLine: null, text: line });
      continue;
    }

    if (line.startsWith("+")) {
      rows.push({ type: "add", oldLine: null, newLine, text: line });
      if (newLine !== null) {
        newLine += 1;
      }
      continue;
    }

    if (line.startsWith("-")) {
      rows.push({ type: "del", oldLine, newLine: null, text: line });
      if (oldLine !== null) {
        oldLine += 1;
      }
      continue;
    }

    if (line.startsWith(" ")) {
      rows.push({ type: "ctx", oldLine, newLine, text: line });
      if (oldLine !== null) {
        oldLine += 1;
      }
      if (newLine !== null) {
        newLine += 1;
      }
      continue;
    }

    rows.push({ type: "meta", oldLine: null, newLine: null, text: line });
  }

  return rows;
}

function collapseContextRows(rows: DiffRow[], changesOnly: boolean): DiffDisplayRow[] {
  if (!changesOnly) {
    return rows;
  }

  const output: DiffDisplayRow[] = [];

  for (let index = 0; index < rows.length; index += 1) {
    const row = rows[index];
    if (row.type !== "ctx") {
      output.push(row);
      continue;
    }

    let end = index;
    while (end + 1 < rows.length && rows[end + 1].type === "ctx") {
      end += 1;
    }

    const run = rows.slice(index, end + 1);
    if (run.length <= COLLAPSE_THRESHOLD) {
      output.push(...run);
      index = end;
      continue;
    }

    const keepHead = run.slice(0, COLLAPSE_LEADING_CONTEXT);
    const keepTail = run.slice(run.length - COLLAPSE_TRAILING_CONTEXT);
    const hidden = run.length - keepHead.length - keepTail.length;

    output.push(...keepHead);

    if (hidden > 0) {
      const firstHidden = run[COLLAPSE_LEADING_CONTEXT];
      const lastHidden = run[run.length - COLLAPSE_TRAILING_CONTEXT - 1];
      const oldRange =
        firstHidden.oldLine !== null && lastHidden.oldLine !== null
          ? `${firstHidden.oldLine}-${lastHidden.oldLine}`
          : "";
      const newRange =
        firstHidden.newLine !== null && lastHidden.newLine !== null
          ? `${firstHidden.newLine}-${lastHidden.newLine}`
          : "";

      output.push({
        type: "collapse",
        oldLine: firstHidden.oldLine,
        newLine: firstHidden.newLine,
        oldRange,
        newRange,
        hiddenCount: hidden,
      });
    }

    output.push(...keepTail);
    index = end;
  }

  return output;
}

function DiffViewer({ diffText, changesOnly }: { diffText: string; changesOnly: boolean }) {
  const rows = useMemo(() => parseUnifiedDiff(diffText), [diffText]);
  const displayRows = useMemo(() => collapseContextRows(rows, changesOnly), [rows, changesOnly]);

  return (
    <div className="ui-panel shadow-md overflow-hidden">
      <div className="grid grid-cols-[70px_70px_minmax(0,1fr)] border-b border-[var(--color-border)]/55 bg-[var(--color-surface-mid)]/65 px-0 py-1.5">
        <span className="mono px-3 text-right text-[9px] font-semibold uppercase tracking-[0.08em] text-[var(--color-text-dim)]/80">
          Old
        </span>
        <span className="mono px-3 text-right text-[9px] font-semibold uppercase tracking-[0.08em] text-[var(--color-text-dim)]/80">
          New
        </span>
        <span className="mono px-3 text-[9px] font-semibold uppercase tracking-[0.08em] text-[var(--color-text-dim)]/80">
          Diff
        </span>
      </div>

      <div className="max-h-full overflow-auto">
        <div className="min-w-[700px]">
          {displayRows.map((row, index) => {
            if (row.type === "collapse") {
              const oldRange = row.oldRange || "…";
              const newRange = row.newRange || "…";
              return (
                <div
                  key={`${index}-collapse-${row.hiddenCount}-${oldRange}-${newRange}`}
                  className="grid grid-cols-[70px_70px_minmax(0,1fr)] border-l-2 border-l-[var(--color-border)]/80 bg-[var(--color-surface-high)]/52 text-[12px] leading-6"
                >
                  <span className="mono px-3 text-right tabular-nums text-[11px] text-[var(--color-text-dim)]/75">{oldRange}</span>
                  <span className="mono px-3 text-right tabular-nums text-[11px] text-[var(--color-text-dim)]/75">{newRange}</span>
                  <span className="mono px-3 whitespace-pre text-[11px] font-semibold tracking-[0.02em] text-[var(--color-text-dim)]">
                    {`… ${row.hiddenCount} unchanged line${row.hiddenCount === 1 ? "" : "s"} …`}
                  </span>
                </div>
              );
            }

            const isAdd = row.type === "add";
            const isDel = row.type === "del";
            const isCtx = row.type === "ctx";
            const isHunk = row.type === "hunk";
            const isFile = row.type === "file";

            let rowClass =
              "grid grid-cols-[70px_70px_minmax(0,1fr)] border-l-2 border-transparent text-[12px] leading-6";
            let numberClass = "mono px-3 text-right tabular-nums text-[11px] text-[var(--color-text-dim)]/75";
            let contentClass = "mono px-3 whitespace-pre text-[12px] text-[var(--color-text-main)]/88";
            let markerClass = "text-[var(--color-text-dim)]/80";

            if (isAdd) {
              rowClass += " border-l-[var(--color-judging)] bg-[var(--color-judging)]/12";
              numberClass = "mono px-3 text-right tabular-nums text-[11px] text-[var(--color-judging)]/85";
              contentClass = "mono px-3 whitespace-pre text-[12px] text-[var(--color-text-main)]/92";
              markerClass = "text-[var(--color-judging)]";
            } else if (isDel) {
              rowClass += " border-l-[var(--color-accent-orange)] bg-[var(--color-accent-orange)]/11";
              numberClass = "mono px-3 text-right tabular-nums text-[11px] text-[var(--color-accent-text)]/88";
              contentClass = "mono px-3 whitespace-pre text-[12px] text-[var(--color-text-main)]/92";
              markerClass = "text-[var(--color-accent-text)]";
            } else if (isHunk) {
              rowClass += " border-l-[var(--color-applying)] bg-[var(--color-applying)]/12";
              contentClass = "mono px-3 whitespace-pre text-[11px] font-semibold tracking-[0.02em] text-[var(--color-applying)]";
              markerClass = "text-[var(--color-applying)]";
            } else if (isFile) {
              rowClass += " border-l-[var(--color-accent-orange)] bg-[var(--color-surface-high)]/72";
              contentClass = "mono px-3 whitespace-pre text-[11px] font-semibold tracking-[0.02em] text-[var(--color-accent-text)]";
              markerClass = "text-[var(--color-accent-text)]";
            } else if (row.type === "meta") {
              rowClass += " bg-[var(--color-surface-high)]/48";
              contentClass = "mono px-3 whitespace-pre text-[11px] text-[var(--color-text-dim)]";
            } else if (isCtx) {
              rowClass += " hover:bg-[var(--color-surface-low)]/45";
            }

            const marker = row.text.charAt(0);
            const body = row.text.slice(1);
            const showSplitMarker = isAdd || isDel || isCtx;

            return (
              <div key={`${index}-${row.type}-${row.oldLine ?? "n"}-${row.newLine ?? "n"}`} className={rowClass}>
                <span className={numberClass}>{row.oldLine ?? ""}</span>
                <span className={numberClass}>{row.newLine ?? ""}</span>
                <span className={contentClass}>
                  {showSplitMarker ? <span className={markerClass}>{marker}</span> : null}
                  {showSplitMarker ? body : row.text}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export function FilePreview({ path, projectRoot }: FilePreviewProps) {
  const [mode, setMode] = useState<PreviewMode>("file");
  const [changesOnly, setChangesOnly] = useState(false);
  const [content, setContent] = useState<string>("");
  const [loadingContent, setLoadingContent] = useState(false);
  const [diffPayload, setDiffPayload] = useState<DiffPayload | null>(null);
  const [diffError, setDiffError] = useState<string | null>(null);
  const [loadingDiff, setLoadingDiff] = useState(false);

  useEffect(() => {
    if (!path) {
      return;
    }

    let canceled = false;
    queueMicrotask(() => setLoadingContent(true));

    const params = new URLSearchParams({ path });
    if (projectRoot) {
      params.set("projectRoot", projectRoot);
    }

    fetch(`/api/fs/read?${params.toString()}`)
      .then((res) => res.json())
      .then((data) => {
        if (canceled) return;
        if (typeof data.content === "string") setContent(data.content);
        else if (data.error) setContent(`Error: ${data.error}`);
        else setContent("");
        setLoadingContent(false);
      })
      .catch((err) => {
        if (canceled) return;
        setContent(`Error: ${err.message}`);
        setLoadingContent(false);
      });

    return () => {
      canceled = true;
    };
  }, [path, projectRoot]);

  useEffect(() => {
    if (!path || mode !== "diff") {
      return;
    }

    let canceled = false;
    queueMicrotask(() => {
      setLoadingDiff(true);
      setDiffPayload(null);
      setDiffError(null);
    });

    const params = new URLSearchParams({ path });
    if (projectRoot) {
      params.set("projectRoot", projectRoot);
    }

    fetch(`/api/fs/diff?${params.toString()}`)
      .then((res) => res.json())
      .then((data) => {
        if (canceled) return;
        if (typeof data.error === "string") {
          setDiffError(data.error);
          setDiffPayload(null);
          setLoadingDiff(false);
          return;
        }

        setDiffPayload({
          state: parseDiffState(data.state),
          diff: typeof data.diff === "string" ? data.diff : "",
          message: typeof data.message === "string" ? data.message : undefined,
        });
        setDiffError(null);
        setLoadingDiff(false);
      })
      .catch((err) => {
        if (canceled) return;
        setDiffError(err.message);
        setDiffPayload(null);
        setLoadingDiff(false);
      });

    return () => {
      canceled = true;
    };
  }, [mode, path, projectRoot]);

  const isMarkdown = mode === "file" && path?.toLowerCase().endsWith(".md");
  const fileName = path ? path.split("/").filter(Boolean).pop() ?? path : "No file selected";
  const loading = mode === "file" ? loadingContent : loadingDiff;

  let statusLabel = "Idle";
  let statusClass = "text-[var(--color-text-dim)] border-[var(--color-border)] bg-[var(--color-surface-low)]";

  if (path) {
    if (loading) {
      statusLabel = "Loading";
      statusClass = "text-[var(--color-accent-text)] border-[var(--color-accent-orange)]/30 bg-[var(--color-accent-orange)]/10";
    } else if (mode === "file") {
      statusLabel = isMarkdown ? "Markdown" : "Text";
      statusClass = isMarkdown
        ? "text-[var(--color-judging)] border-[var(--color-judging)]/35 bg-[var(--color-judging)]/10"
        : "text-[var(--color-applying)] border-[var(--color-applying)]/35 bg-[var(--color-applying)]/10";
    } else if (diffError) {
      statusLabel = "Diff Error";
      statusClass = "text-[var(--color-accent-text)] border-[var(--color-accent-orange)]/35 bg-[var(--color-accent-orange)]/10";
    } else {
      switch (diffPayload?.state) {
        case "changed":
          statusLabel = "Changed";
          statusClass = "text-[var(--color-accent-text)] border-[var(--color-accent-orange)]/35 bg-[var(--color-accent-orange)]/10";
          break;
        case "untracked":
          statusLabel = "Untracked";
          statusClass = "text-[var(--color-applying)] border-[var(--color-applying)]/35 bg-[var(--color-applying)]/10";
          break;
        case "ignored":
          statusLabel = "Ignored";
          statusClass = "text-[var(--color-text-dim)] border-[var(--color-border)] bg-[var(--color-surface-low)]";
          break;
        case "not_repo":
          statusLabel = "No Repo";
          statusClass = "text-[var(--color-text-dim)] border-[var(--color-border)] bg-[var(--color-surface-low)]";
          break;
        default:
          statusLabel = "Clean";
          statusClass = "text-[var(--color-judging)] border-[var(--color-judging)]/35 bg-[var(--color-judging)]/10";
          break;
      }
    }
  }

  const toggleButtonBase = "ui-control ui-focus-ring px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.1em]";
  const fileActive = mode === "file";
  const diffActive = mode === "diff";
  const changesOnlyDisabled = !diffPayload?.diff || loadingDiff || !!diffError;

  return (
    <section className="content-area flex h-full min-h-0 flex-col overflow-hidden rounded-[inherit] bg-transparent">
      <header className="content-header ui-panel-soft flex items-center justify-between gap-3 rounded-none border-t-0 border-x-0 pl-4 pr-14 py-3">
        <div className="min-w-0">
          <p className="ui-type-mono-meta text-[9px] font-semibold text-[var(--color-accent-text)]/85">
            Preview Deck
          </p>
          <p className="mono truncate text-[11px] text-[var(--color-text-main)]/90" title={path ?? "No file selected"}>
            {fileName}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1 rounded-md border border-[var(--color-border)]/80 bg-[var(--color-surface-low)]/78 p-1">
            <button
              type="button"
              onClick={() => setMode("file")}
              className={`${toggleButtonBase} ${
                fileActive
                  ? "border-[var(--color-accent-orange)]/35 bg-[var(--color-accent-orange)]/10 text-[var(--color-accent-text)]"
                  : "border-transparent text-[var(--color-text-dim)]"
              }`}
            >
              File
            </button>
            <button
              type="button"
              onClick={() => setMode("diff")}
              disabled={!path}
              className={`${toggleButtonBase} ${
                diffActive
                  ? "border-[var(--color-accent-orange)]/35 bg-[var(--color-accent-orange)]/10 text-[var(--color-accent-text)]"
                  : "border-transparent text-[var(--color-text-dim)]"
              } ${!path ? "cursor-not-allowed opacity-50" : ""}`}
            >
              Diff
            </button>
            {mode === "diff" ? (
              <button
                type="button"
                onClick={() => setChangesOnly((prev) => !prev)}
                disabled={changesOnlyDisabled}
                className={`${toggleButtonBase} ${
                  changesOnly
                    ? "text-[var(--color-judging)]"
                    : "border-transparent text-[var(--color-text-dim)]"
                } ${changesOnlyDisabled ? "cursor-not-allowed opacity-50" : ""}`}
                style={
                  changesOnly
                    ? {
                        borderColor: "rgba(16, 185, 129, 0.55)",
                        backgroundColor: "rgba(16, 185, 129, 0.2)",
                        color: "var(--color-judging)",
                        boxShadow: "inset 0 0 0 1px rgba(16, 185, 129, 0.16)",
                      }
                    : undefined
                }
                title="Collapse unchanged context lines"
              >
                Changes Only
              </button>
            ) : null}
          </div>
          <span className={`mono rounded border px-2 py-1 text-[10px] font-semibold uppercase tracking-[0.1em] ${statusClass}`}>
            {statusLabel}
          </span>
        </div>
      </header>

      <div className="custom-scrollbar flex-1 min-h-0 overflow-y-auto px-5 py-4">
        {!path ? (
          <div className="ui-panel-soft flex h-full items-center justify-center rounded-xl px-6 text-center">
            <p className="mono text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--color-text-dim)]">
              Select a file to preview.
            </p>
          </div>
        ) : loading ? (
          <div className="ui-panel-soft flex h-full items-center justify-center gap-2 rounded-xl px-6 text-center">
            <span className="h-2.5 w-2.5 rounded-full bg-[var(--color-accent-orange)] animate-pulse" aria-hidden />
            <p className="mono text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--color-text-dim)]">
              {mode === "diff" ? "Loading git diff..." : "Loading content..."}
            </p>
          </div>
        ) : mode === "diff" ? (
          diffError ? (
            <div className="ui-panel-soft flex h-full items-center justify-center rounded-xl px-6 text-center">
              <p className="mono whitespace-pre-wrap text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--color-accent-text)]">
                Diff error: {diffError}
              </p>
            </div>
          ) : diffPayload?.diff ? (
            <DiffViewer diffText={diffPayload.diff} changesOnly={changesOnly} />
          ) : (
            <div className="ui-panel-soft flex h-full items-center justify-center rounded-xl px-6 text-center">
              <p className="mono text-[11px] font-semibold uppercase tracking-[0.12em] text-[var(--color-text-dim)]">
                {diffPayload?.message ?? "No git changes for this file."}
              </p>
            </div>
          )
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
