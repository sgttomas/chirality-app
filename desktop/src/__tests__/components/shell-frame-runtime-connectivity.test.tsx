import React from 'react';
import renderer, { act, type ReactTestRenderer } from 'react-test-renderer';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import type { RuntimeConnectivitySnapshot } from '../../lib/shell/runtime-connectivity';

/**
 * Coverage for the runtime-connectivity indicator the top bar gained alongside
 * the existing working-root chip. Kept in its own file because it needs a
 * `window` with a desktop bridge, which the working-root tests deliberately run
 * without.
 *
 * Same conventions as `shell-frame.test.tsx`: node environment, react-test-renderer,
 * class-name traversal, no CSS assertions.
 */

type WorkspaceFixture = {
  projectRoot: string | null;
  hasElectronDirectoryPicker: boolean;
  errorMessage: string | null;
  clearError: () => void;
  applyProjectRoot: (path: string) => Promise<void>;
  chooseProjectRoot: () => Promise<void>;
  clearProjectRoot: () => void;
};

const workspace = vi.hoisted(() => ({ value: null as unknown }));

vi.mock('next/navigation', () => ({ usePathname: () => '/' }));
vi.mock('next/link', () => ({
  default: ({ children, ...props }: React.AnchorHTMLAttributes<HTMLAnchorElement>) =>
    React.createElement('a', props, children)
}));
vi.mock('../../components/workspace/workspace-provider', () => ({
  useWorkspace: () => workspace.value
}));
vi.mock('../../components/settings/api-key-settings', () => ({ ApiKeySettings: () => null }));
vi.mock('../../components/settings/runtime-settings', () => ({ RuntimeSettings: () => null }));

function snapshot(
  overrides: Partial<RuntimeConnectivitySnapshot> = {}
): RuntimeConnectivitySnapshot {
  return {
    state: 'connected',
    failedAttempts: 0,
    lastError: null,
    changedAt: '2026-07-25T12:00:00.000Z',
    ...overrides
  };
}

type BridgeHarness = {
  push: (next: RuntimeConnectivitySnapshot) => void;
  status: ReturnType<typeof vi.fn>;
  unsubscribeCalls: () => number;
  listenerCount: () => number;
};

/**
 * Install a fake desktop connectivity bridge on the global `window`. The
 * explicit check reads the same bridge (`get`); the retired `runtime.daemon`
 * lifecycle IPC is absent, as it is in the App-owned Runtime build.
 */
function installBridge(
  initial: RuntimeConnectivitySnapshot | null,
  status: ReturnType<typeof vi.fn> = vi.fn(async () => initial)
): BridgeHarness {
  const listeners = new Set<(value: RuntimeConnectivitySnapshot) => void>();
  let unsubscribeCalls = 0;
  Object.assign(globalThis, {
    window: {
      chirality: {
        runtime: {
          connectivity: {
            get: status,
            subscribe: (listener: (value: RuntimeConnectivitySnapshot) => void) => {
              listeners.add(listener);
              return () => {
                unsubscribeCalls += 1;
                listeners.delete(listener);
              };
            }
          }
        }
      }
    }
  });
  return {
    push: (next) => {
      for (const listener of listeners) {
        listener(next);
      }
    },
    status,
    unsubscribeCalls: () => unsubscribeCalls,
    listenerCount: () => listeners.size
  };
}

async function renderShell(): Promise<ReactTestRenderer> {
  Object.assign(globalThis, { React });
  const { ShellFrame } = await import('../../components/shell/shell-frame');
  let tree!: ReactTestRenderer;
  await act(async () => {
    tree = renderer.create(
      <ShellFrame section="PORTAL" title="Portal" subtitle="Workspace">
        <div>content</div>
      </ShellFrame>
    );
  });
  return tree;
}

function textOf(node: renderer.ReactTestInstance): string {
  return node.children
    .map((child) => (typeof child === 'string' ? child : textOf(child)))
    .join('');
}

function findRuntimeChip(tree: ReactTestRenderer): renderer.ReactTestInstance | null {
  const matches = tree.root.findAll(
    (node) => String(node.props.className ?? '').startsWith('shell-runtime-chip ')
  );
  return matches[0] ?? null;
}

function findRuntimeDot(tree: ReactTestRenderer): renderer.ReactTestInstance | null {
  const matches = tree.root.findAll(
    (node) => String(node.props.className ?? '').startsWith('shell-runtime-dot ')
  );
  return matches[0] ?? null;
}

describe('ShellFrame runtime connectivity indicator', () => {
  beforeEach(() => {
    workspace.value = {
      projectRoot: '/tmp/execution-root',
      hasElectronDirectoryPicker: true,
      errorMessage: null,
      clearError: vi.fn(),
      applyProjectRoot: vi.fn(),
      chooseProjectRoot: vi.fn(),
      clearProjectRoot: vi.fn()
    } satisfies WorkspaceFixture;
  });

  afterEach(() => {
    delete (globalThis as { window?: unknown }).window;
  });

  it('renders no runtime chip when there is no desktop bridge', async () => {
    const tree = await renderShell();
    expect(findRuntimeChip(tree)).toBeNull();
    expect(findRuntimeDot(tree)).toBeNull();
  });

  it('renders no runtime chip when the bridge reports no snapshot yet', async () => {
    installBridge(null);
    const tree = await renderShell();
    expect(findRuntimeChip(tree)).toBeNull();
  });

  it('shows a connected runtime with the healthy tone', async () => {
    installBridge(snapshot());
    const tree = await renderShell();

    const chip = findRuntimeChip(tree);
    expect(chip?.props.className).toBe('shell-runtime-chip shell-runtime-chip--ready');
    expect(chip?.props.title).toBe('Runtime daemon connected. Check connection now.');
    expect(chip?.type).toBe('button');
    expect(chip?.props.type).toBe('button');
    expect(chip?.props['aria-label']).toBe(
      'Check runtime connection; reported status: connected'
    );
    expect(findRuntimeDot(tree)?.props.className).toBe(
      'shell-runtime-dot shell-runtime-dot--ready'
    );
    expect(textOf(chip as renderer.ReactTestInstance)).toBe('connected');
  });

  it('shows an offline runtime with the failure reason in the title', async () => {
    installBridge(
      snapshot({ state: 'disconnected', failedAttempts: 2, lastError: 'socket refused' })
    );
    const tree = await renderShell();

    const chip = findRuntimeChip(tree);
    expect(chip?.props.className).toBe('shell-runtime-chip shell-runtime-chip--error');
    expect(chip?.props.title).toBe(
      'Runtime daemon unreachable after 2 attempts: socket refused. Check connection now.'
    );
    expect(findRuntimeDot(tree)?.props.className).toBe(
      'shell-runtime-dot shell-runtime-dot--error'
    );
  });

  it('transitions the indicator when the main process pushes a new state', async () => {
    const bridge = installBridge(snapshot({ state: 'disconnected', failedAttempts: 1 }));
    const tree = await renderShell();
    expect(findRuntimeChip(tree)?.props.className).toBe(
      'shell-runtime-chip shell-runtime-chip--error'
    );

    // This is the behaviour the previous single-shot binding could not deliver: a
    // daemon that comes back updates the bar with no renderer-initiated call.
    await act(async () => {
      bridge.push(snapshot({ state: 'connected', changedAt: '2026-07-25T12:00:05.000Z' }));
    });

    expect(findRuntimeChip(tree)?.props.className).toBe(
      'shell-runtime-chip shell-runtime-chip--ready'
    );
    expect(findRuntimeChip(tree)?.props.title).toBe(
      'Runtime daemon connected. Check connection now.'
    );
  });

  it('shows the pending tone while the first bind is still in flight', async () => {
    installBridge(snapshot({ state: 'connecting' }));
    const tree = await renderShell();
    expect(findRuntimeChip(tree)?.props.className).toBe(
      'shell-runtime-chip shell-runtime-chip--pending'
    );
    expect(textOf(findRuntimeChip(tree) as renderer.ReactTestInstance)).toBe(
      'connecting'
    );
  });

  it('unsubscribes from the bridge on unmount', async () => {
    const bridge = installBridge(snapshot());
    const tree = await renderShell();
    expect(bridge.listenerCount()).toBe(1);

    await act(async () => {
      tree.unmount();
    });

    expect(bridge.unsubscribeCalls()).toBe(1);
    expect(bridge.listenerCount()).toBe(0);
  });

  it('reads the shared provider snapshot instead of subscribing again', async () => {
    // The reconnect epoch and the top-bar chip must come from one subscription:
    // two independent listeners could report different states for the same
    // daemon, which is precisely the split the operator saw.
    const bridge = installBridge(snapshot({ state: 'disconnected', failedAttempts: 1 }));
    Object.assign(globalThis, { React });
    const { ShellFrame } = await import('../../components/shell/shell-frame');
    const { RuntimeConnectivityProvider } = await import(
      '../../components/shell/runtime-connectivity-provider'
    );

    let tree!: ReactTestRenderer;
    await act(async () => {
      tree = renderer.create(
        <RuntimeConnectivityProvider>
          <ShellFrame section="PORTAL" title="Portal" subtitle="Workspace">
            <div>content</div>
          </ShellFrame>
        </RuntimeConnectivityProvider>
      );
    });

    expect(bridge.listenerCount()).toBe(1);
    expect(findRuntimeChip(tree)?.props.className).toBe(
      'shell-runtime-chip shell-runtime-chip--error'
    );

    await act(async () => {
      bridge.push(snapshot({ state: 'connected', changedAt: '2026-07-25T12:00:05.000Z' }));
    });

    expect(findRuntimeChip(tree)?.props.className).toBe(
      'shell-runtime-chip shell-runtime-chip--ready'
    );
  });

  it('leaves the working-root chip and its dot untouched', async () => {
    installBridge(snapshot({ state: 'disconnected', lastError: 'gone' }));
    const tree = await renderShell();

    // The two indicators are independent axes; a dead runtime must not restyle a
    // perfectly valid working root, and the root dot must stay singly addressable.
    const rootDots = tree.root.findAll((node) =>
      String(node.props.className ?? '').startsWith('shell-root-dot')
    );
    expect(rootDots).toHaveLength(1);
    expect(rootDots[0]?.props.className).toBe('shell-root-dot shell-root-dot--ready');
  });

  it('checks the connectivity bridge once more when activated', async () => {
    const bridge = installBridge(snapshot({ state: 'disconnected', failedAttempts: 1 }));
    const tree = await renderShell();
    const beforeClick = bridge.status.mock.calls.length;

    await act(async () => {
      findRuntimeChip(tree)?.props.onClick();
    });

    expect(bridge.status).toHaveBeenCalledTimes(beforeClick + 1);
    expect(findRuntimeChip(tree)?.props.className).toBe(
      'shell-runtime-chip shell-runtime-chip--error'
    );
    expect(findRuntimeChip(tree)?.props['aria-busy']).toBe(false);
  });

  it('keeps the main-process snapshot as visual truth when a check fails', async () => {
    const connected = snapshot({ state: 'connected' });
    const status = vi.fn()
      .mockResolvedValueOnce(connected)
      .mockRejectedValue(new Error('socket refused'));
    installBridge(connected, status);
    const tree = await renderShell();

    await act(async () => {
      findRuntimeChip(tree)?.props.onClick();
    });

    const chip = findRuntimeChip(tree);
    expect(chip?.props.className).toBe('shell-runtime-chip shell-runtime-chip--ready');
    expect(textOf(chip as renderer.ReactTestInstance)).toBe('connected');
    expect(chip?.props.title).toBe(
      'Runtime daemon connected. Last check failed: Unable to contact the Chirality runtime'
    );
    expect(chip?.props['data-runtime-check-error']).toBe(true);
    const feedback = tree.root.findByProps({ role: 'status' });
    expect(textOf(feedback)).toBe('Runtime connection check failed: Unable to contact the Chirality runtime');
  });

  it('reports a stopped Runtime service without changing snapshot truth', async () => {
    const connected = snapshot({ state: 'connected' });
    const status = vi.fn()
      .mockResolvedValueOnce(connected)
      .mockResolvedValue(snapshot({ state: 'disconnected', failedAttempts: 2, lastError: 'socket refused' }));
    installBridge(connected, status);
    const tree = await renderShell();

    await act(async () => {
      findRuntimeChip(tree)?.props.onClick();
    });

    const chip = findRuntimeChip(tree);
    expect(chip?.props.className).toBe('shell-runtime-chip shell-runtime-chip--ready');
    expect(textOf(chip as renderer.ReactTestInstance)).toBe('connected');
    expect(chip?.props.title).toBe(
      'Runtime daemon connected. Last check failed: Runtime service is unreachable: socket refused'
    );
    expect(chip?.props['data-runtime-check-error']).toBe(true);
    const feedback = tree.root.findByProps({ role: 'status' });
    expect(textOf(feedback)).toBe(
      'Runtime connection check failed: Runtime service is unreachable: socket refused'
    );
  });

  it('bounds reentrancy while a status check is in flight', async () => {
    const offline = snapshot({ state: 'disconnected' });
    let resolveStatus!: (value: RuntimeConnectivitySnapshot) => void;
    const status = vi.fn()
      .mockResolvedValueOnce(offline)
      .mockImplementation(
        () => new Promise<RuntimeConnectivitySnapshot>((resolve) => {
          resolveStatus = resolve;
        })
      );
    installBridge(offline, status);
    const tree = await renderShell();
    const chip = findRuntimeChip(tree) as renderer.ReactTestInstance;

    await act(async () => {
      chip.props.onClick();
      chip.props.onClick();
    });

    expect(status).toHaveBeenCalledTimes(2);
    expect(findRuntimeChip(tree)?.props.disabled).toBe(true);
    expect(findRuntimeChip(tree)?.props['aria-busy']).toBe(true);
    expect(findRuntimeChip(tree)?.props['aria-label']).toBe(
      'Checking runtime connection; reported status: offline'
    );

    await act(async () => {
      resolveStatus(snapshot());
    });

    expect(findRuntimeChip(tree)?.props.disabled).toBe(false);
    expect(findRuntimeChip(tree)?.props['aria-busy']).toBe(false);
  });
});
