import { access, readFile } from 'node:fs/promises';
import path from 'node:path';
import { describe, expect, it } from 'vitest';

const REPO_ROOT = path.resolve(process.cwd(), '../../..');
const ACTIVE_WORKFLOW = path.join(
  REPO_ROOT,
  '.github',
  'workflows',
  'desktop-release-template.yml'
);
const RETIRED_WORKFLOW = `${ACTIVE_WORKFLOW}.disabled`;

async function readWorkflow(): Promise<string> {
  return readFile(ACTIVE_WORKFLOW, 'utf8');
}

// The LaunchAgent RunAtLoad proof steps this workflow still carries belong to
// the retired daemon model (D-GOV-43, A2); their script is gone and the
// workflow needs the corresponding edit. The assertions here no longer pin
// them so that edit does not also have to touch this file.
describe('desktop unsigned artifact workflow', () => {
  it('reactivates only the bounded PR/manual proof surface', async () => {
    const workflow = await readWorkflow();

    await expect(access(RETIRED_WORKFLOW)).rejects.toThrow();
    expect(workflow).toContain('pull_request:');
    expect(workflow).toContain('workflow_dispatch:');
    expect(workflow).toContain('".github/workflows/desktop-release-template.yml"');
    expect(workflow).toContain(
      '".github/workflows/desktop-release-template.yml.disabled"'
    );
    expect(workflow).not.toMatch(/^\s+push:/m);
    expect(workflow).not.toMatch(/^\s+tags:/m);
    expect(workflow).toContain('contents: read');
    expect(workflow).not.toContain('contents: write');
    expect(workflow).toContain('timeout-minutes: 60');
    expect(workflow).toContain('cancel-in-progress:');
  });

  it('label-gates the macOS artifact job behind artifact-proof or manual dispatch', async () => {
    const workflow = await readWorkflow();

    expect(workflow).toContain(
      'types: [opened, synchronize, reopened, labeled]'
    );
    expect(workflow).toContain(
      "if: ${{ github.event_name == 'workflow_dispatch' || contains(github.event.pull_request.labels.*.name, 'artifact-proof') }}"
    );

    const pullRequestIndex = workflow.indexOf('pull_request:');
    const typesIndex = workflow.indexOf(
      'types: [opened, synchronize, reopened, labeled]'
    );
    const dispatchIndex = workflow.indexOf('workflow_dispatch:');
    const jobIndex = workflow.indexOf('verify-unsigned-macos:');
    const gateIndex = workflow.indexOf(
      "if: ${{ github.event_name == 'workflow_dispatch' || contains(github.event.pull_request.labels.*.name, 'artifact-proof') }}"
    );
    expect(pullRequestIndex).toBeGreaterThanOrEqual(0);
    expect(typesIndex).toBeGreaterThan(pullRequestIndex);
    expect(typesIndex).toBeLessThan(dispatchIndex);
    expect(gateIndex).toBeGreaterThan(jobIndex);
  });

  it('builds only the unsigned macOS arm64 target without credentials', async () => {
    const workflow = await readWorkflow();

    expect(workflow).toContain('runs-on: macos-15');
    expect(workflow).toContain('CSC_IDENTITY_AUTO_DISCOVERY: "false"');
    expect(workflow).toContain('npm run desktop:dist');
    expect(workflow).toContain('dist/mac-arm64/Chirality.app');
    expect(workflow).toContain("lipo -archs");
    expect(workflow).toContain('LSMinimumSystemVersion');
    expect(workflow).not.toMatch(/runs-on:\s+windows/i);
    expect(workflow).not.toMatch(/--win\b|\bnsis\b/i);
    expect(workflow).not.toContain('${{ secrets.');
  });

  it('fails closed on release signing or notarization posture', async () => {
    const workflow = await readWorkflow();

    expect(workflow).toContain("grep -q '^Authority='");
    expect(workflow).toContain('TeamIdentifier=');
    expect(workflow).toContain('xcrun stapler validate');
    expect(workflow).toContain(
      'assert_no_release_signature "${dmg_path}"'
    );
    expect(workflow).toContain(
      'assert_no_notarization_ticket "${dmg_path}"'
    );
    expect(workflow).toContain(
      'assert_no_release_signature "${mounted_app}"'
    );
    expect(workflow).toContain(
      'assert_no_notarization_ticket "${mounted_app}"'
    );
    expect(workflow).toContain(
      '[[ "${mounted_executable_sha256}" = "${executable_sha256}" ]]'
    );
    expect(workflow).toContain(
      'CI-only artifact unexpectedly has a valid notarization ticket'
    );
    expect(workflow).toContain('hdiutil verify "${dmg_path}"');
    expect(workflow).toContain(
      'artifacts/harness/instruction-root-integrity/latest/summary.json'
    );
    expect(workflow).toContain(
      'artifacts/release-verification/packaged-dependency-boundary.json'
    );
    expect(workflow).toContain(
      'node ./scripts/verify-packaged-dependency-boundary.mjs >"${verification_root}/packaged-dependency-boundary.json"'
    );
    expect(workflow).not.toContain(
      'verify-packaged-dependency-boundary.mjs +'
    );
  });

  it('proves the packaged Agent SDK from both staged and read-only mounted app roots', async () => {
    const workflow = await readWorkflow();

    expect(workflow).toContain(
      'staged_sdk_proof_root="${verification_root}/packaged-agent-sdk/staged"'
    );
    expect(workflow).toContain(
      'mounted_sdk_proof_root="${verification_root}/packaged-agent-sdk/mounted"'
    );
    expect(workflow).toContain(
      '"${app_path}/Contents/Resources" \\\n            "${staged_sdk_proof_root}"'
    );
    expect(workflow).toContain(
      '"${mounted_app}/Contents/Resources" \\\n            "${mounted_sdk_proof_root}"'
    );
    expect(workflow).toContain('summary.status !== "pass"');
    expect(workflow).toContain(
      'summary.proofMode !== "scripted-no-live-provider"'
    );

    const mountIndex = workflow.indexOf('hdiutil attach -nobrowse -readonly');
    const mountedProofIndex = workflow.indexOf(
      '"${mounted_app}/Contents/Resources"'
    );
    const cleanupIndex = workflow.indexOf(
      '\n          cleanup\n',
      mountedProofIndex
    );
    expect(mountIndex).toBeGreaterThanOrEqual(0);
    expect(mountedProofIndex).toBeGreaterThan(mountIndex);
    expect(cleanupIndex).toBeGreaterThan(mountedProofIndex);
  });

  it('fails closed at the deferred S0 qualification boundary before release workload', async () => {
    const workflow = await readWorkflow();

    expect(workflow).toContain(
      '- name: Block release workload pending deferred S0 qualification'
    );
    expect(workflow).toContain(
      'Deferred S0 qualification must supply accepted consume-only packaged-security inputs before release packaging can proceed.'
    );
    expect(workflow).not.toContain('continue-on-error:');
    expect(workflow).not.toContain('npm run proof:packaged-security --');
    expect(workflow).not.toContain(
      'packaged_security_root="${verification_root}/packaged-security"'
    );
    expect(workflow).not.toContain(
      "'artifacts/release-verification/packaged-security/summary.json'"
    );
    expect(workflow).not.toContain('if: always()');

    const checkoutIndex = workflow.indexOf('- name: Checkout');
    const holdIndex = workflow.indexOf(
      '- name: Block release workload pending deferred S0 qualification'
    );
    const failureIndex = workflow.indexOf('\n          exit 1\n', holdIndex);
    const setupIndex = workflow.indexOf('- name: Setup Node.js');
    const downstreamWorkloadIndexes = [
      workflow.indexOf('- name: Install and build shared runtime'),
      workflow.indexOf('npm ci'),
      workflow.indexOf('npm run build'),
      workflow.indexOf('- name: Install frontend dependencies'),
      workflow.indexOf('- name: Verify unsigned build posture'),
      workflow.indexOf('- name: Run release-target policy tests'),
      workflow.indexOf('npm test --'),
      workflow.indexOf('- name: Build unsigned macOS DMG'),
      workflow.indexOf('run: npm run desktop:dist'),
      workflow.indexOf('- name: Verify unsigned artifact'),
      workflow.indexOf('node ./scripts/verify-packaged-dependency-boundary.mjs'),
      workflow.indexOf('hdiutil verify "${dmg_path}"'),
      workflow.indexOf('hdiutil attach -nobrowse -readonly'),
      workflow.indexOf('- name: Upload unsigned CI artifact and verification evidence')
    ];
    expect(checkoutIndex).toBeGreaterThanOrEqual(0);
    expect(holdIndex).toBeGreaterThan(checkoutIndex);
    expect(holdIndex).toBeGreaterThanOrEqual(0);
    expect(failureIndex).toBeGreaterThan(holdIndex);
    expect(setupIndex).toBeGreaterThan(failureIndex);
    for (const workloadIndex of downstreamWorkloadIndexes) {
      expect(workloadIndex).toBeGreaterThan(failureIndex);
    }
  });

  it('uploads CI artifacts without a release-publication path', async () => {
    const workflow = await readWorkflow();

    expect(workflow).toContain('uses: actions/upload-artifact@v4');
    expect(workflow).toContain('chirality-desktop-macos-arm64-unsigned');
    expect(workflow).toContain('artifacts/release-verification/**');
    expect(workflow).toContain(
      'artifacts/release-verification/packaged-agent-sdk/staged/summary.json'
    );
    expect(workflow).toContain(
      'artifacts/release-verification/packaged-agent-sdk/mounted/summary.json'
    );
    expect(workflow).not.toContain('softprops/action-gh-release');
    expect(workflow).not.toContain('actions/create-release');
    expect(workflow).not.toMatch(/\bgh\s+release\b/);
    expect(workflow).not.toMatch(/^\s+publish-release:/m);
    expect(workflow).toContain('if-no-files-found: error');
  });
});
