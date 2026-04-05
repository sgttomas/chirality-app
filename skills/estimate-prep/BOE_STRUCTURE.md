# BOE Structure — Document Contracts

Companion reference for `skills/estimate-prep/SKILL.md`. Defines the structural contracts for the Basis-of-Estimate artifacts produced by the two phases.

---

## BOE_Scaffold.md (Phase SCAFFOLD output)

Produced by Phase SCAFFOLD under `{snapshot}/Scaffold/BOE_Scaffold.md`.

### Minimum contents

- **Per-deliverable table** with columns:
  - `DeliverableID`
  - `Name`
  - `Package`
  - `BASIS_OF_ESTIMATE`
  - `FALLBACK_POLICY`
  - `ALLOW_MIXED`
  - `Substance`
  - `Cost Drivers`
  - `Primary Roles`
- **Package cost ownership hints** (scope items mapped to multiple deliverables)
- **SOW multi-mapping warnings** (double-counting risks)
- Marked `DRAFT — requires human review`

---

## BASIS_OF_ESTIMATE.md (Phase BOE output)

Produced by Phase BOE as `{snapshot}/BASIS_OF_ESTIMATE.md`.

If a canonical BOE exists for the project, follow its structure. Otherwise, the generated BOE MUST include these 10 sections in order:

1. **Purpose**
2. **Project Context**
3. **Estimation Scope** (in/out; base/options)
4. **Estimation Strategy** (methods, defaults, price source posture)
5. **Per-Deliverable Estimation Plan** (tiers, basis, fallback, mixed methods, cost drivers, ownership rules)
6. **Dependency-Informed Run Sequence** (tiers + chains + gates)
7. **Missing / Weak PRICE_SOURCES Register**
8. **Aggregation Strategy** (rollups; totals; optional evaluation view)
9. **Assumptions and Constraints Log**
10. **Document Control**

### Section guidance

- **Per-Deliverable Plan (§5):** every deliverable from the decomposition MUST appear. Record cost ownership rules for every package with multi-deliverable scope overlap.
- **Run Sequence (§6):** every deliverable assigned a tier; tier assignments consistent with dependencies; cycles detected and reported in QA + Conflicts.
- **PRICE_SOURCES Register (§7):** identify and prioritize low-confidence items impacting the plan.
- **Assumptions Log (§9):** merge scaffold assumptions + BOE derivations with IDs and impact-if-wrong.

---

## Run_Context.md (minimum fields — both phases)

Produced at the root of every snapshot folder.

- `RunID` (snapshot folder name)
- `AsOf` (timestamp)
- `Phase` (`SCAFFOLD` | `BOE`)
- `Mode` (`BOOTSTRAP` | `ENRICH`)
- `EXECUTION_ROOT`
- `DECOMPOSITION_PATH`
- `SOURCE_DOCUMENTS` (resolved list)
- `PROJECT_CONTEXT` (full block)
- `CURRENCY`
- `RATE_SCOPE` (SCAFFOLD only)
- `SCAFFOLD_PATH` (BOE only)
- `DEPENDENCY_SOURCES` (BOE only)
- `HUMAN_PRICING` (ENRICH mode only)
- `PRIOR_SNAPSHOT` (ENRICH mode only)
- `CANONICAL_PRICESOURCES_ROOT` (if used)
- `SCHEMA_MODE`
- `EXPORT_BUNDLE`
- `Warnings` (if any)

---

## Publish_Manifest.md (handoff artifact — human-owned action)

Produced at `{snapshot}/Publish_Manifest.md` at the end of every run. Describes how to publish snapshot outputs to canonical locations — **publication is a human-owned step**.

### Required contents

- **Snapshot path** (absolute or relative to `{EXECUTION_ROOT}`)
- **Intended canonical destinations** (e.g., `{EXECUTION_ROOT}/_PriceSources/` and `{EXECUTION_ROOT}/BASIS_OF_ESTIMATE.md`)
- **File-by-file copy list**
- **Warning** that publication requires human approval and review

If `Publish_Package/` exists (i.e., `EXPORT_BUNDLE=MANIFEST_AND_PACKAGE`), the manifest should point to it.

### Human decision rights boundary

The manifest is a proposal. The skill MUST NOT:
- Copy files into `_PriceSources/` or other canonical locations.
- Create or modify `BASIS_OF_ESTIMATE.md` outside the snapshot folder.
- Commit to git or push to any remote.
- Take any irreversible publication action.
