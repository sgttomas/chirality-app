# DAG-001 — proposed initial project-graph basis

**Candidate APP-V4-DAG-BASIS-20260928-CANDIDATE-1. Checkpoint1 is pending.** Trigger INITIAL; no predecessor or accepted DAG. The human has already accepted the11 Packages/41 Deliverables and INITIAL setup. This proposal decides the graph's basis, limitations and case tracking; it does not repeat those acceptances.

## Intended milestone and objective

Prepare an examined, qualified initial project DAG for the accepted App v4 work, with unresolved SCCs characterized and routed for later/post30 work. A fully resolved graph, completed interfaces or supplied future witness inputs are **not prerequisites to the30% gate**. The [owner clarification](../../../_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/RUN_BRIEF.md#owner-clarification--30-and-unresolved-sccs) governs this preparation. Actual30% advancement remains a separate decision; graph acceptance neither passes it automatically nor adds a requirement to resolve every cycle first.

Recommended objective: retain the **full required-contribution account**, using the default project-dag selection rules and an acyclic admitted layer plus explicitly held candidate relationships. An edge means the consumer needs the supplier's stated contribution, at its stated maturity/condition, before the stated part of its work. It does not assert that every part of the supplier must finish before any part of the consumer begins. This is one App project's graph, not a cross-project authority or a schedule.

Canonical direction is consumer→supplier (depends on); UPSTREAM is From→Target and DOWNSTREAM is Target→From. Contribution sketches may show the reverse supplier→consumer direction when labeled. INITIALIZED is checked-contract maturity only; actual artifacts, acts, qualification, provider release/adoption and receiving evidence remain separate. The six target refinements retained their existing TBD maturity; no maturity or satisfaction was promoted.

## Source and coverage

Source revision `85dcc17c3fda4bce82332a40f27aa9b4e849653e`; [source manifest](SOURCE_MANIFEST.sha256) SHA256 `0b60d9a2a9342acf40ac7074876115954d897a7e595ec319b223e7460e0e80a4`. All130 entries bind actual local registers/indexes/SoWs and accepted inventory/coordination input. The inventory is independently derived from accepted Group3 Deliverables.csv:41 nodes,11 Package homes, no exemptions; all modes FULL_GRAPH. All262 scope IDs and10 objectives remain unchanged. [DeliverableNodes.csv](DeliverableNodes.csv) retains every node, independently of edges or input availability.

FULL_GRAPH is the selected tracking posture and intended coverage, with the following explicit qualifications proposed for acceptance. Forty-one valid registers contain759 rows:355 active anchors,403 active execution and1 retired extraction. Of the403,201 local-target rows yield161 arcs;144 EXTERNAL,26 DOCUMENT,18 PACKAGE and14 UNKNOWN rows remain non-topological but relevant to their actual inputs. No execution input is marked SATISFIED. Thirty-two package/unknown entries distinguish already allocated producers/partial support, future candidate/value/contract-subset/reader instances, and genuine technical/allocation choices. They are not32 new owner decisions or a complete allocation/readiness proof.

The [refreshed independent audit](../../../_Evaluation/DepClosure/CLOSURE_APP_V4_TARGETS_2026-09-27_2237/Dependency_Closure_Report.md) passes affected repair fidelity and canonical/source checks, reusing unaffected prior checks. Its raw topology has6 SCCs involving24 nodes,52 internal arcs represented by66 rows,14 bidirectional pairs and a degree21 record-interface hub. There are no schema, orphan, declaration or isolated-node findings. Its raw-acyclic BLOCKER/subjectFAIL means those coupled arcs cannot all be admitted unchanged into an acyclic layer; it is **not** a30% failure or a demand to resolve them now. The17 nodes outside SCCs are not automatically ready.

The original c1038ae5 observation and [target-resolution proposal](../../../_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/TARGET_RESOLUTION.md) remain history. Independent backchecking confirmed five precise target substitutions plus separate trace/owner-ruling inputs, with no SoW, scope, status, declaration or existing maturity/satisfaction change. The selected Codex pin now has its known producer, while its actual value remains open.

## Proposed default selection and reliance

Apply the selected `chirality-root:bundled:workflow:project-dag` SR-1…SR-7 in order:

1. Included inventory registers at the frozen manifest.
2. Canonical ACTIVE EXECUTION rows with local Deliverable targets enter topology. Non-topological, outside, unresolved or invalid rows stay explicitly accounted; their exclusion supplies no input.
3. All canonical dependency types remain selected; no blanket INTERFACE/HANDOVER/verification exclusion.
4. Apply only actual human cut/merge rulings. **None is proposed for application in this recommendation.**
5. No extra confirmation-hold rule is proposed.
6. One representative per arc: consumer UPSTREAM, then DECLARED before EXTRACTED, then lowest DependencyID. Mirrors/same-arc rows and distinct conditions remain in accounting/live input evidence; deduplication does not erase obligations.
7. Unresolved intra-SCC arcs and self-loops go to the non-gating candidate layer with their cases and work lacking inputs. No arbitrary subset is removed to draw an acyclic picture.

An acyclic admitted layer does not resolve or supply held inputs. Held candidates cannot generate blocker queues, waves, schedules, priorities or dispatch-readiness claims. Only work that actually needs a missing contribution remains limited at that point; unrelated independent work is not blanket-held. All local obligations, including non-topological provider/actor inputs and mirrors, remain visible. Cases characterize future resolution; they are not a demand for completed interface production before30%.

## Current coupled groups and proposed case lineage

| Current observed SCC | Members / stable case | Proposed treatment for this initial version |
|---|---|---|
| SCC-001 | 01-01;01-05 / CASE-001 | Retain qualification-return coupling; later coordinate identified pin/protocol, account/provider evidence and the actual return criterion. |
| SCC-002 | 01-04;02-01/02/03/04;03-01/02/03;04-02/03;05-01/02;09-09 / proposed continuing CASE-002 with CASE-004 lineage | Retain the13-member coupling; characterize the existing-output interface/record/catalog/adapter/trace contributions and specific missing inputs. The actual OI-003 disposition stays with its human actor, distinct from trace production. |
| SCC-003 | 01-06;09-01 / CASE-003 | Retain reusable examination-support and actual package-return obligations; native evidence remains required at its witness. |
| SCC-004 | 07-01;07-02;08-01 / CASE-005 | Retain common recovery versus connector-specific meanings/cases and later qualified joins; PEC/Domains availability does not gate initial App or file recovery. |
| SCC-005 | 10-02;10-04 / CASE-006 | Current records support initial graph definition; accepted/current graph supports later selection. No bootstrap requirement for an already accepted graph. |
| SCC-006 | 11-01;11-03 / CASE-007 | Current continuity feeds replacement evidence; an actual later owner disposition returns to continuity. No favorable act, adoption or retirement is implied. |

Abbreviated IDs in this table mean App-v4 DEL-* and SCC-CASE-*. Exact member sets, contributions/OUT/REQ, receivers, alternatives, evidence and next steps are in the linked [reader](READER.md) and stable case folders.

**Case-match proposal reserved to the human in this checkpoint:** continue SCC-CASE-002 as the record for the new13-member component, preserving its original nine-member history and SCC-CASE-004's original two-member inquiry as traceable constituent history. Keep both case IDs/files; do not treat this as a Deliverable, responsibility or product merge. The source-supported extra trace arc exposed a larger existing coupling. Neither case is automatically reassigned or closed before this ruling. Other five member sets match exactly, though positional SCC labels changed.

## What changes the characterized holds

Case plans identify later/post30 contributions under existing owners, without authorizing product or provider construction. The larger case's contribution matrix names existing OUT/REQ, earliest separately usable content, receiver/check and actual evidence still needed. At their points of need, owners produce/identify those versions, receive/check the relevant handoff, and record satisfaction or the remaining limit. A source/contract refinement uses its owning method; material source changes refresh extraction/closure. A different graph objective or a cut/graph group needs an explicit scoped ruling. Neither a new label nor INITIALIZED alone changes a hold.

Routine future candidates, review recipients, source sets and contract versions are selected when the relevant activity is defined; they do not create blanket approval gates. Existing policy/host-placement/model-interface/catalog-representation and Domains allocation/admission choices remain with their recorded owners. SWB/PEC construction, actual human acts and provider qualification/adoption stay external or separately evidenced. No new scope choice is hidden in target resolution.

## Alternative and next actual steps

A narrower initial-production projection is an explicit alternative described in case/design evidence. It would require named objective-relative selection/cut rulings and retain later obligations outside its admitted layer; it cannot stand for a complete lifecycle order. It is not applied or recommended instead of the full contribution account with characterized candidates.

After actual basis/case-match confirmation, apply that recorded choice, assemble the exact41-node version with complete row accounting, run canonical strict audit on its admitted layer, and obtain separate independent version review. Present that concrete qualified initial version for the method's second human decision. Unresolved SCCs may remain characterized candidates; no further SCC resolution or interface-production tranche is inserted as a pre30 condition. Only after actual version acceptance is its immutable snapshot/pointer/handoff written. Product implementation, input fulfilment, lifecycle and the30% decision remain separate.
