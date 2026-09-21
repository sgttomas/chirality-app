import { mkdtemp, mkdir, rm, stat, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { serializeDependencyRegister } from '../../lib/dependencies/register-writer';
import type { DependencyRegisterRow } from '../../lib/dependencies/schema';
import {
  createChiralityReadMcpServers,
  dependenciesReadTool,
  domainCompletenessCheckTool,
  domainRuleCheckRunTool,
  scaffoldPreviewTool,
  scopeScanTool,
  statusReadTool
} from '../../lib/harness/mcp/read-tools';
import { replayHarnessEvents } from '../../lib/harness/session-events';

const STATUS_DOCUMENT = `# Status: DEL-05-03 Lifecycle State Handling

**Current State:** INITIALIZED
**Last Updated:** 2026-02-22

## History
- 2026-02-21 - State set to OPEN (PREPARATION)
- 2026-02-22 - State set to INITIALIZED (4_DOCUMENTS)
`;

const DECOMPOSITION_DOCUMENT = `# Example System - Software Decomposition

## Packages

| PackageID | Package Name | Description |
|---|---|---|
| PKG-05 | Filesystem Execution Model | Runtime filesystem |

## Deliverables

### PKG-05 - Filesystem Execution Model

| DeliverableID | Name | Type |
|---|---|---|
| DEL-05-03 | Lifecycle State Handling | RUNTIME |
`;

// Vendored verbatim byte strings of the load-bearing regions of the REAL
// _DomainEngines/profiles/open_pipe_stress.yaml — quoted YAML ids, exactly as
// the live file writes them (D-APP-51 V-9 regression basis; the pre-D-APP-51
// unquoted fixture masked a marker check that never matched the live bytes).
const DOMAIN_PROFILE = `domain_profile:
  schema_version: "1.0"          # contract schema version (generic)
  id: "open_pipe_stress"
  deterministic_tools:
    - id: "completeness_checker"
      impl: "projects/chirality-piping/core/rules/completeness_checker (Rust)"
      mode: "read_only"
    - id: "rule_check_runner"
      impl: "projects/chirality-piping/core/rules/rule_check_runner (Rust)"
      mode: "read_only"
`;

// Vendored verbatim byte strings of the load-bearing region of the REAL
// _DomainEngines/profiles/pec.yaml (quoted id; declares NO completeness_checker
// or rule_check_runner deterministic tools — the D-APP-51 disclosure basis).
const PEC_DOMAIN_PROFILE = `domain_profile:
  schema_version: "1.0"
  id: "pec"
  deterministic_tools:
    - id: "pilot_drill"
      impl: "projects/pec/tools/pilot-drill.ts via npm run drill"
      mode: "read_only"
`;

type FixtureContext = {
  tmpRoot: string;
  projectRoot: string;
  deliverablePath: string;
  decompositionPath: string;
  domainInputPath: string;
  rulePackPath: string;
  valueBindingsPath: string;
};

let fixture: FixtureContext;
const sessionId = 'sess_chirality_read_mcp';

function makeDependencyRow(): DependencyRegisterRow {
  return {
    RegisterSchemaVersion: 'v3.1',
    DependencyID: 'DEP-05-03-001',
    FromPackageID: 'PKG-05',
    FromDeliverableID: 'DEL-05-03',
    FromDeliverableName: 'Lifecycle State Handling',
    DependencyClass: 'EXECUTION',
    AnchorType: 'NOT_APPLICABLE',
    Direction: 'UPSTREAM',
    DependencyType: 'PREREQUISITE',
    TargetType: 'DELIVERABLE',
    TargetPackageID: 'PKG-05',
    TargetDeliverableID: 'DEL-05-02',
    TargetRefID: '',
    TargetName: 'Execution Root Scaffolding',
    TargetLocation: '',
    Statement: 'Requires scaffolding baseline before lifecycle transitions',
    EvidenceFile: 'Specification.md',
    SourceRef: 'Specification.md#REQ-01',
    EvidenceQuote: 'Ensure lifecycle is represented by _STATUS.md.',
    Explicitness: 'EXPLICIT',
    RequiredMaturity: 'IN_PROGRESS',
    ProposedMaturity: 'IN_PROGRESS',
    SatisfactionStatus: 'PENDING',
    Confidence: 'HIGH',
    Origin: 'EXTRACTED',
    FirstSeen: '2026-02-22',
    LastSeen: '2026-02-22',
    Status: 'ACTIVE',
    Notes: ''
  };
}

function parseJsonToolResult<T>(result: Awaited<ReturnType<typeof statusReadTool>>): T {
  const first = result.content[0];
  if (!first || first.type !== 'text') {
    throw new Error('Expected text MCP result');
  }
  return JSON.parse(first.text) as T;
}

beforeEach(async () => {
  const tmpRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-read-mcp-'));
  const projectRoot = path.join(tmpRoot, 'project-root');
  const deliverablePath = path.join(
    projectRoot,
    'PKG-05_Filesystem_Execution_Model',
    '1_Working',
    'DEL-05-03_Lifecycle_State_Handling'
  );
  const decompositionDirectory = path.join(projectRoot, '_Decomposition');
  const decompositionPath = path.join(decompositionDirectory, 'decomposition.md');
  const profileDirectory = path.join(projectRoot, '_DomainEngines', 'profiles');
  const domainInputPath = path.join(projectRoot, 'domain-input.json');
  const rulePackPath = path.join(projectRoot, 'rule-pack.json');
  const valueBindingsPath = path.join(projectRoot, 'value-bindings.json');

  await mkdir(deliverablePath, { recursive: true });
  await mkdir(decompositionDirectory, { recursive: true });
  await mkdir(profileDirectory, { recursive: true });
  await writeFile(path.join(deliverablePath, '_STATUS.md'), STATUS_DOCUMENT, 'utf8');
  await writeFile(
    path.join(deliverablePath, 'Dependencies.csv'),
    serializeDependencyRegister([makeDependencyRow()], { hostDeliverableId: 'DEL-05-03' }).csv,
    'utf8'
  );
  await writeFile(decompositionPath, DECOMPOSITION_DOCUMENT, 'utf8');
  await writeFile(path.join(profileDirectory, 'open_pipe_stress.yaml'), DOMAIN_PROFILE, 'utf8');
  await writeFile(path.join(profileDirectory, 'pec.yaml'), PEC_DOMAIN_PROFILE, 'utf8');
  await writeFile(domainInputPath, JSON.stringify({ nodes: [], edges: [] }), 'utf8');
  await writeFile(
    rulePackPath,
    JSON.stringify({ grammar_version: 'test', rules: [] }),
    'utf8'
  );
  await writeFile(
    valueBindingsPath,
    JSON.stringify({ supplied_values: {}, solver_results: {} }),
    'utf8'
  );

  fixture = {
    tmpRoot,
    projectRoot,
    deliverablePath,
    decompositionPath,
    domainInputPath,
    rulePackPath,
    valueBindingsPath
  };
  process.env.CHIRALITY_SESSION_ROOT = path.join(tmpRoot, 'sessions');
});

afterEach(async () => {
  delete process.env.CHIRALITY_SESSION_ROOT;
  await rm(fixture.tmpRoot, { recursive: true, force: true });
});

describe('Chirality read MCP tools', () => {
  it('reads parsed lifecycle status and dependency register output', async () => {
    const context = { projectRoot: fixture.projectRoot, sessionId };
    const statusResult = parseJsonToolResult<{
      status: { currentState: string };
      statusFilePath: string;
    }>(
      await statusReadTool(context, {
        deliverablePath: fixture.deliverablePath
      })
    );
    const dependencyResult = parseJsonToolResult<{
      rows: Array<{ DependencyID: string; SatisfactionStatus: string }>;
      warnings: string[];
    }>(
      await dependenciesReadTool(context, {
        deliverablePath: fixture.deliverablePath
      })
    );

    expect(statusResult.status.currentState).toBe('INITIALIZED');
    expect(statusResult.statusFilePath.endsWith('DEL-05-03_Lifecycle_State_Handling/_STATUS.md')).toBe(
      true
    );
    expect(dependencyResult.rows).toHaveLength(1);
    expect(dependencyResult.rows[0]).toMatchObject({
      DependencyID: 'DEP-05-03-001',
      SatisfactionStatus: 'PENDING'
    });
    expect(dependencyResult.warnings).toEqual([]);

    const replay = await replayHarnessEvents(sessionId);
    expect(replay.events.map((event) => event.type)).toEqual([
      'tool.started',
      'tool.completed',
      'tool.started',
      'tool.completed'
    ]);
    expect(replay.events[0].data).toMatchObject({
      source: 'chirality-mcp',
      toolName: 'status_read',
      adapterToolName: 'mcp__chirality__status_read',
      inputMetadata: {
        inputKeys: ['deliverablePath'],
        pathFields: {
          deliverablePath: fixture.deliverablePath
        }
      }
    });
    expect(replay.events[1].data.resultMetadata).toMatchObject({
      contentItemCount: 1,
      contentTextByteLength: expect.any(Number),
      inlineByteLimit: 65536,
      artifactByteLimit: 2097152,
      overflowPolicy: 'artifact',
      budgetClass: 'within-inline-budget',
      rawOutputPersisted: false
    });
    expect(JSON.stringify(replay.events[1].data)).not.toContain('INITIALIZED');
    expect(JSON.stringify(replay.events[3].data)).not.toContain('DEP-05-03-001');
  });

  it('scans project scopes without reading document bodies', async () => {
    const result = parseJsonToolResult<{
      projectRoot: string;
      deliverables: Array<{ id: string; path: string }>;
      knowledgeTypes: unknown[];
    }>(await scopeScanTool({ projectRoot: fixture.projectRoot, sessionId }));

    expect(result.projectRoot).toBe(fixture.projectRoot);
    expect(result.deliverables).toEqual([
      expect.objectContaining({
        id: 'DEL-05-03',
        path: fixture.deliverablePath
      })
    ]);
  });

  it('previews scaffold paths without creating execution-root files', async () => {
    const executionRoot = path.join(fixture.projectRoot, 'execution-preview');
    const result = parseJsonToolResult<{
      executionRoot: string;
      packageCount: number;
      planned: { files: string[] };
    }>(
      await scaffoldPreviewTool(
        { projectRoot: fixture.projectRoot, sessionId },
        {
          executionRoot,
          decompositionPath: fixture.decompositionPath
        }
      )
    );

    expect(result.executionRoot).toBe(executionRoot);
    expect(result.packageCount).toBe(1);
    expect(result.planned.files).toContain(path.join(executionRoot, 'INIT.md'));
    await expect(stat(executionRoot)).rejects.toMatchObject({ code: 'ENOENT' });
  });

  it('returns D-APP-50 read-side domain transport evidence without domain verdicts', async () => {
    const context = { projectRoot: fixture.projectRoot, sessionId };
    const completeness = parseJsonToolResult<{
      profileId: string;
      toolId: string;
      transportStatus: {
        status: string;
        deterministicToolExecution: string;
        resultSemantics: string;
      };
      inputs: Array<{ field: string; relativePath: string; sha256: string; json: unknown }>;
    }>(
      await domainCompletenessCheckTool(context, {
        profileId: 'open_pipe_stress',
        inputRef: path.relative(fixture.projectRoot, fixture.domainInputPath)
      })
    );
    const ruleRun = parseJsonToolResult<{
      profileId: string;
      toolId: string;
      transportStatus: {
        status: string;
        deterministicToolExecution: string;
      };
      inputs: Array<{ field: string; relativePath: string; sha256: string }>;
    }>(
      await domainRuleCheckRunTool(context, {
        profileId: 'open_pipe_stress',
        rulePackRef: path.relative(fixture.projectRoot, fixture.rulePackPath),
        valueBindingsRef: path.relative(fixture.projectRoot, fixture.valueBindingsPath)
      })
    );

    expect(completeness).toMatchObject({
      profileId: 'open_pipe_stress',
      toolId: 'completeness_checker',
      transportStatus: {
        status: 'live',
        deterministicToolExecution: expect.stringContaining('not invoked'),
        resultSemantics: expect.stringContaining('no domain verdict')
      }
    });
    // D-APP-51 V-9 regression pin: the preserved open_pipe_stress envelope
    // strings byte-match the pre-registry values, and the additive registry
    // fields carry the ruled open_pipe_stress entry.
    expect(completeness.transportStatus).toMatchObject({
      posture: 'DEC-041 in-process read transport',
      tranche: 'D-APP-50 tranche-1 read-side exposure',
      toolId: 'completeness_checker',
      writes: false,
      network: false,
      shell: false,
      engineKind: 'deterministic-cli',
      readTransportBinding: 'in-process-read-evidence',
      declaredDeterministicToolId: 'completeness_checker',
      inputContract:
        'project-root-contained JSON references plus _DomainEngines/profiles/open_pipe_stress.yaml',
      deterministicToolExecution:
        'not invoked in this tranche; the authoritative Rust tool is library-only and has no stable JSON CLI transport',
      resultSemantics:
        'transport/evidence envelope only; no domain verdict, no live binding claim, and no professional engineering conclusion'
    });
    expect(completeness.inputs).toEqual([
      expect.objectContaining({
        field: 'inputRef',
        relativePath: 'domain-input.json',
        sha256: expect.any(String),
        json: expect.objectContaining({ topLevelType: 'object' })
      })
    ]);
    expect(ruleRun).toMatchObject({
      profileId: 'open_pipe_stress',
      toolId: 'rule_check_runner',
      transportStatus: {
        status: 'live',
        toolId: 'rule_check_runner',
        tranche: 'D-APP-50 tranche-1 read-side exposure',
        engineKind: 'deterministic-cli',
        readTransportBinding: 'in-process-read-evidence',
        declaredDeterministicToolId: 'rule_check_runner',
        deterministicToolExecution: expect.stringContaining('not invoked'),
        resultSemantics:
          'transport/evidence envelope only; no domain verdict, no live binding claim, and no professional engineering conclusion'
      }
    });
    expect(ruleRun.inputs.map((input) => input.field)).toEqual([
      'rulePackRef',
      'valueBindingsRef'
    ]);
  });

  it('refuses unregistered profileIds on both domain read tools with the enumerated registry', async () => {
    const context = { projectRoot: fixture.projectRoot, sessionId };
    const expectedRefusal = {
      type: 'INVALID_REQUEST',
      status: 400,
      message: 'profileId is not registered for this domain transport',
      details: {
        profileId: 'nope',
        supportedProfileIds: ['open_pipe_stress', 'pec']
      }
    };

    await expect(
      domainCompletenessCheckTool(context, {
        profileId: 'nope',
        inputRef: path.relative(fixture.projectRoot, fixture.domainInputPath)
      })
    ).rejects.toMatchObject(expectedRefusal);
    await expect(
      domainRuleCheckRunTool(context, {
        profileId: 'nope',
        rulePackRef: path.relative(fixture.projectRoot, fixture.rulePackPath),
        valueBindingsRef: path.relative(fixture.projectRoot, fixture.valueBindingsPath)
      })
    ).rejects.toMatchObject(expectedRefusal);
  });

  it('returns D-APP-51 pec read-side evidence with the declared-null deterministic tool disclosure', async () => {
    const context = { projectRoot: fixture.projectRoot, sessionId };
    const completeness = parseJsonToolResult<{
      profileId: string;
      toolId: string;
      transportStatus: Record<string, unknown>;
      profile: { relativePath: string; sha256: string };
      inputs: Array<{ field: string }>;
    }>(
      await domainCompletenessCheckTool(context, {
        profileId: 'pec',
        inputRef: path.relative(fixture.projectRoot, fixture.domainInputPath)
      })
    );
    const ruleRun = parseJsonToolResult<{
      profileId: string;
      toolId: string;
      transportStatus: Record<string, unknown>;
      inputs: Array<{ field: string }>;
    }>(
      await domainRuleCheckRunTool(context, {
        profileId: 'pec',
        rulePackRef: path.relative(fixture.projectRoot, fixture.rulePackPath),
        valueBindingsRef: path.relative(fixture.projectRoot, fixture.valueBindingsPath)
      })
    );

    for (const [result, toolId] of [
      [completeness, 'completeness_checker'],
      [ruleRun, 'rule_check_runner']
    ] as const) {
      expect(result).toMatchObject({
        profileId: 'pec',
        toolId,
        transportStatus: {
          status: 'live',
          posture: 'DEC-041 in-process read transport',
          tranche: 'D-APP-51 P1 multi-engine registry read exposure',
          toolId,
          writes: false,
          network: false,
          shell: false,
          engineKind: 'http-api',
          readTransportBinding: 'in-process-read-evidence',
          declaredDeterministicToolId: null,
          inputContract:
            'project-root-contained JSON references plus _DomainEngines/profiles/pec.yaml',
          deterministicToolExecution: expect.stringContaining('declares no completeness_checker'),
          resultSemantics: expect.stringContaining('no domain verdict')
        }
      });
      expect(result.transportStatus.deterministicToolExecution).toContain(
        'no HTTP transport exists'
      );
    }
    expect(completeness.profile.relativePath).toBe(
      path.join('_DomainEngines', 'profiles', 'pec.yaml')
    );
    expect(completeness.inputs.map((input) => input.field)).toEqual(['inputRef']);
    expect(ruleRun.inputs.map((input) => input.field)).toEqual([
      'rulePackRef',
      'valueBindingsRef'
    ]);
  });

  it('refuses profile files that fail the registered marker checks', async () => {
    const context = { projectRoot: fixture.projectRoot, sessionId };
    const profileDirectory = path.join(fixture.projectRoot, '_DomainEngines', 'profiles');

    // (a) identity-marker mismatch: pec.yaml without its registered id bytes.
    await writeFile(
      path.join(profileDirectory, 'pec.yaml'),
      PEC_DOMAIN_PROFILE.replace('id: "pec"', 'id: "not_pec"'),
      'utf8'
    );
    await expect(
      domainCompletenessCheckTool(context, {
        profileId: 'pec',
        inputRef: path.relative(fixture.projectRoot, fixture.domainInputPath)
      })
    ).rejects.toMatchObject({
      type: 'INVALID_REQUEST',
      status: 400,
      message: 'profile file does not match the registered profileId',
      details: {
        profileId: 'pec',
        profilePath: expect.stringContaining('pec.yaml')
      }
    });

    // (b) per-tool marker mismatch: open_pipe_stress.yaml without the
    // rule_check_runner declaration refuses rule_check_run while
    // completeness_check still passes.
    await writeFile(
      path.join(profileDirectory, 'open_pipe_stress.yaml'),
      DOMAIN_PROFILE.replace('    - id: "rule_check_runner"\n', '    - id: "something_else"\n'),
      'utf8'
    );
    await expect(
      domainRuleCheckRunTool(context, {
        profileId: 'open_pipe_stress',
        rulePackRef: path.relative(fixture.projectRoot, fixture.rulePackPath),
        valueBindingsRef: path.relative(fixture.projectRoot, fixture.valueBindingsPath)
      })
    ).rejects.toMatchObject({
      type: 'INVALID_REQUEST',
      status: 400,
      message: 'profileId does not expose the requested deterministic tool',
      details: {
        profileId: 'open_pipe_stress',
        toolId: 'rule_check_runner',
        profilePath: expect.stringContaining('open_pipe_stress.yaml')
      }
    });
    const completeness = parseJsonToolResult<{ profileId: string; toolId: string }>(
      await domainCompletenessCheckTool(context, {
        profileId: 'open_pipe_stress',
        inputRef: path.relative(fixture.projectRoot, fixture.domainInputPath)
      })
    );
    expect(completeness).toMatchObject({
      profileId: 'open_pipe_stress',
      toolId: 'completeness_checker'
    });
  });

  it('rejects pec input references outside the active project root with failure evidence', async () => {
    const outsideInputPath = path.join(fixture.tmpRoot, 'outside-input.json');
    await writeFile(outsideInputPath, JSON.stringify({ nodes: [] }), 'utf8');

    await expect(
      domainCompletenessCheckTool(
        { projectRoot: fixture.projectRoot, sessionId },
        {
          profileId: 'pec',
          inputRef: outsideInputPath
        }
      )
    ).rejects.toMatchObject({
      type: 'INVALID_REQUEST',
      message: expect.stringContaining('inputRef must resolve inside projectRoot')
    });

    const replay = await replayHarnessEvents(sessionId);
    expect(replay.events.map((event) => event.type)).toEqual(['tool.started', 'tool.failed']);
    expect(replay.events[1].data).toMatchObject({
      source: 'chirality-mcp',
      toolName: 'domain_completeness_check',
      adapterToolName: 'mcp__chirality__domain_completeness_check',
      failureSource: 'handler',
      error: {
        errorName: 'HarnessError',
        message: expect.stringContaining('inputRef must resolve inside projectRoot')
      }
    });
  });

  it('rejects scaffold preview paths outside the active project root', async () => {
    await expect(
      scaffoldPreviewTool(
        { projectRoot: fixture.projectRoot, sessionId },
        {
          executionRoot: path.join(fixture.tmpRoot, 'outside-project'),
          decompositionPath: fixture.decompositionPath
        }
      )
    ).rejects.toMatchObject({
      type: 'INVALID_REQUEST',
      message: expect.stringContaining('executionRoot must resolve inside projectRoot')
    });

    const replay = await replayHarnessEvents(sessionId);
    expect(replay.events.map((event) => event.type)).toEqual(['tool.started', 'tool.failed']);
    expect(replay.events[1].data).toMatchObject({
      source: 'chirality-mcp',
      toolName: 'scaffold_preview',
      adapterToolName: 'mcp__chirality__scaffold_preview',
      failureSource: 'handler',
      error: {
        errorName: 'HarnessError',
        message: expect.stringContaining('executionRoot must resolve inside projectRoot')
      }
    });
  });

  it('attaches the SDK MCP server only when a read MCP tool is explicitly allowed', () => {
    expect(
      createChiralityReadMcpServers({
        context: { projectRoot: fixture.projectRoot, sessionId },
        allowedToolNames: []
      })
    ).toEqual({});

    expect(
      createChiralityReadMcpServers({
        context: { projectRoot: fixture.projectRoot, sessionId },
        allowedToolNames: ['mcp__chirality__status_read']
      })
    ).toMatchObject({
      chirality: {
        type: 'sdk',
        name: 'chirality'
      }
    });

    expect(
      createChiralityReadMcpServers({
        context: { projectRoot: fixture.projectRoot, sessionId },
        allowedToolNames: ['mcp__chirality__domain_completeness_check']
      })
    ).toMatchObject({
      chirality: {
        type: 'sdk',
        name: 'chirality'
      }
    });

    // D-APP-52: the live pec proposal tool names attach the server too.
    expect(
      createChiralityReadMcpServers({
        context: { projectRoot: fixture.projectRoot, sessionId },
        allowedToolNames: ['mcp__chirality__domain_proposal_validate']
      })
    ).toMatchObject({
      chirality: {
        type: 'sdk',
        name: 'chirality'
      }
    });
  });
});
