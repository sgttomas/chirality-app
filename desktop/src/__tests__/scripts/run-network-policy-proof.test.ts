import { describe, expect, it } from 'vitest';
import {
  descendantProcessIds,
  parseLsofTcp,
  scrubProviderCredentialEnv,
  summarizeCaptureIntegrity
} from '../../../scripts/run-network-policy-proof.mjs';

describe('run-network-policy-proof script', () => {
  it('enumerates Electron renderer and network-service descendants', () => {
    expect(
      descendantProcessIds(
        [
          { pid: 10, ppid: 1, command: 'Electron' },
          { pid: 11, ppid: 10, command: 'Electron Helper (Renderer)' },
          { pid: 12, ppid: 11, command: 'Electron Helper (Network)' },
          { pid: 99, ppid: 1, command: 'unrelated' }
        ],
        [10]
      )
    ).toEqual([10, 11, 12]);
  });

  it('credits renderer egress only when a usable capture observes descendant traffic', () => {
    const parsed = parseLsofTcp(
      'Electron 12 user 20u IPv4 TCP 127.0.0.1:5000->api.anthropic.com:443 (ESTABLISHED)'
    );
    const summary = summarizeCaptureIntegrity([
      {
        processLabel: 'electron',
        rootPid: 10,
        pids: [10, 11, 12],
        usable: true,
        parsed
      }
    ]);

    expect(summary.pass).toBe(true);
    expect(summary.electronDescendantPids).toEqual([11, 12]);
    expect(summary.electronDescendantTcp).toEqual([
      expect.objectContaining({ processId: 12, host: 'api.anthropic.com' })
    ]);

    expect(
      summarizeCaptureIntegrity([
        {
          processLabel: 'electron',
          rootPid: 10,
          pids: [10, 11, 12],
          usable: false,
          parsed: { rawLineCount: 0, remoteEndpoints: [] }
        }
      ]).pass
    ).toBe(false);
  });

  it('scrubs every inherited project provider credential variable', () => {
    const clean = scrubProviderCredentialEnv({
      PATH: '/fixture/bin',
      ANTHROPIC_API_KEY: 'owner-secret',
      CHIRALITY_ANTHROPIC_API_KEY: 'owner-alias-secret',
      CHIRALITY_OMLX_API_KEY: 'owner-omlx-secret'
    });

    expect(clean).toEqual({ PATH: '/fixture/bin' });
  });
});
