import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { expect, it, vi } from 'vitest';

vi.mock('../../components/settings/api-key-settings', () => ({ ApiKeySettings: () => <p>API key controls</p> }));
vi.mock('../../components/settings/account-consent-settings', () => ({ AccountConsentSettingsView: () => <p>Compatibility account</p> }));
vi.mock('../../components/settings/hosted-bootstrap-view', () => ({ HostedBootstrapView: () => <p>Codex account</p> }));
vi.mock('../../components/settings/runtime-settings', () => ({ RuntimeSettingsView: () => <p>Local model controls</p> }));
vi.mock('../../components/settings/runtime-status', () => ({ RuntimeStatus: () => <p>Runtime service</p> }));
vi.mock('../../components/shell/theme-control', () => ({ ThemeControl: () => <p>Theme</p> }));
import { SettingsView } from '../../components/settings/settings-view';

it('shows the App-owned Runtime status and omits API-key and local-model panels for hosted Codex while retaining compatibility settings', () => {
  const props = { account: {} as any, runtime: {} as any, folder: '/project' };
  const hosted = renderToStaticMarkup(<SettingsView {...props} hosted={{} as any} />);
  expect(hosted).toContain('Codex account');
  expect(hosted).toContain('Runtime service');
  expect(hosted).not.toContain('API key');
  expect(hosted).not.toContain('Local model');
  const compatibility = renderToStaticMarkup(<SettingsView {...props} />);
  expect(compatibility).toContain('API key controls');
  expect(compatibility).toContain('Local model controls');
});
