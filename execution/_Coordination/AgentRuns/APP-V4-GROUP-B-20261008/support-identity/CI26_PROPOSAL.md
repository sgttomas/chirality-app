# CC-EXP-SUPPORT-IDENTITY-01 — proposed CI-26 disposition

Status: **PROPOSED, offline maintained support implemented; canonical contract
publication and consumer adoption not performed.** Base:
`00ce2e10749dbf72cb69cd6814baab82e339d224` (PR #1134 merged).
Owning route: DEL-09-01 with DEL-01-06, coordinated by the Group B manager and
HELP_HUMAN. This package does not close CI-26 or establish M1 reliance.

- PROPOSAL: Add an explicit versioned full-support binding beside existing records
  - Evidence: DEL-09-01 Design/EXAMINATION_PROTOCOL.md §4.4 defines the support revision as EXP version, three schema IDs and prototype SHA-256, published by the deliverable freeze/merge, never a record writer. Its result schema provides its own schema ID and optional prototype digest, while review/change-impact schemas have no support identity field. DEL-01-06 Design/pkg.identity-record.schema.json carries only `support_revision: EXP-v0.2`. app/CONTRACT_ISSUES.md CI-26 records this mismatch. Staged distribution_successor/ADOPTION_PACKAGE.md S4 preserves complete EXP identity and immutable artifact joins.
  - Change: Review the new `exp-support-binding.v1` sidecar and fixed `exp-support-declaration.v1` as the smallest additive representation candidate. Bind each original exact-byte artifact, record kind and ID to a declaration containing the full support identity plus exact source hashes. Retain all original record bytes and current schemas. The proposed `exp-support-selection.v1` freezes the six artifacts and existing join selections with an externally supplied digest. Keep `frozen_candidate_not_published` distinct from any later canonical publication instrument.
  - Why: Full identity becomes inspectable across result/review/change/PKG without falsely treating legacy version-only data or an opaque alias as a full immutable support revision.
  - Risk: Consumers that ignore sidecars retain only their current partial identity guarantees. Changing source bytes invalidates this frozen candidate. No automatic repinning, mixed-version fallback or apparent publication should be allowed. Historical records lacking a producer's full identity cannot be retroactively asserted to have used it merely by generating a sidecar today.
  - Status: PROPOSED

- PROPOSAL: Adopt declaration selection separately from record writing
  - Evidence: EXP §4.4 reserves publication to the deliverable freeze/merge; CI-26 names DEL-09-01 and DEL-01-06 as owning route. Existing package-link/admission validators are source-pinned and reject drift. The staged S1 consumer plan requires coordinated reader behavior and source-lock migration.
  - Change: Before canonical reliance, owning Design review must identify the published support source bytes and the exact declaration, applicable record/consumer versions, publication provenance and effective boundary through its accepted route. The eventual reader must select that declaration outside the untrusted record and enforce its digest. Writers may describe artifact bindings only. The current tool contains no publication input, approval flag, override manifest or authority-verification mechanism; its only standing is an unpublished frozen candidate.
  - Why: A self-consistent writer-generated declaration cannot manufacture published support identity or adoption.
  - Risk: This proposal does not decide the final publication instrument, does not substitute a SHA-256 digest for authority, and does not establish real-world artifact origin or qualification. The final canonical mechanism remains with the owning loops.
  - Status: PROPOSED

MISSING: Reviewed canonical publication/selection mechanism and disposition;
consumer adoption; actual package/examination artifacts and independent native
witnesses. The supplied joined evidence is explicitly invented.

NEEDS_HUMAN_RULING: none introduced by this bounded tooling proposal. Existing
reserved owner acts and any decision rights in the final adoption route remain
unchanged; manager confirmation authorized only this staged implementation.

DEPENDENCY_NOTES: EXP M1 → PKG; EXP/PKG → SQ and S4 receiving; S1 full-support
identity remains required. No group-order reversal, new Deliverable or source
contract amendment occurs here.

## Diagnosis and implemented boundary

The mismatch is representational rather than merely a missing equality test.
Adding required fields to existing closed schemas would break current writers,
examples, prototypes and source-pinned readers. A versioned sidecar is additive
and permits an actual connected file join while retaining the legacy contracts.
A later canonical successor can reuse, amend or replace it through review.

The new checker pins its declaration and schema, captures all fixed source
bytes and independently confirms schema IDs/formats and prototype identity.
It checks exact input/binding hashes, mandatory full identity and the supplied
candidate/build/pin/package references. It executes the unchanged accepted
package-link, review-join and change-join tools over the captured bytes in a
scratch project. Their rule checks and limits remain visible. It refuses
unresolved extra review/change references for this bounded complete join.
The before/after history is checked by the existing change validator; only the
rerun is joined to the supplied current package. Earlier package custody and
omitted history are not inferred.

The CLI's `bind` command emits only an unpublished description, with no record
validation/pass claim. `check` reports only identity consistency, always with
publication/adoption/qualification false. Observed link checks are best effort,
not hostile-filesystem no-follow custody. Sources and artifact bytes are frozen
for each check, not made immutable on the external filesystem.

## Consumer migration plan — not yet applied

| Order / consumer | Required reviewed change | Current preserved behavior |
| --- | --- | --- |
| 1 / DEL-09-01 publication owner | Decide named CI-26 disposition, canonical full identity representation and external publication-selection mechanism. Identify exact schema/prototype/source bytes and which producer freeze wrote each artifact. Review actual candidate and negative cases. | EXP-v0.2 and existing schemas/prototype untouched; proposed declaration is not publication. |
| 2 / DEL-01-06 PKG owner | Adopt matching support binding or a jointly versioned PKG successor; bind install witness, package and published support by exact bytes. Propagate named contract change. | Current PKG version-only `support_revision` and legacy package-link remain unchanged. |
| 3 / EXP writer/readers | Update maintained writer/reader paths and only then corresponding source locks atomically. Support immutable historical reads; do not backfill historical producer claims from current sources. Preserve native evidence and independence requirements. | Existing examination/sources.json, admission/sources.json, validators and all canonical bytes unchanged. |
| 4 / staged distribution S4 | Combine full EXP identity with exact candidate/package plus full supplier-reference and attestation identities, using S1/S2 contracts and S3 for verified standing. Reject mixed-version and unresolved references; explicit aliases do not establish custody. | This tool has no S1 publication authority, supplier-reference qualification or runtime verified-standing claim. |
| 5 / SQ, native forms and downstream examination | Propagate exact adopted support selection, original record/binding byte identities and changed-rule impact assessment. Re-examine only affected warrants; retain actual performer/reviewer and native route requirements. | Existing SQ/native-form source locks and readers retain their accepted basis; no blanket adoption. |
| 6 / qualification owners | Receive actual packaged install/smoke and joined scenario evidence under the adopted revision, plus real independent review. Only then assess M1/M2/M3 and qualification under governing sources. | Invented fixtures and file passes cannot establish any native witness, gate, 90% claim or release. |

Review/adoption should cover the actual combined revision and all affected
consumer tests. A Git merge of this proposed tool is integration only. No new
publication or signing/owner approval mechanism is invented by this packet.
