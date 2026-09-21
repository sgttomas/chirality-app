/**
 * Opt-in live-seam integration test for the D-APP-52 pec bridge (packet
 * Validation section; brief §3 tests-only carve-out). NOT part of default CI:
 * set `PEC_BRIDGE_IT=1` to run. Spawns a D-PEC-06-guarded scratch-DB pec
 * server from `projects/pec` on a loopback port, drives the two live handlers
 * against it under the rehearsal actor model (agent person `is_admin=0`,
 * coordinator), then tears the server down and deletes the DB (+wal/shm).
 * Requires Node >= 23.6 (pec type-stripping runtime).
 */
import { mkdtemp, rm } from 'node:fs/promises';
import { randomBytes } from 'node:crypto';
import os from 'node:os';
import path from 'node:path';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import {
  domainProposalValidateTool,
  domainProposeOperationTool
} from '../../lib/harness/mcp/domain-proposal-tools';

const OPT_IN = process.env.PEC_BRIDGE_IT === '1';

const SYNTHETIC_MDL_CSV = [
  'doc_no,title,package,discipline,owner,current_rev,state,due_date,milestone,issue_purpose_plan,edms_ref,client_no,remarks,deliverable_type',
  'SYN-D-101,Bridge IT design basis — synthetic,SYN-PKG-101,Process,admin@aurora.dev,A,in_work,2026-09-15,Gate 2,IFR,SYN-EDMS-0101,,Synthetic D-APP-52 integration row,Design Basis',
  'SYN-D-102,Bridge IT equipment list — synthetic,SYN-PKG-101,Mechanical,admin@aurora.dev,A,in_work,2026-09-22,Gate 2,IFR,SYN-EDMS-0102,,Synthetic D-APP-52 integration row,Equipment List',
  ''
].join('\n');

function parseResult(result: { content: Array<{ type: string; text?: string }> }): any {
  const first = result.content[0];
  if (!first || first.type !== 'text' || typeof first.text !== 'string') {
    throw new Error('Expected text MCP result');
  }
  return JSON.parse(first.text);
}

describe.runIf(OPT_IN)('pec bridge live scratch seam (opt-in, PEC_BRIDGE_IT=1)', () => {
  const agentEmail = 'pec-bridge-agent@rehearsal.demo';
  const agentPassword = randomBytes(16).toString('hex');
  const port = 4901 + Math.floor(Math.random() * 50);
  let helper: typeof import('../../../scripts/pec-scratch-server.mjs');
  let repoRoot = '';
  let scratchDir = '';
  let dbPath = '';
  let server: { stop(): Promise<void> } | undefined;
  let projectId = 0;
  let projectRoot = '';
  let sessionRoot = '';
  const savedEnv: Record<string, string | undefined> = {};

  beforeAll(async () => {
    helper = await import('../../../scripts/pec-scratch-server.mjs');
    helper.assertTypeStrippingNode();
    repoRoot = helper.repoRootFrom(process.cwd());
    projectRoot = repoRoot;
    scratchDir = await mkdtemp(path.join(os.tmpdir(), 'pec-scratch-bridge-it-'));
    sessionRoot = path.join(scratchDir, 'sessions');
    dbPath = path.join(scratchDir, 'pec-scratch-bridge.db');

    helper.seedScratchDb({ repoRoot, dbPath });
    const actors = await helper.provisionBridgeActors({
      dbPath,
      agentEmail,
      agentPasswordHash: helper.hashPecPassword(agentPassword)
    });
    projectId = actors.projectId;
    server = await helper.startScratchServer({ repoRoot, dbPath, port });

    for (const key of [
      'CHIRALITY_PEC_PORT',
      'CHIRALITY_PEC_AGENT_EMAIL',
      'CHIRALITY_PEC_AGENT_PASSWORD',
      'CHIRALITY_SESSION_ROOT'
    ]) {
      savedEnv[key] = process.env[key];
    }
    process.env.CHIRALITY_PEC_PORT = String(port);
    process.env.CHIRALITY_PEC_AGENT_EMAIL = agentEmail;
    process.env.CHIRALITY_PEC_AGENT_PASSWORD = agentPassword;
    process.env.CHIRALITY_SESSION_ROOT = sessionRoot;
  }, 180000);

  afterAll(async () => {
    await server?.stop();
    if (dbPath) {
      helper.deleteScratchDb(dbPath);
    }
    if (scratchDir) {
      await rm(scratchDir, { recursive: true, force: true });
    }
    for (const [key, value] of Object.entries(savedEnv)) {
      if (value === undefined) {
        delete process.env[key];
      } else {
        process.env[key] = value;
      }
    }
  }, 60000);

  it('drives propose → validate (no recompute) → refresh through the live seam', async () => {
    const writeContext = { projectRoot, sessionId: 'sess_pec_bridge_it', mode: 'workspaceWrite' };
    const readContext = { projectRoot, sessionId: 'sess_pec_bridge_it' };

    const proposed = parseResult(
      await domainProposeOperationTool(writeContext, {
        profileId: 'pec',
        projectId,
        contract: 'mdl',
        csvContent: SYNTHETIC_MDL_CSV,
        sourceName: 'bridge-it-mdl.csv'
      })
    );
    expect(proposed.ok).toBe(true);
    expect(proposed.engine).toMatchObject({
      contract: 'mdl',
      state: 'ready_for_review',
      sourceName: 'bridge-it-mdl.csv'
    });
    expect(proposed.engine.dryRunReport).toMatchObject({ accepted: 2 });
    const proposalId = proposed.engine.id as number;

    const validated = parseResult(
      await domainProposalValidateTool(readContext, { profileId: 'pec', projectId, proposalId })
    );
    expect(validated.ok).toBe(true);
    // Read-only: the stored report is returned without recompute — version and
    // dryRunAt are unchanged by the GET (rider 7).
    expect(validated.engine.version).toBe(proposed.engine.version);
    expect(validated.engine.dryRunAt).toBe(proposed.engine.dryRunAt);
    expect(validated.engine.dryRunReport).toEqual(proposed.engine.dryRunReport);

    const revalidated = parseResult(
      await domainProposalValidateTool(readContext, { profileId: 'pec', projectId, proposalId })
    );
    expect(revalidated.engine.version).toBe(validated.engine.version);
    expect(revalidated.engine.dryRunAt).toBe(validated.engine.dryRunAt);

    const refreshed = parseResult(
      await domainProposeOperationTool(writeContext, {
        profileId: 'pec',
        projectId,
        mode: 'refresh',
        proposalId,
        expectedVersion: validated.engine.version as number
      })
    );
    expect(refreshed.ok).toBe(true);
    expect(refreshed.engine.version).toBeGreaterThan(validated.engine.version as number);
    expect(refreshed.engine.state).toBe('ready_for_review');
  }, 60000);

  it('surfaces an engine 403 as a structured forbidden result for a non-granted persona', async () => {
    const writeContext = { projectRoot, sessionId: 'sess_pec_bridge_it_403', mode: 'workspaceWrite' };
    const previousEmail = process.env.CHIRALITY_PEC_AGENT_EMAIL;
    const previousPassword = process.env.CHIRALITY_PEC_AGENT_PASSWORD;
    process.env.CHIRALITY_PEC_AGENT_EMAIL = 'viewer@aurora.dev';
    process.env.CHIRALITY_PEC_AGENT_PASSWORD = 'pilot'; // pec's committed demo-seed password
    try {
      const refused = parseResult(
        await domainProposeOperationTool(writeContext, {
          profileId: 'pec',
          projectId,
          contract: 'mdl',
          csvContent: SYNTHETIC_MDL_CSV
        })
      );
      expect(refused).toMatchObject({
        ok: false,
        errorClass: 'forbidden',
        status: 403,
        normalFlow: false
      });
    } finally {
      process.env.CHIRALITY_PEC_AGENT_EMAIL = previousEmail;
      process.env.CHIRALITY_PEC_AGENT_PASSWORD = previousPassword;
    }
  }, 60000);

  it('surfaces an engine 409 version conflict as a structured result with zero retries', async () => {
    const writeContext = { projectRoot, sessionId: 'sess_pec_bridge_it_409', mode: 'workspaceWrite' };
    const proposed = parseResult(
      await domainProposeOperationTool(writeContext, {
        profileId: 'pec',
        projectId,
        contract: 'mdl',
        csvContent: SYNTHETIC_MDL_CSV
      })
    );
    const conflicted = parseResult(
      await domainProposeOperationTool(writeContext, {
        profileId: 'pec',
        projectId,
        mode: 'refresh',
        proposalId: proposed.engine.id as number,
        expectedVersion: (proposed.engine.version as number) + 41
      })
    );
    expect(conflicted).toMatchObject({
      ok: false,
      errorClass: 'version_conflict',
      status: 409,
      normalFlow: false
    });
  }, 60000);
});

if (!OPT_IN) {
  describe('pec bridge live scratch seam (opt-in)', () => {
    it.skip('skipped: set PEC_BRIDGE_IT=1 to spawn the scratch-DB pec server seam test (Node >= 23.6)', () => {
      // Intentionally skipped in the default key-independent suite.
    });
  });
}
