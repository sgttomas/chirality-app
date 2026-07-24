# Scope-of-Work Stage-1 sizing report

Status: CANDIDATE EVIDENCE — read-only enumeration; not an authorization  
Observed commit: `67ba77e5107f941e6fcc7382ef467b6b018e972d`  
Observed date: 2026-07-12  
Observation boundary: tracked project-deliverable production kits on merged
`main`

## Result

The canonical tracked migration population is **154 deliverables** and **616
production documents**.

| Project | Canonical deliverables | Datasheet | Specification | Procedure | Guidance |
|---|---:|---:|---:|---:|---:|
| `chirality-app-dev` | 53 | 53 | 53 | 53 | 53 |
| `chirality-piping` | 101 | 101 | 101 | 101 | 101 |
| **Total** | **154** | **154** | **154** | **154** | **154** |

Every directory selected by `Datasheet.md` has all three companion production
documents at the observed commit (`missing_companions=0` for each project).
The SHA-256 digest of the sorted 154-directory path list is:

```text
b6eca2504a5d7551d96f7c0978ba6b4bc48b0e36c4d51792177fdd7a91e8df31
```

## Canonical membership rule

A Stage-1 migration candidate is a Git-tracked directory selected by exactly
one of these repository-relative path families:

```text
projects/chirality-app-dev/execution/**/1_Working/DEL-*/Datasheet.md
projects/chirality-piping/execution/**/1_Working/DEL-*/Datasheet.md
```

The deliverable directory is the selected path with its final `Datasheet.md`
filename segment removed.
Membership is repository- and path-based; a directory merely named `DEL-*`
does not enter the population.

The result was reproduced with this read-only procedure:

```sh
for project in chirality-app-dev chirality-piping; do
  git ls-files \
    "projects/$project/execution/**/1_Working/DEL-*/Datasheet.md" \
    | LC_ALL=C sort
done
```

For each selected directory, the companion check used `git cat-file -e` at
the observed commit for `Specification.md`, `Procedure.md`, and `Guidance.md`.
Counts for each filename were independently reproduced with the corresponding
`git ls-files` path family. This uses the tracked tree rather than unrestricted
filesystem discovery, which can include archives or worktree-local material.

## Explicit exclusions

The following are outside this population and outside the proposed Stage-1
conversion authority:

- archived or ignored deliverable copies, including any `.archive/` tree;
- `domains/` and all DOMAIN/KTY workspaces and generated domain-decomposition
  evidence;
- templates, fixtures, examples, public exports, staging trees, caches, and
  generated reports;
- decomposition declarations that have not been scaffolded into the two
  canonical tracked `1_Working/DEL-*` path families;
- control-plane files such as `_STATUS.md`, `_CONTEXT.md`,
  `_DEPENDENCIES.md`, `_REFERENCES.md`, and `_SEMANTIC.md`;
- every deliverable outside the two expressly proposed pilot packages during
  Stage 1.

The report sizes the possible later corpus migration; it does not authorize
that migration. D-GOV-15 proposes only ten isolated pilot candidates, and the
remaining 144 deliverables stay on the ratified four-document contract unless
a later owner ruling authorizes Stage 2.

At the observed commit, the proposed pilot prefixes select six App Dev PKG-07
deliverables and four Piping PKG-13 deliverables. All ten `_STATUS.md` records
declare `IN_PROGRESS`. The sole Piping `ISSUED` record is `DEL-01-01`, outside
PKG-13 and outside the proposed variance.

## Primary-source basis

- [`docs/TYPES.md`](../TYPES.md) defines the current four-document kit and its
  lifecycle relationship.
- [`docs/SPEC.md`](../SPEC.md) defines the current MUST files and
  `TASK+four-documents` lifecycle transition.
- The two tracked project `execution/**/1_Working/DEL-*` trees at the observed
  commit are the enumerated primary records.
