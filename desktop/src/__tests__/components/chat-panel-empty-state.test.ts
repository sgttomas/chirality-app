import { createElement } from 'react';
import { act, create, type ReactTestInstance, type ReactTestRenderer } from 'react-test-renderer';
import { beforeEach, describe, expect, it, vi } from 'vitest';

/**
 * D-APP-36 render evidence for the Stage C composer/empty-state arrangement
 * (TRB-APPDEV-WOVEN-REDESIGN-2026-07-24 §5 Stage C, objective 1/4).
 *
 * The defect: the woven chat panel laid out as a grid whose child count moved
 * with state, so the transcript's flexible row could be squeezed below the
 * transcript box's own minimum and its content drew on top of the Attachments
 * row. The fix pins the panel to four rows by wrapping every between-transcript
 * -and-composer notice in a single `.chat-composer-dock`.
 *
 * These assertions are structural — they hold the arrangement the CSS fix
 * depends on. They deliberately do not assert copy, colours or geometry.
 */

const mocks = vi.hoisted(() => ({
  appendEvent: vi.fn(),
  bootHarnessSession: vi.fn(),
  clearEvents: vi.fn(),
  createHarnessSession: vi.fn(),
  interruptHarnessSession: vi.fn(),
  setStreaming: vi.fn(),
  streamHarnessTurn: vi.fn(),
  projectRoot: undefined as string | undefined
}));

vi.mock('next/navigation', () => ({
  usePathname: () => '/chat',
  useSearchParams: () => new URLSearchParams()
}));

vi.mock('../../components/workspace/workspace-provider', () => ({
  useWorkspace: () => ({ projectRoot: mocks.projectRoot })
}));

vi.mock('../../components/workspace/toolkit-provider', () => ({
  useToolkit: () => ({ optsPayload: undefined })
}));

vi.mock('../../components/workspace/harness-events-provider', () => ({
  useHarnessEventActions: () => ({
    appendEvent: mocks.appendEvent,
    clearEvents: mocks.clearEvents,
    hydrateEvents: vi.fn(),
    setStreaming: mocks.setStreaming
  }),
  useHarnessEvents: () => ({ events: [], streaming: false })
}));

vi.mock('../../lib/harness/client', async (importOriginal) => {
  const original = await importOriginal<typeof import('../../lib/harness/client')>();
  return {
    ...original,
    bootHarnessSession: mocks.bootHarnessSession,
    createHarnessSession: mocks.createHarnessSession,
    interruptHarnessSession: mocks.interruptHarnessSession,
    streamHarnessTurn: mocks.streamHarnessTurn,
    getHarnessTurnState: vi.fn(async () => ({ active: false, lastSeq: 0 })),
    attachHarnessTurn: vi.fn(async () => undefined)
  };
});

vi.mock('../../components/shell/file-picker', async () => {
  const { createElement: element } = await import('react');
  return {
    FilePicker: ({
      onAddAttachments
    }: {
      onAddAttachments: (
        attachments: Array<{
          path: string;
          displayName: string;
          mimeType: string;
          clientType: 'text';
        }>
      ) => void;
    }) =>
      element(
        'button',
        {
          type: 'button',
          'data-testid': 'fixture-add-attachment',
          onClick: () =>
            onAddAttachments([
              {
                path: '/tmp/chirality-workroot/notes.md',
                displayName: 'notes.md',
                mimeType: 'text/markdown',
                clientType: 'text'
              }
            ])
        },
        'Add fixture attachment'
      )
  };
});

vi.mock('../../components/shell/permission-requests', () => ({
  PermissionRequests: () => null
}));

import { ChatPanel } from '../../components/shell/chat-panel';

function hasClass(node: ReactTestInstance, className: string): boolean {
  return typeof node.props.className === 'string'
    ? node.props.className.split(/\s+/).includes(className)
    : false;
}

function byClass(root: ReactTestInstance, className: string): ReactTestInstance[] {
  return root.findAll((node) => hasClass(node, className));
}

/**
 * The laid-out rows of the chat panel: its direct host-element children.
 * `FilePicker` is a composite child and never a row — in the app it renders
 * `null` when closed and a `position: fixed` overlay when open.
 */
function panelRows(root: ReactTestInstance): ReactTestInstance[] {
  const panel = root.findByProps({ className: 'panel panel--chat' });
  return panel.children.filter(
    (child): child is ReactTestInstance =>
      typeof child !== 'string' && typeof child.type === 'string'
  );
}

async function renderPanel(): Promise<ReactTestInstance> {
  let renderer: ReactTestRenderer;
  await act(async () => {
    renderer = create(createElement(ChatPanel));
  });
  return renderer!.root;
}

describe('ChatPanel empty-state and composer arrangement', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.projectRoot = undefined;
  });

  it('keeps the transcript empty state inside the transcript, above a single composer dock', async () => {
    const root = await renderPanel();

    const rows = panelRows(root);

    // The conversation stage owns the transcript (and the Plan sidebar when
    // active), while the dock and composer remain independent grid rows.
    expect(rows).toHaveLength(4);
    expect(hasClass(rows[0], 'panel-header')).toBe(true);
    expect(hasClass(rows[1], 'chat-conversation-stage')).toBe(true);
    expect(hasClass(rows[2], 'chat-composer-dock')).toBe(true);
    expect(rows[3].props.className).toBe('chat-input-row');
    const transcript = byClass(rows[1], 'chat-transcript')[0];
    expect(transcript).toBeDefined();

    // The working-root empty state belongs to the transcript, not to the dock.
    const transcriptEmpty = byClass(transcript, 'panel-empty');
    expect(transcriptEmpty).toHaveLength(1);
    expect(transcriptEmpty[0].children.join(' ')).toContain('Working Root');
    expect(byClass(rows[2], 'chat-attachment-preview')).toHaveLength(1);
    expect(byClass(transcript, 'chat-attachment-preview')).toHaveLength(0);

    // The attachments empty state is a separate node inside the dock.
    const dockEmpty = byClass(rows[2], 'panel-empty');
    expect(dockEmpty).toHaveLength(1);
    expect(dockEmpty[0].children.join(' ')).toBe('No attachments selected.');

    // Composer stays a sibling of the dock so it is never scrolled away.
    expect(byClass(rows[2], 'chat-input-row')).toHaveLength(0);
  });

  it('disables the composer and both attachment actions while no Working Root is selected', async () => {
    const root = await renderPanel();

    const input = root.findByProps({ 'aria-label': 'Chat input' });
    expect(input.props.disabled).toBe(true);
    expect(input.props.placeholder).toBe('Select a Working Root first...');
    expect(input.props['data-chat-input']).toBe('primary');

    const send = root.findAllByType('button').find((node) => node.children.includes('Send'));
    expect(send?.props.disabled).toBe(true);

    const attach = root
      .findAllByType('button')
      .find((node) => node.children.includes('Attach Files'));
    expect(attach?.props.disabled).toBe(true);
  });

  it('moves the runtime notices into the dock without disturbing the transcript', async () => {
    mocks.projectRoot = '/tmp/chirality-workroot';
    mocks.createHarnessSession.mockRejectedValueOnce(new Error('session API unavailable'));

    let renderer: ReactTestRenderer;
    await act(async () => {
      renderer = create(createElement(ChatPanel));
    });
    const root = renderer!.root;

    await act(async () => {
      root.findByProps({ 'aria-label': 'Chat input' }).props.onChange({
        target: { value: 'a prompt' }
      });
    });

    await act(async () => {
      root.findByProps({ className: 'chat-input-row' }).props.onSubmit({
        preventDefault: vi.fn()
      });
      await Promise.resolve();
    });

    const rows = panelRows(root);

    // Still four rows with the error showing.
    expect(rows).toHaveLength(4);
    const dock = rows[2];
    expect(hasClass(dock, 'chat-composer-dock')).toBe(true);
    expect(byClass(dock, 'chat-runtime-error')).toHaveLength(1);
    expect(byClass(rows[1], 'chat-runtime-error')).toHaveLength(0);
    expect(rows[3].props.className).toBe('chat-input-row');
  });

  it('renders one attachment chip title per attachment inside the dock', async () => {
    mocks.projectRoot = '/tmp/chirality-workroot';
    const root = await renderPanel();

    await act(async () => {
      root.findByProps({ 'data-testid': 'fixture-add-attachment' }).props.onClick();
    });

    expect(root.findAllByProps({ title: '/tmp/chirality-workroot/notes.md' })).toHaveLength(1);

    const rows = panelRows(root);
    expect(byClass(rows[2], 'attachment-chip')).toHaveLength(1);
    expect(byClass(rows[2], 'panel-empty')).toHaveLength(0);
  });
});
