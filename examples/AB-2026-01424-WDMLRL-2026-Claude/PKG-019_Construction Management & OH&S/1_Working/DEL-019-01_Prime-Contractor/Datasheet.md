# Datasheet — DEL-019-01: Prime Contractor Designation & OH&S Program

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-019-01_Prime-Contractor |
| **Title** | Prime Contractor Designation & OH&S Program |
| **Package** | PKG-019 — Construction Management & OH&S |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Project ID** | AB-2026-01424-WDMLRL-2026-Claude |
| **Owner** | Camrose County |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price Contract |
| **Type** | Management |
| **Category** | Management |
| **Responsible Party** | Project Manager / Safety Officer |
| **Covers SOW** | SOW-0083 |
| **Supports Objective** | OBJ-007 |
| **Status** | SEMANTIC_READY |
| **Created** | 2026-02-25 |
| **Expected Start** | 2026-03-01 |
| **Target Completion** | TBD (project duration; completion no later than December 31, 2026) |

Source: `_CONTEXT.md`; Decomposition §7 PKG-019 table; RFP §3.1 (completion deadline).

> **Enrichment note [B-002]:** Status field normalized from "OPEN" to "SEMANTIC_READY" to align with `_STATUS.md` (authoritative for lifecycle state). Per `_STATUS.md` history: state progressed OPEN -> INITIALIZED -> SEMANTIC_READY.

---

## Attributes

| Attribute | Value | Source |
|---|---|---|
| **Prime Contractor designation trigger** | Upon award of contract | RFP §2.15 |
| **Designation duration** | Full project duration; whenever Proponent's personnel, equipment, or subcontractors are on site | RFP §2.15 |
| **Designation instrument** | Prime Contractor Designation Form issued by Camrose County | RFP §2.15 |
| **Regulatory framework** | Alberta Occupational Health and Safety Act and associated regulations | Decomposition Vocabulary Map; RFP §2.15 (ref. "Health and Safety agencies") |
| **OH&S performance target** | Zero lost-time incidents for full project duration | Decomposition OBJ-007 |
| **Health & Safety Pre-Qualification** | Contractor Health and Safety Pre-Qualification Evaluation form (Appendix A) required at proposal stage | RFP §4.9; Appendix A |
| **Certificate of Recognition** | COR, SECOR, or TLC preferred (supporting documentation item) | Appendix A — H&S Pre-Qual |
| **WCB Clearance Letter** | Required; must be issued within 30 days of submission | Appendix A — H&S Pre-Qual |
| **WCB Premium Rate Statement** | Current statement required | Appendix A — H&S Pre-Qual |
| **Emergency Response Plan** | Required prior to commencing work | Appendix A — H&S Pre-Qual |
| **Health, Safety and Environmental Manual** | Required prior to commencing work | Appendix A — H&S Pre-Qual |
| **Insurance — General Liability** | Minimum $5,000,000 Commercial General Liability (preferred); Camrose County listed as additional insured | Appendix A — H&S Pre-Qual; RFP §4.2.1 |
| **Insurance — Automobile** | Coverage for owned and hired motor vehicles | Appendix A — H&S Pre-Qual; RFP §4.2.1 |
| **Insurance — Professional Liability** | $5,000,000 Errors & Omissions | RFP §4.2.3 |
| **Insurance — WCB** | Workers' Compensation coverage per Alberta law | RFP §4.2.2 |
| **Safety evaluation weight** | 10% of proposal scoring (Health and Safety Program criterion) | RFP §5.1.2, Item C |
| **Subcontractor safety management** | Must be included in OH&S program | RFP §5.1.2, Item C |
| **Hazard Assessments** | Required; appropriate for the project | Appendix A — H&S Pre-Qual |
| **Safe Work Procedures** | Required; appropriate for the project | Appendix A — H&S Pre-Qual |
| **Safety/Training Certificates** | May be required on request (First Aid, WHMIS, trades, etc.) | Appendix A — H&S Pre-Qual |
| **OHS fatalities (last 3 years)** | Must be declared; action plan required if yes | Appendix A — H&S Pre-Qual |
| **OHS orders (last 3 years)** | Must be declared; action plan required if yes | Appendix A — H&S Pre-Qual |
| **Alberta Environmental Orders (last 3 years)** | Must be declared; action plan required if yes | Appendix A — H&S Pre-Qual |
| **Site-specific hazard: waste gas exposure** | TBD — requires site-specific hazard assessment for active landfill environment | ASSUMPTION (landfill site context; Guidance §Considerations — Landfill site context) |
| **Site-specific hazard: heavy equipment interaction** | TBD — requires assessment of interaction between construction activities and ongoing landfill operations | ASSUMPTION (landfill site context; Guidance §Considerations — Landfill site context) |
| **Site-specific hazard: access/egress controls** | TBD — requires assessment of site access and egress routes relative to landfill operations | ASSUMPTION (landfill site context; Guidance §Considerations — Landfill site context) |

> **Enrichment note [B-001]:** Landfill-site-specific hazard category attributes added to capture data points identified as ASSUMPTIONs in Guidance §Considerations (Landfill site context). Values are TBD pending site-specific hazard assessment by the Safety Officer.

---

## Conditions

| Condition | Details | Source |
|---|---|---|
| **Site** | SW 14–44–21–W4, near Ferintosh, Alberta (West Dried Meat Lake Regional Landfill) | RFP §1.0, §3.2 |
| **Governing law** | Province of Alberta | RFP §2.22 |
| **Pre-qualification screening** | Proposals screened for reasonable qualifications to assume Prime Contractor status before evaluation | RFP §5.1.1 |
| **Downstream deliverable dependency** | DEL-019-02 (Weekly Coordination), DEL-019-03 (Subcontractor Mgmt), DEL-019-04 (QC Management) all depend on this designation being in effect | `_DEPENDENCIES.md` |
| **Project completion deadline** | All Work must be complete on or before December 31, 2026 | RFP §3.1 |
| **County contact for Prime Contractor Designation** | Darren King, Manager West Dried Meat Lake Regional Landfill; dking@county.camrose.ab.ca; (780) 679-6519 | RFP §1.3.4 |

> **Enrichment note [E-002]:** County contact for the Prime Contractor Designation Form added to Conditions for cross-reference consistency. This contact was previously recorded only in Procedure Step 2.1 (single-point-of-reference risk). Source: RFP §1.3.4.

---

## Construction

> **Note:** This deliverable is a management/governance artifact, not a physical construction item. "Construction" in this context describes the composition of the deliverable package itself.

| Component | Description | Source |
|---|---|---|
| **Prime Contractor Designation Form** | Completed form issued by Camrose County; signed by Proponent representative | RFP §2.15 |
| **OH&S Program Document** | Written occupational health and safety program covering site operations, subcontractor management, hazard management, emergency response, and reporting | ASSUMPTION (standard Alberta Prime Contractor obligation; specific program structure not detailed in RFP beyond pre-qual requirements) |
| **Health and Safety Pre-Qualification Evaluation** | Completed Appendix A form with all supporting documentation | Appendix A; RFP §4.9 |
| **Hazard Assessments** | Site- and task-specific hazard assessments appropriate to the project | Appendix A — H&S Pre-Qual |
| **Safe Work Procedures** | Written procedures for project activities | Appendix A — H&S Pre-Qual |
| **Emergency Response Plan** | Project-specific ERP required prior to commencing work | Appendix A — H&S Pre-Qual |
| **Health, Safety and Environmental Manual** | Company HSE manual | Appendix A — H&S Pre-Qual |
| **WCB Clearance Letter** | Current (within 30 days) letter from Workers' Compensation Board | Appendix A — H&S Pre-Qual |
| **Insurance Certificates** | Evidence of all required insurance coverages per RFP §4.2 | RFP §4.2 |

---

## References

| Ref ID | Document | Relevant Section |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §2.15 (Prime Contractor); §4.2 (Insurance); §4.9 (Proposal Response Forms); §5.1.1–5.1.2 (Evaluation, H&S screening) |
| R-03 | AB-2026-01424-Appendix A.pdf | Contractor Health and Safety Pre-Qualification Evaluation form |
| — | WDMLRL_Decomposition_Claude.md | §2 (Vocabulary: Prime Contractor definition); §5 (OBJ-007); §6 (PKG-019 description); §7 (DEL-019-01 entry); §3L (SOW-0083) |
| — | `_CONTEXT.md` | Deliverable identification, scope, roles |
| — | `_DEPENDENCIES.md` | Downstream dependencies |
