> **Subsequent act:** [Group2 was approved](../../_Decomposition/checkpoint_snapshots/GROUP2-20260927T233018Z/DECISION.md) after this clarification. The clarification itself was not that approval. Its [exact original bytes](../../_Decomposition/checkpoint_snapshots/GROUP2-20260927T233018Z/presentation/APP-V4-IMPLEMENTATION-CLARIFICATION-20260927.md) remain frozen; the historical account below is unchanged.

# Initial harness and implementation sourcing — scoped owner clarification

HELP_HUMAN supplied this exact owner clarification during the Group2 discussion:

> Codex is sufficient for now. For the "chirality's own" we were going to look at exemplars like Pi and T3 Code (and maybe others, you might have notes on that) so we can implement the best open source code by learning from what works and adapting to our needs.

This is parent-transcribed conversation evidence, not a raw platform export; message identifiers and a platform timestamp were not supplied. It resolves initial harness breadth and implementation sourcing. It is **not Group2 confirmation** or acceptance of the proposed PKG-01/PKG-02 split. The five structural recommendations remain under discussion.

## Treatment in the successor proposal

- PKG-01 is named **Native App and third-party harness integration**: the native App shell integrates the stock third-party Codex harness initially. It is not a new Chirality-owned App agent engine or a generic multi-harness gateway. DEL-01-05 explicitly names Codex-native OAuth/ChatGPT sign-in, API-key and local-provider access; Codex retains credential custody. PKG-05's minimal host-loop receiving work remains separate, with external host construction and conditional common allocation unchanged.
- “Chirality-owned” means responsibility for the required behavior, receiving-contract fit, integration and maintenance. It does not require every implementation to be written from scratch.
- Assess relevant Pi, T3 Code, v3 and other exemplars for suitable components or patterns. Selectively reuse or adapt what fits the receiving contract and maintenance needs; no named source must be copied. Keep significant source/version/attribution and adaptation rationale in the existing SoW or ordinary PR record, and qualify the actual selected code and versions, including applicable reuse terms.
- The retained initial stock-Codex and minimal-host direction, external construction boundaries and exclusions stay intact. Choosing Pi's agent runtime as a new dependency, a whole-application fork or a generalized gateway would be a distinct architecture choice, not a consequence of using reference code. No dedicated research Package or per-row research checklist is added.

## Retained context, with its original standing

The authoring [T8 T3 return](../AgentRuns/V4-CONCEPT-20260925/tasks/T8-t3code.return.md) records a dated source investigation; [MAINTAINABILITY_ANALYSIS §5](../../../conceptual/MAINTAINABILITY_ANALYSIS.md) retained T3 code/patterns as useful references while distinguishing gateway/fork options. Its earlier ACP recommendation was later rejected under conceptual D-17; citing the reuse discussion does not revive that architecture.

The [T10 Pi return](../AgentRuns/V4-CONCEPT-20260925/tasks/T10-pi-libraries.return.md) and analysis §11.1 examined libraries and loop patterns. [Conceptual D-20](../../../conceptual/DECISIONS.md) then selected Tauri and the minimal loop, amending D-19's Pi-runtime direction. The [T7 landscape](../AgentRuns/V4-CONCEPT-20260925/tasks/T7-supplier-landscape.return.md) is a locator for additional candidates. These are dated leads, not current fitness, license or supplier-terms certification. No code is selected, copied, installed or executed by this clarification.

The revision preserves 11 Packages, 41 Deliverables, all 262 ScopeItemIDs, mappings, context envelopes and accepted Group1 meanings. Candidate1 remains recoverable at Git 17b8083da50f0ddc9851e017b2f3e51c48a8da19 and in its unchanged review folder. Candidate2 has its own reader/manifest identity and reuses Candidate1's broad review plus one affected scope/readability backcheck.
