# Historical distribution/terminal receiving disposition

Agent 0 selected this bounded source/reliance disposition on 2026-10-31: the
synthetic LT09/LT23 distribution and terminal cohorts are retired from CURRENT
release reliance. Their original bytes, guards, tests, reports and producer
subjects remain retained. This removes no product acceptance criterion and
establishes no actual lifecycle, custody or release result.

Subjects remain `stop-admission` at producer
`127d48f61d91b70d00d0670d2150c79b8ac26d1f` and `build-selection` at producer
`b5dbfbbdf300b993f34fc87924146073bb017877`. The historical exchange formats
`group-b-s1-reader-exchange.v1` and `group-b-s1-terminal-reader-exchange.v1`
represent synthetic S1/legacy-transport file correspondence, not the current
signed package or an authenticated stopped process tree.

The current operational guard in `distribution_receiving/inputs.json` has exactly
two mismatches at this disposition:

| Input | Retained expected SHA256 | Current SHA256 |
|---|---|---|
| `app/examination/support_identity/canonical.py` | `e08f3d633e9476ce1073e050545f2b8e99bc71c65cd93b2d4bf0fe2a8346c470` | `f1eb9a692d70a13c7b91d7d5d3c38cc3699bf3c4b1158528ce5a731ad04123dd` |
| `app/examination/support_identity/canonical-pins.v1.json` | `5fedcaa0908ff4aa320bc415965c00aad273cac241b731f660a36600e494901c` | `0866799740ba54d572c1bf480d3a95bed546e3a914146b00ea1a3cab9a0e90f3` |

The three selected S1/lifecycle/transport schema hashes and terminal helper hash
still match. Other hashes such as historical `hosting.rs` identify the immutable
producer subject; they are not current executable inputs of these file readers.
No hash is refreshed here. Tests and CI selection remain unchanged; the broad
manual suite is not claimed clean. A future request to execute a historical
entry point must select its legitimate frozen input/reader closure explicitly,
not suppress its failure or label old bytes current.

The additive package/terms/S4 -> EXP/SQ route from PR57/59 does not consume these
exchange formats. Their drift therefore does not block that useful integration.
Pre-spawn installed-S4 package consistency is NOT terminal lifecycle proof.

For the actual release candidate, its native execution owner still supplies
issuer/source-bound stopped/tree-ended events and descendant facts, with the
actual candidate, supplier generation, observed outcomes and unknowns retained.
The examination owner joins that evidence to its candidate and reports limits;
Agent 0 coordinates any reserved acceptance/release decisions. A current terminal
adapter is allocated only when an actual record and consumer need exist. No new
synthetic cohort, live/model/native run or owner act is implied by this disposition.
