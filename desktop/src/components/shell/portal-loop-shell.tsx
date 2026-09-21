'use client';

import { Suspense } from 'react';
import { buildPortalPersonaHref } from '../../lib/shell/loop-first';
import { useHarnessStreaming } from '../workspace/harness-events-provider';
import { ChatPanel } from './chat-panel';
import { PersonaPicker } from './persona-picker';
import { ShellFrame } from './shell-frame';
import { SidebarRightLoopLayout } from './sidebar-right-loop-layout';
import { createTertiarySidebarTabs } from './tertiary-sidebar-tabs';

/**
 * Loop-first portal (`/`, D-APP-28/30). The live loop is the primary surface;
 * the matrix is demoted into the right sidebar's Portal tab. Matrix and picker
 * launches change only `?agent=` on the mounted loop, guarded mid-turn by the
 * shared streaming flag.
 */
export function PortalLoopShell(): JSX.Element {
  const streaming = useHarnessStreaming();
  const tertiaryTabs = createTertiarySidebarTabs();

  return (
    <ShellFrame
      section="PORTAL"
      title="Live Loop Portal"
      subtitle="Run the live harness loop first; use the right sidebar to reach matrix and workspace surfaces."
    >
      <SidebarRightLoopLayout defaultSidebarTab="portal" {...tertiaryTabs}>
        <div className="loop-persona-bar">
          <PersonaPicker buildHref={buildPortalPersonaHref} disabled={streaming} />
          {streaming ? (
            <p className="portal-launch-notice" role="status">
              Role changes pause while the current turn is running.
            </p>
          ) : null}
        </div>
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
