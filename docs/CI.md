# Release projection CI

This repository retains public App v3 source under `desktop/`, Runtime source
under `runtime/`, and the exported role, skill and workflow library. Current
application development and private project coordination live in Chirality.

## Automatic checks

[Release projection CI](../.github/workflows/governance-harness.yml) runs on
pull requests and pushes to `main`, and can be dispatched manually. It checks:

- Required public source files and matching npm package/lock manifests.
- The public method index against its canonical package metadata and resources.
- Role and skill instruction contracts.
- Regressions for omitted project-only methods, undeclared missing packages,
  stale indexes, private paths, escaping resources and manifest drift.
- Conflict markers and credential leaks in the committed change range.

The public library deliberately excludes the project-only `chirality-change`
skill. `--public-export` permits that exact declared omission when rebuilding or
validating the exported index; other missing methods remain errors. Canonical
validation without that flag still requires the referenced project skill.
Legacy identities retain their recorded scope, and the published index remains
unchanged by this CI adaptation.

From the repository root, with Python 3.12:

```sh
python3 -m venv /tmp/chirality-app-ci
/tmp/chirality-app-ci/bin/python -m pip install -r tools/ci/requirements.txt
/tmp/chirality-app-ci/bin/python tools/ci/validate_release_projection.py
/tmp/chirality-app-ci/bin/python tools/validation/validate_agent_instructions.py --json
/tmp/chirality-app-ci/bin/python tools/validation/validate_skill_metadata.py .agents/skills --json
/tmp/chirality-app-ci/bin/python tools/validation/validate_workflow_metadata.py --public-export --json
/tmp/chirality-app-ci/bin/python -m pytest -q tools/ci/test_release_projection.py tools/validation/test_validate_agent_instructions.py tools/validation/test_four_role_contract.py tools/validation/test_validate_conflict_markers.py tools/validation/test_validate_run_record_leaks.py
```

The dependencies are pinned in [tools/ci/requirements.txt](../tools/ci/requirements.txt).
Range checks need Git history; CI obtains it through the checkout step.

## Monorepo checks and release holds

The inherited piping and PEC Actions workflows referenced `projects/` trees
that this projection does not contain. Those workflows are removed from the
active release repository; their previous definitions remain in Git history.
The former Root harness also depended on private execution and migration
evidence, so automatic CI now uses the checks above for the public projection.
Source-project test suites run in their owning development repository.

These checks establish integrity of the retained projection. They do not build
or qualify the frozen App/Runtime, establish a signed installer, or authorize a
release. The existing
[unsigned artifact workflow](../.github/workflows/desktop-release-template.yml)
retains its deferred S0 qualification hold. A manual dispatch or `artifact-proof`
label still encounters that explicit hold.
