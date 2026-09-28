# DEL-02-03 dependency extraction — 2026-09-27

- Actual mechanism: delegated-harness-native fresh terminal TASK `/root/renewal_research_strategy/dep_del_02_03`; parent WORKING_ITEMS `/root/renewal_research_strategy`, under HELP_HUMAN `/root`. No child delegation.
- Scope: one DEL-02-03 register using `chirality-root:bundled:workflow:dependency-extract`; method basis `ffb2b6289dde79a35f22f5d87256df0aa4d3289a`; current unchanged source per brief is setup `ddd721a90ade401d452d102e6e40d1ffdae654eb` / identical-tree main `82efe62783bbe8ac7d21476a6662195c0b0a7587`.
- Instruction write boundary: only this Deliverable's Dependencies.csv, _DEPENDENCIES.md and this run record. Actual host filesystem access is broader; no claim of path-level delegation enforcement. No Git mutation, source/decomposition/status/sibling edits, external messaging, graph construction, lifecycle advancement, adoption or acceptance.
- Source before SHA256: `9a921ba500271c441e64db2e1f34acf41c95fa7821d6dff3d8659352bb4db7fb` matches the dispatched row.
- Dispatch CSV snapshot SHA256: `c7d1625657390580b7038bbb35661bbc1c742c6967c691387bd42a32e690a499`; only this assignment plus target-path rows used. Manager may update its work state concurrently; this identifies the actual read snapshot.
- Original _DEPENDENCIES.md SHA256: `c5f8f67b35f89495ca41bebf9284c38bfc939bed21a50866aedb48f090412021`. Human-owned prefix SHA256: `f48c777d543465bb425bf36282a02334702eb82750c206553b98edbc9855a9ec`; preserved byte-for-byte through the Extracted Register heading. Original history retained: `- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.`.
- Extraction result: 21 ACTIVE / 0 RETIRED; 8 ANCHOR (one parent, seven traces); 13 EXECUTION (six Deliverable, seven External, zero Unknown). Anchors completed before execution pass; no prior CSV or declared rows.
- Caveats: no execution satisfaction asserted; INITIALIZED is contract maturity only. Five open decisions preserve owners and points of need. SWBPIPE DEP-001 remains external and owner-reported building. VER-003 actual positive fixture act evidence does not gate independent/negative cases. DEL-05-01 ownership alone is not an edge. No global closure/qualification claim.

## Actual read identities

| Source relative to checkout | Read extent | SHA256 |
|---|---|---|
| AGENTS.md | full | `c8ce87ef342902cb081bc659b26fc9a4edda1b6dba513814e5cb1e14e0b1dffd` |
| agents/AGENT_TASK.md | full | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| workflows/dependency-extract/WORKFLOW.md | full across read segments | `e5523ebabccf44337ec531280d4d91be2ce7ff1477bd39568a18bb0c4c9f18c3` |
| workflows/dependency-extract/resources/brief.md | full | `b51a8166eda6131302c64dcbc893e375c028dd8931f9d49d64b4a0fb8cb49fde` |
| workflows/dependency-extract/resources/checks.md | full | `a12aa8b32c955d623623353c39b76f771ad9d6b48a9e513b0e0bad9a706a0457` |
| workflows/dependency-extract/resources/tools.md | full | `dbbe7ee79e47dbf673b17e71413c5203f84b2772887dd6406f2ecbac81024db8` |
| projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/DEPENDENCY_BRIEF.md | full | `736418e84c8cba42655c75dfe6020fd32d0fec628718071122f3580cff0ac4ae` |
| projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/ScopeOfWork.md | full | `9a921ba500271c441e64db2e1f34acf41c95fa7821d6dff3d8659352bb4db7fb` |
| projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/_REFERENCES.md | full | `3e92f14cc4d586f7fede1cbe78703b3d34d898626c6977cd231eb5612ff86bb9` |
| projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md | full | `9d44c2ad12f484f3d13901f28d99725ac7fc538dfacc85b832cdbe3c62b8fb81` |
| projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Packages.csv | relevant rows and fields only | `b8a9b949b629fb8dbe3343e0e5a1f09a30621785d99676f71adb1b285f741fbd` |
| projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv | relevant rows and fields only | `bcdf6f2f5352e00360c19a956bd22c026909c388d77c76f92b4983ed906415eb` |
| projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv | relevant rows and fields only | `363643306d3bbda80f4496943a5d1de5187d7910fabdf5b89f929e6c9605fd73` |
| projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Objectives.csv | relevant rows and fields only | `e8e5003d9241c4e6a1d74d00a474b76f3780c6d03c93f66dc1b5c5caa7c9c248` |
| projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Open_Issues.csv | relevant rows and fields only | `b65578a0ff34a45d705aac3d8b714e0a0632bec73fd73c5cc0ac8a19c85dc821` |
| projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/External_Dependencies.csv | relevant rows and fields only | `fa2922f7a4d8c5b31e86752ef44fb654ec037cc46995153ced6345e90c84c134` |

## Validation

- `python3 tools/validation/validate_dependencies_schema.py "projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Dependencies.csv"` — exit 0; VALID: /Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Dependencies.csv;   Columns: 29 (29 required + 0 extension);   Data rows: 21

- `python3 tools/validation/validate_enum.py ENUM VALUE` — all 22 distinct used enum/value pairs exit 0: DEPENDENCY_CLASS=ANCHOR,EXECUTION; ANCHOR_TYPE=IMPLEMENTS_NODE,NOT_APPLICABLE,TRACES_TO_REQUIREMENT; DIRECTION=DOWNSTREAM,UPSTREAM; DEPENDENCY_TYPE=CONSTRAINT,HANDOVER,INTERFACE,OTHER,PREREQUISITE; TARGET_TYPE=DELIVERABLE,EXTERNAL,REQUIREMENT,WBS_NODE; EXPLICITNESS=EXPLICIT; CONFIDENCE=HIGH; ORIGIN=EXTRACTED; STATUS=ACTIVE; SATISFACTION_STATUS=NOT_APPLICABLE,TBD.

- `bash tools/validation/validate_id_format.sh TYPE VALUE` — all 39 distinct supported ID/type pairs exit 0: DEL=DEL-02-01,DEL-02-02,DEL-02-03,DEL-03-01,DEL-04-01,DEL-04-03,DEL-09-06; DEP=DEP-02-03-001,DEP-02-03-002,DEP-02-03-003,DEP-02-03-004,DEP-02-03-005,DEP-02-03-006,DEP-02-03-007,DEP-02-03-008,DEP-02-03-009,DEP-02-03-010,DEP-02-03-011,DEP-02-03-012,DEP-02-03-013,DEP-02-03-014,DEP-02-03-015,DEP-02-03-016,DEP-02-03-017,DEP-02-03-018,DEP-02-03-019,DEP-02-03-020,DEP-02-03-021; OBJ=OBJ-003,OBJ-005; PKG=PKG-02,PKG-03,PKG-04,PKG-09; SOW=SOW-051,SOW-052,SOW-053,SOW-054,SOW-055. The five OI identifiers and external-register DEP-001 are validated by exact accepted companion-row lookup, not recast into local dependency IDs.

- In-memory Python assertions — PASS: 29 columns; 21 unique/prefix-correct row IDs; one parent; 8 anchors/13 execution; 7 External/0 Unknown; no duplicate edge keys; mandatory field presence; every quote verbatim and <=30 words; non-deliverable ID placement; 8 NOT_APPLICABLE/13 TBD closure values; summary counts; exact human-owned prefix and prior history preserved; source before/after SHA256 identical; OI/external references exist in accepted companions.

- `python3 tools/validation/validate_decomposition_registers.py "projects/chirality-app-v4/execution" --families EVQ,DRB --max-per-code 10000` — exit 0; no findings for this register, including EVQ-003, EVQ-004 and DRB-006. Whole-execution report is read-only; any sibling findings are outside this local result. No report file written.


## Output identities

- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Dependencies.csv` — SHA256 `be8c2c02491ed181f9c9c66a1da89b2c2ef9347bae61bd2535d74bad0f664f75`.
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/_DEPENDENCIES.md` — SHA256 `c461be9b42de5d2e309d27abe50958ce9054bb3e89f7ca3a32efa3e208ce886b`.
- Source after SHA256: `9a921ba500271c441e64db2e1f34acf41c95fa7821d6dff3d8659352bb4db7fb` (unchanged).
- This record: `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/_run_records/dependency-extract-20260927.md`; its final SHA256 is returned to the caller separately to avoid self-referential hashing.
