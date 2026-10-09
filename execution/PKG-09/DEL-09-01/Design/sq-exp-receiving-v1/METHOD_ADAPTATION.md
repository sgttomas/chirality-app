# SQ-EXP-RECEIVING-v1 — EXP binding adaptation

Named technical change: **CC-SQ-EXP-RECEIVING-01**. Supplier owner: DEL-09-01;
receiving owner: DEL-09-02, whose `Design/sq-exp-receiving-v1/RECEIVING.md`
specifies the closed selection, joins, reporting and source-level test obligations.
Standing: Design candidate for independent source review, selected as the parent's
bounded technical target. Independent Design READY precedes parent release of
implementation; actual reviewed source adoption/integration is recorded separately.
Neither this file nor any writer flag establishes product acceptance or qualification.

## Existing method remains intact

`../support-identity-v1/METHOD.md` defines EXP-SUPPORT-BINDING-v1 and its initial
six-role `exp-support-selection.canonical.v1` route. Its before/after/rerun/review/
change/package roles and mandatory unchanged package/review/change joins remain
mandatory there. This supplement does not generalize that API, relax its selection,
change its publication reference or alter any of its frozen source pins.

The underlying EXP-v0.2 sources retain their original identities: protocol,
three schema IDs and prototype SHA-256. The canonical declaration still names
prior publication `09106477e351c6e5bde85259c55a00cc8fc5f7f5`; adoption of the
original binding method is separate from that publication, and adoption of this
receiving adaptation is separate again. No relabelling or schema bump is made.

## Explicit new receiving cohort

The new route is **SQ-EXP-RECEIVING-v1**, with selection format
`sq-exp-receiving-selection.v1`. It reuses each canonical
`exp-support-binding.canonical.v1` sidecar exactly: kind, record ID, raw-byte
SHA-256, fixed declaration hash, EXP version, all three schema IDs and prototype
SHA-256; binding_method remains EXP-SUPPORT-BINDING-v1. All sidecars share the
selection's purpose, current_producer_declaration or historical_correspondence.
Neither purpose proves producer use or upgrades historical provenance.

A separately pinned receiver must compare the declaration to actual selected
source bytes and schema IDs, and check each sidecar against original record
bytes. It must then validate the selected records and perform the receiving
joins. `canonical.py:binding` alone is only declaration construction. It is not
record validation and is not a substitute for the receiving checks. The new
reader may reuse the unchanged canonical identity checks and lower validators;
it must not call the existing six-role selection with omitted or fabricated roles.

SQ dossier and case-definition bytes are bound by the receiving selection, not
by inventing a dossier kind in the canonical binding schema. Direct EXP results
and the primary review receive individual sidecars. Package/change sidecars and
joins arise only from their actual selected citations. Missing required records
remain incomplete; honest native_development does not acquire a package duty.
Historical before/after snapshots may share an ID only in their explicit pair,
while exact byte identities remain distinct. Original outcomes/history remain.

DEL-09-02 S1–S3 owns direct-step and exact dossier review mappings, explicit
review-set file closure, conditional attachments and incomplete/unsupported
reporting. Existing one-record review/change helpers' unresolved references
must be accounted for by the new receiver, not silently erased or claimed as
legacy helper coverage. All existing schema/rule errors remain errors. No
additional observation, evidence-location, native-held authority or generic URI
resolution semantics are added by this support adaptation.

## Propagation and limits

A future maintained SQ receiver must freeze both supplements and the complete
selected SQ/EXP/schema/prototype/validator source closure under its own reviewed
pins. Original canonical, S4, standalone preparation and native-form pins/code
remain unchanged. Preparation already captures source identity; it never emits
an executed-result sidecar for a blank form. DEL-11-03 still owns its downstream
receipt and reliance decisions. DEL-01-06 obligations apply only to cited packages.

The receiver reports exact correspondence and declared outcomes only. It never
authenticates source publication, method adoption, producer use, independence,
actual native observation, complete affectedness, criterion permission or
qualification. Source READY releases only the parent's next bounded technical
phase; it is neither implemented behavior nor a product acceptance event.
