# PR #188 Review Disposition

Status: ALL NUMBERED FINDINGS DISPOSITIONED / OWNER RULINGS BOUND / VALIDATION PASS / MERGED
MergeCommit: `a0dc7be326a8aa05e0c34ee2fbc7085264aad888`
ReviewedHead: `5f20ce750896da797319e535898e2959995bc521`
Sources: the 2026-07-11 PR #188 multi-agent review and consolidated PR #188
review feedback in the commissioning checkout

This is a derivative author disposition, not a human ruling. It groups
duplicate findings by remedy while preserving the source IDs for audit.

## Implemented runtime and tool remedies

| Findings | Disposition and evidence surface |
|---|---|
| C08, C09 | Dedicated specialists declare tool policies; ORCHESTRATOR/EVALUATION caller allowlists and validator-required edges cover every prescribed specialist. D-GOV-13 approves the fourteen-role compatibility baseline; all other runtime gates remain fail-closed. |
| H01 | A filesystem-atomic per-run launch lock encloses sibling overlap validation and status reservation; corrupt sibling status fails closed. |
| H02 | Child session identity is written to `STATUS.json` before the first WAIT/BACKGROUND turn, enabling notices and acknowledgments during execution. |
| H03 | The parent run is bound only through a post-validation binder, so an invalid first request cannot poison retry state. |
| H04 | Change-scope validation unions tracked diffs with untracked, non-ignored files. |
| C23, C24 | RELAY requires `noticeId`; statuses are preserved; VALIDATED requires `validationRef`; ACCEPTED requires `humanAcceptanceRef`; claim status cannot accept fan-in or lifecycle state. |
| C39 | The record-less SDK Agent bridge is retired fail-closed; managed delegation is the sole executable app-harness path. |
| C40 | Work graphs require concurrency, return, fan-in, and human-decision arrays; plans render them; amendments use stable versions and typed categories. |
| C44, C46, C60 | Launch briefs emit `ScopePath`; WORKING_ITEMS briefs include ScopePath/EXCLUSIONS; software briefs use `EXCLUSIONS`; TASK local run-record writes must be enclosed by declared targets, with managed read-only runtime records as the non-writing alternative. |
| C37 | Arbitrary Bash remains deliberately fail-closed unless project-root scope is explicit; doctrine now makes that child the serialized integration owner and directs package-parallel work to bounded/registered tools. |
| C61, V08 | Registered checks have positive timeouts and workspace-contained evidence output paths. |
| V01, V02 | Dedicated approval is parsed only from frontmatter; role membership is table-anchored; every positive R identifier is checked against the loaded catalog. |
| V03 | The export byte-identity test builds a fresh temporary staging tree and no longer depends on an untracked generated tree. |
| V04, V05, V06, V07 | Runtime vocabulary includes package/task scopes; unknown status keeps handoff open; read paths reject symlink traversal; background failure recording contains secondary errors. |
| CR coordination | All mutating coordination tools require `workspaceWrite` mode. |
| CR audit rubric | AUDIT_AGENTS now uses the current file-card, CONFORMS/PARTIAL/NONCONFORMANT, disposition, and remediation vocabulary. |

## Implemented governance and compatibility remedies

| Findings | Disposition and evidence surface |
|---|---|
| C01, C16, C18, C42, C43, C49, C50 | Both concordance proto-runs completed under pinned methods/steers/write surfaces and existing TASK execution; old §7 steer references alias to current §8. D-GOV-14 item 8 terminal evidence is integrated through owner-approved non-rewriting `main` merges, preserving ruling SHAs; neither run was retrofitted. |
| C05, C28, C29, C54 | Public export excludes private-project CI, loop launchers, TRB briefs, and development backlog; it uses a public-only init prompt and generalized private-home detection. D-GOV-14 item 9 approves public decisions, handoff, and human-authority records. |
| C06 | K-AGENTS-1 and TYPES implement the D-GOV-14 item 6 ruling: root AGENTS carries the Agent 0/1/2 hierarchy/index; the 3×4 matrix is deployment UI vocabulary only, not runtime authority grammar. |
| C07, C21, C22, C25, C33, C34, C35, C41, C45, C57, C58 | Stale role, pause-boundary, ID-width, migration-state, glossary, ConsumerHint, matrix, and fallback language was corrected; D-GOV-10 was restored to its bound content except its publication-SHA backfill. |
| C10 | All PR-added software skill/tool files now have exactly one terminal newline; merge-range `git diff --check` is a required closure gate. |
| C11, C12, C13, C14, C15, C26, C27, C32, C47, C53, C59, CR app-doc coverage | Human approval semantics are restored; `approvalRef` and approval booleans are explicitly structural citation metadata, not authentication or proof of a human act; consequential categories are defined; claim vocabularies and ruling language are separated; DBM anchors and professional-practice narratives were updated to the current runtime. |
| C31 | Deleted component-persona sources are `NO,RETIRED` in the Chirality domain source manifest with explicit D-GOV-11 replacement notes. |
| C36, C51 | SCHEDULING retirement is documented in the implementation handoff and submitted for explicit confirmation in D-GOV-14 item 5 without editing the SHA-bound D-GOV-11 ruling. |

## Authority corrections ruled by the owner

| Findings | Current disposition |
|---|---|
| C02, C04, C30, C52 | D-GOV-14 items 1–3 ratify the exact workflow-component, decomposition, and software workflow texts at `ee35409f5cf3a81ecb29a271527156b991df97b9`. |
| C03, C19, C20, C38 | D-GOV-14 item 4 approves D-GOV-13's fourteen-role table; runtime and validator still require every remaining declared gate. |
| C55 | D-GOV-14 item 9 affirmatively approves continued publication of the owner identity and business email needed by public authority verification. |

## Notes and non-defects

- C17 records the append-only pause receipt that was deliberately integrated;
  no run evidence beneath either DeliverableConcordance folder was rewritten.
- C48 is covered by HELPS_HUMANS Phase 5's “when implementation is authorized”
  release condition and its explicit dedicated-specialist approval gate.
- C56 and the review's verified-sound list require no remedy.
- The three refuted findings in Part 5 of the source review remain refuted.
- The managed Bash restriction is retained as a conscious safety boundary, not
  weakened to satisfy package parallelism.

## Closure gates

The final ruled candidate passes 333 root governance/validation/software tests;
all 43 skills, all 33 agent packages, instruction entrypoints, and 434 source
path anchors; the complete 699-test app-dev suite plus typecheck, catalog,
desktop packaging/building, 43-file instruction byte identity, and live
premerge probes; and the piping sweep across 36 Rust manifests, 496 Python
tests, 476 desktop tests, 18 development browser tests, one distribution WASM
test, and the production build. The 586-file public derivative has zero boundary
findings, and its independent staging tree passes agent, skill, entrypoint, and
425 path-anchor validation. A dedicated test confirms that C01-C61, H01-H04,
and V01-V08 all appear in this disposition. D-GOV-13 and D-GOV-14 remain bound
to `d22f80bf5d6c1190ce151df75d936bfcf4d38bc3`.

All local closure gates and the hosted governance check passed. PR #188 merged
to `main` with history-preserving commit
`a0dc7be326a8aa05e0c34ee2fbc7085264aad888`. App-dev's pre-existing missing
KG-001 `examples/` source asset and piping's existing npm advisories/chunk-size
warning remain routed product residuals; they do not weaken or expand this
governance tranche's acceptance claim.
