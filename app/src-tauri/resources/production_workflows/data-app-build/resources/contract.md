# data-app-build: contract

Records listed here exist because a named consumer needs them: the owner at the
checkpoint, the examiner, a later rebuild, or recovery. Do not add others.

## Inputs

- **The owner's direction** to build, with the build target if it differs from the
  specification's build profile.
- **The accepted closure**, or for a draft build a frozen candidate, labelled draft.
  - `appspec.json` and `appspec.lock` from the candidate.
  - `DECISION.md` from checkpoint B, read only to confirm acceptance scope and coverage.
  - Every member the lock names.
- **The builder input contract** version (`builder-input-contract.md`).
- **The capability manifest** for the target: the view kinds, transforms, expression
  functions and layout shells the build may implement, and the libraries and versions it
  may use, each with a licence.
- **Locations.**
  - `BUILD_ROOT`: where the build tree and records are written.
  - The permitted execution environment for running components and tests.

The design record, the reference app, inventories and working notes are not inputs. A
builder that needs them has found a specification defect.

## Default locations

Where the direction names none: `BUILD_ROOT = {WORKING_ROOT}/builds/<app-id>/<build-id>/`.
Defaults resolve paths; they are not permissions.

## Outputs under `BUILD_ROOT`

| Path | Content | Consumer |
|---|---|---|
| `closure/` | Copies of every closure member at the lock's relative paths, verified against the lock; component runtimes installed from locked artifacts | Suite author, builder, examiner |
| `admission.txt` | Hash verification, validator output in the buildable profile, capability coverage; or the refusal | Owner, examiner |
| `suite/` | The conformance suite, examined and then frozen before the build, with `SUITE_MANIFEST.csv` (`Path,SHA256,Covers`) and its version | Builder (read only), examiner |
| `app/` | The build tree for the target | Owner, examiner |
| `ELEMENT_MAP.csv` | `SpecElement,Kind,CodeLocation,Tests` for every specification element in the built coverage | Examiner, rebuild |
| `conformance.txt` | Suite results on the final build tree, with the tree hash | Owner, examiner |
| `review/` | Examiner brief, return and backchecks | Owner, recovery |
| `BUILD_MANIFEST.md` | Identities (below) | Owner, rebuild, provenance |
| `provenance/` | At T3, the full PROV-O and RO-Crate package the gates require. Below T3, the build manifest is the provenance record and this folder is not written | Owner, deployed app |
| `checkpoint/ACCEPTANCE.md` | The owner's response (below) | Deployment, recovery |

## Build manifest

```text
Specification:     appspec.json SHA-256; appspec.lock SHA-256; accepted candidate id
Coverage:          whole specification | declared partial coverage <elements>
Builder:           agent identity as recorded by the host (provider, model) and this workflow's version
Contract:          builder input contract version; capability manifest SHA-256
Environment:       language runtimes and lockfiles; container image digest where used
Defaults applied:  presentation defaults the specification left open, each named
Suite:             SUITE_MANIFEST.csv SHA-256
Build tree:        SHA-256 of the build tree, computed by the method stated here
Conformance:       pass | fail, with counts by test kind
Examination:       examiner role and review record
```

**Build tree hash.** The integration owner states the method before the build, and the
builder uses it. The default:
1. Take every file under `app/`, with paths relative to it.
2. Sort the paths bytewise (`LC_ALL=C`).
3. Write one line per file, `<sha256>  <path>`, each ending in a newline.
4. Take the SHA-256 of the concatenated lines.

A file that records the tree hash itself is hashed with that value replaced by `PENDING`.

**Suite versions.** Keep a version log beside the suite: for each version, its manifest
SHA-256, the reason for the change, and the examiner's agreement. Make the suite
read-only while it is frozen.

## Checkpoint record

Write `ACCEPTANCE.md` from the owner's actual response:

```text
Build:             <build id>; BUILD_MANIFEST.md SHA-256; build tree SHA-256
Owner response:    <actual words, attribution, source>
Outcome:           accepted for <tier and intended use> | returned | stopped
Conditions:        <conditions, e.g. professional authentication before submission>
Next action:       <actual direction; deployment only if directed>
```

An agent may transcribe an evidenced response but cannot originate it.

## Invariants

- The builder reads only the closure, the contract, the capability manifest and the
  frozen suite.
- The suite is generated from the specification before the build, by a contributor
  other than the builder, examined against the specification by a separate agent, and
  then frozen by hash. A failing test is repaired in the build.
- Two routes change a test:
  - an expected value that the specification states changes only through a
    specification revision accepted through data-app-spec;
  - a derived test that does not follow from the specification is a suite defect. The
    suite author repairs it with the examiner's agreement, the suite gets a new version
    in its manifest, and every result is re-run.

  The builder edits neither.
- Every specification element in the built coverage appears in `ELEMENT_MAP.csv`. Code
  that realises no element is listed as an examination finding.
- The built application displays acceptance only as recorded and never in its own voice.
- No external effects during the build: no publishing, deploying, emailing or writing
  outside `BUILD_ROOT`.
- Acceptance applies to the identified build tree only. A changed tree needs its suite
  re-run and a new acceptance.
