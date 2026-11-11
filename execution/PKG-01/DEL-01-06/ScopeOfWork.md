---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-01-06
package_id: PKG-01
decomposition_basis: execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z
project_scope_refs: [SOW-098, SOW-117, SOW-134]
package_objective_refs: [OBJ-002]
---

# DEL-01-06 — macOS packaging and distribution evidence

## Purpose and Objective Traceability

This deliverable turns an identified App candidate into one installable macOS package with the supplier's unmodified Codex inside. It builds, signs and notarises the package; records exactly what is in it; witnesses that it installs and launches from a download; ships a notice for every component in it; holds the supplier's written position on distributing an App that uses its sign-in; and states the limitations the release carries.

It is the CI_CD_CHANGE `DEL-01-06` of PKG-01 in the accepted decomposition, the packaging contribution to OBJ-002. A package that launches shows nothing about the access modes or the wider behaviour that other deliverables own.

| Accepted scope | Contribution | Source |
|---|---|---|
| SOW-098 | The package targets macOS on Apple Silicon and is witnessed there | PRD V4-CST-02; EXAMINATION V4-EXM-01, V4-EXM-03, V4-EXM-04 |
| SOW-117 | The supplier's written sign-in distribution position is held before public release beyond owner use | PRD OQ-08; ARCHITECTURE §6, §8 |
| SOW-134 | Signing and notarisation of the App and the Codex files, with their entitlements | ARCHITECTURE §3 |

In the draft 4.0.0 release target it owns criterion 7 (the final candidate with verified resource, profile and supplier identity, signed, notarised, stapled and launched from a quarantined install), criterion 8 (the terms position) and criterion 9's statement of limitations, supplies the notices of criterion 6, and supplies the signed installed identity and the entitlements that the keychain protection of criterion 4 relies on. The target is version 4.0.0 on macOS on Apple Silicon, minimum macOS 15, bundle identifier `com.chirality.app`.

## Deliverable Definition — Ontology

- **OUT-001** — The packaging, signing and notarisation configuration and tools that produce the package from a candidate, including the notices shipped in it. Supports SOW-098, SOW-134; OBJ-002.
- **OUT-002** — The package identity record for each package. Supports SOW-098, SOW-134; OBJ-002.
- **OUT-003** — The install-and-launch witness of each package offered for examination or release. Supports SOW-098, SOW-134; OBJ-002.
- **OUT-004** — The terms position: the supplier's written position on the offering, held with its source and the owner's reading of its applicability, and the limitations stated with the release. Supports SOW-117; OBJ-002.

Terms:

- **Candidate.** One identified build: an App source revision, a build identity and the supplier pin.
- **Vendor tree.** The complete Codex distribution at the pin as the supplier publishes it. It ships byte for byte at `Contents/Resources/codex/` inside the bundle, and the App launches `bin/codex` in it directly; it is not renamed, repacked or wrapped.
- **Signing arrangement.** Every file of the vendor tree keeps the supplier's signature and entitlements. Only the App's own code is signed, with the owner's Developer ID, hardened runtime and a secure timestamp, and without signing into the vendor tree. The whole bundle is notarised and the ticket stapled. The App Sandbox is off, because the App starts Codex and Codex runs its own command sandbox.
- **Publisher identity.** The owner's Developer ID team together with the bundle identifier. It is the same in every release.
- **Package identity record.** For one package: its file name and hash; the candidate; the bundle identifier, version and minimum macOS; the inventory of the packaged vendor tree; the inventory of each bundled resource (the workflows with their shipped-revision list, the guidance, the role files and the role set); for each signed executable its signer and entitlements as read from the package; the App ID, team and allowed entitlements of any provisioning profile in the bundle; the notarisation result; and what was not observed.
- **Install-and-launch witness.** An observation, on macOS on Apple Silicon, of the package downloaded with its quarantine mark, assessed by the operating system, installed and launched, through to a Codex child reported ready and verified.
- **Notice.** The licence text of a shipped component with the component, version and source it belongs to.
- **Offering.** What the owner distributes: a free, locally run, open-source App that uses the supplier's current sign-in flow.
- **Terms position.** A supplier's written position on distributing the offering, as an identified official publication or a direct response.

Boundary:

- **CLM-001** — `DEL-01-01` owns the pin, the expected inventory of the vendor tree and the check an installed App makes of its own Codex before running it. This deliverable puts the tree in the package unchanged and signs the App with the publisher identity that check is compiled to expect. PKG-09 examines the packaged candidate as a whole; the package's own checks stay here.
- **CLM-002** — Re-signing the supplier's files is not part of the signing arrangement. If a pin cannot be notarised or launched with the supplier's signatures in place, the question returns to the owner.
- **CLM-003** — The supplier writes its position. The owner obtains it, decides whether it applies to the offering, and separately decides on public distribution; that decision is not made here and nothing in this deliverable stands for it. The position applies only while the offering and the stock sign-in flow are unchanged, and does not cover a commercial or hosted offering. A position for another supplier's sign-in is needed only if the App comes to offer that sign-in. Owner use and development do not wait on any of this.
- **CLM-004** — The bundled workflows and the bundled role guidance are build inputs from `DEL-02-02` and `DEL-02-04`; their content is theirs. The SWBPIPE host is built and packaged by its own owner; neither package qualifies the other.

## Completion and Reliance Basis — Epistemology

- **REQ-001** — The package targets macOS on Apple Silicon at the stated minimum version, identifies its candidate, and contains the vendor tree of that candidate's pin byte for byte. The bundled workflows with their shipped-revision list, the default guidance, the role files and the role set are packaged byte for byte as `DEL-02-02` and `DEL-02-04` supply them for the candidate. Nothing is written into the bundle after it is signed, at build time or at run time.
- **REQ-002** — The package is signed under the signing arrangement with the publisher identity, notarised and stapled. Each entitlement a named App feature needs is present on the App's own code, and no other entitlement is present; for 4.0.0 this includes what keychain protection (`DEL-01-04`) needs. A provisioning profile in the bundle is identified by its App ID and team, which are those of the publisher identity, and allows every entitlement on the App's own code. Each package has a package identity record read from the package itself.
- **REQ-003** — Each package offered for examination or release has an install-and-launch witness that names the package by hash and distinguishes what was observed from what was not. A browser or development run is not a witness.
- **REQ-004** — Before public release beyond owner use, the terms position for the offering is held with the exact publication or response, its supplier, its dates, where it is kept, its conditions and exclusions, and the owner's statement of whether it applies. Either an official publication or a direct response serves; a product-specific reply is not required when an applicable publication is held. A missing position or an unstated applicability reads as unresolved.
- **REQ-005** — This deliverable performs no act that CLM-001, CLM-003 and CLM-004 give elsewhere: it defines no pin, qualifies no protocol, writes no supplier position, makes no distribution decision and authors no bundled content.
- **REQ-006** — Every component shipped in the package has its notice in the package: the supplier's Codex and the components inside it, the App's own compiled and bundled dependencies, and bundled fonts and assets. A component whose notice cannot be established is named as uncovered, and the package is not offered for public release while one remains.
- **REQ-007** — Every limitation the owner accepted for the release is stated with it. For 4.0.0, rotation of the capture-seal key is unavailable, and the release says so.

- **AC-001** — The package's bundle declares the stated target, identifier and version; the inventory of its vendor tree equals the expected inventory for the pin; the inventory of each bundled resource equals the inventory of the input its supplier maintains; and the bundle read after a run equals the bundle as signed. Verify by VER-001. [REQ-001]
- **AC-002** — Every file of the packaged vendor tree carries the supplier's signature and the supplier's entitlements unchanged; the App's own code carries the publisher identity, hardened runtime and a timestamp, with no debugging entitlement; the entitlements on the App's own code equal the set its named features need, including what keychain protection needs; a provisioning profile in the bundle names the publisher identity's App ID and team and allows those entitlements; the notarisation ticket is stapled; and the package identity record states the same facts as an independent reading of the package. Verify by VER-002. [REQ-001, REQ-002]
- **AC-003** — From a quarantined download, the operating system accepts the package without an override, the App installs and launches, and a Codex child reaches ready and is reported verified; the witness names the package hash, the macOS version and the machine architecture. A changed package has no witness until it is witnessed again. Verify by VER-003. [REQ-003]
- **AC-004** — The held terms position reproduces the supplier's publication or response exactly, names its source and dates, and carries the owner's applicability statement for the offering; with either missing it reads as unresolved. The candidate's offering and sign-in flow are the ones the applicability statement covers; a changed offering or sign-in flow reads as unresolved. Verify by VER-004. [REQ-004]
- **AC-005** — The terms record keeps the supplier's position, the owner's obtaining and applicability statement, and the owner's distribution decision as three separate things, the last shown as made or not made by the owner alone; no package result or recorder's statement appears as any of them. Verify by VER-004. [REQ-004, REQ-005]
- **AC-006** — None of the acts in REQ-005 is produced by this deliverable's code or records, and no result here is presented as Windows support, as a qualification of the SWBPIPE host, or as the joined examination of the candidate. Verify by VER-005. [REQ-005]
- **AC-007** — For the package, every component found in it by reading the package has a notice whose text equals the component's own published licence, or is named as uncovered. Verify by VER-006. [REQ-006]
- **AC-008** — The material a person receives with the package lists every limitation the owner accepted for the release, including that key rotation is unavailable. Verify by VER-007. [REQ-007]

## Production and Verification Method — Praxeology

A package is produced from one candidate in a fixed order: the vendor tree is placed unchanged, the App's own code is built with the publisher identity compiled in, notices are assembled, the App's code is signed, the bundle is notarised and stapled, and the identity record is read from the result. Signing and notarisation use the owner's credentials through the operating system's keychain; no credential is an input to a tool or appears in a record. Checks on configuration and records run without a signed package; signing, notarisation and the witness each need the actual package.

- **VER-001** — Comparison with `DEL-01-01`'s expected inventory for the pin: inventory the packaged vendor tree, compare each bundled resource with the source `DEL-02-02` and `DEL-02-04` maintain for the candidate, read the bundle's declared target, identifier and version, and compare the bundle before and after a run.
- **VER-002** — Comparison with the operating system's own signature, entitlement and notarisation reports: read each signed executable of the package and its stapled ticket with the system tools, compare the supplier's files with the supplier's published signatures, compare the App's entitlements with what each named feature's scope states it needs, decode any embedded provisioning profile and compare its App ID, team and allowed entitlements with the App's signature, and compare the package identity record with that reading.
- **VER-003** — Judgment by an examiner, with the operating system's assessment: download the package so that it carries a quarantine mark, let the system assess it, install, launch, and observe the Codex child's readiness and verification result.
- **VER-004** — Comparison with the supplier's publication at its source: compare the held text, source and dates with the publication or response, and read the applicability statement against the offering and the sign-in flow the candidate actually uses.
- **VER-005** — Judgment by an independent reviewer: trace each act of REQ-005 to its owner, and read the package's results for claims they do not support.
- **VER-006** — Comparison with each component's own published licence: list the components by reading the package and the dependency lists it was built from, and compare each shipped notice with the licence its publisher distributes for that version.
- **VER-007** — Comparison with the limitations the owner accepted for the release: read the limitation text in the material shipped with the package against each accepted limitation.

## Governing Values and Decisions — Axiology

- **AX-001** — What is shipped is what was identified. Better means more of the package read back from the package itself and tied to its candidate, and never by carrying a result over from an earlier package, a development run, a browser build or another project's package.
- **AX-002** — The supplier's Codex reaches the person as the supplier made it. Better means fewer steps between the supplier's publication and the installed tree, and never by altering, re-signing or wrapping the supplier's files to make a build pass.
- **AX-003** — A package result, a supplier's position and the owner's decision are different facts. Better means each is shown with who made it, and never by letting one stand for another or by reading a supplier's publication as approval of this product.
- **TBD-004** — The 4.0.0 release target is a draft. Its minimum macOS version and its list of limitations are working values until the owner accepts it.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-002 | REQ-001, CLM-001 | AC-001 | VER-001 | Outside source: the supplier's published distribution at the pin, through the expected inventory built from it. Bundled resources are compared with the supplying deliverables' maintained sources, which the packaging step did not write. The target values are the owner's, from the release target. |
| OUT-002 | OBJ-002 | REQ-001, REQ-002, CLM-002 | AC-002 | VER-002 | Outside source: the operating system's signature, entitlement and notarisation reports, its decoding of the Apple-issued provisioning profile, and the supplier's published signatures. The set of needed entitlements is what each named feature's own scope states, `DEL-01-04` for keychain protection. |
| OUT-003 | OBJ-002 | REQ-003, CLM-001 | AC-003 | VER-003 | Outside source: the operating system's assessment of a quarantined download and an examiner's observation. The verified result shown is the App's own report; its independent ground is the reading of VER-002. |
| OUT-004 | OBJ-002 | REQ-004, CLM-003 | AC-004 | VER-004 | Outside source: the supplier's official publication or direct response. Owner ruling for its applicability. |
| OUT-004 | OBJ-002 | REQ-004, REQ-005, CLM-003 | AC-005 | VER-004 | Owner ruling: PRD OQ-08 keeps the supplier's position and the owner's distribution decision apart. |
| OUT-002 | OBJ-002 | REQ-005, CLM-001, CLM-003, CLM-004 | AC-006 | VER-005 | Owner ruling: the accepted decomposition's allocation of each act and PRD V4-CST-02 for the target. |
| OUT-001 | OBJ-002 | REQ-006 | AC-007 | VER-006 | Outside source: each component's licence as its publisher distributes it. The component list is read from the package under examination. |
| OUT-004 | OBJ-002 | REQ-007 | AC-008 | VER-007 | Owner ruling: each accepted limitation, including key rotation left unavailable for 4.0.0. |
