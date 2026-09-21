import { createElement } from 'react';
import { act, create, type ReactTestInstance, type ReactTestRenderer } from 'react-test-renderer';
import { describe, expect, it } from 'vitest';
import {
  ApiKeySettingsView,
  type ApiKeySettingsViewProps,
  type ApiKeyStatus
} from '../../components/settings/api-key-settings';
import { CREDENTIAL_STORAGE_STATES } from '../../lib/credential-storage-state';

/**
 * D-APP-36 render evidence for the typed safeStorage states in the API key
 * settings panel (DEL-02-05-V3-01, REQ-002; AT-057 storage-state portion).
 *
 * The four states — `missing`, `storageUnavailable`, `decryptFailed`,
 * `available` — must render distinctly, each with remediation copy where the
 * operator can act, and the rendered tree must never carry key material. These
 * assertions are structural and copy-bearing where the copy is the remediation
 * itself; they deliberately do not assert colours or geometry.
 */

const SECRET_FIXTURE = 'sk-ant-test-super-secret-material';

const baseProps: ApiKeySettingsViewProps = {
  keyInput: '',
  revealed: false,
  status: null,
  error: null,
  saving: false,
  bridgeAvailable: true,
  onKeyInputChange: () => undefined,
  onRevealToggle: () => undefined,
  onSave: () => undefined,
  onRemove: () => undefined
};

function render(overrides: Partial<ApiKeySettingsViewProps>): ReactTestRenderer {
  let renderer!: ReactTestRenderer;
  act(() => {
    renderer = create(createElement(ApiKeySettingsView, { ...baseProps, ...overrides }));
  });
  return renderer;
}

function textOf(instance: ReactTestInstance): string {
  const parts: string[] = [];
  const walk = (node: ReactTestInstance | string): void => {
    if (typeof node === 'string') {
      parts.push(node);
      return;
    }
    for (const child of node.children) {
      walk(child);
    }
  };
  walk(instance);
  return parts.join('');
}

function statusNode(renderer: ReactTestRenderer): ReactTestInstance {
  return renderer.root.find(
    (node) => node.type === 'p' && node.props.className === 'api-key-status'
  );
}

function warningNodes(renderer: ReactTestRenderer): ReactTestInstance[] {
  return renderer.root.findAll(
    (node) => node.type === 'p' && node.props.className === 'api-key-warning'
  );
}

function buttonLabels(renderer: ReactTestRenderer): string[] {
  return renderer.root.findAllByType('button').map((button) => textOf(button));
}

function assertNoSecret(renderer: ReactTestRenderer): void {
  expect(JSON.stringify(renderer.toJSON())).not.toContain(SECRET_FIXTURE);
}

const statuses: Record<(typeof CREDENTIAL_STORAGE_STATES)[number], ApiKeyStatus> = {
  missing: { hasKey: false, encryptionAvailable: true, source: 'none', storage: 'missing' },
  storageUnavailable: {
    hasKey: false,
    encryptionAvailable: false,
    source: 'none',
    storage: 'storageUnavailable'
  },
  decryptFailed: { hasKey: false, encryptionAvailable: true, source: 'none', storage: 'decryptFailed' },
  available: { hasKey: true, encryptionAvailable: true, source: 'ui', storage: 'available' }
};

describe('ApiKeySettingsView typed storage states (D-APP-36 render bar)', () => {
  it('renders each of the four states with a distinct data-storage marker', () => {
    const markers = new Set<string>();
    for (const state of CREDENTIAL_STORAGE_STATES) {
      const renderer = render({ status: statuses[state] });
      const marker = statusNode(renderer).props['data-storage'] as string;
      expect(marker).toBe(state);
      markers.add(marker);
      assertNoSecret(renderer);
      renderer.unmount();
    }
    expect(markers.size).toBe(4);
  });

  it('missing: offers entry with no warning and no removal', () => {
    const renderer = render({ status: statuses.missing });

    expect(textOf(statusNode(renderer))).toBe('No API key configured');
    expect(warningNodes(renderer)).toHaveLength(0);
    expect(buttonLabels(renderer)).toEqual(['Reveal', 'Save Key']);
    expect(renderer.root.findAllByType('input')).toHaveLength(1);
    assertNoSecret(renderer);
  });

  it('storageUnavailable: explains what the operator can do and hides entry', () => {
    const renderer = render({ status: statuses.storageUnavailable });

    expect(textOf(statusNode(renderer))).toBe('Secure storage is unavailable');
    const warnings = warningNodes(renderer);
    expect(warnings).toHaveLength(1);
    expect(warnings[0].props['data-storage-state']).toBe('storageUnavailable');
    const copy = textOf(warnings[0]);
    expect(copy).toContain('Secure storage is not available on this platform.');
    expect(copy).toContain('cannot read or save a stored key');
    expect(copy).toContain('left in place unread');
    expect(copy).toContain('ANTHROPIC_API_KEY');
    expect(copy).toContain('restart Chirality');
    expect(renderer.root.findAllByType('input')).toHaveLength(0);
    expect(buttonLabels(renderer)).toEqual([]);
    assertNoSecret(renderer);
  });

  it('storageUnavailable: names the provider-specific environment variable', () => {
    const renderer = render({
      status: statuses.storageUnavailable,
      title: 'oMLX API Key',
      environmentVariable: 'CHIRALITY_OMLX_API_KEY'
    });

    expect(textOf(warningNodes(renderer)[0])).toContain('CHIRALITY_OMLX_API_KEY');
    expect(textOf(warningNodes(renderer)[0])).not.toContain('ANTHROPIC_API_KEY');
  });

  it('decryptFailed: asks for re-entry, states the ciphertext was retained, and offers explicit removal', () => {
    const renderer = render({ status: statuses.decryptFailed });

    expect(textOf(statusNode(renderer))).toBe('Stored key cannot be read');
    const warnings = warningNodes(renderer);
    expect(warnings).toHaveLength(1);
    expect(warnings[0].props['data-storage-state']).toBe('decryptFailed');
    const copy = textOf(warnings[0]);
    expect(copy).toContain('could not be decrypted');
    expect(copy).toContain('cannot be used');
    expect(copy).toContain('kept unchanged');
    expect(copy).toContain('nothing was deleted');
    expect(copy).toContain('Re-enter the key');
    expect(copy).toContain('remove the stored entry explicitly');
    expect(copy).not.toContain('environment variable');
    expect(renderer.root.findAllByType('input')).toHaveLength(1);
    expect(buttonLabels(renderer)).toEqual(['Reveal', 'Save Key', 'Remove Stored Key']);
    assertNoSecret(renderer);
  });

  it('decryptFailed with an environment credential in use: says so alongside the remediation', () => {
    const renderer = render({
      status: { hasKey: true, encryptionAvailable: true, source: 'env', storage: 'decryptFailed' }
    });

    expect(textOf(statusNode(renderer))).toBe('Key configured (from environment variable)');
    expect(statusNode(renderer).props['data-source']).toBe('env');
    expect(statusNode(renderer).props['data-storage']).toBe('decryptFailed');
    const copy = textOf(warningNodes(renderer)[0]);
    expect(copy).toContain('kept unchanged');
    expect(copy).toContain('using the ANTHROPIC_API_KEY environment variable');
    expect(buttonLabels(renderer)).toContain('Remove Stored Key');
    assertNoSecret(renderer);
  });

  it('available: reports secure storage, offers removal, and shows no warning', () => {
    const renderer = render({ status: statuses.available });

    expect(textOf(statusNode(renderer))).toBe('Key configured (stored in secure storage)');
    expect(statusNode(renderer).props['data-source']).toBe('ui');
    expect(warningNodes(renderer)).toHaveLength(0);
    expect(buttonLabels(renderer)).toEqual(['Reveal', 'Save Key', 'Remove Stored Key']);
    assertNoSecret(renderer);
  });

  it('keeps entered key material out of the rendered tree except the masked input value', () => {
    const renderer = render({ status: statuses.decryptFailed, keyInput: SECRET_FIXTURE });

    const input = renderer.root.findByType('input');
    expect(input.props.type).toBe('password');
    expect(input.props.value).toBe(SECRET_FIXTURE);
    const json = JSON.stringify(renderer.toJSON());
    // The only place the fixture may appear is the controlled input's value.
    expect(json.split(SECRET_FIXTURE)).toHaveLength(2);
    expect(json).toContain(`"value":"${SECRET_FIXTURE}"`);
  });

  it('maps a legacy status without a typed state conservatively', () => {
    // Only an older bridge that reports neither a typed state nor a non-answer,
    // and says encryption is unavailable, is read as storageUnavailable.
    const legacyUnavailable = render({
      status: { hasKey: false, encryptionAvailable: false, source: 'none' }
    });
    expect(statusNode(legacyUnavailable).props['data-storage']).toBe('storageUnavailable');
    expect(statusNode(legacyUnavailable).props['data-answer']).toBe('status');
    expect(warningNodes(legacyUnavailable)).toHaveLength(1);

    const legacyKnown = render({ status: { hasKey: true, encryptionAvailable: true, source: 'ui' } });
    expect(statusNode(legacyKnown).props['data-storage']).toBe('unknown');
    expect(textOf(statusNode(legacyKnown))).toBe('Key configured (stored in secure storage)');
    expect(warningNodes(legacyKnown)).toHaveLength(0);

    const pending = render({ status: null });
    expect(statusNode(pending).props['data-storage']).toBe('unknown');
    expect(textOf(statusNode(pending))).toBe('Checking...');
    expect(buttonLabels(pending)).toEqual(['Reveal', 'Save Key']);
  });

  it('unreachable daemon: says nothing is known, never blames the keychain, keeps entry hidden as before', () => {
    const renderer = render({
      status: {
        hasKey: false,
        encryptionAvailable: false,
        source: 'none',
        unavailable: true,
        error: "ENOENT: no such file or directory, open '/runtime/auth/tokens/operator.token'"
      }
    });

    const node = statusNode(renderer);
    expect(node.props['data-storage']).toBe('unknown');
    expect(node.props['data-answer']).toBe('unavailable');
    expect(textOf(node)).toBe('Cannot determine credential status right now');
    expect(warningNodes(renderer)).toHaveLength(0);
    const json = JSON.stringify(renderer.toJSON());
    expect(json).not.toContain('Secure storage is not available');
    expect(json).not.toContain('keychain');
    const errorNode = renderer.root.find(
      (candidate) => candidate.type === 'p' && candidate.props['data-status-error'] === 'true'
    );
    expect(textOf(errorNode)).toContain('operator.token');
    expect(renderer.root.findAllByType('input')).toHaveLength(0);
    expect(buttonLabels(renderer)).toEqual([]);
    assertNoSecret(renderer);
  });

  it('denied or invalid bridge answers render the same neutral line', () => {
    for (const error of ['Credential request was denied', 'Runtime daemon returned an invalid credential status']) {
      const renderer = render({
        status: { hasKey: false, encryptionAvailable: false, source: 'none', error }
      });
      expect(statusNode(renderer).props['data-storage']).toBe('unknown');
      expect(statusNode(renderer).props['data-answer']).toBe('unavailable');
      expect(textOf(statusNode(renderer))).toBe('Cannot determine credential status right now');
      expect(warningNodes(renderer)).toHaveLength(0);
      expect(JSON.stringify(renderer.toJSON())).toContain(error);
      renderer.unmount();
    }
  });

  it('a typed state wins over a stray error field', () => {
    const renderer = render({
      status: { hasKey: true, encryptionAvailable: true, source: 'ui', storage: 'available', error: 'stale' }
    });
    expect(statusNode(renderer).props['data-storage']).toBe('available');
    expect(statusNode(renderer).props['data-answer']).toBe('status');
    expect(textOf(statusNode(renderer))).toBe('Key configured (stored in secure storage)');
  });
});
