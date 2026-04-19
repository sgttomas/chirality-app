# Plan: Decomposition Package Normalization

## Context

The two live West Doe `DOMAIN` roots currently use materially different decomposition package shapes.

`West_Doe_Comp_and_Liquids_DBM` is already close to a modular authoritative package:
- a relatively compact main decomposition markdown
- companion annex CSVs that hold the heavy machine-truth
- `_ScopeChange` snapshots and `_LATEST.md` that govern amendment state

`West_Doe_Deepcut_DBM` is much more monolithic:
- a very large main decomposition markdown with embedded ledger-heavy and publication-facing sections
- companion registers that exist, but the main `.md` still carries a large amount of the same package truth inline
- final-package wording that treats the monolithic document as a publication candidate rather than just a working control surface

The live package sizes make the mismatch concrete:
- `West_Doe_Comp_and_Liquids_DBM/_Decomposition/WEST_DOE_DOMAIN_DECOMPOSITION.md`
  - `1,520` lines / `272,958` bytes
- `West_Doe_Deepcut_DBM/_Decomposition/DeepCut_DOMAIN_DECOMP_FINAL_v4.md`
  - `144,611` lines / `5,214,485` bytes

The underlying domain size also differs, but that is not the full explanation:
- Comp & Liquids telemetry currently reports `321` units, `85 active` KTYs, and `274` subjects
- Deepcut telemetry currently reports `5,692` units, `98` KTYs, and `434` subjects

The normalization problem is therefore not only “Deepcut has more content.” It is also “Deepcut packages its content in a much more monolithic way.”

---

## Recommendation

Normalize both roots toward a **modular authoritative decomposition package**.

That means:
- the **canonical working package** is a compact main decomposition document plus companion registers / annexes and `_ScopeChange`
- the **monolithic full-package render**, if still desired, becomes a **derived publication artifact**
- agents and amendment workflows operate primarily on the modular package, not on a monolithic embedded-ledger document

This plan recommends moving **Deepcut toward the current Comp & Liquids shape**, not moving Comp & Liquids toward the Deepcut monolith.

---

## Why This Is The Preferred Shape

### Agent workflow benefits

For agents, the modular package is preferable because:
- retrieval is more targeted
- edits touch smaller authoritative surfaces
- parity failures are easier to localize
- diffs are narrower and easier to review
- `SCOPE_CHANGE` propagation is more controlled
- package-review and audit workflows can reason explicitly about duplicated truth instead of parsing a massive embedded document

### Governance fit

The repository now has the governance needed to support modular packages safely:
- `AGENT_SCOPE_CHANGE.md` now treats decomposition-local truth and snapshot integrity explicitly
- `AGENT_AUDIT_DECOMP.md` now audits derivative parity, snapshot completeness, and handoff-state consistency
- `decomposition-package-review` exists to review package parity as a closed system
- `kty-metadata-align` exists to keep KTY metadata drift separate from content regeneration

Because those controls now exist, a monolithic main decomposition document is no longer needed as a crutch for package coherence.

### Publication separation

If humans still want a single-file review or publication artifact, that is compatible with this plan. The key rule is:

- **single-file monoliths may exist as derived outputs**
- **they should not be the authoritative amendment surface**

---

## Scope Of This Plan

This plan is not limited to the two West Doe roots. It also defines the contract-tightening work required across the decomposition agent family so future decompositions are created in the preferred modular format by default.

The implementation scope therefore includes:
- `agents/AGENT_DECOMP_BASE.md`
- `agents/AGENT_PROJECT_DECOMP.md`
- `agents/AGENT_SOFTWARE_DECOMP.md`
- `agents/AGENT_DOMAIN_DECOMP.md`
- `agents/AGENT_SCOPE_CHANGE.md`
- `agents/AGENT_AUDIT_DECOMP.md`
- decomposition-adjacent skills and tools that govern package review, metadata alignment, auditability, and any future derived publication rendering path

The normalization target is:
- **modular authoritative package by default**
- **derived monolithic render only when explicitly needed**
- **package-role labeling made explicit in every decomposition workflow**

---

## Target Architecture

### 1. Canonical working package

Every `DOMAIN` root should converge on this authoritative package model:

- one concise main decomposition markdown
- companion CSV / JSON / markdown registers for heavy machine-truth
- `_ScopeChange/_LATEST.md`
- active `_ScopeChange` snapshot with complete handoff-state artifacts

This same architectural principle should also be made explicit for `PROJECT` and `SOFTWARE` variants:
- the decomposition document remains the canonical working surface
- heavy machine-truth belongs in companion ledgers/registers when present
- publication or review bundles are derived outputs, not the root amendment surface

### 2. Main decomposition document

The main decomposition document should contain:
- status / revision / references
- objective table
- vocabulary highlights or canonical summary
- category summary
- structured domain outline
- knowledge type summary
- knowledge subject summary
- high-level telemetry
- open-issue summary
- decision log / change log
- annex or companion inventory

The main document should not embed:
- the full ledger as the primary working truth
- exhaustive derivative tables when the same truth already exists in companion files
- publication-manifest-style bulk appendices unless explicitly generated as a derived artifact

### 3. Companion authoritative registers

Heavy package truth should live in companion files such as:
- domain ledger
- category register / telemetry
- knowledge type register
- knowledge subject register
- objective register / objective mappings
- open issues
- validation checks
- scope-boundary or standalone-subject derivatives where relevant
- node summary / coverage telemetry
- vocabulary map

### 4. Optional derived monolithic render

If a single-file human-readable package is still useful, create a derived render that:
- assembles the main document and companion surfaces
- is publication-oriented
- is explicitly marked non-authoritative for amendment work
- can be regenerated deterministically from the modular package

---

## Normalization Rules

### Rule 1. The modular package is authoritative

For `DOMAIN`, authoritative amendment surfaces should be:
- main decomposition markdown
- decomposition-local companion registers
- `_ScopeChange/_LATEST.md`
- active `_ScopeChange` snapshot artifacts

### Rule 2. Monolithic renders are derived

A full-package monolithic markdown or publication render may be produced, but it must be treated as:
- derived
- replaceable
- not the primary amendment surface

### Rule 3. Duplicate truth must be justified

If a truth surface is duplicated both in the main decomposition document and in a companion register:
- the duplication must be intentional
- the companion register remains authoritative for machine-truth unless explicitly documented otherwise
- `decomposition-package-review` and `AUDIT_DECOMP` must verify parity

### Rule 4. Package role must be explicit

Every major decomposition artifact should declare its role:
- `authoritative working surface`
- `authoritative companion register`
- `derived publication artifact`
- `snapshot/handoff artifact`

### Rule 5. Publication needs a separate artifact model

Do not overload the main working decomposition document with publication concerns. If publication needs:
- manifest views
- embedded ledger tables
- single-file review bundles

those should be generated into a publication-oriented artifact family rather than permanently embedded into the live working surface.

### Rule 6. Decomposition agents must emit package-role clarity

Every decomposition workflow must explicitly identify:
- the canonical working package
- any authoritative companion registers
- any snapshot / handoff artifacts
- any derived publication artifact families

This must be true at the agent-contract level, not only in project-specific plans.

### Rule 7. New decompositions must default to modular form

Future decomposition runs must not silently fall back to monolithic package shapes for convenience.

If a decomposition variant wants a monolithic publication render, it must:
- declare that render as derived
- keep the modular package authoritative
- define the render path separately from the working package contract

### Rule 8. Audit and amendment contracts must enforce the preferred shape

`SCOPE_CHANGE` and `AUDIT_DECOMP` must be able to distinguish:
- authoritative working surfaces
- authoritative companion registers
- derived publication artifacts
- historical residue

If a package blurs those roles, the audit and amendment workflows should surface that ambiguity as a contract defect rather than accept it as normal background structure.

---

## DECOMP Agent Contract Tightening

The preferred package shape will not remain stable unless the decomposition family itself is tightened. The following contract updates are required.

### `AGENT_DECOMP_BASE.md`

Add decomposition-family-wide rules that:
- define `canonical working package` as the normative decomposition output model
- define `authoritative companion register` as a first-class concept, not a variant-specific afterthought
- define `derived publication artifact` as a distinct artifact role
- require every conforming decomposition agent to declare which package surfaces are authoritative versus derived
- discourage embedding heavy derivative truth in the main decomposition document when a companion register is the better working surface

`DECOMP_BASE` should become the place where “modular by default” is stated once for the whole family.

### `AGENT_DOMAIN_DECOMP.md`

Update `DOMAIN_DECOMP` so it explicitly targets:
- one concise main decomposition document
- decomposition-local companion registers / annexes for heavy machine-truth
- optional derived monolithic publication render only when required

Required clarifications:
- the main decomposition document is a control surface, not a permanent full-ledger dump
- heavy package truth such as ledgers, telemetry, objective mappings, and equivalent derivative surfaces may live in companion files
- the agent must emit a companion inventory section so downstream agents can discover the package layout quickly

### `AGENT_PROJECT_DECOMP.md`

Tighten `PROJECT_DECOMP` so the same package-role language is explicit even if current project decompositions are already smaller.

Required clarifications:
- decomposition truth vs derivative review/publication bundle separation
- when ledgers/registers should be emitted as companion surfaces
- prohibition on mixing publication-style bundle assembly into the working decomposition contract

The goal is consistency across variants, not only fixing `DOMAIN`.

### `AGENT_SOFTWARE_DECOMP.md`

Apply the same separation rules to software decomposition:
- keep the working decomposition document authoritative
- define any future derived reporting/publication bundle separately
- prevent monolithic “everything embedded in one markdown” drift if software decomposition grows more companion analysis surfaces over time

### `AGENT_SCOPE_CHANGE.md`

This file already moved in the right direction, but the normalization plan should require one more step:
- `SCOPE_CHANGE` must classify every touched surface by package role
- amendments must operate on the authoritative modular package
- derived publication artifacts must never be treated as the default amendment target
- Gate 4 / Gate 5 wording should remain explicit about direct package writes vs derived downstream regeneration

### `AGENT_AUDIT_DECOMP.md`

Tighten the audit so it judges package-shape conformance, not only parity:
- does the package clearly label authoritative vs derived surfaces?
- does the main decomposition document duplicate heavy companion truth unnecessarily?
- is any derived monolithic artifact being treated as if it were authoritative?
- are package roles discoverable enough for future agents to amend the root safely?

`AUDIT_DECOMP` should be the enforcement point for future drift away from the preferred package shape.

---

## Skills And Tools To Align

The plan should also tighten associated skills and tools so the normalized package shape persists operationally.

### `decomposition-package-review`

Extend the skill contract so it explicitly reviews:
- package-role labeling
- whether the main document is overly monolithic relative to companion truth
- whether any companion register should be promoted or demoted in package authority
- whether derived publication artifacts are being confused with working truth

### `kty-metadata-align`

No role expansion is needed, but the plan should state that this skill remains downstream and KTY-local only. It must not become a loophole for compensating for poor decomposition package structure.

### `domain-documents`

Keep it metadata-immutable and content-focused. The normalization plan should explicitly state that `domain-documents` is not responsible for fixing decomposition package shape and must not be overloaded with package-governance concerns.

### Future derived-render tool or publication assembler

If the repo keeps or adds a tool that assembles a monolithic decomposition render:
- the tool must mark its output as derived
- the render path must be deterministic from the modular package
- the render must not silently become the amendment surface for future scope changes

### Validators and review utilities

Any future validator or helper that inspects decomposition packages should adopt the same role vocabulary:
- working surface
- authoritative companion
- snapshot/handoff artifact
- derived publication artifact

That vocabulary should remain consistent across tools, skills, and agent instructions.

---

## Root-Specific Direction

### Comp & Liquids

Comp & Liquids is already near the target shape.

Recommended action:
- preserve its general package structure
- continue treating annex CSVs as decomposition-local authoritative detail
- keep the main document concise
- avoid re-monolithizing it for convenience
- add only minimal improvements where parity or inventory clarity is needed

Comp & Liquids should be treated as the preferred working-package baseline for future `DOMAIN` roots.

### Deepcut

Deepcut should be migrated toward the Comp & Liquids model over time.

Recommended action:
- retain the existing companion registers as authoritative machine-truth
- slim down `DeepCut_DOMAIN_DECOMP_FINAL_v4.md`
- remove embedded heavy appendix behavior from the main working document
- preserve any single-file publication need via a derived render or publication-oriented package

The Deepcut migration should not be one giant rewrite. It should be phased and governed so parity is never lost during the transition.

---

## Implementation Phases

### Phase 1. Tighten the decomposition-family contract

Update the decomposition family first so future packages default to the preferred shape:
- `AGENT_DECOMP_BASE.md`
- `AGENT_PROJECT_DECOMP.md`
- `AGENT_SOFTWARE_DECOMP.md`
- `AGENT_DOMAIN_DECOMP.md`

Required contract additions:
- define `canonical working package`
- define `authoritative companion register`
- define `derived publication artifact`
- require explicit package-role labeling in decomposition outputs
- make modular working packages the preferred default across variants

### Phase 2. Tighten amendment and audit governance

Update the relevant governance docs so the target package shape is explicit:
- `AGENT_SCOPE_CHANGE.md`
- `AGENT_AUDIT_DECOMP.md`
- `AGENT_DBM_PUBLISHER.md`
- `WEST_DOE_EXECUTION_MODEL.md`
- `WEST_DOE_TWO_ROOT_DBM_REMEDIATION_AND_PUBLICATION_PLAN.md`

Required contract additions:
- define “canonical working package” vs “derived publication artifact”
- define the authoritative role of companion registers
- require publication flows to consume closure evidence from the modular package, not just a monolithic main doc

### Phase 3. Align decomposition-adjacent skills and tools

Update the relevant skills and any associated render/review tools so the preferred package shape is operationally enforced:
- `decomposition-package-review`
- `kty-metadata-align`
- `domain-documents`
- any future or existing derived-render / publication assembly toolchain that consumes decomposition packages

Required updates:
- package-role terminology stays consistent with the agent docs
- review skills can identify monolithic drift
- content-generation skills do not absorb package-governance responsibilities
- derived-render tools mark their outputs as derived and non-authoritative

### Phase 4. Inventory duplicated Deepcut truth

Run a focused Deepcut package analysis to classify every major surface as:
- `AUTHORITATIVE_MAIN_DOC`
- `AUTHORITATIVE_COMPANION`
- `DERIVED_PUBLICATION`
- `SNAPSHOT_HANDOFF`
- `HISTORICAL_RESIDUE`

This pass must identify:
- which embedded sections in `DeepCut_DOMAIN_DECOMP_FINAL_v4.md` are still needed in the working document
- which sections are just duplicated companion truth
- which sections are publication-only

### Phase 5. Slim Deepcut main decomposition

Revise the Deepcut main decomposition document so it converges toward the normalized working shape.

Target removals or reductions:
- embedded full-ledger style sections
- oversized appendix-style derivative content
- publication-manifest heavy sections that duplicate companion truth

Target retained sections:
- status / references / revision notes
- objectives
- vocabulary summary
- category summary
- structured domain outline
- type summary
- subject summary
- top-level telemetry
- open-issue summary
- decision/change summary
- companion artifact inventory

### Phase 6. Add a derived monolithic render path if still needed

If the project still wants a single-file Deepcut package for review or publication:
- define a deterministic render path from the modular package
- place the output in a clearly publication-oriented location
- mark it non-authoritative for amendment work

If the repo already has suitable publication machinery, reuse it rather than inventing a second monolith workflow.

### Phase 7. Normalize package-role labeling across both roots

Update both roots so the package-role labels are consistent:
- main doc role
- companion register role
- snapshot role
- derived publication artifact role

This should include companion inventories in the main decomposition docs so agents can discover the package layout quickly.

### Phase 8. Verify parity and workflow behavior

After Deepcut is slimmed and package roles are explicit:
- run `decomposition-package-review`
- run `AUDIT_DECOMP`
- verify `SCOPE_CHANGE` can amend the root without reintroducing monolithic drift
- verify DBM publication can consume the modular package without needing the working document to carry the full ledger inline

---

## Required Governance Changes

### `AGENT_DECOMP_BASE.md`

Add family-level structure so the preferred package format is normative for all future decomposition variants, not just a recommendation for one root.

### `AGENT_SCOPE_CHANGE.md`

Add or tighten language so:
- the full decomposition package is the amendment unit, not just the main markdown
- derived publication artifacts are not mistaken for authoritative working surfaces
- Gate 4 / Gate 5 direct-write lanes distinguish clearly between authoritative package edits and derived-artifact regeneration

### `AGENT_AUDIT_DECOMP.md`

Ensure the audit explicitly checks:
- package-role consistency
- parity between main doc and companion registers
- whether any oversized main-doc section is duplicating companion truth without clear authority
- whether derived publication artifacts are incorrectly being treated as amendment truth

### `AGENT_DBM_PUBLISHER.md`

Revise publication admission so it consumes:
- modular package closure state
- handoff-state evidence
- audit evidence

and not merely a monolithic “final” markdown.

### `AGENT_PROJECT_DECOMP.md`, `AGENT_SOFTWARE_DECOMP.md`, `AGENT_DOMAIN_DECOMP.md`

Make the output package shape explicit in each conforming decomposition agent:
- what belongs in the main doc
- what belongs in companion registers
- what may exist as a derived publication artifact
- how package-role labeling is surfaced to downstream agents

### `decomposition-package-review`

Extend the skill guidance so package-role classification is part of the review method:
- authoritative working doc
- authoritative companion
- derived publication
- historical residue

---

## Non-Goals

This plan does not recommend:
- collapsing companion registers back into the main document
- making Comp & Liquids more monolithic
- removing companion registers in favor of one giant markdown
- rewriting DBM publication as a single-file-only workflow
- changing underlying domain truth just to make the two roots superficially equal in size

The goal is package-shape normalization, not forced content homogenization.

---

## Verification

Normalization is complete only when all of the following are true:

1. Both roots expose a clear modular authoritative package:
   - main doc
   - companion registers
   - `_ScopeChange` state

2. The main decomposition documents are concise control surfaces rather than mixed control-surface-plus-ledger monoliths.

3. Any monolithic full-package render is clearly labeled as derived and non-authoritative for amendment work.

4. `SCOPE_CHANGE` can amend either root by editing the modular package without relying on embedded full-ledger sections in the main doc.

5. `AUDIT_DECOMP` and `decomposition-package-review` can validate the package without ambiguity about which surface is authoritative.

6. `DBM_PUBLISHER` can admit a root using modular package closure evidence and does not require a monolithic main decomposition document as its de facto source of truth.

7. New decomposition runs through `PROJECT_DECOMP`, `SOFTWARE_DECOMP`, and `DOMAIN_DECOMP` default to the preferred modular package format unless a variant-specific exception is explicitly approved and documented.

---

## Assumptions

- The preferred long-term `DOMAIN` package baseline is the current Comp & Liquids shape, not the current Deepcut monolith.
- Publication may still benefit from single-file artifacts, but those should be derived from the modular package.
- Deepcut migration should be phased so existing accepted truth is preserved throughout.
- The goal is to improve agent usability, package maintainability, and auditability at the same time.

---

## Recommended Next Step

Use this plan as the basis for a concrete implementation plan focused on Deepcut migration first:
- classify Deepcut package roles
- define which main-doc sections become companion-authoritative only
- specify the derived monolithic render path, if retained
- update governance docs so the normalized package contract becomes the standard for future `DOMAIN` roots

That implementation plan should be written and approved before any live Deepcut decomposition slimming begins.
