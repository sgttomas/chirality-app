# Decision Log — EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035

## Defaults applied

- Phase: `SCAFFOLD`
- Mode: `BOOTSTRAP`
- Rate scope: `PRODUCTION_AND_CONSTRUCTION`
- Schema mode: `DEFAULT_COMPAT` (Schema Annex; no canonical _PriceSources/ discovered)
- Currency: `CAD`

## Methods used

- Deliverable list + metadata: parsed from per-deliverable `_CONTEXT.md` files (multiple templates supported).
- LOE hours: parametric heuristics by deliverable type/discipline with PM/QC overlays; basis recorded as `PARAMETRIC`.
- Pricing libraries: parametric benchmark placeholders; `Confidence=MEDIUM` by default; `ALLOWANCE/LOW` used where vendor-dependent or scope uncertain.

## Human decisions required (next gate)

- Confirm/adjust floor area and key quantities from drawings.
- Decide whether to estimate design effort via LOE (preferred) vs fee-percent method.
- Provide any vendor quotes (cranes, doors, MUA, electrical service) to upgrade LOW-confidence allowances.
