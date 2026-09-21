# OD7-G1 Root Package Validation

Status: `PASS — CANDIDATE ONLY`

Basis: `main@fb16e32ed60bb4f384cf1e07a83c4a14ff63bbae`

## Results

- Proposal containment: PASS. The basis HEAD is exact; tracked diff is empty;
  all untracked bytes are contained in the three declared proposal packages.
- Git identities: PASS. D-GOV-27 merge
  `bfb21d11a955b98eb0a4885cc7777ad8df27fd75`, App PR #363 merge
  `18e5dda568689daadaa05aff65bd4b810489409b`, D-30 publication
  `712df44816cf5253223b449fec0f10b48abd585c`, and SCA-007 application
  `ab0e6cfc4d4871989cf887fdd45e3c2d3168b41f` resolve and are ancestors.
- Source bytes and patches: PASS. All three patch files apply cleanly.
  D-GOV-27 source SHA-256 is
  `7295a4d2f14efd08af555caefa3631d2e1fdf826ff62c74b7de56f94fc2a5677`
  and contains exactly one EffectiveSHA placeholder.
- D-GOV-26 correction basis: PASS. The original notice remains
  `f5a557498c09921d4d2075c801938b5ef90eacecb515487afabbee7c43b2d182`.
  App corpus v17 resolves all eight members to App-local files with all eight
  `MATCH` and no drift; the candidate withdraws only the false historical
  Root-file detector/repin claim.
- Piping C04 rescan: PASS. Accepted SCA-007 evidence establishes revision
  `0.10`. The candidate visibly replaces the evaluated `0.9` pointer target
  with `0.10` and separately returns frontmatter `0.9 → 0.10`.
- Candidate IDs: PASS. Deterministic scans reproduce D-GOV-29, D-APP-76,
  D-58, DEC-091, Root Receipt 53, App Receipt-92, and Piping Receipt-76 as
  next-free candidates. None is reserved.
- App state: PASS. PR #363 application/merge trees are identical; all
  application paths are unchanged through the basis; APP-HOLD live scan passes
  with 53 contracts and six held targets; the full live suite passes 12/12.
- Piping state: PASS. D-30/D-APP-48 JSON hashes are unchanged. The combined
  validator returns the expected exit `1` and exact commit-SHA mismatch.
- Structured artifacts: PASS. All JSON and CSV parse; Root CSV has 13 data
  rows with uniform eight-column width and no blank row. Ruby's standard YAML
  parser accepts the proposed Root manifest.
- Candidate source resolution: PASS. Every Root-local and cross-package
  `ExactCandidateSource` resolves to an existing file within the repository.
  The corrected cross-package entries are unambiguous repo-relative paths.
- Receipt candidates: PASS. Both live project ledgers pass; contained temporary
  ledgers with the proposed App and Piping fragments appended also pass their
  respective validators.
- Whitespace: PASS. Every proposal file passes no-index whitespace checking;
  tracked `git diff --check` is empty.
- Package manifests and hash freeze: PASS. Each package inventory matches its
  declared manifest. Each `ARTIFACT_HASHES.sha256` was generated last, covers
  every other file exactly once, and reproduces end to end.

Passing validation is structural evidence only. It does not approve or apply
any candidate.
