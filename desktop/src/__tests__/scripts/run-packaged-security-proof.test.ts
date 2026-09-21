import { describe, expect, it, vi } from 'vitest';
const fsFault = vi.hoisted(() => ({ specialPath: '' }));
vi.mock('node:fs/promises', async importOriginal => {
  const actual = await importOriginal<typeof import('node:fs/promises')>();
  return { ...actual, lstat: async (name: string) => {
    const info = await actual.lstat(name);
    return name === fsFault.specialPath ? new Proxy(info, { get(target, key) {
      if (['isSymbolicLink', 'isFile', 'isDirectory'].includes(String(key))) return () => false;
      return Reflect.get(target, key);
    } }) : info;
  } };
});
import { createHash } from 'node:crypto';
import { chmod, link, mkdir, mkdtemp, readFile, readdir, rm, symlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { EGRESS_LAYER_PROBE_URL } from '../../../electron/renderer-window-policy';
import {
  D121_FROZEN_SOURCE_IDENTITIES,
  D121_CONTROL_ORIGINS,
  D121_OBSERVATION_ORIGINS,
  D121_STREAMING_FIELD_ORIGINS,
  D121_NEGATIVE_OBSERVATION_CONTROLS,
  D121_PACKAGE_IDENTITY_RELATIVE_PATHS,
  D121_PDF_CONTENT_SECURITY_POLICY,
  D121_REQUIRED_NEGATIVE_CONTROLS,
  D121_REQUIRED_OBSERVATIONS,
  D121_S1_MATRIX_STATUS,
  EGRESS_PROBE_DECOY_URL,
  EGRESS_PROBE_URL,
  PACKAGED_RENDERER_ROUTES,
  captureMatrixBindingPass,
  credentialProviderIsolation,
  descendantProcessIds,
  evaluateCredentialEvidence,
  inspectPackagedPolicyMarkers,
  packagedProofPass,
  parseArgs,
  parseLsofOutbound,
  packageIdentitySha256,
  inventoryPackage,
  verifyPackageBinding,
  parseJsonNoDuplicates,
  runCredentialProof,
  runProof,
  sensitiveMaterialFindings,
  sourceRevisionBindingPass,
  summarizeD121FrozenSourceFiles,
  summarizeNetworkEvidence,
  summarizeD121S0SecurityEvidence,
  summarizeRendererSecurityEvidence,
  verifyCapturedInput,
  verifyD121EvidenceFiles
} from '../../../scripts/run-packaged-security-proof.mjs';

describe('run-packaged-security-proof script', () => {
  it('admits only the explicit consume-only CLI', () => {
    const args = parseArgs([
      '--app-path',
      '/dist/mac-arm64/Chirality.app',
      '--output-root',
      '/artifacts/proof',
      '--source-revision',
      'abc123',
      '--captured-input',
      '/capture/captured-input.json',
      '--accepted-source-binding',
      '/capture/accepted-source-binding.json',
      '--s0-security-evidence',
      '/capture/evidence/s0.json',
      '--s0-security-run-id',
      '012345abcdef'
    ]);

    expect(args.appPath).toContain('/dist/mac-arm64/Chirality.app');
    expect(args.outputRoot).toContain('/artifacts/proof');
    expect(args.sourceRevision).toBe('abc123');
    expect(args.s0SecurityRunId).toBe('012345abcdef');
    expect(args.capturedInputPath).toBe('/capture/captured-input.json');
    expect(args.acceptedSourceBindingPath).toBe('/capture/accepted-source-binding.json');
    expect(args.s0SecurityEvidencePath).toBe('/capture/evidence/s0.json');
    expect(() => parseArgs(['--app-path', '/legacy.app'])).toThrow('--captured-input is required');
    expect(() => parseArgs([
      '--captured-input', 'relative.json', '--output-root', '/out', '--app-path', '/app',
      '--accepted-source-binding', '/capture/binding.json',
      '--source-revision', 'rev', '--s0-security-evidence', '/s0.json',
      '--s0-security-run-id', '012345abcdef'
    ])).toThrow('--captured-input must be an absolute path');
  });

  it('binds the deterministic D121 matrix to every frozen PKG02 source and test locus', async () => {
    const exactFiles = D121_FROZEN_SOURCE_IDENTITIES.map(([relativePath, expectedSha256, expectedBytes]) => ({
      relativePath, expectedSha256, expectedBytes, sha256: expectedSha256, bytes: expectedBytes, pass: true
    }));
    const summary = summarizeD121FrozenSourceFiles(exactFiles);
    expect(summary.pass).toBe(true);
    expect(summary.files).toHaveLength(11);
    expect(summary.mode).toBe('S0_OWNER_DEFERRED');
    expect(summary.inlinePdfPreview).toBe(false);
    expect(summary.s1MatrixStatus).toBe('INAPPLICABLE_OWNER_DEFERRED');
    expect(summary.files.map((entry) => String(entry.relativePath))).toEqual(
      D121_FROZEN_SOURCE_IDENTITIES.map(([relativePath]) => String(relativePath))
    );

    const preload = exactFiles.find((entry) => entry.relativePath === 'electron/preload.ts');
    const contractPins = exactFiles.find((entry) => entry.relativePath === 'src/__tests__/contract-pins.manifest.ts');
    const preloadRegression = exactFiles.find(
      (entry) => entry.relativePath === 'src/__tests__/electron/folder-preload.test.ts'
    );
    expect(preload?.expectedSha256).toBe('bf7c0351875e906e8a2646baf292452b5ac537a0f52887def9ef1d95f45c7560');
    expect(contractPins?.expectedSha256).toBe('f8aa8b27564bb516e938e3d4a81d17ca58d640743c0e8ba105c3e90b041eb753');
    expect(preloadRegression?.expectedSha256).toBe('ab65a700be92ec4c5dc3ae6737a066cf90ac5c11605624b682f0512a4ec49da6');

    for (const relativePath of [
      'electron/preload.ts',
      'src/__tests__/contract-pins.manifest.ts',
      'src/__tests__/electron/folder-preload.test.ts'
    ]) {
      const drifted = structuredClone(exactFiles);
      const entry = drifted.find((candidate) => candidate.relativePath === relativePath)!;
      entry.sha256 = '0'.repeat(64);
      entry.pass = false;
      expect(summarizeD121FrozenSourceFiles(drifted).pass, relativePath).toBe(false);
      expect(summarizeD121FrozenSourceFiles(drifted).mode, relativePath).toBe('UNRECOGNIZED');
    }

    expect(summarizeD121FrozenSourceFiles(exactFiles.slice(1)).pass).toBe(false);
  });

  it('requires the complete identity-bound D121 S0 security matrix and defers S1 explicitly', () => {
    const fixture = { sha256: 'a'.repeat(64), bytes: 131072, pageCount: 3 };
    const evidence: any = {
      schema: 'chirality-d121-s0-security-evidence/v2', sourceRevision: 'revision',
      artifactIdentitySha256: 'artifact', runId: 'proof-run', fixture,
      evidenceFiles: [], observationRefs: {}, negativeControls: [],
      s1Matrix: { status: D121_S1_MATRIX_STATUS }
    };
    const expected: any = {
      sourceRevision: 'revision', artifactIdentitySha256: 'artifact',
      runId: 'proof-run',
      evidenceFileVerification: { pass: true, files: [] }
    };
    const claim = (value: unknown) => ({ outcome: 'pass', actual: value, expected: value });
    let identity = 0;
    const addRecord = (artifactType: string, observationIds: string[], results: Record<string, unknown>,
      origin: string, extra: Record<string, unknown> = {}) => {
      identity += 1;
      const path = `records/result-${identity}.json`;
      const sha256 = identity.toString(16).padStart(64, '0');
      const bytes = 100 + identity;
      const tracePath = `traces/trace-${identity}.json`;
      const traceSha256 = (identity + 1000).toString(16).padStart(64, '0');
      const traceRef = { path: tracePath, sha256: traceSha256, bytes, artifactType: 'raw-trace' };
      const record = {
        schema: 'chirality-d121-executed-result/v2', artifactType,
        sourceRevision: 'revision', packageArtifactIdentitySha256: 'artifact', fixtureIdentity: fixture,
        execution: { status: 'pass', runId: 'proof-run' }, observationIds,
        ...(artifactType === 'negative-control-result' ? {} : { results }), origin,
        measurement: { rawTraceRefs: [traceRef], inputIdentities: { fixtureSha256: fixture.sha256 } }, ...extra
      };
      evidence.evidenceFiles.push({ path, sha256, bytes, artifactType });
      expected.evidenceFileVerification.files.push({ path, sha256, bytes, pass: true, record });
      evidence.evidenceFiles.push(traceRef);
      expected.evidenceFileVerification.files.push({ ...traceRef, pass: true, record: null });
      return { path, sha256, bytes, artifactType };
    };
    const addOpaque = (artifactType: string, path: string, sha256: string, bytes: number) => {
      const reference = { path, sha256, bytes, artifactType };
      evidence.evidenceFiles.push(reference);
      expected.evidenceFileVerification.files.push({ ...reference, pass: true, record: null });
      return reference;
    };
    const fixtureRef = addOpaque('pdf-fixture', 'fixtures/multipage.pdf', fixture.sha256, fixture.bytes);
    evidence.fixtureRef = fixtureRef;
    evidence.observationRefs['response-headers'] = addRecord('http-policy-result', ['response-headers'],
      Object.fromEntries(Object.entries({
        status: 200, contentType: 'application/pdf', contentDisposition: 'inline', nosniff: true,
        noStore: true, contentLengthPositive: true, locationAbsent: true, contentRangeAbsent: true,
        acceptRangesAbsent: true, responseClassHeaderAbsent: true, csp: D121_PDF_CONTENT_SECURITY_POLICY
      }).map(([key, value]) => [key, claim(value)])), D121_OBSERVATION_ORIGINS['response-headers']);
    evidence.observationRefs['finalizer-commit-matrix'] = addRecord('finalizer-result', ['finalizer-commit-matrix'],
      Object.fromEntries(['soleEmitter', 'requestSpoofIgnored', 'responseMarkerStripped', 'conflictingHeadersClosed',
        'explicitCommit', 'implicitFlushCommit', 'implicitWriteCommit', 'implicitEndCommit',
        'restoredAfterCommit', 'errorsClosed', 'redirectsClosed', 'lateHeadersIgnored',
        'packagedDevelopmentParity'].map((key) => [key, claim(true)])),
      D121_OBSERVATION_ORIGINS['finalizer-commit-matrix']);
    const streamingRef = addRecord('streaming-result', ['streaming-range', 'stream-failures'], {
      rangeStatus: claim(200), ifRangeStatus: claim(200), fullResponseBytes: claim(fixture.bytes),
      bounded: claim(true), maxChunkBytes: claim(65536), mutationDetected: claim(true),
      postcommitAborted: claim(true), closeCounts: claim({ complete: 1, cancel: 1, disconnect: 1, failure: 1 })
    }, 'MIXED', { measurement: {
      rawTraceRefs: [], inputIdentities: { fixtureSha256: fixture.sha256 },
      fieldOrigins: D121_STREAMING_FIELD_ORIGINS
    } });
    const streamingRecord = expected.evidenceFileVerification.files
      .find((entry: any) => entry.path === streamingRef.path).record;
    streamingRecord.measurement.rawTraceRefs = expected.evidenceFileVerification.files
      .filter((entry: any) => entry.artifactType === 'raw-trace').slice(-1).map((entry: any) => ({
        path: entry.path, sha256: entry.sha256, bytes: entry.bytes, artifactType: entry.artifactType
      }));
    evidence.observationRefs['streaming-range'] = streamingRef;
    evidence.observationRefs['stream-failures'] = streamingRef;
    const negativeObservationIds = Object.keys(D121_NEGATIVE_OBSERVATION_CONTROLS);
    for (const name of negativeObservationIds) {
      evidence.observationRefs[name] = addRecord('negative-control-suite-result', [name],
        { [name]: claim(D121_NEGATIVE_OBSERVATION_CONTROLS[name as keyof typeof D121_NEGATIVE_OBSERVATION_CONTROLS]) },
        D121_OBSERVATION_ORIGINS[name as keyof typeof D121_OBSERVATION_ORIGINS]);
    }
    for (const id of D121_REQUIRED_NEGATIVE_CONTROLS) {
      const outcome = id.includes('failure') || id === 'cancellation' || id === 'disconnect' ? 'aborted' : 'denied';
      const evidenceRef = addRecord('negative-control-result', [], {}, D121_CONTROL_ORIGINS[id], {
        result: {
          controlId: id, status: 'pass',
          outcome
        }
      });
      evidence.negativeControls.push({ id, evidenceRef });
    }
    expect(summarizeD121S0SecurityEvidence(evidence, expected).pass).toBe(true);

    const cases: Array<[string, (candidate: any, verification: any) => void]> = [
      ['unbound control digest', candidate => { candidate.negativeControls[0].evidenceRef.path = 'records/unbound.json'; }],
      ['generic one-file-for-all reuse', candidate => {
        const oneRef = candidate.observationRefs['response-headers'];
        candidate.observationRefs = Object.fromEntries(D121_REQUIRED_OBSERVATIONS.map((name) => [name, oneRef]));
      }],
      ['wrong artifact type', candidate => { candidate.observationRefs['response-headers'].artifactType = 'streaming-result'; }],
      ['wrong artifact content', (_candidate, verification) => {
        verification.evidenceFileVerification.files.find((entry: any) => entry.record?.artifactType === 'streaming-result')
          .record.results.rangeStatus.actual = 206;
      }],
      ['wrong source identity', (_candidate, verification) => {
        verification.evidenceFileVerification.files.find((entry: any) => entry.record?.artifactType === 'finalizer-result')
          .record.sourceRevision = 'other';
      }],
      ['wrong envelope run identity', candidate => { candidate.runId = 'arbitrary-nonempty-run'; }],
      ['wrong package identity', (_candidate, verification) => {
        verification.evidenceFileVerification.files.find((entry: any) => entry.record?.artifactType === 'http-policy-result')
          .record.packageArtifactIdentitySha256 = 'other';
      }],
      ['wrong fixture identity', (_candidate, verification) => {
        verification.evidenceFileVerification.files.find((entry: any) => entry.record?.artifactType === 'streaming-result')
          .record.fixtureIdentity.bytes += 1;
      }],
      ['self-declared fixture identity', (candidate, verification) => {
        candidate.fixture = { ...candidate.fixture, sha256: 'b'.repeat(64) };
        for (const entry of verification.evidenceFileVerification.files) {
          if (entry.record) entry.record.fixtureIdentity = candidate.fixture;
        }
      }],
      ['boolean-only record', (_candidate, verification) => {
        const record = verification.evidenceFileVerification.files
          .find((entry: any) => entry.record?.artifactType === 'finalizer-result').record;
        record.results = Object.fromEntries(Object.keys(record.results).map((key) => [key, true]));
      }],
      ['wrong evidence origin', (_candidate, verification) => {
        verification.evidenceFileVerification.files.find((entry: any) => entry.record?.artifactType === 'finalizer-result')
          .record.origin = 'PACKAGE_HTTP';
      }],
      ['missing raw trace', (_candidate, verification) => {
        verification.evidenceFileVerification.files.find((entry: any) => entry.record?.artifactType === 'finalizer-result')
          .record.measurement.rawTraceRefs = [];
      }],
      ['extra record field', (_candidate, verification) => {
        verification.evidenceFileVerification.files.find((entry: any) => entry.record?.artifactType === 'http-policy-result')
          .record.fabricated = true;
      }],
      ['S1 PASS claim', candidate => { candidate.s1Matrix.status = 'PASS'; }],
      ['inline-right-panel claim', candidate => { candidate.s1Matrix.inlineRightPanel = true; }],
      ['nested native PASS claim', candidate => {
        candidate.nativePdfSecurity = { status: D121_S1_MATRIX_STATUS, pass: true };
      }],
      ['native S1 observation claim', candidate => {
        candidate.observationRefs['native-readable-pages'] = candidate.observationRefs['response-headers'];
      }],
      ['arbitrary native observation claim', candidate => {
        candidate.observationRefs['native-render-success'] = candidate.observationRefs['response-headers'];
      }],
      ['wrong negative-control outcome', (_candidate, verification) => {
        const record = verification.evidenceFileVerification.files
          .find((entry: any) => entry.record?.artifactType === 'negative-control-result').record;
        record.result.outcome = 'aborted';
      }]
    ];
    for (const [label, mutate] of cases) {
      const candidate = structuredClone(evidence);
      const verification = structuredClone(expected);
      mutate(candidate, verification);
      const summary = summarizeD121S0SecurityEvidence(candidate, verification);
      expect(summary.pass, label).toBe(false);
      expect(summary.s1MatrixStatus).toBe('INAPPLICABLE_OWNER_DEFERRED');
    }

    const executionStatuses = ['pass', 'fail', 'unavailable', 'skipped', 'notrun', 'unknown'];
    for (const status of executionStatuses) {
      for (const runId of ['proof-run', 'arbitrary-nonempty-run']) {
        const verification = structuredClone(expected);
        const control = verification.evidenceFileVerification.files
          .find((entry: any) => entry.record?.artifactType === 'negative-control-result').record;
        control.execution.status = status;
        control.execution.runId = runId;
        control.result.status = status;
        const shouldPass = status === 'pass' && runId === 'proof-run';
        expect(summarizeD121S0SecurityEvidence(evidence, verification).pass, `${status} × ${runId}`).toBe(shouldPass);
      }
    }

    const unavailable = structuredClone(expected);
    const unavailableControl = unavailable.evidenceFileVerification.files
      .find((entry: any) => entry.record?.artifactType === 'negative-control-result').record;
    unavailableControl.result.status = 'unavailable';
    unavailableControl.result.outcome = 'unavailable';
    expect(summarizeD121S0SecurityEvidence(evidence, unavailable).negativeControlsPass).toBe(false);

  });

  it('rehashes retained D121 observations and rejects missing or escaping evidence', async () => {
    const root = await mkdtemp(path.join(tmpdir(), 'chirality-d121-proof-test-'));
    try {
      const evidencePath = path.join(root, 'pdf-security-evidence.json');
      const observationPath = path.join(root, 'observation.log');
      await writeFile(evidencePath, '{}\n');
      const observation = '{}\n';
      await writeFile(observationPath, observation);
      const sha256 = createHash('sha256').update(observation).digest('hex');
      expect((await verifyD121EvidenceFiles({ evidenceFiles: [
        { path: 'observation.log', sha256, bytes: 3, artifactType: 'raw-log' }
      ] }, evidencePath)).pass).toBe(true);
      expect((await verifyD121EvidenceFiles({ evidenceFiles: [
        { path: 'observation.log', sha256: '0'.repeat(64), bytes: 3, artifactType: 'raw-log' }
      ] }, evidencePath)).pass).toBe(false);
      expect((await verifyD121EvidenceFiles({ evidenceFiles: [
        { path: '../outside.log', sha256, bytes: 3, artifactType: 'raw-log' }
      ] }, evidencePath)).pass).toBe(false);
      expect((await verifyD121EvidenceFiles({ evidenceFiles: [
        { path: 'observation.log', sha256, bytes: 3, artifactType: 'raw-log' },
        { path: 'observation.log', sha256, bytes: 3, artifactType: 'raw-log' }
      ] }, evidencePath)).pass).toBe(false);
      expect((await verifyD121EvidenceFiles({ evidenceFiles: [
        { path: 'observation.log', sha256, bytes: 3, artifactType: 'pdf-fixture' }
      ] }, evidencePath)).pass).toBe(false);
      const linkedPath = path.join(root, 'linked.log');
      await link(observationPath, linkedPath);
      expect((await verifyD121EvidenceFiles({ evidenceFiles: [
        { path: 'observation.log', sha256, bytes: 3, artifactType: 'raw-log' },
        { path: 'linked.log', sha256, bytes: 3, artifactType: 'raw-log' }
      ] }, evidencePath)).pass).toBe(false);
      const symlinkPath = path.join(root, 'symlink.log');
      await symlink(observationPath, symlinkPath);
      expect((await verifyD121EvidenceFiles({ evidenceFiles: [
        { path: 'symlink.log', sha256, bytes: 3, artifactType: 'raw-log' }
      ] }, evidencePath)).pass).toBe(false);
    } finally {
      await rm(root, { recursive: true, force: true });
    }
  });

  it('binds source, package, fixtures, and artifact references to independent live identities', async () => {
    const root = await import('node:fs/promises').then(async fs => fs.realpath(await mkdtemp(path.join(tmpdir(), 'chirality-capture-admission-'))));
    try {
      const captureRoot = path.join(root, 'capture');
      const sourceRoot = path.join(root, 'source');
      const packageRoot = path.join(root, 'package');
      const fixtureRoot = path.join(root, 'fixtures');
      await Promise.all([captureRoot, sourceRoot, packageRoot, fixtureRoot].map((directory) => mkdir(directory)));
      const digest = (bytes: string | Buffer) => createHash('sha256').update(bytes).digest('hex');
      const writeRef = async (name: string, content: string, artifactType: string) => {
        const absolute = path.join(captureRoot, name);
        await writeFile(absolute, content);
        return { path: name, sha256: digest(content), bytes: Buffer.byteLength(content), artifactType };
      };
      const acceptedPaths = Array.from({ length: 29 }, (_, index) => `accepted/member-${index}.txt`);
      const sourceMembers = [];
      for (const relativePath of acceptedPaths) {
        const bytes = Buffer.from(`accepted:${relativePath}`);
        await mkdir(path.dirname(path.join(sourceRoot, relativePath)), { recursive: true });
        await writeFile(path.join(sourceRoot, relativePath), bytes);
        sourceMembers.push({ relativePath, sha256: digest(bytes), bytes: bytes.length });
      }
      const patchText = `${acceptedPaths.map((relativePath) =>
        `diff --git a/${relativePath} b/${relativePath}\n`).join('')}accepted patch\n`;
      const patchRef = await writeRef('accepted.patch', patchText, 'accepted-source-patch');
      const manifestText = `${JSON.stringify({ schema: 'chirality-d121-qualified-source-manifest/v1',
        baseCommit: 'accepted-base', patchSha256: patchRef.sha256, members: sourceMembers })}\n`;
      const manifestRef = await writeRef('source-manifest.json', manifestText, 'accepted-source-manifest');
      const bindingText = `${JSON.stringify({ schema: 'chirality-accepted-source-binding/v1',
        baseCommit: 'accepted-base', patchSha256: patchRef.sha256, manifestSha256: manifestRef.sha256,
        pathCount: sourceMembers.length, members: sourceMembers })}\n`;
      const acceptedBindingRef = await writeRef(
        'accepted-source-binding.json', bindingText, 'accepted-source-binding'
      );
      const identityRoles = ['executable', 'appAsar', 'runtimeCli', 'unpackedSdkPackage',
        'unpackedSdkBinary'] as const;
      let packageMembers: any[] = [];
      const identities: Record<string, any> = {};
      for (const role of identityRoles) {
        const relativePath = D121_PACKAGE_IDENTITY_RELATIVE_PATHS[role];
        const content = `package:${role}`;
        const absolute = path.join(packageRoot, ...relativePath.split('/'));
        await mkdir(path.dirname(absolute), { recursive: true });
        await writeFile(absolute, content);
        packageMembers.push({ relativePath, sha256: digest(content), bytes: Buffer.byteLength(content) });
        identities[role] = {
          path: absolute, sha256: digest(content), bytes: Buffer.byteLength(content)
        };
      }
      const packageDecoys = [
        'nested/Contents/MacOS/Chirality',
        'Contents/MacOS/Chirality-wrong'
      ];
      for (const relativePath of packageDecoys) {
        const content = `decoy:${relativePath}`;
        const absolute = path.join(packageRoot, ...relativePath.split('/'));
        await mkdir(path.dirname(absolute), { recursive: true });
        await writeFile(absolute, content);
        packageMembers.push({ relativePath, sha256: digest(content), bytes: Buffer.byteLength(content) });
      }
      packageMembers = await inventoryPackage(await import('node:fs/promises').then(fs => fs.realpath(packageRoot)));
      const compatibilityIdentitySha256 = 'b'.repeat(64);
      const artifactIdentitySha256 = packageIdentitySha256(compatibilityIdentitySha256, packageMembers);
      const inventoryRef = await writeRef('package-inventory.json', `${JSON.stringify({
        schema: 'chirality-reviewed-package-inventory/v2', compatibilityIdentitySha256,
        members: packageMembers
      })}\n`, 'reviewed-package-inventory');
      const fixtureIds = ['positive', 'invalid-signature', 'zero-size', 'outside-root', 'symlink'];
      const fixtureValues = [];
      for (const id of fixtureIds) {
        const content = id === 'zero-size' ? '' : `fixture:${id}`;
        const absolute = path.join(fixtureRoot, `${id}.pdf`);
        await writeFile(absolute, content);
        fixtureValues.push({ id, path: absolute, sha256: digest(content), bytes: Buffer.byteLength(content),
          pageCount: id === 'positive' ? 3 : 0 });
      }
      const memberRef = await writeRef('member.json', '{}\n', 'closed-capture-member');
      const capturePath = path.join(captureRoot, 'capture.json');
      const observations = D121_REQUIRED_OBSERVATIONS.map((id) => ({
        id, origin: D121_OBSERVATION_ORIGINS[id as keyof typeof D121_OBSERVATION_ORIGINS], recordRef: memberRef
      }));
      const controls = D121_REQUIRED_NEGATIVE_CONTROLS.map((id) => ({
        id, origin: D121_CONTROL_ORIGINS[id], recordRef: memberRef
      }));
      const capture: any = {
        schema: 'chirality-d121-s0-captured-input/v2', runId: '012345abcdef',
        source: { root: sourceRoot, revision: 'accepted-base', acceptedBindingRef, patchRef,
          manifestRef, members: sourceMembers },
        package: { appPath: packageRoot, artifactIdentitySha256, compatibilityIdentitySha256, inventoryRef },
        authorities: { coordinatorRef: memberRef, configRef: memberRef, grantRef: memberRef,
          packageReviewRef: memberRef, nativeReleaseRef: memberRef },
        fixtures: { positive: fixtureValues[0], derived: fixtureValues.slice(1) }, identities,
        execution: { toolIdentities: [{ id: 'node', path: identities.executable.path,
          sha256: identities.executable.sha256, bytes: identities.executable.bytes, version: 'test' }],
          argvIdentities: [{ id: 'consumer', cwd: root, argv: ['node', 'consumer'], environmentIdentity: 'clean' }],
          cleanEnvironmentIdentities: [{ id: 'clean', keys: ['PATH'], valuesSha256: 'c'.repeat(64) }],
          processGroups: [{ lifecycle: 'lifecycle-1', rootPid: 1, processGroupId: 1, sessionId: 1 }],
          descendantHistory: [{ lifecycle: 'campaign', snapshotsRef: memberRef }],
          endpointHistory: [{ lifecycle: 'campaign', snapshotsRef: memberRef }],
          startedAt: '2026-09-08T00:00:00.000Z', completedAt: '2026-09-08T00:01:00.000Z' },
        members: [acceptedBindingRef, patchRef, manifestRef, inventoryRef, memberRef],
        artifacts: { packagedMainRef: memberRef, daemonLogRef: memberRef, guiLogRef: memberRef,
          tcpSnapshotsRef: memberRef, s0SecurityEvidenceRef: memberRef, uiRefs: [memberRef],
          httpRefs: [memberRef], sourceComponentRefs: [memberRef], generalRefs: [memberRef] },
        credential: { mutationResultRef: memberRef, postCloseSecretScanRef: memberRef },
        cleanup: { evidenceRef: memberRef, pass: true }, evidenceMatrix: { observations, controls }
      };
      await writeFile(capturePath, `${JSON.stringify(capture)}\n`);
      const expected = { runId: capture.runId, sourceRevision: capture.source.revision,
        appPath: capture.package.appPath, acceptedSourceBindingPath: path.join(captureRoot, acceptedBindingRef.path) };
      const admission = await verifyCapturedInput(capture, capturePath, expected);
      expect(admission.pass, admission.errors.join('; ')).toBe(true);
      const rejected: Array<[string, (value: any) => Promise<void> | void]> = [
        ['unknown capture field', value => { value.extra = true; }],
        ['missing cleanup', value => { delete value.cleanup; }],
        ['artifact type mismatch', value => { value.authorities.coordinatorRef = {
          ...value.authorities.coordinatorRef, artifactType: 'wrong-type'
        }; }],
        ['arbitrary source member', value => { value.source.members[0].relativePath = 'unrelated.txt'; }],
        ['missing source member', value => { value.source.members.pop(); }],
        ['extra source member', value => { value.source.members.push(value.source.members[0]); }],
        ['empty manifest object', async value => {
          await writeFile(path.join(captureRoot, value.source.manifestRef.path), '{}\n');
        }],
        ['self-declared package identity', value => { value.package.artifactIdentitySha256 = 'a'.repeat(64); }],
        ['permuted package identity roles', value => {
          [value.identities.executable, value.identities.appAsar] =
            [value.identities.appAsar, value.identities.executable];
        }],
        ['nested package identity suffix', value => {
          const relativePath = packageDecoys[0];
          const entry = packageMembers.find((member) => member.relativePath === relativePath)!;
          value.identities.executable = { path: path.join(packageRoot, ...relativePath.split('/')),
            sha256: entry.sha256, bytes: entry.bytes };
        }],
        ['wrong package identity filename', value => {
          const relativePath = packageDecoys[1];
          const entry = packageMembers.find((member) => member.relativePath === relativePath)!;
          value.identities.executable = { path: path.join(packageRoot, ...relativePath.split('/')),
            sha256: entry.sha256, bytes: entry.bytes };
        }],
        ['incomplete live package inventory', async _value => { await writeFile(path.join(packageRoot, 'unlisted'), 'x'); }],
        ['fixture path alias', value => { value.fixtures.derived[0] = { ...value.fixtures.derived[0],
          path: value.fixtures.positive.path, sha256: value.fixtures.positive.sha256,
          bytes: value.fixtures.positive.bytes }; }]
      ];
      for (const [label, mutate] of rejected) {
        const changed = structuredClone(capture);
        await mutate(changed);
        expect((await verifyCapturedInput(changed, capturePath, expected)).pass, label).toBe(false);
        if (label === 'empty manifest object') await writeFile(path.join(captureRoot, manifestRef.path), manifestText);
        if (label === 'incomplete live package inventory') await rm(path.join(packageRoot, 'unlisted'));
      }
      const hardlinkCapture = structuredClone(capture);
      await rm(fixtureValues[1].path);
      await link(fixtureValues[0].path, fixtureValues[1].path);
      hardlinkCapture.fixtures.derived[0] = { ...hardlinkCapture.fixtures.derived[0],
        sha256: fixtureValues[0].sha256, bytes: fixtureValues[0].bytes };
      expect((await verifyCapturedInput(hardlinkCapture, capturePath, expected)).pass).toBe(false);
    } finally {
      await rm(root, { recursive: true, force: true });
    }
  });

  it('requires one exact accepted/manifest/capture/CLI source revision', () => {
    expect(sourceRevisionBindingPass('base', 'base', 'base', 'base')).toBe(true);
    for (const revisions of [
      ['other', 'base', 'base', 'base'],
      ['base', 'other', 'base', 'base'],
      ['base', 'base', 'other', 'base'],
      ['base', 'base', 'base', 'other']
    ]) expect(sourceRevisionBindingPass(revisions[0], revisions[1], revisions[2], revisions[3])).toBe(false);
  });

  it('binds matrix rows by path as well as digest, size, and artifact type', () => {
    const reference = { path: 'records/a.json', sha256: 'a'.repeat(64), bytes: 10,
      artifactType: 'http-policy-result' };
    const capture: any = { evidenceMatrix: { observations: [{ id: 'response-headers', recordRef: reference }],
      controls: [] } };
    const evidence: any = { observationRefs: { 'response-headers': { ...reference } }, negativeControls: [] };
    expect(captureMatrixBindingPass(capture, evidence)).toBe(true);
    evidence.observationRefs['response-headers'].path = 'records/other.json';
    expect(captureMatrixBindingPass(capture, evidence)).toBe(false);
  });

  it('writes only a structured summary for a rejected captured input', async () => {
    const root = await mkdtemp(path.join(tmpdir(), 'chirality-consume-only-'));
    try {
      const outputRoot = path.join(root, 'output');
      await mkdir(outputRoot);
      const capturePath = path.join(root, 'capture.json');
      await writeFile(capturePath, '{}\n');
      const summary = await runProof({ capturedInputPath: capturePath, outputRoot,
        appPath: '/missing.app', sourceRevision: 'revision', s0SecurityEvidencePath: '/missing.json',
        s0SecurityRunId: '012345abcdef' });
      expect(summary.status).toBe('fail');
      expect(summary.mode).toBe('consume-only');
      expect(await readdir(outputRoot)).toEqual(['summary.json']);
      expect(JSON.parse(await readFile(path.join(outputRoot, 'summary.json'), 'utf8')).status).toBe('fail');
    } finally {
      await rm(root, { recursive: true, force: true });
    }
  });

  it('uses only the coordinator-supplied credential and exports no plaintext in its result', async () => {
    const root = await mkdtemp(path.join(tmpdir(), 'chirality-credential-helper-'));
    try {
      await mkdir(path.join(root, 'credentials'));
      const supplied = 'coordinator-fixture-credential';
      let storedValue = '';
      const statuses = new Map([['anthropic', false], ['omlx', false]]);
      const client = {
        credentialStatus: async (provider: string) => ({ configured: statuses.get(provider), rawStored: supplied }),
        storeCredential: async (provider: string, value: string) => {
          storedValue = value;
          statuses.set(provider, true);
          await writeFile(path.join(root, 'credentials', 'api-key.enc'), 'encrypted-value');
          await chmod(path.join(root, 'credentials', 'api-key.enc'), 0o600);
          return { configured: true, plaintext: supplied };
        },
        removeCredential: async (provider: string) => {
          statuses.set(provider, false);
          await rm(path.join(root, 'credentials', 'api-key.enc'));
          return { configured: false, plaintext: supplied };
        }
      };
      const result = await runCredentialProof({ client, userDataRoot: root, fixtureCredential: supplied });
      expect(storedValue).toBe(supplied);
      expect(result.proof.mutationPass).toBe(true);
      expect(result).not.toHaveProperty('fixtureCredential');
      expect(() => JSON.stringify(result)).not.toThrow();
      expect(JSON.stringify(result)).not.toContain(supplied);
      expect(result).not.toHaveProperty('rawStored');
    } finally {
      await rm(root, { recursive: true, force: true });
    }
  });

  it('redacts credential plaintext from failure paths', async () => {
    const secret = 'coordinator-fixture-credential';
    const client = {
      credentialStatus: async () => ({ configured: false }),
      storeCredential: async () => { throw new Error(`failed with ${secret}`); },
      removeCredential: async () => { throw new Error(`remove exposed ${secret}`); }
    };
    await expect(runCredentialProof({ client, userDataRoot: '/tmp/credential-proof',
      fixtureCredential: secret })).rejects.toThrow('credential proof failed');
    try {
      await runCredentialProof({ client, userDataRoot: '/tmp/credential-proof', fixtureCredential: secret });
    } catch (error) {
      expect(String(error)).not.toContain(secret);
    }
  });

  it('captures the complete packaged descendant process tree', () => {
    expect(
      descendantProcessIds(
        [
          { pid: 10, ppid: 1, command: 'packaged-gui' },
          { pid: 11, ppid: 10, command: 'renderer' },
          { pid: 12, ppid: 11, command: 'network-service' },
          { pid: 99, ppid: 1, command: 'unrelated' }
        ],
        [10]
      )
    ).toEqual([10, 11, 12]);
  });

  it('fails closed on non-loopback TCP while accepting isolated loopback traffic', () => {
    const parsed = parseLsofOutbound([
      'Chirality 10 user 20u IPv4 TCP 127.0.0.1:5000->127.0.0.1:6000 (ESTABLISHED)',
      'Chirality 11 user 21u IPv4 TCP 127.0.0.1:5001->203.0.113.4:443 (SYN_SENT)'
    ].join('\n'));

    expect(parsed.map((entry: { class: string }) => entry.class)).toEqual([
      'loopback',
      'external-non-allowlisted'
    ]);
  });

  it('expects exactly the egress-probe destination the app fixes, and sets only a loopback decoy in the environment', () => {
    // DEL-09-06-V3-05: the app never reads the probe URL from the environment;
    // the proof's expectation must be byte-equal to the app's constant.
    expect(EGRESS_PROBE_URL).toBe(EGRESS_LAYER_PROBE_URL);
    const destination = new URL(EGRESS_PROBE_URL);
    expect(destination.hostname).toBe('api.anthropic.com');
    expect(destination.port).toBe('8443');
    // The decoy is a destination the egress policy would allow (loopback) but that
    // refuses the connection on the host itself: nothing can leave the machine
    // even if a regression made the app honour the variable again.
    const decoy = new URL(EGRESS_PROBE_DECOY_URL);
    expect(decoy.hostname).toBe('127.0.0.1');
    expect(decoy.port).toBe('9');
    expect(EGRESS_PROBE_DECOY_URL).not.toBe(EGRESS_PROBE_URL);
  });

  it('requires blocked diagnostics, all three probes, and zero non-allowlisted TCP', () => {
    const egressPayload = '{"policy":"REQ-NET-001","destination":{"protocol":"https:","hostname":"api.anthropic.com","port":"8443"},"outcome":"rejected","error":"net::ERR_BLOCKED_BY_CLIENT"}';
    const logText = [
      'Blocked renderer outbound request by network policy { destination: redacted }\n',
      "Blocked renderer outbound request by network policy { reason: 'anthropic_port_not_allowlisted:8443' }\n",
      '[network-policy-probe] {"policy":"REQ-NET-001","results":[',
      '{"url":"https://example.com/chirality-packaged-security-blocked","ok":false},',
      '{"url":"http://127.0.0.1:9/chirality-packaged-security-loopback","ok":false}]}\n',
      `[egress-layer-probe] ${egressPayload}`
    ].join('');
    const snapshots = [
      { pids: [10, 11], endpoints: [{ endpoint: '127.0.0.1:6000', host: '127.0.0.1', class: 'loopback', line: 'fixture' }] }
    ];
    const summary = summarizeNetworkEvidence(logText, snapshots);

    expect(summary.pass).toBe(true);
    expect(summary.egressLayerDiagnostics).toBe(1);
    expect(summary.egressProbeObserved).toBe(true);
    expect(summary.egressProbeUnexpectedDestinations).toEqual([]);
    expect(summary.nonAllowlistedOutboundTcp).toEqual([]);

    // The egress layer must be observed on its own, from the main-process
    // probe: a CSP-only block of the example.com probe is not enough, and a
    // probe that got a response means the egress layer let it through.
    const cspOnly = logText.replace(
      "Blocked renderer outbound request by network policy { reason: 'anthropic_port_not_allowlisted:8443' }\n",
      ''
    );
    expect(summarizeNetworkEvidence(cspOnly, snapshots).pass).toBe(false);
    const responded = logText.replace('"outcome":"rejected"', '"outcome":"response","status":200');
    expect(summarizeNetworkEvidence(responded, snapshots).egressProbeObserved).toBe(false);
    expect(summarizeNetworkEvidence(responded, snapshots).pass).toBe(false);

    // The probe destination is fixed in the app (DEL-09-06-V3-05): a payload for the
    // allowlisted port, for a destination without the port, or for any other
    // destination (the loopback decoy the proof sets in the environment) is not
    // the expected observation and fails the proof.
    const allowlistedPort = logText.replace('"port":"8443"', '"port":"443"');
    expect(summarizeNetworkEvidence(allowlistedPort, snapshots).egressProbeObserved).toBe(false);
    expect(summarizeNetworkEvidence(allowlistedPort, snapshots).egressProbeUnexpectedDestinations).toEqual([
      { protocol: 'https:', hostname: 'api.anthropic.com', port: '443' }
    ]);
    expect(summarizeNetworkEvidence(allowlistedPort, snapshots).pass).toBe(false);
    const portless = logText.replace(',"port":"8443"', '');
    expect(summarizeNetworkEvidence(portless, snapshots).egressProbeObserved).toBe(false);
    expect(summarizeNetworkEvidence(portless, snapshots).pass).toBe(false);
    const decoyFollowed = logText.replace(
      '{"protocol":"https:","hostname":"api.anthropic.com","port":"8443"}',
      '{"protocol":"http:","hostname":"127.0.0.1","port":"9"}'
    );
    const decoySummary = summarizeNetworkEvidence(decoyFollowed, snapshots);
    expect(decoySummary.egressProbeObserved).toBe(false);
    expect(decoySummary.egressProbeUnexpectedDestinations).toEqual([
      { protocol: 'http:', hostname: '127.0.0.1', port: '9' }
    ]);
    expect(decoySummary.pass).toBe(false);
    // An extra payload for another destination fails even beside the expected one.
    const extraDestination = `${logText}\n[egress-layer-probe] {"policy":"REQ-NET-001","destination":{"protocol":"http:","hostname":"127.0.0.1","port":"9"},"outcome":"rejected","error":"net::ERR_CONNECTION_REFUSED"}`;
    const extraSummary = summarizeNetworkEvidence(extraDestination, snapshots);
    expect(extraSummary.egressProbeObserved).toBe(true);
    expect(extraSummary.egressProbeUnexpectedDestinations).toHaveLength(1);
    expect(extraSummary.pass).toBe(false);
  });

  it('fails closed when the egress-layer probe line is absent', () => {
    const logText = [
      'Blocked renderer outbound request by network policy { destination: redacted }',
      "Blocked renderer outbound request by network policy { reason: 'anthropic_port_not_allowlisted:8443' }",
      '[network-policy-probe] {"policy":"REQ-NET-001","results":[{"url":"https://example.com/chirality-packaged-security-blocked","ok":false},{"url":"http://127.0.0.1:9/chirality-packaged-security-loopback","ok":false}]}'
    ].join('\n');
    const snapshots = [
      { pids: [10], endpoints: [{ endpoint: '127.0.0.1:6000', host: '127.0.0.1', class: 'loopback', line: 'fixture' }] }
    ];

    const summary = summarizeNetworkEvidence(logText, snapshots);

    expect(summary.blockedProbeObserved).toBe(true);
    expect(summary.loopbackProbeObserved).toBe(true);
    expect(summary.egressProbePayloadCount).toBe(0);
    expect(summary.egressProbeObserved).toBe(false);
    expect(summary.pass).toBe(false);
  });

  it('fails closed when the egress-layer probe payload is malformed', () => {
    const logText = [
      'Blocked renderer outbound request by network policy { destination: redacted }',
      "Blocked renderer outbound request by network policy { reason: 'anthropic_port_not_allowlisted:8443' }",
      '[network-policy-probe] {"policy":"REQ-NET-001","results":[{"url":"https://example.com/chirality-packaged-security-blocked","ok":false},{"url":"http://127.0.0.1:9/chirality-packaged-security-loopback","ok":false}]}',
      '[egress-layer-probe] not-json'
    ].join('\n');
    const snapshots = [
      { pids: [10], endpoints: [{ endpoint: '127.0.0.1:6000', host: '127.0.0.1', class: 'loopback', line: 'fixture' }] }
    ];

    const summary = summarizeNetworkEvidence(logText, snapshots);

    expect(summary.blockedProbeObserved).toBe(true);
    expect(summary.loopbackProbeObserved).toBe(true);
    expect(summary.egressProbePayloadCount).toBe(1);
    expect(summary.egressProbeObserved).toBe(false);
    expect(summary.egressProbeUnexpectedDestinations).toEqual([null]);
    expect(summary.pass).toBe(false);
  });

  it('requires the renderer hardening evidence from the packaged page', () => {
    const policy = (nonce: string) =>
      `default-src 'self'; script-src 'self' 'nonce-${nonce}'; connect-src 'self'; frame-src 'none'; object-src 'none'`;
    const payloadFor = (route: string, index: number) => {
      const documentNonce = `documentNonce${index}`;
      const firstNonce = `responseNonce${index}a`;
      const secondNonce = `responseNonce${index}b`;
      return {
        policy: 'G-CSP',
        route,
        documentNonce,
        documentInlineScriptCount: 5,
        documentInlineScriptNoncesMatch: true,
        consecutiveResponses: [firstNonce, secondNonce].map((responseNonce) => ({
          status: 200,
          contentType: 'text/html; charset=utf-8',
          cspHeader: policy(responseNonce),
          responseNonce,
          inlineScriptCount: 5,
          inlineScriptNoncesMatch: true,
          documentComplete: true
        })),
        responseError: null,
        windowOpen: { returned: 'null' },
        violations: [
          { blockedURI: 'https://example.com', effectiveDirective: 'connect-src', disposition: 'enforce' }
        ],
        navigationAttempted: 'https://example.com/chirality-renderer-security-navigation'
      };
    };
    const payloads = PACKAGED_RENDERER_ROUTES.map(payloadFor);
    const logText = [
      ...payloads.map((payload) => `[renderer-security-probe] ${JSON.stringify(payload)}`),
      ...PACKAGED_RENDERER_ROUTES.map(
        () => '[chirality-desktop] [warn] renderer.window_open.denied {"destination":{"protocol":"about:","hostname":""}}'
      ),
      ...PACKAGED_RENDERER_ROUTES.map(
        () => '[chirality-desktop] [warn] renderer.navigation.denied {"event":"will-navigate","reason":"ORIGIN_NOT_RENDERER"}'
      )
    ].join('\n');

    const summary = summarizeRendererSecurityEvidence(logText);
    expect(summary).toMatchObject({
      probePayloadCount: 4,
      allObservedNoncesUnique: true,
      cspHeaderPresent: true,
      cspViolationObserved: true,
      unexpectedViolations: [],
      windowOpenReturnedNull: true,
      windowOpenDeniedLogged: true,
      navigationAttempted: true,
      navigationDeniedLogged: true,
      pass: true
    });
    expect(summary.routeResults.map((result: { route: string; pass: boolean }) => [result.route, result.pass])).toEqual(
      PACKAGED_RENDERER_ROUTES.map((route) => [route, true])
    );
    expect(
      summary.routeResults.every(
        (result: { scriptUnsafeInlineAbsent: boolean; scriptUnsafeEvalAbsent: boolean }) =>
          result.scriptUnsafeInlineAbsent && result.scriptUnsafeEvalAbsent
      )
    ).toBe(true);

    expect(summarizeRendererSecurityEvidence(logText.replace('renderer.navigation.denied', 'x')).pass).toBe(false);
    expect(summarizeRendererSecurityEvidence(logText.replace('"returned":"null"', '"returned":"object"')).pass).toBe(false);
    const unsafeInline = summarizeRendererSecurityEvidence(
      logText.replace("script-src 'self' 'nonce-responseNonce0a'", "script-src 'self' 'unsafe-inline'")
    );
    expect(unsafeInline.routeResults[0].scriptUnsafeInlineAbsent).toBe(false);
    expect(unsafeInline.pass).toBe(false);
    // Exact directives only: the superseded port-wildcard form must not pass.
    const wildcard = summarizeRendererSecurityEvidence(
      logText.replace("connect-src 'self';", "connect-src 'self' https://api.anthropic.com:*;")
    );
    expect(wildcard.cspHeaderPresent).toBe(false);
    expect(wildcard.pass).toBe(false);
    expect(summarizeRendererSecurityEvidence(logText.replace("connect-src 'self';", "connect-src 'self' https://example.com;")).cspHeaderPresent).toBe(false);
    expect(summarizeRendererSecurityEvidence(logText.replace("frame-src 'none';", "frame-src 'self';")).cspHeaderPresent).toBe(false);
    const ownResourceViolation = JSON.stringify({
      ...payloads[0],
      violations: [
        ...payloads[0].violations,
        {
          blockedURI: 'http://127.0.0.1:41234/_next/static/x.js',
          effectiveDirective: 'script-src-elem'
        }
      ]
    });
    const withOwnViolation = summarizeRendererSecurityEvidence(
      logText.replace(JSON.stringify(payloads[0]), ownResourceViolation)
    );
    expect(withOwnViolation.unexpectedViolations).toHaveLength(1);
    expect(withOwnViolation.pass).toBe(false);
    expect(
      summarizeRendererSecurityEvidence(
        logText.replace('responseNonce1a', 'responseNonce0a')
      ).allObservedNoncesUnique
    ).toBe(false);
    expect(
      summarizeRendererSecurityEvidence(
        logText.replace(`[renderer-security-probe] ${JSON.stringify(payloads[3])}`, '')
      ).pass
    ).toBe(false);
    expect(summarizeRendererSecurityEvidence('no probe at all').pass).toBe(false);
  });

  it('requires every packaged security marker and reports only hashes for fixture leaks', () => {
    const packagedMain = [
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
    ].join('\n');
    expect(inspectPackagedPolicyMarkers(packagedMain).allPresent).toBe(true);
    expect(inspectPackagedPolicyMarkers(packagedMain.replace('renderer.navigation.denied', '')).allPresent).toBe(false);

    const findings = sensitiveMaterialFindings('log has proof-key-value', [
      { label: 'fixture', value: 'proof-key-value' }
    ]);
    expect(findings).toHaveLength(1);
    expect(findings[0]).toEqual({
      label: 'fixture',
      sha256: expect.stringMatching(/^[a-f0-9]{64}$/)
    });
    expect(JSON.stringify(findings)).not.toContain('proof-key-value');
  });

  it('fails credential evidence when an operation-time stream leaks the fixture', () => {
    const fixture = 'packaged-proof-fixture-not-a-secret';
    const findings = evaluateCredentialEvidence(fixture, {
      beforeOperations: 'clean',
      completeDaemonStream: `credential stored: ${fixture}`,
      completeGuiStream: 'clean after stream closure'
    });

    expect(findings).toHaveLength(1);
    expect(findings[0].label).toBe('fixture-credential:completeDaemonStream');
    expect(JSON.stringify(findings)).not.toContain(fixture);
  });

  it('fails provider isolation when Anthropic mutation changes oMLX', () => {
    expect(
      credentialProviderIsolation({
        beforeOmlx: { configured: false },
        afterStoreOmlx: { configured: true },
        afterRemoveOmlx: { configured: false }
      })
    ).toBe(false);
  });

  it('requires confirmed cleanup in the final PASS predicate', () => {
    const otherwisePassing = {
      identityPresent: true,
      packagedPolicyPass: true,
      credentialProofPass: true,
      networkProofPass: true,
      rendererSecurityProofPass: true,
      d121SourceProofPass: true,
      d121S0SecurityProofPass: true,
      d121S1MatrixStatus: D121_S1_MATRIX_STATUS,
      metadataLeakFindingCount: 0
    };

    expect(packagedProofPass({ ...otherwisePassing, cleanupPass: true })).toBe(true);
    expect(packagedProofPass({ ...otherwisePassing, cleanupPass: false })).toBe(false);
    expect(packagedProofPass({
      ...otherwisePassing, cleanupPass: true, d121S1MatrixStatus: 'PASS'
    })).toBe(false);
  });
});


describe('typed contained package links', () => {
  it('accepts reviewed Electron links and detects inventory, target, and required-role substitutions', async () => {
    const fs = await import('node:fs/promises');
    const root = await fs.realpath(await mkdtemp(path.join(tmpdir(), 'typed-package-')));
    const app = path.join(root, 'Chirality.app');
    try {
      const framework = path.join(app, 'Contents/Frameworks/Electron Framework.framework');
      await mkdir(path.join(framework, 'Versions/A/Resources'), { recursive: true });
      await writeFile(path.join(framework, 'Versions/A/Electron Framework'), 'binary');
      await writeFile(path.join(framework, 'Versions/A/Resources/info'), 'resource');
      await symlink('A', path.join(framework, 'Versions/Current'));
      await symlink('Versions/Current/Electron Framework', path.join(framework, 'Electron Framework'));
      await symlink('Versions/Current/Resources', path.join(framework, 'Resources'));
      const executable = path.join(app, D121_PACKAGE_IDENTITY_RELATIVE_PATHS.executable);
      await mkdir(path.dirname(executable), { recursive: true }); await writeFile(executable, 'main');
      const members = await inventoryPackage(app);
      expect(members.filter((entry: any) => entry.kind === 'symlink')).toHaveLength(3);
      expect(members.find((entry: any) => entry.relativePath.endsWith('/Resources') && entry.kind === 'symlink')?.resolvedTarget.kind).toBe('directory');
      const compatibilityIdentitySha256 = 'b'.repeat(64);
      const capture: any = { package: { appPath: app, compatibilityIdentitySha256,
        artifactIdentitySha256: packageIdentitySha256(compatibilityIdentitySha256, members),
        inventoryRef: { path: 'inventory.json', artifactType: 'reviewed-package-inventory' } }, identities: {} };
      const save = async (rows: any[]) => writeFile(path.join(root, 'inventory.json'), JSON.stringify({
        schema: 'chirality-reviewed-package-inventory/v2', compatibilityIdentitySha256, members: rows }));
      await save(members);
      expect((await verifyPackageBinding(capture, path.join(root, 'capture.json'))).pass).toBe(true);
      for (const rows of [members.slice(1), [...members, members[0]], members.map((row: any) => row.kind === 'symlink' ?
        { ...row, resolvedTarget: { ...row.resolvedTarget, sha256: '0'.repeat(64) } } : row)]) {
        await save(rows); expect((await verifyPackageBinding(capture, path.join(root, 'capture.json'))).pass).toBe(false);
      }
      await save(members);
      await rm(path.join(framework, 'Resources'));
      await symlink('Versions/Current', path.join(framework, 'Resources'));
      expect((await verifyPackageBinding(capture, path.join(root, 'capture.json'))).pass).toBe(false);
      await rm(executable); await symlink('../Frameworks/Electron Framework.framework/Versions/A/Electron Framework', executable);
      const substituted = await inventoryPackage(app); await save(substituted);
      capture.package.artifactIdentitySha256 = packageIdentitySha256(compatibilityIdentitySha256, substituted);
      capture.identities.executable = { path: executable, sha256: createHash('sha256').update('binary').digest('hex'), bytes: 6 };
      expect((await verifyPackageBinding(capture, path.join(root, 'capture.json'))).pass).toBe(false);
    } finally { await rm(root, { recursive: true, force: true }); }
  });

  it.each(['absolute', 'escape', 'dangling', 'cycle', 'directory-cycle', 'absolute-component', 'escape-then-return', 'file-component'])(
    'rejects %s links without following them in the walker', async variant => {
      const fs = await import('node:fs/promises');
      const root = await fs.realpath(await mkdtemp(path.join(tmpdir(), 'bad-package-')));
      const app = path.join(root, 'app'); await mkdir(path.join(app, 'dir'), { recursive: true });
      await writeFile(path.join(app, 'file'), 'data');
      const target: Record<string, string> = { absolute: path.join(app, 'file'), escape: '../../out', dangling: 'missing',
        cycle: 'link', 'directory-cycle': '.', 'absolute-component': 'component/file',
        'escape-then-return': '../app/file', 'file-component': 'file/../file' };
      if (variant === 'absolute-component') await symlink(app, path.join(app, 'component'));
      await symlink(target[variant], path.join(app, 'link'));
      try { await expect(inventoryPackage(app)).rejects.toThrow(); }
      finally { await rm(root, { recursive: true, force: true }); }
    });

  it('rejects duplicate decoded JSON keys at every security input depth', () => {
    for (const value of ['{"a":1,"a":2}', '{"a":{"x":1,"x":2}}', '[{"x":1,"\\u0078":2}]']) {
      expect(() => parseJsonNoDuplicates(value)).toThrow('duplicate JSON key');
    }
    expect(parseJsonNoDuplicates('{"a":[1,true,{"x":"escaped \\" quote"}]}')).toEqual({ a: [1, true, { x: 'escaped " quote' }] });
  });
});


it('rejects a mocked special package member before opening its bytes', async () => {
  const fs = await import('node:fs/promises');
  const root = await fs.realpath(await mkdtemp(path.join(tmpdir(), 'special-package-')));
  try {
    fsFault.specialPath = path.join(root, 'special'); await writeFile(fsFault.specialPath, 'fixture');
    await expect(inventoryPackage(root)).rejects.toThrow('unsupported live package member');
  } finally { fsFault.specialPath = ''; await rm(root, { recursive: true, force: true }); }
});
