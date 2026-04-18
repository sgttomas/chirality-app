# DBM Publication Workflow File Manifest

## Status

Companion file manifest for the DBM publication workflow.

## Purpose

This file lists the project materials that matter for implementing the full
DBM publication workflow described in
`plans/DBM_PUBLICATION_WORKFLOW_PLAN.md`, grouped by how completely they should
be used.

Rules:

- paths ending in `/` mean provide the full directory contents
- "sampled/excerpt" means a partial file handoff is acceptable
- "optional but helpful" means not strictly required for implementation, but
  useful for precedent or richer validation context

## 1. Must Provide In Full

```text
INIT.md
AGENTS.md
plans/DBM_PUBLICATION_WORKFLOW_PLAN.md

CHIRALITY_FRAMEWORK.md
PROFESSIONAL_ENGINEERING.md
docs/SPEC.md
docs/TYPES.md
docs/CONTRACT.md
docs/DBM_Agent_Instruction_Architecture.md

agents/AGENT_HELPS_HUMANS.md
agents/AGENT_SKILLMAKER.md
agents/AGENT_TOOLMAKER.md
agents/AGENT_TASK.md
agents/AGENT_ORCHESTRATOR.md
agents/AGENT_HELP_HUMAN.md
agents/AGENT_DECOMP_BASE.md
agents/AGENT_DOMAIN_DECOMP.md
agents/AGENT_SCOPE_CHANGE.md

skills/README.md
skills/SKILL_TEMPLATE.md
skills/domain-documents/SKILL.md
skills/domain-documents/BRIEF_SCHEMA.md
skills/domain-documents/TOOL_POLICY.md
skills/domain-documents/QA_CHECKS.md

tools/REGISTRY.md
tools/validation/validate_skill_metadata.py

domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Domain_Ledger_v4.csv
domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Category_Register_v4.csv
domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Knowledge_Type_Register_v4.csv
domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Knowledge_Subject_Register_v4.csv
domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Objective_Register_v4.csv
domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Scope_Boundary_Register_v4.csv
domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Vocabulary_Map_v4.csv
domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Open_Issues_v4.csv
domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Node_Summary_v4.csv
domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Coverage_Telemetry_v4.json
domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_Publication_Manifest_v4.md
domain-test/domains/West_Doe_Deepcut_DBM/_Sources/TOC_Deepcut.md
domain-test/domains/West_Doe_Deepcut_DBM/_ScopeChange/_LATEST.md
domain-test/domains/West_Doe_Deepcut_DBM/_ScopeChange/SCA-002_2026-04-14_1510/
domain-test/domains/West_Doe_Deepcut_DBM/_ScopeChange/SCA-001_2026-04-14_1430/

domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/WEST_DOE_DOMAIN_DECOMPOSITION.md
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_domain_ledger.csv
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_categories.csv
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_knowledge_types.csv
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_knowledge_subjects.csv
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_objectives.csv
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_vocabulary_map.csv
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_open_issues.csv
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_decision_log.csv
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_validation_checks.csv
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/annex_inventory.csv
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/README.txt
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Decomposition/_KTY_SCAFFOLD_BRIEF.md
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Sources/TOC_Compression_Liquids.md
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_ScopeChange/_LATEST.md
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_ScopeChange/SCA-002_2026-04-14_0000/
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_ScopeChange/SCA-001_2026-04-14_0000/

domain-test/domains/West_Doe_Deepcut_DBM/CAT-001_Introduction/1_Working/KTY-01-04_Basic-Scope-of-Work/
domain-test/domains/West_Doe_Deepcut_DBM/CAT-004_Deep-Cut-Process/1_Working/KTY-04-09_Amine-Treating/
domain-test/domains/West_Doe_Deepcut_DBM/CAT-007_Plant-Design-Requirements/1_Working/KTY-07-03_Isolation-Philosophy/
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/CAT-004_Process Description/1_Working/KTY-04-09_Condensate-Mercaptan-Treating/
```

## 2. Provide As Sampled/Excerpt

```text
domain-test/domains/West_Doe_Deepcut_DBM/_Decomposition/DeepCut_DOMAIN_DECOMP_FINAL_v4.md
  Recommended: first 300-500 lines, plus TOC/headings if available

domain-test/domains/West_Doe_Deepcut_DBM/_Sources/W235633-PRC-DBM-000001-001_(4-25_Doe)_DBM.md
  Recommended: first 150-200 lines

domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_Sources/W242510-PRC-DBM-000001-001_(3-25_Doe)_DBM.md
  Recommended: first 150-200 lines
```

## 3. Optional But Helpful

```text
docs/DIRECTIVE.md
docs/SE_Design_Analysis.md

skills/four-documents/SKILL.md
skills/content-digest/SKILL.md

tools/aggregation/build_hypergraph.py
tools/pdf2md/assemble_markdown.py

domain-test/domains/West_Doe_Deepcut_DBM/CAT-004_Deep-Cut-Process/1_Working/KTY-04-01_Inlet-Pipeline/
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/CAT-001_Introduction/1_Working/KTY-01-04_Basic-Scope-of-Work/

domain-test/domains/West_Doe_Deepcut_DBM/_ScopeChange/SCA-001/
domain-test/domains/West_Doe_Comp_and_Liquids_DBM/_ScopeChange/SCA-001/
```

## Notes

- This manifest is scoped to full workflow implementation, not just authoring
  the new agent instruction files.
- The two West Doe domain bundles are included as implementation fixtures so
  the workflow can be built against both decomposition naming conventions and
  real scope-change structures.
- The very large Deepcut narrative decomposition and source DBM are kept in the
  excerpt tier because the structured registers matter more than the full
  narrative for workflow implementation.
