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
      setContent("");
      return;
    }

    setLoading(true);
    fetch(`/api/fs/read?path=${encodeURIComponent(path)}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.content) setContent(data.content);
        else if (data.error) setContent(`Error: ${data.error}`);
        setLoading(false);
      })
      .catch((err) => {
        setContent(`Error: ${err.message}`);
        setLoading(false);
      });
  }, [path]);

  const isMarkdown = path?.toLowerCase().endsWith(".md");

    return (

      <div className="content-area glass overflow-hidden flex flex-col h-full min-h-0">

        <div className="content-header shrink-0">

          <span className="mono uppercase text-sm tracking-widest truncate max-w-[70%]">

            PREVIEW: {path || "None Selected"}

          </span>

          <span className="context-status">{loading ? "LOADING..." : (isMarkdown ? "FORMATTED" : "RAW_TEXT")}</span>

        </div>

        <div className="flex-grow overflow-y-auto custom-scrollbar min-h-0">

          {path ? (

            <div className="p-10">

              {isMarkdown ? (

                <div className="markdown-content">

                  <ReactMarkdown remarkPlugins={[remarkGfm]}>

                    {content}

                  </ReactMarkdown>

                </div>

              ) : (

                <pre className="whitespace-pre-wrap font-mono text-sm text-[#cbd5e1]">

                  {content}

                </pre>

              )}

            </div>

          ) : (

            <div className="h-full flex items-center justify-center opacity-20 italic">

              Select a file to preview content

            </div>

          )}

        </div>

      </div>

    );

  }

  