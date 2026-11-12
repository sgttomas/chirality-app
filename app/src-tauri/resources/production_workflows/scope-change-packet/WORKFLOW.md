---
name: scope-change-packet
description: 'Produce a bounded PKG-00 Scope Change Consumable Packet for later human-initiated WORKING_ITEMS (workflow: scope-change) intake.'
metadata:
  kind: instruction
  surface: workflow
---

# WORKFLOW — scope-change-packet

## Purpose

Produce one **Scope Change Consumable Packet** under a PKG-00 control deliverable. The packet prepares evidence, proposed actions, affected-surface inventories, and a human-readable WORKING_ITEMS (workflow: scope-change) seed request.

The packet is not an amendment, not a dependency ruling, and not a DepClosure result. It is a bounded staging artifact for a later human-initiated WORKING_ITEMS (workflow: scope-change) workflow.

Reciprocal needs may supply bounded evidence for this packet when an actual scope decision is needed. They do not automatically require an amendment, become non-gating, or acquire a separate resolution-case workflow.

## Suitable Shell

- `TASK` in generic shell mode with `ScopePath` set to one PKG-00 control deliverable folder.

## Required Inputs

- `ScopePath` — one PKG-00 control deliverable folder.
- `RuntimeOverrides.PACKET_ID` — local packet ID, for example `PKG00-SCA-PACKET-001`.
- `RuntimeOverrides.PACKET_PATH` — absolute output folder inside `{ScopePath}/scope-change-packets/`.
- `RuntimeOverrides.PACKET_TITLE` — human-readable packet title.
- `RuntimeOverrides.SCC_ID` — the reciprocal-group label in the cited bounded dependency observation (for example `SCC-001`); it identifies that observation only, not a persistent dependency entity.
- `RuntimeOverrides.DECOMP_VARIANT` — `SOFTWARE`.
- `RuntimeOverrides.DECOMPOSITION_PATH` — current decomposition authority.
- `RuntimeOverrides.DEPCLOSURE_SNAPSHOT` — cited bounded dependency observation/report and its input basis; it is evidence, not a dependency authority.
- `RuntimeOverrides.AFFECTED_DELIVERABLES` — semicolon-separated deliverable IDs.
- `RuntimeOverrides.FOCUS_ROWS` — semicolon-separated consumer `deliverable.yaml` paths and need indices, or `TBD`; retain this packet field name without creating dependency row IDs.

## Read Boundary

Read only:

- the PKG-00 control deliverable in `ScopePath`;
- PKG-00 package-level control files;
- the cited decomposition document;
- the cited DepClosure snapshot and evidence files;
- affected product deliverable `_CONTEXT.md`, `_STATUS.md`, `deliverable.yaml`, and accepted production files.

Do not scan unrelated packages except as needed to resolve explicitly listed affected deliverables.

## Write Boundary

Write only:

- `{PACKET_PATH}/Packet_Contract.md`
- `{PACKET_PATH}/Packet_Datasheet.md`
- `{PACKET_PATH}/Packet_Specification.md`
- `{PACKET_PATH}/Packet_Procedure.md`
- `{PACKET_PATH}/Packet_Rationale.md`
- `{PACKET_PATH}/SCOPE_CHANGE_INIT.md`
- `{PACKET_PATH}/Proposed_SCA_Actions.csv`
- `{PACKET_PATH}/Affected_Surfaces.csv`
- `{PACKET_PATH}/Evidence_Index.csv`
- `{PACKET_PATH}/Packet_QA.md`

Never write:

- product package files;
- any `deliverable.yaml`;
- `_ScopeChange/`;
- `_Reconciliation/`;
- decomposition files.

## Output Contract

Each packet must contain the fixed ten-file set named above.

`Packet_Contract.md` defines consumption rules, authority limits, the mapping of packet content to WORKING_ITEMS (workflow: scope-change) checkpoint groups, and non-goals.

`Packet_Datasheet.md` records identity, cited reciprocal-group observation and basis, affected deliverables, actual local need locations, and evidence inventory.

`Packet_Specification.md` records proposed amendment requirements, action candidates, acceptance criteria, and invariant checks.

`Packet_Procedure.md` gives WORKING_ITEMS (workflow: scope-change) intake instructions and how the packet serves each of its three checkpoint groups: (1) proposed change and impact, (2) exact amendment and propagation plan, (3) audited poststate acceptance.

`Packet_Rationale.md` records source-grounded reasoning, why the observed input conditions require a scope decision, risks, and alternatives rejected.

`SCOPE_CHANGE_INIT.md` is a seed request. It must say it is not valid until the human explicitly initiates WORKING_ITEMS (workflow: scope-change).

`Proposed_SCA_Actions.csv` uses columns:

```csv
PacketID,ActionSeq,ActionType,EntityType,EntityID,Description,AffectedDeliverables,AffectedFiles,EvidenceRefs,SCOPE_CHANGE_Checkpoint,Status
```

`SCOPE_CHANGE_Checkpoint` records the checkpoint group or groups the row serves
(`CHECKPOINT_GROUP_1`, `CHECKPOINT_GROUP_2`, `CHECKPOINT_GROUP_3`,
semicolon-separated). Historical packets used the legacy column name
`SCOPE_CHANGE_Gate` with gate labels; the validator still accepts that name on
read, and historical packets remain readable as written and are not rewritten.

`Affected_Surfaces.csv` uses columns:

```csv
PacketID,SurfaceType,SurfacePath,PackageRole,ChangeClass,OwnerWorkflow,RequiredAction,EvidenceRefs,Status
```

`Evidence_Index.csv` uses columns:

```csv
EvidenceID,SourcePath,SourceRef,EvidenceType,Supports,Notes
```

`Packet_QA.md` records checklist results, unresolved TBDs, and packet readiness verdict. The verdict must distinguish structural packet validity from WORKING_ITEMS (workflow: scope-change) intake acceptance.

## Method

1. Load `agents/AGENT_TASK.md`, this workflow, and resources required for the current stage.
2. Resolve `PACKET_PATH` and confirm it is inside `ScopePath`.
3. Read PKG-00 control files and deliverable-local packet context.
4. Read the cited dependency observation and its actual condition/source evidence for the scoped reciprocal group.
5. Read only explicitly affected product deliverables and local need declarations. Preserve cases, conditions, `when`, `gating`, unknown/external inputs and outward obligations; do not merge needs by endpoint.
6. Produce the packet file set using evidence-grounded statements.
7. Keep proposed WORKING_ITEMS (workflow: scope-change) actions conservative:
   - use `MODIFY` for decomposition text, package/deliverable metadata, or scope-ledger clarification;
   - use `RECLASSIFY`, `MERGE`, `SPLIT`, `ADD`, or `REMOVE` only when the evidence clearly requires structural amendment framing;
   - use `TBD` where the action requires human or WORKING_ITEMS (workflow: scope-change) ruling.
8. Return the outputs, evidence read and validation notes to the caller.

## Non-Negotiable Constraints

- Do not claim any local need declaration was changed.
- Do not claim any SCC was closed.
- Do not claim WORKING_ITEMS (workflow: scope-change) was initiated.
- Do not claim project-wide blocker status.
- Unknowns remain `TBD`.
- Every proposed action must cite at least one evidence row in `Evidence_Index.csv`.
- Packet readiness means the packet is structurally complete enough for human review. It is not WORKING_ITEMS (workflow: scope-change) intake acceptance unless a human explicitly selects the packet for WORKING_ITEMS (workflow: scope-change).
