# App v4 repository migration

App v4 development remains on hold. Migration does not establish examination,
qualification, acceptance or a new release. SWBPIPE remains in Chirality.

The source is `sgttomas/chirality@a6ad85ae82d534c0c064419219258a4df2109e10`,
subtree `projects/chirality-app-v4/`. The owner selected current main and excluded
the old unmerged App branches. Existing `chirality-app` main was
`866d3e7ba0744570e2e2cdb9785cff648a92b88d`; release tags remain unchanged.

An isolated clone used Git `filter-branch --subdirectory-filter` with a saved
state branch. `commit-map.txt` maps original commits to rewritten commits.
Before privacy sanitization, the unadapted import was
`0d145109d5d59533a71bc34930ee71ca2591642a`. Its tree
`25ac3b58096a646009961e15dfc362a5b943acef` exactly equals the source subtree.
The owner authorized sanitizing private machine identifiers in the unpublished
import: 82 commits retain author/committer names and timestamps but use
`redacted@users.invalid` instead of machine-derived email addresses; five
historical blob versions have private identifiers replaced with `private-host`.
Messages are unchanged. Original published history remains in Chirality. The
commit map points to sanitized commits, not the pre-sanitization rehearsal.
The sanitized import tip is `6208d0de4519d1ff07dd6764c6f7ac28158e9830`.
A merge joins that history to existing App ancestry; subsequent commits adapt
paths and verification. Historical SHAs and PR links still identify Chirality,
not rewritten App commits. GitHub discussions are not copied by the import.

`shared-inputs.json` identifies the copied deliverable utility, workflow test
input and license at their original revision and hashes. Local adaptations are
maintained here; synchronization is explicit, not a runtime sibling dependency.

The examination reader's `app/examination/support_identity/frozen/` contains
30 exact historical files from original commit
`6fbd4c8722c9454981ae9518b39cafe4e6ece7c4`, with their original paths and hashes
in its manifest. Readers retain the original declarations and full-byte checks;
operational helper pins are updated for relocation. Neither the original source
identities nor historical evidence claims are rewritten.

The dependency baseline tag `app-v4/deps-baseline-1` maps original Chirality
commit `a7b93ff9ba35fd069481d4c387650b98ca63cc73` to filtered commit
`5fc90f4c79b83f7bfec4e76af69d5b4ad42107ae`. The pre-sanitization project trees were identical; the mapped imported history
includes the documented privacy substitutions.
This is a dependency-comparison reference, not a product release.

Verification before PR: exact import tree and ancestry, 30 frozen source hashes,
102 examination tests, frontend build, eight Rust workflow-bundle tests, schema
copy check and deliverable structure passed offline. Candidate identity, packaging
and utility checks passed 47 tests with 22 connected-packaging skips because `DISTRIBUTION_STATIC_BIN` was unset.
After building that scanner offline and repairing the staging adapter, all 23
static-packaging tests passed with no skips. The terminal export roundtrip passed
on a clean committed candidate; both relocated Design self-tests also passed. No live
examination, sign-in, supplier run or release was performed.

The owner authorized migration Git operations through the existing administrator
bypass while leaving repository rules and integrations unchanged. Destination
`PRIVATE_TERMS` was configured from this host using the existing checker's
`--from-host` source; the original secret's historical aliases were unavailable.

Status: candidate preparation; no cutover yet. Final PRs and integration SHAs
will be recorded in the migration handover.
