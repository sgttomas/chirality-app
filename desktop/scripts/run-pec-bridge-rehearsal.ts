/**
 * D-APP-52 bridge rehearsal driver (packet Evidence section; plan §5).
 *
 * Captures the hermetic scratch-basis rehearsal
 * `projects/pec/execution/_Coordination/AgentRuns/PEC_2026-07-06_BRIDGE-evidence-01/` by DIRECT HANDLER
 * INVOCATION: it calls the exact handler functions the MCP server registers
 * (`domainProposeOperationTool` / `domainProposalValidateTool`) with a real
 * session context against a D-PEC-06-guarded scratch pec server. No
 * ANTHROPIC_API_KEY exists this session; live-LLM demonstration through a
 * harness model session is DEFERRED and stated plainly in the manifest —
 * nothing is faked as a model session.
 *
 * Demo-cast owner-role acts (accept / screen act / apply) run script-side as
 * the seeded admin persona over the live HTTP API — never through the agent
 * person, never through any registered tool — and every apply passes
 * `force: false` hard-coded with no override parameter (packet rider 5; the
 * Receipt 32 "force=true in any form" exclusion has no scratch carve-out).
 *
 * Run from `projects/chirality-app-dev/frontend/`:
 *   npx vite-node scripts/run-pec-bridge-rehearsal.ts
 */
import { execSync } from 'node:child_process';
import { createHash, randomBytes } from 'node:crypto';
import { mkdir, mkdtemp, readdir, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {
  domainProposalValidateTool,
  domainProposeOperationTool
} from '../src/lib/harness/mcp/domain-proposal-tools';
import {
  assertTypeStrippingNode,
  deleteScratchDb,
  hashPecPassword,
  provisionBridgeActors,
  repoRootFrom,
  seedScratchDb,
  startScratchServer
} from './pec-scratch-server.mjs';

const AGENT_EMAIL = 'pec-bridge-agent@rehearsal.demo';
const ADMIN_EMAIL = 'admin@aurora.dev';
const VIEWER_EMAIL = 'viewer@aurora.dev';
const SEED_DEMO_PASSWORD = 'pilot'; // pec's committed demo-seed password (synthetic personas)
const PORT = 4907;
const EVIDENCE_DIR_NAME = 'PEC_2026-07-06_BRIDGE-evidence-01';

const SYNTHETIC_MDL_CSV = [
  'doc_no,title,package,discipline,owner,current_rev,state,due_date,milestone,issue_purpose_plan,edms_ref,client_no,remarks,deliverable_type',
  'SYN-D-201,Bridge design basis — synthetic,SYN-PKG-201,Process,admin@aurora.dev,A,in_work,2026-09-15,Gate 2,IFR,SYN-EDMS-0201,,Synthetic D-APP-52 bridge rehearsal row,Design Basis',
  'SYN-D-202,Bridge equipment list — synthetic,SYN-PKG-201,Mechanical,admin@aurora.dev,A,in_work,2026-09-22,Gate 2,IFR,SYN-EDMS-0202,,Synthetic D-APP-52 bridge rehearsal row,Equipment List',
  'SYN-D-203,Bridge line list — synthetic,SYN-PKG-201,Piping,admin@aurora.dev,A,in_work,2026-09-29,Gate 2,IFR,SYN-EDMS-0203,,Synthetic D-APP-52 bridge rehearsal row,Line List',
  ''
].join('\n');

type ToolResult = { content: Array<{ type: string; text?: string }> };

function parseEnvelope(result: ToolResult): Record<string, any> {
  const first = result.content[0];
  if (!first || first.type !== 'text' || typeof first.text !== 'string') {
    throw new Error('Expected text MCP tool result');
  }
  return JSON.parse(first.text) as Record<string, any>;
}

function sha256(content: string | Buffer): string {
  return createHash('sha256').update(content).digest('hex');
}

async function main(): Promise<void> {
  assertTypeStrippingNode();
  const repoRoot = repoRootFrom(process.cwd());
  const codeSha = execSync('git rev-parse HEAD', { cwd: repoRoot, encoding: 'utf8' }).trim();

  const evidenceDir = path.join(repoRoot, 'projects', 'pec', 'execution', '_Coordination', 'AgentRuns', EVIDENCE_DIR_NAME);
  const inputsDir = path.join(evidenceDir, 'inputs');
  const artifactsDir = path.join(evidenceDir, 'artifacts');
  const mirrorPath = path.join(
    repoRoot,
    '_DomainEngines',
    'proposals',
    'pec',
    'OP_2026-07-06_BRIDGE_rehearsal_IPR-0001-0002.md'
  );
  await mkdir(inputsDir, { recursive: true });
  await mkdir(artifactsDir, { recursive: true });

  // ---- basis prep (script-side instance setup, not workflow acts) ----------
  const scratchDir = await mkdtemp(path.join(os.tmpdir(), 'pec-scratch-bridge-rehearsal-'));
  const dbPath = path.join(scratchDir, 'pec-scratch-bridge.db');
  const agentPassword = randomBytes(16).toString('hex'); // generated at runtime; never committed
  console.log(`[basis] seeding scratch DB ${dbPath}`);
  seedScratchDb({ repoRoot, dbPath });
  const actors = await provisionBridgeActors({
    dbPath,
    agentEmail: AGENT_EMAIL,
    agentPasswordHash: hashPecPassword(agentPassword)
  });
  console.log(`[basis] provisioned actors ${JSON.stringify(actors)}`);
  const server = await startScratchServer({ repoRoot, dbPath, port: PORT });
  console.log(`[basis] scratch server on 127.0.0.1:${PORT}`);

  process.env.CHIRALITY_PEC_PORT = String(PORT);
  process.env.CHIRALITY_PEC_AGENT_EMAIL = AGENT_EMAIL;
  process.env.CHIRALITY_PEC_AGENT_PASSWORD = agentPassword;
  process.env.CHIRALITY_SESSION_ROOT = path.join(scratchDir, 'sessions');

  const projectId = actors.projectId;
  const writeContext = {
    projectRoot: repoRoot,
    sessionId: 'sess_dapp52_bridge_rehearsal',
    mode: 'workspaceWrite'
  };
  const readContext = { projectRoot: repoRoot, sessionId: 'sess_dapp52_bridge_rehearsal' };

  const artifacts: string[] = [];
  async function writeArtifact(name: string, payload: unknown): Promise<void> {
    const filePath = path.join(artifactsDir, name);
    await writeFile(filePath, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
    artifacts.push(name);
    console.log(`[artifact] ${name}`);
  }

  // ---- demo-cast HTTP machinery (owner-role persona; disclosed) ------------
  const baseUrl = `http://127.0.0.1:${PORT}`;
  async function loginAs(email: string, password: string): Promise<string> {
    const response = await fetch(`${baseUrl}/api/auth/login`, {
      method: 'POST',
      redirect: 'error',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    if (!response.ok) {
      throw new Error(`demo-cast login failed for ${email}: ${response.status}`);
    }
    const setCookie = response.headers.get('set-cookie') ?? '';
    const match = /pec_session=([^;]+)/.exec(setCookie);
    await response.arrayBuffer().catch(() => undefined);
    if (!match) {
      throw new Error('demo-cast login carried no cookie');
    }
    return match[1] as string;
  }
  async function demoCast(
    cookie: string,
    method: 'GET' | 'POST',
    apiPath: string,
    body?: unknown
  ): Promise<{ status: number; body: unknown }> {
    const response = await fetch(`${baseUrl}${apiPath}`, {
      method,
      redirect: 'error',
      headers: {
        cookie: `pec_session=${cookie}`,
        ...(body !== undefined ? { 'content-type': 'application/json' } : {})
      },
      ...(body !== undefined ? { body: JSON.stringify(body) } : {})
    });
    const payload = await response.json().catch(() => undefined);
    return { status: response.status, body: payload };
  }

  try {
    // ---- inputs ------------------------------------------------------------
    const inputFile = path.join(inputsDir, 'mdl-syn-v1.csv');
    await writeFile(inputFile, SYNTHETIC_MDL_CSV, 'utf8');

    // ---- 00: agent login (identity fact only; no credentials, no cookie) ----
    await writeArtifact('00-agent-login.json', {
      step: '00-agent-login',
      ok: true,
      actor: {
        email: AGENT_EMAIL,
        personId: actors.agentPersonId,
        is_admin: 0,
        role: 'coordinator (import.propose grant; never import.accept)'
      },
      note: 'Session established by the transport client login() from local-environment credentials; the login response body is discarded by design and neither credentials nor the cookie appear in any artifact.'
    });

    // ---- 01: propose via the registered handler (csvFileRef path) -----------
    const proposeEnvelope = parseEnvelope(
      (await domainProposeOperationTool(writeContext, {
        profileId: 'pec',
        projectId,
        contract: 'mdl',
        csvFileRef: path.relative(repoRoot, inputFile),
        sourceName: 'mdl-syn-v1.csv'
      })) as ToolResult
    );
    await writeArtifact('01-propose-mdl-v1.json', proposeEnvelope);
    const proposalId = proposeEnvelope.engine.id as number;

    // ---- 02: validate (stored report; no recompute) --------------------------
    const validateEnvelope = parseEnvelope(
      (await domainProposalValidateTool(readContext, {
        profileId: 'pec',
        projectId,
        proposalId
      })) as ToolResult
    );
    await writeArtifact('02-validate-initial.json', validateEnvelope);
    if (validateEnvelope.engine.dryRunAt !== proposeEnvelope.engine.dryRunAt) {
      throw new Error('validate recomputed the dry-run (dryRunAt changed) — rider 7 violation');
    }

    // ---- 03: demo-cast owner accept (disclosed; NOT a registered tool) ------
    const adminCookie = await loginAs(ADMIN_EMAIL, SEED_DEMO_PASSWORD);
    const accept = await demoCast(
      adminCookie,
      'POST',
      `/api/projects/${projectId}/import-proposals/${proposalId}/accept`,
      {
        version: validateEnvelope.engine.version,
        sha256: validateEnvelope.engine.sourceSha256
      }
    );
    await writeArtifact('03-demo-cast-accept.json', {
      demoCast: true,
      act: 'accept',
      actor: `${ADMIN_EMAIL} (owner-role admin persona, personId ${actors.adminPersonId})`,
      mechanism: 'script-side HTTP as the admin persona — not the agent person, not a registered tool',
      engineResponse: accept
    });
    if (accept.status !== 200) {
      throw new Error(`demo-cast accept failed: ${accept.status}`);
    }

    // ---- 04: demo-cast owner screen act moves the watermark ------------------
    const screenAct = await demoCast(adminCookie, 'POST', `/api/projects/${projectId}/intake`, {
      statement: 'Synthetic owner screen act: bridge rehearsal watermark mover (D-APP-52).',
      quickType: 'action'
    });
    await writeArtifact('04-demo-cast-screen-act.json', {
      demoCast: true,
      act: 'screen-act (raise intake item)',
      actor: `${ADMIN_EMAIL} (owner-role admin persona)`,
      purpose: 'moves the project history watermark so the accepted proposal goes stale (RV-13)',
      engineResponse: screenAct
    });
    if (screenAct.status !== 200) {
      throw new Error(`demo-cast screen act failed: ${screenAct.status}`);
    }

    // ---- 05: demo-cast owner apply attempt (force: false) → 409 STALE --------
    const staleApply = await demoCast(
      adminCookie,
      'POST',
      `/api/projects/${projectId}/import-proposals/${proposalId}/apply`,
      {
        version: (accept.body as any).version, // the version the accept act returned
        force: false // rider 5: hard-coded; no override parameter exists in this driver
      }
    );
    await writeArtifact('05-demo-cast-apply-stale-409.json', {
      demoCast: true,
      act: 'apply (attempt)',
      actor: `${ADMIN_EMAIL} (owner-role admin persona)`,
      force: false,
      engineResponse: staleApply
    });
    if (staleApply.status !== 409 || (staleApply.body as any)?.error?.code !== 'STALE_PROPOSAL') {
      throw new Error(`expected 409 STALE_PROPOSAL, got ${JSON.stringify(staleApply)}`);
    }

    // ---- 06: agent recovery through the tool surface -------------------------
    const preRefreshValidate = parseEnvelope(
      (await domainProposalValidateTool(readContext, {
        profileId: 'pec',
        projectId,
        proposalId
      })) as ToolResult
    );
    await writeArtifact('06a-validate-pre-refresh.json', preRefreshValidate);
    const refreshEnvelope = parseEnvelope(
      (await domainProposeOperationTool(writeContext, {
        profileId: 'pec',
        projectId,
        mode: 'refresh',
        proposalId,
        expectedVersion: preRefreshValidate.engine.version as number
      })) as ToolResult
    );
    await writeArtifact('06b-refresh-recovery.json', refreshEnvelope);
    if (refreshEnvelope.engine.acceptedBy !== null) {
      throw new Error('refresh did not void the prior acceptance (RV-13)');
    }

    // ---- 07: validate post-refresh -------------------------------------------
    const postRefreshValidate = parseEnvelope(
      (await domainProposalValidateTool(readContext, {
        profileId: 'pec',
        projectId,
        proposalId
      })) as ToolResult
    );
    await writeArtifact('07-validate-post-refresh.json', postRefreshValidate);

    // ---- 08: demo-cast re-accept + apply (force: false) → applied -------------
    const reAccept = await demoCast(
      adminCookie,
      'POST',
      `/api/projects/${projectId}/import-proposals/${proposalId}/accept`,
      {
        version: postRefreshValidate.engine.version,
        sha256: postRefreshValidate.engine.sourceSha256
      }
    );
    await writeArtifact('08a-demo-cast-re-accept.json', {
      demoCast: true,
      act: 'accept (re-accept after refresh)',
      actor: `${ADMIN_EMAIL} (owner-role admin persona)`,
      engineResponse: reAccept
    });
    if (reAccept.status !== 200) {
      throw new Error(`demo-cast re-accept failed: ${reAccept.status}`);
    }
    const finalApply = await demoCast(
      adminCookie,
      'POST',
      `/api/projects/${projectId}/import-proposals/${proposalId}/apply`,
      {
        version: (reAccept.body as any).version,
        force: false // rider 5: force is ALWAYS false; force=true never occurs in any form
      }
    );
    await writeArtifact('08b-demo-cast-apply.json', {
      demoCast: true,
      act: 'apply',
      actor: `${ADMIN_EMAIL} (owner-role admin persona)`,
      force: false,
      engineResponse: finalApply
    });
    if (finalApply.status !== 200 || (finalApply.body as any).state !== 'applied') {
      throw new Error(`demo-cast apply failed: ${JSON.stringify(finalApply.status)}`);
    }

    // ---- 09: error-taxonomy captures through the tool surface -----------------
    // 09a — engine 400: refresh of a terminal (applied) proposal.
    const taxonomy400 = parseEnvelope(
      (await domainProposeOperationTool(writeContext, {
        profileId: 'pec',
        projectId,
        mode: 'refresh',
        proposalId,
        expectedVersion: (finalApply.body as any).version as number
      })) as ToolResult
    );
    await writeArtifact('09a-taxonomy-400-refresh-of-applied.json', taxonomy400);
    if (taxonomy400.errorClass !== 'bad_request') {
      throw new Error(`expected bad_request, got ${taxonomy400.errorClass}`);
    }

    // 09b — engine 403: propose as a non-granted persona (viewer) through a
    // second client (credentials swapped in the local environment only).
    process.env.CHIRALITY_PEC_AGENT_EMAIL = VIEWER_EMAIL;
    process.env.CHIRALITY_PEC_AGENT_PASSWORD = SEED_DEMO_PASSWORD;
    const taxonomy403 = parseEnvelope(
      (await domainProposeOperationTool(writeContext, {
        profileId: 'pec',
        projectId,
        contract: 'mdl',
        csvContent: SYNTHETIC_MDL_CSV
      })) as ToolResult
    );
    process.env.CHIRALITY_PEC_AGENT_EMAIL = AGENT_EMAIL;
    process.env.CHIRALITY_PEC_AGENT_PASSWORD = agentPassword;
    await writeArtifact('09b-taxonomy-403-viewer-propose.json', taxonomy403);
    if (taxonomy403.errorClass !== 'forbidden') {
      throw new Error(`expected forbidden, got ${taxonomy403.errorClass}`);
    }

    // 09c — engine 409 version conflict: stale expectedVersion refresh on a
    // fresh second proposal (IPR-0002; left ready_for_review, disclosed).
    const secondPropose = parseEnvelope(
      (await domainProposeOperationTool(writeContext, {
        profileId: 'pec',
        projectId,
        contract: 'mdl',
        csvContent: SYNTHETIC_MDL_CSV,
        sourceName: 'mdl-syn-v1-second.csv'
      })) as ToolResult
    );
    await writeArtifact('09c1-propose-second-ipr0002.json', secondPropose);
    const taxonomy409 = parseEnvelope(
      (await domainProposeOperationTool(writeContext, {
        profileId: 'pec',
        projectId,
        mode: 'refresh',
        proposalId: secondPropose.engine.id as number,
        expectedVersion: (secondPropose.engine.version as number) + 41
      })) as ToolResult
    );
    await writeArtifact('09c2-taxonomy-409-version-conflict.json', taxonomy409);
    if (taxonomy409.errorClass !== 'version_conflict') {
      throw new Error(`expected version_conflict, got ${taxonomy409.errorClass}`);
    }

    // ---- 10: history extracts (agent vs demo-cast-admin attribution) ----------
    const histProposal = await demoCast(
      adminCookie,
      'GET',
      `/api/projects/${projectId}/history/import_proposal/${proposalId}`
    );
    await writeArtifact('10a-hist-ipr0001.json', {
      capture: 'history extract (script-side read as the admin persona; disclosed)',
      actorLegend: {
        [String(actors.agentPersonId)]: `${AGENT_EMAIL} (agent person, is_admin=0)`,
        [String(actors.adminPersonId)]: `${ADMIN_EMAIL} (owner-role demo-cast admin persona)`
      },
      engineResponse: histProposal
    });
    const histSecond = await demoCast(
      adminCookie,
      'GET',
      `/api/projects/${projectId}/history/import_proposal/${secondPropose.engine.id}`
    );
    await writeArtifact('10b-hist-ipr0002.json', {
      capture: 'history extract (script-side read as the admin persona; disclosed)',
      engineResponse: histSecond
    });

    // ---- teardown, then 09d network_error through the tool surface ------------
    await server.stop();
    const taxonomyNetwork = parseEnvelope(
      (await domainProposalValidateTool(readContext, {
        profileId: 'pec',
        projectId,
        proposalId
      })) as ToolResult
    );
    await writeArtifact('11-taxonomy-network-error-after-teardown.json', taxonomyNetwork);
    if (taxonomyNetwork.errorClass !== 'network_error') {
      throw new Error(`expected network_error, got ${taxonomyNetwork.errorClass}`);
    }

    deleteScratchDb(dbPath);
    console.log('[teardown] scratch server stopped; scratch DB (+wal/shm) deleted');

    // ---- mirror (brief §7) -----------------------------------------------------
    const csvSha = sha256(SYNTHETIC_MDL_CSV);
    const mirror = `# OP mirror — D-APP-52 bridge rehearsal proposals (IPR-0001..0002, batch form disclosed)

> Non-authoritative mirror of the proposal CSVs and reports captured in
> \`projects/pec/execution/_Coordination/AgentRuns/${EVIDENCE_DIR_NAME}/\` (D-T0-13; brief §7). Scratch
> basis only; synthetic data; the scratch DB was deleted after capture.

## IPR-0001 — mdl, applied after the ruled staleness-recovery loop

- Source CSV: \`inputs/mdl-syn-v1.csv\` (sha256 \`${csvSha}\`), 3 synthetic MDL rows.
- Path: propose (agent tool) → validate → demo-cast accept → owner screen act →
  demo-cast apply \`force: false\` → **409 STALE_PROPOSAL** → tool refresh
  (acceptance voided) → validate → demo-cast re-accept → demo-cast apply
  \`force: false\` → applied.
- Dry-run and apply reports: verbatim in artifacts \`01\`, \`06b\`, \`08b\`.

\`\`\`json
${JSON.stringify({ dryRun: proposeEnvelope.engine.dryRunReport, applyReport: (finalApply.body as any).applyReport }, null, 2)}
\`\`\`

## IPR-0002 — mdl, ready_for_review (taxonomy exercise only; never accepted)

- Same synthetic CSV content (sha256 \`${csvSha}\`); used to capture the 409
  version-conflict taxonomy (artifact \`09c2\`); left un-accepted by design.

\`\`\`json
${JSON.stringify({ dryRun: secondPropose.engine.dryRunReport }, null, 2)}
\`\`\`
`;
    await writeFile(mirrorPath, mirror, 'utf8');

    // ---- manifest ---------------------------------------------------------------
    const shaLines: string[] = [];
    for (const name of ['inputs/mdl-syn-v1.csv', ...artifacts.map((a) => `artifacts/${a}`)]) {
      const content = await readFile(path.join(evidenceDir, name));
      shaLines.push(`${sha256(content)}  ${name}`);
    }

    const manifest = `# PEC D-APP-52 bridge rehearsal 01 — the live proposal tools, driven end to end on a scratch basis

> **Epistemic status: immutable evidence snapshot** (D-T0-13 capture
> convention). Facts only; no pilot-readiness, correctness, go-live, or
> live-LLM-binding claim (K-DOMAIN-4; F-PEC-2).

## Basis

- **Authority:** D-APP-52 O-A (riders 1–11 binding), recorded 2026-07-06 under
  the owner's conditional pre-ruling — packet
  \`projects/chirality-app-dev/execution/_Coordination/_DECISIONS/D-APP-52_PACKET_PEC_TRANSPORT_PROPOSAL_TOOLS_2026-07-06.md\`;
  ruling record \`D-APP-52_RULING_2026-07-06.md\`.
- **Code under test:** this repository at \`${codeSha}\` (the D-APP-52 tranche
  source commit; handlers \`domainProposeOperationTool\` /
  \`domainProposalValidateTool\` in
  \`projects/chirality-app-dev/frontend/src/lib/harness/mcp/domain-proposal-tools.ts\`
  over \`pec-bridge-client.ts\`; zero pec source change).
- **Instance:** fresh scratch DB \`<tmpdir>/pec-scratch-bridge-rehearsal-*/pec-scratch-bridge.db\`
  (D-PEC-06-guarded \`npm run seed\` + script-side basis prep: synthetic project
  \`SYN\` id ${projectId}, actor provisioning), served on \`127.0.0.1:${PORT}\`;
  **scratch DB (+wal/shm) deleted after capture** — recorded below. No real
  data ever existed in it.
- **Driver mechanism (key-independence, stated plainly):** **no
  \`ANTHROPIC_API_KEY\` exists this session and none was used.** The two
  handlers are deterministic HTTP wrappers, so this rehearsal drives them by
  **direct handler invocation** — the same functions
  \`buildChiralityMcpTools\` registers — via
  \`npx vite-node scripts/run-pec-bridge-rehearsal.ts\` (vitest's TS runtime;
  run from \`projects/chirality-app-dev/frontend/\`), capturing the exact
  envelopes a model session would receive. **Live-LLM demonstration through a
  harness model session is DEFERRED.** Nothing is faked, stubbed-as-if-live,
  or key-worked-around.
- **Data:** synthetic MDL CSV fabricated for this rehearsal (\`inputs/\`);
  no D-T0-14 residency question.

## Actors

| Actor | Identity | Acts |
|---|---|---|
| Agent person | \`${AGENT_EMAIL}\` (personId ${actors.agentPersonId}, \`is_admin=0\`, coordinator — \`import.propose\`, never \`import.accept\`) | every registered-tool act: propose, validate, refresh; credentials generated at runtime from the local environment, never committed, never in artifacts |
| Demo-cast owner persona | \`${ADMIN_EMAIL}\` (personId ${actors.adminPersonId}, admin role on SYN) | every accept / screen act / apply — script-side HTTP, disclosed per act below; permitted on the scratch basis by the D-PEC-12 full-agency amendment |
| Non-granted persona | \`${VIEWER_EMAIL}\` (viewer role) | the 403 taxonomy capture only |

Basis prep (seed, SYN project, actor provisioning) ran script-side as instance
setup, not as workflow acts.

## What happened (every step verbatim in \`artifacts/\`)

| Step | Artifact | Act | Result |
|---|---|---|---|
| 00 | \`00-agent-login.json\` | agent session established (identity fact only) | ok |
| 01 | \`01-propose-mdl-v1.json\` | \`domain_propose_operation\` mode=propose, contract=mdl, csvFileRef → IPR-0001 | ready_for_review; dry-run 3 create |
| 02 | \`02-validate-initial.json\` | \`domain_proposal_validate\` | stored report verbatim; \`dryRunAt\` unchanged (no recompute) |
| 03 | \`03-demo-cast-accept.json\` | **demo-cast** owner accept (version + sha256 echo) | accepted |
| 04 | \`04-demo-cast-screen-act.json\` | **demo-cast** owner screen act (intake item raised) | watermark moved |
| 05 | \`05-demo-cast-apply-stale-409.json\` | **demo-cast** owner apply attempt, \`force: false\` | **409 STALE_PROPOSAL** verbatim |
| 06 | \`06a-validate-pre-refresh.json\`, \`06b-refresh-recovery.json\` | agent recovery through the tool surface: validate → \`mode=refresh\` | acceptance voided (RV-13); rebased dry-run |
| 07 | \`07-validate-post-refresh.json\` | \`domain_proposal_validate\` | post-refresh state |
| 08 | \`08a-demo-cast-re-accept.json\`, \`08b-demo-cast-apply.json\` | **demo-cast** owner re-accept + apply, \`force: false\` | applied; apply report captured |
| 09a | \`09a-taxonomy-400-refresh-of-applied.json\` | tool refresh of the applied (terminal) proposal | \`ok:false, errorClass: bad_request\` (engine 400) |
| 09b | \`09b-taxonomy-403-viewer-propose.json\` | tool propose as the non-granted viewer persona | \`ok:false, errorClass: forbidden\` (engine 403; reported verbatim, not retried) |
| 09c | \`09c1-propose-second-ipr0002.json\`, \`09c2-taxonomy-409-version-conflict.json\` | second proposal IPR-0002; tool refresh with stale expectedVersion | \`ok:false, errorClass: version_conflict\` (engine 409) |
| 10 | \`10a-hist-ipr0001.json\`, \`10b-hist-ipr0002.json\` | history extracts | agent-person vs demo-cast-admin attribution on every record |
| 11 | \`11-taxonomy-network-error-after-teardown.json\` | validate after server teardown | \`ok:false, errorClass: network_error\` |

The \`409 STALE_PROPOSAL\` normal-flow surfacing (a P2 requirement) is
unreachable through propose/validate alone — the 409 arises only on
accept/apply — so the demo-cast acts are the minimum needed to evidence the
ruled recovery loop. They change nothing about what is registered: no
accept/apply/force tool exists.

## Demo-cast disclosure (rider 5 / rider 9; one line per owner-role act)

- Step 03 accept — demo-cast as \`${ADMIN_EMAIL}\`; script-side HTTP; no force parameter on accept.
- Step 04 screen act (intake raise) — demo-cast as \`${ADMIN_EMAIL}\`; script-side HTTP.
- Step 05 apply attempt — demo-cast as \`${ADMIN_EMAIL}\`; **force: false**; refused 409 STALE_PROPOSAL.
- Step 08a re-accept — demo-cast as \`${ADMIN_EMAIL}\`; script-side HTTP; no force parameter on accept.
- Step 08b apply — demo-cast as \`${ADMIN_EMAIL}\`; **force: false**; applied.
- Step 10 history extracts — demo-cast read as \`${ADMIN_EMAIL}\` (capture only).

\`force: false\` on every apply act; \`force=true\` never occurred in any form
in this rehearsal, its tests, or its scripts (Receipt 32 exclusion — absolute,
no scratch carve-out; the driver hard-codes \`force: false\` with no override
parameter).

## Deferred live-LLM statement

No \`ANTHROPIC_API_KEY\` existed this session; the live-LLM demonstration of
these tools through a governed harness model session is **deferred** and
remains unclaimed. This pack evidences the transport, handlers, taxonomy, and
actor model only — exposure makes the tools *available*; no working-agent-
bridge, pilot-readiness, or L-level claim is made (K-DOMAIN-4).

## Teardown

Scratch server stopped, then the network_error taxonomy captured against the
dead port (artifact 11); scratch DB \`pec-scratch-bridge.db\` (+\`-wal\`/\`-shm\`)
**deleted after capture**. The D-PEC-01 surfaces and the owner's real
instance were never touched.

## Artifacts (SHA-256)

\`\`\`
${shaLines.join('\n')}
\`\`\`

Mirror artifact (non-authoritative, batch form disclosed):
\`_DomainEngines/proposals/pec/OP_2026-07-06_BRIDGE_rehearsal_IPR-0001-0002.md\`.

## Boundaries respected

Scratch/demo basis only; DB deleted after capture. Accept, apply, and every
owner-role act demo-cast and disclosed; \`force: false\` on every apply. No
accept/apply/force tool registered or reachable; no pec source change; no
real-instance content; no tier-0 act; no publication or release act; every
claim above is reproducible from the transcripts in \`artifacts/\`.
`;
    await writeFile(path.join(evidenceDir, 'MANIFEST.md'), manifest, 'utf8');
    console.log(`[done] evidence pack written to ${evidenceDir}`);
    const remaining = await readdir(scratchDir);
    console.log(`[teardown] scratch dir residue (sessions only expected): ${remaining.join(', ')}`);
  } finally {
    await server.stop().catch(() => undefined);
    deleteScratchDb(dbPath);
    await rm(scratchDir, { recursive: true, force: true });
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
