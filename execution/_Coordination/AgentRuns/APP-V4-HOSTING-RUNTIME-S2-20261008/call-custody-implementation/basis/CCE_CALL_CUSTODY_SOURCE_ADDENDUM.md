# Offered-call source addendum — corrected reply ordering and record origin

PROPOSED, code held. Exact source f028d12edcd23c8aaf6a1b67e6efc66a3cfda19b. Supplements the corrected CCE_CALL_CUSTODY_IMPLEMENTATION_BRIEF.md; no ordinary behavior/schema repair, build, process or test action.

## Correction provenance

Earlier brief SHA8a883c6c19f68bf37cc127106899df68c6ad55f8e8f5da37a35ec85aeaf84fce incorrectly asserted that resolution changes settling to resolved-by-supplier. That assertion is withdrawn. Exact earlier bytes are retained as CCE_CALL_CUSTODY_BRIEF_WITHDRAWN_RACE_PREIMAGE.md, not overwritten as if the error never occurred. The corrected trace below comes from source reading, not a reproduced failure.

## Existing source trace

| Ordering | Actual existing mechanics |
|---|---|
| Resolution while outstanding | native_requests.resolved431–454 sets resolved-by-supplier and retains resolution. prepare refuses an already-resolved entry. |
| Prepare | prepare310 onward admits original unsettled request and sets settling before Host.write_reply. |
| Resolution while queued for final cut | resolved does not change settling. The full resolution notification is journaled; reply_eligible1290 onward scans matching generation/RPC/thread and refuses before write. |
| Resolution after cut, during IO | State remains settling. Bytes cannot be unsent. For a still-current/open generation, written406 onward records actual write success/failure and settles. The journal still preserves resolution. No acknowledgment is inferred from this timing. |
| Resolution after recorded successful reply | Existing resolved branch may record acknowledgment for answered/declined or eligible later-error entries with written result. Do not broaden or retroactively apply that rule. |
| Write failure | written records write-failed while eligible; later resolution in failed/error states is retained without manufacturing success/ack. |
| Generation closes/supersedes during IO | Host.write_reply returns after IO but before written/persistence on changed/closed source. This is the distinct current local-result/canonical-settlement limit. close() marks closedGeneration and changes only outstanding entries, not settling. |

An offered implementation that left its request outstanding during IO would introduce a prospective hazard; it must use the existing prepare→settling discipline. It is not evidence that current ordinary code has the withdrawn race.

## Proposed offered-only attempt accounting

At the final eligible cut reserve one private attempt attached to the original incoming-call capability. Keep immutable original H5/Host/offer/call/RPC identity, cut receipt position, and fixed one-shot local result. The captured private record remains owned by the original handle if Inner moves to a later source. Record actual write_complete outcome before the canonical post-IO generation eligibility branch. A fixed completion cell with checked one-shot state can retain this result without a callback or role-owner lock under Inner; exact synchronization/source scope receives code review.

For a current/open original request, preserve the existing written/resolved behavior and projection. For post-cut closure/supersession, keep the original canonical entry unchanged and expose actual local Written or WriteFailed/UnknownDelivery only in a separate private offered-attempt projection. Do not add fields to the closed ordinary schema, rewrite historical closure, settle a successor, or label canonical not-attempted as the effective result of the already-admitted attempt. The private projection explicitly reports canonical settlement unavailable for that combined observation.

Resolution observation is independent: retain its actual receipt/order, distinguish before-cut refusal from post-cut receipt, and never infer acknowledgment merely from write success or post-cut timing. Existing ordinary acknowledgment rules remain unchanged. No automatic retry, second attempt, new reply after pre-cut resolution, delivery claim, TASK/session record or release of a role/WR capability follows.

The additional projection is prospective treatment for the offered path's post-cut facts, particularly actual IO followed by generation closure. It is not a generic fix for written(), resolved(), or ordinary write_reply. Before code, EXEC/native-request and Host source owners must concur that this separate private observation meets the selected evidence duty without altering canonical meaning.

## Offered origin projection

Current native_requests.records210 onward maps known-answerable methods other than currentTime/read and person-input methods to originClass=a14. Merely admitting item/tool/call as known-answerable would therefore incorrectly inherit A14 origin. The closed runtime_core/hosting.server-request-entry.schema.json permits originClass=named-service. It permits settlement kind=answer with origin={class:app-rule,ruleName:managed-service-unavailable}; answered requires replyWriteResult=written and kind=answer. A14/person-input plus app-rule instead restricts kinds to decline/error, so the fallback is also incompatible with the proposed unavailable result projection.

Propose an offered-only projection branch selected by private provenance created during original register admission, never a native argument or capabilities flag. Preserve that provenance with the retained original entry so historical record projection cannot later fall back to a14 after the active offer slot retires. Only privately offered item/tool/call projects known-answerable/named-service. All unoffered and ordinary mappings/bytes remain unchanged; no broad method-name exemption.

The exact native unavailable content remains success=false with the inputText text specified by the proposal. An eligible local write may project answered/answer/app-rule as a protocol response, not managed-service success or permission. Do not set the person-negative flag or produce decline solely because success is false. Malformed arguments use the explicit RPC error path with kind=error; local write failure is write-failed/unknown delivery. No person actor, A14 authority, human acceptance or acknowledgment is invented.

Private provenance is not a new public schema field/capability. Existing entries() copies cannot be imported to create it. If source owners find named-service unsuitable semantically despite structural schema permission, return that exact source treatment before implementation; do not widen the schema or silently use A14.

## Required discriminating checks after release

Test resolution before prepare, while queued, after final cut/before write completion, after actual write/before settlement, and after recorded settlement separately. Test closure/supersession after cut separately from resolution. Preserve actual local write outcomes and immutable original facts; verify no second write/retarget/retry or acknowledgment inferred from the private result. Offered records must validate existing closed shape without A14/person/decline inference; ordinary records and unsupported bytes must compare unchanged. These tests remain process-free anonymous-pipe scenarios with explicitly synthetic incoming frames/simulated write errors. No execution is authorized by this addendum.

## Private attempt lifetime

The separate attempt observation is same-process and test-owned, bound to the original incoming-call attempt. Its captured original-attempt record remains retained through in-flight completion and source closure while the original handle is alive; closure does not retarget it or confer any current capability. An in-flight operation retains only the original record needed to finish that observation. No new production recovery store, cold durability or hydration is introduced. Dropping the last owning handle/in-flight reference loses this private observation; it is not reconstructed from journal, exported JSON or canonical records. Retained post-closure facts remain historical attempt observations, never authority to send or resume work.
