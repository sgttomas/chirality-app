# DEL-01-05 dependency extraction — 2026-09-27

- Terminal TASK `/root/renewal_research_strategy/dep_del_01_05`, delegated-harness-native child of WORKING_ITEMS `/root/renewal_research_strategy` under HELP_HUMAN `/root`. Actual native TASK execution; no delegated descendants, Git action or source change.
- Method `chirality-root:bundled:workflow:dependency-extract`; source basis `ffb2b6289dde79a35f22f5d87256df0aa4d3289a`; unchanged candidate/integration identities and parameters retained in `_DEPENDENCIES.md`. No other role instruction or skill body consulted. This brief restricts writes more narrowly than actual workspace filesystem permissions.
- Writes confined to own `Dependencies.csv`, `_DEPENDENCIES.md`, and this record. No prior CSV existed. Initial index SHA256: `41ebb08c83573cd521507bede3071b23472e556b1599444071d7fa5c5138c1c6`. An initial combined file read stopped when absent CSV was encountered; remaining index/reference reads completed separately.
- Pass 1 completed 11 anchors (parent PKG-01; 8 SOW + 2 OBJ traces) before Pass 2 extracted 5 positive execution edges (4 upstream, 1 downstream). 16 ACTIVE EXTRACTED; DECLARED/RETIRED/EXTERNAL/UNKNOWN=0. DOCUMENT targets=2 with TBD paths and unresolved actual decision/definition values; known document kind is not known fulfilment.
- All 5 execution rows PENDING; 11 anchors NOT_APPLICABLE; 0 SATISFIED. INITIALIZED on 3 deliverable-target rows is only local contract maturity, distinct from actual consumed/supplied artifacts. OI-009/010/012 and endpoint capability evidence remain unresolved. No provider delivery, host construction, product qualification, release, adoption or global closure claimed.

## Validation

- `python3 tools/validation/validate_dependencies_schema.py <own>/Dependencies.csv`: exit 0; VALID: projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Dependencies.csv
  Columns: 29 (29 required + 0 extension)
  Data rows: 16
- `python3 tools/validation/validate_enum.py <ENUM> <VALUE>`: all 21 calls exit 0. Checked values: {"ANCHOR_TYPE": ["IMPLEMENTS_NODE", "NOT_APPLICABLE", "TRACES_TO_REQUIREMENT"], "CONFIDENCE": ["HIGH"], "DEPENDENCY_CLASS": ["ANCHOR", "EXECUTION"], "DEPENDENCY_TYPE": ["CONSTRAINT", "HANDOVER", "OTHER", "PREREQUISITE"], "DIRECTION": ["DOWNSTREAM", "UPSTREAM"], "EXPLICITNESS": ["EXPLICIT"], "ORIGIN": ["EXTRACTED"], "SATISFACTION_STATUS": ["NOT_APPLICABLE", "PENDING"], "STATUS": ["ACTIVE"], "TARGET_TYPE": ["DELIVERABLE", "DOCUMENT", "REQUIREMENT", "WBS_NODE"]}.
- `bash tools/validation/validate_id_format.sh <TYPE> <ID>`: all 31 calls exit 0. Checked DEP-01-05-001 through DEP-01-05-016; DEL-01-01, DEL-01-05, DEL-05-01; PKG-01, PKG-05; SOW-009 through SOW-012, SOW-132, SOW-133, SOW-149, SOW-150; OBJ-002, OBJ-004. OI-009/OI-010 are source-exact references; the format helper does not support OI.
- Python assertions: 29 columns/16 rows; unique IDs and logical rows; 1 parent; source-matching deliverable/DEP prefix; complete statements/targets/evidence; all 16 quotes verbatim and <=30 words; non-deliverable TargetDeliverableID empty; execution satisfaction PENDING; history prefix and entire human-owned prefix byte-identical; source hash equals dispatch before/after; index counts match register. All passed.
- Preserved human-owned/index prefix SHA256: `f0234af0fb34ce71780dec2157ad5baf6f303a7058d259507bba71ead532b7be`. Two initial-setup declaration placeholders skipped; no declarations created.
- Optional whole-execution EVQ/DRB validator not invoked; equivalent local quote/locus/prefix checks passed. Independent integration/graph checking remains downstream.

## Output identities

- `Dependencies.csv`: `3b038c98f97cd6855b42b10e1602a24c34152f3defa582c037d6ee642f4796a6`
- `_DEPENDENCIES.md`: `7f9f3f8101ccbdcd0dca2bb6f6a4d75217c35802a4940542f83e82530a9030b0`
- Source SHA256 unchanged: `baf68c79b5b8fdf01300fc255d7cf8e433975e6275daadf67b914b4e51eca4a6`

## Actually consulted origins and SHA256

| Repository-relative source | Read extent | SHA256 |
|---|---|---|
| `AGENTS.md` | full | `c8ce87ef342902cb081bc659b26fc9a4edda1b6dba513814e5cb1e14e0b1dffd` |
| `agents/AGENT_TASK.md` | full | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `workflows/index.json` | selected descriptor dependency-extract; initial index header | `2bfa2c5faae1081c55ce95fd3d81c00b1d87ba1f51d0bc13e03c8fcb6ccdafb3` |
| `workflows/dependency-extract/WORKFLOW.md` | entry/method read, truncated combined output completed by lines 280–430 | `e5523ebabccf44337ec531280d4d91be2ce7ff1477bd39568a18bb0c4c9f18c3` |
| `workflows/dependency-extract/resources/brief.md` | full | `b51a8166eda6131302c64dcbc893e375c028dd8931f9d49d64b4a0fb8cb49fde` |
| `workflows/dependency-extract/resources/checks.md` | full | `a12aa8b32c955d623623353c39b76f771ad9d6b48a9e513b0e0bad9a706a0457` |
| `workflows/dependency-extract/resources/tools.md` | full | `dbbe7ee79e47dbf673b17e71413c5203f84b2772887dd6406f2ecbac81024db8` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/DEPENDENCY_BRIEF.md` | full | `736418e84c8cba42655c75dfe6020fd32d0fec628718071122f3580cff0ac4ae` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/DEPENDENCY_WORK_ITEMS.csv` | own dispatch row and target path rows; initial full read | `1644b2fd0c7deccf95f37e739c2bbd822ce2492cd5c4ac28df298a9de5b2c538` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/ScopeOfWork.md` | full | `baf68c79b5b8fdf01300fc255d7cf8e433975e6275daadf67b914b4e51eca4a6` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/_REFERENCES.md` | full | `2d29a9c222160cf1cb9488b102cc22c5ed048cb187250963baab8fbeb7c3eff9` |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` | full | `9d44c2ad12f484f3d13901f28d99725ac7fc538dfacc85b832cdbe3c62b8fb81` |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv` | DEL-01-01, DEL-01-05, DEL-05-01 rows | `bcdf6f2f5352e00360c19a956bd22c026909c388d77c76f92b4983ed906415eb` |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Packages.csv` | PKG-01 row | `b8a9b949b629fb8dbe3343e0e5a1f09a30621785d99676f71adb1b285f741fbd` |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Objectives.csv` | OBJ-002, OBJ-004 rows | `e8e5003d9241c4e6a1d74d00a474b76f3780c6d03c93f66dc1b5c5caa7c9c248` |
| `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/ScopeLedger.csv` | SOW-009..012, SOW-132, SOW-133, SOW-149, SOW-150 rows | `363643306d3bbda80f4496943a5d1de5187d7910fabdf5b89f929e6c9605fd73` |
| `tools/validation/validate_dependencies_schema.py` | lines 1–130 inspected; executed | `75cd74768cc8edf91c6f40b582f0fb570d2427894e6c2236ea2fe7d384291f5f` |
| `tools/validation/validate_enum.py` | full inspected; executed | `562934b075b20e7ec366baf60146cf7524acaebad8612b87873c4828dbeeaa70` |
| `tools/validation/validate_id_format.sh` | full inspected; executed | `370c946c301323b1bb273d268f04d4dc4187b865d9d2865b5273f0dd27d0acac` |
