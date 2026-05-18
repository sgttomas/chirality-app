# Datasheet — DEL-021-05: Guarantee Period Obligations

**Document Type:** Datasheet (descriptive)
**Deliverable ID:** DEL-021-05_Warranty
**Package:** PKG-021 — Bonding, Insurance & Warranty
**Project:** AB-2026-01424-WDMLRL-2026-Claude
**Prepared by:** 4_DOCUMENTS agent (Pass 1+2; Pass 3 enrichment applied)
**Date:** 2026-02-26

---

## Terminology Note

The RFP uses the term "guarantee period" (RFP §2.10) while common industry usage and several sections of these production documents use "warranty period." These terms are synonymous in the context of this deliverable. The authoritative term from the RFP is "guarantee period"; "warranty period" is used interchangeably throughout these documents for readability. Where precision is required for audit or contractual purposes, prefer "guarantee period" as the governing term. (Source: RFP §2.10 heading; Semantic Lensing item E-002)

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-021-05_Warranty |
| Deliverable Title | Guarantee Period Obligations |
| Package | PKG-021 — Bonding, Insurance & Warranty |
| Project | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| Owner | Camrose County |
| Responsible Party | Project Manager |
| Deliverable Type | Warranty / Post-Construction Administration |
| Decomposition Reference | WDMLRL_Decomposition_Claude.md §7 PKG-021 |
| SOW Items Covered | SOW-0120, SOW-0121 |
| Objective Supported | OBJ-008 |

**OBJ-008 (source: Decomposition §5):** "Satisfy all bonding, insurance, and warranty obligations through the 2-year guarantee period post-CCC. This includes timely provision of bonds and insurance pre-construction, and defect rectification within 10 days of Owner instruction during the guarantee period."

---

## Attributes

| Attribute | Value | Source |
|---|---|---|
| Guarantee Period Duration | Construction period + 2 years following CCC date | RFP §2.10.2 |
| Post-CCC Guarantee Period | 2 years | RFP §2.10.2; Decomposition Vocabulary Map (note: also referred to as "warranty period" — see Terminology Note) |
| Defect Rectification Timeline | Within 10 days of Owner's written instruction | RFP §2.10.6; SOW-0121 |
| Guarantee Scope | All materials furnished and Work performed during construction and warranty period | RFP §2.10.2; SOW-0120 |
| Emergency Work Authorization | Owner may perform emergency work immediately and notify Contractor | RFP §2.10.5 |
| Cost of Guarantee Work | Borne entirely by the successful Proponent (Contractor) | RFP §2.10.7 |
| Liability for Damages | Contractor liable to Owner for all expenses, losses, or damages from faulty materials or workmanship | RFP §2.10.8 |
| Deficiency Holdback | Owner may retain amount equal to estimated value of outstanding deficiencies | RFP §2.11.1 |
| Deficiency Holdback Valuation Method | TBD — RFP §2.11.1 states "amount equal to the estimated value" but does not prescribe the estimation methodology (see Specification REQ-021-05-04 and Guidance OI-006) | RFP §2.11.1; Semantic Lensing item D-001 |
| Holdback Release | Upon correction and approval of all deficiencies/defects | RFP §2.11.2 |
| Holdback Withdrawal (Owner) | Owner may withdraw from holdback if Contractor fails to correct deficiencies | RFP §2.11.3 |
| Period Start Trigger | Substantial completion / Construction Completion Certificate (CCC) date | RFP §2.10.2; _DEPENDENCIES.md |
| Responsible Party | Project Manager | _CONTEXT.md |
| Final Inspection Timing | ASSUMPTION: Near end of 2-year guarantee period (per MEMORY.md) | MEMORY.md |
| Warranty Period Start Date | TBD (upon CCC issuance) | _STATUS.md; MEMORY.md |
| Warranty Period End Date | TBD (CCC date + 2 years) | RFP §2.10.2 |

---

## Conditions

### Triggering Conditions

| Condition | Description | Source |
|---|---|---|
| Period Start | Substantial completion; CCC issued by Owner after final inspection | RFP §2.14.3; _DEPENDENCIES.md |
| Defect Notification | Owner observes or discovers deficiency through use, tests, or inspection | RFP §2.10.4 |
| Emergency Condition | Work must be done immediately to prevent serious damage, injury, or loss of life | RFP §2.10.5 |
| Period End | TBD — 2 years post-CCC; specific expiration trigger (calendar expiry alone, final inspection, or Owner written release) TBD. The normative end-trigger must be established in Specification (see REQ-021-05-01 and Guidance OI-005). | RFP §2.10.2; Semantic Lensing item A-001 |

### Performance Conditions

| Condition | Consequence | Source |
|---|---|---|
| Contractor fails to rectify within 10 days | Owner may take whatever action necessary; costs borne by Contractor | RFP §2.10.6, §2.10.7 |
| Contractor fails to correct during guarantee period | Owner may withdraw from Deficiency Holdback | RFP §2.11.3 |
| Contractor corrects all deficiencies | Owner pays all remaining Deficiency Holdback funds to Contractor | RFP §2.11.4 |
| Faulty materials or workmanship | Must be replaced/rectified and approved by Owner; may include replacement of all or portion of Work | RFP §2.10.3 |

### Upstream Dependency Conditions

| Upstream | Condition on DEL-021-05 | Source |
|---|---|---|
| DEL-021-02 (Performance Bonds) | Performance bond must remain in effect during warranty period | _DEPENDENCIES.md |
| DEL-021-03 (Insurance) | Contractor insurance should remain in effect during warranty | _DEPENDENCIES.md |
| DEL-021-04 (Contract Execution) | Contract terms (CCDC 14-2013) establish warranty obligations | _DEPENDENCIES.md |
| PKG-020 (Commissioning & Closeout) | Substantial completion triggers warranty period start | _DEPENDENCIES.md |

---

## Construction

### Deliverable Artifacts (Anticipated)

| Artifact | Description | Key Fields / Content | Status |
|---|---|---|---|
| Warranty Period Register | Document establishing CCC date, warranty start, and expiry date | CCC date, expiry date, PM contact, Contractor contact | TBD |
| Deficiency Log | Ongoing log tracking identified defects, notifications, and rectification status | Deficiency ID, date identified, description, severity, notification date, deadline, completion date, approval date | TBD |
| Defect Notification Records | Owner's written instructions to Contractor for each deficiency | Deficiency ID, location, description, 10-day deadline, RFP reference | TBD |
| Remediation Completion Records | Documentation confirming each deficiency has been rectified and approved by Owner | Deficiency ID, remediation description, completion date, Owner approval date | TBD |
| Post-Completion Inspection Report(s) | Reports from inspections during the warranty period | Inspection date, scope, findings, deficiency IDs raised | TBD |
| Warranty Expiration Checklist | Final checklist for managing end of warranty period | All deficiencies resolved, holdback reconciled, documentation complete | TBD |
| Deficiency Holdback Ledger | Record of holdback amounts retained and released | Deficiency ID, description, estimated holdback value, date identified, date Owner written instruction issued, target rectification date (instruction date + 10 days), date remediation completed, date Owner approved, amount released | TBD |

**Note (Semantic Lensing item E-001):** The Deficiency Holdback Ledger field list above has been normalized to align with the operational field definitions in Procedure Step 1.4. The fields "Date Owner written instruction issued" and "Target rectification date" are included to support cross-reference between notification dates and compliance deadlines (Semantic Lensing item E-001). This ensures traceability between the descriptive (Datasheet) and operational (Procedure) views of the ledger artifact.

### Defect Classification

ASSUMPTION: Defects may be classified as minor, major, or critical for prioritization purposes; specific classification criteria are not defined in the RFP and are TBD. (Source: MEMORY.md Q2; RFP §2.10 does not prescribe classification levels.) See Specification for normative treatment of defect classification (Semantic Lensing item A-002) and Guidance OI-001.

### Remediation Timeline

| Defect Type | Required Timeline | Source |
|---|---|---|
| Standard guarantee work | Within 10 days of Owner's written instruction | RFP §2.10.6 |
| Emergency work | Immediately (Owner may act without waiting for Contractor) | RFP §2.10.5 |
| Non-emergency, Contractor-failed | Owner takes action after 10-day period expires; cost to Contractor | RFP §2.10.6, §2.10.7 |

---

## References

| Ref ID | Document | Sections Used |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §2.10 (Guarantee Period), §2.11 (Deficiency Holdback), §2.12 (Surety Bonding), §2.14 (Completion and Acceptance), §4.2 (Insurance) |
| — | WDMLRL_Decomposition_Claude.md | §2 Vocabulary Map, §5 Objectives (OBJ-008), §7 PKG-021 Deliverables, §8 Scope Ledger (SOW-0120, SOW-0121) |
| — | DEL-021-05 _CONTEXT.md | Deliverable overview, scope, roles, success criteria |
| — | DEL-021-05 _DEPENDENCIES.md | Upstream dependencies |
| — | DEL-021-05 _REFERENCES.md | Reference list |
| — | DEL-021-05 MEMORY.md | Key notes, open questions |
| — | DEL-021-05 _SEMANTIC_LENSING.md | Pass 3 enrichment register (items A-001, D-001, E-001, E-002 applied to this document) |
