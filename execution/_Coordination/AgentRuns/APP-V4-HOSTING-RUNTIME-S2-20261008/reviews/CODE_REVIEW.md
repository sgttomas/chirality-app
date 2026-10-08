# Independent staged S2 runtime review

Verdict: **CHANGES REQUIRED — one blocking scanner defect.** Reviewed exact nine maintained-file hashes in implementation/CANDIDATE.json, receiving HEAD `7311df06d81ce4d45bb1222080e52731f1ed45ba`, and all 13 staged paths. This is a review of the first partial S2 synthetic slice, not whole S2 or canonical adoption. Reviewer changed no reviewed source.

## Blocking finding

**P2 — Validate earlier descendants again before declaring a complete scan stable.** `app/src-tauri/src/distribution_preflight.rs:walk` (immediate entry stamp comparison, lines 190–196; final directory-only check, lines 198–201) and `scan` (lines 204–218). After a regular file has been hashed and immediately restatted, its later in-place modification is invisible while later siblings are scanned: the earlier file is never checked again, and in-place writes do not update its parent directory metadata. The public scan therefore returns a successful stale inventory despite a mutation during the scan. The same scanner is the final pre-spawn revalidation foundation.

Reproduction in independent copied-source harness: create `a` with bytes `old`, then `b` as a 512 MiB regular file; start scanning and change `a` to `new` after 25 ms while `b` is read. `reviewer_earlier_file_mutation_during_later_read_is_detected` fails because scan returns Ok and the old SHA-256 of `a` (`cba06b5736faf67e54b07b561eae94395e774c517a7d910a54369e1263ccfbd4`). See mutation-test.log and retained harness test source. No supplier execution occurs. This is a missing scan-time full-inventory stability check, distinct from the unavoidable residual race after a completed check. Repair by retaining/checking all observed entry identities and metadata through an end-of-traversal full-tree stability pass, including nested files/directories and root, and add a regression. The method need not claim hostile same-user immutability.

## Passing evidence and scope

- All nine candidate hashes match. The only existing Rust source change exports the staged Unix module; production Host remains untouched.
- Exact author suite: 11 passed. Initial sandboxed attempt passed ten and failed invalid-name fixture construction with EPERM; authorized escalated rerun passed unchanged. This was an environment restriction, not a scanner defect or criterion change.
- Six independent copied-source controls pass: replacement pair cannot satisfy original selection digest; malformed schema and escaping/absolute/malformed artifact refs refuse; artifact symlink/hardlink aliases refuse; pure empty-tree scan/mode and relative-root behavior; foreign/extra H5 fields refuse; repeated generation behavior characterized.
- The private seam is stateless: two calls with the same generation both succeed at explicitly unverifiable staging. This is a recorded limit rather than an additional blocker for the bounded slice. The future Host allocator/child registry must establish uniqueness and prevent evidence reuse; exact tuple equality alone does not do so.
- Compiled production selection is None. Test injection is private. Outputs always say staged-preflight.s2/unverifiable, and RETURN explicitly excludes Host.start, native resolver/probe/launch, real environment/home effects, lifecycle publication, installed custody and qualification. Those exclusions are truthful; their absence is not itself a finding against this partial slice.
- Backchecked manager selection status update and RS_CONCURRENCE: bounded agent co-owner concurrence does not become independent code review, canonical adoption, qualification or a new owner gate. Initial method-selection conclusions remain valid.

## Evidence and limits

CODE_READ_BASIS.json identifies source bytes and origins. Author-suite and independent-tests logs preserve executed results. The temporary harness copies the candidate module/resources unchanged and appends independent tests only; no dependency download or supplier/native execution occurred. No production pins, MEMORY, accepted Design, or reviewed source was edited. Full App regression and later actual-path integration are outside this review. Re-review the repaired scanner and affected tests before fan-in.
