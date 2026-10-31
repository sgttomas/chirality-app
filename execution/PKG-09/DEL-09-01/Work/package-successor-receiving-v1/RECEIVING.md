# Package/S4 -> EXP -> SQ receiving v1

The usable current path is explicit: packaging's `packaged-s4-binding/1` and
`static-package-input/2` evidence are checked by its authoritative successor
validator, then joined to existing EXP-v0.2 results and an SQ-v0.2 dossier.
This is selected-evidence consistency with synthetic regression coverage, not
an actual package/installer/native witness or a release decision.

## Interface and identity

`app/examination/package_receiving/adapter.py` consumes packaging's maintained
`check(request_path, evidence_root=..., trusted_publisher_sha256=...)` API.
No scanner, tree measurement, supplier or native operation runs. All nested
artifact references use one explicit evidence root. The validator's exact
source closure comes from its maintained `source_dependencies()` function and
is pinned in `sources.package-v1.json`, not taken from caller evidence.

EXP `subject.app_candidate.package_record` and SQ `candidate.package_record`
cite the OUTER wrapper `record_id`. The producer report independently joins
`candidate.package_record_id` to the INNER static legacy record. These identities
must differ as well as remain semantically distinct; equal strings refuse so
inner-record citations cannot masquerade as wrapper citations. The receiver
neither derives one from the other nor translates
S4 bytes into the S1 `verification_artifact` slot or into PKG-v0.2.

The separate `exp-package-witness-binding/1` sidecar binds exact wrapper bytes,
wrapper identity, candidate tuple, receiving-code/source-profile identity,
configuration digest, original EXP support tuple/declaration and current terms
documentary selection. It is a receiving declaration, not proof of actual
producer use or a published new EXP/package schema. Existing canonical bindings
for EXP results/reviews/changes and legacy packages are unchanged.

Publisher trust comes from an independently selected configuration file and its
separately supplied digest:

```json
{"format":"exp-package-receiving-config/1","trusted_publisher_sha256":null}
```

The field may be null (reported missing trust) or the exact independently chosen
publisher-binding digest. The request cannot choose that digest for the reader.
Synthetic tests supply an invented trust configuration explicitly; no actual
publisher or owner act is inferred. Changing configuration requires new explicit
selection and sidecar correspondence. A matching digest establishes consistency,
not authentication, signing authority or live-start permission.

## Direct EXP use

From `app/`, with prepared Python dependencies and a scratch Codex home:

```sh
python3 examination/package_receiving/adapter.py bind \
  --request PACKET/binding.json --evidence-root PACKET \
  --configuration CONFIG.json --configuration-sha256 SELECTED_CONFIG_SHA
python3 examination/package_receiving/adapter.py package-link \
  --request PACKET/binding.json --evidence-root PACKET \
  --configuration CONFIG.json --configuration-sha256 SELECTED_CONFIG_SHA \
  --result RESULT.json --revision SELECTED_REV --build SELECTED_BUILD \
  --pin SELECTED_CODEX_PIN --package-ref OUTER_WRAPPER_RECORD_ID
```

The link preserves original EXP result-schema/rule checks, candidate/native-
packaged route, packaged subject, exact revision/build/Codex pin, full EXP support
identity, current currency and wrapper citation. Producer errors are errors;
producer missing inputs and a linked non-pass native result remain gaps. Reported
static/FP/S4 values never establish an actual native run. Reports retain false
qualification, release and live-authority flags and the producer's limits.

## SQ use and strict closure

The additive `sq_receiving/receive_packages.py` selects
`sq-exp-receiving-selection.package-s4.v1` with the existing closed selection
fields plus `package_source_profile_sha256` and `configuration_sha256`.
`package_witness` is a new explicit artifact kind with exact record/binding refs;
`packages` still maps each cited outer wrapper to its result slots. Configuration
path/digest are separate command-line arguments, never selected by the packet.

```sh
python3 examination/sq_receiving/receive_packages.py PACKET/sq-selection.json \
  --selection-sha256 SELECTED_SELECTION_SHA \
  --configuration CONFIG.json --configuration-sha256 SELECTED_CONFIG_SHA
```

The original SQ result, review, evidence-set, scenario, candidate, change-impact,
reopening/history and completeness joins remain in the successor worker. Legacy
package artifacts retain the original validator and conditional package-link.
The report names each package's selected route and whether S4 witness evidence
was selected. Legacy completeness never claims an S4 check. New witness
artifacts invoke packaging's validator and preserve errors/missing
through the final SQ report. Missing cited packages, unreferenced artifacts,
duplicate identities, mismatched candidates/configuration/profiles and mixed
sidecars refuse. The successor is explicitly current-purpose; historical
correspondence continues through the original reader unchanged.

The worker captures existing historical EXP/SQ sources as before. Packaging's
maintained Work closure is staged in a SEPARATE private source root, so an
historical Design directory cannot redirect its resolver to an incomplete
layout. Its imports/schemas read only that captured closure; no ambient-repo
fallback is allowed. Evidence remains under the separately selected packet root.

Exit 0 means complete selected consistency, not qualification. Errors, missing
or unsupported joins remain nonzero. Existing external/native evidence references
remain visible; selected coverage never authenticates review independence,
human acts, signatures, custody, signing/notary/installation or release.

## Generation, compatibility and remaining release evidence

Run `python3 app/examination/package_receiving/generate.py` from repository root
after integrating a changed producer/checker head. It derives the package profile,
new SQ source pins and reader constants, and refuses collisions with the original
SQ source selection. It does not refresh old terms, standalone, admission,
canonical, distribution or terminal cohorts. Never hand-merge generated pins.
`app/tests/package_successor_receiving_fixtures.py` composes packaging's maintained
synthetic generator with the existing SQ fixtures and maintained aggregation
rule; original fixture/evidence bytes are not rewritten.

DEL-09-01/DEL-09-02 ScopeOfWork and dependency requirements were reconciled by
inspection and remain unchanged. The new Work accounts and code/check declarations
identify the implemented receiving path. In particular the full-document current-
admission Scope/protocol subjects are not changed to force a repin.

Real release evidence still requires the selected publisher/owner inputs,
identified actual signed/notarized package and installer, full actual inventories,
applicable installed S4/native/FP observations and joined candidate results,
independent examination and the owner's separate release/replacement decision.
No fixture pass supplies those acts or artifacts. Unrelated known terminal/S4
historical-source conditions are not swept into this adoption.
