# Git-ignored archives — inventory and read access

Standing: **source identification and access rule.** This file lists the
Git-ignored material in the original checkout that the v4 undertaking may
examine, how to read it from any worktree, and how to confirm it has not
changed. It makes no product claim.

## Access

| Item | Value |
|---|---|
| Archive root | `/Users/ryan/ai-env/projects/chirality` (the original checkout; override with `CHIRALITY_ARCHIVE_ROOT`) |
| How to read | Absolute paths below the archive root, from any worktree or session. Worktrees do not carry these files. |
| Rule | **Read only.** Do not modify, move, rename, extract into, or delete anything below these paths. Keep them until the owner decides v4 has replaced the v3.0.1 fallback (OD-09). |
| Hazard | These paths are Git-ignored. `git clean -X` or `git clean -x` run in the original checkout would delete them, and Git could not restore them. Do not run either there. |
| Check | `python3 projects/chirality-app-v4/reference/archives/archive_digests.py verify` recomputes the content digests and names any location or subtree that changed. Add `--root <path>` to check the protective clone (below). |
| Recorded | 2026-09-25 (UTC time in [`archive_digests.json`](archive_digests.json)); 19 locations, 57,073 files; recording takes about 20 s |

The digest file holds, for every location, a whole-location digest with its
file count and size, and digests of the subtrees below it to the depth shown
in the inventory. **Because this repository is public and these archives are
deliberately Git-ignored, the committed file names nothing below the 19
locations:** subtree digests are keyed by the SHA-256 of the subtree's path.
`verify` recomputes locally and prints the real name of any changed subtree.
A per-file list can be written to a local, uncommitted path with
`archive_digests.py record --file-list <path>`.

## Inventory

Relevance is to the v4 conceptual investigation: **high** = primary evidence
about App generations or intended hosts; **medium** = useful context or
occasional reference; **low** = kept for preservation, unlikely to inform the
PRD. The history investigation refines these ratings (see the
[source inventory](../SOURCE_INVENTORY.md)).

| Location (below archive root) | What it holds | Files | Size | Subtree depth | Relevance |
|---|---|---|---|---|---|
| `.archive/` (top-level files) | Early governance and product documents: `PRD_CANDIDATE.md`, `WHAT-IS-AN-AGENT.md`, `AGENT_ORCHESTRATOR.md`, `AGENT_DELIVERABLE_TASK.md`, earlier `SPEC/TYPES/CONTRACT/DIRECTIVE/PLAN`, `SE_Design_Analysis.md`, readiness notes | 13 | 0.3 MB | 2 | high |
| `.archive/frontend/` | The earlier Electron/Next.js desktop application source (v1 line) | 83 | 17 MB | 2 | high |
| `.archive/migration/` | Public-export migration of 2026-05-18: path maps, copy manifest, reports, export snapshot | 14 | 24 MB | 2 | medium |
| `.archive/chirality-governance/`, `lens-register/`, `semantic-matrix-build/`, `tier0-bridge-coordination-2026-06-21/` | Earlier governance execution records and method experiments | 21 | < 1 MB together | 2 | medium |
| `.archive/examples/` | Worked project roots used as regression examples (`execution-6a/6b/6c`, `AB-2026-01424…`, price sources) | 5,055 | 208 MB | 2 | medium (evidence cited by thesis Ch. 8) |
| `.archive/domains/` | Earlier domain corpora (`chirality`, `piping-design` sources and OCR work) | 41,025 | 7.6 GB | 2 | low |
| `domains/` | Current domain corpora and local search indexes (`_LocalIndexes` for chirality, chirality-app-dev, chirality-piping, piping-design; piping-design `_Sources`) | 7,634 | 6.9 GB | 2 | low–medium (the indexes are rebuildable projections) |
| `plans/.archive/` | Archived plans: `chirality-app-test`, task-management harness evaluation/plan/handoff, governance-harness assessments, monorepo structure assessments | 72 | 1 MB | 1 | medium |
| `plans/evidence/2026-09-19_manual_theory.zip` | Source bundle for the 2026-09-19 manual theory work | 1 | 33 KB | — | low |
| `projects/chirality-app-dev/.archive/` | Earlier App decomposition and execution: `ChiralityApp_SoftwareDecomposition_2026-02-21_G7-APPROVED.md`, `PKG-01…PKG-08`, harness, UI, change and scope-change records, `building-dmg.md` | 2,313 | 15 MB | 2 | high |
| `projects/chirality-app-dev/chirality-app-dev.zip` | Zipped snapshot of the App project | 1 | 5 MB | — | medium |
| `projects/chirality-app-dev/execution/_Decomposition/.archive/` | `Chirality_App_vNext_SOFTWARE_DECOMP.md`, `…_v2_5.md`, `PRD_software_decomp_aligned_v3.md` | 3 | 165 KB | — | high |
| `projects/chirality-app-dev/frontend/.chirality/` | Local App session records (`sessions/`) from development use | 24 | 3 MB | 1 | medium (observed behaviour; check for private content before quoting) |
| `projects/chirality-app-dev/frontend/artifacts/` | Harness artifacts from local runs | 14 | 99 KB | 1 | low |
| `projects/chirality-app-dev/frontend/dist/` | A locally built `Chirality-0.1.0-arm64.dmg` and builder configuration | 4 | 254 MB | 1 | low |
| `projects/chirality-piping/.archive/` | SWBPIPE planning records: DAG plans, scope-change refresh plans, `TP-MAC-02…10` physics-first and result-review plans, `TP-PER-01` persistence and run history, session notes | 102 | 1 MB | 1 | high (host activities) |
| `projects/pec/pilot-scratch/` | PEC pilot working files | 99 | 27 MB | 1 | low |
| `projects/pec/backups/` | A PEC database backup | 1 | 2 MB | — | low |
| `exports/chirality-app/staging/` | Staging tree of the public `chirality-app` export (AGENTS, framework, agents, docs, skills, tools) | 534 | 5 MB | 1 | medium |
| `_harness_generated/` | Governance-harness generated briefs, closeout and evidence | 43 | 1 MB | 1 | low |
| `_DomainEngines/pec/`, `_DomainEngines/bridge/BRIDGE_2026-06-21_tier0-prep/` | Domain-engine bridge preparation | 16 | 90 KB | — | low |
| `workflows/Software_PRD_Workflow_Draft_v1.zip` | Draft software-PRD workflow bundle | 1 | 29 KB | — | medium (predecessor of a PRD method) |

## Not inventoried

| Location | Reason |
|---|---|
| `.claude/` (28 GB) | Claude Code session data and worktrees, including this undertaking's own worktree. Not an archive. |
| `node_modules/`, `__pycache__/`, `.pytest_cache/`, `.next/`, `target/` (including `projects/chirality-piping/apps/desktop/src-tauri/target`, 9.7 GB) | Dependency and build outputs, reproducible from tracked sources. |
| `projects/pec/*.db*` | Live PEC database files; they change during use. |
| `projects/chirality-piping/apps/desktop/{dist,public,src-tauri/gen}` and `*.tsbuildinfo`, `Cargo.lock` files under `core/` | Build outputs and lock files generated locally. |
| `.DS_Store` files | Finder metadata. |

## Protective clone (owner decision Q-13, 2026-09-25)

| Item | Value |
|---|---|
| Location | `/Users/ryan/ai-env/archives/chirality-2026-09-25/` (outside any repository) |
| Contents | The 19 locations above, at the same relative paths, copied as APFS copy-on-write clones (`cp -cRp`); free disk space was unchanged by the copy |
| Check | `archive_digests.py verify --root /Users/ryan/ai-env/archives/chirality-2026-09-25` — all 19 locations matched the recorded digests on 2026-09-25 |
| Protection | Made read-only (`chmod -R a-w`). To remove it deliberately later: `chmod -R u+w <clone>` first. |
| Limit | 35 symbolic links were copied as links; those with absolute targets still point into the original checkout's `domains/` tree, whose content the clone also holds. A clone protects against deletion or change in the original checkout; it is on the same disk, so it is not a backup against disk failure. |

Both copies are kept until the owner decides v4 has replaced the v3.0.1
fallback (OD-09).
