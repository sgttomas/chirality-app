# Campaign Authority Freeze Record

## Campaign

West Doe Two-Root DBM Remediation and Publication

## Freeze Date

2026-04-18

## Freeze Authority

Human campaign controller, operating with SCOPE_CHANGE persona.

---

## Frozen Source Authority Package

| Artifact | Path | Status |
|----------|------|--------|
| Source anchor PDF | `domain-test/domains/West_Doe_Combined/_Sources/26020-04-PR-PDB-001 R0_IFD Uncontrolled 2026.04.16.pdf` | Present |
| Cleaned package root | `domain-test/domains/West_Doe_Combined/_Sources/west_doe_process_design_basis_clean/` | Present |
| Narrative working authority | `…/west_doe_process_design_basis_clean/Process_DBM_fixed.md` | Present (835 lines) |
| Canonical CSV tables | `…/west_doe_process_design_basis_clean/data/` | 16 CSV files |
| Process block flow diagrams | `…/west_doe_process_design_basis_clean/figures/` | 3 PNG files (300 DPI) |
| Table traceability map | `…/west_doe_process_design_basis_clean/metadata/tables.yaml` | 16 table entries |
| Figure traceability map | `…/west_doe_process_design_basis_clean/metadata/figures.yaml` | 3 figure entries |
| Validation record | `…/west_doe_process_design_basis_clean/validation/validation_report.md` | PASS |
| Validation script | `…/west_doe_process_design_basis_clean/validation/validate_tables.py` | Present |

### Canonical CSV Table Inventory

| # | File | Table ID |
|---|------|----------|
| 1 | `table_00_revision_history.csv` | `table_00_revision_history` |
| 2 | `table_00_client_acceptance.csv` | `table_00_client_acceptance` |
| 3 | `table_02_site_design_parameters.csv` | `table_02_site_design_parameters` |
| 4 | `table_03_02_doe_field_inlet_design_conditions.csv` | `table_03_02_doe_field_inlet_design_conditions` |
| 5 | `table_03_02_doe_field_inlet_composition.csv` | `table_03_02_doe_field_inlet_composition` |
| 6 | `table_03_03_01_produced_water_flows.csv` | `table_03_03_01_produced_water_flows` |
| 7 | `table_03_03_02_condensate_flow_rates.csv` | `table_03_03_02_condensate_flow_rates` |
| 8 | `table_03_03_02_condensate_feed_compositions.csv` | `table_03_03_02_condensate_feed_compositions` |
| 9 | `table_03_04_deep_cut_gas_flow_rates.csv` | `table_03_04_deep_cut_gas_flow_rates` |
| 10 | `table_03_04_deep_cut_gas_compositions.csv` | `table_03_04_deep_cut_gas_compositions` |
| 11 | `table_03_04_feed_stream_design_conditions.csv` | `table_03_04_feed_stream_design_conditions` |
| 12 | `table_03_05_01_sales_gas_specifications.csv` | `table_03_05_01_sales_gas_specifications` |
| 13 | `table_03_05_02_ngl_c3plus_specifications.csv` | `table_03_05_02_ngl_c3plus_specifications` |
| 14 | `table_03_05_03_condensate_c5plus_specifications.csv` | `table_03_05_03_condensate_c5plus_specifications` |
| 15 | `table_03_05_03_capp_butane_equivalent_requirement.csv` | `table_03_05_03_capp_butane_equivalent_requirement` |
| 16 | `table_05_03_product_storage_summary.csv` | `table_05_03_product_storage_summary` |

---

## Active SCA Pointers

| Root | Current SCA | Snapshot | Date | Prior SCA | Description |
|------|------------|----------|------|-----------|-------------|
| Deepcut (`West_Doe_Deepcut_DBM`) | SCA-002 | `SCA-002_2026-04-14_1510/` | 2026-04-14 | SCA-001 (VE workshop closure) | 3-25 interface coordination — incinerator scope boundary, shared F/G and power coordination, LACT excluded (NRM scope) |
| Comp & Liquids (`West_Doe_Comp_and_Liquids_DBM`) | SCA-002 | `SCA-002_2026-04-14_0000/` | 2026-04-14 | SCA-001 | Applied |

**Next amendment in both roots: SCA-003.**

---

## Frozen Decomposition Inventories

### Deepcut (`West_Doe_Deepcut_DBM/_Decomposition/`)

| File | Role |
|------|------|
| `DeepCut_DOMAIN_DECOMP_FINAL_v4.md` | Primary decomposition document |
| `DeepCut_Publication_Manifest_v4.md` | Publication manifest |
| `DeepCut_Domain_Ledger_v4.csv` | Domain Ledger (authoritative unit-level mappings) |
| `DeepCut_Category_Register_v4.csv` | Category register |
| `DeepCut_Knowledge_Type_Register_v4.csv` | Knowledge Type register |
| `DeepCut_Knowledge_Subject_Register_v4.csv` | Knowledge Subject register |
| `DeepCut_Objective_Register_v4.csv` | Objective register |
| `DeepCut_Vocabulary_Map_v4.csv` | Vocabulary map |
| `DeepCut_Open_Issues_v4.csv` | Open issues register |
| `DeepCut_Node_Summary_v4.csv` | Node summary |
| `DeepCut_Scope_Boundary_Register_v4.csv` | Scope boundary register |
| `DeepCut_Standalone_Subject_Coverage_v4.csv` | Subject coverage |
| `DeepCut_Coverage_Telemetry_v4.json` | Coverage and telemetry snapshot |
| `Archive.zip` | Prior version archive |

### Comp & Liquids (`West_Doe_Comp_and_Liquids_DBM/_Decomposition/`)

| File | Role |
|------|------|
| `WEST_DOE_DOMAIN_DECOMPOSITION.md` | Primary decomposition document |
| `_KTY_SCAFFOLD_BRIEF.md` | KTY scaffold brief |
| `README.txt` | Decomposition readme |
| `annex_domain_ledger.csv` | Domain Ledger (authoritative unit-level mappings) |
| `annex_categories.csv` | Category register |
| `annex_knowledge_types.csv` | Knowledge Type register |
| `annex_knowledge_subjects.csv` | Knowledge Subject register |
| `annex_objectives.csv` | Objective register |
| `annex_objective_kty_mapping.csv` | Objective-to-KTY mapping |
| `annex_vocabulary_map.csv` | Vocabulary map |
| `annex_open_issues.csv` | Open issues register |
| `annex_inventory.csv` | Inventory register |
| `annex_decision_log.csv` | Decision log |
| `annex_kty_category_mapping.csv` | KTY-to-Category mapping |
| `annex_unit_category_assignment.csv` | Unit-to-Category assignment |
| `annex_unit_subject_mapping.csv` | Unit-to-Subject mapping |
| `annex_category_telemetry.csv` | Category-level telemetry |
| `annex_coverage_telemetry.csv` | Coverage telemetry |
| `annex_validation_checks.csv` | Validation checks |
| `Archive.zip` | Prior version archive |

---

## Page 18/19 Manual-Review Status

The NGL C3+ specification table (`table_03_05_02_ngl_c3plus_specifications.csv`,
source PDF page 18) and the condensate C5+ specification table
(`table_03_05_03_condensate_c5plus_specifications.csv`, source PDF page 19) were
originally flagged as manual transcriptions requiring human second-person review.

**Status: Reviewed and validated.** The human campaign controller (professional
engineer) manually reviewed PDF pages 18 and 19 on 2026-04-18 and confirmed the
CSV output matches the source exactly. This review is recorded on disk at
`domain-test/domains/West_Doe_Combined/_Sources/west_doe_process_design_basis_clean/validation/validation_report.md`
under "Page 18/19 second-person review". No page 18/19 flagging caveat applies
to allocation matrix rows derived from these tables.

---

## Freeze Statement

The cleaned source authority package at the paths listed above is the governing
source bundle for this campaign. Later edits to any file within the cleaned
source authority package are out of scope unless the campaign is intentionally
restarted by the campaign controller.

The following artifacts are frozen and must not be edited by any root
remediation agent:

- the entire `west_doe_process_design_basis_clean/` package
- the source anchor PDF
- `plans/Authority_Allocation_Matrix.csv` — approved and frozen 2026-04-18
  (26 rows: 6 DEEPCUT_ONLY, 6 COMP_LIQ_ONLY, 14 SHARED_INTERFACE)

Only the campaign controller may amend frozen artifacts, and only if the campaign
is intentionally restarted.

## Execution Note

SHARED_INTERFACE rows in the allocation matrix use root-qualified targeting in
TargetCATs and TargetKTYs columns with the syntax
`West_Doe_Deepcut_DBM:... || West_Doe_Comp_and_Liquids_DBM:...`. Remediation
agent prompts must explicitly instruct agents to parse this encoding rather than
assuming TargetKTYs contains only owning-root IDs.
