# Harness Validation Traceability

## Requirement Mapping (DEL-07-01)

| Requirement | Coverage Artifact(s) |
|---|---|
| REQ-01 Validation Script Coverage | `frontend/scripts/validate-harness-section8.mjs` required check set (`setup.server_reachable`, `regression.session_crud`, `section8.boot_error_taxonomy`, `section8.smoke_stream`, `section8.session_persistence_resume`, `section8.permissions_dontask`, `section8.interrupt_sigint`, `section8.sdk_native_stream`) |
| REQ-02 Local Execution | `npm run harness:validate:section8` and `npm run harness:validate:section9` from `frontend/` |
| REQ-03 CI-Ready Posture | `npm run harness:validate:premerge` (non-interactive, exit-code based for Section 8; report-only Section 9 during the initial integration cycle) |
| REQ-04 Session Boot Validation | `section8.boot_error_taxonomy`, plus `frontend/src/__tests__/api/harness/routes.test.ts` boot route tests |
| REQ-05 Turn Execution Validation | `section8.smoke_stream`, `section8.session_persistence_resume`, plus route tests for invalid empty turns |
| REQ-06 SSE Streaming Validation | `section8.smoke_stream`, `section8.sdk_native_stream` |
| REQ-07 Opts Mapping/Fallback | `frontend/src/__tests__/lib/harness-options.test.ts` |
| REQ-08 Subagent Governance Fail-Closed | `section8.permissions_dontask`, `frontend/src/__tests__/lib/harness-subagent-governance.test.ts`, governance route tests |
| REQ-09 Attachment Resolver Validation | `frontend/src/__tests__/lib/harness-attachment-resolver.test.ts`, attachment-focused route tests |
| REQ-10 Prompt Mode Selection Validation | `frontend/src/__tests__/api/harness/routes.test.ts` prompt-mode assertions |
| REQ-11 Validation Documentation | `frontend/docs/harness/README.md`, this file |
| REQ-12 Repeatable Execution | Two consecutive `harness:validate:premerge` runs; deterministic summary schema |
| REQ-13 CONTRACT K-Invariant Coverage | Governance + options + route tests (`harness-subagent-governance.test.ts`, `harness-options.test.ts`, `routes.test.ts`) |
| REQ-14 Test Isolation | Vitest unit tests are independently executable; section8 checks are isolated by per-check setup/cleanup |
| REQ-15 Error Path Validation | `section8.boot_error_taxonomy`, route tests for invalid request/attachment/governance paths |
| REQ-16 Deliverable Acceptance Criteria | `harness:validate:premerge` gate + docs + traceability mapping |
| REQ-17 Section 9 Runtime IDs | `frontend/scripts/validate-harness-section9.mjs` current deterministic ID set (`section9.runtime_engine_contract`, `section9.adapter_turn_engine_event_log`, `section9.adapter_message_mapper`, `section9.session_event_replay`, `section9.settingsources_isolation`, `section9.permission_overlay_hard_deny_precedence`, `section9.tool_runtime_read_file`, `section9.chirality_mcp_status_dependencies`, `section9.path_containment_hook`, `section9.instruction_root_protection_hook`, `section9.tool_result_budget`, `section9.context_compaction_boundary`, `section9.subagent_governance_hook`) |
| REQ-18 DEL-01-02 Reliance Boundary Register | `docs/harness/reliance_boundary_register.md` maps reliance boundaries to current Section 9 IDs, enforcement surfaces, and future/TBD validation IDs. |
| REQ-19 ADQ-04 Runtime Evidence Reconciliation | `docs/harness/runtime_evidence_reconciliation.md` maps PKG-03 and PKG-04 evidence to current implementation truth, D-APP-18 key-aware default posture, current `harness:event` ownership, D-APP-38 source-state handling, and active Section 9 IDs. |

## Notes

- D-GOV-43 (A2), 2026-09-12: REQ-05 and REQ-06 are read against the revised transport. The stream carries the extensible upstream-preserving event representation (`docs/SPEC.md` §11); a client disconnect unsubscribes and never interrupts the turn; the adapter boundary is the Runtime service's socket API with Codex as the only engine. `section8.sdk_native_stream` and the SDK-named unit tests are Claude-path compatibility history where they still run.
- The premerge script enforces required check IDs and fails if legacy IDs appear.
- The suite uses stable machine-readable summary output for CI consumption.
- Section 9 starts as premerge report-only while `STAB-01` proves the new aggregator.
