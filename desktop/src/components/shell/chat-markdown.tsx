'use client';

import React from 'react';
import ReactMarkdown, { type Components } from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { hasAnsiEscapeCodes, renderAnsiToHtml } from '../../lib/shell/ansi';

function extractLanguage(className: string | undefined): string {
  if (!className) {
    return '';
  }

  if (!className.startsWith('language-')) {
    return '';
  }

  return className.replace('language-', '').trim().toLowerCase();
}

function trimTrailingFenceNewline(value: string): string {
  return value.endsWith('\n') ? value.slice(0, -1) : value;
}

export function resolveCatalogFileLink(
  href: string | undefined,
  projectRoot: string | null | undefined,
  fileCatalog: readonly string[]
): string | null {
  if (!href || !projectRoot || href.includes('\\') || /[\u0000-\u001f\u007f]/.test(href)) {
    return null;
  }

  const withoutFragment = href.split('#', 1)[0];
  let decoded: string;
  try {
    decoded = decodeURIComponent(withoutFragment);
  } catch {
    return null;
  }

  if (!decoded || decoded.includes('?') || decoded.includes('\\') || /[\u0000-\u001f\u007f]/.test(decoded) || /^[a-z][a-z0-9+.-]*:/i.test(decoded)) {
    return null;
  }

  const relative = decoded.startsWith('./') ? decoded.slice(2) : decoded;
  const segments = relative.startsWith('/') ? relative.slice(1).split('/') : relative.split('/');
  if (segments.some((segment) => !segment || segment === '..' || segment === '.')) {
    return null;
  }

  const normalizedRoot = projectRoot.replace(/\/$/, '');
  const candidate = relative.startsWith('/') ? relative : `${normalizedRoot}/${relative}`;
  const prefix = `${normalizedRoot}/`;
  if (!candidate.startsWith(prefix)) {
    return null;
  }
  return fileCatalog.filter((path) => path === candidate).length === 1 ? candidate : null;
}

function markdownComponents(
  projectRoot: string | null | undefined,
  fileCatalog: readonly string[],
  onOpenFile: ((path: string) => void) | undefined
): Components {
  return {
  a: ({ href, children }) => {
    const openFile = onOpenFile;
    const catalogFile = openFile ? resolveCatalogFileLink(href, projectRoot, fileCatalog) : null;
    if (!catalogFile || !openFile) {
      return <a href={href} target="_blank" rel="noreferrer noopener">{children}</a>;
    }
    return <a href={href} onClick={(event) => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      openFile(catalogFile);
    }}>{children}</a>;
  },
  pre: ({ children }) => <pre className="chat-code-block">{children}</pre>,
  code: (props) => {
    const className = 'className' in props ? (props.className as string | undefined) : undefined;
    const rawText = trimTrailingFenceNewline(String(props.children ?? ''));
    const language = extractLanguage(className);
    const shouldUseAnsiFallback = language === 'ansi' || hasAnsiEscapeCodes(rawText);

    if (shouldUseAnsiFallback) {
      return (
          <code
            className="chat-ansi chat-code-block--ansi"
            dangerouslySetInnerHTML={{
              __html: renderAnsiToHtml(rawText)
            }}
          />
      );
    }

    return (
        <code className={className}>{rawText}</code>
    );
  }
  };
}

type ChatMarkdownProps = {
  source: string;
  projectRoot?: string | null;
  fileCatalog?: readonly string[];
  onOpenFile?: (path: string) => void;
};

export function ChatMarkdown({ source, projectRoot, fileCatalog = [], onOpenFile }: ChatMarkdownProps): JSX.Element {
  return (
    <div className="chat-markdown">
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents(projectRoot, fileCatalog, onOpenFile)}>
        {source}
      </ReactMarkdown>
    </div>
  );
}
