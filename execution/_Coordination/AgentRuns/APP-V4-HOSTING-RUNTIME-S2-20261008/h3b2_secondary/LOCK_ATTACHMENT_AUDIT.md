# Secondary-home admission lock and stale-capability audit

Read-only source assessment against37feb501; no tests or implementation. RS concurrence read. Exporter remains frozen.

## Lock order evidence

All three Store use sites in Host release source/custody guards before Store IO: distribution_evidence captures Inner then drops it before read_s1; start captures prospective tuple under writer and drops it before preparation/publish_observed; finish_successor_handshake explicitly drops Inner and attachment_gate before publish_lt09. Store modules contain no REC writer/Host callbacks. No existing REC→Store operation path found in these source call sites. The Store lease must end before each later Inner recheck/final spawn writer acquisition.

Proposed admission order is nonblocking exclusive Store binding lease, then REC writer, then existing REC ledger/source preflight locks. Do not acquire Store from inside existing REC paths. Store shared operation leases span all read/publish reliance, including final checks; nested guards receive the lease rather than locking again. Hash/source closure preflight stays outside REC writer. Final writer section may reobserve bounded namespace geometry and physical IDs only; if this cannot preserve selected identity without rescanning, use a preflight token plus explicit bounded-observation limitation rather than claim atomic filesystem verification. Store busy refuses before REC mutation. This is a source-level lock argument, not tested deadlock proof.

Commit boundary must perform all fallible REC and Store checks before assigning either binding while both guards are held. Prepare key Host/Store capability or classify later construction failure truthfully as post-admission failure. Root must install required current namespace/attachment/Store capabilities before binding or exposing a new key HomeSession for other commands and before its first start. Current lib installs attachment projections before new home creation; preserve this ordering.

## Concrete stale attachment concern: expanded fence required

lib submit_attachments clones home.attachment_custody at557 and passes it into runtime submission. The clone escapes its slot mutex. AttachmentCustody retains an immutable namespace Arc; guard_scope, guard_generation and guard_leaf repeatedly use that same Arc. Replacing the slot at add_api_key299 cannot update or revoke the clone.

Adversarial scheduling trace:
1. An account operation captures old AttachmentCustody, then pauses before its guarded publication/read.
2. Key setup passes the full proposed checks, commits REC/Store, and replaces the account attachment slot with the new capability. The paused clone still contains only old account/probe scope.
3. A newly admitted key-only home or fixed resource binding drifts after admission (for example the key home path is replaced with a symlink, or its required skills link disappears/changes). The complete new binding's protected() would now refuse that observation. The old binding never observes that home/link.
4. The paused operation resumes: old guard_scope/guard_generation succeeds for unchanged account paths and can publish under the stale reduced protective set, whereas the new capability refuses. If the new path aliases an attachment domain, its new-binding exclusion is similarly absent from the old clone; initial preflight alone does not supply at-use coverage.

This is a concrete source-reachable stale-check path, not a reproduced exploit or claim of arbitrary path writes: attachment destinations remain fixed. It predates the proposed Store repair, but a Store-only lease cannot prove the requested invariant that old immutable attachments do not bypass newly expanded protective scope. A short pause of Root slot replacement is also insufficient: cloned capabilities survive the slot update indefinitely.

Return for narrowly expanded design: include attachment namespace-use rebinding/revocation in the reviewed fence, ideally via the same stable shared namespace authority/revision seen by REC, Store and attachment capabilities, or an attachment operation lease plus atomic epoch change that makes retained old capabilities fail closed. Audit attachment ownership lock order and existing Host attachment_gate/REC interactions before choosing the implementation. Do not broaden this into UI/credential behavior or silently claim whole-App atomicity. No implementation should begin on the earlier Store-only fence while this requirement remains unresolved.
