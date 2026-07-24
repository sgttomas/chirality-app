---
name: scope-change-packet
description: Produce a bounded PKG-00 Scope Change Consumable Packet for later human-initiated SCOPE_CHANGE intake; use scc-resolution-case for active SCC resolution receptacles.
compatibility: Chirality TASK in generic shell mode; dispatched by WORKING_ITEMS for PKG-00 control deliverables.
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — scope-change-packet

## Purpose

Produce one **Scope Change Consumable Packet** under a PKG-00 control deliverable. The packet prepares evidence, proposed actions, affected-surface inventories, and a human-readable SCOPE_CHANGE seed request.

The packet is not an amendment, not a dependency ruling, and not a DepClosure result. It is a bounded staging artifact for a later human-initiated SCOPE_CHANGE workflow.

For active SCC resolution work, use `TASK + scc-resolution-case`. Existing scope-change packets may be retained as seed evidence inside an SCC Resolution Case.

## Suitable Shell

- `TASK` in generic shell mode with `ScopePath` set to one PKG-00 control deliverable folder.

## Required Inputs

- `ScopePath` — one PKG-00 control deliverable folder.
- `RuntimeOverrides.PACKET_ID` — local packet ID, for example `PKG00-SCA-PACKET-001`.
- `RuntimeOverrides.PACKET_PATH` — absolute output folder inside `{ScopePath}/scope-change-packets/`.
- `RuntimeOverrides.PACKET_TITLE` — human-readable packet title.
- `RuntimeOverrides.SCC_ID` — `SCC-001` or `SCC-002`.
- `RuntimeOverrides.DECOMP_VARIANT` — `SOFTWARE`.
- `RuntimeOverrides.DECOMPOSITION_PATH` — current decomposition authority.
- `RuntimeOverrides.DEPCLOSURE_SNAPSHOT` — accepted upstream DepClosure snapshot.
- `RuntimeOverrides.AFFECTED_DELIVERABLES` — semicolon-separated deliverable IDs.
- `RuntimeOverrides.FOCUS_ROWS` — semicolon-separated dependency row IDs or `TBD`.

## Read Boundary

Read only:

- the PKG-00 control deliverable in `ScopePath`;
- PKG-00 package-level control files;
- the cited decomposition document;
- the cited DepClosure snapshot and evidence files;
- affected product deliverable `_CONTEXT.md`, `_STATUS.md`, `_DEPENDENCIES.md`, `Dependencies.csv`, and four-doc kit files.

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
- `{ScopePath}/_run_records/TASK_RUN_*.md`

Never write:

- product package files;
- any `Dependencies.csv`;
- `_ScopeChange/`;
- `_Reconciliation/`;
- decomposition files.

## Output Contract

Each packet must contain the fixed ten-file set named above.

`Packet_Contract.md` defines consumption rules, authority limits, SCOPE_CHANGE gate mapping, and non-goals.

`Packet_Datasheet.md` records identity, SCC baseline, affected deliverables, affected rows, and evidence inventory.

`Packet_Specification.md` records proposed amendment requirements, action candidates, acceptance criteria, and invariant checks.

`Packet_Procedure.md` gives SCOPE_CHANGE intake and gate-by-gate use instructions.

`Packet_Rationale.md` records source-grounded reasoning, why dependency-edge treatment is insufficient, risks, and alternatives rejected.

`SCOPE_CHANGE_INIT.md` is a seed request. It must say it is not valid until the human explicitly initiates SCOPE_CHANGE.

`Proposed_SCA_Actions.csv` uses columns:

```csv
PacketID,ActionSeq,ActionType,EntityType,EntityID,Description,AffectedDeliverables,AffectedFiles,EvidenceRefs,SCOPE_CHANGE_Gate,Status
```

`Affected_Surfaces.csv` uses columns:

```csv
PacketID,SurfaceType,SurfacePath,PackageRole,ChangeClass,OwnerWorkflow,RequiredAction,EvidenceRefs,Status
```

`Evidence_Index.csv` uses columns:

```csv
EvidenceID,SourcePath,SourceRef,EvidenceType,Supports,Notes
```

`Packet_QA.md` records checklist results, unresolved TBDs, and packet readiness verdict. The verdict must distinguish structural packet validity from SCOPE_CHANGE intake acceptance.

## Method

1. Load `AGENT_TASK.md`, this skill, and companion files.
2. Resolve `PACKET_PATH` and confirm it is inside `ScopePath`.
3. Read PKG-00 control files and deliverable-local packet context.
4. Read the cited DepClosure evidence for the target SCC.
5. Read only explicitly affected product deliverables and dependency registers.
6. Produce the packet file set using evidence-grounded statements.
7. Keep proposed SCOPE_CHANGE actions conservative:
   - use `MODIFY` for decomposition text, package/deliverable metadata, or scope-ledger clarification;
   - use `RECLASSIFY`, `MERGE`, `SPLIT`, `ADD`, or `REMOVE` only when the evidence clearly requires structural amendment framing;
   - use `TBD` where the action requires human or SCOPE_CHANGE ruling.
8. Write a TASK run record with outputs, evidence read, and validation notes.

## Non-Negotiable Constraints

- Do not claim any dependency row was changed.
- Do not claim any SCC was closed.
- Do not claim SCOPE_CHANGE was initiated.
- Do not claim project-wide blocker status.
- Unknowns remain `TBD`.
- Every proposed action must cite at least one evidence row in `Evidence_Index.csv`.
- Packet readiness means the packet is structurally complete enough for human review. It is not SCOPE_CHANGE intake acceptance unless a human explicitly selects the packet for SCOPE_CHANGE.
