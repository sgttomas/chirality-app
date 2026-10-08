# C3-S4 implementation candidate

Status: author-tested candidate for independent review; no full C3 closure or native witness.

## Basis and scope

The accompanying basis records the exact initial CAM source, reviewed CAM-R1 retention amendment, schema 0.3 and manager releases. Source/schema semantics were not edited. This bounded implementation composes a source-evidence draft from current private source/Git evidence and explicit caller inputs, freezes exact serialized bytes, and publishes once through the existing CRP writer. It does not establish source truth, actor performance, full reconstruction, acceptance or reliance.

The branch received main f25ba6887d85904ebef2a6321c222809d47cfabd at ec0b3b0379f7999a39ea3c4e74304b28022bc177. Shared lib.rs merged cleanly: Host namespace guards remain, and source registry/commands are additive. Runtime, native_items, attachment and distribution semantics were not edited. Approved fence clarifications include the narrow Git association recheck, held-root identity accessor and version-specific cold projection.

## Implemented boundary

The host captures current session, selection and completed Git result; rechecks eligibility and association while freezing under the source lock; reserves no identity on failed preflight. The App-instance registry retains at most 64 lifetime identities and one full prepared/in-flight payload. Atomic replacement and cancellation retain compact tombstones. Publication consumes the token once, retains actual BoundReference or StoreError/Attempt despite cancellation or source-session replacement, and does not retry or roll back. Reconciliation adds an observation without rewriting the original uncertainty. Consumed outcomes remain inspectable without a new current-project association. The 64-identity cap is a development safety bound; final product capacity remains unresolved. No restart-as-recovery or eviction is offered.

Schema 0.3 is embedded unchanged. Additional semantic checks reject duplicate duties, revision disagreement, dangling references and altered excerpt digests. Exact serialized UTF-8 size is capped at 1 MiB. Cold original-byte size refusal occurs only after acquisition and format identification; this does not bound initial cold allocation. Old 0.1/0.2 behavior is retained. Cold rendering shows draft standing, compact receipts, excerpts, interpretations and typed responsibility without promoting inspected claims to prior publication or provenance proof.

The connected renderer handlers pass only host references and caller fields to guarded host commands; publication passes only token and generation. Synthetic selection is recorded as synthetic; the production native callback has a distinct mechanism label. No native callback was executed in these checks.

## Executed checks

All checks used existing offline dependencies and the same private, serial target, with CARGO_NET_OFFLINE=true, CHIRALITY_SKIP_CODEX=1 and CARGO_INCREMENTAL=0. No download or supplier/native launch occurred.

- Combined connector Rust tests after main receipt and freeze repair: 69 passed. This preceded the final additional boundary test and retained-outcome lookup.
- Final affected Rust materialization tests: 10 passed, 559 filtered; includes exact 1 MiB publication/cold read, partial and gaps-only drafts, semantic false positives, 64/65 capacity, atomic replacement, stale freeze, duplicate/incomplete/root-change refusal, repeated publication, post-start cancellation/session replacement and retained uncertainty/reconciliation.
- Maintained full npm test: 23 passed, one supplier handshake skipped; nested Rust decide_flow tests: 4 passed.
- Final affected source/route component and handler tests: 17 passed. These exercise actual renderer handler arguments with mocked command transport and synthetic host-session tests, not a native end-to-end witness.
- Final frontend production build passed. Offline Cargo check passed earlier in development.

Constructed repositories use real restricted Git execution and filesystem operations. They are not actual user-project provenance or native selection evidence. macOS was executed; Linux and unsupported-platform behavior were inspected, not executed. Existing process, path mutation and CRP uncertainty limits remain; no OS network isolation or escaped-descendant guarantee is added.

## Findings and repairs preserved

An initial registry capacity fixture failed after an actual publication changed root metadata: association recheck correctly refused its stale observation. The fixture now explicitly obtains a new Git observation before preparing genuinely new drafts; production refusal was not weakened. An initial combined connector run had 68 passes and one obsolete test expecting format 0.3 to be unsupported. It now tests unknown 0.4 and separately rejects a 0.2-shaped document relabeled 0.3. Both original logs remain local diagnostic evidence.

An initial frontend build rejected duplicate default properties before a spread; the initializer was repaired. A handler fixture initially selected an enclosing fieldset rather than the duty fieldset; its selector was corrected. Some wrong-working-directory attempts failed before edits/check execution and were repeated from the correct directory. These are not represented as production defects.

Manager inspection identified stale eligibility between initial capture and freeze. Final source/root/association checks now occur at atomic reservation and a regression proves stale preflight consumes no slot. Final author inspection added retained-outcome lookup before a fresh project guard so repeated calls can report an already completed attempt without creating a new write.

Only this agent's quiescent disposable incremental cache was removed under disk pressure; dependencies and prior results were preserved. Final free space was 5.6 GiB. Cache reuse is local acceleration, not portable qualification. Independent code review and any resulting repairs remain required.
