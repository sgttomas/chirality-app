# Specification — DEL-021-03: Insurance Package

**Document Type:** Specification (normative)
**Deliverable ID:** DEL-021-03_Insurance
**Package:** PKG-021 — Bonding, Insurance & Warranty
**Project:** AB-2026-01424 — 2026 Design Build of West Dried Meat Lake Regional Landfill Maintenance Shop Addition
**Owner:** Camrose County
**Revision:** Draft P3 — 2026-02-26
**Status:** SEMANTIC_READY

---

## Scope

### What This Deliverable Covers

DEL-021-03 covers the procurement, documentation, and maintenance of all insurance coverages required by the Contract as a condition of the CCDC 14–2013 Design-Build Stipulated Price Contract between the Proponent (Design-Builder) and Camrose County. This includes:

- Obtaining all required policies from qualified insurers
- Issuing certificates of insurance to the County
- Providing additional insured endorsements on all applicable policies
- Maintaining coverage throughout the project duration
- Furnishing updated evidence of coverage as required

### What This Deliverable Excludes

- Performance Bond and Labour & Material Payment Bond (covered by DEL-021-02)
- Bid Security (covered by DEL-021-01)
- WCB clearance letter at project closeout (produced under DEL-020-03, though WCB coverage itself is initiated here)
- Subcontractor insurance procurement on behalf of subcontractors — **ASSUMPTION: each subcontractor is responsible for their own insurance; the Proponent verifies compliance. Subcontractor flow-down requirements not explicitly stated in RFP §4.2. This ASSUMPTION must be resolved to either an explicit requirement or a confirmed exclusion at contract negotiation (see [F-002]).**

---

## Requirements

### REQ-INS-001: Automobile, Bodily Injury & Property Damage Insurance

**Source:** RFP §4.2.1

The Proponent shall obtain and maintain standard automobile, bodily injury, and property damage insurance providing coverage of not less than **$5,000,000 inclusive** in both the primary policy and the re-insurance policy, in respect of any one claim for injury to or death of any one or more persons, or damage to or destruction of property.

> **Note [A-001]:** RFP §4.2.1 heading refers to "Standard automobile, bodily injury, and property damage insurance." The Decomposition (SOW-0102) summarizes this as "CGL" (Commercial General Liability). The RFP §4.2.1 text does not use the term "CGL." Whether §4.2.1 describes a CGL policy, a standalone automobile policy, or a combined policy is ambiguous. This has material implications for the type of policy procured and its coverage scope. See Guidance Conflict Table CONF-INS-001 for proposed resolution. Human ruling is required.

The policy shall include all of the following sub-coverages:

| Sub-Req | Sub-Coverage | Source |
|---|---|---|
| REQ-INS-001a | Non-owned automobiles | RFP §4.2.1.1 |
| REQ-INS-001b | Independent Subcontractors | RFP §4.2.1.2 |
| REQ-INS-001c | Contractual liability, including this Agreement | RFP §4.2.1.3 |
| REQ-INS-001d | Broad form property damage endorsement | RFP §4.2.1.4 |
| REQ-INS-001e | Environmental liability | RFP §4.2.1.5 |
| REQ-INS-001f | Product and completed operations coverage | RFP §4.2.1.6 |

### REQ-INS-002: Workers' Compensation (WCB)

**Source:** RFP §4.2.2

The Proponent shall maintain Workers' Compensation coverage for all employees engaged by the Proponent, in accordance with the laws of the Province of Alberta. Specific WCB assessment rates and account registration requirements are governed by the Alberta Workers' Compensation Board — exact limits TBD based on Proponent's WCB account and applicable industry classification.

### REQ-INS-003: Professional Liability — Errors & Omissions

**Source:** RFP §4.2.3

The Proponent shall maintain Professional Liability (Errors and Omissions) insurance in the amount of not less than **$5,000,000**. This coverage shall remain in force for the duration of the project.

Note: E&O is explicitly excluded from the additional insured endorsement requirement per §4.2.6.

### REQ-INS-004: Employer's Liability

**Source:** RFP §4.2.4

The Proponent shall maintain Employer's Liability insurance with limits of not less than **$5,000,000 per employee** for each accident, accidental injury, or death of an employee or any Subcontractor engaged by the Proponent.

### REQ-INS-005: Additional Insurance as Directed

**Source:** RFP §4.2.5

The Proponent shall obtain such other insurance as the County may from time to time reasonably require. Specific additional coverages TBD — to be confirmed at contract negotiation or as directed by Camrose County.

### REQ-INS-006: Additional Insured — Camrose County

**Source:** RFP §4.2.6

The Proponent shall cause all insurance coverage (except E&O, if required) to name Camrose County and any other party designated by the County as an **additional insured**. Each applicable policy shall contain a **severability of interests** or **cross-liability clause**.

### REQ-INS-007: Cancellation Notice

**Source:** RFP §4.2.6

The Proponent shall cause all insurance policies to provide that no such insurance policy may be cancelled without the insurer providing **not less than 30 days' written notice** of such cancellation to Camrose County.

### REQ-INS-008: Evidence of Coverage

**Source:** RFP §4.2.6

Upon request of the County, the Proponent shall furnish written documentation, satisfactory to the County, evidencing all required insurance coverage.

### REQ-INS-009: Cost

**Source:** RFP §4.2.6

All costs of insurance required to be held by the Proponent shall be borne entirely by the Proponent.

### REQ-INS-010: Timing — Pre-Construction

**Source:** _CONTEXT.md (Success Criteria); _DEPENDENCIES.md; RFP §4.2 (preamble — condition of Contract)

Insurance documentation must be in place as a condition of the Contract, prior to contract execution and commencement of Work. ASSUMPTION: certificates of insurance and additional insured endorsements must be submitted to the County at or before contract signing.

---

## Open Normative Questions

The following items were identified through semantic lensing as requiring normative resolution. They are presented here to support human decision-making.

### [A-002] Insurer Qualification Requirement

**Status:** ASSUMPTION — not yet a normative requirement

The Datasheet lists insurer qualification (licensed to conduct business in Alberta) as an ASSUMPTION, noting consistency with the surety qualification requirement in §2.12.2 but no explicit insurance-specific clause in RFP §4.2. If insurer licensing is a mandatory requirement, it should be elevated to a normative requirement in this Specification. If it is not mandated by the RFP, the ASSUMPTION label should remain and the item should be noted as a best-practice recommendation in Guidance.

**Proposed action:** Add REQ-INS-011 (Insurer Qualification) if confirmed as a contractual obligation, or note explicitly that it is not RFP-mandated. (Source: RFP §2.12.2 for surety analogue; RFP §4.2 does not contain an explicit insurer qualification clause — location TBD.)

### [F-001] Certificate of Insurance Format

**Status:** ASSUMPTION — not normatively required

Procedure Step 5 and Datasheet both reference "ACORD 25 or equivalent" certificate format as an ASSUMPTION (standard industry practice; format not prescribed in RFP). If the County or contract requires a specific certificate format, this should be added as a normative requirement. If not, the ASSUMPTION status is appropriate and no requirement is needed.

**Proposed action:** Either add REQ-INS-011 or REQ-INS-012 for certificate format if mandated, or explicitly confirm that format is not mandated by the RFP. (Source: Procedure.md Step 5; Datasheet.md Construction section; RFP §4.2.6 requires "written documentation" but does not specify form.)

### [F-002] Subcontractor Insurance Flow-Down

**Status:** ASSUMPTION — not normatively resolved

The Specification Exclusions section, Guidance Considerations, and Datasheet Conditions all state as ASSUMPTION that subcontractors are responsible for their own insurance. RFP §4.2.1.2 requires independent subcontractor sub-coverage under the Proponent's policy, but does not explicitly state whether subcontractors must also carry their own separate policies. This ASSUMPTION must be resolved to either an explicit requirement or a confirmed exclusion.

**Proposed action:** Confirm with County at contract negotiation; review CCDC 14-2013 provisions (GC 11.1 or equivalent) when accessible. Resolve to either a normative requirement (add to Requirements) or a confirmed exclusion (move from ASSUMPTION to explicit exclusion). (Source: RFP §4.2.1.2; CCDC 14-2013 — not accessible.)

---

## Standards

| Standard / Authority | Description | Accessibility |
|---|---|---|
| RFP §4.2 | Primary contractual insurance requirements | Accessible — AB-2026-01424-WDMLRL_RFP.pdf, pages 14–15 |
| CCDC 14–2013 | Design-Build Stipulated Price Contract — governing contract form. **[C-001]: Insurance clauses (GC 11.1 or equivalent) must be obtained and reviewed when the contract is accessible (at DEL-021-04). These clauses may impose additional insurance requirements beyond RFP §4.2.** | Not accessible in source set; referenced in decomposition and RFP §2.7. Clause-level requirements: TBD — location TBD |
| Alberta Workers' Compensation Act | WCB statutory framework | Not accessible in source set — location TBD |
| Insurance Act (Alberta) | Governs insurer licensing and policy requirements in Alberta | Not accessible in source set — location TBD |
| ASSUMPTION: IBC standard forms | Insurers will likely use Insurance Bureau of Canada standard policy forms. Not stated in RFP. | location TBD |

---

## Verification

| Req ID | Requirement Summary | Verification Approach |
|---|---|---|
| REQ-INS-001 | Auto / BI / PD — $5M with sub-coverages | Review certificate of insurance and policy schedule; confirm $5M limit. **Individually verify each of the six sub-coverages** (REQ-INS-001a through 001f) by reviewing policy endorsements or schedule of coverage for each sub-coverage line item, not only the aggregate policy presence. (See [X-003]) |
| REQ-INS-002 | WCB coverage | Review WCB clearance certificate / good standing letter from Alberta WCB |
| REQ-INS-003 | E&O — $5M | Review certificate of insurance and policy declarations |
| REQ-INS-004 | Employer's Liability — $5M/employee | Review policy declarations page |
| REQ-INS-005 | Other insurance as required | Confirm with County that any directed additional coverages have been obtained |
| REQ-INS-006 | County named as additional insured (all except E&O) | Review additional insured endorsements for each applicable policy; confirm County is named |
| REQ-INS-007 | 30-day cancellation notice | Review policy conditions or endorsement confirming 30-day notice to County |
| REQ-INS-008 | Evidence of coverage on demand | Confirm written documentation procedures are in place with insurer/broker |
| REQ-INS-009 | Cost borne by Proponent | Administrative confirmation — not tracked as a document artifact |
| REQ-INS-010 | Pre-contract timing | Confirm certificates and endorsements are submitted to and accepted by County prior to contract execution date |
| TBD | Insurer qualification (if confirmed — see [A-002]) | **[A-003]:** Review insurer's Alberta licensing status and financial strength rating. Verification method TBD pending confirmation of whether this is a contractual obligation. |

---

## Documentation

The following artifacts constitute the deliverable output of DEL-021-03:

| Artifact | Description | Mandatory |
|---|---|---|
| Certificate(s) of Insurance | Formal certificate(s) evidencing all required coverages (one per policy, or consolidated) | Yes |
| Additional Insured Endorsement(s) | Policy endorsements naming Camrose County as additional insured on all applicable policies | Yes |
| Severability / Cross-Liability Endorsement | Endorsement confirming severability of interests or cross-liability clause | Yes |
| WCB Good Standing Certificate | Evidence of active WCB account in good standing in Alberta | Yes |
| Broker Confirmation Letter | ASSUMPTION: Letter from insurer or broker confirming all coverage requirements have been placed as specified | Recommended |
| Insurance Schedule | ASSUMPTION: Summary schedule listing all policies, limits, insurers, policy numbers, and expiry dates | Recommended |
