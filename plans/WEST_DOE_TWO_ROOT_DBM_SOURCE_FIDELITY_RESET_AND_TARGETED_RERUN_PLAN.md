# West Doe Two-Root DBM Source-Fidelity Reset and Targeted Rerun Plan

**Date:** 2026-04-20
**Author:** Campaign Controller (SCOPE_CHANGE persona)
**Status:** Active

---

## 1. Purpose

The first publication run for both roots (C&L RUN-20260420-022314, Deepcut RUN-20260419-220000) passed all 7 gates but failed external source-fidelity review against the cleaned Process DBM authority package. This plan defines the remediation path: a Gate 1-4 authority reset followed by targeted Gate 5 section reruns and a full Gate 6 package rebuild.

The publication architecture is sound. The authority model was wrong.

---

## 2. Prior Run Disposition

Both publication runs are **superseded**. They are retained as historical artifacts but are not accepted publication truth and must not be sent to CHANGE.

| Root | Run ID | Disposition |
|---|---|---|
| Comp & Liquids (03-25) | RUN-20260420-022314 | SUPERSEDED — Gate 1 authority error |
| Deepcut (04-25) | RUN-20260419-220000 | SUPERSEDED — Gate 1 authority error |

---

## 3. Root Cause

The Gate 1 authority model allowed KTY-local content (tier 3) and SCA/VE decisions (tier 1-2) to silently override the cleaned source authority (tier 4) without flagging the conflict. Section workers then synthesized prose that blended multiple authority sources without surfacing which source governed each statement.

This produced two categories of failure:
1. **Facility-scope attribution errors** — systems from the sister facility or retired scope appeared as active design basis (e.g., TEG dehydration at 03-25, depropanizer at 04-25, retired equipment as active scope)
2. **Silent authority overrides** — SCA/VE/discipline content superseded Process DBM values without concordance coverage (e.g., MPFF 2×100% vs source 1, sales gas booster 100 vs source 140 MMSCFD, phosphorous <1.5 vs source <1.0 wppm)

---

## 4. Retained Decisions

The following campaign decisions are preserved. They were validated during Phases 1-7 and remain correct:

| Decision | Status | Basis |
|---|---|---|
| One DBM per facility (03-25 and 04-25) | RETAINED | Intentional publication design |
| Sister facility appears only as interface | RETAINED | Evaluator confirmed |
| Section architecture (17 sections C&L, 22 sections Deepcut) | RETAINED unless a section proves unsupportable during rerun |
| Terminology normalizations (NGL, NRM NEBC Connector, Cross-Facility, Sieve) | RETAINED | SCA-003, Phase 7 conformity |
| Cross-root conformity outcomes (14/14 SHARED_INTERFACE PASS) | RETAINED | Phase 7 gate report |
| Concordance machinery (tooling, register structure, checker logic) | RETAINED | Tooling is correct; register content needs revision |
| Confirmed controller rulings that remain source-consistent | RETAINED | 5,200 hp, incinerator framing, LACT routing, buyback gas |
| SCA-001 through SCA-004 amendments | RETAINED as upstream truth | These are valid scope changes, not publication errors |

---

## 5. Revised Authority Model

The revised model makes the Process DBM primary authority for all facility-specific process facts, with explicit admission gates for anything that supersedes it.

### 5.1 Authority Precedence (revised)

| Tier | Source | Role | Override Rule |
|---|---|---|---|
| 1 | Process DBM (cleaned source package) | **Primary authority** for facility-specific process facts, equipment counts, specifications, and cross-facility interfaces | Governs unless explicitly overridden by an admitted superseding source |
| 2 | Accepted SCA state (SCA-001 through SCA-004) | Admitted superseding authority for scope changes | Must be explicitly flagged where it overrides the Process DBM. The override must be recorded in concordance assertions. |
| 3 | Approved decomposition state | Structural authority (categories, KTYs, subjects, coverage) | Governs section structure and content mapping. Does NOT override Process DBM process facts. |
| 4 | KTY-local content (Scoping.md, KA-*.md) | Supplementary detail | May extend the Process DBM but must NOT silently contradict it. Contradictions must be surfaced as concordance items. |
| 5 | Discipline/VE/procurement sources | Supplementary if admitted | Must be explicitly admitted per section. Must NOT override Process DBM process facts without a recorded supersession. |
| 6 | Root-local source DBMs | Provenance/history only | Not authority for any current-state fact. |

### 5.2 Key change from the prior model

The prior model placed SCA state at tier 1 and the cleaned source at tier 4-5, allowing KTY-local content to silently override the source. The revised model makes the cleaned source primary and requires every override to be explicitly admitted and concordance-tracked.

### 5.3 Facility-scope discipline

Each root's publication rules must include a **FacilityScopeRule** defining:
- Systems that ARE at this facility (from the Process DBM facility-specific scope list)
- Systems that are NOT at this facility (belong to the sister facility)
- Systems that are SHARED (cross-facility interface)
- Systems that are RETIRED (per SCA amendments)

Section workers must not synthesize content for systems outside their facility's scope. If KTY-local content describes a system belonging to the sister facility, the section worker must emit a concordance conflict, not include the content.

---

## 6. Review-Item Classification

Both agents must classify every item from the external review feedback into one of four buckets:

| Bucket | Meaning | Action |
|---|---|---|
| `CONFIRMED_PUBLICATION_ERROR` | The published statement contradicts the Process DBM and no admitted override exists | Correct in the rerun |
| `VALID_SCA_OR_ADMITTED_OVERRIDE` | The published statement reflects an SCA/VE decision that legitimately supersedes the Process DBM | Retain, but add explicit concordance assertion flagging the override |
| `VALID_SUPPLEMENTARY_EXTENSION` | The published statement extends beyond the Process DBM using admitted KTY-local/discipline content without contradicting it | Retain |
| `STILL_UNRESOLVED` | The correct value cannot be determined from available sources | Preserve as TBD with explicit authority-gap note |

The classification must be documented before targeted section reruns begin. It becomes the repair specification.

---

## 7. Rerun Protocol

### 7.1 Gate 1-4 Reset (both roots)

**Gate 1 — Authority refreeze:**
- Re-read the cleaned source authority (`Process_DBM_fixed.md` + canonical CSVs)
- Produce a facility-specific scope summary: systems at this facility, systems at the sister facility, shared systems, retired systems
- Refreeze the manifest with the revised authority model (§5.1)

**Gate 2 — Landscape review:**
- Review against the revised authority model
- Identify any KTY-local content that contradicts the Process DBM

**Gate 3 — Schema/rules revision:**
- Add `FacilityScopeRule` to publication rules (§5.3)
- Add source-authority concordance rule: section workers must flag any statement that contradicts the Process DBM, not silently resolve via precedence
- Retain section architecture unless a section proves unsupportable

**Gate 4 — Concordance register revision:**
- Add the evaluator's concordance-critical assertions (see §8 below)
- Add facility-scope assertions for every major system
- Retain existing cross-section value assertions where still valid
- Remove assertions for systems that were incorrectly attributed to this facility

### 7.2 Gate 5 — Targeted Section Reruns

**Not a wholesale regeneration.** Only the sections identified by the external review need reruns. The rest are retained from the prior run after concordance validation confirms they remain source-consistent.

### 7.3 Gate 6 — Full Package Rebuild

- Full `assemble_publication.py` run
- Full `check_concordance.py` run
- Source-concordance validation: prohibited-residue search for each root (see §9)
- Package completeness and readiness classification

### 7.4 Gate 7 — Human acceptance

- Prose sampling of high-risk sections
- Final acceptance decision

---

## 8. Root-Specific Rerun Specifications

### 8.1 Comp & Liquids (03-25)

**Mandatory section reruns:**

| Section | Reason |
|---|---|
| SEC-03 (Feeds, Products, Wastes) | Remove 4 lb/MMSCF dehydration, DSO waste stream, correct condensate flow, reconcile produced-water storage |
| SEC-04 (Compressor Station Process Basis) | Remove TEG dehydration section entirely; redefine outlet gas as compressed wet sour gas |
| SEC-05 (Liquids Hub Process Basis) | Clean non-regenerative caustic treating, remove DSO, reframe LACT, remove glycol/BTEX recovery |
| SEC-06 (Utility Systems) | Remove TEG-derived flare/drain/fuel-gas loads, correct HP KO drum count to 1, resolve heat medium |
| SEC-08 (Plant Design Requirements) | Rebuild sparing table from corrected 03-25 scope |

**Cleanup sweeps (verify and correct, not full rerun):**

| Section | Reason |
|---|---|
| SEC-11 (Civil and Structural) | Remove modules for TEG, stabilizer, heat medium, DSO |
| SEC-12 (Electrical) | Remove electrical loads for deleted systems |
| SEC-14 (Instrumentation) | Remove TEG moisture analyzer, stabilizer-linked analyzer streams |

**Key C&L controller rules:**
- No 03-25 TEG / gas dehydration as active scope
- No DSO / caustic regeneration unless explicitly re-authorized against Process DBM
- One 03-25 HP flare KO drum
- Inlet separators: 2 × 50%, not 2 × 100%
- Condensate flow: 1,111 m³/d / 6,988 bbl/d consistently
- LACT: third-party custody-transfer interface, not excluded from scope
- 04-25 references are interface-only
- No pressure bullets, stabilizers, SOC, or heat medium as active 03-25 equipment

**C&L acceptance criteria (from evaluator §8):**
1. DBM governs 03-25 only; 04-25 handled separately
2. 04-25 appears only as interface
3. 03-25 outlet gas described as compressed sour gas / wet sour gas, not dehydrated
4. No 03-25 TEG system in any section
5. No DSO tank, DSO waste stream, or caustic regeneration
6. Non-regenerative caustic treating described consistently
7. HP flare KO drum count = 1
8. Shared flare stack and incinerator as shared-interface assets
9. Inlet separators: 2 × 50%
10. Condensate flow: 1,111 m³/d / 6,988 bbl/d
11. Produced-water storage: seven-tank basis
12. LACT framed as third-party interface, not erased
13. No retired/legacy equipment as active scope
14. Discipline sections retain only admitted 03-25 content
15. All TBDs are explicit

### 8.2 Deepcut (04-25)

**Mandatory section reruns:**

| Section | Reason |
|---|---|
| SEC-01 (Document Overview) | Remove 400 MMSCFD, clarify 03-25 as interface |
| SEC-02 (Project Scope and Construction) | LACT included not excluded, remove 04-25 condensate storage, resolve MRU |
| SEC-03 (Feeds, Products, Wastes) | Fix composition unit label, correct phosphorous spec, fix product distribution matrix, fix storage table |
| SEC-04 (Inlet Separation and Stabilization) | Inlet separators = 2, MPFF = 1, stabilizers = 3 × 40% |
| SEC-06 (Gas Treating and Acid Gas Disposal) | Correct AGI compressor model/discharge/composition to Process DBM basis |
| SEC-07 (Dehydration) | Resolve TEG sparing to Process DBM basis, handle MRU |
| SEC-08 (Cryogenic Recovery and Fractionation) | Remove depropanizer as current scope |
| SEC-09 (NGL Treating and Dehydration) | Remove depropanizer downstream routing, resolve NGL treating current/future status |
| SEC-10 (Product Handling and Vapour Recovery) | Correct booster coalescer to 140 MMSCFD, remove local condensate storage, fix truck wording |

**Cleanup sweeps:**

| Section | Reason |
|---|---|
| SEC-11 (Utilities) | Quarantine VE-26 heat medium unless admitted, resolve generator diesel/gas |
| SEC-12 (Flare and Drain Systems) | Remove incinerator scope gap; treat as shared-interface per Process DBM |
| SEC-13 (Prime Movers and Emissions) | Fix compressor ratings to match SEC-05, fix incinerator status |
| SEC-14 (Mechanical Design Requirements) | Rebuild sparing table from corrected scope |

**Key Deepcut controller rules:**
- No 400 MMSCFD total-capacity statement
- 03-25 as interface only
- NGL LACT included per Process DBM
- No local 04-25 condensate product storage unless separately admitted
- Composition table: mole fraction, not mol%
- C5+ phosphorous: <1.0 wppm
- No depropanizer as current scope
- Incinerator: shared-interface included equipment per Process DBM
- Inlet separators: 2 (not 4)
- MPFF: 1 (not 2×100%)
- Stabilizers: 3 × 40% (not 2 × 100%)
- Inlet/sales compressors: 5 × 6,700 hp consistently
- Sales gas booster: 1 × 6,700 hp, 140 MMSCFD
- AGI compressors: 2, KBK/6 TBC per Process DBM
- VE/discipline overrides must be explicitly admitted

**Deepcut concordance-critical assertions (from evaluator §6):**

| Assertion | Required governing value |
|---|---|
| 04-25 facility capacity | 300 MMSCFD / 8,490 e3m³/d |
| Doe 02-11 treatment | Included in 303 MMSCFD total, excluded from 300 MMSCFD design composition |
| Composition table units | Mole fraction (not mol%) |
| C5+ phosphorous spec | <1.0 wppm |
| 04-25 NGL LACT | Included |
| 04-25 condensate storage | Not local product tanks unless admitted |
| Stabilized condensate destination | 03-25 Liquids Hub |
| Inlet separator count | Two |
| Inlet separator slug capacity | Process DBM value (~33.9 m³) |
| MPFF count | One |
| Stabilizer count | Three, 3 × 40% |
| Inlet/sales compressors | Five, 6,700 hp |
| Sales gas booster | One, 6,700 hp, 140 MMSCFD |
| AGI compressors | Two, KBK/6 TBC |
| AGI discharge design pressure | 1,500 psig |
| TEG sparing | Process DBM basis unless superseded |
| NGL mercaptan treating status | Current or future — resolved, not both |
| NGL molecular sieve status | Current or future — resolved, not both |
| Depropanizer | Not current scope unless admitted |
| Incinerator | Included shared-interface equipment |
| Emergency generator | Gas-fired unless VE admitted |
| Heat medium configuration | Process DBM basis unless VE-26 admitted |

---

## 9. Source-Concordance Validation (Gate 6)

### 9.1 Prohibited-residue search (C&L)

After section reruns, search the assembled DBM body for these terms. Each remaining occurrence must be either valid interface context, non-governing historical note, or removed:

- `TEG` (except as 04-25 interface reference)
- `dehydrated sour gas`
- `4 lb H2O/MMSCF`
- `DSO`
- `caustic regen`
- `inlet stabilizer` (except as retired/historical)
- `stabilizer overhead` (except as retired/historical)
- `pressure bullets`
- `V-4150` (second HP KO drum tag)
- `Heat Medium` (except as interface or explicitly resolved)

### 9.2 Prohibited-residue search (Deepcut)

- `400 MMSCFD` (total site capacity)
- `depropanizer` (except as future provision or historical)
- `mol%` in composition tables using mole-fraction values
- `1.5 wppm` (phosphorous)
- `KBT/6` (AGI model — Process DBM says KBK/6)
- `1,200 psig` as AGI design basis (Process DBM says 1,500)
- `100 MMSCFD` as booster coalescer design (Process DBM says 140)
- `four inlet separator` or `4 x 50%`
- `2 x 100%` for MPFF
- `1,340 hp` for sales gas booster

---

## 10. SCOPE_CHANGE Escape Hatch

If the rerun proves that upstream root truth is itself wrong — i.e., the decomposition state or KTY-local content contains errors that caused the publication failures — open a targeted SCOPE_CHANGE amendment. Do not use the publication rerun to silently fix upstream truth.

Criteria for SCOPE_CHANGE:
- A KTY-local KA file contains a factual statement that contradicts the Process DBM AND that statement caused a publication error AND the KA file needs correction to prevent recurrence

Criteria for publication-only fix:
- The section worker misinterpreted or misapplied correct source/KTY content — fix in the section rerun, not upstream

Default lane: publication reset. SCOPE_CHANGE is the exception path.

---

## 11. Sequencing

```
1. Write this plan                                    ← you are here
2. Both agents classify review items (4-bucket)
3. Gate 1 refreeze (both roots, parallel)
4. Gate 2-3 revision (both roots, parallel)
5. Gate 4 concordance register revision (both roots, parallel)
6. Gate 5 targeted section reruns (per §8)
7. Gate 6 full package rebuild + source-concordance validation
8. Gate 7 human acceptance
```

Steps 3-5 may proceed in parallel across roots. Step 6 requires all section reruns complete.
