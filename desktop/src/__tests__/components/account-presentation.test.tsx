import React from 'react';
import { act, create, type ReactTestRenderer } from 'react-test-renderer';
import { renderToStaticMarkup } from 'react-dom/server';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { WOVEN_WORKSPACE_STORAGE_KEY } from '../../lib/woven-dialogue/woven-workspace-state';
import { ThemeControl } from '../../components/shell/theme-control';
import { AccountRow } from '../../components/shell/account-row';
import { AccountPopover } from '../../components/shell/account-popover';
import { AppUpdateProvider } from '../../components/shell/app-update-provider';
import { createAppUpdateController, startAppUpdatePolling } from '../../../electron/app-update';
import { APP_UPDATE_RELEASE_ROOT, resolveAppUpdateSource } from '../../../electron/app-update-source';
import { SettingsView } from '../../components/settings/settings-view';
import { useAccountConsentController, type AccountConsentSettingsViewProps } from '../../components/settings/account-consent-settings';
import { useRuntimeSettingsController, type RuntimeSettingsViewProps } from '../../components/settings/runtime-settings-controller';
import { createFakeHostedEngineConsentPort } from '../../lib/consent/fake-hosted-engine-consent-port';
import { CONSENT_UX_FIXTURE_NAMES, consentUxFixture } from '../../lib/consent/consent-ux-fixtures';
import type { HostedEngineConsentPort } from '../../lib/consent/hosted-engine-consent-port';
import type { HostedBootstrapController } from '../../components/settings/hosted-bootstrap-controller';

vi.mock('../../components/settings/api-key-settings', () => ({ ApiKeySettings: () => <p>Existing API key controls</p> }));
vi.mock('../../components/shell/runtime-connectivity-provider', () => ({ useRuntimeEpoch: () => 0, useRuntimeConnectivitySnapshot: () => ({ state: 'connected', failedAttempts: 0, lastError: null, changedAt: '2026-09-12T00:00:00.000Z' }) }));
const noop = () => {};
const accountBase: AccountConsentSettingsViewProps = { snapshot: null, busy: false, error: null, onLogin: noop, onLogout: noop, onGrantConsent: noop, onRevokeConsent: noop, onSelectNetworkPosture: noop, onResolveNetworkPrompt: noop, onSelectRole: noop };
const runtimeBase: RuntimeSettingsViewProps = { bridgeAvailable: false, residency: null, selectedModel: '', busyAction: null, error: null, onRefresh: noop, onSelectedModelChange: noop, onActivateModel: noop };
const hostedBase: HostedBootstrapController = { projectRoot: '/folder', snapshot: { registration: 'required' }, account: null, project: { state: 'setup-required', message: null }, loading: false, busyAction: null, error: null, signOutUncertain: false, authUrl: null, onSetup: noop, onStartLogin: noop, onReopenLogin: noop, onCancelLogin: noop, onSignOut: noop, onRefresh: noop };
const text = (node: { children: unknown[] }): string => node.children.map(child => typeof child === 'string' ? child : child && typeof child === 'object' && 'children' in child ? text(child as {children: unknown[]}) : '').join('');
const trees: ReactTestRenderer[] = [];
afterEach(() => { act(() => trees.splice(0).forEach(tree => tree.unmount())); vi.unstubAllGlobals(); });
function createTree(element: React.ReactElement): ReactTestRenderer { let tree!: ReactTestRenderer; act(() => { tree = create(element); }); trees.push(tree); return tree; }
function Preview({ port, runtime = runtimeBase }: { port: HostedEngineConsentPort | null; runtime?: RuntimeSettingsViewProps }): JSX.Element {
  const account = useAccountConsentController(port);
  return <><AccountRow account={account} folder={account.snapshot?.canonicalRoot ?? null} onOpenSettings={noop} /><SettingsView account={account} runtime={runtime} folder={account.snapshot?.canonicalRoot ?? null} /></>;
}

describe('D122 account presentation', () => {
  it('shows update availability in the closed account row after an automatic check', async () => {
    vi.useFakeTimers();
    let stop: (() => void) | undefined;
    try {
      let latest = '3.0.0';
      const controller = createAppUpdateController({
        source: resolveAppUpdateSource(), appVersion: '3.0.0',
        platform: 'darwin', arch: 'arm64', openExternal: vi.fn(async () => undefined),
        fetchImpl: async () => ({ ok: true, status: 200, text: async () => JSON.stringify({
          tag_name: `v${latest}`, draft: false, prerelease: false,
          html_url: `${APP_UPDATE_RELEASE_ROOT}/tag/v${latest}`,
          published_at: '2026-09-13T00:00:00Z', assets: []
        }) })
      });
      vi.stubGlobal('window', { chirality: { appUpdate: {
        get: async () => controller.getState(), check: () => controller.check(),
        openDownload: () => controller.openDownload(), subscribe: controller.subscribe,
        onShowAbout: () => () => undefined
      } } });
      const tree = createTree(<AppUpdateProvider>
        <AccountRow account={accountBase} folder={null} onOpenSettings={noop} />
      </AppUpdateProvider>);
      await act(async () => {
        stop = startAppUpdatePolling(controller);
        await vi.advanceTimersByTimeAsync(0);
      });
      expect(text(tree.root)).not.toContain('Update available');
      latest = '3.0.1';
      await act(async () => { await vi.advanceTimersByTimeAsync(6 * 60 * 60 * 1000); });
      expect(text(tree.root)).toContain('Update available');
      expect(tree.root.findAllByProps({ 'aria-label': 'Account and settings, update available' })).toHaveLength(1);
      expect(tree.root.findAllByProps({ role: 'dialog' })).toHaveLength(0);
    } finally {
      stop?.();
      vi.clearAllTimers();
      vi.useRealTimers();
    }
  });

  it.each(CONSENT_UX_FIXTURE_NAMES)('renders %s from a real fake port with one local-model dot and unchanged folder semantics', name => {
    const port = createFakeHostedEngineConsentPort({ initial: consentUxFixture(name) });
    const tree = createTree(<Preview port={port} />);
    const groups = tree.root.findAll(node => Boolean(node.props['data-settings-group']));
    expect(groups.map(node => node.props['data-settings-group'])).toEqual(['account', 'folder', 'local-model', 'api-keys', 'appearance']);
    expect(tree.root.findAllByProps({ 'data-local-model-status': 'unknown' })).toHaveLength(1);
    const account = groups[0];
    expect(text(account)).not.toContain('for this root');
    expect(text(groups[1])).toContain('Consent');
    const dom = JSON.stringify(tree.toJSON());
    for (const forbidden of ['Bearer', 'sk-ant-', 'device_code', 'cookie', '@']) expect(dom).not.toContain(forbidden);
    expect(dom).not.toContain('data-openai-status');
    expect(dom).toContain('Opt-in Preview');
  });

  it('keeps unavailable distinct from signed out and omits the folder group without context', () => {
    const html = renderToStaticMarkup(<><AccountRow account={accountBase} folder={null} onOpenSettings={noop} /><SettingsView account={accountBase} runtime={runtimeBase} folder={null} /></>);
    expect(html).toContain('Account service unavailable'); expect(html).not.toContain('Not signed in');
    expect(html).not.toContain('data-settings-group="folder"');
  });

  it('reports the App-owned Runtime service in hosted Codex settings without lifecycle or local-model controls', () => {
    const runtime = { ...runtimeBase, bridgeAvailable: true };
    const html = renderToStaticMarkup(<SettingsView account={accountBase} runtime={runtime} hosted={hostedBase} folder="/folder" />);

    expect(html).toContain('data-settings-group="runtime"');
    expect(html).toContain('>Runtime</h3>');
    expect(html).toContain('Running');
    expect(html).toContain('started and stopped by Chirality');
    expect(html).not.toContain('Install');
    expect(html).not.toContain('Uninstall');
    expect(html).not.toContain('LaunchAgent');
    expect(html).not.toContain('Shared Runtime');
    expect(html).not.toContain('Local model');
    expect(html).not.toContain('Activate Explicitly');
    expect(html).not.toContain('Preview account');
    expect(html).not.toContain('apply to the selected project');
  });

  it('keeps the hosted popover to account, Settings, Appearance, Check for Updates, and About with runtime controls only in Settings', () => {
    const tree = createTree(<AccountPopover account={accountBase} hosted={hostedBase} folder="/folder" onOpenSettings={noop} />);
    expect(tree.root.findAllByType('section').map(node => node.props['aria-label']).filter(Boolean)).toEqual(['Account', 'App controls']);
    expect(tree.root.findAllByType('summary').map(text)).toEqual(['Appearance', 'About Chirality']);
    expect(tree.root.findAllByType('button').map(text)).toEqual(['Use this folder', 'Settings…', 'Light', 'Dark', 'System', 'Check for Updates…']);
    // Without the desktop bridge the update check is disabled and says so; it never claims availability.
    expect(tree.root.findAllByType('button').find(node => text(node) === 'Check for Updates…')!.props.disabled).toBe(true);
    expect(text(tree.root)).toContain('Update checks are available in Chirality Desktop.');
    expect(text(tree.root)).not.toContain('OpenAI');
    const body = text(tree.root);
    expect(body).not.toMatch(/Shared runtime|Set up runtime|runtime daemon|Local model|oMLX|Opt-in Preview/);
    expect(body).toMatch(/Chirality \d+\.\d+/);
  });

  it('uses explicit login/logout/consent actions and does not carry identity across fake roots', async () => {
    const first = createFakeHostedEngineConsentPort({ initial: consentUxFixture('loggedOutDefault') });
    const second = createFakeHostedEngineConsentPort({ initial: { ...consentUxFixture('loggedOutDefault'), canonicalRoot: '/second' } });
    const tree = createTree(<Preview port={first} />);
    expect(first.getSnapshot().account.status).toBe('loggedOut');
    await act(async () => tree.root.findAllByType('button').find(node => text(node) === 'Sign in')!.props.onClick());
    expect(first.getSnapshot().account.status).toBe('loggedIn');
    await act(async () => tree.root.findAllByType('button').find(node => text(node) === 'Grant consent for this root')!.props.onClick());
    expect(first.getSnapshot().consent.status).toBe('granted');
    await act(async () => tree.root.findAllByType('button').find(node => text(node) === 'Sign out')!.props.onClick());
    expect(first.getSnapshot().account.status).toBe('loggedOut');
    act(() => tree.update(<Preview port={second} />));
    expect(second.getSnapshot().account.status).toBe('loggedOut'); expect(text(tree.root)).not.toContain('Signed in as');
  });

  it('asks the hosted controller to re-read status each time the popover opens, never on close', () => {
    const onRefresh = vi.fn();
    const tree = createTree(<AccountRow account={accountBase} hosted={{ ...hostedBase, onRefresh }} folder="/folder" onOpenSettings={noop} />);
    const trigger = () => tree.root.findByProps({ 'aria-label': 'Account and settings', type: 'button' });
    act(() => trigger().props.onClick());
    expect(onRefresh).toHaveBeenCalledTimes(1);
    expect(tree.root.findAllByProps({ role: 'dialog' })).toHaveLength(1);
    act(() => trigger().props.onClick());
    expect(onRefresh).toHaveBeenCalledTimes(1);
    expect(tree.root.findAllByProps({ role: 'dialog' })).toHaveLength(0);
    act(() => trigger().props.onClick());
    expect(onRefresh).toHaveBeenCalledTimes(2);
  });

  it('keeps daemon start/stop out of the non-hosted popover; the popover takes no runtime controller', () => {
    const tree = createTree(<AccountPopover account={accountBase} folder={null} onOpenSettings={noop} />);
    expect(tree.root.findAllByProps({ role: 'switch' })).toHaveLength(0);
    expect(text(tree.root)).not.toMatch(/oMLX|Local model|runtime daemon/);
  });

  it('opens Settings from the popover and the folder shortcut selects the folder group', () => {
    const open = vi.fn();
    const tree = createTree(<AccountPopover account={accountBase} folder="/folder" onOpenSettings={open} />);
    expect(tree.root.findAllByType('button').some(node => text(node) === 'Set up runtime…')).toBe(false);
    act(() => tree.root.findAllByType('button').find(node => text(node) === 'Settings…')!.props.onClick());
    expect(open).toHaveBeenLastCalledWith();
    act(() => tree.root.findAllByType('button').find(node => text(node) === 'This folder…')!.props.onClick());
    expect(open).toHaveBeenLastCalledWith('folder');
  });

  it('shares one controller across the popover and Settings with no extra query when either presentation changes', async () => {
    const models = vi.fn(async () => ({ ok: true, residency: { phase: 'READY', models: [], activeTurns: 0, acceptingLocalTurns: true } }));
    vi.stubGlobal('window', { chirality: { runtime: { models: { status: models } } } });
    function Host({ settings }: { settings: boolean }): JSX.Element {
      const runtime = useRuntimeSettingsController();
      return <><AccountPopover account={accountBase} folder={null} onOpenSettings={noop} />{settings ? <SettingsView account={accountBase} runtime={runtime} folder={null} /> : null}</>;
    }
    let tree!: ReactTestRenderer;
    await act(async () => { tree = create(<Host settings={false} />); }); trees.push(tree);
    expect(models).toHaveBeenCalledTimes(1);
    await act(async () => tree.update(<Host settings />));
    expect(models).toHaveBeenCalledTimes(1);
    // Non-hosted Settings keeps its local-model group; the popover no longer repeats it.
    expect(text(tree.root)).toContain('oMLX server status unknown.');
    expect(text(tree.root.findByProps({ 'aria-label': 'App controls' }))).not.toContain('oMLX');
  });
});

it('keeps both theme controls synchronized when browser storage is unavailable', () => {
  const events = new EventTarget();
  const stamp = vi.fn();
  vi.stubGlobal('window', { addEventListener: events.addEventListener.bind(events), removeEventListener: events.removeEventListener.bind(events), dispatchEvent: events.dispatchEvent.bind(events) });
  vi.stubGlobal('document', { documentElement: { setAttribute: stamp } });
  const tree = createTree(<><ThemeControl /><ThemeControl /></>);
  act(() => tree.root.findAllByProps({ 'data-theme-option': 'dark' })[0].props.onClick());
  expect(tree.root.findAllByProps({ 'data-theme-option': 'dark' }).every(node => node.props['aria-pressed'])).toBe(true);
  expect(stamp).toHaveBeenLastCalledWith('data-theme', 'dark');
  act(() => tree.root.findAllByProps({ 'data-theme-option': 'system' })[1].props.onClick());
  expect(tree.root.findAllByProps({ 'data-theme-option': 'system' }).every(node => node.props['aria-pressed'])).toBe(true);
  expect(stamp).toHaveBeenLastCalledWith('data-theme', 'system');
});

it.each(['unavailable', 'failed-write'] as const)('retains theme through conditional mount and total remount with %s storage', storageMode => {
  const events = new EventTarget();
  const stamp = vi.fn();
  const storage = storageMode === 'failed-write' ? {
    getItem: () => JSON.stringify({ schemaVersion: 1, theme: 'light' }),
    setItem: () => { throw new Error('Storage write denied'); }
  } : undefined;
  vi.stubGlobal('window', { localStorage: storage, addEventListener: events.addEventListener.bind(events), removeEventListener: events.removeEventListener.bind(events), dispatchEvent: events.dispatchEvent.bind(events) });
  vi.stubGlobal('document', { documentElement: { setAttribute: stamp } });
  function Conditional({ popup }: { popup: boolean }): JSX.Element { return <><ThemeControl />{popup ? <ThemeControl /> : null}</>; }
  const tree = createTree(<Conditional popup={false} />);
  act(() => tree.root.findByProps({ 'data-theme-option': 'dark' }).props.onClick());
  stamp.mockClear();
  act(() => tree.update(<Conditional popup />));
  expect(tree.root.findAllByProps({ 'data-theme-option': 'dark' }).every(node => node.props['aria-pressed'])).toBe(true);
  expect(stamp).not.toHaveBeenCalledWith('data-theme', 'light');
  act(() => tree.update(<Conditional popup={false} />));
  act(() => tree.update(<Conditional popup />));
  expect(tree.root.findAllByProps({ 'data-theme-option': 'dark' }).every(node => node.props['aria-pressed'])).toBe(true);
  act(() => tree.update(<></>));
  act(() => tree.update(<ThemeControl />));
  expect(tree.root.findByProps({ 'data-theme-option': 'dark' }).props['aria-pressed']).toBe(true);
  expect(stamp).not.toHaveBeenCalledWith('data-theme', 'light');
});

it('observes an external theme write with zero mounted controls and retains it on remount', () => {
  const events = new EventTarget();
  const stamp = vi.fn();
  const values = new Map<string, string>();
  const storage = { getItem: (key: string) => values.get(key) ?? null, setItem: (key: string, value: string) => values.set(key, value) };
  vi.stubGlobal('window', { localStorage: storage, addEventListener: events.addEventListener.bind(events), removeEventListener: events.removeEventListener.bind(events), dispatchEvent: events.dispatchEvent.bind(events) });
  vi.stubGlobal('document', { documentElement: { setAttribute: stamp } });
  const tree = createTree(<ThemeControl />);
  act(() => tree.root.findByProps({ 'data-theme-option': 'dark' }).props.onClick());
  act(() => tree.update(<></>));
  const saved = JSON.parse(values.get(WOVEN_WORKSPACE_STORAGE_KEY)!);
  values.set(WOVEN_WORKSPACE_STORAGE_KEY, JSON.stringify({ ...saved, theme: 'system' }));
  const change = Object.assign(new Event('storage'), { key: WOVEN_WORKSPACE_STORAGE_KEY });
  act(() => { events.dispatchEvent(change); });
  expect(stamp).toHaveBeenLastCalledWith('data-theme', 'system');
  stamp.mockClear();
  act(() => tree.update(<ThemeControl />));
  expect(tree.root.findByProps({ 'data-theme-option': 'system' }).props['aria-pressed']).toBe(true);
  expect(stamp).not.toHaveBeenCalledWith('data-theme', 'dark');
  act(() => tree.update(<><ThemeControl /><ThemeControl /></>));
  values.set(WOVEN_WORKSPACE_STORAGE_KEY, JSON.stringify({ ...saved, theme: 'dark' }));
  act(() => { events.dispatchEvent(change); });
  expect(tree.root.findAllByProps({ 'data-theme-option': 'dark' }).every(node => node.props['aria-pressed'])).toBe(true);
  // One session subscription remains; unrelated storage does not overwrite it.
  values.set(WOVEN_WORKSPACE_STORAGE_KEY, JSON.stringify({ ...saved, theme: 'light' }));
  act(() => { events.dispatchEvent(Object.assign(new Event('storage'), { key: 'other-key' })); });
  expect(tree.root.findAllByProps({ 'data-theme-option': 'dark' }).every(node => node.props['aria-pressed'])).toBe(true);
});

describe('account menu lifecycle', () => {
  it('closes the open menu when a pending sign-in completes, and keeps it open when the sign-in fails', () => {
    const pending: HostedBootstrapController = { ...hostedBase, snapshot: { registration: 'registered', projectId: 'p', status: { schema: 'chirality-hosted-bootstrap-status/v1', projectId: 'p', ceremony: 'pending', admission: 'unavailable', canStartLogin: false } } };
    const tree = createTree(<AccountRow account={accountBase} hosted={pending} folder="/folder" onOpenSettings={noop} />);
    const trigger = () => tree.root.findByProps({ 'aria-label': 'Account and settings', type: 'button' });
    act(() => trigger().props.onClick());
    expect(tree.root.findAllByProps({ role: 'dialog' })).toHaveLength(1);
    expect(text(tree.root.findByProps({ role: 'dialog' }))).toContain('Waiting for sign-in');
    const failed: HostedBootstrapController = { ...pending, snapshot: { registration: 'registered', projectId: 'p', status: { schema: 'chirality-hosted-bootstrap-status/v1', projectId: 'p', ceremony: 'failed', admission: 'unavailable', canStartLogin: true } } };
    act(() => tree.update(<AccountRow account={accountBase} hosted={failed} folder="/folder" onOpenSettings={noop} />));
    expect(tree.root.findAllByProps({ role: 'dialog' })).toHaveLength(1);
    expect(text(tree.root.findByProps({ role: 'dialog' }))).toContain('Sign-in failed');
    act(() => tree.update(<AccountRow account={accountBase} hosted={pending} folder="/folder" onOpenSettings={noop} />));
    const signedIn: HostedBootstrapController = { ...pending, snapshot: { registration: 'registered', projectId: 'p', status: { schema: 'chirality-hosted-bootstrap-status/v1', projectId: 'p', ceremony: 'signed-in', admission: 'ready', canStartLogin: false } } };
    act(() => tree.update(<AccountRow account={accountBase} hosted={signedIn} folder="/folder" onOpenSettings={noop} />));
    expect(tree.root.findAllByProps({ role: 'dialog' })).toHaveLength(0);
    expect(text(trigger())).toContain('Signed in · Ready to work');
    expect(text(trigger())).toContain('Account');
    expect(trigger().findByType('svg').props['aria-hidden']).toBe('true');
    expect(text(trigger())).not.toContain('OpenAI');
  });

  it('separates authentication from runtime readiness in the popover and routes About to the host', () => {
    const establishing: HostedBootstrapController = { ...hostedBase, snapshot: { registration: 'registered', projectId: 'p', status: { schema: 'chirality-hosted-bootstrap-status/v1', projectId: 'p', ceremony: 'signed-in', admission: 'establishing', canStartLogin: false } } };
    const onOpenAbout = vi.fn();
    const tree = createTree(<AccountPopover account={accountBase} hosted={establishing} folder="/folder" onOpenSettings={noop} onOpenAbout={onOpenAbout} />);
    const states = tree.root.findAllByType('dd').map(node => [node.props['data-auth-state'] ?? node.props['data-readiness-state'], text(node)]);
    expect(states).toEqual([['signed-in', 'Signed in'], ['establishing', 'Preparing engine']]);
    expect(tree.root.findAllByType('summary').map(text)).toEqual(['Appearance']);
    act(() => tree.root.findAllByType('button').find(node => text(node) === 'About Chirality')!.props.onClick());
    expect(onOpenAbout).toHaveBeenCalledTimes(1);
  });
});
