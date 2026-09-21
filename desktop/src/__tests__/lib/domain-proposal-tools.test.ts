import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
  domainProposalValidateTool,
  domainProposeOperationTool,
  type DomainProposalToolOverrides,
  type PecProposalTransportClient
} from '../../lib/harness/mcp/domain-proposal-tools';
import { PecBridgeError } from '../../lib/harness/mcp/pec-bridge-client';
import { replayHarnessEvents } from '../../lib/harness/session-events';

const SENTINEL_EMAIL = 'sentinel-agent-email@rehearsal.test';
const SENTINEL_PASSWORD = 'sentinel-agent-password-3f9c';
const SENTINEL_COOKIE_TOKEN = 'sentinel-cookie-token-a1b2c3d4';

const ENGINE_PROPOSAL = {
  id: 7,
  ref: 'IPR-0007',
  contract: 'mdl',
  state: 'ready_for_review',
  version: 2,
  sourceSha256: 'abc123',
  dryRunAt: '2026-07-06T00:00:00.000Z',
  basisHistoryId: 41,
  dryRunReport: { accepted: 3, updated: 1, conflicts: [], rejected: [], intakeCreated: 0 }
};

type FakeClient = PecProposalTransportClient & {
  login: ReturnType<typeof vi.fn>;
  createProposal: ReturnType<typeof vi.fn>;
  refreshProposal: ReturnType<typeof vi.fn>;
  getProposal: ReturnType<typeof vi.fn>;
  dispose: ReturnType<typeof vi.fn>;
};

function makeFakeClient(): FakeClient {
  return {
    login: vi.fn(async () => undefined),
    createProposal: vi.fn(async () => ENGINE_PROPOSAL),
    refreshProposal: vi.fn(async () => ({ ...ENGINE_PROPOSAL, version: 3 })),
    getProposal: vi.fn(async () => ENGINE_PROPOSAL),
    endpointDescriptor: () => ({ host: '127.0.0.1', port: 4899 }),
    dispose: vi.fn<() => void>()
  };
}

function overridesFor(client: FakeClient): DomainProposalToolOverrides & {
  createClient: ReturnType<typeof vi.fn>;
} {
  const createClient = vi.fn(() => client);
  return { createClient };
}

function parseResult(result: { content: Array<{ type: string; text?: string }> }): any {
  const first = result.content[0];
  if (!first || first.type !== 'text' || typeof first.text !== 'string') {
    throw new Error('Expected text MCP result');
  }
  return JSON.parse(first.text);
}

let tmpRoot = '';
let projectRoot = '';
let sessionCounter = 0;
let sessionId = '';

beforeEach(async () => {
  tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-pec-proposal-'));
  projectRoot = path.join(tmpRoot, 'project-root');
  await mkdir(projectRoot, { recursive: true });
  await writeFile(path.join(projectRoot, 'weekly-mdl.csv'), 'doc_no,title\nSYN-D-001,Synthetic\n', 'utf8');
  await writeFile(path.join(tmpRoot, 'outside.csv'), 'doc_no,title\nX,Y\n', 'utf8');
  process.env.CHIRALITY_SESSION_ROOT = path.join(tmpRoot, 'sessions');
  sessionCounter += 1;
  sessionId = `sess_pec_proposal_${sessionCounter}`;
  vi.stubEnv('CHIRALITY_PEC_AGENT_EMAIL', SENTINEL_EMAIL);
  vi.stubEnv('CHIRALITY_PEC_AGENT_PASSWORD', SENTINEL_PASSWORD);
});

afterEach(async () => {
  vi.unstubAllEnvs();
  delete process.env.CHIRALITY_SESSION_ROOT;
  await rm(tmpRoot, { recursive: true, force: true });
});

function writeContext() {
  return { projectRoot, sessionId, mode: 'workspaceWrite' };
}

function readContext() {
  return { projectRoot, sessionId };
}

describe('pec domain proposal tools — profileId registry gate', () => {
  it('refuses unregistered profileIds on both handlers', async () => {
    const client = makeFakeClient();
    const overrides = overridesFor(client);
    const expected = {
      type: 'INVALID_REQUEST',
      status: 400,
      message: 'profileId is not registered for this domain transport'
    };

    await expect(
      domainProposeOperationTool(
        writeContext(),
        { profileId: 'nope', projectId: 2, contract: 'mdl', csvContent: 'a,b\n' },
        overrides
      )
    ).rejects.toMatchObject(expected);
    await expect(
      domainProposalValidateTool(
        readContext(),
        { profileId: 'nope', projectId: 2, proposalId: 7 },
        overrides
      )
    ).rejects.toMatchObject(expected);
    expect(overrides.createClient).not.toHaveBeenCalled();
  });

  it('refuses open_pipe_stress specifically — the pec client is unreachable under any non-http-api profile', async () => {
    const client = makeFakeClient();
    const overrides = overridesFor(client);
    const expected = {
      type: 'INVALID_REQUEST',
      status: 400,
      message: 'profileId is not registered for the pec loopback HTTP proposal transport',
      details: {
        profileId: 'open_pipe_stress',
        engineKind: 'deterministic-cli',
        requiredEngineKind: 'http-api'
      }
    };

    await expect(
      domainProposeOperationTool(
        writeContext(),
        { profileId: 'open_pipe_stress', projectId: 2, contract: 'mdl', csvContent: 'a,b\n' },
        overrides
      )
    ).rejects.toMatchObject(expected);
    await expect(
      domainProposalValidateTool(
        readContext(),
        { profileId: 'open_pipe_stress', projectId: 2, proposalId: 7 },
        overrides
      )
    ).rejects.toMatchObject(expected);
    expect(overrides.createClient).not.toHaveBeenCalled();
  });
});

describe('domain_propose_operation — argument validation before any client call', () => {
  it('requires exactly one of csvContent or csvFileRef in propose mode', async () => {
    const client = makeFakeClient();
    const overrides = overridesFor(client);

    await expect(
      domainProposeOperationTool(
        writeContext(),
        {
          profileId: 'pec',
          projectId: 2,
          contract: 'mdl',
          csvContent: 'a,b\n',
          csvFileRef: 'weekly-mdl.csv'
        },
        overrides
      )
    ).rejects.toMatchObject({
      message: 'propose mode requires exactly one of csvContent or csvFileRef'
    });
    await expect(
      domainProposeOperationTool(
        writeContext(),
        { profileId: 'pec', projectId: 2, contract: 'mdl' },
        overrides
      )
    ).rejects.toMatchObject({
      message: 'propose mode requires exactly one of csvContent or csvFileRef'
    });
    expect(overrides.createClient).not.toHaveBeenCalled();
  });

  it('requires proposalId and expectedVersion in refresh mode', async () => {
    const client = makeFakeClient();
    const overrides = overridesFor(client);

    await expect(
      domainProposeOperationTool(
        writeContext(),
        { profileId: 'pec', projectId: 2, mode: 'refresh', expectedVersion: 2 },
        overrides
      )
    ).rejects.toMatchObject({ message: 'proposalId must be a positive integer' });
    await expect(
      domainProposeOperationTool(
        writeContext(),
        { profileId: 'pec', projectId: 2, mode: 'refresh', proposalId: 7 },
        overrides
      )
    ).rejects.toMatchObject({
      message: expect.stringContaining('refresh mode requires expectedVersion')
    });
    expect(overrides.createClient).not.toHaveBeenCalled();
  });

  it('refuses an unknown contract before any network call', async () => {
    const client = makeFakeClient();
    const overrides = overridesFor(client);

    await expect(
      domainProposeOperationTool(
        writeContext(),
        { profileId: 'pec', projectId: 2, contract: 'not-a-contract', csvContent: 'a,b\n' },
        overrides
      )
    ).rejects.toMatchObject({
      message: expect.stringContaining('propose mode requires contract')
    });
    expect(overrides.createClient).not.toHaveBeenCalled();
    expect(client.createProposal).not.toHaveBeenCalled();
  });

  it('refuses csvFileRef paths outside the project root (containment assert)', async () => {
    const client = makeFakeClient();
    const overrides = overridesFor(client);

    await expect(
      domainProposeOperationTool(
        writeContext(),
        {
          profileId: 'pec',
          projectId: 2,
          contract: 'mdl',
          csvFileRef: path.join(tmpRoot, 'outside.csv')
        },
        overrides
      )
    ).rejects.toMatchObject({
      type: 'INVALID_REQUEST',
      message: expect.stringContaining('csvFileRef must resolve inside projectRoot')
    });
    expect(overrides.createClient).not.toHaveBeenCalled();
  });
});

describe('domain_propose_operation — workspaceWrite permission overlay', () => {
  it('denies in readOnly mode with a permission event, tool.failed evidence, and no client call', async () => {
    const client = makeFakeClient();
    const overrides = overridesFor(client);

    await expect(
      domainProposeOperationTool(
        { projectRoot, sessionId, mode: 'readOnly' },
        { profileId: 'pec', projectId: 2, contract: 'mdl', csvContent: 'a,b\n' },
        overrides
      )
    ).rejects.toMatchObject({
      type: 'INVALID_REQUEST',
      status: 403
    });
    expect(overrides.createClient).not.toHaveBeenCalled();
    expect(client.createProposal).not.toHaveBeenCalled();

    const replay = await replayHarnessEvents(sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'tool.started',
      'tool.permission',
      'tool.failed'
    ]);
    expect(replay.events[1].data).toMatchObject({
      behavior: 'deny',
      toolName: 'mcp__chirality__domain_propose_operation'
    });
    expect(replay.events[2].data).toMatchObject({
      toolName: 'domain_propose_operation',
      failureSource: 'handler'
    });
  });

  it('allows in workspaceWrite mode and emits permission + completion evidence', async () => {
    const client = makeFakeClient();
    const overrides = overridesFor(client);

    const result = parseResult(
      await domainProposeOperationTool(
        writeContext(),
        { profileId: 'pec', projectId: 2, contract: 'mdl', csvContent: 'doc_no,title\nA,B\n' },
        overrides
      )
    );
    expect(result.ok).toBe(true);

    const replay = await replayHarnessEvents(sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'tool.started',
      'tool.permission',
      'tool.completed'
    ]);
    expect(replay.events[1].data).toMatchObject({ behavior: 'allow' });
    expect(replay.events[2].data).toMatchObject({
      resultSummary: {
        ok: true,
        mode: 'propose',
        id: 7,
        ref: 'IPR-0007',
        state: 'ready_for_review',
        version: 2,
        sourceSha256: 'abc123',
        dryRunAt: '2026-07-06T00:00:00.000Z',
        basisHistoryId: 41
      }
    });
  });
});

describe('domain_propose_operation — envelope and transport facts', () => {
  it('returns the engine response verbatim inside the D-APP-52 transport envelope', async () => {
    const client = makeFakeClient();
    const overrides = overridesFor(client);

    const result = parseResult(
      await domainProposeOperationTool(
        writeContext(),
        {
          profileId: 'pec',
          projectId: 2,
          contract: 'mdl',
          csvContent: 'doc_no,title\nA,B\n',
          sourceName: 'weekly.csv'
        },
        overrides
      )
    );

    expect(client.createProposal).toHaveBeenCalledTimes(1);
    expect(client.createProposal).toHaveBeenCalledWith(
      2,
      'mdl',
      'doc_no,title\nA,B\n',
      'weekly.csv'
    );
    expect(client.dispose).toHaveBeenCalledTimes(1);
    expect(result).toMatchObject({
      ok: true,
      profileId: 'pec',
      toolId: 'domain_propose_operation',
      mode: 'propose',
      transportStatus: {
        status: 'live',
        posture: 'D-T0-19 O-2A loopback HTTP transport (bridge P2, D-APP-52)',
        endpoint: {
          host: '127.0.0.1',
          port: 4899,
          method: 'POST',
          path: '/api/projects/2/import-proposals'
        },
        actorModel: expect.stringContaining('is_admin=0'),
        network: 'loopback-only; endpoint allowlist: login, propose, refresh, get-proposal',
        filesystemWrites: false,
        shell: false,
        originHeader: expect.stringContaining('RV-21')
      },
      inputs: {
        contract: 'mdl',
        sourceName: 'weekly.csv',
        csv: {
          source: 'inline',
          sha256: expect.any(String),
          byteLength: 17
        }
      },
      resultSemantics: expect.stringContaining('a green dry-run is NOT acceptance')
    });
    expect(result.engine).toEqual(ENGINE_PROPOSAL);
  });

  it('resolves csvFileRef inside the project root and records file evidence', async () => {
    const client = makeFakeClient();
    const overrides = overridesFor(client);

    const result = parseResult(
      await domainProposeOperationTool(
        writeContext(),
        { profileId: 'pec', projectId: 2, contract: 'mdl', csvFileRef: 'weekly-mdl.csv' },
        overrides
      )
    );

    expect(client.createProposal).toHaveBeenCalledTimes(1);
    expect(client.createProposal).toHaveBeenCalledWith(
      2,
      'mdl',
      'doc_no,title\nSYN-D-001,Synthetic\n',
      undefined
    );
    expect(result.inputs.csv).toMatchObject({
      source: 'fileRef',
      relativePath: 'weekly-mdl.csv',
      sha256: expect.any(String)
    });
  });

  it('routes refresh mode to refreshProposal with proposalId + expectedVersion', async () => {
    const client = makeFakeClient();
    const overrides = overridesFor(client);

    const result = parseResult(
      await domainProposeOperationTool(
        writeContext(),
        { profileId: 'pec', projectId: 2, mode: 'refresh', proposalId: 7, expectedVersion: 2 },
        overrides
      )
    );

    expect(client.refreshProposal).toHaveBeenCalledTimes(1);
    expect(client.refreshProposal).toHaveBeenCalledWith(2, 7, 2);
    expect(client.createProposal).not.toHaveBeenCalled();
    expect(result).toMatchObject({
      ok: true,
      mode: 'refresh',
      transportStatus: {
        endpoint: {
          method: 'POST',
          path: '/api/projects/2/import-proposals/7/refresh'
        }
      },
      inputs: { proposalId: 7, expectedVersion: 2 },
      engine: { version: 3 }
    });
  });

  it('keeps credentials and cookie material out of envelopes and harness events', async () => {
    const client = makeFakeClient();
    const overrides = overridesFor(client);

    const result = await domainProposeOperationTool(
      writeContext(),
      { profileId: 'pec', projectId: 2, contract: 'mdl', csvContent: 'doc_no,title\nA,B\n' },
      overrides
    );
    await domainProposalValidateTool(
      readContext(),
      { profileId: 'pec', projectId: 2, proposalId: 7 },
      overrides
    );

    const replay = await replayHarnessEvents(sessionId);
    const everything = JSON.stringify({ result, events: replay.events });
    expect(everything).not.toContain(SENTINEL_EMAIL);
    expect(everything).not.toContain(SENTINEL_PASSWORD);
    expect(everything).not.toContain(SENTINEL_COOKIE_TOKEN);
    // CSV bodies stay out of harness events (metadata-only evidence).
    expect(JSON.stringify(replay.events)).not.toContain('doc_no,title');
  });
});

describe('domain_propose_operation — error taxonomy as tool results', () => {
  it('surfaces 409 STALE_PROPOSAL as ok:false, normalFlow:true with the exact guidance (not a throw)', async () => {
    const client = makeFakeClient();
    client.refreshProposal.mockRejectedValueOnce(
      new PecBridgeError({
        errorClass: 'stale_proposal',
        status: 409,
        normalFlow: true,
        guidance: 'refresh the dry-run; a human re-reviews and re-accepts in pec',
        engineError: {
          code: 'STALE_PROPOSAL',
          message:
            "the project changed since this proposal's dry-run; refresh the dry-run and re-review (RV-13)",
          details: { basisHistoryId: 226, currentWatermark: 231 }
        },
        message: 'pec refused the request (409 STALE_PROPOSAL)'
      })
    );
    const overrides = overridesFor(client);

    const result = parseResult(
      await domainProposeOperationTool(
        writeContext(),
        { profileId: 'pec', projectId: 2, mode: 'refresh', proposalId: 7, expectedVersion: 2 },
        overrides
      )
    );

    expect(result).toMatchObject({
      ok: false,
      errorClass: 'stale_proposal',
      status: 409,
      normalFlow: true,
      guidance: 'refresh the dry-run; a human re-reviews and re-accepts in pec',
      engineError: { code: 'STALE_PROPOSAL' },
      transportStatus: { status: 'live' }
    });

    // Taxonomy results are completions, not tool crashes.
    const replay = await replayHarnessEvents(sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'tool.started',
      'tool.permission',
      'tool.completed'
    ]);
    expect(replay.events[2].data).toMatchObject({
      resultSummary: { ok: false, errorClass: 'stale_proposal', normalFlow: true }
    });
  });

  it('surfaces forbidden engine refusals as structured results without retries', async () => {
    const client = makeFakeClient();
    client.createProposal.mockRejectedValueOnce(
      new PecBridgeError({
        errorClass: 'forbidden',
        status: 403,
        engineError: { code: 'FORBIDDEN', message: 'import.propose: requires a register-handling role' },
        message: 'pec refused the request (403 FORBIDDEN)'
      })
    );
    const overrides = overridesFor(client);

    const result = parseResult(
      await domainProposeOperationTool(
        writeContext(),
        { profileId: 'pec', projectId: 2, contract: 'mdl', csvContent: 'a,b\n' },
        overrides
      )
    );

    expect(result).toMatchObject({
      ok: false,
      errorClass: 'forbidden',
      status: 403,
      normalFlow: false
    });
    expect(client.createProposal).toHaveBeenCalledTimes(1);
  });
});

describe('domain_proposal_validate — read grade (packet rider 7)', () => {
  it('performs exactly one GET: no POST-capable client method is reachable from any validate code path', async () => {
    const client = makeFakeClient();
    const overrides = overridesFor(client);

    const result = parseResult(
      await domainProposalValidateTool(
        readContext(),
        { profileId: 'pec', projectId: 2, proposalId: 7 },
        overrides
      )
    );

    expect(client.getProposal).toHaveBeenCalledTimes(1);
    expect(client.getProposal).toHaveBeenCalledWith(2, 7);
    // Rider-7 pin: the validate handler never invokes the mutating client
    // methods (propose/refresh) — the only POST-capable data operations.
    expect(client.createProposal).not.toHaveBeenCalled();
    expect(client.refreshProposal).not.toHaveBeenCalled();
    expect(client.dispose).toHaveBeenCalledTimes(1);

    expect(result).toMatchObject({
      ok: true,
      profileId: 'pec',
      toolId: 'domain_proposal_validate',
      transportStatus: {
        status: 'live',
        endpoint: {
          host: '127.0.0.1',
          port: 4899,
          method: 'GET',
          path: '/api/projects/2/import-proposals/7'
        }
      },
      resultSemantics: expect.stringContaining('no domain verdict')
    });
    // Never recomputes: the stored report is returned verbatim.
    expect(result.engine).toEqual(ENGINE_PROPOSAL);
  });

  it('runs in read mode with read-tool evidence semantics (no permission gate)', async () => {
    const client = makeFakeClient();
    const overrides = overridesFor(client);

    await domainProposalValidateTool(
      readContext(),
      { profileId: 'pec', projectId: 2, proposalId: 7 },
      overrides
    );

    const replay = await replayHarnessEvents(sessionId);
    expect(replay.events.map((event) => event.type)).toEqual(['tool.started', 'tool.completed']);
    expect(replay.events[1].data).toMatchObject({
      toolName: 'domain_proposal_validate',
      adapterToolName: 'mcp__chirality__domain_proposal_validate',
      resultSummary: { ok: true, id: 7, ref: 'IPR-0007', dryRunAt: '2026-07-06T00:00:00.000Z' }
    });
  });

  it('maps transport errors to structured results (network_error) instead of throwing', async () => {
    const client = makeFakeClient();
    client.getProposal.mockRejectedValueOnce(
      new PecBridgeError({
        errorClass: 'network_error',
        message: 'pec engine is unreachable at http://127.0.0.1:4899'
      })
    );
    const overrides = overridesFor(client);

    const result = parseResult(
      await domainProposalValidateTool(
        readContext(),
        { profileId: 'pec', projectId: 2, proposalId: 7 },
        overrides
      )
    );
    expect(result).toMatchObject({
      ok: false,
      errorClass: 'network_error',
      normalFlow: false,
      toolId: 'domain_proposal_validate'
    });
  });
});
