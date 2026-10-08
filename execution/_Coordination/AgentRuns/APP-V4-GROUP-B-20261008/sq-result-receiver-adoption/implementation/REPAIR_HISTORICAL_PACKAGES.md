# Independent-review repair: all selected candidate package citations

Original candidate: `29f390b7c586da94eef4a408ea70bb04dd5a04b4`.
The reviewer found that package citation collection considered direct dossier
steps only. A separate historical before/after candidate pair with an otherwise
valid change join could cite MISSING-HIST-PACKAGE while packages=[] incorrectly
returned complete. Supplying that package for a different historical revision
was also incorrectly refused as uncited. Both new discriminating tests failed
against the original worker before repair. Original author evidence and the
original connected receipt remain unchanged and refer to that candidate.

The repaired worker collects package citations from every selected EXP candidate
result. The package ID and each result's own revision/build/pin must match.
The current dossier identity applies only when the dossier itself cites that
package, not to an unrelated historical candidate. Historical/reopened and
pre-change snapshots retain exact file/binding/identity checks but do not claim
current package_link guarantees; their helper scope is reported unsupported.
No package is fabricated and absent cited package selections remain incomplete.

Three maintained regression tests cover missing historical package, correctly
supplied different historical candidate, and substitution of the current dossier
identity for that historical package. All 35 affected receiver tests pass after
repair. The test retains the actual current direct dossier/results unchanged,
so its historical-package assertion cannot pass merely by changing direct-step
coverage. No Design, schema, six-role, S4 or legacy validator change was made.

Only the new worker identity changes in its 41-source manifest; the 40 existing
source identities are unchanged. The fixed new receiver pin digest is refreshed
for this reviewed repair, not moved to a different source cohort. Staged and
commit-range privacy checks precede return; no machine-name/JUnit output retained.
No native/build/supplier execution, download, credential use or push.
