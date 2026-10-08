# PKG receiving supplement — EXP-SUPPORT-BINDING-v1

DEL-01-06 adopts the additive full-support binding defined by DEL-09-01
`Design/support-identity-v1/METHOD.md`, through named technical change
CC-EXP-SUPPORT-IDENTITY-01, effective at its independently reviewed merge.
Before that merge this receiving supplement is an adoption candidate.

The existing PKG-v0.2 protocol, schema, prototype, records and source locks remain
unchanged. The current package record's `support_revision` retains EXP-v0.2.
For the canonical full-identity cohort, keep its exact bytes and add the
canonical sidecar defined by EXP's binding schema. The maintained canonical
reader externally pins both supplements, declaration and schema; the package
writer cannot select or publish another support revision.

Use `app/examination/support_identity/canonical.py check` for the complete
package + rerun result + review + change-impact join, with the two preserved
prior-result states and a separately frozen selection digest. The selected
package reference must identify the selected package record, and App revision,
build, Codex pin and full support identity must agree. Existing PK-R rules and
EXP rules remain enforced by unchanged validators. A missing sidecar has no
full-identity fallback to the version-only field.

A current producer binding declares its basis; historical correspondence does
not establish producer use. Neither can authenticate custody, actual signing,
review or native observations. File consistency preserves FP prerequisite gaps
and never establishes Option B reliance, FP-2/W-4, M1/M2/M3 or qualification.
Actual installation/smoke witnesses are separate results on the same package.

Existing inventory/unsigned preparation and legacy package checks retain their
current partial standing. SQ, native-form and S4 distribution consumers require
their own explicit receiving adoption before claiming this method's guarantees.
No S1/H3B method or supplier-reference contract is amended by this supplement.
