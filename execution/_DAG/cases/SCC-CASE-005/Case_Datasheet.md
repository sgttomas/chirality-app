# SCC-CASE-005 — Connector receiving and recovery cases

> **30% framing (current owner clarification):** this case characterizes unresolved work and its later/post30 route. A fully resolved DAG, completed interfaces or supplied future witness inputs are not prerequisites to the30% gate. Input-specific limitations apply only when the corresponding work needs them; no whole-Deliverable/project hold follows. Qualified initial graph-basis/version decisions and the actual30% decision remain separate. See the [recorded clarification](../../../_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/RUN_BRIEF.md#owner-clarification--30-and-unresolved-sccs).

## Current observation applicability

WORKING_ITEMS matched this stable case by member set to **SCC-004** in `_Evaluation/DepClosure/CLOSURE_APP_V4_TARGETS_2026-09-27_2237` (source `85dcc17c3fda4bce82332a40f27aa9b4e849653e`, manifest `0b60d9a2a9342acf40ac7074876115954d897a7e595ec319b223e7460e0e80a4`). The set is unchanged. All 8 internal source rows are identical to the original inquiry; current member CSV/index/SoW hashes match the refreshed manifest.

The refreshed independent report `6b0b0268e79315eddb4e2595dffd30e12b5f483bd6c74e2341be03b67d2a1a11` passes affected repair fidelity and retains raw acyclic closure BLOCKER, six SCCs, with no concrete source defect established. This is observation applicability, not a ruling, completed remedy or fulfilled input. The original inquiry and positional SCC labels below remain explicitly historical at their stated first source; the current positional match is the one above. Existing alternatives, responsibilities, missing-input limits and HUMAN_RULINGS_PENDING standing remain unchanged.

## Original inquiry and retained evidence

- CaseState: HUMAN_RULINGS_PENDING (decision-ready inquiry; no ruling supplied).
- CASE_ID: SCC-CASE-005; origin SCC_ID: SCC-005.
- Originating observed DepClosure snapshot: `projects/chirality-app-v4/execution/_Evaluation/DepClosure/CLOSURE_APP_V4_INITIAL_2026-09-27_2149`.
- Member node set / affected Deliverables: `DEL-07-01;DEL-07-02;DEL-08-01`.
- Later matched snapshots / membership changes: none. Seed artifacts / human rulings: none.
- Frozen source revision: `c1038ae5ac5c23a30ea7d3b516cd9033cb47f77b`; source manifest SHA256 `30a85cffb5832313be60bafd297428cca331f3e7712b2a822eae488fe924d7fc`.
- Standing: analyzer COMPLETE / subject FAIL, seven SCCs, complete 41-Deliverable coverage. This is supplied observation evidence, not an accepted graph. Final source audit has now been read: WARNINGS / raw acyclic-production-order closure BLOCKER; no concrete source-fidelity defect found in the bounded examination, including all intra-SCC rows. Its SCC-005 interpretation confirms these distinct receiving/recovery contributions and independent common work. The audit is observation evidence, not graph acceptance or product validation. [E01–E03/E13–E15]
- Identity check: the case home was absent on first read; the manager reserved this unused ID and member set. No duplicate, prior or legacy case was found in the validator's home check.

## What actually circulates

Canonical DAG arcs mean **consumer → supplier (depends on)**: UPSTREAM keeps the written local-owner → target order; DOWNSTREAM reverses it. The table deliberately uses the opposite, **supplier contribution → consumer**, view: UPSTREAM becomes target → local owner and DOWNSTREAM stays local owner → target. Eight rows support four internal arcs; no direct PEC ↔ Domains arc exists. [E04–E09/E13]

| Row | Preserved source Direction | Canonical depends-on arc |
|---|---|---|
| DEP-07-01-014 | UPSTREAM | DEL-07-01 → DEL-07-02 |
| DEP-07-01-015 | DOWNSTREAM | DEL-07-02 → DEL-07-01 |
| DEP-07-02-010 | UPSTREAM | DEL-07-02 → DEL-07-01 |
| DEP-07-02-011 | UPSTREAM | DEL-07-02 → DEL-08-01 |
| DEP-07-02-012 | UPSTREAM | DEL-07-02 → DEL-07-01 |
| DEP-07-02-014 | DOWNSTREAM | DEL-07-01 → DEL-07-02 |
| DEP-08-01-009 | UPSTREAM | DEL-08-01 → DEL-07-02 |
| DEP-08-01-010 | DOWNSTREAM | DEL-07-02 → DEL-08-01 |

| Supplier → consumer contribution view and exact rows | Required contribution and point of need | Relationship |
|---|---|---|
| DEL-07-02 → DEL-07-01: DEP-07-01-014; DEP-07-02-014 | Common limitation/source-file recovery route, used by the PEC adapter for its affected question, including no response. SoW 07-01 REQ-005/AC-005/VER-005; SoW 07-02 CLM-003/REQ-002/004. | Two descriptions of the same supplied route, not opposite transfers. Definition can begin from ordinary source records; actual integration needs the usable route. |
| DEL-07-01 → DEL-07-02: DEP-07-01-015; DEP-07-02-010; DEP-07-02-012 | PEC-specific question, unsupported conclusions and responsible handoff (07-01 AC-005); actual receiving meanings before dependent implementation (07-02 TBD-001); exact qualified/released/adopted envelope account for the later operational join (07-02 REQ-006/AC-006/VER-006). | One graph arc aggregates distinct question/terms and later operational-evidence transfers. These are genuine contributions back toward fallback, not duplicate descriptions of its outgoing route. |
| DEL-07-02 → DEL-08-01: DEP-08-01-009 | Common supported recovery/responsibility behavior at Domains local case preparation/exercise. SoW 08-01 CLM-005/REQ-005/VER-005. | Production/interface input for the Domains cases; it requires neither PEC delivery nor completed Domains operation. |
| DEL-08-01 → DEL-07-02: DEP-07-02-011; DEP-08-01-010 | Domains admission/query/provenance/freshness meanings and applicable boundary terms for integrating the Domains path (07-02 REQ-001/CLM-003/TBD-002), plus Domains-specific admission/query cases (08-01 CLM-005/REQ-004/005). | Two records on one directed arc, with terms and case handoff distinguished. Common recovery is the opposite transfer; neither is a whole-Deliverable start gate. |

The cycle expresses shared contract definition plus connector-specific integration/case return. The sources support later verification and conditional receiving, not an architectural-defect conclusion or a claim that every deliverable must finish before the next begins. Rechecking PEC premises/coverage at its actual receiving point and source freshness at intended Domains use can recur; no version cadence or recurring graph rule is specified. [E07–E09]

## Contributions that can be coordinated

These are proposed work milestones under existing responsibilities, not new lifecycle states or acceptance gates. [E07–E11]

1. **Common recovery definition:** DEL-07-02 maps limited/absent conditions, ordinary records/revisions, missing sources and actual agent/manager/human responsibilities. It can document and walk an independently supported source-file question before either connector or later fleet software is available (REQ-002/004/005).
2. **Separate receiving definitions:** DEL-07-01 supplies proposed PEC questions and identifies agreed versus open OI-022 terms; DEL-08-01 defines query/admission/freshness obligations and exact OI-023/OI-026 decisions. Both use the common route contract and return connector-specific needs. No invented schema, freshness threshold or provider assignment supplies an unknown.
3. **Bounded cases and integration:** PEC preparation may use explicitly simulated terms (07-01 REQ-008); Domains fixtures need identified query meanings and admitted test sources (08-01 REQ-004). Common recovery exercises each supplied case and the absent-PEC/stale-Domains combination. A missing source/term leaves only its affected check unexercised; definitions and independently supported recovery continue.
4. **Actual later joins:** PEC operational use needs provider identity, qualified/released coverage and deliberate App adoption through DEL-07-01. Domains research reliance needs actual query access, source admission and local-data-boundary compatibility; Domains joins a later increment through DEL-08-02. Provider/tool, workflow, host and human acts retain their separate owners and points of need.

PEC ownership remains with PEC; Domains provider construction/allocation remains TBD under OI-026. External knowledge development selects no deployment, transport or extra data destination. No PEC or Domains availability gate applies to initial work. D108's standing described by the local sources supplies neither repaired criteria nor release/adoption; this case does not independently certify provider currency. [E07–E11]

## Candidate treatments and recommendation

| Option | Concrete treatment | Consequence |
|---|---|---|
| R1 — coordinated contribution milestones (recommended) | Use the four contributions above in existing owners' bounded work; keep the four default arcs and all row evidence. Carry the unresolved graph treatment explicitly to project-dag. | Supports useful contract and file-route work now, with actual-case/integration checks at their points of need. It does not make the strict default graph acyclic or resolve external inputs. |
| R2 — narrowly scoped preparation projection | Only if the human selects the objective “ordinary-file recovery plus receiving definition, excluding connector-specific integration and operational evidence,” propose a separate view deferring the contribution-view DEL-07-01 → DEL-07-02 and DEL-08-01 → DEL-07-02 at that milestone (canonical depends-on arcs DEL-07-02 → DEL-07-01 and DEL-07-02 → DEL-08-01). Preserve all five supporting rows (07-01-015;07-02-010/012;07-02-011;08-01-010) in the default basis and enumerate their later obligations. Keep the two common-route contribution arcs (canonical DEL-07-01 → DEL-07-02 and DEL-08-01 → DEL-07-02) for this view. | The three-member projection has no return cycle, but proves only the narrow preparation objective. It cannot stand for complete DEL-07-02 behavior, integration, operational use or the project-wide graph. Requires an explicit objective/cut ruling and later evidence review; none is supplied here. |
| R3 — retain unresolved connector-dependent work in the candidate layer | Hold only implementation/case assertions that need unsupplied PEC terms/envelope or Domains query/admitted-source/boundary inputs. Ask their named owners for those concrete contributions; continue common recovery and source-grounded definitions. | Avoids guessing missing contracts, but supplies no integrated behavior or cycle remedy by itself. R1 still provides the route to make progress while those inputs are outstanding. |

Recommend **R1**, with R3 applied only at a demonstrable missing-input point. No cut or merge-group is preferred or applied. Grouping all three whole Deliverables would conceal the independently optional PEC and Domains lanes and would not establish their missing contracts; the evidence does not require such a group or a scope/decomposition change. [E04–E11]
