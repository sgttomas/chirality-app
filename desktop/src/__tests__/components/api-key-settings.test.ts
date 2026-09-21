import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, it } from 'vitest';
import {
  ApiKeySettings,
  ApiKeySettingsView,
  type ApiKeySettingsViewProps
} from '../../components/settings/api-key-settings';

const SECRET_FIXTURE = 'sk-ant-test-super-secret-material';

const baseProps: ApiKeySettingsViewProps = {
  keyInput: '',
  revealed: false,
  status: { hasKey: false, encryptionAvailable: true, source: 'none' },
  error: null,
  saving: false,
  bridgeAvailable: true,
  onKeyInputChange: () => undefined,
  onRevealToggle: () => undefined,
  onSave: () => undefined,
  onRemove: () => undefined
};

function renderView(overrides: Partial<ApiKeySettingsViewProps> = {}): string {
  const html = renderToStaticMarkup(
    createElement(ApiKeySettingsView, { ...baseProps, ...overrides })
  );
  expect(html).not.toContain(SECRET_FIXTURE);
  return html;
}

describe('ApiKeySettings rendering', () => {
  it('server-renders the outside-Electron fallback without running effects', () => {
    const html = renderToStaticMarkup(createElement(ApiKeySettings));

    expect(html).toContain('data-source="unknown"');
    expect(html).toContain('Checking...');
    expect(html).toContain('Running outside Electron.');
    expect(html).toContain('ANTHROPIC_API_KEY');
    expect(html).toContain('CHIRALITY_OMLX_API_KEY');
    expect(html).toContain('Anthropic API Key');
    expect(html).toContain('oMLX API Key');
    expect(html).not.toContain('Save Key');
    expect(html).not.toContain(SECRET_FIXTURE);
  });

  it('renders UI-stored status and its remove control without key material', () => {
    const html = renderView({
      status: { hasKey: true, encryptionAvailable: true, source: 'ui' }
    });

    expect(html).toContain('data-source="ui"');
    expect(html).toContain('Key configured (stored in secure storage)');
    expect(html).toContain('Remove Stored Key');
    expect(html).toContain('type="password"');
  });

  it('renders environment status without offering removal of an environment key', () => {
    const html = renderView({
      status: { hasKey: true, encryptionAvailable: true, source: 'env' }
    });

    expect(html).toContain('data-source="env"');
    expect(html).toContain('Key configured (from environment variable)');
    expect(html).not.toContain('Remove Stored Key');
    expect(html).toContain('Save Key');
  });

  it('renders the no-key status as an explicit none source', () => {
    const html = renderView();

    expect(html).toContain('data-source="none"');
    expect(html).toContain('No API key configured');
  });

  it('warns when encryption is unavailable and hides storage controls', () => {
    const html = renderView({
      status: { hasKey: false, encryptionAvailable: false, source: 'none' }
    });

    expect(html).toContain('Secure storage is not available on this platform.');
    expect(html).toContain('ANTHROPIC_API_KEY');
    expect(html).not.toContain('Save Key');
    expect(html).not.toContain('Reveal');
  });

  it.each([
    { storage: 'missing', label: 'No API key configured', warning: false },
    { storage: 'storageUnavailable', label: 'Secure storage is unavailable', warning: true },
    { storage: 'decryptFailed', label: 'Stored key cannot be read', warning: true },
    { storage: 'available', label: 'Key configured (stored in secure storage)', warning: false }
  ] as const)('server-renders the $storage storage state distinctly', ({ storage, label, warning }) => {
    const html = renderView({
      status: {
        hasKey: storage === 'available',
        encryptionAvailable: storage !== 'storageUnavailable',
        source: storage === 'available' ? 'ui' : 'none',
        storage
      }
    });

    expect(html).toContain(`data-storage="${storage}"`);
    expect(html).toContain(label);
    expect(html.includes(`data-storage-state="${storage}"`)).toBe(warning);
  });

  it('server-renders an unreachable-daemon answer as unknown, without the keychain warning', () => {
    const html = renderView({
      status: {
        hasKey: false,
        encryptionAvailable: false,
        source: 'none',
        unavailable: true,
        error: 'connect ENOENT control.sock'
      }
    });

    expect(html).toContain('data-storage="unknown"');
    expect(html).toContain('data-answer="unavailable"');
    expect(html).toContain('Cannot determine credential status right now');
    expect(html).toContain('connect ENOENT control.sock');
    expect(html).not.toContain('Secure storage is not available');
    expect(html).not.toContain('data-storage-state=');
    expect(html).not.toContain('Save Key');
  });

  it('renders saving state with the save control disabled', () => {
    const html = renderView({ keyInput: 'pending-value', saving: true });

    expect(html).toContain('Saving...');
    expect(html).toContain('disabled=""');
  });

  it('renders provider-specific oMLX labels without credential material', () => {
    const html = renderView({
      title: 'oMLX API Key',
      environmentVariable: 'CHIRALITY_OMLX_API_KEY',
      placeholder: 'Enter the key configured in oMLX'
    });

    expect(html).toContain('oMLX API Key');
    expect(html).toContain('Enter the key configured in oMLX');
    expect(html).not.toContain(SECRET_FIXTURE);
  });

  it('disables save for blank input and renders actionable error text', () => {
    const html = renderView({ error: 'Please enter an API key' });

    expect(html).toContain('Save Key');
    expect(html).toContain('disabled=""');
    expect(html).toContain('class="api-key-error"');
    expect(html).toContain('Please enter an API key');
  });
});
