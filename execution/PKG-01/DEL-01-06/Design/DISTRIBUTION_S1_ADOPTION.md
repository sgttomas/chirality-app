# PKG S1 Design source selection

Named change: CC-HOSTING-DISTRIBUTION-01/S1-DESIGN-ADOPTION, basis
9f1f96b17b9a9307827b8d00ae880a6c9a2c0039. This is the DEL-01-06 part of the
review-candidate Design patch; it becomes its technical source selection only
with independent review and integration of the complete patch. No production
consumer or package is adopted by this document.

DEL-01-06 selects `pkg-identity.s1` in the shared single physical cohort at
[DEL-01-01 Design/distribution-s1](../../DEL-01-01/Design/distribution-s1/README.md).
The PKG owner retains ownership of package rules despite the shared file home.
The exact schema, semantic model and source dependency identities are in that
cohort's PUBLICATION.json. There is no alternative local copy or fallback.

The complete original pkg.identity-record schema is retained inside the versioned
envelope. Static distribution_status distinguishes reference-equal, unverifiable
and mismatch; missing qualification is representable. Published/packaged full
inventory artifacts and selected reference/attestation are joined by exact bytes.
An optional runtime observation must bind the exact App/build/package subject and
installer digest and agree with packaged inventory and selected reference.
Known contradiction dominates gaps. The old signing, executable coverage,
entitlement, FP-0/1/3 and Option A/B rules remain; changed stock bytes cannot be
reference-equal. PK-R4's separate terms checker remains mandatory.

This supplement does not alter PACKAGING_AND_DISTRIBUTION.md, legacy schemas,
app/packaging/sources.json or the producing tool. It does not apply the historical
§§4.4/5.5 patch in isolation. Canonical successor producer/reader activation still
requires reviewed behavior, explicit version selection and fresh receiving pins.
Existing EXP/SQ package_link and #1161 SQ receiver remain legacy-cohort checks;
they cannot infer S1 semantics from a string citation or new schema publication.
FP-2/W-4, signing/notary/installation, S3 qualification and owner decisions retain
their existing separate conditions. No supplier tree or App is qualified here.
