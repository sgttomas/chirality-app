# BRIEF SCHEMA — scope-change-packet

Use this skill when WORKING_ITEMS needs one PKG-00 control deliverable to produce a SCOPE_CHANGE-consumable packet.

## Required Fields

```yaml
PURPOSE: Produce one Scope Change Consumable Packet.
RequestedBy: WORKING_ITEMS
ScopePath: /abs/path/to/DEL-00-XX_...
TaskSkill: scope-change-packet
ApplyEdits: true
AllowedWriteTargets:
  - /abs/path/to/DEL-00-XX_.../scope-change-packets/<packet-folder>/
  - /abs/path/to/DEL-00-XX_.../_run_records/
RuntimeOverrides:
  PACKET_ID: PKG00-SCA-PACKET-001
  PACKET_PATH: /abs/path/to/DEL-00-XX_.../scope-change-packets/<packet-folder>
  PACKET_TITLE: SCC-002 PKG-10 Policy Proposal
  SCC_ID: SCC-002
  DECOMP_VARIANT: SOFTWARE
  DECOMPOSITION_PATH: /abs/path/to/execution/_Decomposition/Chirality_App_vNext_SOFTWARE_DECOMP_v3_2.md
  DEPCLOSURE_SNAPSHOT: /abs/path/to/execution/_Reconciliation/DepClosure/CLOSURE_...
  AFFECTED_DELIVERABLES: DEL-10-02;DEL-10-03
  FOCUS_ROWS: DEP-10-02-004;DEP-10-03-006
ExpectedOutputs:
  - Packet_Contract.md
  - Packet_Datasheet.md
  - Packet_Specification.md
  - Packet_Procedure.md
  - Packet_Rationale.md
  - SCOPE_CHANGE_INIT.md
  - Proposed_SCA_Actions.csv
  - Affected_Surfaces.csv
  - Evidence_Index.csv
  - Packet_QA.md
```

## Optional Runtime Overrides

- `BIDIRECTIONAL_PAIRS` — semicolon-separated pair labels for SCC-001 packet subsets.
- `PACKET_SCOPE_NOTE` — extra bounded framing.
- `MAX_ACTIONS` — soft cap on proposed actions.

## Required Custom Instructions

- Treat packet outputs as proposals and evidence only.
- Do not edit product deliverables, dependency registers, decomposition files, `_ScopeChange/`, or `_Reconciliation/`.
- Do not report SCC closure or project-wide blocked/unblocked status.
- Keep `SCOPE_CHANGE_INIT.md` human-initiated and gate-controlled.

