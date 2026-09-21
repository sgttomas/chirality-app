#!/usr/bin/env node

import { createHash } from 'node:crypto';
import {
  access,
  lstat,
  readFile,
  readdir,
  readlink,
  realpath,
  stat,
  writeFile
} from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import { isDeepStrictEqual } from 'node:util';
import { fileURLToPath } from 'node:url';

const SCRIPT_PATH = fileURLToPath(import.meta.url);
const FRONTEND_ROOT = path.resolve(path.dirname(SCRIPT_PATH), '..');
const LOOPBACK_HOSTS = new Set(['localhost', '127.0.0.1', '::1', '[::1]']);
const PACKAGED_POLICY_MARKERS = [
  'REQ-NET-001',
  'api.anthropic.com',
  'anthropic_protocol_not_allowlisted',
  'anthropic_port_not_allowlisted',
  'host_not_allowlisted',
  'Blocked renderer outbound request by network policy',
  'Attachment exceeds per-file size limit',
  'Attachment exceeds per-turn size budget',
  'symbolic links are rejected',
  'ATTACHMENT_FAILURE',
  'Content-Security-Policy',
  'X-Chirality-Response-Class',
  'eligible-pdf-v1',
  "frame-ancestors 'self'",
  'PDF preview requires a PDF signature.',
  'Expected one root, one file selector, and no duplicate or unknown selectors.',
  'renderer.window_open.denied',
  'renderer.navigation.denied',
  'contextIsolation',
  'nodeIntegration',
  'sandbox',
  'isAuthorizedSender',
  'Credential request was denied'
];
const BLOCKED_PROBE_URL = 'https://example.com/chirality-packaged-security-blocked';
const LOOPBACK_PROBE_URL = 'http://127.0.0.1:9/chirality-packaged-security-loopback';
export const PACKAGED_RENDERER_ROUTES = ['/', '/chat', '/pipeline', '/workbench'];
export const D121_PDF_CONTENT_SECURITY_POLICY = [
  "default-src 'none'", "script-src 'none'", "frame-src 'none'", "object-src 'none'",
  "base-uri 'none'", "form-action 'none'", "frame-ancestors 'self'"
].join('; ');
export const D121_FROZEN_SOURCE_IDENTITIES = [
  ['electron/renderer-window-policy.ts', 'e2d63d32423d1ef6b0a03259235676ac9cefadde00e4f067be4f13e5ed2cc3ed', 33544],
  ['electron/main.ts', 'ea82a7dcbf9cbb60ac46cf0ab9b649c287a71b59341d0a27f13999787d79d6e3', 39110],
  ['src/app/api/working-root/file/route.ts', '75c098a0af0fe1348a036f9ca0ed71526177cec579d6cb66bb1427b6dd743919', 7476],
  ['src/app/api/working-root/file/file-policy.ts', 'f40f5a14583ff1f43f072273d2c476ecfd899f81571d7531cdc2a95fc43a6f9c', 9480],
  ['src/components/shell/document-view.tsx', '384ef2d622223ef5b4f13a95ce38449f943b65bc81485d187c4a03a87da44982', 23110],
  ['electron/preload.ts', 'bf7c0351875e906e8a2646baf292452b5ac537a0f52887def9ef1d95f45c7560', 4654],
  ['src/__tests__/electron/renderer-window-policy.test.ts', 'd3ef6b47e07cbff491f3fd490f219e5b887f37fa156ecd922991eb5697469248', 46990],
  ['src/__tests__/api/working-root/file-route.test.ts', '8fb4cf4c12b9e6c97065d2194a9122f4cc6257384ec9822289892adbd5111f63', 16443],
  ['src/__tests__/components/document-view.test.tsx', 'e00f193e66afbf4fc1e30a84a17467871b259fd22462d786b6c546265eded861', 13638],
  ['src/__tests__/contract-pins.manifest.ts', 'f8aa8b27564bb516e938e3d4a81d17ca58d640743c0e8ba105c3e90b041eb753', 25929],
  ['src/__tests__/electron/folder-preload.test.ts', 'ab65a700be92ec4c5dc3ae6737a066cf90ac5c11605624b682f0512a4ec49da6', 2658]
];
export const D121_REQUIRED_NEGATIVE_CONTROLS = [
  'foreign-origin', 'blob-url', 'data-url', 'file-url', 'extension-url', 'object-embed',
  'webview', 'wildcard-frame', 'wrong-status', 'wrong-method', 'wrong-path', 'wrong-origin',
  'duplicate-selector', 'unknown-selector', 'invalid-signature', 'zero-size', 'outside-root',
  'instruction-root', 'dot-git', 'symlink', 'nonregular', 'unreadable',
  'descriptor-identity-change', 'raw-encoded-path', 'normalized-encoded-path', 'dot-segment',
  'duplicate-slash', 'spoofed-marker', 'reflected-marker', 'conflicting-header', 'redirect',
  'malformed-pdf', 'polyglot-pdf', 'first-read-failure', 'precommit-failure',
  'postcommit-failure', 'cancellation', 'disconnect'
];
export const D121_REQUIRED_OBSERVATIONS = [
  'response-headers', 'finalizer-commit-matrix', 'selector-path-origin-negatives',
  'descriptor-negatives', 'streaming-range', 'stream-failures', 'framing-negatives',
  'existing-controls'
];
const D121_OBSERVATION_ARTIFACT_TYPES = {
  'response-headers': 'http-policy-result',
  'finalizer-commit-matrix': 'finalizer-result',
  'selector-path-origin-negatives': 'negative-control-suite-result',
  'descriptor-negatives': 'negative-control-suite-result',
  'streaming-range': 'streaming-result',
  'stream-failures': 'streaming-result',
  'framing-negatives': 'negative-control-suite-result',
  'existing-controls': 'negative-control-suite-result'
};
export const D121_S1_MATRIX_STATUS = 'INAPPLICABLE_OWNER_DEFERRED';
export const D121_NEGATIVE_OBSERVATION_CONTROLS = {
  'selector-path-origin-negatives': [
    'wrong-status', 'wrong-method', 'wrong-path', 'wrong-origin', 'duplicate-selector',
    'unknown-selector', 'invalid-signature', 'zero-size', 'outside-root', 'instruction-root',
    'dot-git', 'symlink', 'nonregular', 'unreadable', 'raw-encoded-path',
    'normalized-encoded-path', 'dot-segment', 'duplicate-slash'
  ],
  'descriptor-negatives': ['descriptor-identity-change'],
  'framing-negatives': [
    'foreign-origin', 'blob-url', 'data-url', 'file-url', 'extension-url', 'object-embed',
    'webview', 'wildcard-frame'
  ],
  'existing-controls': [
    'spoofed-marker', 'reflected-marker', 'conflicting-header', 'redirect', 'malformed-pdf',
    'polyglot-pdf', 'first-read-failure', 'precommit-failure', 'postcommit-failure',
    'cancellation', 'disconnect'
  ]
};
export const D121_EVIDENCE_ORIGINS = [
  'SOURCE_COMPONENT', 'PACKAGE_HTTP', 'PACKAGE_UI', 'PACKAGE_GENERAL', 'MIXED'
];
export const D121_OBSERVATION_ORIGINS = {
  'response-headers': 'PACKAGE_HTTP',
  'finalizer-commit-matrix': 'SOURCE_COMPONENT',
  'streaming-range': 'MIXED',
  'stream-failures': 'MIXED',
  'selector-path-origin-negatives': 'MIXED',
  'descriptor-negatives': 'SOURCE_COMPONENT',
  'framing-negatives': 'MIXED',
  'existing-controls': 'MIXED'
};
const HTTP_ONLY_CONTROLS = new Set([
  'duplicate-selector', 'unknown-selector', 'invalid-signature', 'zero-size', 'outside-root',
  'symlink', 'nonregular'
]);
const MIXED_CONTROLS = new Set([
  'wrong-method', 'wrong-path', 'raw-encoded-path', 'normalized-encoded-path', 'dot-segment'
]);
export const D121_CONTROL_ORIGINS = Object.fromEntries(D121_REQUIRED_NEGATIVE_CONTROLS.map((id) => [
  id, HTTP_ONLY_CONTROLS.has(id) ? 'PACKAGE_HTTP' : MIXED_CONTROLS.has(id) ? 'MIXED' : 'SOURCE_COMPONENT'
]));
export const D121_STREAMING_FIELD_ORIGINS = {
  rangeStatus: 'PACKAGE_HTTP', ifRangeStatus: 'PACKAGE_HTTP', fullResponseBytes: 'PACKAGE_HTTP',
  bounded: 'SOURCE_COMPONENT', maxChunkBytes: 'SOURCE_COMPONENT', mutationDetected: 'SOURCE_COMPONENT',
  postcommitAborted: 'SOURCE_COMPONENT', closeCounts: 'SOURCE_COMPONENT'
};
export const CAPTURE_SCHEMA = 'chirality-d121-s0-captured-input/v2';
const D121_FIXTURE_ROLES = ['positive', 'invalid-signature', 'zero-size', 'outside-root', 'symlink'];
export const D121_PACKAGE_IDENTITY_RELATIVE_PATHS = {
  executable: 'Contents/MacOS/Chirality',
  appAsar: 'Contents/Resources/app.asar',
  runtimeCli: 'Contents/Resources/runtime-cli/chirality-cli.mjs',
  unpackedSdkPackage: 'Contents/Resources/app.asar.unpacked/node_modules/@anthropic-ai/sdk/package.json',
  unpackedSdkBinary: 'Contents/Resources/app.asar.unpacked/node_modules/@anthropic-ai/sdk/client.mjs'
};
const CAPTURE_KEYS = [
  'schema', 'runId', 'source', 'package', 'authorities', 'fixtures', 'identities',
  'execution', 'members', 'artifacts', 'credential', 'cleanup', 'evidenceMatrix'
];
const SHA256_PATTERN = /^[a-f0-9]{64}$/;
// The page can no longer reach the REQ-NET-001 egress layer for a foreign host
// (the CSP's connect-src 'self' stops it first), so the packaged app issues this
// request itself, from the main process through the window's session, where
// onBeforeRequest denies it (anthropic_port_not_allowlisted:8443). The
// destination is fixed inside the app (renderer-window-policy.ts
// EGRESS_LAYER_PROBE_URL) and is never read from the environment, so this proof
// cannot point the probe anywhere else (DEL-09-06-V3-05); the constant below is
// what the summarizer expects to observe, and the unit test checks it is
// byte-equal to the app's. The example.com probe above is the CSP-layer
// observation.
export const EGRESS_PROBE_URL = 'https://api.anthropic.com:8443/chirality-packaged-security-egress-blocked';
const EGRESS_PROBE_DESTINATION = new URL(EGRESS_PROBE_URL);
// Negative control: the retired probe-URL variable is set to a destination the
// egress policy WOULD allow (loopback; port 9 refuses the connection, so nothing
// leaves the host). The app must ignore it: the only probe payload observed must
// still name the :8443 destination, and any other destination fails the proof.
export const EGRESS_PROBE_DECOY_URL = 'http://127.0.0.1:9/chirality-packaged-security-egress-probe-decoy';

function nowIso() {
  return new Date().toISOString();
}

function readArgValue(argv, index, flagName) {
  const value = argv[index];
  if (!value || value.startsWith('--')) throw new Error(`Missing value for ${flagName}`);
  return value;
}

export function parseArgs(argv) {
  const options = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === '--app-path') {
      options.appPath = readArgValue(argv, index + 1, token);
      index += 1;
    } else if (token === '--output-root') {
      options.outputRoot = readArgValue(argv, index + 1, token);
      index += 1;
    } else if (token === '--source-revision') {
      options.sourceRevision = readArgValue(argv, index + 1, token);
      index += 1;
    } else if (token === '--captured-input') {
      options.capturedInputPath = readArgValue(argv, index + 1, token);
      index += 1;
    } else if (token === '--accepted-source-binding') {
      options.acceptedSourceBindingPath = readArgValue(argv, index + 1, token);
      index += 1;
    } else if (token === '--s0-security-evidence') {
      options.s0SecurityEvidencePath = readArgValue(argv, index + 1, token);
      index += 1;
    } else if (token === '--s0-security-run-id') {
      options.s0SecurityRunId = readArgValue(argv, index + 1, token);
      index += 1;
    } else if (token === '--help') {
      options.help = true;
    } else {
      throw new Error(`Unknown argument: ${token}`);
    }
  }
  if (options.help === true) return { help: true };
  const required = [
    ['--captured-input', options.capturedInputPath],
    ['--accepted-source-binding', options.acceptedSourceBindingPath],
    ['--output-root', options.outputRoot],
    ['--app-path', options.appPath],
    ['--source-revision', options.sourceRevision],
    ['--s0-security-evidence', options.s0SecurityEvidencePath],
    ['--s0-security-run-id', options.s0SecurityRunId]
  ];
  for (const [flag, value] of required) {
    if (typeof value !== 'string' || value.length === 0) throw new Error(`${flag} is required`);
  }
  for (const [flag, value] of required.filter(([flag]) => flag !== '--source-revision' && flag !== '--s0-security-run-id')) {
    if (!path.isAbsolute(value)) throw new Error(`${flag} must be an absolute path`);
  }
  return {
    appPath: options.appPath,
    acceptedSourceBindingPath: options.acceptedSourceBindingPath,
    capturedInputPath: options.capturedInputPath,
    outputRoot: options.outputRoot,
    sourceRevision: options.sourceRevision,
    s0SecurityEvidencePath: options.s0SecurityEvidencePath,
    s0SecurityRunId: options.s0SecurityRunId,
    help: false
  };
}

export function usage() {
  return `Usage: node ./scripts/run-packaged-security-proof.mjs --captured-input <absolute-json> --accepted-source-binding <absolute-json> --output-root <existing-empty-directory> --app-path <absolute-app> --source-revision <sha> --s0-security-evidence <absolute-json> --s0-security-run-id <id>\n`;
}

async function sha256File(filePath) {
  return createHash('sha256').update(await readFile(filePath)).digest('hex');
}

export async function inspectD121FrozenSource(frontendRoot = FRONTEND_ROOT) {
  const files = await Promise.all(D121_FROZEN_SOURCE_IDENTITIES.map(async ([relativePath, expectedSha256, expectedBytes]) => {
    const bytes = await readFile(path.join(frontendRoot, relativePath));
    const sha256 = createHash('sha256').update(bytes).digest('hex');
    return { relativePath, expectedSha256, expectedBytes, sha256, bytes: bytes.length,
      pass: sha256 === expectedSha256 && bytes.length === expectedBytes };
  }));
  return summarizeD121FrozenSourceFiles(files);
}

export function summarizeD121FrozenSourceFiles(files) {
  const expectedPaths = D121_FROZEN_SOURCE_IDENTITIES.map(([relativePath]) => relativePath);
  const actualPaths = Array.isArray(files) ? files.map((entry) => entry?.relativePath) : [];
  const completeIdentitySet = sameStructuredValue(actualPaths, expectedPaths);
  const pass = completeIdentitySet && files.every((entry) => entry?.pass === true);
  return {
    schema: 'chirality-d121-s0-frozen-source-proof/v1',
    mode: pass ? 'S0_OWNER_DEFERRED' : 'UNRECOGNIZED',
    inlinePdfPreview: pass ? false : null,
    s1MatrixStatus: pass ? D121_S1_MATRIX_STATUS : null,
    files: Array.isArray(files) ? files : [],
    pass
  };
}

function sameStructuredValue(left, right) {
  return isDeepStrictEqual(left, right);
}

function exactClaim(record, claimId, expectedValue) {
  const claim = record?.results?.[claimId];
  return claim?.outcome === 'pass' &&
    Object.hasOwn(claim, 'actual') && Object.hasOwn(claim, 'expected') &&
    sameStructuredValue(claim.expected, expectedValue) &&
    sameStructuredValue(claim.actual, expectedValue);
}

function validReference(reference) {
  return hasExactKeys(reference, ['path', 'sha256', 'bytes', 'artifactType']) &&
    typeof reference.path === 'string' && reference.path.length > 0 &&
    SHA256_PATTERN.test(reference.sha256) && Number.isSafeInteger(reference.bytes) &&
    reference.bytes > 0 && typeof reference.artifactType === 'string' && reference.artifactType.length > 0;
}

function validMeasurement(measurement, resolveFile) {
  const keys = Object.keys(measurement ?? {}).sort();
  const closedShape = sameStructuredValue(keys, ['inputIdentities', 'rawTraceRefs']) ||
    sameStructuredValue(keys, ['fieldOrigins', 'inputIdentities', 'rawTraceRefs']);
  return closedShape &&
    Array.isArray(measurement.rawTraceRefs) && measurement.rawTraceRefs.length > 0 &&
    measurement.rawTraceRefs.every((reference) => validReference(reference) && resolveFile(
      reference, reference.artifactType
    )?.pass === true) &&
    measurement.inputIdentities !== null && typeof measurement.inputIdentities === 'object' &&
    !Array.isArray(measurement.inputIdentities) && Object.keys(measurement.inputIdentities).length > 0 &&
    Object.values(measurement.inputIdentities).every((value) => value !== null && value !== undefined);
}

function exactRecordSubject(record, artifactType, evidence, fixture, expectedRunId, origin, resolveFile) {
  const recordKeys = record?.artifactType === 'negative-control-result'
    ? ['schema', 'artifactType', 'sourceRevision', 'packageArtifactIdentitySha256', 'fixtureIdentity',
      'execution', 'observationIds', 'result', 'origin', 'measurement']
    : ['schema', 'artifactType', 'sourceRevision', 'packageArtifactIdentitySha256', 'fixtureIdentity',
      'execution', 'observationIds', 'results', 'origin', 'measurement'];
  return hasExactKeys(record, recordKeys) && record?.schema === 'chirality-d121-executed-result/v2' &&
    record?.artifactType === artifactType &&
    record?.sourceRevision === evidence?.sourceRevision &&
    record?.packageArtifactIdentitySha256 === evidence?.artifactIdentitySha256 &&
    sameStructuredValue(record?.fixtureIdentity, fixture) &&
    record?.execution?.status === 'pass' &&
    typeof expectedRunId === 'string' && expectedRunId.length > 0 &&
    record?.execution?.runId === expectedRunId &&
    record?.origin === origin && validMeasurement(record?.measurement, resolveFile);
}

function exactObservedControls(controls, resolveReference, evidence, fixture, expectedRunId) {
  if (!Array.isArray(controls) || controls.length !== D121_REQUIRED_NEGATIVE_CONTROLS.length) return false;
  const byId = new Map(controls.map((entry) => [entry?.id, entry]));
  return byId.size === D121_REQUIRED_NEGATIVE_CONTROLS.length &&
    D121_REQUIRED_NEGATIVE_CONTROLS.every((id) => {
      const entry = byId.get(id);
      const record = resolveReference(entry?.evidenceRef, 'negative-control-result');
      const expectedOutcome = id.includes('failure') || id === 'cancellation' || id === 'disconnect'
        ? 'aborted'
        : 'denied';
      return exactRecordSubject(
        record, 'negative-control-result', evidence, fixture, expectedRunId,
        D121_CONTROL_ORIGINS[id], resolveReference.fileResolver
      ) &&
        record?.result?.controlId === id &&
        record?.result?.status === 'pass' &&
        record?.result?.outcome === expectedOutcome;
    });
}

function hasExactKeys(value, expectedKeys) {
  return value !== null && typeof value === 'object' && !Array.isArray(value) &&
    sameStructuredValue(Object.keys(value).sort(), [...expectedKeys].sort());
}

/** Validate the retained closed S0 route/security matrix; S1 is owner-deferred. */
export function summarizeD121S0SecurityEvidence(evidence, expected) {
  const fixture = evidence?.fixture ?? {};
  const evidenceFiles = Array.isArray(evidence?.evidenceFiles) ? evidence.evidenceFiles : [];
  const verifiedEvidenceFiles = expected?.evidenceFileVerification;
  const verifiedByIdentity = new Map((verifiedEvidenceFiles?.files ?? []).map((entry) => [
    `${entry?.path}\0${entry?.sha256}\0${entry?.bytes}`, entry
  ]));
  const evidencePaths = new Set(evidenceFiles.map((entry) => entry?.path));
  const evidenceFilesBound = verifiedEvidenceFiles?.pass === true && evidenceFiles.length > 0 &&
    evidencePaths.size === evidenceFiles.length && evidenceFiles.every((entry) =>
    typeof entry?.path === 'string' && entry.path.length > 0 &&
    typeof entry?.sha256 === 'string' && /^[a-f0-9]{64}$/.test(entry.sha256) &&
    Number.isSafeInteger(entry?.bytes) && entry.bytes > 0 &&
    typeof entry?.artifactType === 'string' && entry.artifactType.length > 0 &&
    verifiedByIdentity.get(`${entry.path}\0${entry.sha256}\0${entry.bytes}`)?.pass === true
  );
  const resolveFile = (reference, artifactType) => {
    if (!evidenceFilesBound || reference?.artifactType !== artifactType ||
        typeof reference?.path !== 'string' || typeof reference?.sha256 !== 'string' ||
        !Number.isSafeInteger(reference?.bytes)) return null;
    const declared = evidenceFiles.find((entry) => entry.path === reference.path &&
      entry.sha256 === reference.sha256 && entry.bytes === reference.bytes && entry.artifactType === artifactType);
    if (!declared) return null;
    return verifiedByIdentity.get(`${reference.path}\0${reference.sha256}\0${reference.bytes}`) ?? null;
  };
  const resolveReference = (reference, artifactType) => resolveFile(reference, artifactType)?.record ?? null;
  resolveReference.fileResolver = resolveFile;
  const expectedRunId = expected?.runId;
  const observationRefs = evidence?.observationRefs ?? {};
  const observationRecords = Object.fromEntries(D121_REQUIRED_OBSERVATIONS.map((name) => {
    const reference = observationRefs[name];
    const artifactType = D121_OBSERVATION_ARTIFACT_TYPES[name];
    const record = resolveReference(reference, artifactType);
    return [name, exactRecordSubject(
      record, artifactType, evidence, fixture, expectedRunId, D121_OBSERVATION_ORIGINS[name], resolveFile
    ) &&
      Array.isArray(record?.observationIds) && record.observationIds.includes(name) ? record : null];
  }));
  const observationsBound = D121_REQUIRED_OBSERVATIONS.every((name) => observationRecords[name] !== null);
  const finalizerRecord = observationRecords['finalizer-commit-matrix'];
  const finalizerPass = [
    'soleEmitter', 'requestSpoofIgnored', 'responseMarkerStripped', 'conflictingHeadersClosed',
    'explicitCommit', 'implicitFlushCommit', 'implicitWriteCommit', 'implicitEndCommit',
    'restoredAfterCommit', 'errorsClosed', 'redirectsClosed', 'lateHeadersIgnored',
    'packagedDevelopmentParity'
  ].every((key) => exactClaim(finalizerRecord, key, true));
  const policyRecord = observationRecords['response-headers'];
  const policyExpected = {
    status: 200, contentType: 'application/pdf', contentDisposition: 'inline', nosniff: true,
    noStore: true, contentLengthPositive: true, locationAbsent: true, contentRangeAbsent: true,
    acceptRangesAbsent: true, responseClassHeaderAbsent: true, csp: D121_PDF_CONTENT_SECURITY_POLICY
  };
  const policyPass = Object.entries(policyExpected).every(([key, value]) => exactClaim(policyRecord, key, value));
  const streamingRecord = observationRecords['streaming-range'];
  const streamingPass = streamingRecord === observationRecords['stream-failures'] &&
    sameStructuredValue(streamingRecord?.measurement?.fieldOrigins, D121_STREAMING_FIELD_ORIGINS) &&
    exactClaim(streamingRecord, 'rangeStatus', 200) && exactClaim(streamingRecord, 'ifRangeStatus', 200) &&
    exactClaim(streamingRecord, 'fullResponseBytes', fixture.bytes) && exactClaim(streamingRecord, 'bounded', true) &&
    Number.isSafeInteger(streamingRecord?.results?.maxChunkBytes?.actual) &&
    streamingRecord.results.maxChunkBytes.actual > 0 && streamingRecord.results.maxChunkBytes.actual <= 64 * 1024 &&
    sameStructuredValue(streamingRecord.results.maxChunkBytes.actual, streamingRecord.results.maxChunkBytes.expected) &&
    streamingRecord.results.maxChunkBytes.outcome === 'pass' && exactClaim(streamingRecord, 'mutationDetected', true) &&
    exactClaim(streamingRecord, 'postcommitAborted', true) &&
    exactClaim(streamingRecord, 'closeCounts', { complete: 1, cancel: 1, disconnect: 1, failure: 1 });
  const fixtureFile = resolveFile(evidence?.fixtureRef, 'pdf-fixture');
  const fixturePass = Number.isSafeInteger(fixture.bytes) && fixture.bytes > 0 &&
    Number.isSafeInteger(fixture.pageCount) && fixture.pageCount >= 2 &&
    typeof fixture.sha256 === 'string' && /^[a-f0-9]{64}$/.test(fixture.sha256) &&
    fixtureFile?.pass === true && evidence.fixtureRef.sha256 === fixture.sha256 &&
    evidence.fixtureRef.bytes === fixture.bytes;
  const identityPass = evidence?.schema === 'chirality-d121-s0-security-evidence/v2' &&
    evidence?.runId === expectedRunId && typeof expectedRunId === 'string' && expectedRunId.length > 0 &&
    evidence?.sourceRevision === expected.sourceRevision &&
    evidence?.artifactIdentitySha256 === expected.artifactIdentitySha256;
  const negativeControlsPass = exactObservedControls(
    evidence?.negativeControls, resolveReference, evidence, fixture, expectedRunId
  );
  const negativeObservationPass = ['selector-path-origin-negatives', 'descriptor-negatives',
    'framing-negatives', 'existing-controls'].every((name) => {
    const record = observationRecords[name];
    return exactClaim(record, name, D121_NEGATIVE_OBSERVATION_CONTROLS[name]);
  });
  const acceptedShapePass = hasExactKeys(evidence, [
    'schema', 'sourceRevision', 'artifactIdentitySha256', 'runId', 'fixture', 'fixtureRef',
    'evidenceFiles', 'observationRefs', 'negativeControls', 's1Matrix'
  ]) && hasExactKeys(evidence?.s1Matrix, ['status']) &&
    evidence.s1Matrix.status === D121_S1_MATRIX_STATUS &&
    hasExactKeys(observationRefs, D121_REQUIRED_OBSERVATIONS);
  const s1MatrixPass = acceptedShapePass;
  return {
    schema: 'chirality-d121-s0-security-summary/v1', identityPass, fixturePass,
    evidenceFilesBound, observationsBound, finalizerPass, policyPass, streamingPass,
    negativeControlsPass, negativeObservationPass, acceptedShapePass,
    s1MatrixStatus: D121_S1_MATRIX_STATUS, s1MatrixPass,
    requiredNegativeControls: D121_REQUIRED_NEGATIVE_CONTROLS,
    pass: identityPass && fixturePass && evidenceFilesBound && observationsBound && finalizerPass && policyPass &&
      streamingPass && negativeControlsPass && negativeObservationPass && acceptedShapePass
  };
}

export async function verifyD121EvidenceFiles(evidence, evidencePath) {
  const evidenceRoot = await realpath(path.dirname(evidencePath));
  const files = [];
  const seenPaths = new Set();
  const seenCanonicalPaths = new Set();
  const seenFileObjects = new Set();
  for (const entry of Array.isArray(evidence?.evidenceFiles) ? evidence.evidenceFiles : []) {
    try {
      if (!validReference(entry)) throw new Error('invalid or non-closed evidence member');
      if (seenPaths.has(entry?.path)) throw new Error('duplicate evidence path');
      seenPaths.add(entry?.path);
      if (path.isAbsolute(entry.path)) throw new Error('absolute evidence path');
      const unresolvedPath = path.resolve(evidenceRoot, entry.path);
      const unresolvedRelative = path.relative(evidenceRoot, unresolvedPath);
      if (unresolvedRelative.startsWith('..') || path.isAbsolute(unresolvedRelative)) {
        throw new Error('outside evidence root');
      }
      let cursor = evidenceRoot;
      for (const component of unresolvedRelative.split(path.sep).filter(Boolean)) {
        cursor = path.join(cursor, component);
        if ((await lstat(cursor)).isSymbolicLink()) throw new Error('symlinked evidence path');
      }
      const absolutePath = await realpath(unresolvedPath);
      const relativePath = path.relative(evidenceRoot, absolutePath);
      if (relativePath.startsWith('..') || path.isAbsolute(relativePath)) throw new Error('outside evidence root');
      if (seenCanonicalPaths.has(absolutePath)) throw new Error('duplicate canonical evidence path');
      seenCanonicalPaths.add(absolutePath);
      const metadata = await stat(absolutePath);
      const fileObject = `${metadata.dev}:${metadata.ino}`;
      if (seenFileObjects.has(fileObject)) throw new Error('duplicate evidence file object');
      seenFileObjects.add(fileObject);
      const retainedBytes = await readFile(absolutePath);
      const sha256 = createHash('sha256').update(retainedBytes).digest('hex');
      const record = entry.path.endsWith('.json') ? parseJsonNoDuplicates(retainedBytes.toString('utf8')) : null;
      const artifactContentPass = entry?.artifactType !== 'pdf-fixture' ||
        retainedBytes.subarray(0, 5).toString('ascii') === '%PDF-';
      files.push({ path: entry.path, sha256, bytes: metadata.size, artifactType: entry.artifactType, record,
        pass: metadata.isFile() && sha256 === entry.sha256 && metadata.size === entry.bytes && artifactContentPass });
    } catch (error) {
      files.push({ path: entry?.path ?? null, pass: false,
        error: error instanceof Error ? error.message : String(error) });
    }
  }
  return { files, pass: files.length > 0 && files.every((entry) => entry.pass) };
}

function isNonNullJson(value) {
  if (value === null || value === undefined) return false;
  if (Array.isArray(value)) return value.every(isNonNullJson);
  if (typeof value === 'object') return Object.values(value).every(isNonNullJson);
  return ['string', 'number', 'boolean'].includes(typeof value);
}

async function verifyRelativeFile(root, entry, key = 'relativePath') {
  if (!hasExactKeys(entry, [key, 'sha256', 'bytes']) || typeof entry[key] !== 'string' ||
      entry[key].length === 0 || path.isAbsolute(entry[key]) || !SHA256_PATTERN.test(entry.sha256) ||
      !Number.isSafeInteger(entry.bytes) || entry.bytes <= 0) return { ...entry, pass: false };
  try {
    const unresolved = path.resolve(root, entry[key]);
    const relative = path.relative(root, unresolved);
    if (relative.startsWith('..') || path.isAbsolute(relative)) throw new Error('outside identity root');
    let cursor = root;
    for (const component of relative.split(path.sep).filter(Boolean)) {
      cursor = path.join(cursor, component);
      if ((await lstat(cursor)).isSymbolicLink()) throw new Error('symlinked identity path');
    }
    const metadata = await stat(unresolved);
    const sha256 = await sha256File(unresolved);
    return { ...entry, actualSha256: sha256, actualBytes: metadata.size,
      fileObject: `${metadata.dev}:${metadata.ino}`,
      pass: metadata.isFile() && sha256 === entry.sha256 && metadata.size === entry.bytes };
  } catch (error) {
    return { ...entry, pass: false, error: error instanceof Error ? error.message : String(error) };
  }
}

async function verifyAbsoluteFile(entry) {
  if (!hasExactKeys(entry, ['path', 'sha256', 'bytes']) || typeof entry.path !== 'string' ||
      !path.isAbsolute(entry.path) || !SHA256_PATTERN.test(entry.sha256) ||
      !Number.isSafeInteger(entry.bytes) || entry.bytes <= 0) return { ...entry, pass: false };
  try {
    if ((await lstat(entry.path)).isSymbolicLink()) throw new Error('symlink identity path');
    const metadata = await stat(entry.path);
    const sha256 = await sha256File(entry.path);
    return { ...entry, actualSha256: sha256, actualBytes: metadata.size,
      fileObject: `${metadata.dev}:${metadata.ino}`,
      pass: metadata.isFile() && sha256 === entry.sha256 && metadata.size === entry.bytes };
  } catch (error) {
    return { ...entry, pass: false, error: error instanceof Error ? error.message : String(error) };
  }
}

function sameFileIdentity(left, right) {
  return left?.sha256 === right?.sha256 && left?.bytes === right?.bytes;
}

function patchPaths(patchText) {
  return patchText.split(/\r?\n/).flatMap((line) => {
    const match = line.match(/^diff --git a\/(.+) b\/(.+)$/);
    return match && match[1] === match[2] ? [match[1]] : [];
  });
}

export function sourceRevisionBindingPass(acceptedBase, manifestBase, captureRevision, expectedRevision) {
  return typeof acceptedBase === 'string' && acceptedBase.length > 0 &&
    acceptedBase === manifestBase && acceptedBase === captureRevision && acceptedBase === expectedRevision;
}

async function verifySourceBinding(capture, capturePath, acceptedSourceBindingPath, expectedSourceRevision) {
  const errors = [];
  let manifest = null;
  let accepted = null;
  if (capture?.source?.acceptedBindingRef?.artifactType !== 'accepted-source-binding' ||
      capture?.source?.patchRef?.artifactType !== 'accepted-source-patch' ||
      capture?.source?.manifestRef?.artifactType !== 'accepted-source-manifest') {
    errors.push('source binding, patch, or manifest artifact type mismatch');
  }
  try {
    const bindingMetadata = await lstat(acceptedSourceBindingPath);
    if (bindingMetadata.isSymbolicLink() || !bindingMetadata.isFile() || bindingMetadata.size === 0) {
      throw new Error('accepted source binding is not a nonempty regular nonsymlink file');
    }
    const capturedBindingPath = path.resolve(path.dirname(capturePath), capture.source.acceptedBindingRef.path);
    if (await realpath(capturedBindingPath) !== await realpath(acceptedSourceBindingPath)) {
      throw new Error('capture source binding does not name the independently supplied binding');
    }
    const bindingBytes = await readFile(acceptedSourceBindingPath);
    if (createHash('sha256').update(bindingBytes).digest('hex') !== capture.source.acceptedBindingRef.sha256 ||
        bindingBytes.length !== capture.source.acceptedBindingRef.bytes) {
      throw new Error('accepted source binding identity drift');
    }
    accepted = parseJsonNoDuplicates(bindingBytes.toString('utf8'));
    if (!hasExactKeys(accepted, [
      'schema', 'baseCommit', 'patchSha256', 'manifestSha256', 'pathCount', 'members'
    ]) || accepted.schema !== 'chirality-accepted-source-binding/v1' ||
        typeof accepted.baseCommit !== 'string' || accepted.baseCommit.length === 0 ||
        accepted.patchSha256 !== capture.source.patchRef.sha256 ||
        accepted.manifestSha256 !== capture.source.manifestRef.sha256 ||
        !Number.isSafeInteger(accepted.pathCount) || accepted.pathCount <= 0 ||
        !Array.isArray(accepted.members) || accepted.pathCount !== accepted.members.length) {
      errors.push('accepted source binding identity or closed shape mismatch');
    }
    const patchBytes = await readCaptureMember(capturePath, capture.source.patchRef);
    const declaredPaths = patchPaths(patchBytes.toString('utf8'));
    manifest = parseJsonNoDuplicates(await readCaptureMember(capturePath, capture.source.manifestRef, 'utf8'));
    if (!hasExactKeys(manifest, ['schema', 'baseCommit', 'patchSha256', 'members']) ||
        manifest.schema !== 'chirality-d121-qualified-source-manifest/v1' ||
        manifest.baseCommit !== accepted?.baseCommit ||
        manifest.patchSha256 !== capture.source.patchRef.sha256) {
      errors.push('source manifest identity or closed shape mismatch');
    }
    if (!sourceRevisionBindingPass(
      accepted?.baseCommit, manifest?.baseCommit, capture?.source?.revision, expectedSourceRevision
    )) errors.push('accepted, manifest, capture, and CLI source revisions do not match');
    if (!sameStructuredValue(declaredPaths, accepted?.members?.map((entry) => entry.relativePath))) {
      errors.push('source patch does not name the exact independently accepted path set');
    }
  } catch (error) {
    errors.push(`source binding, patch, or manifest unreadable: ${error instanceof Error ? error.message : String(error)}`);
  }
  const sourceMembers = Array.isArray(capture?.source?.members) ? capture.source.members : [];
  const memberPaths = sourceMembers.map((entry) => entry?.relativePath);
  if (new Set(memberPaths).size !== memberPaths.length ||
      !sameStructuredValue(sourceMembers, accepted?.members)) {
    errors.push('source members do not exactly match the independently accepted path/hash/size set');
  }
  if (!Array.isArray(manifest?.members) || !sameStructuredValue(manifest.members, sourceMembers)) {
    errors.push('source manifest members do not exactly bind capture source members');
  }
  const checks = await Promise.all(sourceMembers.map((entry) => verifyRelativeFile(capture.source.root, entry)));
  if (!checks.every((entry) => entry.pass)) errors.push('source member identity drift');
  return { accepted, manifest, checks, errors, pass: errors.length === 0 };
}

/** Parse JSON with duplicate decoded keys rejected at every nesting level. */
export function parseJsonNoDuplicates(text) {
  let i = 0;
  const whitespace = () => { while (/\s/.test(text[i] ?? '') && i < text.length) i++; };
  const string = () => {
    const start = i++;
    while (i < text.length) {
      if (text[i] === '\\') { i += 2; continue; }
      if (text[i++] === '"') return JSON.parse(text.slice(start, i));
    }
    throw new Error('unterminated JSON string');
  };
  const value = () => {
    whitespace();
    if (text[i] === '{') {
      i++; whitespace(); const keys = new Set();
      if (text[i] === '}') { i++; return; }
      while (i < text.length) {
        whitespace(); if (text[i] !== '"') throw new Error('JSON object key required');
        const key = string(); if (keys.has(key)) throw new Error('duplicate JSON key'); keys.add(key);
        whitespace(); if (text[i++] !== ':') throw new Error('JSON colon required'); value(); whitespace();
        const next = text[i++]; if (next === '}') return;
        if (next !== ',') throw new Error('JSON object separator required');
      }
    } else if (text[i] === '[') {
      i++; whitespace(); if (text[i] === ']') { i++; return; }
      while (i < text.length) { value(); whitespace(); const next = text[i++];
        if (next === ']') return; if (next !== ',') throw new Error('JSON array separator required'); }
    } else if (text[i] === '"') { string(); return; }
    else {
      const start = i; while (i < text.length && !/[\s,}\]]/.test(text[i])) i++;
      if (i === start) throw new Error('JSON value required');
      JSON.parse(text.slice(start, i)); return;
    }
    throw new Error('incomplete JSON');
  };
  value(); whitespace(); if (i !== text.length) throw new Error('trailing JSON');
  return JSON.parse(text);
}

const pathOrder = (a, b) => a.relativePath < b.relativePath ? -1 : a.relativePath > b.relativePath ? 1 : 0;
export function packageIdentitySha256(compatibilityIdentitySha256, members) {
  return createHash('sha256').update(JSON.stringify({ compatibilityIdentitySha256,
    members: [...members].sort(pathOrder) })).digest('hex');
}

/** Physical entries only; links are resolved component by component, never followed by the walker.
 * Directory target identities hash their physical subtree (including raw links), avoiding recursive hashes.
 * The directory/link graph must be acyclic. Required role identities still use no-link regular paths.
 */
export async function inventoryPackage(appPath) {
  if (await realpath(appPath) !== appPath || !(await lstat(appPath)).isDirectory()) {
    throw new Error('package root must be a canonical directory');
  }
  const basic = [];
  const walk = async (relative = '') => {
    for (const name of (await readdir(path.join(appPath, relative))).sort()) {
      const relativePath = path.posix.join(relative, name);
      const absolute = path.join(appPath, relativePath); const info = await lstat(absolute);
      const mode = info.mode & 0o7777;
      if (info.isSymbolicLink()) basic.push({ relativePath, kind: 'symlink', mode, linkText: await readlink(absolute) });
      else if (info.isDirectory()) { basic.push({ relativePath, kind: 'directory', mode }); await walk(relativePath); }
      else if (info.isFile()) basic.push({ relativePath, kind: 'file', mode, sha256: await sha256File(absolute), bytes: info.size });
      else throw new Error(`unsupported live package member: ${relativePath}`);
    }
  };
  await walk(); basic.sort(pathOrder);
  const byPath = new Map(basic.map(row => [row.relativePath, row]));
  const resolveLink = row => {
    let parts = row.relativePath.split('/').slice(0, -1), pending = row.linkText.split('/');
    const followed = new Set([row.relativePath]);
    if (!row.linkText || path.isAbsolute(row.linkText)) throw new Error('absolute or empty package link');
    while (pending.length) {
      const part = pending.shift();
      if (part === '' || part === '.') continue;
      if (part === '..') { if (!parts.length) throw new Error('escaping package link'); parts.pop(); continue; }
      parts.push(part); const key = parts.join('/'); const member = byPath.get(key);
      if (!member) throw new Error('dangling or unlisted package link component');
      if (member.kind === 'symlink') {
        if (followed.has(key)) throw new Error('cyclic package link'); followed.add(key);
        if (!member.linkText || path.isAbsolute(member.linkText)) throw new Error('absolute or empty package link component');
        parts.pop(); pending = [...member.linkText.split('/'), ...pending];
      } else if (pending.length && member.kind !== 'directory') throw new Error('non-directory package link component');
    }
    return parts.join('/');
  };
  const targets = new Map(basic.filter(row => row.kind === 'symlink').map(row => [row.relativePath, resolveLink(row)]));
  const edges = new Map([['', []], ...basic.filter(row => row.kind === 'directory').map(row => [row.relativePath, []])]);
  for (const row of basic) {
    const target = row.kind === 'symlink' ? targets.get(row.relativePath) : row.relativePath;
    if (edges.has(target)) edges.get(row.relativePath.split('/').slice(0, -1).join('/')).push(target);
  }
  const active = new Set(), done = new Set();
  const visit = dir => {
    if (active.has(dir)) throw new Error('cyclic package directory link'); if (done.has(dir)) return;
    active.add(dir); for (const child of edges.get(dir)) visit(child); active.delete(dir); done.add(dir);
  };
  visit('');
  const identity = target => {
    const row = byPath.get(target);
    if (!row) throw new Error('unlisted package link target');
    if (row.kind === 'file') return { relativePath: target, kind: row.kind, mode: row.mode, sha256: row.sha256, bytes: row.bytes };
    const subtree = basic.filter(item => item.relativePath.startsWith(`${target}/`));
    return { relativePath: target, kind: 'directory', mode: row.mode,
      sha256: createHash('sha256').update(JSON.stringify(subtree)).digest('hex'),
      bytes: subtree.reduce((total, item) => total + (item.kind === 'file' ? item.bytes : 0), 0) };
  };
  return basic.map(row => row.kind === 'symlink' ? { ...row, resolvedTarget: identity(targets.get(row.relativePath)) } : row);
}

export async function verifyPackageBinding(capture, capturePath) {
  const errors = [];
  let inventory = null;
  if (capture?.package?.inventoryRef?.artifactType !== 'reviewed-package-inventory') {
    errors.push('package inventory artifact type mismatch');
  }
  try {
    inventory = parseJsonNoDuplicates(await readCaptureMember(capturePath, capture.package.inventoryRef, 'utf8'));
  } catch (error) {
    errors.push(`package inventory unreadable: ${error instanceof Error ? error.message : String(error)}`);
  }
  if (!hasExactKeys(inventory, ['schema', 'compatibilityIdentitySha256', 'members']) ||
      inventory?.schema !== 'chirality-reviewed-package-inventory/v2' ||
      inventory?.compatibilityIdentitySha256 !== capture?.package?.compatibilityIdentitySha256 ||
      !Array.isArray(inventory?.members) || inventory.members.length === 0) {
    errors.push('package inventory identity or closed shape mismatch');
  }
  const members = Array.isArray(inventory?.members) ? inventory.members : [];
  const paths = members.map((entry) => entry?.relativePath);
  if (new Set(paths).size !== paths.length || !sameStructuredValue(paths, [...paths].sort())) {
    errors.push('package inventory paths must be unique and sorted');
  }
  let liveMembers = [];
  try { liveMembers = await inventoryPackage(capture.package.appPath); } catch (error) {
    errors.push(`live package inventory unreadable: ${error instanceof Error ? error.message : String(error)}`);
  }
  const checks = members.map(entry => ({ ...entry,
    pass: sameStructuredValue(entry, liveMembers.find(row => row.relativePath === entry.relativePath)) }));
  if (!checks.every(entry => entry.pass)) errors.push('live package inventory drift');
  if (!sameStructuredValue(liveMembers, members)) errors.push('inventory is not the complete admitted live package tree');
  const artifactIdentitySha256 = packageIdentitySha256(
    capture?.package?.compatibilityIdentitySha256, liveMembers
  );
  if (artifactIdentitySha256 !== capture?.package?.artifactIdentitySha256) {
    errors.push('self-declared package artifact identity does not match recomputed live inventory');
  }
  const inventoryByAbsolutePath = new Map(members.map((entry) => [
    path.resolve(capture.package.appPath, entry.relativePath), entry
  ]));
  let canonicalAppRoot = null;
  try {
    canonicalAppRoot = await realpath(capture.package.appPath);
  } catch (error) {
    errors.push(`package app root is not canonical: ${error instanceof Error ? error.message : String(error)}`);
  }
  for (const [role, identity] of Object.entries(capture?.identities ?? {})) {
    const relativePath = D121_PACKAGE_IDENTITY_RELATIVE_PATHS[role];
    const requiredPath = relativePath && canonicalAppRoot
      ? path.join(canonicalAppRoot, ...relativePath.split('/')) : null;
    let identityRealpath = null;
    try { identityRealpath = await realpath(identity?.path ?? ''); } catch {}
    if (!requiredPath || identity?.path !== requiredPath || identityRealpath !== requiredPath) {
      errors.push(`package identity role path mismatch: ${role}`);
    }
    if (inventoryByAbsolutePath.get(identity?.path)?.kind !== 'file' ||
        !sameFileIdentity(identity, inventoryByAbsolutePath.get(identity?.path)) ||
        !(await verifyRelativeFile(canonicalAppRoot, { relativePath, sha256: identity?.sha256, bytes: identity?.bytes })).pass) {
      errors.push(`package identity is absent from full inventory: ${identity?.path ?? '<missing>'}`);
    }
  }
  return { inventory, checks, artifactIdentitySha256, errors, pass: errors.length === 0 };
}

/** Admit and rehash the coordinator's immutable, closed consume-only subject. */
export async function verifyCapturedInput(capture, capturePath, expected) {
  const captureRoot = await realpath(path.dirname(capturePath));
  const errors = [];
  const exact = (value, keys, label) => {
    if (!hasExactKeys(value, keys)) errors.push(`${label} has missing or unknown fields`);
  };
  exact(capture, CAPTURE_KEYS, 'capture');
  exact(capture?.source, [
    'root', 'revision', 'acceptedBindingRef', 'patchRef', 'manifestRef', 'members'
  ], 'source');
  exact(capture?.package, [
    'appPath', 'artifactIdentitySha256', 'compatibilityIdentitySha256', 'inventoryRef'
  ], 'package');
  exact(capture?.authorities, [
    'coordinatorRef', 'configRef', 'grantRef', 'packageReviewRef', 'nativeReleaseRef'
  ], 'authorities');
  exact(capture?.fixtures, ['positive', 'derived'], 'fixtures');
  exact(capture?.identities, [
    'executable', 'appAsar', 'runtimeCli', 'unpackedSdkPackage', 'unpackedSdkBinary'
  ], 'identities');
  exact(capture?.execution, [
    'toolIdentities', 'argvIdentities', 'cleanEnvironmentIdentities', 'processGroups',
    'descendantHistory', 'endpointHistory', 'startedAt', 'completedAt'
  ], 'execution');
  exact(capture?.artifacts, [
    'packagedMainRef', 'daemonLogRef', 'guiLogRef', 'tcpSnapshotsRef',
    's0SecurityEvidenceRef', 'uiRefs', 'httpRefs', 'sourceComponentRefs', 'generalRefs'
  ], 'artifacts');
  exact(capture?.credential, ['mutationResultRef', 'postCloseSecretScanRef'], 'credential');
  exact(capture?.cleanup, ['evidenceRef', 'pass'], 'cleanup');
  exact(capture?.evidenceMatrix, ['observations', 'controls'], 'evidenceMatrix');
  if (capture?.schema !== CAPTURE_SCHEMA) errors.push('wrong capture schema');
  if (!isNonNullJson(capture)) errors.push('capture contains null or unsupported values');
  if (capture?.runId !== expected.runId || capture?.source?.revision !== expected.sourceRevision ||
      capture?.package?.appPath !== expected.appPath) errors.push('capture subject identity drift');
  for (const key of ['artifactIdentitySha256', 'compatibilityIdentitySha256']) {
    if (!SHA256_PATTERN.test(capture?.package?.[key] ?? '')) errors.push(`invalid package ${key}`);
  }
  if (!path.isAbsolute(capture?.source?.root ?? '') || !path.isAbsolute(capture?.package?.appPath ?? '')) {
    errors.push('source and package roots must be absolute');
  }
  const referenceGroups = [
    capture?.source?.acceptedBindingRef, capture?.source?.patchRef, capture?.source?.manifestRef,
    ...Object.values(capture?.authorities ?? {}), capture?.package?.inventoryRef,
    capture?.artifacts?.packagedMainRef, capture?.artifacts?.daemonLogRef,
    capture?.artifacts?.guiLogRef, capture?.artifacts?.tcpSnapshotsRef,
    capture?.artifacts?.s0SecurityEvidenceRef, ...(capture?.artifacts?.uiRefs ?? []),
    ...(capture?.artifacts?.httpRefs ?? []), ...(capture?.artifacts?.sourceComponentRefs ?? []),
    ...(capture?.artifacts?.generalRefs ?? []),
    capture?.credential?.mutationResultRef, capture?.credential?.postCloseSecretScanRef,
    capture?.cleanup?.evidenceRef,
    ...(capture?.execution?.descendantHistory ?? []).map((entry) => entry?.snapshotsRef),
    ...(capture?.execution?.endpointHistory ?? []).map((entry) => entry?.snapshotsRef),
    ...(capture?.evidenceMatrix?.observations ?? []).map((row) => row?.recordRef),
    ...(capture?.evidenceMatrix?.controls ?? []).map((row) => row?.recordRef)
  ];
  if (!referenceGroups.every(validReference)) errors.push('invalid capture artifact reference');
  const memberEnvelope = { evidenceFiles: capture?.members };
  const memberVerification = await verifyD121EvidenceFiles(memberEnvelope, capturePath);
  const memberByIdentity = new Map(memberVerification.files.map((entry) => [
    `${entry.path}\0${entry.sha256}\0${entry.bytes}\0${entry.artifactType}`, entry
  ]));
  for (const reference of referenceGroups.filter(validReference)) {
    if (!memberByIdentity.get(
      `${reference.path}\0${reference.sha256}\0${reference.bytes}\0${reference.artifactType}`
    )?.pass) {
      errors.push(`unbound capture reference: ${reference.path}`);
    }
  }
  const sourceBinding = await verifySourceBinding(
    capture, capturePath, expected.acceptedSourceBindingPath, expected.sourceRevision
  );
  errors.push(...sourceBinding.errors);
  const sourceChecks = sourceBinding.checks;
  const packageBinding = await verifyPackageBinding(capture, capturePath);
  errors.push(...packageBinding.errors);
  const identityChecks = await Promise.all(Object.values(capture?.identities ?? {}).map(verifyAbsoluteFile));
  if (identityChecks.length !== 5 || !identityChecks.every((entry) => entry.pass)) {
    errors.push('executable/package identity drift');
  }
  if (new Set(identityChecks.map((entry) => entry.fileObject)).size !== identityChecks.length) {
    errors.push('executable/package identities must be distinct regular file objects');
  }
  for (const key of ['toolIdentities', 'argvIdentities', 'cleanEnvironmentIdentities', 'processGroups',
    'descendantHistory', 'endpointHistory']) {
    if (!Array.isArray(capture?.execution?.[key]) || capture.execution[key].length === 0) {
      errors.push(`missing execution ${key}`);
    }
  }
  const closedArray = (items, keys, label) => {
    if (!Array.isArray(items) || !items.every((entry) => hasExactKeys(entry, keys))) {
      errors.push(`${label} contains missing or unknown fields`);
    }
  };
  closedArray(capture?.execution?.toolIdentities, ['id', 'path', 'sha256', 'bytes', 'version'], 'tool identities');
  closedArray(capture?.execution?.argvIdentities, ['id', 'cwd', 'argv', 'environmentIdentity'], 'argv identities');
  closedArray(capture?.execution?.cleanEnvironmentIdentities, ['id', 'keys', 'valuesSha256'], 'environment identities');
  closedArray(capture?.execution?.processGroups,
    ['lifecycle', 'rootPid', 'processGroupId', 'sessionId'], 'process groups');
  closedArray(capture?.execution?.descendantHistory, ['lifecycle', 'snapshotsRef'], 'descendant history');
  closedArray(capture?.execution?.endpointHistory, ['lifecycle', 'snapshotsRef'], 'endpoint history');
  if (!(capture?.execution?.toolIdentities ?? []).every((entry) => path.isAbsolute(entry.path) &&
      SHA256_PATTERN.test(entry.sha256) && Number.isSafeInteger(entry.bytes) && entry.bytes > 0)) {
    errors.push('invalid tool identity');
  }
  const toolIdentityChecks = await Promise.all((capture?.execution?.toolIdentities ?? []).map((entry) =>
    verifyAbsoluteFile({ path: entry.path, sha256: entry.sha256, bytes: entry.bytes })));
  if (!toolIdentityChecks.every((entry) => entry.pass)) errors.push('tool identity drift');
  if (!(capture?.execution?.argvIdentities ?? []).every((entry) => path.isAbsolute(entry.cwd) &&
      Array.isArray(entry.argv) && entry.argv.length > 0 && entry.argv.every((arg) => typeof arg === 'string'))) {
    errors.push('invalid argv identity');
  }
  if (!(capture?.execution?.cleanEnvironmentIdentities ?? []).every((entry) =>
      Array.isArray(entry.keys) && new Set(entry.keys).size === entry.keys.length &&
      SHA256_PATTERN.test(entry.valuesSha256))) errors.push('invalid clean environment identity');
  if (!(capture?.execution?.processGroups ?? []).every((entry) =>
      ['package', 'lifecycle-1', 'lifecycle-2', 'worker'].includes(entry.lifecycle) &&
      [entry.rootPid, entry.processGroupId, entry.sessionId].every((value) => Number.isSafeInteger(value) && value > 0))) {
    errors.push('invalid process-group identity');
  }
  for (const key of ['uiRefs', 'httpRefs', 'sourceComponentRefs', 'generalRefs']) {
    if (!Array.isArray(capture?.artifacts?.[key]) || capture.artifacts[key].length === 0) {
      errors.push(`missing typed artifact group ${key}`);
    }
  }
  if (!Array.isArray(capture?.fixtures?.derived) || capture.fixtures.derived.length !== 4 ||
      !hasExactKeys(capture?.fixtures?.positive, ['id', 'path', 'sha256', 'bytes', 'pageCount'])) {
    errors.push('missing exact fixture identities');
  }
  const fixtures = [capture?.fixtures?.positive, ...(capture?.fixtures?.derived ?? [])];
  if (!sameStructuredValue(fixtures.map((fixture) => fixture?.id), D121_FIXTURE_ROLES)) {
    errors.push('fixture roles do not match the exact five-role contract');
  }
  const fixtureObjects = [];
  for (const fixture of fixtures) {
    if (!hasExactKeys(fixture, ['id', 'path', 'sha256', 'bytes', 'pageCount']) ||
        !path.isAbsolute(fixture.path) || !SHA256_PATTERN.test(fixture.sha256) ||
        !Number.isSafeInteger(fixture.bytes) || fixture.bytes < 0 ||
        !Number.isSafeInteger(fixture.pageCount) || fixture.pageCount < 0) {
      errors.push('invalid fixture identity');
      break;
    }
    try {
      const object = await lstat(fixture.path);
      const content = await readFile(fixture.path);
      if (!object.isFile() || content.length !== fixture.bytes ||
          createHash('sha256').update(content).digest('hex') !== fixture.sha256) {
        errors.push(`fixture content drift: ${fixture.id}`);
      }
      fixtureObjects.push(`${object.dev}:${object.ino}`);
    } catch (error) {
      errors.push(`fixture unreadable: ${fixture.id}`);
    }
  }
  if (new Set(fixtures.map((fixture) => fixture?.path)).size !== fixtures.length ||
      new Set(fixtureObjects).size !== fixtures.length) {
    errors.push('fixture roles must be distinct paths and file objects');
  }
  if (!/^[a-f0-9]{12}$/.test(capture?.runId ?? '')) errors.push('invalid runId');
  const checkRows = (rows, requiredIds, origins, label) => {
    if (!Array.isArray(rows) || rows.length !== requiredIds.length) {
      errors.push(`${label} row count mismatch`);
      return;
    }
    const byId = new Map(rows.map((row) => [row?.id, row]));
    if (byId.size !== requiredIds.length || !requiredIds.every((id) => {
      const row = byId.get(id);
      return hasExactKeys(row, ['id', 'origin', 'recordRef']) && row.origin === origins[id] &&
        validReference(row.recordRef);
    })) errors.push(`${label} IDs, origins, or row shape mismatch`);
  };
  checkRows(capture?.evidenceMatrix?.observations, D121_REQUIRED_OBSERVATIONS,
    D121_OBSERVATION_ORIGINS, 'observation');
  checkRows(capture?.evidenceMatrix?.controls, D121_REQUIRED_NEGATIVE_CONTROLS,
    D121_CONTROL_ORIGINS, 'control');
  if (capture?.cleanup?.pass !== true) errors.push('cleanup is not proven');
  return { schema: 'chirality-d121-s0-capture-admission/v1', errors, memberVerification,
    sourceChecks, sourceBinding, packageBinding, identityChecks, toolIdentityChecks,
    pass: errors.length === 0 && memberVerification.pass };
}

export function inspectPackagedPolicyMarkers(packagedMain) {
  const markers = PACKAGED_POLICY_MARKERS.map((marker) => ({
    marker,
    present: packagedMain.includes(marker)
  }));
  return {
    markers,
    allPresent: markers.every((entry) => entry.present)
  };
}

function parseProcessTable(output) {
  return output.split(/\r?\n/).flatMap((line) => {
    const match = line.match(/^\s*(\d+)\s+(\d+)\s+(.*)$/);
    return match ? [{ pid: Number(match[1]), ppid: Number(match[2]), command: match[3] }] : [];
  });
}

export function descendantProcessIds(processRows, roots) {
  const selected = new Set(roots.filter((pid) => Number.isSafeInteger(pid) && pid > 0));
  let changed = true;
  while (changed) {
    changed = false;
    for (const row of processRows) {
      if (selected.has(row.ppid) && !selected.has(row.pid)) {
        selected.add(row.pid);
        changed = true;
      }
    }
  }
  return [...selected].sort((left, right) => left - right);
}

function parseRemoteHost(endpoint) {
  if (endpoint.startsWith('[')) {
    const close = endpoint.indexOf(']');
    return close > 0 ? endpoint.slice(1, close) : endpoint;
  }
  const colon = endpoint.lastIndexOf(':');
  return colon > 0 ? endpoint.slice(0, colon) : endpoint;
}

export function parseLsofOutbound(output) {
  return output.split(/\r?\n/).flatMap((line) => {
    const arrow = line.indexOf('->');
    if (arrow === -1) return [];
    const endpoint = line.slice(arrow + 2).trim().split(/\s+/)[0] ?? '';
    const host = parseRemoteHost(endpoint).toLowerCase();
    return [{
      endpoint,
      host,
      class: LOOPBACK_HOSTS.has(host) ? 'loopback' : 'external-non-allowlisted',
      line
    }];
  });
}

function extractMarkedPayloads(logText, marker) {
  return logText.split(/\r?\n/).flatMap((line) => {
    const index = line.indexOf(marker);
    if (index === -1) return [];
    try {
      return [parseJsonNoDuplicates(line.slice(index + marker.length).trim())];
    } catch {
      return [{ parseError: true }];
    }
  });
}

function extractProbePayloads(logText) {
  return extractMarkedPayloads(logText, '[network-policy-probe]');
}

function probeResultFailed(probePayloads, url) {
  return probePayloads.some((payload) =>
    Array.isArray(payload.results) && payload.results.some((result) =>
      result.url === url && result.ok === false
    )
  );
}

export function summarizeNetworkEvidence(logText, snapshots) {
  const blockedDiagnostics = (logText.match(/Blocked renderer outbound request by network policy/g) ?? []).length;
  const egressDiagnostics = (logText.match(/anthropic_port_not_allowlisted:8443/g) ?? []).length;
  const probePayloads = extractProbePayloads(logText);
  const endpoints = snapshots.flatMap((snapshot) => snapshot.endpoints ?? []);
  const unique = [...new Map(endpoints.map((entry) => [entry.endpoint, entry])).values()];
  const nonAllowlisted = unique.filter((entry) => entry.class !== 'loopback');
  const blockedProbeObserved = probeResultFailed(probePayloads, BLOCKED_PROBE_URL);
  const loopbackProbeObserved = probeResultFailed(probePayloads, LOOPBACK_PROBE_URL);
  const egressPayloads = extractMarkedPayloads(logText, '[egress-layer-probe]');
  const expectedEgressDestination = (payload) =>
    payload?.destination?.protocol === EGRESS_PROBE_DESTINATION.protocol &&
    payload?.destination?.hostname === EGRESS_PROBE_DESTINATION.hostname &&
    payload?.destination?.port === EGRESS_PROBE_DESTINATION.port;
  const egressProbeObserved = egressPayloads.some(
    (payload) =>
      payload?.policy === 'REQ-NET-001' &&
      expectedEgressDestination(payload) &&
      payload?.outcome === 'rejected'
  );
  // The probe's destination is fixed in the app; a payload naming any other
  // destination (for example the decoy) means the app took a URL from outside.
  const egressProbeUnexpectedDestinations = egressPayloads
    .filter((payload) => !expectedEgressDestination(payload))
    .map((payload) => payload?.destination ?? null);
  return {
    snapshotCount: snapshots.length,
    sampledProcessIds: [...new Set(snapshots.flatMap((snapshot) => snapshot.pids ?? []))].sort(),
    uniqueOutboundTcp: unique.map(({ line: _line, ...entry }) => entry),
    nonAllowlistedOutboundTcp: nonAllowlisted.map(({ line: _line, ...entry }) => entry),
    blockedRendererDiagnostics: blockedDiagnostics,
    egressLayerDiagnostics: egressDiagnostics,
    probePayloadCount: probePayloads.length,
    egressProbePayloadCount: egressPayloads.length,
    blockedProbeObserved,
    loopbackProbeObserved,
    egressProbeObserved,
    egressProbeUnexpectedDestinations,
    pass:
      snapshots.length > 0 &&
      nonAllowlisted.length === 0 &&
      blockedDiagnostics > 0 &&
      egressDiagnostics > 0 &&
      blockedProbeObserved &&
      loopbackProbeObserved &&
      egressProbeObserved &&
      egressProbeUnexpectedDestinations.length === 0
  };
}

/**
 * Renderer hardening evidence (G-CSP): the document's CSP header as the page
 * itself sees it, a denied window.open, the CSP violation raised by a blocked
 * fetch, the main-process denial lines, and — as important — no violation
 * against the app's own resources.
 */
export function summarizeRendererSecurityEvidence(logText) {
  const payloads = extractMarkedPayloads(logText, '[renderer-security-probe]');
  const validPayloads = payloads.filter(
    (entry) => entry && entry.policy === 'G-CSP' && !entry.error && typeof entry.route === 'string'
  );
  const expectedViolation = (violation) =>
    typeof violation?.blockedURI === 'string' &&
    violation.blockedURI.startsWith('https://example.com') &&
    violation.effectiveDirective === 'connect-src' &&
    violation.disposition === 'enforce';
  const inspectPolicy = (cspHeader) => {
    const directives = typeof cspHeader === 'string'
      ? cspHeader.split(';').map((directive) => directive.trim())
      : [];
    const scriptDirective = directives.find((directive) => directive.startsWith('script-src ')) ?? '';
    const scriptSources = scriptDirective.split(/\s+/).slice(1);
    const nonceSources = scriptSources.filter((source) => /^'nonce-[A-Za-z0-9+/_-]+={0,2}'$/.test(source));
    const unsafeInlineAbsent = !scriptSources.includes("'unsafe-inline'");
    const unsafeEvalAbsent = !scriptSources.includes("'unsafe-eval'");
    return {
      header: typeof cspHeader === 'string' ? cspHeader : null,
      nonce: nonceSources.length === 1 ? nonceSources[0].slice(7, -1) : null,
      unsafeInlineAbsent,
      unsafeEvalAbsent,
      pass:
        directives.includes("default-src 'self'") &&
        directives.includes("connect-src 'self'") &&
        directives.includes("frame-src 'none'") &&
        directives.includes("object-src 'none'") &&
        scriptSources.includes("'self'") &&
        nonceSources.length === 1 &&
        unsafeInlineAbsent &&
        unsafeEvalAbsent
    };
  };
  const routeResults = PACKAGED_RENDERER_ROUTES.map((route) => {
    const matches = validPayloads.filter((entry) => entry.route === route);
    const payload = matches.length === 1 ? matches[0] : null;
    const responses = Array.isArray(payload?.consecutiveResponses)
      ? payload.consecutiveResponses
      : [];
    const responsePolicies = responses.map((response) => inspectPolicy(response?.cspHeader));
    const responseNonces = responsePolicies.map((policy) => policy.nonce);
    const violations = Array.isArray(payload?.violations) ? payload.violations : [];
    const expectedConnectViolation = violations.some(expectedViolation);
    const unexpected = violations.filter((violation) => !expectedViolation(violation));
    const consecutiveNoncesUnique =
      responseNonces.length === 2 &&
      responseNonces.every((nonce) => typeof nonce === 'string') &&
      responseNonces[0] !== responseNonces[1];
    const scriptUnsafeInlineAbsent =
      responsePolicies.length === 2 && responsePolicies.every((policy) => policy.unsafeInlineAbsent);
    const scriptUnsafeEvalAbsent =
      responsePolicies.length === 2 && responsePolicies.every((policy) => policy.unsafeEvalAbsent);
    const responsesConform =
      responses.length === 2 &&
      responses.every(
        (response, index) =>
          response?.status === 200 &&
          typeof response?.contentType === 'string' &&
          response.contentType.startsWith('text/html') &&
          response.documentComplete === true &&
          response.inlineScriptCount > 0 &&
          response.inlineScriptNoncesMatch === true &&
          responsePolicies[index]?.pass === true
      );
    return {
      route,
      payloadCount: matches.length,
      documentNonce: payload?.documentNonce ?? null,
      documentInlineScriptCount: payload?.documentInlineScriptCount ?? 0,
      documentInlineScriptNoncesMatch: payload?.documentInlineScriptNoncesMatch === true,
      responseNonces,
      consecutiveNoncesUnique,
      scriptUnsafeInlineAbsent,
      scriptUnsafeEvalAbsent,
      responsesConform,
      expectedConnectViolation,
      unexpectedViolations: unexpected,
      windowOpenReturnedNull: payload?.windowOpen?.returned === 'null',
      navigationAttempted: typeof payload?.navigationAttempted === 'string',
      pass:
        payload !== null &&
        typeof payload.documentNonce === 'string' &&
        payload.documentInlineScriptCount > 0 &&
        payload.documentInlineScriptNoncesMatch === true &&
        payload.responseError === null &&
        consecutiveNoncesUnique &&
        responsesConform &&
        expectedConnectViolation &&
        unexpected.length === 0 &&
        payload.windowOpen?.returned === 'null' &&
        typeof payload.navigationAttempted === 'string'
    };
  });
  const allObservedNonces = routeResults.flatMap((result) => [
    result.documentNonce,
    ...result.responseNonces
  ]).filter((nonce) => typeof nonce === 'string');
  const allObservedNoncesUnique =
    allObservedNonces.length === PACKAGED_RENDERER_ROUTES.length * 3 &&
    new Set(allObservedNonces).size === allObservedNonces.length;
  const unexpectedViolations = routeResults.flatMap((result) =>
    result.unexpectedViolations.map((violation) => ({ route: result.route, violation }))
  );
  const windowOpenDeniedCount = (logText.match(/renderer\.window_open\.denied/g) ?? []).length;
  const navigationDeniedCount = (logText.match(/renderer\.navigation\.denied/g) ?? []).length;
  const cspHeaderPresent = routeResults.every((result) => result.responsesConform);
  const cspViolationObserved = routeResults.every((result) => result.expectedConnectViolation);
  const windowOpenReturnedNull = routeResults.every((result) => result.windowOpenReturnedNull);
  const windowOpenDeniedLogged = windowOpenDeniedCount >= PACKAGED_RENDERER_ROUTES.length;
  const navigationDeniedLogged = navigationDeniedCount >= PACKAGED_RENDERER_ROUTES.length;
  return {
    probePayloadCount: payloads.length,
    requiredRoutes: PACKAGED_RENDERER_ROUTES,
    routeResults,
    allObservedNoncesUnique,
    cspHeaderPresent,
    cspViolationObserved,
    unexpectedViolations,
    windowOpenReturnedNull,
    windowOpenDeniedLogged,
    navigationAttempted: routeResults.every((result) => result.navigationAttempted),
    navigationDeniedLogged,
    pass:
      payloads.length === PACKAGED_RENDERER_ROUTES.length &&
      routeResults.every((result) => result.pass) &&
      allObservedNoncesUnique &&
      cspHeaderPresent &&
      cspViolationObserved &&
      unexpectedViolations.length === 0 &&
      windowOpenReturnedNull &&
      windowOpenDeniedLogged &&
      navigationDeniedLogged
  };
}

export function sensitiveMaterialFindings(text, values) {
  return values.flatMap(({ label, value }) => {
    const variants = [...new Set([value, encodeURIComponent(value)])];
    return variants.flatMap((variant) => text.includes(variant) ? [{ label, sha256: createHash('sha256').update(variant).digest('hex') }] : []);
  });
}

export function credentialProviderIsolation(statuses) {
  return (
    statuses.beforeOmlx.configured === false &&
    statuses.afterStoreOmlx.configured === false &&
    statuses.afterRemoveOmlx.configured === false
  );
}

export function evaluateCredentialEvidence(fixtureCredential, retainedSurfaces) {
  return Object.entries(retainedSurfaces).flatMap(([surface, text]) =>
    sensitiveMaterialFindings(String(text ?? ''), [
      { label: `fixture-credential:${surface}`, value: fixtureCredential }
    ])
  );
}

export function packagedProofPass({
  identityPresent,
  packagedPolicyPass,
  credentialProofPass,
  networkProofPass,
  rendererSecurityProofPass,
  d121SourceProofPass,
  d121S0SecurityProofPass,
  d121S1MatrixStatus,
  cleanupPass,
  metadataLeakFindingCount
}) {
  return (
    identityPresent &&
    packagedPolicyPass &&
    credentialProofPass &&
    networkProofPass &&
    rendererSecurityProofPass === true &&
    d121SourceProofPass === true &&
    d121S0SecurityProofPass === true &&
    d121S1MatrixStatus === D121_S1_MATRIX_STATUS &&
    cleanupPass &&
    metadataLeakFindingCount === 0
  );
}

export async function runCredentialProof({ client, userDataRoot, fixtureCredential }) {
  if (!client || typeof userDataRoot !== 'string' || !path.isAbsolute(userDataRoot) ||
      typeof fixtureCredential !== 'string' || fixtureCredential.length < 16) {
    throw new Error('runCredentialProof requires client, absolute userDataRoot, and coordinator fixtureCredential');
  }
  const credentialPath = path.join(userDataRoot, 'credentials', 'api-key.enc');
  try {
    const beforeAnthropic = await client.credentialStatus('anthropic');
    const beforeOmlx = await client.credentialStatus('omlx');
    const stored = await client.storeCredential('anthropic', fixtureCredential);
    const afterStore = await client.credentialStatus('anthropic');
    const afterStoreOmlx = await client.credentialStatus('omlx');
    const storedBytes = await readFile(credentialPath);
    const storedMetadata = await stat(credentialPath);
    const rawStored = storedBytes.toString('utf8');
    const removed = await client.removeCredential('anthropic');
    const afterRemove = await client.credentialStatus('anthropic');
    const afterRemoveOmlx = await client.credentialStatus('omlx');
    let credentialFilePresentAfterRemove = true;
    try { await access(credentialPath); } catch { credentialFilePresentAfterRemove = false; }
    const providerIsolation = credentialProviderIsolation({ beforeOmlx, afterStoreOmlx, afterRemoveOmlx });
    const proof = {
      schema: 'chirality-credential-mutation-proof/v2',
      fixtureCredentialSha256: createHash('sha256').update(fixtureCredential).digest('hex'),
      beforeConfigured: { anthropic: beforeAnthropic.configured === true, omlx: beforeOmlx.configured === true },
      afterStoreConfigured: {
        anthropic: afterStore.configured === true, omlx: afterStoreOmlx.configured === true
      },
      encryptedBlob: {
        bytes: storedBytes.length,
        sha256: createHash('sha256').update(storedBytes).digest('hex'),
        ownerOnlyMode: (storedMetadata.mode & 0o777) === 0o600,
        excludesPlaintextFixture: !rawStored.includes(fixtureCredential)
      },
      afterRemoveConfigured: {
        anthropic: afterRemove.configured === true, omlx: afterRemoveOmlx.configured === true
      },
      credentialFilePresentAfterRemove,
      providerIsolation,
      mutationPass:
        beforeAnthropic.configured === false && beforeOmlx.configured === false &&
        stored.configured === true && afterStore.configured === true && afterStoreOmlx.configured === false &&
        storedBytes.length > 0 && (storedMetadata.mode & 0o777) === 0o600 &&
        !rawStored.includes(fixtureCredential) && removed.configured === false &&
        afterRemove.configured === false && afterRemoveOmlx.configured === false &&
        !credentialFilePresentAfterRemove && providerIsolation
    };
    return { proof };
  } catch {
    try { await client.removeCredential('anthropic'); } catch {}
    throw new Error('credential proof failed');
  }
}

async function writeJson(filePath, value) {
  await writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

async function readCaptureMember(capturePath, reference, encoding = null) {
  const bytes = await readFile(path.resolve(path.dirname(capturePath), reference.path));
  return encoding ? bytes.toString(encoding) : bytes;
}

export function captureMatrixBindingPass(capture, evidence) {
  const sameRefIdentity = (left, right) => left?.path === right?.path &&
    left?.sha256 === right?.sha256 && left?.bytes === right?.bytes &&
    left?.artifactType === right?.artifactType;
  const observationsPass = capture?.evidenceMatrix?.observations?.every((row) =>
    sameRefIdentity(row.recordRef, evidence?.observationRefs?.[row.id])) === true;
  const controlsById = new Map((evidence?.negativeControls ?? []).map((entry) => [entry?.id, entry]));
  const controlsPass = capture?.evidenceMatrix?.controls?.every((row) =>
    sameRefIdentity(row.recordRef, controlsById.get(row.id)?.evidenceRef)) === true;
  return observationsPass && controlsPass;
}

export async function runProof(args) {
  const startedAt = nowIso();
  const outputMetadata = await lstat(args.outputRoot);
  if (outputMetadata.isSymbolicLink() || !outputMetadata.isDirectory()) {
    throw new Error('--output-root must be an existing nonsymlink directory');
  }
  if ((await readdir(args.outputRoot)).length !== 0) {
    throw new Error('--output-root must already exist and be empty');
  }
  const fail = async (error) => {
    const summary = {
      schema: 'chirality-packaged-security-proof/v2', status: 'fail', mode: 'consume-only',
      startedAt, completedAt: nowIso(), error: error instanceof Error ? error.message : String(error)
    };
    await writeJson(path.join(args.outputRoot, 'summary.json'), summary);
    return summary;
  };
  try {
    const captureMetadata = await lstat(args.capturedInputPath);
    if (captureMetadata.isSymbolicLink() || !captureMetadata.isFile() || captureMetadata.size === 0) {
      throw new Error('--captured-input must be a nonempty regular nonsymlink file');
    }
    const capture = parseJsonNoDuplicates(await readFile(args.capturedInputPath, 'utf8'));
    const admission = await verifyCapturedInput(capture, args.capturedInputPath, {
      runId: args.s0SecurityRunId, sourceRevision: args.sourceRevision,
      appPath: args.appPath, acceptedSourceBindingPath: args.acceptedSourceBindingPath
    });
    if (!admission.pass) throw new Error(`captured-input admission failed: ${admission.errors.join('; ')}`);
    const capturedEvidencePath = path.resolve(
      path.dirname(args.capturedInputPath), capture.artifacts.s0SecurityEvidenceRef.path
    );
    if (await realpath(capturedEvidencePath) !== await realpath(args.s0SecurityEvidencePath)) {
      throw new Error('S0 evidence path does not match captured-input binding');
    }
    const packagedMain = await readCaptureMember(
      args.capturedInputPath, capture.artifacts.packagedMainRef, 'utf8'
    );
    const daemonLog = await readCaptureMember(args.capturedInputPath, capture.artifacts.daemonLogRef, 'utf8');
    const guiLog = await readCaptureMember(args.capturedInputPath, capture.artifacts.guiLogRef, 'utf8');
    const combinedClosedLogs = `${daemonLog}\n${guiLog}`;
    const snapshots = parseJsonNoDuplicates(await readCaptureMember(
      args.capturedInputPath, capture.artifacts.tcpSnapshotsRef, 'utf8'
    ));
    const credentialMutation = parseJsonNoDuplicates(await readCaptureMember(
      args.capturedInputPath, capture.credential.mutationResultRef, 'utf8'
    ));
    const credentialSecretScan = parseJsonNoDuplicates(await readCaptureMember(
      args.capturedInputPath, capture.credential.postCloseSecretScanRef, 'utf8'
    ));
    const cleanupEvidence = parseJsonNoDuplicates(await readCaptureMember(
      args.capturedInputPath, capture.cleanup.evidenceRef, 'utf8'
    ));
    const credentialProof = {
      mutation: credentialMutation, postCloseSecretScan: credentialSecretScan,
      pass: credentialMutation?.mutationPass === true && credentialSecretScan?.pass === true &&
        Array.isArray(credentialSecretScan?.retainedSecretFindings) &&
        credentialSecretScan.retainedSecretFindings.length === 0 &&
        credentialMutation?.fixtureCredentialSha256 === credentialSecretScan?.fixtureCredentialSha256
    };
    const d121Files = D121_FROZEN_SOURCE_IDENTITIES.map(([relativePath]) =>
      admission.sourceChecks.find((entry) => entry.relativePath === relativePath ||
        entry.relativePath.endsWith(`/projects/chirality-app-dev/frontend/${relativePath}`) ||
        entry.relativePath.endsWith(`/frontend/${relativePath}`)) ?? { relativePath, pass: false }
    ).map((entry, index) => ({
      ...entry, relativePath: D121_FROZEN_SOURCE_IDENTITIES[index][0]
    }));
    const d121SourceProof = summarizeD121FrozenSourceFiles(d121Files);
    const evidence = parseJsonNoDuplicates(await readFile(args.s0SecurityEvidencePath, 'utf8'));
    const verifiedEvidenceFiles = await verifyD121EvidenceFiles(evidence, args.s0SecurityEvidencePath);
    const d121S0SecurityProof = summarizeD121S0SecurityEvidence(evidence, {
      sourceRevision: args.sourceRevision,
      artifactIdentitySha256: admission.packageBinding.artifactIdentitySha256,
      runId: args.s0SecurityRunId,
      evidenceFileVerification: verifiedEvidenceFiles
    });
    d121S0SecurityProof.evidenceFileVerification = verifiedEvidenceFiles;
    d121S0SecurityProof.captureMatrixBindingPass = captureMatrixBindingPass(capture, evidence);
    d121S0SecurityProof.pass = d121S0SecurityProof.pass && d121S0SecurityProof.captureMatrixBindingPass;
    const packagedPolicy = inspectPackagedPolicyMarkers(packagedMain);
    const networkProof = summarizeNetworkEvidence(combinedClosedLogs, snapshots);
    const rendererSecurityProof = summarizeRendererSecurityEvidence(combinedClosedLogs);
    const genericSensitiveFindings = [
      /https?:\/\/[^\s/@:]+:[^\s/@]+@/u,
      /[?&](?:api[_-]?key|token|credential|password)=/iu
    ].flatMap((pattern) => pattern.test(combinedClosedLogs) ? [{ pattern: pattern.source }] : []);
    const cleanup = { captureClaim: capture.cleanup, evidence: cleanupEvidence,
      pass: capture.cleanup.pass === true && cleanupEvidence?.pass === true };
    const summary = {
      schema: 'chirality-packaged-security-proof/v2',
      status: packagedProofPass({
        identityPresent: admission.identityChecks.every((entry) => entry.pass),
        packagedPolicyPass: packagedPolicy.allPresent,
        credentialProofPass: credentialProof.pass,
        networkProofPass: networkProof.pass,
        rendererSecurityProofPass: rendererSecurityProof.pass,
        d121SourceProofPass: d121SourceProof.pass,
        d121S0SecurityProofPass: d121S0SecurityProof.pass,
        d121S1MatrixStatus: d121S0SecurityProof.s1MatrixStatus,
        cleanupPass: cleanup.pass,
        metadataLeakFindingCount: genericSensitiveFindings.length
      }) ? 'pass' : 'fail',
      mode: 'consume-only', startedAt, completedAt: nowIso(),
      proofBoundary: 'closed-coordinator-capture-with-typed-source-and-package-evidence',
      captureAdmission: admission, artifactIdentity: capture.package, packagedPolicy,
      credentialProof, networkProof, rendererSecurityProof, d121SourceProof,
      d121S0SecurityProof, cleanup, retainedMetadataLeakFindings: genericSensitiveFindings,
      exclusions: {
        realCredentialsUsed: false, signingOrNotarization: false,
        distributionOrPublication: false, ownerUserDataTouched: false,
        providerScopeExpanded: false
      }
    };
    await writeJson(path.join(args.outputRoot, 'summary.json'), summary);
    return summary;
  } catch (error) {
    return fail(error);
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    process.stdout.write(usage());
    return;
  }
  const summary = await runProof(args);
  process.stdout.write(`packaged security proof status: ${summary.status}\n`);
  process.stdout.write(`summary: ${path.join(args.outputRoot, 'summary.json')}\n`);
  if (summary.status !== 'pass') process.exitCode = 1;
}

if (process.argv[1] && path.resolve(process.argv[1]) === SCRIPT_PATH) {
  main().catch((error) => {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 1;
  });
}
