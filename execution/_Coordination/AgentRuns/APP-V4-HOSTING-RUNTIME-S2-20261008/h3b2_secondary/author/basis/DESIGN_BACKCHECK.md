# H3B namespace design backcheck

Verdict: READY for bounded implementation of the exact revised H3B-NAMESPACE-01 proposal. Parent alone releases implementation. This is design readiness, not code acceptance, tested lock safety, canonical adoption or qualification.

The four prior required refinements are closed:

- REC-unavailable behavior is selected explicitly: valid configured-path/full-namespace geometry admits live protective authority with ledgerUnavailable=true and REC bindingCommitted=false; no ledger creation or durable-binding claim. Invalid geometry refuses before mutation.
- Dispatch's outer lease explicitly ends after actual write and hot write-result update, before inline persistence and response wait. Nested attachment and Store helpers reuse borrowed leases; ownership-lock lifetime is tied to that lease. Nonblocking authority then REC-writer acquisition resolves the previously open contention choice.
- Exact attachment-owner concurrence covers stale prepared dispatch, stale AttachmentLink outcome refusal and Arc-pointer mismatch cold fallback. Actual original write/response stays visible; no automatic rebind, replay, hot restoration or historical-prepared-as-current-no-send claim is allowed. The original owner concurrence names an earlier proposal hash; its appended precise clarifications explicitly cover these revised decisions. It is not represented as a signature over the final proposal hash.
- All final fallible checks and checked epoch arithmetic precede either assignment; private REC token commits infallibly under retained guards. No prospective Host registration is allowed. Postcommit Host/HomeSession/router failures preserve admitted protection and carry explicit setup-unavailable standing, with no premature key exposure or false rollback claim.

The lock-order and test fence now define concrete implementation obligations: namespace outside frame/custody/gate/Inner, no REC-to-authority reverse edge, no recursive lease, no admission-held frame/gate, slot/home lookup guards released before lease use, prompt busy release, nested operation and Stop/EOF controls, unavailable-REC branches, old capabilities, each final/postcommit failure and visible late outcomes. These are sufficient bounded requirements to begin implementation; exact coverage and deadlock/liveness claims still need independent code review and deterministic synthetic evidence. No unresolved accepted-meaning change is identified within this fence. Any changed pointer join, automatic rebinding, new storage domain, retry/outcome semantics or qualification claim must return for named review.

Source assessment is reused at fa71b93432612a3615d0c2db0e5767811818454a from H3B_NAMESPACE_DESIGN_REVIEW.md; its full source hashes remain the precise inspected basis. This backcheck read only revised proposal and concurrence material, ran no tests and edited no repository source. Continuing independent harness-native TASK under hosting manager; no delegation. Shared code-review instruction basis unchanged.

## Exact input hashes

- `/private/tmp/H3B_NAMESPACE_ADMISSION_PROPOSAL.md`: `15907e97c803d64037251b512110591e9611733611d731242810056492d580d6`
- `/private/tmp/H3B_ATTACHMENT_NAMESPACE_OWNER.md`: `a6921e3b3027707fdb36696deacd6419ddc3881791359fdd7b6f8782800a049f`
- `/private/tmp/H3B_NAMESPACE_DESIGN_REVIEW.md`: `28cff193c46fc7b42f64261b7cf4abde696b21432c378bbb544cabc0bd7e68f9`
- `/private/tmp/H3B2_ATTACHMENT_NAMESPACE_RS_CHOICE.md`: `dd475fc393c1cb70f08e7c38f91f8c9979249ac401749c3bdea36ef31666ab89`
