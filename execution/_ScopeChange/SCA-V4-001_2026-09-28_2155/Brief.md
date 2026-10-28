# SCA-V4-001 — Brief

**Standing: CANDIDATE amendment folder (FIRST_AMENDMENT posture). Not an
accepted or active snapshot.** Checkpoint groups 1 and 2 are accepted
(owner DECISION-7); checkpoint group 3 is not yet presented. `_LATEST.md`
does not exist and is not created before group-3 acceptance.

Transcribed on 2026-09-28 by node AK1 (a Type 2 TASK, Claude Code subagent;
no delegation) of run `APP-V4-BASIS-ALIGN-20260928`, from the accepted
packet (`AgentRuns/APP-V4-BASIS-ALIGN-20260928/AMENDMENT_PACKET/`, revision
2) and the run's `OWNER_DECISIONS.md`. The packet's own words are the
accepted content; this file restates the request and resolution. Method:
`chirality-root:bundled:workflow:scope-change` (`workflows/scope-change/`).

## The human's request (verbatim)

Owner direction to start the undertaking, 2026-09-28, recorded in
`execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md`:

> "go ahead with the next undertaking as recommended."

It answers the recorder's recommendation to bring the accepted basis in line
with owner decisions DECISION-4 (D4-1 phased checkpoints; D4-3 model access
by OAuth sign-in or an API key, no default) and DECISION-5 (revised
V4-HOST-02), recorded in
`execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md`
(sha256 `5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2`),
together with the first closeout's SoW proposals (C1-A/B/C) and later SoW
wording findings.

## The acceptance of checkpoint groups 1 and 2 (verbatim)

Owner, 2026-09-28, DECISION-7 (same `OWNER_DECISIONS.md`, section
"Checkpoint A: acceptance"):

> "accept the remaining items as recommended"

Recorded in the decision snapshots
`../checkpoint_snapshots/SCA-V4-001_GROUP-1_2026-09-28/` and
`../checkpoint_snapshots/SCA-V4-001_GROUP-2_2026-09-28/`.

## Parsed actions

47 atomic actions, all `MODIFY` (IMPACT_ASSESSMENT §3): A01–A17 basis
documents, A18–A31 decomposition package, A32–A47 sixteen ScopeOfWork
contracts. Intake: [Intake_Actions.csv](Intake_Actions.csv) (every row
`PROPOSED`). Accepted register: [Amendment_Actions.csv](Amendment_Actions.csv)
(bound by hash in the group-2 snapshot).

## Resolution (method step 1; IMPACT_ASSESSMENT §1)

| Variable | Value |
|---|---|
| `DECOMP_VARIANT` | `SOFTWARE` |
| `CONTEXT_ROOT` | `projects/chirality-app-v4/execution/` |
| `DECOMPOSITION_PATH` | `execution/_Decomposition/SOFTWARE_DECOMP.md` with the companion registers of `Companion_Inventory.csv` |
| `SCOPE_CHANGE_ROOT` | `execution/_ScopeChange/` (created by this run) |
| `AMENDMENT_ID` | `SCA-V4-001` (owner item O-1). `zsh tools/query/scan_next_amendment_id.sh projects/chirality-app-v4/execution/_ScopeChange V4` returned `SCA-V4-001` before this folder existed |
| Pointer posture | `FIRST_AMENDMENT`: `_LATEST.md` absent; no predecessor is invented |
| `ALLOW_RENUMBERING` | `false` |
| `ALLOWED_PROPAGATION_WRITES` | The group-2 write boundary, named exactly in OWNER_ITEMS O-3 (see [Propagation_Plan.md](Propagation_Plan.md) §1) |

## Pre-change baseline (method step 5) — reuse record

The pre-change baseline is node P3's `audit-decomp` run,
`AgentRuns/APP-V4-BASIS-ALIGN-20260928/BASELINE/`, at basis `306291bdd`,
scope PKG-01, 02, 03, 04, 05, 08, 09 (30 deliverables).
[Pre_Change_Coverage.json](Pre_Change_Coverage.json) is a byte-identical copy
of `BASELINE/coverage_summary.json` (sha256
`d8ac5c4d35012d6a6fb6a3ef2c509caba08a616c8e14a5601bff2a83ee9620f9`).

Reuse test at the application basis `f4ba34c2c`: `git diff --stat
306291bdd f4ba34c2c` changes no docs, decomposition, ScopeOfWork,
`_CONTEXT.md`, register or `_DAG` byte. It changes the 14 `_STATUS.md` files
recorded IN_PROGRESS under owner DECISION-6 (commit `67a2fac4b`) and run-folder
files. Every decomposition and doc input hash recorded in `BASELINE/QA_Report.md`
equals the pre-application hash at `f4ba34c2c`. The lifecycle change is not
an amendment input; its effect on the post-change audit (Check 6 severities)
is isolated by a control run and reported in
`AgentRuns/APP-V4-BASIS-ALIGN-20260928/POSTCHANGE/COMPARISON.md`.

## Pre-application input hashes (sha256 at `f4ba34c2c`)

| File | sha256 |
|---|---|
| `docs/PRD.md` | `657593ce12a9a6da9f8b6c66579945499d909a8b6272d919d2d14a3db4538573` |
| `docs/ARCHITECTURE.md` | `c3ae766ee2d660fb391b7db0aa99526f84d21421cf3a6b692ddd17e42687e533` |
| `docs/HOST_INTEGRATION.md` | `08c8fc7db2d74619ed47d184f44938bb06f1e2abda0a304a9e11b9230d0960da` |
| `docs/EXAMINATION.md` | `1b156553dec7eb103dbb1166f5c0dbe9c719d26630d2fcace26c28b3ef54ee19` |
| `_Decomposition/SOFTWARE_DECOMP.md` | `5b66fefdaa54fa0046275bee40ac8f627230b3cc599f727a102e92d9f7bf4ded` |
| `_Decomposition/ScopeLedger.csv` | `363643306d3bbda80f4496943a5d1de5187d7910fabdf5b89f929e6c9605fd73` |
| `_Decomposition/Vocabulary_Map.csv` | `af6c21872119f299516fb63b68914a0293d4f028b3bb6c93d2e26976e866d8ba` |
| `_Decomposition/Deliverables.csv` | `bcdf6f2f5352e00360c19a956bd22c026909c388d77c76f92b4983ed906415eb` |
| `_Decomposition/Packages.csv` | `b8a9b949b629fb8dbe3343e0e5a1f09a30621785d99676f71adb1b285f741fbd` |
| `_Decomposition/Open_Issues.csv` | `77ecfea2cbe7382715bc4cefedf21e2caf4ad57d2fd5b7c6ed111eb04132aef4` |
| `_Decomposition/Consolidated_Coverage.csv` | `df7a204581a1f95beab3a1d1bae5c715940e8fc6fe128a3ad4cfb3b81b6e5f7f` |
| `_Decomposition/Coverage_Telemetry.json` | `178ec20abeddfb55e558869f0b33157106f7da95b71b804fda80a302a5f2f620` |
| DEL-02-03 `_CONTEXT.md` | `b3e0f69e0f21809d7c4ee5df24a77dcc2fe26f5eea139a76324b641700fd91ee` |
| DEL-05-01 `_CONTEXT.md` | `ddb2ea52306b0021fc568c8e025d9e41bdb619a5f5cbafe84221ba995cf928d1` |
| DEL-05-02 `_CONTEXT.md` | `265c66313439ee2b03b5af1b18c1d2a966080bb39106951b130b2894774842e7` |
| DEL-09-07 `_CONTEXT.md` | `bc84dceb3729803cd1f19fcea65891ed9532b4c5ba71b2ac7ba40b5f59c58caf` |

Each equals the hash prefix recorded in BASIS_AMENDMENT.md "Basis" and B7.

## Files in this folder

| File | Role | Source |
|---|---|---|
| `Brief.md` | intake brief | this transcription |
| `Intake_Actions.csv` | group-1 intake evidence (47 rows, `PROPOSED`) | IMPACT_ASSESSMENT §3 (EntityID as in §3; Description = RequestedChange plus AffectedSections); other columns from §3.1 |
| `Impact_Assessment.md` | group-1 output | byte-identical copy of the accepted `AMENDMENT_PACKET/IMPACT_ASSESSMENT.md` (sha256 `7fd523c2…348e`); its relative links resolve against the packet folder |
| `Pre_Change_Coverage.json` | pre-change baseline | byte-identical copy of `BASELINE/coverage_summary.json` |
| `Amendment_Preview.md` | group-2 exact amendment (rendered) | BASIS_AMENDMENT Parts A and B verbatim; SOW_REVISIONS by hash |
| `Propagation_Plan.md` | group-2 propagation plan | OWNER_ITEMS O-3 and IMPACT_ASSESSMENT §§6, 8–11 |
| `Amendment_Actions.csv` | accepted group-2 action register (47 rows) | IMPACT_ASSESSMENT §3.1, `{AMENDMENT_ID}` filled, deliverable `AffectedFiles` expanded to full repository paths as §3.1 directs |
| `Supersession_Delta.csv` | new supersession bindings (11 rows) | IMPACT_ASSESSMENT §7, with the full original and replacement text quoted |
| `Supersession_Map.csv` | candidate cumulative map | generated by `tools/coordination/accumulate_supersession_map.py` from the delta (first amendment; no prior map) |
| `Decision_Log.md` | checkpoint and execution decisions | this run |
| `Post_Change_Coverage.json` | post-change audit copy | `POSTCHANGE/coverage_summary.json` |
