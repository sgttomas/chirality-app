# Independent R1 scanner repair backcheck

Verdict: **READY for the bounded first partial S2 synthetic slice.** The single blocking scanner finding in CODE_REVIEW.md is repaired and independently backchecked. No unresolved blocking findings remain at this scope. This does not complete S2, adopt canonical consumers, qualify a supplier, establish production verification or satisfy a native/stage gate.

Exact reviewed maintained files are in R1_CANDIDATE.json and R1_READ_BASIS.json; all nine match the frozen candidate on receiving revision `7311df06d81ce4d45bb1222080e52731f1ed45ba`. Scanner SHA-256 is `37ee4686c469bceaa3b5e2812a89c836cc9180799da3baa931cba2ad516a0896`; author-test SHA-256 is `a8a864b5472d95bce914b8e45de069946c076c303ede31831373b29a2c5d0fef`.

## Repair and checks

The scanner retains the initial identity/metadata stamp for every entry, then revisits complete membership and stamps after all content reads. The no-follow final audit checks root/descendant identity, mode, size, link count, nanosecond mtime/ctime, directory membership and path rebound; the root path is also reopened and compared. This addresses the earlier-file/later-read gap rather than merely changing a test expectation.

- Independently reran the original ordinary mutation vector unchanged against copied repaired source: pass (mutation refused).
- Independently reran the original equal-size mutation with restored mtime vector unchanged: pass (mutation refused). The test restores and verifies exact mtime via futimens; it explicitly verifies that ctime changed. It does not claim to restore ctime or all OS metadata.
- All six earlier independent controls pass again: original-anchor replacement, malformed schema/artifact references, linked artifacts, public pure scanning, each H5 field/extra-key contradiction and repeated-generation characterization. Total independent checks: **8 passed**.
- Exact maintained author suite: **13 passed**, with the same authorized escalation used to permit invalid UTF-8 fixture construction; no test criterion changed. Staged diff whitespace check passes.

Original failure evidence, original copied source and CODE_REVIEW.md remain preserved. Repaired-source harness and logs are separate (`harness-r1`, `r1-independent-tests.log`, `r1-author-suite.log`). No reviewed source was edited by this reviewer; no download, supplier execution, credential use, production pin, MEMORY or accepted Design modification occurred.

## Remaining limits

The final metadata sweep is not an atomic OS snapshot. Mutation after an entry's final audit, adversarial interleavings and the later check-to-exec window remain possible. Trustworthy stable installed custody is still required for eventual production reliance. RETURN's R1 section states that bound accurately, and this slice stays explicitly unverifiable with no production selection.

Generation uniqueness remains a future host-allocation/custody duty: the stateless private seam verifies exact H5 tuple agreement but accepts repeated identical allocations. Host.start, actual bundle/probe/launch/environment/home integration, child custody, lifecycle artifact publication, S3 supplier qualification and connected consumer adoption remain the expressly named next increments. These limits do not constitute additional defects in this bounded partial slice and must not disappear from integration claims.
