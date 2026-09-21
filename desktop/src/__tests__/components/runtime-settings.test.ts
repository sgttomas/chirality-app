import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, it } from 'vitest';
import {
  RuntimeSettings,
  RuntimeSettingsView,
  type RuntimeSettingsViewProps
} from '../../components/settings/runtime-settings';
import { RuntimeStatusView } from '../../components/settings/runtime-status';

const baseProps: RuntimeSettingsViewProps = {
  bridgeAvailable: true,
  residency: {
    phase: 'READY',
    managedModelId: 'Qwen-local-exact',
    epoch: {
      epochId: 'epoch-1',
      modelId: 'Qwen-local-exact',
      activatedAt: '2026-07-22T00:00:00.000Z'
    },
    activeTurns: 0,
    acceptingLocalTurns: true,
    models: [
      { id: 'Qwen-local-exact', kind: 'llm', loaded: true, loading: false },
      { id: 'embedding-helper', kind: 'embedding', loaded: true, loading: false }
    ]
  },
  selectedModel: 'Qwen-local-exact',
  busyAction: null,
  error: null,
  onRefresh: () => undefined,
  onSelectedModelChange: () => undefined,
  onActivateModel: () => undefined
};

function renderView(overrides: Partial<RuntimeSettingsViewProps> = {}): string {
  return renderToStaticMarkup(
    createElement(RuntimeSettingsView, { ...baseProps, ...overrides })
  );
}

describe('RuntimeSettings rendering', () => {
  it('server-renders a Desktop-only fallback without invoking the bridge', () => {
    const html = renderToStaticMarkup(createElement(RuntimeSettings));

    expect(html).toContain('>Runtime</h3>');
    expect(html).toContain('available only in Chirality Desktop');
    expect(html).not.toContain('<details');
  });

  it('shows exact managed-model attribution and no service lifecycle controls', () => {
    const html = renderView();

    expect(html).toContain('Residency:');
    expect(html).toContain('Qwen-local-exact');
    expect(html).toContain('Activate Explicitly');
    expect(html).not.toContain('embedding-helper');
    for (const retired of ['Install', 'Uninstall', 'LaunchAgent', 'Start', 'Stop']) {
      expect(html).not.toMatch(new RegExp(`>${retired}<`));
    }
  });

  it('keeps the section without local-model controls for the hosted shell', () => {
    const html = renderToStaticMarkup(
      createElement(RuntimeSettingsView, { ...baseProps, showLocalModels: false })
    );

    expect(html).toContain('>Runtime</h3>');
    expect(html).toContain('managed by Chirality Desktop');
    expect(html).not.toContain('Residency:');
    expect(html).not.toContain('Activate Explicitly');
  });

  it('renders errors', () => {
    const html = renderView({ residency: null, error: 'Runtime failed closed' });
    expect(html).toContain('Runtime failed closed');
  });

  it('disables explicit activation for the already managed model', () => {
    const html = renderView();
    const activationButton = html.match(
      /<button[^>]*disabled=""[^>]*>Activate Explicitly<\/button>/
    );

    expect(activationButton).not.toBeNull();
    expect(html).toContain('Activation never occurs automatically');
  });
});

describe('RuntimeStatusView rendering (App-owned service)', () => {
  it('reports the connectivity snapshot without any install, start, stop or uninstall control', () => {
    const running = renderToStaticMarkup(createElement(RuntimeStatusView, { snapshot: { state: 'connected', failedAttempts: 0, lastError: null, changedAt: '2026-09-12T00:00:00.000Z' } }));
    expect(running).toMatch(/<span class="runtime-status" data-running="true"[^>]*>Running<\/span>/);
    expect(running).toContain('started and stopped by Chirality');
    expect(running).not.toContain('<button');

    const stopped = renderToStaticMarkup(createElement(RuntimeStatusView, { snapshot: { state: 'disconnected', failedAttempts: 6, lastError: 'socket refused', changedAt: '2026-09-12T00:00:00.000Z' } }));
    expect(stopped).toContain('data-running="false"');
    expect(stopped).toContain('Stopped');
    expect(stopped).toContain('socket refused');
    expect(stopped).toContain('quit and reopen the App');

    const web = renderToStaticMarkup(createElement(RuntimeStatusView, { snapshot: null }));
    expect(web).toContain('Unavailable outside Chirality Desktop');
  });
});
