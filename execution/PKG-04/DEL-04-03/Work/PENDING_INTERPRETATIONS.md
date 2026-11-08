# Pending record-store interpretation

Source: [issue 168](https://github.com/sgttomas/chirality-app/issues/168).

Pending DEL-04-03 store-location interpretation, outside cleanup (Scope unchanged):
CLM-001 OLD: “The person's decisions, accepted records and run records are ordinary append-only files in the App's records store, outside the working tree an agent edits and linked to their project by a stable project identity (AX-006).”
Candidate NEW: “The person's project decisions, accepted project records and project run records are ordinary append-only files in the App's records store, outside the working tree an agent edits and linked to their project by a stable project identity; A15 library acts and captures retain the separate library paths specified in AX-006.”
Consequence: qualifies project-store location for project records while retaining library A15 acts/captures separately. AX-006 and RS §13.7/13.8 / DEL-02-02 preserve that distinction, but broad PRD V4-REC-02, REQ-001, AC-001 and SOW-092 need coherent source/consumer interpretation before any amendment; exact companion replacements are not yet proposed. No isolated cleanup rewrite or criterion weakening. Current Scope SHA2561335c4c47dc3a4e649c2628e1d974dd18d963968d9142894e33d2a1bb7f29790 and historical/frozen identities retained. This is not evidence that AC-001–007 are met. The RS register-direction no-change disposition stands.

## Decision route

These are pending questions, not approved replacements. One option is to retain
the governing contract and repair or clarify consumers to satisfy it. The other
is a coherent source/consumer amendment, with the applicable owner decision,
acceptance consequences and historical bindings made explicit. Neither a code
match nor a refreshed pin settles the choice.

Recommendation: App Agent 0 first compare the governing source, selected extents,
actual readers and fixtures, then bring a bounded decision packet with companion
changes to the owner through the coordinator. The owner resolves commitment or
acceptance changes; the relevant implementation owner then carries the selected
repair. Existing Scope, code, pins and evidence are unchanged by this note.

AS §6/VC-21 versus RS §8 LOOP-v0.8/v0.9 citation labels also need source/consumer
reconciliation. AS whole-file `4eca598f…` remains bound by policy_standing and
a16 product bases. Options are a demonstrated citation correction preserving
meaning and bindings, or a substantive adoption if actual meaning differs;
no behavioral difference is established. App Agent 0 develops the assessment
with the owning contracts before any selected-source edit.
