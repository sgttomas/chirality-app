import { createElement } from 'react';
import { act, create, type ReactTestInstance, type ReactTestRenderer } from 'react-test-renderer';
import { beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  appendEvent: vi.fn(),
  bootHarnessSession: vi.fn(),
  clearEvents: vi.fn(),
  createHarnessSession: vi.fn(),
  interruptHarnessSession: vi.fn(),
  setStreaming: vi.fn(),
  streamHarnessTurn: vi.fn()
}));

vi.mock('next/navigation', () => ({
  usePathname: () => '/chat',
  useSearchParams: () => new URLSearchParams()
}));

vi.mock('../../components/workspace/workspace-provider', () => ({
  useWorkspace: () => ({ projectRoot: '/tmp/chirality-workroot' })
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
      onAddAttachments: (attachments: Array<{
        path: string;
        displayName: string;
        mimeType: string;
        clientType: 'text';
      }>) => void;
    }) =>
      element(
        'button',
        {
          type: 'button',
          'data-testid': 'fixture-add-attachment',
          onClick: () =>
            onAddAttachments([
              {
                path: '/tmp/chirality-workroot/retry.md',
                displayName: 'retry.md',
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

function byClass(root: ReactTestInstance, className: string): ReactTestInstance[] {
  return root.findAll((node) =>
    typeof node.props.className === 'string'
      ? node.props.className.split(/\s+/).includes(className)
      : false
  );
}

describe('ChatPanel failed-send retry state', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('restores the entered draft and attachment after session API failure', async () => {
    mocks.createHarnessSession.mockRejectedValueOnce(new Error('session API unavailable'));

    let renderer: ReactTestRenderer;
    await act(async () => {
      renderer = create(createElement(ChatPanel));
    });

    const root = renderer!.root;
    const input = root.findByProps({ 'aria-label': 'Chat input' });
    const addAttachment = root.findByProps({ 'data-testid': 'fixture-add-attachment' });

    await act(async () => {
      input.props.onChange({ target: { value: 'Retry this exact draft' } });
      addAttachment.props.onClick();
    });

    expect(root.findByProps({ 'aria-label': 'Chat input' }).props.value).toBe(
      'Retry this exact draft'
    );
    expect(root.findAllByProps({ title: '/tmp/chirality-workroot/retry.md' })).toHaveLength(1);

    const form = root.findByProps({ className: 'chat-input-row' });
    await act(async () => {
      form.props.onSubmit({ preventDefault: vi.fn() });
      await Promise.resolve();
    });

    expect(mocks.createHarnessSession).toHaveBeenCalledWith({
      projectRoot: '/tmp/chirality-workroot',
      persona: 'HELP_HUMAN',
      roleId: 'HELP_HUMAN',
      mode: 'CHAT',
      interactionMode: 'chat',
      permissionMode: 'workspaceWrite',
      selectedMethods: []
    });
    expect(mocks.bootHarnessSession).not.toHaveBeenCalled();
    expect(mocks.streamHarnessTurn).not.toHaveBeenCalled();

    const restoredInput = root.findByProps({ 'aria-label': 'Chat input' });
    expect(restoredInput.props.value).toBe('Retry this exact draft');
    expect(restoredInput.props.disabled).toBe(false);
    expect(root.findAllByProps({ title: '/tmp/chirality-workroot/retry.md' })).toHaveLength(1);

    const send = root.findAllByType('button').find((node) => node.children.includes('Send'));
    expect(send?.props.disabled).toBe(false);

    const errors = byClass(root, 'chat-runtime-error');
    expect(errors).toHaveLength(1);
    expect(errors[0].findAllByType('p').map((node) => node.children.join(' '))).toEqual(
      expect.arrayContaining(['Unexpected Harness Failure', 'session API unavailable'])
    );

    expect(byClass(root, 'chat-bubble--operator')).toHaveLength(0);
    expect(byClass(root, 'chat-bubble--assistant')).toHaveLength(1);
    expect(
      root
        .findAllByType('p')
        .some((node) => node.children.includes('Retry this exact draft'))
    ).toBe(false);
    expect(mocks.clearEvents).toHaveBeenCalledOnce();
    expect(mocks.setStreaming).toHaveBeenNthCalledWith(1, true);
    expect(mocks.setStreaming).toHaveBeenLastCalledWith(false);
  });
});
