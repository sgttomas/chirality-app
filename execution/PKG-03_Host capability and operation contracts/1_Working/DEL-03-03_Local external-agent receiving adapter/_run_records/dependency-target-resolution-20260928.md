# Dependency target resolution — DEL-03-03 R3

- Timestamp: 2026-09-28T04:25:33+00:00; UTC date used for repaired row LastSeen: 2026-09-28.
- Executing fresh terminal TASK: `/root/renewal_research_strategy/resolve_dep_03_03`; parent WORKING_ITEMS `/root/renewal_research_strategy`, under HELP_HUMAN `/root`. Mechanism: delegated-harness-native descendant. No child delegation.
- Selected method: `chirality-root:bundled:workflow:dependency-extract`, MODE=UPDATE, STRICTNESS=CONSERVATIVE, CONSUMER_CONTEXT=NONE, ARCHITECTURE_BASIS_POLICY=NONE, DOC_ROLE_MAP=DEFAULT. Scope only DEP-03-03-008 repair R3. SOURCE_DOCS=ANCHOR_DOC=EXECUTION_DOC_ORDER=`ScopeOfWork.md`.
- RUN_ROOT: `~/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`. Configured DECOMPOSITION_PATH: `~/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`; this repair read only the accepted companion CSV rows below, not that markdown body. Method basis supplied by common brief: `ffb2b6289dde79a35f22f5d87256df0aa4d3289a`; actual consulted bytes hashed below.
- Allowed writes: own Dependencies.csv, own _DEPENDENCIES.md and this new record only. Host filesystem access is broader; the bound is instruction-enforced. No Git operation, global validator, graph/status/source edit, sibling SoW read, delivery or human-decision act.

## Evidence and resolution

Pass 1 confirmed and preserved the existing single PKG-03 parent plus SOW-148/183/184 and OBJ-004 traces before Pass 2. Local REQ-003 says verbatim: “The receiver carries policy supplied through PKG-04; it does not decide OI-001 or OI-002.” The production-method opening requires adopted PKG-04 policy, and TBD-001/002 retains the owner rulings and actual points of need.

Accepted `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv` SOW-074/179/180/181/182/235 each assigns the policy-producing obligation exclusively to DEL-04-01. `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv` DEL-04-01 names the adopted policy contract and CONFIG representation. The supplied independent `TARGET_RESOLUTION.md` R3 identifies producer OUT-001/002; that prior producer-primary proof was supplied evidence, not a new sibling-source read. `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Open_Issues.csv` OI-001/002 remain OPEN with Owner with App/SWB contract owners. Identity resolution supplies no policy value, host enforcement, technical delivery or satisfaction.

## Exact register field diff

DependencyID remains `DEP-03-03-008`. TargetPackageID remains `PKG-04`. Seven fields changed; every unlisted field and every other row is unchanged.

| Field | Before | After |
|---|---|---|
| TargetType | PACKAGE | DELIVERABLE |
| TargetDeliverableID | (blank) | DEL-04-01 |
| TargetRefID | PKG-04 | (blank) |
| TargetName | Human acts, autonomy and run evidence | Operation-policy and human-act distinctions |
| TargetLocation | projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Packages.csv#PKG-04 | projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions |
| LastSeen | 2026-09-27 | 2026-09-28 |
| Notes | FACT: Supplied adopted policy is the actual input, not a package lifecycle inference. OI-001 remains with Owner/App/SWB contract owners before operation-policy production contracts; OI-002 remains with the same owners before permission-policy implementation. No guessed DEL-04-* mapping or blanket definition hold. | FACT: Adopted operation-policy meaning and representation are produced by App DEL-04-01 under accepted G3 SOW-074/179/180/181/182/235 and its OUT-001/002. The owner with App/SWB contract owners retains OI-001/OI-002 rulings before affected policy/permission implementation. Actual adopted policy must be received for policy-dependent production/fixtures; no policy value, host enforcement or satisfaction is inferred. |

RequiredMaturity=TBD, ProposedMaturity blank, SatisfactionStatus=PENDING, Direction=UPSTREAM, DependencyClass=EXECUTION and DependencyType=PREREQUISITE remain unchanged. Statement, source locator, verbatim quote, FirstSeen and Status=ACTIVE are preserved. The index changes only the R3 table target, adds repair Run Notes and appends one Run History entry.

## Local checks

- Schema validator PASS: canonical 29 columns, 12 rows. All documented enum and supported standard-ID invocations below exited 0.
- 12 unique IDs; 5 ANCHOR (one parent/four traces), 7 EXECUTION (six upstream/one downstream); 12 ACTIVE, 0 RETIRED, 0 DECLARED; 3 EXTERNAL, 0 UNKNOWN. Closure states: 5 NOT_APPLICABLE, 7 PENDING, 0 SATISFIED.
- Own source before/after matches dispatch; report SHA matches supplied hash; accepted allocation, target name and target directory verified. All 12 EvidenceQuote values remain verbatim and at most 30 words. No missing source/locus, duplicate logical row or ID, bad prefix, blank quote or placeholder locus: local EVQ-003=0, EVQ-004=0, DRB-006=0.
- 11 untouched rows remain byte-identical; only seven cells changed in the repaired row. Human-owned mode/declarations and previous Run History remain byte-identical. Both initial declaration placeholders skipped; mirrors added/refreshed/retired=0/0/0. All protected local files below remain byte-identical, including old run, source, status and references.
- No global EVQ/DRB/closure check while peers write. This local verification is not independent repair review or project graph acceptance. Manager retains independent review, source freeze and global closure downstream.

### Validator invocations

```text
$ python3 tools/validation/validate_dependencies_schema.py 'projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Dependencies.csv'
exit=0; VALID: projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Dependencies.csv
  Columns: 29 (29 required + 0 extension)
  Data rows: 12
$ python3 tools/validation/validate_enum.py DEPENDENCY_CLASS ANCHOR
exit=0; VALID: ANCHOR is a valid DEPENDENCY_CLASS
$ python3 tools/validation/validate_enum.py DEPENDENCY_CLASS EXECUTION
exit=0; VALID: EXECUTION is a valid DEPENDENCY_CLASS
$ python3 tools/validation/validate_enum.py ANCHOR_TYPE IMPLEMENTS_NODE
exit=0; VALID: IMPLEMENTS_NODE is a valid ANCHOR_TYPE
$ python3 tools/validation/validate_enum.py ANCHOR_TYPE NOT_APPLICABLE
exit=0; VALID: NOT_APPLICABLE is a valid ANCHOR_TYPE
$ python3 tools/validation/validate_enum.py ANCHOR_TYPE TRACES_TO_REQUIREMENT
exit=0; VALID: TRACES_TO_REQUIREMENT is a valid ANCHOR_TYPE
$ python3 tools/validation/validate_enum.py DIRECTION DOWNSTREAM
exit=0; VALID: DOWNSTREAM is a valid DIRECTION
$ python3 tools/validation/validate_enum.py DIRECTION UPSTREAM
exit=0; VALID: UPSTREAM is a valid DIRECTION
$ python3 tools/validation/validate_enum.py DEPENDENCY_TYPE HANDOVER
exit=0; VALID: HANDOVER is a valid DEPENDENCY_TYPE
$ python3 tools/validation/validate_enum.py DEPENDENCY_TYPE INTERFACE
exit=0; VALID: INTERFACE is a valid DEPENDENCY_TYPE
$ python3 tools/validation/validate_enum.py DEPENDENCY_TYPE OTHER
exit=0; VALID: OTHER is a valid DEPENDENCY_TYPE
$ python3 tools/validation/validate_enum.py DEPENDENCY_TYPE PREREQUISITE
exit=0; VALID: PREREQUISITE is a valid DEPENDENCY_TYPE
$ python3 tools/validation/validate_enum.py TARGET_TYPE DELIVERABLE
exit=0; VALID: DELIVERABLE is a valid TARGET_TYPE
$ python3 tools/validation/validate_enum.py TARGET_TYPE EXTERNAL
exit=0; VALID: EXTERNAL is a valid TARGET_TYPE
$ python3 tools/validation/validate_enum.py TARGET_TYPE REQUIREMENT
exit=0; VALID: REQUIREMENT is a valid TARGET_TYPE
$ python3 tools/validation/validate_enum.py TARGET_TYPE WBS_NODE
exit=0; VALID: WBS_NODE is a valid TARGET_TYPE
$ python3 tools/validation/validate_enum.py EXPLICITNESS EXPLICIT
exit=0; VALID: EXPLICIT is a valid EXPLICITNESS
$ python3 tools/validation/validate_enum.py CONFIDENCE HIGH
exit=0; VALID: HIGH is a valid CONFIDENCE
$ python3 tools/validation/validate_enum.py ORIGIN EXTRACTED
exit=0; VALID: EXTRACTED is a valid ORIGIN
$ python3 tools/validation/validate_enum.py STATUS ACTIVE
exit=0; VALID: ACTIVE is a valid STATUS
$ python3 tools/validation/validate_enum.py SATISFACTION_STATUS NOT_APPLICABLE
exit=0; VALID: NOT_APPLICABLE is a valid SATISFACTION_STATUS
$ python3 tools/validation/validate_enum.py SATISFACTION_STATUS PENDING
exit=0; VALID: PENDING is a valid SATISFACTION_STATUS
$ bash tools/validation/validate_id_format.sh DEL DEL-03-01
exit=0; VALID: DEL-03-01 matches DEL format
$ bash tools/validation/validate_id_format.sh DEL DEL-03-02
exit=0; VALID: DEL-03-02 matches DEL format
$ bash tools/validation/validate_id_format.sh DEL DEL-03-03
exit=0; VALID: DEL-03-03 matches DEL format
$ bash tools/validation/validate_id_format.sh DEL DEL-04-01
exit=0; VALID: DEL-04-01 matches DEL format
$ bash tools/validation/validate_id_format.sh DEL DEL-09-09
exit=0; VALID: DEL-09-09 matches DEL format
$ bash tools/validation/validate_id_format.sh DEP DEP-03-03-001
exit=0; VALID: DEP-03-03-001 matches DEP format
$ bash tools/validation/validate_id_format.sh DEP DEP-03-03-002
exit=0; VALID: DEP-03-03-002 matches DEP format
$ bash tools/validation/validate_id_format.sh DEP DEP-03-03-003
exit=0; VALID: DEP-03-03-003 matches DEP format
$ bash tools/validation/validate_id_format.sh DEP DEP-03-03-004
exit=0; VALID: DEP-03-03-004 matches DEP format
$ bash tools/validation/validate_id_format.sh DEP DEP-03-03-005
exit=0; VALID: DEP-03-03-005 matches DEP format
$ bash tools/validation/validate_id_format.sh DEP DEP-03-03-006
exit=0; VALID: DEP-03-03-006 matches DEP format
$ bash tools/validation/validate_id_format.sh DEP DEP-03-03-007
exit=0; VALID: DEP-03-03-007 matches DEP format
$ bash tools/validation/validate_id_format.sh DEP DEP-03-03-008
exit=0; VALID: DEP-03-03-008 matches DEP format
$ bash tools/validation/validate_id_format.sh DEP DEP-03-03-009
exit=0; VALID: DEP-03-03-009 matches DEP format
$ bash tools/validation/validate_id_format.sh DEP DEP-03-03-010
exit=0; VALID: DEP-03-03-010 matches DEP format
$ bash tools/validation/validate_id_format.sh DEP DEP-03-03-011
exit=0; VALID: DEP-03-03-011 matches DEP format
$ bash tools/validation/validate_id_format.sh DEP DEP-03-03-012
exit=0; VALID: DEP-03-03-012 matches DEP format
$ bash tools/validation/validate_id_format.sh OBJ OBJ-004
exit=0; VALID: OBJ-004 matches OBJ format
$ bash tools/validation/validate_id_format.sh PKG PKG-03
exit=0; VALID: PKG-03 matches PKG format
$ bash tools/validation/validate_id_format.sh PKG PKG-04
exit=0; VALID: PKG-04 matches PKG format
$ bash tools/validation/validate_id_format.sh PKG PKG-09
exit=0; VALID: PKG-09 matches PKG format
$ bash tools/validation/validate_id_format.sh SOW SOW-148
exit=0; VALID: SOW-148 matches SOW format
$ bash tools/validation/validate_id_format.sh SOW SOW-183
exit=0; VALID: SOW-183 matches SOW format
$ bash tools/validation/validate_id_format.sh SOW SOW-184
exit=0; VALID: SOW-184 matches SOW format
```

## Actual input and helper SHA256 identities

| Path | SHA256 | Read extent |
|---|---|---|
| `AGENTS.md` | `c8ce87ef342902cb081bc659b26fc9a4edda1b6dba513814e5cb1e14e0b1dffd` | full Root entry |
| `agents/AGENT_TASK.md` | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` | full active role |
| `workflows/dependency-extract/execution.json` | `bfb5417afe85ee0e268a4c0353f4378a42a015925f383232bdaa766b866110e2` | full descriptor |
| `workflows/dependency-extract/WORKFLOW.md` | `e5523ebabccf44337ec531280d4d91be2ce7ff1477bd39568a18bb0c4c9f18c3` | selected full entrypoint including follow-up excerpt for truncated section |
| `workflows/dependency-extract/resources/brief.md` | `b51a8166eda6131302c64dcbc893e375c028dd8931f9d49d64b4a0fb8cb49fde` | full |
| `workflows/dependency-extract/resources/checks.md` | `a12aa8b32c955d623623353c39b76f771ad9d6b48a9e513b0e0bad9a706a0457` | full |
| `workflows/dependency-extract/resources/tools.md` | `dbbe7ee79e47dbf673b17e71413c5203f84b2772887dd6406f2ecbac81024db8` | full |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/DEPENDENCY_BRIEF.md` | `736418e84c8cba42655c75dfe6020fd32d0fec628718071122f3580cff0ac4ae` | full common brief; dispatch overrides write record name and repair scope |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/DEPENDENCY_WORK_ITEMS.csv` | `eec90734e48ada5dd9efc5cf203c8eecacf1e39e1965aa2a1d82a83acd70e727` | DEL-03-03 row only semantically; full CSV parsed |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/TARGET_RESOLUTION.md` | `f85a371853ec5ef18d3a1b1ebdc016e37e1bbd321217f726c4350204a2cefaa1` | basis, bounded repair R3 and provenance; table/context excerpts also supplied |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/ScopeOfWork.md` | `5ac5db97eba3851eb5324054e5a2b38429a53e8e9c85428903432cd8d9efb1b6` | full own source |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv` | `bcdf6f2f5352e00360c19a956bd22c026909c388d77c76f92b4983ed906415eb` | DEL-03-03/DEL-04-01 rows only semantically |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv` | `363643306d3bbda80f4496943a5d1de5187d7910fabdf5b89f929e6c9605fd73` | SOW-074/148/179/180/181/182/183/184/235 rows only semantically |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Packages.csv` | `b8a9b949b629fb8dbe3343e0e5a1f09a30621785d99676f71adb1b285f741fbd` | PKG-03/PKG-04 rows only semantically |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Objectives.csv` | `e8e5003d9241c4e6a1d74d00a474b76f3780c6d03c93f66dc1b5c5caa7c9c248` | OBJ-004 only semantically |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Open_Issues.csv` | `b65578a0ff34a45d705aac3d8b714e0a0632bec73fd73c5cc0ac8a19c85dc821` | OI-001/OI-002 only semantically |
| `tools/validation/validate_dependencies_schema.py` | `75cd74768cc8edf91c6f40b582f0fb570d2427894e6c2236ea2fe7d384291f5f` | executed; hashed, not semantically read |
| `tools/validation/validate_enum.py` | `562934b075b20e7ec366baf60146cf7524acaebad8612b87873c4828dbeeaa70` | source inspected and executed |
| `tools/validation/validate_id_format.sh` | `370c946c301323b1bb273d268f04d4dc4187b865d9d2865b5273f0dd27d0acac` | source inspected and executed |

## Local before/after identities

| Local path | Before SHA256 | After SHA256 |
|---|---|---|
| `Dependencies.csv` | `e6d39f4a1034ae02809157a2dba717790886b5ea8481e9620786e18ba4384396` | `a962d4d5007fd037b07a8e65bce42957d995a8e34bc3f17581d0eda3748067cf` |
| `_CONTEXT.md` | `adf90811ab41e7fcf5b9e9cb1bf68dbf00cf3f6a2e7d5c24cc327164034eedeb` | `adf90811ab41e7fcf5b9e9cb1bf68dbf00cf3f6a2e7d5c24cc327164034eedeb` |
| `_STATUS.md` | `e095e9303a85222160eed0f22cc671923a48b45c86a081a7ddbd7a03c4cd9c72` | `e095e9303a85222160eed0f22cc671923a48b45c86a081a7ddbd7a03c4cd9c72` |
| `_SEMANTIC.md` | `a3e8e171eaedcd6d49980de2e4f000b410829cf1dc16d5dbd897cf38518a8c02` | `a3e8e171eaedcd6d49980de2e4f000b410829cf1dc16d5dbd897cf38518a8c02` |
| `ScopeOfWork.md` | `5ac5db97eba3851eb5324054e5a2b38429a53e8e9c85428903432cd8d9efb1b6` | `5ac5db97eba3851eb5324054e5a2b38429a53e8e9c85428903432cd8d9efb1b6` |
| `_DEPENDENCIES.md` | `e32a058335b485e73c744f7db8f4c1910592fad418c4fa60289aa8d840d4df11` | `95efc22df551f741c558167811842c03437990c6f214b5561eadce61a425e2f0` |
| `_REFERENCES.md` | `2ba400b208c1ad0276eac4046ec5f2b3b48d0abaec4becbca46e2b51a6a79402` | `2ba400b208c1ad0276eac4046ec5f2b3b48d0abaec4becbca46e2b51a6a79402` |
| `_run_records/dependency-extract-20260927.md` | `4ed39176457461f987c664abb91c6c7a8808cc1f25ab5e9c03ffed7a55c146ac` | `4ed39176457461f987c664abb91c6c7a8808cc1f25ab5e9c03ffed7a55c146ac` |
