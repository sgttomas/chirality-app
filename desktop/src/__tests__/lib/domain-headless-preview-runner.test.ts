import { createHash } from "node:crypto";
import {
  chmod,
  mkdir,
  mkdtemp,
  readFile,
  rm,
  symlink,
  writeFile,
} from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { afterAll, afterEach, beforeEach, describe, expect, it } from "vitest";
import {
  HEADLESS_RUNNER_STDERR_LIMIT_BYTES,
  HEADLESS_RUNNER_STDOUT_LIMIT_BYTES,
  OPEN_PIPE_STRESS_RUNNER_PATH_ENV,
  OPEN_PIPE_STRESS_RUNNER_SHA256_ENV,
  type HeadlessRunnerEnvironment,
  runConfiguredHeadlessPreview,
} from "../../lib/harness/mcp/domain-headless-preview-runner";
import {
  buildChiralityMcpTools,
  domainHeadlessPreviewRunTool,
} from "../../lib/harness/mcp/read-tools";
import { replayHarnessEvents } from "../../lib/harness/session-events";

const REQUEST = {
  request: {
    request_id: "request-1",
    operation: "solve",
    operation_ref: { ref_type: "api_operation", ref_id: "solve" },
    project_ref: { ref_type: "project", ref_id: "invented" },
    model_ref: { ref_type: "model", ref_id: "invented" },
    unit_system_ref: { ref_type: "unit_system", ref_id: "si" },
    load_basis_refs: [{ ref_type: "load_case", ref_id: "LC1" }],
    input_manifest_ref: { ref_type: "audit_manifest", ref_id: "manifest" },
    requested_outputs: ["result_envelope"],
    privacy: { local_only: true },
    provenance: { source_name: "invented" },
    professional_boundary: { human_review_required: true },
    tbd_decisions: { process_invocation: "SETTLED_DEC_065" },
  },
  solve: { preview_model: { model: { nodes: [] } } },
};

const PROVENANCE = {
  source_name: "invented app transport fixture",
  source_location: "domain-headless-preview-runner.test.ts",
  source_license: "project invented",
  contributor: "Chirality app-dev tests",
  contributor_certification: "invented non-engineering example",
  redistribution_status: "invented_non_engineering_example",
  review_status: "accepted",
};

const PRIVACY = {
  local_only: true,
  telemetry_allowed: false,
  private_payload_redacted: true,
  classification: "public_metadata",
};

const PROFESSIONAL_BOUNDARY = {
  human_review_required: true,
  software_makes_compliance_claim: false,
  software_makes_certification_claim: false,
  software_makes_sealing_claim: false,
  software_makes_approval_claim: false,
  software_makes_authentication_claim: false,
};

function diagnostic(code = "BLOCKED") {
  return {
    code,
    class: "RUNNER_BLOCKING",
    severity: "blocking",
    source: { ref_type: "headless_runner", ref_id: "DEL-10-05" },
    affected_object: { ref_type: "runner_result", ref_id: "invented-run" },
    message: "invented blocking outcome",
    remediation: "Correct the invented test input.",
    provenance: { ...PROVENANCE },
  };
}

function resultObject(
  input: { blocking?: boolean; padding?: number; resultRefCount?: number } = {},
): Record<string, unknown> {
  const blockingDiagnostics = input.blocking ? [diagnostic()] : [];
  const resultRefCount = input.resultRefCount ?? 1;
  const value: Record<string, unknown> = {
    artifact: "openpipestress.headless_runner_cli_output",
    schema_version: "1.0.0",
    deliverable_id: "DEL-10-05",
    package_id: "PKG-10",
    command: "solve",
    operation: "solve",
    policy: {
      policy_ref: "DEC-065",
      binary: "openpipestress-runner",
      stdout_default: true,
      explicit_output_path_only: true,
      local_foreground_process: true,
      network_allowed: false,
      telemetry_allowed: false,
      daemon_allowed: false,
      hidden_filesystem_mutation_allowed: false,
      direct_sql_access_allowed: false,
    },
    request_validation: { diagnostics: [] },
    result_validation: { diagnostics: [] },
    runner_result: {
      run_id: "run:invented-app-transport",
      job: {
        job_id: "job:invented-app-transport",
        state: input.blocking ? "FAILED" : "COMPLETED",
        current_step: input.blocking ? 1 : 3,
        total_steps: 3,
        cancellation_supported: true,
        cancellation_requested: false,
      },
      analysis_status: [
        "HUMAN_REVIEW_REQUIRED",
        ...(input.blocking ? ["MODEL_INCOMPLETE"] : ["MECHANICS_SOLVED"]),
      ],
      result_envelope_ref: {
        schema_ref: "schemas/results.schema.yaml",
        envelope_ref: {
          ref_type: "result_envelope",
          ref_id: "result-envelope:invented-app-transport",
        },
        compatibility: "schema_first_json_result_envelope",
      },
      result_refs: Array.from({ length: resultRefCount }, (_, index) => ({
        ref_type: "result",
        ref_id: `result:invented:${index}`,
      })),
      audit_manifest_ref: {
        ref_type: "audit_manifest",
        ref_id: "audit-manifest:invented-app-transport",
      },
      checksums: [
        {
          algorithm: "sha256",
          canonicalization: "rfc8785_jcs",
          payload_ref: { ref_type: "runner_request", ref_id: "request-1" },
          value: "0".repeat(64),
        },
        {
          algorithm: "sha256",
          canonicalization: "rfc8785_jcs",
          payload_ref: {
            ref_type: "result_envelope",
            ref_id: "result-envelope:invented-app-transport",
          },
          value: "1".repeat(64),
        },
      ],
      diagnostics: [],
      privacy: { ...PRIVACY },
      provenance: { ...PROVENANCE },
      professional_boundary: { ...PROFESSIONAL_BOUNDARY },
    },
    mechanics_envelope: { artifact: "invented_mechanics_envelope" },
    diagnostics: blockingDiagnostics,
  };
  if (input.padding) {
    value.padding = "x".repeat(input.padding);
  }
  return value;
}

function resultJson(input: Parameters<typeof resultObject>[0] = {}): string {
  return JSON.stringify(resultObject(input));
}

function asRecord(value: unknown): Record<string, unknown> {
  return value as Record<string, unknown>;
}

type ResultSchemaMutation = {
  name: string;
  mutate: (value: Record<string, unknown>) => void;
};

const RESULT_SCHEMA_MUTATIONS: ResultSchemaMutation[] = [
  {
    name: "missing deliverable id",
    mutate: (value) => delete value.deliverable_id,
  },
  {
    name: "incorrect deliverable id",
    mutate: (value) => {
      value.deliverable_id = "DEL-00-00";
    },
  },
  {
    name: "incorrect package id",
    mutate: (value) => {
      value.package_id = "PKG-00";
    },
  },
  {
    name: "incomplete policy",
    mutate: (value) => {
      delete asRecord(value.policy).network_allowed;
    },
  },
  {
    name: "contradictory policy",
    mutate: (value) => {
      asRecord(value.policy).network_allowed = true;
    },
  },
  {
    name: "ill-typed policy value",
    mutate: (value) => {
      asRecord(value.policy).stdout_default = "true";
    },
  },
  {
    name: "extra policy field",
    mutate: (value) => {
      asRecord(value.policy).sidecar_allowed = false;
    },
  },
  {
    name: "missing request validation",
    mutate: (value) => delete value.request_validation,
  },
  {
    name: "ill-typed request diagnostics",
    mutate: (value) => {
      asRecord(value.request_validation).diagnostics = {};
    },
  },
  {
    name: "extra result validation field",
    mutate: (value) => {
      asRecord(value.result_validation).accepted = true;
    },
  },
  {
    name: "missing runner result",
    mutate: (value) => delete value.runner_result,
  },
  {
    name: "incomplete runner result",
    mutate: (value) => {
      delete asRecord(value.runner_result).checksums;
    },
  },
  {
    name: "extra runner result field",
    mutate: (value) => {
      asRecord(value.runner_result).solver_truth = true;
    },
  },
  {
    name: "bad job progress type",
    mutate: (value) => {
      asRecord(asRecord(value.runner_result).job).current_step = "3";
    },
  },
  {
    name: "bad analysis status token",
    mutate: (value) => {
      asRecord(value.runner_result).analysis_status = ["COMPLIANT"];
    },
  },
  {
    name: "bad result reference shape",
    mutate: (value) => {
      asRecord(value.runner_result).result_refs = [{ ref_type: "result" }];
    },
  },
  {
    name: "bad checksum token",
    mutate: (value) => {
      const checksums = asRecord(value.runner_result).checksums as Record<
        string,
        unknown
      >[];
      checksums[0].canonicalization = "ad_hoc";
    },
  },
  {
    name: "only unrelated complete checksums",
    mutate: (value) => {
      const runnerResult = asRecord(value.runner_result);
      runnerResult.checksums = [
        (runnerResult.checksums as Record<string, unknown>[])[0],
      ];
    },
  },
  {
    name: "result-envelope checksum with mismatched reference id",
    mutate: (value) => {
      const checksums = asRecord(value.runner_result).checksums as Record<
        string,
        unknown
      >[];
      asRecord(checksums[1].payload_ref).ref_id =
        "result-envelope:different-result";
    },
  },
  {
    name: "checksum with matching reference id but wrong reference type",
    mutate: (value) => {
      const checksums = asRecord(value.runner_result).checksums as Record<
        string,
        unknown
      >[];
      asRecord(checksums[1].payload_ref).ref_type = "runner_request";
    },
  },
  {
    name: "bad privacy boundary",
    mutate: (value) => {
      asRecord(asRecord(value.runner_result).privacy).telemetry_allowed = true;
    },
  },
  {
    name: "bad professional boundary",
    mutate: (value) => {
      asRecord(
        asRecord(value.runner_result).professional_boundary,
      ).software_makes_compliance_claim = true;
    },
  },
  {
    name: "ill-shaped diagnostic",
    mutate: (value) => {
      value.diagnostics = [
        { code: "BLOCKED", severity: "Blocking", message: "incomplete" },
      ];
    },
  },
  {
    name: "extra top-level padding",
    mutate: (value) => {
      value.padding = "not allowed";
    },
  },
  {
    name: "bad mechanics envelope type",
    mutate: (value) => {
      value.mechanics_envelope = [];
    },
  },
  {
    name: "non-null solve suite result",
    mutate: (value) => {
      value.suite_run = {};
    },
  },
];

function sha256(value: Buffer | string): string {
  return createHash("sha256").update(value).digest("hex");
}

type Fixture = {
  root: string;
  projectRoot: string;
  inputPath: string;
  inputBytes: Buffer;
  sessionRoot: string;
};

let fixture: Fixture;

/**
 * One byte-identical script serves every happy-path test. macOS Gatekeeper
 * scans each never-before-seen executable on first exec (~130-310ms per
 * distinct content hash); by keeping the script content constant and varying
 * only sibling data files, the whole file pays for a single scan instead of
 * one per test. Behavior is driven by data files resolved relative to "$0"
 * (the runner lib scrubs the child environment, so env vars cannot be used):
 *   expected-input-sha256  verify stdin hash instead of draining stdin
 *   require-argv-solve     assert argv is exactly ["solve"] and no ambient env
 *   stdout-payload         bytes to emit on stdout
 *   stderr-payload         bytes to emit on stderr
 *   exit-code              exit status (always written)
 * Tests that need genuinely different script content (timeout, signal,
 * non-executable) still use makeRunner below.
 */
const SHARED_RUNNER_CONTENT = [
  "#!/bin/sh",
  'dir=$(dirname "$0")',
  'if [ -f "$dir/expected-input-sha256" ]; then',
  "  actual=$(/usr/bin/shasum -a 256 | /usr/bin/cut -d ' ' -f 1)",
  '  [ "$actual" = "$(/bin/cat "$dir/expected-input-sha256")" ] || exit 2',
  "else",
  "  /bin/cat >/dev/null",
  "fi",
  'if [ -f "$dir/require-argv-solve" ]; then',
  '  [ "$#" -eq 1 ] || exit 2',
  '  [ "$1" = "solve" ] || exit 2',
  '  [ -z "$TEST_SECRET" ] || exit 2',
  "fi",
  'if [ -f "$dir/stdout-payload" ]; then',
  '  /bin/cat "$dir/stdout-payload"',
  "fi",
  'if [ -f "$dir/stderr-payload" ]; then',
  '  /bin/cat "$dir/stderr-payload" >&2',
  "fi",
  'exit "$(/bin/cat "$dir/exit-code")"',
  "",
].join("\n");

const SHARED_RUNNER_SHA256 = sha256(SHARED_RUNNER_CONTENT);

/**
 * The shared runner script is written exactly once per test-file run (one
 * inode): macOS assesses executables per file, so reusing the same file —
 * not just the same content — is what avoids the per-test scan. Tests run
 * sequentially, so rewriting the sibling data files between invocations is
 * safe; every known data file is rewritten or removed on every call so no
 * state leaks from a previous test.
 */
let sharedRunnerDir: string | undefined;

async function makeSharedRunner(
  input: {
    stdout?: string | Buffer;
    stderr?: Buffer;
    exitCode?: number;
    verifyInput?: boolean;
    requireArgvSolve?: boolean;
  } = {},
): Promise<{ path: string; sha256: string }> {
  if (!sharedRunnerDir) {
    sharedRunnerDir = await mkdtemp(
      path.join(os.tmpdir(), "chirality-shared-headless-runner-"),
    );
    const scriptPath = path.join(sharedRunnerDir, "runner.sh");
    await writeFile(scriptPath, SHARED_RUNNER_CONTENT, "utf8");
    await chmod(scriptPath, 0o700);
  }
  const runnerDir = sharedRunnerDir;
  const runnerPath = path.join(runnerDir, "runner.sh");
  await writeFile(path.join(runnerDir, "exit-code"), `${input.exitCode ?? 0}\n`, "utf8");
  const optionalFiles: Array<[string, string | Buffer | undefined]> = [
    ["stdout-payload", input.stdout],
    ["stderr-payload", input.stderr],
    [
      "expected-input-sha256",
      input.verifyInput ? `${sha256(fixture.inputBytes)}\n` : undefined,
    ],
    ["require-argv-solve", input.requireArgvSolve ? "" : undefined],
  ];
  for (const [name, content] of optionalFiles) {
    const filePath = path.join(runnerDir, name);
    if (content === undefined) {
      await rm(filePath, { force: true });
    } else {
      await writeFile(filePath, content);
    }
  }
  return { path: runnerPath, sha256: SHARED_RUNNER_SHA256 };
}

afterAll(async () => {
  if (sharedRunnerDir) {
    await rm(sharedRunnerDir, { recursive: true, force: true });
    sharedRunnerDir = undefined;
  }
});

async function makeRunner(
  body: string,
  mode = 0o700,
): Promise<{ path: string; sha256: string }> {
  const runnerPath = path.join(
    fixture.root,
    `runner-${createHash("sha1").update(body).digest("hex")}.sh`,
  );
  const content = `#!/bin/sh\n${body}\n`;
  await writeFile(runnerPath, content, "utf8");
  await chmod(runnerPath, mode);
  return { path: runnerPath, sha256: sha256(content) };
}

function runnerEnv(runner: {
  path: string;
  sha256: string;
}): HeadlessRunnerEnvironment {
  return {
    [OPEN_PIPE_STRESS_RUNNER_PATH_ENV]: runner.path,
    [OPEN_PIPE_STRESS_RUNNER_SHA256_ENV]: runner.sha256,
  };
}

async function makeJsonRunner(
  input: {
    result?: string;
    exitCode?: number;
    verifyInput?: boolean;
  } = {},
) {
  return makeSharedRunner({
    stdout: input.result ?? resultJson(),
    exitCode: input.exitCode,
    verifyInput: input.verifyInput,
  });
}

beforeEach(async () => {
  const root = await mkdtemp(
    path.join(os.tmpdir(), "chirality-headless-runner-"),
  );
  const projectRoot = path.join(root, "project");
  const profileDirectory = path.join(projectRoot, "_DomainEngines", "profiles");
  const inputPath = path.join(projectRoot, "runner-input.json");
  const inputBytes = Buffer.from(
    `${JSON.stringify(REQUEST, null, 2)}\n`,
    "utf8",
  );
  const sessionRoot = path.join(root, "sessions");
  await mkdir(profileDirectory, { recursive: true });
  await writeFile(
    path.join(profileDirectory, "open_pipe_stress.yaml"),
    'domain_profile:\n  id: "open_pipe_stress"\n  deterministic_tools:\n    - id: "headless_runner"\n',
    "utf8",
  );
  await writeFile(inputPath, inputBytes);
  process.env.CHIRALITY_SESSION_ROOT = sessionRoot;
  fixture = { root, projectRoot, inputPath, inputBytes, sessionRoot };
});

afterEach(async () => {
  delete process.env.CHIRALITY_SESSION_ROOT;
  delete process.env[OPEN_PIPE_STRESS_RUNNER_PATH_ENV];
  delete process.env[OPEN_PIPE_STRESS_RUNNER_SHA256_ENV];
  await rm(fixture.root, { recursive: true, force: true });
});

describe("configured DEC-065 headless runner transport", () => {
  it("delivers the exact input and accepts a correlated checksum alongside unrelated checksums", async () => {
    const runner = await makeJsonRunner({ verifyInput: true });
    await expect(
      runConfiguredHeadlessPreview({
        requestBytes: fixture.inputBytes,
        env: runnerEnv(runner),
      }),
    ).resolves.toMatchObject({
      exitCode: 0,
      result: { command: "solve", operation: "solve" },
    });
  });

  it("passes argv exactly solve and does not inherit ambient secrets", async () => {
    const runner = await makeSharedRunner({
      stdout: resultJson(),
      requireArgvSolve: true,
    });
    await expect(
      runConfiguredHeadlessPreview({
        requestBytes: fixture.inputBytes,
        env: {
          ...runnerEnv(runner),
          TEST_SECRET: "must-not-cross-child-boundary",
        },
      }),
    ).resolves.toMatchObject({ exitCode: 0 });
  });

  it("preserves exit 1 as a structured blocking outcome using top-level diagnostics", async () => {
    const runner = await makeJsonRunner({
      result: resultJson({ blocking: true }),
      exitCode: 1,
    });
    await expect(
      runConfiguredHeadlessPreview({
        requestBytes: fixture.inputBytes,
        env: runnerEnv(runner),
      }),
    ).resolves.toMatchObject({
      exitCode: 1,
      result: { diagnostics: [{ severity: "blocking" }] },
    });
  });

  it("correlates runner-result diagnostics with exit 1 even when top-level diagnostics are empty", async () => {
    const output = resultObject();
    const runnerResult = asRecord(output.runner_result);
    asRecord(runnerResult.job).state = "FAILED";
    runnerResult.diagnostics = [diagnostic("RUNNER_RESULT_BLOCKED")];
    const runner = await makeJsonRunner({
      result: JSON.stringify(output),
      exitCode: 1,
    });
    await expect(
      runConfiguredHeadlessPreview({
        requestBytes: fixture.inputBytes,
        env: runnerEnv(runner),
      }),
    ).resolves.toMatchObject({ exitCode: 1 });
  });

  it.each(RESULT_SCHEMA_MUTATIONS)(
    "fails closed on schema-invalid result: $name",
    async ({ mutate }) => {
      const output = resultObject();
      mutate(output);
      const runner = await makeJsonRunner({ result: JSON.stringify(output) });
      await expect(
        runConfiguredHeadlessPreview({
          requestBytes: fixture.inputBytes,
          env: runnerEnv(runner),
        }),
      ).rejects.toMatchObject({
        message: "HEADLESS_RUNNER_RESULT_SCHEMA_MISMATCH",
      });
    },
  );

  it("rejects exit/result correlation mismatches after structural validation", async () => {
    const blockingExitZero = await makeJsonRunner({
      result: resultJson({ blocking: true }),
    });
    await expect(
      runConfiguredHeadlessPreview({
        requestBytes: fixture.inputBytes,
        env: runnerEnv(blockingExitZero),
      }),
    ).rejects.toMatchObject({
      message: "HEADLESS_RUNNER_EXIT_RESULT_MISMATCH",
    });

    const cleanExitOne = await makeJsonRunner({
      result: resultJson(),
      exitCode: 1,
    });
    await expect(
      runConfiguredHeadlessPreview({
        requestBytes: fixture.inputBytes,
        env: runnerEnv(cleanExitOne),
      }),
    ).rejects.toMatchObject({
      message: "HEADLESS_RUNNER_EXIT_RESULT_MISMATCH",
    });

    const missingCompletedResult = resultObject();
    missingCompletedResult.runner_result = null;
    missingCompletedResult.result_validation = null;
    missingCompletedResult.mechanics_envelope = null;
    const nullExitZero = await makeJsonRunner({
      result: JSON.stringify(missingCompletedResult),
    });
    await expect(
      runConfiguredHeadlessPreview({
        requestBytes: fixture.inputBytes,
        env: runnerEnv(nullExitZero),
      }),
    ).rejects.toMatchObject({
      message: "HEADLESS_RUNNER_EXIT_RESULT_MISMATCH",
    });
  });

  it.each([
    [{}, "HEADLESS_RUNNER_CONFIG_MISSING"],
    [
      {
        [OPEN_PIPE_STRESS_RUNNER_PATH_ENV]: "relative/runner",
        [OPEN_PIPE_STRESS_RUNNER_SHA256_ENV]: "a".repeat(64),
      },
      "HEADLESS_RUNNER_PATH_NOT_ABSOLUTE",
    ],
    [
      {
        [OPEN_PIPE_STRESS_RUNNER_PATH_ENV]: "/definitely/missing/runner",
        [OPEN_PIPE_STRESS_RUNNER_SHA256_ENV]: "a".repeat(64),
      },
      "HEADLESS_RUNNER_PATH_INVALID",
    ],
    [
      {
        [OPEN_PIPE_STRESS_RUNNER_PATH_ENV]: "/definitely/missing/runner",
        [OPEN_PIPE_STRESS_RUNNER_SHA256_ENV]: "A".repeat(64),
      },
      "HEADLESS_RUNNER_SHA256_INVALID",
    ],
  ])("refuses invalid local configuration %#", async (env, code) => {
    await expect(
      runConfiguredHeadlessPreview({ requestBytes: fixture.inputBytes, env }),
    ).rejects.toMatchObject({ message: code });
  });

  it("refuses hash mismatch, non-regular, and non-executable targets", async () => {
    const runner = await makeJsonRunner();
    await expect(
      runConfiguredHeadlessPreview({
        requestBytes: fixture.inputBytes,
        env: {
          ...runnerEnv(runner),
          [OPEN_PIPE_STRESS_RUNNER_SHA256_ENV]: "0".repeat(64),
        },
      }),
    ).rejects.toMatchObject({ message: "HEADLESS_RUNNER_SHA256_MISMATCH" });

    await expect(
      runConfiguredHeadlessPreview({
        requestBytes: fixture.inputBytes,
        env: {
          [OPEN_PIPE_STRESS_RUNNER_PATH_ENV]: fixture.projectRoot,
          [OPEN_PIPE_STRESS_RUNNER_SHA256_ENV]: "0".repeat(64),
        },
      }),
    ).rejects.toMatchObject({ message: "HEADLESS_RUNNER_NOT_REGULAR_FILE" });

    const nonExecutable = await makeRunner("/bin/cat >/dev/null", 0o600);
    await expect(
      runConfiguredHeadlessPreview({
        requestBytes: fixture.inputBytes,
        env: runnerEnv(nonExecutable),
      }),
    ).rejects.toMatchObject({ message: "HEADLESS_RUNNER_NOT_EXECUTABLE" });
  });

  it("times out and independently caps stdout and stderr", async () => {
    const timeoutRunner = await makeRunner("/bin/sleep 2");
    await expect(
      runConfiguredHeadlessPreview({
        requestBytes: fixture.inputBytes,
        env: runnerEnv(timeoutRunner),
        timeoutMs: 30,
      }),
    ).rejects.toMatchObject({ message: "HEADLESS_RUNNER_TIMEOUT" });

    const stdoutRunner = await makeSharedRunner({
      stdout: Buffer.alloc(HEADLESS_RUNNER_STDOUT_LIMIT_BYTES + 1, "x"),
    });
    await expect(
      runConfiguredHeadlessPreview({
        requestBytes: fixture.inputBytes,
        env: runnerEnv(stdoutRunner),
      }),
    ).rejects.toMatchObject({ message: "HEADLESS_RUNNER_STDOUT_OVERSIZE" });

    const stderrRunner = await makeSharedRunner({
      stderr: Buffer.alloc(HEADLESS_RUNNER_STDERR_LIMIT_BYTES + 1, "x"),
    });
    await expect(
      runConfiguredHeadlessPreview({
        requestBytes: fixture.inputBytes,
        env: runnerEnv(stderrRunner),
      }),
    ).rejects.toMatchObject({ message: "HEADLESS_RUNNER_STDERR_OVERSIZE" });
  });

  it("maps exit 2, unsupported exits, signals, and result schema mismatch to stable refusals", async () => {
    const exit2 = await makeSharedRunner({ exitCode: 2 });
    await expect(
      runConfiguredHeadlessPreview({
        requestBytes: fixture.inputBytes,
        env: runnerEnv(exit2),
      }),
    ).rejects.toMatchObject({ message: "HEADLESS_RUNNER_INPUT_REFUSED" });

    const unsupported = await makeSharedRunner({ exitCode: 9 });
    await expect(
      runConfiguredHeadlessPreview({
        requestBytes: fixture.inputBytes,
        env: runnerEnv(unsupported),
      }),
    ).rejects.toMatchObject({ message: "HEADLESS_RUNNER_EXIT_UNSUPPORTED" });

    const signalled = await makeRunner(
      "/bin/cat >/dev/null\n/bin/kill -TERM $$",
    );
    await expect(
      runConfiguredHeadlessPreview({
        requestBytes: fixture.inputBytes,
        env: runnerEnv(signalled),
      }),
    ).rejects.toMatchObject({ message: "HEADLESS_RUNNER_SIGNALLED" });

    const mismatch = await makeJsonRunner({
      result: JSON.stringify({ command: "solve" }),
    });
    await expect(
      runConfiguredHeadlessPreview({
        requestBytes: fixture.inputBytes,
        env: runnerEnv(mismatch),
      }),
    ).rejects.toMatchObject({
      message: "HEADLESS_RUNNER_RESULT_SCHEMA_MISMATCH",
    });
  });

  it.each(["not-json", "{}{}"])(
    "rejects invalid or non-single stdout JSON",
    async (stdout) => {
      const runner = await makeJsonRunner({ result: stdout });
      await expect(
        runConfiguredHeadlessPreview({
          requestBytes: fixture.inputBytes,
          env: runnerEnv(runner),
        }),
      ).rejects.toMatchObject({
        message: "HEADLESS_RUNNER_RESULT_JSON_INVALID",
      });
    },
  );

  it("rejects incomplete preview fragments before spawning", async () => {
    const runner = await makeJsonRunner();
    await expect(
      runConfiguredHeadlessPreview({
        requestBytes: Buffer.from(JSON.stringify({ preview_model: {} })),
        env: runnerEnv(runner),
      }),
    ).rejects.toMatchObject({
      message: "HEADLESS_RUNNER_INPUT_SCHEMA_MISMATCH",
    });
  });
});

describe("live domain_headless_preview_run MCP handler", () => {
  async function configureRunner(
    input: Parameters<typeof makeJsonRunner>[0] = {},
  ) {
    const runner = await makeJsonRunner(input);
    process.env[OPEN_PIPE_STRESS_RUNNER_PATH_ENV] = runner.path;
    process.env[OPEN_PIPE_STRESS_RUNNER_SHA256_ENV] = runner.sha256;
    return runner;
  }

  const context = () => ({
    projectRoot: fixture.projectRoot,
    sessionId: "sess-headless-preview",
    mode: "readOnly",
  });

  it("uses the read permission/event/redaction/result pipeline and marks exit 1 non-successful", async () => {
    await configureRunner({
      result: resultJson({ blocking: true }),
      exitCode: 1,
    });
    const result = await domainHeadlessPreviewRunTool(context(), {
      profileId: "open_pipe_stress",
      runnerInputRef: "runner-input.json",
    });
    expect(result.isError).toBe(true);
    const replay = await replayHarnessEvents("sess-headless-preview");
    expect(replay.events.map((event) => event.type)).toEqual([
      "tool.started",
      "tool.permission",
      "tool.completed",
    ]);
    expect(replay.events[1].data).toMatchObject({
      behavior: "allow",
      toolName: "mcp__chirality__domain_headless_preview_run",
      pathScope: "project-root-read",
    });
    expect(JSON.stringify(replay.events)).not.toContain(
      process.env[OPEN_PIPE_STRESS_RUNNER_PATH_ENV],
    );
  });

  it("persists oversized results through the normal redacted artifact pipeline", async () => {
    await configureRunner({ result: resultJson({ resultRefCount: 2_000 }) });
    await domainHeadlessPreviewRunTool(context(), {
      profileId: "open_pipe_stress",
      runnerInputRef: "runner-input.json",
    });
    const replay = await replayHarnessEvents("sess-headless-preview");
    const completed = replay.events.at(-1);
    expect(completed?.type).toBe("tool.completed");
    expect(completed?.data).toMatchObject({
      resultMetadata: {
        budgetClass: "requires-artifact-overflow",
        outputPersisted: true,
      },
      artifactMetadata: { redacted: true, retentionPolicy: "session-lifetime" },
    });
  });

  it.each([
    ["pec", "HEADLESS_RUNNER_PROFILE_REFUSED"],
    ["unknown", "HEADLESS_RUNNER_PROFILE_REFUSED"],
    ["", "HEADLESS_RUNNER_PROFILE_REFUSED"],
  ])("refuses profileId %j", async (profileId, errorCode) => {
    await configureRunner();
    await expect(
      domainHeadlessPreviewRunTool(context(), {
        profileId,
        runnerInputRef: "runner-input.json",
      }),
    ).rejects.toMatchObject({ details: { errorCode } });
  });

  it("requires the live registry profile marker and headless_runner declaration", async () => {
    await configureRunner();
    await writeFile(
      path.join(
        fixture.projectRoot,
        "_DomainEngines",
        "profiles",
        "open_pipe_stress.yaml",
      ),
      'domain_profile:\n  id: "open_pipe_stress"\n  deterministic_tools: []\n',
      "utf8",
    );
    await expect(
      domainHeadlessPreviewRunTool(context(), {
        profileId: "open_pipe_stress",
        runnerInputRef: "runner-input.json",
      }),
    ).rejects.toMatchObject({
      message: "profileId does not expose the requested deterministic tool",
    });

    await writeFile(
      path.join(
        fixture.projectRoot,
        "_DomainEngines",
        "profiles",
        "open_pipe_stress.yaml",
      ),
      'domain_profile:\n  id: "pec"\n  deterministic_tools:\n    - id: "headless_runner"\n',
      "utf8",
    );
    await expect(
      domainHeadlessPreviewRunTool(context(), {
        profileId: "open_pipe_stress",
        runnerInputRef: "runner-input.json",
      }),
    ).rejects.toMatchObject({
      message: "profile file does not match the registered profileId",
    });
  });

  it("refuses missing, outside, symlink, and non-file runnerInputRef values", async () => {
    await configureRunner();
    const outsidePath = path.join(fixture.root, "outside.json");
    await writeFile(outsidePath, fixture.inputBytes);
    const symlinkPath = path.join(fixture.projectRoot, "linked-input.json");
    await symlink(outsidePath, symlinkPath);

    for (const runnerInputRef of [
      "missing.json",
      outsidePath,
      "linked-input.json",
      "_DomainEngines",
    ]) {
      await expect(
        domainHeadlessPreviewRunTool(context(), {
          profileId: "open_pipe_stress",
          runnerInputRef,
        }),
      ).rejects.toMatchObject({ type: "INVALID_REQUEST" });
    }
  });

  it("refuses an omitted runnerInputRef before permission or process execution", async () => {
    await configureRunner();
    await expect(
      domainHeadlessPreviewRunTool(context(), {
        profileId: "open_pipe_stress",
      } as never),
    ).rejects.toMatchObject({
      message: "runnerInputRef is required",
      details: { errorCode: "HEADLESS_RUNNER_INPUT_REF_MISSING" },
    });
  });

  it("registers only the read-only exclusive open_pipe_stress handler", () => {
    const definitions = buildChiralityMcpTools({
      context: context(),
      allowedToolNames: ["mcp__chirality__domain_headless_preview_run"],
    });
    expect(
      definitions.map((definition) => (definition as { name: string }).name),
    ).toEqual(["domain_headless_preview_run"]);
  });

  it("does not alter the exact runnerInputRef bytes", async () => {
    await configureRunner({ verifyInput: true });
    const before = await readFile(fixture.inputPath);
    const result = await domainHeadlessPreviewRunTool(context(), {
      profileId: "open_pipe_stress",
      runnerInputRef: "runner-input.json",
    });
    expect(result.isError).not.toBe(true);
    await expect(readFile(fixture.inputPath)).resolves.toEqual(before);
  });
});
