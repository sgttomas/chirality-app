# Harness Artifact Mirroring Guidance

Date: 2026-02-08  
Scope: CI/pre-merge usage of `npm run harness:validate:premerge`

## Perspective

The current wrapper design is intentionally `summary.json`-first.

- Default behavior should stay lightweight and deterministic for pre-merge gates.
- Full artifact mirroring should be an opt-in diagnostic mode, not a default.
- Mirroring is valuable when triage or audit depth is required, not for every green run.

## Why Not Always Mirror Everything

- CI storage and upload time increase substantially.
- Most runs only need pass/fail + test-level details already present in `summary.json`.
- Full artifacts may include more operational detail than needed for routine gating.
- Keeping the default minimal reduces maintenance and retention complexity.

## When Full Mirroring Is Worth It

Enable full-directory mirroring when one or more of these are true:

- A validation run fails and `summary.json` does not explain root cause.
- Failures are intermittent/flaky and require cross-run evidence comparison.
- Reviewers/release controls require downloadable raw evidence from CI.
- You need long-lived forensic/audit records beyond `${TMPDIR}` lifecycle.
- You are debugging stream-order, interrupt, permission, or parser regressions.

## Recommended Operating Model

- Baseline: publish stable `summary.json` only.
- On-demand: enable full mirroring for failing branches/runs.
- Optional policy: mirror full artifacts automatically only on failure.

## What "Full Mirroring" Means

From `${TMPDIR:-/tmp}/chirality-harness-validation/latest`, mirror:

- `summary.json`
- `sse/*.sse`
- `api/*.json`
- `logs/*.json`
- `mock/**`
- `cleanup/sessions.json`

to a stable CI path under `frontend/artifacts/harness/section8/latest/` (or configured equivalent).

## Guardrails

- Keep secrets redaction guarantees intact; do not bypass logger/env-filter safety.
- Apply artifact retention limits in CI (size/time).
- Treat mirrored artifacts as potentially sensitive operational data.
