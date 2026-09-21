import React from 'react';
import renderer, { act, type ReactTestRenderer } from 'react-test-renderer';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { AppUpdateProvider, type AppUpdateState } from '../../components/shell/app-update-provider';
import { AppUpdateControls, appUpdateStatusText } from '../../components/shell/app-update-summary';
import { AboutPanel } from '../../components/shell/about-panel';
import { publishLiveTurnPhase, resetLiveTurnPhaseForTests } from '../../lib/shell/live-work-store';

/**
 * Item 17 of the refinement brief: the update path downloads an installer for
 * manual installation. The controls must say so, must never read as if the
 * application updated itself, and must account for work still running.
 */
function state(overrides: Partial<AppUpdateState> = {}): AppUpdateState {
  return { currentVersion: '3.0.0-rc.1', status: 'idle', releaseSource: { configured: true, description: 'Owner release feed' }, ...overrides };
}
const available = state({ status: 'update-available', checkedAt: '2026-09-12T10:00:00.000Z', available: { version: '3.1.0', downloadUrl: 'https://example.invalid/Chirality-3.1.0.dmg' } });

function installBridge(initial: AppUpdateState): { openDownload: ReturnType<typeof vi.fn> } {
  const openDownload = vi.fn(async () => ({ ok: true }));
  Object.assign(globalThis, { window: { chirality: { appUpdate: {
    get: vi.fn(async () => initial), check: vi.fn(async () => initial), openDownload,
    subscribe: () => () => undefined, onShowAbout: () => () => undefined
  } } } });
  return { openDownload };
}
const text = (tree: ReactTestRenderer): string => JSON.stringify(tree.toJSON());
async function mount(element: React.ReactElement): Promise<ReactTestRenderer> {
  let tree: ReactTestRenderer | undefined;
  await act(async () => { tree = renderer.create(element); });
  await act(async () => { await Promise.resolve(); });
  return tree!;
}
afterEach(() => { delete (globalThis as { window?: unknown }).window; resetLiveTurnPhaseForTests(); });

describe('update wording', () => {
  it('reports availability as something to download, never as an applied update', () => {
    expect(appUpdateStatusText(available, true)).toBe('Version 3.1.0 is available to download.');
    for (const status of ['idle', 'checking', 'up-to-date', 'update-available', 'failed'] as const) {
      expect(appUpdateStatusText(state({ status }), true)).not.toMatch(/updated|installed|installing|restart/i);
    }
  });

  it('explains the manual install path and preservation next to the download, and warns while work is live', async () => {
    const bridge = installBridge(available);
    const tree = await mount(<AppUpdateProvider><AppUpdateControls /></AppUpdateProvider>);
    const download = tree.root.findAllByType('button').find(node => node.children.join('') === 'Download 3.1.0')!;
    expect(download.props.title).toContain('Chirality does not install updates');
    expect(download.props.title).toContain('quit Chirality, install the downloaded build, then reopen it');
    expect(tree.root.findByProps({ 'data-update-note': 'path' }).children.join('')).toContain('are stored outside the application and are kept');
    expect(tree.root.findAllByProps({ 'data-update-note': 'running-work' })).toHaveLength(0);
    expect(tree.root.findByProps({ className: 'app-update-controls' }).props['data-live-work']).toBe('false');

    act(() => publishLiveTurnPhase('working'));
    expect(tree.root.findByProps({ 'data-update-note': 'running-work' }).children.join('')).toContain('Quitting Chirality to install stops it');
    expect(tree.root.findByProps({ className: 'app-update-controls' }).props['data-live-work']).toBe('true');
    act(() => publishLiveTurnPhase('idle'));
    expect(tree.root.findAllByProps({ 'data-update-note': 'running-work' })).toHaveLength(0);

    await act(async () => { download.props.onClick(); });
    expect(bridge.openDownload).toHaveBeenCalledTimes(1);
    // Opening the download changes nothing about the reported state: the
    // application has not updated.
    expect(text(tree)).toContain('Version 3.1.0 is available to download.');
    expect(text(tree)).not.toMatch(/has been updated|updated to/i);
  });

  it('keeps the compact menu to the status and download, with the path explanation in the About panel', async () => {
    installBridge(available);
    const compact = await mount(<AppUpdateProvider><AppUpdateControls compact /></AppUpdateProvider>);
    expect(compact.root.findAllByProps({ 'data-update-note': 'path' })).toHaveLength(0);
    const about = await mount(<AppUpdateProvider><AboutPanel open onClose={() => {}} /></AppUpdateProvider>);
    expect(about.root.findAllByProps({ 'data-update-note': 'path' })).toHaveLength(1);
  });

  it('describes the path in About even when nothing is available yet', async () => {
    installBridge(state({ releaseSource: { configured: false, description: 'No release source is configured for this build.' } }));
    const about = await mount(<AppUpdateProvider><AboutPanel open onClose={() => {}} /></AppUpdateProvider>);
    const note = about.root.findByProps({ 'data-update-note': 'path' }).children.join('');
    expect(note).toContain('Chirality does not install updates');
    expect(text(about)).toContain('This build has no release source to check against.');
  });
});
