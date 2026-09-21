'use client';

import { Suspense } from 'react';
import { useHarnessStreaming } from '../workspace/harness-events-provider';
import { CHAT_SECTION } from '../../lib/shell/loop-first';
import { ChatPanel } from './chat-panel';
import { PersonaPicker } from './persona-picker';
import { ShellFrame } from './shell-frame';
import { SidebarRightLoopLayout } from './sidebar-right-loop-layout';
import { createTertiarySidebarTabs } from './tertiary-sidebar-tabs';

/**
 * The loop-first / direct-chat surface (`/chat`, D-APP-23 hybrid). The live loop
 * (ChatPanel) is the primary pane and the multi-view sidebar sits on the
 * **right**. The sidebar collapses without unmounting the chat, so an in-flight
 * turn survives the relayout (D-APP-23 constraint). The persona picker
 * (Type-0/Type-1, D-APP-24) drives the loop via `?agent=`.
 */
export function LoopShell(): JSX.Element {
  const streaming = useHarnessStreaming();
  const tertiaryTabs = createTertiarySidebarTabs();

  return (
    <ShellFrame
      section={CHAT_SECTION}
      title="Direct Chat"
      subtitle="Run a live session with a direct-entry role; the multi-view sidebar is on the right."
    >
      <SidebarRightLoopLayout defaultSidebarTab="tools" {...tertiaryTabs}>
        <div className="loop-persona-bar">
          <PersonaPicker disabled={streaming} />
          {streaming ? <p className="portal-launch-notice" role="status">Role changes pause while the current turn is running.</p> : null}
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
