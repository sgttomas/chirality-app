# Specification: Design-Build Firm Experience Profile

## Scope

This specification defines the content, structure, and quality requirements for DEL-01-07, the Design-Build Firm Experience Profile. This deliverable fulfills RFP Section 7.1.6 and directly supports OBJ-006 (Demonstrate a strong team and firm experience, 15 points — evaluated as part of "Project Team and Firms (Appendix I)" criterion, RFP Section 8.2, p. 26).

### Inclusions

- Identification of the Design-Builder entity and key consultant firms / subtrades (per RFP 7.1.6 verbatim: "identify firms and subtrades")
- Description of experience on similar projects (per RFP 7.1.6 verbatim: "describe experience on similar projects")
- Project summaries for comparable municipal facilities demonstrating Design-Build delivery capability
- Relevance statements linking past project experience to Penhold PSB scope
- Delivery track record (schedule adherence, within-budget performance) — ASSUMPTION: implied by OBJ-006 scoring context
- Client references with contact information — ASSUMPTION: implied best practice; not explicitly required in RFP 7.1.6

### Exclusions

- Key team member resumes (covered by DEL-01-08; RFP Section 7.1.7)
- Completed Appendix I table (covered by DEL-01-09; Appendix I form)
- Detailed design or technical construction documentation
- Marketing or promotional content beyond factual project summaries
- Pricing information (covered by DEL-01-04 through DEL-01-06)

### Constraints

| Constraint ID | Constraint | Source | Authority |
|---|---|---|---|
| **CN-01** | Must appear within proposal Section 7.1.6, following RFP section order (Sections 6, 7, 8, 9) | RFP 4.3; Constraint C-02 | Mandatory; non-compliance risks disqualification |
| **CN-02** | Must identify firms and subtrades (align with DEL-01-09 Appendix I) | RFP 7.1.6 verbatim | Mandatory content requirement |
| **CN-03** | Must describe experience on similar projects | RFP 7.1.6 verbatim | Mandatory content requirement |
| **CN-04** | Contributes to overall proposal PDF; total proposal must remain under 15 MB | RFP 4.2; Constraint C-01 | Mandatory |
| **CN-05** | All named team members must be consistent with DEL-01-08 | Decomposition; cross-reference | Internal consistency |
| **CN-06** | "Similar projects" interpreted as comparable municipal facilities (fire halls, public works operations, combined services) per decomposition context for this deliverable | Decomposition DEL-01-07 description | Context constraint |

---

## Requirements

### Functional Requirements

| ID | Requirement | Source | Verification |
|---|---|---|---|
| **R-01** | Narrative shall identify the Design-Builder entity: legal name, jurisdiction of incorporation, years in business, service regions. | RFP 7.1.6 ("identify firms"); ASSUMPTION on detail fields | Presence of firm identification block with all named fields populated |
| **R-02** | Narrative shall identify key consultant firms and subtrades associated with this Design-Build team, coordinated with Appendix I (DEL-01-09). | RFP 7.1.6 ("identify firms and subtrades") | Named consultant firms and/or subtrades are present; names are consistent with DEL-01-09 |
| **R-03** | Narrative shall describe the Design-Builder's experience on similar projects, with project summaries covering comparable municipal facilities. | RFP 7.1.6 ("describe experience on similar projects") | Project summaries present; facility types are comparable (fire, public works, combined municipal) |
| **R-04** | Each project summary shall include: project name, location, client name, completion date, contract value (approximate), delivery method, and building size (square feet). | ASSUMPTION: standard qualifications fields; implied by OBJ-006 scoring context. Building size added per Guidance P-003 evidence-based approach (Guidance.md, Principles, P-003: "Include building size (square footage), contract value, delivery date, and team roles for each project.") [Enrichment B-001] | All seven fields populated for each project summary |
| **R-05** | Each project summary shall include an explicit statement of relevance to Penhold PSB (facility type similarity, team capability, scope comparison). | Decomposition: OBJ-006; context for evaluation scoring | Relevance bridge present in each project summary |
| **R-06** | Narrative shall describe the firm's delivery track record (schedule adherence and within-budget performance). | ASSUMPTION: implied by OBJ-006 "demonstrate a strong... firm experience"; scoring matrix favors evidence of project success | Track record statement present (quantitative preferred; qualitative acceptable) |
| **R-07** | Narrative shall provide client references for at least one comparable project, with contact name, title, and contact information. | ASSUMPTION: standard best practice for qualifications evaluation; evaluation committee may contact references. **TBD: Confirm whether R-07 should be promoted from ASSUMPTION to a confirmed requirement based on Owner/proposal team guidance. NR-03 requires all claims to be supported by verifiable references, which implies references should be available. If evaluators expect references, their absence could reduce scoring.** [Enrichment C-001] | Reference entry present with name, title, and contact details |

| **R-08** | Narrative shall be structured to support Excellent-to-Exceptional scoring under the RFP Section 8.3 qualitative bands for the "Project Team and Firms (Appendix I)" criterion. | Guidance C-002 (Guidance.md, Considerations, C-002): Exceptional scoring (100% band) requires that the response "exceeds expectations and demonstrates a clear understanding of the requirements that provides certainty of success and adds a level of innovation" (RFP Section 8.3, p. 27). This scoring expectation was present in Guidance but had no enforceable counterpart in Specification. [Enrichment A-002] | Review narrative against RFP 8.3 scoring band descriptors; confirm evidence of "clear understanding," "certainty of success," and differentiation elements are present |
| **R-09** | Project summaries shall prioritize projects completed within the past 10-15 years. Projects older than 15 years may be included if they are the best available evidence of comparable facility experience, but the recency limitation shall be acknowledged. | ASSUMPTION: Datasheet Attributes states "projects from past 10-15 years are most relevant" (Datasheet.md, Attributes, Project Recency); Procedure Step 2 action 1 filters for "past 10-15 years" (Procedure.md, Step 2). **TBD: Confirm acceptable recency window with Proposal Manager.** [Enrichment B-002] | Review project completion dates; confirm majority fall within 10-15 year window; any older projects have explicit justification |

### Non-Functional Requirements

| ID | Requirement | Source | Verification |
|---|---|---|---|
| **NR-01** | Writing style shall be professional, factual, and persuasive — suitable for evaluation by a municipal committee. | RFP evaluation context; OBJ-006 scoring matrix | Review for clarity, tone, professional presentation |
| **NR-02** | Terminology shall be consistent with the RFP vocabulary map (Decomposition Section 5): "Design-Builder," "Proponent," "Penhold PSB," "CCDC 14-2013," "Owner." | Decomposition Section 5 | Terminology cross-check against vocabulary map |
| **NR-03** | All claims about firm performance must be supported by project examples or verifiable references; unsupported claims shall not be made. | RFP scoring matrix: "Exceptional" requires clear understanding and certainty of success | Fact-check review: (a) each performance claim must be traceable to a named project in the narrative; (b) quantitative claims (schedule %, budget %, building sizes) must cite source records or client-confirmed data; (c) reviewer identity and review date recorded. [Enrichment X-002: verification method strengthened to define pass/fail criteria per Specification.md, Non-Functional Requirements, NR-03] |
| **NR-04** | Content shall be concise and appropriately scoped — sufficient to address the requirement without excessive page consumption. | Constraint C-01 (PDF <15 MB); proposal page management | Review against estimated page allocation |

---

## Standards

### Applicable Standards and References

| Standard | Applicability | Authority | Notes |
|---|---|---|---|
| **RFP Section 7.1.6** | Primary content requirement | RFP p. 18 | Verbatim: "Design Builder to identify firms and subtrades and describe experience on similar projects." Full requirement. |
| **RFP Section 8.2-8.3** | Evaluation criteria and scoring matrix | RFP pp. 25-27 | "Project Team and Firms (Appendix I)" = 15 points; scored Exceptional/Excellent/Very Good/Good/Fair/Acceptable/Unacceptable |
| **RFP Section 4.3** | Proposal content and section order | RFP (Constraint C-02) | Section 7.1.6 content must appear in its correct location within proposal Section 7 |
| **CCDC 14-2013** | Design-Build contract form reference | RFP Appendix J; Decomposition | Relevant for validating Design-Build delivery methodology in comparable projects |
| **RFP Addendum 03 (Jul 31, 2024)** | Scope clarifications for comparable facility requirements | Decomposition Section 4 | Addendum 03 introduced apparatus bay exhaust, sumps, generator, fill stations, solar roof, bunker gear storage — comparable project experience with any of these is differentiating |
| **RFP Section 4.2** | PDF submission constraints | Constraint C-01 | Firm profile contributes to overall 15 MB proposal PDF limit |

---

## Verification

### Completeness Checks

| Check ID | Check | Acceptance Criteria |
|---|---|---|
| **V-01** | RFP 7.1.6 verbatim requirement addressed | Both components present: (a) firms and subtrades identified; (b) experience on similar projects described |
| **V-02** | Firm identification complete | Design-Builder entity name, jurisdiction, years in business, regions present |
| **V-03** | Subtrades / consultant firms identified | Named firms present; consistent with DEL-01-09 Appendix I |
| **V-04** | Project summaries present | At least one comparable municipal facility project described; preferably 3-5 |
| **V-05** | Project fields complete | Name, location, client, date, value, delivery method populated per project |
| **V-06** | Relevance bridges present | Each project summary explicitly links to Penhold PSB scope |
| **V-07** | Track record stated | On-time / within-budget delivery assertion present (with supporting project evidence) |
| **V-08** | Client references present | At least one reference with contact information |
| **V-09** | Cross-document consistency | Team member names match DEL-01-08; subtrade / consultant names match DEL-01-09 |
| **V-10** | Design-Build delivery method confirmed or qualified | Each cited project either (a) used CCDC 14-2013 or equivalent Design-Build contract form, or (b) if non-DB delivery, the project summary explicitly qualifies the delivery method difference and explains the team's relevant contribution. [Enrichment F-001: verification gap; Specification.md Standards lists CCDC 14-2013 as applicable; Guidance.md P-002 states DB delivery is "strongest comparator"] |
| **V-11** | Addendum 03 specialized systems experience highlighted | Where applicable, project summaries explicitly reference experience with Addendum 03 specialized systems (apparatus bay exhaust, sumps, backup generator, fill stations, solar-capable roof, bunker gear storage). Absence of such experience is acceptable but should not go unverified -- reviewer confirms that any available specialized-systems experience has been surfaced. [Enrichment X-003: missing verification slot; Guidance.md C-005; Procedure.md Step 4 action 5] |

### Quality Gates

| Gate | Evidence Required |
|---|---|
| **QG-01: RFP compliance** | Content directly addresses RFP 7.1.6 two-component requirement (identify firms + describe experience) |
| **QG-02: Scoring readiness** | Narrative supports "Excellent" to "Exceptional" scoring level under 15-point "Project Team and Firms (Appendix I)" criterion (exceeds basic expectations; provides certainty of success; demonstrates clear understanding) [Enrichment E-001: label normalized to official RFP criterion name] |
| **QG-03: Professional presentation** | Narrative free of grammar/spelling errors; terminology consistent; formatting appropriate for municipal evaluation |
| **QG-04: Cross-document alignment** | All names, roles, and company identifications consistent across DEL-01-07, DEL-01-08, DEL-01-09 |

---

## Documentation

### Required Artifacts

| Artifact | Format | Responsibility |
|---|---|---|
| Firm Experience Profile narrative | Prose + project summary tables/blocks; embedded in proposal Section 7.1.6 | Proposal Manager |
| Firm identification block | Text or table within narrative | Proposal Manager |
| Project summary entries (3-5 recommended) | Structured blocks within narrative | Proposal Manager / Estimator |
| Client reference list | Table or structured block with contact details | Proposal Manager |
| Delivery track record statement | Narrative paragraph or summary table | Proposal Manager / Estimator |

### Output Deliverable

| Item | Description |
|---|---|
| **Primary Output** | Section 7.1.6 content in final proposal PDF (within overall proposal assembled per DEL-01-02) |
| **Working Document** | Draft narrative (Word or Markdown) for review, revision, and version control before PDF finalization |
| **Supporting Evidence** | Project files, client reference confirmations, team availability records (stored in project records; not embedded in proposal) |

---

## Notes

### Confirmed Facts (from RFP source review)

- RFP Section 7.1.6 full text confirmed (p. 18): "Design Builder to identify firms and subtrades and describe experience on similar projects." This is the complete requirement — no minimum project count, no page limit, no specific format is prescribed.
- The 15-point "Project Team and Firms (Appendix I)" criterion (RFP Section 8.2, p. 26) covers both the firm profile (this deliverable) AND Appendix I (DEL-01-09) AND key resumes (DEL-01-08) collectively.
- Scoring is on the Exceptional/Excellent/Very Good/Good/Fair/Acceptable/Unacceptable matrix (RFP Section 8.3, p. 27); scoring is based on extent to which requirements are met and confidence in project success.
- R-04 now includes building size (sq ft) as a required project summary field, based on Guidance P-003 evidence. [Enrichment B-001]
- V-10 and V-11 added to close verification gaps for DB delivery method confirmation and Addendum 03 specialized systems experience. [Enrichments F-001, X-003]
- NR-03 verification method strengthened to define specific pass/fail criteria for fact-check review. [Enrichment X-002]

### ASSUMPTION Labels

- **ASSUMPTION (R-04):** Standard qualifications fields (project name, location, client, date, value, delivery method) are implied best practice; RFP 7.1.6 does not specify these fields explicitly.
- **ASSUMPTION (R-06):** Delivery track record (schedule/budget adherence) is implied by OBJ-006 objective language; RFP 7.1.6 does not explicitly require it.
- **ASSUMPTION (R-07):** Client references are standard practice for qualifications submissions; RFP 7.1.6 does not explicitly require them.
- **ASSUMPTION (R-08):** Scoring-level targeting (Excellent-to-Exceptional) is derived from Guidance C-002 interpretation of RFP Section 8.3 scoring bands; RFP 7.1.6 does not explicitly mandate a scoring target. [Enrichment A-002]
- **ASSUMPTION (R-09):** 10-15 year project recency window is inferred from Datasheet and Procedure language; RFP 7.1.6 does not specify a recency constraint. TBD for human confirmation. [Enrichment B-002]
- **ASSUMPTION (CN-06):** "Similar projects" = comparable municipal facilities (fire halls, public works, combined services) per decomposition context; RFP 7.1.6 does not define "similar."
