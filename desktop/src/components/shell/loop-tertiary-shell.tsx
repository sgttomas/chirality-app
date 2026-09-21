'use client';

import { Suspense, useMemo } from 'react';
import { ChatPanel } from './chat-panel';
import { ShellFrame, type ShellSection } from './shell-frame';
import { SidebarRightLoopLayout } from './sidebar-right-loop-layout';
import { createTertiarySidebarTabs } from './tertiary-sidebar-tabs';
import type { SidebarTabId } from './workspace-sidebar';

type LoopTertiaryShellProps = {
  defaultSidebarTab: SidebarTabId;
  section: ShellSection;
  subtitle: string;
  title: string;
};

/**
 * Loop-first route shell for tertiary entry routes. The route-specific form is
 * opened in the right sidebar while the live loop remains the primary pane.
 */
export function LoopTertiaryShell({
  defaultSidebarTab,
  section,
  subtitle,
  title
}: LoopTertiaryShellProps): JSX.Element {
  const tertiaryTabs = useMemo(() => createTertiarySidebarTabs(), []);

  return (
    <ShellFrame section={section} title={title} subtitle={subtitle}>
      <SidebarRightLoopLayout defaultSidebarTab={defaultSidebarTab} {...tertiaryTabs}>
        <div className="loop-chat-host">
          <Suspense
            fallback={
              <aside className="panel panel--chat">
                <header className="panel-header">
                  <h2>Chat Panel</h2>
                </header>
                <div className="panel-body chat-transcript">
                  <p className="panel-empty">Loading chat panel...</p>
                </div>
              </aside>
            }
          >
            <ChatPanel />
          </Suspense>
        </div>
      </SidebarRightLoopLayout>
    </ShellFrame>
  );
}
