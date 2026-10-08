# Lifecycle version-label join, semantic revision s2

`lifecycle-label-join.s2` corrects only the version-label join of the staged
S1 lifecycle reader. It is not a full S1 semantic validator. Shape validation,
exact artifact resolution, generation equality, outcome, reference, custody,
and other lifecycle checks remain separately required before reliance.

`label_join_identity()` identifies the semantic revision, SHA-256 of the
compiled reader source bytes, and SHA-256 of the exact lifecycle-event.s1 and
observed-verification.s1 schema bytes. Consumers must explicitly adopt this
method tuple. The schemas remain byte-identical to the staged S1 schemas;
unchanged shape does not imply compatibility with the historical semantic
reader. No digest is stored inside the bytes it digests.

For a version-bearing legacy event, `observedVersionLabel` must be the full
`codex-cli X.Y.Z` label without a newline. The observation raw label permits
exactly zero or one terminal LF. Removing that one allowed LF must yield the
legacy label byte for byte. Its parsed three ASCII decimal components must
equal observation `observed_label`, observation `pin`, and legacy `declaredPin`.
No other trimming, prefix replacement, case conversion, missing-label synthesis,
or version coercion is allowed. Missing or contradictory inputs refuse.
Non-version-bearing events are dispatched separately; this method refuses them.

The Host's legacy records and historical S1 reader are unchanged. This method
does not establish supplier qualification, package/support joins, or a complete
S1 observation. The synthetic Host test supplies only the facts needed for this
bounded join and claims no full S1 validation. Version-bearing publication is
held pending independent treatment review.
