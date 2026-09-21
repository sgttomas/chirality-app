import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { constants as fsConstants } from "node:fs";
import { access, readFile, realpath, stat } from "node:fs/promises";
import path from "node:path";
import { HarnessError } from "@chirality/runtime-contracts/errors";

export const OPEN_PIPE_STRESS_RUNNER_PATH_ENV =
  "CHIRALITY_OPEN_PIPE_STRESS_RUNNER_PATH";
export const OPEN_PIPE_STRESS_RUNNER_SHA256_ENV =
  "CHIRALITY_OPEN_PIPE_STRESS_RUNNER_SHA256";

export const HEADLESS_RUNNER_TIMEOUT_MS = 30_000;
export const HEADLESS_RUNNER_STDOUT_LIMIT_BYTES = 2 * 1024 * 1024;
export const HEADLESS_RUNNER_STDERR_LIMIT_BYTES = 2 * 1024 * 1024;

type RunnerExit = {
  exitCode: 0 | 1;
  result: Record<string, unknown>;
};

export type HeadlessRunnerEnvironment = Readonly<
  Record<string, string | undefined>
>;

function fail(
  code: string,
  status = 400,
  details: Record<string, unknown> = {},
): never {
  throw new HarnessError("INVALID_REQUEST", status, code, {
    errorCode: code,
    ...details,
  });
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function hasNonEmptyString(
  record: Record<string, unknown>,
  key: string,
): boolean {
  return typeof record[key] === "string" && record[key].trim().length > 0;
}

function hasRecord(record: Record<string, unknown>, key: string): boolean {
  return isRecord(record[key]);
}

function hasNonEmptyArray(
  record: Record<string, unknown>,
  key: string,
): boolean {
  return Array.isArray(record[key]) && record[key].length > 0;
}

function hasExactKeys(
  record: Record<string, unknown>,
  expected: readonly string[],
): boolean {
  const actual = Object.keys(record).sort();
  const sortedExpected = [...expected].sort();
  return (
    actual.length === sortedExpected.length &&
    actual.every((key, index) => key === sortedExpected[index])
  );
}

function isNonEmptyString(value: unknown): value is string {
  return typeof value === "string" && value.trim().length > 0;
}

function isNonNegativeInteger(value: unknown): value is number {
  return Number.isInteger(value) && (value as number) >= 0;
}

function assertCompleteDec065SolveRequest(
  value: unknown,
): asserts value is Record<string, unknown> {
  if (!isRecord(value) || !isRecord(value.request) || !isRecord(value.solve)) {
    fail("HEADLESS_RUNNER_INPUT_SCHEMA_MISMATCH");
  }

  const request = value.request;
  const solve = value.solve;
  const complete =
    hasNonEmptyString(request, "request_id") &&
    request.operation === "solve" &&
    hasRecord(request, "operation_ref") &&
    hasRecord(request, "project_ref") &&
    hasRecord(request, "model_ref") &&
    hasRecord(request, "unit_system_ref") &&
    hasNonEmptyArray(request, "load_basis_refs") &&
    hasRecord(request, "input_manifest_ref") &&
    hasNonEmptyArray(request, "requested_outputs") &&
    hasRecord(request, "privacy") &&
    hasRecord(request, "provenance") &&
    hasRecord(request, "professional_boundary") &&
    hasRecord(request, "tbd_decisions") &&
    hasRecord(solve, "preview_model");

  if (!complete) {
    fail("HEADLESS_RUNNER_INPUT_SCHEMA_MISMATCH");
  }
}

const REFERENCE_KEYS = ["ref_type", "ref_id"] as const;
const PROVENANCE_KEYS = [
  "source_name",
  "source_location",
  "source_license",
  "contributor",
  "contributor_certification",
  "redistribution_status",
  "review_status",
] as const;
const DIAGNOSTIC_KEYS = [
  "code",
  "class",
  "severity",
  "source",
  "affected_object",
  "message",
  "remediation",
  "provenance",
] as const;
const DIAGNOSTIC_CLASSES = new Set([
  "SOLVE_BLOCKING",
  "RULE_CHECK_BLOCKING",
  "PROVENANCE_WARNING",
  "ASSUMPTION_WARNING",
  "NONLINEAR_WARNING",
  "IP_BOUNDARY_WARNING",
  "UNIT_WARNING",
  "RUNNER_BLOCKING",
  "EXPORT_BLOCKING",
  "PRIVACY_WARNING",
  "TBD",
]);
const DIAGNOSTIC_SEVERITIES = new Set(["info", "warning", "blocking"]);
const REDISTRIBUTION_STATUSES = new Set([
  "public_permissive",
  "private_only",
  "unknown",
  "protected_suspected",
  "invented_non_engineering_example",
  "TBD",
]);
const REVIEW_STATUSES = new Set([
  "pending",
  "accepted",
  "rejected",
  "quarantined",
  "TBD",
]);

function isReference(value: unknown): value is Record<string, unknown> {
  return (
    isRecord(value) &&
    hasExactKeys(value, REFERENCE_KEYS) &&
    isNonEmptyString(value.ref_type) &&
    isNonEmptyString(value.ref_id)
  );
}

function isProvenance(value: unknown): value is Record<string, unknown> {
  return (
    isRecord(value) &&
    hasExactKeys(value, PROVENANCE_KEYS) &&
    PROVENANCE_KEYS.slice(0, 5).every((key) => isNonEmptyString(value[key])) &&
    REDISTRIBUTION_STATUSES.has(value.redistribution_status as string) &&
    REVIEW_STATUSES.has(value.review_status as string)
  );
}

function isDiagnostic(value: unknown): value is Record<string, unknown> {
  return (
    isRecord(value) &&
    hasExactKeys(value, DIAGNOSTIC_KEYS) &&
    isNonEmptyString(value.code) &&
    DIAGNOSTIC_CLASSES.has(value.class as string) &&
    DIAGNOSTIC_SEVERITIES.has(value.severity as string) &&
    isReference(value.source) &&
    isReference(value.affected_object) &&
    isNonEmptyString(value.message) &&
    isNonEmptyString(value.remediation) &&
    isProvenance(value.provenance)
  );
}

function isDiagnosticArray(value: unknown): value is Record<string, unknown>[] {
  return Array.isArray(value) && value.every(isDiagnostic);
}

function isValidation(value: unknown): value is Record<string, unknown> {
  return (
    isRecord(value) &&
    hasExactKeys(value, ["diagnostics"]) &&
    isDiagnosticArray(value.diagnostics)
  );
}

function isPrivacy(value: unknown): value is Record<string, unknown> {
  return (
    isRecord(value) &&
    hasExactKeys(value, [
      "local_only",
      "telemetry_allowed",
      "private_payload_redacted",
      "classification",
    ]) &&
    value.local_only === true &&
    value.telemetry_allowed === false &&
    typeof value.private_payload_redacted === "boolean" &&
    new Set([
      "public_metadata",
      "private_project_data",
      "private_rule_pack_data",
      "redacted",
      "protected_suspected",
      "TBD",
    ]).has(value.classification as string)
  );
}

function isProfessionalBoundary(
  value: unknown,
): value is Record<string, unknown> {
  return (
    isRecord(value) &&
    hasExactKeys(value, [
      "human_review_required",
      "software_makes_compliance_claim",
      "software_makes_certification_claim",
      "software_makes_sealing_claim",
      "software_makes_approval_claim",
      "software_makes_authentication_claim",
    ]) &&
    value.human_review_required === true &&
    value.software_makes_compliance_claim === false &&
    value.software_makes_certification_claim === false &&
    value.software_makes_sealing_claim === false &&
    value.software_makes_approval_claim === false &&
    value.software_makes_authentication_claim === false
  );
}

function isChecksum(value: unknown): value is Record<string, unknown> {
  return (
    isRecord(value) &&
    hasExactKeys(value, [
      "algorithm",
      "canonicalization",
      "payload_ref",
      "value",
    ]) &&
    new Set(["sha256", "sha512"]).has(value.algorithm as string) &&
    new Set(["rfc8785_jcs", "NONE"]).has(value.canonicalization as string) &&
    isReference(value.payload_ref) &&
    isNonEmptyString(value.value) &&
    value.value.toUpperCase() !== "TBD"
  );
}

const RUNNER_RESULT_KEYS = [
  "run_id",
  "job",
  "analysis_status",
  "result_envelope_ref",
  "result_refs",
  "audit_manifest_ref",
  "checksums",
  "diagnostics",
  "privacy",
  "provenance",
  "professional_boundary",
] as const;
const JOB_STATES = new Set([
  "QUEUED",
  "RUNNING",
  "CANCELLATION_REQUESTED",
  "COMPLETED",
  "FAILED",
  "TBD",
]);
const ANALYSIS_STATUSES = new Set([
  "MODEL_INCOMPLETE",
  "MECHANICS_SOLVED",
  "RULE_INPUTS_INCOMPLETE",
  "USER_RULE_CHECKED",
  "USER_RULE_FAILED",
  "HUMAN_REVIEW_REQUIRED",
]);

function isJob(value: unknown): value is Record<string, unknown> {
  return (
    isRecord(value) &&
    hasExactKeys(value, [
      "job_id",
      "state",
      "current_step",
      "total_steps",
      "cancellation_supported",
      "cancellation_requested",
    ]) &&
    isNonEmptyString(value.job_id) &&
    JOB_STATES.has(value.state as string) &&
    isNonNegativeInteger(value.current_step) &&
    isNonNegativeInteger(value.total_steps) &&
    (value.current_step as number) <= (value.total_steps as number) &&
    typeof value.cancellation_supported === "boolean" &&
    typeof value.cancellation_requested === "boolean"
  );
}

function isResultEnvelopeRef(value: unknown): value is Record<string, unknown> {
  return (
    isRecord(value) &&
    hasExactKeys(value, ["schema_ref", "envelope_ref", "compatibility"]) &&
    value.schema_ref === "schemas/results.schema.yaml" &&
    isReference(value.envelope_ref) &&
    value.compatibility === "schema_first_json_result_envelope"
  );
}

function hasResultEnvelopeChecksum(
  checksums: unknown,
  resultEnvelopeRef: unknown,
): boolean {
  if (!Array.isArray(checksums) || !isResultEnvelopeRef(resultEnvelopeRef)) {
    return false;
  }

  const envelopeRef = resultEnvelopeRef.envelope_ref;
  return (
    isReference(envelopeRef) &&
    checksums.some(
      (checksum) =>
        isChecksum(checksum) &&
        isReference(checksum.payload_ref) &&
        checksum.payload_ref.ref_type === "result_envelope" &&
        checksum.payload_ref.ref_id === envelopeRef.ref_id,
    )
  );
}

function isRunnerResult(value: unknown): value is Record<string, unknown> {
  if (
    !isRecord(value) ||
    !hasExactKeys(value, RUNNER_RESULT_KEYS) ||
    !isJob(value.job)
  ) {
    return false;
  }
  const analysisStatus = value.analysis_status;
  return (
    isNonEmptyString(value.run_id) &&
    Array.isArray(analysisStatus) &&
    analysisStatus.length > 0 &&
    analysisStatus.every((status) => ANALYSIS_STATUSES.has(status as string)) &&
    analysisStatus.includes("HUMAN_REVIEW_REQUIRED") &&
    isResultEnvelopeRef(value.result_envelope_ref) &&
    Array.isArray(value.result_refs) &&
    value.result_refs.length > 0 &&
    value.result_refs.every(isReference) &&
    isReference(value.audit_manifest_ref) &&
    Array.isArray(value.checksums) &&
    value.checksums.length > 0 &&
    value.checksums.every(isChecksum) &&
    hasResultEnvelopeChecksum(value.checksums, value.result_envelope_ref) &&
    isDiagnosticArray(value.diagnostics) &&
    isPrivacy(value.privacy) &&
    isProvenance(value.provenance) &&
    isProfessionalBoundary(value.professional_boundary)
  );
}

function isPolicy(value: unknown): value is Record<string, unknown> {
  return (
    isRecord(value) &&
    hasExactKeys(value, [
      "policy_ref",
      "binary",
      "stdout_default",
      "explicit_output_path_only",
      "local_foreground_process",
      "network_allowed",
      "telemetry_allowed",
      "daemon_allowed",
      "hidden_filesystem_mutation_allowed",
      "direct_sql_access_allowed",
    ]) &&
    value.policy_ref === "DEC-065" &&
    value.binary === "openpipestress-runner" &&
    value.stdout_default === true &&
    value.explicit_output_path_only === true &&
    value.local_foreground_process === true &&
    value.network_allowed === false &&
    value.telemetry_allowed === false &&
    value.daemon_allowed === false &&
    value.hidden_filesystem_mutation_allowed === false &&
    value.direct_sql_access_allowed === false
  );
}

function collectDiagnostics(
  value: Record<string, unknown>,
): Record<string, unknown>[] {
  const groups = [
    value.diagnostics,
    (value.request_validation as Record<string, unknown>).diagnostics,
    isRecord(value.result_validation)
      ? value.result_validation.diagnostics
      : [],
    isRecord(value.runner_result) ? value.runner_result.diagnostics : [],
  ];
  return groups.flatMap((group) => group as Record<string, unknown>[]);
}

function assertDec065Result(
  value: unknown,
  exitCode: number,
): asserts value is Record<string, unknown> {
  const requiredKeys = [
    "artifact",
    "schema_version",
    "deliverable_id",
    "package_id",
    "command",
    "operation",
    "policy",
    "request_validation",
    "result_validation",
    "runner_result",
    "mechanics_envelope",
    "diagnostics",
  ];
  const allowedKeys = [...requiredKeys, "suite_run"];
  const structurallyValid =
    isRecord(value) &&
    requiredKeys.every((key) => Object.hasOwn(value, key)) &&
    Object.keys(value).every((key) => allowedKeys.includes(key)) &&
    value.artifact === "openpipestress.headless_runner_cli_output" &&
    value.schema_version === "1.0.0" &&
    value.deliverable_id === "DEL-10-05" &&
    value.package_id === "PKG-10" &&
    value.command === "solve" &&
    value.operation === "solve" &&
    isPolicy(value.policy) &&
    isValidation(value.request_validation) &&
    (value.result_validation === null ||
      isValidation(value.result_validation)) &&
    (value.runner_result === null || isRunnerResult(value.runner_result)) &&
    (value.mechanics_envelope === null || isRecord(value.mechanics_envelope)) &&
    isDiagnosticArray(value.diagnostics) &&
    (!Object.hasOwn(value, "suite_run") || value.suite_run === null);
  if (!structurallyValid) {
    fail("HEADLESS_RUNNER_RESULT_SCHEMA_MISMATCH", 502);
  }

  const blocking = collectDiagnostics(value).some(
    (diagnostic) => diagnostic.severity === "blocking",
  );
  const completed =
    isRecord(value.runner_result) &&
    isRecord(value.runner_result.job) &&
    value.runner_result.job.state === "COMPLETED";
  if (
    exitCode === 0 &&
    (!completed ||
      blocking ||
      !isRecord(value.result_validation) ||
      !isRecord(value.mechanics_envelope))
  ) {
    fail("HEADLESS_RUNNER_EXIT_RESULT_MISMATCH", 502);
  }
  if (exitCode === 1 && !blocking) {
    fail("HEADLESS_RUNNER_EXIT_RESULT_MISMATCH", 502);
  }
}

async function resolveVerifiedRunner(
  config: HeadlessRunnerEnvironment,
): Promise<string> {
  const configuredPath = config[OPEN_PIPE_STRESS_RUNNER_PATH_ENV];
  const expectedSha256 = config[OPEN_PIPE_STRESS_RUNNER_SHA256_ENV];
  if (!configuredPath || !expectedSha256) {
    fail("HEADLESS_RUNNER_CONFIG_MISSING");
  }
  if (!path.isAbsolute(configuredPath)) {
    fail("HEADLESS_RUNNER_PATH_NOT_ABSOLUTE");
  }
  if (!/^[0-9a-f]{64}$/.test(expectedSha256)) {
    fail("HEADLESS_RUNNER_SHA256_INVALID");
  }

  let resolvedPath: string;
  try {
    resolvedPath = await realpath(configuredPath);
  } catch {
    fail("HEADLESS_RUNNER_PATH_INVALID");
  }

  let runnerStat;
  try {
    runnerStat = await stat(resolvedPath);
  } catch {
    fail("HEADLESS_RUNNER_PATH_INVALID");
  }
  if (!runnerStat.isFile()) {
    fail("HEADLESS_RUNNER_NOT_REGULAR_FILE");
  }
  try {
    await access(resolvedPath, fsConstants.X_OK);
  } catch {
    fail("HEADLESS_RUNNER_NOT_EXECUTABLE");
  }

  let executableBytes: Buffer;
  try {
    executableBytes = await readFile(resolvedPath);
  } catch {
    fail("HEADLESS_RUNNER_PATH_INVALID");
  }
  const actualSha256 = createHash("sha256")
    .update(executableBytes)
    .digest("hex");
  if (actualSha256 !== expectedSha256) {
    fail("HEADLESS_RUNNER_SHA256_MISMATCH");
  }
  return resolvedPath;
}

async function collectChildResult(input: {
  executablePath: string;
  stdinBytes: Buffer;
  timeoutMs: number;
}): Promise<{
  exitCode: number | null;
  signal: NodeJS.Signals | null;
  stdout: Buffer;
}> {
  return new Promise((resolve, reject) => {
    const child = spawn(input.executablePath, ["solve"], {
      shell: false,
      windowsHide: true,
      stdio: ["pipe", "pipe", "pipe"],
      env: {
        NODE_ENV: "production",
        LANG: "C",
        LC_ALL: "C",
      },
    });
    const stdoutChunks: Buffer[] = [];
    let stdoutBytes = 0;
    let stderrBytes = 0;
    let failureCode: string | undefined;
    let settled = false;

    const terminate = (code: string) => {
      if (!failureCode) {
        failureCode = code;
        child.kill("SIGKILL");
      }
    };
    const timeout = setTimeout(
      () => terminate("HEADLESS_RUNNER_TIMEOUT"),
      input.timeoutMs,
    );

    child.stdout.on("data", (chunk: Buffer | string) => {
      const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
      stdoutBytes += buffer.byteLength;
      if (stdoutBytes > HEADLESS_RUNNER_STDOUT_LIMIT_BYTES) {
        terminate("HEADLESS_RUNNER_STDOUT_OVERSIZE");
        return;
      }
      stdoutChunks.push(buffer);
    });
    child.stderr.on("data", (chunk: Buffer | string) => {
      const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
      stderrBytes += buffer.byteLength;
      if (stderrBytes > HEADLESS_RUNNER_STDERR_LIMIT_BYTES) {
        terminate("HEADLESS_RUNNER_STDERR_OVERSIZE");
      }
    });
    child.once("error", () => {
      clearTimeout(timeout);
      if (!settled) {
        settled = true;
        reject(
          new HarnessError(
            "INVALID_REQUEST",
            502,
            "HEADLESS_RUNNER_SPAWN_FAILED",
            {
              errorCode: "HEADLESS_RUNNER_SPAWN_FAILED",
            },
          ),
        );
      }
    });
    child.once("close", (exitCode, signal) => {
      clearTimeout(timeout);
      if (settled) {
        return;
      }
      settled = true;
      if (failureCode) {
        reject(
          new HarnessError("INVALID_REQUEST", 502, failureCode, {
            errorCode: failureCode,
          }),
        );
        return;
      }
      resolve({
        exitCode,
        signal,
        stdout: Buffer.concat(stdoutChunks, stdoutBytes),
      });
    });

    child.stdin.on("error", () => {
      terminate("HEADLESS_RUNNER_STDIN_FAILED");
    });
    child.stdin.end(input.stdinBytes);
  });
}

export async function runConfiguredHeadlessPreview(input: {
  requestBytes: Buffer;
  env?: HeadlessRunnerEnvironment;
  timeoutMs?: number;
}): Promise<RunnerExit> {
  let parsedInput: unknown;
  try {
    parsedInput = JSON.parse(input.requestBytes.toString("utf8"));
  } catch {
    fail("HEADLESS_RUNNER_INPUT_JSON_INVALID");
  }
  assertCompleteDec065SolveRequest(parsedInput);

  const executablePath = await resolveVerifiedRunner(input.env ?? process.env);
  const childResult = await collectChildResult({
    executablePath,
    stdinBytes: input.requestBytes,
    timeoutMs: input.timeoutMs ?? HEADLESS_RUNNER_TIMEOUT_MS,
  });
  if (childResult.signal) {
    fail("HEADLESS_RUNNER_SIGNALLED", 502);
  }
  if (childResult.exitCode === 2) {
    fail("HEADLESS_RUNNER_INPUT_REFUSED");
  }
  if (childResult.exitCode !== 0 && childResult.exitCode !== 1) {
    fail("HEADLESS_RUNNER_EXIT_UNSUPPORTED", 502);
  }

  let parsedResult: unknown;
  try {
    parsedResult = JSON.parse(childResult.stdout.toString("utf8"));
  } catch {
    fail("HEADLESS_RUNNER_RESULT_JSON_INVALID", 502);
  }
  assertDec065Result(parsedResult, childResult.exitCode);
  return {
    exitCode: childResult.exitCode,
    result: parsedResult,
  };
}
